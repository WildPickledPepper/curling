// Read-only native cooking input discovery. Arguments and memory are unchanged.
let record, tid, descriptors = [], sites = [], seen = new Set(), inputSeen = new Set();
function inside(p) { return p.compare(record.base) >= 0 && p.compare(record.base.add(record.size)) < 0; }
function inspect(p, rva, arg) {
  try {
    const range = Process.findRangeByAddress(p);
    if (!range || range.protection[0] !== 'r' || p.compare(ptr(65536)) < 0) return;
    // Win64 PxBoundedData: stride +0, pointer +8, count +16, size 24.
    if (p.readU32() !== 12 || p.add(16).readU32() !== 512) return;
    const data = p.add(8).readPointer();
    const dataRange = Process.findRangeByAddress(data);
    if (!dataRange || dataRange.protection[0] !== 'r' || data.add(6144).compare(dataRange.base.add(dataRange.size)) > 0) return;
    const flags = p.add(72).readU16(), vertexLimit = p.add(74).readU16(), quantizedCount = p.add(76).readU16();
    if (vertexLimit !== 255 || quantizedCount !== 255) return;
    const key = p.toString() + ':' + data.toString() + ':' + flags;
    if (inputSeen.has(key)) return;
    inputSeen.add(key);
    const pointBits = [];
    for (let i=0;i<512;i++) pointBits.push([data.add(i*12).readU32(),data.add(i*12+4).readU32(),data.add(i*12+8).readU32()]);
    descriptors.push({functionRva:rva,argument:arg,descriptorPtr:p.toString(),dataPtr:data.toString(),
      stride:12,count:512,flags:flags,vertexLimit:vertexLimit,quantizedCount:quantizedCount,pointBits:pointBits});
  } catch (_) {}
}
rpc.exports = {
  arm(threadId, modulePath) {
    tid=threadId; record=Process.enumerateModules().find(m => m.path.toLowerCase()===modulePath.toLowerCase());
    if (!record) throw new Error('exact module not loaded');
    Stalker.follow(tid,{transform(iterator) {
      let ins;
      while ((ins=iterator.next())!==null) {
        if (inside(ins.address) && ins.mnemonic==='call') {
          const operand=ins.operands[0], next=ins.next, site=ins.address.sub(record.base).toString();
          iterator.putCallout(c => {
            try {
              let target;
              if (operand.type==='imm') target=ptr(operand.value);
              else if (operand.type==='reg') target=c[operand.value];
              else {
                const v=operand.value;
                let a=v.base==='rip' ? next : (v.base ? c[v.base] : ptr(0));
                if (v.index) a=a.add(c[v.index].toUInt32()*(v.scale||1));
                target=a.add(v.disp||0).readPointer();
              }
              if (!target || !inside(target)) return;
              const rva=target.sub(record.base).toString();
              if (seen.has(rva)) return;
              seen.add(rva); sites.push({callSiteRva:site,functionRva:rva});
              [c.rcx,c.rdx,c.r8,c.r9].forEach((p,i)=>inspect(p,rva,i));
            } catch (_) {}
          });
        }
        iterator.keep();
      }
    }});
    return {base:record.base.toString(),path:record.path};
  },
  finish() { Stalker.unfollow(tid); Stalker.flush(); return {descriptors:descriptors,sites:sites}; }
};
