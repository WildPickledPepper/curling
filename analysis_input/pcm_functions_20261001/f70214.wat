  (func $f70214 (type $t10) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (result i32)
    (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 i64)
    global.get $g0
    i32.const 32
    i32.sub
    local.tee $l8
    global.set $g0
    local.get $p2
    f32.load offset=4
    local.set $l26
    local.get $l8
    local.get $p3
    f32.load offset=16
    local.tee $l19
    f32.store
    local.get $l8
    local.get $p3
    f32.load offset=20
    local.tee $l20
    f32.store offset=4
    local.get $p3
    f32.load offset=24
    local.set $l16
    local.get $l8
    local.get $l26
    f32.store offset=12
    local.get $l8
    local.get $l16
    f32.store offset=8
    block $B0 (result i32)
      local.get $l8
      i32.const 16
      i32.add
      local.set $l9
      local.get $l8
      i32.const 28
      i32.add
      local.set $l10
      local.get $p4
      i32.load offset=32
      local.tee $p3
      local.set $l7
      global.get $g0
      i32.const 448
      i32.sub
      local.tee $l6
      global.set $g0
      local.get $l8
      f32.load offset=8
      local.set $l15
      local.get $l8
      f32.load
      local.set $l21
      local.get $l8
      f32.load offset=4
      local.set $l18
      local.get $p4
      i32.const 4
      i32.add
      local.tee $p4
      f32.load
      local.set $l11
      local.get $p4
      f32.load offset=4
      local.set $l13
      local.get $p4
      f32.load offset=8
      local.set $l12
      local.get $l6
      i32.const 0
      i32.store offset=380
      local.get $l6
      local.get $l12
      f32.store offset=376
      local.get $l6
      local.get $l13
      f32.store offset=372
      local.get $l6
      local.get $l11
      f32.store offset=368
      local.get $p4
      i64.load offset=12 align=4
      local.set $l32
      local.get $l6
      local.get $p4
      i64.load offset=20 align=4
      i64.store offset=360
      local.get $l6
      local.get $l32
      i64.store offset=352
      local.get $l6
      i32.const 0
      i32.store8 offset=224
      local.get $l6
      i32.const 216
      i32.add
      local.tee $p4
      i64.const 0
      i64.store
      local.get $l6
      i32.const 208
      i32.add
      local.tee $p2
      i64.const 0
      i64.store
      local.get $l6
      i64.const 0
      i64.store offset=200
      local.get $l6
      i64.const 0
      i64.store offset=192
      local.get $l6
      local.get $l7
      i32.const 16
      i32.add
      i32.store offset=336
      local.get $l6
      local.get $l7
      i32.load offset=56
      local.get $l7
      i32.load8_u offset=55
      i32.const 20
      i32.mul
      i32.add
      i32.store offset=344
      local.get $l6
      local.get $l7
      i32.load8_u offset=54
      i32.store8 offset=348
      local.get $p4
      local.get $l11
      local.get $l7
      f32.load offset=68
      f32.mul
      local.tee $l14
      local.get $l13
      local.get $l7
      f32.load offset=72
      f32.mul
      local.tee $l17
      local.get $l14
      local.get $l17
      f32.le
      select
      local.tee $l14
      local.get $l12
      local.get $l7
      f32.load offset=76
      f32.mul
      local.tee $l17
      local.get $l14
      local.get $l17
      f32.le
      select
      local.tee $l14
      f32.const 0x1.99999ap-6 (;=0.025;)
      f32.mul
      f32.store
      local.get $p2
      local.get $l14
      f32.const 0x1.99999ap-4 (;=0.1;)
      f32.mul
      f32.store
      local.get $l6
      local.get $l14
      f32.const 0x1.99999ap-5 (;=0.05;)
      f32.mul
      f32.store offset=212
      local.get $l6
      i32.const 368
      i32.add
      local.get $l6
      i32.const 352
      i32.add
      local.get $l6
      i32.const 240
      i32.add
      local.get $l6
      i32.const 288
      i32.add
      local.get $l6
      i32.const 192
      i32.add
      local.get $l11
      f32.const 0x1p+0 (;=1;)
      f32.eq
      local.get $l13
      f32.const 0x1p+0 (;=1;)
      f32.eq
      i32.and
      local.get $l12
      f32.const 0x1p+0 (;=1;)
      f32.eq
      i32.and
      call $f70494
      local.get $l6
      local.get $l7
      i32.load offset=60
      i32.store offset=340
      local.get $l6
      local.get $p5
      f32.load offset=12
      local.tee $l11
      local.get $l11
      f32.mul
      f32.const -0x1p-1 (;=-0.5;)
      f32.add
      local.tee $l28
      local.get $l18
      local.get $p5
      f32.load offset=20
      f32.sub
      local.tee $l13
      local.get $l13
      f32.add
      local.tee $l18
      f32.mul
      local.get $l11
      local.get $p5
      f32.load
      local.tee $l13
      local.get $l15
      local.get $p5
      f32.load offset=24
      f32.sub
      local.tee $l12
      local.get $l12
      f32.add
      local.tee $l17
      f32.mul
      local.get $p5
      f32.load offset=8
      local.tee $l12
      local.get $l21
      local.get $p5
      f32.load offset=16
      f32.sub
      local.tee $l14
      local.get $l14
      f32.add
      local.tee $l21
      f32.mul
      f32.sub
      f32.mul
      f32.add
      local.get $p5
      f32.load offset=4
      local.tee $l14
      local.get $l18
      local.get $l14
      f32.neg
      f32.mul
      local.get $l13
      local.get $l21
      f32.mul
      f32.sub
      local.get $l12
      local.get $l17
      f32.mul
      f32.sub
      local.tee $l30
      f32.mul
      f32.sub
      f32.store offset=180
      local.get $l6
      i32.const 0
      i32.store offset=188
      local.get $l6
      i32.const 0
      i32.store offset=172
      local.get $l6
      i32.const 0
      i32.store offset=156
      local.get $l6
      i32.const 184
      i32.add
      local.tee $l7
      local.get $l28
      local.get $l17
      f32.mul
      local.get $l11
      local.get $l14
      local.get $l21
      f32.mul
      local.get $l13
      local.get $l18
      f32.mul
      f32.sub
      f32.mul
      f32.add
      local.get $l12
      local.get $l30
      f32.mul
      f32.sub
      f32.store
      local.get $l6
      local.get $l14
      f32.const 0x0p+0 (;=0;)
      f32.mul
      local.tee $l24
      local.get $l11
      f32.const 0x0p+0 (;=0;)
      f32.mul
      local.tee $l22
      local.get $l12
      f32.sub
      local.get $l13
      f32.const 0x0p+0 (;=0;)
      f32.mul
      local.tee $l27
      f32.sub
      f32.add
      local.tee $l15
      local.get $l27
      local.get $l22
      local.get $l14
      f32.sub
      local.get $l12
      f32.const 0x0p+0 (;=0;)
      f32.mul
      local.tee $l25
      f32.sub
      f32.add
      local.tee $l23
      local.get $l23
      f32.add
      local.tee $l31
      f32.mul
      local.tee $l29
      local.get $l25
      local.get $l24
      local.get $l27
      local.get $l11
      f32.add
      f32.add
      f32.add
      local.tee $l27
      local.get $l25
      local.get $l22
      local.get $l13
      f32.sub
      local.get $l24
      f32.sub
      f32.add
      local.tee $l22
      local.get $l22
      f32.add
      local.tee $l24
      f32.mul
      local.tee $l25
      f32.sub
      f32.store offset=164
      local.get $l6
      local.get $l29
      local.get $l25
      f32.add
      f32.store offset=152
      local.get $l6
      f32.const 0x1p+0 (;=1;)
      local.get $l22
      local.get $l24
      f32.mul
      f32.sub
      local.tee $l22
      local.get $l23
      local.get $l31
      f32.mul
      local.tee $l25
      f32.sub
      f32.store offset=168
      local.get $l6
      local.get $l22
      local.get $l15
      local.get $l15
      local.get $l15
      f32.add
      local.tee $l29
      f32.mul
      local.tee $l22
      f32.sub
      f32.store offset=148
      local.get $l6
      local.get $l28
      local.get $l21
      f32.mul
      local.get $l11
      local.get $l12
      local.get $l18
      f32.mul
      local.get $l14
      local.get $l17
      f32.mul
      f32.sub
      f32.mul
      f32.add
      local.get $l13
      local.get $l30
      f32.mul
      f32.sub
      f32.store offset=176
      local.get $l6
      i32.const 0
      i32.store offset=140
      local.get $l6
      local.get $l15
      local.get $l24
      f32.mul
      local.tee $l11
      local.get $l27
      local.get $l31
      f32.mul
      local.tee $l13
      f32.add
      f32.store offset=160
      local.get $l6
      local.get $l23
      local.get $l24
      f32.mul
      local.tee $l12
      local.get $l27
      local.get $l29
      f32.mul
      local.tee $l14
      f32.sub
      f32.store offset=144
      local.get $l6
      local.get $l11
      local.get $l13
      f32.sub
      f32.store offset=136
      local.get $l6
      local.get $l12
      local.get $l14
      f32.add
      f32.store offset=132
      local.get $l6
      f32.const 0x1p+0 (;=1;)
      local.get $l25
      f32.sub
      local.get $l22
      f32.sub
      f32.store offset=128
      local.get $l6
      i64.const 17179869184
      i64.store offset=56
      local.get $l6
      local.get $l6
      i64.load offset=176
      i64.store offset=32
      local.get $l6
      local.get $l7
      i64.load
      i64.store offset=40
      local.get $l6
      i32.const 0
      i32.store offset=112
      local.get $l6
      local.get $l7
      i64.load
      i64.store offset=88
      local.get $l6
      local.get $l6
      i64.load offset=176
      i64.store offset=80
      local.get $l6
      local.get $l7
      i64.load
      i64.store offset=104
      local.get $l6
      i32.const 1
      i32.store8 offset=64
      local.get $l6
      i64.const 0
      i64.store offset=48
      local.get $l6
      local.get $l6
      i64.load offset=176
      i64.store offset=96
      local.get $l6
      i32.const 3132488
      i32.store offset=24
      local.get $l6
      local.get $l6
      i32.const 32
      i32.add
      i32.store offset=28
      local.get $l6
      i32.const 3132572
      i32.store offset=16
      local.get $l6
      local.get $l6
      i32.const 192
      i32.add
      i32.store offset=20
      local.get $l6
      i32.const 2139095039
      i32.store
      block $B1
        local.get $l6
        i32.const 24
        i32.add
        local.get $l6
        i32.const 16
        i32.add
        local.get $l6
        i32.const 176
        i32.add
        local.get $l6
        local.get $l6
        i32.const 432
        i32.add
        local.get $l6
        i32.const 416
        i32.add
        local.get $l6
        i32.const 400
        i32.add
        local.get $l6
        i32.const 384
        i32.add
        call $f70321
        local.tee $l7
        i32.const 2
        i32.eq
        if $I2
          local.get $l10
          i32.const 0
          i32.store
          br $B1
        end
        local.get $l10
        local.get $l6
        f32.load offset=384
        local.tee $l11
        local.get $l11
        f32.mul
        f32.store
        local.get $l6
        i64.load offset=400
        local.set $l32
        local.get $p0
        local.get $l6
        f32.load offset=408
        f32.store offset=8
        local.get $p0
        local.get $l32
        i64.store align=4
        local.get $l6
        i64.load offset=416
        local.set $l32
        local.get $l9
        local.get $l6
        f32.load offset=424
        f32.store offset=8
        local.get $l9
        local.get $l32
        i64.store align=4
        local.get $p0
        local.get $p0
        f32.load offset=8
        local.tee $l11
        local.get $l11
        f32.add
        local.tee $l13
        local.get $p5
        f32.load offset=12
        local.tee $l11
        local.get $l11
        f32.mul
        f32.const -0x1p-1 (;=-0.5;)
        f32.add
        local.tee $l21
        f32.mul
        local.get $l11
        local.get $p0
        f32.load offset=4
        local.tee $l12
        local.get $l12
        f32.add
        local.tee $l12
        local.get $p5
        f32.load
        local.tee $l14
        f32.mul
        local.get $p0
        f32.load
        local.tee $l15
        local.get $l15
        f32.add
        local.tee $l15
        local.get $p5
        f32.load offset=4
        local.tee $l18
        f32.mul
        f32.sub
        f32.mul
        f32.add
        local.get $p5
        f32.load offset=8
        local.tee $l17
        local.get $l15
        local.get $l14
        f32.mul
        local.get $l12
        local.get $l18
        f32.mul
        f32.add
        local.get $l13
        local.get $l17
        f32.mul
        f32.add
        local.tee $l23
        f32.mul
        f32.add
        f32.store offset=8
        local.get $p0
        local.get $l18
        local.get $l23
        f32.mul
        local.get $l12
        local.get $l21
        f32.mul
        local.get $l11
        local.get $l15
        local.get $l17
        f32.mul
        local.get $l13
        local.get $l14
        f32.mul
        f32.sub
        f32.mul
        f32.add
        f32.add
        f32.store offset=4
        local.get $p0
        local.get $l14
        local.get $l23
        f32.mul
        local.get $l15
        local.get $l21
        f32.mul
        local.get $l11
        local.get $l13
        local.get $l18
        f32.mul
        local.get $l12
        local.get $l17
        f32.mul
        f32.sub
        f32.mul
        f32.add
        f32.add
        f32.store
        local.get $p5
        f32.load offset=24
        local.set $l24
        local.get $p5
        f32.load offset=20
        local.set $l28
        local.get $l9
        local.get $p5
        f32.load offset=16
        local.get $p5
        f32.load
        local.tee $l13
        local.get $l13
        local.get $l9
        f32.load
        local.tee $l11
        local.get $l11
        f32.add
        local.tee $l12
        f32.mul
        local.get $l9
        f32.load offset=4
        local.tee $l11
        local.get $l11
        f32.add
        local.tee $l14
        local.get $p5
        f32.load offset=4
        local.tee $l15
        f32.mul
        f32.add
        local.get $l9
        f32.load offset=8
        local.tee $l11
        local.get $l11
        f32.add
        local.tee $l18
        local.get $p5
        f32.load offset=8
        local.tee $l17
        f32.mul
        f32.add
        local.tee $l21
        f32.mul
        local.get $l12
        local.get $p5
        f32.load offset=12
        local.tee $l11
        local.get $l11
        f32.mul
        f32.const -0x1p-1 (;=-0.5;)
        f32.add
        local.tee $l23
        f32.mul
        local.get $l11
        local.get $l18
        local.get $l15
        f32.mul
        local.get $l14
        local.get $l17
        f32.mul
        f32.sub
        f32.mul
        f32.add
        f32.add
        f32.add
        f32.store
        local.get $l9
        local.get $l28
        local.get $l15
        local.get $l21
        f32.mul
        local.get $l14
        local.get $l23
        f32.mul
        local.get $l11
        local.get $l12
        local.get $l17
        f32.mul
        local.get $l18
        local.get $l13
        f32.mul
        f32.sub
        f32.mul
        f32.add
        f32.add
        f32.add
        f32.store offset=4
        local.get $l9
        local.get $l24
        local.get $l18
        local.get $l23
        f32.mul
        local.get $l11
        local.get $l14
        local.get $l13
        f32.mul
        local.get $l12
        local.get $l15
        f32.mul
        f32.sub
        f32.mul
        f32.add
        local.get $l17
        local.get $l21
        f32.mul
        f32.add
        f32.add
        f32.store offset=8
      end
      local.get $l6
      i32.const 448
      i32.add
      global.set $g0
      block $B3
        local.get $l7
        i32.const 2
        i32.ne
        if $I4
          i32.const 0
          local.get $l8
          f32.load offset=28
          local.tee $l16
          local.get $l26
          local.get $l26
          f32.mul
          f32.gt
          br_if $B0
          drop
          local.get $p1
          local.get $l26
          local.get $l16
          f32.sqrt
          f32.sub
          local.tee $l16
          f32.const 0x0p+0 (;=0;)
          local.get $l16
          f32.const 0x0p+0 (;=0;)
          f32.gt
          select
          f32.store
          local.get $p0
          local.get $p0
          f32.load offset=8
          f32.neg
          f32.store offset=8
          local.get $p0
          local.get $p0
          f32.load offset=4
          f32.neg
          f32.store offset=4
          local.get $p0
          local.get $p0
          f32.load
          f32.neg
          f32.store
          br $B3
        end
        block $B5
          local.get $p3
          i32.load8_u offset=55
          local.tee $p4
          i32.eqz
          if $I6
            f32.const -0x1.fffffep+127 (;=-3.40282e+38;)
            local.set $l11
            br $B5
          end
          local.get $l16
          local.get $p5
          f32.load offset=24
          f32.sub
          local.tee $l16
          local.get $l16
          f32.add
          local.tee $l11
          local.get $p5
          f32.load offset=12
          local.tee $l16
          local.get $l16
          f32.mul
          f32.const -0x1p-1 (;=-0.5;)
          f32.add
          local.tee $l14
          f32.mul
          local.get $l16
          local.get $l20
          local.get $p5
          f32.load offset=20
          f32.sub
          local.tee $l20
          local.get $l20
          f32.add
          local.tee $l20
          local.get $p5
          f32.load
          local.tee $l12
          f32.mul
          local.get $l19
          local.get $p5
          f32.load offset=16
          f32.sub
          local.tee $l19
          local.get $l19
          f32.add
          local.tee $l19
          local.get $p5
          f32.load offset=4
          local.tee $l13
          f32.mul
          f32.sub
          f32.mul
          f32.sub
          local.get $p5
          f32.load offset=8
          local.tee $l15
          local.get $l19
          local.get $l12
          f32.mul
          local.get $l20
          local.get $l13
          f32.mul
          f32.add
          local.get $l11
          local.get $l15
          f32.mul
          f32.add
          local.tee $l17
          f32.mul
          f32.add
          local.set $l21
          local.get $l13
          local.get $l17
          f32.mul
          local.get $l20
          local.get $l14
          f32.mul
          local.get $l16
          local.get $l19
          local.get $l15
          f32.mul
          local.get $l11
          local.get $l12
          f32.mul
          f32.sub
          f32.mul
          f32.sub
          f32.add
          local.set $l22
          local.get $l12
          local.get $l17
          f32.mul
          local.get $l19
          local.get $l14
          f32.mul
          local.get $l16
          local.get $l11
          local.get $l13
          f32.mul
          local.get $l20
          local.get $l15
          f32.mul
          f32.sub
          f32.mul
          f32.sub
          f32.add
          local.set $l23
          local.get $p3
          i32.load offset=56
          local.set $p3
          f32.const -0x1.fffffep+127 (;=-3.40282e+38;)
          local.set $l11
          loop $L7
            local.get $p4
            i32.const 1
            i32.sub
            local.set $p4
            local.get $l11
            local.get $p3
            f32.load offset=12
            local.get $l23
            local.get $p3
            f32.load
            local.tee $l19
            f32.mul
            local.get $l22
            local.get $p3
            f32.load offset=4
            local.tee $l20
            f32.mul
            f32.add
            local.get $l21
            local.get $p3
            f32.load offset=8
            local.tee $l16
            f32.mul
            f32.add
            f32.add
            local.tee $l14
            f32.lt
            if $I8
              local.get $p0
              local.get $l16
              local.get $l16
              f32.add
              local.tee $l11
              local.get $p5
              f32.load offset=12
              local.tee $l16
              local.get $l16
              f32.mul
              f32.const -0x1p-1 (;=-0.5;)
              f32.add
              local.tee $l17
              f32.mul
              local.get $l16
              local.get $l20
              local.get $l20
              f32.add
              local.tee $l20
              local.get $p5
              f32.load
              local.tee $l12
              f32.mul
              local.get $l19
              local.get $l19
              f32.add
              local.tee $l19
              local.get $p5
              f32.load offset=4
              local.tee $l13
              f32.mul
              f32.sub
              f32.mul
              f32.add
              local.get $p5
              f32.load offset=8
              local.tee $l15
              local.get $l19
              local.get $l12
              f32.mul
              local.get $l20
              local.get $l13
              f32.mul
              f32.add
              local.get $l11
              local.get $l15
              f32.mul
              f32.add
              local.tee $l18
              f32.mul
              f32.add
              f32.store offset=8
              local.get $p0
              local.get $l13
              local.get $l18
              f32.mul
              local.get $l20
              local.get $l17
              f32.mul
              local.get $l16
              local.get $l19
              local.get $l15
              f32.mul
              local.get $l11
              local.get $l12
              f32.mul
              f32.sub
              f32.mul
              f32.add
              f32.add
              f32.store offset=4
              local.get $p0
              local.get $l12
              local.get $l18
              f32.mul
              local.get $l19
              local.get $l17
              f32.mul
              local.get $l16
              local.get $l11
              local.get $l13
              f32.mul
              local.get $l20
              local.get $l15
              f32.mul
              f32.sub
              f32.mul
              f32.add
              f32.add
              f32.store
              local.get $l14
              local.set $l11
            end
            local.get $p3
            i32.const 20
            i32.add
            local.set $p3
            local.get $p4
            br_if $L7
          end
        end
        local.get $p1
        local.get $l26
        local.get $l11
        f32.sub
        local.tee $l16
        f32.const 0x0p+0 (;=0;)
        local.get $l16
        f32.const 0x0p+0 (;=0;)
        f32.gt
        select
        f32.store
      end
      i32.const 1
    end
    local.set $p3
    local.get $l8
    i32.const 32
    i32.add
    global.set $g0
    local.get $p3)
