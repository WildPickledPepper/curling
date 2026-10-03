  (func $f71744 (type $t7) (param $p0 i32)
    (local $l1 i32)
    local.get $p0
    call $f71741
    local.set $p0
    call $f69753
    local.tee $l1
    local.get $p0
    local.get $l1
    i32.load
    i32.load offset=12
    call_indirect $__indirect_function_table (type $t1))