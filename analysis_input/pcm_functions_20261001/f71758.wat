  (func $f71758 (type $t2) (param $p0 i32) (param $p1 i32) (param $p2 i32)
    (local $l3 i32) (local $l4 i32) (local $l5 i64)
    local.get $p1
    i32.load offset=12
    local.tee $l3
    if $I0
      call $f69753
      local.tee $l4
      local.get $l3
      local.get $l4
      i32.load
      i32.load offset=12
      call_indirect $__indirect_function_table (type $t1)
    end
    local.get $p1
    i32.const 0
    i32.store offset=12
    local.get $p0
    local.get $p2
    i32.load
    local.tee $p1
    i32.store offset=40
    local.get $p0
    local.get $p2
    i32.load offset=4
    i32.store offset=44
    call $f69753
    local.tee $p2
    i32.const -1
    i32.const -1
    local.get $p1
    i64.extend_i32_u
    i64.const 28
    i64.mul
    local.tee $l5
    i32.wrap_i64
    local.tee $l3
    i32.const 4
    i32.add
    local.tee $l4
    local.get $l3
    local.get $l4
    i32.gt_u
    select
    local.get $l5
    i64.const 32
    i64.shr_u
    i32.wrap_i64
    select
    i32.const 3177145
    i32.const 3176295
    i32.const 4700888
    i32.load
    local.tee $l3
    local.get $l3
    i32.load
    i32.load offset=20
    call_indirect $__indirect_function_table (type $t5)
    select
    i32.const 3175524
    i32.const 209
    local.get $p2
    i32.load
    i32.load offset=8
    call_indirect $__indirect_function_table (type $t9)
    local.tee $p2
    local.get $p1
    i32.store
    local.get $p0
    local.get $p2
    i32.const 4
    i32.add
    local.tee $p2
    i32.store offset=8
    local.get $p0
    i32.const 12
    i32.add
    local.tee $p0
    local.get $p2
    call $f71773
    local.get $p0
    call $f70307)