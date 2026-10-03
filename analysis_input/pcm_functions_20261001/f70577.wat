  (func $f70577 (type $t18) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 i32) (param $p7 i32) (result i32)
    (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 i64) (local $l23 i64) (local $l24 i64)
    global.get $g0
    i32.const 560
    i32.sub
    local.tee $l8
    global.set $g0
    local.get $p0
    i32.load offset=40
    local.set $l9
    local.get $p5
    i32.load
    local.set $l11
    local.get $p2
    f32.load offset=24
    local.set $l16
    local.get $p2
    i64.load align=4
    local.set $l22
    local.get $p2
    i64.load offset=8 align=4
    local.set $l23
    local.get $p2
    i64.load offset=16 align=4
    local.set $l24
    local.get $l8
    i32.const 0
    i32.store offset=556
    local.get $l8
    local.get $l16
    f32.store offset=552
    local.get $l8
    local.get $l24
    i64.store offset=544
    local.get $l8
    local.get $l23
    i64.store offset=536
    local.get $l8
    local.get $l22
    i64.store offset=528
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
    i64.store offset=512
    local.get $l8
    i64.const 0
    i64.store offset=504
    local.get $l8
    i64.const 4575657221408423936
    i64.store offset=496
    local.get $l8
    i64.const 0
    i64.store offset=488
    local.get $l8
    i64.const 4575657222473777152
    i64.store offset=480
    local.get $l8
    i64.const 1065353216
    i64.store offset=464
    local.get $l8
    i32.const 0
    i32.store8 offset=520
    local.get $l8
    i64.const 0
    i64.store offset=472
    local.get $l8
    i64.const 0
    i64.store offset=456
    local.get $l8
    i64.const 1065353216
    i64.store offset=448
    local.get $p5
    i32.eqz
    if $I1
      local.get $l8
      i32.const 448
      i32.add
      local.get $p1
      i32.const 4
      i32.add
      local.get $p1
      i32.const 16
      i32.add
      call $f70485
    end
    local.get $l8
    i64.const 4575657221408423936
    i64.store offset=432
    local.get $l8
    i64.const 0
    i64.store offset=424
    local.get $l8
    i64.const 4575657221408423936
    i64.store offset=416
    local.get $l8
    i64.const 0
    i64.store offset=408
    local.get $l8
    i64.const 4575657222473777152
    i64.store offset=400
    local.get $l8
    i64.const 1065353216
    i64.store offset=384
    local.get $l8
    i32.const 0
    i32.store8 offset=440
    local.get $l8
    i64.const 0
    i64.store offset=392
    local.get $l8
    i64.const 0
    i64.store offset=376
    local.get $l8
    i64.const 1065353216
    i64.store offset=368
    local.get $p0
    local.get $l8
    i32.const 368
    i32.add
    local.get $l8
    i32.const 344
    i32.add
    local.get $l8
    i32.const 272
    i32.add
    call $f70031
    local.set $l12
    local.get $p0
    i64.load offset=16 align=4
    local.set $l22
    local.get $l8
    local.get $p0
    i64.load offset=24 align=4
    i64.store offset=264
    local.get $l8
    local.get $l22
    i64.store offset=256
    local.get $p0
    f32.load offset=8
    local.set $l16
    local.get $p0
    f32.load offset=12
    local.set $l17
    local.get $p0
    f32.load offset=4
    local.set $l18
    local.get $l8
    i32.const 0
    i32.store offset=252
    local.get $l8
    local.get $l17
    f32.store offset=248
    local.get $l8
    local.get $l16
    f32.store offset=244
    local.get $l8
    local.get $l18
    f32.store offset=240
    local.get $l8
    local.get $p4
    f32.load offset=8
    f32.const 0x1.99999ap-5 (;=0.05;)
    f32.mul
    local.tee $l21
    local.get $l18
    local.get $l9
    i32.const 52
    i32.add
    local.tee $p0
    f32.load
    f32.mul
    local.tee $l19
    local.get $l16
    local.get $l9
    i32.const 56
    i32.add
    local.tee $l10
    f32.load
    f32.mul
    local.tee $l20
    local.get $l19
    local.get $l20
    f32.le
    select
    local.tee $l19
    local.get $l17
    local.get $l9
    i32.const 60
    i32.add
    local.tee $l13
    f32.load
    f32.mul
    local.tee $l20
    local.get $l19
    local.get $l20
    f32.le
    select
    f32.const 0x1p-2 (;=0.25;)
    f32.mul
    local.tee $l19
    local.get $l19
    local.get $l21
    f32.gt
    select
    f32.store offset=224
    local.get $l8
    i32.const 0
    i32.store8 offset=96
    local.get $l8
    i32.const 88
    i32.add
    local.tee $l14
    i64.const 0
    i64.store
    local.get $l8
    i32.const 80
    i32.add
    local.tee $l15
    i64.const 0
    i64.store
    local.get $l8
    i64.const 0
    i64.store offset=72
    local.get $l8
    i64.const 0
    i64.store offset=64
    local.get $l8
    local.get $l9
    i32.store offset=208
    local.get $l8
    local.get $l9
    i32.load offset=40
    local.get $l9
    i32.load8_u offset=39
    i32.const 20
    i32.mul
    i32.add
    i32.store offset=216
    local.get $l8
    local.get $l9
    i32.load8_u offset=38
    i32.store8 offset=220
    local.get $l14
    local.get $l18
    local.get $p0
    f32.load
    f32.mul
    local.tee $l18
    local.get $l16
    local.get $l10
    f32.load
    f32.mul
    local.tee $l16
    local.get $l16
    local.get $l18
    f32.ge
    select
    local.tee $l16
    local.get $l17
    local.get $l13
    f32.load
    f32.mul
    local.tee $l17
    local.get $l16
    local.get $l17
    f32.le
    select
    local.tee $l16
    f32.const 0x1.99999ap-6 (;=0.025;)
    f32.mul
    f32.store
    local.get $l15
    local.get $l16
    f32.const 0x1.99999ap-4 (;=0.1;)
    f32.mul
    f32.store
    local.get $l8
    local.get $l16
    f32.const 0x1.99999ap-5 (;=0.05;)
    f32.mul
    f32.store offset=84
    local.get $l8
    i32.const 240
    i32.add
    local.get $l8
    i32.const 256
    i32.add
    local.get $l8
    i32.const 112
    i32.add
    local.tee $p0
    local.get $l8
    i32.const 160
    i32.add
    local.tee $l10
    local.get $l8
    i32.const -64
    i32.sub
    local.get $l12
    call $f70494
    local.get $l8
    local.get $l9
    i32.load offset=44
    i32.store offset=212
    block $B2 (result i32)
      local.get $l12
      if $I3
        local.get $l8
        i32.const 1
        i32.store8 offset=44
        local.get $l8
        local.get $l10
        i32.store offset=40
        local.get $l8
        local.get $p0
        i32.store offset=36
        local.get $l8
        i32.const 3125832
        i32.store
        local.get $l8
        local.get $l8
        i32.const 528
        i32.add
        i32.store offset=32
        local.get $l8
        local.get $l8
        i32.const -64
        i32.sub
        i32.store offset=48
        local.get $l8
        i32.const 272
        i32.add
        local.get $l8
        local.get $l8
        i32.const 224
        i32.add
        local.get $l8
        i32.const 344
        i32.add
        local.get $p1
        local.get $p2
        local.get $p3
        local.get $p4
        f32.load
        local.get $p6
        local.get $l8
        i32.const 368
        i32.add
        local.get $l8
        i32.const 448
        i32.add
        i32.const 1
        local.get $p5
        local.get $l11
        local.get $p7
        call $f70030
        br $B2
      end
      local.get $l8
      i32.const 0
      i32.store8 offset=44
      local.get $l8
      local.get $l10
      i32.store offset=40
      local.get $l8
      local.get $p0
      i32.store offset=36
      local.get $l8
      i32.const 3125860
      i32.store
      local.get $l8
      local.get $l8
      i32.const 528
      i32.add
      i32.store offset=32
      local.get $l8
      local.get $l8
      i32.const -64
      i32.sub
      i32.store offset=48
      local.get $l8
      i32.const 272
      i32.add
      local.get $l8
      local.get $l8
      i32.const 224
      i32.add
      local.get $l8
      i32.const 344
      i32.add
      local.get $p1
      local.get $p2
      local.get $p3
      local.get $p4
      f32.load
      local.get $p6
      local.get $l8
      i32.const 368
      i32.add
      local.get $l8
      i32.const 448
      i32.add
      i32.const 0
      local.get $p5
      local.get $l11
      local.get $p7
      call $f70030
    end
    local.set $l9
    local.get $l8
    i32.const 560
    i32.add
    global.set $g0
    local.get $l9)