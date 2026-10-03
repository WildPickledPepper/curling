  (func $f78652 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l2
    global.set $g0
    local.get $l2
    local.get $p0
    i32.load16_u
    i32.store16
    local.get $l2
    local.get $p0
    i32.load16_u offset=4
    call $f80305
    i32.load
    i32.store offset=4
    local.get $p0
    i32.load offset=8
    local.set $p0
    local.get $l2
    i32.const 0
    i32.store16 offset=2
    local.get $l2
    local.get $p0
    i32.store offset=8
    local.get $l2
    local.get $p1
    i32.load offset=4
    local.get $p1
    i32.load
    call_indirect $__indirect_function_table (type $t1)
    local.get $l2
    i32.const 16
    i32.add
    global.set $g0)
