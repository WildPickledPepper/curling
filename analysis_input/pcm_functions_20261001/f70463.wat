  (func $f70463 (type $t80) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 f32) (param $p7 i32) (param $p8 i32) (param $p9 f32) (result i32)
    (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 i32) (local $l17 i32) (local $l18 i32) (local $l19 i32) (local $l20 i32) (local $l21 i32) (local $l22 i32) (local $l23 i32) (local $l24 i32) (local $l25 i32) (local $l26 i32) (local $l27 i32) (local $l28 i32) (local $l29 i32) (local $l30 i32) (local $l31 i32) (local $l32 i32) (local $l33 i32) (local $l34 f32) (local $l35 f32) (local $l36 f32) (local $l37 f32) (local $l38 f32) (local $l39 f32) (local $l40 f32) (local $l41 f32) (local $l42 f32) (local $l43 f32) (local $l44 f32) (local $l45 f32) (local $l46 f32) (local $l47 f32) (local $l48 f32) (local $l49 f32) (local $l50 f32) (local $l51 f32) (local $l52 f32) (local $l53 f32) (local $l54 f32) (local $l55 f32) (local $l56 f32) (local $l57 f32) (local $l58 f32) (local $l59 f32) (local $l60 f32) (local $l61 f32) (local $l62 f32) (local $l63 f32) (local $l64 f32) (local $l65 f32) (local $l66 f32) (local $l67 f32) (local $l68 f32) (local $l69 f32) (local $l70 f32) (local $l71 f32) (local $l72 f32) (local $l73 f32) (local $l74 f32) (local $l75 f32) (local $l76 f32) (local $l77 f32) (local $l78 f32) (local $l79 f32) (local $l80 i64) (local $l81 i64) (local $l82 i64)
    global.get $g0
    i32.const 288
    i32.sub
    local.tee $p2
    global.set $g0
    local.get $p4
    f32.load offset=20
    local.set $l53
    local.get $p4
    f32.load offset=32
    local.set $l54
    local.get $p4
    i32.const 52
    i32.add
    local.tee $l11
    f32.load
    local.set $l46
    local.get $p4
    f32.load offset=16
    local.set $l55
    local.get $p4
    i32.const 56
    i32.add
    local.tee $l13
    f32.load
    local.set $l47
    local.get $p4
    f32.load offset=28
    local.set $l56
    local.get $p3
    f32.load offset=20
    local.set $l35
    local.get $p3
    f32.load offset=24
    local.set $l41
    local.get $p4
    f32.load offset=8
    local.set $l57
    local.get $p4
    f32.load offset=24
    local.set $l58
    local.get $p4
    f32.load
    local.set $l59
    local.get $p4
    f32.load offset=12
    local.set $l60
    local.get $p4
    f32.load offset=48
    local.set $l48
    local.get $p4
    f32.load offset=4
    local.set $l61
    local.get $p3
    f32.load offset=8
    local.set $l34
    local.get $p3
    f32.load
    local.set $l36
    local.get $p3
    f32.load offset=4
    local.set $l39
    local.get $p3
    f32.load offset=16
    local.set $l37
    local.get $p3
    f32.load offset=12
    local.set $l40
    local.get $p2
    i32.const 0
    i32.store offset=284
    local.get $p2
    local.get $l41
    f32.const -0x1p+1 (;=-2;)
    f32.mul
    local.tee $l38
    local.get $l40
    local.get $l40
    f32.mul
    f32.const -0x1p-1 (;=-0.5;)
    f32.add
    local.tee $l41
    f32.mul
    local.get $l40
    local.get $l36
    local.get $l35
    f32.const -0x1p+1 (;=-2;)
    f32.mul
    local.tee $l35
    f32.mul
    local.get $l39
    local.get $l37
    f32.const -0x1p+1 (;=-2;)
    f32.mul
    local.tee $l37
    f32.mul
    f32.sub
    f32.mul
    f32.sub
    local.get $l34
    local.get $l37
    local.get $l36
    f32.mul
    local.get $l35
    local.get $l39
    f32.mul
    f32.add
    local.get $l38
    local.get $l34
    f32.mul
    f32.add
    local.tee $l42
    f32.mul
    f32.add
    f32.store offset=280
    local.get $p2
    local.get $l39
    local.get $l42
    f32.mul
    local.get $l35
    local.get $l41
    f32.mul
    local.get $l40
    local.get $l37
    local.get $l34
    f32.mul
    local.get $l38
    local.get $l36
    f32.mul
    f32.sub
    f32.mul
    f32.sub
    f32.add
    f32.store offset=276
    local.get $p2
    local.get $l40
    f32.store offset=268
    local.get $p2
    local.get $l34
    f32.neg
    f32.store offset=264
    local.get $p2
    local.get $l36
    f32.neg
    f32.store offset=256
    local.get $p2
    local.get $l36
    local.get $l42
    f32.mul
    local.get $l37
    local.get $l41
    f32.mul
    local.get $l40
    local.get $l38
    local.get $l39
    f32.mul
    local.get $l35
    local.get $l34
    f32.mul
    f32.sub
    f32.mul
    f32.sub
    f32.add
    f32.store offset=272
    local.get $p2
    local.get $l39
    f32.neg
    local.tee $l42
    f32.store offset=260
    local.get $p5
    f32.load offset=8
    local.set $l44
    local.get $p5
    f32.load
    local.set $l43
    local.get $p5
    f32.load offset=4
    local.set $l45
    local.get $p2
    i64.const 0
    i64.store offset=200
    local.get $p2
    i64.const 0
    i64.store offset=192
    local.get $l11
    f32.load
    local.set $l38
    local.get $l13
    f32.load
    local.set $l35
    local.get $p4
    f32.load offset=48
    local.set $l37
    local.get $p2
    i32.const 0
    i32.store offset=252
    local.get $p2
    local.get $l35
    f32.store offset=248
    local.get $p2
    local.get $l38
    f32.store offset=244
    local.get $p2
    local.get $l37
    f32.store offset=240
    local.get $p2
    i32.const 0
    i32.store8 offset=224
    local.get $p2
    i32.const 3
    i32.store offset=220
    local.get $p2
    local.get $l37
    local.get $l38
    local.get $l37
    local.get $l38
    f32.le
    select
    local.tee $l38
    local.get $l35
    local.get $l35
    local.get $l38
    f32.ge
    select
    local.tee $l38
    f32.const 0x1.99999ap-5 (;=0.05;)
    f32.mul
    local.tee $l35
    f32.store offset=216
    local.get $p2
    local.get $l35
    f32.store offset=212
    local.get $p2
    local.get $l38
    f32.const 0x1.333334p-3 (;=0.15;)
    f32.mul
    f32.store offset=208
    local.get $p7
    i32.const 2139095039
    i32.store offset=40
    local.get $p0
    i32.load offset=4
    local.set $l11
    local.get $p2
    local.get $p0
    i32.store offset=184
    local.get $p2
    local.get $l11
    i32.store offset=180
    local.get $p2
    f32.const 0x1p+0 (;=1;)
    local.get $p0
    f32.load offset=8
    f32.div
    f32.store offset=172
    local.get $p2
    f32.const 0x1p+0 (;=1;)
    local.get $p0
    f32.load offset=12
    f32.div
    f32.store offset=168
    local.get $p2
    f32.const 0x1p+0 (;=1;)
    local.get $p0
    f32.load offset=16
    f32.div
    f32.store offset=176
    local.get $p8
    i32.load16_u
    local.set $p8
    local.get $p2
    i32.const 0
    i32.store16 offset=90
    local.get $p2
    local.get $p8
    i32.store16 offset=88
    local.get $p2
    local.get $p2
    i32.const 168
    i32.add
    i32.store offset=84
    local.get $p0
    i32.load8_u offset=20
    local.set $l11
    local.get $p2
    local.get $l41
    local.get $l45
    local.get $p6
    f32.mul
    local.tee $l38
    local.get $l38
    f32.add
    local.tee $l38
    f32.mul
    local.get $l40
    local.get $l36
    local.get $l44
    local.get $p6
    f32.mul
    local.tee $l35
    local.get $l35
    f32.add
    local.tee $l35
    f32.mul
    local.get $l34
    local.get $l43
    local.get $p6
    f32.mul
    local.tee $l37
    local.get $l37
    f32.add
    local.tee $l37
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l39
    local.get $l38
    local.get $l42
    f32.mul
    local.get $l36
    local.get $l37
    f32.mul
    f32.sub
    local.get $l34
    local.get $l35
    f32.mul
    f32.sub
    local.tee $l42
    f32.mul
    f32.sub
    f32.store offset=132
    local.get $p2
    local.get $l41
    local.get $l35
    f32.mul
    local.get $l40
    local.get $l39
    local.get $l37
    f32.mul
    local.get $l36
    local.get $l38
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l34
    local.get $l42
    f32.mul
    f32.sub
    f32.store offset=136
    local.get $p2
    i32.const 2139095039
    i32.store offset=112
    local.get $p2
    i32.const 3132144
    i32.store offset=80
    local.get $p2
    local.get $p1
    i32.store offset=100
    local.get $p2
    local.get $l41
    local.get $l37
    f32.mul
    local.get $l40
    local.get $l34
    local.get $l38
    f32.mul
    local.get $l39
    local.get $l35
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l36
    local.get $l42
    f32.mul
    f32.sub
    f32.store offset=128
    local.get $p2
    local.get $p7
    i32.store offset=140
    local.get $p2
    local.get $p9
    f32.store offset=144
    local.get $p2
    local.get $p8
    i32.const 6
    i32.shr_u
    i32.const 1
    i32.and
    i32.store8 offset=93
    local.get $p2
    local.get $p8
    i32.const 128
    i32.and
    local.get $l11
    i32.const 2
    i32.and
    i32.or
    i32.const 0
    i32.ne
    i32.store8 offset=92
    local.get $p2
    local.get $p2
    i32.const 256
    i32.add
    i32.store offset=96
    local.get $p2
    local.get $p2
    i32.const 192
    i32.add
    i32.store offset=104
    local.get $p7
    i32.const -1
    i32.store offset=8
    local.get $p2
    local.get $p1
    f32.load
    local.tee $l34
    local.get $l34
    local.get $p1
    f32.load offset=16
    f32.const -0x1p+1 (;=-2;)
    f32.mul
    local.tee $l35
    f32.mul
    local.get $p1
    f32.load offset=20
    f32.const -0x1p+1 (;=-2;)
    f32.mul
    local.tee $l37
    local.get $p1
    f32.load offset=4
    local.tee $l39
    f32.mul
    f32.add
    local.get $p1
    f32.load offset=24
    f32.const -0x1p+1 (;=-2;)
    f32.mul
    local.tee $l42
    local.get $p1
    f32.load offset=8
    local.tee $l36
    f32.mul
    f32.add
    local.tee $l49
    f32.mul
    local.get $l35
    local.get $p1
    f32.load offset=12
    local.tee $l40
    local.get $l40
    f32.mul
    f32.const -0x1p-1 (;=-0.5;)
    f32.add
    local.tee $l41
    f32.mul
    local.get $l40
    local.get $l42
    local.get $l39
    f32.mul
    local.get $l37
    local.get $l36
    f32.mul
    f32.sub
    f32.mul
    f32.sub
    f32.add
    local.get $l41
    local.get $p4
    f32.load offset=36
    local.tee $l38
    local.get $l38
    f32.add
    local.tee $l44
    f32.mul
    local.get $l40
    local.get $l36
    local.get $p4
    f32.load offset=40
    local.tee $l38
    local.get $l38
    f32.add
    local.tee $l43
    f32.mul
    local.get $l39
    local.get $p4
    f32.load offset=44
    local.tee $l38
    local.get $l38
    f32.add
    local.tee $l45
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l34
    local.get $l43
    local.get $l39
    f32.neg
    local.tee $l38
    f32.mul
    local.get $l34
    local.get $l44
    f32.mul
    f32.sub
    local.get $l36
    local.get $l45
    f32.mul
    f32.sub
    local.tee $l50
    f32.mul
    f32.sub
    f32.add
    local.tee $l51
    f32.store offset=64
    local.get $p2
    local.get $l39
    local.get $l49
    f32.mul
    local.get $l37
    local.get $l41
    f32.mul
    local.get $l40
    local.get $l35
    local.get $l36
    f32.mul
    local.get $l42
    local.get $l34
    f32.mul
    f32.sub
    f32.mul
    f32.sub
    f32.add
    local.get $l41
    local.get $l43
    f32.mul
    local.get $l40
    local.get $l34
    local.get $l45
    f32.mul
    local.get $l36
    local.get $l44
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l39
    local.get $l50
    f32.mul
    f32.sub
    f32.add
    local.tee $l52
    f32.store offset=68
    local.get $p2
    local.get $l42
    local.get $l41
    f32.mul
    local.get $l40
    local.get $l37
    local.get $l34
    f32.mul
    local.get $l35
    local.get $l39
    f32.mul
    f32.sub
    f32.mul
    f32.sub
    local.get $l36
    local.get $l49
    f32.mul
    f32.add
    local.get $l41
    local.get $l45
    f32.mul
    local.get $l40
    local.get $l39
    local.get $l44
    f32.mul
    local.get $l34
    local.get $l43
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l36
    local.get $l50
    f32.mul
    f32.sub
    f32.add
    local.tee $l44
    f32.store offset=72
    local.get $p2
    local.get $l41
    local.get $p5
    f32.load offset=8
    local.tee $l35
    local.get $l35
    f32.add
    local.tee $l35
    f32.mul
    local.get $l40
    local.get $l39
    local.get $p5
    f32.load
    local.tee $l37
    local.get $l37
    f32.add
    local.tee $l37
    f32.mul
    local.get $l34
    local.get $p5
    f32.load offset=4
    local.tee $l42
    local.get $l42
    f32.add
    local.tee $l42
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l36
    local.get $l42
    local.get $l38
    f32.mul
    local.get $l34
    local.get $l37
    f32.mul
    f32.sub
    local.get $l36
    local.get $l35
    f32.mul
    f32.sub
    local.tee $l43
    f32.mul
    f32.sub
    f32.store offset=56
    local.get $p2
    local.get $l41
    local.get $l42
    f32.mul
    local.get $l40
    local.get $l34
    local.get $l35
    f32.mul
    local.get $l36
    local.get $l37
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l39
    local.get $l43
    f32.mul
    f32.sub
    f32.store offset=52
    local.get $p2
    local.get $l41
    local.get $l37
    f32.mul
    local.get $l40
    local.get $l36
    local.get $l42
    f32.mul
    local.get $l39
    local.get $l35
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l34
    local.get $l43
    f32.mul
    f32.sub
    f32.store offset=48
    local.get $p2
    local.get $l48
    local.get $l57
    f32.abs
    f32.mul
    local.get $l46
    local.get $l53
    f32.abs
    f32.mul
    f32.add
    local.get $l47
    local.get $l54
    f32.abs
    f32.mul
    f32.add
    local.get $p9
    f32.add
    local.tee $l35
    local.get $l34
    local.get $l34
    f32.neg
    local.get $l34
    f32.sub
    local.tee $l41
    f32.mul
    f32.const 0x1p+0 (;=1;)
    f32.add
    local.tee $l42
    local.get $l38
    local.get $l39
    f32.sub
    local.tee $l39
    local.get $l38
    f32.mul
    local.tee $l43
    f32.sub
    f32.mul
    f32.abs
    local.get $l48
    local.get $l59
    f32.abs
    f32.mul
    local.get $l46
    local.get $l60
    f32.abs
    f32.mul
    f32.add
    local.get $l47
    local.get $l58
    f32.abs
    f32.mul
    f32.add
    local.get $p9
    f32.add
    local.tee $l37
    local.get $l41
    local.get $l36
    f32.neg
    local.tee $l34
    f32.mul
    local.tee $l45
    local.get $l40
    local.get $l39
    f32.mul
    local.tee $l49
    f32.sub
    f32.mul
    f32.abs
    local.get $l48
    local.get $l61
    f32.abs
    f32.mul
    local.get $l46
    local.get $l55
    f32.abs
    f32.mul
    f32.add
    local.get $l47
    local.get $l56
    f32.abs
    f32.mul
    f32.add
    local.get $p9
    f32.add
    local.tee $l46
    local.get $l40
    local.get $l41
    f32.mul
    local.tee $l47
    local.get $l39
    local.get $l34
    f32.mul
    local.tee $l39
    f32.add
    f32.mul
    f32.abs
    f32.add
    f32.add
    local.tee $l48
    local.get $l44
    f32.add
    local.get $l44
    local.get $l48
    f32.sub
    f32.sub
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.store offset=40
    local.get $p2
    local.get $l35
    local.get $l39
    local.get $l47
    f32.sub
    f32.mul
    f32.abs
    local.get $l37
    local.get $l41
    local.get $l38
    f32.mul
    local.tee $l39
    local.get $l40
    local.get $l34
    local.get $l36
    f32.sub
    local.tee $l36
    f32.mul
    local.tee $l40
    f32.add
    f32.mul
    f32.abs
    local.get $l46
    local.get $l42
    local.get $l36
    local.get $l34
    f32.mul
    local.tee $l34
    f32.sub
    f32.mul
    f32.abs
    f32.add
    f32.add
    local.tee $l36
    local.get $l52
    f32.add
    local.get $l52
    local.get $l36
    f32.sub
    f32.sub
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.store offset=36
    local.get $p2
    local.get $l35
    local.get $l45
    local.get $l49
    f32.add
    f32.mul
    f32.abs
    local.get $l37
    f32.const 0x1p+0 (;=1;)
    local.get $l43
    f32.sub
    local.get $l34
    f32.sub
    f32.mul
    f32.abs
    local.get $l46
    local.get $l39
    local.get $l40
    f32.sub
    f32.mul
    f32.abs
    f32.add
    f32.add
    local.tee $l34
    local.get $l51
    f32.add
    local.get $l51
    local.get $l34
    f32.sub
    f32.sub
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.store offset=32
    local.get $p2
    local.get $p2
    i32.const 32
    i32.add
    i32.store offset=4
    local.get $p2
    local.get $p2
    i32.const 168
    i32.add
    i32.store
    local.get $p2
    i32.const 168
    i32.add
    local.get $p2
    i32.const 8
    i32.add
    local.tee $p8
    call $f70443
    local.get $p2
    i32.const 16
    i32.add
    local.tee $l11
    local.get $l11
    f32.load
    local.get $p2
    f32.load offset=40
    local.tee $l34
    f32.sub
    f32.store
    local.get $p2
    i32.const 12
    i32.add
    local.tee $l11
    local.get $l11
    f32.load
    local.get $p2
    f32.load offset=36
    local.tee $l36
    f32.sub
    f32.store
    local.get $p2
    i32.const 20
    i32.add
    local.tee $l11
    local.get $p2
    f32.load offset=32
    local.tee $l40
    local.get $l11
    f32.load
    f32.add
    f32.store
    local.get $p2
    i32.const 24
    i32.add
    local.tee $l11
    local.get $l36
    local.get $l11
    f32.load
    f32.add
    f32.store
    local.get $p2
    i32.const 28
    i32.add
    local.tee $l11
    local.get $l34
    local.get $l11
    f32.load
    f32.add
    f32.store
    local.get $p2
    local.get $p2
    f32.load offset=8
    local.get $l40
    f32.sub
    f32.store offset=8
    local.get $p2
    i32.load
    local.get $p2
    i32.const -64
    i32.sub
    local.get $p2
    i32.const 48
    i32.add
    local.get $p6
    local.get $p2
    i32.const 80
    i32.add
    local.get $p8
    local.get $p2
    i32.load offset=4
    call $f70461
    f32.const 0x0p+0 (;=0;)
    local.set $l35
    f32.const 0x0p+0 (;=0;)
    local.set $l38
    block $B0
      local.get $p2
      i32.const 80
      i32.add
      local.tee $p8
      i32.load8_u offset=10
      local.tee $l11
      i32.eqz
      br_if $B0
      local.get $p8
      i32.load8_u offset=11
      if $I1
        local.get $p7
        i32.const 1026
        i32.store16 offset=12
        local.get $p8
        i32.load8_u offset=9
        i32.const 2
        i32.and
        if $I2
          local.get $p8
          i32.load8_u offset=12
          local.set $l22
          global.get $g0
          i32.const 6080
          i32.sub
          local.tee $l10
          global.set $g0
          local.get $l10
          i32.const 0
          i32.store offset=1964
          local.get $l10
          i32.const 0
          i32.store offset=1960
          local.get $l10
          i64.const 0
          i64.store offset=1952
          local.get $l10
          i32.const 1952
          i32.add
          i32.const 128
          call $f70632
          local.get $p0
          i32.load offset=4
          local.set $l12
          local.get $l10
          local.get $p0
          i32.store offset=1944
          local.get $l10
          local.get $l12
          i32.store offset=1940
          local.get $l10
          f32.const 0x1p+0 (;=1;)
          local.get $p0
          f32.load offset=8
          f32.div
          f32.store offset=1932
          local.get $l10
          f32.const 0x1p+0 (;=1;)
          local.get $p0
          f32.load offset=12
          f32.div
          f32.store offset=1928
          local.get $l10
          f32.const 0x1p+0 (;=1;)
          local.get $p0
          f32.load offset=16
          f32.div
          f32.store offset=1936
          local.get $p4
          f32.load offset=44
          local.set $l53
          local.get $p4
          f32.load offset=40
          local.set $l63
          local.get $p4
          f32.load offset=28
          local.set $l57
          local.get $p4
          f32.load offset=20
          local.set $l58
          local.get $p4
          f32.load offset=32
          local.set $l45
          local.get $p4
          f32.load offset=16
          local.set $l42
          local.get $p3
          f32.load offset=24
          local.set $l39
          local.get $p4
          f32.load offset=36
          local.set $l54
          local.get $p4
          f32.load offset=24
          local.set $l59
          local.get $p4
          f32.load offset=8
          local.set $l60
          local.get $p4
          f32.load offset=12
          local.set $l61
          local.get $p4
          f32.load offset=4
          local.set $l62
          local.get $p4
          f32.load
          local.set $l48
          local.get $p3
          i64.load align=4
          local.set $l80
          local.get $p3
          i64.load offset=8 align=4
          local.set $l81
          local.get $p3
          i64.load offset=16 align=4
          local.set $l82
          local.get $l10
          local.get $p4
          f32.load offset=48
          local.tee $l34
          local.get $p4
          f32.load offset=52
          local.tee $l37
          local.get $l34
          local.get $l37
          f32.le
          select
          local.tee $l35
          local.get $p4
          f32.load offset=56
          local.tee $l36
          local.get $l35
          local.get $l36
          f32.le
          select
          local.tee $l35
          f32.const 0x1.333334p-3 (;=0.15;)
          f32.mul
          local.tee $l43
          local.get $p9
          f32.add
          local.tee $p6
          f32.store offset=1904
          local.get $l10
          i32.const 1900
          i32.add
          i32.const 0
          i32.store
          local.get $l10
          i32.const 1896
          i32.add
          local.get $l36
          f32.store
          local.get $l10
          i32.const 1892
          i32.add
          local.get $l37
          f32.store
          local.get $l10
          i32.const 0
          i32.store8 offset=1872
          local.get $l10
          i32.const 3
          i32.store offset=1868
          local.get $l10
          i64.const 0
          i64.store offset=1840
          local.get $l10
          i64.const 0
          i64.store offset=1848
          local.get $l10
          local.get $l34
          f32.store offset=1888
          local.get $l10
          local.get $l35
          f32.const 0x1.99999ap-5 (;=0.05;)
          f32.mul
          local.tee $p9
          f32.store offset=1864
          local.get $l10
          local.get $p9
          f32.store offset=1860
          local.get $l10
          local.get $l43
          f32.store offset=1856
          local.get $l10
          i32.const 1544
          i32.add
          local.get $p4
          i32.const 48
          i32.add
          call $f69944
          local.get $l10
          i32.const 1768
          i32.add
          call $f70032
          local.get $l10
          i32.const 1512
          i32.add
          i64.const 0
          i64.store
          local.get $l10
          i32.const 1508
          i32.add
          i32.const 1065353216
          i32.store
          local.get $l10
          i32.const 1520
          i32.add
          i64.const 0
          i64.store
          local.get $l10
          i32.const 1528
          i32.add
          i64.const 1065353216
          i64.store
          local.get $l10
          i64.const 0
          i64.store offset=1492 align=4
          local.get $l10
          i32.const 1065353216
          i32.store offset=1488
          local.get $l10
          i64.const 0
          i64.store offset=1500 align=4
          local.get $p1
          local.tee $l19
          f32.load offset=20
          local.set $l43
          local.get $p1
          f32.load offset=24
          local.set $l49
          local.get $p1
          f32.load offset=8
          local.set $p9
          local.get $p1
          f32.load offset=4
          local.set $l35
          local.get $p1
          f32.load offset=12
          local.set $l50
          local.get $p1
          f32.load
          local.set $l44
          local.get $p1
          f32.load offset=16
          local.set $l51
          local.get $l10
          i32.const 1484
          i32.add
          i32.const 0
          i32.store
          local.get $l10
          i32.const 1480
          i32.add
          local.get $l39
          f32.store
          local.get $l10
          local.get $l82
          i64.store offset=1472
          local.get $l10
          local.get $l81
          i64.store offset=1464
          local.get $l10
          local.get $l80
          i64.store offset=1456
          local.get $l36
          local.get $p6
          f32.add
          local.tee $l46
          f32.const 0x1p+0 (;=1;)
          local.get $l48
          f32.const 0x1p+0 (;=1;)
          f32.add
          local.tee $l55
          local.get $l42
          f32.sub
          local.get $l45
          f32.sub
          local.tee $l36
          f32.const 0x1p-1 (;=0.5;)
          local.get $l36
          f32.sqrt
          f32.div
          local.tee $l36
          f32.mul
          local.get $l62
          local.get $l61
          f32.add
          local.tee $l56
          f32.const 0x1p-1 (;=0.5;)
          local.get $l42
          f32.const 0x1p+0 (;=1;)
          local.get $l48
          f32.sub
          local.tee $l38
          f32.add
          local.get $l45
          f32.sub
          local.tee $l41
          f32.sqrt
          f32.div
          local.tee $l39
          f32.mul
          local.get $l42
          local.get $l48
          f32.lt
          local.tee $p4
          select
          local.get $l60
          local.get $l59
          f32.add
          local.tee $l40
          f32.const 0x1p-1 (;=0.5;)
          local.get $l45
          local.get $l38
          local.get $l42
          f32.sub
          f32.add
          local.tee $l64
          f32.sqrt
          f32.div
          local.tee $l38
          f32.mul
          local.get $l58
          local.get $l57
          f32.sub
          local.tee $l65
          f32.const 0x1p-1 (;=0.5;)
          local.get $l45
          local.get $l55
          local.get $l42
          f32.add
          f32.add
          local.tee $l66
          f32.sqrt
          f32.div
          local.tee $l55
          f32.mul
          local.get $l48
          local.get $l42
          f32.neg
          f32.lt
          local.tee $p0
          select
          local.get $l45
          f32.const 0x0p+0 (;=0;)
          f32.lt
          local.tee $p3
          select
          local.tee $l52
          local.get $l52
          local.get $l52
          f32.add
          local.tee $l52
          f32.mul
          f32.sub
          local.tee $l67
          local.get $l56
          local.get $l36
          f32.mul
          local.get $l41
          local.get $l39
          f32.mul
          local.get $p4
          select
          local.get $l58
          local.get $l57
          f32.add
          local.tee $l68
          local.get $l38
          f32.mul
          local.get $l59
          local.get $l60
          f32.sub
          local.tee $l69
          local.get $l55
          f32.mul
          local.get $p0
          select
          local.get $p3
          select
          local.tee $l56
          local.get $l56
          local.get $l56
          f32.add
          local.tee $l41
          f32.mul
          local.tee $l70
          f32.sub
          f32.mul
          f32.abs
          local.get $l34
          local.get $p6
          f32.add
          local.tee $l47
          local.get $l52
          local.get $l40
          local.get $l36
          f32.mul
          local.get $l68
          local.get $l39
          f32.mul
          local.get $p4
          select
          local.get $l64
          local.get $l38
          f32.mul
          local.get $l62
          local.get $l61
          f32.sub
          local.tee $l40
          local.get $l55
          f32.mul
          local.get $p0
          select
          local.get $p3
          select
          local.tee $l34
          f32.mul
          local.tee $l64
          local.get $l41
          local.get $l65
          local.get $l36
          f32.mul
          local.get $l69
          local.get $l39
          f32.mul
          local.get $p4
          select
          local.get $l40
          local.get $l38
          f32.mul
          local.get $l66
          local.get $l55
          f32.mul
          local.get $p0
          select
          local.get $p3
          select
          local.tee $l36
          f32.mul
          local.tee $l39
          f32.sub
          f32.mul
          f32.abs
          local.get $l37
          local.get $p6
          f32.add
          local.tee $l37
          local.get $l41
          local.get $l34
          f32.mul
          local.tee $p6
          local.get $l52
          local.get $l36
          f32.mul
          local.tee $l38
          f32.add
          f32.mul
          f32.abs
          f32.add
          f32.add
          local.set $l55
          local.get $l46
          local.get $p6
          local.get $l38
          f32.sub
          f32.mul
          f32.abs
          local.get $l47
          local.get $l52
          local.get $l56
          f32.mul
          local.tee $p6
          local.get $l34
          local.get $l34
          f32.add
          local.tee $l38
          local.get $l36
          f32.mul
          local.tee $l36
          f32.add
          f32.mul
          f32.abs
          local.get $l37
          local.get $l67
          local.get $l34
          local.get $l38
          f32.mul
          local.tee $l34
          f32.sub
          f32.mul
          f32.abs
          f32.add
          f32.add
          local.set $l52
          local.get $l46
          local.get $l64
          local.get $l39
          f32.add
          f32.mul
          f32.abs
          local.get $l47
          f32.const 0x1p+0 (;=1;)
          local.get $l70
          f32.sub
          local.get $l34
          f32.sub
          f32.mul
          f32.abs
          local.get $l37
          local.get $p6
          local.get $l36
          f32.sub
          f32.mul
          f32.abs
          f32.add
          f32.add
          local.set $l56
          local.get $l59
          local.get $l51
          f32.mul
          local.get $l57
          local.get $l43
          f32.mul
          f32.add
          local.get $l45
          local.get $l49
          f32.mul
          f32.add
          local.set $l68
          local.get $l61
          local.get $l51
          f32.mul
          local.get $l42
          local.get $l43
          f32.mul
          f32.add
          local.get $l58
          local.get $l49
          f32.mul
          f32.add
          local.set $l69
          local.get $l45
          f32.const 0x1p+0 (;=1;)
          local.get $l44
          local.get $l44
          local.get $l44
          f32.add
          local.tee $l34
          f32.mul
          f32.sub
          local.tee $l44
          local.get $l35
          local.get $l35
          local.get $l35
          f32.add
          local.tee $l37
          f32.mul
          local.tee $l39
          f32.sub
          local.tee $l36
          f32.mul
          local.get $l59
          local.get $l34
          local.get $p9
          f32.mul
          local.tee $l38
          local.get $l37
          local.get $l50
          f32.mul
          local.tee $l46
          f32.add
          local.tee $p6
          f32.mul
          local.get $l57
          local.get $l37
          local.get $p9
          f32.mul
          local.tee $l41
          local.get $l34
          local.get $l50
          f32.mul
          local.tee $l47
          f32.sub
          local.tee $l37
          f32.mul
          f32.add
          f32.add
          local.set $l70
          local.get $l58
          local.get $l36
          f32.mul
          local.get $l61
          local.get $p6
          f32.mul
          local.get $l42
          local.get $l37
          f32.mul
          f32.add
          f32.add
          local.set $l71
          local.get $l60
          local.get $l36
          f32.mul
          local.get $l48
          local.get $p6
          f32.mul
          local.get $l62
          local.get $l37
          f32.mul
          f32.add
          f32.add
          local.set $l72
          local.get $l45
          local.get $l41
          local.get $l47
          f32.add
          local.tee $l37
          f32.mul
          local.get $l59
          local.get $l34
          local.get $l35
          f32.mul
          local.tee $l34
          local.get $l50
          local.get $p9
          local.get $p9
          f32.add
          local.tee $l36
          f32.mul
          local.tee $p6
          f32.sub
          local.tee $l35
          f32.mul
          local.get $l57
          local.get $l44
          local.get $p9
          local.get $l36
          f32.mul
          local.tee $l36
          f32.sub
          local.tee $p9
          f32.mul
          f32.add
          f32.add
          local.set $l73
          local.get $l58
          local.get $l37
          f32.mul
          local.get $l61
          local.get $l35
          f32.mul
          local.get $l42
          local.get $p9
          f32.mul
          f32.add
          f32.add
          local.set $l74
          local.get $l60
          local.get $l37
          f32.mul
          local.get $l48
          local.get $l35
          f32.mul
          local.get $l62
          local.get $p9
          f32.mul
          f32.add
          f32.add
          local.set $l75
          local.get $l45
          local.get $l38
          local.get $l46
          f32.sub
          local.tee $p9
          f32.mul
          local.get $l59
          f32.const 0x1p+0 (;=1;)
          local.get $l39
          f32.sub
          local.get $l36
          f32.sub
          local.tee $l35
          f32.mul
          local.get $l57
          local.get $l34
          local.get $p6
          f32.add
          local.tee $l34
          f32.mul
          f32.add
          f32.add
          local.set $l76
          local.get $l58
          local.get $p9
          f32.mul
          local.get $l61
          local.get $l35
          f32.mul
          local.get $l42
          local.get $l34
          f32.mul
          f32.add
          f32.add
          local.set $l77
          local.get $l60
          local.get $p9
          f32.mul
          local.get $l48
          local.get $l35
          f32.mul
          local.get $l62
          local.get $l34
          f32.mul
          f32.add
          f32.add
          local.set $l78
          local.get $l48
          local.get $l51
          f32.mul
          local.get $l62
          local.get $l43
          f32.mul
          f32.add
          local.get $l60
          local.get $l49
          f32.mul
          f32.add
          local.set $l79
          i32.const 268435455
          local.set $p8
          local.get $l10
          i32.const 1360
          i32.add
          local.tee $l23
          i32.const 8
          i32.add
          local.set $l24
          f32.const 0x0p+0 (;=0;)
          local.set $l43
          f32.const 0x0p+0 (;=0;)
          local.set $l49
          f32.const 0x0p+0 (;=0;)
          local.set $l50
          f32.const 0x0p+0 (;=0;)
          local.set $l44
          f32.const 0x0p+0 (;=0;)
          local.set $l51
          f32.const 0x0p+0 (;=0;)
          local.set $l39
          f32.const 0x0p+0 (;=0;)
          local.set $l65
          f32.const 0x0p+0 (;=0;)
          local.set $l66
          f32.const 0x0p+0 (;=0;)
          local.set $l67
          f32.const 0x0p+0 (;=0;)
          local.set $l46
          f32.const 0x0p+0 (;=0;)
          local.set $l41
          f32.const 0x0p+0 (;=0;)
          local.set $l47
          block $B3 (result i32)
            block $B4
              loop $L5
                block $B6
                  local.get $l10
                  i32.const 0
                  i32.store offset=1956
                  local.get $l10
                  local.get $l53
                  local.get $l55
                  f32.add
                  f32.store offset=1436
                  local.get $l10
                  local.get $l63
                  local.get $l52
                  f32.add
                  f32.store offset=1432
                  local.get $l10
                  local.get $l54
                  local.get $l56
                  f32.add
                  f32.store offset=1428
                  local.get $l10
                  local.get $l53
                  local.get $l55
                  f32.sub
                  f32.store offset=1424
                  local.get $l10
                  local.get $l63
                  local.get $l52
                  f32.sub
                  f32.store offset=1420
                  local.get $l10
                  local.get $l54
                  local.get $l56
                  f32.sub
                  f32.store offset=1416
                  local.get $l10
                  i32.const 3124912
                  i32.store
                  local.get $l10
                  local.get $l10
                  i32.const 1952
                  i32.add
                  i32.store offset=4
                  local.get $l10
                  i32.const 1928
                  i32.add
                  local.get $l19
                  local.get $l10
                  i32.const 1416
                  i32.add
                  i32.const 1
                  local.get $l10
                  call $f70450
                  local.get $l10
                  i32.load offset=1956
                  local.tee $l13
                  i32.eqz
                  br_if $B6
                  i32.const 0
                  local.set $l17
                  local.get $l10
                  i32.const 0
                  i32.store offset=1484
                  local.get $l10
                  local.get $l53
                  f32.store offset=1480
                  local.get $l10
                  local.get $l63
                  f32.store offset=1476
                  local.get $l10
                  local.get $l54
                  f32.store offset=1472
                  local.get $l10
                  i32.const 1
                  i32.store8 offset=1388
                  local.get $l10
                  i32.const 3125888
                  i32.store offset=1344
                  local.get $l10
                  local.get $l10
                  i32.const 1488
                  i32.add
                  i32.store offset=1384
                  local.get $l10
                  local.get $l10
                  i32.const 1488
                  i32.add
                  i32.store offset=1380
                  local.get $l10
                  local.get $l10
                  i32.const 1456
                  i32.add
                  i32.store offset=1376
                  local.get $l10
                  local.get $l10
                  i32.const 1840
                  i32.add
                  i32.store offset=1392
                  local.get $l24
                  i64.const 0
                  i64.store
                  local.get $l23
                  i64.const 0
                  i64.store
                  local.get $l10
                  i32.const 0
                  i32.store offset=1340
                  local.get $l10
                  i32.const 0
                  i32.store offset=1324
                  local.get $l10
                  local.get $l70
                  f32.store offset=1320
                  local.get $l10
                  local.get $l71
                  f32.store offset=1316
                  local.get $l10
                  local.get $l72
                  f32.store offset=1312
                  local.get $l10
                  i32.const 0
                  i32.store offset=1308
                  local.get $l10
                  local.get $l73
                  f32.store offset=1304
                  local.get $l10
                  local.get $l74
                  f32.store offset=1300
                  local.get $l10
                  local.get $l75
                  f32.store offset=1296
                  local.get $l10
                  i32.const 0
                  i32.store offset=1292
                  local.get $l10
                  local.get $l76
                  f32.store offset=1288
                  local.get $l10
                  local.get $l77
                  f32.store offset=1284
                  local.get $l10
                  local.get $l78
                  f32.store offset=1280
                  local.get $l10
                  local.get $l68
                  local.get $l57
                  local.get $l63
                  f32.neg
                  local.tee $p9
                  f32.mul
                  local.get $l59
                  local.get $l54
                  f32.mul
                  f32.sub
                  local.get $l45
                  local.get $l53
                  f32.mul
                  f32.sub
                  f32.add
                  f32.store offset=1336
                  local.get $l10
                  local.get $l69
                  local.get $l42
                  local.get $p9
                  f32.mul
                  local.get $l61
                  local.get $l54
                  f32.mul
                  f32.sub
                  local.get $l58
                  local.get $l53
                  f32.mul
                  f32.sub
                  f32.add
                  f32.store offset=1332
                  local.get $l10
                  local.get $l79
                  local.get $l62
                  local.get $p9
                  f32.mul
                  local.get $l48
                  local.get $l54
                  f32.mul
                  f32.sub
                  local.get $l60
                  local.get $l53
                  f32.mul
                  f32.sub
                  f32.add
                  f32.store offset=1328
                  local.get $l13
                  i32.const 31
                  i32.add
                  i32.const 5
                  i32.shr_u
                  local.tee $l25
                  i32.eqz
                  br_if $B6
                  f32.const 0x1.fffffep+127 (;=3.40282e+38;)
                  local.set $p6
                  local.get $l13
                  local.set $p1
                  i32.const 0
                  local.set $l18
                  loop $L7
                    block $B8
                      local.get $l13
                      local.get $l17
                      i32.const 5
                      i32.shl
                      local.tee $l20
                      i32.sub
                      local.tee $p4
                      i32.const 32
                      local.get $p4
                      i32.const 32
                      i32.lt_u
                      select
                      local.tee $l21
                      if $I9
                        local.get $p1
                        i32.const 32
                        local.get $p1
                        i32.const 32
                        i32.lt_u
                        select
                        local.set $p3
                        i32.const 0
                        local.set $p4
                        loop $L10
                          local.get $l10
                          i32.const 1928
                          i32.add
                          local.get $l19
                          local.get $l10
                          local.get $p4
                          i32.const 40
                          i32.mul
                          i32.add
                          local.tee $p0
                          i32.const 0
                          i32.const 0
                          local.get $l10
                          i32.load offset=1952
                          local.get $p4
                          local.get $l20
                          i32.add
                          i32.const 2
                          i32.shl
                          i32.add
                          i32.load
                          i32.const 0
                          i32.const 0
                          call $f70452
                          local.get $p0
                          i32.const 56
                          i32.store8 offset=36
                          local.get $p4
                          i32.const 1
                          i32.add
                          local.tee $p4
                          local.get $p3
                          i32.ne
                          br_if $L10
                        end
                        local.get $l10
                        i32.const 6072
                        i32.add
                        local.get $l10
                        i32.const 1448
                        i32.add
                        i32.load
                        i32.store
                        local.get $l10
                        local.get $l10
                        i64.load offset=1440 align=4
                        i64.store offset=6064
                        i32.const 0
                        local.set $p3
                        local.get $l21
                        i32.eqz
                        br_if $B8
                        i32.const 0
                        local.set $l14
                        loop $L11
                          local.get $l10
                          i32.const 0
                          i32.store offset=1964
                          local.get $l10
                          i32.const 1768
                          i32.add
                          local.get $l10
                          i32.const 1344
                          i32.add
                          local.get $l10
                          local.get $l14
                          i32.const 40
                          i32.mul
                          i32.add
                          local.tee $p4
                          local.get $l14
                          local.get $l20
                          i32.add
                          local.tee $l26
                          local.get $p4
                          i32.load8_u offset=36
                          local.get $l10
                          i32.const 1904
                          i32.add
                          local.get $l22
                          local.get $l10
                          i32.const 1456
                          i32.add
                          local.get $l10
                          i32.const 1280
                          i32.add
                          local.get $l10
                          i32.const 1968
                          i32.add
                          local.get $l10
                          i32.const 1964
                          i32.add
                          call $f70063
                          block $B12
                            local.get $l10
                            i32.load offset=1964
                            local.tee $p4
                            i32.eqz
                            br_if $B12
                            i32.const 0
                            local.set $p0
                            local.get $l10
                            f32.load offset=2012
                            local.set $p9
                            block $B13
                              local.get $p4
                              i32.const 1
                              i32.eq
                              br_if $B13
                              local.get $p4
                              i32.const 1
                              i32.sub
                              local.tee $p0
                              i32.const 3
                              i32.and
                              local.set $p3
                              block $B14
                                local.get $p4
                                i32.const 2
                                i32.sub
                                i32.const 3
                                i32.lt_u
                                if $I15
                                  i32.const 0
                                  local.set $p0
                                  i32.const 1
                                  local.set $p4
                                  br $B14
                                end
                                local.get $p0
                                i32.const -4
                                i32.and
                                local.set $l12
                                i32.const 0
                                local.set $p0
                                i32.const 1
                                local.set $p4
                                loop $L16
                                  local.get $p4
                                  i32.const 3
                                  i32.add
                                  local.tee $l27
                                  i32.const 6
                                  i32.shl
                                  local.get $l10
                                  i32.add
                                  i32.const 2012
                                  i32.add
                                  f32.load
                                  local.tee $l35
                                  local.get $p4
                                  i32.const 2
                                  i32.add
                                  local.tee $l28
                                  i32.const 6
                                  i32.shl
                                  local.get $l10
                                  i32.add
                                  i32.const 2012
                                  i32.add
                                  f32.load
                                  local.tee $l34
                                  local.get $p4
                                  i32.const 1
                                  i32.add
                                  local.tee $l29
                                  i32.const 6
                                  i32.shl
                                  local.get $l10
                                  i32.add
                                  i32.const 2012
                                  i32.add
                                  f32.load
                                  local.tee $l37
                                  local.get $p4
                                  i32.const 6
                                  i32.shl
                                  local.get $l10
                                  i32.add
                                  i32.const 2012
                                  i32.add
                                  f32.load
                                  local.tee $l36
                                  local.get $p9
                                  local.get $p9
                                  local.get $l36
                                  f32.gt
                                  local.tee $l30
                                  select
                                  local.tee $p9
                                  local.get $p9
                                  local.get $l37
                                  f32.gt
                                  local.tee $l31
                                  select
                                  local.tee $p9
                                  local.get $p9
                                  local.get $l34
                                  f32.gt
                                  local.tee $l32
                                  select
                                  local.tee $p9
                                  local.get $p9
                                  local.get $l35
                                  f32.gt
                                  local.tee $l33
                                  select
                                  local.set $p9
                                  local.get $l27
                                  local.get $l28
                                  local.get $l29
                                  local.get $p4
                                  local.get $p0
                                  local.get $l30
                                  select
                                  local.get $l31
                                  select
                                  local.get $l32
                                  select
                                  local.get $l33
                                  select
                                  local.set $p0
                                  local.get $p4
                                  i32.const 4
                                  i32.add
                                  local.set $p4
                                  local.get $l12
                                  i32.const 4
                                  i32.sub
                                  local.tee $l12
                                  br_if $L16
                                end
                              end
                              local.get $p3
                              i32.eqz
                              br_if $B13
                              loop $L17
                                local.get $p4
                                i32.const 6
                                i32.shl
                                local.get $l10
                                i32.add
                                i32.const 2012
                                i32.add
                                f32.load
                                local.tee $l35
                                local.get $p9
                                local.get $p9
                                local.get $l35
                                f32.gt
                                local.tee $l12
                                select
                                local.set $p9
                                local.get $p4
                                local.get $p0
                                local.get $l12
                                select
                                local.set $p0
                                local.get $p4
                                i32.const 1
                                i32.add
                                local.set $p4
                                local.get $p3
                                i32.const 1
                                i32.sub
                                local.tee $p3
                                br_if $L17
                              end
                            end
                            i32.const 1
                            local.set $p3
                            local.get $p6
                            local.get $p9
                            f32.gt
                            i32.eqz
                            br_if $B12
                            local.get $l10
                            i32.const 1968
                            i32.add
                            local.get $p0
                            i32.const 6
                            i32.shl
                            i32.add
                            local.tee $p4
                            f32.load offset=16
                            local.set $l50
                            local.get $p4
                            f32.load offset=32
                            local.set $l39
                            local.get $p4
                            f32.load offset=24
                            local.set $l43
                            local.get $p4
                            f32.load offset=20
                            local.set $l49
                            local.get $p4
                            f32.load offset=40
                            local.set $l44
                            local.get $p4
                            f32.load offset=36
                            local.set $l51
                            local.get $l26
                            local.set $p8
                            local.get $p9
                            local.set $p6
                          end
                          local.get $l14
                          i32.const 1
                          i32.add
                          local.tee $l14
                          local.get $l21
                          i32.ne
                          br_if $L11
                        end
                        local.get $p3
                        local.get $l18
                        i32.or
                        local.set $l18
                        br $B8
                      end
                      local.get $l10
                      i32.const 6072
                      i32.add
                      local.get $l10
                      i32.const 1448
                      i32.add
                      i32.load
                      i32.store
                      local.get $l10
                      local.get $l10
                      i64.load offset=1440 align=4
                      i64.store offset=6064
                    end
                    local.get $l10
                    i32.const 1448
                    i32.add
                    local.get $l10
                    i32.const 6072
                    i32.add
                    i32.load
                    i32.store
                    local.get $l10
                    local.get $l10
                    i64.load offset=6064
                    i64.store offset=1440
                    local.get $p1
                    i32.const 32
                    i32.sub
                    local.set $p1
                    local.get $l17
                    i32.const 1
                    i32.add
                    local.tee $l17
                    local.get $l25
                    i32.ne
                    br_if $L7
                  end
                  local.get $l18
                  i32.const 1
                  i32.and
                  i32.eqz
                  br_if $B6
                  local.get $l10
                  f32.load offset=1480
                  local.get $l10
                  f32.load offset=1464
                  local.tee $p9
                  local.get $l50
                  local.get $l10
                  f32.load offset=1456
                  local.tee $l35
                  f32.mul
                  local.get $l49
                  local.get $l10
                  f32.load offset=1460
                  local.tee $l34
                  f32.mul
                  f32.add
                  local.get $l43
                  local.get $p9
                  f32.mul
                  f32.add
                  local.tee $l38
                  f32.mul
                  local.get $l10
                  f32.load offset=1468
                  local.tee $l37
                  local.get $l49
                  local.get $l35
                  f32.mul
                  local.get $l50
                  local.get $l34
                  f32.mul
                  f32.sub
                  f32.mul
                  local.get $l43
                  local.get $l37
                  local.get $l37
                  f32.mul
                  f32.const -0x1p-1 (;=-0.5;)
                  f32.add
                  local.tee $l36
                  f32.mul
                  f32.add
                  f32.add
                  local.tee $l40
                  local.get $l40
                  f32.add
                  f32.add
                  local.set $l65
                  local.get $l10
                  f32.load offset=1476
                  local.get $l34
                  local.get $l38
                  f32.mul
                  local.get $l37
                  local.get $l50
                  local.get $p9
                  f32.mul
                  local.get $l43
                  local.get $l35
                  f32.mul
                  f32.sub
                  f32.mul
                  local.get $l49
                  local.get $l36
                  f32.mul
                  f32.add
                  f32.add
                  local.tee $l40
                  local.get $l40
                  f32.add
                  f32.add
                  local.set $l66
                  local.get $l10
                  f32.load offset=1472
                  local.get $l35
                  local.get $l38
                  f32.mul
                  local.get $l37
                  local.get $l43
                  local.get $l34
                  f32.mul
                  local.get $l49
                  local.get $p9
                  f32.mul
                  f32.sub
                  f32.mul
                  local.get $l50
                  local.get $l36
                  f32.mul
                  f32.add
                  f32.add
                  local.tee $l38
                  local.get $l38
                  f32.add
                  f32.add
                  local.set $l67
                  local.get $p9
                  local.get $l39
                  local.get $l35
                  f32.mul
                  local.get $l51
                  local.get $l34
                  f32.mul
                  f32.add
                  local.get $l44
                  local.get $p9
                  f32.mul
                  f32.add
                  local.tee $l38
                  f32.mul
                  local.get $l37
                  local.get $l51
                  local.get $l35
                  f32.mul
                  local.get $l39
                  local.get $l34
                  f32.mul
                  f32.sub
                  f32.mul
                  local.get $l44
                  local.get $l36
                  f32.mul
                  f32.add
                  f32.add
                  local.tee $l40
                  local.get $l40
                  f32.add
                  local.set $l64
                  local.get $l34
                  local.get $l38
                  f32.mul
                  local.get $l37
                  local.get $l39
                  local.get $p9
                  f32.mul
                  local.get $l44
                  local.get $l35
                  f32.mul
                  f32.sub
                  f32.mul
                  local.get $l51
                  local.get $l36
                  f32.mul
                  f32.add
                  f32.add
                  local.tee $l40
                  local.get $l40
                  f32.add
                  local.set $l40
                  local.get $l35
                  local.get $l38
                  f32.mul
                  local.get $l37
                  local.get $l44
                  local.get $l34
                  f32.mul
                  local.get $l51
                  local.get $p9
                  f32.mul
                  f32.sub
                  f32.mul
                  local.get $l39
                  local.get $l36
                  f32.mul
                  f32.add
                  f32.add
                  local.tee $p9
                  local.get $p9
                  f32.add
                  local.set $p9
                  local.get $l10
                  i32.load offset=1952
                  local.get $p8
                  i32.const 2
                  i32.shl
                  i32.add
                  i32.load
                  local.set $p8
                  local.get $p6
                  f32.const 0x0p+0 (;=0;)
                  f32.le
                  i32.eqz
                  if $I18
                    i32.const 1
                    local.set $l15
                    local.get $l16
                    br_if $B6
                    local.get $p7
                    local.get $l64
                    f32.store offset=36
                    local.get $p7
                    local.get $l40
                    f32.store offset=32
                    local.get $p7
                    local.get $p9
                    f32.store offset=28
                    local.get $p7
                    local.get $l65
                    f32.store offset=24
                    local.get $p7
                    local.get $l66
                    f32.store offset=20
                    local.get $p7
                    local.get $l67
                    f32.store offset=16
                    local.get $p7
                    i32.const 0
                    i32.store offset=40
                    local.get $p7
                    local.get $p8
                    i32.store offset=8
                    br $B4
                  end
                  local.get $l53
                  local.get $p6
                  local.get $l64
                  f32.mul
                  local.tee $l35
                  f32.sub
                  local.set $l53
                  local.get $l63
                  local.get $p6
                  local.get $l40
                  f32.mul
                  local.tee $l34
                  f32.sub
                  local.set $l63
                  local.get $l54
                  local.get $p6
                  local.get $p9
                  f32.mul
                  local.tee $p9
                  f32.sub
                  local.set $l54
                  local.get $l46
                  local.get $l35
                  f32.sub
                  local.set $l46
                  local.get $l41
                  local.get $l34
                  f32.sub
                  local.set $l41
                  local.get $l47
                  local.get $p9
                  f32.sub
                  local.set $l47
                  i32.const 1
                  local.set $l15
                  local.get $l16
                  i32.const 1
                  i32.add
                  local.tee $l16
                  i32.const 4
                  i32.ne
                  br_if $L5
                end
              end
              i32.const 0
              local.get $l15
              i32.eqz
              br_if $B3
              drop
              local.get $p7
              local.get $l65
              f32.store offset=24
              local.get $p7
              local.get $l66
              f32.store offset=20
              local.get $p7
              local.get $l67
              f32.store offset=16
              local.get $p7
              local.get $p8
              i32.store offset=8
              local.get $p7
              local.get $l46
              local.get $l46
              f32.mul
              local.get $l41
              local.get $l41
              f32.mul
              local.get $l47
              local.get $l47
              f32.mul
              f32.add
              f32.add
              f32.sqrt
              local.tee $p9
              f32.neg
              f32.store offset=40
              local.get $p7
              local.get $l46
              f32.const 0x1p+0 (;=1;)
              local.get $p9
              f32.div
              local.tee $l35
              f32.mul
              f32.const 0x0p+0 (;=0;)
              local.get $p9
              f32.const 0x0p+0 (;=0;)
              f32.gt
              local.tee $p4
              select
              f32.store offset=36
              local.get $p7
              local.get $l41
              local.get $l35
              f32.mul
              f32.const 0x0p+0 (;=0;)
              local.get $p4
              select
              f32.store offset=32
              local.get $p7
              local.get $l47
              local.get $l35
              f32.mul
              f32.const 0x0p+0 (;=0;)
              local.get $p4
              select
              f32.store offset=28
            end
            i32.const 1
          end
          local.set $p4
          block $B19
            local.get $l10
            i32.load offset=1960
            local.tee $p0
            i32.const 0
            i32.lt_s
            br_if $B19
            local.get $p0
            i32.const 2147483647
            i32.and
            i32.eqz
            br_if $B19
            local.get $l10
            i32.load offset=1952
            local.tee $p0
            i32.eqz
            br_if $B19
            call $f69753
            local.tee $p3
            local.get $p0
            local.get $p3
            i32.load
            i32.load offset=12
            call_indirect $__indirect_function_table (type $t1)
          end
          local.get $l10
          i32.const 6080
          i32.add
          global.set $g0
          local.get $p4
          i32.eqz
          if $I20
            local.get $p7
            i32.const 0
            i32.store offset=40
            local.get $p5
            f32.load
            local.set $p6
            local.get $p5
            f32.load offset=4
            local.set $p9
            local.get $p7
            local.get $p5
            f32.load offset=8
            f32.neg
            f32.store offset=36
            local.get $p7
            local.get $p9
            f32.neg
            f32.store offset=32
            local.get $p7
            local.get $p6
            f32.neg
            f32.store offset=28
            br $B0
          end
          local.get $p7
          local.get $p7
          i32.load16_u offset=12
          i32.const 1
          i32.or
          i32.store16 offset=12
          br $B0
        end
        local.get $p7
        i32.const 0
        i32.store offset=40
        local.get $p5
        f32.load
        local.set $p6
        local.get $p5
        f32.load offset=4
        local.set $p9
        local.get $p7
        local.get $p5
        f32.load offset=8
        f32.neg
        f32.store offset=36
        local.get $p7
        local.get $p9
        f32.neg
        f32.store offset=32
        local.get $p7
        local.get $p6
        f32.neg
        f32.store offset=28
        br $B0
      end
      f32.const 0x0p+0 (;=0;)
      local.set $p9
      local.get $p7
      f32.load offset=28
      local.tee $l34
      local.get $l34
      f32.mul
      local.get $p7
      f32.load offset=32
      local.tee $l36
      local.get $l36
      f32.mul
      f32.add
      local.get $p7
      f32.load offset=36
      local.tee $l37
      local.get $l37
      f32.mul
      f32.add
      local.tee $l39
      f32.const 0x0p+0 (;=0;)
      f32.gt
      if $I21
        local.get $l37
        f32.const 0x1p+0 (;=1;)
        local.get $l39
        f32.sqrt
        f32.div
        local.tee $p9
        f32.mul
        local.set $l38
        local.get $l36
        local.get $p9
        f32.mul
        local.set $l35
        local.get $l34
        local.get $p9
        f32.mul
        local.set $p9
      end
      local.get $p8
      f32.load offset=56
      local.set $l34
      local.get $p8
      f32.load offset=52
      local.set $l36
      local.get $p8
      f32.load offset=48
      local.set $l37
      local.get $p7
      local.get $p7
      f32.load offset=40
      local.get $p6
      f32.mul
      f32.store offset=40
      local.get $p7
      local.get $l38
      f32.neg
      local.get $l38
      local.get $p9
      local.get $l37
      f32.mul
      local.get $l35
      local.get $l36
      f32.mul
      f32.add
      local.get $l38
      local.get $l34
      f32.mul
      f32.add
      f32.const 0x0p+0 (;=0;)
      f32.gt
      local.tee $p8
      select
      local.tee $p6
      local.get $p6
      f32.add
      local.tee $l38
      local.get $p3
      f32.load offset=12
      local.tee $p6
      local.get $p6
      f32.mul
      f32.const -0x1p-1 (;=-0.5;)
      f32.add
      local.tee $l39
      f32.mul
      local.get $p6
      local.get $p3
      f32.load
      local.tee $l34
      local.get $l35
      f32.neg
      local.get $l35
      local.get $p8
      select
      local.tee $l35
      local.get $l35
      f32.add
      local.tee $l35
      f32.mul
      local.get $p9
      f32.neg
      local.get $p9
      local.get $p8
      select
      local.tee $p9
      local.get $p9
      f32.add
      local.tee $p9
      local.get $p3
      f32.load offset=4
      local.tee $l36
      f32.mul
      f32.sub
      f32.mul
      f32.add
      local.get $p3
      f32.load offset=8
      local.tee $l37
      local.get $l34
      local.get $p9
      f32.mul
      local.get $l35
      local.get $l36
      f32.mul
      f32.add
      local.get $l38
      local.get $l37
      f32.mul
      f32.add
      local.tee $l40
      f32.mul
      f32.add
      f32.store offset=36
      local.get $p7
      local.get $l36
      local.get $l40
      f32.mul
      local.get $l35
      local.get $l39
      f32.mul
      local.get $p6
      local.get $p9
      local.get $l37
      f32.mul
      local.get $l34
      local.get $l38
      f32.mul
      f32.sub
      f32.mul
      f32.add
      f32.add
      f32.store offset=32
      local.get $p7
      local.get $l34
      local.get $l40
      f32.mul
      local.get $p9
      local.get $l39
      f32.mul
      local.get $p6
      local.get $l38
      local.get $l36
      f32.mul
      local.get $l35
      local.get $l37
      f32.mul
      f32.sub
      f32.mul
      f32.add
      f32.add
      f32.store offset=28
      local.get $p3
      f32.load offset=20
      local.set $l41
      local.get $p3
      f32.load offset=24
      local.set $l34
      local.get $p3
      f32.load offset=16
      local.set $l42
      local.get $p3
      f32.load offset=8
      local.set $p9
      local.get $p3
      f32.load offset=12
      local.set $p6
      local.get $p3
      f32.load
      local.set $l35
      local.get $p3
      f32.load offset=4
      local.set $l38
      local.get $p7
      i32.const 1027
      i32.store16 offset=12
      local.get $p7
      i32.const 24
      i32.add
      local.tee $p8
      local.get $l34
      local.get $p8
      f32.load
      local.tee $l34
      local.get $l34
      f32.add
      local.tee $l34
      local.get $p6
      local.get $p6
      f32.mul
      f32.const -0x1p-1 (;=-0.5;)
      f32.add
      local.tee $l39
      f32.mul
      local.get $p6
      local.get $l35
      local.get $p7
      i32.const 20
      i32.add
      local.tee $p8
      f32.load
      local.tee $l36
      local.get $l36
      f32.add
      local.tee $l36
      f32.mul
      local.get $l38
      local.get $p7
      f32.load offset=16
      local.tee $l37
      local.get $l37
      f32.add
      local.tee $l37
      f32.mul
      f32.sub
      f32.mul
      f32.add
      local.get $p9
      local.get $l37
      local.get $l35
      f32.mul
      local.get $l36
      local.get $l38
      f32.mul
      f32.add
      local.get $l34
      local.get $p9
      f32.mul
      f32.add
      local.tee $l40
      f32.mul
      f32.add
      f32.add
      f32.store
      local.get $p8
      local.get $l41
      local.get $l38
      local.get $l40
      f32.mul
      local.get $l36
      local.get $l39
      f32.mul
      local.get $p6
      local.get $l37
      local.get $p9
      f32.mul
      local.get $l34
      local.get $l35
      f32.mul
      f32.sub
      f32.mul
      f32.add
      f32.add
      f32.add
      f32.store
      local.get $p7
      local.get $l42
      local.get $l35
      local.get $l40
      f32.mul
      local.get $l37
      local.get $l39
      f32.mul
      local.get $p6
      local.get $l34
      local.get $l38
      f32.mul
      local.get $l36
      local.get $p9
      f32.mul
      f32.sub
      f32.mul
      f32.add
      f32.add
      f32.add
      f32.store offset=16
    end
    local.get $p2
    i32.const 288
    i32.add
    global.set $g0
    local.get $l11
    i32.const 0
    i32.ne)
