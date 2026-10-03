  (func $f71567 (type $t7) (param $p0 i32)
    local.get $p0
    i32.load offset=164
    i32.eqz
    if $I0
      local.get $p0
      i32.load offset=40
      i32.load offset=1000
      local.get $p0
      i64.load offset=144
      call $f70713
    end)