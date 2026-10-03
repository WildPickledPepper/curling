  (func $f70060 (type $t3) (param $p0 i32) (param $p1 i32) (param $p2 i32) (result i32)
    (local $l3 f32) (local $l4 f32) (local $l5 f32) (local $l6 f32) (local $l7 f32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 i32)
    local.get $p2
    f32.load
    local.tee $l3
    local.get $p1
    i32.load offset=36
    local.tee $p1
    f32.load
    f32.mul
    local.get $p2
    f32.load offset=4
    local.tee $l4
    local.get $p1
    f32.load offset=4
    f32.mul
    f32.add
    local.get $p2
    f32.load offset=8
    local.tee $l6
    local.get $p1
    f32.load offset=8
    f32.mul
    f32.add
    local.tee $l7
    local.get $p0
    i32.load offset=24
    local.tee $l13
    f32.load
    f32.mul
    local.get $l3
    local.get $p1
    f32.load offset=16
    f32.mul
    local.get $l4
    local.get $p1
    f32.load offset=20
    f32.mul
    f32.add
    local.get $l6
    local.get $p1
    f32.load offset=24
    f32.mul
    f32.add
    local.tee $l5
    local.get $l13
    f32.load offset=4
    f32.mul
    f32.add
    local.get $l3
    local.get $p1
    f32.load offset=32
    f32.mul
    local.get $l4
    local.get $p1
    f32.load offset=36
    f32.mul
    f32.add
    local.get $l6
    local.get $p1
    f32.load offset=40
    f32.mul
    f32.add
    local.tee $l8
    local.get $l13
    f32.load offset=8
    f32.mul
    f32.add
    local.set $l3
    block $B0
      local.get $p0
      i32.load offset=16
      local.tee $p1
      i32.const 2
      i32.lt_u
      br_if $B0
      i32.const 1
      local.set $p2
      local.get $p1
      i32.const 1
      i32.sub
      local.tee $l12
      i32.const 1
      i32.and
      local.set $l16
      block $B1
        local.get $p1
        i32.const 2
        i32.eq
        if $I2
          br $B1
        end
        local.get $l12
        i32.const -2
        i32.and
        local.set $l12
        loop $L3
          local.get $l7
          local.get $l13
          local.get $p2
          i32.const 20
          i32.mul
          i32.add
          local.tee $p1
          f32.load offset=20
          f32.mul
          local.get $l5
          local.get $p1
          f32.load offset=24
          f32.mul
          f32.add
          local.get $l8
          local.get $p1
          f32.load offset=28
          f32.mul
          f32.add
          local.tee $l4
          local.get $l7
          local.get $p1
          f32.load
          f32.mul
          local.get $l5
          local.get $p1
          f32.load offset=4
          f32.mul
          f32.add
          local.get $l8
          local.get $p1
          f32.load offset=8
          f32.mul
          f32.add
          local.tee $l6
          local.get $l3
          local.get $l3
          local.get $l6
          f32.gt
          local.tee $p1
          select
          local.tee $l3
          local.get $l3
          local.get $l4
          f32.gt
          local.tee $l15
          select
          local.set $l3
          local.get $p2
          i32.const 1
          i32.add
          local.get $p2
          local.get $l14
          local.get $p1
          select
          local.get $l15
          select
          local.set $l14
          local.get $p2
          i32.const 2
          i32.add
          local.set $p2
          local.get $l12
          i32.const 2
          i32.sub
          local.tee $l12
          br_if $L3
        end
      end
      local.get $l16
      i32.eqz
      br_if $B0
      local.get $l7
      local.get $l13
      local.get $p2
      i32.const 20
      i32.mul
      i32.add
      local.tee $p1
      f32.load
      f32.mul
      local.get $l5
      local.get $p1
      f32.load offset=4
      f32.mul
      f32.add
      local.get $l8
      local.get $p1
      f32.load offset=8
      f32.mul
      f32.add
      local.tee $l4
      local.get $l3
      local.get $l3
      local.get $l4
      f32.gt
      local.tee $p1
      select
      local.set $l3
      local.get $p2
      local.get $l14
      local.get $p1
      select
      local.set $l14
    end
    block $B4
      local.get $p0
      i32.load offset=20
      local.tee $l16
      i32.eqz
      br_if $B4
      local.get $l5
      f32.neg
      local.set $l9
      local.get $p0
      i32.load offset=36
      local.set $p0
      local.get $l3
      local.get $l3
      f32.mul
      local.set $l3
      i32.const 0
      local.set $p1
      i32.const -1
      local.set $l15
      loop $L5
        local.get $l3
        local.get $l13
        local.get $p0
        local.get $p1
        i32.const 1
        i32.shl
        local.tee $l12
        i32.add
        i32.load8_u
        i32.const 20
        i32.mul
        i32.add
        local.tee $p2
        f32.load offset=4
        local.get $l13
        local.get $p0
        local.get $l12
        i32.const 1
        i32.or
        i32.add
        i32.load8_u
        i32.const 20
        i32.mul
        i32.add
        local.tee $l12
        f32.load offset=4
        f32.add
        local.tee $l5
        local.get $l9
        f32.mul
        local.get $l7
        local.get $p2
        f32.load
        local.get $l12
        f32.load
        f32.add
        local.tee $l4
        f32.mul
        f32.sub
        local.get $l8
        local.get $p2
        f32.load offset=8
        local.get $l12
        f32.load offset=8
        f32.add
        local.tee $l6
        f32.mul
        f32.sub
        local.tee $l10
        local.get $l10
        f32.mul
        local.tee $l11
        local.get $l4
        local.get $l4
        f32.mul
        local.get $l5
        local.get $l5
        f32.mul
        f32.add
        local.get $l6
        local.get $l6
        f32.mul
        f32.add
        local.tee $l5
        f32.div
        local.get $l10
        f32.const 0x0p+0 (;=0;)
        f32.ge
        i32.eqz
        local.get $l11
        local.get $l3
        local.get $l5
        f32.mul
        f32.gt
        i32.eqz
        i32.or
        local.tee $p2
        select
        local.set $l3
        local.get $l15
        local.get $p1
        local.get $p2
        select
        local.set $l15
        local.get $p1
        i32.const 1
        i32.add
        local.tee $p1
        local.get $l16
        i32.ne
        br_if $L5
      end
      local.get $l15
      i32.const -1
      i32.eq
      br_if $B4
      local.get $p0
      local.get $l15
      i32.const 1
      i32.shl
      local.tee $p1
      i32.add
      i32.load8_u
      local.tee $p2
      local.get $p0
      local.get $p1
      i32.const 1
      i32.or
      i32.add
      i32.load8_u
      local.tee $l12
      local.get $l13
      local.get $p2
      i32.const 20
      i32.mul
      i32.add
      local.tee $p1
      f32.load offset=4
      local.get $l9
      f32.mul
      local.get $l7
      local.get $p1
      f32.load
      f32.mul
      f32.sub
      local.get $l8
      local.get $p1
      f32.load offset=8
      f32.mul
      f32.sub
      local.get $l13
      local.get $l12
      i32.const 20
      i32.mul
      i32.add
      local.tee $p1
      f32.load offset=4
      local.get $l9
      f32.mul
      local.get $l7
      local.get $p1
      f32.load
      f32.mul
      f32.sub
      local.get $l8
      local.get $p1
      f32.load offset=8
      f32.mul
      f32.sub
      f32.gt
      select
      local.set $l14
    end
    local.get $l14)