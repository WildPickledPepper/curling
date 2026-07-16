"use strict";

const fs = require("fs");
const path = require("path");

function f32(bytes, offset) {
  const data = bytes instanceof Uint8Array ? bytes : Uint8Array.from(bytes);
  const view = new DataView(data.buffer, data.byteOffset, data.byteLength);
  return view.getFloat32(offset, true);
}

function floatArray(bytes, count) {
  return Array.from({ length: count }, (_, index) => f32(bytes, index * 4));
}

function delta(actual, expected) {
  const values = actual.map((value, index) => value - expected[index]);
  return { values, maxAbs: Math.max(...values.map(Math.abs)) };
}

function c11Calls(eventsPath) {
  for (const line of fs.readFileSync(eventsPath, "utf8").split(/\r?\n/)) {
    if (!line) continue;
    const event = JSON.parse(line);
    if (event.type !== "c04.dynamic_solver_frame" || event.data?.frameIndex !== 1) continue;
    return event.data.dynamicSolves.map((call, index) => {
      const before = call.before.descs[0];
      const after = call.after.descs[0];
      return {
        index,
        bodyA: before.bodyAWindow.rawBytes.slice(0, 32),
        bodyB: before.bodyBWindow.rawBytes.slice(0, 32),
        constraint: before.constraintWindow.rawBytes,
        unityBodyAAfter: after.bodyAWindow.rawBytes.slice(0, 32),
        unityBodyBAfter: after.bodyBWindow.rawBytes.slice(0, 32),
        unityConstraintAfter: after.constraintWindow.rawBytes,
      };
    });
  }
  throw new Error("C11 frame 1 regular dynamic solves missing");
}

async function main() {
  const [wasmJs, eventsPath, outputPath] = process.argv.slice(2);
  if (!wasmJs || !eventsPath || !outputPath) {
    throw new Error("usage: node audit_c13_wasm_solver_stage.js harness.js C11-events.jsonl output.json");
  }
  const createModule = require(path.resolve(wasmJs));
  const module = await createModule({ noInitialRun: true });
  const bodyBytes = module.cwrap("c13_solver_body_bytes", "number", [])();
  const constraintBytes = module.cwrap("c13_constraint_bytes", "number", [])();
  if (bodyBytes !== 32 || constraintBytes !== 320) {
    throw new Error(`unexpected harness layout body=${bodyBytes} constraint=${constraintBytes}`);
  }
  const solve = module.cwrap("c13_solve_regular", "number", ["number", "number", "number", "number", "number", "number", "number"]);
  const block = module._malloc(bodyBytes * 4 + constraintBytes * 2);
  const bodyAIn = block;
  const bodyBIn = bodyAIn + bodyBytes;
  const bodyAOut = bodyBIn + bodyBytes;
  const bodyBOut = bodyAOut + bodyBytes;
  const constraintIn = bodyBOut + bodyBytes;
  const constraintOut = constraintIn + constraintBytes;
  function run(call, doFriction) {
    module.HEAPU8.set(call.bodyA, bodyAIn);
    module.HEAPU8.set(call.bodyB, bodyBIn);
    module.HEAPU8.set(call.constraint, constraintIn);
    const status = solve(bodyAIn, bodyBIn, constraintIn, doFriction, bodyAOut, bodyBOut, constraintOut);
    if (status) throw new Error(`solver harness returned ${status} on regular call ${call.index}`);
    const wasmBodyA = Array.from(module.HEAPU8.subarray(bodyAOut, bodyAOut + bodyBytes));
    const wasmBodyB = Array.from(module.HEAPU8.subarray(bodyBOut, bodyBOut + bodyBytes));
    const wasmConstraint = Array.from(module.HEAPU8.subarray(constraintOut, constraintOut + constraintBytes));
    const unityBodyA = call.unityBodyAAfter;
    const unityBodyB = call.unityBodyBAfter;
    return {
      doFriction: Boolean(doFriction),
      bodyA: { wasm: floatArray(wasmBodyA, 8), unity: floatArray(unityBodyA, 8), delta: delta(floatArray(wasmBodyA, 8), floatArray(unityBodyA, 8)) },
      bodyB: { wasm: floatArray(wasmBodyB, 8), unity: floatArray(unityBodyB, 8), delta: delta(floatArray(wasmBodyB, 8), floatArray(unityBodyB, 8)) },
      constraintBytesExact: wasmConstraint.every((value, index) => value === call.unityConstraintAfter[index]),
      firstTargetLinearYDelta: f32(wasmBodyB, 4) - f32(unityBodyB, 4),
    };
  }
  const calls = c11Calls(eventsPath).map((call) => {
    const noFriction = run(call, 0);
    const withFriction = run(call, 1);
    return {
      regularCall: call.index,
      noFriction,
      withFriction,
      matchingMode: noFriction.bodyA.delta.maxAbs === 0 && noFriction.bodyB.delta.maxAbs === 0 ? "no_friction" :
        withFriction.bodyA.delta.maxAbs === 0 && withFriction.bodyB.delta.maxAbs === 0 ? "friction" : "neither",
    };
  });
  module._free(block);
  const result = {
    schema: "c13-wasm-solver-stage-v1",
    boundary: "C11 frame-1 regular solveContactBlock direct raw body/constraint replay",
    singleVariable: "x64 hybrid consume replaced by scalar Wasm solveContactBlock at same post-pre-integrate stage",
    scope: "diagnostic only; no Scene.simulate, actor, pair, cache or production path",
    solverBodyBytes: bodyBytes,
    constraintBytes,
    calls,
  };
  fs.writeFileSync(outputPath, JSON.stringify(result, null, 2) + "\n");
  console.log(JSON.stringify({ output: outputPath, calls: calls.map((call) => ({ regularCall: call.regularCall, matchingMode: call.matchingMode, noFrictionTargetY: call.noFriction.firstTargetLinearYDelta, frictionTargetY: call.withFriction.firstTargetLinearYDelta })) }));
}

main().catch((error) => {
  console.error(error.stack || error);
  process.exitCode = 1;
});
