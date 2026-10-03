  (func $f69972 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 f32) (local $l3 f32) (local $l4 f32) (local $l5 f32) (local $l6 f32) (local $l7 f32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32)
    block $B0
      local.get $p1
      f32.load offset=8
      local.tee $l2
      f32.abs
      f32.const 0x1.fff2e4p-1 (;=0.9999;)
      f32.lt
      if $I1
        local.get $l2
        f32.const 0x1p+0 (;=1;)
        local.get $l2
        f32.const 0x1p+0 (;=1;)
        f32.add
        f32.div
        local.tee $l3
        local.get $p1
        f32.load
        local.tee $l5
        local.get $l5
        f32.mul
        f32.mul
        f32.add
        local.set $l4
        local.get $l2
        local.get $p1
        f32.load offset=4
        local.tee $l6
        local.get $l3
        local.get $l6
        f32.neg
        local.tee $l9
        f32.mul
        local.tee $l8
        f32.mul
        f32.sub
        local.set $l3
        local.get $l5
        f32.neg
        local.set $l7
        local.get $l8
        local.get $l5
        f32.mul
        local.tee $l8
        local.set $l10
        br $B0
      end
      f32.const 0x1p+0 (;=1;)
      local.get $p1
      f32.load offset=4
      f32.sub
      local.tee $l4
      f32.const 0x0p+0 (;=0;)
      local.get $p1
      f32.load
      f32.sub
      local.tee $l3
      f32.const -0x1p+1 (;=-2;)
      f32.const 0x0p+0 (;=0;)
      local.get $l2
      f32.sub
      local.tee $l2
      local.get $l2
      f32.mul
      local.get $l3
      local.get $l3
      f32.mul
      local.get $l4
      local.get $l4
      f32.mul
      f32.add
      f32.add
      f32.div
      local.tee $l5
      f32.mul
      local.tee $l11
      f32.mul
      local.get $l3
      local.get $l3
      f32.const 0x0p+0 (;=0;)
      f32.mul
      local.get $l4
      f32.add
      local.get $l2
      f32.sub
      local.get $l5
      f32.neg
      f32.mul
      local.tee $l6
      f32.mul
      local.tee $l12
      f32.add
      local.set $l8
      local.get $l4
      local.get $l2
      local.get $l5
      f32.mul
      local.tee $l7
      f32.mul
      local.get $l2
      local.get $l6
      f32.mul
      local.tee $l13
      f32.add
      f32.const 0x1p+0 (;=1;)
      f32.add
      local.set $l9
      local.get $l2
      local.get $l4
      local.get $l5
      f32.mul
      local.tee $l14
      f32.mul
      local.get $l4
      local.get $l6
      f32.mul
      local.tee $l15
      f32.sub
      f32.const 0x1p+0 (;=1;)
      f32.add
      local.set $l6
      local.get $l3
      local.get $l14
      f32.mul
      local.get $l15
      f32.const 0x0p+0 (;=0;)
      f32.mul
      f32.add
      local.set $l10
      local.get $l2
      local.get $l11
      f32.mul
      local.get $l12
      f32.sub
      f32.const 0x0p+0 (;=0;)
      f32.add
      local.set $l5
      local.get $l2
      local.get $l7
      f32.mul
      local.get $l13
      f32.sub
      f32.const -0x1p+0 (;=-1;)
      f32.add
      f32.const 0x1p+0 (;=1;)
      f32.add
      local.set $l2
      local.get $l3
      local.get $l7
      f32.mul
      local.get $l13
      f32.const 0x0p+0 (;=0;)
      f32.mul
      f32.add
      f32.const 0x0p+0 (;=0;)
      f32.add
      local.set $l7
      local.get $l4
      local.get $l14
      f32.mul
      local.get $l15
      f32.add
      f32.const -0x1p+0 (;=-1;)
      f32.add
      f32.const 0x1p+0 (;=1;)
      f32.add
      local.set $l4
      local.get $l3
      local.get $l11
      f32.mul
      local.get $l12
      f32.const 0x0p+0 (;=0;)
      f32.mul
      f32.add
      f32.const 0x1p+0 (;=1;)
      f32.add
      local.set $l3
    end
    local.get $p0
    local.get $l7
    f32.store offset=32
    local.get $p0
    local.get $l10
    f32.store offset=16
    local.get $p0
    i32.const 0
    i32.store offset=12
    local.get $p0
    local.get $l5
    f32.store offset=8
    local.get $p0
    local.get $l8
    f32.store offset=4
    local.get $p0
    local.get $l3
    f32.store
    local.get $p0
    i32.const 0
    i32.store offset=44
    local.get $p0
    local.get $l2
    f32.store offset=40
    local.get $p0
    local.get $l9
    f32.store offset=36
    local.get $p0
    i32.const 0
    i32.store offset=28
    local.get $p0
    local.get $l6
    f32.store offset=24
    local.get $p0
    local.get $l4
    f32.store offset=20)
