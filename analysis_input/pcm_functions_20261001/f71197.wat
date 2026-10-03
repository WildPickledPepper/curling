  (func $f71197 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32)
    block $B0
      local.get $p1
      i32.eqz
      br_if $B0
      local.get $p1
      i32.const 5
      i32.shl
      local.tee $l2
      i32.eqz
      br_if $B0
      call $f69753
      local.tee $l3
      local.get $l2
      i32.const 3153137
      i32.const 3150980
      i32.const 4700888
      i32.load
      local.tee $l4
      local.get $l4
      i32.load
      i32.load offset=20
      call_indirect $__indirect_function_table (type $t5)
      select
      i32.const 3150938
      i32.const 553
      local.get $l3
      i32.load
      i32.load offset=8
      call_indirect $__indirect_function_table (type $t9)
      local.set $l5
    end
    local.get $p0
    i32.load offset=4
    local.tee $l2
    i32.const 0
    i32.gt_s
    if $I1
      local.get $l5
      local.get $l2
      i32.const 5
      i32.shl
      i32.add
      local.set $l4
      local.get $p0
      i32.load
      local.set $l2
      local.get $l5
      local.set $l3
      loop $L2
        local.get $l3
        local.get $l2
        f32.load
        f32.store
        local.get $l3
        local.get $l2
        f32.load offset=4
        f32.store offset=4
        local.get $l3
        local.get $l2
        f32.load offset=8
        f32.store offset=8
        local.get $l3
        local.get $l2
        f32.load offset=12
        f32.store offset=12
        local.get $l3
        local.get $l2
        f32.load offset=16
        f32.store offset=16
        local.get $l3
        local.get $l2
        f32.load offset=20
        f32.store offset=20
        local.get $l3
        local.get $l2
        f32.load offset=24
        f32.store offset=24
        local.get $l3
        local.get $l2
        f32.load offset=28
        f32.store offset=28
        local.get $l2
        i32.const 32
        i32.add
        local.set $l2
        local.get $l3
        i32.const 32
        i32.add
        local.tee $l3
        local.get $l4
        i32.lt_u
        br_if $L2
      end
    end
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
    local.get $p1
    i32.store offset=8
    local.get $p0
    local.get $l5
    i32.store)
