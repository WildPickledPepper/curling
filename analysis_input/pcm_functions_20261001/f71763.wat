  (func $f71763 (type $t2) (param $p0 i32) (param $p1 i32) (param $p2 i32)
    (local $l3 i32) (local $l4 i32)
    global.get $g0
    i32.const 32
    i32.sub
    local.tee $l3
    global.set $g0
    local.get $l3
    local.get $p1
    f32.load
    f32.store
    local.get $l3
    local.get $p1
    f32.load offset=4
    f32.store offset=4
    local.get $l3
    local.get $p1
    f32.load offset=8
    f32.store offset=8
    local.get $l3
    local.get $p1
    f32.load offset=12
    f32.store offset=12
    local.get $l3
    local.get $p1
    f32.load offset=16
    f32.store offset=16
    local.get $l3
    local.get $p1
    f32.load offset=20
    f32.store offset=20
    local.get $l3
    i32.const 1
    i32.store8 offset=24
    local.get $p2
    local.get $l3
    call $f69806
    local.get $p1
    i32.load offset=24
    local.tee $l4
    i32.const 1
    i32.and
    i32.eqz
    if $I0
      local.get $p0
      local.get $p0
      local.get $l4
      i32.const 1
      i32.shr_u
      i32.const 28
      i32.mul
      i32.add
      local.get $p2
      call $f71763
      local.get $p0
      local.get $p0
      local.get $p1
      i32.load offset=24
      i32.const 1
      i32.shr_u
      i32.const 28
      i32.mul
      i32.add
      i32.const 28
      i32.add
      i32.const 0
      local.get $p0
      select
      local.get $p2
      call $f71763
    end
    local.get $l3
    i32.const 32
    i32.add
    global.set $g0)