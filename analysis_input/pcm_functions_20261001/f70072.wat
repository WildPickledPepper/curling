  (func $f70072 (type $t14) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 i32) (result i32)
    (local $l7 f32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 i32)
    i32.const 1
    local.set $l11
    block $B0
      local.get $p1
      f32.load offset=16
      local.get $p0
      f32.load offset=16
      f32.sub
      local.tee $l8
      local.get $l8
      f32.neg
      local.tee $l7
      local.get $l7
      local.get $l8
      f32.lt
      select
      local.tee $l8
      local.get $p1
      f32.load offset=20
      local.get $p0
      f32.load offset=20
      f32.sub
      local.tee $l7
      local.get $l7
      f32.neg
      local.tee $l9
      local.get $l7
      local.get $l9
      f32.gt
      select
      local.tee $l7
      local.get $l7
      local.get $l8
      f32.le
      select
      local.tee $l9
      local.get $l8
      f32.const 0x0p+0 (;=0;)
      local.get $p1
      f32.load offset=24
      local.get $p0
      f32.load offset=24
      f32.sub
      local.tee $l7
      local.get $l7
      f32.neg
      local.tee $l10
      local.get $l7
      local.get $l10
      f32.gt
      select
      f32.const 0x0p+0 (;=0;)
      f32.ge
      select
      local.tee $l8
      local.get $l8
      local.get $l9
      f32.le
      select
      local.get $p0
      i32.load8_u offset=64
      i32.const 2
      i32.shl
      local.tee $p1
      i32.const 3124080
      i32.add
      f32.load
      local.get $p4
      f32.load
      f32.mul
      local.tee $l8
      f32.gt
      br_if $B0
      local.get $p1
      i32.const 3124112
      i32.add
      f32.load
      local.tee $l9
      local.get $p2
      f32.load
      local.get $p0
      f32.load offset=32
      f32.mul
      local.get $p2
      f32.load offset=4
      local.get $p0
      f32.load offset=36
      f32.mul
      f32.add
      local.get $p2
      f32.load offset=8
      local.get $p0
      f32.load offset=40
      f32.mul
      f32.add
      local.get $p2
      f32.load offset=12
      local.get $p0
      f32.load offset=44
      f32.mul
      f32.add
      local.tee $l7
      f32.gt
      br_if $B0
      local.get $l9
      local.get $p3
      f32.load
      local.get $p0
      f32.load offset=48
      f32.mul
      local.get $p3
      f32.load offset=4
      local.get $p0
      f32.load offset=52
      f32.mul
      f32.add
      local.get $p3
      f32.load offset=8
      local.get $p0
      f32.load offset=56
      f32.mul
      f32.add
      local.get $p3
      f32.load offset=12
      local.get $p0
      f32.load offset=60
      f32.mul
      f32.add
      local.tee $l10
      f32.gt
      br_if $B0
      f32.const 0x0p+0 (;=0;)
      local.set $l9
      local.get $l7
      f32.const 0x1p+0 (;=1;)
      f32.lt
      if $I1 (result f32)
        local.get $l7
        f32.const -0x1p+0 (;=-1;)
        f32.max
        f32.const 0x1p+0 (;=1;)
        f32.min
        call $f35882
      else
        local.get $l9
      end
      local.get $p5
      f32.load
      f32.mul
      local.get $l8
      f32.gt
      local.get $l10
      f32.const 0x1p+0 (;=1;)
      f32.lt
      if $I2 (result f32)
        local.get $l10
        f32.const -0x1p+0 (;=-1;)
        f32.max
        f32.const 0x1p+0 (;=1;)
        f32.min
        call $f35882
      else
        local.get $l9
      end
      local.get $p6
      f32.load
      f32.mul
      local.get $l8
      f32.gt
      i32.or
      local.set $l11
    end
    local.get $l11)