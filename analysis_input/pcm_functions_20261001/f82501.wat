  (func $f82501 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i64)
    global.get $g0
    i32.const 32
    i32.sub
    local.tee $l2
    global.set $g0
    block $B0
      local.get $p0
      i32.eqz
      br_if $B0
      local.get $p0
      call $f79964
      local.tee $l3
      i32.eqz
      br_if $B0
      local.get $l3
      local.get $p1
      call $f73034
      local.get $l2
      i32.const 32
      i32.add
      global.set $g0
      return
    end
    local.get $l2
    i32.const 24
    i32.add
    call $f82960
    local.get $l2
    local.get $l2
    i64.load offset=24
    local.tee $l4
    i64.store offset=16
    local.get $l2
    local.get $l4
    i64.store offset=8
    local.get $l2
    i32.const 8
    i32.add
    call $f82953
    unreachable)