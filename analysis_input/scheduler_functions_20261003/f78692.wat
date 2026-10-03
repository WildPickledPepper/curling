  (func $f78692 (type $t7) (param $p0 i32)
    (local $l1 i32) (local $l2 i32)
    local.get $p0
    i32.load
    local.tee $l1
    if $I0
      local.get $p0
      i32.load offset=4
      local.set $l2
      local.get $l1
      local.get $l1
      i32.load offset=4
      call $f78684
      local.get $l1
      local.get $l2
      i32.const 403047
      i32.const 162
      call $f83342
    end
    local.get $p0
    i32.const 0
    i32.store)
