"use strict";

const fs = require("fs");
const path = require("path");

function f32(bytes, offset) {
  const data = bytes instanceof Uint8Array ? bytes : Uint8Array.from(bytes);
  return new DataView(data.buffer, data.byteOffset, data.byteLength).getFloat32(offset, true);
}

function floats(bytes, count = 8) {
  return Array.from({ length: count }, (_, index) => f32(bytes, index * 4));
}

function x64StaticConstraintToWasm(bytes) {
  if (bytes.length !== 608) throw new Error(`unexpected x64 static constraint length ${bytes.length}`);
  // SolverContactHeader has two native pointers plus x64 padding (80B) but is
  // 64B in Wasm. The static no-writeback solve reads only the first 56B of the
  // header; zero the Wasm pointer slots and shift the contact payload by 16B.
  const wasm = new Uint8Array(608);
  wasm.set(bytes.slice(0, 56), 0);
  wasm.set(bytes.slice(80), 64);
  return Array.from(wasm);
}

function c11ExpectedTargetY(eventsPath) {
  for (const line of fs.readFileSync(eventsPath, "utf8").split(/\r?\n/)) {
    if (!line) continue;
    const event = JSON.parse(line);
    if (event.type !== "c04.dynamic_solver_frame" || event.data?.frameIndex !== 1) continue;
    const calls = event.data.dynamicSolves;
    return {
      regular0After: calls[0].after.descs[0].bodyBWindow.rawBytes.slice(0, 32),
      regular1Before: calls[1].before.descs[0].bodyBWindow.rawBytes.slice(0, 32),
    };
  }
  throw new Error("C11 frame-1 regular dynamic solves missing");
}

async function main() {
  const [wasmJs, c14Path, c11Events, outputPath] = process.argv.slice(2);
  if (!wasmJs || !c14Path || !c11Events || !outputPath) {
    throw new Error("usage: node audit_c14_wasm_static_solver_stage.js harness.js c14.json c11-events.jsonl output.json");
  }
  const trace = JSON.parse(fs.readFileSync(c14Path, "utf8"));
  const entry = trace.hybrid.solveBlockTrace.find((item) =>
    item.sequence === 18 && item.constraint_type === 5 && item.body_a_data_index === 1);
  if (!entry) throw new Error("target static seq=18 missing from C14 trace");
  if (entry.constraint_bytes_before.length !== 608 || entry.constraint_length_over16 !== 38) {
    throw new Error("unexpected C14 target static constraint layout");
  }
  const expected = c11ExpectedTargetY(c11Events);
  const createModule = require(path.resolve(wasmJs));
  const module = await createModule({ noInitialRun: true });
  const bodyBytes = module.cwrap("c14_solver_body_bytes", "number", [])();
  const constraintBytes = module.cwrap("c14_constraint_bytes", "number", [])();
  if (bodyBytes !== 32 || constraintBytes !== 608) throw new Error(`unexpected layout ${bodyBytes}/${constraintBytes}`);
  const solve = module.cwrap("c14_solve_static", "number", ["number", "number", "number", "number", "number", "number"]);
  const ptr = module._malloc(bodyBytes * 2 + constraintBytes * 2);
  const bodyIn = ptr;
  const bodyOut = bodyIn + bodyBytes;
  const constraintIn = bodyOut + bodyBytes;
  const constraintOut = constraintIn + constraintBytes;
  const inputBody = entry.body_a_before.raw_bytes.slice(0, bodyBytes);
  const inputConstraint = x64StaticConstraintToWasm(entry.constraint_bytes_before);
  const wasmConstraintLengthOver16 = entry.constraint_length_over16 - 1;
  function run(doFriction) {
    module.HEAPU8.set(inputBody, bodyIn);
    module.HEAPU8.set(inputConstraint, constraintIn);
    const status = solve(bodyIn, constraintIn, wasmConstraintLengthOver16, doFriction, bodyOut, constraintOut);
    if (status) throw new Error(`static solver returned ${status}`);
    const wasmBody = Array.from(module.HEAPU8.subarray(bodyOut, bodyOut + bodyBytes));
    const localBody = entry.body_a_after.raw_bytes.slice(0, bodyBytes);
    const unityAfter = expected.regular1Before;
    return {
      doFriction: Boolean(doFriction),
      inputY: f32(inputBody, 4),
      wasmY: f32(wasmBody, 4),
      localX64Y: f32(localBody, 4),
      unityY: f32(unityAfter, 4),
      wasmMinusUnity: f32(wasmBody, 4) - f32(unityAfter, 4),
      x64MinusUnity: f32(localBody, 4) - f32(unityAfter, 4),
      wasmBody: floats(wasmBody),
      x64Body: floats(localBody),
      unityBody: floats(unityAfter),
      wasmConstraintLengthOver16,
    };
  }
  const result = {
    schema: "c14-wasm-static-solver-stage-v1",
    boundary: "C14 target-ice static support direct raw solver replay between C11 regular dynamic calls 0 and 1",
    singleVariable: "x64 solveContact_BStaticBlock replaced by scalar Wasm function at identical local raw body/constraint input",
    scope: "diagnostic only; no Scene.simulate, pair/cache/material mutation, Unity resampling, or production correction",
    entry: { sequence: entry.sequence, x64ConstraintLengthOver16: entry.constraint_length_over16, wasmConstraintLengthOver16, normalCount: entry.normal_constraint_count, frictionCount: entry.friction_constraint_count },
    modes: [run(0), run(1)],
  };
  module._free(ptr);
  fs.writeFileSync(outputPath, JSON.stringify(result, null, 2) + "\n");
  console.log(JSON.stringify({ output: outputPath, modes: result.modes.map((mode) => ({ doFriction: mode.doFriction, wasmMinusUnity: mode.wasmMinusUnity, x64MinusUnity: mode.x64MinusUnity, wasmY: mode.wasmY })) }));
}

main().catch((error) => {
  console.error(error.stack || error);
  process.exitCode = 1;
});
