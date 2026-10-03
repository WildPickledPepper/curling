  (func $f78671 (type $t7) (param $p0 i32)
    (local $l1 i32) (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32)
    i32.const 504
    i32.const 8
    i32.const 16
    i32.const 0
    i32.const 403047
    i32.const 483
    call $f83341
    local.set $p0
    global.get $g0
    i32.const 256
    i32.sub
    local.tee $l1
    global.set $g0
    local.get $p0
    i64.const 0
    i64.store offset=8
    local.get $p0
    i32.const 16
    i32.store
    local.get $p0
    i32.const 16
    i32.add
    call $f65728
    local.set $l2
    local.get $l1
    i64.const 4294967296
    i64.store offset=228 align=4
    local.get $l1
    i32.const 16
    i32.store offset=224
    local.get $l1
    i32.const 0
    i32.store offset=220
    local.get $l1
    i32.const 0
    i32.store offset=212
    local.get $l1
    i64.const 0
    i64.store offset=204 align=4
    local.get $l1
    i64.const 4294967296
    i64.store offset=196 align=4
    local.get $l1
    i32.const 16
    i32.store offset=192
    local.get $l1
    i32.const 0
    i32.store offset=188
    local.get $l1
    i32.const 16
    i32.store offset=180
    local.get $l1
    i32.const 0
    i32.store offset=172
    local.get $l1
    i64.const 0
    i64.store offset=164 align=4
    local.get $l1
    i32.const 16
    i32.store offset=156
    local.get $l1
    i32.const 0
    i32.store offset=148
    local.get $l1
    i64.const 0
    i64.store offset=140 align=4
    local.get $l1
    i32.const 16
    i32.store offset=216
    local.get $l1
    i32.const 16
    i32.store offset=184
    local.get $l1
    i32.const 403680
    i32.store offset=160
    local.get $l1
    i32.const 403680
    i32.store offset=136
    local.get $l1
    i64.const 0
    i64.store offset=128
    local.get $l1
    i64.const 0
    i64.store offset=244 align=4
    local.get $l1
    i64.const 0
    i64.store offset=236 align=4
    local.get $l1
    i64.const 4294967296
    i64.store offset=100 align=4
    local.get $l1
    i32.const 16
    i32.store offset=96
    local.get $l1
    i32.const 92
    i32.add
    local.tee $l3
    i32.const 0
    i32.store
    local.get $l1
    i32.const 0
    i32.store offset=84
    local.get $l1
    i64.const 0
    i64.store offset=76 align=4
    local.get $l1
    i64.const 4294967296
    i64.store offset=68 align=4
    local.get $l1
    i32.const -64
    i32.sub
    i32.const 16
    i32.store
    local.get $l1
    i32.const 60
    i32.add
    local.tee $l4
    i32.const 0
    i32.store
    local.get $l1
    i32.const 16
    i32.store offset=52
    local.get $l1
    i32.const 0
    i32.store offset=44
    local.get $l1
    i64.const 0
    i64.store offset=36 align=4
    local.get $l1
    i32.const 16
    i32.store offset=28
    local.get $l1
    i32.const 0
    i32.store offset=20
    local.get $l1
    i64.const 0
    i64.store offset=12 align=4
    local.get $l1
    i32.const 16
    i32.store offset=88
    local.get $l1
    i32.const 16
    i32.store offset=56
    local.get $l1
    i32.const 403680
    i32.store offset=32
    local.get $l1
    i32.const 403680
    i32.store offset=8
    local.get $l1
    i64.const 0
    i64.store
    local.get $l1
    i64.const 0
    i64.store offset=116 align=4
    local.get $l1
    i64.const 0
    i64.store offset=108 align=4
    local.get $p0
    i32.const 88
    i32.add
    local.tee $l5
    i32.const 0
    i32.store
    local.get $p0
    local.get $l2
    i32.store offset=84
    local.get $l2
    i32.const 124
    local.get $l5
    local.get $p0
    i32.const 92
    i32.add
    local.get $l1
    i32.const 128
    i32.add
    call $f78674
    local.get $p0
    i32.const 216
    i32.add
    local.get $l1
    call $f78674
    call $f65733
    local.get $l3
    call $f554
    drop
    local.get $l4
    call $f554
    drop
    local.get $l1
    i32.load offset=32
    local.tee $l2
    i32.const 403680
    i32.ne
    if $I0
      local.get $l2
      local.get $l1
      i32.load offset=52
      i32.const 403047
      i32.const 1027
      call $f83342
    end
    local.get $l1
    i32.load offset=8
    local.tee $l2
    i32.const 403680
    i32.ne
    if $I1
      local.get $l2
      local.get $l1
      i32.load offset=28
      i32.const 403047
      i32.const 1027
      call $f83342
    end
    local.get $l1
    i32.const 220
    i32.add
    call $f554
    drop
    local.get $l1
    i32.const 188
    i32.add
    call $f554
    drop
    local.get $l1
    i32.load offset=160
    local.tee $l2
    i32.const 403680
    i32.ne
    if $I2
      local.get $l2
      local.get $l1
      i32.load offset=180
      i32.const 403047
      i32.const 1027
      call $f83342
    end
    local.get $l1
    i32.load offset=136
    local.tee $l2
    i32.const 403680
    i32.ne
    if $I3
      local.get $l2
      local.get $l1
      i32.load offset=156
      i32.const 403047
      i32.const 1027
      call $f83342
    end
    local.get $p0
    i32.const 340
    i32.add
    call $f65728
    local.set $l2
    local.get $l1
    i32.const 64
    i32.store offset=144
    local.get $l1
    i64.const 4294967296
    i64.store offset=136
    local.get $l1
    i64.const 322122547200
    i64.store offset=128
    local.get $l1
    i32.const 64
    i32.store offset=16
    local.get $l1
    i64.const 4294967296
    i64.store offset=8
    local.get $l1
    i64.const 322122547200
    i64.store
    local.get $p0
    i64.const 64
    i64.store offset=432
    local.get $p0
    i64.const 75
    i64.store offset=440
    local.get $p0
    i64.const 274877906945
    i64.store offset=448
    local.get $p0
    i32.const 1
    i32.store offset=428
    local.get $p0
    i32.const 412
    i32.add
    local.tee $l3
    i64.const 0
    i64.store align=4
    local.get $p0
    i64.const 75
    i64.store offset=420 align=4
    local.get $p0
    local.get $l2
    i32.store offset=408
    local.get $l2
    i32.const 20
    local.get $l3
    local.get $p0
    i32.const 416
    i32.add
    local.get $p0
    i32.const 436
    i32.add
    call $f65733
    local.get $l1
    call $f554
    drop
    local.get $l1
    i32.const 128
    i32.add
    call $f554
    drop
    local.get $p0
    i64.const 4294967296
    i64.store offset=492 align=4
    local.get $p0
    i32.const 16
    i32.store offset=488
    local.get $p0
    i32.const 0
    i32.store offset=484
    local.get $p0
    i32.const 16
    i32.store offset=476
    local.get $p0
    i32.const 0
    i32.store offset=468
    local.get $p0
    i64.const 0
    i64.store offset=460 align=4
    local.get $p0
    i32.const 403680
    i32.store offset=456
    local.get $l1
    i32.const 256
    i32.add
    global.set $g0
    i32.const 4758716
    local.get $p0
    i32.store)
