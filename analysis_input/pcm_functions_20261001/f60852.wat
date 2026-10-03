  (func $f60852 (type $t2) (param $p0 i32) (param $p1 i32) (param $p2 i32)
    local.get $p0
    i32.load offset=8
    local.tee $p2
    if $I0
      local.get $p2
      i32.load offset=32
      local.get $p0
      local.get $p1
      local.get $p2
      i32.load offset=20
      local.get $p2
      i32.load offset=12
      call_indirect $__indirect_function_table (type $t4)
    end)
