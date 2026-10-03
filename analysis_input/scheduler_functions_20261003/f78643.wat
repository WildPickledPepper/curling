  (func $f78643 (type $t9) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (result i32)
    (local $l5 i32) (local $l6 i32) (local $l7 i32)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l5
    global.set $g0
    i32.const -1
    local.set $l6
    block $B0
      local.get $p0
      i32.eqz
      br_if $B0
      local.get $p1
      i32.const 0
      i32.lt_s
      br_if $B0
      local.get $p2
      i32.eqz
      br_if $B0
      i32.const 0
      local.set $l6
      i32.const 4787792
      i32.load
      local.tee $l7
      i32.eqz
      br_if $B0
      local.get $l5
      local.get $p2
      call $strlen
      i32.store offset=12
      local.get $l5
      local.get $p2
      i32.store offset=8
      local.get $l7
      local.get $p0
      local.get $p1
      local.get $l5
      i32.const 8
      i32.add
      local.get $p3
      local.get $p4
      call $f80331
    end
    local.get $l5
    i32.const 16
    i32.add
    global.set $g0
    local.get $l6)
