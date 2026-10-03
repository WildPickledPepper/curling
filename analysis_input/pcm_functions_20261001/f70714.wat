  (func $f70714 (type $t81) (param $p0 i32) (param $p1 i64)
    local.get $p1
    i64.const 2199023255040
    i64.and
    i64.const 2199023255040
    i64.ne
    if $I0
      local.get $p0
      i32.const 168
      i32.add
      local.get $p1
      call $f70662
      local.get $p0
      i32.const 640
      i32.add
      local.get $p1
      call $f70662
    end)