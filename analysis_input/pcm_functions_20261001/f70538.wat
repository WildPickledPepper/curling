  (func $f70538 (type $t11) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32)
    (local $l6 f32) (local $l7 f32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 i32) (local $l31 i32) (local $l32 i32) (local $l33 i32) (local $l34 i32) (local $l35 i32) (local $l36 i32)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l30
    global.set $g0
    local.get $p4
    f32.load offset=40
    local.set $l11
    local.get $p4
    f32.load offset=24
    local.set $l12
    local.get $p4
    f32.load offset=36
    local.set $l7
    local.get $p4
    f32.load offset=20
    local.set $l13
    local.get $p4
    f32.load offset=8
    local.set $l14
    local.get $p4
    f32.load offset=4
    local.set $l15
    local.get $p4
    f32.load offset=32
    local.set $l8
    local.get $p2
    f32.load offset=8
    local.set $l6
    local.get $p4
    f32.load
    local.set $l16
    local.get $p2
    f32.load
    local.set $l9
    local.get $p4
    f32.load offset=16
    local.set $l17
    local.get $p2
    f32.load offset=4
    local.set $l10
    local.get $p1
    i32.const 56
    i32.add
    local.tee $p4
    f32.load
    local.set $l18
    local.get $p1
    i32.const 52
    i32.add
    local.tee $p2
    f32.load
    local.set $l19
    local.get $p1
    i32.const 72
    i32.add
    local.tee $l31
    f32.load
    local.set $l20
    local.get $p1
    i32.const 68
    i32.add
    local.tee $l32
    f32.load
    local.set $l21
    local.get $p1
    i32.const -64
    i32.sub
    local.tee $l33
    f32.load
    local.set $l22
    local.get $p1
    i32.const 88
    i32.add
    local.tee $l34
    f32.load
    local.set $l23
    local.get $p1
    i32.const 84
    i32.add
    local.tee $l35
    f32.load
    local.set $l24
    local.get $p1
    i32.const 80
    i32.add
    local.tee $l36
    f32.load
    local.set $l25
    local.get $p1
    f32.load offset=48
    local.set $l26
    local.get $l30
    i32.const 0
    i32.store offset=12
    local.get $l30
    local.get $l25
    local.get $l9
    local.get $l16
    f32.mul
    local.get $l10
    local.get $l17
    f32.mul
    f32.add
    local.get $l6
    local.get $l8
    f32.mul
    f32.add
    local.tee $l8
    f32.mul
    local.get $l24
    local.get $l9
    local.get $l15
    f32.mul
    local.get $l10
    local.get $l13
    f32.mul
    f32.add
    local.get $l6
    local.get $l7
    f32.mul
    f32.add
    local.tee $l7
    f32.mul
    f32.add
    local.get $l23
    local.get $l9
    local.get $l14
    f32.mul
    local.get $l10
    local.get $l12
    f32.mul
    f32.add
    local.get $l6
    local.get $l11
    f32.mul
    f32.add
    local.tee $l6
    f32.mul
    f32.add
    f32.store offset=8
    local.get $l30
    local.get $l8
    local.get $l22
    f32.mul
    local.get $l7
    local.get $l21
    f32.mul
    f32.add
    local.get $l6
    local.get $l20
    f32.mul
    f32.add
    f32.store offset=4
    local.get $l30
    local.get $l8
    local.get $l26
    f32.mul
    local.get $l7
    local.get $l19
    f32.mul
    f32.add
    local.get $l6
    local.get $l18
    f32.mul
    f32.add
    f32.store
    local.get $p5
    local.get $p1
    local.get $l30
    call $f70525
    local.tee $p5
    i32.store
    local.get $l34
    f32.load
    local.set $l11
    local.get $p4
    f32.load
    local.set $l12
    local.get $l31
    f32.load
    local.set $l13
    local.get $l33
    f32.load
    local.set $l8
    local.get $l36
    f32.load
    local.set $l7
    local.get $l35
    f32.load
    local.set $l14
    local.get $p1
    i32.load offset=152
    local.get $p5
    i32.const 12
    i32.mul
    i32.add
    local.tee $p4
    f32.load offset=8
    local.set $l6
    local.get $p2
    f32.load
    local.set $l15
    local.get $p4
    f32.load
    local.set $l9
    local.get $l32
    f32.load
    local.set $l16
    local.get $p4
    f32.load offset=4
    local.set $l10
    local.get $p1
    f32.load offset=48
    local.set $l17
    local.get $p3
    f32.load offset=52
    local.set $l18
    local.get $p3
    f32.load offset=36
    local.set $l19
    local.get $p3
    f32.load offset=20
    local.set $l20
    local.get $p3
    f32.load offset=56
    local.set $l21
    local.get $p3
    f32.load offset=40
    local.set $l22
    local.get $p3
    f32.load offset=24
    local.set $l23
    local.get $p3
    f32.load offset=48
    local.set $l24
    local.get $p3
    f32.load offset=32
    local.set $l25
    local.get $p3
    f32.load
    local.set $l26
    local.get $p3
    f32.load offset=16
    local.set $l27
    local.get $p3
    f32.load offset=4
    local.set $l28
    local.get $p3
    f32.load offset=8
    local.set $l29
    local.get $p0
    i32.const 0
    i32.store offset=12
    local.get $p0
    local.get $l21
    local.get $l29
    local.get $l9
    local.get $l17
    f32.mul
    local.get $l10
    local.get $l8
    f32.mul
    f32.add
    local.get $l6
    local.get $l7
    f32.mul
    f32.add
    local.tee $l8
    f32.mul
    local.get $l23
    local.get $l9
    local.get $l15
    f32.mul
    local.get $l10
    local.get $l16
    f32.mul
    f32.add
    local.get $l6
    local.get $l14
    f32.mul
    f32.add
    local.tee $l7
    f32.mul
    f32.add
    local.get $l22
    local.get $l9
    local.get $l12
    f32.mul
    local.get $l10
    local.get $l13
    f32.mul
    f32.add
    local.get $l6
    local.get $l11
    f32.mul
    f32.add
    local.tee $l6
    f32.mul
    f32.add
    f32.add
    f32.store offset=8
    local.get $p0
    local.get $l18
    local.get $l8
    local.get $l28
    f32.mul
    local.get $l7
    local.get $l20
    f32.mul
    f32.add
    local.get $l6
    local.get $l19
    f32.mul
    f32.add
    f32.add
    f32.store offset=4
    local.get $p0
    local.get $l24
    local.get $l8
    local.get $l26
    f32.mul
    local.get $l7
    local.get $l27
    f32.mul
    f32.add
    local.get $l6
    local.get $l25
    f32.mul
    f32.add
    f32.add
    f32.store
    local.get $l30
    i32.const 16
    i32.add
    global.set $g0)