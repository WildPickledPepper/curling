  (func $f71588 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32)
    local.get $p0
    local.get $p1
    i32.store offset=4
    local.get $p0
    i32.const 0
    i32.store
    local.get $p0
    local.get $p0
    i32.load offset=8
    i32.const 2147483647
    i32.and
    i32.store offset=8
    block $B0
      local.get $p1
      i32.load offset=40
      local.tee $l4
      i32.load offset=2376
      local.tee $l2
      i32.load offset=12
      local.tee $l3
      if $I1
        local.get $l2
        i32.load offset=8
        local.get $l3
        i32.const 1
        i32.sub
        local.tee $l5
        i32.const 2
        i32.shl
        i32.add
        i32.load
        local.set $l3
        local.get $l2
        local.get $l5
        i32.store offset=12
        br $B0
      end
      local.get $l2
      local.get $l2
      i32.load offset=4
      local.tee $l3
      i32.const 1
      i32.add
      i32.store offset=4
    end
    local.get $p0
    local.get $l3
    i32.const 2147483647
    i32.and
    local.tee $l2
    local.get $p0
    i32.load offset=8
    i32.const -2147483648
    i32.and
    i32.or
    i32.store offset=8
    local.get $l2
    i32.const 1
    i32.add
    local.tee $l2
    local.get $l4
    i32.load offset=1140
    local.tee $l4
    i32.load offset=12
    i32.const 2147483647
    i32.and
    local.tee $l3
    i32.ge_u
    if $I2
      local.get $l2
      i32.const 1
      i32.shr_u
      local.get $l2
      i32.or
      local.tee $l2
      i32.const 2
      i32.shr_u
      local.get $l2
      i32.or
      local.tee $l2
      i32.const 4
      i32.shr_u
      local.get $l2
      i32.or
      local.tee $l2
      i32.const 8
      i32.shr_u
      local.get $l2
      i32.or
      local.tee $l2
      i32.const 16
      i32.shr_u
      local.get $l2
      i32.or
      i32.const 1
      i32.add
      local.tee $l2
      local.get $l3
      i32.gt_u
      if $I3
        local.get $l4
        local.get $l2
        call $f71589
      end
      local.get $l4
      local.get $l2
      i32.store offset=8
    end
    local.get $p0
    local.get $p1
    i32.load offset=32
    i32.store
    local.get $p1
    local.get $p0
    i32.store offset=32
    local.get $p1
    local.get $p1
    i32.load offset=36
    i32.const 1
    i32.add
    i32.store offset=36)