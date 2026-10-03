  (func $f82670 (type $t15) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 i32)
    (local $l7 i32) (local $l8 i64)
    global.get $g0
    i32.const 32
    i32.sub
    local.tee $l7
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
      call $f75739
      local.get $p1
      local.get $p2
      call $f75715
      local.get $p3
      i32.const 0
      i32.ne
      local.get $p4
      i32.const 0
      i32.ne
      local.get $p5
      i32.const 0
      i32.ne
      local.get $p6
      i32.const 0
      i32.ne
      call $f75750
      local.get $l7
      i32.const 32
      i32.add
      global.set $g0
      return
    end
    local.get $l7
    i32.const 24
    i32.add
    i32.const 143717
    call $f82954
    local.get $l7
    local.get $l7
    i64.load offset=24
    local.tee $l8
    i64.store offset=16
    local.get $l7
    local.get $l8
    i64.store offset=8
    local.get $l7
    i32.const 8
    i32.add
    call $f82953
    unreachable)