  (func $f54401 (type $t0) (param $p0 i32) (param $p1 i32) (result i32)
    i32.const 4671128
    i32.load
    local.tee $p1
    i32.eqz
    if $I0
      i32.const 4671128
      i32.const 340400
      call $f1659
      local.tee $p1
      i32.store
    end
    local.get $p0
    local.get $p1
    call_indirect $__indirect_function_table (type $t5))