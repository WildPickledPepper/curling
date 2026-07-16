"use strict";

const fs = require("fs");

const BASE_FRICTION = 0.0010000000474974513;
const STEP = 0.0010000000474974513;
const DT = 0.01;
const STATE_FLOATS = 13;

function loadTrace(eventsPath) {
  for (const line of fs.readFileSync(eventsPath, "utf8").split(/\r?\n/)) {
    if (!line) continue;
    const event = JSON.parse(line);
    if (event.type === "a0.angular_write.last_pre_pcm") {
      const rows = event.data && event.data.a2StaticTrace;
      if (Array.isArray(rows) && rows.length === 1560) return rows;
    }
  }
  throw new Error("missing 1560-row A2 static trace");
}

async function loadMotionOracle(wasmPath) {
  const bytes = fs.readFileSync(wasmPath);
  const { instance } = await WebAssembly.instantiate(bytes, {
    env: { cos: Math.cos, sin: Math.sin, atan: Math.atan, pow: (x, y) => Math.pow(x, y) },
  });
  const view = new DataView(instance.exports.memory.buffer);
  const vectorAddress = 1024;
  const outputAddress = 2048;
  return (friction, vx, vy, angle) => {
    view.setFloat64(vectorAddress, vx, true);
    view.setFloat64(vectorAddress + 8, vy, true);
    instance.exports.newfrictionstep(outputAddress, friction, vectorAddress, angle, STEP, 0);
    return {
      vx: view.getFloat64(outputAddress, true),
      vy: view.getFloat64(outputAddress + 8, true),
      angle: view.getFloat64(outputAddress + 16, true),
    };
  };
}

function maxComponentDelta(actual, expected) {
  let max = 0;
  for (let i = 0; i < actual.length; ++i) max = Math.max(max, Math.abs(actual[i] - expected[i]));
  return max;
}

