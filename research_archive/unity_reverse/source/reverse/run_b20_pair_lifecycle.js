"use strict";

const fs = require("fs");
const BASE_FRICTION = 0.0010000000474974513;
const STEP = 0.0010000000474974513;
const STATE_FLOATS = 13;

function loadTrace(eventsPath) {
  for (const line of fs.readFileSync(eventsPath, "utf8").split(/\r?\n/)) {
    if (!line) continue;
    const event = JSON.parse(line);
    if (event.type === "a0.angular_write.last_pre_pcm") {
      const rows = event.data && event.data.a2StaticTrace;
      const tailNoise = event.data.lastTwoFrictionNoises && event.data.lastTwoFrictionNoises.at(-1);
      const tailWrite = event.data.lastAngularWrite;
      // The trace begins at the actual release boundary. Its length varies
      // when the captured run reaches first PCM before the legacy 1560-tick
      // protocol window, so valid non-empty traces must not be discarded.
      if (Array.isArray(rows) && rows.length > 0 && tailNoise && tailWrite) {
        return {
          rows,
          tail: {
            tickSerial: tailWrite.tickSerial,
            frictionNoise: Number(tailNoise.value),
            unityAngularSetter: Number(tailWrite.wy),
          },
        };
      }
    }
  }
  throw new Error("missing 1560-row A2 static trace");
}

function loadFirstUnityPcm(eventsPath) {
  for (const line of fs.readFileSync(eventsPath, "utf8").split(/\r?\n/)) {
    if (!line) continue;
    const event = JSON.parse(line);
    const data = event.data;
    if (event.type !== "physx.native.after" || data?.hook?.name !== "PxcPCMContactConvexConvex") continue;
    const dump = data.extraDumps?.[0];
    const transform0 = dump?.transform0?.decoded;
    const transform1 = dump?.transform1?.decoded;
    if (transform0 && transform1) return { callIndex: data.callIndex, transform0, transform1 };
  }
  throw new Error("missing Unity PCM transform for diagnostic");
}

async function loadMotionOracle(wasmPath) {
  const { instance } = await WebAssembly.instantiate(fs.readFileSync(wasmPath), {
    env: { cos: Math.cos, sin: Math.sin, atan: Math.atan, pow: (x, y) => Math.pow(x, y) },
  });
  const view = new DataView(instance.exports.memory.buffer);
  return (friction, vx, vy, angle) => {
    view.setFloat64(1024, vx, true);
    view.setFloat64(1032, vy, true);
    instance.exports.newfrictionstep(2048, friction, 1024, angle, STEP, 0);
    return { vx: view.getFloat64(2048, true), vy: view.getFloat64(2056, true), angle: view.getFloat64(2064, true) };
  };
}

