  (func $f71732 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32)
    local.get $p1
    i32.load offset=48
    local.set $l3
    local.get $p1
    i32.const -1
    i32.store offset=48
    local.get $p0
    i32.load
    local.tee $l2
    local.get $l3
    i32.const 2
    i32.shl
    local.tee $p1
    i32.add
    local.get $p0
    i32.load offset=4
    i32.const 2
    i32.shl
    local.get $l2
    i32.add
    i32.const 4
    i32.sub
    i32.load
    i32.store
    local.get $p0
    i32.load offset=24
    local.tee $l2
    local.get $p1
    i32.add
    local.get $p0
    i32.load offset=28
    i32.const 2
    i32.shl
    local.get $l2
    i32.add
    i32.const 4
    i32.sub
    i32.load
    i32.store
    local.get $p0
    i32.load offset=12
    local.tee $l2
    local.get $p1
    i32.add
    local.get $p0
    i32.load offset=16
    i32.const 2
    i32.shl
    local.get $l2
    i32.add
    i32.const 4
    i32.sub
    i32.load
    i32.store
    local.get $p0
    local.get $l3
    i32.const 1
    i32.add
    local.tee $l2
    local.get $p0
    i32.load offset=4
    i32.ne
    if $I0 (result i32)
      local.get $p0
      i32.load
      local.get $p1
      i32.add
      i32.load
      local.get $l3
      i32.store offset=48
      local.get $p0
      i32.load offset=4
    else
      local.get $l2
    end
    i32.const 1
    i32.sub
    i32.store offset=4
    local.get $p0
    local.get $p0
    i32.load offset=16
    i32.const 1
    i32.sub
    i32.store offset=16
    local.get $p0
    local.get $p0
    i32.load offset=28
    i32.const 1
    i32.sub
    i32.store offset=28)