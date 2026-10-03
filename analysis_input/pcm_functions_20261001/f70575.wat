  (func $f70575 (type $t18) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 i32) (param $p7 i32) (result i32)
    (local $l8 i32) (local $l9 i32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 i64) (local $l20 i64) (local $l21 i64)
    global.get $g0
    i32.const 720
    i32.sub
    local.tee $l8
    global.set $g0
    local.get $p5
    i32.load
    local.set $l9
    local.get $p0
    f32.load offset=8
    local.set $l10
    local.get $p0
    f32.load offset=4
    local.set $l11
    local.get $l8
    local.get $p0
    f32.load offset=12
    local.tee $l12
    f32.store offset=716
    local.get $l8
    local.get $l10
    f32.store offset=712
    local.get $l8
    local.get $l11
    f32.store offset=708
    local.get $l8
    local.get $l12
    f32.neg
    local.tee $l13
    f32.store offset=704
    local.get $l8
    local.get $l10
    f32.neg
    local.tee $l14
    f32.store offset=700
    local.get $l8
    local.get $l11
    f32.neg
    local.tee $l15
    f32.store offset=696
    block $B0 (result i32)
      i32.const 0
      local.get $p1
      f32.load offset=4
      f32.const 0x1p+0 (;=1;)
      f32.ne
      br_if $B0
      drop
      i32.const 0
      local.get $p1
      f32.load offset=8
      f32.const 0x1p+0 (;=1;)
      f32.ne
      br_if $B0
      drop
      local.get $p1
      f32.load offset=12
      f32.const 0x1p+0 (;=1;)
      f32.eq
    end
    local.set $p5
    local.get $l8
    i64.const 4575657221408423936
    i64.store offset=680
    local.get $l8
    i64.const 0
    i64.store offset=672
    local.get $l8
    i64.const 4575657221408423936
    i64.store offset=664
    local.get $l8
    i64.const 0
    i64.store offset=656
    local.get $l8
    i64.const 4575657222473777152
    i64.store offset=648
    local.get $l8
    i64.const 1065353216
    i64.store offset=632
    local.get $l8
    i32.const 0
    i32.store8 offset=688
    local.get $l8
    i64.const 0
    i64.store offset=640
    local.get $l8
    i64.const 0
    i64.store offset=624
    local.get $l8
    i64.const 1065353216
    i64.store offset=616
    local.get $p5
    i32.eqz
    if $I1
      local.get $l8
      i32.const 616
      i32.add
      local.get $p1
      i32.const 4
      i32.add
      local.get $p1
      i32.const 16
      i32.add
      call $f70485
      local.get $p0
      f32.load offset=8
      local.tee $l10
      f32.neg
      local.set $l14
      local.get $p0
      f32.load offset=4
      local.tee $l11
      f32.neg
      local.set $l15
      local.get $p0
      f32.load offset=12
      local.tee $l12
      f32.neg
      local.set $l13
    end
    local.get $l8
    i64.const 4575657221408423936
    i64.store offset=600
    local.get $l8
    i64.const 0
    i64.store offset=592
    local.get $l8
    i64.const 4575657221408423936
    i64.store offset=584
    local.get $l8
    i64.const 0
    i64.store offset=576
    local.get $l8
    i64.const 4575657222473777152
    i64.store offset=568
    local.get $l8
    i64.const 1065353216
    i64.store offset=552
    local.get $l8
    i32.const 0
    i32.store8 offset=608
    local.get $l8
    i64.const 0
    i64.store offset=560
    local.get $l8
    i64.const 0
    i64.store offset=544
    local.get $l8
    i64.const 1065353216
    i64.store offset=536
    local.get $l8
    local.get $p4
    f32.load offset=8
    f32.const 0x1.99999ap-5 (;=0.05;)
    f32.mul
    local.tee $l17
    local.get $l11
    local.get $l10
    local.get $l10
    local.get $l11
    f32.ge
    select
    local.tee $l16
    local.get $l12
    local.get $l12
    local.get $l16
    f32.ge
    select
    local.tee $l18
    f32.const 0x1.333334p-3 (;=0.15;)
    f32.mul
    local.tee $l16
    local.get $l16
    local.get $l17
    f32.gt
    select
    f32.store offset=512
    local.get $l8
    i32.const 0
    i32.store offset=508
    local.get $l8
    local.get $l12
    f32.store offset=504
    local.get $l8
    local.get $l10
    f32.store offset=500
    local.get $l8
    i64.const 0
    i64.store offset=456
    local.get $l8
    i64.const 0
    i64.store offset=448
    local.get $l8
    local.get $l11
    f32.store offset=496
    local.get $l8
    i32.const 0
    i32.store8 offset=480
    local.get $l8
    i32.const 3
    i32.store offset=476
    local.get $l8
    local.get $l18
    f32.const 0x1.99999ap-5 (;=0.05;)
    f32.mul
    local.tee $l17
    f32.store offset=472
    local.get $l8
    local.get $l17
    f32.store offset=468
    local.get $l8
    local.get $l16
    f32.store offset=464
    local.get $p2
    f32.load offset=24
    local.set $l16
    local.get $p2
    i64.load align=4
    local.set $l19
    local.get $p2
    i64.load offset=8 align=4
    local.set $l20
    local.get $p2
    i64.load offset=16 align=4
    local.set $l21
    local.get $l8
    i32.const 0
    i32.store offset=444
    local.get $l8
    local.get $l16
    f32.store offset=440
    local.get $l8
    local.get $l21
    i64.store offset=432
    local.get $l8
    local.get $l20
    i64.store offset=424
    local.get $l8
    local.get $l19
    i64.store offset=416
    local.get $l8
    i32.const 4
    i32.store8 offset=238
    local.get $l8
    local.get $l12
    f32.store offset=216
    local.get $l8
    local.get $l10
    f32.store offset=212
    local.get $l8
    local.get $l15
    f32.store offset=208
    local.get $l8
    local.get $l12
    f32.store offset=204
    local.get $l8
    local.get $l10
    f32.store offset=200
    local.get $l8
    local.get $l11
    f32.store offset=196
    local.get $l8
    local.get $l12
    f32.store offset=192
    local.get $l8
    local.get $l14
    f32.store offset=188
    local.get $l8
    local.get $l11
    f32.store offset=184
    local.get $l8
    local.get $l12
    f32.store offset=180
    local.get $l8
    local.get $l14
    f32.store offset=176
    local.get $l8
    local.get $l15
    f32.store offset=172
    local.get $l8
    local.get $l13
    f32.store offset=168
    local.get $l8
    local.get $l10
    f32.store offset=164
    local.get $l8
    local.get $l15
    f32.store offset=160
    local.get $l8
    local.get $l13
    f32.store offset=156
    local.get $l8
    local.get $l10
    f32.store offset=152
    local.get $l8
    local.get $l11
    f32.store offset=148
    local.get $l8
    local.get $l13
    f32.store offset=144
    local.get $l8
    local.get $l14
    f32.store offset=140
    local.get $l8
    local.get $l11
    f32.store offset=136
    local.get $l8
    local.get $l13
    f32.store offset=132
    local.get $l8
    local.get $l14
    f32.store offset=128
    local.get $l8
    local.get $l15
    f32.store offset=124
    local.get $l8
    local.get $p0
    i32.const 4
    i32.add
    i32.store offset=120
    local.get $l8
    i32.const 0
    i32.store16 offset=236
    local.get $l8
    i32.const 4
    i32.store8 offset=278
    local.get $l8
    i32.const 262148
    i32.store offset=256
    local.get $l8
    i32.const 8
    i32.store16 offset=276
    local.get $l8
    i32.const 4
    i32.store8 offset=318
    local.get $l8
    i32.const 17039372
    i32.store offset=296
    local.get $l8
    i32.const 4
    i32.store8 offset=338
    local.get $l8
    i32.const 16
    i32.store16 offset=316
    local.get $l8
    i32.const 20
    i32.store16 offset=336
    local.get $l8
    local.get $l15
    f32.store offset=252
    local.get $l8
    local.get $l15
    f32.store offset=292
    local.get $l8
    i64.const 1065353216
    i64.store offset=240
    local.get $l8
    i64.const 3212836864
    i64.store offset=280
    local.get $l8
    i32.const 0
    i32.store offset=288
    local.get $l8
    i32.const 0
    i32.store offset=248
    local.get $l8
    local.get $l14
    f32.store offset=312
    local.get $l8
    local.get $l14
    f32.store offset=332
    local.get $l8
    i64.const 4575657221408423936
    i64.store offset=300 align=4
    local.get $l8
    i64.const -4647714815446351872
    i64.store offset=320
    local.get $l8
    i32.const 0
    i32.store offset=328
    local.get $l8
    i32.const 0
    i32.store offset=308
    local.get $l8
    i32.const 2
    i32.store8 offset=339
    local.get $l8
    i32.const 0
    i32.store8 offset=319
    local.get $l8
    local.get $l13
    f32.store offset=272
    local.get $l8
    i64.const 0
    i64.store offset=260 align=4
    local.get $l8
    i32.const 1065353216
    i32.store offset=268
    local.get $l8
    i32.const 0
    i32.store8 offset=279
    local.get $l8
    i32.const -1082130432
    i32.store offset=228
    local.get $l8
    local.get $l13
    f32.store offset=232
    local.get $l8
    i32.const 4
    i32.store8 offset=239
    local.get $l8
    i64.const 0
    i64.store offset=396 align=4
    local.get $l8
    i64.const 0
    i64.store offset=388 align=4
    local.get $l8
    i64.const 0
    i64.store offset=220 align=4
    local.get $l8
    local.get $l8
    i32.const 220
    i32.add
    i32.store offset=368
    local.get $l8
    i64.const 0
    i64.store offset=344
    local.get $l8
    i64.const 34359738368
    i64.store offset=352
    local.get $l8
    i32.const 3124144
    i32.store offset=376
    local.get $l8
    local.get $l8
    i32.const 120
    i32.add
    i32.const 4
    i32.or
    i32.store offset=372
    local.get $l8
    i64.const 6
    i64.store offset=360
    local.get $l8
    i64.const 0
    i64.store offset=380 align=4
    local.get $l8
    i64.const 0
    i64.store offset=88
    local.get $l8
    i32.const 1065353216
    i32.store offset=84
    local.get $l8
    i64.const 0
    i64.store offset=96
    local.get $l8
    i64.const 1065353216
    i64.store offset=104
    local.get $l8
    i64.const 0
    i64.store offset=68 align=4
    local.get $l8
    i32.const 1065353216
    i32.store offset=64
    local.get $l8
    i64.const 0
    i64.store offset=76 align=4
    local.get $l8
    i32.const 1
    i32.store8 offset=44
    local.get $l8
    i32.const 3125888
    i32.store
    local.get $l8
    local.get $l8
    i32.const -64
    i32.sub
    i32.store offset=40
    local.get $l8
    local.get $l8
    i32.const -64
    i32.sub
    i32.store offset=36
    local.get $l8
    local.get $l8
    i32.const 416
    i32.add
    i32.store offset=32
    local.get $l8
    local.get $l8
    i32.const 448
    i32.add
    i32.store offset=48
    local.get $l8
    i32.const 344
    i32.add
    local.get $l8
    local.get $l8
    i32.const 512
    i32.add
    local.get $l8
    i32.const 696
    i32.add
    local.get $p1
    local.get $p2
    local.get $p3
    local.get $p4
    f32.load
    local.get $p6
    local.get $l8
    i32.const 536
    i32.add
    local.get $l8
    i32.const 616
    i32.add
    i32.const 1
    local.get $p5
    local.get $l9
    local.get $p7
    call $f70030
    local.set $p0
    local.get $l8
    i32.const 720
    i32.add
    global.set $g0
    local.get $p0)
