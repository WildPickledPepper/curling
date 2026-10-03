  (func $f71747 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32)
    local.get $p0
    i32.load offset=52
    i32.eqz
    if $I0
      local.get $p0
      local.get $p0
      i32.load offset=40
      local.tee $l2
      i32.const 5
      i32.shr_u
      local.get $l2
      i32.const 31
      i32.and
      i32.const 0
      i32.ne
      i32.add
      local.tee $l2
      i32.store offset=56
      block $B1 (result i32)
        local.get $l2
        i32.eqz
        if $I2
          i32.const 0
          local.set $l2
          i32.const 0
          br $B1
        end
        call $f69753
        local.tee $l3
        local.get $l2
        i32.const 2
        i32.shl
        i32.const 3176237
        i32.const 3175524
        i32.const 325
        local.get $l3
        i32.load
        i32.load offset=8
        call_indirect $__indirect_function_table (type $t9)
        local.set $l2
        local.get $p0
        i32.load offset=56
        i32.const 2
        i32.shl
      end
      local.set $l3
      local.get $p0
      local.get $l2
      i32.store offset=52
      local.get $l2
      i32.const 0
      local.get $l3
      call $f484
      drop
    end
    local.get $p0
    i32.load offset=36
    i32.eqz
    if $I3
      block $B4
        local.get $p0
        i32.load offset=40
        local.tee $l4
        i32.const 2
        i32.shl
        local.tee $l2
        i32.eqz
        if $I5
          i32.const 0
          local.set $l3
          br $B4
        end
        call $f69753
        local.tee $l3
        local.get $l2
        i32.const 3176237
        i32.const 3175524
        i32.const 464
        local.get $l3
        i32.load
        i32.load offset=8
        call_indirect $__indirect_function_table (type $t9)
        local.set $l3
        local.get $p0
        i32.load offset=40
        local.set $l4
      end
      local.get $p0
      local.get $l3
      i32.store offset=36
      local.get $l4
      local.get $l3
      local.get $p0
      i32.load offset=8
      local.tee $l2
      local.get $l2
      local.get $l2
      call $f71748
    end
    loop $L6
      local.get $p0
      i32.load offset=52
      local.get $p1
      i32.const 5
      i32.shr_u
      local.tee $l2
      i32.const 2
      i32.shl
      i32.add
      local.tee $l3
      i32.load
      local.tee $l4
      i32.const 1
      local.get $p1
      i32.shl
      local.tee $l5
      i32.and
      i32.eqz
      if $I7
        local.get $l3
        local.get $l4
        local.get $l5
        i32.or
        i32.store
        local.get $p0
        local.get $l2
        local.get $p0
        i32.load offset=60
        local.tee $l3
        local.get $l2
        local.get $l3
        i32.gt_u
        select
        i32.store offset=60
        local.get $p1
        local.get $p0
        i32.load offset=36
        local.get $p1
        i32.const 2
        i32.shl
        i32.add
        i32.load
        local.tee $l2
        i32.ne
        local.set $l3
        local.get $l2
        local.set $p1
        local.get $l3
        br_if $L6
      end
    end)