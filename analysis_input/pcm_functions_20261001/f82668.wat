  (func $f82668 (type $t2) (param $p0 i32) (param $p1 i32) (param $p2 i32)
    (local $l3 i32) (local $l4 i64)
    global.get $g0
    i32.const 32
    i32.sub
    local.tee $l3
    global.set $g0
    block $B0
      local.get $p0
      i32.eqz
      br_if $B0
      local.get $p0
      i32.load offset=8
      local.tee $p0
      i32.eqz
      br_if $B0
      local.get $p0
      local.get $p1
      i32.const 4
      i32.shl
      i32.add
      local.tee $p0
      local.get $p2
      i64.load offset=8 align=4
      i64.store offset=196 align=4
      local.get $p0
      local.get $p2
      i64.load align=4
      i64.store offset=188 align=4
      local.get $l3
      i32.const 32
      i32.add
      global.set $g0
      return
    end
    local.get $l3
    i32.const 24
    i32.add
    i32.const 143717
    call $f82954
    local.get $l3
    local.get $l3
    i64.load offset=24
    local.tee $l4
    i64.store offset=16
    local.get $l3
    local.get $l4
    i64.store offset=8
    local.get $l3
    i32.const 8
    i32.add
    call $f82953
    unreachable)