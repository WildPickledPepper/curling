  (func $f70567 (type $t18) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 i32) (param $p7 i32) (result i32)
    (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32) (local $l33 f32) (local $l34 f32) (local $l35 f32) (local $l36 f32) (local $l37 f32) (local $l38 i32) (local $l39 i32) (local $l40 i32) (local $l41 i32) (local $l42 i32)
    global.get $g0
    i32.const 144
    i32.sub
    local.tee $p0
    global.set $g0
    local.get $p3
    f32.load offset=20
    local.set $l28
    local.get $p3
    f32.load offset=24
    local.set $l29
    local.get $p3
    f32.load offset=8
    local.set $l18
    local.get $p3
    f32.load
    local.set $l12
    local.get $p3
    f32.load offset=4
    local.set $l14
    local.get $p3
    f32.load offset=12
    local.set $l23
    local.get $p3
    f32.load offset=16
    local.set $l26
    local.get $p5
    i32.load
    local.set $p3
    local.get $p2
    f32.load offset=20
    local.set $l13
    local.get $p2
    f32.load offset=24
    local.set $l19
    local.get $p2
    f32.load
    local.set $l10
    local.get $p2
    f32.load offset=4
    local.set $l8
    local.get $p2
    f32.load offset=8
    local.set $l11
    local.get $p2
    f32.load offset=12
    local.set $l9
    local.get $p2
    f32.load offset=16
    local.set $l25
    i32.const 0
    local.set $p2
    local.get $p0
    i32.const 0
    i32.store offset=140
    local.get $p0
    local.get $l19
    f32.store offset=136
    local.get $p0
    local.get $l13
    f32.store offset=132
    local.get $p0
    local.get $l25
    f32.store offset=128
    local.get $p0
    local.get $l9
    f32.store offset=124
    local.get $p0
    local.get $l11
    f32.store offset=120
    local.get $p0
    local.get $l8
    f32.store offset=116
    local.get $p0
    local.get $l10
    f32.store offset=112
    local.get $p0
    i32.const 0
    i32.store offset=108
    local.get $p0
    f32.const 0x1p+0 (;=1;)
    local.get $l11
    local.get $l10
    local.get $l10
    f32.add
    local.tee $l15
    f32.mul
    local.get $l8
    local.get $l9
    local.get $l9
    f32.add
    local.tee $l16
    f32.mul
    f32.sub
    local.tee $l21
    local.get $l21
    f32.mul
    local.get $l15
    local.get $l8
    f32.mul
    local.get $l11
    local.get $l16
    f32.mul
    f32.add
    local.tee $l22
    local.get $l22
    f32.mul
    local.get $l10
    local.get $l15
    f32.mul
    local.get $l9
    local.get $l16
    f32.mul
    f32.add
    f32.const -0x1p+0 (;=-1;)
    f32.add
    local.tee $l15
    local.get $l15
    f32.mul
    f32.add
    f32.add
    f32.sqrt
    f32.div
    local.tee $l16
    local.get $l21
    f32.neg
    f32.mul
    f32.store offset=104
    local.get $p0
    local.get $l16
    local.get $l22
    f32.neg
    f32.mul
    f32.store offset=100
    local.get $p0
    local.get $l16
    local.get $l15
    f32.neg
    f32.mul
    f32.store offset=96
    local.get $p0
    local.get $p4
    f32.load
    f32.store offset=80
    local.get $p0
    local.get $p4
    f32.load offset=8
    f32.const 0x1.333334p-3 (;=0.15;)
    f32.mul
    local.tee $l22
    local.get $p1
    f32.load offset=4
    local.tee $l15
    local.get $p1
    f32.load offset=8
    local.tee $l16
    local.get $l15
    local.get $l16
    f32.le
    select
    local.tee $l27
    local.get $p1
    f32.load offset=12
    local.tee $l21
    local.get $l21
    local.get $l27
    f32.ge
    select
    f32.const 0x1.333334p-3 (;=0.15;)
    f32.mul
    local.tee $l27
    local.get $l22
    local.get $l27
    f32.lt
    select
    f32.const 0x1.99999ap-3 (;=0.2;)
    f32.mul
    local.tee $l34
    f32.store offset=64
    local.get $p3
    i32.load8_u offset=64
    local.set $p1
    local.get $p0
    i32.const 0
    i32.store offset=60
    local.get $p0
    local.get $l9
    local.get $l9
    f32.mul
    f32.const -0x1p-1 (;=-0.5;)
    f32.add
    local.tee $l20
    local.get $l29
    local.get $l19
    f32.sub
    local.tee $l29
    f32.mul
    local.get $l9
    local.get $l8
    local.get $l26
    local.get $l25
    f32.sub
    local.tee $l26
    f32.mul
    local.get $l10
    local.get $l28
    local.get $l13
    f32.sub
    local.tee $l27
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l11
    local.get $l27
    local.get $l8
    f32.neg
    local.tee $l32
    f32.mul
    local.get $l10
    local.get $l26
    f32.mul
    f32.sub
    local.get $l11
    local.get $l29
    f32.mul
    f32.sub
    local.tee $l24
    f32.mul
    f32.sub
    local.tee $l13
    local.get $l13
    f32.add
    local.tee $l25
    f32.store offset=56
    local.get $p0
    local.get $l20
    local.get $l27
    f32.mul
    local.get $l9
    local.get $l10
    local.get $l29
    f32.mul
    local.get $l11
    local.get $l26
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l8
    local.get $l24
    f32.mul
    f32.sub
    local.tee $l13
    local.get $l13
    f32.add
    local.tee $l22
    f32.store offset=52
    local.get $p0
    i32.const 0
    i32.store offset=44
    local.get $p0
    f32.const 0x1p+0 (;=1;)
    local.get $l14
    local.get $l11
    f32.mul
    local.get $l18
    local.get $l8
    f32.mul
    f32.sub
    local.get $l12
    local.get $l9
    f32.mul
    local.get $l23
    local.get $l10
    f32.mul
    f32.sub
    f32.add
    local.tee $l28
    local.get $l28
    local.get $l28
    f32.add
    local.tee $l31
    f32.mul
    f32.sub
    local.tee $l33
    local.get $l18
    local.get $l10
    f32.mul
    local.get $l12
    local.get $l11
    f32.mul
    f32.sub
    local.get $l14
    local.get $l9
    f32.mul
    local.get $l23
    local.get $l8
    f32.mul
    f32.sub
    f32.add
    local.tee $l19
    local.get $l19
    local.get $l19
    f32.add
    local.tee $l17
    f32.mul
    local.tee $l30
    f32.sub
    local.tee $l35
    f32.store offset=40
    local.get $p0
    local.get $l12
    local.get $l8
    f32.mul
    local.get $l14
    local.get $l10
    f32.mul
    f32.sub
    local.get $l18
    local.get $l9
    f32.mul
    local.get $l23
    local.get $l11
    f32.mul
    f32.sub
    f32.add
    local.tee $l13
    local.get $l17
    f32.mul
    local.tee $l36
    local.get $l23
    local.get $l9
    f32.mul
    local.get $l14
    local.get $l32
    f32.mul
    local.get $l12
    local.get $l10
    f32.mul
    f32.sub
    local.get $l18
    local.get $l11
    f32.mul
    f32.sub
    f32.sub
    local.tee $l18
    local.get $l31
    f32.mul
    local.tee $l12
    f32.sub
    local.tee $l37
    f32.store offset=36
    local.get $p0
    i32.const 0
    i32.store offset=28
    local.get $p0
    local.get $l36
    local.get $l12
    f32.add
    local.tee $l32
    f32.store offset=24
    local.get $p0
    local.get $l33
    local.get $l13
    local.get $l13
    local.get $l13
    f32.add
    local.tee $l12
    f32.mul
    local.tee $l14
    f32.sub
    local.tee $l33
    f32.store offset=20
    local.get $p0
    local.get $l20
    local.get $l26
    f32.mul
    local.get $l9
    local.get $l11
    local.get $l27
    f32.mul
    local.get $l8
    local.get $l29
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l10
    local.get $l24
    f32.mul
    f32.sub
    local.tee $l9
    local.get $l9
    f32.add
    local.tee $l9
    f32.store offset=48
    local.get $p0
    local.get $l13
    local.get $l31
    f32.mul
    local.tee $l10
    local.get $l18
    local.get $l17
    f32.mul
    local.tee $l11
    f32.add
    local.tee $l20
    f32.store offset=32
    local.get $p0
    local.get $l19
    local.get $l31
    f32.mul
    local.tee $l8
    local.get $l18
    local.get $l12
    f32.mul
    local.tee $l12
    f32.sub
    local.tee $l29
    f32.store offset=16
    local.get $p0
    i32.const 0
    i32.store offset=12
    local.get $p0
    local.get $l10
    local.get $l11
    f32.sub
    local.tee $l10
    f32.store offset=8
    local.get $p0
    local.get $l8
    local.get $l12
    f32.add
    local.tee $l11
    f32.store offset=4
    local.get $p0
    f32.const 0x1p+0 (;=1;)
    local.get $l30
    f32.sub
    local.get $l14
    f32.sub
    local.tee $l8
    f32.store
    local.get $p3
    local.get $p0
    local.get $p0
    i32.const -64
    i32.sub
    call $f70045
    block $B0
      block $B1
        local.get $p1
        local.get $p3
        i32.load8_u offset=64
        i32.ne
        br_if $B1
        local.get $l28
        local.get $p3
        f32.load
        f32.mul
        local.get $l19
        local.get $p3
        f32.load offset=4
        f32.mul
        f32.add
        local.get $l13
        local.get $p3
        f32.load offset=8
        f32.mul
        f32.add
        local.get $l18
        local.get $p3
        f32.load offset=12
        f32.mul
        f32.add
        f32.const 0x1.ffe5cap-1 (;=0.9998;)
        f32.lt
        br_if $B1
        local.get $l9
        local.get $p3
        f32.load offset=16
        f32.sub
        local.tee $l12
        local.get $l12
        f32.neg
        local.tee $l14
        local.get $l12
        local.get $l14
        f32.gt
        select
        local.tee $l12
        local.get $l22
        local.get $p3
        f32.load offset=20
        f32.sub
        local.tee $l14
        local.get $l14
        f32.neg
        local.tee $l23
        local.get $l14
        local.get $l23
        f32.gt
        select
        local.tee $l14
        local.get $l12
        local.get $l14
        f32.ge
        select
        local.tee $l23
        local.get $l12
        f32.const 0x0p+0 (;=0;)
        local.get $l25
        local.get $p3
        f32.load offset=24
        f32.sub
        local.tee $l14
        local.get $l14
        f32.neg
        local.tee $l26
        local.get $l14
        local.get $l26
        f32.gt
        select
        f32.const 0x0p+0 (;=0;)
        f32.ge
        select
        local.tee $l12
        local.get $l12
        local.get $l23
        f32.le
        select
        local.get $l34
        f32.gt
        i32.eqz
        br_if $B0
      end
      local.get $p3
      local.get $l9
      f32.store offset=16
      local.get $p3
      local.get $l18
      f32.store offset=12
      local.get $p3
      local.get $l13
      f32.store offset=8
      local.get $p3
      local.get $l19
      f32.store offset=4
      local.get $p3
      local.get $l28
      f32.store
      local.get $p3
      i32.const 0
      i32.store8 offset=64
      local.get $p3
      i32.const 0
      i32.store offset=28
      local.get $p3
      local.get $l25
      f32.store offset=24
      local.get $p3
      local.get $l22
      f32.store offset=20
      local.get $l10
      local.get $l15
      f32.mul
      local.tee $l12
      local.get $l32
      local.get $l16
      f32.mul
      local.tee $l26
      f32.add
      local.set $l17
      local.get $l11
      local.get $l15
      f32.mul
      local.tee $l14
      local.get $l33
      local.get $l16
      f32.mul
      local.tee $l27
      f32.add
      local.set $l30
      local.get $l8
      local.get $l15
      f32.mul
      local.tee $l23
      local.get $l29
      local.get $l16
      f32.mul
      local.tee $l31
      f32.sub
      local.set $l13
      local.get $l23
      local.get $l31
      f32.add
      local.tee $l28
      local.get $l20
      local.get $l21
      f32.mul
      local.tee $l10
      f32.sub
      local.set $l8
      local.get $l35
      local.get $l21
      f32.mul
      local.set $l19
      local.get $l37
      local.get $l21
      f32.mul
      local.set $l18
      local.get $p0
      f32.load offset=80
      local.get $l9
      f32.sub
      local.tee $l11
      local.get $l10
      local.get $l28
      f32.add
      local.tee $l20
      f32.gt
      if $I2
        local.get $p6
        i64.const 4575657221408423936
        i64.store offset=28 align=4
        local.get $p6
        i32.const 0
        i32.store offset=12
        local.get $p6
        local.get $l21
        f32.store offset=8
        local.get $p6
        local.get $l16
        f32.store offset=4
        local.get $p6
        local.get $l15
        f32.store
        local.get $p6
        local.get $l9
        local.get $l20
        f32.add
        local.tee $l20
        f32.store offset=44
        local.get $p6
        i64.const 0
        i64.store offset=36 align=4
        local.get $p6
        local.get $l20
        local.get $l20
        f32.sub
        f32.store offset=16
        local.get $p6
        local.get $l25
        local.get $l17
        local.get $l19
        f32.add
        f32.add
        local.get $l20
        f32.const 0x0p+0 (;=0;)
        f32.mul
        local.tee $l20
        f32.sub
        f32.store offset=24
        local.get $p6
        local.get $l22
        local.get $l30
        local.get $l18
        f32.add
        f32.add
        local.get $l20
        f32.sub
        f32.store offset=20
        i32.const 1
        local.set $p2
      end
      local.get $l10
      local.get $l13
      f32.add
      local.set $l24
      local.get $l21
      f32.neg
      local.set $l20
      local.get $l8
      local.get $l11
      f32.lt
      if $I3
        local.get $p6
        local.get $p2
        i32.const 48
        i32.mul
        i32.add
        local.tee $p1
        local.get $l9
        local.get $l8
        f32.add
        local.tee $l8
        local.get $l8
        f32.sub
        f32.store offset=16
        local.get $p1
        i32.const 0
        i32.store offset=12
        local.get $p1
        local.get $l20
        f32.store offset=8
        local.get $p1
        local.get $l16
        f32.store offset=4
        local.get $p1
        local.get $l15
        f32.store
        local.get $p1
        local.get $l8
        f32.store offset=44
        local.get $p1
        i64.const 0
        i64.store offset=36 align=4
        local.get $p1
        i64.const 4575657221408423936
        i64.store offset=28 align=4
        local.get $p1
        local.get $l25
        local.get $l17
        local.get $l19
        f32.sub
        f32.add
        local.get $l8
        f32.const 0x0p+0 (;=0;)
        f32.mul
        local.tee $l8
        f32.sub
        f32.store offset=24
        local.get $p1
        local.get $l22
        local.get $l30
        local.get $l18
        f32.sub
        f32.add
        local.get $l8
        f32.sub
        f32.store offset=20
        local.get $p2
        i32.const 1
        i32.add
        local.set $p2
      end
      local.get $l13
      local.get $l10
      f32.sub
      local.set $l17
      local.get $l16
      f32.neg
      local.set $l8
      local.get $l11
      local.get $l24
      f32.gt
      if $I4
        local.get $p6
        local.get $p2
        i32.const 48
        i32.mul
        i32.add
        local.tee $p1
        local.get $l9
        local.get $l24
        f32.add
        local.tee $l24
        local.get $l24
        f32.sub
        f32.store offset=16
        local.get $p1
        i32.const 0
        i32.store offset=12
        local.get $p1
        local.get $l21
        f32.store offset=8
        local.get $p1
        local.get $l8
        f32.store offset=4
        local.get $p1
        local.get $l15
        f32.store
        local.get $p1
        local.get $l24
        f32.store offset=44
        local.get $p1
        i64.const 0
        i64.store offset=36 align=4
        local.get $p1
        i64.const 4575657221408423936
        i64.store offset=28 align=4
        local.get $p1
        local.get $l25
        local.get $l12
        local.get $l26
        f32.sub
        local.get $l19
        f32.add
        f32.add
        local.get $l24
        f32.const 0x0p+0 (;=0;)
        f32.mul
        local.tee $l24
        f32.sub
        f32.store offset=24
        local.get $p1
        local.get $l22
        local.get $l14
        local.get $l27
        f32.sub
        local.get $l18
        f32.add
        f32.add
        local.get $l24
        f32.sub
        f32.store offset=20
        local.get $p2
        i32.const 1
        i32.add
        local.set $p2
      end
      local.get $l10
      f32.neg
      local.set $l24
      local.get $l10
      local.get $l13
      f32.sub
      local.set $l30
      local.get $l11
      local.get $l17
      f32.gt
      if $I5
        local.get $p6
        local.get $p2
        i32.const 48
        i32.mul
        i32.add
        local.tee $p1
        local.get $l9
        local.get $l17
        f32.add
        local.tee $l17
        local.get $l17
        f32.sub
        f32.store offset=16
        local.get $p1
        i32.const 0
        i32.store offset=12
        local.get $p1
        local.get $l20
        f32.store offset=8
        local.get $p1
        local.get $l8
        f32.store offset=4
        local.get $p1
        local.get $l15
        f32.store
        local.get $p1
        local.get $l17
        f32.store offset=44
        local.get $p1
        i64.const 0
        i64.store offset=36 align=4
        local.get $p1
        i64.const 4575657221408423936
        i64.store offset=28 align=4
        local.get $p1
        local.get $l25
        local.get $l12
        local.get $l26
        f32.sub
        local.get $l19
        f32.sub
        f32.add
        local.get $l17
        f32.const 0x0p+0 (;=0;)
        f32.mul
        local.tee $l17
        f32.sub
        f32.store offset=24
        local.get $p1
        local.get $l22
        local.get $l14
        local.get $l27
        f32.sub
        local.get $l18
        f32.sub
        f32.add
        local.get $l17
        f32.sub
        f32.store offset=20
        local.get $p2
        i32.const 1
        i32.add
        local.set $p2
      end
      local.get $l24
      local.get $l13
      f32.sub
      local.set $l13
      local.get $l15
      f32.neg
      local.set $l15
      local.get $l11
      local.get $l30
      f32.gt
      if $I6
        local.get $p6
        local.get $p2
        i32.const 48
        i32.mul
        i32.add
        local.tee $p1
        i32.const 0
        i32.store offset=12
        local.get $p1
        local.get $l21
        f32.store offset=8
        local.get $p1
        local.get $l16
        f32.store offset=4
        local.get $p1
        local.get $l15
        f32.store
        local.get $p1
        local.get $l9
        local.get $l30
        f32.add
        local.tee $l17
        f32.store offset=44
        local.get $p1
        i64.const 0
        i64.store offset=36 align=4
        local.get $p1
        i64.const 4575657221408423936
        i64.store offset=28 align=4
        local.get $p1
        local.get $l25
        local.get $l26
        local.get $l12
        f32.sub
        local.get $l19
        f32.add
        f32.add
        local.get $l17
        f32.const 0x0p+0 (;=0;)
        f32.mul
        local.tee $l30
        f32.sub
        f32.store offset=24
        local.get $p1
        local.get $l22
        local.get $l27
        local.get $l14
        f32.sub
        local.get $l18
        f32.add
        f32.add
        local.get $l30
        f32.sub
        f32.store offset=20
        local.get $p1
        local.get $l9
        local.get $l31
        local.get $l23
        f32.sub
        local.get $l10
        f32.add
        f32.add
        local.get $l17
        f32.sub
        f32.store offset=16
        local.get $p2
        i32.const 1
        i32.add
        local.set $p2
      end
      local.get $l10
      local.get $l28
      f32.sub
      local.set $l17
      local.get $l11
      local.get $l13
      f32.gt
      if $I7
        local.get $p6
        local.get $p2
        i32.const 48
        i32.mul
        i32.add
        local.tee $p1
        i32.const 0
        i32.store offset=12
        local.get $p1
        local.get $l20
        f32.store offset=8
        local.get $p1
        local.get $l16
        f32.store offset=4
        local.get $p1
        local.get $l15
        f32.store
        local.get $p1
        local.get $l9
        local.get $l13
        f32.add
        local.tee $l16
        f32.store offset=44
        local.get $p1
        i64.const 0
        i64.store offset=36 align=4
        local.get $p1
        i64.const 4575657221408423936
        i64.store offset=28 align=4
        local.get $p1
        local.get $l25
        local.get $l26
        local.get $l12
        f32.sub
        local.get $l19
        f32.sub
        f32.add
        local.get $l16
        f32.const 0x0p+0 (;=0;)
        f32.mul
        local.tee $l13
        f32.sub
        f32.store offset=24
        local.get $p1
        local.get $l22
        local.get $l27
        local.get $l14
        f32.sub
        local.get $l18
        f32.sub
        f32.add
        local.get $l13
        f32.sub
        f32.store offset=20
        local.get $p1
        local.get $l9
        local.get $l31
        local.get $l23
        f32.sub
        local.get $l10
        f32.sub
        f32.add
        local.get $l16
        f32.sub
        f32.store offset=16
        local.get $p2
        i32.const 1
        i32.add
        local.set $p2
      end
      local.get $l24
      local.get $l28
      f32.sub
      local.set $l16
      local.get $l11
      local.get $l17
      f32.gt
      if $I8
        local.get $p6
        local.get $p2
        i32.const 48
        i32.mul
        i32.add
        local.tee $p1
        i32.const 0
        i32.store offset=12
        local.get $p1
        local.get $l21
        f32.store offset=8
        local.get $p1
        local.get $l8
        f32.store offset=4
        local.get $p1
        local.get $l15
        f32.store
        local.get $p1
        local.get $l9
        local.get $l17
        f32.add
        local.tee $l21
        f32.store offset=44
        local.get $p1
        i64.const 0
        i64.store offset=36 align=4
        local.get $p1
        i64.const 4575657221408423936
        i64.store offset=28 align=4
        local.get $p1
        local.get $l25
        local.get $l32
        local.get $l8
        f32.mul
        local.get $l12
        f32.sub
        local.get $l19
        f32.add
        f32.add
        local.get $l21
        f32.const 0x0p+0 (;=0;)
        f32.mul
        local.tee $l13
        f32.sub
        f32.store offset=24
        local.get $p1
        local.get $l22
        local.get $l33
        local.get $l8
        f32.mul
        local.get $l14
        f32.sub
        local.get $l18
        f32.add
        f32.add
        local.get $l13
        f32.sub
        f32.store offset=20
        local.get $p1
        local.get $l9
        local.get $l29
        local.get $l8
        f32.mul
        local.get $l23
        f32.sub
        local.get $l10
        f32.add
        f32.add
        local.get $l21
        f32.sub
        f32.store offset=16
        local.get $p2
        i32.const 1
        i32.add
        local.set $p2
      end
      i32.const 0
      local.set $p4
      local.get $l11
      local.get $l16
      f32.gt
      if $I9
        local.get $p6
        local.get $p2
        i32.const 48
        i32.mul
        i32.add
        local.tee $p1
        i32.const 0
        i32.store offset=12
        local.get $p1
        local.get $l20
        f32.store offset=8
        local.get $p1
        local.get $l8
        f32.store offset=4
        local.get $p1
        local.get $l15
        f32.store
        local.get $p1
        local.get $l9
        local.get $l16
        f32.add
        local.tee $l11
        f32.store offset=44
        local.get $p1
        i64.const 0
        i64.store offset=36 align=4
        local.get $p1
        i64.const 4575657221408423936
        i64.store offset=28 align=4
        local.get $p1
        local.get $l25
        local.get $l32
        local.get $l8
        f32.mul
        local.get $l12
        f32.sub
        local.get $l19
        f32.sub
        f32.add
        local.get $l11
        f32.const 0x0p+0 (;=0;)
        f32.mul
        local.tee $l15
        f32.sub
        f32.store offset=24
        local.get $p1
        local.get $l22
        local.get $l33
        local.get $l8
        f32.mul
        local.get $l14
        f32.sub
        local.get $l18
        f32.sub
        f32.add
        local.get $l15
        f32.sub
        f32.store offset=20
        local.get $p1
        local.get $l9
        local.get $l29
        local.get $l8
        f32.mul
        local.get $l23
        f32.sub
        local.get $l10
        f32.sub
        f32.add
        local.get $l11
        f32.sub
        f32.store offset=16
        local.get $p2
        i32.const 1
        i32.add
        local.set $p2
      end
      block $B10
        block $B11
          local.get $p2
          i32.const 4
          i32.le_u
          if $I12
            local.get $p2
            i32.eqz
            br_if $B11
            local.get $p3
            i32.load offset=76
            local.tee $p4
            local.get $p6
            i64.load
            i64.store
            local.get $p4
            local.get $p6
            i64.load offset=8
            i64.store offset=8
            local.get $p3
            i32.load offset=76
            local.tee $p4
            local.get $p6
            i64.load offset=16
            i64.store offset=16
            local.get $p4
            local.get $p6
            i64.load offset=24
            i64.store offset=24
            local.get $p3
            i32.load offset=76
            local.tee $p4
            local.get $p6
            i64.load offset=32
            i64.store offset=32
            local.get $p4
            local.get $p6
            i64.load offset=40
            i64.store offset=40
            local.get $p2
            i32.const 1
            i32.eq
            br_if $B11
            local.get $p3
            i32.load offset=76
            local.tee $p4
            local.get $p6
            i64.load offset=48
            i64.store offset=48
            local.get $p4
            local.get $p6
            i64.load offset=56
            i64.store offset=56
            local.get $p3
            i32.load offset=76
            local.tee $p4
            i32.const -64
            i32.sub
            local.get $p6
            i32.const -64
            i32.sub
            i64.load
            i64.store
            local.get $p4
            local.get $p6
            i64.load offset=72
            i64.store offset=72
            local.get $p3
            i32.load offset=76
            local.tee $p4
            local.get $p6
            i64.load offset=80
            i64.store offset=80
            local.get $p4
            local.get $p6
            i64.load offset=88
            i64.store offset=88
            local.get $p2
            i32.const 2
            i32.eq
            br_if $B11
            local.get $p3
            i32.load offset=76
            local.tee $p4
            local.get $p6
            i64.load offset=96
            i64.store offset=96
            local.get $p4
            local.get $p6
            i64.load offset=104
            i64.store offset=104
            local.get $p3
            i32.load offset=76
            local.tee $p4
            local.get $p6
            i64.load offset=112
            i64.store offset=112
            local.get $p4
            local.get $p6
            i64.load offset=120
            i64.store offset=120
            local.get $p3
            i32.load offset=76
            local.tee $p4
            local.get $p6
            i64.load offset=128
            i64.store offset=128
            local.get $p4
            local.get $p6
            i64.load offset=136
            i64.store offset=136
            local.get $p2
            i32.const 3
            i32.eq
            br_if $B11
            local.get $p3
            i32.load offset=76
            local.tee $p4
            local.get $p6
            i64.load offset=144
            i64.store offset=144
            local.get $p4
            local.get $p6
            i64.load offset=152
            i64.store offset=152
            local.get $p3
            i32.load offset=76
            local.tee $p4
            local.get $p6
            i64.load offset=160
            i64.store offset=160
            local.get $p4
            local.get $p6
            i64.load offset=168
            i64.store offset=168
            local.get $p3
            i32.load offset=76
            local.tee $p4
            local.get $p6
            i64.load offset=176
            i64.store offset=176
            local.get $p4
            local.get $p6
            i64.load offset=184
            i64.store offset=184
            local.get $p3
            local.get $p2
            i32.store8 offset=64
            br $B10
          end
          global.get $g0
          i32.const 80
          i32.sub
          local.tee $p7
          global.set $g0
          local.get $p7
          i32.const 16
          i32.add
          i32.const 0
          local.get $p2
          call $f484
          drop
          local.get $p2
          if $I13
            f32.const -0x1.fffffep+127 (;=-3.40282e+38;)
            local.set $l8
            loop $L14
              local.get $p6
              local.get $p4
              i32.const 48
              i32.mul
              i32.add
              local.tee $p1
              f32.load offset=16
              local.tee $l9
              local.get $l9
              f32.mul
              local.get $p1
              f32.load offset=20
              local.tee $l9
              local.get $l9
              f32.mul
              f32.add
              local.get $p1
              f32.load offset=24
              local.tee $l9
              local.get $l9
              f32.mul
              f32.add
              local.tee $l9
              local.get $l8
              local.get $l8
              local.get $l9
              f32.lt
              local.tee $p1
              select
              local.set $l8
              local.get $p4
              local.get $l40
              local.get $p1
              select
              local.set $l40
              local.get $p4
              i32.const 1
              i32.add
              local.tee $p4
              local.get $p2
              i32.ne
              br_if $L14
            end
          end
          local.get $p3
          i32.load offset=76
          local.tee $p4
          local.get $p6
          local.get $l40
          i32.const 48
          i32.mul
          i32.add
          local.tee $p1
          i64.load
          i64.store
          local.get $p4
          local.get $p1
          i64.load offset=40
          i64.store offset=40
          local.get $p4
          local.get $p1
          i64.load offset=32
          i64.store offset=32
          local.get $p4
          local.get $p1
          i64.load offset=24
          i64.store offset=24
          local.get $p4
          local.get $p1
          i64.load offset=16
          i64.store offset=16
          local.get $p4
          local.get $p1
          i64.load offset=8
          i64.store offset=8
          local.get $p7
          i32.const 16
          i32.add
          local.get $l40
          i32.add
          i32.const 1
          i32.store8
          local.get $p7
          local.get $l40
          i32.store
          local.get $p3
          i32.load offset=76
          local.set $p5
          local.get $p2
          i32.const 2
          i32.ge_u
          if $I15
            local.get $p6
            f32.load offset=16
            local.get $p5
            f32.load offset=16
            local.tee $l11
            f32.sub
            local.tee $l8
            local.get $l8
            f32.mul
            local.get $p6
            f32.load offset=20
            local.get $p5
            f32.load offset=20
            local.tee $l12
            f32.sub
            local.tee $l8
            local.get $l8
            f32.mul
            f32.add
            local.get $p6
            f32.load offset=24
            local.get $p5
            f32.load offset=24
            local.tee $l10
            f32.sub
            local.tee $l8
            local.get $l8
            f32.mul
            f32.add
            local.set $l8
            i32.const 1
            local.set $p4
            loop $L16
              local.get $p6
              local.get $p4
              i32.const 48
              i32.mul
              i32.add
              local.tee $p1
              f32.load offset=16
              local.get $l11
              f32.sub
              local.tee $l9
              local.get $l9
              f32.mul
              local.get $p1
              f32.load offset=20
              local.get $l12
              f32.sub
              local.tee $l9
              local.get $l9
              f32.mul
              f32.add
              local.get $p1
              f32.load offset=24
              local.get $l10
              f32.sub
              local.tee $l9
              local.get $l9
              f32.mul
              f32.add
              local.tee $l9
              local.get $l8
              local.get $l8
              local.get $l9
              f32.lt
              local.tee $p1
              select
              local.set $l8
              local.get $p4
              local.get $l39
              local.get $p1
              select
              local.set $l39
              local.get $p4
              i32.const 1
              i32.add
              local.tee $p4
              local.get $p2
              i32.ne
              br_if $L16
            end
          end
          local.get $p5
          local.get $p6
          local.get $l39
          i32.const 48
          i32.mul
          i32.add
          local.tee $p4
          i64.load
          i64.store offset=48
          local.get $p5
          local.get $p4
          i64.load offset=40
          i64.store offset=88
          local.get $p5
          local.get $p4
          i64.load offset=32
          i64.store offset=80
          local.get $p5
          local.get $p4
          i64.load offset=24
          i64.store offset=72
          local.get $p5
          i32.const -64
          i32.sub
          local.get $p4
          i64.load offset=16
          i64.store
          local.get $p5
          local.get $p4
          i64.load offset=8
          i64.store offset=56
          local.get $p7
          i32.const 16
          i32.add
          local.get $l39
          i32.add
          i32.const 1
          i32.store8
          local.get $p7
          local.get $l39
          i32.store offset=4
          local.get $p3
          i32.load offset=76
          local.tee $l38
          i32.const -64
          i32.sub
          f32.load
          local.get $l38
          f32.load offset=16
          local.tee $l15
          f32.sub
          local.tee $l10
          local.get $l38
          f32.load offset=36
          local.tee $l8
          f32.mul
          local.get $l38
          f32.load offset=68
          local.get $l38
          f32.load offset=20
          local.tee $l16
          f32.sub
          local.tee $l12
          local.get $l38
          f32.load offset=32
          local.tee $l9
          f32.mul
          f32.sub
          local.tee $l11
          f32.const 0x1p+0 (;=1;)
          local.get $l11
          local.get $l11
          f32.mul
          local.get $l12
          local.get $l38
          f32.load offset=40
          local.tee $l11
          f32.mul
          local.get $l38
          f32.load offset=72
          local.get $l38
          f32.load offset=24
          local.tee $l17
          f32.sub
          local.tee $l13
          local.get $l8
          f32.mul
          f32.sub
          local.tee $l12
          local.get $l12
          f32.mul
          local.get $l13
          local.get $l9
          f32.mul
          local.get $l10
          local.get $l11
          f32.mul
          f32.sub
          local.tee $l13
          local.get $l13
          f32.mul
          f32.add
          f32.add
          local.tee $l10
          f32.sqrt
          f32.div
          local.tee $l14
          f32.mul
          local.get $l11
          local.get $l10
          f32.const 0x0p+0 (;=0;)
          f32.gt
          local.tee $p4
          select
          local.set $l10
          local.get $l13
          local.get $l14
          f32.mul
          local.get $l8
          local.get $p4
          select
          local.set $l13
          local.get $l12
          local.get $l14
          f32.mul
          local.get $l9
          local.get $p4
          select
          local.set $l14
          i32.const -1
          local.set $p1
          f32.const -0x1.fffffep+127 (;=-3.40282e+38;)
          local.set $l12
          f32.const 0x1.fffffep+127 (;=3.40282e+38;)
          local.set $l11
          block $B17
            local.get $p2
            i32.eqz
            if $I18
              f32.const -0x1.fffffep+127 (;=-3.40282e+38;)
              local.set $l9
              i32.const -1
              local.set $l41
              br $B17
            end
            i32.const 0
            local.set $p4
            i32.const -1
            local.set $l41
            f32.const -0x1.fffffep+127 (;=-3.40282e+38;)
            local.set $l9
            loop $L19
              local.get $p7
              i32.const 16
              i32.add
              local.get $p4
              i32.add
              i32.load8_u
              i32.eqz
              if $I20
                local.get $l14
                local.get $p6
                local.get $p4
                i32.const 48
                i32.mul
                i32.add
                local.tee $p5
                f32.load offset=16
                local.get $l15
                f32.sub
                f32.mul
                local.get $l13
                local.get $p5
                f32.load offset=20
                local.get $l16
                f32.sub
                f32.mul
                f32.add
                local.get $l10
                local.get $p5
                f32.load offset=24
                local.get $l17
                f32.sub
                f32.mul
                f32.add
                local.tee $l8
                local.get $l11
                local.get $l8
                local.get $l11
                f32.lt
                local.tee $p5
                select
                local.set $l11
                local.get $l8
                local.get $l9
                local.get $l8
                local.get $l9
                f32.gt
                local.tee $l42
                select
                local.set $l9
                local.get $p4
                local.get $l41
                local.get $l42
                select
                local.set $l41
                local.get $p4
                local.get $p1
                local.get $p5
                select
                local.set $p1
              end
              local.get $p4
              i32.const 1
              i32.add
              local.tee $p4
              local.get $p2
              i32.ne
              br_if $L19
            end
          end
          local.get $l38
          local.get $p6
          local.get $l41
          i32.const 48
          i32.mul
          i32.add
          local.tee $p4
          i64.load
          i64.store offset=96
          local.get $l38
          local.get $p4
          i64.load offset=40
          i64.store offset=136
          local.get $l38
          local.get $p4
          i64.load offset=32
          i64.store offset=128
          local.get $l38
          local.get $p4
          i64.load offset=24
          i64.store offset=120
          local.get $l38
          local.get $p4
          i64.load offset=16
          i64.store offset=112
          local.get $l38
          local.get $p4
          i64.load offset=8
          i64.store offset=104
          local.get $p7
          i32.const 16
          i32.add
          local.get $l41
          i32.add
          i32.const 1
          i32.store8
          local.get $p7
          local.get $l41
          i32.store offset=8
          block $B21
            local.get $l11
            local.get $l9
            f32.mul
            f32.const 0x0p+0 (;=0;)
            f32.gt
            i32.eqz
            br_if $B21
            local.get $p2
            i32.eqz
            br_if $B21
            i32.const 0
            local.set $p4
            loop $L22
              local.get $p7
              i32.const 16
              i32.add
              local.get $p4
              i32.add
              i32.load8_u
              i32.eqz
              if $I23
                local.get $l14
                local.get $p6
                local.get $p4
                i32.const 48
                i32.mul
                i32.add
                local.tee $p5
                f32.load offset=16
                local.get $p3
                i32.load offset=76
                local.tee $l42
                f32.load offset=16
                f32.sub
                f32.mul
                local.get $l13
                local.get $p5
                f32.load offset=20
                local.get $l42
                f32.load offset=20
                f32.sub
                f32.mul
                f32.add
                local.get $l10
                local.get $p5
                f32.load offset=24
                local.get $l42
                f32.load offset=24
                f32.sub
                f32.mul
                f32.add
                local.tee $l8
                local.get $l12
                local.get $l8
                local.get $l12
                f32.gt
                local.tee $p5
                select
                local.set $l12
                local.get $p4
                local.get $p1
                local.get $p5
                select
                local.set $p1
              end
              local.get $p4
              i32.const 1
              i32.add
              local.tee $p4
              local.get $p2
              i32.ne
              br_if $L22
            end
          end
          local.get $p3
          i32.load offset=76
          local.tee $p4
          local.get $p6
          local.get $p1
          i32.const 48
          i32.mul
          i32.add
          local.tee $p5
          i64.load
          i64.store offset=144
          local.get $p4
          local.get $p5
          i64.load offset=40
          i64.store offset=184
          local.get $p4
          local.get $p5
          i64.load offset=32
          i64.store offset=176
          local.get $p4
          local.get $p5
          i64.load offset=24
          i64.store offset=168
          local.get $p4
          local.get $p5
          i64.load offset=16
          i64.store offset=160
          local.get $p4
          local.get $p5
          i64.load offset=8
          i64.store offset=152
          local.get $p7
          i32.const 16
          i32.add
          local.get $p1
          i32.add
          i32.const 1
          i32.store8
          local.get $p7
          local.get $p1
          i32.store offset=12
          local.get $p2
          if $I24
            i32.const 0
            local.set $p1
            loop $L25
              block $B26
                local.get $p7
                i32.const 16
                i32.add
                local.get $p1
                i32.add
                i32.load8_u
                br_if $B26
                local.get $p6
                local.get $p7
                i32.const 3
                i32.const 2
                local.get $p6
                local.get $p1
                i32.const 48
                i32.mul
                i32.add
                local.tee $l40
                f32.load offset=16
                local.tee $l8
                local.get $p3
                i32.load offset=76
                local.tee $p4
                f32.load offset=16
                f32.sub
                local.tee $l9
                local.get $l9
                f32.mul
                local.get $l40
                f32.load offset=20
                local.tee $l9
                local.get $p4
                f32.load offset=20
                f32.sub
                local.tee $l11
                local.get $l11
                f32.mul
                f32.add
                local.get $l40
                f32.load offset=24
                local.tee $l11
                local.get $p4
                f32.load offset=24
                f32.sub
                local.tee $l12
                local.get $l12
                f32.mul
                f32.add
                local.tee $l12
                f32.const 0x1.fffffep+127 (;=3.40282e+38;)
                local.get $l12
                f32.const 0x1.fffffep+127 (;=3.40282e+38;)
                f32.lt
                select
                local.tee $l12
                local.get $l8
                local.get $p4
                i32.const -64
                i32.sub
                f32.load
                f32.sub
                local.tee $l10
                local.get $l10
                f32.mul
                local.get $l9
                local.get $p4
                f32.load offset=68
                f32.sub
                local.tee $l10
                local.get $l10
                f32.mul
                f32.add
                local.get $l11
                local.get $p4
                f32.load offset=72
                f32.sub
                local.tee $l10
                local.get $l10
                f32.mul
                f32.add
                local.tee $l10
                f32.gt
                local.tee $l39
                local.get $l10
                local.get $l12
                local.get $l39
                select
                local.tee $l12
                local.get $l8
                local.get $p4
                f32.load offset=112
                f32.sub
                local.tee $l10
                local.get $l10
                f32.mul
                local.get $l9
                local.get $p4
                f32.load offset=116
                f32.sub
                local.tee $l10
                local.get $l10
                f32.mul
                f32.add
                local.get $l11
                local.get $p4
                f32.load offset=120
                f32.sub
                local.tee $l10
                local.get $l10
                f32.mul
                f32.add
                local.tee $l10
                f32.gt
                local.tee $l39
                select
                local.get $l8
                local.get $p4
                f32.load offset=160
                f32.sub
                local.tee $l8
                local.get $l8
                f32.mul
                local.get $l9
                local.get $p4
                f32.load offset=164
                f32.sub
                local.tee $l8
                local.get $l8
                f32.mul
                f32.add
                local.get $l11
                local.get $p4
                f32.load offset=168
                f32.sub
                local.tee $l8
                local.get $l8
                f32.mul
                f32.add
                local.get $l10
                local.get $l12
                local.get $l39
                select
                f32.lt
                select
                i32.const 2
                i32.shl
                i32.or
                local.tee $p4
                i32.load
                i32.const 48
                i32.mul
                i32.add
                f32.load offset=44
                local.get $l40
                f32.load offset=44
                f32.gt
                i32.eqz
                br_if $B26
                local.get $p4
                local.get $p1
                i32.store
              end
              local.get $p1
              i32.const 1
              i32.add
              local.tee $p1
              local.get $p2
              i32.ne
              br_if $L25
            end
            local.get $p7
            i32.load offset=8
            local.set $l41
            local.get $p7
            i32.load offset=4
            local.set $l39
            local.get $p7
            i32.load
            local.set $l40
            local.get $p7
            i32.load offset=12
            local.set $p1
          end
          local.get $p3
          i32.load offset=76
          local.tee $p2
          local.get $p6
          local.get $l40
          i32.const 48
          i32.mul
          i32.add
          local.tee $p4
          i64.load
          i64.store
          local.get $p2
          local.get $p4
          i64.load offset=32
          i64.store offset=32
          local.get $p2
          local.get $p4
          i64.load offset=16
          i64.store offset=16
          local.get $p2
          local.get $p4
          i64.load offset=40
          i64.store offset=40
          local.get $p2
          local.get $p4
          i64.load offset=24
          i64.store offset=24
          local.get $p2
          local.get $p4
          i64.load offset=8
          i64.store offset=8
          local.get $p3
          i32.load offset=76
          local.tee $p2
          local.get $p6
          local.get $l39
          i32.const 48
          i32.mul
          i32.add
          local.tee $p4
          i64.load
          i64.store offset=48
          local.get $p2
          i32.const -64
          i32.sub
          local.get $p4
          i64.load offset=16
          i64.store
          local.get $p2
          local.get $p4
          i64.load offset=32
          i64.store offset=80
          local.get $p2
          local.get $p4
          i64.load offset=8
          i64.store offset=56
          local.get $p2
          local.get $p4
          i64.load offset=24
          i64.store offset=72
          local.get $p2
          local.get $p4
          i64.load offset=40
          i64.store offset=88
          local.get $p3
          i32.load offset=76
          local.tee $p2
          local.get $p6
          local.get $l41
          i32.const 48
          i32.mul
          i32.add
          local.tee $p4
          i64.load offset=8
          i64.store offset=104
          local.get $p2
          local.get $p4
          i64.load offset=40
          i64.store offset=136
          local.get $p2
          local.get $p4
          i64.load
          i64.store offset=96
          local.get $p2
          local.get $p4
          i64.load offset=16
          i64.store offset=112
          local.get $p2
          local.get $p4
          i64.load offset=24
          i64.store offset=120
          local.get $p2
          local.get $p4
          i64.load offset=32
          i64.store offset=128
          local.get $p3
          i32.load offset=76
          local.tee $p2
          local.get $p6
          local.get $p1
          i32.const 48
          i32.mul
          i32.add
          local.tee $p4
          i64.load
          i64.store offset=144
          local.get $p2
          local.get $p4
          i64.load offset=8
          i64.store offset=152
          local.get $p2
          local.get $p4
          i64.load offset=16
          i64.store offset=160
          local.get $p2
          local.get $p4
          i64.load offset=24
          i64.store offset=168
          local.get $p2
          local.get $p4
          i64.load offset=32
          i64.store offset=176
          local.get $p2
          local.get $p4
          i64.load offset=40
          i64.store offset=184
          local.get $p7
          i32.const 80
          i32.add
          global.set $g0
          i32.const 4
          local.set $p2
        end
        local.get $p3
        local.get $p2
        i32.store8 offset=64
      end
    end
    local.get $p3
    local.get $p6
    local.get $p0
    i32.const 96
    i32.add
    local.get $p0
    i32.const 112
    i32.add
    local.get $p0
    i32.const 80
    i32.add
    call $f69970
    local.get $p3
    i32.load8_u offset=64
    local.set $p3
    local.get $p0
    i32.const 144
    i32.add
    global.set $g0
    local.get $p3
    i32.const 0
    i32.ne)
