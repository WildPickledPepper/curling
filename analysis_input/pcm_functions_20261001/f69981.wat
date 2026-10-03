  (func $f69981 (type $t6) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32)
    (local $l5 i32) (local $l6 f32) (local $l7 f32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 i64)
    global.get $g0
    i32.const 32
    i32.sub
    local.tee $l5
    global.set $g0
    local.get $p3
    f32.load offset=36
    local.set $l9
    local.get $p3
    f32.load offset=40
    local.set $l10
    local.get $p3
    f32.load offset=32
    local.set $l11
    local.get $p3
    f32.load offset=8
    local.set $l12
    local.get $p3
    f32.load offset=4
    local.set $l13
    local.get $p3
    f32.load
    local.set $l14
    local.get $l5
    local.get $p2
    f32.load
    local.get $p3
    f32.load offset=48
    f32.sub
    local.tee $l6
    local.get $p3
    f32.load offset=16
    f32.mul
    local.get $p2
    f32.load offset=4
    local.get $p3
    f32.load offset=52
    f32.sub
    local.tee $l7
    local.get $p3
    f32.load offset=20
    f32.mul
    f32.add
    local.get $p2
    f32.load offset=8
    local.get $p3
    f32.load offset=56
    f32.sub
    local.tee $l8
    local.get $p3
    f32.load offset=24
    f32.mul
    f32.add
    f32.store offset=20
    local.get $l5
    local.get $l6
    local.get $l14
    f32.mul
    local.get $l7
    local.get $l13
    f32.mul
    f32.add
    local.get $l8
    local.get $l12
    f32.mul
    f32.add
    f32.store offset=16
    local.get $l5
    i32.const 0
    i32.store offset=28
    local.get $l5
    local.get $l6
    local.get $l11
    f32.mul
    local.get $l7
    local.get $l9
    f32.mul
    f32.add
    local.get $l8
    local.get $l10
    f32.mul
    f32.add
    f32.store offset=24
    local.get $p2
    f32.load offset=40
    local.set $l6
    local.get $p2
    i64.load offset=32
    local.set $l15
    local.get $l5
    local.get $p2
    f32.load offset=64
    f32.store offset=12
    local.get $l5
    local.get $l6
    f32.store offset=8
    local.get $p0
    local.get $l5
    i64.load offset=24
    i64.store offset=8
    local.get $l5
    local.get $l15
    i64.store
    local.get $p0
    local.get $l5
    i64.load offset=16
    i64.store
    local.get $p0
    local.get $p2
    i64.load offset=24
    i64.store offset=24
    local.get $p0
    local.get $p2
    i64.load offset=16
    i64.store offset=16
    local.get $p0
    local.get $l5
    i64.load offset=8
    i64.store offset=40
    local.get $p0
    local.get $l5
    i64.load
    i64.store offset=32
    local.get $p1
    local.get $l5
    i32.const 16
    i32.add
    local.get $p2
    i32.const 16
    i32.add
    local.get $l5
    local.get $p4
    call $f69973
    drop
    local.get $l5
    i32.const 32
    i32.add
    global.set $g0)