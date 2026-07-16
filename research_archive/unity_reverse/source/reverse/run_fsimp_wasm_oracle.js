"use strict";

const fs = require("fs");

async function main() {
  const [wasmPath, inputPath] = process.argv.slice(2);
  if (!wasmPath || !inputPath) {
    throw new Error("usage: node run_fsimp_wasm_oracle.js ORACLE.wasm INPUT.json");
  }
  const bytes = fs.readFileSync(wasmPath);
  const imports = {
    env: {
      cos: Math.cos,
      sin: Math.sin,
      atan: Math.atan,
      pow: (x, y, _unused) => Math.pow(x, y),
    },
  };
  const { instance } = await WebAssembly.instantiate(bytes, imports);
  const rows = JSON.parse(fs.readFileSync(inputPath, "utf8"));
  const view = new DataView(instance.exports.memory.buffer);
  const paramsAddress = 1024;
  const output = rows.map((row) => {
    const params = row.params;
    [params.vx, params.vy, params.w, params.r1, params.r2].forEach((value, index) => {
      view.setFloat64(paramsAddress + index * 8, Number(value), true);
    });
    const value = instance.exports.fsimp(
      Number(row.a),
      Number(row.b),
      Number(row.eps),
      paramsAddress,
      Number(row.type),
      Number(row.index),
      0,
    );
    return { ...row, value };
  });
  process.stdout.write(JSON.stringify(output));
}

main().catch((error) => {
  process.stderr.write(`${error.stack || error}\n`);
  process.exitCode = 1;
});
