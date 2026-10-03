  (func $f70705 (type $t2) (param $p0 i32) (param $p1 i32) (param $p2 i32)
    (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32)
    local.get $p1
    local.get $p0
    i32.load offset=8
    i32.const 2147483647
    i32.and
    i32.gt_u
    if $I0
      block $B1
        local.get $p1
        i32.eqz
        br_if $B1
        local.get $p1
        i32.const 2
        i32.shl
        local.tee $l4
        i32.eqz
        br_if $B1
        call $f69753
        local.tee $l3
        local.get $l4
        i32.const 3138895
        i32.const 3134052
        i32.const 4700888
        i32.load
        local.tee $l6
        local.get $l6
        i32.load
        i32.load offset=20
        call_indirect $__indirect_function_table (type $t5)
        select
        i32.const 3134537
        i32.const 553
        local.get $l3
        i32.load
        i32.load offset=8
        call_indirect $__indirect_function_table (type $t9)
        local.set $l5
      end
      local.get $p0
      i32.load offset=4
      local.tee $l4
      i32.const 0
      i32.gt_s
      if $I2
        local.get $l5
        local.get $l4
        i32.const 2
        i32.shl
        i32.add
        local.set $l6
        local.get $p0
        i32.load
        local.set $l4
        local.get $l5
        local.set $l3
        loop $L3
          local.get $l3
          local.get $l4
          i32.load
          i32.store
          local.get $l4
          i32.const 4
          i32.add
          local.set $l4
          local.get $l3
          i32.const 4
          i32.add
          local.tee $l3
          local.get $l6
          i32.lt_u
          br_if $L3
        end
      end
      block $B4
        local.get $p0
        i32.load offset=8
        i32.const 0
        i32.lt_s
        br_if $B4
        local.get $p0
        i32.load
        local.tee $l4
        i32.eqz
        br_if $B4
        call $f69753
        local.tee $l3
        local.get $l4
        local.get $l3
        i32.load
        i32.load offset=12
        call_indirect $__indirect_function_table (type $t1)
      end
      local.get $p0
      local.get $p1
      i32.store offset=8
      local.get $p0
      local.get $l5
      i32.store
    end
    local.get $p1
    local.get $p0
    i32.load offset=4
    local.tee $l3
    i32.gt_s
    if $I5
      local.get $p0
      i32.load
      local.tee $l5
      local.get $p1
      i32.const 2
      i32.shl
      i32.add
      local.set $l4
      local.get $l5
      local.get $l3
      i32.const 2
      i32.shl
      i32.add
      local.set $l3
      loop $L6
        local.get $l3
        local.get $p2
        i32.load
        i32.store
        local.get $l3
        i32.const 4
        i32.add
        local.tee $l3
        local.get $l4
        i32.lt_u
        br_if $L6
      end
    end
    local.get $p0
    local.get $p1
    i32.store offset=4)