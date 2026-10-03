  (func $f69806 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i64) (local $l7 f32) (local $l8 f32)
    global.get $g0
    i32.const 480
    i32.sub
    local.tee $l2
    global.set $g0
    block $B0 (result i32)
      local.get $p1
      i32.load8_u offset=24
      if $I1
        local.get $p0
        i32.const 0
        i32.store offset=32
        local.get $p0
        i32.const 2
        i32.store
        local.get $p1
        i64.load align=4
        local.set $l6
        local.get $l2
        local.get $p1
        f32.load offset=8
        f32.store offset=472
        local.get $l2
        local.get $l6
        i64.store offset=464
        local.get $p0
        local.get $l2
        i32.const 464
        i32.add
        call $f69801
        local.set $l4
        local.get $p1
        f32.load offset=12
        local.set $l7
        local.get $p1
        f32.load offset=4
        local.set $l8
        local.get $l2
        local.get $p1
        f32.load offset=8
        f32.store offset=456
        local.get $l2
        local.get $l8
        f32.store offset=452
        local.get $l2
        local.get $l7
        f32.store offset=448
        local.get $l4
        local.get $l2
        i32.const 448
        i32.add
        call $f69801
        local.set $l4
        local.get $p1
        i64.load offset=12 align=4
        local.set $l6
        local.get $l2
        local.get $p1
        f32.load offset=8
        f32.store offset=440
        local.get $l2
        local.get $l6
        i64.store offset=432
        local.get $l4
        local.get $l2
        i32.const 432
        i32.add
        call $f69801
        local.set $l4
        local.get $p1
        i32.const 16
        i32.add
        local.tee $l5
        f32.load
        local.set $l7
        local.get $p1
        f32.load
        local.set $l8
        local.get $l2
        local.get $p1
        f32.load offset=8
        f32.store offset=424
        local.get $l2
        local.get $l7
        f32.store offset=420
        local.get $l2
        local.get $l8
        f32.store offset=416
        local.get $l4
        local.get $l2
        i32.const 416
        i32.add
        call $f69801
        local.set $l4
        local.get $p1
        i64.load align=4
        local.set $l6
        local.get $l2
        local.get $p1
        f32.load offset=8
        f32.store offset=408
        local.get $l2
        local.get $l6
        i64.store offset=400
        local.get $l4
        local.get $l2
        i32.const 400
        i32.add
        call $f69801
        local.set $l3
        local.get $p1
        i64.load align=4
        local.set $l6
        local.get $l2
        local.get $p1
        i32.const 20
        i32.add
        local.tee $l4
        f32.load
        f32.store offset=392
        local.get $l2
        local.get $l6
        i64.store offset=384
        local.get $l3
        local.get $l2
        i32.const 384
        i32.add
        call $f69801
        local.set $l3
        local.get $p1
        f32.load offset=12
        local.set $l7
        local.get $p1
        f32.load offset=4
        local.set $l8
        local.get $l2
        local.get $l4
        f32.load
        f32.store offset=376
        local.get $l2
        local.get $l8
        f32.store offset=372
        local.get $l2
        local.get $l7
        f32.store offset=368
        local.get $l3
        local.get $l2
        i32.const 368
        i32.add
        call $f69801
        local.set $l3
        local.get $p1
        i64.load offset=12 align=4
        local.set $l6
        local.get $l2
        local.get $l4
        f32.load
        f32.store offset=360
        local.get $l2
        local.get $l6
        i64.store offset=352
        local.get $l3
        local.get $l2
        i32.const 352
        i32.add
        call $f69801
        local.set $l3
        local.get $l5
        f32.load
        local.set $l7
        local.get $p1
        f32.load
        local.set $l8
        local.get $l2
        local.get $l4
        f32.load
        f32.store offset=344
        local.get $l2
        local.get $l7
        f32.store offset=340
        local.get $l2
        local.get $l8
        f32.store offset=336
        local.get $l3
        local.get $l2
        i32.const 336
        i32.add
        call $f69801
        local.set $l3
        local.get $p1
        i64.load align=4
        local.set $l6
        local.get $l2
        local.get $l4
        f32.load
        f32.store offset=328
        local.get $l2
        local.get $l6
        i64.store offset=320
        local.get $l3
        local.get $l2
        i32.const 320
        i32.add
        call $f69801
        local.set $l3
        local.get $p0
        i32.const 0
        i32.store offset=32
        local.get $p0
        i32.const 1
        i32.store
        local.get $p1
        f32.load offset=12
        local.set $l7
        local.get $p1
        f32.load offset=4
        local.set $l8
        local.get $l2
        local.get $p1
        f32.load offset=8
        f32.store offset=312
        local.get $l2
        local.get $l8
        f32.store offset=308
        local.get $l2
        local.get $l7
        f32.store offset=304
        local.get $l3
        local.get $l2
        i32.const 304
        i32.add
        call $f69801
        local.set $l3
        local.get $p1
        f32.load offset=12
        local.set $l7
        local.get $p1
        f32.load offset=4
        local.set $l8
        local.get $l2
        local.get $l4
        f32.load
        f32.store offset=296
        local.get $l2
        local.get $l8
        f32.store offset=292
        local.get $l2
        local.get $l7
        f32.store offset=288
        local.get $l3
        local.get $l2
        i32.const 288
        i32.add
        call $f69801
        local.set $l3
        local.get $p1
        i64.load offset=12 align=4
        local.set $l6
        local.get $l2
        local.get $p1
        f32.load offset=8
        f32.store offset=280
        local.get $l2
        local.get $l6
        i64.store offset=272
        local.get $l3
        local.get $l2
        i32.const 272
        i32.add
        call $f69801
        local.set $l3
        local.get $p1
        i64.load offset=12 align=4
        local.set $l6
        local.get $l2
        local.get $l4
        f32.load
        f32.store offset=264
        local.get $l2
        local.get $l6
        i64.store offset=256
        local.get $l3
        local.get $l2
        i32.const 256
        i32.add
        call $f69801
        local.set $l3
        local.get $l5
        f32.load
        local.set $l7
        local.get $p1
        f32.load
        local.set $l8
        local.get $l2
        local.get $p1
        f32.load offset=8
        f32.store offset=248
        local.get $l2
        local.get $l7
        f32.store offset=244
        local.get $l2
        local.get $l8
        f32.store offset=240
        local.get $l3
        local.get $l2
        i32.const 240
        i32.add
        call $f69801
        drop
        local.get $l4
        f32.load
        local.set $l7
        local.get $l5
        f32.load
        local.set $l8
        local.get $l2
        local.get $p1
        f32.load
        f32.store offset=224
        local.get $l2
        i32.const 224
        i32.add
        br $B0
      end
      local.get $p0
      i32.const 0
      i32.store offset=32
      local.get $p0
      i32.const 4
      i32.store
      local.get $p1
      i64.load align=4
      local.set $l6
      local.get $l2
      local.get $p1
      f32.load offset=8
      f32.store offset=216
      local.get $l2
      local.get $l6
      i64.store offset=208
      local.get $p0
      local.get $l2
      i32.const 208
      i32.add
      call $f69801
      local.set $l4
      local.get $p1
      i32.const 16
      i32.add
      local.tee $l5
      f32.load
      local.set $l7
      local.get $p1
      f32.load
      local.set $l8
      local.get $l2
      local.get $p1
      f32.load offset=8
      f32.store offset=200
      local.get $l2
      local.get $l7
      f32.store offset=196
      local.get $l2
      local.get $l8
      f32.store offset=192
      local.get $l4
      local.get $l2
      i32.const 192
      i32.add
      call $f69801
      local.set $l4
      local.get $p1
      f32.load offset=12
      local.set $l7
      local.get $p1
      f32.load offset=4
      local.set $l8
      local.get $l2
      local.get $p1
      f32.load offset=8
      f32.store offset=184
      local.get $l2
      local.get $l8
      f32.store offset=180
      local.get $l2
      local.get $l7
      f32.store offset=176
      local.get $l4
      local.get $l2
      i32.const 176
      i32.add
      call $f69801
      local.set $l4
      local.get $p1
      i64.load offset=12 align=4
      local.set $l6
      local.get $l2
      local.get $p1
      f32.load offset=8
      f32.store offset=168
      local.get $l2
      local.get $l6
      i64.store offset=160
      local.get $l4
      local.get $l2
      i32.const 160
      i32.add
      call $f69801
      local.set $l3
      local.get $p1
      i64.load offset=12 align=4
      local.set $l6
      local.get $l2
      local.get $p1
      i32.const 20
      i32.add
      local.tee $l4
      f32.load
      f32.store offset=152
      local.get $l2
      local.get $l6
      i64.store offset=144
      local.get $l3
      local.get $l2
      i32.const 144
      i32.add
      call $f69801
      local.set $l3
      local.get $l5
      f32.load
      local.set $l7
      local.get $p1
      f32.load
      local.set $l8
      local.get $l2
      local.get $p1
      f32.load offset=8
      f32.store offset=136
      local.get $l2
      local.get $l7
      f32.store offset=132
      local.get $l2
      local.get $l8
      f32.store offset=128
      local.get $l3
      local.get $l2
      i32.const 128
      i32.add
      call $f69801
      local.set $l3
      local.get $l5
      f32.load
      local.set $l7
      local.get $p1
      f32.load
      local.set $l8
      local.get $l2
      local.get $l4
      f32.load
      f32.store offset=120
      local.get $l2
      local.get $l7
      f32.store offset=116
      local.get $l2
      local.get $l8
      f32.store offset=112
      local.get $l3
      local.get $l2
      i32.const 112
      i32.add
      call $f69801
      local.set $l3
      local.get $p1
      i64.load align=4
      local.set $l6
      local.get $l2
      local.get $p1
      f32.load offset=8
      f32.store offset=104
      local.get $l2
      local.get $l6
      i64.store offset=96
      local.get $l3
      local.get $l2
      i32.const 96
      i32.add
      call $f69801
      local.set $l3
      local.get $p1
      i64.load align=4
      local.set $l6
      local.get $l2
      local.get $l4
      f32.load
      f32.store offset=88
      local.get $l2
      local.get $l6
      i64.store offset=80
      local.get $l3
      local.get $l2
      i32.const 80
      i32.add
      call $f69801
      local.set $l3
      local.get $p1
      f32.load offset=12
      local.set $l7
      local.get $p1
      f32.load offset=4
      local.set $l8
      local.get $l2
      local.get $p1
      f32.load offset=8
      f32.store offset=72
      local.get $l2
      local.get $l8
      f32.store offset=68
      local.get $l2
      local.get $l7
      f32.store offset=64
      local.get $l3
      local.get $l2
      i32.const -64
      i32.sub
      call $f69801
      local.set $l3
      local.get $p1
      f32.load offset=12
      local.set $l7
      local.get $p1
      f32.load offset=4
      local.set $l8
      local.get $l2
      local.get $l4
      f32.load
      f32.store offset=56
      local.get $l2
      local.get $l8
      f32.store offset=52
      local.get $l2
      local.get $l7
      f32.store offset=48
      local.get $l3
      local.get $l2
      i32.const 48
      i32.add
      call $f69801
      local.set $l3
      local.get $p1
      i64.load offset=12 align=4
      local.set $l6
      local.get $l2
      local.get $l4
      f32.load
      f32.store offset=40
      local.get $l2
      local.get $l6
      i64.store offset=32
      local.get $l3
      local.get $l2
      i32.const 32
      i32.add
      call $f69801
      local.set $l3
      local.get $p1
      i64.load align=4
      local.set $l6
      local.get $l2
      local.get $l4
      f32.load
      f32.store offset=24
      local.get $l2
      local.get $l6
      i64.store offset=16
      local.get $l3
      local.get $l2
      i32.const 16
      i32.add
      call $f69801
      drop
      local.get $l4
      f32.load
      local.set $l7
      local.get $l5
      f32.load
      local.set $l8
      local.get $l2
      local.get $p1
      f32.load
      f32.store
      local.get $l2
    end
    local.tee $p1
    local.get $l7
    f32.store offset=8
    local.get $p1
    local.get $l8
    f32.store offset=4
    local.get $p0
    local.get $p1
    call $f69801
    drop
    local.get $l2
    i32.const 480
    i32.add
    global.set $g0)
