  (func $f70047 (type $t2) (param $p0 i32) (param $p1 i32) (param $p2 i32)
    (local $l3 f32) (local $l4 f32) (local $l5 f32) (local $l6 f32) (local $l7 f32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 i32)
    local.get $p1
    i32.load offset=76
    local.tee $l14
    f32.load offset=32
    local.tee $l7
    local.set $l3
    local.get $l14
    f32.load offset=36
    local.tee $l8
    local.set $l4
    local.get $l14
    f32.load offset=40
    local.tee $l5
    local.set $l6
    block $B0
      local.get $p1
      i32.load8_u offset=64
      local.tee $p1
      i32.const 2
      i32.lt_u
      br_if $B0
      i32.const 1
      local.set $l13
      local.get $p1
      i32.const 1
      i32.sub
      local.tee $l15
      i32.const 1
      i32.and
      local.set $l16
      local.get $l5
      local.set $l6
      local.get $l8
      local.set $l4
      local.get $l7
      local.set $l3
      local.get $p1
      i32.const 2
      i32.ne
      if $I1
        local.get $l15
        i32.const -2
        i32.and
        local.set $l15
        loop $L2
          local.get $l3
          local.get $l14
          local.get $l13
          i32.const 48
          i32.mul
          i32.add
          local.tee $p1
          f32.load offset=32
          f32.add
          local.get $p1
          f32.load offset=80
          f32.add
          local.set $l3
          local.get $l6
          local.get $p1
          f32.load offset=40
          f32.add
          local.get $p1
          f32.load offset=88
          f32.add
          local.set $l6
          local.get $l4
          local.get $p1
          f32.load offset=36
          f32.add
          local.get $p1
          f32.load offset=84
          f32.add
          local.set $l4
          local.get $l13
          i32.const 2
          i32.add
          local.set $l13
          local.get $l15
          i32.const 2
          i32.sub
          local.tee $l15
          br_if $L2
        end
      end
      local.get $l16
      i32.eqz
      br_if $B0
      local.get $l3
      local.get $l14
      local.get $l13
      i32.const 48
      i32.mul
      i32.add
      local.tee $p1
      f32.load offset=32
      f32.add
      local.set $l3
      local.get $l4
      local.get $p1
      f32.load offset=36
      f32.add
      local.set $l4
      local.get $l6
      local.get $p1
      f32.load offset=40
      f32.add
      local.set $l6
    end
    local.get $p2
    f32.load offset=4
    local.set $l10
    local.get $p2
    f32.load offset=8
    local.set $l11
    local.get $p2
    f32.load
    local.set $l12
    local.get $p2
    f32.load offset=12
    local.set $l9
    local.get $p0
    i32.const 0
    i32.store offset=12
    local.get $p0
    local.get $l11
    local.get $l12
    local.get $l3
    local.get $l7
    local.get $l3
    local.get $l3
    f32.mul
    local.get $l4
    local.get $l4
    f32.mul
    f32.add
    local.get $l6
    local.get $l6
    f32.mul
    f32.add
    f32.const 0x1p-23 (;=1.19209e-07;)
    f32.gt
    local.tee $p1
    select
    local.tee $l3
    f32.mul
    local.get $l10
    local.get $l4
    local.get $l8
    local.get $p1
    select
    local.tee $l4
    f32.mul
    f32.add
    local.get $l11
    local.get $l6
    local.get $l5
    local.get $p1
    select
    local.tee $l6
    f32.mul
    f32.add
    local.tee $l7
    f32.mul
    local.get $l9
    local.get $l4
    local.get $l12
    f32.mul
    local.get $l3
    local.get $l10
    f32.mul
    f32.sub
    f32.mul
    local.get $l6
    local.get $l9
    local.get $l9
    f32.mul
    f32.const -0x1p-1 (;=-0.5;)
    f32.add
    local.tee $l8
    f32.mul
    f32.add
    f32.add
    local.tee $l5
    local.get $l5
    f32.add
    local.tee $l5
    f32.const 0x1p+0 (;=1;)
    local.get $l5
    local.get $l5
    f32.mul
    local.get $l12
    local.get $l7
    f32.mul
    local.get $l9
    local.get $l6
    local.get $l10
    f32.mul
    local.get $l4
    local.get $l11
    f32.mul
    f32.sub
    f32.mul
    local.get $l3
    local.get $l8
    f32.mul
    f32.add
    f32.add
    local.tee $l5
    local.get $l5
    f32.add
    local.tee $l5
    local.get $l5
    f32.mul
    local.get $l10
    local.get $l7
    f32.mul
    local.get $l9
    local.get $l3
    local.get $l11
    f32.mul
    local.get $l6
    local.get $l12
    f32.mul
    f32.sub
    f32.mul
    local.get $l4
    local.get $l8
    f32.mul
    f32.add
    f32.add
    local.tee $l3
    local.get $l3
    f32.add
    local.tee $l3
    local.get $l3
    f32.mul
    f32.add
    f32.add
    f32.sqrt
    f32.div
    local.tee $l4
    f32.mul
    f32.store offset=8
    local.get $p0
    local.get $l3
    local.get $l4
    f32.mul
    f32.store offset=4
    local.get $p0
    local.get $l5
    local.get $l4
    f32.mul
    f32.store)