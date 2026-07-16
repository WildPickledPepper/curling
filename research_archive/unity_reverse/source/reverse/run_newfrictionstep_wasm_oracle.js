"use strict";

const fs = require("fs");

async function main() {
  const [wasmPath, inputPath] = process.argv.slice(2);
  if (!wasmPath || !inputPath) {
    throw new Error("usage: node run_newfrictionstep_wasm_oracle.js ORACLE.wasm INPUT.json");
  }
  const bytes = fs.readFileSync(wasmPath);
  const { instance } = await WebAssembly.instantiate(bytes, {
    env: {
      cos: Math.cos,
      sin: Math.sin,
      atan: Math.atan,
      pow: (x, y, _unused) => Math.pow(x, y),
    },
  });
  const rows = JSON.parse(fs.readFileSync(inputPath, "utf8"));
  const view = new DataView(instance.exports.memory.buffer);
  const vectorAddress = 1024;
  const outputAddress = 2048;
  const output = rows.map((row) => {
    view.setFloat64(vectorAddress, Number(row.vx), true);
    view.setFloat64(vectorAddress + 8, Number(row.vy), true);
    instance.exports.newfrictionstep(
      outputAddress,
      Number(row.friction),
      vectorAddress,
      Number(row.angle),
      Number(row.steptime),
      0,
    );
    return {
      ...row,
      output: {
        vx: view.getFloat64(outputAddress, true),
        vy: view.getFloat64(outputAddress + 8, true),
        angle: view.getFloat64(outputAddress + 16, true),
      },
    };
  });
  process.stdout.write(JSON.stringify(output));
}

main().catch((error) => {
  process.stderr.write(`${error.stack || error}\n`);
  process.exitCode = 1;
});
