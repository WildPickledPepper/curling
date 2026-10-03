  (func $f78655 (type $t1) (param $p0 i32) (param $p1 i32)
    local.get $p0
    local.get $p1
    i32.load offset=4
    local.get $p1
    i32.load
    call_indirect $__indirect_function_table (type $t1))
