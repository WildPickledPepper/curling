  (func $f70225 (type $t10) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (result i32)
    (local $l6 i32) (local $l7 f32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32)
    global.get $g0
    i32.const 4320
    i32.sub
    local.tee $l6
    global.set $g0
    local.get $p3
    f32.load offset=20
    local.set $l7
    local.get $p3
    f32.load offset=16
    local.set $l9
    local.get $l6
    local.get $p3
    f32.load offset=24
    local.tee $l15
    local.get $p2
    f32.load offset=8
    local.tee $l10
    local.get $p3
    f32.load
    local.tee $l11
    local.get $l11
    f32.add
    local.tee $l12
    local.get $p3
    f32.load offset=8
    local.tee $l8
    f32.mul
    local.get $p3
    f32.load offset=12
    local.tee $l13
    local.get $l13
    f32.add
    local.tee $l14
    local.get $p3
    f32.load offset=4
    local.tee $l16
    f32.mul
    f32.sub
    f32.mul
    local.tee $l17
    f32.sub
    f32.store offset=20
    local.get $l6
    local.get $l7
    local.get $l10
    local.get $l8
    local.get $l14
    f32.mul
    local.get $l12
    local.get $l16
    f32.mul
    f32.add
    f32.mul
    local.tee $l8
    f32.sub
    f32.store offset=16
    local.get $l6
    local.get $l17
    local.get $l15
    f32.add
    f32.store offset=8
    local.get $l6
    local.get $l7
    local.get $l8
    f32.add
    f32.store offset=4
    local.get $l6
    local.get $l9
    local.get $l10
    local.get $l11
    local.get $l12
    f32.mul
    local.get $l13
    local.get $l14
    f32.mul
    f32.const -0x1p+0 (;=-1;)
    f32.add
    f32.add
    f32.mul
    local.tee $l7
    f32.sub
    f32.store offset=12
    local.get $l6
    local.get $l9
    local.get $l7
    f32.add
    f32.store
    local.get $l6
    local.get $p2
    f32.load offset=4
    f32.store offset=24
    local.get $l6
    i32.const 4288
    i32.add
    local.get $l6
    local.get $l6
    i32.const 12
    i32.add
    local.get $l6
    i32.const 4316
    i32.add
    call $f69767
    local.get $l6
    i32.const -1
    i32.store offset=4232
    local.get $l6
    local.get $l6
    f32.load offset=4316
    f32.store offset=56
    local.get $l6
    local.get $l6
    f32.load offset=24
    f32.store offset=52
    local.get $l6
    i32.const 2
    i32.store offset=48
    local.get $l6
    i32.const 4232
    i32.add
    local.get $l6
    i32.const 48
    i32.add
    call $f70398
    local.get $l6
    i32.const -1
    i32.store offset=4176
    local.get $l6
    i32.const 4176
    i32.add
    local.get $p4
    call $f70398
    local.get $l6
    i64.const 0
    i64.store offset=4168
    i32.const 0
    local.set $p3
    local.get $l6
    i32.const 0
    i32.store offset=4144
    local.get $l6
    i32.const 1065353216
    i32.store offset=40
    local.get $l6
    i64.const 0
    i64.store offset=32
    block $B0
      local.get $l6
      i32.const 4232
      i32.add
      local.get $l6
      i32.const 4176
      i32.add
      local.get $l6
      i32.const 4288
      i32.add
      local.get $p5
      local.get $l6
      i32.const 32
      i32.add
      local.get $l6
      i32.const 48
      i32.add
      call $f70191
      i32.eqz
      br_if $B0
      local.get $p0
      local.get $p1
      local.get $l6
      i32.load offset=4144
      local.get $l6
      i32.const 48
      i32.add
      call $f70216
      i32.eqz
      br_if $B0
      local.get $l6
      i32.load offset=4144
      i32.const 0
      i32.ne
      local.set $p3
    end
    local.get $l6
    i32.const 4320
    i32.add
    global.set $g0
    local.get $p3)
