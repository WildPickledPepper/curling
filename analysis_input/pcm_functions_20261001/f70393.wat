  (func $f70393 (type $t80) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 f32) (param $p7 i32) (param $p8 i32) (param $p9 f32) (result i32)
    (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32) (local $l33 i32) (local $l34 i32) (local $l35 i32)
    global.get $g0
    i32.const 144
    i32.sub
    local.tee $p2
    global.set $g0
    local.get $p1
    f32.load offset=20
    local.set $p9
    local.get $p4
    f32.load offset=40
    local.set $l11
    local.get $p1
    f32.load offset=24
    local.set $l12
    local.get $p4
    f32.load offset=44
    local.set $l10
    local.get $p1
    f32.load offset=16
    local.set $l13
    local.get $p4
    f32.load offset=36
    local.set $l15
    local.get $p2
    local.get $p4
    f32.load
    f32.store offset=80
    local.get $p2
    local.get $p4
    f32.load offset=4
    f32.store offset=84
    local.get $p2
    local.get $p4
    f32.load offset=8
    f32.store offset=88
    local.get $p2
    local.get $p4
    f32.load offset=12
    f32.store offset=92
    local.get $p2
    local.get $p4
    f32.load offset=16
    f32.store offset=96
    local.get $p2
    local.get $p4
    f32.load offset=20
    f32.store offset=100
    local.get $p2
    local.get $p4
    f32.load offset=24
    f32.store offset=104
    local.get $p2
    local.get $p4
    f32.load offset=28
    f32.store offset=108
    local.get $p4
    f32.load offset=32
    local.set $l14
    local.get $p2
    local.get $l10
    local.get $l12
    f32.sub
    f32.store offset=124
    local.get $p2
    local.get $l11
    local.get $p9
    f32.sub
    f32.store offset=120
    local.get $p2
    local.get $l14
    f32.store offset=112
    local.get $p2
    local.get $l15
    local.get $l13
    f32.sub
    f32.store offset=116
    local.get $p2
    local.get $p4
    f32.load offset=48
    f32.store offset=128
    local.get $p2
    local.get $p4
    f32.load offset=52
    f32.store offset=132
    local.get $p2
    local.get $p4
    f32.load offset=56
    f32.store offset=136
    local.get $p1
    f32.load offset=8
    local.set $p9
    local.get $p1
    f32.load offset=4
    local.set $l11
    local.get $p1
    f32.load offset=12
    local.set $l12
    local.get $p1
    f32.load
    local.set $l10
    local.get $p2
    i32.const 0
    i32.store offset=60
    local.get $p2
    local.get $p9
    local.get $l11
    local.get $l11
    f32.add
    local.tee $l15
    f32.mul
    local.tee $l14
    local.get $l12
    local.get $l10
    local.get $l10
    f32.add
    local.tee $l13
    f32.mul
    local.tee $l16
    f32.sub
    f32.store offset=44
    local.get $p2
    local.get $l14
    local.get $l16
    f32.add
    f32.store offset=36
    local.get $p2
    f32.const 0x1p+0 (;=1;)
    local.get $l10
    local.get $l13
    f32.mul
    f32.sub
    local.tee $l10
    local.get $l11
    local.get $l15
    f32.mul
    local.tee $l14
    f32.sub
    f32.store offset=48
    local.get $p2
    local.get $l10
    local.get $p9
    local.get $p9
    local.get $p9
    f32.add
    local.tee $l16
    f32.mul
    local.tee $l17
    f32.sub
    f32.store offset=32
    local.get $p2
    i64.const 0
    i64.store offset=52 align=4
    local.get $p2
    local.get $l13
    local.get $p9
    f32.mul
    local.tee $p9
    local.get $l15
    local.get $l12
    f32.mul
    local.tee $l10
    f32.add
    f32.store offset=40
    local.get $p2
    local.get $l13
    local.get $l11
    f32.mul
    local.tee $l11
    local.get $l16
    local.get $l12
    f32.mul
    local.tee $l12
    f32.sub
    f32.store offset=28
    local.get $p2
    local.get $p9
    local.get $l10
    f32.sub
    f32.store offset=24
    local.get $p2
    local.get $l11
    local.get $l12
    f32.add
    f32.store offset=20
    local.get $p2
    f32.const 0x1p+0 (;=1;)
    local.get $l14
    f32.sub
    local.get $l17
    f32.sub
    f32.store offset=16
    local.get $p2
    local.get $p0
    f32.load offset=4
    f32.store offset=64
    local.get $p2
    local.get $p0
    f32.load offset=8
    f32.store offset=68
    local.get $p2
    local.get $p0
    f32.load offset=12
    f32.store offset=72
    local.get $p2
    local.get $p8
    i32.load16_u
    i32.store16 offset=8
    local.get $p2
    i32.const 80
    i32.add
    local.set $p3
    local.get $p2
    i32.const 16
    i32.add
    local.set $p4
    global.get $g0
    i32.const 592
    i32.sub
    local.tee $p0
    global.set $g0
    block $B0
      block $B1
        local.get $p2
        i32.const 8
        i32.add
        i32.load8_u
        i32.const 16
        i32.and
        br_if $B1
        i32.const 1
        local.set $l34
        local.get $p3
        i32.const 48
        i32.add
        local.get $p3
        i32.const 36
        i32.add
        local.get $p3
        local.get $p4
        i32.const 48
        i32.add
        local.get $p4
        i32.const 36
        i32.add
        local.get $p4
        call $f69906
        i32.eqz
        br_if $B1
        local.get $p7
        i32.const 0
        i32.store offset=40
        local.get $p7
        i32.const 2
        i32.store16 offset=12
        local.get $p5
        f32.load
        local.set $p9
        local.get $p5
        f32.load offset=4
        local.set $l10
        local.get $p7
        local.get $p5
        f32.load offset=8
        f32.neg
        f32.store offset=36
        local.get $p7
        local.get $l10
        f32.neg
        f32.store offset=32
        local.get $p7
        local.get $p9
        f32.neg
        f32.store offset=28
        br $B0
      end
      local.get $p0
      i32.const 496
      i32.add
      local.get $p3
      i32.const 36
      i32.add
      local.get $p3
      i32.const 48
      i32.add
      local.get $p3
      local.get $p3
      i32.const 12
      i32.add
      local.get $p3
      i32.const 24
      i32.add
      call $f70389
      local.get $p0
      i32.const 400
      i32.add
      local.get $p4
      i32.const 36
      i32.add
      local.get $p4
      i32.const 48
      i32.add
      local.get $p4
      local.get $p4
      i32.const 12
      i32.add
      local.get $p4
      i32.const 24
      i32.add
      call $f70389
      local.get $p3
      f32.load offset=52
      local.set $p9
      local.get $p3
      f32.load offset=48
      local.set $l10
      local.get $p0
      local.get $p3
      f32.load offset=56
      local.tee $l11
      f32.neg
      f32.store offset=232
      local.get $p0
      local.get $p9
      f32.neg
      f32.store offset=228
      local.get $p0
      local.get $l10
      f32.neg
      f32.store offset=224
      local.get $p0
      local.get $l11
      f32.store offset=88
      local.get $p0
      local.get $p9
      f32.store offset=84
      local.get $p0
      local.get $l10
      f32.store offset=80
      local.get $p3
      f32.load offset=28
      local.tee $l13
      local.get $p3
      f32.load offset=40
      f32.neg
      local.tee $p9
      f32.mul
      local.get $p3
      f32.load offset=24
      local.tee $l14
      local.get $p3
      f32.load offset=36
      local.tee $l10
      f32.mul
      f32.sub
      local.get $p3
      f32.load offset=32
      local.tee $l16
      local.get $p3
      f32.load offset=44
      local.tee $l11
      f32.mul
      f32.sub
      local.set $l22
      local.get $p3
      f32.load offset=16
      local.tee $l17
      local.get $p9
      f32.mul
      local.get $p3
      f32.load offset=12
      local.tee $l15
      local.get $l10
      f32.mul
      f32.sub
      local.get $p3
      f32.load offset=20
      local.tee $l19
      local.get $l11
      f32.mul
      f32.sub
      local.set $l24
      local.get $p3
      f32.load offset=4
      local.tee $l20
      local.get $p9
      f32.mul
      local.get $p3
      f32.load
      local.tee $l21
      local.get $l10
      f32.mul
      f32.sub
      local.get $p3
      f32.load offset=8
      local.tee $l18
      local.get $l11
      f32.mul
      f32.sub
      local.set $l27
      local.get $l14
      local.get $p5
      f32.load
      local.tee $p9
      f32.mul
      local.get $l13
      local.get $p5
      f32.load offset=4
      local.tee $l10
      f32.mul
      f32.add
      local.get $l16
      local.get $p5
      f32.load offset=8
      local.tee $l11
      f32.mul
      f32.add
      f32.neg
      local.set $l28
      local.get $l15
      local.get $p9
      f32.mul
      local.get $l17
      local.get $l10
      f32.mul
      f32.add
      local.get $l19
      local.get $l11
      f32.mul
      f32.add
      f32.neg
      local.set $l29
      local.get $l21
      local.get $p9
      f32.mul
      local.get $l20
      local.get $l10
      f32.mul
      f32.add
      local.get $l18
      local.get $l11
      f32.mul
      f32.add
      f32.neg
      local.set $l30
      i32.const -1
      local.set $l35
      loop $L2
        local.get $p0
        local.get $l22
        local.get $l14
        local.get $p0
        i32.const 400
        i32.add
        local.get $l33
        i32.const 12
        i32.mul
        i32.add
        local.tee $l34
        f32.load
        local.tee $p9
        f32.mul
        local.get $l13
        local.get $l34
        f32.load offset=4
        local.tee $l10
        f32.mul
        f32.add
        local.get $l16
        local.get $l34
        f32.load offset=8
        local.tee $l11
        f32.mul
        f32.add
        f32.add
        f32.store offset=392
        local.get $p0
        local.get $l24
        local.get $l15
        local.get $p9
        f32.mul
        local.get $l17
        local.get $l10
        f32.mul
        f32.add
        local.get $l19
        local.get $l11
        f32.mul
        f32.add
        f32.add
        f32.store offset=388
        local.get $p0
        local.get $l27
        local.get $l21
        local.get $p9
        f32.mul
        local.get $l20
        local.get $l10
        f32.mul
        f32.add
        local.get $l18
        local.get $l11
        f32.mul
        f32.add
        f32.add
        f32.store offset=384
        local.get $p0
        local.get $l28
        f32.store offset=376
        local.get $p0
        local.get $l29
        f32.store offset=372
        local.get $p0
        local.get $l30
        f32.store offset=368
        block $B3
          local.get $p0
          i32.const 224
          i32.add
          local.get $p0
          i32.const 80
          i32.add
          local.get $p0
          i32.const 384
          i32.add
          local.get $p0
          i32.const 368
          i32.add
          local.get $p0
          i32.const -64
          i32.sub
          local.get $p0
          i32.const 48
          i32.add
          call $f69910
          local.tee $p8
          i32.const -1
          i32.eq
          br_if $B3
          local.get $p0
          f32.load offset=64
          local.tee $p9
          f32.const 0x0p+0 (;=0;)
          f32.lt
          br_if $B3
          local.get $p6
          local.get $p9
          f32.ge
          i32.eqz
          br_if $B3
          local.get $p3
          f32.load offset=24
          local.set $p6
          local.get $p3
          f32.load
          local.set $l25
          local.get $p3
          f32.load offset=12
          local.set $l23
          local.get $p3
          f32.load offset=28
          local.set $l26
          local.get $p3
          f32.load offset=4
          local.set $l31
          local.get $p3
          f32.load offset=16
          local.set $l32
          local.get $p7
          local.get $p8
          i32.const 12
          i32.mul
          local.tee $p8
          i32.const 3128848
          i32.add
          f32.load
          local.tee $l10
          local.get $p3
          f32.load offset=8
          f32.mul
          local.get $p8
          i32.const 3128852
          i32.add
          f32.load
          local.tee $l11
          local.get $p3
          f32.load offset=20
          f32.mul
          f32.add
          local.get $p8
          i32.const 3128856
          i32.add
          f32.load
          local.tee $l12
          local.get $p3
          f32.load offset=32
          f32.mul
          f32.add
          f32.store offset=36
          local.get $p7
          local.get $l10
          local.get $l31
          f32.mul
          local.get $l11
          local.get $l32
          f32.mul
          f32.add
          local.get $l12
          local.get $l26
          f32.mul
          f32.add
          f32.store offset=32
          local.get $p7
          local.get $l10
          local.get $l25
          f32.mul
          local.get $l11
          local.get $l23
          f32.mul
          f32.add
          local.get $l12
          local.get $p6
          f32.mul
          f32.add
          f32.store offset=28
          local.get $p7
          local.get $l34
          f32.load
          f32.store offset=16
          local.get $p7
          local.get $l34
          f32.load offset=4
          f32.store offset=20
          local.get $p7
          local.get $l34
          f32.load offset=8
          f32.store offset=24
          i32.const 0
          local.set $l35
          local.get $p9
          local.set $p6
        end
        local.get $l33
        i32.const 1
        i32.add
        local.tee $l33
        i32.const 8
        i32.ne
        br_if $L2
      end
      local.get $p4
      f32.load offset=52
      local.set $p9
      local.get $p4
      f32.load offset=48
      local.set $l10
      local.get $p0
      local.get $p4
      f32.load offset=56
      local.tee $l11
      f32.neg
      f32.store offset=232
      local.get $p0
      local.get $p9
      f32.neg
      f32.store offset=228
      local.get $p0
      local.get $l10
      f32.neg
      f32.store offset=224
      local.get $p0
      local.get $l11
      f32.store offset=88
      local.get $p0
      local.get $p9
      f32.store offset=84
      local.get $p0
      local.get $l10
      f32.store offset=80
      local.get $p4
      f32.load offset=40
      local.set $l24
      local.get $p4
      f32.load offset=44
      local.set $p9
      local.get $p4
      f32.load offset=20
      local.set $l13
      local.get $p4
      f32.load offset=16
      local.set $l14
      local.get $p4
      f32.load offset=36
      local.set $l10
      local.get $p4
      f32.load offset=8
      local.set $l16
      local.get $p4
      f32.load
      local.set $l17
      local.get $p4
      f32.load offset=4
      local.set $l15
      local.get $p4
      f32.load offset=12
      local.set $l19
      local.get $p0
      local.get $p4
      f32.load offset=24
      local.tee $l20
      local.get $p5
      f32.load
      local.tee $l11
      f32.mul
      local.get $p4
      f32.load offset=28
      local.tee $l21
      local.get $p5
      f32.load offset=4
      local.tee $l12
      f32.mul
      f32.add
      local.get $p4
      f32.load offset=32
      local.tee $l18
      local.get $p5
      f32.load offset=8
      local.tee $l22
      f32.mul
      f32.add
      f32.store offset=392
      local.get $p0
      local.get $l19
      local.get $l11
      f32.mul
      local.get $l14
      local.get $l12
      f32.mul
      f32.add
      local.get $l13
      local.get $l22
      f32.mul
      f32.add
      f32.store offset=388
      local.get $p0
      local.get $l17
      local.get $l11
      f32.mul
      local.get $l15
      local.get $l12
      f32.mul
      f32.add
      local.get $l16
      local.get $l22
      f32.mul
      f32.add
      f32.store offset=384
      local.get $l21
      local.get $l24
      f32.neg
      local.tee $l11
      f32.mul
      local.get $l20
      local.get $l10
      f32.mul
      f32.sub
      local.get $l18
      local.get $p9
      f32.mul
      f32.sub
      local.set $l22
      local.get $l14
      local.get $l11
      f32.mul
      local.get $l19
      local.get $l10
      f32.mul
      f32.sub
      local.get $l13
      local.get $p9
      f32.mul
      f32.sub
      local.set $l24
      local.get $l15
      local.get $l11
      f32.mul
      local.get $l17
      local.get $l10
      f32.mul
      f32.sub
      local.get $l16
      local.get $p9
      f32.mul
      f32.sub
      local.set $l27
      i32.const 0
      local.set $l33
      loop $L4
        local.get $p0
        local.get $l22
        local.get $l20
        local.get $p0
        i32.const 496
        i32.add
        local.get $l33
        i32.const 12
        i32.mul
        i32.add
        local.tee $l34
        f32.load
        local.tee $p9
        f32.mul
        local.get $l21
        local.get $l34
        f32.load offset=4
        local.tee $l10
        f32.mul
        f32.add
        local.get $l18
        local.get $l34
        f32.load offset=8
        local.tee $l11
        f32.mul
        f32.add
        f32.add
        f32.store offset=376
        local.get $p0
        local.get $l24
        local.get $l19
        local.get $p9
        f32.mul
        local.get $l14
        local.get $l10
        f32.mul
        f32.add
        local.get $l13
        local.get $l11
        f32.mul
        f32.add
        f32.add
        f32.store offset=372
        local.get $p0
        local.get $l27
        local.get $l17
        local.get $p9
        f32.mul
        local.get $l15
        local.get $l10
        f32.mul
        f32.add
        local.get $l16
        local.get $l11
        f32.mul
        f32.add
        f32.add
        f32.store offset=368
        block $B5
          local.get $p0
          i32.const 224
          i32.add
          local.get $p0
          i32.const 80
          i32.add
          local.get $p0
          i32.const 368
          i32.add
          local.get $p0
          i32.const 384
          i32.add
          local.get $p0
          i32.const -64
          i32.sub
          local.get $p0
          i32.const 48
          i32.add
          call $f69910
          local.tee $p8
          i32.const -1
          i32.eq
          br_if $B5
          local.get $p0
          f32.load offset=64
          local.tee $p9
          f32.const 0x0p+0 (;=0;)
          f32.lt
          br_if $B5
          local.get $p6
          local.get $p9
          f32.ge
          i32.eqz
          br_if $B5
          local.get $p4
          f32.load offset=24
          local.set $p6
          local.get $p4
          f32.load offset=12
          local.set $l28
          local.get $p4
          f32.load
          local.set $l29
          local.get $p4
          f32.load offset=28
          local.set $l30
          local.get $p4
          f32.load offset=16
          local.set $l25
          local.get $p4
          f32.load offset=4
          local.set $l23
          local.get $p7
          local.get $p4
          f32.load offset=20
          local.get $p8
          i32.const 12
          i32.mul
          local.tee $p8
          i32.const 3128852
          i32.add
          f32.load
          f32.neg
          local.tee $l10
          f32.mul
          local.get $p8
          i32.const 3128848
          i32.add
          f32.load
          local.tee $l11
          local.get $p4
          f32.load offset=8
          f32.mul
          f32.sub
          local.get $p8
          i32.const 3128856
          i32.add
          f32.load
          local.tee $l12
          local.get $p4
          f32.load offset=32
          f32.mul
          f32.sub
          f32.store offset=36
          local.get $p7
          local.get $l25
          local.get $l10
          f32.mul
          local.get $l11
          local.get $l23
          f32.mul
          f32.sub
          local.get $l12
          local.get $l30
          f32.mul
          f32.sub
          f32.store offset=32
          local.get $p7
          local.get $l28
          local.get $l10
          f32.mul
          local.get $l11
          local.get $l29
          f32.mul
          f32.sub
          local.get $l12
          local.get $p6
          f32.mul
          f32.sub
          f32.store offset=28
          local.get $l34
          f32.load
          local.set $l10
          local.get $p5
          f32.load
          local.set $l11
          local.get $l34
          f32.load offset=4
          local.set $l12
          local.get $p5
          f32.load offset=4
          local.set $p6
          local.get $p7
          local.get $p9
          local.get $p5
          f32.load offset=8
          f32.mul
          local.get $l34
          f32.load offset=8
          f32.add
          f32.store offset=24
          local.get $p7
          local.get $l12
          local.get $p9
          local.get $p6
          f32.mul
          f32.add
          f32.store offset=20
          local.get $p7
          local.get $l10
          local.get $p9
          local.get $l11
          f32.mul
          f32.add
          f32.store offset=16
          i32.const 1
          local.set $l35
          local.get $p9
          local.set $p6
        end
        local.get $l33
        i32.const 1
        i32.add
        local.tee $l33
        i32.const 8
        i32.ne
        br_if $L4
      end
      local.get $p3
      f32.load offset=32
      local.set $l12
      local.get $p3
      f32.load offset=28
      local.set $l13
      local.get $p3
      f32.load offset=24
      local.set $l14
      local.get $p3
      f32.load offset=20
      local.set $l16
      local.get $p3
      f32.load offset=16
      local.set $l17
      local.get $p3
      f32.load offset=12
      local.set $l15
      local.get $p3
      f32.load offset=8
      local.set $l19
      local.get $p3
      f32.load offset=4
      local.set $l20
      local.get $p3
      f32.load
      local.set $l21
      i32.const 0
      local.set $l33
      loop $L6
        local.get $l33
        i32.const 12
        i32.mul
        local.tee $p3
        local.get $p0
        i32.const 224
        i32.add
        i32.add
        local.tee $p8
        local.get $p3
        i32.const 3128928
        i32.add
        f32.load
        local.tee $p9
        local.get $l19
        f32.mul
        local.get $p3
        i32.const 3128932
        i32.add
        f32.load
        local.tee $l10
        local.get $l16
        f32.mul
        f32.add
        local.get $p3
        i32.const 3128936
        i32.add
        f32.load
        local.tee $l11
        local.get $l12
        f32.mul
        f32.add
        f32.store offset=8
        local.get $p8
        local.get $p9
        local.get $l20
        f32.mul
        local.get $l10
        local.get $l17
        f32.mul
        f32.add
        local.get $l11
        local.get $l13
        f32.mul
        f32.add
        f32.store offset=4
        local.get $p8
        local.get $p9
        local.get $l21
        f32.mul
        local.get $l10
        local.get $l15
        f32.mul
        f32.add
        local.get $l11
        local.get $l14
        f32.mul
        f32.add
        f32.store
        local.get $l33
        i32.const 1
        i32.add
        local.tee $l33
        i32.const 12
        i32.ne
        br_if $L6
      end
      local.get $p4
      f32.load offset=32
      local.set $l12
      local.get $p4
      f32.load offset=28
      local.set $l13
      local.get $p4
      f32.load offset=24
      local.set $l14
      local.get $p4
      f32.load offset=20
      local.set $l16
      local.get $p4
      f32.load offset=16
      local.set $l17
      local.get $p4
      f32.load offset=12
      local.set $l15
      local.get $p4
      f32.load offset=8
      local.set $l19
      local.get $p4
      f32.load offset=4
      local.set $l20
      local.get $p4
      f32.load
      local.set $l21
      i32.const 0
      local.set $p4
      loop $L7
        local.get $p4
        i32.const 12
        i32.mul
        local.tee $p3
        local.get $p0
        i32.const 80
        i32.add
        i32.add
        local.tee $l33
        local.get $p3
        i32.const 3128928
        i32.add
        f32.load
        local.tee $p9
        local.get $l19
        f32.mul
        local.get $p3
        i32.const 3128932
        i32.add
        f32.load
        local.tee $l10
        local.get $l16
        f32.mul
        f32.add
        local.get $p3
        i32.const 3128936
        i32.add
        f32.load
        local.tee $l11
        local.get $l12
        f32.mul
        f32.add
        f32.store offset=8
        local.get $l33
        local.get $p9
        local.get $l20
        f32.mul
        local.get $l10
        local.get $l17
        f32.mul
        f32.add
        local.get $l11
        local.get $l13
        f32.mul
        f32.add
        f32.store offset=4
        local.get $l33
        local.get $p9
        local.get $l21
        f32.mul
        local.get $l10
        local.get $l15
        f32.mul
        f32.add
        local.get $l11
        local.get $l14
        f32.mul
        f32.add
        f32.store
        local.get $p4
        i32.const 1
        i32.add
        local.tee $p4
        i32.const 12
        i32.ne
        br_if $L7
      end
      i32.const 0
      local.set $p8
      loop $L8
        block $B9
          local.get $p0
          i32.const 224
          i32.add
          local.get $p8
          i32.const 12
          i32.mul
          i32.add
          local.tee $p3
          f32.load
          local.tee $l19
          local.get $p5
          f32.load
          local.tee $p9
          f32.mul
          local.get $p3
          f32.load offset=4
          local.tee $l20
          local.get $p5
          f32.load offset=4
          local.tee $l10
          f32.mul
          f32.add
          local.get $p3
          f32.load offset=8
          local.tee $l21
          local.get $p5
          f32.load offset=8
          local.tee $l11
          f32.mul
          f32.add
          f32.const 0x0p+0 (;=0;)
          f32.ge
          i32.eqz
          br_if $B9
          local.get $p0
          local.get $p0
          i32.const 496
          i32.add
          local.get $p8
          i32.const 1
          i32.shl
          local.tee $p4
          i32.const 4117344
          i32.add
          i32.load8_u
          i32.const 12
          i32.mul
          i32.add
          local.tee $p3
          f32.load
          local.tee $l12
          f32.store offset=64
          local.get $p0
          local.get $p3
          f32.load offset=4
          local.tee $l13
          f32.store offset=68
          local.get $p0
          local.get $p3
          f32.load offset=8
          local.tee $l14
          f32.store offset=72
          local.get $p0
          local.get $p0
          i32.const 496
          i32.add
          local.get $p4
          i32.const 1
          i32.or
          i32.const 4117344
          i32.add
          i32.load8_u
          i32.const 12
          i32.mul
          i32.add
          local.tee $p3
          f32.load
          local.tee $l16
          f32.store offset=48
          local.get $p0
          local.get $p3
          f32.load offset=4
          local.tee $l17
          f32.store offset=52
          local.get $p0
          local.get $p3
          f32.load offset=8
          local.tee $l15
          f32.store offset=56
          local.get $l16
          local.get $l12
          f32.sub
          local.tee $l18
          local.get $l18
          f32.mul
          local.get $l17
          local.get $l13
          f32.sub
          local.tee $l25
          local.get $l25
          f32.mul
          f32.add
          local.get $l15
          local.get $l14
          f32.sub
          local.tee $l23
          local.get $l23
          f32.mul
          f32.add
          f32.sqrt
          local.tee $l26
          f32.const 0x0p+0 (;=0;)
          f32.gt
          if $I10
            local.get $p0
            local.get $l14
            local.get $l23
            f32.const 0x1.47ae14p-7 (;=0.01;)
            local.get $l26
            f32.div
            local.tee $l26
            f32.mul
            local.tee $l23
            f32.sub
            f32.store offset=72
            local.get $p0
            local.get $l13
            local.get $l25
            local.get $l26
            f32.mul
            local.tee $l14
            f32.sub
            f32.store offset=68
            local.get $p0
            local.get $l12
            local.get $l18
            local.get $l26
            f32.mul
            local.tee $l13
            f32.sub
            f32.store offset=64
            local.get $p0
            local.get $l15
            local.get $l23
            f32.add
            f32.store offset=56
            local.get $p0
            local.get $l17
            local.get $l14
            f32.add
            f32.store offset=52
            local.get $p0
            local.get $l16
            local.get $l13
            f32.add
            f32.store offset=48
          end
          i32.const 0
          local.set $p3
          loop $L11
            block $B12
              local.get $p0
              i32.const 80
              i32.add
              local.get $p3
              i32.const 12
              i32.mul
              i32.add
              local.tee $p4
              f32.load
              local.tee $l12
              local.get $p9
              f32.mul
              local.get $p4
              f32.load offset=4
              local.tee $p9
              local.get $l10
              f32.mul
              f32.add
              local.get $p4
              f32.load offset=8
              local.tee $l10
              local.get $l11
              f32.mul
              f32.add
              f32.const 0x0p+0 (;=0;)
              f32.ge
              br_if $B12
              local.get $l12
              local.get $l19
              f32.mul
              local.get $p9
              local.get $l20
              f32.mul
              f32.add
              local.get $l10
              local.get $l21
              f32.mul
              f32.add
              f32.const 0x0p+0 (;=0;)
              f32.ge
              br_if $B12
              local.get $p0
              local.get $p0
              i32.const 400
              i32.add
              local.get $p3
              i32.const 1
              i32.shl
              local.tee $l33
              i32.const 4117344
              i32.add
              i32.load8_u
              i32.const 12
              i32.mul
              i32.add
              local.tee $p4
              f32.load
              local.tee $p9
              f32.store offset=32
              local.get $p0
              local.get $p4
              f32.load offset=4
              local.tee $l10
              f32.store offset=36
              local.get $p0
              local.get $p4
              f32.load offset=8
              local.tee $l11
              f32.store offset=40
              local.get $p0
              local.get $p0
              i32.const 400
              i32.add
              local.get $l33
              i32.const 1
              i32.or
              i32.const 4117344
              i32.add
              i32.load8_u
              i32.const 12
              i32.mul
              i32.add
              local.tee $p4
              f32.load
              local.tee $l12
              f32.store offset=16
              local.get $p0
              local.get $p4
              f32.load offset=4
              local.tee $l13
              f32.store offset=20
              local.get $p0
              local.get $p4
              f32.load offset=8
              local.tee $l14
              f32.store offset=24
              local.get $l12
              local.get $p9
              f32.sub
              local.tee $l16
              local.get $l16
              f32.mul
              local.get $l13
              local.get $l10
              f32.sub
              local.tee $l17
              local.get $l17
              f32.mul
              f32.add
              local.get $l14
              local.get $l11
              f32.sub
              local.tee $l15
              local.get $l15
              f32.mul
              f32.add
              f32.sqrt
              local.tee $l18
              f32.const 0x0p+0 (;=0;)
              f32.gt
              if $I13
                local.get $p0
                local.get $l11
                local.get $l15
                f32.const 0x1.47ae14p-7 (;=0.01;)
                local.get $l18
                f32.div
                local.tee $l18
                f32.mul
                local.tee $l15
                f32.sub
                f32.store offset=40
                local.get $p0
                local.get $l10
                local.get $l17
                local.get $l18
                f32.mul
                local.tee $l11
                f32.sub
                f32.store offset=36
                local.get $p0
                local.get $p9
                local.get $l16
                local.get $l18
                f32.mul
                local.tee $l10
                f32.sub
                f32.store offset=32
                local.get $p0
                local.get $l14
                local.get $l15
                f32.add
                f32.store offset=24
                local.get $p0
                local.get $l13
                local.get $l11
                f32.add
                f32.store offset=20
                local.get $p0
                local.get $l12
                local.get $l10
                f32.add
                f32.store offset=16
              end
              local.get $p0
              i32.const -64
              i32.sub
              local.get $p0
              i32.const 48
              i32.add
              local.get $p5
              local.get $p0
              i32.const 32
              i32.add
              local.get $p0
              i32.const 16
              i32.add
              local.get $p0
              i32.const 12
              i32.add
              local.get $p0
              call $f69908
              i32.eqz
              br_if $B12
              local.get $p0
              f32.load offset=12
              local.tee $p9
              local.get $p6
              f32.le
              i32.eqz
              br_if $B12
              local.get $p0
              local.get $p0
              f32.load offset=64
              f32.store offset=384
              local.get $p0
              local.get $p0
              i64.load offset=68 align=4
              i64.store offset=388 align=4
              local.get $p0
              local.get $p0
              f32.load offset=32
              f32.store offset=368
              local.get $p0
              local.get $p0
              i64.load offset=36 align=4
              i64.store offset=372 align=4
              local.get $p5
              f32.load
              local.set $l10
              local.get $p5
              f32.load offset=4
              local.set $l11
              local.get $p0
              f32.load offset=48
              local.set $l27
              local.get $p0
              f32.load offset=52
              local.set $l24
              local.get $p0
              f32.load offset=56
              local.set $l22
              local.get $p0
              f32.load offset=16
              local.set $l30
              local.get $p0
              f32.load offset=20
              local.set $l29
              local.get $p0
              f32.load offset=24
              local.set $l28
              local.get $p0
              f32.load
              local.set $l12
              local.get $p0
              f32.load offset=4
              local.set $l13
              local.get $p7
              local.get $p9
              local.get $p5
              f32.load offset=8
              f32.mul
              local.get $p0
              f32.load offset=8
              f32.add
              f32.store offset=24
              local.get $p7
              local.get $l13
              local.get $p9
              local.get $l11
              f32.mul
              f32.add
              f32.store offset=20
              local.get $p7
              local.get $l12
              local.get $p9
              local.get $l10
              f32.mul
              f32.add
              f32.store offset=16
              i32.const 2
              local.set $l35
              local.get $p9
              local.set $p6
            end
            local.get $p3
            i32.const 1
            i32.add
            local.tee $p3
            i32.const 12
            i32.eq
            br_if $B9
            local.get $p5
            f32.load offset=8
            local.set $l11
            local.get $p5
            f32.load offset=4
            local.set $l10
            local.get $p5
            f32.load
            local.set $p9
            br $L11
          end
          unreachable
        end
        local.get $p8
        i32.const 1
        i32.add
        local.tee $p8
        i32.const 12
        i32.ne
        br_if $L8
      end
      local.get $l35
      i32.const -1
      i32.ne
      if $I14
        block $B15
          local.get $l35
          i32.const 2
          i32.ne
          br_if $B15
          local.get $p0
          local.get $l22
          local.get $p0
          f32.load offset=392
          f32.sub
          f32.store offset=232
          local.get $p0
          local.get $l24
          local.get $p0
          f32.load offset=388
          f32.sub
          f32.store offset=228
          local.get $p0
          local.get $l27
          local.get $p0
          f32.load offset=384
          f32.sub
          f32.store offset=224
          local.get $p0
          local.get $l28
          local.get $p0
          f32.load offset=376
          f32.sub
          f32.store offset=88
          local.get $p0
          local.get $l29
          local.get $p0
          f32.load offset=372
          f32.sub
          f32.store offset=84
          local.get $p0
          local.get $l30
          local.get $p0
          f32.load offset=368
          f32.sub
          f32.store offset=80
          local.get $p7
          i32.const 28
          i32.add
          local.get $p0
          i32.const 384
          i32.add
          local.get $p0
          i32.const 224
          i32.add
          local.get $p0
          i32.const 368
          i32.add
          local.get $p0
          i32.const 80
          i32.add
          local.get $p5
          local.get $p6
          call $f69959
          local.get $p7
          f32.load offset=28
          local.tee $p9
          local.get $p9
          f32.mul
          local.get $p7
          f32.load offset=32
          local.tee $l10
          local.get $l10
          f32.mul
          f32.add
          local.get $p7
          f32.load offset=36
          local.tee $l11
          local.get $l11
          f32.mul
          f32.add
          f32.sqrt
          local.tee $l12
          f32.const 0x0p+0 (;=0;)
          f32.gt
          i32.eqz
          br_if $B15
          local.get $p7
          local.get $l11
          f32.const 0x1p+0 (;=1;)
          local.get $l12
          f32.div
          local.tee $l12
          f32.mul
          f32.store offset=36
          local.get $p7
          local.get $l10
          local.get $l12
          f32.mul
          f32.store offset=32
          local.get $p7
          local.get $p9
          local.get $l12
          f32.mul
          f32.store offset=28
        end
        local.get $p7
        local.get $p6
        f32.store offset=40
        local.get $p7
        i32.const 3
        i32.store16 offset=12
      end
      local.get $l35
      i32.const -1
      i32.ne
      local.set $l34
    end
    local.get $p0
    i32.const 592
    i32.add
    global.set $g0
    block $B16
      local.get $l34
      local.tee $p4
      i32.eqz
      br_if $B16
      local.get $p7
      f32.load offset=40
      f32.const 0x0p+0 (;=0;)
      f32.eq
      br_if $B16
      local.get $p7
      local.get $p1
      f32.load offset=16
      local.get $p7
      f32.load offset=16
      f32.add
      f32.store offset=16
      local.get $p7
      i32.const 20
      i32.add
      local.tee $p0
      local.get $p1
      f32.load offset=20
      local.get $p0
      f32.load
      f32.add
      f32.store
      local.get $p7
      i32.const 24
      i32.add
      local.tee $p0
      local.get $p1
      f32.load offset=24
      local.get $p0
      f32.load
      f32.add
      f32.store
    end
    local.get $p2
    i32.const 144
    i32.add
    global.set $g0
    local.get $p4)
