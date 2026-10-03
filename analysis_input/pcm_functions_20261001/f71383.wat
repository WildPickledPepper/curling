  (func $f71383 (type $t2) (param $p0 i32) (param $p1 i32) (param $p2 i32)
    (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l7
    global.set $g0
    local.get $l7
    local.get $p1
    i32.store offset=12
    local.get $p1
    local.get $p0
    local.get $p1
    i32.load8_u offset=20
    local.tee $l6
    i32.const 12
    i32.mul
    i32.add
    local.tee $l3
    i32.const 56
    i32.add
    local.tee $l5
    i32.load
    local.tee $l8
    i32.store offset=8
    local.get $l3
    i32.const 52
    i32.add
    local.set $l4
    block $B0
      local.get $l3
      i32.const 60
      i32.add
      local.tee $l9
      i32.load
      i32.const 2147483647
      i32.and
      local.tee $l3
      if $I1 (result i32)
        local.get $l3
      else
        local.get $l4
        i32.const 64
        call $f71384
        local.get $l9
        i32.load
        i32.const 2147483647
        i32.and
      end
      local.get $l5
      i32.load
      local.tee $l9
      i32.le_u
      if $I2
        local.get $l4
        local.get $l7
        i32.const 12
        i32.add
        call $f71385
        br $B0
      end
      local.get $l4
      i32.load
      local.get $l9
      i32.const 2
      i32.shl
      i32.add
      local.get $p1
      i32.store
      local.get $l5
      local.get $l5
      i32.load
      i32.const 1
      i32.add
      i32.store
    end
    local.get $p2
    if $I3
      local.get $p0
      local.get $l6
      i32.const 2
      i32.shl
      i32.add
      i32.const 88
      i32.add
      local.tee $l3
      i32.load
      local.tee $p1
      local.get $l8
      i32.lt_u
      if $I4
        local.get $p0
        local.get $l6
        i32.const 12
        i32.mul
        i32.add
        i32.const 52
        i32.add
        local.tee $p0
        i32.load
        local.tee $l4
        local.get $l8
        i32.const 2
        i32.shl
        i32.add
        local.tee $p2
        i32.load
        local.set $l5
        local.get $p2
        local.get $l4
        local.get $p1
        i32.const 2
        i32.shl
        local.tee $l6
        i32.add
        i32.load
        local.tee $l4
        i32.store
        local.get $p0
        i32.load
        local.get $l6
        i32.add
        local.get $l5
        i32.store
        local.get $l5
        local.get $p1
        i32.store offset=8
        local.get $l4
        local.get $l8
        i32.store offset=8
        local.get $l3
        i32.load
        local.set $p1
      end
      local.get $l3
      local.get $p1
      i32.const 1
      i32.add
      i32.store
    end
    local.get $l7
    i32.const 16
    i32.add
    global.set $g0)