  (func $f71093 (type $t6) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32)
    (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32) (local $l33 f32) (local $l34 f32) (local $l35 f32) (local $l36 f32) (local $l37 f32) (local $l38 f32) (local $l39 f32) (local $l40 f32) (local $l41 f32) (local $l42 f32) (local $l43 f32) (local $l44 f32) (local $l45 f32) (local $l46 f32) (local $l47 f32) (local $l48 f32) (local $l49 f32) (local $l50 f32) (local $l51 f32) (local $l52 f32) (local $l53 f32) (local $l54 f32) (local $l55 f32) (local $l56 f32) (local $l57 f32) (local $l58 f32) (local $l59 f32) (local $l60 f32) (local $l61 f32) (local $l62 f32) (local $l63 f32) (local $l64 f32) (local $l65 f32) (local $l66 f32) (local $l67 f32)
    global.get $g0
    i32.const 512
    i32.sub
    local.tee $l5
    global.set $g0
    local.get $p0
    i32.load16_u offset=42
    local.set $l10
    local.get $p0
    i32.load16_u offset=6
    local.set $l8
    local.get $p0
    i32.load16_u offset=40
    local.set $l9
    local.get $p4
    local.get $p4
    i32.load offset=8
    local.tee $l7
    local.get $p0
    i32.load16_u offset=4
    local.tee $l6
    i32.const 144
    i32.mul
    local.tee $l11
    i32.add
    i32.store offset=8
    local.get $l7
    local.get $p4
    i32.load
    i32.add
    local.get $p1
    local.get $l11
    call $f483
    local.set $l7
    local.get $p0
    i32.load16_u offset=4
    i32.const 1
    i32.sub
    local.tee $p1
    if $I0
      local.get $p0
      local.get $l9
      i32.add
      local.get $l6
      i32.const 400
      i32.mul
      i32.add
      local.get $l6
      i32.const 5
      i32.shl
      i32.add
      local.set $l12
      local.get $p0
      local.get $l8
      i32.add
      local.set $l13
      local.get $p0
      local.get $l10
      i32.add
      i32.const 144
      i32.add
      local.set $l14
      local.get $l5
      i32.const 352
      i32.add
      local.set $l11
      local.get $l5
      i32.const 336
      i32.add
      local.set $l10
      loop $L1
        local.get $l5
        i32.const 368
        i32.add
        local.get $l7
        local.get $p1
        i32.const 144
        i32.mul
        i32.add
        local.tee $l6
        local.get $l12
        local.get $p1
        i32.const 96
        i32.mul
        i32.add
        local.get $l5
        i32.const 416
        i32.add
        call $f71056
        local.get $l5
        i32.const 360
        i32.add
        local.tee $l8
        local.get $p2
        local.get $p1
        i32.const 2
        i32.shl
        i32.add
        f32.load
        local.tee $l16
        local.get $p3
        local.get $p1
        i32.const 48
        i32.mul
        i32.add
        local.tee $p4
        f32.load
        f32.mul
        local.get $l5
        f32.load offset=368
        f32.add
        local.tee $l20
        local.get $l16
        local.get $p4
        f32.load offset=20
        f32.mul
        local.get $l5
        f32.load offset=388
        f32.add
        local.tee $l18
        f32.mul
        local.get $l16
        local.get $p4
        f32.load offset=4
        f32.mul
        local.get $l5
        f32.load offset=372
        f32.add
        local.tee $l19
        local.get $l16
        local.get $p4
        f32.load offset=16
        f32.mul
        local.get $l5
        f32.load offset=384
        f32.add
        local.tee $l17
        f32.mul
        f32.sub
        f32.const 0x1p+0 (;=1;)
        local.get $l16
        local.get $p4
        f32.load offset=8
        f32.mul
        local.get $l5
        f32.load offset=376
        f32.add
        local.tee $l25
        local.get $l17
        local.get $l16
        local.get $p4
        f32.load offset=36
        f32.mul
        local.get $l5
        f32.load offset=404
        f32.add
        local.tee $l23
        f32.mul
        local.get $l18
        local.get $l16
        local.get $p4
        f32.load offset=32
        f32.mul
        local.get $l5
        f32.load offset=400
        f32.add
        local.tee $l21
        f32.mul
        f32.sub
        local.tee $l22
        f32.mul
        local.get $l20
        local.get $l18
        local.get $l16
        local.get $p4
        f32.load offset=40
        f32.mul
        local.get $l5
        f32.load offset=408
        f32.add
        local.tee $l24
        f32.mul
        local.get $l16
        local.get $p4
        f32.load offset=24
        f32.mul
        local.get $l5
        f32.load offset=392
        f32.add
        local.tee $l16
        local.get $l23
        f32.mul
        f32.sub
        local.tee $l18
        f32.mul
        local.get $l19
        local.get $l16
        local.get $l21
        f32.mul
        local.get $l17
        local.get $l24
        f32.mul
        f32.sub
        local.tee $l17
        f32.mul
        f32.add
        f32.add
        f32.div
        local.tee $l16
        f32.mul
        f32.store
        local.get $l11
        local.get $l22
        local.get $l16
        f32.mul
        local.tee $l22
        f32.store
        local.get $l5
        i32.const 344
        i32.add
        local.tee $l9
        local.get $l19
        local.get $l21
        f32.mul
        local.get $l20
        local.get $l23
        f32.mul
        f32.sub
        local.get $l16
        f32.mul
        local.tee $l19
        f32.store
        local.get $l10
        local.get $l17
        local.get $l16
        f32.mul
        local.tee $l17
        f32.store
        local.get $l5
        i32.const 0
        i32.store offset=332
        local.get $l5
        local.get $l22
        f32.store offset=328
        local.get $l5
        i32.const 0
        i32.store offset=364
        local.get $l5
        i32.const 0
        i32.store offset=348
        local.get $l5
        local.get $l19
        f32.store offset=356
        local.get $l5
        local.get $l20
        local.get $l24
        f32.mul
        local.get $l25
        local.get $l21
        f32.mul
        f32.sub
        local.get $l16
        f32.mul
        f32.store offset=340
        local.get $l5
        local.get $l17
        f32.store offset=324
        local.get $l5
        local.get $l18
        local.get $l16
        f32.mul
        f32.store offset=320
        local.get $l14
        local.get $p1
        i32.const 208
        i32.mul
        i32.add
        local.tee $p4
        local.get $l5
        i64.load offset=328
        i64.store offset=104
        local.get $p4
        local.get $l5
        i64.load offset=320
        i64.store offset=96
        local.get $p4
        local.get $l8
        i64.load
        i64.store offset=136
        local.get $p4
        local.get $l11
        i64.load
        i64.store offset=128
        local.get $p4
        local.get $l9
        i64.load
        i64.store offset=120
        local.get $p4
        local.get $l10
        i64.load
        i64.store offset=112
        local.get $p0
        local.get $p1
        i32.add
        i32.const 80
        i32.add
        local.tee $l8
        i32.load8_u
        local.set $l9
        local.get $l5
        local.get $l13
        local.get $p1
        i32.const 5
        i32.shl
        i32.add
        local.tee $l15
        i64.load offset=8
        i64.store offset=168
        local.get $l5
        local.get $l15
        i64.load
        i64.store offset=160
        local.get $l5
        i32.const 16
        i32.add
        local.get $l6
        local.get $l5
        i32.const 320
        i32.add
        local.get $l5
        i32.const 416
        i32.add
        local.get $p4
        call $f71057
        local.get $l5
        local.get $l5
        i64.load offset=168
        i64.store offset=8
        local.get $l5
        local.get $l5
        i64.load offset=160
        i64.store
        local.get $l5
        i32.const 176
        i32.add
        local.get $l5
        local.get $l5
        i32.const 16
        i32.add
        call $f71092
        local.get $l7
        local.get $l9
        i32.const 144
        i32.mul
        i32.add
        local.tee $l6
        f32.load offset=20
        local.set $l16
        local.get $l6
        f32.load offset=24
        local.set $l20
        local.get $l6
        f32.load offset=36
        local.set $l21
        local.get $l6
        f32.load offset=40
        local.set $l18
        local.get $l6
        f32.load offset=52
        local.set $l19
        local.get $l6
        f32.load offset=56
        local.set $l17
        local.get $l6
        i32.const -64
        i32.sub
        f32.load
        local.set $l23
        local.get $l6
        f32.load offset=68
        local.set $l24
        local.get $l6
        f32.load offset=72
        local.set $l25
        local.get $l6
        f32.load offset=80
        local.set $l22
        local.get $l6
        f32.load offset=84
        local.set $l26
        local.get $l6
        f32.load offset=88
        local.set $l27
        local.get $l6
        f32.load offset=100
        local.set $l28
        local.get $l6
        f32.load offset=104
        local.set $l29
        local.get $l6
        f32.load offset=112
        local.set $l30
        local.get $l6
        f32.load offset=116
        local.set $l31
        local.get $l6
        f32.load offset=120
        local.set $l32
        local.get $l6
        f32.load offset=128
        local.set $l33
        local.get $l6
        f32.load offset=132
        local.set $l34
        local.get $l6
        f32.load offset=136
        local.set $l35
        local.get $l6
        f32.load
        local.set $l36
        local.get $l6
        f32.load offset=4
        local.set $l37
        local.get $l6
        f32.load offset=8
        local.set $l38
        local.get $l6
        f32.load offset=16
        local.set $l39
        local.get $l6
        f32.load offset=32
        local.set $l40
        local.get $l6
        f32.load offset=48
        local.set $l41
        local.get $l5
        f32.load offset=196
        local.set $l42
        local.get $l5
        f32.load offset=200
        local.set $l43
        local.get $l5
        f32.load offset=212
        local.set $l44
        local.get $l5
        f32.load offset=216
        local.set $l45
        local.get $l5
        f32.load offset=228
        local.set $l46
        local.get $l5
        f32.load offset=232
        local.set $l47
        local.get $l5
        f32.load offset=240
        local.set $l48
        local.get $l5
        f32.load offset=244
        local.set $l49
        local.get $l5
        f32.load offset=248
        local.set $l50
        local.get $l5
        f32.load offset=256
        local.set $l51
        local.get $l5
        f32.load offset=260
        local.set $l52
        local.get $l5
        f32.load offset=264
        local.set $l53
        local.get $l5
        f32.load offset=276
        local.set $l54
        local.get $l5
        f32.load offset=280
        local.set $l55
        local.get $l5
        f32.load offset=288
        local.set $l56
        local.get $l5
        f32.load offset=292
        local.set $l57
        local.get $l5
        f32.load offset=296
        local.set $l58
        local.get $l5
        f32.load offset=304
        local.set $l59
        local.get $l5
        f32.load offset=308
        local.set $l60
        local.get $l5
        f32.load offset=312
        local.set $l61
        local.get $l5
        f32.load offset=176
        local.set $l62
        local.get $l5
        f32.load offset=180
        local.set $l63
        local.get $l5
        f32.load offset=184
        local.set $l64
        local.get $l5
        f32.load offset=192
        local.set $l65
        local.get $l5
        f32.load offset=208
        local.set $l66
        local.get $l5
        f32.load offset=224
        local.set $l67
        local.get $l7
        local.get $l8
        i32.load8_u
        i32.const 144
        i32.mul
        i32.add
        local.tee $p4
        local.get $l6
        f32.load offset=96
        local.get $l5
        f32.load offset=272
        f32.add
        f32.store offset=96
        local.get $p4
        local.get $l41
        local.get $l67
        f32.add
        f32.store offset=48
        local.get $p4
        local.get $l40
        local.get $l66
        f32.add
        f32.store offset=32
        local.get $p4
        local.get $l39
        local.get $l65
        f32.add
        f32.store offset=16
        local.get $p4
        i32.const 0
        i32.store offset=12
        local.get $p4
        local.get $l38
        local.get $l64
        f32.add
        f32.store offset=8
        local.get $p4
        local.get $l37
        local.get $l63
        f32.add
        f32.store offset=4
        local.get $p4
        local.get $l36
        local.get $l62
        f32.add
        f32.store
        local.get $p4
        i32.const 0
        i32.store offset=140
        local.get $p4
        local.get $l35
        local.get $l61
        f32.add
        f32.store offset=136
        local.get $p4
        local.get $l34
        local.get $l60
        f32.add
        f32.store offset=132
        local.get $p4
        local.get $l33
        local.get $l59
        f32.add
        f32.store offset=128
        local.get $p4
        i32.const 0
        i32.store offset=124
        local.get $p4
        local.get $l32
        local.get $l58
        f32.add
        f32.store offset=120
        local.get $p4
        local.get $l31
        local.get $l57
        f32.add
        f32.store offset=116
        local.get $p4
        local.get $l30
        local.get $l56
        f32.add
        f32.store offset=112
        local.get $p4
        i32.const 0
        i32.store offset=108
        local.get $p4
        local.get $l29
        local.get $l55
        f32.add
        f32.store offset=104
        local.get $p4
        local.get $l28
        local.get $l54
        f32.add
        f32.store offset=100
        local.get $p4
        i32.const 0
        i32.store offset=92
        local.get $p4
        local.get $l27
        local.get $l53
        f32.add
        f32.store offset=88
        local.get $p4
        local.get $l26
        local.get $l52
        f32.add
        f32.store offset=84
        local.get $p4
        local.get $l22
        local.get $l51
        f32.add
        f32.store offset=80
        local.get $p4
        i32.const 0
        i32.store offset=76
        local.get $p4
        local.get $l25
        local.get $l50
        f32.add
        f32.store offset=72
        local.get $p4
        local.get $l24
        local.get $l49
        f32.add
        f32.store offset=68
        local.get $p4
        i32.const -64
        i32.sub
        local.get $l23
        local.get $l48
        f32.add
        f32.store
        local.get $p4
        i32.const 0
        i32.store offset=60
        local.get $p4
        local.get $l17
        local.get $l47
        f32.add
        f32.store offset=56
        local.get $p4
        local.get $l19
        local.get $l46
        f32.add
        f32.store offset=52
        local.get $p4
        i32.const 0
        i32.store offset=44
        local.get $p4
        local.get $l18
        local.get $l45
        f32.add
        f32.store offset=40
        local.get $p4
        local.get $l21
        local.get $l44
        f32.add
        f32.store offset=36
        local.get $p4
        i32.const 0
        i32.store offset=28
        local.get $p4
        local.get $l20
        local.get $l43
        f32.add
        f32.store offset=24
        local.get $p4
        local.get $l16
        local.get $l42
        f32.add
        f32.store offset=20
        local.get $p1
        i32.const 1
        i32.sub
        local.tee $p1
        br_if $L1
      end
    end
    local.get $l5
    i32.const 176
    i32.add
    local.get $l7
    call $f71055
    local.get $p0
    local.get $p0
    i32.load16_u offset=42
    i32.add
    local.tee $p4
    local.get $l5
    i64.load offset=176
    i64.store
    local.get $p4
    local.get $l5
    i64.load offset=184
    i64.store offset=8
    local.get $p4
    local.get $l5
    i64.load offset=192
    i64.store offset=16
    local.get $p4
    local.get $l5
    i64.load offset=200
    i64.store offset=24
    local.get $p4
    local.get $l5
    i64.load offset=208
    i64.store offset=32
    local.get $p4
    local.get $l5
    i64.load offset=216
    i64.store offset=40
    local.get $p4
    local.get $l5
    i64.load offset=224
    i64.store offset=48
    local.get $p4
    local.get $l5
    i64.load offset=232
    i64.store offset=56
    local.get $p4
    local.get $l5
    i64.load offset=240
    i64.store offset=64
    local.get $p4
    local.get $l5
    i64.load offset=248
    i64.store offset=72
    local.get $p4
    local.get $l5
    i64.load offset=256
    i64.store offset=80
    local.get $p4
    local.get $l5
    i64.load offset=264
    i64.store offset=88
    local.get $p4
    local.get $l5
    i64.load offset=272
    i64.store offset=96
    local.get $p4
    local.get $l5
    i64.load offset=280
    i64.store offset=104
    local.get $p4
    local.get $l5
    i64.load offset=296
    i64.store offset=120
    local.get $p4
    local.get $l5
    i64.load offset=288
    i64.store offset=112
    local.get $p4
    local.get $l5
    i64.load offset=312
    i64.store offset=136
    local.get $p4
    local.get $l5
    i64.load offset=304
    i64.store offset=128
    local.get $l5
    i32.const 512
    i32.add
    global.set $g0)
