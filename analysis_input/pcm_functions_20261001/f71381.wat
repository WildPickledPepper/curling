  (func $f71381 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32)
    local.get $p1
    i32.load offset=156
    local.set $l2
    local.get $p1
    i32.const -2
    i32.store offset=156
    local.get $p0
    i32.load offset=28
    local.set $l5
    block $B0
      local.get $p0
      i32.load offset=36
      local.tee $l3
      local.get $l2
      i32.le_u
      if $I1
        local.get $l2
        local.set $l4
        br $B0
      end
      local.get $p0
      local.get $l3
      i32.const 1
      i32.sub
      local.tee $l4
      i32.store offset=36
      local.get $l3
      local.get $l5
      i32.eq
      if $I2
        local.get $l2
        local.set $l4
        br $B0
      end
      local.get $l2
      local.get $l4
      i32.ge_u
      if $I3
        local.get $l2
        local.set $l4
        br $B0
      end
      local.get $p0
      i32.load offset=24
      local.get $l4
      i32.const 2
      i32.shl
      i32.add
      i32.load
      local.tee $l3
      i32.load
      local.get $l2
      i32.store offset=156
      local.get $p0
      i32.load offset=24
      local.get $l2
      i32.const 2
      i32.shl
      i32.add
      local.get $l3
      i32.store
    end
    local.get $l5
    i32.const 1
    i32.sub
    local.set $l2
    local.get $p1
    i32.load8_u offset=153
    i32.const 16
    i32.and
    if $I4
      local.get $p1
      i32.load offset=160
      local.set $l5
      local.get $p1
      i32.const -2
      i32.store offset=160
      local.get $p0
      i32.load offset=44
      i32.const 1
      i32.sub
      local.tee $p1
      local.get $l5
      i32.ne
      if $I5
        local.get $p0
        i32.load offset=40
        local.tee $l3
        local.get $l5
        i32.const 2
        i32.shl
        i32.add
        local.get $l3
        local.get $p1
        i32.const 2
        i32.shl
        i32.add
        i32.load
        local.tee $l3
        i32.store
        local.get $l3
        i32.load
        local.get $l5
        i32.store offset=160
      end
      local.get $p0
      local.get $p1
      i32.store offset=44
    end
    local.get $l2
    local.get $l4
    i32.ne
    if $I6
      local.get $p0
      i32.load offset=24
      local.tee $p1
      local.get $l4
      i32.const 2
      i32.shl
      i32.add
      local.get $p1
      local.get $l2
      i32.const 2
      i32.shl
      i32.add
      i32.load
      local.tee $p1
      i32.store
      local.get $p1
      i32.load
      local.get $l4
      i32.store offset=156
    end
    local.get $p0
    local.get $l2
    i32.store offset=28)