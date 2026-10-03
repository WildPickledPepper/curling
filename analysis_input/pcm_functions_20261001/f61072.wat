  (func $f61072 (type $t16) (param $p0 i32) (param $p1 i32) (result i64)
    (local $l2 i64) (local $l3 f64)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $p0
    global.set $g0
    i32.const 4675135
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3748144
      call $f1661
      i32.const 3748752
      call $f1661
      i32.const 3756320
      call $f1661
      i32.const 4675135
      i32.const 1
      i32.store8
    end
    i32.const 3748752
    i32.load
    local.tee $p1
    i32.load offset=116
    i32.eqz
    if $I1
      local.get $p1
      call $f65192
    end
    i32.const 0
    call $f50492
    local.set $l2
    local.get $p0
    i64.const 0
    i64.store
    local.get $p0
    i32.const 1970
    i32.const 1
    i32.const 1
    i32.const 0
    i32.const 0
    i32.const 0
    i32.const 0
    i32.const 0
    call $f50423
    local.get $p0
    local.get $l2
    local.get $p0
    i64.load
    i32.const 0
    call $f50541
    i64.store offset=8
    i32.const 3756320
    i32.load
    local.tee $p1
    i32.load offset=116
    i32.eqz
    if $I2
      local.get $p1
      call $f65192
    end
    local.get $p0
    i32.const 8
    i32.add
    i32.const 0
    call $f57094
    local.set $l3
    i32.const 3748144
    i32.load
    local.tee $p1
    i32.load offset=116
    i32.eqz
    if $I3
      local.get $p1
      call $f65192
    end
    local.get $l3
    i32.const 0
    call $f58934
    local.set $l2
    local.get $p0
    i32.const 16
    i32.add
    global.set $g0
    local.get $l2)
