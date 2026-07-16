"use strict";

const fs = require("fs");
const path = require("path");

const STATE_FLOATS = 13;

function frames(eventsPath) {
  const result = new Map();
  for (const line of fs.readFileSync(eventsPath, "utf8").split(/\r?\n/)) {
    if (!line) continue;
    const event = JSON.parse(line);
    if (event.type === "c04.dynamic_solver_frame" &&
        (event.data?.frameIndex === 0 || event.data?.frameIndex === 1)) {
      const cores = (items) => items.map((item) => item.decodedCandidate);
      result.set(event.data.frameIndex, { entry: cores(event.data.entryCores), exit: cores(event.data.exitCores) });
    }
  }
  if (!result.has(0) || !result.has(1)) throw new Error("missing C11 frame 0/1");
  return result;
}

function stateFromCore(core) {
  return [
    ...core.p, ...core.q, ...core.linearVelocity, ...core.angularVelocity,
  ].map(Math.fround);
}

function compare(local, unity) {
  const components = local.map((value, index) => value - unity[index]);
  return { components, maxAbs: Math.max(...components.map(Math.abs)) };
}

async function main() {
  const [sceneJs, eventsPath, outputPath] = process.argv.slice(2);
  if (!sceneJs || !eventsPath || !outputPath) {
    throw new Error("usage: node audit_c12_wasm_dynamic_consume.js B20.js events.jsonl output.json");
  }
  const c11 = frames(eventsPath);
  const frame0 = c11.get(0);
  const frame1 = c11.get(1);
  const createModule = require(path.resolve(sceneJs));
  const module = await createModule({ noInitialRun: false });
  module.cwrap("a19_init", null, [])();
  const reset = module.cwrap("b20_reset", null, new Array(13).fill("number"));
  const setCurrentPoseTransition = module.cwrap("b20_set_material_transition_current_pose", null, ["number"]);
  const step = module.cwrap("b20_physics_step", null, []);
  const getState = module.cwrap("b20_get_state", null, ["number", "number"]);
  const ptr = module._malloc(STATE_FLOATS * 4);
  const read = (which) => {
    getState(which, ptr);
    return Array.from(module.HEAPF32.subarray(ptr >> 2, (ptr >> 2) + STATE_FLOATS));
  };

  const activeEntry = stateFromCore(frame0.entry[0]);
  reset(...activeEntry);
  setCurrentPoseTransition(1);
  const before = { active: read(0), target: read(1) };
  step();
  const afterFrame0 = { active: read(0), target: read(1) };
  step();
  const after = { active: read(0), target: read(1) };
  module._free(ptr);

  const unityFrame0 = { active: stateFromCore(frame0.exit[0]), target: stateFromCore(frame0.exit[1]) };
  const unity = { active: stateFromCore(frame1.exit[0]), target: stateFromCore(frame1.exit[1]) };
  const result = {
    schema: "c12-wasm-dynamic-consume-v1",
    boundary: "C11 frame-0 entry -> frame-1 exit through two persistent Wasm Scene steps",
    singleVariable: "x64 hybrid scene replaced by existing scalar Wasm B20 scene",
    scope: "C11 same Unity pre-state; diagnostic only, no production integration",
    input: { unityActiveFrame0Entry: activeEntry, wasmBefore: before },
    unityFrame0Exit: unityFrame0,
    wasmFrame0Exit: afterFrame0,
    frame0Delta: { active: compare(afterFrame0.active, unityFrame0.active), target: compare(afterFrame0.target, unityFrame0.target) },
    unityExit: unity,
    wasmExit: after,
    delta: { active: compare(after.active, unity.active), target: compare(after.target, unity.target) },
  };
  fs.writeFileSync(outputPath, JSON.stringify(result, null, 2) + "\n");
  console.log(JSON.stringify({ output: outputPath, delta: result.delta }));
}

main().catch((error) => {
  console.error(error.stack || error);
  process.exitCode = 1;
});
