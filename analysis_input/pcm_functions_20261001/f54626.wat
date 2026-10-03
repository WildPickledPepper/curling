  (func $f54626 (type $t2) (param $p0 i32) (param $p1 i32) (param $p2 i32)
    i32.const 4671704
    i32.load
    local.tee $p2
    i32.eqz
    if $I0
      i32.const 4671704
      i32.const 364209
      call $f1659
      local.tee $p2
      i32.store
    end
    local.get $p0
    local.get $p1
    local.get $p2
    call_indirect $__indirect_function_table (type $t1))