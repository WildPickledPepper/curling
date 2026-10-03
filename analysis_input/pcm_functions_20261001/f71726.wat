  (func $f71726 (type $t3) (param $p0 i32) (param $p1 i32) (param $p2 i32) (result i32)
    (local $l3 i32)
    local.get $p0
    i64.const 0
    i64.store offset=20 align=4
    local.get $p0
    i32.const 3156420
    i32.store
    local.get $p0
    local.get $p2
    i32.store offset=44
    local.get $p0
    local.get $p1
    i32.store offset=40
    local.get $p0
    i64.const 0
    i64.store offset=28 align=4
    local.get $p0
    i32.const 0
    i32.store offset=36
    local.get $p2
    local.get $p0
    i32.store
    local.get $p0
    i32.const 3172120
    i32.store
    local.get $p1
    i32.load offset=2372
    local.tee $p1
    i32.load offset=12
    local.tee $p2
    if $I0
      local.get $p1
      i32.load offset=8
      local.get $p2
      i32.const 1
      i32.sub
      local.tee $p2
      i32.const 2
      i32.shl
      i32.add
      i32.load
      local.set $l3
      local.get $p1
      local.get $p2
      i32.store offset=12
      local.get $p0
      local.get $l3
      i32.store offset=48
      local.get $p0
      return
    end
    local.get $p1
    local.get $p1
    i32.load offset=4
    local.tee $p2
    i32.const 1
    i32.add
    i32.store offset=4
    local.get $p0
    local.get $p2
    i32.store offset=48
    local.get $p0)