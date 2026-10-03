  (func $f54557 (type $t187) (param $p0 f32) (param $p1 i32)
    i32.const 4671504
    i32.load
    local.tee $p1
    i32.eqz
    if $I0
      i32.const 4671504
      i32.const 319343
      call $f1659
      local.tee $p1
      i32.store
    end
    local.get $p0
    local.get $p1
    call_indirect $__indirect_function_table (type $t193))
