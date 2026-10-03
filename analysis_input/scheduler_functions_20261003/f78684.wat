  (func $f78684 (type $t1) (param $p0 i32) (param $p1 i32)
    local.get $p1
    if $I0
      local.get $p0
      local.get $p1
      i32.load
      call $f78684
      local.get $p0
      local.get $p1
      i32.load offset=4
      call $f78684
      local.get $p1
      i32.const -64
      i32.sub
      i32.load8_u
      i32.eqz
      if $I1
        local.get $p1
        i32.load offset=44
        local.get $p1
        i32.load offset=68
        i32.const 403047
        i32.const 518
        call $f83342
      end
      local.get $p1
      i32.load8_u offset=36
      i32.eqz
      if $I2
        local.get $p1
        i32.load offset=16
        local.get $p1
        i32.load offset=40
        i32.const 403047
        i32.const 518
        call $f83342
      end
      local.get $p1
      i32.const 16
      i32.const 403047
      i32.const 99
      call $f83342
    end)
