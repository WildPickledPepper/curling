  (func $f70657 (type $t183) (param $p0 i32) (param $p1 i64) (param $p2 i64) (param $p3 i32) (param $p4 i32)
    (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l9
    global.set $g0
    local.get $l9
    local.get $p4
    i32.store offset=12
    local.get $p0
    i32.const 40
    i32.add
    local.set $l5
    block $B0
      local.get $p0
      i32.load offset=56
      local.get $p4
      i32.gt_u
      br_if $B0
      local.get $l5
      local.get $p4
      i32.const 2048
      i32.add
      call $f70648
      local.get $p0
      i32.load offset=56
      i32.const 31
      i32.add
      i32.const 5
      i32.shr_u
      local.tee $l6
      local.get $p0
      i32.load offset=232
      i32.const 2147483647
      i32.and
      i32.le_u
      br_if $B0
      call $f69753
      local.tee $l7
      local.get $l6
      i32.const 2
      i32.shl
      i32.const 3133968
      i32.const 3135509
      i32.const 438
      local.get $l7
      i32.load
      i32.load offset=8
      call_indirect $__indirect_function_table (type $t9)
      local.set $l7
      block $B1
        local.get $p0
        i32.load offset=228
        local.tee $l8
        i32.eqz
        br_if $B1
        local.get $l7
        local.get $l8
        local.get $p0
        i32.load offset=232
        i32.const 2
        i32.shl
        call $f483
        drop
        local.get $p0
        i32.load offset=232
        i32.const 0
        i32.lt_s
        br_if $B1
        local.get $p0
        i32.load offset=228
        local.tee $l8
        i32.eqz
        br_if $B1
        call $f69753
        local.tee $l10
        local.get $l8
        local.get $l10
        i32.load
        i32.load offset=12
        call_indirect $__indirect_function_table (type $t1)
      end
      local.get $l7
      local.get $p0
      i32.load offset=232
      local.tee $l8
      i32.const 2
      i32.shl
      i32.add
      i32.const 0
      local.get $l6
      local.get $l8
      i32.sub
      i32.const 2
      i32.shl
      call $f484
      drop
      local.get $p0
      local.get $l6
      i32.store offset=232
      local.get $p0
      local.get $l7
      i32.store offset=228
    end
    local.get $l5
    local.get $p4
    i32.const 1
    i32.add
    local.tee $l6
    local.get $p0
    i32.const 52
    i32.add
    local.tee $l8
    i32.load
    local.tee $l7
    local.get $l6
    local.get $l7
    i32.gt_u
    select
    local.tee $l7
    call $f70648
    local.get $l7
    local.get $l8
    i32.load
    local.tee $l5
    i32.gt_u
    if $I2
      loop $L3
        local.get $p0
        i32.load offset=40
        local.get $l5
        local.get $p0
        i32.load offset=60
        local.tee $p4
        i32.div_u
        local.tee $l6
        i32.const 2
        i32.shl
        i32.add
        i32.load
        local.get $l5
        local.get $p4
        local.get $l6
        i32.mul
        i32.sub
        i32.const 4
        i32.shl
        i32.add
        local.tee $p4
        i64.const -1
        i64.store offset=8 align=4
        local.get $p4
        i32.const 16
        i32.store16 offset=4
        local.get $p4
        i32.const 0
        i32.store
        local.get $l5
        i32.const 1
        i32.add
        local.tee $l5
        local.get $l7
        i32.ne
        br_if $L3
      end
      local.get $l9
      i32.load offset=12
      local.set $p4
    end
    local.get $p0
    local.get $l7
    i32.store offset=52
    local.get $p0
    i32.load offset=228
    local.get $p4
    i32.const 3
    i32.shr_u
    i32.const 536870908
    i32.and
    i32.add
    local.tee $l5
    local.get $l5
    i32.load
    i32.const -2
    local.get $p4
    i32.rotl
    i32.and
    i32.store
    block $B4
      local.get $p0
      i32.load offset=40
      local.get $l9
      i32.load offset=12
      local.tee $l5
      local.get $p0
      i32.load offset=60
      local.tee $p4
      i32.div_u
      local.tee $l6
      i32.const 2
      i32.shl
      i32.add
      i32.load
      local.tee $l7
      local.get $l5
      local.get $p4
      local.get $l6
      i32.mul
      i32.sub
      local.tee $l6
      i32.const 4
      i32.shl
      i32.add
      local.tee $p4
      i32.const 4
      i32.add
      local.tee $l5
      block $B5 (result i32)
        local.get $p4
        i32.load16_u offset=4
        local.tee $p4
        i32.const 2
        i32.and
        if $I6
          local.get $p4
          i32.const 65533
          i32.and
          br $B5
        end
        local.get $p4
        i32.const 8
        i32.and
        br_if $B4
        local.get $l5
        local.get $p4
        i32.const 65519
        i32.and
        i32.store16
        local.get $l7
        local.get $l6
        i32.const 4
        i32.shl
        i32.add
        local.get $p3
        i32.store
        local.get $p0
        local.get $p3
        i32.const 12
        i32.mul
        i32.add
        local.tee $p4
        i32.const 284
        i32.add
        local.set $p0
        block $B7
          local.get $p4
          i32.load offset=292
          i32.const 2147483647
          i32.and
          local.get $p4
          i32.const 288
          i32.add
          local.tee $p4
          i32.load
          local.tee $l6
          i32.le_u
          if $I8
            local.get $p0
            local.get $l9
            i32.const 12
            i32.add
            call $f72545
            br $B7
          end
          local.get $p0
          i32.load
          local.get $l6
          i32.const 2
          i32.shl
          i32.add
          local.get $l9
          i32.load offset=12
          i32.store
          local.get $p4
          local.get $p4
          i32.load
          i32.const 1
          i32.add
          i32.store
        end
        local.get $l5
        i32.load16_u
        i32.const -73
        i32.and
        i32.const 8
        i32.or
      end
      i32.store16
    end
    local.get $l9
    i32.const 16
    i32.add
    global.set $g0)