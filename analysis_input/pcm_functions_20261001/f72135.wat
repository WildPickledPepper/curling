  (func $f72135 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32)
    local.get $p0
    local.get $p1
    call $f72134
    local.get $p1
    local.get $p1
    i32.load
    i32.load offset=272
    call_indirect $__indirect_function_table (type $t5)
    local.tee $l2
    if $I0
      local.get $p0
      i32.const 16
      i32.add
      local.get $l2
      local.get $l2
      i32.load
      i32.load offset=48
      call_indirect $__indirect_function_table (type $t5)
      call $f72007
    end
    local.get $p1
    i32.load offset=16
    if $I1
      local.get $p1
      i32.const 12
      i32.add
      call $f71928
    end
    local.get $p1
    local.get $p1
    i32.load
    i32.load offset=268
    call_indirect $__indirect_function_table (type $t5)
    local.tee $p0
    local.get $p0
    i32.load
    i32.load offset=100
    call_indirect $__indirect_function_table (type $t5)
    i32.load offset=12
    local.tee $p0
    if $I2
      local.get $p1
      local.get $p0
      local.get $p1
      i32.const -64
      i32.sub
      i32.load
      call $f71656
      i32.store offset=364
    end)