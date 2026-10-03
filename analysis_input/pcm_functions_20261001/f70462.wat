  (func $f70462 (type $t130) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 f32) (param $p6 i32) (param $p7 i32) (param $p8 f32) (result i32)
    (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 i32) (local $l17 i32) (local $l18 i32) (local $l19 i32) (local $l20 i32) (local $l21 i32) (local $l22 i32) (local $l23 i32) (local $l24 i32) (local $l25 i32) (local $l26 i32) (local $l27 i32) (local $l28 i32) (local $l29 i32) (local $l30 i32) (local $l31 i32) (local $l32 i32) (local $l33 i32) (local $l34 i32) (local $l35 i32) (local $l36 i32) (local $l37 i32) (local $l38 i32) (local $l39 f32) (local $l40 f32) (local $l41 f32) (local $l42 f32) (local $l43 f32) (local $l44 f32) (local $l45 f32) (local $l46 f32) (local $l47 f32) (local $l48 f32) (local $l49 f32) (local $l50 f32) (local $l51 f32) (local $l52 f32) (local $l53 f32) (local $l54 f32) (local $l55 f32) (local $l56 f32) (local $l57 f32) (local $l58 f32) (local $l59 f32) (local $l60 f32) (local $l61 f32) (local $l62 f32) (local $l63 f32) (local $l64 f32) (local $l65 f32) (local $l66 f32) (local $l67 f32) (local $l68 f32) (local $l69 f32) (local $l70 f32) (local $l71 f32) (local $l72 f32) (local $l73 f32) (local $l74 f32) (local $l75 f32) (local $l76 f32) (local $l77 f32) (local $l78 f32) (local $l79 f32) (local $l80 f32) (local $l81 f32) (local $l82 f32) (local $l83 f32) (local $l84 f32) (local $l85 f32) (local $l86 f32) (local $l87 f32) (local $l88 f32) (local $l89 i64) (local $l90 i64)
    global.get $g0
    i32.const 624
    i32.sub
    local.tee $l10
    global.set $g0
    f32.const 0x1p+0 (;=1;)
    local.set $l45
    block $B0 (result i32)
      i32.const 0
      local.get $p2
      f32.load offset=4
      f32.const 0x1p+0 (;=1;)
      f32.ne
      br_if $B0
      drop
      i32.const 0
      local.get $p2
      f32.load offset=8
      f32.const 0x1p+0 (;=1;)
      f32.ne
      br_if $B0
      drop
      local.get $p2
      f32.load offset=12
      f32.const 0x1p+0 (;=1;)
      f32.eq
    end
    local.set $l13
    local.get $p2
    i32.const 4
    i32.add
    local.set $l15
    local.get $p2
    i32.load offset=32
    local.set $l12
    local.get $l10
    i64.const 4575657221408423936
    i64.store offset=608
    local.get $l10
    i64.const 0
    i64.store offset=600
    local.get $l10
    i64.const 4575657221408423936
    i64.store offset=592
    local.get $l10
    i64.const 0
    i64.store offset=584
    local.get $l10
    i64.const 4575657222473777152
    i64.store offset=576
    local.get $l10
    i64.const 1065353216
    i64.store offset=560
    local.get $l10
    i32.const 0
    i32.store8 offset=616
    local.get $l10
    i64.const 0
    i64.store offset=568
    local.get $l10
    i64.const 0
    i64.store offset=552
    local.get $l10
    i64.const 1065353216
    i64.store offset=544
    f32.const 0x1p+0 (;=1;)
    local.set $l43
    f32.const 0x1p+0 (;=1;)
    local.set $l46
    local.get $l13
    i32.eqz
    if $I1
      local.get $l10
      i32.const 544
      i32.add
      local.get $l15
      local.get $p2
      i32.const 16
      i32.add
      call $f70485
      local.get $l10
      f32.load offset=568
      local.set $l41
      local.get $l10
      f32.load offset=564
      local.set $l40
      local.get $l10
      f32.load offset=560
      local.set $l43
      local.get $l10
      f32.load offset=552
      local.set $l44
      local.get $l10
      f32.load offset=548
      local.set $l47
      local.get $l10
      f32.load offset=544
      local.set $l46
      local.get $l10
      f32.load offset=576
      local.set $l45
      local.get $l10
      f32.load offset=556
      local.set $l48
      local.get $l10
      f32.load offset=572
      local.set $l39
    end
    local.get $l10
    local.get $l12
    f32.load offset=16
    local.tee $l50
    local.get $l44
    f32.mul
    local.get $l12
    f32.load offset=20
    local.tee $l49
    local.get $l40
    f32.mul
    f32.add
    local.get $l12
    f32.load offset=24
    local.tee $l51
    local.get $l45
    f32.mul
    f32.add
    local.tee $l53
    local.get $l44
    local.get $l12
    f32.load offset=28
    local.tee $l52
    f32.mul
    f32.abs
    local.get $l40
    local.get $l12
    f32.load offset=32
    local.tee $l44
    f32.mul
    f32.abs
    f32.add
    local.get $l45
    local.get $l12
    f32.load offset=36
    local.tee $l40
    f32.mul
    f32.abs
    f32.add
    local.tee $l45
    f32.add
    f32.store offset=540
    local.get $l10
    local.get $l50
    local.get $l47
    f32.mul
    local.get $l49
    local.get $l43
    f32.mul
    f32.add
    local.get $l51
    local.get $l39
    f32.mul
    f32.add
    local.tee $l57
    local.get $l47
    local.get $l52
    f32.mul
    f32.abs
    local.get $l43
    local.get $l44
    f32.mul
    f32.abs
    f32.add
    local.get $l39
    local.get $l40
    f32.mul
    f32.abs
    f32.add
    local.tee $l39
    f32.add
    f32.store offset=536
    local.get $l10
    local.get $l50
    local.get $l46
    f32.mul
    local.get $l49
    local.get $l48
    f32.mul
    f32.add
    local.get $l51
    local.get $l41
    f32.mul
    f32.add
    local.tee $l43
    local.get $l46
    local.get $l52
    f32.mul
    f32.abs
    local.get $l48
    local.get $l44
    f32.mul
    f32.abs
    f32.add
    local.get $l41
    local.get $l40
    f32.mul
    f32.abs
    f32.add
    local.tee $l41
    f32.add
    f32.store offset=532
    local.get $l10
    local.get $l53
    local.get $l45
    f32.sub
    f32.store offset=528
    local.get $l10
    local.get $l57
    local.get $l39
    f32.sub
    f32.store offset=524
    local.get $l10
    local.get $l43
    local.get $l41
    f32.sub
    f32.store offset=520
    local.get $p0
    i32.load offset=4
    local.set $l13
    local.get $l10
    local.get $p0
    i32.store offset=512
    local.get $l10
    local.get $l13
    i32.store offset=508
    local.get $l10
    f32.const 0x1p+0 (;=1;)
    local.get $p0
    f32.load offset=8
    f32.div
    f32.store offset=500
    local.get $l10
    f32.const 0x1p+0 (;=1;)
    local.get $p0
    f32.load offset=12
    f32.div
    f32.store offset=496
    local.get $l10
    f32.const 0x1p+0 (;=1;)
    local.get $p0
    f32.load offset=16
    f32.div
    f32.store offset=504
    local.get $p4
    f32.load
    local.set $l45
    local.get $p4
    f32.load offset=4
    local.set $l39
    local.get $l10
    local.get $p4
    f32.load offset=8
    f32.neg
    f32.store offset=8
    local.get $l10
    local.get $l39
    f32.neg
    f32.store offset=4
    local.get $l10
    local.get $l45
    f32.neg
    f32.store
    local.get $l10
    local.get $p7
    i32.load16_u
    i32.store16 offset=104
    local.get $l12
    i32.const 16
    i32.add
    local.set $l17
    global.get $g0
    i32.const 32
    i32.sub
    local.tee $l9
    global.set $g0
    local.get $l10
    i32.load16_u offset=104
    local.set $l14
    local.get $l10
    i32.const 112
    i32.add
    local.tee $l11
    i32.const 0
    i32.store16 offset=10
    local.get $l11
    local.get $l14
    i32.store16 offset=8
    local.get $l11
    local.get $l10
    i32.const 496
    i32.add
    local.tee $l13
    i32.store offset=4
    local.get $l11
    i32.const 3132068
    i32.store
    local.get $l13
    i32.load offset=16
    i32.load8_u offset=20
    local.set $l13
    local.get $l11
    local.get $l14
    i32.const 6
    i32.shr_u
    i32.const 1
    i32.and
    i32.store8 offset=13
    local.get $l11
    i32.const -64
    i32.sub
    local.tee $l16
    i64.const 0
    i64.store
    local.get $l11
    i32.const 3132088
    i32.store
    local.get $l11
    i32.const 72
    i32.add
    local.tee $l18
    i64.const 0
    i64.store
    local.get $l11
    i32.const 20
    i32.add
    local.tee $l19
    i64.const 0
    i64.store align=4
    local.get $l11
    i32.const 28
    i32.add
    local.tee $l20
    i64.const 0
    i64.store align=4
    local.get $l11
    i32.const 40
    i32.add
    local.tee $l21
    i64.const 0
    i64.store
    local.get $l11
    i32.const 48
    i32.add
    local.tee $l22
    i64.const 0
    i64.store
    local.get $l11
    i32.const 96
    i32.add
    local.tee $l23
    i64.const 0
    i64.store
    local.get $l11
    i32.const 56
    i32.add
    local.tee $l26
    i64.const 1065353216
    i64.store
    local.get $l11
    i32.const 36
    i32.add
    local.tee $l27
    i32.const 1065353216
    i32.store
    local.get $l11
    i32.const 1065353216
    i32.store offset=16
    local.get $l11
    i32.const 104
    i32.add
    local.tee $l12
    i64.const 0
    i64.store
    local.get $l11
    i32.const 88
    i32.add
    local.tee $p7
    i64.const 4575657221408423936
    i64.store
    local.get $l11
    i64.const 0
    i64.store offset=80
    local.get $l11
    i64.const 0
    i64.store offset=112
    local.get $l11
    i64.const 0
    i64.store offset=120
    local.get $l11
    i32.const 128
    i32.add
    local.tee $l24
    i64.const 0
    i64.store
    local.get $l11
    i32.const 136
    i32.add
    local.tee $l25
    i64.const 0
    i64.store
    local.get $l11
    i32.const 0
    i32.store8 offset=144
    local.get $l11
    local.get $l14
    i32.const 128
    i32.and
    local.get $l13
    i32.const 2
    i32.and
    i32.or
    i32.const 0
    i32.ne
    i32.store8 offset=12
    local.get $l11
    i32.const 0
    i32.store16 offset=284
    local.get $l11
    i32.const 280
    i32.add
    local.tee $l14
    i32.const -1
    i32.store
    local.get $l11
    i64.const 0
    i64.store offset=272 align=4
    local.get $l11
    i64.const 0
    i64.store offset=288 align=4
    local.get $l11
    i64.const 0
    i64.store offset=296 align=4
    local.get $l11
    i64.const 0
    i64.store offset=304 align=4
    local.get $l11
    i32.const 312
    i32.add
    local.tee $l13
    i32.const 2139095039
    i32.store
    local.get $l11
    local.get $l10
    f32.load
    f32.store offset=352
    local.get $l11
    local.get $l10
    f32.load offset=4
    f32.store offset=356
    local.get $l10
    f32.load offset=8
    local.set $l39
    local.get $l11
    local.get $p8
    f32.store offset=376
    local.get $l11
    local.get $l39
    f32.store offset=360
    local.get $l13
    local.get $p5
    f32.store
    local.get $l14
    i32.const -1
    i32.store
    local.get $p1
    local.tee $l13
    f32.load offset=20
    local.set $l52
    local.get $l13
    f32.load offset=24
    local.set $l57
    local.get $p3
    f32.load offset=20
    local.set $l50
    local.get $p3
    f32.load offset=24
    local.set $l40
    local.get $l10
    f32.load offset=4
    local.set $l58
    local.get $l10
    f32.load
    local.set $l59
    local.get $l10
    f32.load offset=8
    local.set $l60
    local.get $l13
    f32.load offset=8
    local.set $l41
    local.get $l13
    f32.load
    local.set $l46
    local.get $l13
    f32.load offset=4
    local.set $l49
    local.get $l13
    f32.load offset=12
    local.set $l48
    local.get $l13
    f32.load offset=16
    local.set $l53
    local.get $p3
    f32.load
    local.set $l42
    local.get $p3
    f32.load offset=4
    local.set $l44
    local.get $p3
    f32.load offset=8
    local.set $l39
    local.get $p3
    f32.load offset=12
    local.set $l43
    local.get $p3
    f32.load offset=16
    local.set $l47
    local.get $l11
    local.get $p5
    f32.store offset=336
    local.get $l11
    i32.const 0
    i32.store offset=332
    local.get $l11
    i32.const 0
    i32.store offset=108
    local.get $l12
    local.get $l40
    f32.store
    local.get $l11
    local.get $l50
    f32.store offset=100
    local.get $l23
    local.get $l47
    f32.store
    local.get $l11
    local.get $l43
    f32.store offset=92
    local.get $p7
    local.get $l39
    f32.store
    local.get $l11
    local.get $l44
    f32.store offset=84
    local.get $l11
    local.get $l42
    f32.store offset=80
    local.get $l11
    i32.const 0
    i32.store offset=76
    local.get $l11
    i32.const 0
    i32.store offset=60
    local.get $l11
    i32.const 0
    i32.store offset=44
    local.get $l20
    i32.const 0
    i32.store
    local.get $l18
    local.get $l43
    local.get $l43
    f32.mul
    f32.const -0x1p-1 (;=-0.5;)
    f32.add
    local.tee $l51
    local.get $l57
    local.get $l40
    f32.sub
    local.tee $l40
    f32.mul
    local.get $l43
    local.get $l44
    local.get $l53
    local.get $l47
    f32.sub
    local.tee $l47
    f32.mul
    local.get $l42
    local.get $l52
    local.get $l50
    f32.sub
    local.tee $l50
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l39
    local.get $l50
    local.get $l44
    f32.neg
    local.tee $l57
    f32.mul
    local.get $l42
    local.get $l47
    f32.mul
    f32.sub
    local.get $l39
    local.get $l40
    f32.mul
    f32.sub
    local.tee $l52
    f32.mul
    f32.sub
    local.tee $l53
    local.get $l53
    f32.add
    f32.store
    local.get $l11
    local.get $l51
    local.get $l50
    f32.mul
    local.get $l43
    local.get $l42
    local.get $l40
    f32.mul
    local.get $l39
    local.get $l47
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l44
    local.get $l52
    f32.mul
    f32.sub
    local.tee $l53
    local.get $l53
    f32.add
    f32.store offset=68
    local.get $l16
    local.get $l51
    local.get $l47
    f32.mul
    local.get $l43
    local.get $l39
    local.get $l50
    f32.mul
    local.get $l44
    local.get $l40
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l42
    local.get $l52
    f32.mul
    f32.sub
    local.tee $l40
    local.get $l40
    f32.add
    f32.store
    local.get $l26
    f32.const 0x1p+0 (;=1;)
    local.get $l49
    local.get $l39
    f32.mul
    local.get $l41
    local.get $l44
    f32.mul
    f32.sub
    local.get $l46
    local.get $l43
    f32.mul
    local.get $l48
    local.get $l42
    f32.mul
    f32.sub
    f32.add
    local.tee $l40
    local.get $l40
    local.get $l40
    f32.add
    local.tee $l47
    f32.mul
    f32.sub
    local.tee $l53
    local.get $l41
    local.get $l42
    f32.mul
    local.get $l46
    local.get $l39
    f32.mul
    f32.sub
    local.get $l49
    local.get $l43
    f32.mul
    local.get $l48
    local.get $l44
    f32.mul
    f32.sub
    f32.add
    local.tee $l50
    local.get $l50
    local.get $l50
    f32.add
    local.tee $l52
    f32.mul
    local.tee $l55
    f32.sub
    f32.store
    local.get $l11
    local.get $l46
    local.get $l44
    f32.mul
    local.get $l49
    local.get $l42
    f32.mul
    f32.sub
    local.get $l41
    local.get $l43
    f32.mul
    local.get $l48
    local.get $l39
    f32.mul
    f32.sub
    f32.add
    local.tee $l40
    local.get $l52
    f32.mul
    local.tee $l56
    local.get $l48
    local.get $l43
    f32.mul
    local.get $l49
    local.get $l57
    f32.mul
    local.get $l46
    local.get $l42
    f32.mul
    f32.sub
    local.get $l41
    local.get $l39
    f32.mul
    f32.sub
    f32.sub
    local.tee $l41
    local.get $l47
    f32.mul
    local.tee $l46
    f32.sub
    f32.store offset=52
    local.get $l22
    local.get $l40
    local.get $l47
    f32.mul
    local.tee $l49
    local.get $l41
    local.get $l52
    f32.mul
    local.tee $l48
    f32.add
    f32.store
    local.get $l21
    local.get $l56
    local.get $l46
    f32.add
    f32.store
    local.get $l27
    local.get $l53
    local.get $l40
    local.get $l40
    local.get $l40
    f32.add
    local.tee $l46
    f32.mul
    local.tee $l40
    f32.sub
    f32.store
    local.get $l11
    local.get $l50
    local.get $l47
    f32.mul
    local.tee $l47
    local.get $l41
    local.get $l46
    f32.mul
    local.tee $l41
    f32.sub
    f32.store offset=32
    local.get $l11
    local.get $l49
    local.get $l48
    f32.sub
    f32.store offset=24
    local.get $l19
    local.get $l47
    local.get $l41
    f32.add
    f32.store
    local.get $l11
    f32.const 0x1p+0 (;=1;)
    local.get $l55
    f32.sub
    local.get $l40
    f32.sub
    f32.store offset=16
    local.get $l11
    local.get $l39
    local.get $l42
    local.get $l59
    f32.neg
    local.get $p5
    f32.mul
    local.tee $l41
    f32.mul
    local.get $l44
    local.get $l58
    f32.neg
    local.get $p5
    f32.mul
    local.tee $l46
    f32.mul
    f32.add
    local.get $l39
    local.get $l60
    f32.neg
    local.get $p5
    f32.mul
    local.tee $l54
    f32.mul
    f32.add
    local.tee $l49
    f32.mul
    local.get $l54
    local.get $l51
    f32.mul
    local.get $l43
    local.get $l46
    local.get $l42
    f32.mul
    local.get $l41
    local.get $l44
    f32.mul
    f32.sub
    f32.mul
    f32.sub
    f32.add
    local.tee $l48
    local.get $l48
    f32.add
    f32.store offset=328
    local.get $l11
    local.get $l44
    local.get $l49
    f32.mul
    local.get $l46
    local.get $l51
    f32.mul
    local.get $l43
    local.get $l41
    local.get $l39
    f32.mul
    local.get $l54
    local.get $l42
    f32.mul
    f32.sub
    f32.mul
    f32.sub
    f32.add
    local.tee $l48
    local.get $l48
    f32.add
    f32.store offset=324
    local.get $l11
    local.get $l42
    local.get $l49
    f32.mul
    local.get $l41
    local.get $l51
    f32.mul
    local.get $l43
    local.get $l54
    local.get $l44
    f32.mul
    local.get $l46
    local.get $l39
    f32.mul
    f32.sub
    f32.mul
    f32.sub
    f32.add
    local.tee $l42
    local.get $l42
    f32.add
    f32.store offset=320
    local.get $l15
    local.tee $l12
    f32.load
    local.set $l46
    local.get $l12
    f32.load offset=4
    local.set $l49
    local.get $l12
    f32.load offset=8
    local.set $l48
    local.get $l9
    i32.const 0
    i32.store offset=28
    local.get $l9
    local.get $l48
    f32.store offset=24
    local.get $l9
    local.get $l49
    f32.store offset=20
    local.get $l9
    local.get $l46
    f32.store offset=16
    local.get $l12
    i64.load offset=12 align=4
    local.set $l89
    local.get $l9
    local.get $l12
    i64.load offset=20 align=4
    i64.store offset=8
    local.get $l9
    local.get $l89
    i64.store
    local.get $l11
    local.get $l13
    f32.load offset=4
    local.tee $l39
    local.get $l10
    f32.load
    local.tee $l42
    local.get $l42
    f32.add
    local.tee $l43
    local.get $l13
    f32.load
    local.tee $l44
    f32.mul
    local.get $l39
    local.get $l10
    f32.load offset=4
    local.tee $l42
    local.get $l42
    f32.add
    local.tee $l54
    f32.mul
    f32.add
    local.get $l10
    f32.load offset=8
    local.tee $l42
    local.get $l42
    f32.add
    local.tee $l51
    local.get $l13
    f32.load offset=8
    local.tee $l41
    f32.mul
    f32.add
    local.tee $l40
    f32.mul
    local.get $l54
    local.get $l13
    f32.load offset=12
    local.tee $l42
    local.get $l42
    f32.mul
    f32.const -0x1p-1 (;=-0.5;)
    f32.add
    local.tee $l47
    f32.mul
    local.get $l42
    local.get $l43
    local.get $l41
    f32.mul
    local.get $l51
    local.get $l44
    f32.mul
    f32.sub
    f32.mul
    f32.sub
    f32.add
    f32.store offset=368
    local.get $l11
    local.get $l51
    local.get $l47
    f32.mul
    local.get $l42
    local.get $l54
    local.get $l44
    f32.mul
    local.get $l43
    local.get $l39
    f32.mul
    f32.sub
    f32.mul
    f32.sub
    local.get $l41
    local.get $l40
    f32.mul
    f32.add
    f32.store offset=372
    local.get $l11
    local.get $l44
    local.get $l40
    f32.mul
    local.get $l43
    local.get $l47
    f32.mul
    local.get $l42
    local.get $l51
    local.get $l39
    f32.mul
    local.get $l54
    local.get $l41
    f32.mul
    f32.sub
    f32.mul
    f32.sub
    f32.add
    f32.store offset=364
    local.get $l11
    i32.const 112
    i32.add
    local.set $l13
    block $B2
      local.get $l12
      f32.load
      f32.const 0x1p+0 (;=1;)
      f32.ne
      br_if $B2
      local.get $l12
      f32.load offset=4
      f32.const 0x1p+0 (;=1;)
      f32.ne
      br_if $B2
      local.get $l12
      f32.load offset=8
      f32.const 0x1p+0 (;=1;)
      f32.eq
      local.set $l28
    end
    local.get $l17
    i32.load offset=40
    local.set $p7
    local.get $l17
    i32.load8_u offset=39
    local.set $l12
    local.get $l25
    local.get $l46
    local.get $l17
    f32.load offset=52
    f32.mul
    local.tee $l42
    local.get $l49
    local.get $l17
    f32.load offset=56
    f32.mul
    local.tee $l39
    local.get $l39
    local.get $l42
    f32.ge
    select
    local.tee $l42
    local.get $l48
    local.get $l17
    f32.load offset=60
    f32.mul
    local.tee $l39
    local.get $l39
    local.get $l42
    f32.ge
    select
    local.tee $l42
    f32.const 0x1.99999ap-6 (;=0.025;)
    f32.mul
    f32.store
    local.get $l11
    local.get $l42
    f32.const 0x1.99999ap-5 (;=0.05;)
    f32.mul
    f32.store offset=132
    local.get $l24
    local.get $l42
    f32.const 0x1.99999ap-4 (;=0.1;)
    f32.mul
    f32.store
    local.get $l9
    i32.const 16
    i32.add
    local.get $l9
    local.get $l11
    i32.const 160
    i32.add
    local.get $l11
    i32.const 208
    i32.add
    local.get $l13
    local.get $l28
    call $f70494
    local.get $l11
    local.get $p7
    local.get $l12
    i32.const 20
    i32.mul
    i32.add
    i32.store offset=264
    local.get $l11
    local.get $l17
    i32.load8_u offset=38
    i32.store8 offset=268
    local.get $l13
    i64.const 0
    i64.store offset=8
    local.get $l13
    i64.const 0
    i64.store
    local.get $l17
    i32.load offset=44
    local.set $l13
    local.get $l11
    local.get $l17
    i32.store offset=256
    local.get $l11
    local.get $l13
    i32.store offset=260
    local.get $l17
    i32.load offset=44
    drop
    local.get $l9
    i32.const 32
    i32.add
    global.set $g0
    local.get $l10
    i32.const 80
    i32.add
    local.get $p3
    local.get $l10
    i32.const 520
    i32.add
    call $f70451
    local.get $l10
    local.get $p1
    f32.load
    local.tee $l45
    local.get $l45
    local.get $p1
    f32.load offset=16
    f32.const -0x1p+1 (;=-2;)
    f32.mul
    local.tee $l44
    f32.mul
    local.get $p1
    f32.load offset=20
    f32.const -0x1p+1 (;=-2;)
    f32.mul
    local.tee $l47
    local.get $p1
    f32.load offset=4
    local.tee $l40
    f32.mul
    f32.add
    local.get $p1
    f32.load offset=24
    f32.const -0x1p+1 (;=-2;)
    f32.mul
    local.tee $l46
    local.get $p1
    f32.load offset=8
    local.tee $l39
    f32.mul
    f32.add
    local.tee $l52
    f32.mul
    local.get $l44
    local.get $p1
    f32.load offset=12
    local.tee $l41
    local.get $l41
    f32.mul
    f32.const -0x1p-1 (;=-0.5;)
    f32.add
    local.tee $l43
    f32.mul
    local.get $l41
    local.get $l46
    local.get $l40
    f32.mul
    local.get $l47
    local.get $l39
    f32.mul
    f32.sub
    f32.mul
    f32.sub
    f32.add
    local.get $l10
    f32.load offset=92
    local.tee $l58
    local.get $l10
    f32.load offset=80
    local.tee $l59
    f32.add
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    local.tee $l48
    local.get $l48
    f32.add
    local.tee $l50
    local.get $l43
    f32.mul
    local.get $l41
    local.get $l10
    f32.load offset=96
    local.tee $l55
    local.get $l10
    f32.load offset=84
    local.tee $l56
    f32.add
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    local.tee $l48
    local.get $l48
    f32.add
    local.tee $l49
    local.get $l39
    f32.mul
    local.get $l10
    f32.load offset=100
    local.tee $l42
    local.get $l10
    f32.load offset=88
    local.tee $l54
    f32.add
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    local.tee $l48
    local.get $l48
    f32.add
    local.tee $l51
    local.get $l40
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l45
    local.get $l49
    local.get $l40
    f32.neg
    local.tee $l48
    f32.mul
    local.get $l50
    local.get $l45
    f32.mul
    f32.sub
    local.get $l51
    local.get $l39
    f32.mul
    f32.sub
    local.tee $l53
    f32.mul
    f32.sub
    f32.add
    local.tee $l57
    f32.store offset=64
    local.get $l10
    local.get $l40
    local.get $l52
    f32.mul
    local.get $l47
    local.get $l43
    f32.mul
    local.get $l41
    local.get $l44
    local.get $l39
    f32.mul
    local.get $l46
    local.get $l45
    f32.mul
    f32.sub
    f32.mul
    f32.sub
    f32.add
    local.get $l49
    local.get $l43
    f32.mul
    local.get $l41
    local.get $l51
    local.get $l45
    f32.mul
    local.get $l50
    local.get $l39
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l40
    local.get $l53
    f32.mul
    f32.sub
    f32.add
    local.tee $l60
    f32.store offset=68
    local.get $l10
    local.get $l51
    local.get $l43
    f32.mul
    local.get $l41
    local.get $l50
    local.get $l40
    f32.mul
    local.get $l49
    local.get $l45
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l39
    local.get $l53
    f32.mul
    f32.sub
    local.get $l46
    local.get $l43
    f32.mul
    local.get $l41
    local.get $l47
    local.get $l45
    f32.mul
    local.get $l44
    local.get $l40
    f32.mul
    f32.sub
    f32.mul
    f32.sub
    local.get $l39
    local.get $l52
    f32.mul
    f32.add
    f32.add
    local.tee $l50
    f32.store offset=72
    local.get $l10
    local.get $l43
    local.get $p4
    f32.load offset=8
    local.tee $l44
    local.get $l44
    f32.add
    local.tee $l44
    f32.mul
    local.get $l41
    local.get $l40
    local.get $p4
    f32.load
    local.tee $l47
    local.get $l47
    f32.add
    local.tee $l47
    f32.mul
    local.get $l45
    local.get $p4
    f32.load offset=4
    local.tee $l46
    local.get $l46
    f32.add
    local.tee $l46
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l39
    local.get $l46
    local.get $l48
    f32.mul
    local.get $l45
    local.get $l47
    f32.mul
    f32.sub
    local.get $l39
    local.get $l44
    f32.mul
    f32.sub
    local.tee $l49
    f32.mul
    f32.sub
    f32.store offset=56
    local.get $l10
    local.get $l43
    local.get $l46
    f32.mul
    local.get $l41
    local.get $l45
    local.get $l44
    f32.mul
    local.get $l39
    local.get $l47
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l40
    local.get $l49
    f32.mul
    f32.sub
    f32.store offset=52
    local.get $l10
    local.get $l43
    local.get $l47
    f32.mul
    local.get $l41
    local.get $l39
    local.get $l46
    f32.mul
    local.get $l40
    local.get $l44
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l45
    local.get $l49
    f32.mul
    f32.sub
    f32.store offset=48
    local.get $l10
    local.get $l50
    local.get $l42
    local.get $l54
    f32.sub
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    local.get $p8
    f32.add
    local.tee $l44
    local.get $l45
    local.get $l45
    f32.neg
    local.get $l45
    f32.sub
    local.tee $l43
    f32.mul
    f32.const 0x1p+0 (;=1;)
    f32.add
    local.tee $l49
    local.get $l48
    local.get $l40
    f32.sub
    local.tee $l40
    local.get $l48
    f32.mul
    local.tee $l51
    f32.sub
    f32.mul
    f32.abs
    local.get $l58
    local.get $l59
    f32.sub
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    local.get $p8
    f32.add
    local.tee $l47
    local.get $l43
    local.get $l39
    f32.neg
    local.tee $l45
    f32.mul
    local.tee $l52
    local.get $l41
    local.get $l40
    f32.mul
    local.tee $l53
    f32.sub
    f32.mul
    f32.abs
    local.get $l55
    local.get $l56
    f32.sub
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    local.get $p8
    f32.add
    local.tee $l46
    local.get $l41
    local.get $l43
    f32.mul
    local.tee $l58
    local.get $l40
    local.get $l45
    f32.mul
    local.tee $l40
    f32.add
    f32.mul
    f32.abs
    f32.add
    f32.add
    local.tee $l59
    f32.add
    local.get $l50
    local.get $l59
    f32.sub
    f32.sub
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.store offset=40
    local.get $l10
    local.get $l60
    local.get $l44
    local.get $l40
    local.get $l58
    f32.sub
    f32.mul
    f32.abs
    local.get $l47
    local.get $l43
    local.get $l48
    f32.mul
    local.tee $l40
    local.get $l41
    local.get $l45
    local.get $l39
    f32.sub
    local.tee $l39
    f32.mul
    local.tee $l41
    f32.add
    f32.mul
    f32.abs
    local.get $l46
    local.get $l49
    local.get $l39
    local.get $l45
    f32.mul
    local.tee $l45
    f32.sub
    f32.mul
    f32.abs
    f32.add
    f32.add
    local.tee $l39
    f32.add
    local.get $l60
    local.get $l39
    f32.sub
    f32.sub
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.store offset=36
    local.get $l10
    local.get $l57
    local.get $l44
    local.get $l52
    local.get $l53
    f32.add
    f32.mul
    f32.abs
    local.get $l47
    f32.const 0x1p+0 (;=1;)
    local.get $l51
    f32.sub
    local.get $l45
    f32.sub
    f32.mul
    f32.abs
    local.get $l46
    local.get $l40
    local.get $l41
    f32.sub
    f32.mul
    f32.abs
    f32.add
    f32.add
    local.tee $l45
    f32.add
    local.get $l57
    local.get $l45
    f32.sub
    f32.sub
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.store offset=32
    local.get $l10
    local.get $l10
    i32.const 32
    i32.add
    i32.store offset=4
    local.get $l10
    local.get $l10
    i32.const 496
    i32.add
    i32.store
    local.get $l10
    i32.const 496
    i32.add
    local.get $l10
    i32.const 8
    i32.add
    local.tee $l13
    call $f70443
    local.get $l10
    i32.const 16
    i32.add
    local.tee $l15
    local.get $l15
    f32.load
    local.get $l10
    f32.load offset=40
    local.tee $l45
    f32.sub
    f32.store
    local.get $l10
    i32.const 12
    i32.add
    local.tee $l15
    local.get $l15
    f32.load
    local.get $l10
    f32.load offset=36
    local.tee $l39
    f32.sub
    f32.store
    local.get $l10
    i32.const 20
    i32.add
    local.tee $l15
    local.get $l10
    f32.load offset=32
    local.tee $l41
    local.get $l15
    f32.load
    f32.add
    f32.store
    local.get $l10
    i32.const 24
    i32.add
    local.tee $l15
    local.get $l39
    local.get $l15
    f32.load
    f32.add
    f32.store
    local.get $l10
    i32.const 28
    i32.add
    local.tee $l15
    local.get $l45
    local.get $l15
    f32.load
    f32.add
    f32.store
    local.get $l10
    local.get $l10
    f32.load offset=8
    local.get $l41
    f32.sub
    f32.store offset=8
    local.get $l10
    i32.load
    local.get $l10
    i32.const -64
    i32.sub
    local.get $l10
    i32.const 48
    i32.add
    local.get $p5
    local.get $l11
    local.tee $l12
    local.get $l13
    local.get $l10
    i32.load offset=4
    call $f70461
    block $B3
      local.get $l11
      i32.load8_u offset=10
      local.tee $p7
      i32.eqz
      br_if $B3
      local.get $l12
      i32.load8_u offset=11
      if $I4
        local.get $l12
        i32.load8_u offset=9
        i32.const 2
        i32.and
        if $I5
          local.get $p8
          local.set $l54
          local.get $l12
          i32.load8_u offset=12
          local.set $l29
          f32.const 0x0p+0 (;=0;)
          local.set $l43
          f32.const 0x0p+0 (;=0;)
          local.set $l44
          f32.const 0x0p+0 (;=0;)
          local.set $l46
          f32.const 0x0p+0 (;=0;)
          local.set $l48
          f32.const 0x0p+0 (;=0;)
          local.set $l49
          f32.const 0x0p+0 (;=0;)
          local.set $l52
          f32.const 0x0p+0 (;=0;)
          local.set $l59
          f32.const 0x0p+0 (;=0;)
          local.set $l60
          i32.const 0
          local.set $l24
          i32.const 0
          local.set $l25
          global.get $g0
          i32.const 6096
          i32.sub
          local.tee $l9
          global.set $g0
          local.get $p0
          i32.load offset=4
          local.set $l14
          local.get $l9
          local.get $p0
          i32.store offset=6072
          local.get $l9
          local.get $l14
          i32.store offset=6068
          f32.const 0x1p+0 (;=1;)
          local.set $l47
          local.get $l9
          f32.const 0x1p+0 (;=1;)
          local.get $p0
          f32.load offset=8
          f32.div
          f32.store offset=6060
          local.get $l9
          f32.const 0x1p+0 (;=1;)
          local.get $p0
          f32.load offset=12
          f32.div
          f32.store offset=6056
          local.get $l9
          f32.const 0x1p+0 (;=1;)
          local.get $p0
          f32.load offset=16
          f32.div
          f32.store offset=6064
          local.get $l9
          i32.const 0
          i32.store offset=1948
          local.get $p2
          i32.load offset=32
          local.set $l16
          block $B6 (result i32)
            i32.const 0
            local.get $p2
            f32.load offset=4
            local.tee $l40
            f32.const 0x1p+0 (;=1;)
            f32.ne
            br_if $B6
            drop
            i32.const 0
            local.get $p2
            f32.load offset=8
            f32.const 0x1p+0 (;=1;)
            f32.ne
            br_if $B6
            drop
            local.get $p2
            f32.load offset=12
            f32.const 0x1p+0 (;=1;)
            f32.eq
          end
          local.set $l19
          local.get $l16
          i32.const 16
          i32.add
          local.set $p0
          local.get $l9
          i32.const 1936
          i32.add
          i64.const 4575657221408423936
          i64.store
          local.get $l9
          i32.const 1928
          i32.add
          i64.const 0
          i64.store
          local.get $l9
          i32.const 1920
          i32.add
          i64.const 4575657221408423936
          i64.store
          local.get $l9
          i32.const 1912
          i32.add
          i64.const 0
          i64.store
          local.get $l9
          i32.const 1904
          i32.add
          i64.const 4575657222473777152
          i64.store
          local.get $l9
          i32.const 1888
          i32.add
          i64.const 1065353216
          i64.store
          local.get $l9
          i32.const 0
          i32.store8 offset=1944
          local.get $l9
          i64.const 0
          i64.store offset=1896
          local.get $l9
          i64.const 0
          i64.store offset=1880
          local.get $l9
          i64.const 1065353216
          i64.store offset=1872
          f32.const 0x1p+0 (;=1;)
          local.set $l50
          f32.const 0x1p+0 (;=1;)
          local.set $l45
          local.get $l19
          i32.eqz
          if $I7
            local.get $l9
            i32.const 1872
            i32.add
            local.get $p2
            i32.const 4
            i32.add
            local.get $p2
            i32.const 16
            i32.add
            call $f70485
            local.get $l9
            f32.load offset=1904
            local.set $l47
            local.get $l9
            f32.load offset=1900
            local.set $l46
            local.get $l9
            f32.load offset=1896
            local.set $l48
            local.get $l9
            f32.load offset=1892
            local.set $l49
            local.get $l9
            f32.load offset=1888
            local.set $l50
            local.get $l9
            f32.load offset=1884
            local.set $l52
            local.get $l9
            f32.load offset=1880
            local.set $l44
            local.get $l9
            f32.load offset=1876
            local.set $l43
            local.get $l9
            f32.load offset=1872
            local.set $l45
            local.get $p2
            f32.load offset=4
            local.set $l40
          end
          local.get $l16
          f32.load offset=44
          local.set $p5
          local.get $p3
          f32.load offset=20
          local.set $l53
          local.get $p3
          f32.load offset=24
          local.set $l55
          local.get $l16
          f32.load offset=48
          local.set $l39
          local.get $l16
          f32.load offset=40
          local.set $l42
          local.get $p3
          i64.load align=4
          local.set $l89
          local.get $p3
          i64.load offset=8 align=4
          local.set $l90
          local.get $p3
          f32.load offset=16
          local.set $l56
          local.get $l9
          i32.const 1868
          i32.add
          i32.const 0
          i32.store
          local.get $l9
          i32.const 1864
          i32.add
          local.get $l55
          f32.store
          local.get $l9
          i32.const 1860
          i32.add
          local.get $l53
          f32.store
          local.get $l9
          local.get $l56
          f32.store offset=1856
          local.get $l9
          local.get $l90
          i64.store offset=1848
          local.get $l9
          local.get $l89
          i64.store offset=1840
          local.get $p2
          f32.load offset=8
          local.set $l41
          local.get $p2
          f32.load offset=12
          local.set $p8
          local.get $l9
          i32.const 0
          i32.store offset=1836
          local.get $l9
          local.get $p8
          f32.store offset=1832
          local.get $l9
          local.get $l41
          f32.store offset=1828
          local.get $l9
          local.get $l40
          f32.store offset=1824
          local.get $p2
          i64.load offset=16 align=4
          local.set $l89
          local.get $l9
          local.get $p2
          i64.load offset=24 align=4
          i64.store offset=1816
          local.get $l9
          local.get $l89
          i64.store offset=1808
          local.get $l9
          i32.const 1680
          i32.add
          i32.const 0
          i32.store8
          local.get $l9
          i32.const 1672
          i32.add
          local.tee $l14
          i64.const 0
          i64.store
          local.get $l9
          i32.const 1664
          i32.add
          local.tee $l18
          i64.const 0
          i64.store
          local.get $l9
          i64.const 0
          i64.store offset=1656
          local.get $l9
          i64.const 0
          i64.store offset=1648
          local.get $l9
          local.get $p0
          i32.store offset=1792
          local.get $l9
          local.get $l16
          i32.load offset=56
          local.get $l16
          i32.load8_u offset=55
          i32.const 20
          i32.mul
          i32.add
          i32.store offset=1800
          local.get $l9
          local.get $l16
          i32.load8_u offset=54
          i32.store8 offset=1804
          local.get $l14
          local.get $l40
          local.get $l16
          i32.const 68
          i32.add
          local.tee $p0
          f32.load
          f32.mul
          local.tee $l40
          local.get $l41
          local.get $l16
          f32.load offset=72
          f32.mul
          local.tee $l41
          local.get $l40
          local.get $l41
          f32.le
          select
          local.tee $l40
          local.get $p8
          local.get $l16
          i32.const 76
          i32.add
          local.tee $l21
          f32.load
          f32.mul
          local.tee $l41
          local.get $l40
          local.get $l41
          f32.le
          select
          local.tee $l40
          f32.const 0x1.99999ap-6 (;=0.025;)
          f32.mul
          f32.store
          local.get $l18
          local.get $l40
          f32.const 0x1.99999ap-4 (;=0.1;)
          f32.mul
          f32.store
          local.get $l9
          local.get $l40
          f32.const 0x1.99999ap-5 (;=0.05;)
          f32.mul
          f32.store offset=1668
          local.get $l9
          i32.const 1824
          i32.add
          local.get $l9
          i32.const 1808
          i32.add
          local.get $l9
          i32.const 1696
          i32.add
          local.tee $l28
          local.get $l9
          i32.const 1744
          i32.add
          local.tee $l30
          local.get $l9
          i32.const 1648
          i32.add
          local.get $l19
          call $f70494
          local.get $l9
          local.get $l16
          i32.load offset=60
          i32.store offset=1796
          local.get $l9
          local.get $p0
          f32.load
          local.get $l9
          f32.load offset=1824
          f32.mul
          local.tee $l40
          local.get $l16
          f32.load offset=72
          local.get $l9
          f32.load offset=1828
          f32.mul
          local.tee $l41
          local.get $l40
          local.get $l41
          f32.le
          select
          local.tee $l40
          local.get $l21
          f32.load
          local.get $l9
          f32.load offset=1832
          f32.mul
          local.tee $l41
          local.get $l40
          local.get $l41
          f32.le
          select
          f32.const 0x1p-2 (;=0.25;)
          f32.mul
          local.get $l54
          f32.add
          local.tee $l65
          f32.store offset=1568
          local.get $l9
          i32.const 0
          i32.store offset=1560
          local.get $l9
          i64.const 0
          i64.store offset=1552
          local.get $l9
          i32.const 1552
          i32.add
          i32.const 128
          call $f70632
          local.get $l9
          i32.const 1648
          i32.add
          local.get $l19
          local.get $l9
          i32.const 1480
          i32.add
          call $f70029
          local.get $l9
          local.get $p3
          f32.load
          f32.store offset=1432
          local.get $l9
          local.get $p3
          f32.load offset=4
          f32.store offset=1436
          local.get $l9
          local.get $p3
          f32.load offset=8
          f32.store offset=1440
          local.get $l9
          local.get $p3
          f32.load offset=12
          f32.store offset=1444
          i32.const 3125832
          i32.const 3125860
          local.get $l19
          select
          local.set $l31
          local.get $l42
          local.get $l44
          f32.mul
          local.get $p5
          local.get $l49
          f32.mul
          f32.add
          local.get $l39
          local.get $l47
          f32.mul
          f32.add
          local.set $l81
          local.get $l42
          local.get $l43
          f32.mul
          local.get $p5
          local.get $l50
          f32.mul
          f32.add
          local.get $l39
          local.get $l46
          f32.mul
          f32.add
          local.set $l82
          local.get $l42
          local.get $l45
          f32.mul
          local.get $p5
          local.get $l52
          f32.mul
          f32.add
          local.get $l39
          local.get $l48
          f32.mul
          f32.add
          local.set $l83
          local.get $p1
          f32.load offset=4
          local.tee $l39
          local.get $l39
          f32.add
          local.tee $l40
          local.get $p1
          f32.load offset=8
          local.tee $p5
          f32.mul
          local.tee $l47
          local.get $p1
          f32.load
          local.tee $l41
          local.get $l41
          f32.add
          local.tee $l42
          local.get $p1
          f32.load offset=12
          local.tee $p8
          f32.mul
          local.tee $l46
          f32.sub
          local.set $l66
          local.get $l42
          local.get $p5
          f32.mul
          local.tee $l48
          local.get $l40
          local.get $p8
          f32.mul
          local.tee $l49
          f32.add
          local.set $l67
          local.get $l47
          local.get $l46
          f32.add
          local.set $l68
          local.get $l42
          local.get $l39
          f32.mul
          local.tee $l47
          local.get $p5
          local.get $p5
          f32.add
          local.tee $l46
          local.get $p8
          f32.mul
          local.tee $p8
          f32.sub
          local.set $l69
          local.get $l48
          local.get $l49
          f32.sub
          local.set $l70
          local.get $l47
          local.get $p8
          f32.add
          local.set $l71
          f32.const 0x1p+0 (;=1;)
          local.get $l41
          local.get $l42
          f32.mul
          f32.sub
          local.tee $l42
          local.get $l39
          local.get $l40
          f32.mul
          local.tee $l39
          f32.sub
          local.set $l72
          local.get $l42
          local.get $p5
          local.get $l46
          f32.mul
          local.tee $p5
          f32.sub
          local.set $l73
          f32.const 0x1p+0 (;=1;)
          local.get $l39
          f32.sub
          local.get $p5
          f32.sub
          local.set $l74
          local.get $p1
          f32.load offset=24
          local.set $l75
          local.get $p1
          f32.load offset=20
          local.set $l76
          local.get $p1
          f32.load offset=16
          local.set $l77
          i32.const 268435455
          local.set $l11
          f32.const 0x0p+0 (;=0;)
          local.set $l47
          f32.const 0x0p+0 (;=0;)
          local.set $l46
          f32.const 0x0p+0 (;=0;)
          local.set $l48
          f32.const 0x0p+0 (;=0;)
          local.set $l49
          f32.const 0x0p+0 (;=0;)
          local.set $l50
          f32.const 0x0p+0 (;=0;)
          local.set $l52
          block $B8 (result i32)
            block $B9
              loop $L10
                block $B11
                  local.get $l9
                  local.get $l55
                  f32.store offset=1456
                  local.get $l9
                  local.get $l53
                  f32.store offset=1452
                  local.get $l9
                  local.get $l56
                  f32.store offset=1448
                  local.get $l9
                  i32.const 0
                  i32.store offset=1556
                  local.get $l9
                  i32.const 0
                  i32.store offset=1868
                  local.get $l9
                  local.get $l55
                  f32.store offset=1864
                  local.get $l9
                  local.get $l53
                  f32.store offset=1860
                  local.get $l9
                  local.get $l56
                  f32.store offset=1856
                  local.get $l9
                  local.get $l19
                  i32.store8 offset=1628
                  local.get $l9
                  local.get $l30
                  i32.store offset=1624
                  local.get $l9
                  local.get $l28
                  i32.store offset=1620
                  local.get $l9
                  local.get $l31
                  i32.store offset=1584
                  local.get $l9
                  i32.const 0
                  i32.store offset=1612
                  local.get $l9
                  local.get $l81
                  f32.store offset=1608
                  local.get $l9
                  local.get $l82
                  f32.store offset=1604
                  local.get $l9
                  local.get $l83
                  f32.store offset=1600
                  local.get $l9
                  local.get $l9
                  i32.const 1840
                  i32.add
                  i32.store offset=1616
                  local.get $l9
                  local.get $l9
                  i32.const 1648
                  i32.add
                  i32.store offset=1632
                  local.get $l9
                  i32.const 1368
                  i32.add
                  local.get $p2
                  local.get $l16
                  local.get $l9
                  i32.const 1432
                  i32.add
                  call $f69942
                  local.get $l9
                  local.get $l65
                  local.get $l9
                  f32.load offset=1420
                  f32.add
                  local.tee $p5
                  f32.store offset=1420
                  local.get $l9
                  f32.load offset=1388
                  local.set $l40
                  local.get $l9
                  local.get $l65
                  local.get $l9
                  f32.load offset=1416
                  f32.add
                  local.tee $l39
                  f32.store offset=1416
                  local.get $l9
                  f32.load offset=1376
                  local.set $l41
                  local.get $l9
                  local.get $l65
                  local.get $l9
                  f32.load offset=1424
                  f32.add
                  local.tee $l42
                  f32.store offset=1424
                  local.get $l9
                  local.get $l9
                  f32.load offset=1412
                  local.tee $p8
                  local.get $l39
                  local.get $l41
                  f32.mul
                  f32.abs
                  local.get $p5
                  local.get $l40
                  f32.mul
                  f32.abs
                  f32.add
                  local.get $l42
                  local.get $l9
                  f32.load offset=1400
                  f32.mul
                  f32.abs
                  f32.add
                  local.tee $l40
                  f32.add
                  f32.store offset=1364
                  local.get $l9
                  local.get $l9
                  f32.load offset=1408
                  local.tee $l41
                  local.get $l39
                  local.get $l9
                  f32.load offset=1372
                  f32.mul
                  f32.abs
                  local.get $p5
                  local.get $l9
                  f32.load offset=1384
                  f32.mul
                  f32.abs
                  f32.add
                  local.get $l42
                  local.get $l9
                  f32.load offset=1396
                  f32.mul
                  f32.abs
                  f32.add
                  local.tee $l44
                  f32.add
                  f32.store offset=1360
                  local.get $l9
                  local.get $l9
                  f32.load offset=1404
                  local.tee $l43
                  local.get $l39
                  local.get $l9
                  f32.load offset=1368
                  f32.mul
                  f32.abs
                  local.get $p5
                  local.get $l9
                  f32.load offset=1380
                  f32.mul
                  f32.abs
                  f32.add
                  local.get $l42
                  local.get $l9
                  f32.load offset=1392
                  f32.mul
                  f32.abs
                  f32.add
                  local.tee $p5
                  f32.add
                  f32.store offset=1356
                  local.get $l9
                  local.get $p8
                  local.get $l40
                  f32.sub
                  f32.store offset=1352
                  local.get $l9
                  local.get $l41
                  local.get $l44
                  f32.sub
                  f32.store offset=1348
                  local.get $l9
                  local.get $l43
                  local.get $p5
                  f32.sub
                  f32.store offset=1344
                  local.get $l9
                  i32.const 3124912
                  i32.store
                  local.get $l9
                  local.get $l9
                  i32.const 1552
                  i32.add
                  i32.store offset=4
                  local.get $l9
                  i32.const 6056
                  i32.add
                  local.get $p1
                  local.get $l9
                  i32.const 1344
                  i32.add
                  i32.const 1
                  local.get $l9
                  call $f70450
                  local.get $l9
                  i32.load offset=1556
                  local.tee $l15
                  i32.eqz
                  br_if $B11
                  local.get $l9
                  f32.load offset=1452
                  local.set $l57
                  local.get $l9
                  f32.load offset=1448
                  local.set $l58
                  local.get $l9
                  f32.load offset=1456
                  local.set $l54
                  local.get $l9
                  f32.load offset=1444
                  local.set $p5
                  local.get $l9
                  f32.load offset=1432
                  local.set $l39
                  local.get $l9
                  f32.load offset=1440
                  local.set $l42
                  local.get $l9
                  f32.load offset=1436
                  local.set $l40
                  i32.const 0
                  local.set $l22
                  local.get $l9
                  i32.const 0
                  i32.store offset=1340
                  local.get $l9
                  i32.const 0
                  i32.store offset=1324
                  local.get $l9
                  i32.const 0
                  i32.store offset=1308
                  local.get $l9
                  i32.const 0
                  i32.store offset=1292
                  local.get $l9
                  local.get $l72
                  local.get $l39
                  local.get $l39
                  f32.neg
                  local.get $l39
                  f32.sub
                  local.tee $l41
                  f32.mul
                  f32.const 0x1p+0 (;=1;)
                  f32.add
                  local.tee $l84
                  local.get $l40
                  f32.neg
                  local.tee $l51
                  local.get $l40
                  f32.sub
                  local.tee $l45
                  local.get $l51
                  f32.mul
                  local.tee $l85
                  f32.sub
                  local.tee $p8
                  f32.mul
                  local.get $l67
                  local.get $l41
                  local.get $l42
                  f32.neg
                  local.tee $l44
                  f32.mul
                  local.tee $l86
                  local.get $p5
                  local.get $l45
                  f32.mul
                  local.tee $l87
                  f32.sub
                  local.tee $l43
                  f32.mul
                  local.get $l66
                  local.get $p5
                  local.get $l41
                  f32.mul
                  local.tee $l78
                  local.get $l45
                  local.get $l44
                  f32.mul
                  local.tee $l88
                  f32.add
                  local.tee $l45
                  f32.mul
                  f32.add
                  f32.add
                  f32.store offset=1320
                  local.get $l9
                  local.get $l68
                  local.get $p8
                  f32.mul
                  local.get $l69
                  local.get $l43
                  f32.mul
                  local.get $l73
                  local.get $l45
                  f32.mul
                  f32.add
                  f32.add
                  f32.store offset=1304
                  local.get $l9
                  local.get $l70
                  local.get $p8
                  f32.mul
                  local.get $l74
                  local.get $l43
                  f32.mul
                  local.get $l71
                  local.get $l45
                  f32.mul
                  f32.add
                  f32.add
                  f32.store offset=1288
                  local.get $l9
                  local.get $l54
                  f32.const -0x1p+1 (;=-2;)
                  f32.mul
                  local.tee $l54
                  local.get $p5
                  local.get $p5
                  f32.mul
                  f32.const -0x1p-1 (;=-0.5;)
                  f32.add
                  local.tee $l79
                  f32.mul
                  local.get $p5
                  local.get $l39
                  local.get $l57
                  f32.const -0x1p+1 (;=-2;)
                  f32.mul
                  local.tee $l57
                  f32.mul
                  local.get $l40
                  local.get $l58
                  f32.const -0x1p+1 (;=-2;)
                  f32.mul
                  local.tee $l58
                  f32.mul
                  f32.sub
                  f32.mul
                  f32.sub
                  local.get $l42
                  local.get $l58
                  local.get $l39
                  f32.mul
                  local.get $l57
                  local.get $l40
                  f32.mul
                  f32.add
                  local.get $l54
                  local.get $l42
                  f32.mul
                  f32.add
                  local.tee $l80
                  f32.mul
                  f32.add
                  local.get $l75
                  local.get $p8
                  f32.mul
                  local.get $l77
                  local.get $l43
                  f32.mul
                  local.get $l76
                  local.get $l45
                  f32.mul
                  f32.add
                  f32.add
                  f32.add
                  f32.store offset=1336
                  local.get $l9
                  local.get $l72
                  local.get $l88
                  local.get $l78
                  f32.sub
                  local.tee $p8
                  f32.mul
                  local.get $l67
                  local.get $l41
                  local.get $l51
                  f32.mul
                  local.tee $l51
                  local.get $p5
                  local.get $l44
                  local.get $l42
                  f32.sub
                  local.tee $l43
                  f32.mul
                  local.tee $l78
                  f32.add
                  local.tee $l41
                  f32.mul
                  local.get $l66
                  local.get $l84
                  local.get $l43
                  local.get $l44
                  f32.mul
                  local.tee $l45
                  f32.sub
                  local.tee $l44
                  f32.mul
                  f32.add
                  f32.add
                  f32.store offset=1316
                  local.get $l9
                  local.get $l72
                  local.get $l86
                  local.get $l87
                  f32.add
                  local.tee $l43
                  f32.mul
                  local.get $l67
                  f32.const 0x1p+0 (;=1;)
                  local.get $l85
                  f32.sub
                  local.get $l45
                  f32.sub
                  local.tee $l45
                  f32.mul
                  local.get $l66
                  local.get $l51
                  local.get $l78
                  f32.sub
                  local.tee $l51
                  f32.mul
                  f32.add
                  f32.add
                  f32.store offset=1312
                  local.get $l9
                  local.get $l68
                  local.get $p8
                  f32.mul
                  local.get $l69
                  local.get $l41
                  f32.mul
                  local.get $l73
                  local.get $l44
                  f32.mul
                  f32.add
                  f32.add
                  f32.store offset=1300
                  local.get $l9
                  local.get $l68
                  local.get $l43
                  f32.mul
                  local.get $l69
                  local.get $l45
                  f32.mul
                  local.get $l73
                  local.get $l51
                  f32.mul
                  f32.add
                  f32.add
                  f32.store offset=1296
                  local.get $l9
                  local.get $l70
                  local.get $p8
                  f32.mul
                  local.get $l74
                  local.get $l41
                  f32.mul
                  local.get $l71
                  local.get $l44
                  f32.mul
                  f32.add
                  f32.add
                  f32.store offset=1284
                  local.get $l9
                  local.get $l70
                  local.get $l43
                  f32.mul
                  local.get $l74
                  local.get $l45
                  f32.mul
                  local.get $l71
                  local.get $l51
                  f32.mul
                  f32.add
                  f32.add
                  f32.store offset=1280
                  local.get $l9
                  local.get $l40
                  local.get $l80
                  f32.mul
                  local.get $l57
                  local.get $l79
                  f32.mul
                  local.get $p5
                  local.get $l58
                  local.get $l42
                  f32.mul
                  local.get $l54
                  local.get $l39
                  f32.mul
                  f32.sub
                  f32.mul
                  f32.sub
                  f32.add
                  local.get $l75
                  local.get $p8
                  f32.mul
                  local.get $l77
                  local.get $l41
                  f32.mul
                  local.get $l76
                  local.get $l44
                  f32.mul
                  f32.add
                  f32.add
                  f32.add
                  f32.store offset=1332
                  local.get $l9
                  local.get $l39
                  local.get $l80
                  f32.mul
                  local.get $l58
                  local.get $l79
                  f32.mul
                  local.get $p5
                  local.get $l54
                  local.get $l40
                  f32.mul
                  local.get $l57
                  local.get $l42
                  f32.mul
                  f32.sub
                  f32.mul
                  f32.sub
                  f32.add
                  local.get $l75
                  local.get $l43
                  f32.mul
                  local.get $l77
                  local.get $l45
                  f32.mul
                  local.get $l76
                  local.get $l51
                  f32.mul
                  f32.add
                  f32.add
                  f32.add
                  f32.store offset=1328
                  local.get $l15
                  i32.const 31
                  i32.add
                  i32.const 5
                  i32.shr_u
                  local.tee $l32
                  i32.eqz
                  br_if $B11
                  f32.const 0x1.fffffep+127 (;=3.40282e+38;)
                  local.set $p8
                  local.get $l15
                  local.set $l13
                  i32.const 0
                  local.set $l23
                  loop $L12
                    block $B13
                      local.get $l15
                      local.get $l22
                      i32.const 5
                      i32.shl
                      local.tee $l26
                      i32.sub
                      local.tee $p3
                      i32.const 32
                      local.get $p3
                      i32.const 32
                      i32.lt_u
                      select
                      local.tee $l27
                      if $I14
                        local.get $l13
                        i32.const 32
                        local.get $l13
                        i32.const 32
                        i32.lt_u
                        select
                        local.set $l14
                        i32.const 0
                        local.set $p3
                        loop $L15
                          local.get $l9
                          i32.const 6056
                          i32.add
                          local.get $p1
                          local.get $l9
                          local.get $p3
                          i32.const 40
                          i32.mul
                          i32.add
                          local.tee $p0
                          i32.const 0
                          i32.const 0
                          local.get $l9
                          i32.load offset=1552
                          local.get $p3
                          local.get $l26
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
                          local.get $p3
                          i32.const 1
                          i32.add
                          local.tee $p3
                          local.get $l14
                          i32.ne
                          br_if $L15
                        end
                        local.get $l9
                        i32.const 6088
                        i32.add
                        local.get $l9
                        i32.const 1472
                        i32.add
                        i32.load
                        i32.store
                        local.get $l9
                        local.get $l9
                        i64.load offset=1464 align=4
                        i64.store offset=6080
                        i32.const 0
                        local.set $l14
                        local.get $l27
                        i32.eqz
                        br_if $B13
                        i32.const 0
                        local.set $l20
                        loop $L16
                          local.get $l9
                          i32.const 0
                          i32.store offset=1948
                          local.get $l9
                          i32.const 1480
                          i32.add
                          local.get $l9
                          i32.const 1584
                          i32.add
                          local.get $l9
                          local.get $l20
                          i32.const 40
                          i32.mul
                          i32.add
                          local.tee $p3
                          local.get $l20
                          local.get $l26
                          i32.add
                          local.tee $l17
                          local.get $p3
                          i32.load8_u offset=36
                          local.get $l9
                          i32.const 1568
                          i32.add
                          local.get $l29
                          local.get $l9
                          i32.const 1840
                          i32.add
                          local.get $l9
                          i32.const 1280
                          i32.add
                          local.get $l9
                          i32.const 1952
                          i32.add
                          local.get $l9
                          i32.const 1948
                          i32.add
                          call $f70063
                          block $B17
                            local.get $l9
                            i32.load offset=1948
                            local.tee $p3
                            i32.eqz
                            br_if $B17
                            i32.const 0
                            local.set $p0
                            local.get $l9
                            f32.load offset=1996
                            local.set $p5
                            block $B18
                              local.get $p3
                              i32.const 1
                              i32.eq
                              br_if $B18
                              local.get $p3
                              i32.const 1
                              i32.sub
                              local.tee $p0
                              i32.const 3
                              i32.and
                              local.set $l14
                              block $B19
                                local.get $p3
                                i32.const 2
                                i32.sub
                                i32.const 3
                                i32.lt_u
                                if $I20
                                  i32.const 0
                                  local.set $p0
                                  i32.const 1
                                  local.set $p3
                                  br $B19
                                end
                                local.get $p0
                                i32.const -4
                                i32.and
                                local.set $l18
                                i32.const 0
                                local.set $p0
                                i32.const 1
                                local.set $p3
                                loop $L21
                                  local.get $p3
                                  i32.const 3
                                  i32.add
                                  local.tee $l21
                                  i32.const 6
                                  i32.shl
                                  local.get $l9
                                  i32.add
                                  i32.const 1996
                                  i32.add
                                  f32.load
                                  local.tee $l39
                                  local.get $p3
                                  i32.const 2
                                  i32.add
                                  local.tee $l33
                                  i32.const 6
                                  i32.shl
                                  local.get $l9
                                  i32.add
                                  i32.const 1996
                                  i32.add
                                  f32.load
                                  local.tee $l42
                                  local.get $p3
                                  i32.const 1
                                  i32.add
                                  local.tee $l34
                                  i32.const 6
                                  i32.shl
                                  local.get $l9
                                  i32.add
                                  i32.const 1996
                                  i32.add
                                  f32.load
                                  local.tee $l40
                                  local.get $p3
                                  i32.const 6
                                  i32.shl
                                  local.get $l9
                                  i32.add
                                  i32.const 1996
                                  i32.add
                                  f32.load
                                  local.tee $l41
                                  local.get $p5
                                  local.get $p5
                                  local.get $l41
                                  f32.gt
                                  local.tee $l35
                                  select
                                  local.tee $p5
                                  local.get $p5
                                  local.get $l40
                                  f32.gt
                                  local.tee $l36
                                  select
                                  local.tee $p5
                                  local.get $p5
                                  local.get $l42
                                  f32.gt
                                  local.tee $l37
                                  select
                                  local.tee $p5
                                  local.get $p5
                                  local.get $l39
                                  f32.gt
                                  local.tee $l38
                                  select
                                  local.set $p5
                                  local.get $l21
                                  local.get $l33
                                  local.get $l34
                                  local.get $p3
                                  local.get $p0
                                  local.get $l35
                                  select
                                  local.get $l36
                                  select
                                  local.get $l37
                                  select
                                  local.get $l38
                                  select
                                  local.set $p0
                                  local.get $p3
                                  i32.const 4
                                  i32.add
                                  local.set $p3
                                  local.get $l18
                                  i32.const 4
                                  i32.sub
                                  local.tee $l18
                                  br_if $L21
                                end
                              end
                              local.get $l14
                              i32.eqz
                              br_if $B18
                              loop $L22
                                local.get $p3
                                i32.const 6
                                i32.shl
                                local.get $l9
                                i32.add
                                i32.const 1996
                                i32.add
                                f32.load
                                local.tee $l39
                                local.get $p5
                                local.get $p5
                                local.get $l39
                                f32.gt
                                local.tee $l18
                                select
                                local.set $p5
                                local.get $p3
                                local.get $p0
                                local.get $l18
                                select
                                local.set $p0
                                local.get $p3
                                i32.const 1
                                i32.add
                                local.set $p3
                                local.get $l14
                                i32.const 1
                                i32.sub
                                local.tee $l14
                                br_if $L22
                              end
                            end
                            i32.const 1
                            local.set $l14
                            local.get $p5
                            local.get $p8
                            f32.lt
                            i32.eqz
                            br_if $B17
                            local.get $l9
                            i32.const 1952
                            i32.add
                            local.get $p0
                            i32.const 6
                            i32.shl
                            i32.add
                            local.tee $p3
                            f32.load offset=16
                            local.set $l48
                            local.get $p3
                            f32.load offset=32
                            local.set $l52
                            local.get $p3
                            f32.load offset=24
                            local.set $l47
                            local.get $p3
                            f32.load offset=20
                            local.set $l46
                            local.get $p3
                            f32.load offset=40
                            local.set $l49
                            local.get $p3
                            f32.load offset=36
                            local.set $l50
                            local.get $l17
                            local.set $l11
                            local.get $p5
                            local.set $p8
                          end
                          local.get $l20
                          i32.const 1
                          i32.add
                          local.tee $l20
                          local.get $l27
                          i32.ne
                          br_if $L16
                        end
                        local.get $l14
                        local.get $l23
                        i32.or
                        local.set $l23
                        br $B13
                      end
                      local.get $l9
                      i32.const 6088
                      i32.add
                      local.get $l9
                      i32.const 1472
                      i32.add
                      i32.load
                      i32.store
                      local.get $l9
                      local.get $l9
                      i64.load offset=1464 align=4
                      i64.store offset=6080
                    end
                    local.get $l9
                    i32.const 1472
                    i32.add
                    local.get $l9
                    i32.const 6088
                    i32.add
                    i32.load
                    i32.store
                    local.get $l9
                    local.get $l9
                    i64.load offset=6080
                    i64.store offset=1464
                    local.get $l13
                    i32.const 32
                    i32.sub
                    local.set $l13
                    local.get $l22
                    i32.const 1
                    i32.add
                    local.tee $l22
                    local.get $l32
                    i32.ne
                    br_if $L12
                  end
                  local.get $l23
                  i32.const 1
                  i32.and
                  i32.eqz
                  br_if $B11
                  local.get $l9
                  f32.load offset=1864
                  local.get $l9
                  f32.load offset=1848
                  local.tee $p5
                  local.get $l48
                  local.get $l9
                  f32.load offset=1840
                  local.tee $l39
                  f32.mul
                  local.get $l46
                  local.get $l9
                  f32.load offset=1844
                  local.tee $l42
                  f32.mul
                  f32.add
                  local.get $l47
                  local.get $p5
                  f32.mul
                  f32.add
                  local.tee $l44
                  f32.mul
                  local.get $l9
                  f32.load offset=1852
                  local.tee $l40
                  local.get $l46
                  local.get $l39
                  f32.mul
                  local.get $l48
                  local.get $l42
                  f32.mul
                  f32.sub
                  f32.mul
                  local.get $l47
                  local.get $l40
                  local.get $l40
                  f32.mul
                  f32.const -0x1p-1 (;=-0.5;)
                  f32.add
                  local.tee $l41
                  f32.mul
                  f32.add
                  f32.add
                  local.tee $l43
                  local.get $l43
                  f32.add
                  f32.add
                  local.set $l62
                  local.get $l9
                  f32.load offset=1860
                  local.get $l42
                  local.get $l44
                  f32.mul
                  local.get $l40
                  local.get $l48
                  local.get $p5
                  f32.mul
                  local.get $l47
                  local.get $l39
                  f32.mul
                  f32.sub
                  f32.mul
                  local.get $l46
                  local.get $l41
                  f32.mul
                  f32.add
                  f32.add
                  local.tee $l43
                  local.get $l43
                  f32.add
                  f32.add
                  local.set $l63
                  local.get $l9
                  f32.load offset=1856
                  local.get $l39
                  local.get $l44
                  f32.mul
                  local.get $l40
                  local.get $l47
                  local.get $l42
                  f32.mul
                  local.get $l46
                  local.get $p5
                  f32.mul
                  f32.sub
                  f32.mul
                  local.get $l48
                  local.get $l41
                  f32.mul
                  f32.add
                  f32.add
                  local.tee $l44
                  local.get $l44
                  f32.add
                  f32.add
                  local.set $l64
                  local.get $p5
                  local.get $l52
                  local.get $l39
                  f32.mul
                  local.get $l50
                  local.get $l42
                  f32.mul
                  f32.add
                  local.get $l49
                  local.get $p5
                  f32.mul
                  f32.add
                  local.tee $l44
                  f32.mul
                  local.get $l40
                  local.get $l50
                  local.get $l39
                  f32.mul
                  local.get $l52
                  local.get $l42
                  f32.mul
                  f32.sub
                  f32.mul
                  local.get $l49
                  local.get $l41
                  f32.mul
                  f32.add
                  f32.add
                  local.tee $l43
                  local.get $l43
                  f32.add
                  local.set $l45
                  local.get $l42
                  local.get $l44
                  f32.mul
                  local.get $l40
                  local.get $l52
                  local.get $p5
                  f32.mul
                  local.get $l49
                  local.get $l39
                  f32.mul
                  f32.sub
                  f32.mul
                  local.get $l50
                  local.get $l41
                  f32.mul
                  f32.add
                  f32.add
                  local.tee $l43
                  local.get $l43
                  f32.add
                  local.set $l43
                  local.get $l39
                  local.get $l44
                  f32.mul
                  local.get $l40
                  local.get $l49
                  local.get $l42
                  f32.mul
                  local.get $l50
                  local.get $p5
                  f32.mul
                  f32.sub
                  f32.mul
                  local.get $l52
                  local.get $l41
                  f32.mul
                  f32.add
                  f32.add
                  local.tee $p5
                  local.get $p5
                  f32.add
                  local.set $p5
                  local.get $l9
                  i32.load offset=1552
                  local.get $l11
                  i32.const 2
                  i32.shl
                  i32.add
                  i32.load
                  local.set $l11
                  local.get $p8
                  f32.const 0x0p+0 (;=0;)
                  f32.le
                  i32.eqz
                  if $I23
                    i32.const 1
                    local.set $l24
                    local.get $l25
                    br_if $B11
                    local.get $p6
                    local.get $l45
                    f32.store offset=36
                    local.get $p6
                    local.get $l43
                    f32.store offset=32
                    local.get $p6
                    local.get $p5
                    f32.store offset=28
                    local.get $p6
                    local.get $l62
                    f32.store offset=24
                    local.get $p6
                    local.get $l63
                    f32.store offset=20
                    local.get $p6
                    local.get $l64
                    f32.store offset=16
                    local.get $p6
                    i32.const 0
                    i32.store offset=40
                    local.get $p6
                    local.get $l11
                    i32.store offset=8
                    br $B9
                  end
                  local.get $l55
                  local.get $p8
                  local.get $l45
                  f32.mul
                  local.tee $l39
                  f32.sub
                  local.set $l55
                  local.get $l53
                  local.get $p8
                  local.get $l43
                  f32.mul
                  local.tee $l42
                  f32.sub
                  local.set $l53
                  local.get $l56
                  local.get $p8
                  local.get $p5
                  f32.mul
                  local.tee $p5
                  f32.sub
                  local.set $l56
                  local.get $l59
                  local.get $l39
                  f32.sub
                  local.set $l59
                  local.get $l60
                  local.get $l42
                  f32.sub
                  local.set $l60
                  local.get $l61
                  local.get $p5
                  f32.sub
                  local.set $l61
                  i32.const 1
                  local.set $l24
                  local.get $l25
                  i32.const 1
                  i32.add
                  local.tee $l25
                  i32.const 2
                  i32.ne
                  br_if $L10
                end
              end
              i32.const 0
              local.get $l24
              i32.eqz
              br_if $B8
              drop
              local.get $p6
              local.get $l62
              f32.store offset=24
              local.get $p6
              local.get $l63
              f32.store offset=20
              local.get $p6
              local.get $l64
              f32.store offset=16
              local.get $p6
              local.get $l11
              i32.store offset=8
              local.get $p6
              local.get $l59
              local.get $l59
              f32.mul
              local.get $l60
              local.get $l60
              f32.mul
              local.get $l61
              local.get $l61
              f32.mul
              f32.add
              f32.add
              f32.sqrt
              local.tee $p5
              f32.neg
              f32.store offset=40
              local.get $p6
              local.get $l59
              f32.const 0x1p+0 (;=1;)
              local.get $p5
              f32.div
              local.tee $l39
              f32.mul
              f32.const 0x0p+0 (;=0;)
              local.get $p5
              f32.const 0x0p+0 (;=0;)
              f32.gt
              local.tee $p3
              select
              f32.store offset=36
              local.get $p6
              local.get $l60
              local.get $l39
              f32.mul
              f32.const 0x0p+0 (;=0;)
              local.get $p3
              select
              f32.store offset=32
              local.get $p6
              local.get $l61
              local.get $l39
              f32.mul
              f32.const 0x0p+0 (;=0;)
              local.get $p3
              select
              f32.store offset=28
            end
            i32.const 1
          end
          local.set $p3
          block $B24
            local.get $l9
            i32.load offset=1560
            local.tee $p0
            i32.const 0
            i32.lt_s
            br_if $B24
            local.get $p0
            i32.const 2147483647
            i32.and
            i32.eqz
            br_if $B24
            local.get $l9
            i32.load offset=1552
            local.tee $p0
            i32.eqz
            br_if $B24
            call $f69753
            local.tee $l14
            local.get $p0
            local.get $l14
            i32.load
            i32.load offset=12
            call_indirect $__indirect_function_table (type $t1)
          end
          local.get $l9
          i32.const 6096
          i32.add
          global.set $g0
          local.get $p3
          local.set $p0
          local.get $l12
          i32.load offset=280
          local.set $l12
          local.get $p6
          i32.const 1026
          i32.store16 offset=12
          local.get $p6
          local.get $l12
          i32.store offset=8
          local.get $p0
          i32.eqz
          if $I25
            local.get $p6
            i32.const 0
            i32.store offset=40
            local.get $p4
            f32.load
            local.set $p8
            local.get $p4
            f32.load offset=4
            local.set $l55
            local.get $p6
            local.get $p4
            f32.load offset=8
            f32.neg
            f32.store offset=36
            local.get $p6
            local.get $l55
            f32.neg
            f32.store offset=32
            local.get $p6
            local.get $p8
            f32.neg
            f32.store offset=28
            br $B3
          end
          local.get $p6
          i32.const 1027
          i32.store16 offset=12
          br $B3
        end
        local.get $l12
        i32.load offset=280
        local.set $l12
        local.get $p6
        i32.const 1026
        i32.store16 offset=12
        local.get $p6
        local.get $l12
        i32.store offset=8
        local.get $p4
        f32.load
        local.set $p8
        local.get $p4
        f32.load offset=4
        local.set $l55
        local.get $p4
        f32.load offset=8
        local.set $l56
        local.get $p6
        i32.const 0
        i32.store offset=40
        local.get $p6
        local.get $l56
        f32.neg
        f32.store offset=36
        local.get $p6
        local.get $l55
        f32.neg
        f32.store offset=32
        local.get $p6
        local.get $p8
        f32.neg
        f32.store offset=28
        br $B3
      end
      local.get $p6
      local.get $l12
      i64.load offset=272 align=4
      i64.store align=4
      local.get $p6
      local.get $l12
      i32.load offset=280
      i32.store offset=8
      local.get $p6
      local.get $l12
      i32.load16_u offset=284
      i32.store16 offset=12
      local.get $p6
      local.get $l12
      f32.load offset=288
      f32.store offset=16
      local.get $p6
      local.get $l12
      f32.load offset=292
      f32.store offset=20
      local.get $p6
      local.get $l12
      f32.load offset=296
      f32.store offset=24
      local.get $p6
      local.get $l12
      f32.load offset=300
      local.tee $p8
      f32.store offset=28
      local.get $p6
      i32.const 32
      i32.add
      local.tee $p4
      local.get $l12
      f32.load offset=304
      local.tee $l55
      f32.store
      local.get $p6
      i32.const 36
      i32.add
      local.tee $p0
      local.get $l12
      f32.load offset=308
      local.tee $l56
      f32.store
      local.get $p6
      local.get $l12
      f32.load offset=312
      f32.store offset=40
      local.get $l12
      i32.load offset=316
      local.set $l12
      local.get $p0
      local.get $l56
      f32.neg
      local.tee $l42
      f32.store
      local.get $p4
      local.get $l55
      f32.neg
      local.tee $l54
      f32.store
      local.get $p6
      local.get $p8
      f32.neg
      local.tee $p5
      f32.store offset=28
      local.get $p6
      local.get $l12
      i32.store offset=44
      local.get $p8
      local.get $p8
      f32.mul
      local.get $l55
      local.get $l55
      f32.mul
      f32.add
      local.get $l56
      local.get $l56
      f32.mul
      f32.add
      f32.sqrt
      local.tee $p8
      f32.const 0x0p+0 (;=0;)
      f32.gt
      i32.eqz
      br_if $B3
      local.get $p6
      f32.const 0x1p+0 (;=1;)
      local.get $p8
      f32.div
      local.tee $p8
      local.get $l42
      f32.mul
      f32.store offset=36
      local.get $p6
      local.get $p8
      local.get $l54
      f32.mul
      f32.store offset=32
      local.get $p6
      local.get $p8
      local.get $p5
      f32.mul
      f32.store offset=28
    end
    local.get $l10
    i32.const 624
    i32.add
    global.set $g0
    local.get $p7
    i32.const 0
    i32.ne)
