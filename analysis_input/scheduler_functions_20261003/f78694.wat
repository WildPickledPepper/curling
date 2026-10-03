  (func $f78694 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32)
    global.get $g0
    i32.const 32
    i32.sub
    local.tee $l2
    global.set $g0
    local.get $p0
    local.get $p1
    i32.load
    i32.store offset=32
    local.get $p0
    i32.load offset=28
    i32.const 4128028
    call $f80185
    local.tee $p1
    if $I0
      local.get $l2
      local.get $p0
      i32.load offset=32
      i32.store offset=8
      local.get $p1
      local.get $l2
      i32.const 8
      i32.add
      call $f79387
    end
    local.get $l2
    i64.const 0
    i64.store offset=16
    local.get $l2
    i32.const 0
    i32.store offset=24
    local.get $p0
    i32.const 4759172
    local.get $l2
    i32.const 16
    i32.add
    call $f80200
    i32.const 4758660
    i32.load8_u
    if $I1
      local.get $p0
      call $f78679
    end
    local.get $l2
    i32.const 32
    i32.add
    global.set $g0)
