  (func $f72748 (type $t32) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 i32) (param $p7 i32) (param $p8 i32) (param $p9 i32) (result i32)
    (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32) (local $l33 i32) (local $l34 i32) (local $l35 i32) (local $l36 i32) (local $l37 i64)
    global.get $g0
    i32.const 304
    i32.sub
    local.tee $p2
    global.set $g0
    local.get $p2
    local.get $p0
    i32.store offset=156
    local.get $p2
    local.get $p0
    i32.store offset=152
    local.get $p3
    local.get $p4
    i64.load offset=8
    i64.store offset=8
    local.get $p3
    local.get $p4
    i64.load
    i64.store
    local.get $p2
    i32.const 240
    i32.add
    local.get $p2
    i32.const 208
    i32.add
    local.get $p4
    local.get $p5
    local.get $p6
    call $f72749
    local.get $p5
    i32.const 20
    i32.add
    local.tee $p3
    f32.load
    local.set $l11
    local.get $p5
    f32.load offset=16
    local.set $l16
    local.get $p2
    f32.load offset=228
    local.set $l12
    local.get $p2
    f32.load offset=224
    local.set $l13
    local.get $p1
    local.get $p2
    f32.load offset=232
    local.tee $l20
    local.get $p5
    i32.const 24
    i32.add
    local.tee $p0
    f32.load
    f32.sub
    f32.store offset=8
    local.get $p1
    local.get $l12
    local.get $l11
    f32.sub
    f32.store offset=4
    local.get $p1
    local.get $l13
    local.get $l16
    f32.sub
    f32.store
    local.get $p3
    f32.load
    local.set $l11
    local.get $p5
    f32.load offset=16
    local.set $l16
    local.get $p2
    local.get $l20
    local.get $p0
    f32.load
    f32.sub
    f32.store offset=168
    local.get $p2
    local.get $l12
    local.get $l11
    f32.sub
    f32.store offset=164
    local.get $p2
    local.get $l13
    local.get $l16
    f32.sub
    f32.store offset=160
    local.get $p6
    f32.load offset=20
    local.set $l11
    local.get $p6
    f32.load offset=24
    local.set $l16
    local.get $p6
    f32.load offset=16
    local.set $l15
    local.get $p2
    local.get $l20
    f32.store offset=204
    local.get $p2
    local.get $l12
    f32.store offset=200
    local.get $p2
    local.get $p2
    f32.load offset=264
    local.tee $l21
    f32.store offset=192
    local.get $p2
    local.get $p2
    f32.load offset=260
    local.tee $l22
    f32.store offset=188
    local.get $p2
    local.get $l20
    local.get $l16
    f32.sub
    f32.store offset=180
    local.get $p2
    local.get $l12
    local.get $l11
    f32.sub
    f32.store offset=176
    local.get $p2
    local.get $l13
    f32.store offset=196
    local.get $p2
    local.get $p2
    f32.load offset=256
    local.tee $l23
    f32.store offset=184
    local.get $p2
    local.get $l13
    local.get $l15
    f32.sub
    f32.store offset=172
    local.get $p4
    i32.load offset=460
    local.set $l34
    local.get $p2
    f32.load offset=240
    local.set $l16
    block $B0
      local.get $p7
      if $I1
        local.get $p2
        f32.load offset=212
        local.set $l17
        local.get $p2
        f32.load offset=216
        local.set $l14
        local.get $p2
        f32.load offset=220
        local.set $l18
        local.get $p2
        f32.load offset=208
        local.set $l19
        local.get $p2
        f32.load offset=252
        local.set $l11
        local.get $p2
        f32.load offset=248
        local.set $l15
        local.get $p2
        f32.load offset=244
        local.set $l10
        br $B0
      end
      local.get $l16
      local.get $p2
      f32.load offset=208
      local.tee $l19
      f32.mul
      local.get $p2
      f32.load offset=244
      local.tee $l10
      local.get $p2
      f32.load offset=212
      local.tee $l17
      f32.mul
      f32.add
      local.get $p2
      f32.load offset=248
      local.tee $l15
      local.get $p2
      f32.load offset=216
      local.tee $l14
      f32.mul
      f32.add
      local.get $p2
      f32.load offset=252
      local.tee $l11
      local.get $p2
      f32.load offset=220
      local.tee $l18
      f32.mul
      f32.add
      f32.const 0x0p+0 (;=0;)
      f32.lt
      i32.eqz
      br_if $B0
      local.get $p2
      local.get $l18
      f32.neg
      local.tee $l18
      f32.store offset=220
      local.get $p2
      local.get $l14
      f32.neg
      local.tee $l14
      f32.store offset=216
      local.get $p2
      local.get $l17
      f32.neg
      local.tee $l17
      f32.store offset=212
      local.get $p2
      local.get $l19
      f32.neg
      local.tee $l19
      f32.store offset=208
    end
    local.get $p4
    i32.load offset=456
    local.set $l33
    local.get $p4
    i32.load offset=452
    local.set $p7
    local.get $p2
    local.get $l11
    local.get $l13
    local.get $l23
    f32.sub
    local.tee $l13
    local.get $l13
    f32.add
    local.tee $l13
    local.get $l10
    f32.mul
    local.get $l12
    local.get $l22
    f32.sub
    local.tee $l12
    local.get $l12
    f32.add
    local.tee $l12
    local.get $l16
    f32.mul
    f32.sub
    f32.mul
    local.get $l20
    local.get $l21
    f32.sub
    local.tee $l20
    local.get $l20
    f32.add
    local.tee $l20
    local.get $l11
    local.get $l11
    f32.mul
    f32.const -0x1p-1 (;=-0.5;)
    f32.add
    local.tee $l21
    f32.mul
    f32.add
    local.get $l15
    local.get $l12
    local.get $l10
    f32.neg
    f32.mul
    local.get $l13
    local.get $l16
    f32.mul
    f32.sub
    local.get $l20
    local.get $l15
    f32.mul
    f32.sub
    local.tee $l22
    f32.mul
    f32.sub
    f32.store offset=144
    local.get $p2
    local.get $l11
    local.get $l20
    local.get $l16
    f32.mul
    local.get $l13
    local.get $l15
    f32.mul
    f32.sub
    f32.mul
    local.get $l12
    local.get $l21
    f32.mul
    f32.add
    local.get $l10
    local.get $l22
    f32.mul
    f32.sub
    f32.store offset=140
    local.get $p2
    local.get $l15
    local.get $l14
    f32.mul
    local.get $l16
    local.get $l19
    f32.mul
    local.get $l11
    local.get $l18
    f32.mul
    f32.add
    local.get $l10
    local.get $l17
    f32.mul
    f32.add
    f32.add
    f32.store offset=132
    local.get $p2
    local.get $l10
    local.get $l19
    f32.mul
    local.get $l11
    local.get $l14
    f32.mul
    local.get $l15
    local.get $l18
    f32.mul
    f32.sub
    local.get $l16
    local.get $l17
    f32.mul
    f32.sub
    f32.add
    f32.store offset=128
    local.get $p2
    local.get $l16
    local.get $l14
    f32.mul
    local.get $l11
    local.get $l17
    f32.mul
    local.get $l10
    local.get $l18
    f32.mul
    f32.sub
    local.get $l15
    local.get $l19
    f32.mul
    f32.sub
    f32.add
    f32.store offset=124
    local.get $p2
    local.get $l11
    local.get $l19
    f32.mul
    local.get $l16
    local.get $l18
    f32.mul
    f32.sub
    local.get $l10
    local.get $l14
    f32.mul
    f32.sub
    local.get $l15
    local.get $l17
    f32.mul
    f32.add
    f32.store offset=120
    local.get $p2
    local.get $l11
    local.get $l12
    local.get $l15
    f32.mul
    local.get $l20
    local.get $l10
    f32.mul
    f32.sub
    f32.mul
    local.get $l13
    local.get $l21
    f32.mul
    f32.add
    local.get $l16
    local.get $l22
    f32.mul
    f32.sub
    f32.store offset=136
    local.get $p2
    f32.const 0x1p+0 (;=1;)
    local.get $p2
    f32.load offset=240
    local.tee $l11
    local.get $l11
    local.get $l11
    f32.add
    local.tee $l16
    f32.mul
    f32.sub
    local.tee $l13
    local.get $p2
    f32.load offset=244
    local.tee $l15
    local.get $l15
    local.get $l15
    f32.add
    local.tee $l10
    f32.mul
    local.tee $l17
    f32.sub
    f32.store offset=112
    local.get $p2
    local.get $l10
    local.get $p2
    f32.load offset=248
    local.tee $l11
    f32.mul
    local.tee $l14
    local.get $l16
    local.get $p2
    f32.load offset=252
    local.tee $l12
    f32.mul
    local.tee $l18
    f32.sub
    f32.store offset=108
    local.get $p2
    local.get $l14
    local.get $l18
    f32.add
    f32.store offset=100
    local.get $p2
    local.get $l13
    local.get $l11
    local.get $l11
    local.get $l11
    f32.add
    local.tee $l14
    f32.mul
    local.tee $l18
    f32.sub
    f32.store offset=96
    local.get $p2
    local.get $l16
    local.get $l11
    f32.mul
    local.tee $l11
    local.get $l10
    local.get $l12
    f32.mul
    local.tee $l10
    f32.add
    f32.store offset=104
    local.get $p2
    local.get $l16
    local.get $l15
    f32.mul
    local.tee $l16
    local.get $l14
    local.get $l12
    f32.mul
    local.tee $l15
    f32.sub
    f32.store offset=92
    local.get $p2
    local.get $l11
    local.get $l10
    f32.sub
    f32.store offset=88
    local.get $p2
    local.get $l16
    local.get $l15
    f32.add
    f32.store offset=84
    local.get $p2
    f32.const 0x1p+0 (;=1;)
    local.get $l17
    f32.sub
    local.get $l18
    f32.sub
    f32.store offset=80
    local.get $p2
    local.get $p2
    f32.load offset=212
    local.tee $l16
    local.get $l16
    f32.add
    local.tee $l10
    local.get $p2
    f32.load offset=216
    local.tee $l11
    f32.mul
    local.tee $l17
    local.get $p2
    f32.load offset=208
    local.tee $l12
    local.get $l12
    f32.add
    local.tee $l15
    local.get $p2
    f32.load offset=220
    local.tee $l13
    f32.mul
    local.tee $l14
    f32.sub
    f32.store offset=68
    local.get $p2
    local.get $l17
    local.get $l14
    f32.add
    f32.store offset=60
    local.get $p2
    f32.const 0x1p+0 (;=1;)
    local.get $l12
    local.get $l15
    f32.mul
    f32.sub
    local.tee $l12
    local.get $l16
    local.get $l10
    f32.mul
    local.tee $l17
    f32.sub
    f32.store offset=72
    local.get $p2
    local.get $l12
    local.get $l11
    local.get $l11
    local.get $l11
    f32.add
    local.tee $l14
    f32.mul
    local.tee $l18
    f32.sub
    f32.store offset=56
    local.get $p2
    local.get $l15
    local.get $l11
    f32.mul
    local.tee $l11
    local.get $l10
    local.get $l13
    f32.mul
    local.tee $l10
    f32.add
    f32.store offset=64
    local.get $p2
    local.get $l15
    local.get $l16
    f32.mul
    local.tee $l16
    local.get $l14
    local.get $l13
    f32.mul
    local.tee $l15
    f32.sub
    f32.store offset=52
    local.get $p2
    local.get $l11
    local.get $l10
    f32.sub
    f32.store offset=48
    local.get $p2
    local.get $l16
    local.get $l15
    f32.add
    f32.store offset=44
    local.get $p2
    f32.const 0x1p+0 (;=1;)
    local.get $l17
    f32.sub
    local.get $l18
    f32.sub
    f32.store offset=40
    local.get $l34
    i32.const 7
    i32.and
    if $I2
      local.get $p4
      i32.const 304
      i32.add
      local.set $l35
      local.get $p4
      f32.load offset=416
      local.set $l11
      local.get $p4
      f32.load offset=420
      local.set $l16
      local.get $p2
      local.get $p4
      f32.load offset=424
      local.get $p2
      f32.load offset=144
      f32.sub
      f32.store offset=8
      local.get $p2
      local.get $l16
      local.get $p2
      f32.load offset=140
      f32.sub
      f32.store offset=4
      local.get $p2
      local.get $l11
      local.get $p2
      f32.load offset=136
      f32.sub
      f32.store
      local.get $p4
      i32.const 428
      i32.add
      local.set $l36
      i32.const 0
      local.set $p0
      loop $L3
        local.get $l34
        local.get $p0
        i32.shr_u
        i32.const 1
        i32.and
        if $I4
          local.get $l36
          local.get $p0
          i32.const 2
          i32.shl
          local.tee $p3
          i32.add
          f32.load
          local.set $l17
          local.get $p2
          local.get $p2
          i32.load offset=156
          local.tee $p1
          i32.const 80
          i32.add
          i32.store offset=156
          local.get $p2
          local.get $p3
          i32.add
          f32.load
          local.set $l14
          local.get $p1
          i32.const 0
          i32.store16 offset=78
          local.get $p1
          local.get $p2
          i32.const 80
          i32.add
          local.get $p0
          i32.const 12
          i32.mul
          i32.add
          local.tee $p3
          f32.load
          f32.store
          local.get $p1
          local.get $p3
          f32.load offset=4
          f32.store offset=4
          local.get $p1
          local.get $p3
          f32.load offset=8
          f32.store offset=8
          local.get $p3
          f32.load offset=8
          local.set $l11
          local.get $p2
          f32.load offset=168
          local.set $l16
          local.get $p1
          local.get $p3
          f32.load offset=4
          local.tee $l15
          local.get $p2
          f32.load offset=160
          local.tee $l10
          f32.mul
          local.get $p2
          f32.load offset=164
          local.tee $l12
          local.get $p3
          f32.load
          local.tee $l13
          f32.mul
          f32.sub
          f32.store offset=24
          local.get $p1
          local.get $l16
          local.get $l13
          f32.mul
          local.get $l11
          local.get $l10
          f32.mul
          f32.sub
          f32.store offset=20
          local.get $p1
          local.get $l12
          local.get $l11
          f32.mul
          local.get $l16
          local.get $l15
          f32.mul
          f32.sub
          f32.store offset=16
          local.get $p1
          local.get $p3
          f32.load
          f32.store offset=32
          local.get $p1
          local.get $p3
          f32.load offset=4
          f32.store offset=36
          local.get $p1
          local.get $p3
          f32.load offset=8
          f32.store offset=40
          local.get $p3
          f32.load offset=8
          local.set $l11
          local.get $p3
          f32.load offset=4
          local.set $l16
          local.get $p3
          f32.load
          local.set $l15
          local.get $p2
          f32.load offset=180
          local.set $l10
          local.get $p2
          f32.load offset=172
          local.set $l12
          local.get $p2
          f32.load offset=176
          local.set $l13
          local.get $p1
          local.get $l17
          f32.neg
          f32.store offset=28
          local.get $p1
          local.get $l14
          f32.store offset=12
          local.get $p1
          local.get $l16
          local.get $l12
          f32.mul
          local.get $l13
          local.get $l15
          f32.mul
          f32.sub
          f32.store offset=56
          local.get $p1
          local.get $l10
          local.get $l15
          f32.mul
          local.get $l11
          local.get $l12
          f32.mul
          f32.sub
          f32.store offset=52
          local.get $p1
          local.get $l13
          local.get $l11
          f32.mul
          local.get $l10
          local.get $l16
          f32.mul
          f32.sub
          f32.store offset=48
          local.get $p1
          local.get $p1
          i32.load16_u offset=76
          i32.const 35
          i32.const 33
          local.get $l35
          local.get $p0
          i32.const 4
          i32.shl
          i32.add
          local.tee $p3
          i32.load offset=12
          i32.const 1
          i32.and
          select
          i32.or
          i32.store16 offset=76
          local.get $p1
          local.get $p3
          f32.load
          f32.store offset=64
          local.get $p1
          local.get $p3
          f32.load offset=4
          f32.store offset=68
          local.get $p1
          local.get $p3
          f32.load offset=8
          f32.neg
          f32.store offset=44
          local.get $p1
          local.get $p3
          f32.load offset=8
          f32.store offset=60
        end
        local.get $p0
        i32.const 1
        i32.add
        local.tee $p0
        i32.const 3
        i32.ne
        br_if $L3
      end
    end
    block $B5
      local.get $l34
      i32.const 56
      i32.and
      i32.eqz
      br_if $B5
      local.get $p2
      f32.load offset=120
      local.tee $l12
      local.get $p4
      f32.load offset=400
      local.tee $l11
      f32.mul
      local.tee $l20
      local.get $p2
      f32.load offset=124
      local.tee $l14
      local.get $p4
      f32.load offset=404
      local.tee $l16
      f32.mul
      local.tee $l21
      f32.add
      local.get $p2
      f32.load offset=128
      local.tee $l18
      local.get $p4
      f32.load offset=408
      local.tee $l15
      f32.mul
      local.tee $l22
      f32.add
      local.get $p2
      f32.load offset=132
      local.tee $l19
      local.get $p4
      f32.load offset=412
      local.tee $l10
      f32.mul
      local.tee $l23
      f32.add
      f32.const 0x0p+0 (;=0;)
      f32.gt
      i32.eqz
      if $I6
        local.get $l18
        local.get $l15
        f32.neg
        local.tee $l15
        f32.mul
        local.set $l22
        local.get $l14
        local.get $l16
        f32.neg
        local.tee $l16
        f32.mul
        local.set $l21
        local.get $l19
        local.get $l10
        f32.neg
        local.tee $l10
        f32.mul
        local.set $l23
        local.get $l12
        local.get $l11
        f32.neg
        local.tee $l11
        f32.mul
        local.set $l20
      end
      local.get $l12
      local.get $l16
      f32.mul
      local.get $l18
      local.get $l10
      f32.mul
      local.get $l19
      local.get $l15
      f32.mul
      f32.sub
      local.get $l14
      local.get $l11
      f32.mul
      f32.sub
      f32.add
      local.set $l13
      local.get $l18
      local.get $l11
      f32.mul
      local.get $l14
      local.get $l10
      f32.mul
      local.get $l19
      local.get $l16
      f32.mul
      f32.sub
      local.get $l12
      local.get $l15
      f32.mul
      f32.sub
      f32.add
      local.set $l17
      local.get $l14
      local.get $l15
      f32.mul
      local.get $l12
      local.get $l10
      f32.mul
      local.get $l19
      local.get $l11
      f32.mul
      f32.sub
      local.get $l18
      local.get $l16
      f32.mul
      f32.sub
      f32.add
      local.set $l12
      local.get $l34
      i32.const 32
      i32.and
      if $I7
        local.get $p4
        f32.load offset=448
        local.set $l23
        local.get $p4
        f32.load offset=440
        local.set $l21
        local.get $p4
        f32.load offset=444
        local.set $l22
        local.get $p2
        f32.load offset=252
        local.set $l14
        local.get $p2
        f32.load offset=248
        local.set $l18
        local.get $p2
        f32.load offset=240
        local.set $l19
        local.get $p2
        f32.load offset=244
        local.set $l20
        local.get $p2
        i32.const 1065353216
        i32.store offset=32
        local.get $p2
        i64.const 1065353216
        i64.store offset=16
        local.get $p2
        i64.const 0
        i64.store offset=24
        local.get $p2
        i64.const 0
        i64.store offset=8
        local.get $p2
        i64.const 1065353216
        i64.store
        local.get $l18
        local.get $l19
        local.get $l21
        local.get $l21
        f32.add
        local.tee $l21
        f32.mul
        local.get $l20
        local.get $l22
        local.get $l22
        f32.add
        local.tee $l22
        f32.mul
        f32.add
        local.get $l18
        local.get $l23
        local.get $l23
        f32.add
        local.tee $l23
        f32.mul
        f32.add
        local.tee $l24
        f32.mul
        local.set $l27
        local.get $l23
        local.get $l14
        local.get $l14
        f32.mul
        f32.const -0x1p-1 (;=-0.5;)
        f32.add
        local.tee $l25
        f32.mul
        local.get $l14
        local.get $l22
        local.get $l19
        f32.mul
        local.get $l21
        local.get $l20
        f32.mul
        f32.sub
        f32.mul
        f32.add
        local.set $l28
        local.get $l21
        local.get $l25
        f32.mul
        local.get $l14
        local.get $l23
        local.get $l20
        f32.mul
        local.get $l22
        local.get $l18
        f32.mul
        f32.sub
        f32.mul
        f32.add
        local.set $l29
        local.get $l19
        local.get $l24
        f32.mul
        local.set $l30
        local.get $l20
        local.get $l24
        f32.mul
        local.get $l22
        local.get $l25
        f32.mul
        local.get $l14
        local.get $l21
        local.get $l18
        f32.mul
        local.get $l23
        local.get $l19
        f32.mul
        f32.sub
        f32.mul
        f32.add
        f32.add
        local.set $l31
        block $B8
          local.get $p4
          f32.load offset=384
          f32.const 0x0p+0 (;=0;)
          f32.eq
          br_if $B8
          local.get $p2
          local.get $p2
          f32.load offset=212
          local.tee $l21
          local.get $l16
          local.get $l19
          f32.mul
          local.get $l15
          local.get $l14
          f32.mul
          local.get $l10
          local.get $l18
          f32.mul
          f32.add
          f32.add
          local.get $l11
          local.get $l20
          f32.mul
          f32.sub
          local.tee $l22
          f32.mul
          local.get $l16
          local.get $l14
          f32.mul
          local.get $l10
          local.get $l20
          f32.mul
          f32.add
          local.get $l11
          local.get $l18
          f32.mul
          f32.add
          local.get $l15
          local.get $l19
          f32.mul
          f32.sub
          local.tee $l23
          local.get $p2
          f32.load offset=216
          local.tee $l24
          f32.mul
          f32.add
          local.tee $l32
          local.get $p2
          f32.load offset=220
          local.tee $l25
          local.get $l11
          local.get $l14
          f32.mul
          local.get $l10
          local.get $l19
          f32.mul
          f32.add
          local.get $l15
          local.get $l20
          f32.mul
          f32.add
          local.get $l16
          local.get $l18
          f32.mul
          f32.sub
          local.tee $l26
          f32.mul
          local.get $l10
          local.get $l14
          f32.mul
          local.get $l11
          local.get $l19
          f32.mul
          f32.sub
          local.get $l16
          local.get $l20
          f32.mul
          f32.sub
          local.get $l15
          local.get $l18
          f32.mul
          f32.sub
          local.tee $l11
          local.get $p2
          f32.load offset=208
          local.tee $l16
          f32.mul
          f32.add
          local.tee $l15
          f32.sub
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          f32.store offset=28
          local.get $p2
          local.get $l25
          local.get $l23
          f32.mul
          local.get $l11
          local.get $l21
          f32.mul
          f32.add
          local.tee $l10
          local.get $l16
          local.get $l22
          f32.mul
          local.get $l26
          local.get $l24
          f32.mul
          f32.add
          local.tee $l14
          f32.add
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          f32.store offset=24
          local.get $p2
          local.get $l15
          local.get $l32
          f32.add
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          f32.store offset=20
          local.get $p2
          local.get $l16
          local.get $l23
          f32.mul
          local.get $l26
          local.get $l21
          f32.mul
          f32.add
          local.tee $l15
          local.get $l25
          local.get $l22
          f32.mul
          local.get $l11
          local.get $l24
          f32.mul
          f32.add
          local.tee $l18
          f32.sub
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          f32.store offset=12
          local.get $p2
          local.get $l14
          local.get $l10
          f32.sub
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          f32.store offset=8
          local.get $p2
          local.get $l15
          local.get $l18
          f32.add
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          f32.store offset=4
          local.get $p2
          local.get $l22
          local.get $l24
          f32.mul
          local.tee $l15
          local.get $l15
          f32.add
          local.get $l25
          local.get $l11
          f32.mul
          local.tee $l10
          local.get $l26
          local.get $l16
          f32.mul
          local.tee $l11
          local.get $l23
          local.get $l21
          f32.mul
          local.tee $l16
          f32.add
          local.get $l15
          f32.add
          local.tee $l14
          f32.sub
          local.tee $l15
          f32.add
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          local.tee $l18
          f32.store offset=32
          local.get $p2
          local.get $l16
          local.get $l16
          f32.add
          local.get $l15
          f32.add
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          local.tee $l16
          f32.store offset=16
          local.get $p2
          local.get $l11
          local.get $l11
          f32.add
          local.get $l15
          f32.add
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          local.tee $l11
          f32.store
          local.get $l10
          local.get $l14
          f32.add
          f32.const 0x0p+0 (;=0;)
          f32.ne
          br_if $B8
          local.get $p2
          local.get $l18
          f32.const 0x1p-23 (;=1.19209e-07;)
          f32.add
          f32.store offset=32
          local.get $p2
          local.get $l16
          f32.const 0x1p-23 (;=1.19209e-07;)
          f32.add
          f32.store offset=16
          local.get $p2
          local.get $l11
          f32.const 0x1p-23 (;=1.19209e-07;)
          f32.add
          f32.store
        end
        local.get $l28
        local.get $l27
        f32.add
        local.set $l14
        local.get $l30
        local.get $l29
        f32.add
        local.set $l18
        local.get $l31
        f32.neg
        local.set $l19
        i32.const 0
        local.set $p3
        loop $L9
          local.get $p7
          local.get $p3
          i32.shr_u
          i32.const 8
          i32.and
          i32.eqz
          if $I10
            local.get $p2
            local.get $p3
            i32.const 12
            i32.mul
            i32.add
            local.tee $p1
            f32.load
            local.set $l11
            local.get $p1
            f32.load offset=4
            local.set $l16
            local.get $p1
            f32.load offset=8
            local.set $l15
            local.get $p2
            local.get $l13
            f32.store offset=296
            local.get $p2
            local.get $l17
            f32.store offset=292
            local.get $p2
            local.get $l12
            f32.store offset=288
            local.get $p2
            local.get $p2
            i32.load offset=156
            local.tee $p1
            i32.const 80
            i32.add
            i32.store offset=156
            local.get $p2
            i32.const 288
            i32.add
            local.get $p3
            i32.const 2
            i32.shl
            i32.add
            f32.load
            local.set $l10
            local.get $p1
            i64.const 0
            i64.store align=4
            local.get $p1
            local.get $l15
            f32.store offset=56
            local.get $p1
            local.get $l16
            f32.store offset=52
            local.get $p1
            local.get $l11
            f32.store offset=48
            local.get $p1
            i32.const 0
            i32.store offset=40
            local.get $p1
            i64.const 0
            i64.store offset=32 align=4
            local.get $p1
            local.get $l15
            f32.store offset=24
            local.get $p1
            local.get $l16
            f32.store offset=20
            local.get $p1
            local.get $l11
            f32.store offset=16
            local.get $p1
            i32.const 0
            i32.store offset=8
            local.get $p1
            i32.const 258
            i32.store16 offset=78
            local.get $p1
            local.get $l16
            local.get $l19
            f32.mul
            local.get $l18
            local.get $l11
            f32.mul
            f32.sub
            local.get $l14
            local.get $l15
            f32.mul
            f32.sub
            f32.store offset=28
            local.get $p1
            local.get $p1
            i32.load16_u offset=76
            i32.const 64
            i32.or
            local.tee $p0
            i32.store16 offset=76
            local.get $p1
            local.get $l10
            f32.neg
            f32.store offset=12
            local.get $p1
            i32.const 35
            i32.const 33
            local.get $p4
            i32.load offset=396
            i32.const 1
            i32.and
            select
            local.get $p0
            i32.or
            i32.store16 offset=76
            local.get $p1
            local.get $p4
            f32.load offset=384
            f32.store offset=64
            local.get $p1
            local.get $p4
            f32.load offset=388
            f32.store offset=68
            local.get $p1
            local.get $p4
            f32.load offset=392
            f32.neg
            f32.store offset=44
            local.get $p1
            local.get $p4
            f32.load offset=392
            f32.store offset=60
          end
          local.get $p3
          i32.const 1
          i32.add
          local.tee $p3
          i32.const 3
          i32.ne
          br_if $L9
        end
        br $B5
      end
      local.get $l34
      i32.const 16
      i32.and
      if $I11
        local.get $p4
        f32.load offset=440
        local.set $l11
        local.get $p2
        local.get $p2
        i32.load offset=156
        local.tee $p1
        i32.const 80
        i32.add
        i32.store offset=156
        local.get $p1
        i32.const 0
        i32.store offset=8
        local.get $p1
        i64.const 0
        i64.store align=4
        local.get $p1
        i32.const 0
        i32.store16 offset=78
        local.get $p1
        local.get $p2
        f32.load offset=40
        local.tee $l16
        f32.store offset=16
        local.get $p1
        local.get $p2
        f32.load offset=44
        local.tee $l15
        f32.store offset=20
        local.get $p1
        local.get $p2
        f32.load offset=48
        local.tee $l10
        f32.store offset=56
        local.get $p1
        local.get $l15
        f32.store offset=52
        local.get $p1
        local.get $l16
        f32.store offset=48
        local.get $p1
        i32.const 0
        i32.store offset=40
        local.get $p1
        i64.const 0
        i64.store offset=32 align=4
        local.get $p1
        local.get $l10
        f32.store offset=24
        local.get $p1
        local.get $l12
        f32.const -0x1p+1 (;=-2;)
        f32.mul
        f32.store offset=12
        local.get $p1
        local.get $p1
        i32.load16_u offset=76
        i32.const 64
        i32.or
        local.tee $p3
        i32.store16 offset=76
        local.get $p1
        local.get $l11
        f32.store offset=28
        local.get $p1
        i32.const 35
        i32.const 33
        local.get $p4
        i32.load offset=380
        i32.const 1
        i32.and
        select
        local.get $p3
        i32.or
        i32.store16 offset=76
        local.get $p1
        local.get $p4
        f32.load offset=368
        f32.store offset=64
        local.get $p1
        local.get $p4
        f32.load offset=372
        f32.store offset=68
        local.get $p1
        local.get $p4
        f32.load offset=376
        f32.neg
        f32.store offset=44
        local.get $p1
        local.get $p4
        f32.load offset=376
        f32.store offset=60
      end
      local.get $l34
      i32.const 8
      i32.and
      i32.eqz
      br_if $B5
      local.get $l12
      f32.const 0x0p+0 (;=0;)
      f32.mul
      local.set $l16
      local.get $l22
      local.get $l21
      local.get $l20
      local.get $l23
      f32.add
      f32.add
      f32.add
      local.tee $l11
      local.get $l11
      f32.mul
      f32.const -0x1p-1 (;=-0.5;)
      f32.add
      f32.const 0x0p+0 (;=0;)
      f32.mul
      local.set $l15
      local.get $l13
      f32.const 0x0p+0 (;=0;)
      f32.mul
      local.get $l12
      local.get $l12
      f32.add
      local.get $l17
      f32.const 0x0p+0 (;=0;)
      f32.mul
      f32.add
      f32.add
      local.set $l10
      local.get $p7
      i32.const 16
      i32.and
      i32.eqz
      if $I12
        local.get $p4
        f32.load offset=444
        local.set $l12
        local.get $p2
        local.get $p2
        i32.load offset=156
        local.tee $p1
        i32.const 80
        i32.add
        i32.store offset=156
        local.get $p1
        i32.const 0
        i32.store offset=8
        local.get $p1
        i64.const 0
        i64.store align=4
        local.get $p1
        i32.const 0
        i32.store16 offset=78
        local.get $p1
        local.get $p2
        f32.load offset=52
        local.tee $l14
        f32.store offset=16
        local.get $p1
        local.get $p2
        f32.load offset=56
        local.tee $l18
        f32.store offset=20
        local.get $p1
        local.get $p2
        f32.load offset=60
        local.tee $l19
        f32.store offset=56
        local.get $p1
        local.get $l18
        f32.store offset=52
        local.get $p1
        local.get $l14
        f32.store offset=48
        local.get $p1
        i32.const 0
        i32.store offset=40
        local.get $p1
        i64.const 0
        i64.store offset=32 align=4
        local.get $p1
        local.get $l19
        f32.store offset=24
        local.get $p1
        local.get $l15
        local.get $l11
        local.get $l16
        local.get $l17
        local.get $l17
        f32.add
        f32.sub
        f32.mul
        f32.add
        local.get $l13
        local.get $l10
        f32.mul
        f32.add
        f32.store offset=12
        local.get $p1
        local.get $p1
        i32.load16_u offset=76
        i32.const 64
        i32.or
        local.tee $p3
        i32.store16 offset=76
        local.get $p1
        local.get $l12
        f32.store offset=28
        local.get $p1
        i32.const 35
        i32.const 33
        local.get $p4
        i32.load offset=364
        i32.const 1
        i32.and
        select
        local.get $p3
        i32.or
        i32.store16 offset=76
        local.get $p1
        local.get $p4
        f32.load offset=352
        f32.store offset=64
        local.get $p1
        local.get $p4
        f32.load offset=356
        f32.store offset=68
        local.get $p1
        local.get $p4
        f32.load offset=360
        f32.neg
        f32.store offset=44
        local.get $p1
        local.get $p4
        f32.load offset=360
        f32.store offset=60
      end
      local.get $p7
      i32.const 32
      i32.and
      br_if $B5
      local.get $p4
      f32.load offset=448
      local.set $l12
      local.get $p2
      local.get $p2
      i32.load offset=156
      local.tee $p1
      i32.const 80
      i32.add
      i32.store offset=156
      local.get $p1
      i32.const 0
      i32.store offset=8
      local.get $p1
      i64.const 0
      i64.store align=4
      local.get $p1
      i32.const 0
      i32.store16 offset=78
      local.get $p1
      local.get $p2
      f32.load offset=64
      f32.store offset=16
      local.get $p1
      local.get $p2
      i32.const 68
      i32.add
      local.tee $p3
      f32.load
      f32.store offset=20
      local.get $p2
      i32.const 72
      i32.add
      local.tee $p0
      f32.load
      local.set $l14
      local.get $p1
      i32.const 0
      i32.store offset=40
      local.get $p1
      i64.const 0
      i64.store offset=32 align=4
      local.get $p1
      local.get $l14
      f32.store offset=24
      local.get $p1
      local.get $p2
      f32.load offset=64
      f32.store offset=48
      local.get $p1
      local.get $p3
      f32.load
      f32.store offset=52
      local.get $p0
      f32.load
      local.set $l14
      local.get $p1
      local.get $l17
      local.get $l10
      f32.mul
      local.get $l15
      local.get $l11
      local.get $l13
      local.get $l13
      f32.add
      local.get $l16
      f32.sub
      f32.mul
      f32.add
      f32.add
      f32.neg
      f32.store offset=12
      local.get $p1
      local.get $l14
      f32.store offset=56
      local.get $p1
      local.get $l12
      f32.store offset=28
      local.get $p1
      local.get $p1
      i32.load16_u offset=76
      i32.const 64
      i32.or
      local.tee $p3
      i32.store16 offset=76
      local.get $p1
      i32.const 35
      i32.const 33
      local.get $p4
      i32.load offset=364
      i32.const 1
      i32.and
      select
      local.get $p3
      i32.or
      i32.store16 offset=76
      local.get $p1
      local.get $p4
      f32.load offset=352
      f32.store offset=64
      local.get $p1
      local.get $p4
      f32.load offset=356
      f32.store offset=68
      local.get $p1
      local.get $p4
      f32.load offset=360
      f32.neg
      f32.store offset=44
      local.get $p1
      local.get $p4
      f32.load offset=360
      f32.store offset=60
    end
    block $B13
      local.get $l33
      i32.const 56
      i32.and
      i32.eqz
      br_if $B13
      f32.const 0x0p+0 (;=0;)
      local.set $l11
      local.get $p2
      f32.load offset=132
      local.set $l10
      block $B14
        local.get $p2
        f32.load offset=120
        local.tee $l12
        f32.const 0x0p+0 (;=0;)
        f32.eq
        if $I15
          f32.const 0x1p+0 (;=1;)
          local.set $l16
          f32.const 0x0p+0 (;=0;)
          local.set $l15
          br $B14
        end
        local.get $l10
        f32.const 0x1p+0 (;=1;)
        local.get $l12
        local.get $l12
        f32.mul
        f32.const 0x0p+0 (;=0;)
        f32.add
        local.get $l10
        local.get $l10
        f32.mul
        f32.add
        f32.sqrt
        f32.div
        local.tee $l11
        f32.mul
        local.set $l16
        local.get $l11
        f32.const 0x0p+0 (;=0;)
        f32.mul
        local.set $l15
        local.get $l12
        local.get $l11
        f32.mul
        local.set $l11
      end
      local.get $p2
      local.get $l12
      local.get $l11
      f32.mul
      local.get $l16
      local.get $l10
      f32.mul
      f32.add
      local.get $l15
      local.get $p2
      f32.load offset=124
      local.tee $l13
      f32.mul
      local.tee $l14
      f32.add
      local.get $l15
      local.get $p2
      f32.load offset=128
      local.tee $l17
      f32.mul
      local.tee $l18
      f32.add
      local.tee $l21
      f32.store offset=12
      local.get $p2
      local.get $l11
      local.get $l13
      f32.mul
      local.get $l16
      local.get $l17
      f32.mul
      local.get $l15
      local.get $l10
      f32.mul
      local.tee $l19
      f32.sub
      local.get $l12
      local.get $l15
      f32.mul
      local.tee $l20
      f32.sub
      f32.add
      local.tee $l22
      f32.store offset=8
      local.get $p2
      local.get $l20
      local.get $l16
      local.get $l13
      f32.mul
      local.get $l19
      f32.sub
      local.get $l11
      local.get $l17
      f32.mul
      f32.sub
      f32.add
      local.tee $l13
      f32.store offset=4
      local.get $p2
      local.get $l12
      local.get $l16
      f32.mul
      local.get $l11
      local.get $l10
      f32.mul
      f32.sub
      local.get $l14
      f32.sub
      local.get $l18
      f32.add
      local.tee $l10
      f32.store
      block $B16
        local.get $l33
        i32.const 48
        i32.and
        i32.const 48
        i32.eq
        if $I17
          block $B18
            local.get $p4
            i32.load8_u offset=478
            i32.eqz
            br_if $B18
            f32.const 0x0p+0 (;=0;)
            local.set $l10
            block $B19
              local.get $p4
              f32.load offset=252
              f32.const 0x0p+0 (;=0;)
              f32.gt
              br_if $B19
              local.get $p4
              f32.load offset=248
              f32.const 0x0p+0 (;=0;)
              f32.gt
              br_if $B19
              local.get $p4
              f32.load offset=256
              local.set $l10
            end
            local.get $p4
            i64.load offset=260 align=4
            local.set $l37
            local.get $p2
            local.get $l10
            f32.store offset=280
            local.get $p2
            local.get $l37
            i64.store offset=272
            local.get $p2
            i32.const 288
            i32.add
            local.set $p3
            local.get $p2
            i32.const 284
            i32.add
            local.set $l34
            local.get $p2
            f32.load
            local.set $l10
            local.get $p2
            f32.load offset=4
            local.tee $l19
            local.get $p2
            f32.load offset=12
            local.tee $l12
            f32.const 0x1p+0 (;=1;)
            f32.add
            local.tee $l13
            call $f35884
            f32.const 0x1p+2 (;=4;)
            f32.mul
            local.tee $l25
            f32.abs
            local.tee $l18
            local.get $p2
            i32.const 272
            i32.add
            local.tee $p1
            f32.load offset=8
            local.tee $l14
            f32.add
            local.get $p1
            f32.load
            local.tee $l22
            f32.div
            local.tee $l21
            local.get $l21
            f32.mul
            local.get $l14
            local.get $p2
            f32.load offset=8
            local.tee $l21
            local.get $l13
            call $f35884
            f32.const 0x1p+2 (;=4;)
            f32.mul
            local.tee $l26
            f32.abs
            local.tee $l17
            f32.add
            local.get $p1
            f32.load offset=4
            local.tee $l20
            f32.div
            local.tee $l13
            local.get $l13
            f32.mul
            f32.add
            f32.const 0x1p+0 (;=1;)
            f32.le
            local.tee $p1
            i32.eqz
            if $I20
              local.get $l10
              local.get $l10
              f32.add
              local.tee $l13
              local.get $l21
              f32.mul
              local.get $l12
              local.get $l12
              f32.add
              local.tee $l14
              local.get $l19
              f32.mul
              f32.sub
              local.set $l27
              local.get $l21
              local.get $l14
              f32.mul
              local.get $l13
              local.get $l19
              f32.mul
              f32.add
              local.set $l28
              local.get $l10
              local.get $l13
              f32.mul
              local.get $l12
              local.get $l14
              f32.mul
              f32.const -0x1p+0 (;=-1;)
              f32.add
              f32.add
              local.set $l29
              local.get $p3
              f32.const 0x1p+0 (;=1;)
              block $B21 (result f32)
                block $B22
                  local.get $l20
                  local.get $l22
                  f32.le
                  if $I23
                    local.get $l17
                    f32.const 0x1.0c6f7ap-20 (;=1e-06;)
                    f32.lt
                    i32.eqz
                    br_if $B22
                    f32.const 0x0p+0 (;=0;)
                    local.set $l17
                    local.get $l22
                    local.get $l22
                    f32.neg
                    local.get $l25
                    f32.const 0x0p+0 (;=0;)
                    f32.gt
                    select
                    br $B21
                  end
                  local.get $l18
                  f32.const 0x1.0c6f7ap-20 (;=1e-06;)
                  f32.lt
                  i32.eqz
                  br_if $B22
                  local.get $l20
                  local.get $l20
                  f32.neg
                  local.get $l26
                  f32.const 0x0p+0 (;=0;)
                  f32.gt
                  select
                  local.set $l17
                  f32.const 0x0p+0 (;=0;)
                  br $B21
                end
                local.get $l18
                local.get $l22
                f32.mul
                local.tee $l23
                local.get $l22
                local.get $l22
                f32.mul
                local.tee $l18
                f32.sub
                local.tee $l10
                local.get $l17
                local.get $l20
                f32.mul
                local.tee $l24
                local.get $l20
                local.get $l20
                f32.mul
                local.tee $l17
                f32.sub
                local.tee $l12
                local.get $l10
                local.get $l12
                f32.gt
                select
                local.set $l10
                i32.const 0
                local.set $p0
                block $B24
                  loop $L25
                    local.get $l23
                    f32.const 0x1p+0 (;=1;)
                    local.get $l18
                    local.get $l10
                    f32.add
                    f32.div
                    local.tee $l12
                    f32.mul
                    local.tee $l13
                    local.get $l13
                    f32.mul
                    local.tee $l21
                    local.get $l24
                    f32.const 0x1p+0 (;=1;)
                    local.get $l17
                    local.get $l10
                    f32.add
                    f32.div
                    local.tee $l13
                    f32.mul
                    local.tee $l14
                    local.get $l14
                    f32.mul
                    local.tee $l14
                    f32.add
                    f32.const -0x1p+0 (;=-1;)
                    f32.add
                    local.tee $l19
                    f32.const 0x1.a36e2ep-14 (;=0.0001;)
                    f32.lt
                    br_if $B24
                    local.get $l10
                    local.get $l19
                    local.get $l13
                    local.get $l14
                    f32.mul
                    local.get $l12
                    local.get $l21
                    f32.mul
                    f32.const 0x0p+0 (;=0;)
                    f32.add
                    f32.add
                    local.tee $l14
                    local.get $l14
                    f32.add
                    f32.div
                    f32.add
                    local.set $l10
                    local.get $p0
                    i32.const 1
                    i32.add
                    local.tee $p0
                    i32.const 20
                    i32.ne
                    br_if $L25
                  end
                  local.get $l26
                  local.get $l17
                  f32.mul
                  local.get $l13
                  f32.mul
                  local.tee $l10
                  f32.const 0x1p+0 (;=1;)
                  local.get $l25
                  local.get $l18
                  f32.mul
                  local.get $l12
                  f32.mul
                  local.tee $l12
                  local.get $l22
                  f32.div
                  local.tee $l13
                  local.get $l13
                  f32.mul
                  local.get $l10
                  local.get $l20
                  f32.div
                  local.tee $l10
                  local.get $l10
                  f32.mul
                  f32.add
                  f32.sqrt
                  f32.div
                  local.tee $l10
                  f32.mul
                  local.set $l17
                  local.get $l12
                  local.get $l10
                  f32.mul
                  br $B21
                end
                local.get $l26
                local.get $l17
                f32.mul
                local.get $l13
                f32.mul
                local.set $l17
                local.get $l25
                local.get $l18
                f32.mul
                local.get $l12
                f32.mul
              end
              local.tee $l23
              f32.const 0x1p-2 (;=0.25;)
              f32.mul
              call $f18177
              local.tee $l13
              local.get $l13
              f32.mul
              f32.const 0x0p+0 (;=0;)
              f32.add
              local.get $l17
              f32.const 0x1p-2 (;=0.25;)
              f32.mul
              call $f18177
              local.tee $l12
              local.get $l12
              f32.mul
              f32.add
              local.tee $l19
              f32.sub
              local.tee $l14
              local.get $l14
              local.get $l14
              f32.add
              f32.const 0x1p+0 (;=1;)
              local.get $l19
              f32.const 0x1p+0 (;=1;)
              f32.add
              f32.div
              local.tee $l18
              local.get $l18
              f32.mul
              local.tee $l24
              f32.mul
              local.tee $l10
              f32.mul
              f32.const -0x1p+0 (;=-1;)
              f32.add
              local.tee $l21
              local.get $l17
              local.get $l20
              local.get $l20
              f32.mul
              f32.div
              local.tee $l17
              local.get $l17
              f32.add
              local.get $l10
              f32.mul
              local.get $l12
              local.get $l12
              f32.add
              local.tee $l20
              local.get $l18
              f32.const 0x1.8p+1 (;=3;)
              local.get $l19
              f32.sub
              local.get $l13
              local.get $l23
              local.get $l22
              local.get $l22
              f32.mul
              f32.div
              local.tee $l23
              f32.mul
              f32.const 0x0p+0 (;=0;)
              f32.add
              local.get $l17
              local.get $l12
              f32.mul
              f32.add
              local.tee $l17
              f32.const -0x1p+2 (;=-4;)
              f32.mul
              f32.mul
              local.get $l24
              f32.mul
              f32.mul
              local.tee $l18
              f32.mul
              f32.add
              local.tee $l12
              f32.mul
              local.get $l20
              local.get $l10
              f32.mul
              local.tee $l19
              local.get $l14
              local.get $l18
              f32.mul
              local.get $l17
              local.get $l17
              f32.add
              local.get $l10
              f32.mul
              f32.sub
              local.tee $l14
              f32.mul
              f32.sub
              f32.const 0x1p+0 (;=1;)
              local.get $l13
              f32.const -0x1p+1 (;=-2;)
              f32.mul
              local.tee $l24
              local.get $l18
              f32.mul
              local.get $l23
              local.get $l23
              f32.add
              local.get $l10
              f32.mul
              f32.sub
              local.tee $l13
              local.get $l13
              f32.mul
              local.get $l14
              local.get $l14
              f32.mul
              local.get $l12
              local.get $l12
              f32.mul
              f32.add
              f32.add
              f32.sqrt
              f32.div
              local.tee $l18
              f32.mul
              local.tee $l17
              f32.store offset=8
              local.get $p3
              local.get $l24
              local.get $l10
              f32.mul
              local.tee $l10
              local.get $l14
              f32.mul
              local.get $l21
              local.get $l13
              f32.mul
              f32.sub
              local.get $l18
              f32.mul
              local.tee $l14
              f32.store offset=4
              local.get $p3
              local.get $l19
              local.get $l13
              f32.mul
              local.get $l10
              local.get $l12
              f32.mul
              f32.sub
              local.get $l18
              f32.mul
              local.tee $l12
              f32.store
              local.get $l34
              local.get $l27
              local.get $l21
              local.get $l14
              f32.mul
              local.get $l19
              local.get $l12
              f32.mul
              f32.sub
              f32.mul
              local.get $l29
              local.get $l19
              local.get $l17
              f32.mul
              local.get $l10
              local.get $l14
              f32.mul
              f32.sub
              f32.mul
              local.get $l28
              local.get $l10
              local.get $l12
              f32.mul
              local.get $l21
              local.get $l17
              f32.mul
              f32.sub
              f32.mul
              f32.add
              f32.add
              f32.store
            end
            local.get $p1
            i32.const 1
            i32.xor
            i32.eqz
            br_if $B18
            local.get $p2
            local.get $p2
            i32.load offset=156
            local.tee $p1
            i32.const 80
            i32.add
            i32.store offset=156
            local.get $p2
            f32.load offset=252
            local.set $l10
            local.get $p2
            f32.load offset=248
            local.set $l12
            local.get $p2
            f32.load offset=296
            local.set $l14
            local.get $p2
            f32.load offset=240
            local.set $l13
            local.get $p2
            f32.load offset=288
            local.set $l19
            local.get $p2
            f32.load offset=244
            local.set $l17
            local.get $p2
            f32.load offset=292
            local.set $l18
            local.get $p2
            f32.load offset=284
            local.set $l22
            local.get $p1
            i32.const 0
            i32.store offset=40
            local.get $p1
            i64.const 0
            i64.store offset=32 align=4
            local.get $p1
            i32.const 0
            i32.store offset=8
            local.get $p1
            i64.const 0
            i64.store align=4
            local.get $p1
            i32.const 0
            i32.store16 offset=78
            local.get $p1
            local.get $l22
            f32.store offset=12
            local.get $p1
            local.get $p1
            i32.load16_u offset=76
            local.tee $p3
            i32.const 64
            i32.or
            local.tee $p0
            i32.store16 offset=76
            local.get $p1
            local.get $l14
            local.get $l14
            f32.add
            local.tee $l14
            local.get $l10
            local.get $l10
            f32.mul
            f32.const -0x1p-1 (;=-0.5;)
            f32.add
            local.tee $l20
            f32.mul
            local.get $l10
            local.get $l13
            local.get $l18
            local.get $l18
            f32.add
            local.tee $l18
            f32.mul
            local.get $l17
            local.get $l19
            local.get $l19
            f32.add
            local.tee $l19
            f32.mul
            f32.sub
            f32.mul
            f32.add
            local.get $l12
            local.get $l19
            local.get $l13
            f32.mul
            local.get $l18
            local.get $l17
            f32.mul
            f32.add
            local.get $l14
            local.get $l12
            f32.mul
            f32.add
            local.tee $l21
            f32.mul
            f32.add
            local.tee $l23
            f32.store offset=56
            local.get $p1
            local.get $l17
            local.get $l21
            f32.mul
            local.get $l18
            local.get $l20
            f32.mul
            local.get $l10
            local.get $l19
            local.get $l12
            f32.mul
            local.get $l14
            local.get $l13
            f32.mul
            f32.sub
            f32.mul
            f32.add
            f32.add
            local.tee $l24
            f32.store offset=52
            local.get $p1
            local.get $l13
            local.get $l21
            f32.mul
            local.get $l19
            local.get $l20
            f32.mul
            local.get $l10
            local.get $l14
            local.get $l17
            f32.mul
            local.get $l18
            local.get $l12
            f32.mul
            f32.sub
            f32.mul
            f32.add
            f32.add
            local.tee $l10
            f32.store offset=48
            local.get $p1
            local.get $l23
            f32.store offset=24
            local.get $p1
            local.get $l24
            f32.store offset=20
            local.get $p1
            local.get $l10
            f32.store offset=16
            block $B26 (result i32)
              local.get $p4
              f32.load offset=252
              f32.const 0x0p+0 (;=0;)
              f32.gt
              local.get $p4
              f32.load offset=248
              local.tee $l10
              f32.const 0x0p+0 (;=0;)
              f32.gt
              i32.or
              if $I27
                local.get $p1
                local.get $l10
                f32.store offset=64
                local.get $p1
                local.get $p4
                f32.load offset=252
                f32.store offset=68
                local.get $p3
                i32.const 81
                i32.or
                br $B26
              end
              local.get $p1
              i32.const 2049
              i32.store16 offset=78
              local.get $p1
              local.get $p4
              f32.load offset=240
              f32.store offset=64
              local.get $p1
              local.get $p4
              f32.load offset=244
              f32.store offset=68
              local.get $p0
              i32.const 24
              i32.const 16
              local.get $l22
              f32.const 0x0p+0 (;=0;)
              f32.gt
              select
              i32.or
              local.tee $p3
              local.get $p4
              f32.load offset=240
              f32.const 0x0p+0 (;=0;)
              f32.gt
              i32.eqz
              br_if $B26
              drop
              local.get $p3
              i32.const 4
              i32.or
            end
            local.set $p3
            local.get $p1
            i32.const 0
            i32.store offset=44
            local.get $p1
            local.get $p3
            i32.store16 offset=76
          end
          local.get $p4
          i32.load8_u offset=479
          i32.eqz
          br_if $B16
          global.get $g0
          i32.const 16
          i32.sub
          local.tee $p0
          global.set $g0
          local.get $p2
          i32.const 240
          i32.add
          local.tee $p1
          f32.load offset=12
          local.tee $l10
          local.get $p2
          f32.load offset=12
          local.tee $l14
          f32.mul
          local.get $p2
          f32.load
          local.tee $l12
          local.get $p1
          f32.load
          local.tee $l13
          f32.mul
          f32.sub
          local.get $p1
          f32.load offset=4
          local.tee $l17
          local.get $p2
          f32.load offset=4
          local.tee $l18
          f32.mul
          f32.sub
          local.get $p2
          f32.load offset=8
          local.tee $l19
          local.get $p1
          f32.load offset=8
          local.tee $l20
          f32.mul
          f32.sub
          local.set $l21
          local.get $l13
          local.get $l18
          f32.mul
          local.get $l10
          local.get $l19
          f32.mul
          local.get $l14
          local.get $l20
          f32.mul
          f32.add
          f32.add
          local.get $l12
          local.get $l17
          f32.mul
          f32.sub
          local.set $l22
          local.get $l14
          local.get $l17
          f32.mul
          local.get $l10
          local.get $l18
          f32.mul
          f32.add
          local.get $l12
          local.get $l20
          f32.mul
          f32.add
          local.get $l13
          local.get $l19
          f32.mul
          f32.sub
          local.set $l23
          local.get $l10
          local.get $l12
          f32.mul
          local.get $l14
          local.get $l13
          f32.mul
          f32.add
          local.get $l17
          local.get $l19
          f32.mul
          f32.add
          local.get $l18
          local.get $l20
          f32.mul
          f32.sub
          local.set $l10
          local.get $p4
          f32.load offset=284
          local.set $l17
          local.get $p4
          f32.load offset=292
          local.set $l19
          local.get $p4
          f32.load offset=288
          local.set $l20
          local.get $p0
          local.get $l10
          local.get $l21
          local.get $l21
          f32.add
          local.tee $l12
          f32.mul
          local.get $l23
          local.get $l23
          f32.add
          local.tee $l13
          local.get $l22
          f32.mul
          f32.add
          f32.store offset=8
          local.get $p0
          local.get $l23
          local.get $l13
          f32.mul
          local.get $l21
          local.get $l12
          f32.mul
          f32.const -0x1p+0 (;=-1;)
          f32.add
          f32.add
          f32.store offset=4
          local.get $p0
          local.get $l10
          local.get $l13
          f32.mul
          local.get $l12
          local.get $l22
          f32.mul
          f32.sub
          f32.store
          local.get $p2
          i32.const 152
          i32.add
          local.tee $p3
          local.get $l18
          local.get $l14
          f32.const 0x1p+0 (;=1;)
          f32.add
          call $f35884
          f32.const 0x1p+2 (;=4;)
          f32.mul
          local.get $l20
          local.get $l19
          local.get $l17
          local.get $p0
          local.get $p4
          i32.const 268
          i32.add
          local.tee $p1
          call $f72750
          local.get $p2
          f32.load offset=12
          local.set $l12
          local.get $p2
          f32.load offset=8
          local.set $l13
          local.get $p4
          f32.load offset=284
          local.set $l17
          local.get $p4
          f32.load offset=300
          local.set $l19
          local.get $p4
          f32.load offset=296
          local.set $l20
          local.get $p0
          local.get $l21
          local.get $l21
          local.get $l21
          f32.add
          local.tee $l14
          f32.mul
          f32.const -0x1p+0 (;=-1;)
          f32.add
          local.get $l22
          local.get $l22
          local.get $l22
          f32.add
          local.tee $l18
          f32.mul
          f32.add
          f32.store offset=8
          local.get $p0
          local.get $l23
          local.get $l18
          f32.mul
          local.get $l10
          local.get $l14
          f32.mul
          f32.sub
          f32.store offset=4
          local.get $p0
          local.get $l23
          local.get $l14
          f32.mul
          local.get $l10
          local.get $l18
          f32.mul
          f32.add
          f32.store
          local.get $p3
          local.get $l13
          local.get $l12
          f32.const 0x1p+0 (;=1;)
          f32.add
          call $f35884
          f32.const 0x1p+2 (;=4;)
          f32.mul
          local.get $l20
          local.get $l19
          local.get $l17
          local.get $p0
          local.get $p1
          call $f72750
          local.get $p0
          i32.const 16
          i32.add
          global.set $g0
          br $B16
        end
        local.get $l33
        i32.const 32
        i32.and
        local.set $p1
        block $B28
          local.get $l33
          i32.const 16
          i32.and
          i32.eqz
          br_if $B28
          local.get $p4
          i32.load8_u offset=479
          local.set $p3
          local.get $p7
          i32.const 32
          i32.and
          if $I29
            local.get $p3
            i32.const 255
            i32.and
            if $I30
              local.get $p4
              f32.load offset=284
              local.set $l25
              local.get $p4
              f32.load offset=292
              local.set $l26
              local.get $p4
              f32.load offset=288
              local.set $l27
              local.get $p2
              local.get $l10
              local.get $p2
              f32.load offset=252
              local.tee $l12
              f32.mul
              local.get $l21
              local.get $p2
              f32.load offset=240
              local.tee $l17
              f32.mul
              f32.add
              local.get $l22
              local.get $p2
              f32.load offset=244
              local.tee $l14
              f32.mul
              f32.add
              local.get $l13
              local.get $p2
              f32.load offset=248
              local.tee $l18
              f32.mul
              f32.sub
              local.tee $l28
              local.get $l21
              local.get $l12
              f32.mul
              local.get $l10
              local.get $l17
              f32.mul
              f32.sub
              local.get $l13
              local.get $l14
              f32.mul
              f32.sub
              local.get $l22
              local.get $l18
              f32.mul
              f32.sub
              local.tee $l19
              local.get $l19
              f32.add
              local.tee $l20
              f32.mul
              local.get $l13
              local.get $l12
              f32.mul
              local.get $l21
              local.get $l14
              f32.mul
              f32.add
              local.get $l10
              local.get $l18
              f32.mul
              f32.add
              local.get $l22
              local.get $l17
              f32.mul
              f32.sub
              local.tee $l23
              local.get $l23
              f32.add
              local.tee $l24
              local.get $l13
              local.get $l17
              f32.mul
              local.get $l22
              local.get $l12
              f32.mul
              local.get $l21
              local.get $l18
              f32.mul
              f32.add
              f32.add
              local.get $l10
              local.get $l14
              f32.mul
              f32.sub
              local.tee $l10
              f32.mul
              f32.add
              f32.store offset=296
              local.get $p2
              local.get $l28
              local.get $l24
              f32.mul
              local.get $l20
              local.get $l10
              f32.mul
              f32.sub
              f32.store offset=288
              local.get $p2
              local.get $l23
              local.get $l24
              f32.mul
              local.get $l19
              local.get $l20
              f32.mul
              f32.const -0x1p+0 (;=-1;)
              f32.add
              f32.add
              f32.store offset=292
              local.get $p2
              i32.const 152
              i32.add
              local.get $l13
              local.get $l21
              f32.const 0x1p+0 (;=1;)
              f32.add
              call $f35884
              f32.const 0x1p+2 (;=4;)
              f32.mul
              local.get $l27
              local.get $l26
              local.get $l25
              local.get $p2
              i32.const 288
              i32.add
              local.get $p4
              i32.const 268
              i32.add
              call $f72750
              br $B28
            end
            local.get $p2
            i32.const 152
            i32.add
            local.get $l13
            local.get $l21
            f32.const 0x1p+0 (;=1;)
            f32.add
            call $f35884
            f32.const 0x1p+2 (;=4;)
            f32.mul
            local.get $p4
            f32.load offset=260
            local.tee $l10
            f32.neg
            local.get $l10
            local.get $p4
            f32.load offset=256
            local.get $p2
            i32.const 92
            i32.add
            local.get $p4
            i32.const 240
            i32.add
            call $f72750
            br $B28
          end
          local.get $p3
          i32.const 255
          i32.and
          i32.eqz
          if $I31
            f32.const 0x0p+0 (;=0;)
            local.set $l20
            local.get $p2
            f32.load offset=48
            local.tee $l10
            local.get $p2
            f32.load offset=112
            local.tee $l12
            f32.mul
            local.get $p2
            f32.load offset=108
            local.tee $l13
            local.get $p2
            f32.load offset=44
            local.tee $l17
            f32.mul
            local.get $p2
            f32.load offset=40
            local.tee $l14
            local.get $p2
            f32.load offset=104
            local.tee $l18
            f32.mul
            f32.add
            f32.add
            f32.neg
            f32.const -0x1p+0 (;=-1;)
            f32.max
            local.set $l24
            local.get $p4
            f32.load offset=256
            local.set $l25
            local.get $p4
            f32.load offset=260
            local.set $l19
            f32.const 0x0p+0 (;=0;)
            local.set $l21
            f32.const 0x0p+0 (;=0;)
            local.set $l22
            local.get $l17
            local.get $l18
            f32.mul
            local.get $l13
            local.get $l14
            f32.mul
            f32.sub
            local.tee $l23
            local.get $l23
            f32.mul
            local.get $l13
            local.get $l10
            f32.mul
            local.get $l12
            local.get $l17
            f32.mul
            f32.sub
            local.tee $l13
            local.get $l13
            f32.mul
            local.get $l12
            local.get $l14
            f32.mul
            local.get $l10
            local.get $l18
            f32.mul
            f32.sub
            local.tee $l10
            local.get $l10
            f32.mul
            f32.add
            f32.add
            local.tee $l12
            f32.const 0x0p+0 (;=0;)
            f32.gt
            if $I32
              local.get $l23
              f32.const 0x1p+0 (;=1;)
              local.get $l12
              f32.sqrt
              f32.div
              local.tee $l12
              f32.mul
              local.set $l22
              local.get $l10
              local.get $l12
              f32.mul
              local.set $l21
              local.get $l13
              local.get $l12
              f32.mul
              local.set $l20
            end
            local.get $p2
            local.get $l22
            f32.store offset=296
            local.get $p2
            local.get $l21
            f32.store offset=292
            local.get $p2
            local.get $l20
            f32.store offset=288
            local.get $p2
            i32.const 152
            i32.add
            local.get $l24
            f32.const 0x1p+0 (;=1;)
            f32.min
            call $f65711
            local.get $l19
            f32.neg
            local.get $l19
            local.get $l25
            local.get $p2
            i32.const 288
            i32.add
            local.get $p4
            i32.const 240
            i32.add
            call $f72750
            br $B28
          end
          i32.const 4700888
          i32.load
          i32.const 8
          i32.const 3208342
          i32.const 1016
          i32.const 3209479
          i32.const 0
          call $f69760
        end
        local.get $p1
        i32.eqz
        br_if $B16
        local.get $p4
        i32.load8_u offset=479
        local.set $p1
        local.get $p7
        i32.const 16
        i32.and
        if $I33
          local.get $p1
          i32.const 255
          i32.and
          if $I34
            local.get $p4
            f32.load offset=284
            local.set $l23
            local.get $p4
            f32.load offset=300
            local.set $l24
            local.get $p4
            f32.load offset=296
            local.set $l25
            local.get $p2
            local.get $p2
            f32.load offset=12
            local.tee $l10
            local.get $p2
            f32.load offset=244
            local.tee $l13
            f32.mul
            local.get $p2
            f32.load offset=252
            local.tee $l17
            local.get $p2
            f32.load offset=4
            local.tee $l14
            f32.mul
            f32.add
            local.get $p2
            f32.load
            local.tee $l18
            local.get $p2
            f32.load offset=248
            local.tee $l19
            f32.mul
            f32.add
            local.get $p2
            f32.load offset=240
            local.tee $l20
            local.get $p2
            f32.load offset=8
            local.tee $l12
            f32.mul
            f32.sub
            local.tee $l26
            local.get $l20
            local.get $l14
            f32.mul
            local.get $l17
            local.get $l12
            f32.mul
            local.get $l10
            local.get $l19
            f32.mul
            f32.add
            f32.add
            local.get $l18
            local.get $l13
            f32.mul
            f32.sub
            local.tee $l21
            local.get $l21
            f32.add
            local.tee $l22
            f32.mul
            local.get $l17
            local.get $l18
            f32.mul
            local.get $l10
            local.get $l20
            f32.mul
            f32.add
            local.get $l13
            local.get $l12
            f32.mul
            f32.add
            local.get $l14
            local.get $l19
            f32.mul
            f32.sub
            local.tee $l27
            local.get $l17
            local.get $l10
            f32.mul
            local.get $l18
            local.get $l20
            f32.mul
            f32.sub
            local.get $l13
            local.get $l14
            f32.mul
            f32.sub
            local.get $l12
            local.get $l19
            f32.mul
            f32.sub
            local.tee $l13
            local.get $l13
            f32.add
            local.tee $l17
            f32.mul
            f32.sub
            f32.store offset=292
            local.get $p2
            local.get $l26
            local.get $l17
            f32.mul
            local.get $l27
            local.get $l22
            f32.mul
            f32.add
            f32.store offset=288
            local.get $p2
            local.get $l13
            local.get $l17
            f32.mul
            f32.const -0x1p+0 (;=-1;)
            f32.add
            local.get $l21
            local.get $l22
            f32.mul
            f32.add
            f32.store offset=296
            local.get $p2
            i32.const 152
            i32.add
            local.get $l12
            local.get $l10
            f32.const 0x1p+0 (;=1;)
            f32.add
            call $f35884
            f32.const 0x1p+2 (;=4;)
            f32.mul
            local.get $l25
            local.get $l24
            local.get $l23
            local.get $p2
            i32.const 288
            i32.add
            local.get $p4
            i32.const 268
            i32.add
            call $f72750
            br $B16
          end
          local.get $p2
          i32.const 152
          i32.add
          local.get $p2
          f32.load offset=8
          local.get $p2
          f32.load offset=12
          f32.const 0x1p+0 (;=1;)
          f32.add
          call $f35884
          f32.const 0x1p+2 (;=4;)
          f32.mul
          local.get $p4
          f32.load offset=264
          local.tee $l10
          f32.neg
          local.get $l10
          local.get $p4
          f32.load offset=256
          local.get $p2
          i32.const 104
          i32.add
          local.get $p4
          i32.const 240
          i32.add
          call $f72750
          br $B16
        end
        local.get $p1
        i32.const 255
        i32.and
        i32.eqz
        if $I35
          f32.const 0x0p+0 (;=0;)
          local.set $l20
          local.get $p2
          f32.load offset=48
          local.tee $l10
          local.get $p2
          f32.load offset=100
          local.tee $l12
          f32.mul
          local.get $p2
          f32.load offset=96
          local.tee $l13
          local.get $p2
          f32.load offset=44
          local.tee $l17
          f32.mul
          local.get $p2
          f32.load offset=40
          local.tee $l14
          local.get $p2
          f32.load offset=92
          local.tee $l18
          f32.mul
          f32.add
          f32.add
          f32.const -0x1p+0 (;=-1;)
          f32.max
          local.set $l24
          local.get $p4
          f32.load offset=256
          local.set $l25
          local.get $p4
          f32.load offset=264
          local.set $l19
          f32.const 0x0p+0 (;=0;)
          local.set $l21
          f32.const 0x0p+0 (;=0;)
          local.set $l22
          local.get $l17
          local.get $l18
          f32.mul
          local.get $l13
          local.get $l14
          f32.mul
          f32.sub
          local.tee $l23
          local.get $l23
          f32.mul
          local.get $l13
          local.get $l10
          f32.mul
          local.get $l12
          local.get $l17
          f32.mul
          f32.sub
          local.tee $l13
          local.get $l13
          f32.mul
          local.get $l12
          local.get $l14
          f32.mul
          local.get $l10
          local.get $l18
          f32.mul
          f32.sub
          local.tee $l10
          local.get $l10
          f32.mul
          f32.add
          f32.add
          local.tee $l12
          f32.const 0x0p+0 (;=0;)
          f32.gt
          if $I36
            f32.const 0x1p+0 (;=1;)
            local.get $l12
            f32.sqrt
            f32.div
            local.tee $l12
            local.get $l23
            f32.neg
            f32.mul
            local.set $l22
            local.get $l12
            local.get $l10
            f32.neg
            f32.mul
            local.set $l21
            local.get $l12
            local.get $l13
            f32.neg
            f32.mul
            local.set $l20
          end
          local.get $p2
          local.get $l22
          f32.store offset=296
          local.get $p2
          local.get $l21
          f32.store offset=292
          local.get $p2
          local.get $l20
          f32.store offset=288
          local.get $p2
          i32.const 152
          i32.add
          local.get $l24
          f32.const 0x1p+0 (;=1;)
          f32.min
          call $f65711
          local.get $l19
          f32.neg
          local.get $l19
          local.get $l25
          local.get $p2
          i32.const 288
          i32.add
          local.get $p4
          i32.const 240
          i32.add
          call $f72750
          br $B16
        end
        i32.const 4700888
        i32.load
        i32.const 8
        i32.const 3208342
        i32.const 1032
        i32.const 3209479
        i32.const 0
        call $f69760
      end
      local.get $l33
      i32.const 8
      i32.and
      i32.eqz
      br_if $B13
      local.get $l16
      local.get $l16
      f32.mul
      local.get $l15
      local.get $l15
      f32.mul
      local.tee $l15
      local.get $l15
      local.get $l11
      local.get $l11
      f32.mul
      f32.add
      f32.add
      f32.add
      f32.sqrt
      local.tee $l15
      f32.const 0x0p+0 (;=0;)
      f32.ne
      if $I37
        local.get $l16
        f32.const 0x1p+0 (;=1;)
        local.get $l15
        f32.div
        local.tee $l15
        f32.mul
        local.set $l16
        local.get $l11
        local.get $l15
        f32.mul
        local.set $l11
      end
      local.get $p2
      i32.const 152
      i32.add
      local.get $l16
      f32.const -0x1p+0 (;=-1;)
      f32.max
      f32.const 0x1p+0 (;=1;)
      f32.min
      call $f35882
      local.tee $l16
      local.get $l16
      f32.add
      local.tee $l16
      f32.neg
      local.get $l16
      local.get $l11
      f32.const 0x0p+0 (;=0;)
      f32.lt
      select
      local.get $p4
      f32.load offset=236
      local.get $p4
      f32.load offset=232
      local.get $p4
      f32.load offset=228
      local.get $p2
      i32.const 40
      i32.add
      local.get $p4
      i32.const 212
      i32.add
      call $f72750
    end
    block $B38
      local.get $l33
      i32.const 7
      i32.and
      i32.eqz
      br_if $B38
      block $B39
        local.get $p4
        i32.load8_u offset=476
        i32.eqz
        br_if $B39
        f32.const 0x0p+0 (;=0;)
        local.set $l11
        f32.const 0x0p+0 (;=0;)
        local.set $l16
        f32.const 0x0p+0 (;=0;)
        local.set $l15
        local.get $p4
        i32.load offset=456
        local.tee $p1
        i32.const 1
        i32.and
        if $I40
          local.get $p2
          f32.load offset=136
          local.tee $l11
          local.get $p2
          f32.load offset=88
          f32.mul
          f32.const 0x0p+0 (;=0;)
          f32.add
          local.set $l15
          local.get $l11
          local.get $p2
          f32.load offset=84
          f32.mul
          f32.const 0x0p+0 (;=0;)
          f32.add
          local.set $l16
          local.get $l11
          local.get $p2
          f32.load offset=80
          f32.mul
          f32.const 0x0p+0 (;=0;)
          f32.add
          local.set $l11
        end
        local.get $p1
        i32.const 2
        i32.and
        if $I41
          local.get $l11
          local.get $p2
          f32.load offset=140
          local.tee $l10
          local.get $p2
          f32.load offset=92
          f32.mul
          f32.add
          local.set $l11
          local.get $l16
          local.get $l10
          local.get $p2
          f32.load offset=96
          f32.mul
          f32.add
          local.set $l16
          local.get $l15
          local.get $l10
          local.get $p2
          f32.load offset=100
          f32.mul
          f32.add
          local.set $l15
        end
        local.get $p1
        i32.const 4
        i32.and
        if $I42
          local.get $l11
          local.get $p2
          f32.load offset=144
          local.tee $l10
          local.get $p2
          f32.load offset=104
          f32.mul
          f32.add
          local.set $l11
          local.get $l16
          local.get $l10
          local.get $p2
          f32.load offset=108
          f32.mul
          f32.add
          local.set $l16
          local.get $l15
          local.get $l10
          local.get $p2
          f32.load offset=112
          f32.mul
          f32.add
          local.set $l15
        end
        local.get $l11
        local.get $l11
        f32.mul
        local.get $l16
        local.get $l16
        f32.mul
        f32.add
        local.get $l15
        local.get $l15
        f32.mul
        f32.add
        f32.sqrt
        local.tee $l10
        local.get $p4
        f32.load offset=464
        f32.gt
        i32.eqz
        br_if $B39
        f32.const 0x0p+0 (;=0;)
        local.set $l13
        local.get $p4
        f32.load offset=124
        local.set $l12
        block $B43
          local.get $p4
          f32.load offset=116
          f32.const 0x0p+0 (;=0;)
          f32.gt
          br_if $B43
          local.get $p4
          f32.load offset=112
          f32.const 0x0p+0 (;=0;)
          f32.gt
          br_if $B43
          local.get $p4
          f32.load offset=120
          local.set $l13
        end
        local.get $l10
        local.get $l13
        f32.add
        local.get $l12
        f32.gt
        i32.eqz
        br_if $B39
        local.get $p2
        local.get $p2
        i32.load offset=156
        local.tee $p1
        i32.const 80
        i32.add
        i32.store offset=156
        local.get $p1
        local.get $l15
        f32.const 0x1p+0 (;=1;)
        local.get $l10
        f32.div
        local.tee $l13
        f32.mul
        local.tee $l15
        f32.store offset=8
        local.get $p1
        local.get $l16
        local.get $l13
        f32.mul
        local.tee $l16
        f32.store offset=4
        local.get $p1
        local.get $l11
        local.get $l13
        f32.mul
        local.tee $l11
        f32.store
        local.get $p1
        i32.const 0
        i32.store16 offset=78
        local.get $p2
        f32.load offset=168
        local.set $l13
        local.get $p2
        f32.load offset=160
        local.set $l17
        local.get $p2
        f32.load offset=164
        local.set $l14
        local.get $p1
        local.get $l15
        f32.store offset=40
        local.get $p1
        local.get $l16
        f32.store offset=36
        local.get $p1
        local.get $l11
        f32.store offset=32
        local.get $p1
        local.get $l16
        local.get $l17
        f32.mul
        local.get $l11
        local.get $l14
        f32.mul
        f32.sub
        f32.store offset=24
        local.get $p1
        local.get $l11
        local.get $l13
        f32.mul
        local.get $l15
        local.get $l17
        f32.mul
        f32.sub
        f32.store offset=20
        local.get $p1
        local.get $l15
        local.get $l14
        f32.mul
        local.get $l16
        local.get $l13
        f32.mul
        f32.sub
        f32.store offset=16
        local.get $p2
        f32.load offset=180
        local.set $l13
        local.get $p2
        f32.load offset=172
        local.set $l17
        local.get $p2
        f32.load offset=176
        local.set $l14
        local.get $p1
        local.get $l12
        local.get $l10
        f32.sub
        local.tee $l10
        f32.store offset=12
        local.get $p1
        local.get $l16
        local.get $l17
        f32.mul
        local.get $l11
        local.get $l14
        f32.mul
        f32.sub
        f32.store offset=56
        local.get $p1
        local.get $l11
        local.get $l13
        f32.mul
        local.get $l15
        local.get $l17
        f32.mul
        f32.sub
        f32.store offset=52
        local.get $p1
        local.get $l15
        local.get $l14
        f32.mul
        local.get $l16
        local.get $l13
        f32.mul
        f32.sub
        f32.store offset=48
        local.get $p1
        i32.load16_u offset=76
        local.set $p3
        block $B44 (result i32)
          local.get $p4
          f32.load offset=116
          f32.const 0x0p+0 (;=0;)
          f32.gt
          local.get $p4
          f32.load offset=112
          local.tee $l11
          f32.const 0x0p+0 (;=0;)
          f32.gt
          i32.or
          if $I45
            local.get $p1
            local.get $l11
            f32.store offset=64
            local.get $p1
            local.get $p4
            f32.load offset=116
            f32.store offset=68
            local.get $p3
            i32.const 17
            i32.or
            br $B44
          end
          local.get $p1
          i32.const 2049
          i32.store16 offset=78
          local.get $p1
          local.get $p4
          f32.load offset=104
          f32.store offset=64
          local.get $p1
          local.get $p4
          f32.load offset=108
          f32.store offset=68
          local.get $p3
          i32.const 24
          i32.const 16
          local.get $l10
          f32.const 0x0p+0 (;=0;)
          f32.gt
          select
          i32.or
          local.tee $p3
          local.get $p4
          f32.load offset=104
          f32.const 0x0p+0 (;=0;)
          f32.gt
          i32.eqz
          br_if $B44
          drop
          local.get $p3
          i32.const 4
          i32.or
        end
        local.set $p3
        local.get $p1
        i32.const 0
        i32.store offset=44
        local.get $p1
        local.get $p3
        i32.store16 offset=76
      end
      local.get $p4
      i32.load8_u offset=477
      i32.eqz
      br_if $B38
      block $B46
        local.get $l33
        i32.const 1
        i32.and
        i32.eqz
        br_if $B46
        local.get $p4
        f32.load offset=152
        local.tee $l10
        local.get $p4
        f32.load offset=148
        local.tee $l13
        f32.le
        i32.eqz
        br_if $B46
        f32.const 0x0p+0 (;=0;)
        local.set $l11
        local.get $p2
        f32.load offset=136
        local.set $l12
        block $B47
          local.get $p4
          f32.load offset=140
          local.tee $l17
          f32.const 0x0p+0 (;=0;)
          f32.gt
          br_if $B47
          local.get $p4
          f32.load offset=136
          f32.const 0x0p+0 (;=0;)
          f32.gt
          br_if $B47
          local.get $p4
          f32.load offset=144
          local.set $l11
        end
        block $B48
          local.get $l12
          local.get $l11
          f32.add
          local.get $l13
          f32.gt
          i32.eqz
          if $I49
            local.get $p2
            f32.load offset=88
            local.set $l15
            local.get $p2
            f32.load offset=84
            local.set $l11
            local.get $p2
            f32.load offset=80
            local.set $l16
            br $B48
          end
          local.get $p2
          local.get $p2
          i32.load offset=156
          local.tee $p1
          i32.const 80
          i32.add
          i32.store offset=156
          local.get $p1
          i32.const 0
          i32.store16 offset=78
          local.get $p1
          local.get $p2
          f32.load offset=80
          f32.store
          local.get $p1
          local.get $p2
          f32.load offset=84
          f32.store offset=4
          local.get $p1
          local.get $p2
          f32.load offset=88
          f32.store offset=8
          local.get $p2
          f32.load offset=168
          local.set $l10
          local.get $p2
          f32.load offset=160
          local.set $l17
          local.get $p2
          f32.load offset=164
          local.set $l14
          local.get $p2
          f32.load offset=80
          local.set $l16
          local.get $p2
          f32.load offset=84
          local.set $l11
          local.get $p1
          local.get $p2
          f32.load offset=88
          local.tee $l15
          f32.store offset=40
          local.get $p1
          local.get $l11
          f32.store offset=36
          local.get $p1
          local.get $l16
          f32.store offset=32
          local.get $p1
          local.get $l11
          local.get $l17
          f32.mul
          local.get $l14
          local.get $l16
          f32.mul
          f32.sub
          f32.store offset=24
          local.get $p1
          local.get $l10
          local.get $l16
          f32.mul
          local.get $l15
          local.get $l17
          f32.mul
          f32.sub
          f32.store offset=20
          local.get $p1
          local.get $l14
          local.get $l15
          f32.mul
          local.get $l10
          local.get $l11
          f32.mul
          f32.sub
          f32.store offset=16
          local.get $p2
          f32.load offset=180
          local.set $l10
          local.get $p2
          f32.load offset=172
          local.set $l17
          local.get $p2
          f32.load offset=176
          local.set $l14
          local.get $p1
          local.get $l13
          local.get $l12
          f32.sub
          local.tee $l13
          f32.store offset=12
          local.get $p1
          local.get $l11
          local.get $l17
          f32.mul
          local.get $l16
          local.get $l14
          f32.mul
          f32.sub
          f32.store offset=56
          local.get $p1
          local.get $l16
          local.get $l10
          f32.mul
          local.get $l15
          local.get $l17
          f32.mul
          f32.sub
          f32.store offset=52
          local.get $p1
          local.get $l15
          local.get $l14
          f32.mul
          local.get $l11
          local.get $l10
          f32.mul
          f32.sub
          f32.store offset=48
          local.get $p1
          i32.load16_u offset=76
          local.set $p3
          block $B50 (result i32)
            local.get $p4
            f32.load offset=140
            f32.const 0x0p+0 (;=0;)
            f32.gt
            local.get $p4
            f32.load offset=136
            local.tee $l10
            f32.const 0x0p+0 (;=0;)
            f32.gt
            i32.or
            if $I51
              local.get $p1
              local.get $l10
              f32.store offset=64
              local.get $p1
              local.get $p4
              f32.load offset=140
              f32.store offset=68
              local.get $p3
              i32.const 17
              i32.or
              br $B50
            end
            local.get $p1
            i32.const 2049
            i32.store16 offset=78
            local.get $p1
            local.get $p4
            f32.load offset=128
            f32.store offset=64
            local.get $p1
            local.get $p4
            f32.load offset=132
            f32.store offset=68
            local.get $p3
            i32.const 24
            i32.const 16
            local.get $l13
            f32.const 0x0p+0 (;=0;)
            f32.gt
            select
            i32.or
            local.tee $p3
            local.get $p4
            f32.load offset=128
            f32.const 0x0p+0 (;=0;)
            f32.gt
            i32.eqz
            br_if $B50
            drop
            local.get $p3
            i32.const 4
            i32.or
          end
          local.set $p3
          local.get $p1
          i32.const 0
          i32.store offset=44
          local.get $p1
          local.get $p3
          i32.store16 offset=76
          local.get $p4
          f32.load offset=140
          local.set $l17
          local.get $p4
          f32.load offset=152
          local.set $l10
        end
        f32.const 0x0p+0 (;=0;)
        local.set $l13
        local.get $l10
        f32.neg
        local.set $l14
        block $B52
          local.get $l17
          f32.const 0x0p+0 (;=0;)
          f32.gt
          br_if $B52
          local.get $p4
          f32.load offset=136
          f32.const 0x0p+0 (;=0;)
          f32.gt
          br_if $B52
          local.get $p4
          f32.load offset=144
          local.set $l13
        end
        local.get $l13
        local.get $l12
        f32.sub
        local.get $l14
        f32.gt
        i32.eqz
        br_if $B46
        local.get $p2
        local.get $p2
        i32.load offset=156
        local.tee $p1
        i32.const 80
        i32.add
        i32.store offset=156
        local.get $p1
        local.get $l15
        f32.neg
        local.tee $l18
        f32.store offset=8
        local.get $p1
        local.get $l11
        f32.neg
        local.tee $l19
        f32.store offset=4
        local.get $p1
        local.get $l16
        f32.neg
        local.tee $l20
        f32.store
        local.get $p1
        i32.const 0
        i32.store16 offset=78
        local.get $p2
        f32.load offset=168
        local.set $l13
        local.get $p2
        f32.load offset=164
        local.set $l17
        local.get $p2
        f32.load offset=160
        local.set $l14
        local.get $p1
        local.get $l18
        f32.store offset=40
        local.get $p1
        local.get $l19
        f32.store offset=36
        local.get $p1
        local.get $l20
        f32.store offset=32
        local.get $p1
        local.get $l16
        local.get $l17
        f32.mul
        local.get $l11
        local.get $l14
        f32.mul
        f32.sub
        f32.store offset=24
        local.get $p1
        local.get $l15
        local.get $l14
        f32.mul
        local.get $l16
        local.get $l13
        f32.mul
        f32.sub
        f32.store offset=20
        local.get $p1
        local.get $l11
        local.get $l13
        f32.mul
        local.get $l15
        local.get $l17
        f32.mul
        f32.sub
        f32.store offset=16
        local.get $p2
        f32.load offset=180
        local.set $l13
        local.get $p2
        f32.load offset=176
        local.set $l17
        local.get $p2
        f32.load offset=172
        local.set $l14
        local.get $p1
        local.get $l12
        local.get $l10
        f32.sub
        local.tee $l10
        f32.store offset=12
        local.get $p1
        local.get $l16
        local.get $l17
        f32.mul
        local.get $l11
        local.get $l14
        f32.mul
        f32.sub
        f32.store offset=56
        local.get $p1
        local.get $l15
        local.get $l14
        f32.mul
        local.get $l16
        local.get $l13
        f32.mul
        f32.sub
        f32.store offset=52
        local.get $p1
        local.get $l11
        local.get $l13
        f32.mul
        local.get $l15
        local.get $l17
        f32.mul
        f32.sub
        f32.store offset=48
        local.get $p1
        i32.load16_u offset=76
        local.set $p3
        block $B53 (result i32)
          local.get $p4
          f32.load offset=140
          f32.const 0x0p+0 (;=0;)
          f32.gt
          local.get $p4
          f32.load offset=136
          local.tee $l11
          f32.const 0x0p+0 (;=0;)
          f32.gt
          i32.or
          if $I54
            local.get $p1
            local.get $l11
            f32.store offset=64
            local.get $p1
            local.get $p4
            f32.load offset=140
            f32.store offset=68
            local.get $p3
            i32.const 17
            i32.or
            br $B53
          end
          local.get $p1
          i32.const 2049
          i32.store16 offset=78
          local.get $p1
          local.get $p4
          f32.load offset=128
          f32.store offset=64
          local.get $p1
          local.get $p4
          f32.load offset=132
          f32.store offset=68
          local.get $p3
          i32.const 24
          i32.const 16
          local.get $l10
          f32.const 0x0p+0 (;=0;)
          f32.gt
          select
          i32.or
          local.tee $p3
          local.get $p4
          f32.load offset=128
          f32.const 0x0p+0 (;=0;)
          f32.gt
          i32.eqz
          br_if $B53
          drop
          local.get $p3
          i32.const 4
          i32.or
        end
        local.set $p3
        local.get $p1
        i32.const 0
        i32.store offset=44
        local.get $p1
        local.get $p3
        i32.store16 offset=76
      end
      block $B55
        local.get $l33
        i32.const 2
        i32.and
        i32.eqz
        br_if $B55
        local.get $p4
        f32.load offset=180
        local.tee $l11
        local.get $p4
        f32.load offset=176
        local.tee $l15
        f32.le
        i32.eqz
        br_if $B55
        f32.const 0x0p+0 (;=0;)
        local.set $l12
        local.get $p2
        f32.load offset=140
        local.set $l16
        block $B56
          local.get $p4
          f32.load offset=168
          local.tee $l10
          f32.const 0x0p+0 (;=0;)
          f32.gt
          br_if $B56
          local.get $p4
          f32.load offset=164
          f32.const 0x0p+0 (;=0;)
          f32.gt
          br_if $B56
          local.get $p4
          f32.load offset=172
          local.set $l12
        end
        local.get $l15
        local.get $l16
        local.get $l12
        f32.add
        f32.lt
        if $I57
          local.get $p2
          local.get $p2
          i32.load offset=156
          local.tee $p1
          i32.const 80
          i32.add
          i32.store offset=156
          local.get $p1
          i32.const 0
          i32.store16 offset=78
          local.get $p1
          local.get $p2
          f32.load offset=92
          f32.store
          local.get $p1
          local.get $p2
          f32.load offset=96
          f32.store offset=4
          local.get $p1
          local.get $p2
          f32.load offset=100
          f32.store offset=8
          local.get $p2
          f32.load offset=168
          local.set $l10
          local.get $p2
          f32.load offset=100
          local.set $l12
          local.get $p2
          f32.load offset=160
          local.set $l13
          local.get $p2
          f32.load offset=96
          local.set $l17
          local.get $p2
          f32.load offset=164
          local.set $l14
          local.get $p1
          local.get $p2
          f32.load offset=92
          local.tee $l11
          f32.store offset=32
          local.get $p1
          local.get $l17
          local.get $l13
          f32.mul
          local.get $l14
          local.get $l11
          f32.mul
          f32.sub
          f32.store offset=24
          local.get $p1
          local.get $l10
          local.get $l11
          f32.mul
          local.get $l12
          local.get $l13
          f32.mul
          f32.sub
          f32.store offset=20
          local.get $p1
          local.get $l14
          local.get $l12
          f32.mul
          local.get $l10
          local.get $l17
          f32.mul
          f32.sub
          f32.store offset=16
          local.get $p1
          local.get $p2
          f32.load offset=96
          local.tee $l10
          f32.store offset=36
          local.get $p1
          local.get $p2
          f32.load offset=100
          local.tee $l12
          f32.store offset=40
          local.get $p2
          f32.load offset=180
          local.set $l13
          local.get $p2
          f32.load offset=172
          local.set $l17
          local.get $p2
          f32.load offset=176
          local.set $l14
          local.get $p1
          local.get $l15
          local.get $l16
          f32.sub
          local.tee $l15
          f32.store offset=12
          local.get $p1
          local.get $l10
          local.get $l17
          f32.mul
          local.get $l11
          local.get $l14
          f32.mul
          f32.sub
          f32.store offset=56
          local.get $p1
          local.get $l11
          local.get $l13
          f32.mul
          local.get $l12
          local.get $l17
          f32.mul
          f32.sub
          f32.store offset=52
          local.get $p1
          local.get $l12
          local.get $l14
          f32.mul
          local.get $l10
          local.get $l13
          f32.mul
          f32.sub
          f32.store offset=48
          local.get $p1
          i32.load16_u offset=76
          local.set $p3
          block $B58 (result i32)
            local.get $p4
            f32.load offset=168
            f32.const 0x0p+0 (;=0;)
            f32.gt
            local.get $p4
            f32.load offset=164
            local.tee $l11
            f32.const 0x0p+0 (;=0;)
            f32.gt
            i32.or
            if $I59
              local.get $p1
              local.get $l11
              f32.store offset=64
              local.get $p1
              local.get $p4
              f32.load offset=168
              f32.store offset=68
              local.get $p3
              i32.const 17
              i32.or
              br $B58
            end
            local.get $p1
            i32.const 2049
            i32.store16 offset=78
            local.get $p1
            local.get $p4
            f32.load offset=156
            f32.store offset=64
            local.get $p1
            local.get $p4
            f32.load offset=160
            f32.store offset=68
            local.get $p3
            i32.const 24
            i32.const 16
            local.get $l15
            f32.const 0x0p+0 (;=0;)
            f32.gt
            select
            i32.or
            local.tee $p3
            local.get $p4
            f32.load offset=156
            f32.const 0x0p+0 (;=0;)
            f32.gt
            i32.eqz
            br_if $B58
            drop
            local.get $p3
            i32.const 4
            i32.or
          end
          local.set $p3
          local.get $p1
          i32.const 0
          i32.store offset=44
          local.get $p1
          local.get $p3
          i32.store16 offset=76
          local.get $p4
          f32.load offset=168
          local.set $l10
          local.get $p4
          f32.load offset=180
          local.set $l11
        end
        f32.const 0x0p+0 (;=0;)
        local.set $l15
        local.get $l11
        f32.neg
        local.set $l12
        block $B60
          local.get $l10
          f32.const 0x0p+0 (;=0;)
          f32.gt
          br_if $B60
          local.get $p4
          f32.load offset=164
          f32.const 0x0p+0 (;=0;)
          f32.gt
          br_if $B60
          local.get $p4
          f32.load offset=172
          local.set $l15
        end
        local.get $l15
        local.get $l16
        f32.sub
        local.get $l12
        f32.gt
        i32.eqz
        br_if $B55
        local.get $p2
        f32.load offset=100
        local.set $l15
        local.get $p2
        f32.load offset=96
        local.set $l10
        local.get $p2
        f32.load offset=92
        local.set $l12
        local.get $p2
        local.get $p2
        i32.load offset=156
        local.tee $p1
        i32.const 80
        i32.add
        i32.store offset=156
        local.get $p1
        local.get $l15
        f32.neg
        local.tee $l18
        f32.store offset=8
        local.get $p1
        local.get $l10
        f32.neg
        local.tee $l19
        f32.store offset=4
        local.get $p1
        local.get $l12
        f32.neg
        local.tee $l20
        f32.store
        local.get $p1
        i32.const 0
        i32.store16 offset=78
        local.get $p2
        f32.load offset=168
        local.set $l13
        local.get $p2
        f32.load offset=164
        local.set $l17
        local.get $p2
        f32.load offset=160
        local.set $l14
        local.get $p1
        local.get $l18
        f32.store offset=40
        local.get $p1
        local.get $l19
        f32.store offset=36
        local.get $p1
        local.get $l20
        f32.store offset=32
        local.get $p1
        local.get $l12
        local.get $l17
        f32.mul
        local.get $l10
        local.get $l14
        f32.mul
        f32.sub
        f32.store offset=24
        local.get $p1
        local.get $l15
        local.get $l14
        f32.mul
        local.get $l12
        local.get $l13
        f32.mul
        f32.sub
        f32.store offset=20
        local.get $p1
        local.get $l10
        local.get $l13
        f32.mul
        local.get $l15
        local.get $l17
        f32.mul
        f32.sub
        f32.store offset=16
        local.get $p2
        f32.load offset=180
        local.set $l13
        local.get $p2
        f32.load offset=176
        local.set $l17
        local.get $p2
        f32.load offset=172
        local.set $l14
        local.get $p1
        local.get $l16
        local.get $l11
        f32.sub
        local.tee $l16
        f32.store offset=12
        local.get $p1
        local.get $l12
        local.get $l17
        f32.mul
        local.get $l10
        local.get $l14
        f32.mul
        f32.sub
        f32.store offset=56
        local.get $p1
        local.get $l15
        local.get $l14
        f32.mul
        local.get $l12
        local.get $l13
        f32.mul
        f32.sub
        f32.store offset=52
        local.get $p1
        local.get $l10
        local.get $l13
        f32.mul
        local.get $l15
        local.get $l17
        f32.mul
        f32.sub
        f32.store offset=48
        local.get $p1
        i32.load16_u offset=76
        local.set $p3
        block $B61 (result i32)
          local.get $p4
          f32.load offset=168
          f32.const 0x0p+0 (;=0;)
          f32.gt
          local.get $p4
          f32.load offset=164
          local.tee $l11
          f32.const 0x0p+0 (;=0;)
          f32.gt
          i32.or
          if $I62
            local.get $p1
            local.get $l11
            f32.store offset=64
            local.get $p1
            local.get $p4
            f32.load offset=168
            f32.store offset=68
            local.get $p3
            i32.const 17
            i32.or
            br $B61
          end
          local.get $p1
          i32.const 2049
          i32.store16 offset=78
          local.get $p1
          local.get $p4
          f32.load offset=156
          f32.store offset=64
          local.get $p1
          local.get $p4
          f32.load offset=160
          f32.store offset=68
          local.get $p3
          i32.const 24
          i32.const 16
          local.get $l16
          f32.const 0x0p+0 (;=0;)
          f32.gt
          select
          i32.or
          local.tee $p3
          local.get $p4
          f32.load offset=156
          f32.const 0x0p+0 (;=0;)
          f32.gt
          i32.eqz
          br_if $B61
          drop
          local.get $p3
          i32.const 4
          i32.or
        end
        local.set $p3
        local.get $p1
        i32.const 0
        i32.store offset=44
        local.get $p1
        local.get $p3
        i32.store16 offset=76
      end
      local.get $l33
      i32.const 4
      i32.and
      i32.eqz
      br_if $B38
      local.get $p4
      f32.load offset=208
      local.tee $l11
      local.get $p4
      f32.load offset=204
      local.tee $l15
      f32.le
      i32.eqz
      br_if $B38
      f32.const 0x0p+0 (;=0;)
      local.set $l12
      local.get $p2
      f32.load offset=144
      local.set $l16
      block $B63
        local.get $p4
        f32.load offset=196
        local.tee $l10
        f32.const 0x0p+0 (;=0;)
        f32.gt
        br_if $B63
        local.get $p4
        f32.load offset=192
        f32.const 0x0p+0 (;=0;)
        f32.gt
        br_if $B63
        local.get $p4
        f32.load offset=200
        local.set $l12
      end
      local.get $l15
      local.get $l16
      local.get $l12
      f32.add
      f32.lt
      if $I64
        local.get $p2
        local.get $p2
        i32.load offset=156
        local.tee $p1
        i32.const 80
        i32.add
        i32.store offset=156
        local.get $p1
        i32.const 0
        i32.store16 offset=78
        local.get $p1
        local.get $p2
        f32.load offset=104
        f32.store
        local.get $p1
        local.get $p2
        f32.load offset=108
        f32.store offset=4
        local.get $p1
        local.get $p2
        f32.load offset=112
        f32.store offset=8
        local.get $p2
        f32.load offset=168
        local.set $l11
        local.get $p2
        f32.load offset=112
        local.set $l10
        local.get $p1
        local.get $p2
        f32.load offset=108
        local.tee $l12
        local.get $p2
        f32.load offset=160
        local.tee $l13
        f32.mul
        local.get $p2
        f32.load offset=164
        local.tee $l17
        local.get $p2
        f32.load offset=104
        local.tee $l14
        f32.mul
        f32.sub
        f32.store offset=24
        local.get $p1
        local.get $l11
        local.get $l14
        f32.mul
        local.get $l10
        local.get $l13
        f32.mul
        f32.sub
        f32.store offset=20
        local.get $p1
        local.get $l17
        local.get $l10
        f32.mul
        local.get $l11
        local.get $l12
        f32.mul
        f32.sub
        f32.store offset=16
        local.get $p1
        local.get $p2
        f32.load offset=104
        local.tee $l11
        f32.store offset=32
        local.get $p1
        local.get $p2
        f32.load offset=108
        local.tee $l10
        f32.store offset=36
        local.get $p1
        local.get $p2
        f32.load offset=112
        local.tee $l12
        f32.store offset=40
        local.get $p2
        f32.load offset=180
        local.set $l13
        local.get $p2
        f32.load offset=172
        local.set $l17
        local.get $p2
        f32.load offset=176
        local.set $l14
        local.get $p1
        local.get $l15
        local.get $l16
        f32.sub
        local.tee $l15
        f32.store offset=12
        local.get $p1
        local.get $l10
        local.get $l17
        f32.mul
        local.get $l11
        local.get $l14
        f32.mul
        f32.sub
        f32.store offset=56
        local.get $p1
        local.get $l11
        local.get $l13
        f32.mul
        local.get $l12
        local.get $l17
        f32.mul
        f32.sub
        f32.store offset=52
        local.get $p1
        local.get $l12
        local.get $l14
        f32.mul
        local.get $l10
        local.get $l13
        f32.mul
        f32.sub
        f32.store offset=48
        local.get $p1
        i32.load16_u offset=76
        local.set $p3
        block $B65 (result i32)
          local.get $p4
          f32.load offset=196
          f32.const 0x0p+0 (;=0;)
          f32.gt
          local.get $p4
          f32.load offset=192
          local.tee $l11
          f32.const 0x0p+0 (;=0;)
          f32.gt
          i32.or
          if $I66
            local.get $p1
            local.get $l11
            f32.store offset=64
            local.get $p1
            local.get $p4
            f32.load offset=196
            f32.store offset=68
            local.get $p3
            i32.const 17
            i32.or
            br $B65
          end
          local.get $p1
          i32.const 2049
          i32.store16 offset=78
          local.get $p1
          local.get $p4
          f32.load offset=184
          f32.store offset=64
          local.get $p1
          local.get $p4
          f32.load offset=188
          f32.store offset=68
          local.get $p3
          i32.const 24
          i32.const 16
          local.get $l15
          f32.const 0x0p+0 (;=0;)
          f32.gt
          select
          i32.or
          local.tee $p3
          local.get $p4
          f32.load offset=184
          f32.const 0x0p+0 (;=0;)
          f32.gt
          i32.eqz
          br_if $B65
          drop
          local.get $p3
          i32.const 4
          i32.or
        end
        local.set $p3
        local.get $p1
        i32.const 0
        i32.store offset=44
        local.get $p1
        local.get $p3
        i32.store16 offset=76
        local.get $p4
        f32.load offset=196
        local.set $l10
        local.get $p4
        f32.load offset=208
        local.set $l11
      end
      f32.const 0x0p+0 (;=0;)
      local.set $l15
      local.get $l11
      f32.neg
      local.set $l12
      block $B67
        local.get $l10
        f32.const 0x0p+0 (;=0;)
        f32.gt
        br_if $B67
        local.get $p4
        f32.load offset=192
        f32.const 0x0p+0 (;=0;)
        f32.gt
        br_if $B67
        local.get $p4
        f32.load offset=200
        local.set $l15
      end
      local.get $l15
      local.get $l16
      f32.sub
      local.get $l12
      f32.gt
      i32.eqz
      br_if $B38
      local.get $p2
      f32.load offset=112
      local.set $l15
      local.get $p2
      f32.load offset=108
      local.set $l10
      local.get $p2
      f32.load offset=104
      local.set $l12
      local.get $p2
      local.get $p2
      i32.load offset=156
      local.tee $p1
      i32.const 80
      i32.add
      i32.store offset=156
      local.get $p1
      local.get $l15
      f32.neg
      local.tee $l18
      f32.store offset=8
      local.get $p1
      local.get $l10
      f32.neg
      local.tee $l19
      f32.store offset=4
      local.get $p1
      local.get $l12
      f32.neg
      local.tee $l20
      f32.store
      local.get $p1
      i32.const 0
      i32.store16 offset=78
      local.get $p2
      f32.load offset=168
      local.set $l13
      local.get $p2
      f32.load offset=164
      local.set $l17
      local.get $p2
      f32.load offset=160
      local.set $l14
      local.get $p1
      local.get $l18
      f32.store offset=40
      local.get $p1
      local.get $l19
      f32.store offset=36
      local.get $p1
      local.get $l20
      f32.store offset=32
      local.get $p1
      local.get $l12
      local.get $l17
      f32.mul
      local.get $l10
      local.get $l14
      f32.mul
      f32.sub
      f32.store offset=24
      local.get $p1
      local.get $l15
      local.get $l14
      f32.mul
      local.get $l12
      local.get $l13
      f32.mul
      f32.sub
      f32.store offset=20
      local.get $p1
      local.get $l10
      local.get $l13
      f32.mul
      local.get $l15
      local.get $l17
      f32.mul
      f32.sub
      f32.store offset=16
      local.get $p2
      f32.load offset=180
      local.set $l13
      local.get $p2
      f32.load offset=176
      local.set $l17
      local.get $p2
      f32.load offset=172
      local.set $l14
      local.get $p1
      local.get $l16
      local.get $l11
      f32.sub
      local.tee $l16
      f32.store offset=12
      local.get $p1
      local.get $l12
      local.get $l17
      f32.mul
      local.get $l10
      local.get $l14
      f32.mul
      f32.sub
      f32.store offset=56
      local.get $p1
      local.get $l15
      local.get $l14
      f32.mul
      local.get $l12
      local.get $l13
      f32.mul
      f32.sub
      f32.store offset=52
      local.get $p1
      local.get $l10
      local.get $l13
      f32.mul
      local.get $l15
      local.get $l17
      f32.mul
      f32.sub
      f32.store offset=48
      local.get $p1
      i32.load16_u offset=76
      local.set $p3
      block $B68 (result i32)
        local.get $p4
        f32.load offset=196
        f32.const 0x0p+0 (;=0;)
        f32.gt
        local.get $p4
        f32.load offset=192
        local.tee $l11
        f32.const 0x0p+0 (;=0;)
        f32.gt
        i32.or
        if $I69
          local.get $p1
          local.get $l11
          f32.store offset=64
          local.get $p1
          local.get $p4
          f32.load offset=196
          f32.store offset=68
          local.get $p3
          i32.const 17
          i32.or
          br $B68
        end
        local.get $p1
        i32.const 2049
        i32.store16 offset=78
        local.get $p1
        local.get $p4
        f32.load offset=184
        f32.store offset=64
        local.get $p1
        local.get $p4
        f32.load offset=188
        f32.store offset=68
        local.get $p3
        i32.const 24
        i32.const 16
        local.get $l16
        f32.const 0x0p+0 (;=0;)
        f32.gt
        select
        i32.or
        local.tee $p3
        local.get $p4
        f32.load offset=184
        f32.const 0x0p+0 (;=0;)
        f32.gt
        i32.eqz
        br_if $B68
        drop
        local.get $p3
        i32.const 4
        i32.or
      end
      local.set $p3
      local.get $p1
      i32.const 0
      i32.store offset=44
      local.get $p1
      local.get $p3
      i32.store16 offset=76
    end
    block $B70
      block $B71
        block $B72
          local.get $p7
          i32.const 56
          i32.and
          i32.const 16
          i32.sub
          br_table $B72 $B70 $B70 $B70 $B70 $B70 $B70 $B70 $B70 $B70 $B70 $B70 $B70 $B70 $B70 $B70 $B71 $B70
        end
        local.get $p2
        local.get $p2
        i32.load offset=156
        local.tee $p1
        i32.const 80
        i32.add
        i32.store offset=156
        local.get $p2
        f32.load offset=48
        local.set $l11
        local.get $p2
        f32.load offset=112
        local.set $l16
        local.get $p1
        local.get $p2
        f32.load offset=108
        local.tee $l15
        local.get $p2
        f32.load offset=40
        local.tee $l10
        f32.mul
        local.get $p2
        f32.load offset=44
        local.tee $l12
        local.get $p2
        f32.load offset=104
        local.tee $l13
        f32.mul
        f32.sub
        local.tee $l17
        f32.store offset=56
        local.get $p1
        local.get $l11
        local.get $l13
        f32.mul
        local.get $l16
        local.get $l10
        f32.mul
        f32.sub
        local.tee $l14
        f32.store offset=52
        local.get $p1
        local.get $l12
        local.get $l16
        f32.mul
        local.get $l11
        local.get $l15
        f32.mul
        f32.sub
        local.tee $l18
        f32.store offset=48
        local.get $p1
        i32.const 0
        i32.store offset=40
        local.get $p1
        i64.const 0
        i64.store offset=32 align=4
        local.get $p1
        local.get $l17
        f32.store offset=24
        local.get $p1
        local.get $l14
        f32.store offset=20
        local.get $p1
        local.get $l18
        f32.store offset=16
        local.get $p1
        i32.const 0
        i32.store offset=8
        local.get $p1
        i64.const 0
        i64.store align=4
        local.get $p1
        i32.const 2048
        i32.store16 offset=78
        local.get $p1
        local.get $p1
        i32.load16_u offset=76
        i32.const 80
        i32.or
        i32.store16 offset=76
        local.get $p1
        local.get $l16
        local.get $l11
        f32.mul
        local.get $l12
        local.get $l15
        f32.mul
        local.get $l13
        local.get $l10
        f32.mul
        f32.add
        f32.add
        f32.neg
        f32.store offset=12
        local.get $p7
        i32.const -17
        i32.and
        local.set $p7
        br $B70
      end
      local.get $p2
      local.get $p2
      i32.load offset=156
      local.tee $p1
      i32.const 80
      i32.add
      i32.store offset=156
      local.get $p2
      f32.load offset=48
      local.set $l11
      local.get $p2
      f32.load offset=100
      local.set $l16
      local.get $p1
      local.get $p2
      f32.load offset=96
      local.tee $l15
      local.get $p2
      f32.load offset=40
      local.tee $l10
      f32.mul
      local.get $p2
      f32.load offset=44
      local.tee $l12
      local.get $p2
      f32.load offset=92
      local.tee $l13
      f32.mul
      f32.sub
      local.tee $l17
      f32.store offset=56
      local.get $p1
      local.get $l11
      local.get $l13
      f32.mul
      local.get $l16
      local.get $l10
      f32.mul
      f32.sub
      local.tee $l14
      f32.store offset=52
      local.get $p1
      local.get $l12
      local.get $l16
      f32.mul
      local.get $l11
      local.get $l15
      f32.mul
      f32.sub
      local.tee $l18
      f32.store offset=48
      local.get $p1
      i32.const 0
      i32.store offset=40
      local.get $p1
      i64.const 0
      i64.store offset=32 align=4
      local.get $p1
      local.get $l17
      f32.store offset=24
      local.get $p1
      local.get $l14
      f32.store offset=20
      local.get $p1
      local.get $l18
      f32.store offset=16
      local.get $p1
      i32.const 0
      i32.store offset=8
      local.get $p1
      i64.const 0
      i64.store align=4
      local.get $p1
      i32.const 2048
      i32.store16 offset=78
      local.get $p1
      local.get $p1
      i32.load16_u offset=76
      i32.const 80
      i32.or
      i32.store16 offset=76
      local.get $p1
      local.get $l16
      local.get $l11
      f32.mul
      local.get $l12
      local.get $l15
      f32.mul
      local.get $l13
      local.get $l10
      f32.mul
      f32.add
      f32.add
      f32.neg
      f32.store offset=12
      local.get $p7
      i32.const -33
      i32.and
      local.set $p7
    end
    local.get $p2
    i32.const 152
    i32.add
    local.get $p2
    i32.const 240
    i32.add
    local.get $p2
    i32.const 208
    i32.add
    local.get $p2
    i32.const 136
    i32.add
    local.get $p7
    i32.const 7
    i32.and
    local.get $p7
    i32.const 3
    i32.shr_u
    local.get $p2
    local.get $p2
    i32.const 288
    i32.add
    call $f72751
    local.get $p5
    f32.load offset=16
    local.set $l11
    local.get $p5
    f32.load offset=20
    local.set $l16
    local.get $p2
    f32.load
    local.set $l15
    local.get $p2
    f32.load offset=4
    local.set $l10
    local.get $p8
    local.get $p2
    f32.load offset=8
    local.get $p5
    f32.load offset=24
    f32.add
    f32.store offset=8
    local.get $p8
    local.get $l10
    local.get $l16
    f32.add
    f32.store offset=4
    local.get $p8
    local.get $l15
    local.get $l11
    f32.add
    f32.store
    local.get $p6
    f32.load offset=16
    local.set $l11
    local.get $p6
    f32.load offset=20
    local.set $l16
    local.get $p2
    f32.load offset=288
    local.set $l15
    local.get $p2
    f32.load offset=292
    local.set $l10
    local.get $p9
    local.get $p2
    f32.load offset=296
    local.get $p6
    f32.load offset=24
    f32.add
    f32.store offset=8
    local.get $p9
    local.get $l10
    local.get $l16
    f32.add
    f32.store offset=4
    local.get $p9
    local.get $l15
    local.get $l11
    f32.add
    f32.store
    local.get $p2
    i32.load offset=152
    local.set $p1
    local.get $p2
    i32.load offset=156
    local.set $p3
    local.get $p2
    i32.const 304
    i32.add
    global.set $g0
    local.get $p3
    local.get $p1
    i32.sub
    i32.const 80
    i32.div_s)
