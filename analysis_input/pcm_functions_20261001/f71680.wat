  (func $f71680 (type $t9) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (result i32)
    local.get $p0
    i32.const 0
    i32.store8 offset=22
    local.get $p0
    local.get $p4
    i32.store8 offset=21
    local.get $p0
    local.get $p3
    i32.store8 offset=20
    local.get $p0
    i32.const -1
    i32.store offset=16
    local.get $p0
    i64.const -1
    i64.store offset=8 align=4
    local.get $p0
    local.get $p2
    i32.store offset=4
    local.get $p0
    local.get $p1
    i32.store
    local.get $p0)