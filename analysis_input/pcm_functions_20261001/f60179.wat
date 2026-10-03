  (func $f60179 (type $t40) (param $p0 i32) (param $p1 f32) (param $p2 i32) (result i32)
    i32.const 4674503
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3752504
      call $f1661
      i32.const 4674503
      i32.const 1
      i32.store8
    end
    i32.const 3752504
    i32.load
    local.tee $p0
    i32.load offset=116
    i32.eqz
    if $I1
      local.get $p0
      call $f65192
    end
    local.get $p1
    f32.abs
    f32.const 0x1.28f5c2p-3 (;=0.145;)
    f32.le)
