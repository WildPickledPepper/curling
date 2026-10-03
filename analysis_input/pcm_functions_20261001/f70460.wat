  (func $f70460 (type $t80) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 f32) (param $p7 i32) (param $p8 i32) (param $p9 f32) (result i32)
    (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32) (local $l33 f32) (local $l34 f32) (local $l35 f32) (local $l36 f32) (local $l37 i32) (local $l38 i32) (local $l39 i32) (local $l40 i32) (local $l41 i32) (local $l42 i32) (local $l43 i32) (local $l44 i32) (local $l45 i32) (local $l46 i32) (local $l47 i32) (local $l48 i32) (local $l49 i64)
    global.get $g0
    i32.const 240
    i32.sub
    local.tee $p2
    global.set $g0
    local.get $p4
    f32.load offset=24
    local.set $l10
    local.get $p2
    local.get $p4
    f32.load
    f32.store offset=208
    local.get $p2
    local.get $p4
    f32.load offset=4
    f32.store offset=212
    local.get $p2
    local.get $p4
    f32.load offset=8
    f32.store offset=216
    local.get $p2
    local.get $p4
    f32.load offset=12
    f32.store offset=220
    local.get $p2
    local.get $p4
    f32.load offset=16
    f32.store offset=224
    local.get $p2
    local.get $p4
    f32.load offset=20
    f32.store offset=228
    local.get $p2
    local.get $l10
    local.get $p9
    f32.add
    f32.store offset=232
    local.get $p2
    i32.const 208
    i32.add
    local.get $p2
    i32.const 144
    i32.add
    call $f70397
    local.get $p2
    f32.load offset=176
    local.set $l28
    local.get $p2
    f32.load offset=164
    local.set $l29
    local.get $p2
    f32.load offset=200
    local.set $l19
    local.get $p2
    f32.load offset=172
    local.set $l30
    local.get $p2
    f32.load offset=196
    local.set $l21
    local.get $p2
    f32.load offset=160
    local.set $l31
    local.get $p2
    f32.load offset=152
    local.set $l32
    local.get $p2
    f32.load offset=168
    local.set $l33
    local.get $p2
    f32.load offset=144
    local.set $l34
    local.get $p2
    f32.load offset=156
    local.set $l35
    local.get $p2
    f32.load offset=192
    local.set $l22
    local.get $p2
    f32.load offset=148
    local.set $l36
    local.get $p0
    i32.load offset=4
    local.set $p3
    local.get $p2
    local.get $p0
    i32.store offset=136
    local.get $p2
    local.get $p3
    i32.store offset=132
    local.get $p2
    f32.const 0x1p+0 (;=1;)
    local.get $p0
    f32.load offset=8
    f32.div
    f32.store offset=124
    local.get $p2
    f32.const 0x1p+0 (;=1;)
    local.get $p0
    f32.load offset=12
    f32.div
    f32.store offset=120
    local.get $p2
    f32.const 0x1p+0 (;=1;)
    local.get $p0
    f32.load offset=16
    f32.div
    f32.store offset=128
    local.get $p8
    i32.load16_u
    local.set $p8
    local.get $p2
    i32.const 0
    i32.store16 offset=90
    local.get $p2
    local.get $p8
    i32.store16 offset=88
    local.get $p2
    local.get $p2
    i32.const 120
    i32.add
    i32.store offset=84
    local.get $p0
    i32.load8_u offset=20
    local.set $p3
    local.get $p2
    i32.const 3132048
    i32.store offset=80
    local.get $p2
    local.get $p5
    i32.store offset=100
    local.get $p2
    local.get $p7
    i32.store offset=104
    local.get $p2
    local.get $p1
    i32.store offset=108
    local.get $p2
    local.get $p6
    f32.store offset=112
    local.get $p2
    local.get $p8
    i32.const 6
    i32.shr_u
    i32.const 1
    i32.and
    i32.store8 offset=93
    local.get $p2
    local.get $p8
    i32.const 128
    i32.and
    local.get $p3
    i32.const 2
    i32.and
    i32.or
    i32.const 0
    i32.ne
    i32.store8 offset=92
    local.get $p2
    local.get $p2
    i32.const 208
    i32.add
    i32.store offset=96
    local.get $p7
    i32.const 2139095039
    i32.store offset=40
    local.get $p7
    i32.const -1
    i32.store offset=8
    local.get $p2
    local.get $p1
    f32.load
    local.tee $p9
    local.get $p9
    local.get $p1
    f32.load offset=16
    f32.const -0x1p+1 (;=-2;)
    f32.mul
    local.tee $l13
    f32.mul
    local.get $p1
    f32.load offset=20
    f32.const -0x1p+1 (;=-2;)
    f32.mul
    local.tee $l14
    local.get $p1
    f32.load offset=4
    local.tee $l11
    f32.mul
    f32.add
    local.get $p1
    f32.load offset=24
    f32.const -0x1p+1 (;=-2;)
    f32.mul
    local.tee $l16
    local.get $p1
    f32.load offset=8
    local.tee $l10
    f32.mul
    f32.add
    local.tee $l24
    f32.mul
    local.get $l13
    local.get $p1
    f32.load offset=12
    local.tee $l12
    local.get $l12
    f32.mul
    f32.const -0x1p-1 (;=-0.5;)
    f32.add
    local.tee $l15
    f32.mul
    local.get $l12
    local.get $l16
    local.get $l11
    f32.mul
    local.get $l14
    local.get $l10
    f32.mul
    f32.sub
    f32.mul
    f32.sub
    f32.add
    local.get $l15
    local.get $p2
    f32.load offset=180
    local.tee $l17
    local.get $l17
    f32.add
    local.tee $l20
    f32.mul
    local.get $l12
    local.get $l10
    local.get $p2
    f32.load offset=184
    local.tee $l17
    local.get $l17
    f32.add
    local.tee $l18
    f32.mul
    local.get $l11
    local.get $p2
    f32.load offset=188
    local.tee $l17
    local.get $l17
    f32.add
    local.tee $l23
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $p9
    local.get $l18
    local.get $l11
    f32.neg
    local.tee $l17
    f32.mul
    local.get $p9
    local.get $l20
    f32.mul
    f32.sub
    local.get $l10
    local.get $l23
    f32.mul
    f32.sub
    local.tee $l25
    f32.mul
    f32.sub
    f32.add
    local.tee $l26
    f32.store offset=64
    local.get $p2
    local.get $l11
    local.get $l24
    f32.mul
    local.get $l14
    local.get $l15
    f32.mul
    local.get $l12
    local.get $l13
    local.get $l10
    f32.mul
    local.get $l16
    local.get $p9
    f32.mul
    f32.sub
    f32.mul
    f32.sub
    f32.add
    local.get $l15
    local.get $l18
    f32.mul
    local.get $l12
    local.get $p9
    local.get $l23
    f32.mul
    local.get $l10
    local.get $l20
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l11
    local.get $l25
    f32.mul
    f32.sub
    f32.add
    local.tee $l27
    f32.store offset=68
    local.get $p2
    local.get $l16
    local.get $l15
    f32.mul
    local.get $l12
    local.get $l14
    local.get $p9
    f32.mul
    local.get $l13
    local.get $l11
    f32.mul
    f32.sub
    f32.mul
    f32.sub
    local.get $l10
    local.get $l24
    f32.mul
    f32.add
    local.get $l15
    local.get $l23
    f32.mul
    local.get $l12
    local.get $l11
    local.get $l20
    f32.mul
    local.get $p9
    local.get $l18
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l10
    local.get $l25
    f32.mul
    f32.sub
    f32.add
    local.tee $l20
    f32.store offset=72
    local.get $p2
    local.get $l15
    local.get $p5
    f32.load offset=8
    local.tee $l13
    local.get $l13
    f32.add
    local.tee $l13
    f32.mul
    local.get $l12
    local.get $l11
    local.get $p5
    f32.load
    local.tee $l14
    local.get $l14
    f32.add
    local.tee $l14
    f32.mul
    local.get $p9
    local.get $p5
    f32.load offset=4
    local.tee $l16
    local.get $l16
    f32.add
    local.tee $l16
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l10
    local.get $l16
    local.get $l17
    f32.mul
    local.get $p9
    local.get $l14
    f32.mul
    f32.sub
    local.get $l10
    local.get $l13
    f32.mul
    f32.sub
    local.tee $l18
    f32.mul
    f32.sub
    f32.store offset=56
    local.get $p2
    local.get $l15
    local.get $l16
    f32.mul
    local.get $l12
    local.get $p9
    local.get $l13
    f32.mul
    local.get $l10
    local.get $l14
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l11
    local.get $l18
    f32.mul
    f32.sub
    f32.store offset=52
    local.get $p2
    local.get $l15
    local.get $l14
    f32.mul
    local.get $l12
    local.get $l10
    local.get $l16
    f32.mul
    local.get $l11
    local.get $l13
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $p9
    local.get $l18
    f32.mul
    f32.sub
    f32.store offset=48
    local.get $p2
    local.get $l22
    local.get $l32
    f32.abs
    f32.mul
    local.get $l21
    local.get $l29
    f32.abs
    f32.mul
    f32.add
    local.get $l19
    local.get $l28
    f32.abs
    f32.mul
    f32.add
    local.tee $l13
    local.get $p9
    local.get $p9
    f32.neg
    local.get $p9
    f32.sub
    local.tee $l15
    f32.mul
    f32.const 0x1p+0 (;=1;)
    f32.add
    local.tee $l16
    local.get $l17
    local.get $l11
    f32.sub
    local.tee $l11
    local.get $l17
    f32.mul
    local.tee $l18
    f32.sub
    f32.mul
    f32.abs
    local.get $l22
    local.get $l34
    f32.abs
    f32.mul
    local.get $l21
    local.get $l35
    f32.abs
    f32.mul
    f32.add
    local.get $l19
    local.get $l33
    f32.abs
    f32.mul
    f32.add
    local.tee $l14
    local.get $l15
    local.get $l10
    f32.neg
    local.tee $p9
    f32.mul
    local.tee $l23
    local.get $l12
    local.get $l11
    f32.mul
    local.tee $l24
    f32.sub
    f32.mul
    f32.abs
    local.get $l22
    local.get $l36
    f32.abs
    f32.mul
    local.get $l21
    local.get $l31
    f32.abs
    f32.mul
    f32.add
    local.get $l19
    local.get $l30
    f32.abs
    f32.mul
    f32.add
    local.tee $l19
    local.get $l12
    local.get $l15
    f32.mul
    local.tee $l21
    local.get $l11
    local.get $p9
    f32.mul
    local.tee $l11
    f32.add
    f32.mul
    f32.abs
    f32.add
    f32.add
    local.tee $l22
    local.get $l20
    f32.add
    local.get $l20
    local.get $l22
    f32.sub
    f32.sub
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.store offset=40
    local.get $p2
    local.get $l13
    local.get $l11
    local.get $l21
    f32.sub
    f32.mul
    f32.abs
    local.get $l14
    local.get $l15
    local.get $l17
    f32.mul
    local.tee $l11
    local.get $l12
    local.get $p9
    local.get $l10
    f32.sub
    local.tee $l10
    f32.mul
    local.tee $l12
    f32.add
    f32.mul
    f32.abs
    local.get $l19
    local.get $l16
    local.get $l10
    local.get $p9
    f32.mul
    local.tee $p9
    f32.sub
    f32.mul
    f32.abs
    f32.add
    f32.add
    local.tee $l10
    local.get $l27
    f32.add
    local.get $l27
    local.get $l10
    f32.sub
    f32.sub
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.store offset=36
    local.get $p2
    local.get $l13
    local.get $l23
    local.get $l24
    f32.add
    f32.mul
    f32.abs
    local.get $l14
    f32.const 0x1p+0 (;=1;)
    local.get $l18
    f32.sub
    local.get $p9
    f32.sub
    f32.mul
    f32.abs
    local.get $l19
    local.get $l11
    local.get $l12
    f32.sub
    f32.mul
    f32.abs
    f32.add
    f32.add
    local.tee $p9
    local.get $l26
    f32.add
    local.get $l26
    local.get $p9
    f32.sub
    f32.sub
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.store offset=32
    local.get $p2
    local.get $p2
    i32.const 32
    i32.add
    i32.store offset=4
    local.get $p2
    local.get $p2
    i32.const 120
    i32.add
    i32.store
    local.get $p2
    i32.const 120
    i32.add
    local.get $p2
    i32.const 8
    i32.add
    local.tee $p8
    call $f70443
    local.get $p2
    i32.const 16
    i32.add
    local.tee $p3
    local.get $p3
    f32.load
    local.get $p2
    f32.load offset=40
    local.tee $p9
    f32.sub
    f32.store
    local.get $p2
    i32.const 12
    i32.add
    local.tee $p3
    local.get $p3
    f32.load
    local.get $p2
    f32.load offset=36
    local.tee $l10
    f32.sub
    f32.store
    local.get $p2
    i32.const 20
    i32.add
    local.tee $p3
    local.get $p2
    f32.load offset=32
    local.tee $l12
    local.get $p3
    f32.load
    f32.add
    f32.store
    local.get $p2
    i32.const 24
    i32.add
    local.tee $p3
    local.get $l10
    local.get $p3
    f32.load
    f32.add
    f32.store
    local.get $p2
    i32.const 28
    i32.add
    local.tee $p3
    local.get $p9
    local.get $p3
    f32.load
    f32.add
    f32.store
    local.get $p2
    local.get $p2
    f32.load offset=8
    local.get $l12
    f32.sub
    f32.store offset=8
    local.get $p2
    i32.load
    local.get $p2
    i32.const -64
    i32.sub
    local.get $p2
    i32.const 48
    i32.add
    local.get $p6
    local.get $p2
    i32.const 80
    i32.add
    local.get $p8
    local.get $p2
    i32.load offset=4
    call $f70461
    local.get $p2
    i32.const 208
    i32.add
    local.set $l37
    global.get $g0
    i32.const 96
    i32.sub
    local.tee $p3
    global.set $g0
    block $B0
      local.get $p2
      i32.const 80
      i32.add
      local.tee $p8
      i32.load8_u offset=10
      local.tee $l44
      i32.eqz
      br_if $B0
      local.get $p8
      i32.load8_u offset=11
      if $I1
        local.get $p7
        i32.const 1026
        i32.store16 offset=12
        local.get $p8
        i32.load8_u offset=9
        i32.const 2
        i32.and
        if $I2
          local.get $p4
          f32.load offset=16
          local.set $p9
          local.get $p4
          f32.load offset=20
          local.set $l10
          local.get $p4
          f32.load
          local.set $l11
          local.get $p4
          f32.load offset=12
          local.set $l12
          local.get $p4
          f32.load offset=24
          local.set $p6
          local.get $p4
          f32.load offset=4
          local.set $l13
          local.get $p4
          f32.load offset=8
          local.set $l14
          local.get $p3
          i32.const 0
          i32.store offset=76
          local.get $p3
          local.get $l10
          f32.store offset=72
          local.get $p3
          local.get $p9
          f32.store offset=68
          local.get $p3
          i32.const 0
          i32.store offset=60
          local.get $p3
          local.get $l14
          f32.store offset=56
          local.get $p3
          local.get $l13
          f32.store offset=52
          local.get $p3
          local.get $p6
          f32.store offset=80
          local.get $p3
          i32.const 1
          i32.store8 offset=32
          local.get $p3
          i32.const 4
          i32.store offset=28
          local.get $p3
          local.get $l12
          f32.store offset=64
          local.get $p3
          local.get $l11
          f32.store offset=48
          local.get $p3
          local.get $p6
          f32.store offset=24
          local.get $p3
          local.get $p6
          f32.store offset=20
          local.get $p3
          local.get $p6
          f32.store offset=16
          local.get $p3
          i32.const 0
          i32.store offset=12
          local.get $p3
          local.get $l11
          local.get $l12
          f32.add
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          f32.store
          local.get $p3
          local.get $l14
          local.get $l10
          f32.add
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          f32.store offset=8
          local.get $p3
          local.get $l13
          local.get $p9
          f32.add
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          f32.store offset=4
          local.get $p1
          local.set $l43
          local.get $l37
          f32.load offset=24
          local.set $l21
          local.get $p8
          i32.load8_u offset=12
          local.set $l45
          f32.const 0x0p+0 (;=0;)
          local.set $l17
          f32.const 0x0p+0 (;=0;)
          local.set $l18
          f32.const 0x0p+0 (;=0;)
          local.set $l19
          global.get $g0
          i32.const 5664
          i32.sub
          local.tee $p8
          global.set $g0
          local.get $p8
          i32.const 0
          i32.store offset=1564
          local.get $p8
          local.get $l21
          f32.const 0x1.028f5cp+0 (;=1.01;)
          f32.mul
          f32.store offset=1536
          local.get $p8
          i32.const 0
          i32.store offset=1528
          local.get $p8
          i64.const 0
          i64.store offset=1520
          local.get $p8
          i32.const 1520
          i32.add
          i32.const 128
          call $f70632
          local.get $p0
          i32.load offset=4
          local.set $l37
          local.get $p8
          local.get $p0
          i32.store offset=1512
          local.get $p8
          local.get $l37
          i32.store offset=1508
          local.get $p8
          f32.const 0x1p+0 (;=1;)
          local.get $p0
          f32.load offset=8
          f32.div
          f32.store offset=1500
          local.get $p8
          f32.const 0x1p+0 (;=1;)
          local.get $p0
          f32.load offset=12
          f32.div
          f32.store offset=1496
          local.get $p8
          f32.const 0x1p+0 (;=1;)
          local.get $p0
          f32.load offset=16
          f32.div
          f32.store offset=1504
          local.get $p8
          i64.const 0
          i64.store offset=1480
          local.get $p8
          i64.const 0
          i64.store offset=1472
          local.get $p8
          i64.const 0
          i64.store offset=1464
          local.get $p8
          i64.const 0
          i64.store offset=1456
          local.get $p8
          i64.const 0
          i64.store offset=1448
          local.get $p8
          i64.const 0
          i64.store offset=1440
          local.get $p8
          i32.const 268435455
          i32.store offset=1436
          block $B3 (result i32)
            block $B4
              loop $L5
                local.get $p3
                i64.load offset=48
                local.set $l49
                local.get $p8
                local.get $p3
                f32.load offset=56
                f32.store offset=1384
                local.get $p8
                local.get $l49
                i64.store offset=1376
                local.get $p3
                f32.load offset=72
                local.set $p6
                local.get $p3
                i64.load offset=64
                local.set $l49
                local.get $p8
                local.get $l21
                f32.store offset=1400
                local.get $p8
                local.get $l49
                i64.store offset=1388 align=4
                local.get $p8
                local.get $p6
                f32.store offset=1396
                local.get $p8
                i32.const 1376
                i32.add
                local.get $p8
                i32.const 1312
                i32.add
                call $f70397
                local.get $p8
                f32.load offset=1328
                local.set $p6
                local.get $p8
                f32.load offset=1312
                local.set $l10
                block $B6 (result f32)
                  local.get $p8
                  f32.load offset=1344
                  local.tee $p9
                  f32.const 0x0p+0 (;=0;)
                  f32.lt
                  if $I7
                    local.get $p6
                    local.get $l10
                    f32.lt
                    if $I8
                      f32.const 0x1p-1 (;=0.5;)
                      local.get $l10
                      f32.const 0x1p+0 (;=1;)
                      f32.add
                      local.get $p6
                      f32.sub
                      local.get $p9
                      f32.sub
                      local.tee $l11
                      f32.sqrt
                      f32.div
                      local.tee $p9
                      local.get $p8
                      f32.load offset=1332
                      local.get $p8
                      f32.load offset=1340
                      f32.sub
                      f32.mul
                      local.set $l12
                      local.get $p9
                      local.get $p8
                      f32.load offset=1316
                      local.get $p8
                      f32.load offset=1324
                      f32.add
                      f32.mul
                      local.set $l10
                      local.get $l11
                      local.get $p9
                      f32.mul
                      local.set $l11
                      local.get $p9
                      local.get $p8
                      f32.load offset=1336
                      local.get $p8
                      f32.load offset=1320
                      f32.add
                      f32.mul
                      br $B6
                    end
                    f32.const 0x1p-1 (;=0.5;)
                    f32.const 0x1p+0 (;=1;)
                    local.get $l10
                    f32.sub
                    local.get $p6
                    f32.add
                    local.get $p9
                    f32.sub
                    local.tee $l10
                    f32.sqrt
                    f32.div
                    local.tee $p9
                    local.get $p8
                    f32.load offset=1336
                    local.get $p8
                    f32.load offset=1320
                    f32.sub
                    f32.mul
                    local.set $l12
                    local.get $l10
                    local.get $p9
                    f32.mul
                    local.set $l10
                    local.get $p9
                    local.get $p8
                    f32.load offset=1316
                    local.get $p8
                    f32.load offset=1324
                    f32.add
                    f32.mul
                    local.set $l11
                    local.get $p9
                    local.get $p8
                    f32.load offset=1332
                    local.get $p8
                    f32.load offset=1340
                    f32.add
                    f32.mul
                    br $B6
                  end
                  local.get $p6
                  f32.neg
                  local.get $l10
                  f32.gt
                  if $I9
                    f32.const 0x1p-1 (;=0.5;)
                    local.get $p9
                    f32.const 0x1p+0 (;=1;)
                    local.get $l10
                    f32.sub
                    local.get $p6
                    f32.sub
                    f32.add
                    local.tee $p6
                    f32.sqrt
                    f32.div
                    local.tee $p9
                    local.get $p8
                    f32.load offset=1316
                    local.get $p8
                    f32.load offset=1324
                    f32.sub
                    f32.mul
                    local.set $l12
                    local.get $p9
                    local.get $p8
                    f32.load offset=1332
                    local.get $p8
                    f32.load offset=1340
                    f32.add
                    f32.mul
                    local.set $l10
                    local.get $p9
                    local.get $p8
                    f32.load offset=1336
                    local.get $p8
                    f32.load offset=1320
                    f32.add
                    f32.mul
                    local.set $l11
                    local.get $p6
                    local.get $p9
                    f32.mul
                    br $B6
                  end
                  local.get $p9
                  local.get $l10
                  f32.const 0x1p+0 (;=1;)
                  f32.add
                  local.get $p6
                  f32.add
                  f32.add
                  local.tee $p6
                  f32.const 0x1p-1 (;=0.5;)
                  local.get $p6
                  f32.sqrt
                  f32.div
                  local.tee $p9
                  f32.mul
                  local.set $l12
                  local.get $p9
                  local.get $p8
                  f32.load offset=1336
                  local.get $p8
                  f32.load offset=1320
                  f32.sub
                  f32.mul
                  local.set $l10
                  local.get $p9
                  local.get $p8
                  f32.load offset=1332
                  local.get $p8
                  f32.load offset=1340
                  f32.sub
                  f32.mul
                  local.set $l11
                  local.get $p9
                  local.get $p8
                  f32.load offset=1316
                  local.get $p8
                  f32.load offset=1324
                  f32.sub
                  f32.mul
                end
                local.set $p6
                local.get $p8
                f32.load offset=1348
                local.set $l14
                local.get $p8
                f32.load offset=1352
                local.set $l15
                local.get $p8
                local.get $p8
                f32.load offset=1356
                local.tee $l22
                local.get $l11
                local.get $l11
                f32.add
                local.tee $p9
                local.get $p6
                f32.mul
                local.tee $l23
                local.get $l10
                local.get $l10
                f32.add
                local.tee $l13
                local.get $l12
                f32.mul
                local.tee $l24
                f32.sub
                local.get $p8
                f32.load offset=1360
                local.tee $l16
                f32.mul
                f32.abs
                local.get $l13
                local.get $p6
                f32.mul
                local.tee $l25
                local.get $p9
                local.get $l12
                f32.mul
                local.tee $l26
                f32.add
                local.get $p8
                f32.load offset=1364
                local.tee $l20
                f32.mul
                f32.abs
                f32.add
                f32.const 0x1p+0 (;=1;)
                local.get $l11
                local.get $p9
                f32.mul
                f32.sub
                local.tee $l27
                local.get $l10
                local.get $l13
                f32.mul
                local.tee $l13
                f32.sub
                local.get $p8
                f32.load offset=1368
                local.tee $l11
                f32.mul
                f32.abs
                f32.add
                local.tee $l28
                f32.add
                f32.store offset=1308
                local.get $p8
                local.get $l22
                local.get $l28
                f32.sub
                f32.store offset=1296
                local.get $p8
                local.get $l15
                local.get $l16
                local.get $p9
                local.get $l10
                f32.mul
                local.tee $l10
                local.get $p6
                local.get $p6
                f32.add
                local.tee $p9
                local.get $l12
                f32.mul
                local.tee $l12
                f32.add
                f32.mul
                f32.abs
                local.get $l20
                local.get $l27
                local.get $p6
                local.get $p9
                f32.mul
                local.tee $p6
                f32.sub
                f32.mul
                f32.abs
                f32.add
                local.get $l11
                local.get $l25
                local.get $l26
                f32.sub
                f32.mul
                f32.abs
                f32.add
                local.tee $p9
                f32.add
                f32.store offset=1304
                local.get $p8
                local.get $l14
                local.get $l16
                f32.const 0x1p+0 (;=1;)
                local.get $l13
                f32.sub
                local.get $p6
                f32.sub
                f32.mul
                f32.abs
                local.get $l20
                local.get $l10
                local.get $l12
                f32.sub
                f32.mul
                f32.abs
                f32.add
                local.get $l11
                local.get $l23
                local.get $l24
                f32.add
                f32.mul
                f32.abs
                f32.add
                local.tee $p6
                f32.add
                f32.store offset=1300
                local.get $p8
                local.get $l15
                local.get $p9
                f32.sub
                f32.store offset=1292
                local.get $p8
                local.get $l14
                local.get $p6
                f32.sub
                f32.store offset=1288
                local.get $p8
                i32.const 3124912
                i32.store
                local.get $p8
                local.get $p8
                i32.const 1520
                i32.add
                i32.store offset=4
                local.get $p8
                i32.const 1496
                i32.add
                local.get $l43
                local.get $p8
                i32.const 1288
                i32.add
                i32.const 1
                local.get $p8
                call $f70450
                block $B10
                  local.get $p8
                  i32.load offset=1524
                  local.tee $p4
                  i32.eqz
                  br_if $B10
                  local.get $p8
                  i32.const 2139095039
                  i32.store offset=1408
                  i32.const 0
                  local.set $l41
                  i32.const 0
                  local.set $l42
                  local.get $p4
                  local.tee $p1
                  i32.const 31
                  i32.add
                  i32.const 5
                  i32.shr_u
                  local.tee $l46
                  i32.eqz
                  br_if $B10
                  loop $L11
                    local.get $p4
                    local.get $l41
                    i32.const 5
                    i32.shl
                    local.tee $l38
                    i32.sub
                    local.tee $p0
                    i32.const 32
                    local.get $p0
                    i32.const 32
                    i32.lt_u
                    select
                    local.tee $l47
                    if $I12
                      local.get $p1
                      i32.const 32
                      local.get $p1
                      i32.const 32
                      i32.lt_u
                      select
                      local.set $l48
                      i32.const 0
                      local.set $p0
                      loop $L13
                        local.get $p8
                        i32.const 1496
                        i32.add
                        local.get $l43
                        local.get $p8
                        local.get $p0
                        i32.const 40
                        i32.mul
                        i32.add
                        local.tee $l37
                        i32.const 0
                        i32.const 0
                        local.get $p8
                        i32.load offset=1520
                        local.get $p0
                        local.get $l38
                        i32.add
                        i32.const 2
                        i32.shl
                        i32.add
                        i32.load
                        i32.const 1
                        i32.const 1
                        call $f70452
                        local.get $l37
                        i32.const 56
                        i32.store8 offset=36
                        local.get $p0
                        i32.const 1
                        i32.add
                        local.tee $p0
                        local.get $l48
                        i32.ne
                        br_if $L13
                      end
                    end
                    local.get $p3
                    local.get $p8
                    i32.const 1536
                    i32.add
                    local.get $l45
                    local.get $p8
                    local.get $l47
                    local.get $l38
                    local.get $p8
                    i32.const 1568
                    i32.add
                    local.get $p8
                    i32.const 1564
                    i32.add
                    local.get $p8
                    i32.const 1440
                    i32.add
                    local.get $p8
                    i32.const 1472
                    i32.add
                    local.get $p8
                    i32.const 1456
                    i32.add
                    local.get $p8
                    i32.const 1436
                    i32.add
                    local.get $p8
                    i32.const 1408
                    i32.add
                    call $f70102
                    local.get $l42
                    i32.or
                    local.set $l42
                    local.get $p1
                    i32.const 32
                    i32.sub
                    local.set $p1
                    local.get $l41
                    i32.const 1
                    i32.add
                    local.tee $l41
                    local.get $l46
                    i32.ne
                    br_if $L11
                  end
                  local.get $l42
                  i32.const 1
                  i32.and
                  i32.eqz
                  br_if $B10
                  local.get $p8
                  local.get $p8
                  i32.load offset=1520
                  local.get $p8
                  i32.load offset=1436
                  i32.const 2
                  i32.shl
                  i32.add
                  i32.load
                  local.tee $p0
                  i32.store offset=1436
                  local.get $p8
                  f32.load offset=1408
                  local.get $p3
                  f32.load offset=80
                  f32.sub
                  local.tee $p6
                  f32.const 0x0p+0 (;=0;)
                  f32.le
                  i32.eqz
                  if $I14
                    i32.const 1
                    local.set $l39
                    local.get $l40
                    br_if $B10
                    local.get $p7
                    i32.const 0
                    i32.store offset=40
                    local.get $p8
                    i64.load offset=1472
                    local.set $l49
                    local.get $p7
                    local.get $p8
                    f32.load offset=1480
                    f32.store offset=24
                    local.get $p7
                    local.get $l49
                    i64.store offset=16 align=4
                    local.get $p8
                    f32.load offset=1448
                    local.set $p6
                    local.get $p7
                    local.get $p8
                    i64.load offset=1440
                    i64.store offset=28 align=4
                    local.get $p7
                    local.get $p0
                    i32.store offset=8
                    local.get $p7
                    local.get $p6
                    f32.store offset=36
                    br $B4
                  end
                  local.get $p8
                  f32.load offset=1440
                  local.set $l10
                  local.get $p8
                  f32.load offset=1444
                  local.set $p9
                  local.get $p8
                  f32.load offset=1448
                  local.set $l12
                  local.get $p3
                  i32.const 0
                  i32.store offset=12
                  local.get $p3
                  i32.const 0
                  i32.store offset=60
                  local.get $p3
                  local.get $p3
                  f32.load offset=8
                  local.tee $l11
                  local.get $p6
                  local.get $l12
                  f32.mul
                  local.tee $l12
                  f32.sub
                  local.tee $l14
                  f32.store offset=8
                  local.get $p3
                  local.get $p3
                  f32.load offset=4
                  local.tee $l15
                  local.get $p6
                  local.get $p9
                  f32.mul
                  local.tee $p9
                  f32.sub
                  local.tee $l13
                  f32.store offset=4
                  local.get $p3
                  local.get $p3
                  f32.load
                  local.tee $l16
                  local.get $p6
                  local.get $l10
                  f32.mul
                  local.tee $p6
                  f32.sub
                  local.tee $l10
                  f32.store
                  local.get $p3
                  local.get $l10
                  local.get $l16
                  f32.sub
                  local.tee $l10
                  local.get $p3
                  f32.load offset=48
                  f32.add
                  f32.store offset=48
                  local.get $p3
                  local.get $l13
                  local.get $l15
                  f32.sub
                  local.tee $l15
                  local.get $p3
                  f32.load offset=52
                  f32.add
                  f32.store offset=52
                  local.get $p3
                  local.get $l14
                  local.get $l11
                  f32.sub
                  local.tee $l11
                  local.get $p3
                  f32.load offset=56
                  f32.add
                  f32.store offset=56
                  local.get $p3
                  f32.load offset=64
                  local.set $l14
                  local.get $p3
                  f32.load offset=68
                  local.set $l13
                  local.get $p3
                  f32.load offset=72
                  local.set $l16
                  local.get $p3
                  i32.const 0
                  i32.store offset=76
                  local.get $p3
                  local.get $l11
                  local.get $l16
                  f32.add
                  f32.store offset=72
                  local.get $p3
                  local.get $l15
                  local.get $l13
                  f32.add
                  f32.store offset=68
                  local.get $p3
                  local.get $l10
                  local.get $l14
                  f32.add
                  f32.store offset=64
                  local.get $l17
                  local.get $l12
                  f32.sub
                  local.set $l17
                  local.get $l18
                  local.get $p9
                  f32.sub
                  local.set $l18
                  local.get $l19
                  local.get $p6
                  f32.sub
                  local.set $l19
                  i32.const 1
                  local.set $l39
                  local.get $l40
                  i32.const 1
                  i32.add
                  local.tee $l40
                  i32.const 4
                  i32.ne
                  br_if $L5
                end
              end
              local.get $p8
              local.get $l17
              f32.const 0x1p+0 (;=1;)
              local.get $l17
              local.get $l17
              f32.mul
              local.get $l18
              local.get $l18
              f32.mul
              local.get $l19
              local.get $l19
              f32.mul
              f32.add
              f32.add
              f32.sqrt
              local.tee $l10
              f32.div
              local.tee $p6
              f32.mul
              f32.const 0x0p+0 (;=0;)
              local.get $l10
              f32.const 0x0p+0 (;=0;)
              f32.gt
              local.tee $p0
              select
              local.tee $p9
              f32.store offset=1448
              local.get $p8
              local.get $l18
              local.get $p6
              f32.mul
              f32.const 0x0p+0 (;=0;)
              local.get $p0
              select
              local.tee $l12
              f32.store offset=1444
              local.get $p8
              local.get $l19
              local.get $p6
              f32.mul
              f32.const 0x0p+0 (;=0;)
              local.get $p0
              select
              local.tee $p6
              f32.store offset=1440
              i32.const 0
              local.get $l39
              i32.eqz
              br_if $B3
              drop
              local.get $p7
              local.get $l10
              f32.neg
              f32.store offset=40
              local.get $p8
              i64.load offset=1472
              local.set $l49
              local.get $p8
              f32.load offset=1480
              local.set $l10
              local.get $p7
              local.get $p9
              f32.store offset=36
              local.get $p7
              local.get $l12
              f32.store offset=32
              local.get $p7
              local.get $p6
              f32.store offset=28
              local.get $p7
              local.get $l10
              f32.store offset=24
              local.get $p7
              local.get $l49
              i64.store offset=16 align=4
              local.get $p7
              local.get $p8
              i32.load offset=1436
              i32.store offset=8
            end
            i32.const 1
          end
          local.set $p0
          block $B15
            local.get $p8
            i32.load offset=1528
            local.tee $l37
            i32.const 0
            i32.lt_s
            br_if $B15
            local.get $l37
            i32.const 2147483647
            i32.and
            i32.eqz
            br_if $B15
            local.get $p8
            i32.load offset=1520
            local.tee $l37
            i32.eqz
            br_if $B15
            call $f69753
            local.tee $l38
            local.get $l37
            local.get $l38
            i32.load
            i32.load offset=12
            call_indirect $__indirect_function_table (type $t1)
          end
          local.get $p8
          i32.const 5664
          i32.add
          global.set $g0
          local.get $p0
          i32.eqz
          if $I16
            local.get $p7
            i32.const 0
            i32.store offset=40
            local.get $p5
            f32.load
            local.set $p6
            local.get $p5
            f32.load offset=4
            local.set $p9
            local.get $p7
            local.get $p5
            f32.load offset=8
            f32.neg
            f32.store offset=36
            local.get $p7
            local.get $p9
            f32.neg
            f32.store offset=32
            local.get $p7
            local.get $p6
            f32.neg
            f32.store offset=28
            br $B0
          end
          local.get $p7
          local.get $p7
          i32.load16_u offset=12
          i32.const 1
          i32.or
          i32.store16 offset=12
          br $B0
        end
        local.get $p7
        i32.const 0
        i32.store offset=40
        local.get $p5
        f32.load
        local.set $p6
        local.get $p5
        f32.load offset=4
        local.set $p9
        local.get $p7
        local.get $p5
        f32.load offset=8
        f32.neg
        f32.store offset=36
        local.get $p7
        local.get $p9
        f32.neg
        f32.store offset=32
        local.get $p7
        local.get $p6
        f32.neg
        f32.store offset=28
        br $B0
      end
      local.get $p7
      i32.const 1027
      i32.store16 offset=12
    end
    local.get $p3
    i32.const 96
    i32.add
    global.set $g0
    local.get $p2
    i32.const 240
    i32.add
    global.set $g0
    local.get $l44
    i32.const 0
    i32.ne)
