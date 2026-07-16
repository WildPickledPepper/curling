"use strict";

const fs = require("fs");

async function readStdin() {
  const chunks = [];
  for await (const chunk of process.stdin) chunks.push(chunk);
  return JSON.parse(Buffer.concat(chunks).toString("utf8"));
}

async function main() {
  const [wasmPath] = process.argv.slice(2);
  if (!wasmPath) {
    throw new Error("usage: node run_newfrictionstep_wasm_rollout.js ORACLE.wasm < input.json");
  }
  const input = await readStdin();
  const bytes = fs.readFileSync(wasmPath);
  const { instance } = await WebAssembly.instantiate(bytes, {
    env: {
      cos: Math.cos,
      sin: Math.sin,
      atan: Math.atan,
      pow: (x, y, _unused) => Math.pow(x, y),
    },
  });
  const view = new DataView(instance.exports.memory.buffer);
  const vectorAddress = 1024;
  const outputAddress = 2048;
  let vx = Number(input.vx);
  let vy = Number(input.vy);
  let angle = Number(input.angle);
  const steptime = Number(input.steptime);
  const steps = [];
  for (const friction of input.frictions) {
    view.setFloat64(vectorAddress, vx, true);
    view.setFloat64(vectorAddress + 8, vy, true);
    instance.exports.newfrictionstep(
      outputAddress,
      Number(friction),
      vectorAddress,
      angle,
      steptime,
      0,
    );
    vx = view.getFloat64(outputAddress, true);
    vy = view.getFloat64(outputAddress + 8, true);
    angle = view.getFloat64(outputAddress + 16, true);
    steps.push({ vx, vy, angle });
  }
  process.stdout.write(JSON.stringify({ steps }));
}

main().catch((error) => {
  process.stderr.write(`${error.stack || error}\n`);
  process.exitCode = 1;
});
