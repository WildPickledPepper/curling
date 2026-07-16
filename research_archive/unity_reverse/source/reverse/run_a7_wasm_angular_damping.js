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
    throw new Error("usage: node run_a7_wasm_angular_damping.js KERNEL.wasm < input.json");
  }
  const input = await readStdin();
  const { instance } = await WebAssembly.instantiate(fs.readFileSync(wasmPath), {});
  const apply = instance.exports.a7_apply_angular_damping || instance.exports._a7_apply_angular_damping;
  if (typeof apply !== "function") {
    throw new Error("missing a7_apply_angular_damping export");
  }
  const angularDamping = Number(input.angularDamping);
  const dt = Number(input.dt);
  const rows = input.rows.map((row) => ({
    tickSerial: row.tickSerial,
    setterWy: Number(row.setterWy),
    wasmGetterWy: Number(apply(Number(row.setterWy), angularDamping, dt)),
  }));
  process.stdout.write(JSON.stringify({ rows }));
}

main().catch((error) => {
  process.stderr.write(`${error.stack || error}\n`);
  process.exitCode = 1;
});
