  (func $f71693 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i64)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l2
    global.set $g0
    local.get $l2
    local.get $p1
    i32.load offset=28
    local.tee $l3
    local.get $p1
    i32.load offset=32
    local.tee $l4
    local.get $l3
    local.get $l4
    i32.gt_u
    local.tee $l5
    select
    i32.store offset=4
    local.get $l2
    local.get $l4
    local.get $l3
    local.get $l5
    select
    i32.store
    local.get $p0
    i32.const 1956
    i32.add
    local.get $l2
    local.get $l2
    i32.const 15
    i32.add
    call $f71694
    local.set $l3
    local.get $l2
    i32.load8_u offset=15
    i32.eqz
    if $I0
      local.get $l2
      i64.load
      local.set $l6
      local.get $l3
      local.get $p1
      i32.store offset=8
      local.get $l3
      local.get $l6
      i64.store align=4
    end
    local.get $l2
    i32.const 16
    i32.add
    global.set $g0)