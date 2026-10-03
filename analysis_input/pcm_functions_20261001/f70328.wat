  (func $f70328 (type $t9) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (result i32)
    (local $l5 i32) (local $l6 i32) (local $l7 f32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32) (local $l33 f32) (local $l34 i64)
    global.get $g0
    i32.const 400
    i32.sub
    local.tee $l5
    global.set $g0
    block $B0 (result f32)
      local.get $p4
      i32.eqz
      if $I1
        f32.const 0x1p+0 (;=1;)
        local.set $l21
        f32.const 0x0p+0 (;=0;)
        br $B0
      end
      f32.const 0x1p+0 (;=1;)
      local.set $l21
      f32.const 0x0p+0 (;=0;)
      local.get $p4
      i32.load16_u offset=12
      i32.const 2
      i32.ne
      br_if $B0
      drop
      local.get $p4
      f32.load offset=8
      local.set $l21
      local.get $p4
      f32.load
      local.set $l24
      local.get $p4
      f32.load offset=4
    end
    local.set $l32
    local.get $p2
    i32.load offset=32
    local.set $l6
    local.get $p0
    f32.load offset=4
    local.set $l17
    local.get $p0
    f32.load offset=8
    local.set $l18
    local.get $p2
    f32.load offset=4
    local.set $l13
    local.get $p2
    f32.load offset=8
    local.set $l25
    local.get $p2
    f32.load offset=12
    local.set $l26
    local.get $l5
    i32.const 0
    i32.store offset=396
    local.get $l5
    local.get $l26
    f32.store offset=392
    local.get $l5
    local.get $l25
    f32.store offset=388
    local.get $l5
    local.get $l13
    f32.store offset=384
    local.get $p2
    i64.load offset=16 align=4
    local.set $l34
    local.get $l5
    local.get $p2
    i64.load offset=24 align=4
    i64.store offset=376
    local.get $l5
    local.get $l34
    i64.store offset=368
    local.get $p3
    f32.load offset=12
    local.tee $l7
    local.get $l7
    f32.mul
    f32.const -0x1p-1 (;=-0.5;)
    f32.add
    local.tee $l14
    local.get $p1
    f32.load offset=24
    local.get $p3
    f32.load offset=24
    f32.sub
    local.tee $l8
    local.get $l8
    f32.add
    local.tee $l15
    f32.mul
    local.get $l7
    local.get $p3
    f32.load offset=4
    local.tee $l8
    local.get $p1
    f32.load offset=16
    local.get $p3
    f32.load offset=16
    f32.sub
    local.tee $l9
    local.get $l9
    f32.add
    local.tee $l11
    f32.mul
    local.get $p3
    f32.load
    local.tee $l9
    local.get $p1
    f32.load offset=20
    local.get $p3
    f32.load offset=20
    f32.sub
    local.tee $l10
    local.get $l10
    f32.add
    local.tee $l12
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $p3
    f32.load offset=8
    local.tee $l10
    local.get $l12
    local.get $l8
    f32.neg
    f32.mul
    local.get $l9
    local.get $l11
    f32.mul
    f32.sub
    local.get $l10
    local.get $l15
    f32.mul
    f32.sub
    local.tee $l16
    f32.mul
    f32.sub
    local.set $l19
    local.get $l14
    local.get $l12
    f32.mul
    local.get $l7
    local.get $l9
    local.get $l15
    f32.mul
    local.get $l10
    local.get $l11
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l8
    local.get $l16
    f32.mul
    f32.sub
    local.set $l20
    local.get $l14
    local.get $l11
    f32.mul
    local.get $l7
    local.get $l10
    local.get $l12
    f32.mul
    local.get $l8
    local.get $l15
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l9
    local.get $l16
    f32.mul
    f32.sub
    local.set $l15
    local.get $l10
    local.get $p1
    f32.load offset=8
    local.tee $l12
    f32.mul
    local.get $l9
    local.get $p1
    f32.load
    local.tee $l14
    f32.mul
    local.get $l7
    local.get $p1
    f32.load offset=12
    local.tee $l16
    f32.mul
    f32.add
    local.get $l8
    local.get $p1
    f32.load offset=4
    local.tee $l22
    f32.mul
    f32.add
    f32.add
    local.tee $l27
    local.get $l8
    local.get $l14
    f32.mul
    local.get $l7
    local.get $l12
    f32.mul
    local.get $l10
    local.get $l16
    f32.mul
    f32.sub
    local.get $l9
    local.get $l22
    f32.mul
    f32.sub
    f32.add
    local.tee $l11
    local.get $l11
    f32.add
    local.tee $l33
    f32.mul
    local.set $l28
    local.get $l27
    local.get $l9
    local.get $l12
    f32.mul
    local.get $l7
    local.get $l22
    f32.mul
    local.get $l8
    local.get $l16
    f32.mul
    f32.sub
    local.get $l10
    local.get $l14
    f32.mul
    f32.sub
    f32.add
    local.tee $l23
    local.get $l23
    f32.add
    local.tee $l29
    f32.mul
    local.set $l30
    local.get $l11
    local.get $l29
    f32.mul
    local.set $l31
    local.get $l7
    local.get $l14
    f32.mul
    local.get $l9
    local.get $l16
    f32.mul
    f32.sub
    local.get $l8
    local.get $l12
    f32.mul
    f32.sub
    local.get $l10
    local.get $l22
    f32.mul
    f32.add
    local.tee $l8
    local.get $l8
    f32.add
    local.tee $l7
    local.get $l27
    f32.mul
    local.set $l9
    local.get $l7
    local.get $l11
    f32.mul
    local.set $l10
    local.get $l7
    local.get $l23
    f32.mul
    local.set $l12
    local.get $l11
    local.get $l33
    f32.mul
    local.set $l11
    local.get $l23
    local.get $l29
    f32.mul
    local.set $l14
    f32.const 0x1p+0 (;=1;)
    local.get $l8
    local.get $l7
    f32.mul
    f32.sub
    local.set $l8
    block $B2 (result i32)
      i32.const 0
      local.get $l13
      f32.const 0x1p+0 (;=1;)
      f32.ne
      br_if $B2
      drop
      i32.const 0
      local.get $p2
      f32.load offset=8
      f32.const 0x1p+0 (;=1;)
      f32.ne
      br_if $B2
      drop
      local.get $p2
      f32.load offset=12
      f32.const 0x1p+0 (;=1;)
      f32.eq
    end
    local.set $p1
    local.get $l5
    i32.const 0
    i32.store8 offset=240
    local.get $l5
    i32.const 232
    i32.add
    local.tee $p2
    i64.const 0
    i64.store
    local.get $l5
    i32.const 224
    i32.add
    local.tee $p3
    i64.const 0
    i64.store
    local.get $l5
    i64.const 0
    i64.store offset=216
    local.get $l5
    i64.const 0
    i64.store offset=208
    local.get $l5
    local.get $l6
    i32.const 16
    i32.add
    i32.store offset=352
    local.get $l5
    local.get $l6
    i32.load offset=56
    local.get $l6
    i32.load8_u offset=55
    i32.const 20
    i32.mul
    i32.add
    i32.store offset=360
    local.get $l5
    local.get $l6
    i32.load8_u offset=54
    i32.store8 offset=364
    local.get $p2
    local.get $l13
    local.get $l6
    f32.load offset=68
    f32.mul
    local.tee $l7
    local.get $l25
    local.get $l6
    f32.load offset=72
    f32.mul
    local.tee $l13
    local.get $l7
    local.get $l13
    f32.le
    select
    local.tee $l7
    local.get $l26
    local.get $l6
    f32.load offset=76
    f32.mul
    local.tee $l13
    local.get $l7
    local.get $l13
    f32.le
    select
    local.tee $l7
    f32.const 0x1.99999ap-6 (;=0.025;)
    f32.mul
    f32.store
    local.get $p3
    local.get $l7
    f32.const 0x1.99999ap-4 (;=0.1;)
    f32.mul
    f32.store
    local.get $l5
    local.get $l7
    f32.const 0x1.99999ap-5 (;=0.05;)
    f32.mul
    f32.store offset=228
    local.get $l5
    i32.const 384
    i32.add
    local.get $l5
    i32.const 368
    i32.add
    local.get $l5
    i32.const 256
    i32.add
    local.get $l5
    i32.const 304
    i32.add
    local.get $l5
    i32.const 208
    i32.add
    local.get $p1
    call $f70494
    local.get $l5
    local.get $l6
    i32.load offset=60
    i32.store offset=356
    local.get $l5
    i32.const 0
    i32.store offset=188
    local.get $l5
    i32.const 0
    i32.store offset=172
    local.get $l5
    local.get $l19
    f32.store offset=120
    local.get $l5
    local.get $l19
    local.get $l18
    f32.const 0x0p+0 (;=0;)
    f32.mul
    local.tee $l7
    local.get $l8
    local.get $l14
    f32.sub
    f32.mul
    local.get $l18
    local.get $l10
    local.get $l30
    f32.sub
    f32.mul
    local.get $l7
    local.get $l9
    local.get $l31
    f32.add
    f32.mul
    f32.add
    f32.add
    local.tee $l13
    f32.sub
    f32.store offset=184
    local.get $l5
    local.get $l20
    f32.store offset=116
    local.get $l5
    local.get $l20
    local.get $l18
    local.get $l12
    local.get $l28
    f32.add
    f32.mul
    local.get $l7
    local.get $l8
    local.get $l11
    f32.sub
    f32.mul
    f32.add
    local.get $l7
    local.get $l31
    local.get $l9
    f32.sub
    f32.mul
    f32.add
    local.tee $l8
    f32.sub
    f32.store offset=180
    local.get $l5
    local.get $l19
    local.get $l13
    f32.add
    f32.store offset=168
    local.get $l5
    local.get $l20
    local.get $l8
    f32.add
    f32.store offset=164
    local.get $l5
    local.get $l17
    f32.store offset=192
    local.get $l5
    i32.const 0
    i32.store offset=124
    local.get $l5
    i32.const 4
    i32.store offset=140
    local.get $l5
    i32.const 1
    i32.store8 offset=144
    local.get $l5
    local.get $l17
    f32.store offset=136
    local.get $l5
    local.get $l17
    f32.store offset=132
    local.get $l5
    local.get $l17
    f32.store offset=128
    local.get $l5
    local.get $l15
    f32.store offset=112
    local.get $l5
    local.get $l15
    local.get $l7
    local.get $l10
    local.get $l30
    f32.add
    f32.mul
    local.get $l7
    local.get $l12
    local.get $l28
    f32.sub
    f32.mul
    local.get $l18
    f32.const 0x1p+0 (;=1;)
    local.get $l14
    f32.sub
    local.get $l11
    f32.sub
    f32.mul
    f32.add
    f32.add
    local.tee $l7
    f32.sub
    f32.store offset=176
    local.get $l5
    local.get $l15
    local.get $l7
    f32.add
    f32.store offset=160
    local.get $l5
    i32.const 3132488
    i32.store offset=40
    local.get $l5
    local.get $l5
    i32.const 112
    i32.add
    i32.store offset=44
    local.get $l5
    i32.const 3132572
    i32.store offset=32
    local.get $l5
    local.get $l5
    i32.const 208
    i32.add
    i32.store offset=36
    local.get $l5
    i32.const 0
    i32.store offset=28
    local.get $l5
    local.get $l19
    local.get $l5
    f32.load offset=216
    f32.sub
    f32.store offset=24
    local.get $l5
    local.get $l20
    local.get $l5
    f32.load offset=212
    f32.sub
    f32.store offset=20
    local.get $l5
    local.get $l15
    local.get $l5
    f32.load offset=208
    f32.sub
    f32.store offset=16
    local.get $l5
    i32.const 0
    i32.store
    local.get $l5
    i32.const 40
    i32.add
    local.get $l5
    i32.const 32
    i32.add
    local.get $l5
    i32.const 16
    i32.add
    local.get $l5
    local.get $l5
    i32.const 96
    i32.add
    local.get $l5
    i32.const 80
    i32.add
    local.get $l5
    i32.const -64
    i32.sub
    local.get $l5
    i32.const 48
    i32.add
    call $f70321
    local.set $l6
    block $B3
      local.get $p4
      i32.eqz
      br_if $B3
      local.get $l6
      i32.const 2
      i32.ne
      br_if $B3
      local.get $p4
      local.get $l21
      f32.store offset=8
      local.get $p4
      local.get $l32
      f32.store offset=4
      local.get $p4
      local.get $l24
      f32.store
    end
    local.get $p4
    if $I4
      local.get $p4
      local.get $l6
      i32.const 2
      i32.eq
      i32.const 1
      i32.shl
      i32.store16 offset=12
    end
    local.get $l5
    i32.const 400
    i32.add
    global.set $g0
    local.get $l6
    i32.const 2
    i32.eq)
