  (func $f72779 (type $t2) (param $p0 i32) (param $p1 i32) (param $p2 i32)
    (local $l3 f32) (local $l4 f32) (local $l5 f32) (local $l6 f32) (local $l7 f32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32)
    local.get $p0
    local.get $p2
    f32.load
    local.tee $l8
    local.get $l8
    f32.add
    local.tee $l7
    local.get $p2
    f32.load offset=8
    local.tee $l4
    f32.mul
    local.tee $l15
    local.get $p2
    f32.load offset=4
    local.tee $l3
    local.get $l3
    f32.add
    local.tee $l5
    local.get $p2
    f32.load offset=12
    local.tee $l6
    f32.mul
    local.tee $l25
    f32.sub
    local.tee $l9
    local.get $l9
    local.get $p1
    f32.load
    local.tee $l12
    f32.mul
    local.get $p1
    f32.load offset=4
    local.tee $l17
    local.get $l5
    local.get $l4
    f32.mul
    local.tee $l26
    local.get $l7
    local.get $l6
    f32.mul
    local.tee $l27
    f32.add
    local.tee $l10
    f32.mul
    f32.add
    f32.const 0x1p+0 (;=1;)
    local.get $l8
    local.get $l7
    f32.mul
    f32.sub
    local.tee $l16
    local.get $l3
    local.get $l5
    f32.mul
    local.tee $l5
    f32.sub
    local.tee $l8
    local.get $p1
    f32.load offset=8
    local.tee $l18
    f32.mul
    f32.add
    local.tee $l11
    f32.mul
    local.get $l10
    local.get $l9
    local.get $p1
    f32.load offset=12
    local.tee $l19
    f32.mul
    local.get $l10
    local.get $p1
    f32.load offset=16
    local.tee $l20
    f32.mul
    f32.add
    local.get $l8
    local.get $p1
    f32.load offset=20
    local.tee $l21
    f32.mul
    f32.add
    local.tee $l13
    f32.mul
    f32.add
    local.get $l8
    local.get $l9
    local.get $p1
    f32.load offset=24
    local.tee $l22
    f32.mul
    local.get $l10
    local.get $p1
    f32.load offset=28
    local.tee $l23
    f32.mul
    f32.add
    local.get $l8
    local.get $p1
    f32.load offset=32
    local.tee $l24
    f32.mul
    f32.add
    local.tee $l14
    f32.mul
    f32.add
    f32.store offset=32
    local.get $p0
    local.get $l7
    local.get $l3
    f32.mul
    local.tee $l28
    local.get $l6
    local.get $l4
    local.get $l4
    f32.add
    local.tee $l3
    f32.mul
    local.tee $l6
    f32.add
    local.tee $l7
    local.get $l11
    f32.mul
    local.get $l16
    local.get $l4
    local.get $l3
    f32.mul
    local.tee $l16
    f32.sub
    local.tee $l4
    local.get $l13
    f32.mul
    f32.add
    local.get $l26
    local.get $l27
    f32.sub
    local.tee $l3
    local.get $l14
    f32.mul
    f32.add
    f32.store offset=20
    local.get $p0
    f32.const 0x1p+0 (;=1;)
    local.get $l5
    f32.sub
    local.get $l16
    f32.sub
    local.tee $l5
    local.get $l11
    f32.mul
    local.get $l28
    local.get $l6
    f32.sub
    local.tee $l6
    local.get $l13
    f32.mul
    f32.add
    local.get $l15
    local.get $l25
    f32.add
    local.tee $l11
    local.get $l14
    f32.mul
    f32.add
    f32.store offset=8
    local.get $p0
    local.get $l9
    local.get $l12
    local.get $l7
    f32.mul
    local.get $l17
    local.get $l4
    f32.mul
    f32.add
    local.get $l3
    local.get $l18
    f32.mul
    f32.add
    local.tee $l13
    f32.mul
    local.get $l10
    local.get $l7
    local.get $l19
    f32.mul
    local.get $l4
    local.get $l20
    f32.mul
    f32.add
    local.get $l3
    local.get $l21
    f32.mul
    f32.add
    local.tee $l14
    f32.mul
    f32.add
    local.get $l8
    local.get $l7
    local.get $l22
    f32.mul
    local.get $l4
    local.get $l23
    f32.mul
    f32.add
    local.get $l3
    local.get $l24
    f32.mul
    f32.add
    local.tee $l15
    f32.mul
    f32.add
    f32.store offset=28
    local.get $p0
    local.get $l9
    local.get $l12
    local.get $l5
    f32.mul
    local.get $l17
    local.get $l6
    f32.mul
    f32.add
    local.get $l11
    local.get $l18
    f32.mul
    f32.add
    local.tee $l12
    f32.mul
    local.get $l10
    local.get $l5
    local.get $l19
    f32.mul
    local.get $l6
    local.get $l20
    f32.mul
    f32.add
    local.get $l11
    local.get $l21
    f32.mul
    f32.add
    local.tee $l9
    f32.mul
    f32.add
    local.get $l8
    local.get $l5
    local.get $l22
    f32.mul
    local.get $l6
    local.get $l23
    f32.mul
    f32.add
    local.get $l11
    local.get $l24
    f32.mul
    f32.add
    local.tee $l10
    f32.mul
    f32.add
    f32.store offset=24
    local.get $p0
    local.get $l7
    local.get $l13
    f32.mul
    local.get $l4
    local.get $l14
    f32.mul
    f32.add
    local.get $l3
    local.get $l15
    f32.mul
    f32.add
    f32.store offset=16
    local.get $p0
    local.get $l7
    local.get $l12
    f32.mul
    local.get $l4
    local.get $l9
    f32.mul
    f32.add
    local.get $l3
    local.get $l10
    f32.mul
    f32.add
    f32.store offset=12
    local.get $p0
    local.get $l5
    local.get $l13
    f32.mul
    local.get $l6
    local.get $l14
    f32.mul
    f32.add
    local.get $l11
    local.get $l15
    f32.mul
    f32.add
    f32.store offset=4
    local.get $p0
    local.get $l5
    local.get $l12
    f32.mul
    local.get $l6
    local.get $l9
    f32.mul
    f32.add
    local.get $l11
    local.get $l10
    f32.mul
    f32.add
    f32.store)