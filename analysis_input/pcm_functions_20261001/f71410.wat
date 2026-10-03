  (func $f71410 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l2
    global.set $g0
    local.get $l2
    local.get $p1
    i32.store offset=8
    local.get $p0
    i32.const 1252
    i32.add
    local.get $l2
    i32.const 8
    i32.add
    local.get $l2
    i32.const 15
    i32.add
    call $f71568
    local.set $p0
    local.get $l2
    i32.load8_u offset=15
    i32.eqz
    if $I0
      local.get $p0
      local.get $l2
      i32.load offset=8
      i32.store
    end
    local.get $l2
    i32.load offset=8
    local.tee $p0
    local.get $p0
    i32.load8_u offset=68
    i32.const 4
    i32.or
    i32.store8 offset=68
    local.get $l2
    i32.const 16
    i32.add
    global.set $g0)