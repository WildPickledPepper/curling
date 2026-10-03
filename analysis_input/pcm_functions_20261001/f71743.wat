  (func $f71743 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32)
    local.get $p0
    i32.load offset=48
    local.tee $l3
    if $I0
      block $B1
        local.get $l3
        i32.load offset=8
        local.tee $l2
        i32.const 0
        i32.lt_s
        br_if $B1
        local.get $l2
        i32.const 2147483647
        i32.and
        i32.eqz
        br_if $B1
        local.get $l3
        i32.load
        local.tee $l2
        i32.eqz
        br_if $B1
        call $f69753
        local.tee $l4
        local.get $l2
        local.get $l4
        i32.load
        i32.load offset=12
        call_indirect $__indirect_function_table (type $t1)
      end
      call $f69753
      local.tee $l2
      local.get $l3
      local.get $l2
      i32.load
      i32.load offset=12
      call_indirect $__indirect_function_table (type $t1)
    end
    local.get $p0
    i32.const 0
    i32.store offset=48
    local.get $p0
    i32.load offset=36
    local.tee $l3
    if $I2
      call $f69753
      local.tee $l2
      local.get $l3
      local.get $l2
      i32.load
      i32.load offset=12
      call_indirect $__indirect_function_table (type $t1)
    end
    local.get $p0
    i32.const 0
    i32.store offset=36
    local.get $p0
    i32.load offset=8
    local.tee $l3
    if $I3
      call $f69753
      local.tee $l2
      local.get $l3
      i32.const 4
      i32.sub
      local.get $l2
      i32.load
      i32.load offset=12
      call_indirect $__indirect_function_table (type $t1)
    end
    local.get $p0
    i32.const 0
    i32.store offset=8
    local.get $p0
    i32.const 12
    i32.add
    call $f70307
    local.get $p0
    i32.load
    local.tee $l3
    if $I4
      call $f69753
      local.tee $l2
      local.get $l3
      local.get $l2
      i32.load
      i32.load offset=12
      call_indirect $__indirect_function_table (type $t1)
    end
    local.get $p0
    i32.const 0
    i32.store offset=40
    local.get $p0
    i64.const 0
    i64.store align=4
    local.get $p1
    if $I5
      local.get $p0
      i32.load offset=52
      i32.const 0
      local.get $p0
      i32.load offset=56
      i32.const 2
      i32.shl
      call $f484
      drop
    end
    local.get $p0
    i32.const 0
    i32.store offset=60)