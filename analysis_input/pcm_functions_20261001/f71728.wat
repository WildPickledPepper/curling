  (func $f71728 (type $t7) (param $p0 i32)
    (local $l1 i32)
    local.get $p0
    i32.const 3172120
    i32.store
    local.get $p0
    i32.load offset=40
    i32.load offset=2372
    local.get $p0
    i32.load offset=48
    call $f71674
    local.get $p0
    call $f71330
    drop
    call $f69753
    local.tee $l1
    local.get $p0
    local.get $l1
    i32.load
    i32.load offset=12
    call_indirect $__indirect_function_table (type $t1))