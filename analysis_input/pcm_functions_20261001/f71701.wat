  (func $f71701 (type $t7) (param $p0 i32)
    (local $l1 i32) (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l6
    global.set $g0
    local.get $l6
    local.get $p0
    i32.load offset=284
    local.tee $l1
    if $I0 (result i32)
      call $f69753
      local.tee $l4
      local.get $l1
      i32.const 3173013
      i32.const 3172190
      i32.const 4700888
      i32.load
      local.tee $l1
      local.get $l1
      i32.load
      i32.load offset=20
      call_indirect $__indirect_function_table (type $t5)
      select
      i32.const 3174354
      i32.const 180
      local.get $l4
      i32.load
      i32.load offset=8
      call_indirect $__indirect_function_table (type $t9)
    else
      i32.const 0
    end
    local.tee $l5
    i32.store offset=12
    block $B1
      local.get $p0
      i32.load offset=268
      local.tee $l1
      local.get $p0
      i32.load offset=272
      i32.const 2147483647
      i32.and
      i32.ge_u
      if $I2
        local.get $l6
        i32.const 12
        i32.add
        local.set $l9
        block $B3 (result i32)
          i32.const 0
          local.get $p0
          i32.const 4
          i32.add
          local.tee $l2
          i32.load offset=268
          i32.const 2147483647
          i32.and
          local.tee $l3
          i32.const 1
          i32.shl
          i32.const 1
          local.get $l3
          select
          local.tee $l8
          i32.eqz
          br_if $B3
          drop
          block $B4
            local.get $l8
            i32.const 2
            i32.shl
            local.tee $l3
            i32.const 256
            i32.gt_u
            br_if $B4
            local.get $l2
            i32.load8_u offset=256
            br_if $B4
            local.get $l2
            i32.const 1
            i32.store8 offset=256
            local.get $l2
            br $B3
          end
          i32.const 0
          local.get $l3
          i32.eqz
          br_if $B3
          drop
          call $f69753
          local.tee $l1
          local.get $l3
          i32.const 3173013
          i32.const 3172190
          i32.const 4700888
          i32.load
          local.tee $l7
          local.get $l7
          i32.load
          i32.load offset=20
          call_indirect $__indirect_function_table (type $t5)
          select
          i32.const 3172148
          i32.const 553
          local.get $l1
          i32.load
          i32.load offset=8
          call_indirect $__indirect_function_table (type $t9)
        end
        local.set $l4
        local.get $l4
        local.get $l2
        i32.load offset=264
        local.tee $l3
        i32.const 0
        i32.gt_s
        if $I5 (result i32)
          local.get $l4
          local.get $l3
          i32.const 2
          i32.shl
          i32.add
          local.set $l7
          local.get $l2
          i32.load offset=260
          local.set $l3
          local.get $l4
          local.set $l1
          loop $L6
            local.get $l1
            local.get $l3
            i32.load
            i32.store
            local.get $l3
            i32.const 4
            i32.add
            local.set $l3
            local.get $l1
            i32.const 4
            i32.add
            local.tee $l1
            local.get $l7
            i32.lt_u
            br_if $L6
          end
          local.get $l2
          i32.load offset=264
        else
          local.get $l3
        end
        i32.const 2
        i32.shl
        i32.add
        local.get $l9
        i32.load
        i32.store
        block $B7
          local.get $l2
          i32.load offset=268
          i32.const 0
          i32.lt_s
          br_if $B7
          local.get $l2
          i32.load offset=260
          local.tee $l3
          local.get $l2
          i32.eq
          if $I8
            local.get $l2
            i32.const 0
            i32.store8 offset=256
            br $B7
          end
          local.get $l3
          i32.eqz
          br_if $B7
          call $f69753
          local.tee $l1
          local.get $l3
          local.get $l1
          i32.load
          i32.load offset=12
          call_indirect $__indirect_function_table (type $t1)
        end
        local.get $l2
        local.get $l8
        i32.store offset=268
        local.get $l2
        local.get $l4
        i32.store offset=260
        local.get $l2
        local.get $l2
        i32.load offset=264
        i32.const 1
        i32.add
        i32.store offset=264
        br $B1
      end
      local.get $p0
      i32.load offset=264
      local.get $l1
      i32.const 2
      i32.shl
      i32.add
      local.get $l5
      i32.store
      local.get $p0
      local.get $p0
      i32.load offset=268
      i32.const 1
      i32.add
      i32.store offset=268
    end
    local.get $l5
    local.get $l5
    local.get $p0
    i32.load offset=276
    i32.const 60
    i32.mul
    i32.add
    i32.const 60
    i32.sub
    local.tee $l1
    i32.le_u
    if $I9
      local.get $p0
      i32.load offset=288
      local.set $l4
      loop $L10
        local.get $l1
        local.get $l4
        i32.store
        local.get $p0
        local.get $l1
        i32.store offset=288
        local.get $l1
        local.set $l4
        local.get $l1
        i32.const 60
        i32.sub
        local.tee $l1
        local.get $l5
        i32.ge_u
        br_if $L10
      end
    end
    local.get $l6
    i32.const 16
    i32.add
    global.set $g0)