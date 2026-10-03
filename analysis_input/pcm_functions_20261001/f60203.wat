  (func $f60203 (type $t1) (param $p0 i32) (param $p1 i32)
    i32.const 4674526
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3748808
      call $f1661
      i32.const 3849164
      call $f1661
      i32.const 4674526
      i32.const 1
      i32.store8
    end
    i32.const 3748808
    i32.load
    local.tee $p1
    i32.load offset=116
    i32.eqz
    if $I1
      local.get $p1
      call $f65192
    end
    i32.const 3849164
    i32.load
    i32.const 0
    call $f42976
    local.get $p0
    i32.load offset=68
    local.tee $p1
    if $I2
      local.get $p1
      i32.const 0
      call $f52643
    end
    local.get $p0
    i32.load offset=64
    local.tee $p1
    if $I3
      local.get $p1
      i32.const 0
      call $f52643
    end
    local.get $p0
    i32.load offset=60
    i32.const 0
    call $f9402)
