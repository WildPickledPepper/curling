  (func $f71777 (type $t528) (param $p0 i32) (param $p1 f32) (param $p2 f32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 i32) (param $p7 i32) (param $p8 i32) (param $p9 i32)
    (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32) (local $l33 i64)
    global.get $g0
    i32.const 160
    i32.sub
    local.tee $l10
    global.set $g0
    local.get $p0
    i32.const 0
    i32.store offset=16
    local.get $p0
    i64.const 0
    i64.store offset=8 align=4
    local.get $p0
    i64.const 0
    i64.store align=4
    local.get $l10
    i64.const 2122317823
    i64.store offset=104
    local.get $l10
    i64.const 4269801471
    i64.store offset=24
    local.get $l10
    i64.const 2122317823
    i64.store offset=120
    local.get $l10
    i64.const 4269801471
    i64.store offset=40
    local.get $l10
    i64.const 2122317823
    i64.store offset=136
    local.get $l10
    i64.const 4269801471
    i64.store offset=56
    local.get $l10
    i64.const 2122317823
    i64.store offset=152
    local.get $l10
    i64.const 2122317823
    i64.store offset=88
    local.get $l10
    i64.const 9115285643625234431
    i64.store offset=80
    local.get $l10
    i64.const 4269801471
    i64.store offset=8
    local.get $l10
    i64.const -108086391082057729
    i64.store
    local.get $l10
    i64.const 9115285643625234431
    i64.store offset=96
    local.get $l10
    i64.const -108086391082057729
    i64.store offset=16
    local.get $l10
    i64.const 9115285643625234431
    i64.store offset=112
    local.get $l10
    i64.const -108086391082057729
    i64.store offset=32
    local.get $l10
    i64.const 9115285643625234431
    i64.store offset=128
    local.get $l10
    i64.const -108086391082057729
    i64.store offset=48
    local.get $l10
    i64.const 9115285643625234431
    i64.store offset=144
    local.get $l10
    i64.const 4269801471
    i64.store offset=72
    local.get $l10
    i64.const -108086391082057729
    i64.store offset=64
    block $B0 (result i32)
      local.get $p3
      if $I1
        i32.const 16
        i32.const 0
        local.get $p8
        select
        local.set $l15
        i32.const 2
        i32.const 1
        local.get $p9
        i32.const 1
        i32.eq
        select
        i32.const 2
        i32.shl
        local.set $l14
        loop $L2
          local.get $l10
          local.get $p4
          local.get $l12
          i32.const 5
          i32.shl
          i32.add
          local.tee $p9
          local.get $l14
          i32.add
          f32.load
          local.tee $l16
          local.get $p9
          i32.const 16
          i32.add
          local.get $l14
          i32.add
          f32.load
          local.tee $l17
          f32.sub
          local.get $p2
          f32.gt
          i32.const 2
          i32.shl
          local.get $l15
          i32.or
          local.get $l16
          local.get $l17
          f32.add
          local.get $p2
          f32.lt
          i32.const 3
          i32.shl
          i32.or
          local.get $p9
          f32.load
          local.tee $l17
          local.get $p9
          f32.load offset=16
          local.tee $l18
          f32.sub
          local.tee $l16
          local.get $p1
          f32.gt
          i32.or
          local.get $l17
          local.get $l18
          f32.add
          local.tee $l17
          local.get $p1
          f32.lt
          i32.const 1
          i32.shl
          i32.or
          i32.const 3176464
          i32.add
          i32.load8_u
          local.tee $l13
          i32.const 4
          i32.shl
          local.tee $l11
          i32.add
          local.tee $p8
          f32.load
          local.set $l18
          local.get $p8
          f32.load offset=4
          local.set $l19
          local.get $p8
          f32.load offset=8
          local.set $l20
          local.get $p8
          f32.load offset=12
          local.set $l21
          local.get $l10
          i32.const 80
          i32.add
          local.get $l11
          i32.add
          local.tee $l11
          f32.load
          local.set $l24
          local.get $l11
          f32.load offset=4
          local.set $l25
          local.get $l11
          f32.load offset=8
          local.set $l22
          local.get $p9
          f32.load offset=4
          local.set $l26
          local.get $p9
          f32.load offset=20
          local.set $l27
          local.get $p9
          f32.load offset=8
          local.set $l28
          local.get $p9
          f32.load offset=24
          local.set $l29
          local.get $l11
          local.get $l11
          f32.load offset=12
          local.tee $l23
          local.get $p9
          f32.load offset=12
          local.tee $l30
          local.get $p9
          f32.load offset=28
          local.tee $l31
          f32.sub
          local.tee $l32
          local.get $l23
          local.get $l32
          f32.lt
          select
          f32.store offset=12
          local.get $l11
          local.get $l22
          local.get $l28
          local.get $l29
          f32.sub
          local.tee $l23
          local.get $l22
          local.get $l23
          f32.lt
          select
          f32.store offset=8
          local.get $l11
          local.get $l25
          local.get $l26
          local.get $l27
          f32.sub
          local.tee $l22
          local.get $l22
          local.get $l25
          f32.gt
          select
          f32.store offset=4
          local.get $l11
          local.get $l24
          local.get $l16
          local.get $l16
          local.get $l24
          f32.gt
          select
          f32.store
          local.get $p8
          local.get $l21
          local.get $l30
          local.get $l31
          f32.add
          local.tee $l16
          local.get $l16
          local.get $l21
          f32.lt
          select
          f32.store offset=12
          local.get $p8
          local.get $l20
          local.get $l28
          local.get $l29
          f32.add
          local.tee $l16
          local.get $l16
          local.get $l20
          f32.lt
          select
          f32.store offset=8
          local.get $p8
          local.get $l19
          local.get $l26
          local.get $l27
          f32.add
          local.tee $l16
          local.get $l16
          local.get $l19
          f32.lt
          select
          f32.store offset=4
          local.get $p8
          local.get $l18
          local.get $l17
          local.get $l17
          local.get $l18
          f32.lt
          select
          f32.store
          local.get $p9
          local.get $l13
          i32.store offset=12
          local.get $p0
          local.get $l13
          i32.const 2
          i32.shl
          i32.add
          local.tee $p9
          local.get $p9
          i32.load
          i32.const 1
          i32.add
          i32.store
          local.get $l12
          i32.const 1
          i32.add
          local.tee $l12
          local.get $p3
          i32.ne
          br_if $L2
        end
        local.get $p0
        i32.load
        local.tee $p9
        local.get $p0
        i32.load offset=4
        i32.add
        local.tee $p8
        local.get $p0
        i32.load offset=8
        i32.add
        local.tee $l12
        local.get $p0
        i32.load offset=12
        i32.add
        br $B0
      end
      i32.const 0
      local.set $p8
      i32.const 0
      local.set $p9
      i32.const 0
    end
    local.set $l13
    i32.const 0
    local.set $l11
    local.get $p0
    i32.const 0
    i32.store offset=20
    local.get $p0
    local.get $l13
    i32.store offset=36
    local.get $p0
    local.get $l12
    i32.store offset=32
    local.get $p0
    local.get $p8
    i32.store offset=28
    local.get $p0
    local.get $p9
    i32.store offset=24
    local.get $p0
    local.get $p3
    if $I3 (result i32)
      loop $L4
        local.get $p0
        local.get $p4
        local.get $l11
        i32.const 5
        i32.shl
        i32.add
        local.tee $p9
        i32.load offset=12
        local.tee $l13
        i32.const 2
        i32.shl
        i32.add
        i32.const 20
        i32.add
        local.tee $p8
        local.get $p8
        i32.load
        local.tee $l12
        i32.const 1
        i32.add
        i32.store
        local.get $p9
        i64.load align=4
        local.set $l33
        local.get $p9
        f32.load offset=8
        local.set $l16
        local.get $p6
        local.get $l12
        i32.const 5
        i32.shl
        i32.add
        local.tee $p8
        local.get $l13
        i32.store offset=12
        local.get $p8
        local.get $l16
        f32.store offset=8
        local.get $p8
        local.get $l33
        i64.store
        local.get $p9
        i64.load offset=16 align=4
        local.set $l33
        local.get $p8
        local.get $p9
        i64.load offset=24 align=4
        i64.store offset=24
        local.get $p8
        local.get $l33
        i64.store offset=16
        local.get $p7
        local.get $l12
        i32.const 3
        i32.shl
        i32.add
        local.get $p5
        local.get $l11
        i32.const 3
        i32.shl
        i32.add
        i64.load align=4
        i64.store align=4
        local.get $l11
        i32.const 1
        i32.add
        local.tee $l11
        local.get $p3
        i32.ne
        br_if $L4
      end
      local.get $p0
      i32.load
      local.tee $p9
      local.get $p0
      i32.load offset=4
      i32.add
      local.tee $p8
      local.get $p0
      i32.load offset=8
      i32.add
      local.tee $l12
      local.get $p0
      i32.load offset=12
      i32.add
    else
      local.get $l13
    end
    i32.store offset=36
    local.get $p0
    local.get $l12
    i32.store offset=32
    local.get $p0
    local.get $p8
    i32.store offset=28
    local.get $p0
    local.get $p9
    i32.store offset=24
    local.get $p0
    i32.const 0
    i32.store offset=20
    local.get $l10
    f32.load
    local.set $l16
    local.get $l10
    f32.load offset=80
    local.set $l17
    local.get $l10
    f32.load offset=4
    local.set $l18
    local.get $l10
    f32.load offset=84
    local.set $l19
    local.get $p0
    local.get $l10
    f32.load offset=8
    local.tee $l20
    local.get $l10
    f32.load offset=88
    local.tee $l21
    f32.sub
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.store offset=72
    local.get $p0
    local.get $l18
    local.get $l19
    f32.sub
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.store offset=68
    local.get $p0
    i32.const -64
    i32.sub
    local.get $l16
    local.get $l17
    f32.sub
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.store
    local.get $p0
    local.get $l21
    local.get $l20
    f32.add
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.store offset=56
    local.get $p0
    local.get $l19
    local.get $l18
    f32.add
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.store offset=52
    local.get $p0
    local.get $l17
    local.get $l16
    f32.add
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.store offset=48
    local.get $l10
    f32.load offset=16
    local.set $l16
    local.get $l10
    f32.load offset=96
    local.set $l17
    local.get $l10
    f32.load offset=20
    local.set $l18
    local.get $l10
    f32.load offset=100
    local.set $l19
    local.get $p0
    local.get $l10
    f32.load offset=24
    local.tee $l20
    local.get $l10
    f32.load offset=104
    local.tee $l21
    f32.sub
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.store offset=104
    local.get $p0
    local.get $l18
    local.get $l19
    f32.sub
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.store offset=100
    local.get $p0
    local.get $l16
    local.get $l17
    f32.sub
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.store offset=96
    local.get $p0
    local.get $l21
    local.get $l20
    f32.add
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.store offset=88
    local.get $p0
    local.get $l19
    local.get $l18
    f32.add
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.store offset=84
    local.get $p0
    local.get $l17
    local.get $l16
    f32.add
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.store offset=80
    local.get $l10
    f32.load offset=32
    local.set $l16
    local.get $l10
    f32.load offset=112
    local.set $l17
    local.get $l10
    f32.load offset=36
    local.set $l18
    local.get $l10
    f32.load offset=116
    local.set $l19
    local.get $p0
    local.get $l10
    f32.load offset=40
    local.tee $l20
    local.get $l10
    f32.load offset=120
    local.tee $l21
    f32.sub
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.store offset=136
    local.get $p0
    local.get $l18
    local.get $l19
    f32.sub
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.store offset=132
    local.get $p0
    local.get $l16
    local.get $l17
    f32.sub
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.store offset=128
    local.get $p0
    local.get $l21
    local.get $l20
    f32.add
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.store offset=120
    local.get $p0
    local.get $l19
    local.get $l18
    f32.add
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.store offset=116
    local.get $p0
    local.get $l17
    local.get $l16
    f32.add
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.store offset=112
    local.get $l10
    f32.load offset=48
    local.set $l16
    local.get $l10
    f32.load offset=128
    local.set $l17
    local.get $l10
    f32.load offset=52
    local.set $l18
    local.get $l10
    f32.load offset=132
    local.set $l19
    local.get $p0
    local.get $l10
    f32.load offset=56
    local.tee $l20
    local.get $l10
    f32.load offset=136
    local.tee $l21
    f32.sub
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.store offset=168
    local.get $p0
    local.get $l18
    local.get $l19
    f32.sub
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.store offset=164
    local.get $p0
    local.get $l16
    local.get $l17
    f32.sub
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.store offset=160
    local.get $p0
    local.get $l21
    local.get $l20
    f32.add
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.store offset=152
    local.get $p0
    local.get $l19
    local.get $l18
    f32.add
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.store offset=148
    local.get $p0
    local.get $l17
    local.get $l16
    f32.add
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.store offset=144
    local.get $l10
    f32.load offset=64
    local.set $l16
    local.get $l10
    f32.load offset=144
    local.set $l17
    local.get $l10
    f32.load offset=68
    local.set $l18
    local.get $l10
    f32.load offset=148
    local.set $l19
    local.get $p0
    local.get $l10
    f32.load offset=72
    local.tee $l20
    local.get $l10
    f32.load offset=152
    local.tee $l21
    f32.sub
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.store offset=200
    local.get $p0
    local.get $l18
    local.get $l19
    f32.sub
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.store offset=196
    local.get $p0
    local.get $l16
    local.get $l17
    f32.sub
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.store offset=192
    local.get $p0
    local.get $l21
    local.get $l20
    f32.add
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.store offset=184
    local.get $p0
    local.get $l19
    local.get $l18
    f32.add
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.store offset=180
    local.get $p0
    local.get $l17
    local.get $l16
    f32.add
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.store offset=176
    local.get $l10
    i32.const 160
    i32.add
    global.set $g0)
