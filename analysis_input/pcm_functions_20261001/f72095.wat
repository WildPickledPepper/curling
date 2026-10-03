  (func $f72095 (type $t7) (param $p0 i32)
    (local $l1 i32)
    block $B0
      local.get $p0
      i32.load offset=48
      local.tee $l1
      i32.eqz
      br_if $B0
      local.get $l1
      i32.load8_u offset=4785
      br_if $B0
      local.get $l1
      local.get $p0
      i32.const 48
      i32.add
      i32.const 0
      call $f71995
    end)