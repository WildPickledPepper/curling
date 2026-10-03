  (func $f70223 (type $t10) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (result i32)
    (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32) (local $l33 f32) (local $l34 f32) (local $l35 f32) (local $l36 f32) (local $l37 i64)
    global.get $g0
    i32.const 496
    i32.sub
    local.tee $l6
    global.set $g0
    local.get $p3
    i32.const 24
    i32.add
    local.tee $l10
    f32.load
    local.set $l22
    local.get $p3
    i32.const 20
    i32.add
    local.tee $l11
    f32.load
    local.set $l23
    local.get $p2
    f32.load offset=4
    local.set $l30
    local.get $p3
    f32.load offset=16
    local.set $l31
    local.get $p2
    f32.load offset=8
    local.set $l16
    local.get $p3
    f32.load offset=8
    local.set $l32
    local.get $p3
    f32.load offset=12
    local.set $l13
    local.get $p3
    f32.load offset=4
    local.set $l33
    local.get $p3
    f32.load
    local.set $l17
    local.get $p4
    i32.load offset=32
    local.set $p2
    local.get $p4
    f32.load offset=4
    local.set $l12
    local.get $p4
    f32.load offset=8
    local.set $l14
    local.get $p4
    f32.load offset=12
    local.set $l19
    local.get $l6
    i32.const 0
    i32.store offset=348
    local.get $l6
    local.get $l19
    f32.store offset=344
    local.get $l6
    local.get $l14
    f32.store offset=340
    local.get $l6
    local.get $l12
    f32.store offset=336
    local.get $p4
    i64.load offset=16 align=4
    local.set $l37
    local.get $l6
    local.get $p4
    i64.load offset=24 align=4
    i64.store offset=328
    local.get $l6
    local.get $l37
    i64.store offset=320
    local.get $l6
    i32.const 0
    i32.store8 offset=192
    local.get $l6
    i32.const 184
    i32.add
    local.tee $l7
    i64.const 0
    i64.store
    local.get $l6
    i32.const 176
    i32.add
    local.tee $l8
    i64.const 0
    i64.store
    local.get $l6
    i64.const 0
    i64.store offset=168
    local.get $l6
    i64.const 0
    i64.store offset=160
    local.get $l6
    local.get $p2
    i32.const 16
    i32.add
    i32.store offset=304
    local.get $l6
    local.get $p2
    i32.load offset=56
    local.get $p2
    i32.load8_u offset=55
    i32.const 20
    i32.mul
    i32.add
    i32.store offset=312
    local.get $l6
    local.get $p2
    i32.load8_u offset=54
    i32.store8 offset=316
    local.get $l7
    local.get $l12
    local.get $p2
    f32.load offset=68
    f32.mul
    local.tee $l15
    local.get $l14
    local.get $p2
    f32.load offset=72
    f32.mul
    local.tee $l18
    local.get $l15
    local.get $l18
    f32.le
    select
    local.tee $l15
    local.get $l19
    local.get $p2
    f32.load offset=76
    f32.mul
    local.tee $l18
    local.get $l15
    local.get $l18
    f32.le
    select
    local.tee $l15
    f32.const 0x1.99999ap-6 (;=0.025;)
    f32.mul
    f32.store
    local.get $l8
    local.get $l15
    f32.const 0x1.99999ap-4 (;=0.1;)
    f32.mul
    f32.store
    local.get $l6
    local.get $l15
    f32.const 0x1.99999ap-5 (;=0.05;)
    f32.mul
    f32.store offset=180
    local.get $l6
    i32.const 336
    i32.add
    local.get $l6
    i32.const 320
    i32.add
    local.get $l6
    i32.const 208
    i32.add
    local.tee $l7
    local.get $l6
    i32.const 256
    i32.add
    local.tee $l8
    local.get $l6
    i32.const 160
    i32.add
    local.get $l12
    f32.const 0x1p+0 (;=1;)
    f32.eq
    local.get $l14
    f32.const 0x1p+0 (;=1;)
    f32.eq
    i32.and
    local.get $l19
    f32.const 0x1p+0 (;=1;)
    f32.eq
    i32.and
    call $f70494
    local.get $l6
    local.get $p2
    i32.load offset=60
    i32.store offset=308
    local.get $l11
    f32.load
    local.set $l34
    local.get $l10
    f32.load
    local.set $l24
    local.get $p5
    f32.load offset=20
    local.set $l25
    local.get $p5
    f32.load offset=24
    local.set $l26
    local.get $p3
    f32.load offset=16
    local.set $l27
    local.get $p3
    f32.load
    local.set $l18
    local.get $p3
    f32.load offset=4
    local.set $l21
    local.get $p3
    f32.load offset=8
    local.set $l20
    local.get $p3
    f32.load offset=12
    local.set $l28
    local.get $p5
    f32.load
    local.set $l14
    local.get $p5
    f32.load offset=4
    local.set $l15
    local.get $p5
    f32.load offset=8
    local.set $l19
    local.get $p5
    f32.load offset=12
    local.set $l12
    local.get $p5
    f32.load offset=16
    local.set $l29
    local.get $l6
    i32.const 0
    i32.store offset=156
    local.get $l6
    local.get $l26
    f32.store offset=152
    local.get $l6
    local.get $l25
    f32.store offset=148
    local.get $l6
    local.get $l29
    f32.store offset=144
    local.get $l6
    local.get $l12
    f32.store offset=140
    local.get $l6
    local.get $l19
    f32.store offset=136
    local.get $l6
    local.get $l15
    f32.store offset=132
    local.get $l6
    local.get $l14
    f32.store offset=128
    local.get $l6
    i64.const 0
    i64.store offset=120
    local.get $l6
    i64.const 0
    i64.store offset=112
    local.get $l6
    i32.const 0
    i32.store offset=96
    local.get $l6
    i32.const 0
    i32.store offset=76
    local.get $l6
    i32.const 0
    i32.store offset=60
    local.get $l6
    local.get $l12
    local.get $l12
    f32.mul
    f32.const -0x1p-1 (;=-0.5;)
    f32.add
    local.tee $l36
    local.get $l24
    local.get $l26
    f32.sub
    local.tee $l26
    f32.mul
    local.get $l12
    local.get $l15
    local.get $l27
    local.get $l29
    f32.sub
    local.tee $l29
    f32.mul
    local.get $l14
    local.get $l34
    local.get $l25
    f32.sub
    local.tee $l25
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l19
    local.get $l25
    local.get $l15
    f32.neg
    local.tee $l35
    f32.mul
    local.get $l14
    local.get $l29
    f32.mul
    f32.sub
    local.get $l19
    local.get $l26
    f32.mul
    f32.sub
    local.tee $l34
    f32.mul
    f32.sub
    local.tee $l24
    local.get $l24
    f32.add
    local.tee $l24
    f32.store offset=8
    local.get $l6
    local.get $l24
    local.get $l31
    local.get $l16
    local.get $l17
    local.get $l17
    local.get $l17
    f32.add
    local.tee $l27
    f32.mul
    local.get $l13
    local.get $l13
    local.get $l13
    f32.add
    local.tee $l17
    f32.mul
    f32.const -0x1p+0 (;=-1;)
    f32.add
    f32.add
    f32.mul
    local.tee $l13
    f32.sub
    local.get $l31
    local.get $l13
    f32.add
    f32.sub
    local.tee $l13
    local.get $l13
    f32.mul
    local.get $l23
    local.get $l16
    local.get $l32
    local.get $l17
    f32.mul
    local.get $l27
    local.get $l33
    f32.mul
    f32.add
    f32.mul
    local.tee $l13
    f32.sub
    local.get $l23
    local.get $l13
    f32.add
    f32.sub
    local.tee $l13
    local.get $l13
    f32.mul
    f32.add
    local.get $l22
    local.get $l16
    local.get $l27
    local.get $l32
    f32.mul
    local.get $l17
    local.get $l33
    f32.mul
    f32.sub
    f32.mul
    local.tee $l16
    f32.sub
    local.get $l16
    local.get $l22
    f32.add
    f32.sub
    local.tee $l16
    local.get $l16
    f32.mul
    f32.add
    f32.sqrt
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    local.tee $l13
    local.get $l18
    local.get $l15
    f32.mul
    local.get $l21
    local.get $l14
    f32.mul
    f32.sub
    local.get $l20
    local.get $l12
    f32.mul
    local.get $l28
    local.get $l19
    f32.mul
    f32.sub
    f32.add
    local.tee $l16
    local.get $l21
    local.get $l19
    f32.mul
    local.get $l20
    local.get $l15
    f32.mul
    f32.sub
    local.get $l18
    local.get $l12
    f32.mul
    local.get $l28
    local.get $l14
    f32.mul
    f32.sub
    f32.add
    local.tee $l22
    local.get $l22
    f32.add
    local.tee $l17
    f32.mul
    local.tee $l31
    local.get $l28
    local.get $l12
    f32.mul
    local.get $l21
    local.get $l35
    f32.mul
    local.get $l18
    local.get $l14
    f32.mul
    f32.sub
    local.get $l20
    local.get $l19
    f32.mul
    f32.sub
    f32.sub
    local.tee $l23
    local.get $l20
    local.get $l14
    f32.mul
    local.get $l18
    local.get $l19
    f32.mul
    f32.sub
    local.get $l21
    local.get $l12
    f32.mul
    local.get $l28
    local.get $l15
    f32.mul
    f32.sub
    f32.add
    local.tee $l21
    local.get $l21
    f32.add
    local.tee $l20
    f32.mul
    local.tee $l28
    f32.sub
    f32.mul
    local.get $l13
    f32.const 0x0p+0 (;=0;)
    f32.mul
    local.tee $l18
    local.get $l16
    local.get $l20
    f32.mul
    local.tee $l32
    local.get $l23
    local.get $l17
    f32.mul
    local.tee $l33
    f32.add
    f32.mul
    f32.add
    local.get $l18
    f32.const 0x1p+0 (;=1;)
    local.get $l22
    local.get $l17
    f32.mul
    f32.sub
    local.tee $l22
    local.get $l21
    local.get $l20
    f32.mul
    local.tee $l27
    f32.sub
    f32.mul
    f32.add
    local.tee $l35
    f32.sub
    f32.store offset=72
    local.get $l6
    local.get $l36
    local.get $l25
    f32.mul
    local.get $l12
    local.get $l14
    local.get $l26
    f32.mul
    local.get $l19
    local.get $l29
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l15
    local.get $l34
    f32.mul
    f32.sub
    local.tee $l20
    local.get $l20
    f32.add
    local.tee $l20
    f32.store offset=4
    local.get $l6
    local.get $l20
    local.get $l18
    local.get $l32
    local.get $l33
    f32.sub
    f32.mul
    local.get $l13
    local.get $l21
    local.get $l17
    f32.mul
    local.tee $l21
    local.get $l23
    local.get $l16
    local.get $l16
    f32.add
    local.tee $l17
    f32.mul
    local.tee $l23
    f32.add
    f32.mul
    local.get $l18
    local.get $l22
    local.get $l16
    local.get $l17
    f32.mul
    local.tee $l16
    f32.sub
    f32.mul
    f32.add
    f32.add
    local.tee $l17
    f32.sub
    f32.store offset=68
    local.get $l6
    local.get $l24
    local.get $l35
    f32.add
    f32.store offset=56
    local.get $l6
    local.get $l20
    local.get $l17
    f32.add
    f32.store offset=52
    local.get $l6
    local.get $l30
    f32.store offset=80
    local.get $l6
    i32.const 0
    i32.store offset=12
    local.get $l6
    i32.const 4
    i32.store offset=28
    local.get $l6
    i32.const 1
    i32.store8 offset=32
    local.get $l6
    local.get $l30
    f32.store offset=24
    local.get $l6
    local.get $l30
    f32.store offset=20
    local.get $l6
    local.get $l30
    f32.store offset=16
    local.get $l6
    local.get $l36
    local.get $l29
    f32.mul
    local.get $l12
    local.get $l19
    local.get $l25
    f32.mul
    local.get $l15
    local.get $l26
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l14
    local.get $l34
    f32.mul
    f32.sub
    local.tee $l12
    local.get $l12
    f32.add
    local.tee $l12
    f32.store
    local.get $l6
    local.get $l12
    local.get $l18
    local.get $l31
    local.get $l28
    f32.add
    f32.mul
    local.get $l18
    local.get $l21
    local.get $l23
    f32.sub
    f32.mul
    local.get $l13
    f32.const 0x1p+0 (;=1;)
    local.get $l27
    f32.sub
    local.get $l16
    f32.sub
    f32.mul
    f32.add
    f32.add
    local.tee $l14
    f32.sub
    f32.store offset=64
    local.get $l6
    local.get $l12
    local.get $l14
    f32.add
    f32.store offset=48
    block $B0
      local.get $p4
      f32.load offset=4
      f32.const 0x1p+0 (;=1;)
      f32.ne
      br_if $B0
      local.get $p4
      f32.load offset=8
      f32.const 0x1p+0 (;=1;)
      f32.ne
      br_if $B0
      local.get $p4
      f32.load offset=12
      f32.const 0x1p+0 (;=1;)
      f32.eq
      local.set $l9
    end
    local.get $l6
    i32.const 160
    i32.add
    local.get $l9
    local.get $l6
    i32.const 424
    i32.add
    call $f70029
    local.get $l6
    local.get $l9
    i32.store8 offset=396
    local.get $l6
    local.get $l8
    i32.store offset=392
    local.get $l6
    local.get $l7
    i32.store offset=388
    local.get $l6
    i32.const 3125832
    i32.const 3125860
    local.get $l9
    select
    i32.store offset=352
    local.get $l6
    local.get $l6
    i32.const 128
    i32.add
    i32.store offset=384
    local.get $l6
    local.get $l6
    i32.const 160
    i32.add
    i32.store offset=400
    local.get $l6
    i32.const 96
    i32.add
    local.set $l7
    local.get $l6
    i32.const 112
    i32.add
    local.set $p5
    global.get $g0
    i32.const 48
    i32.sub
    local.tee $p3
    global.set $g0
    local.get $p3
    i32.const 0
    i32.store offset=32
    local.get $l6
    local.get $l6
    i32.const 424
    i32.add
    local.get $l6
    i32.const 352
    i32.add
    local.tee $p4
    local.get $p3
    i32.const 32
    i32.add
    local.get $p3
    local.get $p3
    i32.const 16
    i32.add
    call $f70034
    local.tee $p2
    if $I1
      local.get $p4
      i32.load offset=32
      local.tee $p4
      f32.load offset=8
      local.set $l13
      local.get $p4
      f32.load offset=12
      local.set $l12
      local.get $p4
      f32.load
      local.set $l14
      local.get $p4
      f32.load offset=4
      local.set $l15
      local.get $p3
      f32.load offset=24
      local.set $l16
      local.get $p3
      f32.load offset=20
      local.set $l17
      local.get $p3
      f32.load offset=16
      local.set $l18
      local.get $p5
      i32.const 0
      i32.store offset=12
      local.get $p5
      local.get $l13
      local.get $l14
      local.get $l18
      f32.mul
      local.get $l15
      local.get $l17
      f32.mul
      f32.add
      local.get $l13
      local.get $l16
      f32.mul
      f32.add
      local.tee $l20
      f32.mul
      local.get $l16
      local.get $l12
      local.get $l12
      f32.mul
      f32.const -0x1p-1 (;=-0.5;)
      f32.add
      local.tee $l21
      f32.mul
      local.get $l12
      local.get $l14
      local.get $l17
      f32.mul
      local.get $l15
      local.get $l18
      f32.mul
      f32.sub
      f32.mul
      f32.add
      f32.add
      local.tee $l19
      local.get $l19
      f32.add
      f32.store offset=8
      local.get $p5
      local.get $l15
      local.get $l20
      f32.mul
      local.get $l21
      local.get $l17
      f32.mul
      local.get $l12
      local.get $l13
      local.get $l18
      f32.mul
      local.get $l14
      local.get $l16
      f32.mul
      f32.sub
      f32.mul
      f32.add
      f32.add
      local.tee $l19
      local.get $l19
      f32.add
      f32.store offset=4
      local.get $p5
      local.get $l14
      local.get $l20
      f32.mul
      local.get $l18
      local.get $l21
      f32.mul
      local.get $l12
      local.get $l15
      local.get $l16
      f32.mul
      local.get $l13
      local.get $l17
      f32.mul
      f32.sub
      f32.mul
      f32.add
      f32.add
      local.tee $l12
      local.get $l12
      f32.add
      f32.store
      local.get $l7
      local.get $p3
      i64.load offset=8
      i64.store offset=8
      local.get $l7
      local.get $p3
      i64.load
      i64.store
    end
    local.get $p3
    i32.const 48
    i32.add
    global.set $g0
    local.get $p2
    local.tee $p3
    if $I2
      local.get $p1
      local.get $l6
      f32.load offset=96
      local.tee $l12
      f32.const 0x0p+0 (;=0;)
      local.get $l12
      f32.const 0x0p+0 (;=0;)
      f32.gt
      select
      f32.store
      local.get $l6
      i64.load offset=112
      local.set $l37
      local.get $p0
      local.get $l6
      f32.load offset=120
      f32.store offset=8
      local.get $p0
      local.get $l37
      i64.store align=4
    end
    local.get $l6
    i32.const 496
    i32.add
    global.set $g0
    local.get $p3)
