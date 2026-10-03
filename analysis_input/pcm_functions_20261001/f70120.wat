  (func $f70120 (type $t130) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 f32) (param $p6 i32) (param $p7 i32) (param $p8 f32) (result i32)
    (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 i32) (local $l17 i32) (local $l18 i32) (local $l19 i32) (local $l20 i32) (local $l21 i32) (local $l22 i32) (local $l23 i32) (local $l24 i32) (local $l25 i32) (local $l26 i32) (local $l27 i32) (local $l28 i32) (local $l29 i32) (local $l30 i32) (local $l31 i32) (local $l32 i32) (local $l33 i32) (local $l34 i32) (local $l35 i32) (local $l36 i32) (local $l37 i32) (local $l38 i32) (local $l39 i32) (local $l40 i32) (local $l41 i32) (local $l42 i32) (local $l43 f32) (local $l44 f32) (local $l45 f32) (local $l46 f32) (local $l47 f32) (local $l48 f32) (local $l49 f32) (local $l50 f32) (local $l51 f32) (local $l52 f32) (local $l53 f32) (local $l54 f32) (local $l55 f32) (local $l56 f32) (local $l57 f32) (local $l58 f32) (local $l59 f32) (local $l60 f32) (local $l61 f32) (local $l62 f32) (local $l63 f32) (local $l64 f32) (local $l65 f32) (local $l66 f32) (local $l67 f32) (local $l68 f32) (local $l69 f32) (local $l70 f32) (local $l71 f32) (local $l72 f32) (local $l73 f32) (local $l74 f32) (local $l75 f32) (local $l76 f32) (local $l77 f32) (local $l78 f32) (local $l79 f32) (local $l80 f32) (local $l81 f32) (local $l82 f32) (local $l83 f32) (local $l84 f32) (local $l85 f32) (local $l86 f32) (local $l87 f32) (local $l88 f32) (local $l89 f32) (local $l90 f32) (local $l91 f32) (local $l92 f32) (local $l93 i64) (local $l94 i64)
    global.get $g0
    i32.const 784
    i32.sub
    local.tee $l10
    global.set $g0
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
    local.set $l16
    block $B1
      local.get $p0
      f32.load offset=4
      f32.const 0x1p+0 (;=1;)
      f32.ne
      br_if $B1
      local.get $p0
      f32.load offset=8
      f32.const 0x1p+0 (;=1;)
      f32.ne
      br_if $B1
      local.get $p0
      f32.load offset=12
      f32.const 0x1p+0 (;=1;)
      f32.eq
      local.set $l18
    end
    local.get $p2
    i32.const 4
    i32.add
    local.set $l32
    local.get $p0
    i32.load offset=36
    local.set $l29
    local.get $p2
    i32.load offset=32
    local.set $l19
    local.get $l10
    i64.const 4575657221408423936
    i64.store offset=768
    local.get $l10
    i64.const 0
    i64.store offset=760
    local.get $l10
    i64.const 4575657221408423936
    i64.store offset=752
    local.get $l10
    i64.const 0
    i64.store offset=744
    local.get $l10
    i64.const 4575657222473777152
    i64.store offset=736
    local.get $l10
    i64.const 1065353216
    i64.store offset=720
    local.get $l10
    i32.const 0
    i32.store8 offset=776
    local.get $l10
    i64.const 0
    i64.store offset=728
    local.get $l10
    i64.const 0
    i64.store offset=712
    local.get $l10
    i64.const 1065353216
    i64.store offset=704
    local.get $l16
    i32.eqz
    if $I2
      local.get $l10
      i32.const 704
      i32.add
      local.get $l32
      local.get $p2
      i32.const 16
      i32.add
      call $f70485
    end
    local.get $l10
    i64.const 4575657221408423936
    i64.store offset=688
    local.get $l10
    i64.const 0
    i64.store offset=680
    local.get $l10
    i64.const 4575657221408423936
    i64.store offset=672
    local.get $l10
    i64.const 0
    i64.store offset=664
    local.get $l10
    i64.const 4575657222473777152
    i64.store offset=656
    local.get $l10
    i64.const 1065353216
    i64.store offset=640
    local.get $l10
    i32.const 0
    i32.store8 offset=696
    local.get $l10
    i64.const 0
    i64.store offset=648
    local.get $l10
    i64.const 0
    i64.store offset=632
    local.get $l10
    i64.const 1065353216
    i64.store offset=624
    local.get $l18
    i32.eqz
    if $I3
      local.get $l10
      i32.const 624
      i32.add
      local.get $p0
      i32.const 4
      i32.add
      local.get $p0
      i32.const 16
      i32.add
      call $f70485
    end
    local.get $l10
    local.get $l19
    f32.load offset=16
    local.tee $l44
    local.get $l10
    f32.load offset=712
    local.tee $l47
    f32.mul
    local.get $l19
    f32.load offset=20
    local.tee $l46
    local.get $l10
    f32.load offset=724
    local.tee $l56
    f32.mul
    f32.add
    local.get $l19
    f32.load offset=24
    local.tee $l45
    local.get $l10
    f32.load offset=736
    local.tee $l51
    f32.mul
    f32.add
    local.tee $l61
    local.get $l47
    local.get $l19
    f32.load offset=28
    local.tee $l48
    f32.mul
    f32.abs
    local.get $l56
    local.get $l19
    f32.load offset=32
    local.tee $l47
    f32.mul
    f32.abs
    f32.add
    local.get $l51
    local.get $l19
    f32.load offset=36
    local.tee $l56
    f32.mul
    f32.abs
    f32.add
    local.tee $l51
    f32.add
    f32.store offset=620
    local.get $l10
    local.get $l44
    local.get $l10
    f32.load offset=708
    local.tee $l64
    f32.mul
    local.get $l46
    local.get $l10
    f32.load offset=720
    local.tee $l67
    f32.mul
    f32.add
    local.get $l45
    local.get $l10
    f32.load offset=732
    local.tee $l68
    f32.mul
    f32.add
    local.tee $l69
    local.get $l64
    local.get $l48
    f32.mul
    f32.abs
    local.get $l67
    local.get $l47
    f32.mul
    f32.abs
    f32.add
    local.get $l68
    local.get $l56
    f32.mul
    f32.abs
    f32.add
    local.tee $l64
    f32.add
    f32.store offset=616
    local.get $l10
    local.get $l44
    local.get $l10
    f32.load offset=704
    local.tee $l67
    f32.mul
    local.get $l46
    local.get $l10
    f32.load offset=716
    local.tee $l44
    f32.mul
    f32.add
    local.get $l45
    local.get $l10
    f32.load offset=728
    local.tee $l46
    f32.mul
    f32.add
    local.tee $l45
    local.get $l67
    local.get $l48
    f32.mul
    f32.abs
    local.get $l44
    local.get $l47
    f32.mul
    f32.abs
    f32.add
    local.get $l46
    local.get $l56
    f32.mul
    f32.abs
    f32.add
    local.tee $l44
    f32.add
    f32.store offset=612
    local.get $l10
    local.get $l61
    local.get $l51
    f32.sub
    f32.store offset=608
    local.get $l10
    local.get $l69
    local.get $l64
    f32.sub
    f32.store offset=604
    local.get $l10
    local.get $l45
    local.get $l44
    f32.sub
    f32.store offset=600
    local.get $l10
    local.get $p3
    f32.load offset=4
    local.tee $l46
    local.get $l46
    f32.add
    local.tee $l48
    local.get $p3
    f32.load offset=8
    local.tee $l44
    f32.mul
    local.tee $l51
    local.get $p3
    f32.load
    local.tee $l47
    local.get $l47
    f32.add
    local.tee $l45
    local.get $p3
    f32.load offset=12
    local.tee $l56
    f32.mul
    local.tee $l61
    f32.sub
    f32.store offset=60
    local.get $l10
    local.get $l51
    local.get $l61
    f32.add
    f32.store offset=52
    local.get $l10
    i32.const -64
    i32.sub
    f32.const 0x1p+0 (;=1;)
    local.get $l47
    local.get $l45
    f32.mul
    f32.sub
    local.tee $l47
    local.get $l46
    local.get $l48
    f32.mul
    local.tee $l51
    f32.sub
    f32.store
    local.get $l10
    local.get $l47
    local.get $l44
    local.get $l44
    local.get $l44
    f32.add
    local.tee $l61
    f32.mul
    local.tee $l64
    f32.sub
    f32.store offset=48
    local.get $l10
    local.get $l45
    local.get $l44
    f32.mul
    local.tee $l44
    local.get $l48
    local.get $l56
    f32.mul
    local.tee $l48
    f32.add
    f32.store offset=56
    local.get $l10
    local.get $l45
    local.get $l46
    f32.mul
    local.tee $l46
    local.get $l61
    local.get $l56
    f32.mul
    local.tee $l45
    f32.sub
    f32.store offset=44
    local.get $l10
    local.get $l44
    local.get $l48
    f32.sub
    f32.store offset=40
    local.get $l10
    local.get $l46
    local.get $l45
    f32.add
    f32.store offset=36
    local.get $l10
    f32.const 0x1p+0 (;=1;)
    local.get $l51
    f32.sub
    local.get $l64
    f32.sub
    f32.store offset=32
    local.get $l10
    local.get $p3
    f32.load offset=16
    f32.store offset=68
    local.get $l10
    local.get $p3
    f32.load offset=20
    f32.store offset=72
    local.get $l10
    local.get $p3
    f32.load offset=24
    f32.store offset=76
    local.get $l10
    local.get $p1
    f32.load offset=4
    local.tee $l46
    local.get $l46
    f32.add
    local.tee $l48
    local.get $p1
    f32.load offset=8
    local.tee $l44
    f32.mul
    local.tee $l51
    local.get $p1
    f32.load
    local.tee $l47
    local.get $l47
    f32.add
    local.tee $l45
    local.get $p1
    f32.load offset=12
    local.tee $l56
    f32.mul
    local.tee $l61
    f32.sub
    f32.store offset=516
    local.get $l10
    local.get $l51
    local.get $l61
    f32.add
    f32.store offset=508
    local.get $l10
    f32.const 0x1p+0 (;=1;)
    local.get $l47
    local.get $l45
    f32.mul
    f32.sub
    local.tee $l47
    local.get $l46
    local.get $l48
    f32.mul
    local.tee $l51
    f32.sub
    f32.store offset=520
    local.get $l10
    local.get $l47
    local.get $l44
    local.get $l44
    local.get $l44
    f32.add
    local.tee $l61
    f32.mul
    local.tee $l64
    f32.sub
    f32.store offset=504
    local.get $l10
    local.get $l45
    local.get $l44
    f32.mul
    local.tee $l44
    local.get $l48
    local.get $l56
    f32.mul
    local.tee $l48
    f32.add
    f32.store offset=512
    local.get $l10
    local.get $l45
    local.get $l46
    f32.mul
    local.tee $l46
    local.get $l61
    local.get $l56
    f32.mul
    local.tee $l45
    f32.sub
    f32.store offset=500
    local.get $l10
    local.get $l44
    local.get $l48
    f32.sub
    f32.store offset=496
    local.get $l10
    local.get $l46
    local.get $l45
    f32.add
    f32.store offset=492
    local.get $l10
    f32.const 0x1p+0 (;=1;)
    local.get $l51
    f32.sub
    local.get $l64
    f32.sub
    f32.store offset=488
    local.get $l10
    local.get $p1
    f32.load offset=16
    f32.store offset=524
    local.get $l10
    local.get $p1
    f32.load offset=20
    f32.store offset=528
    local.get $l10
    local.get $p1
    f32.load offset=24
    f32.store offset=532
    local.get $l10
    i32.const 536
    i32.add
    local.get $l10
    i32.const 600
    i32.add
    f32.const 0x0p+0 (;=0;)
    local.get $l10
    i32.const 32
    i32.add
    local.get $l10
    i32.const 488
    i32.add
    local.get $l10
    i32.const 624
    i32.add
    local.get $l18
    call $f69939
    local.get $l10
    i32.const 588
    i32.add
    local.tee $l16
    local.get $l16
    f32.load
    local.get $p8
    f32.add
    f32.store
    local.get $l10
    i32.const 592
    i32.add
    local.tee $l16
    local.get $l16
    f32.load
    local.get $p8
    f32.add
    f32.store
    local.get $l10
    local.get $l10
    f32.load offset=584
    local.get $p8
    f32.add
    f32.store offset=584
    local.get $l10
    local.get $l10
    f32.load offset=668
    local.get $p1
    f32.load
    local.tee $l46
    local.get $l46
    local.get $p4
    f32.load
    local.tee $l61
    local.get $l61
    f32.add
    local.tee $l45
    f32.mul
    local.get $p4
    f32.load offset=4
    local.tee $l64
    local.get $l64
    f32.add
    local.tee $l48
    local.get $p1
    f32.load offset=4
    local.tee $l47
    f32.mul
    f32.add
    local.get $p4
    f32.load offset=8
    local.tee $l67
    local.get $l67
    f32.add
    local.tee $l56
    local.get $p1
    f32.load offset=8
    local.tee $l51
    f32.mul
    f32.add
    local.tee $l68
    f32.mul
    local.get $l45
    local.get $p1
    f32.load offset=12
    local.tee $l44
    local.get $l44
    f32.mul
    f32.const -0x1p-1 (;=-0.5;)
    f32.add
    local.tee $l69
    f32.mul
    local.get $l44
    local.get $l56
    local.get $l47
    f32.mul
    local.get $l48
    local.get $l51
    f32.mul
    f32.sub
    f32.mul
    f32.sub
    f32.add
    local.get $p5
    f32.mul
    local.tee $l43
    f32.mul
    local.get $l47
    local.get $l68
    f32.mul
    local.get $l48
    local.get $l69
    f32.mul
    local.get $l44
    local.get $l45
    local.get $l51
    f32.mul
    local.get $l56
    local.get $l46
    f32.mul
    f32.sub
    f32.mul
    f32.sub
    f32.add
    local.get $p5
    f32.mul
    local.tee $l49
    local.get $l10
    f32.load offset=680
    f32.mul
    f32.add
    local.get $l56
    local.get $l69
    f32.mul
    local.get $l44
    local.get $l48
    local.get $l46
    f32.mul
    local.get $l45
    local.get $l47
    f32.mul
    f32.sub
    f32.mul
    f32.sub
    local.get $l51
    local.get $l68
    f32.mul
    f32.add
    local.get $p5
    f32.mul
    local.tee $l45
    local.get $l10
    f32.load offset=692
    f32.mul
    f32.add
    local.tee $l44
    f32.store offset=496
    local.get $l10
    local.get $l10
    f32.load offset=664
    local.get $l43
    f32.mul
    local.get $l49
    local.get $l10
    f32.load offset=676
    f32.mul
    f32.add
    local.get $l45
    local.get $l10
    f32.load offset=688
    f32.mul
    f32.add
    local.tee $l46
    f32.store offset=492
    local.get $l10
    local.get $l10
    f32.load offset=660
    local.get $l43
    f32.mul
    local.get $l49
    local.get $l10
    f32.load offset=672
    f32.mul
    f32.add
    local.get $l45
    local.get $l10
    f32.load offset=684
    f32.mul
    f32.add
    local.tee $l45
    f32.store offset=488
    local.get $l45
    local.get $l45
    f32.mul
    local.get $l46
    local.get $l46
    f32.mul
    f32.add
    local.get $l44
    local.get $l44
    f32.mul
    f32.add
    f32.sqrt
    local.tee $l48
    f32.const 0x0p+0 (;=0;)
    f32.gt
    if $I4
      local.get $l10
      local.get $l44
      f32.const 0x1p+0 (;=1;)
      local.get $l48
      f32.div
      local.tee $l47
      f32.mul
      f32.store offset=496
      local.get $l10
      local.get $l46
      local.get $l47
      f32.mul
      f32.store offset=492
      local.get $l10
      local.get $l45
      local.get $l47
      f32.mul
      f32.store offset=488
    end
    local.get $p0
    i32.load8_u offset=32
    local.set $l25
    local.get $l10
    local.get $p7
    i32.load16_u
    local.tee $l16
    i32.store16 offset=8
    local.get $l10
    local.get $l67
    f32.neg
    f32.store offset=24
    local.get $l10
    local.get $l64
    f32.neg
    f32.store offset=20
    local.get $l10
    local.get $l61
    f32.neg
    f32.store offset=16
    local.get $l29
    local.get $l10
    i32.const 536
    i32.add
    local.get $l10
    i32.const 488
    i32.add
    local.get $l48
    block $B5 (result i32)
      local.get $l19
      i32.const 16
      i32.add
      local.set $l20
      local.get $l32
      local.set $l13
      global.get $g0
      i32.const 32
      i32.sub
      local.tee $l21
      global.set $g0
      local.get $l10
      i32.const 624
      i32.add
      local.tee $l26
      i32.load8_u offset=72
      local.set $l27
      local.get $l10
      i32.const 32
      i32.add
      local.tee $l11
      i32.const 3124980
      i32.store
      local.get $l11
      i32.const 2
      i32.store offset=4
      local.get $l10
      i32.load16_u offset=8
      local.set $l28
      local.get $l11
      f32.const 0x1p+0 (;=1;)
      local.get $l48
      local.get $p5
      f32.div
      local.get $l18
      select
      f32.store offset=16
      local.get $l11
      local.get $l27
      i32.store8 offset=12
      local.get $l11
      i32.const 0
      i32.store16 offset=10
      local.get $l11
      local.get $l28
      i32.store16 offset=8
      local.get $l11
      i64.const 0
      i64.store offset=64
      local.get $l11
      i32.const 3125040
      i32.store
      local.get $l11
      i32.const 72
      i32.add
      local.tee $l28
      i64.const 0
      i64.store
      local.get $l11
      i32.const 80
      i32.add
      local.tee $l27
      i64.const 0
      i64.store
      local.get $l11
      i32.const 88
      i32.add
      local.tee $l31
      i64.const 0
      i64.store
      local.get $l11
      i32.const 0
      i32.store8 offset=96
      local.get $l11
      i32.const 272
      i32.add
      local.tee $l33
      i64.const 0
      i64.store
      local.get $l11
      i32.const 280
      i32.add
      local.tee $l34
      i64.const 0
      i64.store
      local.get $l11
      i32.const 228
      i32.add
      local.tee $l35
      i64.const 0
      i64.store align=4
      local.get $l11
      i32.const 236
      i32.add
      local.tee $l36
      i64.const 0
      i64.store align=4
      local.get $l11
      i32.const 248
      i32.add
      local.tee $l37
      i64.const 0
      i64.store
      local.get $l11
      i32.const 256
      i32.add
      local.tee $l38
      i64.const 0
      i64.store
      local.get $l11
      i32.const 1065353216
      i32.store offset=224
      local.get $l11
      i32.const 244
      i32.add
      local.tee $l39
      i32.const 1065353216
      i32.store
      local.get $l11
      i32.const 264
      i32.add
      local.tee $l40
      i64.const 1065353216
      i64.store
      local.get $l11
      i32.const 312
      i32.add
      local.tee $l41
      i64.const 0
      i64.store
      local.get $l11
      i32.const 304
      i32.add
      local.tee $l42
      i64.const 0
      i64.store
      local.get $l11
      local.get $l26
      i32.store offset=320
      local.get $l11
      i32.const 332
      i32.add
      local.tee $l26
      i32.const -1
      i32.store
      local.get $l11
      i64.const 0
      i64.store offset=288
      local.get $l11
      i32.const 296
      i32.add
      local.tee $l12
      i64.const 4575657221408423936
      i64.store
      local.get $l11
      i64.const 0
      i64.store offset=324 align=4
      local.get $l11
      i32.const 0
      i32.store16 offset=336
      local.get $l11
      i64.const 0
      i64.store offset=340 align=4
      local.get $l11
      i64.const 0
      i64.store offset=348 align=4
      local.get $l11
      i64.const 0
      i64.store offset=356 align=4
      local.get $l11
      i32.const 364
      i32.add
      local.tee $l18
      i32.const 2139095039
      i32.store
      local.get $l11
      local.get $l10
      i32.const 16
      i32.add
      local.tee $l17
      f32.load
      f32.store offset=416
      local.get $l11
      local.get $l17
      f32.load offset=4
      f32.store offset=420
      local.get $l17
      f32.load offset=8
      local.set $l52
      local.get $l11
      local.get $l16
      i32.const 128
      i32.and
      local.tee $l19
      local.get $l25
      i32.const 2
      i32.and
      local.tee $l25
      i32.or
      i32.const 0
      i32.ne
      local.tee $l32
      i32.store8 offset=445
      local.get $l11
      local.get $l16
      i32.const 64
      i32.and
      i32.const 6
      i32.shr_u
      local.tee $l16
      i32.store8 offset=444
      local.get $l11
      local.get $p8
      f32.store offset=440
      local.get $l11
      local.get $l52
      f32.store offset=424
      local.get $l18
      local.get $p5
      f32.store
      local.get $l26
      i32.const -1
      i32.store
      local.get $l11
      local.get $l17
      f32.load offset=8
      local.tee $l49
      local.get $l49
      f32.add
      local.tee $l52
      local.get $p1
      f32.load offset=12
      local.tee $l49
      local.get $l49
      f32.mul
      f32.const -0x1p-1 (;=-0.5;)
      f32.add
      local.tee $l44
      f32.mul
      local.get $l49
      local.get $l17
      f32.load offset=4
      local.tee $l53
      local.get $l53
      f32.add
      local.tee $l53
      local.get $p1
      f32.load
      local.tee $l54
      f32.mul
      local.get $l17
      f32.load
      local.tee $l47
      local.get $l47
      f32.add
      local.tee $l47
      local.get $p1
      f32.load offset=4
      local.tee $l60
      f32.mul
      f32.sub
      f32.mul
      f32.sub
      local.get $p1
      f32.load offset=8
      local.tee $l62
      local.get $l47
      local.get $l54
      f32.mul
      local.get $l53
      local.get $l60
      f32.mul
      f32.add
      local.get $l52
      local.get $l62
      f32.mul
      f32.add
      local.tee $l45
      f32.mul
      f32.add
      f32.store offset=436
      local.get $l11
      local.get $l60
      local.get $l45
      f32.mul
      local.get $l53
      local.get $l44
      f32.mul
      local.get $l49
      local.get $l47
      local.get $l62
      f32.mul
      local.get $l52
      local.get $l54
      f32.mul
      f32.sub
      f32.mul
      f32.sub
      f32.add
      f32.store offset=432
      local.get $l11
      local.get $l54
      local.get $l45
      f32.mul
      local.get $l47
      local.get $l44
      f32.mul
      local.get $l49
      local.get $l52
      local.get $l60
      f32.mul
      local.get $l53
      local.get $l62
      f32.mul
      f32.sub
      f32.mul
      f32.sub
      f32.add
      f32.store offset=428
      local.get $p1
      f32.load offset=20
      local.set $l51
      local.get $p1
      f32.load offset=24
      local.set $l61
      local.get $p3
      f32.load offset=20
      local.set $l48
      local.get $p3
      f32.load offset=24
      local.set $l57
      local.get $l17
      f32.load offset=4
      local.set $l64
      local.get $l17
      f32.load
      local.set $l67
      local.get $l17
      f32.load offset=8
      local.set $l68
      local.get $p1
      f32.load offset=8
      local.set $l60
      local.get $p1
      f32.load
      local.set $l62
      local.get $p1
      f32.load offset=4
      local.set $l44
      local.get $p1
      f32.load offset=12
      local.set $l45
      local.get $p1
      f32.load offset=16
      local.set $l56
      local.get $p3
      f32.load
      local.set $l49
      local.get $p3
      f32.load offset=4
      local.set $l54
      local.get $p3
      f32.load offset=8
      local.set $l52
      local.get $p3
      f32.load offset=12
      local.set $l53
      local.get $p3
      f32.load offset=16
      local.set $l46
      local.get $l11
      i32.const 0
      i32.store offset=412
      local.get $l11
      i32.const 0
      i32.store offset=316
      local.get $l41
      local.get $l57
      f32.store
      local.get $l11
      local.get $l48
      f32.store offset=308
      local.get $l42
      local.get $l46
      f32.store
      local.get $l11
      local.get $l53
      f32.store offset=300
      local.get $l12
      local.get $l52
      f32.store
      local.get $l11
      local.get $l54
      f32.store offset=292
      local.get $l11
      local.get $l49
      f32.store offset=288
      local.get $l11
      i32.const 0
      i32.store offset=284
      local.get $l11
      i32.const 0
      i32.store offset=268
      local.get $l11
      i32.const 0
      i32.store offset=252
      local.get $l36
      i32.const 0
      i32.store
      local.get $l34
      local.get $l53
      local.get $l53
      f32.mul
      f32.const -0x1p-1 (;=-0.5;)
      f32.add
      local.tee $l47
      local.get $l61
      local.get $l57
      f32.sub
      local.tee $l57
      f32.mul
      local.get $l53
      local.get $l54
      local.get $l56
      local.get $l46
      f32.sub
      local.tee $l46
      f32.mul
      local.get $l49
      local.get $l51
      local.get $l48
      f32.sub
      local.tee $l48
      f32.mul
      f32.sub
      f32.mul
      f32.add
      local.get $l52
      local.get $l48
      local.get $l54
      f32.neg
      local.tee $l61
      f32.mul
      local.get $l49
      local.get $l46
      f32.mul
      f32.sub
      local.get $l52
      local.get $l57
      f32.mul
      f32.sub
      local.tee $l51
      f32.mul
      f32.sub
      local.tee $l56
      local.get $l56
      f32.add
      f32.store
      local.get $l11
      local.get $l47
      local.get $l48
      f32.mul
      local.get $l53
      local.get $l49
      local.get $l57
      f32.mul
      local.get $l52
      local.get $l46
      f32.mul
      f32.sub
      f32.mul
      f32.add
      local.get $l54
      local.get $l51
      f32.mul
      f32.sub
      local.tee $l56
      local.get $l56
      f32.add
      f32.store offset=276
      local.get $l33
      local.get $l47
      local.get $l46
      f32.mul
      local.get $l53
      local.get $l52
      local.get $l48
      f32.mul
      local.get $l54
      local.get $l57
      f32.mul
      f32.sub
      f32.mul
      f32.add
      local.get $l49
      local.get $l51
      f32.mul
      f32.sub
      local.tee $l57
      local.get $l57
      f32.add
      f32.store
      local.get $l40
      f32.const 0x1p+0 (;=1;)
      local.get $l44
      local.get $l52
      f32.mul
      local.get $l60
      local.get $l54
      f32.mul
      f32.sub
      local.get $l62
      local.get $l53
      f32.mul
      local.get $l45
      local.get $l49
      f32.mul
      f32.sub
      f32.add
      local.tee $l57
      local.get $l57
      local.get $l57
      f32.add
      local.tee $l46
      f32.mul
      f32.sub
      local.tee $l56
      local.get $l60
      local.get $l49
      f32.mul
      local.get $l62
      local.get $l52
      f32.mul
      f32.sub
      local.get $l44
      local.get $l53
      f32.mul
      local.get $l45
      local.get $l54
      f32.mul
      f32.sub
      f32.add
      local.tee $l48
      local.get $l48
      local.get $l48
      f32.add
      local.tee $l51
      f32.mul
      local.tee $l69
      f32.sub
      f32.store
      local.get $l11
      local.get $l62
      local.get $l54
      f32.mul
      local.get $l44
      local.get $l49
      f32.mul
      f32.sub
      local.get $l60
      local.get $l53
      f32.mul
      local.get $l45
      local.get $l52
      f32.mul
      f32.sub
      f32.add
      local.tee $l57
      local.get $l51
      f32.mul
      local.tee $l43
      local.get $l45
      local.get $l53
      f32.mul
      local.get $l44
      local.get $l61
      f32.mul
      local.get $l62
      local.get $l49
      f32.mul
      f32.sub
      local.get $l60
      local.get $l52
      f32.mul
      f32.sub
      f32.sub
      local.tee $l60
      local.get $l46
      f32.mul
      local.tee $l62
      f32.sub
      f32.store offset=260
      local.get $l38
      local.get $l57
      local.get $l46
      f32.mul
      local.tee $l44
      local.get $l60
      local.get $l51
      f32.mul
      local.tee $l45
      f32.add
      f32.store
      local.get $l37
      local.get $l43
      local.get $l62
      f32.add
      f32.store
      local.get $l39
      local.get $l56
      local.get $l57
      local.get $l57
      local.get $l57
      f32.add
      local.tee $l62
      f32.mul
      local.tee $l57
      f32.sub
      f32.store
      local.get $l11
      local.get $l48
      local.get $l46
      f32.mul
      local.tee $l46
      local.get $l60
      local.get $l62
      f32.mul
      local.tee $l60
      f32.sub
      f32.store offset=240
      local.get $l11
      local.get $l44
      local.get $l45
      f32.sub
      f32.store offset=232
      local.get $l35
      local.get $l46
      local.get $l60
      f32.add
      f32.store
      local.get $l11
      f32.const 0x1p+0 (;=1;)
      local.get $l69
      f32.sub
      local.get $l57
      f32.sub
      f32.store offset=224
      local.get $l11
      local.get $l52
      local.get $l49
      local.get $l67
      f32.neg
      local.get $p5
      f32.mul
      local.tee $l60
      f32.mul
      local.get $l54
      local.get $l64
      f32.neg
      local.get $p5
      f32.mul
      local.tee $l62
      f32.mul
      f32.add
      local.get $l52
      local.get $l68
      f32.neg
      local.get $p5
      f32.mul
      local.tee $l44
      f32.mul
      f32.add
      local.tee $l45
      f32.mul
      local.get $l44
      local.get $l47
      f32.mul
      local.get $l53
      local.get $l62
      local.get $l49
      f32.mul
      local.get $l60
      local.get $l54
      f32.mul
      f32.sub
      f32.mul
      f32.sub
      f32.add
      local.tee $l57
      local.get $l57
      f32.add
      f32.store offset=408
      local.get $l11
      local.get $l54
      local.get $l45
      f32.mul
      local.get $l62
      local.get $l47
      f32.mul
      local.get $l53
      local.get $l60
      local.get $l52
      f32.mul
      local.get $l44
      local.get $l49
      f32.mul
      f32.sub
      f32.mul
      f32.sub
      f32.add
      local.tee $l57
      local.get $l57
      f32.add
      f32.store offset=404
      local.get $l11
      local.get $l49
      local.get $l45
      f32.mul
      local.get $l60
      local.get $l47
      f32.mul
      local.get $l53
      local.get $l44
      local.get $l54
      f32.mul
      local.get $l62
      local.get $l52
      f32.mul
      f32.sub
      f32.mul
      f32.sub
      f32.add
      local.tee $l49
      local.get $l49
      f32.add
      f32.store offset=400
      local.get $l11
      local.get $p5
      f32.store offset=384
      local.get $l13
      f32.load
      local.set $l49
      local.get $l13
      f32.load offset=4
      local.set $l52
      local.get $l13
      f32.load offset=8
      local.set $l53
      local.get $l21
      i32.const 0
      i32.store offset=28
      local.get $l21
      local.get $l53
      f32.store offset=24
      local.get $l21
      local.get $l52
      f32.store offset=20
      local.get $l21
      local.get $l49
      f32.store offset=16
      local.get $l13
      i64.load offset=12 align=4
      local.set $l93
      local.get $l21
      local.get $l13
      i64.load offset=20 align=4
      i64.store offset=8
      local.get $l21
      local.get $l93
      i64.store
      local.get $l20
      i32.load offset=40
      local.set $l13
      local.get $l20
      i32.load8_u offset=39
      local.set $l17
      local.get $l11
      local.get $l49
      local.get $l20
      f32.load offset=52
      f32.mul
      local.tee $l54
      local.get $l52
      local.get $l20
      f32.load offset=56
      f32.mul
      local.tee $p5
      local.get $p5
      local.get $l54
      f32.ge
      select
      local.tee $l54
      local.get $l53
      local.get $l20
      f32.load offset=60
      f32.mul
      local.tee $p5
      local.get $p5
      local.get $l54
      f32.ge
      select
      local.tee $l54
      f32.const 0x1.99999ap-5 (;=0.05;)
      f32.mul
      f32.store offset=84
      local.get $l31
      local.get $l54
      f32.const 0x1.99999ap-6 (;=0.025;)
      f32.mul
      f32.store
      local.get $l27
      local.get $l54
      f32.const 0x1.99999ap-4 (;=0.1;)
      f32.mul
      f32.store
      local.get $l21
      i32.const 16
      i32.add
      local.get $l21
      local.get $l11
      i32.const 112
      i32.add
      local.get $l11
      i32.const 160
      i32.add
      local.get $l11
      i32.const -64
      i32.sub
      local.get $l49
      f32.const 0x1p+0 (;=1;)
      f32.eq
      local.get $l52
      f32.const 0x1p+0 (;=1;)
      f32.eq
      i32.and
      local.get $l53
      f32.const 0x1p+0 (;=1;)
      f32.eq
      i32.and
      call $f70494
      local.get $l11
      local.get $l13
      local.get $l17
      i32.const 20
      i32.mul
      i32.add
      i32.store offset=216
      local.get $l20
      i32.load8_u offset=38
      local.set $l13
      local.get $l11
      i64.const 0
      i64.store offset=64
      local.get $l11
      local.get $l13
      i32.store8 offset=220
      local.get $l28
      i64.const 0
      i64.store
      local.get $l20
      i32.load offset=44
      local.set $l13
      local.get $l11
      local.get $l20
      i32.store offset=208
      local.get $l11
      local.get $l13
      i32.store offset=212
      local.get $l20
      i32.load offset=44
      drop
      local.get $l21
      i32.const 32
      i32.add
      global.set $g0
      local.get $l11
    end
    local.get $l16
    local.get $l29
    i32.load16_u offset=4
    i32.const 2
    i32.shl
    i32.const 3125056
    i32.add
    i32.load
    call_indirect $__indirect_function_table (type $t159)
    local.get $p6
    local.set $l12
    local.get $p4
    local.set $l18
    local.get $p7
    i32.load16_u
    i32.const 512
    i32.and
    i32.const 9
    i32.shr_u
    local.set $p7
    local.get $l19
    i32.const 7
    i32.shr_u
    local.set $p6
    local.get $l25
    i32.const 1
    i32.shr_u
    local.set $l13
    f32.const 0x0p+0 (;=0;)
    local.set $l51
    f32.const 0x0p+0 (;=0;)
    local.set $l52
    f32.const 0x0p+0 (;=0;)
    local.set $l53
    i32.const 0
    local.set $l29
    i32.const 0
    local.set $l31
    f32.const 0x0p+0 (;=0;)
    local.set $l64
    f32.const 0x0p+0 (;=0;)
    local.set $l67
    f32.const 0x0p+0 (;=0;)
    local.set $l68
    block $B6
      local.get $l11
      i32.load8_u offset=10
      local.tee $l42
      i32.eqz
      br_if $B6
      local.get $l11
      i32.load8_u offset=11
      if $I7
        block $B8
          block $B9
            block $B10
              local.get $p7
              i32.eqz
              if $I11
                local.get $l12
                i32.const 1026
                i32.store16 offset=12
                br $B10
              end
              local.get $p3
              local.set $p4
              global.get $g0
              i32.const 6096
              i32.sub
              local.tee $l9
              global.set $g0
              local.get $p0
              local.tee $p3
              i32.load offset=36
              local.tee $l19
              i32.load offset=56
              local.set $l33
              local.get $p2
              local.tee $l13
              i32.load offset=32
              local.set $l22
              local.get $l9
              i32.const 0
              i32.store offset=1980
              f32.const 0x1p+0 (;=1;)
              local.set $l80
              block $B12 (result i32)
                i32.const 0
                local.get $l13
                f32.load offset=4
                local.tee $l50
                f32.const 0x1p+0 (;=1;)
                f32.ne
                br_if $B12
                drop
                i32.const 0
                local.get $l13
                f32.load offset=8
                f32.const 0x1p+0 (;=1;)
                f32.ne
                br_if $B12
                drop
                local.get $l13
                f32.load offset=12
                f32.const 0x1p+0 (;=1;)
                f32.eq
              end
              local.set $l16
              local.get $l22
              i32.const 16
              i32.add
              local.set $l14
              local.get $l9
              i32.const 1968
              i32.add
              i64.const 4575657221408423936
              i64.store
              local.get $l9
              i32.const 1960
              i32.add
              i64.const 0
              i64.store
              local.get $l9
              i32.const 1952
              i32.add
              i64.const 4575657221408423936
              i64.store
              local.get $l9
              i32.const 1944
              i32.add
              i64.const 0
              i64.store
              local.get $l9
              i32.const 1936
              i32.add
              i64.const 4575657222473777152
              i64.store
              local.get $l9
              i32.const 1920
              i32.add
              i64.const 1065353216
              i64.store
              local.get $l9
              i32.const 0
              i32.store8 offset=1976
              local.get $l9
              i64.const 0
              i64.store offset=1928
              local.get $l9
              i64.const 0
              i64.store offset=1912
              local.get $l9
              i64.const 1065353216
              i64.store offset=1904
              f32.const 0x1p+0 (;=1;)
              local.set $l81
              f32.const 0x1p+0 (;=1;)
              local.set $l71
              local.get $l16
              i32.eqz
              if $I13
                local.get $l9
                i32.const 1904
                i32.add
                local.get $l13
                i32.const 4
                i32.add
                local.get $l13
                i32.const 16
                i32.add
                call $f70485
                local.get $l9
                f32.load offset=1932
                local.set $l77
                local.get $l9
                f32.load offset=1928
                local.set $l78
                local.get $l9
                f32.load offset=1924
                local.set $l79
                local.get $l9
                f32.load offset=1920
                local.set $l81
                local.get $l9
                f32.load offset=1912
                local.set $l66
                local.get $l9
                f32.load offset=1908
                local.set $l63
                local.get $l9
                f32.load offset=1904
                local.set $l71
                local.get $l13
                f32.load offset=4
                local.set $l50
                local.get $l9
                f32.load offset=1936
                local.set $l80
                local.get $l9
                f32.load offset=1916
                local.set $l70
              end
              local.get $l22
              f32.load offset=44
              local.set $l43
              local.get $p4
              f32.load offset=20
              local.set $l90
              local.get $p4
              f32.load offset=24
              local.set $l91
              local.get $l22
              f32.load offset=48
              local.set $l55
              local.get $l22
              f32.load offset=40
              local.set $l58
              local.get $p4
              i64.load align=4
              local.set $l94
              local.get $p4
              i64.load offset=8 align=4
              local.set $l93
              local.get $p4
              f32.load offset=16
              local.set $l92
              local.get $l9
              i32.const 1900
              i32.add
              i32.const 0
              i32.store
              local.get $l9
              i32.const 1896
              i32.add
              local.get $l91
              f32.store
              local.get $l9
              i32.const 1892
              i32.add
              local.get $l90
              f32.store
              local.get $l9
              local.get $l92
              f32.store offset=1888
              local.get $l9
              local.get $l93
              i64.store offset=1880
              local.get $l9
              local.get $l94
              i64.store offset=1872
              local.get $l13
              f32.load offset=8
              local.set $l59
              local.get $l13
              f32.load offset=12
              local.set $p5
              local.get $l9
              i32.const 0
              i32.store offset=1868
              local.get $l9
              local.get $p5
              f32.store offset=1864
              local.get $l9
              local.get $l59
              f32.store offset=1860
              local.get $l9
              local.get $l50
              f32.store offset=1856
              local.get $l13
              i64.load offset=16 align=4
              local.set $l94
              local.get $l9
              local.get $l13
              i64.load offset=24 align=4
              i64.store offset=1848
              local.get $l9
              local.get $l94
              i64.store offset=1840
              local.get $l9
              i32.const 1712
              i32.add
              i32.const 0
              i32.store8
              local.get $l9
              i32.const 1704
              i32.add
              local.tee $l15
              i64.const 0
              i64.store
              local.get $l9
              i32.const 1696
              i32.add
              local.tee $l24
              i64.const 0
              i64.store
              local.get $l9
              i64.const 0
              i64.store offset=1688
              local.get $l9
              i64.const 0
              i64.store offset=1680
              local.get $l9
              local.get $l14
              i32.store offset=1824
              local.get $l9
              local.get $l22
              i32.load offset=56
              local.get $l22
              i32.load8_u offset=55
              i32.const 20
              i32.mul
              i32.add
              i32.store offset=1832
              local.get $l9
              local.get $l22
              i32.load8_u offset=54
              i32.store8 offset=1836
              local.get $l15
              local.get $l50
              local.get $l22
              i32.const 68
              i32.add
              local.tee $l14
              f32.load
              f32.mul
              local.tee $l50
              local.get $l59
              local.get $l22
              f32.load offset=72
              f32.mul
              local.tee $l59
              local.get $l50
              local.get $l59
              f32.le
              select
              local.tee $l50
              local.get $p5
              local.get $l22
              i32.const 76
              i32.add
              local.tee $l30
              f32.load
              f32.mul
              local.tee $l59
              local.get $l50
              local.get $l59
              f32.le
              select
              local.tee $l50
              f32.const 0x1.99999ap-6 (;=0.025;)
              f32.mul
              f32.store
              local.get $l24
              local.get $l50
              f32.const 0x1.99999ap-4 (;=0.1;)
              f32.mul
              f32.store
              local.get $l9
              local.get $l50
              f32.const 0x1.99999ap-5 (;=0.05;)
              f32.mul
              f32.store offset=1700
              local.get $l9
              i32.const 1856
              i32.add
              local.get $l9
              i32.const 1840
              i32.add
              local.get $l9
              i32.const 1728
              i32.add
              local.tee $l36
              local.get $l9
              i32.const 1776
              i32.add
              local.tee $l37
              local.get $l9
              i32.const 1680
              i32.add
              local.get $l16
              call $f70494
              local.get $l9
              local.get $l22
              i32.load offset=60
              i32.store offset=1828
              local.get $l9
              local.get $l14
              f32.load
              local.get $l9
              f32.load offset=1856
              f32.mul
              local.tee $l50
              local.get $l22
              f32.load offset=72
              local.get $l9
              f32.load offset=1860
              f32.mul
              local.tee $l59
              local.get $l50
              local.get $l59
              f32.le
              select
              local.tee $l50
              local.get $l30
              f32.load
              local.get $l9
              f32.load offset=1864
              f32.mul
              local.tee $l59
              local.get $l50
              local.get $l59
              f32.le
              select
              f32.const 0x1p-2 (;=0.25;)
              f32.mul
              local.get $p8
              f32.add
              local.tee $l56
              f32.store offset=1600
              local.get $l9
              i32.const 0
              i32.store offset=1592
              local.get $l9
              i64.const 0
              i64.store offset=1584
              local.get $l9
              i32.const 1584
              i32.add
              i32.const 128
              call $f70632
              local.get $l9
              i32.const 1536
              i32.add
              local.get $p1
              local.get $p3
              i32.const 4
              i32.add
              local.tee $l38
              call $f70133
              local.get $l9
              i32.const 1680
              i32.add
              local.get $l16
              local.get $l9
              i32.const 1464
              i32.add
              call $f70029
              local.get $l9
              local.get $p4
              f32.load
              f32.store offset=1416
              local.get $l9
              local.get $p4
              f32.load offset=4
              f32.store offset=1420
              local.get $l9
              local.get $p4
              f32.load offset=8
              f32.store offset=1424
              local.get $l9
              local.get $p4
              f32.load offset=12
              f32.store offset=1428
              i32.const 3125832
              i32.const 3125860
              local.get $l16
              select
              local.set $l39
              local.get $l58
              local.get $l66
              f32.mul
              local.get $l43
              local.get $l79
              f32.mul
              f32.add
              local.get $l55
              local.get $l80
              f32.mul
              f32.add
              local.set $l72
              local.get $l58
              local.get $l63
              f32.mul
              local.get $l43
              local.get $l81
              f32.mul
              f32.add
              local.get $l55
              local.get $l77
              f32.mul
              f32.add
              local.set $l73
              local.get $l58
              local.get $l71
              f32.mul
              local.get $l43
              local.get $l70
              f32.mul
              f32.add
              local.get $l55
              local.get $l78
              f32.mul
              f32.add
              local.set $l74
              i32.const 268435455
              local.set $p6
              f32.const 0x0p+0 (;=0;)
              local.set $l80
              f32.const 0x0p+0 (;=0;)
              local.set $l77
              f32.const 0x0p+0 (;=0;)
              local.set $l78
              f32.const 0x0p+0 (;=0;)
              local.set $l79
              f32.const 0x0p+0 (;=0;)
              local.set $l81
              f32.const 0x0p+0 (;=0;)
              local.set $l70
              block $B14 (result i32)
                block $B15
                  loop $L16
                    block $B17
                      local.get $l9
                      local.get $l91
                      f32.store offset=1440
                      local.get $l9
                      local.get $l90
                      f32.store offset=1436
                      local.get $l9
                      local.get $l92
                      f32.store offset=1432
                      local.get $l9
                      i32.const 0
                      i32.store offset=1588
                      local.get $l9
                      i32.const 0
                      i32.store offset=1900
                      local.get $l9
                      local.get $l91
                      f32.store offset=1896
                      local.get $l9
                      local.get $l90
                      f32.store offset=1892
                      local.get $l9
                      local.get $l92
                      f32.store offset=1888
                      local.get $l9
                      local.get $l16
                      i32.store8 offset=1660
                      local.get $l9
                      local.get $l37
                      i32.store offset=1656
                      local.get $l9
                      local.get $l36
                      i32.store offset=1652
                      local.get $l9
                      local.get $l39
                      i32.store offset=1616
                      local.get $l9
                      i32.const 0
                      i32.store offset=1644
                      local.get $l9
                      local.get $l72
                      f32.store offset=1640
                      local.get $l9
                      local.get $l73
                      f32.store offset=1636
                      local.get $l9
                      local.get $l74
                      f32.store offset=1632
                      local.get $l9
                      local.get $l9
                      i32.const 1872
                      i32.add
                      i32.store offset=1648
                      local.get $l9
                      local.get $l9
                      i32.const 1680
                      i32.add
                      i32.store offset=1664
                      local.get $l9
                      i32.const 1352
                      i32.add
                      local.get $l13
                      local.get $l22
                      local.get $l9
                      i32.const 1416
                      i32.add
                      call $f69942
                      local.get $l9
                      local.get $l56
                      local.get $l9
                      f32.load offset=1400
                      f32.add
                      f32.store offset=1400
                      local.get $l9
                      local.get $l56
                      local.get $l9
                      f32.load offset=1404
                      f32.add
                      f32.store offset=1404
                      local.get $l9
                      local.get $l56
                      local.get $l9
                      f32.load offset=1408
                      f32.add
                      f32.store offset=1408
                      local.get $p3
                      i32.load offset=36
                      local.set $p4
                      local.get $l9
                      local.get $l9
                      i32.const 1352
                      i32.add
                      local.get $p1
                      local.get $l38
                      call $f69940
                      local.get $l9
                      i32.const 3124884
                      i32.store offset=1280
                      local.get $l9
                      local.get $l9
                      i32.const 1584
                      i32.add
                      i32.store offset=1288
                      local.get $l9
                      i32.const 2
                      i32.store offset=1284
                      local.get $p4
                      local.get $l9
                      local.get $l9
                      i32.const 1280
                      i32.add
                      i32.const 1
                      i32.const 1
                      local.get $p4
                      i32.load16_u offset=4
                      i32.const 2
                      i32.shl
                      i32.const 3124884
                      i32.add
                      i32.load
                      call_indirect $__indirect_function_table (type $t6)
                      local.get $l9
                      i32.load offset=1588
                      local.tee $p2
                      i32.eqz
                      br_if $B17
                      local.get $l9
                      f32.load offset=1580
                      local.set $l59
                      local.get $l9
                      f32.load offset=1572
                      local.set $p5
                      local.get $l9
                      f32.load offset=1576
                      local.set $l66
                      local.get $l9
                      f32.load offset=1436
                      local.set $l44
                      local.get $l9
                      f32.load offset=1432
                      local.set $l45
                      local.get $l9
                      f32.load offset=1440
                      local.set $l46
                      local.get $l9
                      f32.load offset=1544
                      local.set $l63
                      local.get $l9
                      f32.load offset=1536
                      local.set $l71
                      local.get $l9
                      f32.load offset=1540
                      local.set $p8
                      local.get $l9
                      f32.load offset=1556
                      local.set $l57
                      local.get $l9
                      f32.load offset=1548
                      local.set $l60
                      local.get $l9
                      f32.load offset=1552
                      local.set $l61
                      local.get $l9
                      f32.load offset=1568
                      local.set $l62
                      local.get $l9
                      f32.load offset=1560
                      local.set $l84
                      local.get $l9
                      f32.load offset=1564
                      local.set $l85
                      local.get $l9
                      f32.load offset=1428
                      local.set $l43
                      local.get $l9
                      f32.load offset=1416
                      local.set $l55
                      local.get $l9
                      f32.load offset=1424
                      local.set $l58
                      local.get $l9
                      f32.load offset=1420
                      local.set $l50
                      i32.const 0
                      local.set $l21
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
                      local.get $l84
                      local.get $l55
                      f32.neg
                      local.get $l55
                      f32.sub
                      local.tee $l86
                      local.get $l58
                      f32.neg
                      local.tee $l87
                      f32.mul
                      local.tee $l82
                      local.get $l43
                      local.get $l50
                      f32.neg
                      local.tee $l54
                      local.get $l50
                      f32.sub
                      local.tee $l83
                      f32.mul
                      local.tee $l88
                      f32.sub
                      local.tee $l75
                      f32.mul
                      local.get $l85
                      local.get $l43
                      local.get $l86
                      f32.mul
                      local.tee $l89
                      local.get $l83
                      local.get $l87
                      f32.mul
                      local.tee $l47
                      f32.add
                      local.tee $l76
                      f32.mul
                      f32.add
                      local.get $l62
                      local.get $l55
                      local.get $l86
                      f32.mul
                      f32.const 0x1p+0 (;=1;)
                      f32.add
                      local.tee $l48
                      local.get $l83
                      local.get $l54
                      f32.mul
                      local.tee $l49
                      f32.sub
                      local.tee $l83
                      f32.mul
                      f32.add
                      f32.store offset=1320
                      local.get $l9
                      local.get $l75
                      local.get $l60
                      f32.mul
                      local.get $l76
                      local.get $l61
                      f32.mul
                      f32.add
                      local.get $l83
                      local.get $l57
                      f32.mul
                      f32.add
                      f32.store offset=1304
                      local.get $l9
                      local.get $l71
                      local.get $l75
                      f32.mul
                      local.get $p8
                      local.get $l76
                      f32.mul
                      f32.add
                      local.get $l83
                      local.get $l63
                      f32.mul
                      f32.add
                      f32.store offset=1288
                      local.get $l9
                      local.get $l46
                      f32.const -0x1p+1 (;=-2;)
                      f32.mul
                      local.tee $l46
                      local.get $l43
                      local.get $l43
                      f32.mul
                      f32.const -0x1p-1 (;=-0.5;)
                      f32.add
                      local.tee $l69
                      f32.mul
                      local.get $l43
                      local.get $l55
                      local.get $l44
                      f32.const -0x1p+1 (;=-2;)
                      f32.mul
                      local.tee $l44
                      f32.mul
                      local.get $l50
                      local.get $l45
                      f32.const -0x1p+1 (;=-2;)
                      f32.mul
                      local.tee $l45
                      f32.mul
                      f32.sub
                      f32.mul
                      f32.sub
                      local.get $l58
                      local.get $l45
                      local.get $l55
                      f32.mul
                      local.get $l44
                      local.get $l50
                      f32.mul
                      f32.add
                      local.get $l46
                      local.get $l58
                      f32.mul
                      f32.add
                      local.tee $l65
                      f32.mul
                      f32.add
                      local.get $l75
                      local.get $p5
                      f32.mul
                      local.get $l76
                      local.get $l66
                      f32.mul
                      f32.add
                      local.get $l83
                      local.get $l59
                      f32.mul
                      f32.add
                      f32.add
                      f32.store offset=1336
                      local.get $l9
                      local.get $l84
                      local.get $l86
                      local.get $l54
                      f32.mul
                      local.tee $l83
                      local.get $l43
                      local.get $l87
                      local.get $l58
                      f32.sub
                      local.tee $l75
                      f32.mul
                      local.tee $l54
                      f32.add
                      local.tee $l86
                      f32.mul
                      local.get $l85
                      local.get $l48
                      local.get $l75
                      local.get $l87
                      f32.mul
                      local.tee $l76
                      f32.sub
                      local.tee $l87
                      f32.mul
                      f32.add
                      local.get $l62
                      local.get $l47
                      local.get $l89
                      f32.sub
                      local.tee $l75
                      f32.mul
                      f32.add
                      f32.store offset=1316
                      local.get $l9
                      local.get $l84
                      f32.const 0x1p+0 (;=1;)
                      local.get $l49
                      f32.sub
                      local.get $l76
                      f32.sub
                      local.tee $l76
                      f32.mul
                      local.get $l85
                      local.get $l83
                      local.get $l54
                      f32.sub
                      local.tee $l84
                      f32.mul
                      f32.add
                      local.get $l62
                      local.get $l82
                      local.get $l88
                      f32.add
                      local.tee $l85
                      f32.mul
                      f32.add
                      f32.store offset=1312
                      local.get $l9
                      local.get $l86
                      local.get $l60
                      f32.mul
                      local.get $l87
                      local.get $l61
                      f32.mul
                      f32.add
                      local.get $l75
                      local.get $l57
                      f32.mul
                      f32.add
                      f32.store offset=1300
                      local.get $l9
                      local.get $l76
                      local.get $l60
                      f32.mul
                      local.get $l84
                      local.get $l61
                      f32.mul
                      f32.add
                      local.get $l85
                      local.get $l57
                      f32.mul
                      f32.add
                      f32.store offset=1296
                      local.get $l9
                      local.get $l75
                      local.get $l63
                      f32.mul
                      local.get $l71
                      local.get $l86
                      f32.mul
                      local.get $p8
                      local.get $l87
                      f32.mul
                      f32.add
                      f32.add
                      f32.store offset=1284
                      local.get $l9
                      local.get $l85
                      local.get $l63
                      f32.mul
                      local.get $l71
                      local.get $l76
                      f32.mul
                      local.get $p8
                      local.get $l84
                      f32.mul
                      f32.add
                      f32.add
                      f32.store offset=1280
                      local.get $l9
                      local.get $l50
                      local.get $l65
                      f32.mul
                      local.get $l44
                      local.get $l69
                      f32.mul
                      local.get $l43
                      local.get $l45
                      local.get $l58
                      f32.mul
                      local.get $l46
                      local.get $l55
                      f32.mul
                      f32.sub
                      f32.mul
                      f32.sub
                      f32.add
                      local.get $l86
                      local.get $p5
                      f32.mul
                      local.get $l87
                      local.get $l66
                      f32.mul
                      f32.add
                      local.get $l75
                      local.get $l59
                      f32.mul
                      f32.add
                      f32.add
                      f32.store offset=1332
                      local.get $l9
                      local.get $l55
                      local.get $l65
                      f32.mul
                      local.get $l45
                      local.get $l69
                      f32.mul
                      local.get $l43
                      local.get $l46
                      local.get $l50
                      f32.mul
                      local.get $l44
                      local.get $l58
                      f32.mul
                      f32.sub
                      f32.mul
                      f32.sub
                      f32.add
                      local.get $l76
                      local.get $p5
                      f32.mul
                      local.get $l84
                      local.get $l66
                      f32.mul
                      f32.add
                      local.get $l85
                      local.get $l59
                      f32.mul
                      f32.add
                      f32.add
                      f32.store offset=1328
                      local.get $p2
                      i32.const 31
                      i32.add
                      i32.const 5
                      i32.shr_u
                      local.tee $l40
                      i32.eqz
                      br_if $B17
                      f32.const 0x1.fffffep+127 (;=3.40282e+38;)
                      local.set $p5
                      local.get $p2
                      local.set $p7
                      i32.const 0
                      local.set $l25
                      loop $L18
                        block $B19
                          local.get $p2
                          local.get $l21
                          i32.const 5
                          i32.shl
                          local.tee $l34
                          i32.sub
                          local.tee $p4
                          i32.const 32
                          local.get $p4
                          i32.const 32
                          i32.lt_u
                          select
                          local.tee $l35
                          if $I20
                            local.get $p7
                            i32.const 32
                            local.get $p7
                            i32.const 32
                            i32.lt_u
                            select
                            local.set $l26
                            local.get $p3
                            f32.load offset=4
                            local.get $p3
                            f32.load offset=8
                            f32.mul
                            local.get $p3
                            f32.load offset=12
                            f32.mul
                            local.set $l43
                            local.get $l9
                            i32.load offset=1584
                            local.set $l27
                            i32.const 0
                            local.set $l14
                            loop $L21
                              local.get $l27
                              local.get $l14
                              local.get $l34
                              i32.add
                              i32.const 2
                              i32.shl
                              i32.add
                              i32.load
                              local.set $l17
                              block $B22 (result i32)
                                local.get $l19
                                i32.load8_u offset=64
                                i32.const 2
                                i32.and
                                if $I23
                                  local.get $l19
                                  i32.load offset=28
                                  local.get $l17
                                  i32.const 6
                                  i32.mul
                                  i32.add
                                  local.tee $p4
                                  i32.load16_u offset=4
                                  local.set $l15
                                  local.get $p4
                                  i32.load16_u
                                  local.set $l23
                                  local.get $p4
                                  i32.load16_u offset=2
                                  br $B22
                                end
                                local.get $l19
                                i32.load offset=28
                                local.get $l17
                                i32.const 12
                                i32.mul
                                i32.add
                                local.tee $p4
                                i32.load offset=8
                                local.set $l15
                                local.get $p4
                                i32.load
                                local.set $l23
                                local.get $p4
                                i32.load offset=4
                              end
                              local.set $l24
                              local.get $l9
                              local.get $l14
                              i32.const 40
                              i32.mul
                              i32.add
                              local.tee $p4
                              local.get $l19
                              i32.load offset=24
                              local.tee $l30
                              local.get $l23
                              i32.const 12
                              i32.mul
                              i32.add
                              local.tee $l23
                              f32.load
                              f32.store
                              local.get $p4
                              local.get $l23
                              f32.load offset=4
                              f32.store offset=4
                              local.get $p4
                              local.get $l23
                              f32.load offset=8
                              f32.store offset=8
                              local.get $p4
                              local.get $l30
                              local.get $l15
                              local.get $l24
                              local.get $l43
                              f32.const 0x0p+0 (;=0;)
                              f32.lt
                              local.tee $l28
                              select
                              i32.const 12
                              i32.mul
                              i32.add
                              local.tee $l23
                              f32.load
                              f32.store offset=12
                              local.get $p4
                              local.get $l23
                              f32.load offset=4
                              f32.store offset=16
                              local.get $p4
                              local.get $l23
                              f32.load offset=8
                              f32.store offset=20
                              local.get $p4
                              local.get $l30
                              local.get $l24
                              local.get $l15
                              local.get $l28
                              select
                              i32.const 12
                              i32.mul
                              i32.add
                              local.tee $l15
                              f32.load
                              f32.store offset=24
                              local.get $p4
                              local.get $l15
                              f32.load offset=4
                              f32.store offset=28
                              local.get $p4
                              local.get $l15
                              f32.load offset=8
                              f32.store offset=32
                              local.get $p4
                              local.get $l33
                              if $I24 (result i32)
                                local.get $l17
                                local.get $l33
                                i32.add
                                i32.load8_u
                              else
                                i32.const 56
                              end
                              i32.store8 offset=36
                              local.get $l14
                              i32.const 1
                              i32.add
                              local.tee $l14
                              local.get $l26
                              i32.ne
                              br_if $L21
                            end
                            local.get $l9
                            i32.const 6088
                            i32.add
                            local.get $l9
                            i32.const 1456
                            i32.add
                            i32.load
                            i32.store
                            local.get $l9
                            local.get $l9
                            i64.load offset=1448 align=4
                            i64.store offset=6080
                            i32.const 0
                            local.set $l15
                            local.get $l35
                            i32.eqz
                            br_if $B19
                            i32.const 0
                            local.set $l20
                            loop $L25
                              local.get $l9
                              i32.const 0
                              i32.store offset=1980
                              local.get $l9
                              i32.const 1464
                              i32.add
                              local.get $l9
                              i32.const 1616
                              i32.add
                              local.get $l9
                              local.get $l20
                              i32.const 40
                              i32.mul
                              i32.add
                              local.tee $p4
                              local.get $l20
                              local.get $l34
                              i32.add
                              local.tee $p0
                              local.get $p4
                              i32.load8_u offset=36
                              local.get $l9
                              i32.const 1600
                              i32.add
                              local.get $l32
                              local.get $l9
                              i32.const 1872
                              i32.add
                              local.get $l9
                              i32.const 1280
                              i32.add
                              local.get $l9
                              i32.const 1984
                              i32.add
                              local.get $l9
                              i32.const 1980
                              i32.add
                              call $f70063
                              block $B26
                                local.get $l9
                                i32.load offset=1980
                                local.tee $p4
                                i32.eqz
                                br_if $B26
                                i32.const 0
                                local.set $l14
                                local.get $l9
                                f32.load offset=2028
                                local.set $l43
                                block $B27
                                  local.get $p4
                                  i32.const 1
                                  i32.eq
                                  br_if $B27
                                  local.get $p4
                                  i32.const 1
                                  i32.sub
                                  local.tee $l14
                                  i32.const 3
                                  i32.and
                                  local.set $l15
                                  block $B28
                                    local.get $p4
                                    i32.const 2
                                    i32.sub
                                    i32.const 3
                                    i32.lt_u
                                    if $I29
                                      i32.const 0
                                      local.set $l14
                                      i32.const 1
                                      local.set $p4
                                      br $B28
                                    end
                                    local.get $l14
                                    i32.const -4
                                    i32.and
                                    local.set $l24
                                    i32.const 0
                                    local.set $l14
                                    i32.const 1
                                    local.set $p4
                                    loop $L30
                                      local.get $p4
                                      i32.const 3
                                      i32.add
                                      local.tee $l30
                                      i32.const 6
                                      i32.shl
                                      local.get $l9
                                      i32.add
                                      i32.const 2028
                                      i32.add
                                      f32.load
                                      local.tee $l55
                                      local.get $p4
                                      i32.const 2
                                      i32.add
                                      local.tee $l23
                                      i32.const 6
                                      i32.shl
                                      local.get $l9
                                      i32.add
                                      i32.const 2028
                                      i32.add
                                      f32.load
                                      local.tee $l58
                                      local.get $p4
                                      i32.const 1
                                      i32.add
                                      local.tee $l17
                                      i32.const 6
                                      i32.shl
                                      local.get $l9
                                      i32.add
                                      i32.const 2028
                                      i32.add
                                      f32.load
                                      local.tee $l50
                                      local.get $p4
                                      i32.const 6
                                      i32.shl
                                      local.get $l9
                                      i32.add
                                      i32.const 2028
                                      i32.add
                                      f32.load
                                      local.tee $l59
                                      local.get $l43
                                      local.get $l43
                                      local.get $l59
                                      f32.gt
                                      local.tee $l28
                                      select
                                      local.tee $l43
                                      local.get $l43
                                      local.get $l50
                                      f32.gt
                                      local.tee $l26
                                      select
                                      local.tee $l43
                                      local.get $l43
                                      local.get $l58
                                      f32.gt
                                      local.tee $l27
                                      select
                                      local.tee $l43
                                      local.get $l43
                                      local.get $l55
                                      f32.gt
                                      local.tee $l41
                                      select
                                      local.set $l43
                                      local.get $l30
                                      local.get $l23
                                      local.get $l17
                                      local.get $p4
                                      local.get $l14
                                      local.get $l28
                                      select
                                      local.get $l26
                                      select
                                      local.get $l27
                                      select
                                      local.get $l41
                                      select
                                      local.set $l14
                                      local.get $p4
                                      i32.const 4
                                      i32.add
                                      local.set $p4
                                      local.get $l24
                                      i32.const 4
                                      i32.sub
                                      local.tee $l24
                                      br_if $L30
                                    end
                                  end
                                  local.get $l15
                                  i32.eqz
                                  br_if $B27
                                  loop $L31
                                    local.get $p4
                                    i32.const 6
                                    i32.shl
                                    local.get $l9
                                    i32.add
                                    i32.const 2028
                                    i32.add
                                    f32.load
                                    local.tee $l55
                                    local.get $l43
                                    local.get $l43
                                    local.get $l55
                                    f32.gt
                                    local.tee $l24
                                    select
                                    local.set $l43
                                    local.get $p4
                                    local.get $l14
                                    local.get $l24
                                    select
                                    local.set $l14
                                    local.get $p4
                                    i32.const 1
                                    i32.add
                                    local.set $p4
                                    local.get $l15
                                    i32.const 1
                                    i32.sub
                                    local.tee $l15
                                    br_if $L31
                                  end
                                end
                                i32.const 1
                                local.set $l15
                                local.get $p5
                                local.get $l43
                                f32.gt
                                i32.eqz
                                br_if $B26
                                local.get $l9
                                i32.const 1984
                                i32.add
                                local.get $l14
                                i32.const 6
                                i32.shl
                                i32.add
                                local.tee $p4
                                f32.load offset=16
                                local.set $l78
                                local.get $p4
                                f32.load offset=32
                                local.set $l70
                                local.get $p4
                                f32.load offset=24
                                local.set $l80
                                local.get $p4
                                f32.load offset=20
                                local.set $l77
                                local.get $p4
                                f32.load offset=40
                                local.set $l79
                                local.get $p4
                                f32.load offset=36
                                local.set $l81
                                local.get $p0
                                local.set $p6
                                local.get $l43
                                local.set $p5
                              end
                              local.get $l20
                              i32.const 1
                              i32.add
                              local.tee $l20
                              local.get $l35
                              i32.ne
                              br_if $L25
                            end
                            local.get $l15
                            local.get $l25
                            i32.or
                            local.set $l25
                            br $B19
                          end
                          local.get $l9
                          i32.const 6088
                          i32.add
                          local.get $l9
                          i32.const 1456
                          i32.add
                          i32.load
                          i32.store
                          local.get $l9
                          local.get $l9
                          i64.load offset=1448 align=4
                          i64.store offset=6080
                        end
                        local.get $l9
                        i32.const 1456
                        i32.add
                        local.get $l9
                        i32.const 6088
                        i32.add
                        i32.load
                        i32.store
                        local.get $l9
                        local.get $l9
                        i64.load offset=6080
                        i64.store offset=1448
                        local.get $p7
                        i32.const 32
                        i32.sub
                        local.set $p7
                        local.get $l21
                        i32.const 1
                        i32.add
                        local.tee $l21
                        local.get $l40
                        i32.ne
                        br_if $L18
                      end
                      local.get $l25
                      i32.const 1
                      i32.and
                      i32.eqz
                      br_if $B17
                      local.get $l9
                      f32.load offset=1896
                      local.get $l9
                      f32.load offset=1880
                      local.tee $l43
                      local.get $l78
                      local.get $l9
                      f32.load offset=1872
                      local.tee $l55
                      f32.mul
                      local.get $l77
                      local.get $l9
                      f32.load offset=1876
                      local.tee $l58
                      f32.mul
                      f32.add
                      local.get $l80
                      local.get $l43
                      f32.mul
                      f32.add
                      local.tee $l66
                      f32.mul
                      local.get $l9
                      f32.load offset=1884
                      local.tee $l50
                      local.get $l77
                      local.get $l55
                      f32.mul
                      local.get $l78
                      local.get $l58
                      f32.mul
                      f32.sub
                      f32.mul
                      local.get $l80
                      local.get $l50
                      local.get $l50
                      f32.mul
                      f32.const -0x1p-1 (;=-0.5;)
                      f32.add
                      local.tee $l59
                      f32.mul
                      f32.add
                      f32.add
                      local.tee $l63
                      local.get $l63
                      f32.add
                      f32.add
                      local.set $l64
                      local.get $l9
                      f32.load offset=1892
                      local.get $l58
                      local.get $l66
                      f32.mul
                      local.get $l50
                      local.get $l78
                      local.get $l43
                      f32.mul
                      local.get $l80
                      local.get $l55
                      f32.mul
                      f32.sub
                      f32.mul
                      local.get $l77
                      local.get $l59
                      f32.mul
                      f32.add
                      f32.add
                      local.tee $l63
                      local.get $l63
                      f32.add
                      f32.add
                      local.set $l67
                      local.get $l9
                      f32.load offset=1888
                      local.get $l55
                      local.get $l66
                      f32.mul
                      local.get $l50
                      local.get $l80
                      local.get $l58
                      f32.mul
                      local.get $l77
                      local.get $l43
                      f32.mul
                      f32.sub
                      f32.mul
                      local.get $l78
                      local.get $l59
                      f32.mul
                      f32.add
                      f32.add
                      local.tee $l66
                      local.get $l66
                      f32.add
                      f32.add
                      local.set $l68
                      local.get $l43
                      local.get $l70
                      local.get $l55
                      f32.mul
                      local.get $l81
                      local.get $l58
                      f32.mul
                      f32.add
                      local.get $l79
                      local.get $l43
                      f32.mul
                      f32.add
                      local.tee $l66
                      f32.mul
                      local.get $l50
                      local.get $l81
                      local.get $l55
                      f32.mul
                      local.get $l70
                      local.get $l58
                      f32.mul
                      f32.sub
                      f32.mul
                      local.get $l79
                      local.get $l59
                      f32.mul
                      f32.add
                      f32.add
                      local.tee $l63
                      local.get $l63
                      f32.add
                      local.set $l71
                      local.get $l58
                      local.get $l66
                      f32.mul
                      local.get $l50
                      local.get $l70
                      local.get $l43
                      f32.mul
                      local.get $l79
                      local.get $l55
                      f32.mul
                      f32.sub
                      f32.mul
                      local.get $l81
                      local.get $l59
                      f32.mul
                      f32.add
                      f32.add
                      local.tee $l63
                      local.get $l63
                      f32.add
                      local.set $l63
                      local.get $l55
                      local.get $l66
                      f32.mul
                      local.get $l50
                      local.get $l79
                      local.get $l58
                      f32.mul
                      local.get $l81
                      local.get $l43
                      f32.mul
                      f32.sub
                      f32.mul
                      local.get $l70
                      local.get $l59
                      f32.mul
                      f32.add
                      f32.add
                      local.tee $l43
                      local.get $l43
                      f32.add
                      local.set $l43
                      local.get $l9
                      i32.load offset=1584
                      local.get $p6
                      i32.const 2
                      i32.shl
                      i32.add
                      i32.load
                      local.set $p6
                      local.get $p5
                      f32.const 0x0p+0 (;=0;)
                      f32.le
                      i32.eqz
                      if $I32
                        i32.const 1
                        local.set $l29
                        local.get $l31
                        br_if $B17
                        local.get $l12
                        local.get $l71
                        f32.store offset=36
                        local.get $l12
                        local.get $l63
                        f32.store offset=32
                        local.get $l12
                        local.get $l43
                        f32.store offset=28
                        local.get $l12
                        local.get $l64
                        f32.store offset=24
                        local.get $l12
                        local.get $l67
                        f32.store offset=20
                        local.get $l12
                        local.get $l68
                        f32.store offset=16
                        local.get $l12
                        i32.const 0
                        i32.store offset=40
                        local.get $l12
                        local.get $p6
                        i32.store offset=8
                        br $B15
                      end
                      local.get $l91
                      local.get $p5
                      local.get $l71
                      f32.mul
                      local.tee $l55
                      f32.sub
                      local.set $l91
                      local.get $l90
                      local.get $p5
                      local.get $l63
                      f32.mul
                      local.tee $l58
                      f32.sub
                      local.set $l90
                      local.get $l92
                      local.get $p5
                      local.get $l43
                      f32.mul
                      local.tee $l43
                      f32.sub
                      local.set $l92
                      local.get $l51
                      local.get $l55
                      f32.sub
                      local.set $l51
                      local.get $l52
                      local.get $l58
                      f32.sub
                      local.set $l52
                      local.get $l53
                      local.get $l43
                      f32.sub
                      local.set $l53
                      i32.const 1
                      local.set $l29
                      local.get $l31
                      i32.const 1
                      i32.add
                      local.tee $l31
                      i32.const 2
                      i32.ne
                      br_if $L16
                    end
                  end
                  i32.const 0
                  local.get $l29
                  i32.eqz
                  br_if $B14
                  drop
                  local.get $l12
                  local.get $l64
                  f32.store offset=24
                  local.get $l12
                  local.get $l67
                  f32.store offset=20
                  local.get $l12
                  local.get $l68
                  f32.store offset=16
                  local.get $l12
                  local.get $p6
                  i32.store offset=8
                  local.get $l12
                  local.get $l51
                  local.get $l51
                  f32.mul
                  local.get $l52
                  local.get $l52
                  f32.mul
                  local.get $l53
                  local.get $l53
                  f32.mul
                  f32.add
                  f32.add
                  f32.sqrt
                  local.tee $l43
                  f32.neg
                  f32.store offset=40
                  local.get $l12
                  local.get $l51
                  f32.const 0x1p+0 (;=1;)
                  local.get $l43
                  f32.div
                  local.tee $l55
                  f32.mul
                  f32.const 0x0p+0 (;=0;)
                  local.get $l43
                  f32.const 0x0p+0 (;=0;)
                  f32.gt
                  local.tee $p4
                  select
                  f32.store offset=36
                  local.get $l12
                  local.get $l52
                  local.get $l55
                  f32.mul
                  f32.const 0x0p+0 (;=0;)
                  local.get $p4
                  select
                  f32.store offset=32
                  local.get $l12
                  local.get $l53
                  local.get $l55
                  f32.mul
                  f32.const 0x0p+0 (;=0;)
                  local.get $p4
                  select
                  f32.store offset=28
                end
                i32.const 1
              end
              local.set $p4
              block $B33
                local.get $l9
                i32.load offset=1592
                local.tee $l14
                i32.const 0
                i32.lt_s
                br_if $B33
                local.get $l14
                i32.const 2147483647
                i32.and
                i32.eqz
                br_if $B33
                local.get $l9
                i32.load offset=1584
                local.tee $l14
                i32.eqz
                br_if $B33
                call $f69753
                local.tee $l15
                local.get $l14
                local.get $l15
                i32.load
                i32.load offset=12
                call_indirect $__indirect_function_table (type $t1)
              end
              local.get $l9
              i32.const 6096
              i32.add
              global.set $g0
              local.get $l12
              i32.const 1026
              i32.store16 offset=12
              local.get $p4
              br_if $B9
            end
            local.get $l12
            i32.const 0
            i32.store offset=40
            local.get $l18
            f32.load
            local.set $p8
            local.get $l18
            f32.load offset=4
            local.set $l65
            local.get $l12
            local.get $l18
            f32.load offset=8
            f32.neg
            f32.store offset=36
            local.get $l12
            local.get $l65
            f32.neg
            f32.store offset=32
            local.get $l12
            local.get $p8
            f32.neg
            f32.store offset=28
            br $B8
          end
          local.get $l12
          f32.load offset=40
          f32.const 0x0p+0 (;=0;)
          f32.eq
          if $I34
            local.get $l18
            f32.load
            local.set $p8
            local.get $l18
            f32.load offset=4
            local.set $l65
            local.get $l12
            local.get $l18
            f32.load offset=8
            f32.neg
            f32.store offset=36
            local.get $l12
            local.get $l65
            f32.neg
            f32.store offset=32
            local.get $l12
            local.get $p8
            f32.neg
            f32.store offset=28
          end
          local.get $l12
          i32.const 1027
          i32.store16 offset=12
        end
        local.get $l12
        local.get $l11
        i32.load offset=332
        i32.store offset=8
        br $B6
      end
      local.get $l12
      local.get $l11
      i64.load offset=324 align=4
      i64.store align=4
      local.get $l12
      local.get $l11
      i32.load offset=332
      i32.store offset=8
      local.get $l12
      local.get $l11
      i32.load16_u offset=336
      i32.store16 offset=12
      local.get $l12
      local.get $l11
      f32.load offset=340
      f32.store offset=16
      local.get $l12
      local.get $l11
      f32.load offset=344
      f32.store offset=20
      local.get $l12
      local.get $l11
      f32.load offset=348
      f32.store offset=24
      local.get $l12
      local.get $l11
      f32.load offset=352
      local.tee $p8
      f32.store offset=28
      local.get $l12
      i32.const 32
      i32.add
      local.tee $p7
      local.get $l11
      f32.load offset=356
      local.tee $l65
      f32.store
      local.get $l12
      i32.const 36
      i32.add
      local.tee $p0
      local.get $l11
      f32.load offset=360
      local.tee $l72
      f32.store
      local.get $l12
      local.get $l11
      f32.load offset=364
      f32.store offset=40
      local.get $l11
      i32.load offset=368
      local.set $p2
      local.get $p0
      local.get $l72
      f32.neg
      local.tee $l47
      f32.store
      local.get $p7
      local.get $l65
      f32.neg
      local.tee $l48
      f32.store
      local.get $l12
      local.get $p8
      f32.neg
      local.tee $l49
      f32.store offset=28
      local.get $l12
      local.get $p2
      i32.store offset=44
      local.get $p8
      local.get $p8
      f32.mul
      local.get $l65
      local.get $l65
      f32.mul
      f32.add
      local.get $l72
      local.get $l72
      f32.mul
      f32.add
      f32.sqrt
      local.tee $p8
      f32.const 0x0p+0 (;=0;)
      f32.gt
      if $I35
        local.get $l12
        f32.const 0x1p+0 (;=1;)
        local.get $p8
        f32.div
        local.tee $p8
        local.get $l47
        f32.mul
        local.tee $l47
        f32.store offset=36
        local.get $l12
        local.get $p8
        local.get $l48
        f32.mul
        local.tee $l48
        f32.store offset=32
        local.get $l12
        local.get $p8
        local.get $l49
        f32.mul
        local.tee $l49
        f32.store offset=28
      end
      local.get $p6
      i32.eqz
      br_if $B6
      local.get $l13
      br_if $B6
      local.get $l18
      f32.load offset=8
      local.get $l11
      f32.load offset=32
      local.get $l11
      f32.load offset=20
      local.tee $p8
      f32.sub
      local.tee $l73
      local.get $l11
      f32.load offset=48
      local.get $l11
      f32.load offset=24
      local.tee $l65
      f32.sub
      local.tee $l74
      f32.mul
      local.get $l11
      f32.load offset=36
      local.get $l65
      f32.sub
      local.tee $l88
      local.get $l11
      f32.load offset=44
      local.get $p8
      f32.sub
      local.tee $l89
      f32.mul
      f32.sub
      local.tee $p8
      local.get $p8
      f32.add
      local.tee $l65
      local.get $p1
      f32.load offset=12
      local.tee $p8
      local.get $p8
      f32.mul
      f32.const -0x1p-1 (;=-0.5;)
      f32.add
      local.tee $l43
      f32.mul
      local.get $p8
      local.get $p1
      f32.load
      local.tee $l72
      local.get $l11
      f32.load offset=40
      local.get $l11
      f32.load offset=28
      local.tee $l82
      f32.sub
      local.tee $p5
      local.get $l89
      f32.mul
      local.get $l73
      local.get $l11
      f32.load offset=52
      local.get $l82
      f32.sub
      local.tee $l82
      f32.mul
      f32.sub
      local.tee $l73
      local.get $l73
      f32.add
      local.tee $l73
      f32.mul
      local.get $p1
      f32.load offset=4
      local.tee $l89
      local.get $l88
      local.get $l82
      f32.mul
      local.get $p5
      local.get $l74
      f32.mul
      f32.sub
      local.tee $l74
      local.get $l74
      f32.add
      local.tee $l74
      f32.mul
      f32.sub
      f32.mul
      f32.add
      local.get $p1
      f32.load offset=8
      local.tee $l88
      local.get $l65
      local.get $l88
      f32.mul
      local.get $l72
      local.get $l74
      f32.mul
      local.get $l89
      local.get $l73
      f32.mul
      f32.add
      f32.add
      local.tee $l82
      f32.mul
      f32.add
      f32.mul
      local.get $l18
      f32.load
      local.get $l72
      local.get $l82
      f32.mul
      local.get $l43
      local.get $l74
      f32.mul
      local.get $p8
      local.get $l65
      local.get $l89
      f32.mul
      local.get $l73
      local.get $l88
      f32.mul
      f32.sub
      f32.mul
      f32.add
      f32.add
      f32.mul
      local.get $l18
      f32.load offset=4
      local.get $l89
      local.get $l82
      f32.mul
      local.get $l43
      local.get $l73
      f32.mul
      local.get $p8
      local.get $l74
      local.get $l88
      f32.mul
      local.get $l72
      local.get $l65
      f32.mul
      f32.sub
      f32.mul
      f32.add
      f32.add
      f32.mul
      f32.add
      f32.add
      f32.const 0x0p+0 (;=0;)
      f32.gt
      i32.eqz
      br_if $B6
      local.get $l12
      local.get $l47
      f32.neg
      f32.store offset=36
      local.get $l12
      local.get $l48
      f32.neg
      f32.store offset=32
      local.get $l12
      local.get $l49
      f32.neg
      f32.store offset=28
    end
    local.get $l42
    i32.const 0
    i32.ne
    local.set $p1
    local.get $l10
    i32.const 784
    i32.add
    global.set $g0
    local.get $p1)
