  (func $f71759 (type $t4) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32)
    (local $l4 i32) (local $l5 i32) (local $l6 f32) (local $l7 f32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32)
    local.get $p0
    i32.load offset=24
    local.tee $l4
    i32.const 1
    i32.shr_u
    local.set $l5
    block $B0
      local.get $l4
      i32.const 1
      i32.and
      if $I1
        local.get $l5
        i32.const 15
        i32.and
        local.tee $p3
        i32.eqz
        if $I2
          f32.const 0x1.c162fep+53 (;=1.58114e+16;)
          local.set $l9
          f32.const -0x1.c162fep+53 (;=-1.58114e+16;)
          local.set $l7
          f32.const -0x1.c162fep+53 (;=-1.58114e+16;)
          local.set $l10
          f32.const -0x1.c162fep+53 (;=-1.58114e+16;)
          local.set $l11
          f32.const 0x1.c162fep+53 (;=1.58114e+16;)
          local.set $l8
          f32.const 0x1.c162fep+53 (;=1.58114e+16;)
          local.set $l12
          br $B0
        end
        local.get $p1
        local.get $p2
        local.get $l4
        i32.const 3
        i32.shr_u
        i32.const 536870908
        i32.and
        i32.add
        local.tee $p2
        i32.load
        i32.const 24
        i32.mul
        i32.add
        local.tee $l4
        f32.load offset=12
        local.set $l13
        local.get $l4
        f32.load offset=8
        local.set $l12
        local.get $l4
        f32.load offset=4
        local.set $l8
        local.get $l4
        f32.load
        local.set $l9
        local.get $l4
        f32.load offset=20
        local.set $l11
        local.get $l4
        f32.load offset=16
        local.set $l10
        local.get $p3
        i32.const 1
        i32.eq
        if $I3
          local.get $l13
          local.set $l7
          br $B0
        end
        local.get $p2
        i32.const 4
        i32.add
        local.set $l5
        local.get $p2
        local.get $p3
        i32.const 2
        i32.shl
        i32.add
        local.set $p3
        local.get $l4
        f32.load offset=24
        local.set $l14
        local.get $l13
        local.set $l7
        loop $L4
          local.get $l7
          local.get $p1
          local.get $l5
          i32.load
          i32.const 24
          i32.mul
          i32.add
          local.tee $l4
          f32.load offset=12
          local.tee $l6
          local.get $l6
          local.get $l7
          f32.lt
          select
          local.set $l7
          local.get $l13
          local.get $l6
          local.get $l6
          local.get $l13
          f32.gt
          select
          local.set $l13
          local.get $l12
          local.get $l4
          f32.load offset=8
          local.tee $l6
          local.get $l6
          local.get $l12
          f32.gt
          select
          local.set $l12
          local.get $l8
          local.get $l4
          f32.load offset=4
          local.tee $l6
          local.get $l6
          local.get $l8
          f32.gt
          select
          local.set $l8
          local.get $l9
          local.get $l4
          f32.load
          local.tee $l6
          local.get $l6
          local.get $l9
          f32.gt
          select
          local.set $l9
          local.get $l14
          local.get $l4
          f32.load offset=24
          local.tee $l6
          local.get $l6
          local.get $l14
          f32.lt
          select
          local.set $l14
          local.get $l11
          local.get $l4
          f32.load offset=20
          local.tee $l6
          local.get $l6
          local.get $l11
          f32.lt
          select
          local.set $l11
          local.get $l10
          local.get $l4
          f32.load offset=16
          local.tee $l6
          local.get $l6
          local.get $l10
          f32.lt
          select
          local.set $l10
          local.get $l5
          i32.const 4
          i32.add
          local.tee $l5
          local.get $p3
          i32.ne
          br_if $L4
        end
        br $B0
      end
      local.get $p3
      local.get $l5
      i32.const 28
      i32.mul
      i32.add
      local.tee $l4
      f32.load
      local.tee $l6
      local.get $l4
      f32.load offset=28
      local.tee $l9
      local.get $l6
      local.get $l9
      f32.lt
      select
      local.set $l9
      local.get $l4
      f32.load offset=20
      local.tee $l6
      local.get $l4
      f32.load offset=48
      local.tee $l7
      local.get $l6
      local.get $l7
      f32.gt
      select
      local.set $l11
      local.get $l4
      f32.load offset=16
      local.tee $l6
      local.get $l4
      f32.load offset=44
      local.tee $l7
      local.get $l6
      local.get $l7
      f32.gt
      select
      local.set $l10
      local.get $l4
      f32.load offset=12
      local.tee $l6
      local.get $l4
      f32.load offset=40
      local.tee $l7
      local.get $l6
      local.get $l7
      f32.gt
      select
      local.set $l7
      local.get $l4
      f32.load offset=8
      local.tee $l6
      local.get $l4
      f32.load offset=36
      local.tee $l8
      local.get $l6
      local.get $l8
      f32.lt
      select
      local.set $l12
      local.get $l4
      f32.load offset=4
      local.tee $l6
      local.get $l4
      f32.load offset=32
      local.tee $l8
      local.get $l6
      local.get $l8
      f32.lt
      select
      local.set $l8
    end
    local.get $p0
    local.get $l7
    f32.store offset=12
    local.get $p0
    local.get $l12
    f32.store offset=8
    local.get $p0
    local.get $l8
    f32.store offset=4
    local.get $p0
    local.get $l9
    f32.store
    local.get $p0
    local.get $l11
    f32.store offset=20
    local.get $p0
    local.get $l10
    f32.store offset=16)