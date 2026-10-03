  (func $f32511 (type $t17) (param $p0 i32) (param $p1 f32) (param $p2 i32)
    i32.const 4658992
    i32.load
    local.tee $p2
    i32.eqz
    if $I0
      i32.const 4658992
      i32.const 318700
      call $f1659
      local.tee $p2
      i32.store
    end
    local.get $p0
    local.get $p1
    local.get $p2
    call_indirect $__indirect_function_table (type $t21))
