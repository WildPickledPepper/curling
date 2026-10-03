  (func $f69992 (type $t0) (param $p0 i32) (param $p1 i32) (result i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32)
    global.get $g0
    i32.const -64
    i32.add
    local.tee $l2
    global.set $g0
    block $B0 (result i32)
      local.get $p0
      i32.load offset=64
      local.tee $l4
      if $I1
        local.get $l4
        local.get $p1
        i32.const 12
        i32.mul
        i32.add
        local.tee $l3
        i32.load offset=8
        local.set $l5
        local.get $l3
        i32.load
        local.set $l6
        local.get $l3
        i32.load offset=4
        br $B0
      end
      local.get $p0
      i32.load offset=68
      local.get $p1
      i32.const 6
      i32.mul
      i32.add
      local.tee $l3
      i32.load16_u offset=4
      local.set $l5
      local.get $l3
      i32.load16_u
      local.set $l6
      local.get $l3
      i32.load16_u offset=2
    end
    local.set $l4
    local.get $p0
    i32.load offset=72
    local.tee $l3
    local.get $l4
    i32.const 12
    i32.mul
    i32.add
    local.tee $l4
    f32.load offset=8
    local.set $l16
    local.get $l3
    local.get $l5
    i32.const 12
    i32.mul
    i32.add
    local.tee $l5
    f32.load offset=8
    local.set $l17
    local.get $l3
    local.get $l6
    i32.const 12
    i32.mul
    i32.add
    local.tee $l3
    f32.load offset=8
    local.set $l15
    local.get $l2
    local.get $l4
    f32.load
    local.get $l3
    f32.load
    local.tee $l14
    f32.sub
    local.tee $l20
    local.get $l5
    f32.load offset=4
    local.get $l3
    f32.load offset=4
    local.tee $l18
    f32.sub
    local.tee $l19
    f32.mul
    local.get $l4
    f32.load offset=4
    local.get $l18
    f32.sub
    local.tee $l18
    local.get $l5
    f32.load
    local.get $l14
    f32.sub
    local.tee $l21
    f32.mul
    f32.sub
    local.tee $l14
    f32.store offset=56
    local.get $l2
    local.get $l16
    local.get $l15
    f32.sub
    local.tee $l16
    local.get $l21
    f32.mul
    local.get $l20
    local.get $l17
    local.get $l15
    f32.sub
    local.tee $l17
    f32.mul
    f32.sub
    local.tee $l15
    f32.store offset=52
    local.get $l2
    local.get $l18
    local.get $l17
    f32.mul
    local.get $l16
    local.get $l19
    f32.mul
    f32.sub
    local.tee $l16
    f32.store offset=48
    block $B2
      local.get $p0
      i32.load offset=96
      if $I3
        i32.const 0
        local.set $l6
        local.get $l16
        local.get $p0
        f32.load offset=32
        f32.mul
        local.get $l15
        local.get $p0
        f32.load offset=36
        f32.mul
        f32.add
        local.get $l14
        local.get $p0
        f32.load offset=40
        f32.mul
        f32.add
        f32.const 0x0p+0 (;=0;)
        f32.gt
        br_if $B2
      end
      local.get $l2
      local.get $l3
      f32.load
      f32.store offset=8
      local.get $l2
      local.get $l3
      i32.const 4
      i32.add
      local.tee $l7
      f32.load
      f32.store offset=12
      local.get $l2
      local.get $l3
      i32.const 8
      i32.add
      local.tee $l8
      f32.load
      f32.store offset=16
      local.get $l2
      local.get $l4
      f32.load
      f32.store offset=20
      local.get $l2
      local.get $l4
      i32.const 4
      i32.add
      local.tee $l9
      f32.load
      f32.store offset=24
      local.get $l2
      local.get $l4
      i32.const 8
      i32.add
      local.tee $l10
      f32.load
      f32.store offset=28
      local.get $l2
      local.get $l5
      f32.load
      f32.store offset=32
      local.get $l2
      local.get $l5
      i32.const 4
      i32.add
      local.tee $l11
      f32.load
      f32.store offset=36
      local.get $l2
      local.get $l5
      i32.const 8
      i32.add
      local.tee $l12
      f32.load
      f32.store offset=40
      local.get $l14
      local.get $l14
      f32.mul
      local.get $l16
      local.get $l16
      f32.mul
      local.get $l15
      local.get $l15
      f32.mul
      f32.add
      f32.add
      f32.sqrt
      local.tee $l17
      f32.const 0x0p+0 (;=0;)
      f32.gt
      if $I4
        local.get $l2
        local.get $l14
        f32.const 0x1p+0 (;=1;)
        local.get $l17
        f32.div
        local.tee $l17
        f32.mul
        f32.store offset=56
        local.get $l2
        local.get $l15
        local.get $l17
        f32.mul
        f32.store offset=52
        local.get $l2
        local.get $l16
        local.get $l17
        f32.mul
        f32.store offset=48
      end
      i32.const 0
      local.set $l6
      local.get $l2
      i32.const 8
      i32.add
      local.get $l2
      i32.const 48
      i32.add
      local.get $p0
      i32.const 48
      i32.add
      local.get $p0
      f32.load offset=76
      local.get $p0
      i32.const 32
      i32.add
      local.get $l2
      i32.const 4
      i32.add
      local.get $l2
      i32.const 3
      i32.add
      i32.const 1
      call $f69960
      i32.eqz
      br_if $B2
      local.get $l2
      f32.load offset=4
      local.tee $l14
      local.get $p0
      f32.load offset=160
      f32.gt
      br_if $B2
      local.get $l2
      f32.load offset=48
      local.tee $l17
      local.get $p0
      f32.load offset=32
      f32.mul
      local.get $l2
      f32.load offset=52
      local.tee $l20
      local.get $p0
      f32.load offset=36
      f32.mul
      f32.add
      local.get $l2
      f32.load offset=56
      local.tee $l18
      local.get $p0
      f32.load offset=40
      f32.mul
      f32.add
      f32.abs
      f32.neg
      local.set $l16
      block $B5
        local.get $p0
        f32.load offset=156
        local.tee $l15
        local.get $l14
        local.get $l15
        local.get $l14
        local.get $l15
        f32.gt
        local.tee $l13
        select
        f32.const 0x1p+0 (;=1;)
        f32.max
        f32.const 0x1.0624dep-10 (;=0.001;)
        f32.mul
        local.tee $l19
        f32.sub
        local.get $l14
        f32.gt
        br_if $B5
        local.get $l16
        local.get $p0
        f32.load offset=152
        local.tee $l21
        f32.lt
        local.get $l15
        local.get $l19
        f32.add
        local.get $l14
        f32.gt
        i32.and
        br_if $B5
        local.get $l14
        f32.const 0x0p+0 (;=0;)
        f32.eq
        br_if $B5
        local.get $l16
        local.get $l21
        f32.eq
        local.get $l14
        local.get $l15
        f32.lt
        i32.and
        i32.eqz
        br_if $B2
      end
      local.get $p0
      local.get $l14
      f32.store offset=88
      local.get $p0
      local.get $p1
      i32.store offset=92
      local.get $p0
      local.get $l3
      f32.load
      f32.store offset=104
      local.get $p0
      local.get $l7
      f32.load
      f32.store offset=108
      local.get $p0
      local.get $l8
      f32.load
      f32.store offset=112
      local.get $p0
      local.get $l4
      f32.load
      f32.store offset=116
      local.get $p0
      local.get $l9
      f32.load
      f32.store offset=120
      local.get $p0
      local.get $l10
      f32.load
      f32.store offset=124
      local.get $p0
      local.get $l5
      f32.load
      f32.store offset=128
      local.get $p0
      local.get $l11
      f32.load
      f32.store offset=132
      local.get $l12
      f32.load
      local.set $l19
      local.get $p0
      local.get $l15
      local.get $l14
      local.get $l13
      select
      f32.store offset=156
      local.get $p0
      local.get $l19
      f32.store offset=136
      local.get $p0
      local.get $l16
      f32.store offset=152
      local.get $p0
      local.get $l18
      f32.store offset=148
      local.get $p0
      local.get $l20
      f32.store offset=144
      local.get $p0
      local.get $l17
      f32.store offset=140
      i32.const 1
      local.set $l6
    end
    local.get $l2
    i32.const -64
    i32.sub
    global.set $g0
    local.get $l6)
