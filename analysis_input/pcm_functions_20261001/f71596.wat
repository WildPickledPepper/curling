  (func $f71596 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l2
    global.set $g0
    local.get $p0
    local.get $p1
    f32.load
    f32.store offset=16
    local.get $p0
    local.get $p1
    f32.load offset=4
    f32.store offset=20
    local.get $p0
    local.get $p1
    f32.load offset=8
    f32.store offset=24
    local.get $p0
    local.get $p1
    f32.load offset=12
    f32.store offset=28
    local.get $p0
    local.get $p1
    f32.load offset=16
    f32.store offset=32
    local.get $p0
    local.get $p1
    f32.load offset=20
    f32.store offset=36
    local.get $p0
    local.get $p1
    f32.load offset=24
    f32.store offset=40
    local.get $p0
    i32.load
    local.tee $p0
    if $I0
      local.get $p0
      local.get $p0
      i32.load offset=100
      local.tee $p1
      f32.load
      f32.store offset=64
      local.get $p0
      local.get $p1
      f32.load offset=4
      f32.store offset=68
      local.get $p0
      local.get $p1
      f32.load offset=8
      f32.store offset=72
      local.get $p0
      local.get $p1
      f32.load offset=12
      f32.store offset=76
      local.get $p0
      local.get $p1
      f32.load offset=16
      f32.store offset=80
      local.get $p0
      local.get $p1
      f32.load offset=20
      f32.store offset=84
      local.get $p0
      local.get $p1
      f32.load offset=24
      f32.store offset=88
      local.get $p0
      call $f71729
      local.get $p0
      i32.load offset=40
      i32.load offset=1012
      local.set $p1
      local.get $p0
      i32.load offset=44
      i32.load8_u offset=9
      local.set $l3
      local.get $l2
      local.get $p0
      i64.load offset=144
      i64.store offset=8
      local.get $p1
      local.get $l3
      i32.const 2
      i32.eq
      local.get $l2
      i32.const 8
      i32.add
      local.get $p1
      i32.load
      i32.load offset=44
      call_indirect $__indirect_function_table (type $t2)
    end
    local.get $l2
    i32.const 16
    i32.add
    global.set $g0)