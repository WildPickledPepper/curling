  (func $f54556 (type $t23) (param $p0 i32) (result f32)
    i32.const 4671500
    i32.load
    local.tee $p0
    i32.eqz
    if $I0
      i32.const 4671500
      i32.const 345824
      call $f1659
      local.tee $p0
      i32.store
    end
    local.get $p0
    call_indirect $__indirect_function_table (type $t62))
