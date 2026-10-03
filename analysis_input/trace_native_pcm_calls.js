// Read-only callsite observation; no register/memory substitutions.
let moduleRecord = null;
let rows = [];
let active = [];
let nextId = 0;
let tracedThread = null;
let dropped = 0;
let listeners = [];
let lightDiscovery = false;
let unhookedTargets = [];
let mxcsrProbes = [];

function inside(p) {
  return p.compare(moduleRecord.base) >= 0 &&
    p.compare(moduleRecord.base.add(moduleRecord.size)) < 0;
}

function multiCacheSnapshot(cache) {
  const data = cache.readPointer();
  const size = cache.add(8).readU16();
  return {ptr:cache.toString(),cachedDataPtr:data.toString(),cachedSize:size,
    manifoldFlags:cache.add(11).readU8(),
    serializedBytes:data.isNull() ? [] : Array.from(new Uint8Array(data.readByteArray(Math.max(48,Math.min(size,304)))))};
}

function snapshot(args) {
  if (lightDiscovery) return [];
  const out = [];
  args.forEach((p, index) => {
    try {
      const range = Process.findRangeByAddress(p);
      if (!range || range.protection[0] !== 'r' || p.compare(ptr(65536)) < 0) return;
      const length = Math.min(4096, range.base.add(range.size).sub(p).toUInt32());
      if (length < 64) return;
      const bytes = new Uint8Array(p.readByteArray(length));
      let hex = '';
      bytes.forEach(b => { hex += b.toString(16).padStart(2, '0'); });
      out.push({argument: index, ptr: p.toString(), byteLength: length, hex: hex});
    } catch (_) { /* Not a readable pointer argument. */ }
  });
  return out;
}

function rigidIdPool(pool) {
  const freeCount=pool.add(0x10).readU32();
  const pendingCount=pool.add(0x30).readU32();
  function ids(address,count) {
    if (count>256) throw new Error('invalid ID count');
    const p=address.readPointer();
    const result=[];
    for(let i=0;i<count;i++) result.push(p.add(i*4).readU32());
    return result;
  }
  return {ptr:pool.toString(),nextId:pool.readU32(),
    freeIds:ids(pool.add(8),freeCount),pendingIds:ids(pool.add(0x28),pendingCount)};
}

function resolveTarget(operand, next, context) {
  if (operand.type === 'imm') return ptr(operand.value);
  if (operand.type === 'reg') return context[operand.value];
  if (operand.type === 'mem') {
    const v = operand.value;
    let address = v.base === 'rip' ? next : (v.base ? context[v.base] : ptr(0));
    if (v.index) address = address.add(context[v.index].toUInt32() * (v.scale || 1));
    return address.add(v.disp || 0).readPointer();
  }
  return null;
}

