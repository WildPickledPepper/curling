  (func $f70546 (type $t18) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 i32) (param $p7 i32) (result i32)
    (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32) (local $l33 f32) (local $l34 f32) (local $l35 f32) (local $l36 f32) (local $l37 f32) (local $l38 f32) (local $l39 f32) (local $l40 f32) (local $l41 f32) (local $l42 f32) (local $l43 f32) (local $l44 f32) (local $l45 f32) (local $l46 f32) (local $l47 f32) (local $l48 f32) (local $l49 f32) (local $l50 f32) (local $l51 f32) (local $l52 f32) (local $l53 f32) (local $l54 i64)
    local.get $p6
    local.set $p7
    global.get $g0
    i32.const 8544
    i32.sub
    local.tee $l8
    global.set $g0
    local.get $p1
    i32.load offset=32
    local.set $l9
    local.get $p0
    f32.load offset=8
    local.set $l22
    local.get $p1
    i32.const 8
    i32.add
    local.tee $l10
    f32.load
    local.set $l29
    local.get $p1
    f32.load offset=12
    local.set $l31
    local.get $p1
    f32.load offset=4
    local.set $l32
    local.get $l8
    i32.const 0
    i32.store offset=284
    local.get $l8
    local.get $l31
    f32.store offset=280
    local.get $l8
    local.get $l29
    f32.store offset=276
    local.get $l8
    local.get $l32
    f32.store offset=272
    local.get $p1
    i32.const 16
    i32.add
    local.tee $l11
    i64.load align=4
    local.set $l54
    local.get $l8
    local.get $p1
    i64.load offset=24 align=4
    i64.store offset=264
    local.get $l8
    local.get $l54
    i64.store offset=256
    local.get $p3
    local.tee $p5
    f32.load offset=4
    local.tee $l17
    local.get $p2
    local.tee $p3
    f32.load
    local.tee $l21
    f32.mul
    local.get $p5
    f32.load offset=12
    local.tee $l16
    local.get $p3
    f32.load offset=8
    local.tee $l20
    f32.mul
    local.get $p5
    f32.load offset=8
    local.tee $l18
    local.get $p3
    f32.load offset=12
    local.tee $l24
    f32.mul
    f32.sub
    local.get $p5
    f32.load
    local.tee $l19
    local.get $p3
    f32.load offset=4
    local.tee $l23
    f32.mul
    f32.sub
    f32.add
    local.tee $l25
    local.get $l19
    local.get $l20
    f32.mul
    local.get $l16
    local.get $l23
    f32.mul
    local.get $l17
    local.get $l24
    f32.mul
    f32.sub
    local.get $l18
    local.get $l21
    f32.mul
    f32.sub
    f32.add
    local.tee $l26
    local.get $l26
    f32.add
    local.tee $l30
    f32.mul
    local.tee $l28
    local.get $l16
    local.get $l21
    f32.mul
    local.get $l19
    local.get $l24
    f32.mul
    f32.sub
    local.get $l17
    local.get $l20
    f32.mul
    f32.sub
    local.get $l18
    local.get $l23
    f32.mul
    f32.add
    local.tee $l34
    local.get $l34
    f32.add
    local.tee $l27
    local.get $l18
    local.get $l20
    f32.mul
    local.get $l19
    local.get $l21
    f32.mul
    local.get $l16
    local.get $l24
    f32.mul
    f32.add
    local.get $l17
    local.get $l23
    f32.mul
    f32.add
    f32.add
    local.tee $l21
    f32.mul
    local.tee $l20
    f32.sub
    local.set $l35
    local.get $l27
    local.get $l25
    f32.mul
    local.tee $l24
    local.get $l21
    local.get $l30
    f32.mul
    local.tee $l23
    f32.add
    local.set $l36
    local.get $l20
    local.get $l28
    f32.add
    local.set $l41
    local.get $l27
    local.get $l26
    f32.mul
    local.tee $l20
    local.get $l21
    local.get $l25
    local.get $l25
    f32.add
    local.tee $l38
    f32.mul
    local.tee $l21
    f32.sub
    local.set $l39
    local.get $l24
    local.get $l23
    f32.sub
    local.set $l40
    local.get $l20
    local.get $l21
    f32.add
    local.set $l42
    local.get $l16
    local.get $l16
    f32.mul
    f32.const -0x1p-1 (;=-0.5;)
    f32.add
    local.tee $l33
    local.get $p3
    f32.load offset=24
    local.get $p5
    f32.load offset=24
    f32.sub
    local.tee $l21
    local.get $l21
    f32.add
    local.tee $l24
    f32.mul
    local.get $l16
    local.get $l17
    local.get $p3
    f32.load offset=16
    local.get $p5
    f32.load offset=16
    f32.sub
    local.tee $l21
    local.get $l21
    f32.add
    local.tee $l23
    f32.mul
    local.get $l19
    local.get $p3
    f32.load offset=20
    local.get $p5
    f32.load offset=20
    f32.sub
    local.tee $l21
    local.get $l21
    f32.add
    local.tee $l28
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l18
    local.get $l28
    local.get $l17
    f32.neg
    f32.mul
    local.get $l19
    local.get $l23
    f32.mul
    f32.sub
    local.get $l18
    local.get $l24
    f32.mul
    f32.sub
    local.tee $l37
    f32.mul
    f32.sub
    local.set $l21
    local.get $l33
    local.get $l28
    f32.mul
    local.get $l16
    local.get $l19
    local.get $l24
    f32.mul
    local.get $l18
    local.get $l23
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l17
    local.get $l37
    f32.mul
    f32.sub
    local.set $l20
    local.get $l33
    local.get $l23
    f32.mul
    local.get $l16
    local.get $l18
    local.get $l28
    f32.mul
    local.get $l17
    local.get $l24
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l19
    local.get $l37
    f32.mul
    f32.sub
    local.set $l17
    f32.const 0x1p+0 (;=1;)
    local.get $l34
    local.get $l27
    f32.mul
    f32.sub
    local.tee $l16
    local.get $l26
    local.get $l30
    f32.mul
    local.tee $l18
    f32.sub
    local.set $l19
    local.get $l16
    local.get $l25
    local.get $l38
    f32.mul
    local.tee $l25
    f32.sub
    local.set $l23
    f32.const 0x1p+0 (;=1;)
    local.get $l18
    f32.sub
    local.get $l25
    f32.sub
    local.set $l18
    local.get $l9
    i32.const 16
    i32.add
    local.set $p2
    block $B0 (result i32)
      i32.const 0
      local.get $p1
      f32.load offset=4
      f32.const 0x1p+0 (;=1;)
      f32.ne
      br_if $B0
      drop
      i32.const 0
      local.get $l10
      f32.load
      f32.const 0x1p+0 (;=1;)
      f32.ne
      br_if $B0
      drop
      local.get $p1
      f32.load offset=12
      f32.const 0x1p+0 (;=1;)
      f32.eq
    end
    local.set $p6
    local.get $l8
    i32.const 0
    i32.store8 offset=384
    local.get $l8
    i32.const 376
    i32.add
    local.tee $l10
    i64.const 0
    i64.store
    local.get $l8
    i32.const 368
    i32.add
    local.tee $l12
    i64.const 0
    i64.store
    local.get $l8
    i64.const 0
    i64.store offset=360
    local.get $l8
    i64.const 0
    i64.store offset=352
    local.get $l8
    local.get $p2
    i32.store offset=496
    local.get $l8
    local.get $l9
    i32.load offset=56
    local.get $l9
    i32.load8_u offset=55
    i32.const 20
    i32.mul
    i32.add
    i32.store offset=504
    local.get $l8
    local.get $l9
    i32.load8_u offset=54
    i32.store8 offset=508
    local.get $l10
    local.get $l32
    local.get $l9
    f32.load offset=68
    f32.mul
    local.tee $l16
    local.get $l29
    local.get $l9
    f32.load offset=72
    f32.mul
    local.tee $l25
    local.get $l16
    local.get $l25
    f32.le
    select
    local.tee $l16
    local.get $l31
    local.get $l9
    f32.load offset=76
    f32.mul
    local.tee $l25
    local.get $l16
    local.get $l25
    f32.le
    select
    local.tee $l16
    f32.const 0x1.99999ap-6 (;=0.025;)
    f32.mul
    f32.store
    local.get $l12
    local.get $l16
    f32.const 0x1.99999ap-4 (;=0.1;)
    f32.mul
    f32.store
    local.get $l8
    local.get $l16
    f32.const 0x1.99999ap-5 (;=0.05;)
    f32.mul
    f32.store offset=372
    local.get $l8
    i32.const 272
    i32.add
    local.get $l8
    i32.const 256
    i32.add
    local.get $l8
    i32.const 400
    i32.add
    local.get $l8
    i32.const 448
    i32.add
    local.get $l8
    i32.const 352
    i32.add
    local.get $p6
    call $f70494
    local.get $l8
    local.get $l9
    i32.load offset=60
    i32.store offset=500
    local.get $l8
    i64.const 0
    i64.store offset=236 align=4
    local.get $l8
    i32.const 0
    i32.store offset=220
    f32.const 0x0p+0 (;=0;)
    local.set $l24
    local.get $l8
    local.get $l21
    f32.store offset=168
    local.get $l8
    local.get $l21
    local.get $l22
    f32.const 0x0p+0 (;=0;)
    f32.mul
    local.tee $l16
    local.get $l19
    f32.mul
    local.get $l22
    local.get $l40
    f32.mul
    local.get $l16
    local.get $l41
    f32.mul
    f32.add
    f32.add
    local.tee $l19
    f32.sub
    f32.store offset=232
    local.get $l8
    local.get $l20
    f32.store offset=164
    local.get $l8
    local.get $l20
    local.get $l22
    local.get $l42
    f32.mul
    local.get $l16
    local.get $l23
    f32.mul
    f32.add
    local.get $l16
    local.get $l35
    f32.mul
    f32.add
    local.tee $l25
    f32.sub
    f32.store offset=228
    local.get $l8
    local.get $l21
    local.get $l19
    f32.add
    f32.store offset=216
    local.get $l8
    local.get $l20
    local.get $l25
    f32.add
    f32.store offset=212
    local.get $l8
    i64.const 17179869184
    i64.store offset=184
    local.get $l8
    i32.const 0
    i32.store offset=172
    local.get $l8
    i32.const 1
    i32.store8 offset=192
    local.get $l8
    i64.const 0
    i64.store offset=176
    local.get $l8
    local.get $l17
    f32.store offset=160
    local.get $l8
    local.get $l17
    local.get $l16
    local.get $l36
    f32.mul
    local.get $l16
    local.get $l39
    f32.mul
    local.get $l22
    local.get $l18
    f32.mul
    f32.add
    f32.add
    local.tee $l16
    f32.sub
    f32.store offset=224
    local.get $l8
    local.get $l17
    local.get $l16
    f32.add
    f32.store offset=208
    local.get $l8
    i32.const 3132488
    i32.store offset=320
    local.get $l8
    local.get $l8
    i32.const 160
    i32.add
    i32.store offset=324
    local.get $l8
    i32.const 3132572
    i32.store offset=304
    local.get $l8
    local.get $l8
    i32.const 352
    i32.add
    i32.store offset=308
    local.get $l8
    i32.const 0
    i32.store offset=156
    local.get $l8
    local.get $l21
    local.get $l8
    f32.load offset=360
    f32.sub
    f32.store offset=152
    local.get $l8
    local.get $l20
    local.get $l8
    f32.load offset=356
    f32.sub
    f32.store offset=148
    local.get $l8
    local.get $l17
    local.get $l8
    f32.load offset=352
    f32.sub
    f32.store offset=144
    local.get $l8
    i32.const 2139095039
    i32.store offset=128
    local.get $l8
    i32.const 320
    i32.add
    local.get $l8
    i32.const 304
    i32.add
    local.get $l8
    i32.const 144
    i32.add
    local.get $l8
    i32.const 128
    i32.add
    local.get $l8
    i32.const 16
    i32.add
    local.get $l8
    i32.const 96
    i32.add
    local.get $l8
    i32.const 336
    i32.add
    local.get $l8
    i32.const 288
    i32.add
    call $f70321
    i32.const 2
    i32.ne
    if $I1
      local.get $l8
      f32.load offset=344
      local.tee $l16
      local.get $l16
      f32.add
      local.tee $l22
      local.get $p5
      f32.load offset=12
      local.tee $l16
      local.get $l16
      f32.mul
      f32.const -0x1p-1 (;=-0.5;)
      f32.add
      local.tee $l20
      f32.mul
      local.get $l16
      local.get $l8
      f32.load offset=340
      local.tee $l17
      local.get $l17
      f32.add
      local.tee $l24
      local.get $p5
      f32.load
      local.tee $l17
      f32.mul
      local.get $l8
      f32.load offset=336
      local.tee $l18
      local.get $l18
      f32.add
      local.tee $l23
      local.get $p5
      f32.load offset=4
      local.tee $l18
      f32.mul
      f32.sub
      f32.mul
      f32.add
      local.get $p5
      f32.load offset=8
      local.tee $l19
      local.get $l23
      local.get $l17
      f32.mul
      local.get $l24
      local.get $l18
      f32.mul
      f32.add
      local.get $l22
      local.get $l19
      f32.mul
      f32.add
      local.tee $l26
      f32.mul
      f32.add
      local.set $l25
      local.get $l18
      local.get $l26
      f32.mul
      local.get $l24
      local.get $l20
      f32.mul
      local.get $l16
      local.get $l23
      local.get $l19
      f32.mul
      local.get $l22
      local.get $l17
      f32.mul
      f32.sub
      f32.mul
      f32.add
      f32.add
      local.set $l21
      local.get $l17
      local.get $l26
      f32.mul
      local.get $l23
      local.get $l20
      f32.mul
      local.get $l16
      local.get $l22
      local.get $l18
      f32.mul
      local.get $l24
      local.get $l19
      f32.mul
      f32.sub
      f32.mul
      f32.add
      f32.add
      local.set $l22
      local.get $p5
      f32.load offset=24
      local.get $l8
      f32.load offset=104
      local.tee $l24
      local.get $l24
      f32.add
      local.tee $l24
      local.get $l20
      f32.mul
      local.get $l16
      local.get $l8
      f32.load offset=100
      local.tee $l23
      local.get $l23
      f32.add
      local.tee $l23
      local.get $l17
      f32.mul
      local.get $l8
      f32.load offset=96
      local.tee $l26
      local.get $l26
      f32.add
      local.tee $l26
      local.get $l18
      f32.mul
      f32.sub
      f32.mul
      f32.add
      local.get $l19
      local.get $l26
      local.get $l17
      f32.mul
      local.get $l23
      local.get $l18
      f32.mul
      f32.add
      local.get $l24
      local.get $l19
      f32.mul
      f32.add
      local.tee $l27
      f32.mul
      f32.add
      f32.add
      local.set $l46
      local.get $p5
      f32.load offset=20
      local.get $l18
      local.get $l27
      f32.mul
      local.get $l23
      local.get $l20
      f32.mul
      local.get $l16
      local.get $l26
      local.get $l19
      f32.mul
      local.get $l24
      local.get $l17
      f32.mul
      f32.sub
      f32.mul
      f32.add
      f32.add
      f32.add
      local.set $l47
      local.get $p5
      f32.load offset=16
      local.get $l17
      local.get $l27
      f32.mul
      local.get $l26
      local.get $l20
      f32.mul
      local.get $l16
      local.get $l24
      local.get $l18
      f32.mul
      local.get $l23
      local.get $l19
      f32.mul
      f32.sub
      f32.mul
      f32.add
      f32.add
      f32.add
      local.set $l48
      local.get $l8
      f32.load offset=288
      local.set $l24
    end
    block $B2 (result i32)
      i32.const 0
      local.get $l24
      local.get $p0
      f32.load offset=4
      local.get $p4
      f32.load
      f32.add
      f32.ge
      br_if $B2
      drop
      local.get $p1
      i32.const 4
      i32.add
      local.set $l10
      local.get $p3
      f32.load offset=16
      local.set $l16
      local.get $p3
      f32.load offset=20
      local.set $l17
      local.get $l8
      local.get $p3
      f32.load offset=24
      local.tee $l27
      local.get $p0
      f32.load offset=8
      local.tee $l18
      local.get $p3
      f32.load
      local.tee $l19
      local.get $l19
      f32.add
      local.tee $l20
      local.get $p3
      f32.load offset=8
      local.tee $l28
      f32.mul
      local.get $p3
      f32.load offset=12
      local.tee $l23
      local.get $l23
      f32.add
      local.tee $l26
      local.get $p3
      f32.load offset=4
      local.tee $l29
      f32.mul
      f32.sub
      f32.mul
      local.tee $l30
      f32.sub
      local.tee $l31
      f32.store offset=116
      local.get $l8
      local.get $l17
      local.get $l18
      local.get $l28
      local.get $l26
      f32.mul
      local.get $l20
      local.get $l29
      f32.mul
      f32.add
      f32.mul
      local.tee $l28
      f32.sub
      local.tee $l32
      f32.store offset=112
      local.get $l8
      local.get $l30
      local.get $l27
      f32.add
      local.tee $l27
      f32.store offset=104
      local.get $l8
      local.get $l17
      local.get $l28
      f32.add
      local.tee $l28
      f32.store offset=100
      local.get $l8
      local.get $l16
      local.get $l18
      local.get $l19
      local.get $l20
      f32.mul
      local.get $l23
      local.get $l26
      f32.mul
      f32.const -0x1p+0 (;=-1;)
      f32.add
      f32.add
      f32.mul
      local.tee $l17
      f32.sub
      local.tee $l30
      f32.store offset=108
      local.get $l8
      local.get $l16
      local.get $l17
      f32.add
      local.tee $l29
      f32.store offset=96
      local.get $l8
      i64.const 4575657221408423936
      i64.store offset=224
      local.get $l8
      i64.const 0
      i64.store offset=216
      local.get $l8
      i64.const 4575657221408423936
      i64.store offset=208
      local.get $l8
      i64.const 0
      i64.store offset=200
      local.get $l8
      i64.const 4575657222473777152
      i64.store offset=192
      local.get $l8
      i64.const 1065353216
      i64.store offset=176
      local.get $l8
      i32.const 0
      i32.store8 offset=232
      local.get $l8
      i64.const 0
      i64.store offset=184
      local.get $l8
      i64.const 0
      i64.store offset=168
      local.get $l8
      i64.const 1065353216
      i64.store offset=160
      local.get $l29
      local.get $l30
      f32.eq
      local.get $l28
      local.get $l32
      f32.eq
      i32.and
      local.get $l27
      local.get $l31
      f32.eq
      i32.and
      local.set $p2
      block $B3
        block $B4
          local.get $p1
          f32.load offset=4
          f32.const 0x1p+0 (;=1;)
          f32.ne
          br_if $B4
          local.get $p1
          f32.load offset=8
          f32.const 0x1p+0 (;=1;)
          f32.ne
          br_if $B4
          local.get $p1
          f32.load offset=12
          f32.const 0x1p+0 (;=1;)
          f32.eq
          br_if $B3
        end
        local.get $l8
        i32.const 160
        i32.add
        local.get $l10
        local.get $l11
        call $f70485
      end
      i32.const 1
      i32.const 2
      local.get $p2
      select
      local.set $l12
      local.get $l8
      i32.const 160
      i32.add
      local.tee $p6
      f32.load offset=16
      local.set $l33
      local.get $p6
      f32.load offset=28
      local.set $l34
      local.get $p6
      f32.load offset=24
      local.set $l18
      local.get $p6
      f32.load offset=12
      local.set $l19
      local.get $p6
      f32.load
      local.set $l20
      local.get $p6
      f32.load offset=4
      local.set $l23
      local.get $l8
      i32.const 16
      i32.add
      local.tee $p3
      local.get $p1
      i32.load offset=40
      local.tee $p1
      f32.load offset=24
      local.tee $l16
      local.get $p6
      f32.load offset=8
      f32.mul
      local.get $p1
      f32.load offset=28
      local.tee $l17
      local.get $p6
      f32.load offset=20
      f32.mul
      f32.add
      local.get $p1
      f32.load offset=32
      local.tee $l26
      local.get $p6
      f32.load offset=32
      f32.mul
      f32.add
      f32.store offset=8
      local.get $p3
      local.get $l16
      local.get $l23
      f32.mul
      local.get $l17
      local.get $l33
      f32.mul
      f32.add
      local.get $l26
      local.get $l34
      f32.mul
      f32.add
      f32.store offset=4
      local.get $p3
      local.get $l16
      local.get $l20
      f32.mul
      local.get $l17
      local.get $l19
      f32.mul
      f32.add
      local.get $l26
      local.get $l18
      f32.mul
      f32.add
      f32.store
      local.get $p3
      local.get $p1
      i32.load8_u offset=38
      local.tee $p6
      i32.store offset=12
      local.get $p3
      local.get $p1
      i32.load8_u offset=39
      local.tee $l9
      i32.store offset=16
      local.get $p3
      local.get $p1
      i32.load16_s offset=36
      local.tee $l14
      i32.const 32767
      i32.and
      local.tee $l11
      i32.store offset=20
      local.get $p3
      local.get $p1
      i32.load offset=40
      local.tee $l13
      i32.store offset=24
      local.get $p3
      local.get $l13
      local.get $l9
      i32.const 20
      i32.mul
      i32.add
      local.tee $l9
      i32.store offset=28
      local.get $p3
      local.get $l9
      local.get $p6
      i32.const 12
      i32.mul
      i32.add
      local.tee $l9
      i32.store offset=36
      local.get $p3
      local.get $l9
      local.get $l11
      i32.const 1
      i32.shl
      i32.add
      local.get $p6
      i32.const 3
      i32.mul
      i32.add
      local.tee $p6
      local.get $p6
      local.get $l11
      i32.const 2
      i32.shl
      i32.add
      local.get $l14
      i32.const 0
      i32.ge_s
      select
      i32.store offset=32
      local.get $p3
      local.get $p1
      i64.load offset=48 align=4
      i64.store offset=44 align=4
      local.get $p3
      local.get $p1
      i64.load offset=56 align=4
      i64.store offset=52 align=4
      local.get $p3
      local.get $p1
      i32.load offset=44
      local.tee $p1
      i32.store offset=60
      local.get $p3
      i32.const 119634
      i32.store offset=68
      local.get $p3
      i32.const 119635
      i32.const 119636
      local.get $p1
      select
      i32.store offset=64
      f32.const 0x0p+0 (;=0;)
      local.set $l37
      block $B5
        block $B6
          local.get $l24
          f32.const 0x0p+0 (;=0;)
          f32.gt
          if $I7
            local.get $l8
            local.get $l25
            f32.neg
            local.tee $l49
            f32.store offset=8
            local.get $l8
            local.get $l21
            f32.neg
            local.tee $l43
            f32.store offset=4
            local.get $l8
            local.get $l22
            f32.neg
            local.tee $l51
            f32.store
            local.get $p7
            local.get $p5
            local.get $l8
            i32.const 16
            i32.add
            local.get $l10
            local.get $l12
            local.get $l8
            i32.const 96
            i32.add
            local.get $p0
            f32.load offset=4
            local.get $l8
            local.get $p4
            f32.load
            call $f70168
            local.get $p7
            i32.load offset=4096
            local.tee $p3
            i32.const 2
            i32.eq
            br_if $B6
            local.get $p2
            if $I8 (result i32)
              local.get $p3
            else
              local.get $p4
              f32.load
              local.set $l44
              local.get $p0
              f32.load offset=4
              local.set $l50
              local.get $p5
              f32.load offset=24
              local.set $l23
              local.get $p5
              f32.load offset=20
              local.set $l26
              local.get $p5
              f32.load offset=16
              local.set $l34
              local.get $l8
              local.get $p5
              f32.load offset=4
              local.tee $l17
              local.get $l17
              f32.add
              local.tee $l19
              local.get $p5
              f32.load offset=8
              local.tee $l16
              f32.mul
              local.tee $l38
              local.get $p5
              f32.load
              local.tee $l20
              local.get $l20
              f32.add
              local.tee $l18
              local.get $p5
              f32.load offset=12
              local.tee $l41
              f32.mul
              local.tee $l39
              f32.sub
              local.tee $l33
              local.get $l43
              f32.mul
              local.get $l22
              local.get $l18
              local.get $l16
              f32.mul
              local.tee $l42
              local.get $l19
              local.get $l41
              f32.mul
              local.tee $l45
              f32.add
              local.tee $l37
              f32.mul
              f32.sub
              local.get $l25
              f32.const 0x1p+0 (;=1;)
              local.get $l20
              local.get $l18
              f32.mul
              f32.sub
              local.tee $l20
              local.get $l17
              local.get $l19
              f32.mul
              local.tee $l19
              f32.sub
              local.tee $l35
              f32.mul
              f32.sub
              f32.store offset=344
              local.get $l8
              local.get $l20
              local.get $l16
              local.get $l16
              local.get $l16
              f32.add
              local.tee $l40
              f32.mul
              local.tee $l16
              f32.sub
              local.tee $l36
              local.get $l43
              f32.mul
              local.get $l22
              local.get $l18
              local.get $l17
              f32.mul
              local.tee $l17
              local.get $l40
              local.get $l41
              f32.mul
              local.tee $l18
              f32.sub
              local.tee $l41
              f32.mul
              f32.sub
              local.get $l25
              local.get $l38
              local.get $l39
              f32.add
              local.tee $l38
              f32.mul
              f32.sub
              f32.store offset=340
              local.get $l8
              local.get $l17
              local.get $l18
              f32.add
              local.tee $l39
              local.get $l43
              f32.mul
              local.get $l22
              f32.const 0x1p+0 (;=1;)
              local.get $l19
              f32.sub
              local.get $l16
              f32.sub
              local.tee $l40
              f32.mul
              f32.sub
              local.get $l25
              local.get $l42
              local.get $l45
              f32.sub
              local.tee $l42
              f32.mul
              f32.sub
              f32.store offset=336
              local.get $l8
              i32.const 16
              i32.add
              local.get $l8
              i32.const 160
              i32.add
              local.get $l8
              i32.const 336
              i32.add
              local.get $l8
              i32.load offset=84
              call_indirect $__indirect_function_table (type $t3)
              local.set $p5
              local.get $l8
              local.get $l27
              f32.store offset=296
              local.get $l8
              local.get $l29
              f32.store offset=288
              local.get $l8
              local.get $l28
              f32.store offset=292
              local.get $l8
              local.get $l32
              f32.store offset=276
              local.get $l8
              local.get $l30
              f32.store offset=272
              local.get $l8
              local.get $l31
              f32.store offset=280
              local.get $l30
              local.get $l29
              f32.sub
              local.tee $l16
              local.get $l16
              f32.mul
              local.get $l32
              local.get $l28
              f32.sub
              local.tee $l17
              local.get $l17
              f32.mul
              f32.add
              local.get $l31
              local.get $l27
              f32.sub
              local.tee $l18
              local.get $l18
              f32.mul
              f32.add
              f32.sqrt
              local.tee $l19
              f32.const 0x0p+0 (;=0;)
              f32.gt
              if $I9
                local.get $l8
                local.get $l27
                local.get $l18
                f32.const 0x1.47ae14p-7 (;=0.01;)
                local.get $l19
                f32.div
                local.tee $l19
                f32.mul
                local.tee $l18
                f32.sub
                local.tee $l27
                f32.store offset=296
                local.get $l8
                local.get $l28
                local.get $l17
                local.get $l19
                f32.mul
                local.tee $l17
                f32.sub
                local.tee $l28
                f32.store offset=292
                local.get $l8
                local.get $l29
                local.get $l16
                local.get $l19
                f32.mul
                local.tee $l16
                f32.sub
                local.tee $l29
                f32.store offset=288
                local.get $l8
                local.get $l31
                local.get $l18
                f32.add
                local.tee $l18
                f32.store offset=280
                local.get $l18
                local.get $l27
                f32.sub
                local.set $l18
                local.get $l8
                local.get $l32
                local.get $l17
                f32.add
                local.tee $l17
                f32.store offset=276
                local.get $l17
                local.get $l28
                f32.sub
                local.set $l17
                local.get $l8
                local.get $l30
                local.get $l16
                f32.add
                local.tee $l16
                f32.store offset=272
                local.get $l16
                local.get $l29
                f32.sub
                local.set $l16
              end
              local.get $l8
              local.get $l16
              f32.store offset=256
              local.get $l8
              local.get $l17
              f32.store offset=260
              local.get $l8
              local.get $l18
              f32.store offset=264
              local.get $l8
              local.get $l22
              local.get $l17
              f32.mul
              local.get $l21
              local.get $l16
              f32.mul
              f32.sub
              local.tee $l19
              f32.neg
              f32.store offset=360
              local.get $l8
              local.get $l21
              local.get $l18
              f32.mul
              local.get $l25
              local.get $l17
              f32.mul
              f32.sub
              local.tee $l17
              f32.neg
              f32.store offset=352
              local.get $l8
              local.get $l25
              local.get $l16
              f32.mul
              local.get $l22
              local.get $l18
              f32.mul
              f32.sub
              local.tee $l18
              f32.neg
              local.tee $l16
              f32.store offset=356
              local.get $l8
              local.get $l28
              local.get $l16
              f32.mul
              local.get $l17
              local.get $l29
              f32.mul
              f32.sub
              local.get $l27
              local.get $l19
              f32.mul
              f32.sub
              f32.neg
              f32.store offset=364
              local.get $l19
              f32.abs
              local.set $l16
              block $B10 (result i32)
                block $B11
                  block $B12
                    local.get $l18
                    f32.abs
                    local.tee $l18
                    local.get $l17
                    f32.abs
                    local.tee $l17
                    f32.gt
                    i32.eqz
                    br_if $B12
                    local.get $l16
                    local.get $l18
                    f32.lt
                    i32.eqz
                    br_if $B12
                    i32.const 0
                    local.set $p2
                    i32.const 2
                    local.set $p3
                    br $B11
                  end
                  i32.const 2
                  local.set $l10
                  i32.const 0
                  local.set $p3
                  i32.const 1
                  local.tee $p2
                  local.get $l16
                  local.get $l17
                  f32.gt
                  i32.eqz
                  br_if $B10
                  drop
                end
                local.get $p2
                local.set $l10
                local.get $p3
              end
              local.set $p2
              local.get $l8
              i32.load offset=40
              local.get $p5
              i32.const 20
              i32.mul
              i32.add
              local.tee $p5
              i32.load8_u offset=18
              local.tee $p3
              if $I13
                f32.const 0x1p+0 (;=1;)
                local.get $l10
                i32.const 2
                i32.shl
                local.tee $p1
                local.get $l8
                i32.const 256
                i32.add
                i32.add
                f32.load
                local.get $l8
                local.get $p2
                i32.const 2
                i32.shl
                local.tee $l9
                i32.add
                f32.load
                f32.mul
                local.get $l8
                i32.const 256
                i32.add
                local.get $l9
                i32.add
                f32.load
                local.get $p1
                local.get $l8
                i32.add
                f32.load
                f32.mul
                f32.sub
                f32.div
                local.set $l52
                local.get $l50
                local.get $l44
                f32.add
                local.set $l53
                local.get $l8
                i32.load offset=48
                local.get $p5
                i32.load16_u offset=16
                i32.add
                local.set $l9
                local.get $l8
                i32.load offset=44
                local.set $p6
                local.get $p3
                i32.const 1
                i32.sub
                local.set $p1
                i32.const 0
                local.set $p4
                loop $L14
                  local.get $l8
                  local.get $l23
                  local.get $l42
                  local.get $p6
                  local.get $p1
                  local.get $l9
                  i32.add
                  i32.load8_u
                  i32.const 12
                  i32.mul
                  i32.add
                  local.tee $p5
                  f32.load
                  local.tee $l16
                  local.get $l8
                  f32.load offset=160
                  local.tee $l27
                  f32.mul
                  local.get $p5
                  f32.load offset=4
                  local.tee $l17
                  local.get $l8
                  f32.load offset=172
                  local.tee $l28
                  f32.mul
                  f32.add
                  local.get $p5
                  f32.load offset=8
                  local.tee $l18
                  local.get $l8
                  f32.load offset=184
                  local.tee $l29
                  f32.mul
                  f32.add
                  local.tee $l19
                  f32.mul
                  local.get $l38
                  local.get $l16
                  local.get $l8
                  f32.load offset=164
                  local.tee $l31
                  f32.mul
                  local.get $l17
                  local.get $l8
                  f32.load offset=176
                  local.tee $l32
                  f32.mul
                  f32.add
                  local.get $l18
                  local.get $l8
                  f32.load offset=188
                  local.tee $l30
                  f32.mul
                  f32.add
                  local.tee $l20
                  f32.mul
                  f32.add
                  local.get $l35
                  local.get $l16
                  local.get $l8
                  f32.load offset=168
                  local.tee $l45
                  f32.mul
                  local.get $l17
                  local.get $l8
                  f32.load offset=180
                  local.tee $l44
                  f32.mul
                  f32.add
                  local.get $l18
                  local.get $l8
                  f32.load offset=192
                  local.tee $l18
                  f32.mul
                  f32.add
                  local.tee $l16
                  f32.mul
                  f32.add
                  f32.add
                  f32.store offset=152
                  local.get $l8
                  local.get $l26
                  local.get $l39
                  local.get $l19
                  f32.mul
                  local.get $l36
                  local.get $l20
                  f32.mul
                  f32.add
                  local.get $l33
                  local.get $l16
                  f32.mul
                  f32.add
                  f32.add
                  f32.store offset=148
                  local.get $l8
                  local.get $l34
                  local.get $l40
                  local.get $l19
                  f32.mul
                  local.get $l41
                  local.get $l20
                  f32.mul
                  f32.add
                  local.get $l37
                  local.get $l16
                  f32.mul
                  f32.add
                  f32.add
                  f32.store offset=144
                  local.get $l8
                  local.get $l23
                  local.get $l35
                  local.get $l45
                  local.get $p6
                  local.get $l9
                  local.get $p4
                  local.tee $p1
                  i32.add
                  i32.load8_u
                  i32.const 12
                  i32.mul
                  i32.add
                  local.tee $p5
                  f32.load
                  local.tee $l16
                  f32.mul
                  local.get $l44
                  local.get $p5
                  f32.load offset=4
                  local.tee $l17
                  f32.mul
                  f32.add
                  local.get $l18
                  local.get $p5
                  f32.load offset=8
                  local.tee $l18
                  f32.mul
                  f32.add
                  local.tee $l19
                  f32.mul
                  local.get $l42
                  local.get $l27
                  local.get $l16
                  f32.mul
                  local.get $l28
                  local.get $l17
                  f32.mul
                  f32.add
                  local.get $l29
                  local.get $l18
                  f32.mul
                  f32.add
                  local.tee $l20
                  f32.mul
                  local.get $l38
                  local.get $l31
                  local.get $l16
                  f32.mul
                  local.get $l32
                  local.get $l17
                  f32.mul
                  f32.add
                  local.get $l30
                  local.get $l18
                  f32.mul
                  f32.add
                  local.tee $l16
                  f32.mul
                  f32.add
                  f32.add
                  f32.add
                  f32.store offset=136
                  local.get $l8
                  local.get $l26
                  local.get $l33
                  local.get $l19
                  f32.mul
                  local.get $l39
                  local.get $l20
                  f32.mul
                  local.get $l36
                  local.get $l16
                  f32.mul
                  f32.add
                  f32.add
                  f32.add
                  f32.store offset=132
                  local.get $l8
                  local.get $l34
                  local.get $l37
                  local.get $l19
                  f32.mul
                  local.get $l40
                  local.get $l20
                  f32.mul
                  local.get $l41
                  local.get $l16
                  f32.mul
                  f32.add
                  f32.add
                  f32.add
                  f32.store offset=128
                  local.get $l8
                  local.get $l25
                  f32.store offset=312
                  local.get $l8
                  local.get $l21
                  f32.store offset=308
                  local.get $l8
                  local.get $l22
                  f32.store offset=304
                  local.get $p3
                  i32.const 1
                  i32.sub
                  local.set $p3
                  block $B15
                    local.get $l8
                    i32.const 288
                    i32.add
                    local.get $l8
                    i32.const 272
                    i32.add
                    local.get $l8
                    i32.const 256
                    i32.add
                    local.get $l8
                    i32.const 352
                    i32.add
                    local.get $p2
                    local.get $l10
                    local.get $l52
                    local.get $l8
                    i32.const 304
                    i32.add
                    local.get $l8
                    i32.const 144
                    i32.add
                    local.get $l8
                    i32.const 128
                    i32.add
                    local.get $l8
                    i32.const 316
                    i32.add
                    local.get $l8
                    i32.const 320
                    i32.add
                    f32.const 0x0p+0 (;=0;)
                    call $f70169
                    i32.eqz
                    br_if $B15
                    local.get $l8
                    f32.load offset=316
                    local.tee $l16
                    local.get $l53
                    f32.lt
                    i32.eqz
                    br_if $B15
                    local.get $p7
                    i32.load offset=4096
                    local.tee $p5
                    i32.const 63
                    i32.gt_u
                    br_if $B15
                    local.get $l8
                    f32.load offset=324
                    local.set $l17
                    local.get $l8
                    f32.load offset=328
                    local.set $l18
                    local.get $l8
                    f32.load offset=320
                    local.set $l19
                    local.get $p7
                    local.get $p5
                    i32.const 1
                    i32.add
                    i32.store offset=4096
                    local.get $p7
                    local.get $p5
                    i32.const 6
                    i32.shl
                    i32.add
                    local.tee $p5
                    local.get $l19
                    local.get $l22
                    local.get $l16
                    f32.mul
                    f32.add
                    f32.store offset=16
                    local.get $p5
                    local.get $l49
                    f32.store offset=8
                    local.get $p5
                    local.get $l43
                    f32.store offset=4
                    local.get $p5
                    local.get $l51
                    f32.store
                    local.get $p5
                    i32.const -1
                    i32.store offset=52
                    local.get $p5
                    local.get $l16
                    local.get $l50
                    f32.sub
                    f32.store offset=12
                    local.get $p5
                    local.get $l18
                    local.get $l25
                    local.get $l16
                    f32.mul
                    f32.add
                    f32.store offset=24
                    local.get $p5
                    local.get $l17
                    local.get $l21
                    local.get $l16
                    f32.mul
                    f32.add
                    f32.store offset=20
                  end
                  local.get $p1
                  i32.const 1
                  i32.add
                  local.set $p4
                  local.get $p3
                  br_if $L14
                end
              end
              local.get $p7
              i32.load offset=4096
            end
            br_if $B6
            local.get $p0
            f32.load offset=4
            local.set $l16
            local.get $p7
            i32.const 1
            i32.store offset=4096
            local.get $p7
            local.get $l8
            f32.load
            f32.store
            local.get $l8
            f32.load offset=4
            local.set $l17
            local.get $p7
            local.get $l46
            f32.store offset=24
            local.get $p7
            local.get $l47
            f32.store offset=20
            local.get $p7
            local.get $l48
            f32.store offset=16
            local.get $p7
            local.get $l49
            f32.store offset=8
            local.get $p7
            local.get $l17
            f32.store offset=4
            local.get $p7
            i32.const -1
            i32.store offset=52
            local.get $p7
            local.get $l24
            local.get $l16
            f32.sub
            f32.store offset=12
            br $B6
          end
          local.get $p0
          f32.load offset=4
          local.set $l25
          local.get $l8
          i32.load offset=32
          local.set $l9
          local.get $l8
          i32.load offset=40
          local.set $p6
          local.get $l8
          local.get $p5
          f32.load offset=4
          local.tee $l17
          local.get $l17
          f32.add
          local.tee $l22
          local.get $p5
          f32.load offset=8
          local.tee $l16
          f32.mul
          local.tee $l18
          local.get $p5
          f32.load
          local.tee $l19
          local.get $l19
          f32.add
          local.tee $l24
          local.get $p5
          f32.load offset=12
          local.tee $l23
          f32.mul
          local.tee $l20
          f32.sub
          local.tee $l21
          f32.store offset=380
          local.get $l8
          local.get $l18
          local.get $l20
          f32.add
          local.tee $l18
          f32.store offset=372
          local.get $l8
          f32.const 0x1p+0 (;=1;)
          local.get $l19
          local.get $l24
          f32.mul
          f32.sub
          local.tee $l20
          local.get $l17
          local.get $l22
          f32.mul
          local.tee $l26
          f32.sub
          local.tee $l19
          f32.store offset=384
          local.get $l8
          local.get $l20
          local.get $l16
          local.get $l16
          local.get $l16
          f32.add
          local.tee $l34
          f32.mul
          local.tee $l33
          f32.sub
          local.tee $l20
          f32.store offset=368
          local.get $l8
          local.get $l24
          local.get $l16
          f32.mul
          local.tee $l16
          local.get $l22
          local.get $l23
          f32.mul
          local.tee $l35
          f32.add
          local.tee $l22
          f32.store offset=376
          local.get $l8
          local.get $l24
          local.get $l17
          f32.mul
          local.tee $l36
          local.get $l34
          local.get $l23
          f32.mul
          local.tee $l23
          f32.sub
          local.tee $l24
          f32.store offset=364
          local.get $l8
          local.get $l16
          local.get $l35
          f32.sub
          local.tee $l17
          f32.store offset=360
          local.get $l8
          local.get $l36
          local.get $l23
          f32.add
          local.tee $l23
          f32.store offset=356
          local.get $l8
          f32.const 0x1p+0 (;=1;)
          local.get $l26
          f32.sub
          local.get $l33
          f32.sub
          local.tee $l26
          f32.store offset=352
          local.get $l8
          local.get $p5
          f32.load offset=16
          f32.store offset=388
          local.get $l8
          local.get $p5
          f32.load offset=20
          f32.store offset=392
          local.get $l8
          local.get $p5
          f32.load offset=24
          f32.store offset=396
          f32.const 0x1.fffffep+127 (;=3.40282e+38;)
          local.set $l33
          block $B16
            local.get $l9
            i32.eqz
            if $I17
              f32.const 0x0p+0 (;=0;)
              local.set $l35
              f32.const 0x0p+0 (;=0;)
              local.set $l36
              br $B16
            end
            i32.const 0
            local.set $p1
            f32.const 0x0p+0 (;=0;)
            local.set $l36
            f32.const 0x0p+0 (;=0;)
            local.set $l35
            loop $L18
              local.get $l8
              local.get $l17
              local.get $p6
              local.get $p1
              i32.const 20
              i32.mul
              i32.add
              local.tee $p3
              f32.load
              local.tee $l16
              f32.mul
              local.get $l18
              local.get $p3
              f32.load offset=4
              local.tee $l17
              f32.mul
              f32.add
              local.get $l19
              local.get $p3
              f32.load offset=8
              local.tee $l18
              f32.mul
              f32.add
              local.tee $l19
              f32.store offset=344
              local.get $l8
              local.get $l26
              local.get $l16
              f32.mul
              local.get $l24
              local.get $l17
              f32.mul
              f32.add
              local.get $l22
              local.get $l18
              f32.mul
              f32.add
              local.tee $l22
              f32.store offset=336
              local.get $l8
              local.get $l23
              local.get $l16
              f32.mul
              local.get $l20
              local.get $l17
              f32.mul
              f32.add
              local.get $l21
              local.get $l18
              f32.mul
              f32.add
              local.tee $l16
              f32.store offset=340
              local.get $l8
              i32.const 16
              i32.add
              local.get $l8
              i32.const 336
              i32.add
              local.get $l8
              i32.const 352
              i32.add
              local.get $l8
              i32.const 160
              i32.add
              local.get $l8
              i32.const 288
              i32.add
              local.get $l8
              i32.const 272
              i32.add
              local.get $l8
              i32.load offset=80
              call_indirect $__indirect_function_table (type $t11)
              local.get $l25
              local.get $l27
              local.get $l19
              f32.mul
              local.get $l29
              local.get $l22
              f32.mul
              local.get $l28
              local.get $l16
              f32.mul
              f32.add
              f32.add
              local.tee $l17
              local.get $l31
              local.get $l19
              f32.mul
              local.get $l30
              local.get $l22
              f32.mul
              local.get $l32
              local.get $l16
              f32.mul
              f32.add
              f32.add
              local.tee $l16
              local.get $l16
              local.get $l17
              f32.lt
              local.tee $p3
              select
              f32.add
              local.tee $l18
              local.get $l8
              f32.load offset=288
              local.tee $l19
              f32.sub
              local.tee $l22
              local.get $l8
              f32.load offset=272
              local.tee $l21
              local.get $l16
              local.get $l17
              local.get $p3
              select
              local.get $l25
              f32.sub
              local.tee $l17
              f32.sub
              local.tee $l16
              local.get $l16
              local.get $l22
              f32.gt
              select
              local.set $l16
              block $B19
                local.get $l18
                local.get $l19
                f32.lt
                local.get $l17
                local.get $l21
                f32.gt
                i32.or
                local.tee $p3
                br_if $B19
                local.get $l34
                local.get $l16
                local.get $p3
                select
                local.tee $l17
                local.get $l33
                f32.lt
                i32.eqz
                br_if $B19
                local.get $l8
                f32.load offset=344
                local.set $l37
                local.get $l8
                f32.load offset=340
                local.set $l36
                local.get $l8
                f32.load offset=336
                local.set $l35
                local.get $l17
                local.set $l33
              end
              local.get $p3
              br_if $B5
              local.get $p1
              i32.const 1
              i32.add
              local.tee $p1
              local.get $l9
              i32.eq
              br_if $B16
              local.get $l8
              f32.load offset=384
              local.set $l19
              local.get $l8
              f32.load offset=380
              local.set $l21
              local.get $l8
              f32.load offset=376
              local.set $l22
              local.get $l8
              f32.load offset=372
              local.set $l18
              local.get $l8
              f32.load offset=368
              local.set $l20
              local.get $l8
              f32.load offset=364
              local.set $l24
              local.get $l8
              f32.load offset=360
              local.set $l17
              local.get $l8
              f32.load offset=356
              local.set $l23
              local.get $l8
              f32.load offset=352
              local.set $l26
              local.get $l16
              local.set $l34
              br $L18
            end
            unreachable
          end
          block $B20
            local.get $p2
            br_if $B20
            f32.const 0x0p+0 (;=0;)
            local.set $l20
            f32.const 0x0p+0 (;=0;)
            local.set $l24
            f32.const 0x0p+0 (;=0;)
            local.set $l23
            local.get $l30
            local.get $l29
            f32.sub
            local.tee $l16
            local.get $l16
            f32.mul
            local.get $l32
            local.get $l28
            f32.sub
            local.tee $l17
            local.get $l17
            f32.mul
            f32.add
            local.get $l31
            local.get $l27
            f32.sub
            local.tee $l18
            local.get $l18
            f32.mul
            f32.add
            local.tee $l19
            f32.const 0x0p+0 (;=0;)
            f32.gt
            if $I21
              local.get $l18
              f32.const 0x1p+0 (;=1;)
              local.get $l19
              f32.sqrt
              f32.div
              local.tee $l19
              f32.mul
              local.set $l23
              local.get $l17
              local.get $l19
              f32.mul
              local.set $l24
              local.get $l16
              local.get $l19
              f32.mul
              local.set $l20
            end
            local.get $l9
            i32.eqz
            br_if $B20
            i32.const 0
            local.set $p3
            loop $L22
              local.get $l20
              local.get $p6
              local.get $p3
              i32.const 20
              i32.mul
              i32.add
              local.tee $p1
              f32.load
              local.tee $l16
              local.get $l8
              f32.load offset=356
              f32.mul
              local.get $p1
              f32.load offset=4
              local.tee $l17
              local.get $l8
              f32.load offset=368
              f32.mul
              f32.add
              local.get $p1
              f32.load offset=8
              local.tee $l18
              local.get $l8
              f32.load offset=380
              f32.mul
              f32.add
              local.tee $l22
              f32.mul
              local.get $l24
              local.get $l16
              local.get $l8
              f32.load offset=352
              f32.mul
              local.get $l17
              local.get $l8
              f32.load offset=364
              f32.mul
              f32.add
              local.get $l18
              local.get $l8
              f32.load offset=376
              f32.mul
              f32.add
              local.tee $l21
              f32.mul
              f32.sub
              local.set $l19
              local.get $l23
              local.get $l21
              f32.mul
              local.get $l20
              local.get $l16
              local.get $l8
              f32.load offset=360
              f32.mul
              local.get $l17
              local.get $l8
              f32.load offset=372
              f32.mul
              f32.add
              local.get $l18
              local.get $l8
              f32.load offset=384
              f32.mul
              f32.add
              local.tee $l17
              f32.mul
              f32.sub
              local.set $l16
              block $B23
                block $B24
                  local.get $l24
                  local.get $l17
                  f32.mul
                  local.get $l23
                  local.get $l22
                  f32.mul
                  f32.sub
                  local.tee $l17
                  f32.abs
                  f32.const 0x1.0c6f7ap-20 (;=1e-06;)
                  f32.gt
                  br_if $B24
                  local.get $l16
                  f32.abs
                  f32.const 0x1.0c6f7ap-20 (;=1e-06;)
                  f32.gt
                  br_if $B24
                  local.get $l19
                  f32.abs
                  f32.const 0x1.0c6f7ap-20 (;=1e-06;)
                  f32.gt
                  br_if $B24
                  local.get $l26
                  local.set $l16
                  br $B23
                end
                f32.const 0x0p+0 (;=0;)
                local.set $l18
                f32.const 0x0p+0 (;=0;)
                local.set $l22
                f32.const 0x0p+0 (;=0;)
                local.set $l21
                local.get $l19
                local.get $l19
                f32.mul
                local.get $l17
                local.get $l17
                f32.mul
                local.get $l16
                local.get $l16
                f32.mul
                f32.add
                f32.add
                local.tee $l34
                f32.const 0x0p+0 (;=0;)
                f32.gt
                if $I25
                  local.get $l19
                  f32.const 0x1p+0 (;=1;)
                  local.get $l34
                  f32.sqrt
                  f32.div
                  local.tee $l18
                  f32.mul
                  local.set $l21
                  local.get $l16
                  local.get $l18
                  f32.mul
                  local.set $l22
                  local.get $l17
                  local.get $l18
                  f32.mul
                  local.set $l18
                end
                local.get $l8
                local.get $l21
                f32.store offset=344
                local.get $l8
                local.get $l18
                f32.store offset=336
                local.get $l8
                local.get $l22
                f32.store offset=340
                local.get $l8
                i32.const 16
                i32.add
                local.get $l8
                i32.const 336
                i32.add
                local.get $l8
                i32.const 352
                i32.add
                local.get $l8
                i32.const 160
                i32.add
                local.get $l8
                i32.const 288
                i32.add
                local.get $l8
                i32.const 272
                i32.add
                local.get $l8
                i32.load offset=80
                call_indirect $__indirect_function_table (type $t11)
                local.get $l25
                local.get $l29
                local.get $l18
                f32.mul
                local.get $l28
                local.get $l22
                f32.mul
                f32.add
                local.get $l27
                local.get $l21
                f32.mul
                f32.add
                local.tee $l16
                local.get $l30
                local.get $l18
                f32.mul
                local.get $l32
                local.get $l22
                f32.mul
                f32.add
                local.get $l31
                local.get $l21
                f32.mul
                f32.add
                local.tee $l17
                local.get $l16
                local.get $l17
                f32.gt
                local.tee $p1
                select
                f32.add
                local.tee $l18
                local.get $l8
                f32.load offset=288
                local.tee $l19
                f32.sub
                local.tee $l22
                local.get $l8
                f32.load offset=272
                local.tee $l21
                local.get $l17
                local.get $l16
                local.get $p1
                select
                local.get $l25
                f32.sub
                local.tee $l17
                f32.sub
                local.tee $l16
                local.get $l16
                local.get $l22
                f32.gt
                select
                local.set $l16
                block $B26
                  local.get $l18
                  local.get $l19
                  f32.lt
                  local.get $l17
                  local.get $l21
                  f32.gt
                  i32.or
                  local.tee $p1
                  br_if $B26
                  local.get $l26
                  local.get $l16
                  local.get $p1
                  select
                  local.tee $l17
                  local.get $l33
                  f32.lt
                  i32.eqz
                  br_if $B26
                  local.get $l8
                  f32.load offset=344
                  local.set $l37
                  local.get $l8
                  f32.load offset=340
                  local.set $l36
                  local.get $l8
                  f32.load offset=336
                  local.set $l35
                  local.get $l17
                  local.set $l33
                end
                local.get $p1
                br_if $B5
              end
              local.get $l16
              local.set $l26
              local.get $p3
              i32.const 1
              i32.add
              local.tee $p3
              local.get $l9
              i32.ne
              br_if $L22
            end
          end
          local.get $l8
          local.get $l37
          f32.neg
          local.get $l37
          local.get $l37
          local.get $l27
          local.get $l31
          f32.add
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          local.get $p5
          f32.load offset=24
          local.get $l8
          f32.load offset=24
          local.tee $l16
          local.get $l16
          f32.add
          local.tee $l17
          local.get $p5
          f32.load offset=12
          local.tee $l16
          local.get $l16
          f32.mul
          f32.const -0x1p-1 (;=-0.5;)
          f32.add
          local.tee $l20
          f32.mul
          local.get $l16
          local.get $l8
          f32.load offset=20
          local.tee $l18
          local.get $l18
          f32.add
          local.tee $l18
          local.get $p5
          f32.load
          local.tee $l19
          f32.mul
          local.get $l8
          f32.load offset=16
          local.tee $l22
          local.get $l22
          f32.add
          local.tee $l22
          local.get $p5
          f32.load offset=4
          local.tee $l25
          f32.mul
          f32.sub
          f32.mul
          f32.add
          local.get $p5
          f32.load offset=8
          local.tee $l21
          local.get $l22
          local.get $l19
          f32.mul
          local.get $l18
          local.get $l25
          f32.mul
          f32.add
          local.get $l17
          local.get $l21
          f32.mul
          f32.add
          local.tee $l24
          f32.mul
          f32.add
          f32.add
          f32.sub
          f32.mul
          local.get $l35
          local.get $l29
          local.get $l30
          f32.add
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          local.get $p5
          f32.load offset=16
          local.get $l19
          local.get $l24
          f32.mul
          local.get $l22
          local.get $l20
          f32.mul
          local.get $l16
          local.get $l17
          local.get $l25
          f32.mul
          local.get $l18
          local.get $l21
          f32.mul
          f32.sub
          f32.mul
          f32.add
          f32.add
          f32.add
          f32.sub
          f32.mul
          local.get $l36
          local.get $l28
          local.get $l32
          f32.add
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          local.get $p5
          f32.load offset=20
          local.get $l25
          local.get $l24
          f32.mul
          local.get $l18
          local.get $l20
          f32.mul
          local.get $l16
          local.get $l22
          local.get $l21
          f32.mul
          local.get $l17
          local.get $l19
          f32.mul
          f32.sub
          f32.mul
          f32.add
          f32.add
          f32.add
          f32.sub
          f32.mul
          f32.add
          f32.add
          f32.const 0x0p+0 (;=0;)
          f32.lt
          local.tee $p3
          select
          local.tee $l38
          f32.store offset=312
          local.get $l8
          local.get $l36
          f32.neg
          local.get $l36
          local.get $p3
          select
          local.tee $l39
          f32.store offset=308
          local.get $l8
          local.get $l35
          f32.neg
          local.get $l35
          local.get $p3
          select
          local.tee $l40
          f32.store offset=304
          local.get $p7
          local.get $p5
          local.get $l8
          i32.const 16
          i32.add
          local.get $l10
          local.get $l12
          local.get $l8
          i32.const 96
          i32.add
          local.get $p0
          f32.load offset=4
          local.get $l8
          i32.const 304
          i32.add
          local.get $p4
          f32.load
          call $f70168
          local.get $p2
          local.get $p7
          i32.load offset=4096
          i32.const 2
          i32.eq
          i32.or
          br_if $B6
          local.get $p4
          f32.load
          local.set $l22
          local.get $p0
          f32.load offset=4
          local.set $l42
          block $B27 (result i32)
            local.get $l8
            i32.const 352
            i32.add
            local.set $l11
            local.get $l8
            i32.load offset=40
            local.set $p3
            local.get $l8
            i32.load offset=48
            local.set $l15
            i32.const 0
            local.set $p2
            local.get $l8
            i32.load offset=32
            local.tee $l13
            if $I28
              loop $L29
                local.get $p3
                i32.load8_u offset=18
                local.tee $p6
                if $I30
                  local.get $p6
                  local.get $l15
                  local.get $p3
                  i32.load16_u offset=16
                  i32.add
                  local.tee $l14
                  i32.add
                  i32.const 1
                  i32.sub
                  i32.load8_u
                  local.set $p0
                  i32.const 0
                  local.set $l10
                  loop $L31
                    local.get $p0
                    local.get $l10
                    local.get $l14
                    i32.add
                    i32.load8_u
                    local.tee $p1
                    local.get $p1
                    local.get $p0
                    i32.const 255
                    i32.and
                    i32.lt_u
                    local.tee $p4
                    select
                    local.set $l9
                    local.get $p1
                    local.get $p0
                    local.get $p4
                    select
                    local.set $l12
                    i32.const 0
                    local.set $p0
                    block $B32
                      local.get $p2
                      if $I33
                        loop $L34
                          block $B35
                            local.get $l11
                            local.get $p0
                            i32.const 4
                            i32.shl
                            i32.add
                            local.tee $p4
                            i32.load8_u
                            local.get $l12
                            i32.const 255
                            i32.and
                            i32.ne
                            br_if $B35
                            local.get $p4
                            i32.load8_u offset=1
                            local.get $l9
                            i32.const 255
                            i32.and
                            i32.ne
                            br_if $B35
                            local.get $p4
                            local.get $p3
                            f32.load
                            local.get $p4
                            f32.load offset=4
                            f32.add
                            f32.store offset=4
                            local.get $p4
                            i32.const 8
                            i32.add
                            local.tee $p0
                            local.get $p3
                            f32.load offset=4
                            local.get $p0
                            f32.load
                            f32.add
                            f32.store
                            local.get $p4
                            i32.const 12
                            i32.add
                            local.tee $p0
                            local.get $p3
                            f32.load offset=8
                            local.get $p0
                            f32.load
                            f32.add
                            f32.store
                            br $B32
                          end
                          local.get $p0
                          i32.const 1
                          i32.add
                          local.tee $p0
                          local.get $p2
                          i32.ne
                          br_if $L34
                        end
                      end
                      i32.const 512
                      local.get $p2
                      i32.const 512
                      i32.eq
                      br_if $B27
                      drop
                      local.get $l11
                      local.get $p2
                      i32.const 4
                      i32.shl
                      i32.add
                      local.tee $p0
                      local.get $l9
                      i32.store8 offset=1
                      local.get $p0
                      local.get $l12
                      i32.store8
                      local.get $p0
                      local.get $p3
                      f32.load
                      f32.store offset=4
                      local.get $p0
                      local.get $p3
                      f32.load offset=4
                      f32.store offset=8
                      local.get $p0
                      local.get $p3
                      f32.load offset=8
                      f32.store offset=12
                      local.get $p2
                      i32.const 1
                      i32.add
                      local.set $p2
                    end
                    local.get $l10
                    i32.const 1
                    i32.add
                    local.set $l10
                    local.get $p1
                    local.set $p0
                    local.get $p6
                    i32.const 1
                    i32.sub
                    local.tee $p6
                    br_if $L31
                  end
                end
                local.get $p3
                i32.const 20
                i32.add
                local.set $p3
                local.get $l13
                i32.const 1
                i32.sub
                local.tee $l13
                br_if $L29
              end
            end
            local.get $p2
          end
          local.set $p4
          local.get $l8
          local.get $l27
          f32.store offset=296
          local.get $l8
          local.get $l29
          f32.store offset=288
          local.get $l8
          local.get $l28
          f32.store offset=292
          local.get $l8
          local.get $l32
          f32.store offset=276
          local.get $l8
          local.get $l30
          f32.store offset=272
          local.get $l8
          local.get $l31
          f32.store offset=280
          local.get $l30
          local.get $l29
          f32.sub
          local.tee $l16
          local.get $l16
          f32.mul
          local.get $l32
          local.get $l28
          f32.sub
          local.tee $l17
          local.get $l17
          f32.mul
          f32.add
          local.get $l31
          local.get $l27
          f32.sub
          local.tee $l18
          local.get $l18
          f32.mul
          f32.add
          f32.sqrt
          local.tee $l19
          f32.const 0x0p+0 (;=0;)
          f32.gt
          if $I36
            local.get $l8
            local.get $l27
            local.get $l18
            f32.const 0x1.47ae14p-7 (;=0.01;)
            local.get $l19
            f32.div
            local.tee $l19
            f32.mul
            local.tee $l18
            f32.sub
            local.tee $l27
            f32.store offset=296
            local.get $l8
            local.get $l28
            local.get $l17
            local.get $l19
            f32.mul
            local.tee $l17
            f32.sub
            local.tee $l28
            f32.store offset=292
            local.get $l8
            local.get $l29
            local.get $l16
            local.get $l19
            f32.mul
            local.tee $l16
            f32.sub
            local.tee $l29
            f32.store offset=288
            local.get $l8
            local.get $l31
            local.get $l18
            f32.add
            local.tee $l18
            f32.store offset=280
            local.get $l18
            local.get $l27
            f32.sub
            local.set $l18
            local.get $l8
            local.get $l32
            local.get $l17
            f32.add
            local.tee $l17
            f32.store offset=276
            local.get $l17
            local.get $l28
            f32.sub
            local.set $l17
            local.get $l8
            local.get $l30
            local.get $l16
            f32.add
            local.tee $l16
            f32.store offset=272
            local.get $l16
            local.get $l29
            f32.sub
            local.set $l16
          end
          local.get $l8
          local.get $l16
          f32.store offset=256
          local.get $l8
          local.get $l18
          f32.store offset=264
          local.get $l8
          local.get $l17
          f32.store offset=260
          local.get $l8
          local.get $l18
          local.get $l40
          f32.mul
          local.get $l16
          local.get $l38
          f32.mul
          f32.sub
          local.tee $l19
          f32.store offset=340
          local.get $l8
          local.get $l17
          local.get $l38
          f32.mul
          local.get $l18
          local.get $l39
          f32.mul
          f32.sub
          local.tee $l18
          f32.store offset=336
          local.get $l8
          local.get $l16
          local.get $l39
          f32.mul
          local.get $l17
          local.get $l40
          f32.mul
          f32.sub
          local.tee $l16
          f32.store offset=344
          local.get $l8
          local.get $l27
          local.get $l16
          f32.mul
          local.get $l29
          local.get $l18
          f32.mul
          local.get $l28
          local.get $l19
          f32.mul
          f32.add
          f32.add
          f32.neg
          f32.store offset=348
          local.get $l16
          f32.abs
          local.set $l16
          block $B37 (result i32)
            block $B38
              block $B39
                local.get $l19
                f32.abs
                local.tee $l17
                local.get $l18
                f32.abs
                local.tee $l18
                f32.gt
                i32.eqz
                br_if $B39
                local.get $l16
                local.get $l17
                f32.lt
                i32.eqz
                br_if $B39
                i32.const 0
                local.set $p6
                i32.const 2
                local.set $p3
                br $B38
              end
              i32.const 2
              local.set $p2
              i32.const 0
              local.set $p3
              i32.const 1
              local.tee $p6
              local.get $l16
              local.get $l18
              f32.gt
              i32.eqz
              br_if $B37
              drop
            end
            local.get $p6
            local.set $p2
            local.get $p3
          end
          local.set $p6
          local.get $p4
          i32.eqz
          br_if $B6
          f32.const 0x1p+0 (;=1;)
          local.get $p6
          i32.const 2
          i32.shl
          local.tee $p3
          local.get $l8
          i32.const 256
          i32.add
          i32.add
          f32.load
          local.get $p2
          i32.const 2
          i32.shl
          local.tee $p1
          local.get $l8
          i32.const 304
          i32.add
          i32.add
          f32.load
          f32.mul
          local.get $l8
          i32.const 256
          i32.add
          local.get $p1
          i32.add
          f32.load
          local.get $l8
          i32.const 304
          i32.add
          local.get $p3
          i32.add
          f32.load
          f32.mul
          f32.sub
          f32.div
          local.set $l36
          local.get $l42
          f32.neg
          local.get $l22
          f32.sub
          local.set $l41
          i32.const 0
          local.set $p3
          local.get $l8
          i32.load offset=44
          local.set $l9
          loop $L40
            local.get $l8
            i32.const 352
            i32.add
            local.get $p3
            i32.const 4
            i32.shl
            i32.add
            local.tee $p1
            i32.load8_u offset=1
            local.set $p0
            local.get $p5
            f32.load offset=16
            local.set $l24
            local.get $p5
            f32.load offset=20
            local.set $l23
            local.get $l8
            local.get $l9
            local.get $p1
            i32.load8_u
            i32.const 12
            i32.mul
            i32.add
            local.tee $p1
            f32.load
            local.tee $l18
            local.get $l8
            f32.load offset=168
            local.tee $l27
            f32.mul
            local.get $p1
            f32.load offset=4
            local.tee $l19
            local.get $l8
            f32.load offset=180
            local.tee $l28
            f32.mul
            f32.add
            local.get $p1
            f32.load offset=8
            local.tee $l20
            local.get $l8
            f32.load offset=192
            local.tee $l29
            f32.mul
            f32.add
            local.tee $l16
            local.get $l16
            f32.add
            local.tee $l25
            local.get $p5
            f32.load offset=12
            local.tee $l16
            local.get $l16
            f32.mul
            f32.const -0x1p-1 (;=-0.5;)
            f32.add
            local.tee $l22
            f32.mul
            local.get $l16
            local.get $l18
            local.get $l8
            f32.load offset=164
            local.tee $l31
            f32.mul
            local.get $l19
            local.get $l8
            f32.load offset=176
            local.tee $l32
            f32.mul
            f32.add
            local.get $l20
            local.get $l8
            f32.load offset=188
            local.tee $l30
            f32.mul
            f32.add
            local.tee $l17
            local.get $l17
            f32.add
            local.tee $l21
            local.get $p5
            f32.load
            local.tee $l17
            f32.mul
            local.get $l18
            local.get $l8
            f32.load offset=160
            local.tee $l34
            f32.mul
            local.get $l19
            local.get $l8
            f32.load offset=172
            local.tee $l33
            f32.mul
            f32.add
            local.get $l20
            local.get $l8
            f32.load offset=184
            local.tee $l37
            f32.mul
            f32.add
            local.tee $l18
            local.get $l18
            f32.add
            local.tee $l20
            local.get $p5
            f32.load offset=4
            local.tee $l18
            f32.mul
            f32.sub
            f32.mul
            f32.add
            local.get $p5
            f32.load offset=8
            local.tee $l19
            local.get $l20
            local.get $l17
            f32.mul
            local.get $l21
            local.get $l18
            f32.mul
            f32.add
            local.get $l25
            local.get $l19
            f32.mul
            f32.add
            local.tee $l26
            f32.mul
            f32.add
            local.get $p5
            f32.load offset=24
            local.tee $l35
            f32.add
            f32.store offset=152
            local.get $l8
            local.get $l23
            local.get $l18
            local.get $l26
            f32.mul
            local.get $l21
            local.get $l22
            f32.mul
            local.get $l16
            local.get $l20
            local.get $l19
            f32.mul
            local.get $l25
            local.get $l17
            f32.mul
            f32.sub
            f32.mul
            f32.add
            f32.add
            f32.add
            f32.store offset=148
            local.get $l8
            local.get $l24
            local.get $l17
            local.get $l26
            f32.mul
            local.get $l20
            local.get $l22
            f32.mul
            local.get $l16
            local.get $l25
            local.get $l18
            f32.mul
            local.get $l21
            local.get $l19
            f32.mul
            f32.sub
            f32.mul
            f32.add
            f32.add
            f32.add
            f32.store offset=144
            local.get $l8
            local.get $l35
            local.get $l22
            local.get $l27
            local.get $l9
            local.get $p0
            i32.const 12
            i32.mul
            i32.add
            local.tee $p1
            f32.load
            local.tee $l20
            f32.mul
            local.get $l28
            local.get $p1
            f32.load offset=4
            local.tee $l26
            f32.mul
            f32.add
            local.get $l29
            local.get $p1
            f32.load offset=8
            local.tee $l27
            f32.mul
            f32.add
            local.tee $l25
            local.get $l25
            f32.add
            local.tee $l25
            f32.mul
            local.get $l16
            local.get $l17
            local.get $l31
            local.get $l20
            f32.mul
            local.get $l32
            local.get $l26
            f32.mul
            f32.add
            local.get $l30
            local.get $l27
            f32.mul
            f32.add
            local.tee $l21
            local.get $l21
            f32.add
            local.tee $l21
            f32.mul
            local.get $l18
            local.get $l34
            local.get $l20
            f32.mul
            local.get $l33
            local.get $l26
            f32.mul
            f32.add
            local.get $l37
            local.get $l27
            f32.mul
            f32.add
            local.tee $l20
            local.get $l20
            f32.add
            local.tee $l20
            f32.mul
            f32.sub
            f32.mul
            f32.add
            local.get $l19
            local.get $l19
            local.get $l25
            f32.mul
            local.get $l17
            local.get $l20
            f32.mul
            local.get $l18
            local.get $l21
            f32.mul
            f32.add
            f32.add
            local.tee $l26
            f32.mul
            f32.add
            f32.add
            f32.store offset=136
            local.get $l8
            local.get $l23
            local.get $l18
            local.get $l26
            f32.mul
            local.get $l22
            local.get $l21
            f32.mul
            local.get $l16
            local.get $l19
            local.get $l20
            f32.mul
            local.get $l17
            local.get $l25
            f32.mul
            f32.sub
            f32.mul
            f32.add
            f32.add
            f32.add
            f32.store offset=132
            local.get $l8
            local.get $l24
            local.get $l17
            local.get $l26
            f32.mul
            local.get $l22
            local.get $l20
            f32.mul
            local.get $l16
            local.get $l18
            local.get $l25
            f32.mul
            local.get $l19
            local.get $l21
            f32.mul
            f32.sub
            f32.mul
            f32.add
            f32.add
            f32.add
            f32.store offset=128
            block $B41
              local.get $l8
              i32.const 288
              i32.add
              local.get $l8
              i32.const 272
              i32.add
              local.get $l8
              i32.const 256
              i32.add
              local.get $l8
              i32.const 336
              i32.add
              local.get $p6
              local.get $p2
              local.get $l36
              local.get $l8
              i32.const 304
              i32.add
              local.get $l8
              i32.const 144
              i32.add
              local.get $l8
              i32.const 128
              i32.add
              local.get $l8
              local.get $l8
              i32.const 320
              i32.add
              local.get $l41
              call $f70169
              i32.eqz
              br_if $B41
              local.get $p7
              i32.load offset=4096
              local.tee $p1
              i32.const 63
              i32.gt_u
              br_if $B41
              local.get $l8
              f32.load
              local.set $l16
              local.get $l8
              f32.load offset=324
              local.set $l17
              local.get $l8
              f32.load offset=328
              local.set $l18
              local.get $l8
              f32.load offset=320
              local.set $l19
              local.get $p7
              local.get $p1
              i32.const 1
              i32.add
              i32.store offset=4096
              local.get $p7
              local.get $p1
              i32.const 6
              i32.shl
              i32.add
              local.tee $p1
              local.get $l19
              local.get $l40
              local.get $l16
              f32.mul
              f32.sub
              f32.store offset=16
              local.get $p1
              local.get $l38
              f32.store offset=8
              local.get $p1
              local.get $l39
              f32.store offset=4
              local.get $p1
              local.get $l40
              f32.store
              local.get $p1
              i32.const -1
              i32.store offset=52
              local.get $p1
              local.get $l42
              local.get $l16
              f32.add
              f32.neg
              f32.store offset=12
              local.get $p1
              local.get $l18
              local.get $l38
              local.get $l16
              f32.mul
              f32.sub
              f32.store offset=24
              local.get $p1
              local.get $l17
              local.get $l39
              local.get $l16
              f32.mul
              f32.sub
              f32.store offset=20
            end
            local.get $p3
            i32.const 1
            i32.add
            local.tee $p3
            local.get $p4
            i32.ne
            br_if $L40
          end
        end
        i32.const 1
        br $B2
      end
      i32.const 0
    end
    local.set $l9
    local.get $l8
    i32.const 8544
    i32.add
    global.set $g0
    local.get $l9)
