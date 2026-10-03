  (func $f73714 (type $t7) (param $p0 i32)
    (local $l1 i32) (local $l2 i32)
    local.get $p0
    i32.load offset=188
    if $I0
      loop $L1
        local.get $p0
        i32.load offset=180
        local.set $l1
        call $f78306
        drop
        local.get $l1
        local.get $l2
        i32.const 4
        i32.shl
        i32.add
        local.tee $l1
        i64.load
        i64.eqz
        i32.eqz
        if $I2
          local.get $l1
          call $f79912
          local.get $l1
          call $f79911
        end
        local.get $l2
        i32.const 1
        i32.add
        local.tee $l2
        local.get $p0
        i32.load offset=188
        i32.lt_u
        br_if $L1
      end
      block $B3
        local.get $p0
        i32.load offset=180
        local.tee $l2
        i32.eqz
        br_if $B3
        local.get $p0
        i32.load8_u offset=192
        i32.const 1
        i32.and
        br_if $B3
        local.get $l2
        local.get $p0
        i32.load offset=184
        i32.const 403047
        i32.const 774
        call $f83342
      end
      local.get $p0
      i64.const 4294967296
      i64.store offset=188 align=4
      local.get $p0
      i32.const 0
      i32.store offset=180
    end)
