  (func $f71632 (type $t7) (param $p0 i32)
    (local $l1 i32) (local $l2 i32)
    local.get $p0
    i32.load offset=56
    local.tee $l1
    if $I0
      local.get $p0
      i32.load offset=4
      i32.load offset=40
      i32.load offset=976
      i32.load offset=1024
      local.set $l2
      local.get $l1
      i32.const 0
      i32.store8 offset=42
      local.get $l1
      i64.const 0
      i64.store offset=32 align=4
      local.get $l2
      local.get $p0
      i32.load offset=56
      local.get $l2
      i32.load
      i32.load offset=40
      call_indirect $__indirect_function_table (type $t1)
    end)
