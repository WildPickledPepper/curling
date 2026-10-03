  (func $f78644 (type $t3) (param $p0 i32) (param $p1 i32) (param $p2 i32) (result i32)
    (local $l3 i32) (local $l4 i32)
    i32.const -1
    local.set $p2
    block $B0
      local.get $p0
      i32.eqz
      br_if $B0
      local.get $p1
      i32.eqz
      br_if $B0
      global.get $g0
      i32.const 16
      i32.sub
      local.tee $l3
      global.set $g0
      i32.const 4787792
      i32.load
      local.tee $l4
      if $I1 (result i32)
        local.get $l3
        local.get $p1
        call $strlen
        i32.store offset=12
        local.get $l3
        local.get $p1
        i32.store offset=8
        local.get $l4
        local.get $l3
        i32.const 8
        i32.add
        i32.const 1
        call $f80326
      else
        i32.const 0
      end
      local.set $p1
      local.get $l3
      i32.const 16
      i32.add
      global.set $g0
      local.get $p1
      i32.eqz
      br_if $B0
      local.get $p0
      local.get $p1
      i32.load16_u
      i32.store16
      i32.const 0
      local.set $p2
    end
    local.get $p2)
