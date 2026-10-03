  (func $f71772 (type $t4) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32)
    (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i64)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l9
    global.set $g0
    local.get $p2
    i32.load
    local.set $l4
    local.get $p0
    i32.load offset=40
    local.set $l5
    local.get $p1
    i32.load offset=24
    local.set $l8
    call $f69753
    local.tee $l6
    i32.const -1
    i32.const -1
    local.get $l4
    local.get $l5
    i32.add
    i32.const 1
    i32.add
    local.tee $l4
    i64.extend_i32_u
    i64.const 28
    i64.mul
    local.tee $l12
    i32.wrap_i64
    local.tee $l5
    i32.const 4
    i32.add
    local.tee $l7
    local.get $l5
    local.get $l7
    i32.gt_u
    select
    local.get $l12
    i64.const 32
    i64.shr_u
    i32.wrap_i64
    select
    i32.const 3177145
    i32.const 3176295
    i32.const 4700888
    i32.load
    local.tee $l5
    local.get $l5
    i32.load
    i32.load offset=20
    call_indirect $__indirect_function_table (type $t5)
    select
    i32.const 3175524
    i32.const 725
    local.get $l6
    i32.load
    i32.load offset=8
    call_indirect $__indirect_function_table (type $t9)
    local.tee $l5
    local.get $l4
    i32.store
    local.get $l5
    i32.const 4
    i32.add
    local.set $l4
    local.get $l8
    i32.const 1
    i32.shr_u
    local.set $l6
    local.get $p2
    i32.load
    local.get $p0
    i32.load offset=40
    i32.add
    i32.const 2
    i32.shl
    i32.const 4
    i32.add
    local.tee $l5
    if $I0 (result i32)
      call $f69753
      local.tee $l7
      local.get $l5
      i32.const 3176237
      i32.const 3175524
      i32.const 726
      local.get $l7
      i32.load
      i32.load offset=8
      call_indirect $__indirect_function_table (type $t9)
    else
      i32.const 0
    end
    local.set $l7
    local.get $l4
    local.get $p0
    i32.load offset=8
    local.get $l6
    i32.const 28
    i32.mul
    local.tee $l10
    call $f483
    local.set $l5
    local.get $l7
    local.get $p0
    i32.load offset=36
    local.get $l6
    i32.const 2
    i32.shl
    local.tee $l11
    call $f483
    local.set $l7
    local.get $l9
    local.get $l6
    i32.store offset=12
    local.get $l5
    local.get $l10
    i32.add
    local.tee $l4
    local.get $p1
    f32.load
    f32.store
    local.get $l4
    local.get $p1
    f32.load offset=4
    f32.store offset=4
    local.get $l4
    local.get $p1
    f32.load offset=8
    f32.store offset=8
    local.get $l4
    local.get $p1
    f32.load offset=12
    f32.store offset=12
    local.get $l4
    local.get $p1
    f32.load offset=16
    f32.store offset=16
    local.get $l4
    local.get $p1
    f32.load offset=20
    f32.store offset=20
    local.get $l4
    local.get $p2
    i32.load
    local.get $p1
    i32.load offset=24
    i32.const 1
    i32.shr_u
    i32.add
    i32.const 1
    i32.shl
    i32.const 2
    i32.add
    i32.store offset=24
    local.get $l7
    local.get $l11
    i32.add
    local.tee $l10
    local.get $p3
    i32.store
    block $B1
      local.get $p0
      i32.load offset=52
      local.tee $p1
      i32.eqz
      br_if $B1
      local.get $p1
      local.get $p3
      i32.const 3
      i32.shr_u
      i32.const 536870908
      i32.and
      i32.add
      i32.load
      local.get $p3
      i32.shr_u
      i32.const 1
      i32.and
      i32.eqz
      br_if $B1
      local.get $p1
      local.get $l8
      i32.const 6
      i32.shr_u
      local.tee $l8
      i32.const 2
      i32.shl
      i32.add
      local.tee $p1
      local.get $p1
      i32.load
      i32.const 1
      local.get $l6
      i32.shl
      i32.or
      i32.store
      local.get $p0
      local.get $l8
      local.get $p0
      i32.load offset=60
      local.tee $p1
      local.get $p1
      local.get $l8
      i32.lt_u
      select
      i32.store offset=60
    end
    local.get $p0
    i32.load offset=40
    local.get $l6
    i32.sub
    local.tee $p1
    if $I2
      local.get $l4
      local.get $p2
      i32.load
      i32.const 28
      i32.mul
      i32.add
      i32.const 28
      i32.add
      local.get $p0
      i32.load offset=8
      local.get $l6
      i32.const 28
      i32.mul
      i32.add
      local.get $p1
      i32.const 28
      i32.mul
      call $f483
      drop
      local.get $l10
      local.get $p2
      i32.load
      i32.const 2
      i32.shl
      i32.add
      i32.const 4
      i32.add
      local.get $p0
      i32.load offset=36
      local.get $l6
      i32.const 2
      i32.shl
      i32.add
      local.get $p0
      i32.load offset=40
      local.get $l6
      i32.sub
      i32.const 2
      i32.shl
      call $f483
      drop
    end
    local.get $p0
    i32.load offset=8
    local.tee $p1
    if $I3
      call $f69753
      local.tee $l4
      local.get $p1
      i32.const 4
      i32.sub
      local.get $l4
      i32.load
      i32.load offset=12
      call_indirect $__indirect_function_table (type $t1)
    end
    local.get $p0
    local.get $l5
    i32.store offset=8
    local.get $p0
    i32.load offset=36
    local.tee $p1
    if $I4
      call $f69753
      local.tee $l4
      local.get $p1
      local.get $l4
      i32.load
      i32.load offset=12
      call_indirect $__indirect_function_table (type $t1)
    end
    local.get $p0
    local.get $l7
    i32.store offset=36
    local.get $l9
    local.get $l6
    i32.const 1
    i32.add
    local.tee $p1
    i32.store offset=12
    local.get $p0
    local.get $l9
    i32.const 12
    i32.add
    local.get $p2
    call $f71776
    local.get $p0
    local.get $p0
    i32.load offset=40
    local.get $p2
    i32.load
    i32.add
    i32.const 1
    i32.add
    i32.store offset=40
    local.get $p0
    i32.load offset=36
    local.get $p1
    i32.const 2
    i32.shl
    i32.add
    local.get $p3
    i32.store
    local.get $p2
    i32.load
    local.get $p1
    i32.add
    local.tee $p1
    local.get $p0
    i32.load offset=40
    i32.lt_u
    if $I5
      loop $L6
        block $B7
          local.get $p3
          local.get $p0
          i32.load offset=36
          local.get $p1
          i32.const 2
          i32.shl
          i32.add
          local.tee $l5
          i32.load
          local.tee $l4
          i32.eq
          if $I8
            local.get $l5
            local.get $l6
            i32.store
            br $B7
          end
          local.get $l4
          local.get $l6
          i32.ge_u
          if $I9
            local.get $l5
            local.get $l4
            local.get $p2
            i32.load
            i32.add
            i32.const 1
            i32.add
            i32.store
            br $B7
          end
          local.get $p1
          i32.const 1
          i32.and
          i32.eqz
          br_if $B7
          local.get $p0
          i32.load offset=8
          local.get $l4
          i32.const 28
          i32.mul
          i32.add
          local.tee $l4
          local.get $l4
          i32.load offset=24
          local.get $p2
          i32.load
          i32.const 1
          i32.shl
          i32.add
          i32.const 2
          i32.add
          i32.const -2
          i32.and
          i32.store offset=24
        end
        local.get $p0
        i32.load offset=8
        local.get $p1
        i32.const 28
        i32.mul
        i32.add
        local.tee $l4
        i32.load offset=24
        local.tee $l5
        i32.const 1
        i32.and
        i32.eqz
        if $I10
          local.get $l4
          local.get $l5
          local.get $p2
          i32.load
          i32.const 1
          i32.shl
          i32.add
          i32.const 2
          i32.add
          i32.const -2
          i32.and
          i32.store offset=24
        end
        local.get $p1
        i32.const 1
        i32.add
        local.tee $p1
        local.get $p0
        i32.load offset=40
        i32.lt_u
        br_if $L6
      end
    end
    local.get $l9
    i32.const 16
    i32.add
    global.set $g0)