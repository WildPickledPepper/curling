  (func $f71703 (type $t8) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (result i32)
    (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i64)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l4
    global.set $g0
    local.get $p1
    i32.load offset=4
    local.set $l5
    local.get $p2
    i32.load offset=4
    local.set $l6
    local.get $p0
    i32.const -1
    i32.store offset=36
    local.get $p0
    local.get $p2
    i32.store offset=32
    local.get $p0
    local.get $p1
    i32.store offset=28
    local.get $p0
    i32.const 0
    i32.store8 offset=26
    local.get $p0
    i32.const 1282
    i32.store16 offset=24
    local.get $p0
    i32.const -1
    i32.store offset=20
    local.get $p0
    i64.const -1
    i64.store offset=12 align=4
    local.get $p0
    local.get $l6
    i32.store offset=8
    local.get $p0
    local.get $l5
    i32.store offset=4
    local.get $p0
    i32.const 3171888
    i32.store
    block $B0
      local.get $p3
      br_if $B0
      local.get $p0
      i32.const 4
      i32.add
      local.tee $p2
      call $f71361
      drop
      local.get $p0
      i32.load offset=4
      local.get $p2
      call $f71333
      local.get $p0
      i32.load offset=8
      local.get $p2
      call $f71333
      local.get $p0
      i32.load offset=4
      i32.load offset=40
      local.get $p2
      i32.const 0
      call $f71383
      local.get $p0
      i32.load offset=4
      i32.load offset=40
      i32.load offset=2168
      local.set $p3
      local.get $l4
      local.get $p0
      i32.load offset=28
      local.tee $p2
      local.get $p0
      i32.load offset=32
      local.tee $p1
      local.get $p1
      local.get $p2
      i32.lt_u
      local.tee $l5
      select
      i32.store offset=4
      local.get $l4
      local.get $p1
      local.get $p2
      local.get $l5
      select
      i32.store
      local.get $p3
      i32.const 1956
      i32.add
      local.get $l4
      local.get $l4
      i32.const 15
      i32.add
      call $f71694
      local.set $p2
      local.get $l4
      i32.load8_u offset=15
      br_if $B0
      local.get $l4
      i64.load
      local.set $l7
      local.get $p2
      local.get $p0
      i32.store offset=8
      local.get $p2
      local.get $l7
      i64.store align=4
    end
    local.get $l4
    i32.const 16
    i32.add
    global.set $g0
    local.get $p0)