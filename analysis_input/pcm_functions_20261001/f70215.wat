  (func $f70215 (type $t10) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (result i32)
    (local $l6 i32) (local $l7 f32) (local $l8 f32) (local $l9 i64)
    global.get $g0
    i32.const 4288
    i32.sub
    local.tee $l6
    global.set $g0
    local.get $p3
    f32.load offset=24
    local.set $l7
    local.get $p3
    i64.load offset=16 align=4
    local.set $l9
    local.get $p2
    f32.load offset=4
    local.set $l8
    local.get $l6
    i32.const -1
    i32.store offset=4232
    local.get $l6
    local.get $l8
    f32.store offset=52
    i32.const 0
    local.set $p3
    local.get $l6
    i32.const 0
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
    local.get $l6
    i32.const 0
    i32.store offset=4144
    local.get $l6
    local.get $l7
    f32.store offset=40
    local.get $l6
    local.get $l9
    i64.store offset=32
    local.get $l6
    i64.const 4575657221408423936
    i64.store offset=24
    local.get $l6
    i64.const 0
    i64.store offset=16
    local.get $l6
    i32.const 1065353216
    i32.store offset=8
    local.get $l6
    i64.const 0
    i64.store
    block $B0
      local.get $l6
      i32.const 4232
      i32.add
      local.get $l6
      i32.const 4176
      i32.add
      local.get $l6
      i32.const 16
      i32.add
      local.get $p5
      local.get $l6
      local.get $l6
      i32.const 48
      i32.add
      i32.const 0
      call $f70177
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
    i32.const 4288
    i32.add
    global.set $g0
    local.get $p3)
