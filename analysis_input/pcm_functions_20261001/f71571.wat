  (func $f71571 (type $t7) (param $p0 i32)
    local.get $p0
    i32.load offset=156
    i32.const -2
    i32.ge_u
    if $I0
      local.get $p0
      i32.load offset=40
      local.get $p0
      call $f71379
      local.get $p0
      call $f71555
    end
    local.get $p0
    i32.load offset=40
    i32.load offset=1000
    local.get $p0
    i64.load offset=144
    call $f70712)