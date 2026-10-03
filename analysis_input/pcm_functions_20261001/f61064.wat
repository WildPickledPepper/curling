  (func $f61064 (type $t0) (param $p0 i32) (param $p1 i32) (result i32)
    i32.const 4675132
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3751540
      call $f1661
      i32.const 4675132
      i32.const 1
      i32.store8
    end
    block $B1
      local.get $p0
      if $I2
        local.get $p0
        i32.load
        i32.load offset=32
        i32.const 3751540
        i32.load
        local.tee $p1
        i32.load offset=32
        i32.ne
        br_if $B1
        local.get $p0
        call $f1451
        i32.load
        return
      end
      call $f1679
      unreachable
    end
    local.get $p0
    local.get $p1
    call $f1678
    unreachable)
