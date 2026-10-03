  (func $f71460 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32)
    local.get $p0
    i32.load offset=4
    i32.load offset=40
    local.set $l2
    local.get $p1
    if $I0
      local.get $p0
      i32.const 0
      local.get $l2
      i32.load offset=980
      i32.const 160
      i32.add
      call $f71458
      return
    end
    local.get $p0
    i32.load offset=8
    local.tee $p0
    i32.const 0
    i32.lt_s
    if $I1
      block $B2
        local.get $p0
        i32.const 2147483647
        i32.and
        local.tee $l5
        i32.const 32
        i32.add
        i32.const 5
        i32.shr_u
        local.tee $l4
        local.get $l2
        i32.const 2520
        i32.add
        i32.load
        i32.const 2147483647
        i32.and
        i32.le_u
        if $I3
          local.get $l2
          i32.load offset=2516
          local.set $p1
          br $B2
        end
        call $f69753
        local.tee $p1
        local.get $l4
        i32.const 2
        i32.shl
        i32.const 3158048
        i32.const 3160746
        i32.const 438
        local.get $p1
        i32.load
        i32.load offset=8
        call_indirect $__indirect_function_table (type $t9)
        local.set $p1
        block $B4
          local.get $l2
          i32.load offset=2516
          local.tee $l3
          i32.eqz
          br_if $B4
          local.get $p1
          local.get $l3
          local.get $l2
          i32.load offset=2520
          i32.const 2
          i32.shl
          call $f483
          drop
          local.get $l2
          i32.load offset=2520
          i32.const 0
          i32.lt_s
          br_if $B4
          local.get $l2
          i32.load offset=2516
          local.tee $l3
          i32.eqz
          br_if $B4
          call $f69753
          local.tee $l6
          local.get $l3
          local.get $l6
          i32.load
          i32.load offset=12
          call_indirect $__indirect_function_table (type $t1)
        end
        local.get $p1
        local.get $l2
        i32.load offset=2520
        local.tee $l3
        i32.const 2
        i32.shl
        i32.add
        i32.const 0
        local.get $l4
        local.get $l3
        i32.sub
        i32.const 2
        i32.shl
        call $f484
        drop
        local.get $l2
        local.get $l4
        i32.store offset=2520
        local.get $l2
        local.get $p1
        i32.store offset=2516
      end
      local.get $p1
      local.get $l5
      i32.const 3
      i32.shr_u
      i32.const 268435452
      i32.and
      i32.add
      local.tee $l2
      local.get $l2
      i32.load
      i32.const 1
      local.get $p0
      i32.shl
      i32.or
      i32.store
    end)
