// Exact instruction boundaries. Stores preserve flags, GPRs and XMM registers.
let mod,crt,thread,rows=[],buffers=[];
const points=new Set([0x2049c7,0x204cb5,0x204cc3,0x204ccc,0x204d12,0x204d1b,
  0x204d6e,0x204d99,0x204daa,0x204dae,0x204dc7,0x204dcf,0x204e02]);
const crtPoints=new Set([0xa77e0,0xa7840,0xa7848,0xa7851,0xa7855]);
function hex(p,n) {return Array.from(new Uint8Array(p.readByteArray(n)))
  .map(b=>b.toString(16).padStart(2,'0')).join('');}
function storeXmm(buffer) {
  // push rax; movabs rax, buffer; movups [rax+16*n], xmmN; pop rax.
  const out=[0x50,0x48,0xb8];
  let addr=BigInt(buffer.toString());
  for(let i=0;i<8;i++){out.push(Number(addr&255n));addr>>=8n;}
  for(let i=0;i<16;i++) {
    if(i>=8)out.push(0x44);
    out.push(0x0f,0x11,0x80|((i%8)<<3));
    const offset=i*16;
    out.push(offset&255,(offset>>8)&255,0,0);
  }
  out.push(0x0f,0xae,0x98,0x00,0x01,0,0); // stmxcsr [rax+256]
  out.push(0x58);
  return out;
}
rpc.exports={
 arm(threadId,modulePath) {
  mod=Process.enumerateModules().find(m=>m.path.toLowerCase()===modulePath.toLowerCase());
  if(!mod)throw Error('module absent');
  crt=Process.findModuleByAddress(mod.base.add(0x455348).readPointer());
  thread=threadId;
  Stalker.follow(thread,{transform(iterator){
   let instruction;
   while((instruction=iterator.next())!==null){
    const rva=instruction.address.sub(mod.base).toUInt32();
    const crtRva=instruction.address.sub(crt.base).toUInt32();
    const inCrt=crtPoints.has(crtRva);
    if(points.has(rva)||inCrt){
     const description=instruction.toString();
     const buffer=Memory.alloc(272);buffers.push(buffer);
     iterator.putBytes(storeXmm(buffer));
     iterator.putCallout(c=>{
      const row={functionRva:'0x'+(inCrt?crtRva:rva).toString(16),
       modulePath:inCrt?crt.path:mod.path,instruction:description,
       xmmHex:hex(buffer,256),mxcsr:buffer.add(256).readU32()};
      if(!inCrt){
       row.bodyDataHex=hex(c.rdi.add(c.rbp),112);
       row.solverBodyHex=hex(c.rbx.add(c.rsi),32);
       row.motionBodyHex=hex(c.rbx.add(c.rsp.add(0x40).readPointer()),32);
       row.stackHex=hex(c.rsp.add(0x50),32);
      }
      rows.push(row);
     });
    }
    iterator.keep();
   }
  }});
  // IAT slots decoded from the observed module's import descriptors.
  const trigImports=[['cosf',0x455348],['sinf',0x4553d0]].map(x=>{
   const address=mod.base.add(x[1]).readPointer();
   const dll=Process.findModuleByAddress(address);
   let addr=address;const instructions=[];
   for(let i=0;i<24;i++){const ins=Instruction.parse(addr);instructions.push(ins.toString());addr=ins.next;}
   return {name:x[0],iatSlotRva:'0x'+x[1].toString(16),address:address.toString(),
    implementationModule:dll?dll.path:null,implementationRva:dll?address.sub(dll.base).toString():null,
    runtimeCodeHex:hex(address,256),
    instructions};
  });
  return {base:mod.base.toString(),path:mod.path,size:mod.size,trigImports,
    targets:Array.from(points).map(x=>'0x'+x.toString(16))};
 },
 finish(){Stalker.unfollow(thread);Stalker.flush();
  return {calls:rows,dropped:0,unfinished:[],unhookedTargets:[],readOnlyRegisterStores:true};}
};
