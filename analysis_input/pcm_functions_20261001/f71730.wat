  (func $f71730 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l2
    global.set $g0
    local.get $p1
    local.get $p0
    i32.load offset=4
    i32.store offset=48
    local.get $l2
    local.get $p1
    i32.store offset=12
    block $B0
      local.get $p0
      i32.load offset=4
      local.tee $l3
      local.get $p0
      i32.load offset=8
      i32.const 2147483647
      i32.and
      i32.ge_u
      if $I1
        local.get $p0
        local.get $l2
        i32.const 12
        i32.add
        call $f71731
        br $B0
      end
      local.get $p0
      i32.load
      local.get $l3
      i32.const 2
      i32.shl
      i32.add
      local.get $p1
      i32.store
      local.get $p0
      local.get $p0
      i32.load offset=4
      i32.const 1
      i32.add
      i32.store offset=4
    end
    local.get $l2
    i32.const -1
    i32.store offset=12
    block $B2
      local.get $p0
      i32.load offset=16
      local.tee $l3
      local.get $p0
      i32.load offset=20
      i32.const 2147483647
      i32.and
      i32.ge_u
      if $I3
        local.get $p0
        i32.const 12
        i32.add
        local.get $l2
        i32.const 12
        i32.add
        call $f72545
        br $B2
      end
      local.get $p0
      i32.load offset=12
      local.get $l3
      i32.const 2
      i32.shl
      i32.add
      i32.const -1
      i32.store
      local.get $p0
      local.get $p0
      i32.load offset=16
      i32.const 1
      i32.add
      i32.store offset=16
    end
    local.get $l2
    local.get $p1
    i32.load offset=8
    i32.const 2147483647
    i32.and
    local.tee $l3
    i32.store offset=12
    block $B4
      local.get $p0
      i32.load offset=28
      local.tee $l4
      local.get $p0
      i32.load offset=32
      i32.const 2147483647
      i32.and
      i32.ge_u
      if $I5
        local.get $p0
        i32.const 24
        i32.add
        local.get $l2
        i32.const 12
        i32.add
        call $f72545
        br $B4
      end
      local.get $p0
      i32.load offset=24
      local.get $l4
      i32.const 2
      i32.shl
      i32.add
      local.get $l3
      i32.store
      local.get $p0
      local.get $p0
      i32.load offset=28
      i32.const 1
      i32.add
      i32.store offset=28
    end
    local.get $l2
    local.get $p1
    i32.store offset=12
    block $B6
      local.get $p0
      i32.load offset=40
      local.tee $l3
      local.get $p0
      i32.load offset=44
      i32.const 2147483647
      i32.and
      i32.ge_u
      if $I7
        local.get $p0
        i32.const 36
        i32.add
        local.get $l2
        i32.const 12
        i32.add
        call $f71731
        br $B6
      end
      local.get $p0
      i32.load offset=36
      local.get $l3
      i32.const 2
      i32.shl
      i32.add
      local.get $p1
      i32.store
      local.get $p0
      local.get $p0
      i32.load offset=40
      i32.const 1
      i32.add
      i32.store offset=40
    end
    local.get $l2
    i32.const 16
    i32.add
    global.set $g0)