  (func $f71557 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32)
    block $B0
      local.get $p1
      local.get $p0
      i32.load offset=156
      i32.const -2
      i32.lt_u
      i32.ne
      if $I1
        local.get $p0
        i32.load offset=40
        local.set $l2
        local.get $p1
        if $I2
          local.get $l2
          local.get $p0
          call $f71379
          br $B0
        end
        local.get $l2
        local.get $p0
        call $f71381
        local.get $p0
        call $f71556
      end
      return
    end
    local.get $p0
    call $f71555)