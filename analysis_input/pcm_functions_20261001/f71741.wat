  (func $f71741 (type $t5) (param $p0 i32) (result i32)
    (local $l1 i32) (local $l2 i32)
    local.get $p0
    i32.const 3175444
    i32.store
    local.get $p0
    call $f71742
    block $B0
      local.get $p0
      i32.load offset=360
      local.tee $l1
      i32.const 0
      i32.lt_s
      br_if $B0
      local.get $l1
      i32.const 2147483647
      i32.and
      i32.eqz
      br_if $B0
      local.get $p0
      i32.load offset=352
      local.tee $l1
      i32.eqz
      br_if $B0
      call $f69753
      local.tee $l2
      local.get $l1
      local.get $l2
      i32.load
      i32.load offset=12
      call_indirect $__indirect_function_table (type $t1)
    end
    block $B1
      local.get $p0
      i32.load offset=348
      local.tee $l1
      i32.const 0
      i32.lt_s
      br_if $B1
      local.get $l1
      i32.const 2147483647
      i32.and
      i32.eqz
      br_if $B1
      local.get $p0
      i32.load offset=340
      local.tee $l1
      i32.eqz
      br_if $B1
      call $f69753
      local.tee $l2
      local.get $l1
      local.get $l2
      i32.load
      i32.load offset=12
      call_indirect $__indirect_function_table (type $t1)
    end
    block $B2
      local.get $p0
      i32.load offset=332
      local.tee $l1
      i32.const 0
      i32.lt_s
      br_if $B2
      local.get $l1
      i32.const 2147483647
      i32.and
      i32.eqz
      br_if $B2
      local.get $p0
      i32.load offset=324
      local.tee $l1
      i32.eqz
      br_if $B2
      call $f69753
      local.tee $l2
      local.get $l1
      local.get $l2
      i32.load
      i32.load offset=12
      call_indirect $__indirect_function_table (type $t1)
    end
    block $B3
      local.get $p0
      i32.load offset=320
      local.tee $l1
      i32.const 0
      i32.lt_s
      br_if $B3
      local.get $l1
      i32.const 2147483647
      i32.and
      i32.eqz
      br_if $B3
      local.get $p0
      i32.load offset=312
      local.tee $l1
      i32.eqz
      br_if $B3
      call $f69753
      local.tee $l2
      local.get $l1
      local.get $l2
      i32.load
      i32.load offset=12
      call_indirect $__indirect_function_table (type $t1)
    end
    local.get $p0
    i32.const 284
    i32.add
    call $f71883
    local.get $p0
    i32.const 52
    i32.add
    call $f71861
    drop
    local.get $p0
    i32.const 0
    i32.store offset=16
    local.get $p0
    i64.const 0
    i64.store offset=8 align=4
    local.get $p0
    i32.load offset=20
    local.tee $l1
    if $I4
      call $f69753
      local.tee $l2
      local.get $l1
      local.get $l2
      i32.load
      i32.load offset=12
      call_indirect $__indirect_function_table (type $t1)
    end
    local.get $p0
    i32.const 0
    i32.store offset=20
    local.get $p0)