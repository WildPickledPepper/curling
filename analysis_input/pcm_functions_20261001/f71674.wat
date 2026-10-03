  (func $f71674 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l4
    global.set $g0
    local.get $l4
    local.get $p1
    i32.store offset=12
    block $B0
      local.get $p1
      i32.const 32
      i32.add
      i32.const 5
      i32.shr_u
      local.tee $l5
      local.get $p0
      i32.load offset=24
      i32.const 2147483647
      i32.and
      i32.le_u
      if $I1
        local.get $p0
        i32.load offset=20
        local.set $l2
        br $B0
      end
      call $f69753
      local.tee $l2
      local.get $l5
      i32.const 2
      i32.shl
      i32.const 3172132
      i32.const 3172322
      i32.const 438
      local.get $l2
      i32.load
      i32.load offset=8
      call_indirect $__indirect_function_table (type $t9)
      local.set $l2
      block $B2
        local.get $p0
        i32.load offset=20
        local.tee $l3
        i32.eqz
        br_if $B2
        local.get $l2
        local.get $l3
        local.get $p0
        i32.load offset=24
        i32.const 2
        i32.shl
        call $f483
        drop
        local.get $p0
        i32.load offset=24
        i32.const 0
        i32.lt_s
        br_if $B2
        local.get $p0
        i32.load offset=20
        local.tee $l3
        i32.eqz
        br_if $B2
        call $f69753
        local.tee $l6
        local.get $l3
        local.get $l6
        i32.load
        i32.load offset=12
        call_indirect $__indirect_function_table (type $t1)
      end
      local.get $l2
      local.get $p0
      i32.load offset=24
      local.tee $l3
      i32.const 2
      i32.shl
      i32.add
      i32.const 0
      local.get $l5
      local.get $l3
      i32.sub
      i32.const 2
      i32.shl
      call $f484
      drop
      local.get $p0
      local.get $l5
      i32.store offset=24
      local.get $p0
      local.get $l2
      i32.store offset=20
    end
    local.get $l2
    local.get $p1
    i32.const 3
    i32.shr_u
    i32.const 536870908
    i32.and
    i32.add
    local.tee $l2
    local.get $l2
    i32.load
    i32.const 1
    local.get $p1
    i32.shl
    i32.or
    i32.store
    block $B3
      local.get $p0
      i32.load offset=36
      local.tee $p1
      local.get $p0
      i32.load offset=40
      i32.const 2147483647
      i32.and
      i32.ge_u
      if $I4
        local.get $p0
        i32.const 32
        i32.add
        local.get $l4
        i32.const 12
        i32.add
        call $f72545
        br $B3
      end
      local.get $p0
      i32.load offset=32
      local.get $p1
      i32.const 2
      i32.shl
      i32.add
      local.get $l4
      i32.load offset=12
      i32.store
      local.get $p0
      local.get $p0
      i32.load offset=36
      i32.const 1
      i32.add
      i32.store offset=36
    end
    local.get $l4
    i32.const 16
    i32.add
    global.set $g0)