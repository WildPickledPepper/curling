  (func $f72474 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32)
    global.get $g0
    i32.const -64
    i32.add
    local.tee $l5
    global.set $g0
    local.get $l5
    local.get $p0
    local.get $p0
    i32.load
    i32.load offset=76
    call_indirect $__indirect_function_table (type $t1)
    local.get $l5
    i32.const 32
    i32.add
    local.get $l5
    local.get $p1
    call $f72757
    local.get $p0
    i32.const 48
    i32.add
    local.tee $l2
    local.get $l5
    i32.const 32
    i32.add
    local.tee $l3
    f32.load
    f32.store offset=208
    local.get $l2
    local.get $l3
    f32.load offset=4
    f32.store offset=212
    local.get $l2
    local.get $l3
    f32.load offset=8
    f32.store offset=216
    local.get $l2
    local.get $l3
    f32.load offset=12
    f32.store offset=220
    local.get $l2
    local.get $l3
    f32.load offset=16
    f32.store offset=224
    local.get $l2
    local.get $l3
    f32.load offset=20
    f32.store offset=228
    local.get $l2
    local.get $l3
    f32.load offset=24
    f32.store offset=232
    block $B0
      block $B1
        block $B2
          block $B3
            local.get $l2
            i32.load offset=4
            i32.const 30
            i32.shr_u
            i32.const 2
            i32.sub
            br_table $B3 $B1 $B2
          end
          local.get $l2
          i32.load
          i32.load8_u offset=4785
          br_if $B1
        end
        local.get $l2
        i32.const 16
        i32.add
        local.get $l3
        call $f71596
        br $B0
      end
      local.get $l2
      i32.load offset=268
      local.tee $l3
      i32.const 1048576
      i32.and
      i32.eqz
      if $I4
        local.get $l2
        local.get $l3
        i32.const 2097152
        i32.or
        i32.store offset=268
      end
      local.get $l2
      i32.load
      local.get $l2
      call $f71985
      local.get $l2
      local.get $l2
      i32.load offset=268
      i32.const 1048576
      i32.or
      i32.store offset=268
    end
    block $B5
      block $B6
        block $B7
          block $B8
            local.get $l2
            i32.load offset=4
            local.tee $l3
            i32.const 30
            i32.shr_u
            i32.const 2
            i32.sub
            br_table $B8 $B6 $B7
          end
          local.get $l2
          i32.load
          i32.load8_u offset=4785
          br_if $B6
        end
        local.get $l2
        i32.const 16
        i32.add
        local.get $p1
        call $f71599
        br $B5
      end
      local.get $l2
      i32.load offset=8
      local.tee $l4
      i32.eqz
      if $I9
        local.get $l2
        local.get $l2
        i32.load
        local.get $l3
        i32.const 24
        i32.shr_u
        i32.const 15
        i32.and
        call $f71984
        local.tee $l4
        i32.store offset=8
      end
      local.get $l4
      local.get $p1
      f32.load
      f32.store offset=144
      local.get $l4
      local.get $p1
      f32.load offset=4
      f32.store offset=148
      local.get $l4
      local.get $p1
      f32.load offset=8
      f32.store offset=152
      local.get $l4
      local.get $p1
      f32.load offset=12
      f32.store offset=156
      local.get $l4
      local.get $p1
      f32.load offset=16
      f32.store offset=160
      local.get $l4
      local.get $p1
      f32.load offset=20
      f32.store offset=164
      local.get $l4
      local.get $p1
      f32.load offset=24
      f32.store offset=168
      local.get $l2
      i32.load
      local.get $l2
      call $f71985
      local.get $l2
      local.get $l2
      i32.load offset=268
      i32.const 1024
      i32.or
      i32.store offset=268
    end
    i32.const 0
    local.set $p1
    local.get $p0
    i32.load offset=16
    local.tee $l2
    if $I10 (result i32)
      local.get $l2
      i32.load offset=36
      local.set $l7
      local.get $l2
      i32.load offset=40
    else
      i32.const 0
    end
    local.set $l6
    loop $L11
      local.get $p1
      local.get $l6
      local.get $p1
      local.get $l6
      i32.gt_u
      select
      local.set $l4
      block $B12
        loop $L13
          local.get $p1
          local.get $l4
          i32.eq
          br_if $B12
          local.get $p1
          i32.const 3
          i32.shl
          local.set $l2
          local.get $p1
          i32.const 1
          i32.add
          local.tee $l3
          local.set $p1
          local.get $l2
          local.get $l7
          i32.add
          local.tee $l2
          i32.load8_u
          br_if $L13
        end
        local.get $l2
        i32.load offset=4
        local.tee $p1
        i32.eqz
        br_if $B12
        local.get $p1
        i32.load offset=56
        local.set $l2
        local.get $p0
        local.get $p1
        i32.load offset=8
        i32.eq
        if $I14
          local.get $l2
          i32.const 0
          local.get $l2
          i32.load
          i32.load offset=12
          call_indirect $__indirect_function_table (type $t1)
        end
        local.get $p0
        local.get $p1
        i32.load offset=12
        i32.eq
        if $I15
          local.get $l2
          i32.const 1
          local.get $l2
          i32.load
          i32.load offset=12
          call_indirect $__indirect_function_table (type $t1)
        end
        local.get $l3
        local.set $p1
        br $L11
      end
    end
    local.get $l5
    i32.const -64
    i32.sub
    global.set $g0)
