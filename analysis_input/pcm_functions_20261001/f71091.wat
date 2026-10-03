  (func $f71091 (type $t6) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32)
    (local $l5 i32) (local $l6 f32) (local $l7 f32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32) (local $l33 f32) (local $l34 f32) (local $l35 f32) (local $l36 f32) (local $l37 f32) (local $l38 f32) (local $l39 f32) (local $l40 f32) (local $l41 f32) (local $l42 f32) (local $l43 f32) (local $l44 f32) (local $l45 f32) (local $l46 f32) (local $l47 f32) (local $l48 f32) (local $l49 f32) (local $l50 f32)
    global.get $g0
    i32.const 240
    i32.sub
    local.tee $l5
    global.set $g0
    local.get $l5
    local.get $p1
    local.get $p2
    local.get $l5
    i32.const 144
    i32.add
    call $f71056
    local.get $p3
    f32.load
    local.set $l9
    local.get $p3
    f32.load offset=4
    local.set $l7
    local.get $p4
    f32.load
    local.set $l6
    local.get $p3
    f32.load offset=8
    local.set $l10
    local.get $l5
    i32.const 0
    i32.store offset=12
    local.get $l5
    local.get $l10
    local.get $l6
    f32.mul
    local.get $l5
    f32.load offset=8
    f32.add
    local.tee $l11
    f32.store offset=8
    local.get $l5
    local.get $l7
    local.get $l6
    f32.mul
    local.get $l5
    f32.load offset=4
    f32.add
    local.tee $l7
    f32.store offset=4
    local.get $l5
    local.get $l9
    local.get $l6
    f32.mul
    local.get $l5
    f32.load
    f32.add
    local.tee $l9
    f32.store
    local.get $p3
    f32.load offset=20
    local.set $l10
    local.get $p3
    f32.load offset=24
    local.set $l8
    local.get $p3
    f32.load offset=16
    local.set $l12
    local.get $l5
    i32.const 0
    i32.store offset=28
    local.get $l5
    i32.const 24
    i32.add
    local.tee $p4
    local.get $l6
    local.get $l8
    f32.mul
    local.get $p4
    f32.load
    f32.add
    local.tee $l13
    f32.store
    local.get $l5
    i32.const 20
    i32.add
    local.tee $p4
    local.get $l6
    local.get $l10
    f32.mul
    local.get $p4
    f32.load
    f32.add
    local.tee $l10
    f32.store
    local.get $l5
    local.get $l6
    local.get $l12
    f32.mul
    local.get $l5
    f32.load offset=16
    f32.add
    f32.store offset=16
    local.get $p3
    f32.load offset=36
    local.set $l8
    local.get $p3
    f32.load offset=40
    local.set $l12
    local.get $p3
    f32.load offset=32
    local.set $l14
    local.get $l5
    i32.const 0
    i32.store offset=44
    local.get $l5
    i32.const 40
    i32.add
    local.tee $p3
    local.get $l6
    local.get $l12
    f32.mul
    local.get $p3
    f32.load
    f32.add
    local.tee $l24
    f32.store
    local.get $l5
    i32.const 36
    i32.add
    local.tee $p3
    local.get $l6
    local.get $l8
    f32.mul
    local.get $p3
    f32.load
    f32.add
    f32.store
    local.get $l5
    local.get $l6
    local.get $l14
    f32.mul
    local.get $l5
    f32.load offset=32
    f32.add
    f32.store offset=32
    local.get $l5
    f32.load offset=212
    local.set $l25
    local.get $l5
    f32.load offset=216
    local.set $l26
    local.get $l5
    f32.load offset=224
    local.set $l27
    local.get $l5
    f32.load offset=228
    local.set $l28
    local.get $l5
    f32.load offset=232
    local.set $l29
    local.get $l5
    f32.load offset=180
    local.set $l18
    local.get $l5
    f32.load offset=184
    local.set $l19
    local.get $l5
    f32.load offset=192
    local.set $l20
    local.get $l5
    f32.load offset=196
    local.set $l21
    local.get $l5
    f32.load offset=200
    local.set $l22
    local.get $l5
    f32.load offset=164
    local.set $l12
    local.get $l5
    f32.load offset=168
    local.set $l8
    local.get $l5
    f32.load offset=208
    local.set $l30
    local.get $l5
    f32.load offset=176
    local.set $l23
    local.get $l5
    f32.load offset=144
    local.set $l14
    local.get $l5
    f32.load offset=148
    local.set $l15
    local.get $l5
    f32.load offset=152
    local.set $l16
    local.get $l5
    f32.load offset=160
    local.set $l17
    local.get $l5
    i32.const 0
    i32.store offset=140
    local.get $l5
    i32.const 0
    i32.store offset=124
    local.get $l5
    i32.const 0
    i32.store offset=108
    local.get $l5
    i32.const 0
    i32.store offset=92
    local.get $l5
    i32.const 0
    i32.store offset=76
    local.get $l5
    local.get $l8
    f32.const 0x1p+0 (;=1;)
    local.get $l9
    f32.div
    f32.const 0x0p+0 (;=0;)
    f32.max
    f32.sqrt
    local.tee $l6
    f32.mul
    f32.store offset=72
    local.get $l5
    local.get $l6
    local.get $l12
    f32.mul
    f32.store offset=68
    local.get $l5
    local.get $l22
    f32.const 0x1p+0 (;=1;)
    local.get $l10
    local.get $l7
    local.get $l6
    f32.mul
    local.tee $l7
    local.get $l7
    f32.mul
    f32.sub
    f32.div
    f32.const 0x0p+0 (;=0;)
    f32.max
    f32.sqrt
    local.tee $l9
    f32.mul
    local.get $l8
    local.get $l6
    local.get $l7
    f32.mul
    local.get $l9
    f32.mul
    local.tee $l10
    f32.mul
    f32.sub
    f32.store offset=104
    local.get $l5
    local.get $l9
    local.get $l21
    f32.mul
    local.get $l10
    local.get $l12
    f32.mul
    f32.sub
    f32.store offset=100
    local.get $l5
    local.get $l9
    local.get $l20
    f32.mul
    local.get $l10
    local.get $l17
    f32.mul
    f32.sub
    f32.store offset=96
    local.get $l5
    local.get $l9
    local.get $l19
    f32.mul
    local.get $l10
    local.get $l16
    f32.mul
    f32.sub
    f32.store offset=88
    local.get $l5
    local.get $l9
    local.get $l18
    f32.mul
    local.get $l10
    local.get $l15
    f32.mul
    f32.sub
    f32.store offset=84
    local.get $l5
    local.get $l8
    local.get $l13
    local.get $l7
    local.get $l11
    local.get $l6
    f32.mul
    local.tee $l11
    f32.mul
    f32.sub
    local.get $l9
    f32.mul
    local.tee $l13
    local.get $l10
    f32.mul
    local.get $l6
    local.get $l11
    f32.mul
    f32.sub
    f32.const 0x1p+0 (;=1;)
    local.get $l24
    local.get $l13
    local.get $l13
    f32.mul
    f32.sub
    local.get $l11
    local.get $l11
    f32.mul
    f32.sub
    f32.div
    f32.const 0x0p+0 (;=0;)
    f32.max
    f32.sqrt
    local.tee $l7
    f32.mul
    local.tee $l11
    f32.mul
    local.get $l22
    local.get $l9
    local.get $l7
    f32.mul
    local.get $l13
    f32.neg
    f32.mul
    local.tee $l8
    f32.mul
    local.get $l7
    local.get $l29
    f32.mul
    f32.add
    f32.add
    f32.store offset=136
    local.get $l5
    local.get $l11
    local.get $l12
    f32.mul
    local.get $l8
    local.get $l21
    f32.mul
    local.get $l7
    local.get $l28
    f32.mul
    f32.add
    f32.add
    f32.store offset=132
    local.get $l5
    local.get $l11
    local.get $l17
    f32.mul
    local.get $l8
    local.get $l20
    f32.mul
    local.get $l7
    local.get $l27
    f32.mul
    f32.add
    f32.add
    f32.store offset=128
    local.get $l5
    local.get $l16
    local.get $l11
    f32.mul
    local.get $l8
    local.get $l19
    f32.mul
    local.get $l7
    local.get $l26
    f32.mul
    f32.add
    f32.add
    f32.store offset=120
    local.get $l5
    local.get $l15
    local.get $l11
    f32.mul
    local.get $l18
    local.get $l8
    f32.mul
    local.get $l7
    local.get $l25
    f32.mul
    f32.add
    f32.add
    f32.store offset=116
    local.get $l5
    i32.const 0
    i32.store offset=60
    local.get $l5
    local.get $l6
    local.get $l17
    f32.mul
    f32.store offset=64
    local.get $l5
    local.get $l6
    local.get $l16
    f32.mul
    f32.store offset=56
    local.get $l5
    local.get $l6
    local.get $l15
    f32.mul
    f32.store offset=52
    local.get $l5
    local.get $l6
    local.get $l14
    f32.mul
    f32.store offset=48
    local.get $l5
    local.get $l9
    local.get $l23
    f32.mul
    local.get $l10
    local.get $l14
    f32.mul
    f32.sub
    f32.store offset=80
    local.get $l5
    local.get $l14
    local.get $l11
    f32.mul
    local.get $l23
    local.get $l8
    f32.mul
    local.get $l7
    local.get $l30
    f32.mul
    f32.add
    f32.add
    f32.store offset=112
    local.get $p1
    i32.const -64
    i32.sub
    f32.load
    local.set $l35
    local.get $p1
    f32.load offset=68
    local.set $l36
    local.get $p1
    f32.load offset=72
    local.set $l37
    local.get $p1
    f32.load offset=80
    local.set $l38
    local.get $p1
    f32.load offset=84
    local.set $l39
    local.get $p1
    f32.load offset=88
    local.set $l40
    local.get $p1
    f32.load offset=100
    local.set $l41
    local.get $p1
    f32.load offset=104
    local.set $l42
    local.get $p1
    f32.load offset=112
    local.set $l43
    local.get $p1
    f32.load offset=116
    local.set $l44
    local.get $p1
    f32.load offset=120
    local.set $l45
    local.get $p1
    f32.load offset=128
    local.set $l27
    local.get $l5
    i32.const 48
    i32.add
    local.tee $p2
    f32.load offset=84
    local.set $l9
    local.get $p1
    f32.load offset=132
    local.set $l28
    local.get $p2
    f32.load offset=20
    local.set $l10
    local.get $p2
    f32.load offset=52
    local.set $l11
    local.get $p2
    f32.load offset=88
    local.set $l12
    local.get $p2
    f32.load offset=56
    local.set $l13
    local.get $p1
    f32.load offset=136
    local.set $l29
    local.get $p2
    f32.load offset=24
    local.set $l14
    local.get $p1
    f32.load offset=20
    local.set $l25
    local.get $p1
    f32.load offset=24
    local.set $l26
    local.get $p1
    f32.load offset=36
    local.set $l15
    local.get $p1
    f32.load offset=40
    local.set $l30
    local.get $p2
    f32.load offset=68
    local.set $l16
    local.get $p1
    f32.load offset=52
    local.set $l31
    local.get $p2
    f32.load offset=36
    local.set $l17
    local.get $p2
    f32.load offset=72
    local.set $l18
    local.get $p1
    f32.load offset=56
    local.set $l32
    local.get $p2
    f32.load offset=40
    local.set $l19
    local.get $p2
    f32.load offset=80
    local.set $l6
    local.get $p2
    f32.load offset=48
    local.set $l7
    local.get $p1
    f32.load
    local.set $l46
    local.get $p1
    f32.load offset=4
    local.set $l47
    local.get $p1
    f32.load offset=8
    local.set $l48
    local.get $p1
    f32.load offset=16
    local.set $l49
    local.get $p1
    f32.load offset=32
    local.set $l33
    local.get $p2
    f32.load offset=64
    local.set $l20
    local.get $p1
    f32.load offset=48
    local.set $l34
    local.get $p2
    f32.load
    local.set $l21
    local.get $p2
    f32.load offset=32
    local.set $l22
    local.get $p2
    f32.load offset=4
    local.set $l23
    local.get $p2
    f32.load offset=8
    local.set $l24
    local.get $p1
    f32.load offset=96
    local.set $l50
    local.get $p2
    f32.load offset=16
    local.set $l8
    local.get $p0
    i32.const 0
    i32.store offset=140
    local.get $p0
    i32.const 0
    i32.store offset=124
    local.get $p0
    i32.const 0
    i32.store offset=108
    local.get $p0
    i32.const 0
    i32.store offset=92
    local.get $p0
    i32.const 0
    i32.store offset=76
    local.get $p0
    i32.const 0
    i32.store offset=60
    local.get $p0
    i32.const 0
    i32.store offset=44
    local.get $p0
    i32.const 0
    i32.store offset=28
    local.get $p0
    i32.const 0
    i32.store offset=12
    local.get $p0
    local.get $l50
    local.get $l8
    local.get $l8
    f32.mul
    f32.sub
    local.get $l7
    local.get $l7
    f32.mul
    f32.sub
    local.get $l6
    local.get $l6
    f32.mul
    f32.sub
    f32.store offset=96
    local.get $p0
    local.get $l32
    local.get $l24
    local.get $l8
    f32.mul
    f32.sub
    local.get $l19
    local.get $l7
    f32.mul
    f32.sub
    local.get $l18
    local.get $l6
    f32.mul
    f32.sub
    f32.store offset=56
    local.get $p0
    local.get $l31
    local.get $l23
    local.get $l8
    f32.mul
    f32.sub
    local.get $l17
    local.get $l7
    f32.mul
    f32.sub
    local.get $l16
    local.get $l6
    f32.mul
    f32.sub
    f32.store offset=52
    local.get $p0
    local.get $l34
    local.get $l21
    local.get $l8
    f32.mul
    f32.sub
    local.get $l22
    local.get $l7
    f32.mul
    f32.sub
    local.get $l20
    local.get $l6
    f32.mul
    f32.sub
    f32.store offset=48
    local.get $p0
    local.get $l30
    local.get $l24
    local.get $l24
    f32.mul
    f32.sub
    local.get $l19
    local.get $l19
    f32.mul
    f32.sub
    local.get $l18
    local.get $l18
    f32.mul
    f32.sub
    f32.store offset=40
    local.get $p0
    local.get $l15
    local.get $l23
    local.get $l24
    f32.mul
    local.tee $l30
    f32.sub
    local.get $l17
    local.get $l19
    f32.mul
    local.tee $l15
    f32.sub
    local.get $l16
    local.get $l18
    f32.mul
    local.tee $l31
    f32.sub
    f32.store offset=36
    local.get $p0
    local.get $l33
    local.get $l21
    local.get $l24
    f32.mul
    local.tee $l32
    f32.sub
    local.get $l22
    local.get $l19
    f32.mul
    local.tee $l33
    f32.sub
    local.get $l20
    local.get $l18
    f32.mul
    local.tee $l34
    f32.sub
    f32.store offset=32
    local.get $p0
    local.get $l26
    local.get $l30
    f32.sub
    local.get $l15
    f32.sub
    local.get $l31
    f32.sub
    f32.store offset=24
    local.get $p0
    local.get $l25
    local.get $l23
    local.get $l23
    f32.mul
    f32.sub
    local.get $l17
    local.get $l17
    f32.mul
    f32.sub
    local.get $l16
    local.get $l16
    f32.mul
    f32.sub
    f32.store offset=20
    local.get $p0
    local.get $l49
    local.get $l21
    local.get $l23
    f32.mul
    local.tee $l25
    f32.sub
    local.get $l22
    local.get $l17
    f32.mul
    local.tee $l26
    f32.sub
    local.get $l20
    local.get $l16
    f32.mul
    local.tee $l15
    f32.sub
    f32.store offset=16
    local.get $p0
    local.get $l48
    local.get $l32
    f32.sub
    local.get $l33
    f32.sub
    local.get $l34
    f32.sub
    f32.store offset=8
    local.get $p0
    local.get $l47
    local.get $l25
    f32.sub
    local.get $l26
    f32.sub
    local.get $l15
    f32.sub
    f32.store offset=4
    local.get $p0
    local.get $l46
    local.get $l21
    local.get $l21
    f32.mul
    f32.sub
    local.get $l22
    local.get $l22
    f32.mul
    f32.sub
    local.get $l20
    local.get $l20
    f32.mul
    f32.sub
    f32.store
    local.get $p0
    local.get $l29
    local.get $l14
    local.get $l14
    f32.mul
    f32.sub
    local.get $l13
    local.get $l13
    f32.mul
    f32.sub
    local.get $l12
    local.get $l12
    f32.mul
    f32.sub
    f32.store offset=136
    local.get $p0
    local.get $l28
    local.get $l10
    local.get $l14
    f32.mul
    local.tee $l29
    f32.sub
    local.get $l11
    local.get $l13
    f32.mul
    local.tee $l28
    f32.sub
    local.get $l9
    local.get $l12
    f32.mul
    local.tee $l25
    f32.sub
    f32.store offset=132
    local.get $p0
    local.get $l27
    local.get $l8
    local.get $l14
    f32.mul
    local.tee $l26
    f32.sub
    local.get $l7
    local.get $l13
    f32.mul
    local.tee $l27
    f32.sub
    local.get $l6
    local.get $l12
    f32.mul
    local.tee $l15
    f32.sub
    f32.store offset=128
    local.get $p0
    local.get $l45
    local.get $l29
    f32.sub
    local.get $l28
    f32.sub
    local.get $l25
    f32.sub
    f32.store offset=120
    local.get $p0
    local.get $l44
    local.get $l10
    local.get $l10
    f32.mul
    f32.sub
    local.get $l11
    local.get $l11
    f32.mul
    f32.sub
    local.get $l9
    local.get $l9
    f32.mul
    f32.sub
    f32.store offset=116
    local.get $p0
    local.get $l43
    local.get $l8
    local.get $l10
    f32.mul
    local.tee $l8
    f32.sub
    local.get $l7
    local.get $l11
    f32.mul
    local.tee $l7
    f32.sub
    local.get $l6
    local.get $l9
    f32.mul
    local.tee $l6
    f32.sub
    f32.store offset=112
    local.get $p0
    local.get $l42
    local.get $l26
    f32.sub
    local.get $l27
    f32.sub
    local.get $l15
    f32.sub
    f32.store offset=104
    local.get $p0
    local.get $l41
    local.get $l8
    f32.sub
    local.get $l7
    f32.sub
    local.get $l6
    f32.sub
    f32.store offset=100
    local.get $p0
    local.get $l40
    local.get $l24
    local.get $l14
    f32.mul
    f32.sub
    local.get $l19
    local.get $l13
    f32.mul
    f32.sub
    local.get $l18
    local.get $l12
    f32.mul
    f32.sub
    f32.store offset=88
    local.get $p0
    local.get $l39
    local.get $l23
    local.get $l14
    f32.mul
    f32.sub
    local.get $l17
    local.get $l13
    f32.mul
    f32.sub
    local.get $l16
    local.get $l12
    f32.mul
    f32.sub
    f32.store offset=84
    local.get $p0
    local.get $l38
    local.get $l21
    local.get $l14
    f32.mul
    f32.sub
    local.get $l22
    local.get $l13
    f32.mul
    f32.sub
    local.get $l20
    local.get $l12
    f32.mul
    f32.sub
    f32.store offset=80
    local.get $p0
    local.get $l37
    local.get $l24
    local.get $l10
    f32.mul
    f32.sub
    local.get $l19
    local.get $l11
    f32.mul
    f32.sub
    local.get $l18
    local.get $l9
    f32.mul
    f32.sub
    f32.store offset=72
    local.get $p0
    local.get $l36
    local.get $l23
    local.get $l10
    f32.mul
    f32.sub
    local.get $l17
    local.get $l11
    f32.mul
    f32.sub
    local.get $l16
    local.get $l9
    f32.mul
    f32.sub
    f32.store offset=68
    local.get $p0
    i32.const -64
    i32.sub
    local.get $l35
    local.get $l21
    local.get $l10
    f32.mul
    f32.sub
    local.get $l22
    local.get $l11
    f32.mul
    f32.sub
    local.get $l20
    local.get $l9
    f32.mul
    f32.sub
    f32.store
    local.get $l5
    i32.const 240
    i32.add
    global.set $g0)
