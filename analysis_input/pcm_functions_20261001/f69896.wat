  (func $f69896 (type $t11) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32)
    (local $l6 f32) (local $l7 f32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32)
    local.get $p4
    local.get $p2
    f32.load
    local.tee $l19
    local.get $p1
    f32.load
    local.tee $l9
    f32.sub
    local.tee $l15
    local.get $p3
    f32.load offset=4
    local.tee $l13
    local.get $p1
    f32.load offset=4
    local.tee $l6
    f32.sub
    local.tee $l14
    f32.mul
    local.get $p2
    f32.load offset=4
    local.tee $l20
    local.get $l6
    f32.sub
    local.tee $l7
    local.get $p3
    f32.load
    local.tee $l8
    local.get $l9
    f32.sub
    local.tee $l16
    f32.mul
    f32.sub
    local.tee $l17
    local.get $l8
    local.get $p0
    f32.load
    local.tee $l10
    f32.sub
    local.tee $l8
    local.get $l6
    local.get $p0
    f32.load offset=4
    local.tee $l11
    f32.sub
    local.tee $l6
    f32.mul
    local.get $l9
    local.get $l10
    f32.sub
    local.tee $l9
    local.get $l13
    local.get $l11
    f32.sub
    local.tee $l13
    f32.mul
    f32.sub
    f32.mul
    local.get $l7
    local.get $p3
    f32.load offset=8
    local.tee $l21
    local.get $p1
    f32.load offset=8
    local.tee $l12
    f32.sub
    local.tee $l22
    f32.mul
    local.get $p2
    f32.load offset=8
    local.tee $l23
    local.get $l12
    f32.sub
    local.tee $l24
    local.get $l14
    f32.mul
    f32.sub
    local.tee $l18
    local.get $l13
    local.get $l12
    local.get $p0
    f32.load offset=8
    local.tee $l7
    f32.sub
    local.tee $l12
    f32.mul
    local.get $l6
    local.get $l21
    local.get $l7
    f32.sub
    local.tee $l14
    f32.mul
    f32.sub
    f32.mul
    local.get $l24
    local.get $l16
    f32.mul
    local.get $l15
    local.get $l22
    f32.mul
    f32.sub
    local.tee $l15
    local.get $l9
    local.get $l14
    f32.mul
    local.get $l8
    local.get $l12
    f32.mul
    f32.sub
    f32.mul
    f32.add
    f32.add
    local.tee $l16
    f32.const 0x1p+0 (;=1;)
    local.get $l17
    local.get $l19
    local.get $l10
    f32.sub
    local.tee $l10
    local.get $l13
    f32.mul
    local.get $l8
    local.get $l20
    local.get $l11
    f32.sub
    local.tee $l11
    f32.mul
    f32.sub
    f32.mul
    local.get $l18
    local.get $l11
    local.get $l14
    f32.mul
    local.get $l13
    local.get $l23
    local.get $l7
    f32.sub
    local.tee $l7
    f32.mul
    f32.sub
    f32.mul
    local.get $l15
    local.get $l8
    local.get $l7
    f32.mul
    local.get $l10
    local.get $l14
    f32.mul
    f32.sub
    f32.mul
    f32.add
    f32.add
    local.get $l16
    local.get $l17
    local.get $l9
    local.get $l11
    f32.mul
    local.get $l10
    local.get $l6
    f32.mul
    f32.sub
    f32.mul
    local.get $l18
    local.get $l6
    local.get $l7
    f32.mul
    local.get $l11
    local.get $l12
    f32.mul
    f32.sub
    f32.mul
    local.get $l15
    local.get $l10
    local.get $l12
    f32.mul
    local.get $l9
    local.get $l7
    f32.mul
    f32.sub
    f32.mul
    f32.add
    f32.add
    local.tee $l8
    f32.add
    f32.add
    local.tee $l6
    f32.div
    f32.const 0x0p+0 (;=0;)
    local.get $l6
    f32.const 0x0p+0 (;=0;)
    f32.ne
    select
    local.tee $l6
    f32.mul
    f32.store
    local.get $p5
    local.get $l8
    local.get $l6
    f32.mul
    f32.store)