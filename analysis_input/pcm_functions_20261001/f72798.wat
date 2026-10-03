  (func $f72798 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 f32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32)
    global.get $g0
    i32.const 48
    i32.sub
    local.tee $l3
    global.set $g0
    local.get $p0
    f32.load offset=16
    local.set $l7
    local.get $p0
    f32.load offset=20
    local.set $l8
    local.get $p1
    f32.load offset=16
    local.set $l9
    local.get $p1
    f32.load offset=28
    local.set $l10
    local.get $p0
    f32.load offset=28
    local.set $l11
    local.get $p1
    f32.load offset=20
    local.set $l12
    local.get $p0
    f32.load offset=32
    local.set $l13
    local.get $p1
    f32.load offset=32
    local.set $l14
    local.get $p0
    f32.load offset=12
    local.set $l15
    local.get $p1
    f32.load offset=4
    local.set $l16
    local.get $p0
    f32.load offset=24
    local.set $l17
    local.get $p1
    f32.load offset=8
    local.set $l18
    local.get $l3
    i32.const 8
    i32.add
    local.tee $l2
    local.get $p0
    f32.load
    local.tee $l19
    local.get $p1
    f32.load
    local.tee $l20
    f32.mul
    local.get $p0
    f32.load offset=4
    local.tee $l21
    local.get $p1
    f32.load offset=12
    local.tee $l22
    f32.mul
    f32.add
    local.get $p0
    f32.load offset=8
    local.tee $l23
    local.get $p1
    f32.load offset=24
    local.tee $l24
    f32.mul
    f32.add
    f32.store
    local.get $l2
    local.get $l18
    local.get $l17
    f32.mul
    local.get $l12
    local.get $l11
    f32.mul
    f32.add
    local.get $l14
    local.get $l13
    f32.mul
    f32.add
    f32.store offset=32
    local.get $l2
    local.get $l16
    local.get $l17
    f32.mul
    local.get $l9
    local.get $l11
    f32.mul
    f32.add
    local.get $l10
    local.get $l13
    f32.mul
    f32.add
    f32.store offset=28
    local.get $l2
    local.get $l20
    local.get $l17
    f32.mul
    local.get $l22
    local.get $l11
    f32.mul
    f32.add
    local.get $l24
    local.get $l13
    f32.mul
    f32.add
    f32.store offset=24
    local.get $l2
    local.get $l18
    local.get $l15
    f32.mul
    local.get $l12
    local.get $l7
    f32.mul
    f32.add
    local.get $l14
    local.get $l8
    f32.mul
    f32.add
    f32.store offset=20
    local.get $l2
    local.get $l16
    local.get $l15
    f32.mul
    local.get $l9
    local.get $l7
    f32.mul
    f32.add
    local.get $l10
    local.get $l8
    f32.mul
    f32.add
    f32.store offset=16
    local.get $l2
    local.get $l20
    local.get $l15
    f32.mul
    local.get $l22
    local.get $l7
    f32.mul
    f32.add
    local.get $l24
    local.get $l8
    f32.mul
    f32.add
    f32.store offset=12
    local.get $l2
    local.get $l19
    local.get $l18
    f32.mul
    local.get $l21
    local.get $l12
    f32.mul
    f32.add
    local.get $l23
    local.get $l14
    f32.mul
    f32.add
    f32.store offset=8
    local.get $l2
    local.get $l19
    local.get $l16
    f32.mul
    local.get $l21
    local.get $l9
    f32.mul
    f32.add
    local.get $l23
    local.get $l10
    f32.mul
    f32.add
    f32.store offset=4
    local.get $p1
    i32.const 28
    i32.add
    local.tee $l2
    f32.load
    local.set $l7
    local.get $p1
    i32.const 16
    i32.add
    local.tee $l4
    f32.load
    local.set $l8
    local.get $p1
    f32.load offset=24
    local.set $l9
    local.get $p1
    f32.load
    local.set $l10
    local.get $p1
    f32.load offset=12
    local.set $l11
    local.get $p1
    f32.load offset=4
    local.set $l12
    local.get $l3
    f32.load offset=36
    local.set $l13
    local.get $l3
    f32.load offset=24
    local.set $l14
    local.get $l3
    f32.load offset=32
    local.set $l15
    local.get $l3
    f32.load offset=8
    local.set $l16
    local.get $l3
    f32.load offset=20
    local.set $l17
    local.get $l3
    f32.load offset=12
    local.set $l18
    local.get $p0
    local.get $p1
    f32.load offset=8
    local.tee $l19
    local.get $l3
    f32.load offset=16
    local.tee $l20
    f32.mul
    local.get $p1
    i32.const 20
    i32.add
    local.tee $l5
    f32.load
    local.tee $l21
    local.get $l3
    f32.load offset=28
    local.tee $l22
    f32.mul
    f32.add
    local.get $p1
    i32.const 32
    i32.add
    local.tee $l6
    f32.load
    local.tee $l23
    local.get $l3
    f32.load offset=40
    local.tee $l24
    f32.mul
    f32.add
    f32.store offset=32
    local.get $p0
    local.get $l19
    local.get $l18
    f32.mul
    local.get $l21
    local.get $l14
    f32.mul
    f32.add
    local.get $l23
    local.get $l13
    f32.mul
    f32.add
    f32.store offset=28
    local.get $p0
    local.get $l19
    local.get $l16
    f32.mul
    local.get $l21
    local.get $l17
    f32.mul
    f32.add
    local.get $l23
    local.get $l15
    f32.mul
    f32.add
    f32.store offset=24
    local.get $p0
    local.get $l12
    local.get $l20
    f32.mul
    local.get $l8
    local.get $l22
    f32.mul
    f32.add
    local.get $l7
    local.get $l24
    f32.mul
    f32.add
    f32.store offset=20
    local.get $p0
    local.get $l12
    local.get $l18
    f32.mul
    local.get $l8
    local.get $l14
    f32.mul
    f32.add
    local.get $l7
    local.get $l13
    f32.mul
    f32.add
    f32.store offset=16
    local.get $p0
    local.get $l12
    local.get $l16
    f32.mul
    local.get $l8
    local.get $l17
    f32.mul
    f32.add
    local.get $l7
    local.get $l15
    f32.mul
    f32.add
    f32.store offset=12
    local.get $p0
    local.get $l10
    local.get $l20
    f32.mul
    local.get $l11
    local.get $l22
    f32.mul
    f32.add
    local.get $l9
    local.get $l24
    f32.mul
    f32.add
    f32.store offset=8
    local.get $p0
    local.get $l10
    local.get $l18
    f32.mul
    local.get $l11
    local.get $l14
    f32.mul
    f32.add
    local.get $l9
    local.get $l13
    f32.mul
    f32.add
    f32.store offset=4
    local.get $p0
    local.get $l10
    local.get $l16
    f32.mul
    local.get $l11
    local.get $l17
    f32.mul
    f32.add
    local.get $l9
    local.get $l15
    f32.mul
    f32.add
    f32.store
    local.get $l4
    f32.load
    local.set $l10
    local.get $l2
    f32.load
    local.set $l11
    local.get $p1
    f32.load offset=24
    local.set $l12
    local.get $p1
    f32.load
    local.set $l13
    local.get $p1
    f32.load offset=12
    local.set $l14
    local.get $p1
    f32.load offset=4
    local.set $l15
    local.get $p0
    i32.const 44
    i32.add
    local.tee $l2
    local.get $p0
    f32.load offset=36
    local.tee $l7
    local.get $p1
    f32.load offset=8
    f32.mul
    local.get $p0
    i32.const 40
    i32.add
    local.tee $p1
    f32.load
    local.tee $l8
    local.get $l5
    f32.load
    f32.mul
    f32.add
    local.get $l2
    f32.load
    local.tee $l9
    local.get $l6
    f32.load
    f32.mul
    f32.add
    f32.store
    local.get $p1
    local.get $l7
    local.get $l15
    f32.mul
    local.get $l8
    local.get $l10
    f32.mul
    f32.add
    local.get $l9
    local.get $l11
    f32.mul
    f32.add
    f32.store
    local.get $p0
    local.get $l7
    local.get $l13
    f32.mul
    local.get $l8
    local.get $l14
    f32.mul
    f32.add
    local.get $l9
    local.get $l12
    f32.mul
    f32.add
    f32.store offset=36
    local.get $l3
    i32.const 48
    i32.add
    global.set $g0)