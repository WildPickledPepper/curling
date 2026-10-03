  (func $f71385 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32)
    block $B0
      local.get $p0
      i32.load offset=8
      i32.const 2147483647
      i32.and
      local.tee $l2
      i32.const 1
      i32.shl
      i32.const 1
      local.get $l2
      select
      local.tee $l6
      i32.eqz
      br_if $B0
      local.get $l6
      i32.const 2
      i32.shl
      local.tee $l2
      i32.eqz
      br_if $B0
      call $f69753
      local.tee $l3
      local.get $l2
      i32.const 3166920
      i32.const 3158199
      i32.const 4700888
      i32.load
      local.tee $l5
      local.get $l5
      i32.load
      i32.load offset=20
      call_indirect $__indirect_function_table (type $t5)
      select
      i32.const 3158349
      i32.const 553
      local.get $l3
      i32.load
      i32.load offset=8
      call_indirect $__indirect_function_table (type $t9)
      local.set $l4
    end
    local.get $l4
    local.get $p0
    i32.load offset=4
    local.tee $l2
    i32.const 0
    i32.gt_s
    if $I1 (result i32)
      local.get $l4
      local.get $l2
      i32.const 2
      i32.shl
      i32.add
      local.set $l5
      local.get $p0
      i32.load
      local.set $l2
      local.get $l4
      local.set $l3
      loop $L2
        local.get $l3
        local.get $l2
        i32.load
        i32.store
        local.get $l2
        i32.const 4
        i32.add
        local.set $l2
        local.get $l3
        i32.const 4
        i32.add
        local.tee $l3
        local.get $l5
        i32.lt_u
        br_if $L2
      end
      local.get $p0
      i32.load offset=4
    else
      local.get $l2
    end
    i32.const 2
    i32.shl
    i32.add
    local.get $p1
    i32.load
    i32.store
    block $B3
      local.get $p0
      i32.load offset=8
      i32.const 0
      i32.lt_s
      br_if $B3
      local.get $p0
      i32.load
      local.tee $l2
      i32.eqz
      br_if $B3
      call $f69753
      local.tee $l3
      local.get $l2
      local.get $l3
      i32.load
      i32.load offset=12
      call_indirect $__indirect_function_table (type $t1)
    end
    local.get $p0
    local.get $l6
    i32.store offset=8
    local.get $p0
    local.get $l4
    i32.store
    local.get $p0
    local.get $p0
    i32.load offset=4
    i32.const 1
    i32.add
    i32.store offset=4)