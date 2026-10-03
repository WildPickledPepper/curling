  (func $f71379 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l2
    global.set $g0
    local.get $p0
    i32.const 24
    i32.add
    local.set $l5
    local.get $p0
    i32.load offset=28
    local.set $l3
    local.get $l2
    local.get $p1
    i32.load offset=44
    local.tee $l4
    i32.store offset=12
    block $B0
      local.get $l4
      i32.load8_u offset=44
      i32.const 1
      i32.and
      i32.eqz
      if $I1
        local.get $l3
        local.set $l4
        br $B0
      end
      local.get $p0
      local.get $p0
      i32.load offset=36
      local.tee $l4
      i32.const 1
      i32.add
      i32.store offset=36
      local.get $l3
      local.get $l4
      i32.eq
      if $I2
        local.get $l3
        local.set $l4
        br $B0
      end
      local.get $l2
      local.get $l4
      i32.const 2
      i32.shl
      local.tee $l6
      local.get $l5
      i32.load
      i32.add
      i32.load
      local.tee $l7
      i32.store offset=12
      local.get $l7
      i32.load
      local.get $l3
      i32.store offset=156
      local.get $l5
      i32.load
      local.get $l6
      i32.add
      local.get $p1
      i32.load offset=44
      i32.store
    end
    local.get $p1
    i32.load8_u offset=153
    i32.const 16
    i32.and
    if $I3
      block $B4
        local.get $p0
        i32.load offset=44
        local.tee $l3
        local.get $p0
        i32.load offset=48
        i32.const 2147483647
        i32.and
        i32.ge_u
        if $I5
          local.get $p0
          i32.const 40
          i32.add
          local.get $l2
          i32.const 12
          i32.add
          call $f71380
          br $B4
        end
        local.get $p0
        i32.load offset=40
        local.get $l3
        i32.const 2
        i32.shl
        i32.add
        local.get $l2
        i32.load offset=12
        i32.store
        local.get $p0
        local.get $p0
        i32.load offset=44
        i32.const 1
        i32.add
        i32.store offset=44
      end
      local.get $p1
      local.get $l3
      i32.store offset=160
    end
    local.get $p1
    local.get $l4
    i32.store offset=156
    block $B6
      local.get $p0
      i32.load offset=28
      local.tee $p1
      local.get $p0
      i32.load offset=32
      i32.const 2147483647
      i32.and
      i32.ge_u
      if $I7
        local.get $l5
        local.get $l2
        i32.const 12
        i32.add
        call $f71380
        br $B6
      end
      local.get $p0
      i32.load offset=24
      local.get $p1
      i32.const 2
      i32.shl
      i32.add
      local.get $l2
      i32.load offset=12
      i32.store
      local.get $p0
      local.get $p0
      i32.load offset=28
      i32.const 1
      i32.add
      i32.store offset=28
    end
    local.get $l2
    i32.const 16
    i32.add
    global.set $g0)