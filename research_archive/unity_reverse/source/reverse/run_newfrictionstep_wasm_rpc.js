"use strict";

// Line-oriented persistent companion for unity_wasm_motion_oracle.py.  Keeping
// one wasm instance alive makes it practical to feed it the current local
// PhysX getter state on every fixed tick.
const fs = require("fs");
const readline = require("readline");

async function main() {
  const [wasmPath] = process.argv.slice(2);
  if (!wasmPath) throw new Error("usage: node run_newfrictionstep_wasm_rpc.js ORACLE.wasm");
  const { instance } = await WebAssembly.instantiate(fs.readFileSync(wasmPath), {
    env: { cos: Math.cos, sin: Math.sin, atan: Math.atan, pow: (x, y) => Math.pow(x, y) },
  });
  const view = new DataView(instance.exports.memory.buffer);
  const vectorAddress = 1024;
  const outputAddress = 2048;
  const STEP = 0.0010000000474974513;
  const input = readline.createInterface({ input: process.stdin, crlfDelay: Infinity });
  for await (const line of input) {
    if (!line) continue;
    const row = JSON.parse(line);
    view.setFloat64(vectorAddress, Number(row.vx), true);
    view.setFloat64(vectorAddress + 8, Number(row.vy), true);
    instance.exports.newfrictionstep(outputAddress, Number(row.friction), vectorAddress, Number(row.angle), STEP, 0);
    process.stdout.write(JSON.stringify({
      vx: view.getFloat64(outputAddress, true),
      vy: view.getFloat64(outputAddress + 8, true),
      angle: view.getFloat64(outputAddress + 16, true),
    }) + "\n");
  }
}

main().catch((error) => {
  process.stderr.write(`${error.stack || error}\n`);
  process.exitCode = 1;
});
