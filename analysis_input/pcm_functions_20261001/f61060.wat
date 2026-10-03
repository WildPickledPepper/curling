  (func $f61060 (type $t3) (param $p0 i32) (param $p1 i32) (param $p2 i32) (result i32)
    (local $l3 i32)
    i32.const 4675128
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3753376
      call $f1661
      i32.const 4675128
      i32.const 1
      i32.store8
    end
    local.get $p0
    i32.load offset=32
    local.set $p2
    i32.const 3753376
    i32.load
    local.tee $l3
    i32.load offset=116
    i32.eqz
    if $I1
      local.get $l3
      call $f65192
    end
    block $B2
      local.get $p2
      i32.const 0
      i32.const 0
      call $f54425
      i32.eqz
      if $I3
        local.get $p0
        i32.load offset=32
        local.set $p2
        br $B2
      end
      i32.const 4675186
      i32.load8_u
      i32.eqz
      if $I4
        i32.const 3752300
        call $f1661
        i32.const 4675186
        i32.const 1
        i32.store8
      end
      local.get $p0
      i32.const 3752300
      i32.load
      i32.load offset=92
      i32.load
      local.tee $p2
      i32.store offset=32
    end
    local.get $p2
    local.get $p1
    i32.const 0
    call $f60665)
