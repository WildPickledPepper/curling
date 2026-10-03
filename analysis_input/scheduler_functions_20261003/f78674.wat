  (func $f78674 (type $t0) (param $p0 i32) (param $p1 i32) (result i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i64)
    local.get $p1
    i64.load align=4
    local.set $l7
    local.get $p0
    i32.const 76
    i32.store offset=28
    local.get $p0
    i32.const 0
    i32.store offset=20
    local.get $p0
    i64.const 0
    i64.store offset=12 align=4
    local.get $p0
    i32.const 403680
    i32.store offset=8
    local.get $p0
    local.get $l7
    i64.store align=4
    local.get $p0
    i32.const 8
    i32.add
    local.get $p1
    i32.const 8
    i32.add
    call $f78689
    local.get $p0
    i32.const 76
    i32.store offset=52
    local.get $p0
    i32.const 0
    i32.store offset=44
    local.get $p0
    i64.const 0
    i64.store offset=36 align=4
    local.get $p0
    i32.const 403680
    i32.store offset=32
    local.get $p0
    i32.const 32
    i32.add
    local.get $p1
    i32.const 32
    i32.add
    call $f78689
    local.get $p0
    local.get $p1
    i32.load offset=56
    i32.store offset=56
    local.get $p1
    i32.const -64
    i32.sub
    i32.load
    local.set $l2
    local.get $p0
    i64.const 4294967296
    i64.store offset=68 align=4
    local.get $p0
    i32.const -64
    i32.sub
    local.get $l2
    i32.store
    local.get $p0
    i32.const 60
    i32.add
    local.tee $l4
    i32.const 0
    i32.store
    local.get $p1
    i32.load offset=60
    local.set $l6
    local.get $p1
    i32.load offset=68
    local.tee $l2
    if $I0
      local.get $l4
      local.get $l2
      i32.const 1
      call $f66024
      local.get $l4
      i32.load
      local.set $l3
    end
    local.get $p0
    local.get $l2
    i32.store offset=68
    local.get $l3
    local.get $l6
    local.get $l2
    i32.const 2
    i32.shl
    call $f483
    drop
    local.get $p0
    local.get $p1
    i32.load offset=84
    i32.store offset=84
    local.get $p0
    local.get $p1
    i64.load offset=76 align=4
    i64.store offset=76 align=4
    local.get $p0
    local.get $p1
    i32.load offset=88
    i32.store offset=88
    local.get $p1
    i32.load offset=96
    local.set $l2
    local.get $p0
    i64.const 4294967296
    i64.store offset=100 align=4
    local.get $p0
    local.get $l2
    i32.store offset=96
    local.get $p0
    i32.const 92
    i32.add
    local.tee $l3
    i32.const 0
    i32.store
    local.get $p1
    i32.load offset=92
    local.set $l4
    local.get $p1
    i32.load offset=100
    local.tee $l2
    if $I1
      local.get $l3
      local.get $l2
      i32.const 1
      call $f65937
      local.get $l3
      i32.load
      local.set $l5
    end
    local.get $p0
    local.get $l2
    i32.store offset=100
    local.get $l5
    local.get $l4
    local.get $l2
    i32.const 3
    i32.shl
    call $f483
    drop
    local.get $p0
    local.get $p1
    i32.load offset=116
    i32.store offset=116
    local.get $p0
    local.get $p1
    i64.load offset=108 align=4
    i64.store offset=108 align=4
    local.get $p0
    local.get $p1
    i32.load offset=120
    i32.store offset=120
    local.get $p0)
