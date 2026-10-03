  (func $f78462 (type $t0) (param $p0 i32) (param $p1 i32) (result i32)
    (local $l2 f32)
    local.get $p0
    local.get $p1
    f32.load
    f32.store
    local.get $p0
    local.get $p1
    f32.load offset=4
    f32.store offset=4
    local.get $p1
    f32.load offset=8
    local.set $l2
    local.get $p0
    i32.const 0
    i32.store offset=12
    local.get $p0
    local.get $l2
    f32.store offset=8
    local.get $p0
    local.get $p1
    f32.load offset=12
    f32.store offset=16
    local.get $p0
    local.get $p1
    f32.load offset=16
    f32.store offset=20
    local.get $p1
    f32.load offset=20
    local.set $l2
    local.get $p0
    i32.const 0
    i32.store offset=28
    local.get $p0
    local.get $l2
    f32.store offset=24
    local.get $p0
    local.get $p1
    f32.load offset=24
    f32.store offset=32
    local.get $p0
    local.get $p1
    f32.load offset=28
    f32.store offset=36
    local.get $p1
    f32.load offset=32
    local.set $l2
    local.get $p0
    i64.const 0
    i64.store offset=44 align=4
    local.get $p0
    local.get $l2
    f32.store offset=40
    local.get $p0
    i64.const 0
    i64.store offset=52 align=4
    local.get $p0
    i32.const 1065353216
    i32.store offset=60
    local.get $p0)
