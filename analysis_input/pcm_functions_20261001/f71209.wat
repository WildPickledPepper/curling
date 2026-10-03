  (func $f71209 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32) (local $l33 f32) (local $l34 f32) (local $l35 f32) (local $l36 f32) (local $l37 f32) (local $l38 f32) (local $l39 f32) (local $l40 f32) (local $l41 f32) (local $l42 f32) (local $l43 f32) (local $l44 f32) (local $l45 f32) (local $l46 f32) (local $l47 f32) (local $l48 f32)
    global.get $g0
    i32.const 48
    i32.sub
    local.tee $l5
    global.set $g0
    local.get $p0
    i32.const 0
    i32.store offset=660
    local.get $p0
    i32.load offset=408
    i32.const 0
    local.get $p0
    i32.load offset=412
    i32.const 2
    i32.shl
    call $f484
    drop
    local.get $p0
    i32.load offset=312
    i32.const 0
    local.get $p0
    i32.const 448
    i32.add
    local.tee $l7
    i32.load
    i32.const 5
    i32.shl
    local.tee $l11
    call $f484
    drop
    local.get $p0
    i32.load offset=168
    i32.const 0
    local.get $p0
    i32.load offset=468
    i32.const 2
    i32.shl
    call $f484
    drop
    local.get $p0
    i32.const 0
    i32.store8 offset=489
    local.get $p0
    local.get $p0
    i32.const 112
    i32.add
    local.tee $l2
    i32.const 0
    call $f71016
    local.get $l5
    i32.const 36
    i32.add
    local.tee $l3
    i64.const 0
    i64.store align=4
    local.get $l5
    i32.const 28
    i32.add
    local.tee $l4
    i64.const 0
    i64.store align=4
    local.get $l5
    i64.const 0
    i64.store offset=20 align=4
    local.get $l5
    local.get $p0
    i32.load offset=228
    i32.store
    local.get $l5
    local.get $p0
    i32.load offset=240
    i32.store offset=4
    local.get $l5
    local.get $p0
    i32.load offset=252
    i32.store offset=8
    local.get $l5
    local.get $p0
    i32.load offset=264
    i32.store offset=12
    local.get $l4
    local.get $p0
    i32.load offset=144
    i32.store
    local.get $l5
    local.get $p0
    i32.load offset=156
    i32.store offset=24
    local.get $l3
    local.get $p0
    i32.load offset=180
    i32.store
    local.get $l5
    local.get $p0
    i32.load offset=192
    i32.store offset=32
    local.get $l5
    local.get $p0
    i32.load offset=480
    i32.store offset=16
    local.get $l2
    call $f71020
    local.get $l2
    local.get $l5
    call $f71022
    i32.const 0
    local.set $l4
    local.get $l2
    call $f71017
    local.get $l2
    local.get $p1
    local.get $l5
    call $f71018
    local.get $l2
    i32.load offset=336
    i32.const 2
    i32.ge_u
    if $I0
      local.get $p0
      i32.load offset=276
      local.get $p0
      i32.load offset=264
      local.get $p0
      i32.load offset=448
      i32.const 5
      i32.shl
      call $f483
      drop
    end
    local.get $p0
    local.get $l2
    call $f71203
    global.get $g0
    i32.const 176
    i32.sub
    local.tee $p1
    global.set $g0
    local.get $l2
    i32.load offset=224
    local.set $l9
    local.get $l2
    i32.load offset=336
    local.set $l12
    local.get $l2
    i32.load offset=332
    local.set $l13
    block $B1
      local.get $l2
      i32.load offset=364
      i32.load8_u
      i32.const 1
      i32.and
      i32.eqz
      if $I2
        local.get $p1
        i32.const 160
        i32.add
        local.set $l6
        loop $L3
          local.get $p1
          i32.const 168
          i32.add
          local.tee $l3
          i64.const 0
          i64.store
          local.get $l6
          i64.const 0
          i64.store
          local.get $p1
          i64.const 0
          i64.store offset=152
          local.get $p1
          i64.const 0
          i64.store offset=144
          local.get $l4
          i32.const 2
          i32.shl
          local.tee $l8
          local.get $p1
          i32.const 144
          i32.add
          i32.add
          local.get $l6
          local.get $l8
          i32.add
          i32.const 12
          i32.sub
          local.get $l4
          i32.const 3
          i32.lt_u
          select
          i32.const 1065353216
          i32.store
          local.get $l2
          f32.load offset=468
          local.set $l31
          local.get $l2
          f32.load offset=444
          local.set $l32
          local.get $l2
          f32.load offset=456
          local.set $l33
          local.get $l2
          f32.load offset=472
          local.set $l34
          local.get $l2
          f32.load offset=448
          local.set $l35
          local.get $l2
          f32.load offset=460
          local.set $l36
          local.get $l2
          f32.load offset=476
          local.set $l37
          local.get $l2
          f32.load offset=452
          local.set $l38
          local.get $l2
          f32.load offset=464
          local.set $l39
          local.get $l2
          f32.load offset=416
          local.set $l22
          local.get $l2
          f32.load offset=408
          local.set $l23
          local.get $l2
          f32.load offset=412
          local.set $l24
          local.get $l2
          f32.load offset=504
          local.set $l40
          local.get $l2
          f32.load offset=480
          local.set $l41
          local.get $l2
          f32.load offset=492
          local.set $l42
          local.get $l2
          f32.load offset=428
          local.set $l25
          local.get $l2
          f32.load offset=420
          local.set $l26
          local.get $l2
          f32.load offset=424
          local.set $l27
          local.get $l2
          f32.load offset=508
          local.set $l43
          local.get $l2
          f32.load offset=484
          local.set $l44
          local.get $l2
          f32.load offset=496
          local.set $l45
          local.get $l3
          f32.load
          local.set $l16
          local.get $l2
          f32.load offset=440
          local.set $l28
          local.get $l6
          f32.load
          local.set $l17
          local.get $l2
          f32.load offset=432
          local.set $l29
          local.get $l2
          f32.load offset=436
          local.set $l30
          local.get $l2
          f32.load offset=512
          local.set $l46
          local.get $l2
          f32.load offset=488
          local.set $l47
          local.get $l2
          f32.load offset=500
          local.set $l48
          local.get $p1
          f32.load offset=164
          local.set $l18
          local.get $p1
          f32.load offset=152
          local.set $l19
          local.get $p1
          f32.load offset=144
          local.set $l20
          local.get $p1
          f32.load offset=148
          local.set $l21
          local.get $l9
          local.get $l4
          i32.const 5
          i32.shl
          i32.add
          local.tee $l3
          i32.const 0
          i32.store offset=28
          local.get $l3
          i32.const 0
          i32.store offset=12
          local.get $l3
          local.get $l29
          local.get $l17
          f32.mul
          local.get $l30
          local.get $l18
          f32.mul
          f32.add
          local.get $l28
          local.get $l16
          f32.mul
          f32.add
          local.get $l20
          local.get $l47
          f32.mul
          local.get $l21
          local.get $l48
          f32.mul
          f32.add
          local.get $l19
          local.get $l46
          f32.mul
          f32.add
          f32.add
          f32.store offset=24
          local.get $l3
          local.get $l26
          local.get $l17
          f32.mul
          local.get $l27
          local.get $l18
          f32.mul
          f32.add
          local.get $l25
          local.get $l16
          f32.mul
          f32.add
          local.get $l20
          local.get $l44
          f32.mul
          local.get $l21
          local.get $l45
          f32.mul
          f32.add
          local.get $l19
          local.get $l43
          f32.mul
          f32.add
          f32.add
          f32.store offset=20
          local.get $l3
          local.get $l23
          local.get $l17
          f32.mul
          local.get $l24
          local.get $l18
          f32.mul
          f32.add
          local.get $l22
          local.get $l16
          f32.mul
          f32.add
          local.get $l20
          local.get $l41
          f32.mul
          local.get $l21
          local.get $l42
          f32.mul
          f32.add
          local.get $l19
          local.get $l40
          f32.mul
          f32.add
          f32.add
          f32.store offset=16
          local.get $l3
          local.get $l20
          local.get $l22
          f32.mul
          local.get $l21
          local.get $l25
          f32.mul
          f32.add
          local.get $l19
          local.get $l28
          f32.mul
          f32.add
          local.get $l17
          local.get $l38
          f32.mul
          local.get $l18
          local.get $l39
          f32.mul
          f32.add
          local.get $l16
          local.get $l37
          f32.mul
          f32.add
          f32.add
          f32.store offset=8
          local.get $l3
          local.get $l20
          local.get $l24
          f32.mul
          local.get $l21
          local.get $l27
          f32.mul
          f32.add
          local.get $l19
          local.get $l30
          f32.mul
          f32.add
          local.get $l17
          local.get $l35
          f32.mul
          local.get $l18
          local.get $l36
          f32.mul
          f32.add
          local.get $l16
          local.get $l34
          f32.mul
          f32.add
          f32.add
          f32.store offset=4
          local.get $l3
          local.get $l20
          local.get $l23
          f32.mul
          local.get $l21
          local.get $l26
          f32.mul
          f32.add
          local.get $l19
          local.get $l29
          f32.mul
          f32.add
          local.get $l17
          local.get $l32
          f32.mul
          local.get $l18
          local.get $l33
          f32.mul
          f32.add
          local.get $l16
          local.get $l31
          f32.mul
          f32.add
          f32.add
          f32.store
          local.get $l4
          i32.const 1
          i32.add
          local.tee $l4
          i32.const 6
          i32.ne
          br_if $L3
        end
        br $B1
      end
      local.get $l9
      i32.const 0
      i32.const 192
      call $f484
      drop
    end
    i32.const 1
    local.set $l4
    local.get $l12
    i32.const 1
    i32.gt_u
    if $I4
      local.get $p1
      i32.const 160
      i32.add
      local.set $l8
      loop $L5
        local.get $p1
        local.get $l2
        local.get $l4
        call $f70976
        local.tee $l3
        f32.load offset=120
        f32.store offset=128
        local.get $p1
        local.get $l3
        f32.load offset=124
        f32.store offset=132
        local.get $p1
        local.get $l3
        f32.load offset=128
        f32.store offset=136
        local.get $l13
        local.get $l4
        i32.const 80
        i32.mul
        i32.add
        i32.const 72
        i32.add
        local.set $l14
        i32.const 0
        local.set $l6
        loop $L6
          local.get $p1
          i32.const 168
          i32.add
          local.tee $l3
          i64.const 0
          i64.store
          local.get $l8
          i64.const 0
          i64.store
          local.get $p1
          i64.const 0
          i64.store offset=152
          local.get $p1
          i64.const 0
          i64.store offset=144
          local.get $l6
          i32.const 2
          i32.shl
          local.tee $l15
          local.get $p1
          i32.const 144
          i32.add
          i32.add
          local.get $l8
          local.get $l15
          i32.add
          i32.const 12
          i32.sub
          local.get $l6
          i32.const 3
          i32.lt_u
          select
          i32.const 1065353216
          i32.store
          local.get $p1
          i32.const 0
          i32.store offset=124
          local.get $p1
          i32.const 0
          i32.store offset=108
          local.get $p1
          local.get $l3
          f32.load
          f32.neg
          f32.store offset=120
          local.get $p1
          local.get $p1
          f32.load offset=164
          f32.neg
          f32.store offset=116
          local.get $p1
          local.get $l8
          f32.load
          f32.neg
          f32.store offset=112
          local.get $p1
          local.get $p1
          f32.load offset=152
          f32.neg
          f32.store offset=104
          local.get $p1
          local.get $p1
          f32.load offset=148
          f32.neg
          f32.store offset=100
          local.get $p1
          local.get $p1
          f32.load offset=144
          f32.neg
          f32.store offset=96
          local.get $p1
          i32.const -64
          i32.sub
          local.get $l2
          i32.load offset=284
          local.get $l4
          i32.const 96
          i32.mul
          i32.add
          local.get $p1
          i32.const 128
          i32.add
          local.get $l4
          i32.const 76
          i32.mul
          local.tee $l3
          local.get $l2
          i32.load offset=272
          i32.add
          local.get $p1
          i32.const 96
          i32.add
          call $f71003
          local.get $p1
          local.get $l9
          local.get $l14
          i32.load
          i32.const 192
          i32.mul
          i32.add
          local.get $p1
          i32.const -64
          i32.sub
          call $f71205
          local.get $p1
          i32.const 0
          i32.store offset=60
          local.get $p1
          i32.const 0
          i32.store offset=44
          local.get $p1
          local.get $p1
          f32.load offset=24
          f32.neg
          f32.store offset=56
          local.get $p1
          local.get $p1
          f32.load offset=20
          f32.neg
          f32.store offset=52
          local.get $p1
          local.get $p1
          f32.load offset=16
          f32.neg
          f32.store offset=48
          local.get $p1
          local.get $p1
          f32.load offset=8
          f32.neg
          f32.store offset=40
          local.get $p1
          local.get $p1
          f32.load offset=4
          f32.neg
          f32.store offset=36
          local.get $p1
          local.get $p1
          f32.load
          f32.neg
          f32.store offset=32
          local.get $p1
          local.get $p1
          i32.const 128
          i32.add
          local.get $l2
          i32.load offset=236
          local.get $l4
          i32.const 112
          i32.mul
          i32.add
          local.get $l2
          i32.load offset=248
          local.get $l4
          i32.const 36
          i32.mul
          i32.add
          local.get $l2
          i32.load offset=272
          local.get $l3
          i32.add
          local.get $p1
          i32.const 96
          i32.add
          local.get $p1
          i32.const 32
          i32.add
          call $f70999
          local.get $l9
          local.get $l4
          i32.const 192
          i32.mul
          i32.add
          local.get $l6
          i32.const 5
          i32.shl
          i32.add
          local.tee $l3
          local.get $p1
          f32.load
          f32.store
          local.get $l3
          local.get $p1
          f32.load offset=4
          f32.store offset=4
          local.get $p1
          f32.load offset=8
          local.set $l16
          local.get $l3
          i32.const 0
          i32.store offset=12
          local.get $l3
          local.get $l16
          f32.store offset=8
          local.get $l3
          local.get $p1
          f32.load offset=16
          f32.store offset=16
          local.get $l3
          local.get $p1
          f32.load offset=20
          f32.store offset=20
          local.get $p1
          f32.load offset=24
          local.set $l16
          local.get $l3
          i32.const 0
          i32.store offset=28
          local.get $l3
          local.get $l16
          f32.store offset=24
          local.get $l6
          i32.const 1
          i32.add
          local.tee $l6
          i32.const 6
          i32.ne
          br_if $L6
        end
        local.get $l4
        i32.const 1
        i32.add
        local.tee $l4
        local.get $l12
        i32.ne
        br_if $L5
      end
    end
    local.get $p1
    i32.const 176
    i32.add
    global.set $g0
    local.get $l5
    local.set $p1
    i32.const 0
    local.set $l4
    local.get $l2
    i32.load offset=336
    if $I7
      f32.const 0x1p+0 (;=1;)
      local.get $l2
      f32.load offset=352
      local.tee $l30
      f32.div
      local.set $l34
      local.get $p1
      i32.load offset=12
      local.set $l6
      local.get $p1
      i32.load
      local.set $l9
      loop $L8
        f32.const 0x0p+0 (;=0;)
        f32.const 0x1p+0 (;=1;)
        local.get $l2
        i32.load offset=332
        local.get $l4
        i32.const 80
        i32.mul
        i32.add
        i32.load offset=64
        local.tee $p1
        f32.load offset=124
        local.tee $l16
        f32.div
        local.get $l16
        f32.const 0x0p+0 (;=0;)
        f32.eq
        select
        local.set $l35
        f32.const 0x1p+0 (;=1;)
        local.get $p1
        f32.load offset=112
        f32.div
        local.set $l36
        f32.const 0x1p+0 (;=1;)
        local.get $p1
        f32.load offset=120
        f32.div
        local.set $l31
        f32.const 0x1p+0 (;=1;)
        local.get $p1
        f32.load offset=116
        f32.div
        local.set $l32
        local.get $l9
        local.get $l4
        i32.const 5
        i32.shl
        local.tee $l8
        i32.add
        local.tee $l3
        f32.load offset=16
        local.set $l38
        local.get $l3
        f32.load offset=8
        local.set $l16
        local.get $l3
        f32.load offset=4
        local.set $l20
        local.get $l3
        f32.load
        local.set $l21
        local.get $p1
        f32.load offset=108
        local.set $l25
        local.get $l3
        f32.load offset=24
        local.set $l39
        local.get $l3
        f32.load offset=20
        local.set $l40
        block $B9 (result f32)
          local.get $p1
          f32.load offset=104
          local.tee $l37
          f32.const 0x0p+0 (;=0;)
          f32.gt
          i32.eqz
          if $I10
            f32.const 0x0p+0 (;=0;)
            local.set $l22
            f32.const 0x0p+0 (;=0;)
            local.set $l24
            f32.const 0x0p+0 (;=0;)
            local.set $l23
            f32.const 0x0p+0 (;=0;)
            local.set $l29
            f32.const 0x0p+0 (;=0;)
            local.set $l26
            f32.const 0x0p+0 (;=0;)
            local.get $l25
            f32.const 0x0p+0 (;=0;)
            f32.gt
            i32.eqz
            br_if $B9
            drop
          end
          local.get $p1
          f32.load offset=12
          local.tee $l17
          local.get $l17
          f32.mul
          f32.const -0x1p-1 (;=-0.5;)
          f32.add
          local.tee $l33
          local.get $l31
          local.get $l30
          local.get $l25
          f32.mul
          local.tee $l22
          f32.const 0x1p+0 (;=1;)
          local.get $l22
          f32.const 0x1p+0 (;=1;)
          f32.lt
          select
          local.tee $l25
          local.get $l33
          local.get $l16
          local.get $l16
          f32.add
          local.tee $l29
          f32.mul
          local.get $l17
          local.get $l20
          local.get $l20
          f32.add
          local.tee $l26
          local.get $p1
          f32.load
          local.tee $l22
          f32.mul
          local.get $l21
          local.get $l21
          f32.add
          local.tee $l19
          local.get $p1
          f32.load offset=4
          local.tee $l24
          f32.mul
          f32.sub
          f32.mul
          f32.sub
          local.get $p1
          f32.load offset=8
          local.tee $l23
          local.get $l19
          local.get $l22
          f32.mul
          local.get $l26
          local.get $l24
          f32.mul
          f32.add
          local.get $l29
          local.get $l23
          f32.mul
          f32.add
          local.tee $l27
          f32.mul
          f32.add
          f32.mul
          f32.mul
          local.tee $l28
          local.get $l28
          f32.add
          local.tee $l28
          f32.mul
          local.get $l17
          local.get $l22
          local.get $l32
          local.get $l25
          local.get $l24
          local.get $l27
          f32.mul
          local.get $l26
          local.get $l33
          f32.mul
          local.get $l17
          local.get $l19
          local.get $l23
          f32.mul
          local.get $l29
          local.get $l22
          f32.mul
          f32.sub
          f32.mul
          f32.sub
          f32.add
          f32.mul
          f32.mul
          local.tee $l18
          local.get $l18
          f32.add
          local.tee $l18
          f32.mul
          local.get $l24
          local.get $l36
          local.get $l25
          local.get $l22
          local.get $l27
          f32.mul
          local.get $l19
          local.get $l33
          f32.mul
          local.get $l17
          local.get $l29
          local.get $l24
          f32.mul
          local.get $l26
          local.get $l23
          f32.mul
          f32.sub
          f32.mul
          f32.sub
          f32.add
          f32.mul
          f32.mul
          local.tee $l29
          local.get $l29
          f32.add
          local.tee $l19
          f32.mul
          f32.sub
          f32.mul
          f32.add
          local.get $l23
          local.get $l23
          local.get $l28
          f32.mul
          local.get $l22
          local.get $l19
          f32.mul
          local.get $l24
          local.get $l18
          f32.mul
          f32.add
          f32.add
          local.tee $l27
          f32.mul
          f32.add
          local.get $l25
          local.get $l30
          local.get $l6
          local.get $l8
          i32.add
          local.tee $l3
          f32.load offset=24
          f32.mul
          f32.mul
          f32.sub
          f32.const 0x0p+0 (;=0;)
          f32.add
          local.set $l26
          local.get $l24
          local.get $l27
          f32.mul
          local.get $l33
          local.get $l18
          f32.mul
          local.get $l17
          local.get $l23
          local.get $l19
          f32.mul
          local.get $l22
          local.get $l28
          f32.mul
          f32.sub
          f32.mul
          f32.add
          f32.add
          local.get $l25
          local.get $l30
          local.get $l3
          f32.load offset=20
          f32.mul
          f32.mul
          f32.sub
          f32.const 0x0p+0 (;=0;)
          f32.add
          local.set $l29
          local.get $l22
          local.get $l27
          f32.mul
          local.get $l33
          local.get $l19
          f32.mul
          local.get $l17
          local.get $l24
          local.get $l28
          f32.mul
          local.get $l23
          local.get $l18
          f32.mul
          f32.sub
          f32.mul
          f32.add
          f32.add
          local.get $l25
          local.get $l30
          local.get $l3
          f32.load offset=16
          f32.mul
          f32.mul
          f32.sub
          f32.const 0x0p+0 (;=0;)
          f32.add
          local.set $l23
          local.get $l35
          local.get $l39
          local.get $l30
          local.get $l37
          f32.mul
          local.tee $l17
          f32.const 0x1p+0 (;=1;)
          local.get $l17
          f32.const 0x1p+0 (;=1;)
          f32.lt
          select
          local.tee $l17
          f32.mul
          f32.mul
          local.get $l17
          local.get $l30
          local.get $l3
          f32.load offset=8
          f32.mul
          f32.mul
          f32.sub
          f32.const 0x0p+0 (;=0;)
          f32.add
          local.set $l24
          local.get $l35
          local.get $l40
          local.get $l17
          f32.mul
          f32.mul
          local.get $l17
          local.get $l30
          local.get $l3
          f32.load offset=4
          f32.mul
          f32.mul
          f32.sub
          f32.const 0x0p+0 (;=0;)
          f32.add
          local.set $l22
          local.get $l35
          local.get $l38
          local.get $l17
          f32.mul
          f32.mul
          local.get $l17
          local.get $l30
          local.get $l3
          f32.load
          f32.mul
          f32.mul
          f32.sub
          f32.const 0x0p+0 (;=0;)
          f32.add
        end
        local.set $l17
        block $B11
          local.get $l21
          local.get $l21
          f32.mul
          local.get $l20
          local.get $l20
          f32.mul
          f32.add
          local.get $l16
          local.get $l16
          f32.mul
          f32.add
          local.tee $l18
          local.get $p1
          f32.load offset=96
          local.tee $l27
          f32.gt
          local.tee $l3
          local.get $p1
          f32.load offset=100
          local.tee $l25
          local.get $l38
          local.get $l38
          f32.mul
          local.get $l40
          local.get $l40
          f32.mul
          f32.add
          local.get $l39
          local.get $l39
          f32.mul
          f32.add
          local.tee $l33
          f32.lt
          i32.or
          i32.eqz
          br_if $B11
          local.get $l3
          if $I12
            local.get $l26
            local.get $p1
            f32.load offset=12
            local.tee $l19
            local.get $l19
            f32.mul
            f32.const -0x1p-1 (;=-0.5;)
            f32.add
            local.tee $l28
            f32.const 0x1p+0 (;=1;)
            local.get $l27
            f32.sqrt
            local.get $l18
            f32.sqrt
            f32.div
            f32.sub
            local.tee $l26
            local.get $l31
            local.get $l28
            local.get $l16
            local.get $l16
            f32.add
            local.tee $l18
            f32.mul
            local.get $l19
            local.get $l20
            local.get $l20
            f32.add
            local.tee $l27
            local.get $p1
            f32.load
            local.tee $l16
            f32.mul
            local.get $l21
            local.get $l21
            f32.add
            local.tee $l37
            local.get $p1
            f32.load offset=4
            local.tee $l20
            f32.mul
            f32.sub
            f32.mul
            f32.sub
            local.get $p1
            f32.load offset=8
            local.tee $l21
            local.get $l37
            local.get $l16
            f32.mul
            local.get $l27
            local.get $l20
            f32.mul
            f32.add
            local.get $l18
            local.get $l21
            f32.mul
            f32.add
            local.tee $l41
            f32.mul
            f32.add
            f32.mul
            f32.mul
            local.tee $l31
            local.get $l31
            f32.add
            local.tee $l31
            f32.mul
            local.get $l19
            local.get $l16
            local.get $l26
            local.get $l32
            local.get $l20
            local.get $l41
            f32.mul
            local.get $l27
            local.get $l28
            f32.mul
            local.get $l19
            local.get $l37
            local.get $l21
            f32.mul
            local.get $l18
            local.get $l16
            f32.mul
            f32.sub
            f32.mul
            f32.sub
            f32.add
            f32.mul
            f32.mul
            local.tee $l32
            local.get $l32
            f32.add
            local.tee $l32
            f32.mul
            local.get $l20
            local.get $l26
            local.get $l36
            local.get $l16
            local.get $l41
            f32.mul
            local.get $l37
            local.get $l28
            f32.mul
            local.get $l19
            local.get $l18
            local.get $l20
            f32.mul
            local.get $l27
            local.get $l21
            f32.mul
            f32.sub
            f32.mul
            f32.sub
            f32.add
            f32.mul
            f32.mul
            local.tee $l18
            local.get $l18
            f32.add
            local.tee $l18
            f32.mul
            f32.sub
            f32.mul
            f32.add
            local.get $l21
            local.get $l21
            local.get $l31
            f32.mul
            local.get $l16
            local.get $l18
            f32.mul
            local.get $l20
            local.get $l32
            f32.mul
            f32.add
            f32.add
            local.tee $l36
            f32.mul
            f32.add
            f32.add
            local.set $l26
            local.get $l29
            local.get $l20
            local.get $l36
            f32.mul
            local.get $l28
            local.get $l32
            f32.mul
            local.get $l19
            local.get $l21
            local.get $l18
            f32.mul
            local.get $l16
            local.get $l31
            f32.mul
            f32.sub
            f32.mul
            f32.add
            f32.add
            f32.add
            local.set $l29
            local.get $l23
            local.get $l16
            local.get $l36
            f32.mul
            local.get $l28
            local.get $l18
            f32.mul
            local.get $l19
            local.get $l20
            local.get $l31
            f32.mul
            local.get $l21
            local.get $l32
            f32.mul
            f32.sub
            f32.mul
            f32.add
            f32.add
            f32.add
            local.set $l23
          end
          local.get $l25
          local.get $l33
          f32.lt
          i32.eqz
          br_if $B11
          local.get $l24
          local.get $l35
          local.get $l39
          f32.mul
          f32.const 0x1p+0 (;=1;)
          local.get $l25
          f32.sqrt
          local.get $l33
          f32.sqrt
          f32.div
          f32.sub
          local.tee $l16
          f32.mul
          f32.add
          local.set $l24
          local.get $l22
          local.get $l35
          local.get $l40
          f32.mul
          local.get $l16
          f32.mul
          f32.add
          local.set $l22
          local.get $l17
          local.get $l35
          local.get $l38
          f32.mul
          local.get $l16
          f32.mul
          f32.add
          local.set $l17
        end
        local.get $l6
        local.get $l8
        i32.add
        local.tee $p1
        local.get $l34
        local.get $l17
        f32.mul
        local.get $p1
        f32.load
        f32.add
        f32.store
        local.get $p1
        local.get $l34
        local.get $l22
        f32.mul
        local.get $p1
        f32.load offset=4
        f32.add
        f32.store offset=4
        local.get $p1
        local.get $l34
        local.get $l24
        f32.mul
        local.get $p1
        f32.load offset=8
        f32.add
        f32.store offset=8
        local.get $p1
        local.get $l34
        local.get $l23
        f32.mul
        local.get $p1
        f32.load offset=16
        f32.add
        f32.store offset=16
        local.get $p1
        i32.const 20
        i32.add
        local.tee $l3
        local.get $l34
        local.get $l29
        f32.mul
        local.get $l3
        f32.load
        f32.add
        f32.store
        local.get $p1
        i32.const 24
        i32.add
        local.tee $p1
        local.get $l34
        local.get $l26
        f32.mul
        local.get $p1
        f32.load
        f32.add
        f32.store
        local.get $l4
        i32.const 1
        i32.add
        local.tee $l4
        local.get $l2
        i32.load offset=336
        i32.lt_u
        br_if $L8
      end
    end
    local.get $l2
    local.get $l5
    call $f71019
    local.get $p0
    i32.const 112
    i32.add
    local.get $l5
    call $f71204
    local.get $p0
    local.get $l2
    local.get $l5
    call $f71207
    local.get $l7
    i32.load
    i32.const 2
    i32.ge_u
    if $I13
      local.get $l5
      local.get $p0
      i32.load offset=276
      i32.store offset=12
      local.get $l2
      local.get $l5
      call $f71112
      local.get $l5
      i32.load offset=12
      local.set $l3
      local.get $l2
      i32.load offset=336
      i32.const 1
      i32.sub
      local.tee $l4
      i32.const 1
      i32.gt_u
      if $I14
        loop $L15
          local.get $l2
          i32.load offset=332
          local.set $l6
          local.get $l2
          local.get $l4
          call $f70976
          local.set $p1
          local.get $l3
          local.get $l4
          i32.const 5
          i32.shl
          i32.add
          local.tee $l7
          f32.load offset=24
          local.set $l22
          local.get $l7
          f32.load offset=20
          local.set $l23
          local.get $p1
          f32.load offset=120
          local.set $l18
          local.get $l7
          f32.load offset=16
          local.set $l24
          local.get $p1
          f32.load offset=124
          local.set $l19
          local.get $p1
          f32.load offset=128
          local.set $l20
          local.get $l7
          f32.load offset=8
          local.set $l16
          local.get $l7
          f32.load offset=4
          local.set $l17
          local.get $l3
          local.get $l6
          local.get $l4
          i32.const 80
          i32.mul
          i32.add
          i32.load offset=72
          i32.const 5
          i32.shl
          i32.add
          local.tee $p1
          local.get $l7
          f32.load
          local.tee $l21
          local.get $p1
          f32.load
          f32.add
          f32.store
          local.get $p1
          local.get $l17
          local.get $p1
          f32.load offset=4
          f32.add
          f32.store offset=4
          local.get $p1
          local.get $l16
          local.get $p1
          f32.load offset=8
          f32.add
          f32.store offset=8
          local.get $p1
          local.get $l24
          local.get $l19
          local.get $l16
          f32.mul
          local.get $l20
          local.get $l17
          f32.mul
          f32.sub
          f32.add
          local.get $p1
          f32.load offset=16
          f32.add
          f32.store offset=16
          local.get $p1
          i32.const 20
          i32.add
          local.tee $l7
          local.get $l23
          local.get $l20
          local.get $l21
          f32.mul
          local.get $l16
          local.get $l18
          f32.mul
          f32.sub
          f32.add
          local.get $l7
          f32.load
          f32.add
          f32.store
          local.get $p1
          i32.const 24
          i32.add
          local.tee $p1
          local.get $l22
          local.get $l17
          local.get $l18
          f32.mul
          local.get $l19
          local.get $l21
          f32.mul
          f32.sub
          f32.add
          local.get $p1
          f32.load
          f32.add
          f32.store
          local.get $l4
          i32.const 1
          i32.sub
          local.tee $l4
          i32.const 1
          i32.gt_u
          br_if $L15
        end
      end
      local.get $l3
      i64.const 0
      i64.store align=4
      local.get $l3
      i64.const 0
      i64.store offset=24 align=4
      local.get $l3
      i64.const 0
      i64.store offset=16 align=4
      local.get $l3
      i64.const 0
      i64.store offset=8 align=4
    end
    local.get $p0
    i32.const 1
    i32.store8 offset=488
    local.get $p0
    i32.load offset=264
    i32.const 0
    local.get $l11
    call $f484
    drop
    local.get $p0
    i32.const 0
    i32.store8 offset=12
    local.get $p0
    i64.const 0
    i64.store offset=4 align=4
    local.get $p0
    i32.load offset=448
    if $I16
      loop $L17
        local.get $l10
        i32.const 28
        i32.mul
        local.tee $l7
        local.get $p0
        i32.load offset=496
        i32.add
        local.tee $l2
        local.get $l10
        i32.const 80
        i32.mul
        local.tee $l11
        local.get $p0
        i32.load offset=444
        i32.add
        i32.load offset=64
        local.tee $p1
        f32.load
        f32.store
        local.get $l2
        local.get $p1
        f32.load offset=4
        f32.store offset=4
        local.get $l2
        local.get $p1
        f32.load offset=8
        f32.store offset=8
        local.get $l2
        local.get $p1
        f32.load offset=12
        f32.store offset=12
        local.get $l2
        local.get $p1
        f32.load offset=16
        f32.store offset=16
        local.get $l2
        local.get $p1
        f32.load offset=20
        f32.store offset=20
        local.get $l2
        local.get $p1
        f32.load offset=24
        f32.store offset=24
        local.get $p0
        i32.load offset=324
        local.get $l7
        i32.add
        local.tee $l2
        local.get $p0
        i32.load offset=444
        local.get $l11
        i32.add
        i32.load offset=64
        local.tee $p1
        f32.load
        f32.store
        local.get $l2
        local.get $p1
        f32.load offset=4
        f32.store offset=4
        local.get $l2
        local.get $p1
        f32.load offset=8
        f32.store offset=8
        local.get $l2
        local.get $p1
        f32.load offset=12
        f32.store offset=12
        local.get $l2
        local.get $p1
        f32.load offset=16
        f32.store offset=16
        local.get $l2
        local.get $p1
        f32.load offset=20
        f32.store offset=20
        local.get $l2
        local.get $p1
        f32.load offset=24
        f32.store offset=24
        local.get $p0
        i32.load offset=508
        local.get $l10
        i32.const 4
        i32.shl
        i32.add
        local.tee $l2
        i64.const 4575657221408423936
        i64.store offset=8 align=4
        local.get $l2
        i64.const 0
        i64.store align=4
        local.get $l10
        i32.const 1
        i32.add
        local.tee $l10
        local.get $p0
        i32.load offset=448
        i32.lt_u
        br_if $L17
      end
    end
    local.get $l5
    i32.const 48
    i32.add
    global.set $g0)
