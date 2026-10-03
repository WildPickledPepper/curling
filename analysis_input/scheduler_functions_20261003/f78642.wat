  (func $f78642 (type $t9) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (result i32)
    (local $l5 i32) (local $l6 i32)
    i32.const -1
    local.set $p4
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
      local.tee $l5
      global.set $g0
      i32.const 4787792
      i32.load
      local.tee $l6
      if $I1 (result i32)
        local.get $l5
        local.get $p1
        call $strlen
        i32.store offset=12
        local.get $l5
        local.get $p1
        i32.store offset=8
        local.get $l6
        local.get $p2
        local.get $l5
        i32.const 8
        i32.add
        local.get $p3
        call $f80329
      else
        i32.const 4787088
      end
      local.set $p1
      local.get $l5
      i32.const 16
      i32.add
      global.set $g0
      local.get $p1
      i32.eqz
      br_if $B0
      local.get $p0
      local.get $p1
      i32.store
      i32.const 0
      local.set $p4
    end
    local.get $p4)
