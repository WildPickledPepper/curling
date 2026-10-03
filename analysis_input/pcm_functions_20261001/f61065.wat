  (func $f61065 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $p1
    global.set $g0
    i32.const 4675133
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3765356
      call $f1661
      i32.const 3748320
      call $f1661
      i32.const 4675133
      i32.const 1
      i32.store8
    end
    local.get $p1
    i32.const 0
    i32.store offset=12
    i32.const 3748320
    i32.load
    local.tee $l2
    i32.load offset=116
    if $I1 (result i32)
      local.get $l2
    else
      local.get $l2
      call $f65192
      i32.const 3748320
      i32.load
    end
    i32.load offset=92
    i32.load
    local.get $p1
    i32.const 12
    i32.add
    i32.const 3765356
    i32.load
    call $f49306
    if $I2
      local.get $p0
      local.get $p1
      i32.load offset=12
      local.get $p1
      call $f61066
      drop
    end
    local.get $p1
    i32.const 16
    i32.add
    global.set $g0)
