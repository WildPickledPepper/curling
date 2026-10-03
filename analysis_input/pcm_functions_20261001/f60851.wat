  (func $f60851 (type $t1) (param $p0 i32) (param $p1 i32)
    i32.const 4674968
    i32.load
    local.tee $p1
    i32.eqz
    if $I0
      i32.const 4674968
      i32.const 325966
      call $f1659
      local.tee $p1
      i32.store
    end
    local.get $p0
    i64.const 0
    local.get $p1
    call_indirect $__indirect_function_table (type $t81))
