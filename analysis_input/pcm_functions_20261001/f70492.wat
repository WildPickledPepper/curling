  (func $f70492 (type $t171) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 f32) (param $p7 i32) (param $p8 i32) (param $p9 f32) (param $p10 i32) (param $p11 f32) (result f32)
    (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 i32) (local $l17 i32) (local $l18 i32) (local $l19 i32) (local $l20 i32) (local $l21 i32) (local $l22 i32) (local $l23 i32) (local $l24 i32) (local $l25 i32) (local $l26 i32) (local $l27 i32) (local $l28 i32) (local $l29 i32) (local $l30 i32) (local $l31 i32) (local $l32 i32) (local $l33 i32) (local $l34 i32) (local $l35 f32) (local $l36 f32) (local $l37 f32) (local $l38 f32) (local $l39 f32) (local $l40 f32) (local $l41 f32) (local $l42 f32) (local $l43 f32) (local $l44 f32) (local $l45 f32) (local $l46 f32) (local $l47 f32) (local $l48 f32) (local $l49 f32) (local $l50 f32) (local $l51 f32) (local $l52 f32) (local $l53 f32) (local $l54 f32) (local $l55 f32) (local $l56 f32) (local $l57 f32) (local $l58 f32) (local $l59 f32) (local $l60 f32) (local $l61 f32) (local $l62 f32) (local $l63 f32) (local $l64 f32) (local $l65 f32) (local $l66 f32) (local $l67 f32) (local $l68 f32) (local $l69 f32) (local $l70 f32) (local $l71 f32) (local $l72 f32) (local $l73 f32) (local $l74 f32) (local $l75 f32) (local $l76 f32) (local $l77 f32) (local $l78 f32) (local $l79 f32) (local $l80 f32) (local $l81 f32) (local $l82 f32) (local $l83 f32) (local $l84 f32) (local $l85 f32) (local $l86 f32) (local $l87 i64) (local $l88 i64)
    global.get $g0
    i32.const 416
    i32.sub
    local.tee $p10
    global.set $g0
    local.get $p1
    i32.load
    local.set $p1
    local.get $p0
    i32.load
    local.set $p0
    local.get $p10
    i64.const 0
    i64.store offset=72
    local.get $p10
    i64.const 0
    i64.store offset=64
    local.get $p10
    i32.const 0
    i32.store8 offset=96
    local.get $p10
    i64.const 17179869184
    i64.store offset=88
    local.get $p10
    i64.const 0
    i64.store offset=80
    local.get $p0
    f32.load offset=4
    local.set $p9
    local.get $p0
    f32.load offset=8
    local.set $l45
    local.get $p10
    i32.const 0
    i32.store offset=140
    local.get $p10
    i32.const 0
    i32.store offset=124
    local.get $p10
    local.get $l45
    f32.const 0x0p+0 (;=0;)
    f32.mul
    local.tee $l47
    f32.store offset=120
    local.get $p10
    local.get $l47
    f32.store offset=116
    local.get $p10
    local.get $l47
    f32.neg
    local.tee $l47
    f32.store offset=136
    local.get $p10
    local.get $l47
    f32.store offset=132
    local.get $p10
    local.get $p9
    f32.store offset=144
    local.get $p10
    local.get $l45
    f32.store offset=112
    local.get $p10
    i32.const 1
    i32.store8 offset=96
    local.get $p10
    local.get $p9
    f32.store offset=88
    local.get $p10
    local.get $p9
    f32.store offset=84
    local.get $p10
    local.get $p9
    f32.store offset=80
    local.get $p10
    local.get $l45
    f32.neg
    f32.store offset=128
    local.get $p10
    i64.const 0
    i64.store offset=8
    local.get $p10
    i64.const 0
    i64.store
    local.get $p10
    i32.const 0
    i32.store8 offset=32
    local.get $p10
    i64.const 12884901888
    i64.store offset=24
    local.get $p10
    i64.const 0
    i64.store offset=16
    local.get $p1
    f32.load offset=4
    local.set $p9
    local.get $p1
    f32.load offset=8
    local.set $l45
    local.get $p1
    f32.load offset=12
    local.set $l47
    local.get $p10
    i32.const 0
    i32.store offset=60
    local.get $p10
    local.get $l47
    f32.store offset=56
    local.get $p10
    local.get $l45
    f32.store offset=52
    local.get $p10
    local.get $p9
    f32.store offset=48
    local.get $p10
    local.get $p9
    local.get $l45
    local.get $p9
    local.get $l45
    f32.le
    select
    local.tee $p9
    local.get $l47
    local.get $p9
    local.get $l47
    f32.le
    select
    local.tee $p9
    f32.const 0x1.99999ap-5 (;=0.05;)
    f32.mul
    f32.store offset=24
    local.get $p10
    local.get $p9
    f32.const 0x1.47ae14p-8 (;=0.005;)
    f32.mul
    f32.store offset=20
    local.get $p10
    local.get $p9
    f32.const 0x1.47ae14p-7 (;=0.01;)
    f32.mul
    f32.store offset=16
    local.get $p0
    f32.load offset=4
    local.set $l39
    local.get $p10
    i64.const 0
    i64.store offset=408
    local.get $p10
    i64.const 0
    i64.store offset=400
    local.get $p5
    f32.load offset=20
    local.set $l76
    local.get $p4
    f32.load offset=20
    local.set $l71
    local.get $p5
    f32.load offset=24
    local.set $l77
    local.get $p4
    f32.load offset=24
    local.set $l72
    local.get $p2
    f32.load offset=8
    local.set $l50
    local.get $p2
    f32.load
    local.set $l43
    local.get $p2
    f32.load offset=4
    local.set $l44
    local.get $p2
    f32.load offset=12
    local.set $l36
    local.get $p3
    f32.load offset=12
    local.set $l47
    local.get $p3
    f32.load
    local.set $p9
    local.get $p5
    f32.load offset=16
    local.set $l78
    local.get $p4
    f32.load offset=16
    local.set $l73
    local.get $p3
    f32.load offset=4
    local.set $l55
    local.get $p3
    f32.load offset=8
    local.set $l45
    local.get $p10
    i32.const 0
    i32.store offset=396
    local.get $p10
    i32.const 0
    i32.store offset=380
    local.get $p10
    i32.const 0
    i32.store offset=364
    local.get $p10
    i32.const 392
    i32.add
    local.tee $p0
    local.get $l47
    local.get $l47
    f32.mul
    f32.const -0x1p-1 (;=-0.5;)
    f32.add
    local.tee $l60
    local.get $l72
    local.get $l77
    f32.sub
    local.tee $p11
    f32.mul
    local.get $l47
    local.get $l55
    local.get $l73
    local.get $l78
    f32.sub
    local.tee $l49
    f32.mul
    local.get $p9
    local.get $l71
    local.get $l76
    f32.sub
    local.tee $l38
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l45
    local.get $l38
    local.get $l55
    f32.neg
    local.tee $l40
    f32.mul
    local.get $p9
    local.get $l49
    f32.mul
    f32.sub
    local.get $l45
    local.get $p11
    f32.mul
    f32.sub
    local.tee $l35
    f32.mul
    f32.sub
    local.tee $l37
    local.get $l37
    f32.add
    f32.store
    local.get $p10
    local.get $l60
    local.get $l38
    f32.mul
    local.get $l47
    local.get $p9
    local.get $p11
    f32.mul
    local.get $l45
    local.get $l49
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l55
    local.get $l35
    f32.mul
    f32.sub
    local.tee $l37
    local.get $l37
    f32.add
    f32.store offset=388
    local.get $p10
    i32.const 384
    i32.add
    local.tee $p4
    local.get $l60
    local.get $l49
    f32.mul
    local.get $l47
    local.get $l45
    local.get $l38
    f32.mul
    local.get $l55
    local.get $p11
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $p9
    local.get $l35
    f32.mul
    f32.sub
    local.tee $p11
    local.get $p11
    f32.add
    f32.store
    local.get $p10
    i32.const 376
    i32.add
    local.tee $l17
    f32.const 0x1p+0 (;=1;)
    local.get $l44
    local.get $l45
    f32.mul
    local.get $l50
    local.get $l55
    f32.mul
    f32.sub
    local.get $l43
    local.get $l47
    f32.mul
    local.get $l36
    local.get $p9
    f32.mul
    f32.sub
    f32.add
    local.tee $p11
    local.get $p11
    local.get $p11
    f32.add
    local.tee $l49
    f32.mul
    f32.sub
    local.tee $l37
    local.get $l50
    local.get $p9
    f32.mul
    local.get $l43
    local.get $l45
    f32.mul
    f32.sub
    local.get $l44
    local.get $l47
    f32.mul
    local.get $l36
    local.get $l55
    f32.mul
    f32.sub
    f32.add
    local.tee $l38
    local.get $l38
    local.get $l38
    f32.add
    local.tee $l35
    f32.mul
    local.tee $l42
    f32.sub
    f32.store
    local.get $p10
    local.get $l43
    local.get $l55
    f32.mul
    local.get $l44
    local.get $p9
    f32.mul
    f32.sub
    local.get $l50
    local.get $l47
    f32.mul
    local.get $l36
    local.get $l45
    f32.mul
    f32.sub
    f32.add
    local.tee $p11
    local.get $l35
    f32.mul
    local.tee $l46
    local.get $l36
    local.get $l47
    f32.mul
    local.get $l44
    local.get $l40
    f32.mul
    local.get $l43
    local.get $p9
    f32.mul
    f32.sub
    local.get $l50
    local.get $l45
    f32.mul
    f32.sub
    f32.sub
    local.tee $l50
    local.get $l49
    f32.mul
    local.tee $l43
    f32.sub
    f32.store offset=372
    local.get $p10
    i32.const 368
    i32.add
    local.tee $l24
    local.get $p11
    local.get $l49
    f32.mul
    local.tee $l44
    local.get $l50
    local.get $l35
    f32.mul
    local.tee $l36
    f32.add
    f32.store
    local.get $p10
    i32.const 360
    i32.add
    local.tee $p5
    local.get $l46
    local.get $l43
    f32.add
    f32.store
    local.get $p10
    local.get $l37
    local.get $p11
    local.get $p11
    local.get $p11
    f32.add
    local.tee $l43
    f32.mul
    local.tee $p11
    f32.sub
    f32.store offset=356
    local.get $p10
    i32.const 352
    i32.add
    local.tee $p1
    local.get $l38
    local.get $l49
    f32.mul
    local.tee $l49
    local.get $l50
    local.get $l43
    f32.mul
    local.tee $l50
    f32.sub
    f32.store
    local.get $p10
    i32.const 0
    i32.store offset=348
    local.get $p10
    local.get $l44
    local.get $l36
    f32.sub
    f32.store offset=344
    local.get $p10
    local.get $l49
    local.get $l50
    f32.add
    f32.store offset=340
    local.get $p10
    f32.const 0x1p+0 (;=1;)
    local.get $l42
    f32.sub
    local.get $p11
    f32.sub
    f32.store offset=336
    local.get $p3
    f32.load offset=20
    local.set $l43
    local.get $p2
    f32.load offset=20
    local.set $l44
    local.get $p3
    f32.load offset=24
    local.set $l36
    local.get $p2
    f32.load offset=24
    local.set $p11
    local.get $p3
    f32.load offset=16
    local.set $l50
    local.get $p2
    f32.load offset=16
    local.set $l49
    local.get $p10
    i32.const 0
    i32.store offset=332
    local.get $p10
    local.get $l45
    local.get $p9
    local.get $l50
    local.get $l78
    f32.sub
    local.get $l49
    local.get $l73
    f32.sub
    local.tee $l73
    f32.sub
    local.tee $l50
    f32.mul
    local.get $l55
    local.get $l43
    local.get $l76
    f32.sub
    local.get $l44
    local.get $l71
    f32.sub
    local.tee $l71
    f32.sub
    local.tee $l43
    f32.mul
    f32.add
    local.get $l45
    local.get $l36
    local.get $l77
    f32.sub
    local.get $p11
    local.get $l72
    f32.sub
    local.tee $l72
    f32.sub
    local.tee $l44
    f32.mul
    f32.add
    local.tee $l36
    f32.mul
    local.get $l60
    local.get $l44
    f32.mul
    local.get $l47
    local.get $p9
    local.get $l43
    f32.mul
    local.get $l55
    local.get $l50
    f32.mul
    f32.sub
    f32.mul
    f32.sub
    f32.add
    local.tee $p11
    local.get $p11
    f32.add
    f32.store offset=328
    local.get $p10
    local.get $l55
    local.get $l36
    f32.mul
    local.get $l60
    local.get $l43
    f32.mul
    local.get $l47
    local.get $l45
    local.get $l50
    f32.mul
    local.get $p9
    local.get $l44
    f32.mul
    f32.sub
    f32.mul
    f32.sub
    f32.add
    local.tee $p11
    local.get $p11
    f32.add
    f32.store offset=324
    local.get $p10
    local.get $p9
    local.get $l36
    f32.mul
    local.get $l60
    local.get $l50
    f32.mul
    local.get $l47
    local.get $l55
    local.get $l44
    f32.mul
    local.get $l45
    local.get $l43
    f32.mul
    f32.sub
    f32.mul
    f32.sub
    f32.add
    local.tee $l50
    local.get $l50
    f32.add
    f32.store offset=320
    local.get $p10
    i32.const 0
    i32.store offset=256
    local.get $p10
    i32.const 3132452
    i32.store offset=176
    local.get $p10
    local.get $p10
    i32.const 336
    i32.add
    i32.store offset=184
    local.get $p10
    local.get $p10
    i32.const -64
    i32.sub
    i32.store offset=180
    local.get $p10
    i32.const 208
    i32.add
    local.tee $p3
    local.get $p1
    i64.load
    i64.store
    local.get $p10
    i32.const 216
    i32.add
    local.tee $p2
    local.get $p5
    i64.load
    i64.store
    local.get $p10
    i32.const 200
    i32.add
    local.tee $p5
    local.get $p10
    i64.load offset=344
    i64.store
    local.get $p10
    i32.const 224
    i32.add
    local.tee $p1
    local.get $l24
    i64.load
    i64.store
    local.get $p10
    local.get $l17
    i64.load
    i64.store offset=232
    local.get $p10
    local.get $p4
    i64.load
    i64.store offset=240
    local.get $p10
    local.get $p0
    i64.load
    i64.store offset=248
    local.get $p10
    local.get $p10
    i64.load offset=336
    i64.store offset=192
    local.get $p10
    i32.const 196
    i32.add
    local.tee $p0
    f32.load
    local.set $l50
    local.get $p0
    local.get $p3
    f32.load
    f32.store
    local.get $p2
    f32.load
    local.set $l43
    local.get $p5
    f32.load
    local.set $l44
    local.get $p5
    local.get $p1
    f32.load
    f32.store
    local.get $p2
    local.get $p10
    i32.const 228
    i32.add
    local.tee $p5
    f32.load
    f32.store
    local.get $p1
    local.get $l44
    f32.store
    local.get $p5
    local.get $l43
    f32.store
    local.get $p3
    local.get $l50
    f32.store
    local.get $p10
    i32.const 3132536
    i32.store offset=168
    local.get $p10
    local.get $p10
    i32.store offset=172
    f32.const 0x1.fffffep+127 (;=3.40282e+38;)
    local.set $l50
    local.get $p10
    i32.const 304
    i32.add
    local.set $p3
    local.get $p10
    i32.const 272
    i32.add
    local.set $l31
    local.get $p10
    i32.const 288
    i32.add
    local.set $l32
    global.get $g0
    i32.const 288
    i32.sub
    local.tee $p0
    global.set $g0
    local.get $p0
    i32.const 240
    i32.add
    local.set $p5
    local.get $p0
    i32.const 256
    i32.add
    local.set $l25
    local.get $p0
    i32.const 272
    i32.add
    local.set $l26
    local.get $l39
    local.get $p6
    f32.add
    f32.const 0x0p+0 (;=0;)
    f32.add
    local.set $l86
    global.get $g0
    i32.const 272
    i32.sub
    local.tee $l13
    global.set $g0
    local.get $l13
    i64.const 0
    i64.store offset=264
    local.get $l13
    i64.const 0
    i64.store offset=256
    local.get $p10
    i32.const 400
    i32.add
    local.tee $l27
    f32.load offset=8
    local.set $l51
    local.get $l27
    f32.load offset=4
    local.set $l54
    local.get $l27
    f32.load
    local.set $l61
    local.get $p10
    i32.const 320
    i32.add
    local.tee $l29
    local.tee $l24
    f32.load offset=8
    local.set $l62
    local.get $l24
    f32.load offset=4
    local.set $l63
    local.get $l24
    f32.load
    local.set $l66
    local.get $l13
    i32.const 1
    i32.store offset=240
    local.get $p10
    i32.const 168
    i32.add
    local.tee $l33
    local.tee $p2
    i32.load offset=4
    local.tee $p1
    f32.load offset=52
    local.set $l37
    local.get $p10
    i32.const 176
    i32.add
    local.tee $l30
    local.tee $l19
    i32.load offset=8
    local.tee $l15
    f32.load offset=52
    local.set $l74
    local.get $l15
    f32.load offset=36
    local.set $l69
    local.get $l15
    f32.load offset=20
    local.set $l57
    local.get $p1
    f32.load offset=56
    local.set $l40
    local.get $l15
    f32.load offset=56
    local.set $l56
    local.get $l15
    f32.load offset=40
    local.set $l58
    local.get $l15
    f32.load offset=24
    local.set $l64
    local.get $l19
    i32.load offset=4
    local.tee $l17
    f32.load offset=56
    local.set $l39
    local.get $l17
    f32.load offset=52
    local.set $l41
    local.get $l17
    f32.load offset=72
    local.set $l52
    local.get $l19
    f32.load offset=56
    local.set $l65
    local.get $l19
    f32.load offset=40
    local.set $l80
    local.get $l19
    f32.load offset=24
    local.set $l81
    local.get $l19
    f32.load offset=48
    local.set $l82
    local.get $l19
    f32.load offset=32
    local.set $l43
    local.get $l17
    f32.load offset=68
    local.set $l48
    local.get $l19
    f32.load offset=52
    local.set $l44
    local.get $l19
    f32.load offset=36
    local.set $l49
    local.get $l19
    f32.load offset=20
    local.set $l75
    local.get $p1
    f32.load offset=48
    local.set $l42
    local.get $l15
    f32.load offset=48
    local.set $l83
    local.get $l15
    f32.load offset=32
    local.set $l70
    local.get $l15
    f32.load
    local.set $l84
    local.get $l15
    f32.load offset=16
    local.set $p11
    local.get $l15
    f32.load offset=4
    local.set $p6
    local.get $l15
    f32.load offset=8
    local.set $l46
    local.get $l17
    f32.load offset=48
    local.set $l53
    local.get $l17
    f32.load offset=64
    local.set $l59
    local.get $l19
    f32.load offset=16
    local.set $l85
    local.get $p4
    f32.load offset=8
    local.set $l36
    local.get $p4
    f32.load
    local.set $l35
    local.get $p4
    f32.load offset=4
    local.set $l38
    local.get $l13
    i64.const 0
    i64.store offset=196 align=4
    local.get $l13
    i64.const 0
    i64.store offset=204 align=4
    local.get $l13
    i64.const 0
    i64.store offset=212 align=4
    local.get $l13
    i64.const 0
    i64.store offset=220 align=4
    local.get $l13
    i64.const 0
    i64.store offset=228 align=4
    local.get $l13
    i32.const 0
    i32.store offset=236
    local.get $l13
    i64.const 0
    i64.store offset=188 align=4
    local.get $l13
    local.get $l56
    local.get $l46
    local.get $l53
    local.get $l59
    local.get $l53
    local.get $l43
    local.get $l38
    f32.const 0x0p+0 (;=0;)
    local.get $l35
    local.get $l35
    f32.mul
    local.get $l38
    local.get $l38
    f32.mul
    f32.add
    local.get $l36
    local.get $l36
    f32.mul
    f32.add
    f32.const 0x1p-23 (;=1.19209e-07;)
    f32.gt
    local.tee $l15
    select
    local.tee $l38
    f32.const 0x1p+0 (;=1;)
    local.get $l36
    f32.const 0x0p+0 (;=0;)
    local.get $l15
    select
    local.tee $l36
    local.get $l36
    f32.mul
    local.get $l35
    f32.const 0x1p+0 (;=1;)
    local.get $l15
    select
    local.tee $l35
    local.get $l35
    f32.mul
    local.get $l38
    local.get $l38
    f32.mul
    f32.add
    f32.add
    f32.sqrt
    f32.div
    local.tee $l67
    f32.mul
    local.tee $l46
    f32.neg
    local.tee $l68
    f32.mul
    local.get $l85
    local.get $l35
    local.get $l67
    f32.mul
    local.tee $l38
    f32.mul
    f32.sub
    local.get $l82
    local.get $l36
    local.get $l67
    f32.mul
    local.tee $l36
    f32.mul
    f32.sub
    local.tee $l35
    f32.mul
    local.get $l41
    local.get $l49
    local.get $l68
    f32.mul
    local.get $l75
    local.get $l38
    f32.mul
    f32.sub
    local.get $l44
    local.get $l36
    f32.mul
    f32.sub
    local.tee $l67
    f32.mul
    f32.add
    local.get $l39
    local.get $l80
    local.get $l68
    f32.mul
    local.get $l81
    local.get $l38
    f32.mul
    f32.sub
    local.get $l36
    local.get $l65
    f32.mul
    f32.sub
    local.tee $l68
    f32.mul
    f32.add
    local.get $l35
    local.get $l59
    f32.mul
    local.get $l67
    local.get $l48
    f32.mul
    f32.add
    local.get $l68
    local.get $l52
    f32.mul
    f32.add
    f32.gt
    local.tee $l15
    select
    local.tee $l53
    f32.mul
    local.get $l64
    local.get $l41
    local.get $l48
    local.get $l15
    select
    local.tee $l41
    f32.mul
    f32.add
    local.get $l58
    local.get $l39
    local.get $l52
    local.get $l15
    select
    local.tee $l39
    f32.mul
    f32.add
    f32.add
    local.tee $l52
    local.get $l40
    local.get $l40
    f32.neg
    local.get $l36
    f32.const 0x0p+0 (;=0;)
    f32.gt
    select
    local.tee $l40
    f32.sub
    local.tee $l36
    f32.store offset=184
    local.get $l13
    local.get $l74
    local.get $l53
    local.get $p6
    f32.mul
    local.get $l41
    local.get $l57
    f32.mul
    f32.add
    local.get $l39
    local.get $l69
    f32.mul
    f32.add
    f32.add
    local.tee $l48
    local.get $l37
    local.get $l37
    f32.neg
    local.get $l46
    f32.const 0x0p+0 (;=0;)
    f32.gt
    select
    local.tee $l37
    f32.sub
    local.tee $l35
    f32.store offset=180
    local.get $l13
    local.get $l83
    local.get $l53
    local.get $l84
    f32.mul
    local.get $l41
    local.get $p11
    f32.mul
    f32.add
    local.get $l39
    local.get $l70
    f32.mul
    f32.add
    f32.add
    local.tee $l39
    local.get $l42
    local.get $l42
    f32.neg
    local.get $l38
    f32.const 0x0p+0 (;=0;)
    f32.gt
    select
    local.tee $l41
    f32.sub
    local.tee $l38
    f32.store offset=176
    local.get $l13
    i64.const 0
    i64.store offset=132 align=4
    local.get $l13
    i64.const 0
    i64.store offset=140 align=4
    local.get $l13
    i64.const 0
    i64.store offset=148 align=4
    local.get $l13
    i64.const 0
    i64.store offset=156 align=4
    local.get $l13
    i64.const 0
    i64.store offset=164 align=4
    local.get $l13
    i32.const 0
    i32.store offset=172
    local.get $l13
    i64.const 0
    i64.store offset=124 align=4
    local.get $l13
    local.get $l52
    f32.store offset=120
    local.get $l13
    local.get $l48
    f32.store offset=116
    local.get $l13
    local.get $l39
    f32.store offset=112
    local.get $l13
    i64.const 0
    i64.store offset=68 align=4
    local.get $l13
    i64.const 0
    i64.store offset=76 align=4
    local.get $l13
    i64.const 0
    i64.store offset=84 align=4
    local.get $l13
    i64.const 0
    i64.store offset=92 align=4
    local.get $l13
    i64.const 0
    i64.store offset=100 align=4
    local.get $l13
    i32.const 0
    i32.store offset=108
    local.get $l13
    i64.const 0
    i64.store offset=60 align=4
    local.get $l13
    local.get $l40
    f32.store offset=56
    local.get $l13
    local.get $l37
    f32.store offset=52
    local.get $l13
    local.get $l41
    f32.store offset=48
    local.get $l36
    f32.neg
    local.set $l37
    local.get $l35
    f32.neg
    local.set $l40
    local.get $l38
    f32.neg
    local.set $l39
    i32.const -1
    local.set $l15
    block $B0
      block $B1
        local.get $l38
        local.get $l38
        f32.mul
        local.get $l35
        local.get $l35
        f32.mul
        f32.add
        local.get $l36
        local.get $l36
        f32.mul
        f32.add
        local.tee $l42
        local.get $p1
        f32.load offset=24
        local.tee $l41
        f32.const 0x0p+0 (;=0;)
        local.get $l41
        f32.const 0x0p+0 (;=0;)
        f32.lt
        select
        f32.const 0x1.99999ap-4 (;=0.1;)
        f32.mul
        local.tee $l41
        local.get $l41
        f32.mul
        local.tee $l85
        f32.gt
        i32.eqz
        if $I2
          local.get $l39
          local.set $p11
          local.get $l40
          local.set $p6
          local.get $l37
          local.set $l46
          f32.const 0x0p+0 (;=0;)
          local.set $l56
          local.get $l38
          local.set $l43
          local.get $l35
          local.set $l44
          local.get $l36
          local.set $l49
          br $B1
        end
        local.get $l41
        local.get $l86
        f32.add
        local.tee $l75
        local.get $l75
        f32.mul
        local.set $l83
        local.get $l66
        f32.const 0x0p+0 (;=0;)
        f32.mul
        local.get $l61
        f32.add
        local.set $l58
        local.get $l63
        f32.const 0x0p+0 (;=0;)
        f32.mul
        local.get $l54
        f32.add
        local.set $l64
        local.get $l62
        f32.const 0x0p+0 (;=0;)
        f32.mul
        local.get $l51
        f32.add
        local.set $l65
        f32.const 0x0p+0 (;=0;)
        local.set $l56
        local.get $l37
        local.set $l46
        local.get $l40
        local.set $p6
        local.get $l39
        local.set $p11
        loop $L3
          local.get $l38
          local.set $l43
          local.get $l35
          local.set $l44
          local.get $l36
          local.set $l49
          block $B4
            local.get $l40
            f32.const 0x1p+0 (;=1;)
            local.get $l39
            local.get $l39
            f32.mul
            local.get $l40
            local.get $l40
            f32.mul
            f32.add
            local.get $l37
            local.get $l37
            f32.mul
            f32.add
            f32.sqrt
            f32.div
            local.tee $l38
            f32.mul
            local.tee $l36
            local.get $l19
            i32.load offset=8
            local.tee $l15
            f32.load offset=52
            local.get $l19
            i32.load offset=4
            local.tee $l17
            f32.load offset=48
            local.tee $l41
            local.get $l17
            f32.load offset=64
            local.tee $l52
            local.get $l41
            local.get $l39
            local.get $l38
            f32.mul
            local.tee $l35
            local.get $l19
            f32.load offset=16
            f32.mul
            local.get $l36
            local.get $l19
            f32.load offset=32
            f32.mul
            f32.add
            local.get $l37
            local.get $l38
            f32.mul
            local.tee $l38
            local.get $l19
            f32.load offset=48
            f32.mul
            f32.add
            local.tee $l48
            f32.mul
            local.get $l35
            local.get $l19
            f32.load offset=20
            f32.mul
            local.get $l36
            local.get $l19
            f32.load offset=36
            f32.mul
            f32.add
            local.get $l38
            local.get $l19
            f32.load offset=52
            f32.mul
            f32.add
            local.tee $l41
            local.get $l17
            f32.load offset=52
            local.tee $l53
            f32.mul
            f32.add
            local.get $l35
            local.get $l19
            f32.load offset=24
            f32.mul
            local.get $l36
            local.get $l19
            f32.load offset=40
            f32.mul
            f32.add
            local.get $l38
            local.get $l19
            f32.load offset=56
            f32.mul
            f32.add
            local.tee $l59
            local.get $l17
            f32.load offset=56
            local.tee $l67
            f32.mul
            f32.add
            local.get $l48
            local.get $l52
            f32.mul
            local.get $l41
            local.get $l17
            f32.load offset=68
            local.tee $l52
            f32.mul
            f32.add
            local.get $l59
            local.get $l17
            f32.load offset=72
            local.tee $l48
            f32.mul
            f32.add
            f32.gt
            local.tee $l17
            select
            local.tee $l41
            local.get $l15
            f32.load offset=4
            f32.mul
            local.get $l53
            local.get $l52
            local.get $l17
            select
            local.tee $l52
            local.get $l15
            f32.load offset=20
            f32.mul
            f32.add
            local.get $l67
            local.get $l48
            local.get $l17
            select
            local.tee $l48
            local.get $l15
            f32.load offset=36
            f32.mul
            f32.add
            f32.add
            local.tee $l67
            local.get $l64
            local.get $p2
            i32.load offset=4
            local.tee $l17
            f32.load offset=52
            local.tee $l53
            local.get $l53
            f32.neg
            local.get $l36
            f32.const 0x0p+0 (;=0;)
            f32.lt
            select
            local.tee $l80
            f32.add
            local.tee $l68
            f32.sub
            local.tee $l53
            f32.neg
            f32.mul
            local.get $l35
            local.get $l15
            f32.load offset=48
            local.get $l41
            local.get $l15
            f32.load
            f32.mul
            local.get $l52
            local.get $l15
            f32.load offset=16
            f32.mul
            f32.add
            local.get $l48
            local.get $l15
            f32.load offset=32
            f32.mul
            f32.add
            f32.add
            local.tee $l74
            local.get $l58
            local.get $l17
            f32.load offset=48
            local.tee $l59
            local.get $l59
            f32.neg
            local.get $l35
            f32.const 0x0p+0 (;=0;)
            f32.lt
            select
            local.tee $l81
            f32.add
            local.tee $l69
            f32.sub
            local.tee $l59
            f32.mul
            f32.sub
            local.get $l38
            local.get $l15
            f32.load offset=56
            local.get $l41
            local.get $l15
            f32.load offset=8
            f32.mul
            local.get $l52
            local.get $l15
            f32.load offset=24
            f32.mul
            f32.add
            local.get $l48
            local.get $l15
            f32.load offset=40
            f32.mul
            f32.add
            f32.add
            local.tee $l52
            local.get $l65
            local.get $l17
            f32.load offset=56
            local.tee $l41
            local.get $l41
            f32.neg
            local.get $l38
            f32.const 0x0p+0 (;=0;)
            f32.lt
            select
            local.tee $l82
            f32.add
            local.tee $l48
            f32.sub
            local.tee $l41
            f32.mul
            f32.sub
            local.get $l75
            f32.sub
            local.tee $l57
            f32.const 0x0p+0 (;=0;)
            f32.gt
            i32.eqz
            if $I5
              local.get $l42
              local.set $l57
              br $B4
            end
            i32.const 0
            local.set $l15
            local.get $l35
            local.get $l24
            f32.load
            local.tee $l70
            f32.mul
            local.get $l36
            local.get $l24
            f32.load offset=4
            local.tee $l35
            f32.mul
            f32.add
            local.get $l38
            local.get $l24
            f32.load offset=8
            local.tee $l84
            f32.mul
            f32.add
            local.tee $l36
            f32.const 0x0p+0 (;=0;)
            f32.ge
            br_if $B0
            local.get $l56
            local.get $l57
            local.get $l36
            f32.div
            f32.sub
            local.tee $l36
            local.get $l56
            f32.gt
            if $I6 (result f32)
              local.get $l36
              f32.const 0x1p+0 (;=1;)
              f32.gt
              br_if $B0
              local.get $l27
              f32.load offset=8
              local.set $l42
              local.get $l27
              f32.load offset=4
              local.set $l48
              local.get $l27
              f32.load
              local.set $l38
              local.get $l13
              i32.const 0
              i32.store offset=92
              local.get $l13
              i32.const 0
              i32.store offset=76
              local.get $l13
              i32.const 0
              i32.store offset=60
              local.get $l13
              local.get $l38
              local.get $l70
              local.get $l36
              f32.mul
              f32.add
              local.tee $l38
              local.get $l58
              f32.sub
              local.tee $l41
              local.get $l13
              f32.load offset=80
              f32.add
              local.tee $l59
              f32.store offset=80
              local.get $l13
              local.get $l48
              local.get $l35
              local.get $l36
              f32.mul
              f32.add
              local.tee $l35
              local.get $l64
              f32.sub
              local.tee $l48
              local.get $l13
              f32.load offset=84
              f32.add
              local.tee $l68
              f32.store offset=84
              local.get $l13
              local.get $l42
              local.get $l84
              local.get $l36
              f32.mul
              f32.add
              local.tee $l42
              local.get $l65
              f32.sub
              local.tee $l53
              local.get $l13
              f32.load offset=88
              f32.add
              local.tee $l69
              f32.store offset=88
              local.get $l13
              local.get $l41
              local.get $l13
              f32.load offset=64
              f32.add
              local.tee $l57
              f32.store offset=64
              local.get $l13
              local.get $l48
              local.get $l13
              f32.load offset=68
              f32.add
              local.tee $l56
              f32.store offset=68
              local.get $l13
              local.get $l53
              local.get $l13
              f32.load offset=72
              f32.add
              local.tee $l58
              f32.store offset=72
              local.get $l13
              local.get $l41
              local.get $l13
              f32.load offset=48
              f32.add
              local.tee $l41
              f32.store offset=48
              local.get $l13
              local.get $l48
              local.get $l13
              f32.load offset=52
              f32.add
              local.tee $l48
              f32.store offset=52
              local.get $l13
              local.get $l53
              local.get $l13
              f32.load offset=56
              f32.add
              local.tee $l53
              f32.store offset=56
              local.get $l13
              f32.load offset=112
              local.set $l64
              local.get $l13
              f32.load offset=116
              local.set $l65
              local.get $l13
              f32.load offset=120
              local.set $l70
              local.get $l13
              i32.const 0
              i32.store offset=188
              local.get $l13
              local.get $l70
              local.get $l53
              f32.sub
              f32.store offset=184
              local.get $l13
              local.get $l65
              local.get $l48
              f32.sub
              f32.store offset=180
              local.get $l13
              local.get $l64
              local.get $l41
              f32.sub
              f32.store offset=176
              local.get $l13
              f32.load offset=128
              local.set $l41
              local.get $l13
              f32.load offset=132
              local.set $l48
              local.get $l13
              f32.load offset=136
              local.set $l53
              local.get $l13
              i32.const 0
              i32.store offset=204
              local.get $l13
              local.get $l53
              local.get $l58
              f32.sub
              f32.store offset=200
              local.get $l13
              local.get $l48
              local.get $l56
              f32.sub
              f32.store offset=196
              local.get $l13
              local.get $l41
              local.get $l57
              f32.sub
              f32.store offset=192
              local.get $l13
              f32.load offset=144
              local.set $l41
              local.get $l13
              f32.load offset=148
              local.set $l48
              local.get $l13
              f32.load offset=152
              local.set $l53
              local.get $l13
              i32.const 0
              i32.store offset=220
              local.get $l13
              local.get $l53
              local.get $l69
              f32.sub
              f32.store offset=216
              local.get $l13
              local.get $l48
              local.get $l68
              f32.sub
              f32.store offset=212
              local.get $l13
              local.get $l41
              local.get $l59
              f32.sub
              f32.store offset=208
              local.get $l52
              local.get $l82
              local.get $l42
              f32.add
              local.tee $l48
              f32.sub
              local.set $l41
              local.get $l67
              local.get $l80
              local.get $l35
              f32.add
              local.tee $l68
              f32.sub
              local.set $l53
              local.get $l74
              local.get $l81
              local.get $l38
              f32.add
              local.tee $l69
              f32.sub
              local.set $l59
              local.get $l39
              local.set $p11
              local.get $l40
              local.set $p6
              local.get $l37
              local.set $l46
              local.get $l38
              local.set $l58
              local.get $l35
              local.set $l64
              local.get $l42
              local.set $l65
              f32.const 0x1.fffffep+127 (;=3.40282e+38;)
            else
              local.get $l42
            end
            local.set $l57
            local.get $l36
            local.set $l56
          end
          local.get $l13
          i32.load offset=240
          local.tee $l17
          i32.const 4
          i32.shl
          local.tee $p1
          local.get $l13
          i32.const 112
          i32.add
          i32.add
          local.tee $l15
          i32.const 0
          i32.store offset=12
          local.get $l15
          local.get $l52
          f32.store offset=8
          local.get $l15
          local.get $l67
          f32.store offset=4
          local.get $l15
          local.get $l74
          f32.store
          local.get $l13
          i32.const 48
          i32.add
          local.get $p1
          i32.add
          local.tee $l15
          i32.const 0
          i32.store offset=12
          local.get $l15
          local.get $l48
          f32.store offset=8
          local.get $l15
          local.get $l68
          f32.store offset=4
          local.get $l15
          local.get $l69
          f32.store
          local.get $l13
          i32.const 176
          i32.add
          local.get $p1
          i32.add
          local.tee $l15
          i32.const 0
          i32.store offset=12
          local.get $l15
          local.get $l41
          f32.store offset=8
          local.get $l15
          local.get $l53
          f32.store offset=4
          local.get $l15
          local.get $l59
          f32.store
          local.get $l13
          local.get $l17
          i32.const 1
          i32.add
          i32.store offset=240
          block $B7
            block $B8
              block $B9
                block $B10
                  block $B11
                    local.get $l17
                    i32.const 1
                    i32.sub
                    br_table $B11 $B10 $B9 $B8
                  end
                  local.get $l13
                  f32.load offset=192
                  local.get $l13
                  f32.load offset=176
                  local.tee $l37
                  f32.sub
                  local.tee $l36
                  local.get $l36
                  f32.mul
                  local.get $l13
                  f32.load offset=196
                  local.get $l13
                  f32.load offset=180
                  local.tee $l40
                  f32.sub
                  local.tee $l35
                  local.get $l35
                  f32.mul
                  f32.add
                  local.get $l13
                  f32.load offset=200
                  local.get $l13
                  f32.load offset=184
                  local.tee $l39
                  f32.sub
                  local.tee $l38
                  local.get $l38
                  f32.mul
                  f32.add
                  local.tee $l41
                  f32.const 0x1p-23 (;=1.19209e-07;)
                  f32.le
                  if $I12
                    local.get $l13
                    i32.const 1
                    i32.store offset=240
                    local.get $l13
                    local.get $l13
                    i64.load offset=176
                    i64.store offset=32
                    local.get $l13
                    local.get $l13
                    i64.load offset=184
                    i64.store offset=40
                    br $B7
                  end
                  local.get $l13
                  local.get $l39
                  local.get $l38
                  local.get $l35
                  local.get $l40
                  f32.neg
                  f32.mul
                  local.get $l37
                  local.get $l36
                  f32.mul
                  f32.sub
                  local.get $l39
                  local.get $l38
                  f32.mul
                  f32.sub
                  local.get $l41
                  f32.div
                  f32.const 0x1p+0 (;=1;)
                  f32.min
                  local.tee $l41
                  f32.const 0x0p+0 (;=0;)
                  local.get $l41
                  f32.const 0x0p+0 (;=0;)
                  f32.gt
                  select
                  local.tee $l41
                  f32.mul
                  f32.add
                  f32.store offset=40
                  local.get $l13
                  local.get $l40
                  local.get $l35
                  local.get $l41
                  f32.mul
                  f32.add
                  f32.store offset=36
                  local.get $l13
                  local.get $l37
                  local.get $l36
                  local.get $l41
                  f32.mul
                  f32.add
                  f32.store offset=32
                  br $B7
                end
                local.get $l13
                i32.const 32
                i32.add
                local.get $l13
                i32.const 176
                i32.add
                local.get $l13
                i32.const 112
                i32.add
                local.get $l13
                i32.const 48
                i32.add
                local.get $l13
                i32.const 240
                i32.add
                call $f70516
                br $B7
              end
              local.get $l13
              i32.const 32
              i32.add
              local.get $l13
              i32.const 176
              i32.add
              local.get $l13
              i32.const 112
              i32.add
              local.get $l13
              i32.const 48
              i32.add
              local.get $l13
              i32.const 240
              i32.add
              call $f69903
              br $B7
            end
            local.get $l13
            local.get $l41
            f32.store offset=40
            local.get $l13
            local.get $l53
            f32.store offset=36
            local.get $l13
            local.get $l59
            f32.store offset=32
          end
          local.get $l13
          f32.load offset=40
          local.tee $l36
          f32.neg
          local.set $l37
          local.get $l13
          f32.load offset=36
          local.tee $l35
          f32.neg
          local.set $l40
          local.get $l13
          f32.load offset=32
          local.tee $l38
          f32.neg
          local.set $l39
          local.get $l83
          local.get $l38
          local.get $l38
          f32.mul
          local.get $l35
          local.get $l35
          f32.mul
          f32.add
          local.get $l36
          local.get $l36
          f32.mul
          f32.add
          local.tee $l42
          f32.lt
          local.get $l42
          local.get $l57
          f32.lt
          i32.and
          br_if $L3
        end
        i32.const -1
        i32.const 0
        local.get $l42
        local.get $l57
        f32.lt
        select
        local.set $l15
      end
      local.get $l19
      i32.load offset=4
      i32.load8_u offset=32
      local.set $p1
      f32.const 0x0p+0 (;=0;)
      local.set $l41
      f32.const 0x0p+0 (;=0;)
      local.set $l52
      local.get $l39
      local.get $p11
      local.get $l15
      i32.const 0
      i32.ne
      local.get $l42
      local.get $l85
      f32.gt
      i32.and
      local.tee $l17
      select
      local.tee $l39
      local.get $l39
      f32.mul
      local.get $l40
      local.get $p6
      local.get $l17
      select
      local.tee $l40
      local.get $l40
      f32.mul
      f32.add
      local.get $l37
      local.get $l46
      local.get $l17
      select
      local.tee $l37
      local.get $l37
      f32.mul
      f32.add
      f32.sqrt
      local.tee $l48
      f32.const 0x1p-23 (;=1.19209e-07;)
      f32.le
      i32.eqz
      if $I13
        local.get $l37
        f32.const 0x1p+0 (;=1;)
        local.get $l48
        f32.div
        local.tee $l52
        f32.mul
        local.set $l79
        local.get $l40
        local.get $l52
        f32.mul
        local.set $l41
        local.get $l39
        local.get $l52
        f32.mul
        local.set $l52
      end
      local.get $l25
      i32.const 0
      i32.store offset=12
      local.get $l25
      local.get $l79
      f32.neg
      f32.store offset=8
      local.get $l25
      local.get $l41
      f32.neg
      f32.store offset=4
      local.get $l25
      local.get $l52
      f32.neg
      f32.store
      local.get $p5
      local.get $l56
      f32.store
      local.get $p5
      local.get $l13
      i32.load offset=252
      i32.store offset=12
      local.get $p5
      local.get $l13
      i64.load offset=244 align=4
      i64.store offset=4 align=4
      local.get $l13
      i32.const 0
      i32.store offset=44
      local.get $l13
      local.get $l36
      local.get $l49
      local.get $l15
      select
      f32.store offset=40
      local.get $l13
      local.get $l35
      local.get $l44
      local.get $l15
      select
      f32.store offset=36
      local.get $l13
      local.get $l38
      local.get $l43
      local.get $l15
      select
      f32.store offset=32
      local.get $l13
      local.get $l13
      i64.load offset=264
      local.tee $l87
      i64.store offset=24
      local.get $l13
      local.get $l13
      i64.load offset=256
      local.tee $l88
      i64.store offset=16
      local.get $l13
      local.get $l87
      i64.store offset=8
      local.get $l13
      local.get $l88
      i64.store
      local.get $l13
      i32.const 176
      i32.add
      local.get $l13
      i32.const 112
      i32.add
      local.get $l13
      i32.const 48
      i32.add
      local.get $l13
      i32.const 32
      i32.add
      local.get $l13
      i32.const 16
      i32.add
      local.get $l13
      local.get $l13
      i32.load offset=240
      call $f70517
      local.get $l19
      i32.load offset=4
      f32.load offset=16
      local.set $l36
      local.get $l13
      f32.load offset=16
      local.set $l35
      local.get $l13
      f32.load offset=20
      local.set $l38
      local.get $l13
      f32.load offset=24
      local.set $l37
      local.get $l26
      i32.const 0
      i32.store offset=12
      local.get $l26
      local.get $l37
      local.get $l79
      local.get $l36
      f32.mul
      f32.add
      local.get $l37
      local.get $p1
      i32.const 255
      i32.and
      local.tee $l19
      select
      f32.store offset=8
      local.get $l26
      local.get $l38
      local.get $l41
      local.get $l36
      f32.mul
      f32.add
      local.get $l38
      local.get $l19
      select
      f32.store offset=4
      local.get $l26
      local.get $l35
      local.get $l52
      local.get $l36
      f32.mul
      f32.add
      local.get $l35
      local.get $l19
      select
      f32.store
      i32.const 1
      local.set $l15
    end
    local.get $l13
    i32.const 272
    i32.add
    global.set $g0
    local.get $l15
    local.tee $l27
    if $I14
      local.get $p3
      local.get $p0
      i64.load offset=240
      i64.store
      local.get $p3
      local.get $p0
      i64.load offset=248
      i64.store offset=8
      local.get $p0
      f32.load offset=240
      f32.const 0x0p+0 (;=0;)
      f32.eq
      if $I15
        local.get $p0
        local.get $l30
        i32.load offset=4
        local.tee $p2
        f32.load offset=16
        local.get $l33
        i32.load offset=4
        local.tee $l26
        f32.load offset=16
        f32.add
        f32.const 0x1.9p+6 (;=100;)
        f32.mul
        f32.store offset=224
        local.get $p0
        i32.const 0
        i32.store8 offset=215
        local.get $p0
        i32.const 168
        i32.add
        local.tee $p5
        i64.const 0
        i64.store
        local.get $p0
        i64.const 0
        i64.store offset=160
        local.get $p0
        i64.const 0
        i64.store offset=152
        local.get $p0
        i64.const 0
        i64.store offset=144
        local.get $p0
        i64.const 0
        i64.store offset=136
        local.get $p0
        i64.const 0
        i64.store offset=128
        local.get $p0
        i32.const 0
        i32.store offset=192
        local.get $p0
        local.get $l30
        i32.load offset=8
        local.tee $p1
        i32.store offset=56
        local.get $p0
        i32.const 3132452
        i32.store offset=48
        local.get $p0
        local.get $p2
        i32.store offset=52
        local.get $p0
        i32.const 72
        i32.add
        local.tee $p2
        local.get $p1
        i64.load offset=8
        i64.store
        local.get $p0
        i32.const 80
        i32.add
        local.tee $l17
        local.get $p1
        i64.load offset=16
        i64.store
        local.get $p0
        i32.const 88
        i32.add
        local.tee $l24
        local.get $p1
        i64.load offset=24
        i64.store
        local.get $p0
        i32.const 96
        i32.add
        local.tee $l25
        local.get $p1
        i64.load offset=32
        i64.store
        local.get $p0
        local.get $p1
        i64.load offset=40
        i64.store offset=104
        local.get $p0
        local.get $p1
        i64.load offset=48
        i64.store offset=112
        local.get $p0
        local.get $p1
        i64.load offset=56
        i64.store offset=120
        local.get $p0
        local.get $p1
        i64.load
        i64.store offset=64
        local.get $p0
        i32.const 68
        i32.add
        local.tee $p1
        f32.load
        local.set $p6
        local.get $p1
        local.get $l17
        f32.load
        f32.store
        local.get $l24
        f32.load
        local.set $p11
        local.get $p2
        f32.load
        local.set $l43
        local.get $p2
        local.get $l25
        f32.load
        f32.store
        local.get $l17
        local.get $p6
        f32.store
        local.get $l25
        local.get $l43
        f32.store
        local.get $l24
        local.get $p0
        i32.const 100
        i32.add
        local.tee $p1
        f32.load
        f32.store
        local.get $p1
        local.get $p11
        f32.store
        local.get $p0
        i32.const 3132536
        i32.store offset=40
        local.get $p0
        local.get $l26
        i32.store offset=44
        local.get $p3
        block $B16 (result f32)
          local.get $p0
          i32.const 220
          i32.add
          local.set $l21
          local.get $p0
          i32.const 216
          i32.add
          local.set $l23
          local.get $p0
          i32.const 128
          i32.add
          local.set $l18
          i32.const 0
          local.set $p2
          global.get $g0
          i32.const 320
          i32.sub
          local.tee $l12
          global.set $g0
          local.get $p0
          i32.const 40
          i32.add
          local.tee $l24
          i32.load offset=4
          local.tee $l22
          f32.load offset=20
          local.set $l35
          local.get $p0
          i32.const 48
          i32.add
          local.tee $l17
          i32.load offset=4
          local.tee $l14
          f32.load offset=20
          local.set $l37
          local.get $p0
          i32.const 224
          i32.add
          f32.load
          local.set $l36
          local.get $l14
          i32.load8_u offset=32
          local.set $l25
          local.get $l14
          f32.load offset=16
          local.set $l66
          local.get $l22
          i32.load8_u offset=32
          local.set $l26
          local.get $l22
          f32.load offset=16
          local.set $l56
          local.get $l12
          i32.const 0
          i32.store offset=44
          local.get $l35
          local.get $l37
          local.get $l35
          local.get $l37
          f32.lt
          select
          f32.const 0x1.99999ap-4 (;=0.1;)
          f32.mul
          local.set $l38
          block $B17 (result f32)
            local.get $p0
            i32.const 215
            i32.add
            local.tee $l28
            i32.load8_u
            local.tee $p3
            if $I18
              local.get $l14
              i32.const 48
              i32.add
              local.set $l34
              local.get $l17
              i32.load offset=8
              local.set $l14
              i32.const 0
              local.set $p4
              loop $L19
                local.get $p4
                i32.const 2
                i32.shl
                local.tee $l16
                local.get $l12
                i32.const -64
                i32.sub
                i32.add
                local.get $p4
                local.get $l21
                i32.add
                i32.load8_u
                local.tee $l20
                i32.store
                local.get $l12
                i32.const 48
                i32.add
                local.get $l16
                i32.add
                local.get $p4
                local.get $l23
                i32.add
                i32.load8_u
                local.tee $p1
                i32.store
                local.get $l34
                i32.const 1
                local.get $l20
                i32.sub
                i32.const 4
                i32.shl
                i32.add
                local.tee $l16
                f32.load offset=8
                local.set $l35
                local.get $l16
                f32.load
                local.set $l37
                local.get $l16
                f32.load offset=4
                local.set $l39
                local.get $p1
                i32.const 4
                i32.shl
                i32.const 3123152
                i32.add
                local.tee $l16
                i32.load
                local.set $l13
                local.get $l16
                i32.load offset=4
                local.set $l15
                local.get $l16
                i32.load offset=8
                local.set $l19
                local.get $l14
                f32.load offset=48
                local.set $l40
                local.get $l14
                f32.load offset=32
                local.set $p11
                local.get $l14
                f32.load
                local.set $p6
                local.get $l14
                f32.load offset=16
                local.set $l61
                local.get $l14
                f32.load offset=52
                local.set $l54
                local.get $l14
                f32.load offset=36
                local.set $l62
                local.get $l14
                f32.load offset=4
                local.set $l63
                local.get $l14
                f32.load offset=20
                local.set $l64
                local.get $l14
                f32.load offset=56
                local.set $l58
                local.get $l14
                f32.load offset=40
                local.set $l65
                local.get $l14
                f32.load offset=8
                local.set $l57
                local.get $l14
                f32.load offset=24
                local.set $l43
                local.get $l22
                f32.load offset=48
                local.set $l42
                local.get $l22
                f32.load offset=52
                local.set $l46
                local.get $l22
                f32.load offset=56
                local.set $l51
                local.get $p2
                local.tee $p1
                i32.const 4
                i32.shl
                local.tee $l20
                local.get $l12
                i32.const 144
                i32.add
                i32.add
                local.tee $l16
                i32.const 0
                i32.store offset=12
                local.get $l12
                i32.const 80
                i32.add
                local.get $l20
                i32.add
                local.tee $p2
                i32.const 0
                i32.store offset=12
                local.get $l12
                i32.const 208
                i32.add
                local.get $l20
                i32.add
                local.tee $l20
                i32.const 0
                i32.store offset=12
                local.get $p2
                local.get $l51
                local.get $l51
                f32.neg
                local.get $l19
                select
                local.tee $l51
                f32.store offset=8
                local.get $p2
                local.get $l46
                local.get $l46
                f32.neg
                local.get $l15
                select
                local.tee $l46
                f32.store offset=4
                local.get $p2
                local.get $l42
                local.get $l42
                f32.neg
                local.get $l13
                select
                local.tee $l42
                f32.store
                local.get $l16
                local.get $l58
                local.get $l37
                local.get $l57
                f32.mul
                local.get $l39
                local.get $l43
                f32.mul
                f32.add
                local.get $l35
                local.get $l65
                f32.mul
                f32.add
                f32.add
                local.tee $l58
                f32.store offset=8
                local.get $l16
                local.get $l54
                local.get $l37
                local.get $l63
                f32.mul
                local.get $l39
                local.get $l64
                f32.mul
                f32.add
                local.get $l35
                local.get $l62
                f32.mul
                f32.add
                f32.add
                local.tee $l54
                f32.store offset=4
                local.get $l16
                local.get $l40
                local.get $l37
                local.get $p6
                f32.mul
                local.get $l39
                local.get $l61
                f32.mul
                f32.add
                local.get $l35
                local.get $p11
                f32.mul
                f32.add
                f32.add
                local.tee $l35
                f32.store
                local.get $l20
                local.get $l58
                local.get $l51
                f32.sub
                local.tee $l37
                f32.store offset=8
                local.get $l20
                local.get $l54
                local.get $l46
                f32.sub
                local.tee $l39
                f32.store offset=4
                local.get $l20
                local.get $l35
                local.get $l42
                f32.sub
                local.tee $l35
                f32.store
                local.get $l12
                local.get $p1
                i32.const 1
                i32.add
                local.tee $p2
                i32.store offset=44
                local.get $p4
                i32.const 1
                i32.add
                local.tee $p4
                local.get $p3
                i32.ne
                br_if $L19
              end
              block $B20
                block $B21
                  block $B22
                    block $B23
                      block $B24
                        block $B25
                          block $B26
                            local.get $p1
                            br_table $B26 $B25 $B24 $B23 $B22
                          end
                          local.get $l12
                          i32.const 0
                          i32.store offset=28
                          br $B21
                        end
                        local.get $l12
                        f32.load offset=224
                        local.get $l12
                        f32.load offset=208
                        local.tee $l42
                        f32.sub
                        local.tee $l35
                        local.get $l35
                        f32.mul
                        local.get $l12
                        f32.load offset=228
                        local.get $l12
                        f32.load offset=212
                        local.tee $l46
                        f32.sub
                        local.tee $l37
                        local.get $l37
                        f32.mul
                        f32.add
                        local.get $l12
                        f32.load offset=232
                        local.get $l12
                        f32.load offset=216
                        local.tee $l51
                        f32.sub
                        local.tee $l39
                        local.get $l39
                        f32.mul
                        f32.add
                        local.tee $l40
                        f32.const 0x1p-23 (;=1.19209e-07;)
                        f32.le
                        if $I27
                          local.get $l12
                          i32.const 1
                          i32.store offset=44
                          local.get $l12
                          local.get $l12
                          i64.load offset=208
                          i64.store offset=16
                          local.get $l12
                          local.get $l12
                          i64.load offset=216
                          i64.store offset=24
                          br $B20
                        end
                        local.get $l12
                        i32.const 0
                        i32.store offset=28
                        local.get $l12
                        local.get $l51
                        local.get $l39
                        local.get $l37
                        local.get $l46
                        f32.neg
                        f32.mul
                        local.get $l42
                        local.get $l35
                        f32.mul
                        f32.sub
                        local.get $l51
                        local.get $l39
                        f32.mul
                        f32.sub
                        local.get $l40
                        f32.div
                        f32.const 0x1p+0 (;=1;)
                        f32.min
                        local.tee $l40
                        f32.const 0x0p+0 (;=0;)
                        local.get $l40
                        f32.const 0x0p+0 (;=0;)
                        f32.gt
                        select
                        local.tee $l40
                        f32.mul
                        f32.add
                        f32.store offset=24
                        local.get $l12
                        local.get $l46
                        local.get $l37
                        local.get $l40
                        f32.mul
                        f32.add
                        f32.store offset=20
                        local.get $l12
                        local.get $l42
                        local.get $l35
                        local.get $l40
                        f32.mul
                        f32.add
                        f32.store offset=16
                        br $B20
                      end
                      local.get $l12
                      i32.const 16
                      i32.add
                      local.get $l12
                      i32.const 208
                      i32.add
                      local.get $l12
                      i32.const 144
                      i32.add
                      local.get $l12
                      i32.const 80
                      i32.add
                      local.get $l12
                      i32.const -64
                      i32.sub
                      local.get $l12
                      i32.const 48
                      i32.add
                      local.get $l12
                      i32.const 44
                      i32.add
                      call $f70518
                      br $B20
                    end
                    local.get $l12
                    i32.const 16
                    i32.add
                    local.get $l12
                    i32.const 208
                    i32.add
                    local.get $l12
                    i32.const 144
                    i32.add
                    local.get $l12
                    i32.const 80
                    i32.add
                    local.get $l12
                    i32.const -64
                    i32.sub
                    local.get $l12
                    i32.const 48
                    i32.add
                    local.get $l12
                    i32.const 44
                    i32.add
                    call $f69905
                    br $B20
                  end
                  local.get $l12
                  i32.const 0
                  i32.store offset=28
                end
                local.get $l12
                local.get $l37
                f32.store offset=24
                local.get $l12
                local.get $l39
                f32.store offset=20
                local.get $l12
                local.get $l35
                f32.store offset=16
              end
              local.get $l12
              local.get $l12
              i64.load offset=16
              i64.store offset=272
              local.get $l12
              local.get $l12
              i64.load offset=24
              i64.store offset=280
              local.get $l12
              f32.load offset=272
              local.tee $l40
              local.get $l40
              f32.mul
              local.get $l12
              f32.load offset=276
              local.tee $p11
              local.get $p11
              f32.mul
              f32.add
              local.get $l12
              f32.load offset=280
              local.tee $p6
              local.get $p6
              f32.mul
              f32.add
              f32.sqrt
              local.tee $l46
              local.get $l38
              f32.gt
              local.set $l14
              local.get $p6
              f32.const 0x1p+0 (;=1;)
              local.get $l46
              f32.div
              local.tee $l35
              f32.mul
              local.set $l54
              local.get $p11
              local.get $l35
              f32.mul
              local.set $l62
              local.get $l40
              local.get $l35
              f32.mul
              local.set $l63
              local.get $l12
              f32.load offset=284
              br $B17
            end
            local.get $p4
            f32.load offset=8
            local.set $l35
            local.get $p4
            f32.load
            local.set $l37
            local.get $p4
            f32.load offset=4
            local.set $l39
            local.get $l12
            i32.const 0
            i32.store offset=284
            local.get $l12
            local.get $l35
            f32.const 0x0p+0 (;=0;)
            local.get $l37
            local.get $l37
            f32.mul
            local.get $l39
            local.get $l39
            f32.mul
            f32.add
            local.get $l35
            local.get $l35
            f32.mul
            f32.add
            f32.const 0x0p+0 (;=0;)
            f32.gt
            local.tee $l14
            select
            local.tee $p6
            f32.store offset=280
            local.get $l12
            local.get $l39
            f32.const 0x0p+0 (;=0;)
            local.get $l14
            select
            local.tee $p11
            f32.store offset=276
            local.get $l12
            local.get $l37
            f32.const 0x1p+0 (;=1;)
            local.get $l14
            select
            local.tee $l40
            f32.store offset=272
            local.get $p6
            f32.const 0x1p+0 (;=1;)
            local.get $p6
            local.get $p6
            f32.mul
            local.get $l40
            local.get $l40
            f32.mul
            local.get $p11
            local.get $p11
            f32.mul
            f32.add
            f32.add
            f32.sqrt
            f32.div
            local.tee $l35
            f32.mul
            local.set $l54
            local.get $p11
            local.get $l35
            f32.mul
            local.set $l62
            local.get $l40
            local.get $l35
            f32.mul
            local.set $l63
            f32.const 0x1.fffffep+127 (;=3.40282e+38;)
            local.set $l46
            i32.const 1
            local.set $l14
            f32.const 0x0p+0 (;=0;)
          end
          local.set $l49
          block $B28
            block $B29
              local.get $l14
              i32.eqz
              br_if $B29
              local.get $l36
              local.get $l66
              f32.const 0x0p+0 (;=0;)
              local.get $l25
              select
              local.tee $l66
              local.get $l56
              f32.const 0x0p+0 (;=0;)
              local.get $l26
              select
              local.tee $l56
              f32.add
              local.tee $l44
              f32.add
              local.set $l36
              local.get $l12
              i32.const 296
              i32.add
              local.set $l22
              loop $L30
                local.get $l22
                local.get $l12
                i32.load offset=312
                i32.store
                local.get $l12
                local.get $l12
                i64.load offset=304 align=4
                i64.store offset=288
                local.get $l12
                i32.const 0
                i32.store offset=12
                local.get $l12
                local.get $p6
                f32.neg
                f32.store offset=8
                local.get $l12
                local.get $p11
                f32.neg
                f32.store offset=4
                local.get $l12
                local.get $l40
                f32.neg
                f32.store
                local.get $l12
                i32.const 16
                i32.add
                local.get $l17
                local.get $l12
                local.get $l12
                i32.const -64
                i32.sub
                local.get $l12
                i32.load offset=44
                i32.const 2
                i32.shl
                i32.add
                call $f70511
                local.get $l12
                f32.load offset=28
                local.set $l58
                local.get $l12
                f32.load offset=16
                local.set $l35
                local.get $l12
                f32.load offset=20
                local.set $l37
                local.get $l12
                f32.load offset=24
                local.set $l39
                local.get $l24
                i32.load offset=4
                local.set $l14
                local.get $l12
                i32.const 48
                i32.add
                local.get $l12
                i32.load offset=44
                local.tee $p4
                i32.const 2
                i32.shl
                i32.add
                local.get $l12
                f32.load offset=272
                f32.const 0x0p+0 (;=0;)
                f32.gt
                local.tee $p2
                local.get $l12
                f32.load offset=276
                f32.const 0x0p+0 (;=0;)
                f32.gt
                local.tee $l16
                i32.const 1
                i32.shl
                i32.or
                local.get $l12
                f32.load offset=280
                f32.const 0x0p+0 (;=0;)
                f32.gt
                local.tee $l20
                i32.const 2
                i32.shl
                i32.or
                i32.store
                local.get $l36
                local.get $l63
                local.get $l35
                local.get $l14
                f32.load offset=48
                local.tee $l42
                local.get $l42
                f32.neg
                local.get $p2
                select
                local.tee $l65
                f32.sub
                local.tee $l42
                f32.mul
                local.get $l62
                local.get $l37
                local.get $l14
                f32.load offset=52
                local.tee $l51
                local.get $l51
                f32.neg
                local.get $l16
                select
                local.tee $l57
                f32.sub
                local.tee $l51
                f32.mul
                f32.add
                local.get $l54
                local.get $l39
                local.get $l14
                f32.load offset=56
                local.tee $l61
                local.get $l61
                f32.neg
                local.get $l20
                select
                local.tee $l43
                f32.sub
                local.tee $l61
                f32.mul
                f32.add
                local.tee $l64
                f32.lt
                if $I31
                  i32.const 0
                  local.set $l20
                  local.get $l21
                  i32.eqz
                  br_if $B28
                  local.get $l28
                  local.get $p4
                  i32.store8
                  local.get $p4
                  i32.eqz
                  br_if $B28
                  local.get $p4
                  i32.const 1
                  i32.and
                  local.set $l22
                  i32.const 0
                  local.set $l14
                  local.get $p4
                  i32.const 1
                  i32.ne
                  if $I32
                    local.get $p4
                    i32.const -2
                    i32.and
                    local.set $l16
                    loop $L33
                      local.get $l14
                      local.get $l21
                      i32.add
                      local.get $l14
                      i32.const 2
                      i32.shl
                      local.tee $p4
                      local.get $l12
                      i32.const -64
                      i32.sub
                      i32.add
                      i32.load
                      i32.store8
                      local.get $l14
                      local.get $l23
                      i32.add
                      local.get $l12
                      i32.const 48
                      i32.add
                      local.get $p4
                      i32.add
                      i32.load
                      i32.store8
                      local.get $l21
                      local.get $l14
                      i32.const 1
                      i32.or
                      local.tee $p4
                      i32.add
                      local.get $p4
                      i32.const 2
                      i32.shl
                      local.tee $p2
                      local.get $l12
                      i32.const -64
                      i32.sub
                      i32.add
                      i32.load
                      i32.store8
                      local.get $p4
                      local.get $l23
                      i32.add
                      local.get $l12
                      i32.const 48
                      i32.add
                      local.get $p2
                      i32.add
                      i32.load
                      i32.store8
                      local.get $l14
                      i32.const 2
                      i32.add
                      local.set $l14
                      local.get $l16
                      i32.const 2
                      i32.sub
                      local.tee $l16
                      br_if $L33
                    end
                  end
                  local.get $l22
                  i32.eqz
                  br_if $B28
                  local.get $l14
                  local.get $l21
                  i32.add
                  local.get $l14
                  i32.const 2
                  i32.shl
                  local.tee $p4
                  local.get $l12
                  i32.const -64
                  i32.sub
                  i32.add
                  i32.load
                  i32.store8
                  local.get $l14
                  local.get $l23
                  i32.add
                  local.get $l12
                  i32.const 48
                  i32.add
                  local.get $p4
                  i32.add
                  i32.load
                  i32.store8
                  br $B28
                end
                local.get $l46
                f32.const 0x1.ffe282p-1 (;=0.999775;)
                f32.mul
                local.get $l64
                f32.lt
                if $I34
                  block $B35
                    local.get $l21
                    i32.eqz
                    br_if $B35
                    local.get $l28
                    local.get $p4
                    i32.store8
                    local.get $p4
                    i32.eqz
                    br_if $B35
                    local.get $p4
                    i32.const 1
                    i32.and
                    local.set $l22
                    i32.const 0
                    local.set $l14
                    local.get $p4
                    i32.const 1
                    i32.ne
                    if $I36
                      local.get $p4
                      i32.const -2
                      i32.and
                      local.set $p2
                      loop $L37
                        local.get $l14
                        local.get $l21
                        i32.add
                        local.get $l14
                        i32.const 2
                        i32.shl
                        local.tee $l16
                        local.get $l12
                        i32.const -64
                        i32.sub
                        i32.add
                        i32.load
                        i32.store8
                        local.get $l14
                        local.get $l23
                        i32.add
                        local.get $l12
                        i32.const 48
                        i32.add
                        local.get $l16
                        i32.add
                        i32.load
                        i32.store8
                        local.get $l21
                        local.get $l14
                        i32.const 1
                        i32.or
                        local.tee $l16
                        i32.add
                        local.get $l16
                        i32.const 2
                        i32.shl
                        local.tee $l20
                        local.get $l12
                        i32.const -64
                        i32.sub
                        i32.add
                        i32.load
                        i32.store8
                        local.get $l16
                        local.get $l23
                        i32.add
                        local.get $l12
                        i32.const 48
                        i32.add
                        local.get $l20
                        i32.add
                        i32.load
                        i32.store8
                        local.get $l14
                        i32.const 2
                        i32.add
                        local.set $l14
                        local.get $p2
                        i32.const 2
                        i32.sub
                        local.tee $p2
                        br_if $L37
                      end
                    end
                    local.get $l22
                    i32.eqz
                    br_if $B35
                    local.get $l14
                    local.get $l21
                    i32.add
                    local.get $l14
                    i32.const 2
                    i32.shl
                    local.tee $l16
                    local.get $l12
                    i32.const -64
                    i32.sub
                    i32.add
                    i32.load
                    i32.store8
                    local.get $l14
                    local.get $l23
                    i32.add
                    local.get $l12
                    i32.const 48
                    i32.add
                    local.get $l16
                    i32.add
                    i32.load
                    i32.store8
                  end
                  local.get $l18
                  local.get $l63
                  f32.store offset=32
                  local.get $l18
                  i32.const 0
                  i32.store offset=44
                  local.get $l18
                  local.get $l54
                  f32.store offset=40
                  local.get $l18
                  local.get $l62
                  f32.store offset=36
                  local.get $l12
                  i32.const 208
                  i32.add
                  local.get $l12
                  i32.const 144
                  i32.add
                  local.get $l12
                  i32.const 80
                  i32.add
                  local.get $l12
                  i32.const 272
                  i32.add
                  local.get $l12
                  i32.const 16
                  i32.add
                  local.get $l12
                  local.get $p4
                  call $f70517
                  local.get $l12
                  f32.load offset=16
                  local.set $l35
                  local.get $l12
                  f32.load offset=20
                  local.set $l37
                  local.get $l12
                  f32.load offset=24
                  local.set $l39
                  local.get $l18
                  i32.const 0
                  i32.store offset=12
                  local.get $l18
                  local.get $l39
                  local.get $l66
                  local.get $l54
                  f32.mul
                  f32.sub
                  f32.store offset=8
                  local.get $l18
                  local.get $l37
                  local.get $l66
                  local.get $l62
                  f32.mul
                  f32.sub
                  f32.store offset=4
                  local.get $l18
                  local.get $l35
                  local.get $l66
                  local.get $l63
                  f32.mul
                  f32.sub
                  f32.store
                  local.get $l12
                  f32.load
                  local.set $l35
                  local.get $l12
                  f32.load offset=4
                  local.set $l37
                  local.get $l12
                  f32.load offset=8
                  local.set $l39
                  local.get $l18
                  i32.const 0
                  i32.store offset=28
                  local.get $l18
                  local.get $l39
                  local.get $l56
                  local.get $l54
                  f32.mul
                  f32.add
                  f32.store offset=24
                  local.get $l18
                  local.get $l37
                  local.get $l56
                  local.get $l62
                  f32.mul
                  f32.add
                  f32.store offset=20
                  local.get $l18
                  local.get $l35
                  local.get $l56
                  local.get $l63
                  f32.mul
                  f32.add
                  f32.store offset=16
                  local.get $l18
                  local.get $l46
                  local.get $l44
                  f32.sub
                  f32.store offset=64
                  i32.const 2
                  local.set $l20
                  br $B28
                end
                local.get $p4
                i32.const 4
                i32.shl
                local.tee $l16
                local.get $l12
                i32.const 144
                i32.add
                i32.add
                local.tee $l14
                local.get $l58
                f32.store offset=12
                local.get $l14
                local.get $l39
                f32.store offset=8
                local.get $l14
                local.get $l37
                f32.store offset=4
                local.get $l14
                local.get $l35
                f32.store
                local.get $l12
                i32.const 80
                i32.add
                local.get $l16
                i32.add
                local.tee $l14
                i32.const 0
                i32.store offset=12
                local.get $l14
                local.get $l43
                f32.store offset=8
                local.get $l14
                local.get $l57
                f32.store offset=4
                local.get $l14
                local.get $l65
                f32.store
                local.get $l12
                i32.const 208
                i32.add
                local.get $l16
                i32.add
                local.tee $l14
                i32.const 0
                i32.store offset=12
                local.get $l14
                local.get $l61
                f32.store offset=8
                local.get $l14
                local.get $l51
                f32.store offset=4
                local.get $l14
                local.get $l42
                f32.store
                local.get $l12
                local.get $p4
                i32.const 1
                i32.add
                i32.store offset=44
                block $B38
                  block $B39
                    block $B40
                      block $B41
                        block $B42
                          local.get $p4
                          i32.const 1
                          i32.sub
                          br_table $B42 $B41 $B40 $B39
                        end
                        local.get $l12
                        f32.load offset=224
                        local.get $l12
                        f32.load offset=208
                        local.tee $l42
                        f32.sub
                        local.tee $l35
                        local.get $l35
                        f32.mul
                        local.get $l12
                        f32.load offset=228
                        local.get $l12
                        f32.load offset=212
                        local.tee $l51
                        f32.sub
                        local.tee $l37
                        local.get $l37
                        f32.mul
                        f32.add
                        local.get $l12
                        f32.load offset=232
                        local.get $l12
                        f32.load offset=216
                        local.tee $l61
                        f32.sub
                        local.tee $l39
                        local.get $l39
                        f32.mul
                        f32.add
                        local.tee $l54
                        f32.const 0x1p-23 (;=1.19209e-07;)
                        f32.le
                        if $I43
                          local.get $l12
                          i32.const 1
                          i32.store offset=44
                          local.get $l12
                          local.get $l12
                          i64.load offset=208
                          i64.store offset=16
                          local.get $l12
                          local.get $l12
                          i64.load offset=216
                          i64.store offset=24
                          br $B38
                        end
                        local.get $l12
                        i32.const 0
                        i32.store offset=28
                        local.get $l12
                        local.get $l61
                        local.get $l39
                        local.get $l37
                        local.get $l51
                        f32.neg
                        f32.mul
                        local.get $l42
                        local.get $l35
                        f32.mul
                        f32.sub
                        local.get $l61
                        local.get $l39
                        f32.mul
                        f32.sub
                        local.get $l54
                        f32.div
                        f32.const 0x1p+0 (;=1;)
                        f32.min
                        local.tee $l54
                        f32.const 0x0p+0 (;=0;)
                        local.get $l54
                        f32.const 0x0p+0 (;=0;)
                        f32.gt
                        select
                        local.tee $l54
                        f32.mul
                        f32.add
                        f32.store offset=24
                        local.get $l12
                        local.get $l51
                        local.get $l37
                        local.get $l54
                        f32.mul
                        f32.add
                        f32.store offset=20
                        local.get $l12
                        local.get $l42
                        local.get $l35
                        local.get $l54
                        f32.mul
                        f32.add
                        f32.store offset=16
                        br $B38
                      end
                      local.get $l12
                      i32.const 16
                      i32.add
                      local.get $l12
                      i32.const 208
                      i32.add
                      local.get $l12
                      i32.const 144
                      i32.add
                      local.get $l12
                      i32.const 80
                      i32.add
                      local.get $l12
                      i32.const -64
                      i32.sub
                      local.get $l12
                      i32.const 48
                      i32.add
                      local.get $l12
                      i32.const 44
                      i32.add
                      call $f70518
                      br $B38
                    end
                    local.get $l12
                    i32.const 16
                    i32.add
                    local.get $l12
                    i32.const 208
                    i32.add
                    local.get $l12
                    i32.const 144
                    i32.add
                    local.get $l12
                    i32.const 80
                    i32.add
                    local.get $l12
                    i32.const -64
                    i32.sub
                    local.get $l12
                    i32.const 48
                    i32.add
                    local.get $l12
                    i32.const 44
                    i32.add
                    call $f69905
                    br $B38
                  end
                  local.get $l12
                  i32.const 0
                  i32.store offset=28
                  local.get $l12
                  local.get $l61
                  f32.store offset=24
                  local.get $l12
                  local.get $l51
                  f32.store offset=20
                  local.get $l12
                  local.get $l42
                  f32.store offset=16
                end
                local.get $l12
                local.get $l12
                i64.load offset=16
                i64.store offset=272
                local.get $l12
                local.get $l12
                i64.load offset=24
                i64.store offset=280
                local.get $l12
                f32.load offset=280
                local.tee $l37
                f32.const 0x1p+0 (;=1;)
                local.get $l12
                f32.load offset=272
                local.tee $l39
                local.get $l39
                f32.mul
                local.get $l12
                f32.load offset=276
                local.tee $l42
                local.get $l42
                f32.mul
                f32.add
                local.get $l37
                local.get $l37
                f32.mul
                f32.add
                f32.sqrt
                local.tee $l35
                f32.div
                local.tee $l51
                f32.mul
                local.set $l54
                local.get $l42
                local.get $l51
                f32.mul
                local.set $l62
                local.get $l39
                local.get $l51
                f32.mul
                local.set $l63
                block $B44
                  local.get $l35
                  local.get $l38
                  f32.gt
                  i32.eqz
                  br_if $B44
                  local.get $l35
                  local.get $l46
                  f32.lt
                  i32.eqz
                  br_if $B44
                  local.get $l12
                  f32.load offset=284
                  local.set $l49
                  local.get $l37
                  local.set $p6
                  local.get $l42
                  local.set $p11
                  local.get $l39
                  local.set $l40
                  local.get $l35
                  local.set $l46
                  br $L30
                end
              end
              local.get $l35
              local.get $l46
              f32.lt
              br_if $B29
              local.get $l12
              i32.load offset=44
              local.set $l20
              block $B45
                local.get $l21
                i32.eqz
                br_if $B45
                local.get $l28
                local.get $l20
                i32.const 1
                i32.sub
                local.tee $p4
                i32.store8
                local.get $p4
                i32.eqz
                br_if $B45
                local.get $p4
                i32.const 1
                i32.and
                local.set $l22
                i32.const 0
                local.set $l14
                local.get $l20
                i32.const 2
                i32.ne
                if $I46
                  local.get $p4
                  i32.const -2
                  i32.and
                  local.set $l16
                  loop $L47
                    local.get $l14
                    local.get $l21
                    i32.add
                    local.get $l14
                    i32.const 2
                    i32.shl
                    local.tee $p4
                    local.get $l12
                    i32.const -64
                    i32.sub
                    i32.add
                    i32.load
                    i32.store8
                    local.get $l14
                    local.get $l23
                    i32.add
                    local.get $l12
                    i32.const 48
                    i32.add
                    local.get $p4
                    i32.add
                    i32.load
                    i32.store8
                    local.get $l21
                    local.get $l14
                    i32.const 1
                    i32.or
                    local.tee $p4
                    i32.add
                    local.get $p4
                    i32.const 2
                    i32.shl
                    local.tee $p2
                    local.get $l12
                    i32.const -64
                    i32.sub
                    i32.add
                    i32.load
                    i32.store8
                    local.get $p4
                    local.get $l23
                    i32.add
                    local.get $l12
                    i32.const 48
                    i32.add
                    local.get $p2
                    i32.add
                    i32.load
                    i32.store8
                    local.get $l14
                    i32.const 2
                    i32.add
                    local.set $l14
                    local.get $l16
                    i32.const 2
                    i32.sub
                    local.tee $l16
                    br_if $L47
                  end
                end
                local.get $l22
                i32.eqz
                br_if $B45
                local.get $l14
                local.get $l21
                i32.add
                local.get $l14
                i32.const 2
                i32.shl
                local.tee $p4
                local.get $l12
                i32.const -64
                i32.sub
                i32.add
                i32.load
                i32.store8
                local.get $l14
                local.get $l23
                i32.add
                local.get $l12
                i32.const 48
                i32.add
                local.get $p4
                i32.add
                i32.load
                i32.store8
              end
              local.get $l12
              local.get $l12
              i32.load offset=296
              i32.store offset=312
              local.get $l12
              local.get $l12
              i64.load offset=288
              i64.store offset=304
              local.get $l12
              local.get $l49
              f32.store offset=284
              local.get $l12
              local.get $l40
              f32.store offset=272
              local.get $l12
              local.get $p11
              f32.store offset=276
              local.get $l12
              local.get $p6
              f32.store offset=280
              local.get $l12
              i32.const 208
              i32.add
              local.get $l12
              i32.const 144
              i32.add
              local.get $l12
              i32.const 80
              i32.add
              local.get $l12
              i32.const 272
              i32.add
              local.get $l12
              i32.const 16
              i32.add
              local.get $l12
              local.get $l20
              call $f70517
              local.get $l18
              i32.const 0
              i32.store offset=60
              local.get $l18
              local.get $l54
              f32.store offset=56
              local.get $l18
              local.get $l62
              f32.store offset=52
              local.get $l18
              local.get $l63
              f32.store offset=48
              local.get $l18
              i32.const 0
              i32.store offset=44
              local.get $l18
              local.get $p6
              f32.const 0x1p+0 (;=1;)
              local.get $l46
              f32.div
              local.tee $l35
              f32.mul
              local.tee $l37
              f32.store offset=40
              local.get $l18
              local.get $p11
              local.get $l35
              f32.mul
              local.tee $l39
              f32.store offset=36
              local.get $l18
              local.get $l40
              local.get $l35
              f32.mul
              local.tee $l35
              f32.store offset=32
              local.get $l12
              f32.load offset=16
              local.set $l42
              local.get $l12
              f32.load offset=20
              local.set $l51
              local.get $l12
              f32.load offset=24
              local.set $l40
              local.get $l18
              i32.const 0
              i32.store offset=12
              local.get $l18
              local.get $l40
              local.get $l66
              local.get $l37
              f32.mul
              f32.sub
              f32.store offset=8
              local.get $l18
              local.get $l51
              local.get $l66
              local.get $l39
              f32.mul
              f32.sub
              f32.store offset=4
              local.get $l18
              local.get $l42
              local.get $l66
              local.get $l35
              f32.mul
              f32.sub
              f32.store
              local.get $l12
              f32.load
              local.set $l42
              local.get $l12
              f32.load offset=4
              local.set $l51
              local.get $l12
              f32.load offset=8
              local.set $l40
              local.get $l18
              local.get $l46
              local.get $l44
              f32.sub
              f32.store offset=64
              local.get $l18
              i32.const 0
              i32.store offset=28
              local.get $l18
              local.get $l40
              local.get $l56
              local.get $l37
              f32.mul
              f32.add
              f32.store offset=24
              local.get $l18
              local.get $l51
              local.get $l56
              local.get $l39
              f32.mul
              f32.add
              f32.store offset=20
              local.get $l18
              local.get $l42
              local.get $l56
              local.get $l35
              f32.mul
              f32.add
              f32.store offset=16
              i32.const 2
              local.set $l20
              local.get $l44
              local.get $l46
              f32.ge
              br_if $B28
              i32.const 4
              local.set $l20
              br $B28
            end
            i32.const 5
            local.set $l20
            local.get $l21
            i32.eqz
            br_if $B28
            local.get $l28
            local.get $l12
            i32.load offset=44
            local.tee $p4
            i32.store8
            local.get $p4
            i32.eqz
            br_if $B28
            local.get $p4
            i32.const 1
            i32.and
            local.set $l22
            i32.const 0
            local.set $l14
            local.get $p4
            i32.const 1
            i32.ne
            if $I48
              local.get $p4
              i32.const -2
              i32.and
              local.set $l16
              loop $L49
                local.get $l14
                local.get $l21
                i32.add
                local.get $l14
                i32.const 2
                i32.shl
                local.tee $p4
                local.get $l12
                i32.const -64
                i32.sub
                i32.add
                i32.load
                i32.store8
                local.get $l14
                local.get $l23
                i32.add
                local.get $l12
                i32.const 48
                i32.add
                local.get $p4
                i32.add
                i32.load
                i32.store8
                local.get $l21
                local.get $l14
                i32.const 1
                i32.or
                local.tee $p4
                i32.add
                local.get $p4
                i32.const 2
                i32.shl
                local.tee $p2
                local.get $l12
                i32.const -64
                i32.sub
                i32.add
                i32.load
                i32.store8
                local.get $p4
                local.get $l23
                i32.add
                local.get $l12
                i32.const 48
                i32.add
                local.get $p2
                i32.add
                i32.load
                i32.store8
                local.get $l14
                i32.const 2
                i32.add
                local.set $l14
                local.get $l16
                i32.const 2
                i32.sub
                local.tee $l16
                br_if $L49
              end
            end
            local.get $l22
            i32.eqz
            br_if $B28
            local.get $l14
            local.get $l21
            i32.add
            local.get $l14
            i32.const 2
            i32.shl
            local.tee $p4
            local.get $l12
            i32.const -64
            i32.sub
            i32.add
            i32.load
            i32.store8
            local.get $l14
            local.get $l23
            i32.add
            local.get $l12
            i32.const 48
            i32.add
            local.get $p4
            i32.add
            i32.load
            i32.store8
          end
          local.get $l12
          i32.const 320
          i32.add
          global.set $g0
          block $B50
            block $B51
              block $B52
                block $B53
                  local.get $l20
                  i32.const 2
                  i32.sub
                  br_table $B53 $B51 $B51 $B52 $B51
                end
                local.get $p0
                local.get $p0
                i64.load offset=136
                i64.store offset=280
                local.get $p0
                local.get $p0
                i64.load offset=128
                i64.store offset=272
                local.get $p0
                local.get $p0
                i64.load offset=160
                i64.store offset=256
                local.get $p0
                local.get $p5
                i64.load
                i64.store offset=264
                br $B50
              end
              local.get $p0
              i32.const 1065353216
              i32.store offset=16
              local.get $p0
              local.get $p0
              i64.load offset=24
              i64.store offset=8
              local.get $p0
              local.get $p0
              i64.load offset=16
              i64.store
              local.get $l30
              local.get $l33
              local.get $p0
              i32.const 220
              i32.add
              local.get $p0
              i32.const 216
              i32.add
              local.get $p0
              i32.load8_u offset=215
              i32.const 0
              local.get $p0
              local.get $p0
              i32.const 128
              i32.add
              call $f69898
              i32.const 5
              i32.sub
              i32.const 1
              i32.le_u
              if $I54
                local.get $p0
                local.get $p0
                i64.load offset=136
                i64.store offset=280
                local.get $p0
                local.get $p0
                i64.load offset=128
                i64.store offset=272
                local.get $p0
                local.get $p0
                i64.load offset=160
                i64.store offset=256
                local.get $p0
                local.get $p0
                i64.load offset=168
                i64.store offset=264
                br $B50
              end
              local.get $p0
              i64.const 0
              i64.store offset=280
              local.get $p0
              i64.const 0
              i64.store offset=272
              local.get $l29
              f32.load offset=8
              local.set $p6
              local.get $l29
              f32.load
              local.set $p11
              local.get $l29
              f32.load offset=4
              local.set $l43
              local.get $p0
              i32.const 0
              i32.store offset=268
              local.get $p0
              f32.const 0x1p+0 (;=1;)
              local.get $p11
              local.get $p11
              f32.mul
              local.get $l43
              local.get $l43
              f32.mul
              f32.add
              local.get $p6
              local.get $p6
              f32.mul
              f32.add
              f32.sqrt
              f32.div
              local.tee $l44
              local.get $p6
              f32.neg
              f32.mul
              f32.store offset=264
              local.get $p0
              local.get $l44
              local.get $l43
              f32.neg
              f32.mul
              f32.store offset=260
              local.get $p0
              local.get $l44
              local.get $p11
              f32.neg
              f32.mul
              f32.store offset=256
              f32.const 0x0p+0 (;=0;)
              br $B16
            end
            local.get $p0
            local.get $p0
            i64.load offset=136
            i64.store offset=280
            local.get $p0
            local.get $p0
            i64.load offset=128
            i64.store offset=272
            local.get $p0
            local.get $p0
            i64.load offset=160
            i64.store offset=256
            local.get $p0
            local.get $p5
            i64.load
            i64.store offset=264
          end
          local.get $p0
          f32.load offset=192
        end
        local.tee $p6
        f32.const 0x0p+0 (;=0;)
        local.get $p6
        f32.const 0x0p+0 (;=0;)
        f32.lt
        select
        f32.store
      end
      local.get $l32
      local.get $p0
      i64.load offset=272
      i64.store
      local.get $l32
      local.get $p0
      i64.load offset=280
      i64.store offset=8
      local.get $l31
      local.get $p0
      i64.load offset=256
      i64.store
      local.get $l31
      local.get $p0
      i64.load offset=264
      i64.store offset=8
    end
    local.get $p0
    i32.const 288
    i32.add
    global.set $g0
    local.get $l27
    if $I55
      local.get $p10
      f32.load offset=304
      local.set $l50
      local.get $p10
      f32.load offset=296
      local.set $l43
      local.get $p10
      f32.load offset=292
      local.set $l44
      local.get $p10
      f32.load offset=288
      local.set $l36
      local.get $p7
      local.get $l45
      local.get $p9
      local.get $p10
      f32.load offset=272
      local.tee $p11
      f32.mul
      local.get $l55
      local.get $p10
      f32.load offset=276
      local.tee $l49
      f32.mul
      f32.add
      local.get $l45
      local.get $p10
      f32.load offset=280
      local.tee $l38
      f32.mul
      f32.add
      local.tee $l35
      f32.mul
      local.get $l60
      local.get $l38
      f32.mul
      local.get $l47
      local.get $p9
      local.get $l49
      f32.mul
      local.get $l55
      local.get $p11
      f32.mul
      f32.sub
      f32.mul
      f32.add
      f32.add
      local.tee $p6
      local.get $p6
      f32.add
      f32.store offset=8
      local.get $p7
      local.get $l55
      local.get $l35
      f32.mul
      local.get $l60
      local.get $l49
      f32.mul
      local.get $l47
      local.get $l45
      local.get $p11
      f32.mul
      local.get $p9
      local.get $l38
      f32.mul
      f32.sub
      f32.mul
      f32.add
      f32.add
      local.tee $p6
      local.get $p6
      f32.add
      f32.store offset=4
      local.get $p7
      local.get $p9
      local.get $l35
      f32.mul
      local.get $l60
      local.get $p11
      f32.mul
      local.get $l47
      local.get $l55
      local.get $l38
      f32.mul
      local.get $l45
      local.get $l49
      f32.mul
      f32.sub
      f32.mul
      f32.add
      f32.add
      local.tee $p11
      local.get $p11
      f32.add
      f32.store
      local.get $p8
      local.get $l72
      local.get $l50
      f32.const 0x0p+0 (;=0;)
      local.get $l50
      f32.const 0x0p+0 (;=0;)
      f32.gt
      select
      local.tee $p11
      f32.mul
      local.get $l77
      local.get $l45
      local.get $p9
      local.get $l36
      f32.mul
      local.get $l55
      local.get $l44
      f32.mul
      f32.add
      local.get $l45
      local.get $l43
      f32.mul
      f32.add
      local.tee $l49
      f32.mul
      local.get $l60
      local.get $l43
      f32.mul
      local.get $l47
      local.get $p9
      local.get $l44
      f32.mul
      local.get $l55
      local.get $l36
      f32.mul
      f32.sub
      f32.mul
      f32.add
      f32.add
      local.tee $l38
      local.get $l38
      f32.add
      f32.add
      f32.add
      f32.store offset=8
      local.get $p8
      local.get $l71
      local.get $p11
      f32.mul
      local.get $l76
      local.get $l55
      local.get $l49
      f32.mul
      local.get $l60
      local.get $l44
      f32.mul
      local.get $l47
      local.get $l45
      local.get $l36
      f32.mul
      local.get $p9
      local.get $l43
      f32.mul
      f32.sub
      f32.mul
      f32.add
      f32.add
      local.tee $l38
      local.get $l38
      f32.add
      f32.add
      f32.add
      f32.store offset=4
      local.get $p8
      local.get $l73
      local.get $p11
      f32.mul
      local.get $l78
      local.get $p9
      local.get $l49
      f32.mul
      local.get $l60
      local.get $l36
      f32.mul
      local.get $l47
      local.get $l55
      local.get $l43
      f32.mul
      local.get $l45
      local.get $l44
      f32.mul
      f32.sub
      f32.mul
      f32.add
      f32.add
      local.tee $p9
      local.get $p9
      f32.add
      f32.add
      f32.add
      f32.store
    end
    local.get $p10
    i32.const 416
    i32.add
    global.set $g0
    local.get $l50)
