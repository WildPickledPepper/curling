  (func $f70697 (type $t7) (param $p0 i32)
    (local $l1 i32) (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32)
    block $B0
      local.get $p0
      i32.load offset=84
      local.tee $l5
      local.get $p0
      i32.load offset=44
      local.tee $l8
      i32.add
      local.tee $l2
      local.get $p0
      i32.load offset=48
      i32.const 2147483647
      i32.and
      local.tee $l3
      i32.le_u
      br_if $B0
      local.get $l2
      local.get $l3
      i32.const 1
      i32.shl
      local.tee $l1
      local.get $l1
      local.get $l2
      i32.lt_u
      select
      local.tee $l1
      i32.const 256
      local.get $l1
      i32.const 256
      i32.gt_u
      select
      local.tee $l1
      local.get $l3
      i32.gt_u
      if $I1
        local.get $p0
        i32.const 40
        i32.add
        local.get $l1
        call $f70698
      end
      local.get $l1
      local.get $p0
      i32.load offset=36
      i32.const 2147483647
      i32.and
      i32.gt_u
      if $I2
        local.get $p0
        i32.const 28
        i32.add
        local.set $l6
        block $B3
          local.get $l1
          i32.eqz
          br_if $B3
          local.get $l1
          i32.const 4
          i32.shl
          local.tee $l4
          i32.eqz
          br_if $B3
          call $f69753
          local.tee $l3
          local.get $l4
          i32.const 3139013
          i32.const 3134052
          i32.const 4700888
          i32.load
          local.tee $l9
          local.get $l9
          i32.load
          i32.load offset=20
          call_indirect $__indirect_function_table (type $t5)
          select
          i32.const 3134537
          i32.const 553
          local.get $l3
          i32.load
          i32.load offset=8
          call_indirect $__indirect_function_table (type $t9)
          local.set $l7
        end
        local.get $l6
        i32.load offset=4
        local.tee $l4
        i32.const 0
        i32.gt_s
        if $I4
          local.get $l7
          local.get $l4
          i32.const 4
          i32.shl
          i32.add
          local.set $l9
          local.get $l6
          i32.load
          local.set $l4
          local.get $l7
          local.set $l3
          loop $L5
            local.get $l3
            local.get $l4
            i64.load
            i64.store
            local.get $l3
            local.get $l4
            i64.load offset=8
            i64.store offset=8
            local.get $l4
            i32.const 16
            i32.add
            local.set $l4
            local.get $l3
            i32.const 16
            i32.add
            local.tee $l3
            local.get $l9
            i32.lt_u
            br_if $L5
          end
        end
        block $B6
          local.get $l6
          i32.load offset=8
          i32.const 0
          i32.lt_s
          br_if $B6
          local.get $l6
          i32.load
          local.tee $l4
          i32.eqz
          br_if $B6
          call $f69753
          local.tee $l3
          local.get $l4
          local.get $l3
          i32.load
          i32.load offset=12
          call_indirect $__indirect_function_table (type $t1)
        end
        local.get $l6
        local.get $l1
        i32.store offset=8
        local.get $l6
        local.get $l7
        i32.store
      end
      local.get $p0
      i32.load offset=60
      i32.const 2147483647
      i32.and
      local.get $l1
      i32.ge_u
      br_if $B0
      local.get $p0
      i32.const 52
      i32.add
      local.get $l1
      call $f70699
    end
    local.get $p0
    local.get $l2
    i32.store offset=44
    local.get $p0
    local.get $l2
    i32.store offset=56
    local.get $p0
    local.get $l2
    i32.store offset=32
    local.get $p0
    i32.load offset=40
    local.get $l8
    i32.const 2
    i32.shl
    i32.add
    local.get $p0
    i32.load offset=80
    local.get $l5
    i32.const 2
    i32.shl
    call $f483
    drop
    local.get $p0
    i32.load offset=28
    local.get $l8
    i32.const 4
    i32.shl
    i32.add
    local.get $p0
    i32.load offset=68
    local.get $l5
    i32.const 4
    i32.shl
    call $f483
    drop
    local.get $p0
    i32.load offset=52
    local.get $l8
    i32.const 3
    i32.shl
    i32.add
    local.get $p0
    i32.load offset=92
    local.get $l5
    i32.const 3
    i32.shl
    call $f483
    drop
    local.get $p0
    i32.load offset=84
    if $I7
      local.get $p0
      i32.load offset=108
      i32.load offset=456
      local.set $l3
      i32.const 0
      local.set $l1
      loop $L8
        local.get $p0
        i32.load offset=80
        local.get $l1
        i32.const 2
        i32.shl
        i32.add
        i32.load
        local.tee $l5
        local.get $p0
        i32.load offset=24
        local.get $l1
        local.get $l8
        i32.add
        i32.const 3
        i32.shl
        i32.or
        local.tee $l7
        i32.store offset=68
        block $B9
          local.get $l5
          i32.load8_u offset=43
          local.tee $l2
          i32.const 64
          i32.and
          i32.eqz
          br_if $B9
          local.get $l5
          local.get $l2
          i32.const 191
          i32.and
          i32.store8 offset=43
          local.get $l5
          i32.load8_u offset=41
          i32.const 8
          i32.and
          br_if $B9
          local.get $p0
          i32.load offset=108
          i32.load offset=444
          i32.load
          local.get $l5
          i32.const -64
          i32.sub
          i32.load
          i32.const 2
          i32.shl
          i32.add
          i32.load
          local.tee $l2
          i32.eqz
          br_if $B9
          local.get $l3
          local.get $l2
          i32.load offset=32
          i32.const 2
          i32.shl
          i32.add
          local.get $l7
          i32.store
          local.get $l2
          i32.load offset=28
          local.tee $l2
          i32.eqz
          br_if $B9
          loop $L10
            local.get $l3
            local.get $l2
            i32.load offset=32
            i32.const 2
            i32.shl
            i32.add
            local.get $l5
            i32.load offset=68
            i32.store
            local.get $l2
            i32.load offset=28
            local.tee $l2
            br_if $L10
          end
        end
        local.get $l1
        i32.const 1
        i32.add
        local.tee $l1
        local.get $p0
        i32.load offset=84
        i32.lt_u
        br_if $L8
      end
    end
    local.get $p0
    i32.const 0
    i32.store offset=84
    local.get $p0
    i32.const 0
    i32.store offset=96
    local.get $p0
    i32.const 0
    i32.store offset=72)