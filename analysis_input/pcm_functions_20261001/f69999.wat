  (func $f69999 (type $t30) (param $p0 i32) (param $p1 i32) (param $p2 f32) (param $p3 i32)
    (local $l4 f32) (local $l5 f32) (local $l6 f32) (local $l7 f32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 i32) (local $l27 i32) (local $l28 i32) (local $l29 i32)
    local.get $p0
    f32.load offset=44
    local.set $l4
    local.get $p0
    f32.load offset=40
    local.set $l5
    local.get $p0
    f32.load offset=36
    local.set $l6
    local.get $p0
    f32.load
    local.set $l10
    local.get $p0
    f32.load offset=4
    local.set $l11
    local.get $p3
    local.get $p0
    f32.load offset=8
    local.tee $l13
    f32.store offset=412
    local.get $p3
    local.get $l11
    f32.store offset=400
    local.get $p3
    local.get $l10
    f32.store offset=388
    local.get $p3
    local.get $l6
    local.get $l10
    f32.mul
    local.get $l5
    local.get $l11
    f32.mul
    f32.add
    local.get $l4
    local.get $l13
    f32.mul
    f32.add
    f32.neg
    f32.store offset=424
    local.get $p0
    i32.const 16
    i32.add
    local.tee $l27
    f32.load
    local.set $l12
    local.get $p0
    f32.load offset=12
    local.set $l14
    local.get $p3
    local.get $p0
    i32.const 20
    i32.add
    local.tee $l28
    f32.load
    local.tee $l18
    f32.store offset=416
    local.get $p3
    local.get $l12
    f32.store offset=404
    local.get $p3
    local.get $l14
    f32.store offset=392
    local.get $p3
    local.get $l6
    local.get $l14
    f32.mul
    local.get $l5
    local.get $l12
    f32.mul
    f32.add
    local.get $l4
    local.get $l18
    f32.mul
    f32.add
    f32.neg
    f32.store offset=428
    local.get $p0
    i32.const 28
    i32.add
    local.tee $l26
    f32.load
    local.set $l15
    local.get $p0
    f32.load offset=24
    local.set $l16
    local.get $p3
    local.get $p0
    i32.const 32
    i32.add
    local.tee $l29
    f32.load
    local.tee $l19
    f32.store offset=420
    local.get $p3
    local.get $l15
    f32.store offset=408
    local.get $p3
    local.get $l16
    f32.store offset=396
    local.get $p3
    local.get $l6
    local.get $l16
    f32.mul
    local.get $l5
    local.get $l15
    f32.mul
    f32.add
    local.get $l4
    local.get $l19
    f32.mul
    f32.add
    f32.neg
    f32.store offset=432
    local.get $p3
    local.get $p0
    f32.load offset=48
    local.tee $l22
    f32.store offset=436
    local.get $p3
    local.get $p0
    f32.load offset=52
    local.tee $l20
    f32.store offset=440
    local.get $p3
    local.get $p0
    f32.load offset=56
    local.tee $l21
    f32.store offset=444
    local.get $p1
    f32.load
    local.set $l9
    local.get $p1
    f32.load offset=4
    local.set $l7
    local.get $p1
    f32.load offset=8
    local.set $l8
    local.get $p3
    local.get $p2
    f32.store offset=260
    local.get $p3
    local.get $l8
    f32.store offset=256
    local.get $p3
    local.get $l7
    f32.store offset=252
    local.get $p3
    local.get $l9
    f32.store offset=248
    local.get $p3
    local.get $l21
    f32.store offset=244
    local.get $p3
    local.get $l20
    f32.store offset=240
    local.get $p3
    local.get $l22
    f32.store offset=236
    local.get $p3
    local.get $l4
    f32.store offset=232
    local.get $p3
    local.get $l5
    f32.store offset=228
    local.get $p3
    local.get $l6
    f32.store offset=224
    local.get $p3
    local.get $l19
    f32.store offset=220
    local.get $p3
    local.get $l15
    f32.store offset=216
    local.get $p3
    local.get $l16
    f32.store offset=212
    local.get $p3
    local.get $l18
    f32.store offset=208
    local.get $p3
    local.get $l12
    f32.store offset=204
    local.get $p3
    local.get $l14
    f32.store offset=200
    local.get $p3
    local.get $l13
    f32.store offset=196
    local.get $p3
    local.get $l11
    f32.store offset=192
    local.get $p3
    local.get $l10
    f32.store offset=188
    local.get $p3
    local.get $l16
    local.get $l9
    f32.mul
    local.get $l15
    local.get $l7
    f32.mul
    f32.add
    local.get $l19
    local.get $l8
    f32.mul
    f32.add
    local.tee $l4
    f32.store offset=456
    local.get $p3
    local.get $l14
    local.get $l9
    f32.mul
    local.get $l12
    local.get $l7
    f32.mul
    f32.add
    local.get $l18
    local.get $l8
    f32.mul
    f32.add
    local.tee $l5
    f32.store offset=452
    local.get $p3
    local.get $l10
    local.get $l9
    f32.mul
    local.get $l11
    local.get $l7
    f32.mul
    f32.add
    local.get $l13
    local.get $l8
    f32.mul
    f32.add
    local.tee $l6
    f32.store offset=448
    local.get $p3
    f32.const 0x1p+0 (;=1;)
    local.get $l4
    f32.div
    f32.const 0x0p+0 (;=0;)
    local.get $l4
    f32.const 0x0p+0 (;=0;)
    f32.ne
    select
    local.tee $l10
    f32.store offset=480
    local.get $p3
    f32.const 0x1p+0 (;=1;)
    local.get $l5
    f32.div
    f32.const 0x0p+0 (;=0;)
    local.get $l5
    f32.const 0x0p+0 (;=0;)
    f32.ne
    select
    local.tee $l5
    f32.store offset=476
    local.get $p3
    f32.const 0x1p+0 (;=1;)
    local.get $l6
    f32.div
    f32.const 0x0p+0 (;=0;)
    local.get $l6
    f32.const 0x0p+0 (;=0;)
    f32.ne
    select
    local.tee $l6
    f32.store offset=472
    local.get $p3
    f32.const 0x1p+0 (;=1;)
    local.get $p2
    f32.div
    local.tee $l4
    local.get $l10
    f32.mul
    f32.store offset=468
    local.get $p3
    local.get $l4
    local.get $l5
    f32.mul
    f32.store offset=464
    local.get $p3
    local.get $l4
    local.get $l6
    f32.mul
    f32.store offset=460
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $p1
    local.get $l9
    local.get $p0
    f32.load
    local.tee $l14
    f32.mul
    local.get $l7
    local.get $p0
    f32.load offset=4
    local.tee $l15
    f32.mul
    f32.add
    local.get $l8
    local.get $p0
    f32.load offset=8
    local.tee $l16
    f32.mul
    f32.add
    local.tee $l10
    f32.abs
    local.tee $l4
    f32.store offset=4
    local.get $p1
    local.get $l9
    local.get $p0
    f32.load offset=12
    local.tee $l13
    f32.mul
    local.get $l7
    local.get $l27
    f32.load
    local.tee $l18
    f32.mul
    f32.add
    local.get $l8
    local.get $l28
    f32.load
    local.tee $l19
    f32.mul
    f32.add
    local.tee $l11
    f32.abs
    local.tee $l5
    f32.store offset=8
    local.get $p1
    local.get $l9
    local.get $p0
    f32.load offset=24
    local.tee $l23
    f32.mul
    local.get $l7
    local.get $l26
    f32.load
    local.tee $l24
    f32.mul
    f32.add
    local.get $l8
    local.get $l29
    f32.load
    local.tee $l25
    f32.mul
    f32.add
    local.tee $l12
    f32.abs
    local.tee $l6
    f32.store offset=12
    local.get $p0
    i32.const 1
    i32.const 2
    local.get $l6
    local.get $l5
    local.get $l4
    local.get $l4
    local.get $l5
    f32.lt
    local.tee $l26
    select
    f32.gt
    local.tee $l27
    select
    local.tee $l28
    local.get $l26
    local.get $l27
    i32.or
    i32.const 1
    i32.xor
    local.tee $l26
    local.get $p1
    i32.const 4
    i32.add
    local.get $l28
    i32.const 2
    i32.shl
    i32.add
    f32.load
    local.get $p1
    i32.const 4
    i32.add
    local.get $l26
    i32.const 2
    i32.shl
    i32.add
    f32.load
    f32.lt
    select
    i32.const 12
    i32.mul
    i32.add
    local.tee $p1
    f32.load offset=8
    local.tee $l4
    local.get $l8
    local.get $l9
    local.get $p1
    f32.load
    local.tee $l5
    f32.mul
    local.get $l7
    local.get $p1
    f32.load offset=4
    local.tee $l17
    f32.mul
    f32.add
    local.get $l8
    local.get $l4
    f32.mul
    f32.add
    local.tee $l6
    f32.mul
    f32.sub
    local.tee $l4
    local.get $l4
    f32.mul
    local.get $l5
    local.get $l9
    local.get $l6
    f32.mul
    f32.sub
    local.tee $l5
    local.get $l5
    f32.mul
    local.get $l17
    local.get $l7
    local.get $l6
    f32.mul
    f32.sub
    local.tee $l6
    local.get $l6
    f32.mul
    f32.add
    f32.add
    f32.sqrt
    local.tee $l17
    f32.const 0x0p+0 (;=0;)
    f32.gt
    if $I0
      local.get $l4
      f32.const 0x1p+0 (;=1;)
      local.get $l17
      f32.div
      local.tee $l17
      f32.mul
      local.set $l4
      local.get $l6
      local.get $l17
      f32.mul
      local.set $l6
      local.get $l5
      local.get $l17
      f32.mul
      local.set $l5
    end
    local.get $p3
    i32.const 1056964608
    i32.store offset=328
    local.get $p3
    local.get $l21
    local.get $l12
    f32.mul
    f32.abs
    local.get $l22
    local.get $l10
    f32.mul
    f32.abs
    local.get $l20
    local.get $l11
    f32.mul
    f32.abs
    f32.add
    f32.add
    local.tee $l17
    f32.store offset=340
    local.get $p3
    i32.const 332
    i32.add
    local.tee $p1
    local.get $l9
    local.get $l5
    f32.mul
    local.get $l7
    local.get $l6
    f32.mul
    f32.add
    local.get $l8
    local.get $l4
    f32.mul
    f32.add
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.store
    local.get $p3
    i32.const 336
    i32.add
    local.tee $l26
    local.get $l8
    local.get $l9
    local.get $l6
    f32.mul
    local.get $l7
    local.get $l5
    f32.mul
    f32.sub
    local.tee $l10
    f32.mul
    local.get $l9
    local.get $l7
    local.get $l4
    f32.mul
    local.get $l8
    local.get $l6
    f32.mul
    f32.sub
    local.tee $l11
    f32.mul
    local.get $l7
    local.get $l8
    local.get $l5
    f32.mul
    local.get $l9
    local.get $l4
    f32.mul
    f32.sub
    local.tee $l12
    f32.mul
    f32.add
    f32.add
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.store
    local.get $p3
    i32.const 344
    i32.add
    local.tee $l27
    local.get $l21
    local.get $l23
    local.get $l5
    f32.mul
    local.get $l24
    local.get $l6
    f32.mul
    f32.add
    local.get $l25
    local.get $l4
    f32.mul
    f32.add
    f32.mul
    f32.abs
    local.get $l22
    local.get $l14
    local.get $l5
    f32.mul
    local.get $l15
    local.get $l6
    f32.mul
    f32.add
    local.get $l16
    local.get $l4
    f32.mul
    f32.add
    f32.mul
    f32.abs
    local.get $l20
    local.get $l13
    local.get $l5
    f32.mul
    local.get $l18
    local.get $l6
    f32.mul
    f32.add
    local.get $l19
    local.get $l4
    f32.mul
    f32.add
    f32.mul
    f32.abs
    f32.add
    f32.add
    f32.store
    local.get $p3
    local.get $l21
    local.get $l23
    local.get $l11
    f32.mul
    local.get $l24
    local.get $l12
    f32.mul
    f32.add
    local.get $l25
    local.get $l10
    f32.mul
    f32.add
    f32.mul
    f32.abs
    local.get $l22
    local.get $l14
    local.get $l11
    f32.mul
    local.get $l15
    local.get $l12
    f32.mul
    f32.add
    local.get $l16
    local.get $l10
    f32.mul
    f32.add
    f32.mul
    f32.abs
    local.get $l20
    local.get $l13
    local.get $l11
    f32.mul
    local.get $l18
    local.get $l12
    f32.mul
    f32.add
    local.get $l19
    local.get $l10
    f32.mul
    f32.add
    f32.mul
    f32.abs
    f32.add
    f32.add
    local.tee $l22
    f32.store offset=348
    local.get $p0
    f32.load offset=44
    local.set $l20
    local.get $p0
    f32.load offset=36
    local.set $l21
    local.get $p0
    f32.load offset=40
    local.set $l13
    local.get $p3
    local.get $l9
    f32.abs
    f32.const 0x1.0c6f7ap-20 (;=1e-06;)
    f32.add
    local.tee $l14
    f32.store offset=352
    local.get $p3
    local.get $l14
    f32.store offset=128
    local.get $p3
    local.get $l12
    f32.store offset=120
    local.get $p3
    local.get $l5
    f32.store offset=116
    local.get $p3
    local.get $l8
    f32.store offset=112
    local.get $p3
    local.get $l11
    f32.store offset=104
    local.get $p3
    local.get $l4
    f32.store offset=100
    local.get $p3
    local.get $l7
    f32.store offset=96
    local.get $p3
    local.get $l10
    f32.store offset=88
    local.get $p3
    local.get $l6
    f32.store offset=84
    local.get $p3
    local.get $l9
    f32.store offset=80
    local.get $p3
    local.get $l7
    f32.abs
    f32.const 0x1.0c6f7ap-20 (;=1e-06;)
    f32.add
    local.tee $l15
    f32.store offset=356
    local.get $p3
    local.get $l15
    f32.store offset=144
    local.get $p3
    local.get $l8
    f32.abs
    f32.const 0x1.0c6f7ap-20 (;=1e-06;)
    f32.add
    local.tee $l16
    f32.store offset=360
    local.get $p3
    local.get $l16
    f32.store offset=160
    local.get $p3
    local.get $l5
    f32.abs
    f32.const 0x1.0c6f7ap-20 (;=1e-06;)
    f32.add
    local.tee $l5
    f32.store offset=364
    local.get $p3
    local.get $l5
    f32.store offset=164
    local.get $p3
    local.get $l17
    local.get $l9
    local.get $l21
    f32.mul
    local.get $l7
    local.get $l13
    f32.mul
    f32.add
    local.get $l8
    local.get $l20
    f32.mul
    f32.add
    f32.add
    f32.store offset=324
    local.get $p3
    local.get $l6
    f32.abs
    f32.const 0x1.0c6f7ap-20 (;=1e-06;)
    f32.add
    local.tee $l6
    f32.store offset=368
    local.get $p3
    local.get $l6
    f32.store offset=132
    local.get $p3
    local.get $l4
    f32.abs
    f32.const 0x1.0c6f7ap-20 (;=1e-06;)
    f32.add
    local.tee $l4
    f32.store offset=372
    local.get $p3
    local.get $l4
    f32.store offset=148
    local.get $p3
    local.get $l11
    f32.abs
    f32.const 0x1.0c6f7ap-20 (;=1e-06;)
    f32.add
    local.tee $l11
    f32.store offset=376
    local.get $p3
    local.get $l11
    f32.store offset=152
    local.get $p3
    local.get $l12
    f32.abs
    f32.const 0x1.0c6f7ap-20 (;=1e-06;)
    f32.add
    local.tee $l12
    f32.store offset=380
    local.get $p3
    local.get $l12
    f32.store offset=168
    local.get $p3
    local.get $l10
    f32.abs
    f32.const 0x1.0c6f7ap-20 (;=1e-06;)
    f32.add
    local.tee $l10
    f32.store offset=384
    local.get $p3
    local.get $l10
    f32.store offset=136
    local.get $l27
    f32.load
    local.set $l7
    local.get $p1
    f32.load
    local.set $l8
    local.get $p3
    f32.load offset=224
    local.set $l20
    local.get $p3
    f32.load offset=248
    local.set $l21
    local.get $p3
    f32.load offset=228
    local.set $l13
    local.get $p3
    f32.load offset=252
    local.set $l18
    local.get $p3
    f32.load offset=232
    local.set $l19
    local.get $p3
    f32.load offset=256
    local.set $l23
    local.get $p3
    f32.load offset=328
    local.set $l24
    local.get $p3
    local.get $l26
    f32.load
    local.get $p2
    f32.mul
    local.get $l22
    f32.add
    local.tee $l9
    f32.store offset=72
    local.get $p3
    local.get $l7
    local.get $l8
    local.get $p2
    f32.mul
    f32.add
    local.tee $l7
    f32.store offset=68
    local.get $p3
    local.get $l17
    local.get $l24
    local.get $p2
    f32.mul
    f32.add
    local.tee $l8
    f32.store offset=64
    local.get $p3
    local.get $l19
    local.get $l23
    local.get $p2
    f32.mul
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.add
    f32.store offset=40
    local.get $p3
    local.get $l13
    local.get $l18
    local.get $p2
    f32.mul
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.add
    f32.store offset=36
    local.get $p3
    local.get $l20
    local.get $l21
    local.get $p2
    f32.mul
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.add
    f32.store offset=32
    local.get $p3
    local.get $l8
    local.get $l16
    f32.mul
    local.get $l7
    local.get $l4
    f32.mul
    f32.add
    local.get $l9
    local.get $l10
    f32.mul
    f32.add
    f32.store offset=56
    local.get $p3
    local.get $l8
    local.get $l15
    f32.mul
    local.get $l7
    local.get $l6
    f32.mul
    f32.add
    local.get $l9
    local.get $l12
    f32.mul
    f32.add
    f32.store offset=52
    local.get $p3
    local.get $l8
    local.get $l14
    f32.mul
    local.get $l7
    local.get $l5
    f32.mul
    f32.add
    local.get $l9
    local.get $l11
    f32.mul
    f32.add
    f32.store offset=48)
