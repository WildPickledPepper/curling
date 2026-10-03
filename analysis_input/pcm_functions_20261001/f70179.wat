  (func $f70179 (type $t4) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32)
    (local $l4 f32) (local $l5 f32) (local $l6 f32) (local $l7 f32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 i32) (local $l17 i32) (local $l18 i32) (local $l19 i32) (local $l20 i32) (local $l21 i32) (local $l22 i32) (local $l23 i32)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l13
    global.set $g0
    local.get $p0
    i32.const 48
    i32.add
    local.tee $l14
    f32.load
    local.set $l7
    local.get $p0
    i32.const 60
    i32.add
    local.tee $l15
    f32.load
    local.set $l8
    local.get $p0
    i32.const -64
    i32.sub
    local.tee $l16
    f32.load
    local.set $l9
    local.get $p0
    i32.const 40
    i32.add
    local.tee $l17
    f32.load
    local.set $l10
    local.get $p0
    i32.const 52
    i32.add
    local.tee $l18
    f32.load
    local.set $l11
    local.get $p0
    f32.load offset=36
    local.set $l12
    local.get $p3
    local.get $p2
    f32.load
    local.tee $l4
    local.get $p3
    f32.load
    f32.mul
    local.tee $l5
    local.get $p0
    i32.const 44
    i32.add
    local.tee $l19
    f32.load
    f32.mul
    local.get $l4
    local.get $p3
    f32.load offset=4
    f32.mul
    local.tee $l6
    local.get $p0
    i32.const 56
    i32.add
    local.tee $l20
    f32.load
    f32.mul
    f32.add
    local.get $l4
    local.get $p3
    f32.load offset=8
    f32.mul
    local.tee $l4
    local.get $p0
    i32.const 68
    i32.add
    local.tee $l21
    f32.load
    f32.mul
    f32.add
    f32.store offset=8
    local.get $p3
    local.get $l5
    local.get $l10
    f32.mul
    local.get $l6
    local.get $l11
    f32.mul
    f32.add
    local.get $l4
    local.get $l9
    f32.mul
    f32.add
    f32.store offset=4
    local.get $p3
    local.get $l5
    local.get $l12
    f32.mul
    local.get $l6
    local.get $l7
    f32.mul
    f32.add
    local.get $l4
    local.get $l8
    f32.mul
    f32.add
    f32.store
    local.get $l14
    f32.load
    local.set $l7
    local.get $l15
    f32.load
    local.set $l8
    local.get $l16
    f32.load
    local.set $l9
    local.get $l17
    f32.load
    local.set $l10
    local.get $l18
    f32.load
    local.set $l11
    local.get $p0
    f32.load offset=36
    local.set $l12
    local.get $p3
    i32.const 20
    i32.add
    local.tee $l22
    local.get $p2
    f32.load offset=4
    local.tee $l4
    local.get $p3
    f32.load offset=12
    f32.mul
    local.tee $l5
    local.get $l19
    f32.load
    f32.mul
    local.get $l4
    local.get $p3
    i32.const 16
    i32.add
    local.tee $l23
    f32.load
    f32.mul
    local.tee $l6
    local.get $l20
    f32.load
    f32.mul
    f32.add
    local.get $l4
    local.get $l22
    f32.load
    f32.mul
    local.tee $l4
    local.get $l21
    f32.load
    f32.mul
    f32.add
    f32.store
    local.get $l23
    local.get $l5
    local.get $l10
    f32.mul
    local.get $l6
    local.get $l11
    f32.mul
    f32.add
    local.get $l4
    local.get $l9
    f32.mul
    f32.add
    f32.store
    local.get $p3
    local.get $l5
    local.get $l12
    f32.mul
    local.get $l6
    local.get $l7
    f32.mul
    f32.add
    local.get $l4
    local.get $l8
    f32.mul
    f32.add
    f32.store offset=12
    local.get $l14
    f32.load
    local.set $l7
    local.get $l15
    f32.load
    local.set $l8
    local.get $l16
    f32.load
    local.set $l9
    local.get $l17
    f32.load
    local.set $l10
    local.get $l18
    f32.load
    local.set $l11
    local.get $p0
    f32.load offset=36
    local.set $l12
    local.get $p3
    i32.const 32
    i32.add
    local.tee $l22
    local.get $p2
    f32.load offset=8
    local.tee $l4
    local.get $p3
    f32.load offset=24
    f32.mul
    local.tee $l5
    local.get $l19
    f32.load
    f32.mul
    local.get $l4
    local.get $p3
    i32.const 28
    i32.add
    local.tee $l23
    f32.load
    f32.mul
    local.tee $l6
    local.get $l20
    f32.load
    f32.mul
    f32.add
    local.get $l4
    local.get $l22
    f32.load
    f32.mul
    local.tee $l4
    local.get $l21
    f32.load
    f32.mul
    f32.add
    f32.store
    local.get $l23
    local.get $l5
    local.get $l10
    f32.mul
    local.get $l6
    local.get $l11
    f32.mul
    f32.add
    local.get $l4
    local.get $l9
    f32.mul
    f32.add
    f32.store
    local.get $p3
    local.get $l5
    local.get $l12
    f32.mul
    local.get $l6
    local.get $l7
    f32.mul
    f32.add
    local.get $l4
    local.get $l8
    f32.mul
    f32.add
    f32.store offset=24
    local.get $l15
    f32.load
    local.set $l7
    local.get $l14
    f32.load
    local.set $l8
    local.get $l16
    f32.load
    local.set $l9
    local.get $l17
    f32.load
    local.set $l10
    local.get $l18
    f32.load
    local.set $l11
    local.get $p0
    f32.load offset=36
    local.set $l12
    local.get $p1
    local.get $p1
    f32.load
    local.tee $l4
    local.get $l19
    f32.load
    f32.mul
    local.get $p1
    f32.load offset=4
    local.tee $l5
    local.get $l20
    f32.load
    f32.mul
    f32.add
    local.get $p1
    f32.load offset=8
    local.tee $l6
    local.get $l21
    f32.load
    f32.mul
    f32.add
    f32.store offset=8
    local.get $p1
    local.get $l4
    local.get $l10
    f32.mul
    local.get $l5
    local.get $l11
    f32.mul
    f32.add
    local.get $l6
    local.get $l9
    f32.mul
    f32.add
    f32.store offset=4
    local.get $p1
    local.get $l4
    local.get $l12
    f32.mul
    local.get $l5
    local.get $l8
    f32.mul
    f32.add
    local.get $l6
    local.get $l7
    f32.mul
    f32.add
    f32.store
    local.get $l13
    local.get $p3
    call $f69769
    local.get $p2
    local.get $l13
    f32.load
    f32.store
    local.get $p2
    local.get $l13
    f32.load offset=4
    f32.store offset=4
    local.get $p2
    local.get $l13
    f32.load offset=8
    f32.store offset=8
    local.get $l13
    i32.const 16
    i32.add
    global.set $g0)