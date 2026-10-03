  (func $f53861 (type $t3) (param $p0 i32) (param $p1 i32) (param $p2 i32) (result i32)
    (local $l3 i32)
    local.get $p0
    local.get $p1
    i32.eq
    if $I0
      i32.const 1
      return
    end
    i32.const 0
    local.set $p2
    block $B1
      local.get $p0
      i32.eqz
      br_if $B1
      local.get $p1
      i32.eqz
      br_if $B1
      local.get $p0
      i32.load offset=8
      local.tee $l3
      local.get $p1
      i32.load offset=8
      i32.ne
      br_if $B1
      local.get $p0
      i32.const 12
      i32.add
      local.get $p1
      i32.const 12
      i32.add
      local.get $l3
      i64.extend_i32_s
      i64.const 1
      i64.shl
      i32.const 0
      call $f57023
      local.set $p2
    end
    local.get $p2)
