  (func $f78641 (type $t4) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32)
    (local $l4 i32)
    block $B0
      local.get $p0
      i32.load
      i32.eqz
      br_if $B0
      local.get $p0
      i32.load
      local.tee $l4
      i32.eqz
      br_if $B0
      local.get $p2
      i32.const 65535
      i32.and
      local.set $p2
      loop $L1
        local.get $p0
        local.get $p1
        local.get $p2
        local.get $p3
        local.get $l4
        i32.load offset=4
        local.get $l4
        i32.load
        call_indirect $__indirect_function_table (type $t6)
        local.get $l4
        i32.load offset=8
        local.tee $l4
        br_if $L1
      end
    end)
