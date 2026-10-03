// Replay byte-preserved Unity functions against captured input/output memory.
const fs = require('fs');
const crypto = require('crypto');
const root = 'analysis_input';
const capture = `${root}/unity_transform_scale_calc_trace_20261001/logs`;
const dirs = fs.readdirSync(capture);
if (dirs.length !== 1) throw Error('Ambiguous event log');
const eventPath = `${capture}/${dirs[0]}/events.jsonl`;
const events = fs.readFileSync(eventPath, 'utf8').trim().split('\n').map(JSON.parse);
const rows = events.filter(r => r.type === 'a12.pcm_internal_call').map(r => r.data);
const kernel = fs.readFileSync(`${root}/unity_transform_scale_kernel_20261001.wasm`);
const manifest = JSON.parse(fs.readFileSync(`${root}/unity_transform_scale_kernel_20261001.json`));
const sha = b => crypto.createHash('sha256').update(b).digest('hex');
if (sha(kernel) !== manifest.kernelSha256) throw Error('Kernel SHA mismatch');
const instance = new WebAssembly.Instance(new WebAssembly.Module(kernel));
const mem = new Uint8Array(instance.exports.memory.buffer);
const view = new DataView(mem.buffer);
const verified = [], counts = {};
for (const row of rows) {
  if (![78119, 78120, 78121].includes(row.functionIndex)) continue;
  for (const arg of row.before) mem.set(Buffer.from(arg.hex, 'hex'), arg.ptr);
  const h = row.transformHierarchy;
  if (!h || !h.chain.length) throw Error('Missing hierarchy');
  mem.fill(0, h.hierarchyPtr, h.hierarchyPtr + 24);
  view.setUint32(h.hierarchyPtr + 24, h.nodesPtr, true);
  view.setUint32(h.hierarchyPtr + 28, h.parentsPtr, true);
  for (const n of h.chain) {
    for (let k = 0; k < n.bits.length; k++) view.setUint32(n.ptr + k*4, n.bits[k], true);
    view.setInt32(h.parentsPtr + n.index*4, n.parent, true);
  }
  instance.exports[`f${row.functionIndex}`](...row.args);
  const expected = Buffer.from(row.after.find(a => a.argument === 0).hex, 'hex').subarray(0,36);
  const actual = Buffer.from(mem.subarray(row.args[0],row.args[0]+36));
  if (!actual.equals(expected)) throw Error(`Matrix mismatch f${row.functionIndex}, call ${row.callId}: ${actual.toString('hex')} vs ${expected.toString('hex')}`);
  counts[row.functionIndex] = (counts[row.functionIndex] || 0) + 1;
  const floats = Array.from({length:9}, (_,i) => actual.readFloatLE(i*4));
  verified.push({callId:row.callId,functionIndex:row.functionIndex,releaseSerial:row.releaseSerial,
    matrixBits:Array.from({length:9},(_,i)=>actual.readUInt32LE(i*4)),matrix:floats,
    diagonal:[floats[0],floats[4],floats[8]],hierarchy:h});
}
if (verified.length !== 138) throw Error(`Expected 138 matrix calls, got ${verified.length}`);
const result = {eventPath,eventSha256:sha(fs.readFileSync(eventPath)),kernelSha256:sha(kernel),
  callsVerified:counts,totalCallsVerified:verified.length,matrixFloatsVerified:verified.length*9,
  verification:'All nine f32 output fields bit-exact; original numeric instructions executed.',verified};
fs.writeFileSync(`${root}/transform_scale_kernel_verified_20261001.json`,JSON.stringify(result,null,2));
console.log(JSON.stringify({callsVerified:counts,matrixFloatsVerified:result.matrixFloatsVerified}));
