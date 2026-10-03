  (func $f70443 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 f32) (local $l4 f32) (local $l5 f32) (local $l6 f32) (local $l7 f32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32)
    local.get $p1
    local.get $p0
    i32.load offset=16
    local.tee $l2
    f32.load offset=16
    local.tee $l10
    f32.const 0x0p+0 (;=0;)
    f32.mul
    local.tee $l5
    local.get $l2
    f32.load offset=12
    local.tee $l11
    f32.const 0x0p+0 (;=0;)
    f32.mul
    local.tee $l3
    local.get $l2
    f32.load offset=8
    local.tee $l12
    f32.const 0x0p+0 (;=0;)
    f32.mul
    local.tee $l7
    f32.const 0x0p+0 (;=0;)
    f32.mul
    local.tee $l8
    f32.add
    f32.add
    local.tee $l4
    local.get $p0
    i32.load offset=12
    local.tee $l2
    f32.load offset=16
    local.get $l2
    f32.load offset=28
    f32.sub
    local.tee $l13
    f32.mul
    local.get $l3
    f32.const 0x0p+0 (;=0;)
    f32.mul
    local.tee $l9
    local.get $l7
    f32.add
    local.get $l5
    f32.add
    local.tee $l6
    local.get $l2
    f32.load offset=20
    local.get $l2
    f32.load offset=32
    f32.sub
    local.tee $l14
    f32.mul
    f32.add
    local.get $l10
    local.get $l9
    local.get $l8
    f32.add
    f32.add
    local.tee $l15
    local.get $l2
    f32.load offset=24
    local.get $l2
    f32.load offset=36
    f32.sub
    local.tee $l10
    f32.mul
    f32.add
    f32.store offset=8
    local.get $p1
    local.get $l3
    local.get $l7
    f32.add
    local.get $l5
    f32.const 0x0p+0 (;=0;)
    f32.mul
    local.tee $l3
    f32.add
    local.tee $l5
    local.get $l13
    f32.mul
    local.get $l12
    local.get $l9
    f32.add
    local.get $l3
    f32.add
    local.tee $l12
    local.get $l14
    f32.mul
    f32.add
    local.get $l6
    local.get $l10
    f32.mul
    f32.add
    local.tee $l9
    f32.store offset=4
    local.get $p1
    local.get $l11
    local.get $l8
    f32.add
    local.get $l3
    f32.add
    local.tee $l11
    local.get $l13
    f32.mul
    local.get $l5
    local.get $l14
    f32.mul
    f32.add
    local.get $l4
    local.get $l10
    f32.mul
    f32.add
    f32.store
    local.get $p1
    local.get $l4
    local.get $p0
    i32.load offset=12
    local.tee $l2
    f32.load offset=16
    local.get $l2
    f32.load offset=28
    f32.add
    local.tee $l3
    f32.mul
    local.get $l6
    local.get $l2
    f32.load offset=20
    local.get $l2
    f32.load offset=32
    f32.add
    local.tee $l7
    f32.mul
    f32.add
    local.get $l15
    local.get $l2
    f32.load offset=24
    local.get $l2
    f32.load offset=36
    f32.add
    local.tee $l8
    f32.mul
    f32.add
    f32.store offset=20
    local.get $p1
    local.get $l5
    local.get $l3
    f32.mul
    local.get $l12
    local.get $l7
    f32.mul
    f32.add
    local.get $l6
    local.get $l8
    f32.mul
    f32.add
    local.tee $l6
    f32.store offset=16
    local.get $p1
    local.get $l11
    local.get $l3
    f32.mul
    local.get $l5
    local.get $l7
    f32.mul
    f32.add
    local.get $l4
    local.get $l8
    f32.mul
    f32.add
    f32.store offset=12
    local.get $l9
    local.get $l6
    f32.sub
    f32.const 0x1.0624dep-11 (;=0.0005;)
    f32.add
    local.tee $l4
    f32.const 0x0p+0 (;=0;)
    f32.gt
    if $I0
      local.get $p1
      local.get $l9
      local.get $l4
      f32.const 0x1.333334p-1 (;=0.6;)
      f32.mul
      local.tee $l4
      f32.sub
      f32.store offset=4
      local.get $p1
      local.get $l6
      local.get $l4
      f32.add
      f32.store offset=16
    end)
