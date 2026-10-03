  (func $f72775 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 f32) (local $l3 f32) (local $l4 f32) (local $l5 f32) (local $l6 f32) (local $l7 f32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 i32)
    local.get $p1
    f32.load offset=4
    local.set $l6
    block $B0
      block $B1
        local.get $p1
        f32.load
        local.tee $l7
        f32.const 0x0p+0 (;=0;)
        f32.ne
        br_if $B1
        local.get $l6
        f32.const 0x0p+0 (;=0;)
        f32.ne
        br_if $B1
        local.get $p1
        f32.load offset=8
        f32.const 0x0p+0 (;=0;)
        f32.eq
        br_if $B0
      end
      local.get $p0
      f32.load offset=44
      local.tee $l4
      local.get $p1
      f32.load offset=8
      f32.add
      local.set $l3
      local.get $p0
      f32.load offset=40
      local.tee $l2
      local.get $l6
      f32.add
      local.set $l5
      local.get $l2
      f32.neg
      local.set $l9
      local.get $p0
      f32.load offset=36
      local.tee $l6
      f32.neg
      local.set $l14
      block $B2
        block $B3
          local.get $l7
          local.get $l6
          f32.add
          local.tee $l8
          f32.const 0x0p+0 (;=0;)
          f32.ne
          br_if $B3
          local.get $l5
          f32.const 0x0p+0 (;=0;)
          f32.ne
          br_if $B3
          local.get $l3
          f32.const 0x0p+0 (;=0;)
          f32.ne
          br_if $B3
          local.get $p0
          f32.const 0x0p+0 (;=0;)
          local.get $l4
          local.get $l4
          f32.mul
          f32.sub
          local.tee $l3
          local.get $l2
          local.get $l9
          f32.mul
          local.tee $l7
          f32.add
          local.get $p0
          f32.load offset=48
          local.tee $l5
          f32.mul
          local.get $p0
          f32.load
          f32.add
          f32.store
          local.get $p0
          local.get $l5
          local.get $l4
          f32.const 0x0p+0 (;=0;)
          f32.mul
          local.tee $l8
          local.get $l8
          f32.add
          local.get $l2
          local.get $l6
          f32.mul
          local.tee $l8
          f32.add
          f32.mul
          local.get $p0
          f32.load offset=4
          f32.add
          f32.store offset=4
          local.get $p0
          local.get $l5
          local.get $l2
          f32.const -0x0p+0 (;=-0;)
          f32.mul
          local.tee $l9
          local.get $l9
          local.get $l4
          local.get $l6
          f32.mul
          local.tee $l11
          f32.add
          f32.add
          f32.mul
          local.get $p0
          f32.load offset=8
          f32.add
          f32.store offset=8
          local.get $p0
          local.get $l5
          local.get $l4
          f32.const -0x0p+0 (;=-0;)
          f32.mul
          local.tee $l9
          local.get $l9
          f32.add
          local.get $l8
          f32.add
          f32.mul
          local.get $p0
          f32.load offset=12
          f32.add
          f32.store offset=12
          local.get $p0
          i32.const 16
          i32.add
          local.tee $l19
          local.get $l5
          local.get $l3
          local.get $l6
          local.get $l14
          f32.mul
          local.tee $l8
          f32.add
          f32.mul
          local.get $l19
          f32.load
          f32.add
          f32.store
          local.get $p0
          i32.const 20
          i32.add
          local.tee $l19
          local.get $l5
          local.get $l6
          f32.const 0x0p+0 (;=0;)
          f32.mul
          local.tee $l3
          local.get $l3
          local.get $l4
          local.get $l2
          f32.mul
          local.tee $l9
          f32.add
          f32.add
          f32.mul
          local.get $l19
          f32.load
          f32.add
          f32.store
          local.get $p0
          local.get $l5
          local.get $l2
          f32.const 0x0p+0 (;=0;)
          f32.mul
          local.tee $l3
          local.get $l3
          local.get $l11
          f32.add
          f32.add
          f32.mul
          local.get $p0
          f32.load offset=24
          f32.add
          f32.store offset=24
          local.get $p0
          i32.const 28
          i32.add
          local.tee $l19
          local.get $l5
          local.get $l6
          f32.const -0x0p+0 (;=-0;)
          f32.mul
          local.tee $l3
          local.get $l9
          local.get $l3
          f32.add
          f32.add
          f32.mul
          local.get $l19
          f32.load
          f32.add
          f32.store
          local.get $p0
          i32.const 32
          i32.add
          local.tee $l19
          local.get $l5
          local.get $l7
          local.get $l8
          f32.add
          f32.const 0x0p+0 (;=0;)
          f32.add
          f32.mul
          local.get $l19
          f32.load
          f32.add
          f32.store
          br $B2
        end
        local.get $p0
        f32.const 0x0p+0 (;=0;)
        local.get $l4
        local.get $l4
        f32.mul
        f32.sub
        local.tee $l11
        local.get $l2
        local.get $l9
        f32.mul
        local.tee $l9
        f32.add
        local.get $l5
        local.get $l5
        f32.neg
        f32.mul
        local.tee $l15
        f32.const 0x0p+0 (;=0;)
        local.get $l3
        local.get $l3
        f32.mul
        f32.sub
        local.tee $l12
        f32.add
        f32.sub
        local.get $p0
        f32.load offset=48
        local.tee $l7
        f32.mul
        local.get $p0
        f32.load
        f32.add
        f32.store
        local.get $p0
        local.get $l7
        local.get $l4
        f32.const 0x0p+0 (;=0;)
        f32.mul
        local.tee $l13
        local.get $l13
        f32.add
        local.get $l2
        local.get $l6
        f32.mul
        local.tee $l13
        f32.add
        local.get $l8
        local.get $l5
        f32.mul
        local.tee $l16
        local.get $l3
        f32.const 0x0p+0 (;=0;)
        f32.mul
        local.tee $l10
        local.get $l10
        f32.add
        f32.add
        f32.sub
        f32.mul
        local.get $p0
        f32.load offset=4
        f32.add
        f32.store offset=4
        local.get $p0
        local.get $l7
        local.get $l2
        f32.const -0x0p+0 (;=-0;)
        f32.mul
        local.tee $l10
        local.get $l10
        local.get $l4
        local.get $l6
        f32.mul
        local.tee $l17
        f32.add
        f32.add
        local.get $l5
        f32.const -0x0p+0 (;=-0;)
        f32.mul
        local.tee $l10
        local.get $l10
        local.get $l8
        local.get $l3
        f32.mul
        local.tee $l18
        f32.add
        f32.add
        f32.sub
        f32.mul
        local.get $p0
        f32.load offset=8
        f32.add
        f32.store offset=8
        local.get $p0
        local.get $l7
        local.get $l4
        f32.const -0x0p+0 (;=-0;)
        f32.mul
        local.tee $l10
        local.get $l10
        f32.add
        local.get $l13
        f32.add
        local.get $l16
        local.get $l3
        f32.const -0x0p+0 (;=-0;)
        f32.mul
        local.tee $l13
        local.get $l13
        f32.add
        f32.add
        f32.sub
        f32.mul
        local.get $p0
        f32.load offset=12
        f32.add
        f32.store offset=12
        local.get $p0
        i32.const 16
        i32.add
        local.tee $l19
        local.get $l7
        local.get $l11
        local.get $l6
        local.get $l14
        f32.mul
        local.tee $l14
        f32.add
        local.get $l8
        local.get $l8
        f32.neg
        f32.mul
        local.tee $l11
        local.get $l12
        f32.add
        f32.sub
        f32.mul
        local.get $l19
        f32.load
        f32.add
        f32.store
        local.get $p0
        i32.const 20
        i32.add
        local.tee $l19
        local.get $l7
        local.get $l6
        f32.const 0x0p+0 (;=0;)
        f32.mul
        local.tee $l12
        local.get $l12
        local.get $l4
        local.get $l2
        f32.mul
        local.tee $l4
        f32.add
        f32.add
        local.get $l8
        f32.const 0x0p+0 (;=0;)
        f32.mul
        local.tee $l12
        local.get $l12
        local.get $l5
        local.get $l3
        f32.mul
        local.tee $l3
        f32.add
        f32.add
        f32.sub
        f32.mul
        local.get $l19
        f32.load
        f32.add
        f32.store
        local.get $p0
        local.get $l7
        local.get $l2
        f32.const 0x0p+0 (;=0;)
        f32.mul
        local.tee $l2
        local.get $l2
        local.get $l17
        f32.add
        f32.add
        local.get $l5
        f32.const 0x0p+0 (;=0;)
        f32.mul
        local.tee $l2
        local.get $l2
        local.get $l18
        f32.add
        f32.add
        f32.sub
        f32.mul
        local.get $p0
        f32.load offset=24
        f32.add
        f32.store offset=24
        local.get $p0
        i32.const 28
        i32.add
        local.tee $l19
        local.get $l7
        local.get $l6
        f32.const -0x0p+0 (;=-0;)
        f32.mul
        local.tee $l2
        local.get $l4
        local.get $l2
        f32.add
        f32.add
        local.get $l8
        f32.const -0x0p+0 (;=-0;)
        f32.mul
        local.tee $l2
        local.get $l2
        local.get $l3
        f32.add
        f32.add
        f32.sub
        f32.mul
        local.get $l19
        f32.load
        f32.add
        f32.store
        local.get $p0
        i32.const 32
        i32.add
        local.tee $l19
        local.get $l7
        local.get $l9
        local.get $l14
        f32.add
        f32.const 0x0p+0 (;=0;)
        f32.add
        local.get $l11
        local.get $l15
        f32.add
        f32.const 0x0p+0 (;=0;)
        f32.add
        f32.sub
        f32.mul
        local.get $l19
        f32.load
        f32.add
        f32.store
        local.get $p0
        f32.load offset=44
        local.set $l4
        local.get $p0
        f32.load offset=40
        local.set $l2
      end
      local.get $p0
      local.get $l6
      local.get $p1
      f32.load
      f32.add
      f32.store offset=36
      local.get $p0
      local.get $p1
      f32.load offset=4
      local.get $l2
      f32.add
      f32.store offset=40
      local.get $p0
      local.get $p1
      f32.load offset=8
      local.get $l4
      f32.add
      f32.store offset=44
    end)