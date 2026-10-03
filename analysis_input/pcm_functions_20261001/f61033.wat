  (func $f61033 (type $t2) (param $p0 i32) (param $p1 i32) (param $p2 i32)
    (local $l3 i32) (local $l4 i32)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $p2
    global.set $g0
    i32.const 4675112
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3748808
      call $f1661
      i32.const 3813952
      call $f1661
      i32.const 3814256
      call $f1661
      i32.const 3836212
      call $f1661
      i32.const 4675112
      i32.const 1
      i32.store8
    end
    local.get $p2
    local.get $p1
    i32.const 3813952
    i32.load
    i32.const 0
    call $f53732
    local.tee $p1
    i32.load offset=8
    i32.store offset=12
    local.get $p2
    i32.const 12
    i32.add
    i32.const 0
    call $f56590
    local.set $l3
    i32.const 3836212
    i32.load
    local.get $p1
    i32.const 3814256
    i32.load
    local.get $l3
    i32.const 0
    call $f53874
    local.set $l3
    i32.const 3748808
    i32.load
    local.tee $l4
    i32.load offset=116
    i32.eqz
    if $I1
      local.get $l4
      call $f65192
    end
    local.get $l3
    i32.const 0
    call $f42976
    local.get $p0
    i32.load offset=8
    i32.const 0
    call $f53201
    local.tee $p0
    local.get $p1
    local.get $p0
    i32.load
    local.tee $p0
    i32.load offset=348
    local.get $p0
    i32.load offset=344
    call_indirect $__indirect_function_table (type $t3)
    i32.const 0
    call $f59734
    local.get $p2
    i32.const 16
    i32.add
    global.set $g0)
