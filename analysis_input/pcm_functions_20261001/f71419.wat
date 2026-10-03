  (func $f71419 (type $t5) (param $p0 i32) (result i32)
    local.get $p0
    i32.load offset=4
    local.tee $p0
    i32.const 0
    local.get $p0
    i32.load offset=44
    i32.load8_u offset=9
    i32.const 1
    i32.sub
    i32.const 2
    i32.lt_u
    select)