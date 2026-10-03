  (func $f78647 (type $t32) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 i32) (param $p7 i32) (param $p8 i32) (param $p9 i32) (result i32)
    (local $l10 i32) (local $l11 i32) (local $l12 i32)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l10
    global.set $g0
    block $B0
      local.get $p1
      i32.eqz
      br_if $B0
      local.get $p3
      i32.const 2
      i32.sub
      i32.const 255
      i32.and
      i32.const 5
      i32.gt_u
      br_if $B0
      i32.const 4787792
      i32.load
      local.tee $l11
      i32.eqz
      br_if $B0
      local.get $l10
      local.get $p1
      call $strlen
      i32.store offset=12
      local.get $l10
      local.get $p1
      i32.store offset=8
      local.get $l11
      i32.const 0
      i64.const 0
      local.get $p0
      local.get $l10
      i32.const 8
      i32.add
      local.get $p2
      i32.const 2
      i32.or
      local.get $p3
      local.get $p4
      local.get $p5
      local.get $p6
      local.get $p7
      local.get $p8
      local.get $p9
      call $f80330
      local.set $l12
    end
    local.get $l10
    i32.const 16
    i32.add
    global.set $g0
    local.get $l12)
