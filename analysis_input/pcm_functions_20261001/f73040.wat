  (func $f73040 (type $t7) (param $p0 i32)
    (local $l1 i32) (local $l2 i32) (local $l3 i64)
    local.get $p0
    i32.load offset=168
    local.set $l1
    block $B0
      local.get $p0
      i32.load8_u offset=164
      if $I1
        local.get $p0
        i32.load8_u offset=84
        br_if $B0
      end
      local.get $l1
      if $I2
        local.get $l1
        i32.load
        local.tee $l2
        if $I3
          local.get $l2
          local.get $l1
          i32.load offset=4
          i32.store offset=4
          local.get $l1
          i32.load offset=4
          local.get $l1
          i32.load
          i32.store
          local.get $l1
          i64.const 0
          i64.store align=4
        end
        local.get $l1
        i32.const 41
        i32.const 403047
        i32.const 1927
        call $f83342
      end
      local.get $p0
      i32.const 0
      i32.store offset=168
      return
    end
    block $B4
      local.get $l1
      br_if $B4
      local.get $p0
      i32.load offset=68
      i32.eqz
      br_if $B4
      i32.const 44
      i32.const 41
      i32.const 4
      i32.const 1934
      call $f83338
      local.tee $l1
      i64.const 0
      i64.store align=4
      local.get $p0
      local.get $l1
      i32.store offset=168
      local.get $l1
      i32.const 1
      i32.store offset=40
      local.get $l1
      local.get $p0
      i32.store offset=36
      i32.const 4748496
      i32.load
      local.set $l2
      i32.const 4748488
      i64.load align=4
      local.set $l3
      local.get $l1
      i64.const 4575657221408423936
      i64.store offset=28 align=4
      local.get $l1
      i64.const 0
      i64.store offset=20 align=4
      local.get $l1
      local.get $l2
      i32.store offset=16
      local.get $l1
      local.get $l3
      i64.store offset=8 align=4
      local.get $p0
      i32.load offset=168
      local.tee $l1
      local.get $p0
      i32.load offset=68
      i32.const 768
      i32.add
      local.tee $p0
      i32.eq
      br_if $B4
      local.get $l1
      i32.load
      local.tee $l2
      if $I5
        local.get $l2
        local.get $l1
        i32.load offset=4
        i32.store offset=4
        local.get $l1
        i32.load offset=4
        local.get $l1
        i32.load
        i32.store
        local.get $l1
        i64.const 0
        i64.store align=4
      end
      local.get $p0
      i32.load
      local.set $l2
      local.get $l1
      local.get $p0
      i32.store offset=4
      local.get $l1
      local.get $l2
      i32.store
      local.get $l2
      local.get $l1
      i32.store offset=4
      local.get $l1
      i32.load offset=4
      local.get $l1
      i32.store
    end)