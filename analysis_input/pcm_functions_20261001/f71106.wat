  (func $f71106 (type $t1) (param $p0 i32) (param $p1 i32)
    local.get $p1
    local.get $p0
    i32.load8_u offset=12
    i32.store16 offset=20
    local.get $p1
    local.get $p0
    i32.load offset=8
    i32.store offset=28
    local.get $p0
    i32.load8_u offset=12
    drop)