async function main() {
  const [sceneJs, oracleWasm, eventsPath, outputPath] = process.argv.slice(2);
  if (!sceneJs || !oracleWasm || !eventsPath || !outputPath) {
    throw new Error("usage: node run_b20_pair_lifecycle.js B20.js MOTION.wasm events.jsonl output.json");
  }
  const { rows, tail } = loadTrace(eventsPath);
  const unityFirstPcm = loadFirstUnityPcm(eventsPath);
  const createModule = require(sceneJs);
  const module = await createModule({ noInitialRun: false });
  module.cwrap("a19_init", null, [])();
  const reset = module.cwrap("b20_reset", null, new Array(13).fill("number"));
  const setActiveState = module.cwrap("a19_reset", null, new Array(13).fill("number"));
  const setTargetSimulation = module.cwrap("b20_set_target_simulation", null, ["number"]);
  const setFeatureSeedDiagnostic = module.cwrap("b20_set_feature_seed_diagnostic", null, ["number"]);
  const setMaterialTransitionCurrentPose = module.cwrap("b20_set_material_transition_current_pose", null, ["number"]);
  const getShapeOffsets = module.cwrap("b20_get_shape_offsets", null, ["number"]);
  const step = module.cwrap("b20_step", null, ["number", "number", "number", "number"]);
  const physicsStep = module.cwrap("b20_physics_step", null, []);
  const getState = module.cwrap("b20_get_state", null, ["number", "number"]);
  const getContact = module.cwrap("b20_get_contact", null, ["number"]);
  const getContacts = module.cwrap("b20_get_contacts", null, ["number"]);
  const getNarrowphase = module.cwrap("b20_get_narrowphase", null, ["number"]);
  const motion = await loadMotionOracle(oracleWasm);
  const statePtr = module._malloc(STATE_FLOATS * 4);
  const contactPtr = module._malloc(2 * 4);
  const contactsPtr = module._malloc((1 + 16 * 7) * 4);
  const narrowphasePtr = module._malloc((73 + 4 * 7) * 4);
  const offsetsPtr = module._malloc(4 * 4);
  const readState = (which) => {
    getState(which, statePtr);
    return Array.from(module.HEAPF32.subarray(statePtr >> 2, (statePtr >> 2) + STATE_FLOATS));
  };
  const readContact = () => {
    getContact(contactPtr);
    return Array.from(module.HEAPF32.subarray(contactPtr >> 2, (contactPtr >> 2) + 2));
  };
  const readContacts = () => {
    getContacts(contactsPtr);
    const values = module.HEAPF32.subarray(contactsPtr >> 2, (contactsPtr >> 2) + 1 + 16 * 7);
    const count = values[0];
    const result = [];
    for (let i = 0; i < count; i += 1) {
      const base = 1 + i * 7;
      result.push({ point: Array.from(values.slice(base, base + 3)), normal: Array.from(values.slice(base + 3, base + 6)), separation: values[base + 6] });
    }
    return result;
  };
  const readNarrowphase = () => {
    getNarrowphase(narrowphasePtr);
    const values = module.HEAPF32.subarray(narrowphasePtr >> 2, (narrowphasePtr >> 2) + 73 + 4 * 7);
    if (!values[0]) return null;
    const transform = (offset) => ({ p: Array.from(values.slice(offset, offset + 3)), q: Array.from(values.slice(offset + 3, offset + 7)) });
    const pcmContacts = [];
    for (let index = 0; index < values[38]; index += 1) {
      const base = 39 + index * 7;
      pcmContacts.push({ point: Array.from(values.slice(base, base + 3)), normal: Array.from(values.slice(base + 3, base + 6)), separation: values[base + 6] });
    }
    const sceneDirectContacts = [];
    for (let index = 0; index < values[72]; index += 1) {
      const base = 73 + index * 7;
      sceneDirectContacts.push({ point: Array.from(values.slice(base, base + 3)), normal: Array.from(values.slice(base + 3, base + 6)), separation: values[base + 6] });
    }
    return {
      flags: values[1], statusFlags: values[2], transform0: transform(3), transform1: transform(10),
      frictionPatchCount: values[17], index: values[18], transformCache0: values[19], transformCache1: values[20],
      edgeIndex: values[21], npIndex: values[22], cacheSize: values[23], cachePairData: values[24],
      cacheManifoldFlags: values[25], manifoldHeader: Array.from(values.slice(26, 38)), pcmContacts, sceneDirectContacts,
      narrowPhaseParams: { contactDistance: values[67], meshContactMargin: values[68], toleranceLength: values[69], transformContactDistance0: values[70], transformContactDistance1: values[71] },
    };
  };
  const readShapeOffsets = () => {
    getShapeOffsets(offsetsPtr);
    return Array.from(module.HEAPF32.subarray(offsetsPtr >> 2, (offsetsPtr >> 2) + 4));
  };

  // Local BESTSHOT release. Target placement is protocol input embedded in b20_reset,
  // not a Unity first-PCM pose/cache injection.
  const releaseY = process.env.B20_UNITY_RELEASE_Y === "1"
    ? 14.43239974975586
    : 14.419784545898438;
  reset(-96.85420227050781, releaseY, 54.174400329589844,
    6.657902673623539e-8, 0, 0, 1, 3.4000000953674316, 0, 0, 0, 0, 0);
  if (process.env.B20_DIAGNOSTIC_FEATURE_SEED === "1") setFeatureSeedDiagnostic(1);
  if (process.env.B20_MATERIAL_TRANSITION_CURRENT_POSE === "1") setMaterialTransitionCurrentPose(1);
  if (process.env.B20_TARGET_DISABLED === "1") setTargetSimulation(0);
  const shapeOffsetsAtReset = readShapeOffsets();
  let firstContact = null;
  let firstPoseDifference = null;
  let firstSignificantPoseDifference = null;
  let maxQuaternionDelta = 0;
  let maxPositionDelta = 0;
  const earlyTrace = [];
  let lastActive = readState(0);
  let lastTarget = readState(1);
  for (let index = 0; index < rows.length; index += 1) {
    const before = readState(0);
    const friction = Math.fround(Math.fround(BASE_FRICTION) + Math.fround(Number(rows[index].frictionNoise)));
    const output = motion(friction, -before[9], -before[7], before[11]);
    step(-output.vy, 0, -output.vx, output.angle);
    const contact = readContact();
    lastActive = readState(0);
    lastTarget = readState(1);
    const expected = rows[index + 1];
    if (expected) {
      const positionDelta = Math.max(...lastActive.slice(0, 3).map((value, part) => Math.abs(value - Number(expected.p[part]))));
      const quaternionDelta = Math.max(...lastActive.slice(3, 7).map((value, part) => Math.abs(value - Number(expected.q[part]))));
      maxPositionDelta = Math.max(maxPositionDelta, positionDelta);
      maxQuaternionDelta = Math.max(maxQuaternionDelta, quaternionDelta);
      if (!firstPoseDifference && (positionDelta > 1e-6 || quaternionDelta > 1e-7)) {
        firstPoseDifference = { index: index + 1, tickSerial: expected.tickSerial, positionDelta, quaternionDelta };
      }
      if (!firstSignificantPoseDifference && (positionDelta > 1e-5 || quaternionDelta > 1e-5)) {
        firstSignificantPoseDifference = { index: index + 1, tickSerial: expected.tickSerial, positionDelta, quaternionDelta };
      }
      if (index < 12) earlyTrace.push({ index: index + 1, active: lastActive, expectedP: expected.p, expectedQ: expected.q, positionDelta, quaternionDelta });
    }
    if (contact[0] > 0 && !firstContact) {
      firstContact = {
        index: index + 1,
        tickSerial: rows[index + 1].tickSerial,
        contactCount: contact[0],
        role: contact[1] === 1 ? "active_to_target" : contact[1] === 2 ? "target_to_active" : "unknown",
        contacts: readContacts(),
        narrowphase: readNarrowphase(),
        active: lastActive,
        target: lastTarget,
      };
      break;
    }
  }
  let physicsOnlyTrailingStep = false;
  const postContactPhysics = [];
  let tailScriptStep = null;
  let tailPreStep = null;
  let diagnosticExactPcmInput = null;
  if (!firstContact && process.env.B20_DIAGNOSTIC_EXACT_PCM_INPUT === "1") {
    const unity = loadFirstUnityPcm(eventsPath);
    diagnosticExactPcmInput = unity;
    // Diagnostic only: preserve the B20 actors/pair history, replace just the
    // active actor's next PCM transform, then let the Scene create contacts.
    // This is intentionally excluded from the no-oracle acceptance path.
    setActiveState(
      ...unity.transform0.p, ...unity.transform0.q,
      0, 0, 0, 0, 0, 0,
    );
    physicsStep();
    const contact = readContact();
    lastActive = readState(0);
    lastTarget = readState(1);
    if (contact[0] > 0) {
      firstContact = {
        index: "diagnostic_exact_unity_pcm_input",
        tickSerial: unity.callIndex,
        contactCount: contact[0],
        role: contact[1] === 1 ? "active_to_target" : contact[1] === 2 ? "target_to_active" : "unknown",
        contacts: readContacts(),
        narrowphase: readNarrowphase(),
        active: lastActive,
        target: lastTarget,
      };
    }
  }
  if (!firstContact) {
    const before = readState(0);
    const friction = Math.fround(Math.fround(BASE_FRICTION) + Math.fround(tail.frictionNoise));
    const output = motion(friction, -before[9], -before[7], before[11]);
    tailPreStep = {
      tickSerial: tail.tickSerial,
      localActive: before,
      unityFirstPcmTransform: unityFirstPcm.transform0,
      positionDelta: before.slice(0, 3).map((value, index) => value - Number(unityFirstPcm.transform0.p[index])),
      quaternionDelta: before.slice(3, 7).map((value, index) => value - Number(unityFirstPcm.transform0.q[index])),
    };
    step(-output.vy, 0, -output.vx, output.angle);
    const contact = readContact();
    lastActive = readState(0);
    lastTarget = readState(1);
    tailScriptStep = {
      tickSerial: tail.tickSerial,
      frictionNoise: tail.frictionNoise,
      localLinearSetter: [-output.vy, 0, -output.vx],
      localAngularSetter: output.angle,
      unityAngularSetter: tail.unityAngularSetter,
      angularSetterDelta: output.angle - tail.unityAngularSetter,
    };
    if (contact[0] > 0) {
      firstContact = {
        index: rows.length + 1,
        tickSerial: tail.tickSerial,
        contactCount: contact[0],
        role: contact[1] === 1 ? "active_to_target" : contact[1] === 2 ? "target_to_active" : "unknown",
        contacts: readContacts(),
        narrowphase: readNarrowphase(),
        active: lastActive,
        target: lastTarget,
      };
    }
  }
  if (!firstContact) {
    physicsOnlyTrailingStep = true;
    physicsStep();
    const contact = readContact();
    lastActive = readState(0);
    lastTarget = readState(1);
    if (contact[0] > 0) {
      firstContact = {
        index: rows.length,
        tickSerial: "physics_only_after_a2_trace",
        contactCount: contact[0],
        role: contact[1] === 1 ? "active_to_target" : contact[1] === 2 ? "target_to_active" : "unknown",
        contacts: readContacts(),
        active: lastActive,
        target: lastTarget,
      };
    }
  }
  const extraPhysicsSteps = Number(process.env.B20_EXTRA_PHYSICS_STEPS || 0);
  for (let stepIndex = 0; stepIndex < extraPhysicsSteps; stepIndex += 1) {
    physicsStep();
    const contact = readContact();
    postContactPhysics.push({
      step: stepIndex + 1,
      contactCount: contact[0],
      role: contact[1] === 1 ? "active_to_target" : contact[1] === 2 ? "target_to_active" : "unknown",
      contacts: readContacts(),
      active: readState(0),
      target: readState(1),
    });
  }
  module._free(statePtr);
  module._free(contactPtr);
  module._free(contactsPtr);
  module._free(narrowphasePtr);
  module._free(offsetsPtr);
  const result = {
    schema: "b20_wasm_pair_lifecycle_v1",
    policy: "No Unity first-PCM pose, cache, or setter is injected; Unity trace supplies only friction noise.",
    diagnosticFeatureSeed: process.env.B20_DIAGNOSTIC_FEATURE_SEED === "1",
    materialTransition: process.env.B20_MATERIAL_TRANSITION_CURRENT_POSE === "1" ? "current_pcm_pose" : "predictive_shell",
    lifecycle: process.env.B20_TARGET_DISABLED === "1"
      ? "active eDISABLE_SIMULATION re-enable; target remains no-sim diagnostic control"
      : "target then active eDISABLE_SIMULATION re-enable with persistent PxActor/PxShape",
    releaseY,
    shapeOffsetsAtReset: {
      activeContactOffset: shapeOffsetsAtReset[0], activeRestOffset: shapeOffsetsAtReset[1],
      targetContactOffset: shapeOffsetsAtReset[2], targetRestOffset: shapeOffsetsAtReset[3],
    },
    expected: { role: "active_to_target", contactCount: 2 },
    firstPoseDifference,
    firstSignificantPoseDifference,
    maxPositionDelta,
    maxQuaternionDelta,
    earlyTrace,
    firstContact,
    tailScriptStep,
    tailPreStep,
    diagnosticExactPcmInput,
    physicsOnlyTrailingStep,
    postContactPhysics,
    finalActive: lastActive,
    finalTarget: lastTarget,
  };
  fs.writeFileSync(outputPath, JSON.stringify(result, null, 2) + "\n");
  process.stdout.write(JSON.stringify(result) + "\n");
}

main().catch((error) => { process.stderr.write(`${error.stack || error}\n`); process.exitCode = 1; });