rpc.exports = {
  arm(threadId, modulePath, targetRvas, lightweight, probeMxcsr) {
    lightDiscovery = Boolean(lightweight);
    moduleRecord = Process.enumerateModules().find(m =>
      m.path.toLowerCase() === modulePath.toLowerCase());
    if (!moduleRecord) throw new Error('exact native module not loaded');
    tracedThread = threadId;
    if (targetRvas) {
      targetRvas.forEach(rva => {
        try {
        let mxcsrSlot = null;
        if (probeMxcsr) {
          // Native listener reads MXCSR before any JS numeric conversion.
          // stmxcsr [rip+9]; ret, with its 4-byte destination at code+16.
          const page = Memory.alloc(Process.pageSize);
          page.writeByteArray([0x0f,0xae,0x1d,9,0,0,0,0xc3]);
          mxcsrSlot = page.add(16);
          mxcsrSlot.writeU32(0xffffffff);
          Memory.protect(page, Process.pageSize, 'rwx');
          mxcsrProbes.push(page);
          listeners.push(Interceptor.attach(moduleRecord.base.add(ptr(rva)), {onEnter:page}));
        }
        if (rva === '0x1fc5aa' || rva === '0x2049c7') {
          listeners.push(Interceptor.attach(moduleRecord.base.add(ptr(rva)), {
            onEnter() {
              if (this.threadId !== tracedThread) return;
              const c=this.context;
              const bodyData=c.rdi.add(c.rbp);
              const solverBody=c.rbx.add(c.rsi);
              const motionBody=rva==='0x2049c7'
                ? c.rbx.add(c.rsp.add(0x40).readPointer()) : c.rbx.add(c.r13);
              rows.push({callId:++nextId,functionRva:rva,instructionSnapshot:true,
                mxcsrAtNativeEntry:mxcsrSlot ? mxcsrSlot.readU32() : null,
                bodyDataPtr:bodyData.toString(),solverBodyPtr:solverBody.toString(),
                motionBodyPtr:motionBody.toString(),
                bodyDataBytes:Array.from(new Uint8Array(bodyData.readByteArray(112))),
                solverBodyBytes:Array.from(new Uint8Array(solverBody.readByteArray(32))),
                motionBodyBytes:Array.from(new Uint8Array(motionBody.readByteArray(32)))});
            }
          }));
          return;
        }
        listeners.push(Interceptor.attach(moduleRecord.base.add(ptr(rva)), {
          onEnter(args) {
            if (this.threadId !== tracedThread) return;
            const values = [];
            for (let index = 0; index < 14; index++) values.push(args[index]);
            this.row = {callId: ++nextId,
              parentCallId: active.length ? active[active.length - 1] : null,
              functionRva: rva,
              returnAddressRva: inside(this.returnAddress)
                ? this.returnAddress.sub(moduleRecord.base).toString() : null,
              args: values.map(p => p.toString()), before: snapshot(values)};
            if(rva==='0x330f0') {
              this.cache=values[2];
              this.row.multiCacheBefore=multiCacheSnapshot(this.cache);
            }
            if (rva === '0x236ed0') {
              this.row.pairSortInput = [values[1],values[2]].map(shape => {
                const sim = shape.add(8).readPointer();
                const core = sim.add(0x50).readPointer();
                const type = core.add(0x0d).readU8();
                const body = type === 1 ? sim.add(0x88).readPointer() : null;
                return {shape:shape.toString(),actorSim:sim.toString(),
                  rigidId:sim.add(0x58).readU32(),actorType:type,
                  bodyCore:body ? body.toString() : null,
                  bodyCoreBytes:body ? Array.from(new Uint8Array(body.readByteArray(192))) : null};
              });
            }
            if(rva==='0x214bd0' || rva==='0x214c50') {
              const scene=rva==='0x214bd0' ? values[1] : values[0].add(0x48).readPointer();
              this.pool=scene.add(0x10d0).readPointer();
              this.row.rigidIdPoolBefore=rigidIdPool(this.pool);
              this.row.actorSim=values[0].toString();
              this.row.rigidIdBefore=values[0].add(0x58).readU32();
            }
            active.push(this.row.callId);
            rows.push(this.row);
          },
          onLeave(result) {
            if (!this.row) return;
            this.row.resultRax = result.toString();
            if (mxcsrSlot) this.row.mxcsrAtNativeEntry = mxcsrSlot.readU32();
            this.row.after = snapshot(this.row.args.map(p => ptr(p)));
            if(this.cache) this.row.multiCacheAfter=multiCacheSnapshot(this.cache);
            if(this.pool) {
              this.row.rigidIdAfter=ptr(this.row.actorSim).add(0x58).readU32();
              this.row.rigidIdPoolAfter=rigidIdPool(this.pool);
            }
            if (active.pop() !== this.row.callId) this.row.stackMismatch = true;
          }
        }));
        } catch (error) {
          unhookedTargets.push({functionRva:rva, error:String(error)});
        }
      });
      return {base: moduleRecord.base.toString(), size: moduleRecord.size,
        path: moduleRecord.path, targets: targetRvas, unhookedTargets:unhookedTargets};
    }
    Stalker.follow(threadId, {
      transform(iterator) {
        let instruction;
        while ((instruction = iterator.next()) !== null) {
          if (!inside(instruction.address) || instruction.mnemonic !== 'call') {
            iterator.keep();
            continue;
          }
          const operand = instruction.operands[0];
          const next = instruction.next;
          const site = instruction.address.sub(moduleRecord.base).toString();
          const text = instruction.toString();
          let invocation = null;
          iterator.putCallout(context => {
            try {
              const target = resolveTarget(operand, next, context);
              if (!target || !inside(target)) { invocation = null; return; }
              const targetRva = target.sub(moduleRecord.base).toUInt32();
              if (lightDiscovery && (targetRva < 0x100000 || targetRva >= 0x440000)) {
                invocation = null; return;
              }
              if (rows.length >= (lightDiscovery ? 20000 : 3000)) { dropped++; invocation = null; return; }
              const args = [context.rcx, context.rdx, context.r8, context.r9];
              for (let index = 0; index < 10; index++) {
                args.push(context.rsp.add(32 + index * 8).readPointer());
              }
              invocation = {callId: ++nextId,
                parentCallId: active.length ? active[active.length - 1] : null,
                callSiteRva: site, functionRva: target.sub(moduleRecord.base).toString(),
                instruction: text, args: args.map(p => p.toString()),
                before: snapshot(args)};
              active.push(invocation.callId);
              rows.push(invocation);
            } catch (error) {
              rows.push({callSiteRva: site, error: String(error)});
              invocation = null;
            }
          });
          iterator.keep();
          iterator.putCallout(context => {
            if (!invocation) return;
            invocation.resultRax = context.rax.toString();
            invocation.after = snapshot(invocation.args.map(p => ptr(p)));
            active.pop();
            invocation = null;
          });
        }
      }
    });
    return {base: moduleRecord.base.toString(), size: moduleRecord.size, path: moduleRecord.path};
  },
  finish() {
    if (listeners.length) listeners.forEach(listener => listener.detach());
    else { Stalker.unfollow(tracedThread); Stalker.flush(); }
    return {calls: rows, dropped: dropped, unfinished: active, unhookedTargets:unhookedTargets};
  }
};
