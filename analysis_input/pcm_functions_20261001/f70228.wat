  (func $f70228 (type $t10) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (result i32)
    (local $l6 i32) (local $l7 f32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32)
    global.get $g0
    i32.const 4288
    i32.sub
    local.tee $l6
    global.set $g0
    local.get $p3
    f32.load offset=4
    local.tee $l9
    local.get $l9
    f32.add
    local.tee $l7
    local.get $p3
    f32.load offset=8
    local.tee $l8
    f32.mul
    local.tee $l12
    local.get $p3
    f32.load
    local.tee $l13
    local.get $l13
    f32.add
    local.tee $l10
    local.get $p3
    f32.load offset=12
    local.tee $l11
    f32.mul
    local.tee $l15
    f32.sub
    local.set $l16
    local.get $l10
    local.get $l8
    f32.mul
    local.tee $l14
    local.get $l7
    local.get $l11
    f32.mul
    local.tee $l19
    f32.add
    local.set $l17
    local.get $l12
    local.get $l15
    f32.add
    local.set $l12
    local.get $l10
    local.get $l9
    f32.mul
    local.tee $l15
    local.get $l8
    local.get $l8
    f32.add
    local.tee $l20
    local.get $l11
    f32.mul
    local.tee $l11
    f32.sub
    local.set $l18
    local.get $l14
    local.get $l19
    f32.sub
    local.set $l14
    local.get $l15
    local.get $l11
    f32.add
    local.set $l11
    f32.const 0x1p+0 (;=1;)
    local.get $l13
    local.get $l10
    f32.mul
    f32.sub
    local.tee $l10
    local.get $l8
    local.get $l20
    f32.mul
    local.tee $l13
    f32.sub
    local.set $l8
    f32.const 0x1p+0 (;=1;)
    local.get $l9
    local.get $l7
    f32.mul
    local.tee $l7
    f32.sub
    local.get $l13
    f32.sub
    local.set $l9
    local.get $p3
    f32.load offset=24
    local.set $l13
    local.get $p3
    f32.load offset=20
    local.set $l15
    local.get $p2
    f32.load offset=12
    local.set $l19
    local.get $p2
    f32.load offset=8
    local.set $l20
    local.get $p2
    f32.load offset=4
    local.set $l21
    local.get $p3
    f32.load offset=16
    local.set $l22
    block $B0 (result f32)
      local.get $l10
      local.get $l7
      f32.sub
      local.tee $l10
      f32.const 0x0p+0 (;=0;)
      f32.lt
      if $I1
        local.get $l8
        local.get $l9
        f32.lt
        if $I2
          local.get $l12
          local.get $l16
          f32.sub
          f32.const 0x1p-1 (;=0.5;)
          local.get $l9
          f32.const 0x1p+0 (;=1;)
          f32.add
          local.get $l8
          f32.sub
          local.get $l10
          f32.sub
          local.tee $l12
          f32.sqrt
          f32.div
          local.tee $l7
          f32.mul
          local.set $l8
          local.get $l17
          local.get $l14
          f32.add
          local.get $l7
          f32.mul
          local.set $l9
          local.get $l11
          local.get $l18
          f32.add
          local.get $l7
          f32.mul
          local.set $l10
          local.get $l12
          local.get $l7
          f32.mul
          br $B0
        end
        local.get $l17
        local.get $l14
        f32.sub
        f32.const 0x1p-1 (;=0.5;)
        local.get $l8
        f32.const 0x1p+0 (;=1;)
        local.get $l9
        f32.sub
        f32.add
        local.get $l10
        f32.sub
        local.tee $l10
        f32.sqrt
        f32.div
        local.tee $l7
        f32.mul
        local.set $l8
        local.get $l12
        local.get $l16
        f32.add
        local.get $l7
        f32.mul
        local.set $l9
        local.get $l10
        local.get $l7
        f32.mul
        local.set $l10
        local.get $l11
        local.get $l18
        f32.add
        local.get $l7
        f32.mul
        br $B0
      end
      local.get $l8
      f32.neg
      local.get $l9
      f32.gt
      if $I3
        local.get $l11
        local.get $l18
        f32.sub
        f32.const 0x1p-1 (;=0.5;)
        local.get $l10
        f32.const 0x1p+0 (;=1;)
        local.get $l9
        f32.sub
        local.get $l8
        f32.sub
        f32.add
        local.tee $l9
        f32.sqrt
        f32.div
        local.tee $l7
        f32.mul
        local.set $l8
        local.get $l9
        local.get $l7
        f32.mul
        local.set $l9
        local.get $l12
        local.get $l16
        f32.add
        local.get $l7
        f32.mul
        local.set $l10
        local.get $l17
        local.get $l14
        f32.add
        local.get $l7
        f32.mul
        br $B0
      end
      local.get $l10
      local.get $l8
      local.get $l9
      f32.const 0x1p+0 (;=1;)
      f32.add
      f32.add
      f32.add
      local.tee $l8
      f32.const 0x1p-1 (;=0.5;)
      local.get $l8
      f32.sqrt
      f32.div
      local.tee $l7
      f32.mul
      local.set $l8
      local.get $l11
      local.get $l18
      f32.sub
      local.get $l7
      f32.mul
      local.set $l9
      local.get $l17
      local.get $l14
      f32.sub
      local.get $l7
      f32.mul
      local.set $l10
      local.get $l12
      local.get $l16
      f32.sub
      local.get $l7
      f32.mul
    end
    local.set $l7
    local.get $l6
    i32.const 4280
    i32.add
    local.get $l13
    f32.store
    local.get $l6
    i32.const 4276
    i32.add
    local.get $l15
    f32.store
    local.get $l6
    local.get $l22
    f32.store offset=4272
    local.get $l6
    local.get $l8
    f32.store offset=4268
    local.get $l6
    local.get $l9
    f32.store offset=4264
    local.get $l6
    local.get $l10
    f32.store offset=4260
    local.get $l6
    local.get $l7
    f32.store offset=4256
    local.get $l6
    i32.const -1
    i32.store offset=4200
    local.get $l6
    local.get $l19
    f32.store offset=28
    local.get $l6
    local.get $l20
    f32.store offset=24
    local.get $l6
    local.get $l21
    f32.store offset=20
    local.get $l6
    i32.const 3
    i32.store offset=16
    local.get $l6
    i32.const 4200
    i32.add
    local.get $l6
    i32.const 16
    i32.add
    call $f70398
    local.get $l6
    i32.const -1
    i32.store offset=4144
    local.get $l6
    i32.const 4144
    i32.add
    local.get $p4
    call $f70398
    local.get $l6
    i64.const 0
    i64.store offset=4136
    i32.const 0
    local.set $p3
    local.get $l6
    i32.const 0
    i32.store offset=4112
    local.get $l6
    i32.const 1065353216
    i32.store offset=8
    local.get $l6
    i64.const 0
    i64.store
    block $B4
      local.get $l6
      i32.const 4200
      i32.add
      local.get $l6
      i32.const 4144
      i32.add
      local.get $l6
      i32.const 4256
      i32.add
      local.get $p5
      local.get $l6
      local.get $l6
      i32.const 16
      i32.add
      call $f70202
      i32.eqz
      br_if $B4
      local.get $p0
      local.get $p1
      local.get $l6
      i32.load offset=4112
      local.get $l6
      i32.const 16
      i32.add
      call $f70216
      i32.eqz
      br_if $B4
      local.get $l6
      i32.load offset=4112
      i32.const 0
      i32.ne
      local.set $p3
    end
    local.get $l6
    i32.const 4288
    i32.add
    global.set $g0
    local.get $p3)