async function main() {
  const [a19Js, oracleWasm, eventsPath, outputPath] = process.argv.slice(2);
  if (!a19Js || !oracleWasm || !eventsPath || !outputPath) {
    throw new Error("usage: node run_a19_live_feedback.js A19.js MOTION.wasm events.jsonl output.json");
  }
  const rows = loadTrace(eventsPath);
  const createA19Module = require(a19Js);
  const module = await createA19Module({ noInitialRun: false });
  module.cwrap("a19_init", null, [])();
  const motionStep = await loadMotionOracle(oracleWasm);
  const reset = module.cwrap("a19_reset", null, [
    "number", "number", "number", "number", "number", "number", "number",
    "number", "number", "number", "number", "number", "number",
  ]);
  const stepScene = module.cwrap("a19_step", null, ["number", "number", "number", "number"]);
  const getState = module.cwrap("a19_get_state", null, ["number"]);
  const ptr = module._malloc(STATE_FLOATS * 4);
  const readState = () => {
    getState(ptr);
    return Array.from(module.HEAPF32.subarray(ptr >> 2, (ptr >> 2) + STATE_FLOATS));
  };

  // This is the local BESTSHOT release state, not Unity's captured release pose:
  // its Y is the current no-oracle backend's release support height.
  reset(
    -96.85420227050781, 14.419784545898438, 54.174400329589844,
    6.657902673623539e-8, 0, 0, 1,
    3.4000000953674316, 0, 0, 0, 0, 0,
  );

  let maxPositionDelta = 0;
  let maxQuaternionDelta = 0;
  let maxLinearSetterDelta = 0;
  let maxAngularSetterDelta = 0;
  let maxGetterDelta = 0;
  let maxMotionInputDelta = 0;
  let firstSetterDifference = null;
  let firstPoseDifference = null;
  let firstGetterDifference = null;
  let firstMotionInputDifference = null;
  for (let index = 0; index + 1 < rows.length; ++index) {
    const before = readState();
    const expectedGetter = rows[index].scriptGetter;
    const expectedGetterV = expectedGetter.linearVelocity.vector.map(Number);
    const expectedGetterW = expectedGetter.angularVelocity.vector.map(Number);
    const getterDelta = maxComponentDelta(before.slice(7, 10), expectedGetterV);
    const getterAngularDelta = maxComponentDelta(before.slice(10, 13), expectedGetterW);
    const combinedGetterDelta = Math.max(getterDelta, getterAngularDelta);
    maxGetterDelta = Math.max(maxGetterDelta, combinedGetterDelta);
    if (!firstGetterDifference && combinedGetterDelta > 1e-8) {
      firstGetterDifference = {
        index, tickSerial: rows[index].tickSerial,
        linearDelta: before.slice(7, 10).map((value, component) => value - expectedGetterV[component]),
        angularDelta: before.slice(10, 13).map((value, component) => value - expectedGetterW[component]),
      };
    }
    const motionInputDelta = [
      -before[9] - -expectedGetterV[2],
      -before[7] - -expectedGetterV[0],
      before[11] - expectedGetterW[1],
    ];
    const motionInputMax = Math.max(...motionInputDelta.map(Math.abs));
    maxMotionInputDelta = Math.max(maxMotionInputDelta, motionInputMax);
    if (!firstMotionInputDifference && motionInputMax > 1e-8) {
      firstMotionInputDifference = { index, tickSerial: rows[index].tickSerial, delta: motionInputDelta };
    }
    const friction = Math.fround(Math.fround(BASE_FRICTION) + Math.fround(Number(rows[index].frictionNoise)));
    const motion = motionStep(friction, -before[9], -before[7], before[11]);
    const setter = [-motion.vy, 0, -motion.vx];
    const expectedSetter = rows[index].linearSetter.map(Number);
    const linearDelta = maxComponentDelta(setter, expectedSetter);
    const angularDelta = Math.abs(motion.angle - Number(rows[index].setterWy));
    if (!firstSetterDifference && (linearDelta > 1.2e-7 || angularDelta > 1.2e-7)) {
      firstSetterDifference = { index, tickSerial: rows[index].tickSerial, linearDelta, angularDelta };
    }
    stepScene(setter[0], setter[1], setter[2], motion.angle);
    const after = readState();
    const expected = rows[index + 1];
    const positionDelta = maxComponentDelta(after.slice(0, 3), expected.p.map(Number));
    const quaternionDelta = maxComponentDelta(after.slice(3, 7), expected.q.map(Number));
    if (!firstPoseDifference && (positionDelta > 1e-6 || quaternionDelta > 1e-7)) {
      firstPoseDifference = { index: index + 1, tickSerial: expected.tickSerial, positionDelta, quaternionDelta };
    }
    maxPositionDelta = Math.max(maxPositionDelta, positionDelta);
    maxQuaternionDelta = Math.max(maxQuaternionDelta, quaternionDelta);
    maxLinearSetterDelta = Math.max(maxLinearSetterDelta, linearDelta);
    maxAngularSetterDelta = Math.max(maxAngularSetterDelta, angularDelta);
  }
  const finalState = readState();
  module._free(ptr);
  const result = {
    schema: "a19_wasm_live_feedback_v1",
    policy: "No Unity captured linear/angular setters or pose injection after local BESTSHOT release; trace is used only for noise input and acceptance.",
    initialState: "local_bestshot_release",
    steps: rows.length - 1,
    firstSetterDifference,
    firstGetterDifference,
    firstMotionInputDifference,
    firstPoseDifference,
    maxPositionDelta,
    maxQuaternionDelta,
    maxLinearSetterDelta,
    maxAngularSetterDelta,
    maxGetterDelta,
    maxMotionInputDelta,
    finalState,
    unityFinal: { p: rows[1559].p, q: rows[1559].q },
  };
  fs.writeFileSync(outputPath, JSON.stringify(result, null, 2) + "\n");
  process.stdout.write(JSON.stringify(result) + "\n");
}

main().catch((error) => {
  process.stderr.write(`${error.stack || error}\n`);
  process.exitCode = 1;
});
