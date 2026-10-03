  (func $f73036 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32)
    global.get $g0
    i32.const 32
    i32.sub
    local.tee $l3
    global.set $g0
    block $B0
      local.get $p0
      i32.load8_u offset=133
      local.get $p1
      i32.eq
      br_if $B0
      i32.const 4758660
      i32.load8_u
      i32.eqz
      br_if $B0
      local.get $p0
      call $f78679
    end
    local.get $p0
    local.get $p1
    i32.store8 offset=133
    block $B1
      local.get $p0
      i32.load offset=52
      local.tee $l2
      i32.eqz
      br_if $B1
      local.get $l3
      i32.const 8
      i32.add
      local.get $l2
      local.get $l2
      i32.load
      i32.load offset=216
      call_indirect $__indirect_function_table (type $t1)
      local.get $l3
      i32.load16_u offset=8
      i32.const 1
      i32.and
      local.get $p1
      i32.eq
      br_if $B1
      i32.const 9
      call $f80140
      call $f73714
      local.get $l3
      i64.const 4294967296
      i64.store offset=16
      local.get $l3
      i64.const 4294967296
      i64.store offset=8
      block $B2
        local.get $p0
        i32.load offset=48
        local.tee $l4
        local.get $p0
        i32.const 44
        i32.add
        local.tee $l7
        i32.eq
        br_if $B2
        i32.const 1
        local.set $l5
        local.get $l4
        local.set $l2
        loop $L3
          block $B4
            local.get $l2
            local.get $l4
            i32.ne
            br_if $B4
            local.get $l5
            i32.const 63
            i32.gt_u
            br_if $B4
            local.get $l3
            i32.const 8
            i32.add
            i32.const 32
            i32.const 4
            i32.const 4
            call $f545
            local.get $l3
            i32.load offset=20
            local.set $l5
          end
          local.get $l2
          i32.load offset=8
          local.set $l4
          local.get $l3
          i32.load offset=16
          local.tee $l8
          i32.const 1
          i32.add
          local.tee $l6
          local.get $l5
          i32.const 1
          i32.shr_u
          i32.gt_u
          if $I5
            local.get $l3
            i32.const 8
            i32.add
            call $f552
          end
          local.get $l3
          local.get $l6
          i32.store offset=16
          local.get $l3
          i32.load offset=8
          local.get $l8
          i32.const 2
          i32.shl
          i32.add
          local.get $l4
          i32.store
          local.get $l2
          i32.load offset=4
          local.tee $l2
          local.get $l7
          i32.eq
          br_if $B2
          local.get $p0
          i32.load offset=48
          local.set $l4
          local.get $l3
          i32.load offset=20
          local.set $l5
          br $L3
        end
        unreachable
      end
      local.get $p1
      if $I6
        local.get $p0
        i32.load offset=52
        local.get $p0
        i32.load offset=140
        i32.const 1
        call $f73710
        local.get $p0
        i32.load offset=52
        local.tee $l2
        i32.const 1
        i32.const 1
        local.get $l2
        i32.load
        i32.load offset=208
        call_indirect $__indirect_function_table (type $t2)
      end
      block $B7
        local.get $l3
        i32.load offset=16
        i32.eqz
        br_if $B7
        local.get $p0
        i32.load8_u offset=84
        i32.eqz
        br_if $B7
        local.get $l3
        i32.load offset=8
        local.set $l2
        loop $L8
          block $B9
            local.get $l2
            i32.load
            local.tee $l6
            i32.load offset=28
            local.tee $l4
            i32.eqz
            br_if $B9
            local.get $l4
            call $f80180
            i32.eqz
            br_if $B9
            local.get $l6
            local.get $l6
            i32.load
            i32.load offset=104
            call_indirect $__indirect_function_table (type $t5)
            i32.eqz
            br_if $B9
            local.get $l6
            i32.const 0
            local.get $l6
            i32.load
            i32.load offset=148
            call_indirect $__indirect_function_table (type $t1)
          end
          local.get $l2
          i32.const 4
          i32.add
          local.tee $l2
          local.get $l3
          i32.load offset=8
          local.get $l3
          i32.load offset=16
          i32.const 2
          i32.shl
          i32.add
          i32.ne
          br_if $L8
        end
      end
      local.get $p1
      i32.eqz
      if $I10
        local.get $p0
        i32.load offset=52
        local.tee $l2
        i32.const 1
        i32.const 0
        local.get $l2
        i32.load
        i32.load offset=208
        call_indirect $__indirect_function_table (type $t2)
        local.get $p0
        i32.load offset=52
        local.get $p0
        i32.load offset=140
        i32.const 0
        call $f73710
      end
      local.get $p0
      call $f73040
      local.get $p0
      local.get $p0
      i32.load offset=136
      call $f73059
      local.get $p0
      call $f73060
      local.get $l3
      i32.const 24
      i32.add
      local.get $p0
      i32.load offset=52
      local.tee $l2
      local.get $l2
      i32.load
      i32.load offset=216
      call_indirect $__indirect_function_table (type $t1)
      local.get $p0
      local.get $l3
      i32.load16_u offset=24
      i32.const 1
      i32.and
      local.tee $l2
      i32.store8 offset=133
      local.get $p0
      local.get $p1
      i32.store8 offset=150
      block $B11
        local.get $l2
        br_if $B11
        local.get $p0
        i32.load offset=52
        local.tee $l2
        i32.eqz
        br_if $B11
        i32.const 9
        call $f80140
        call $f73714
        local.get $l2
        i32.load16_u offset=4
        local.tee $l5
        i32.const 5
        i32.ne
        br_if $B11
        local.get $l3
        i32.const 24
        i32.add
        local.get $l2
        i32.const 0
        local.get $l5
        i32.const 5
        i32.eq
        select
        local.tee $l2
        local.get $l2
        i32.load
        i32.load offset=216
        call_indirect $__indirect_function_table (type $t1)
        local.get $l3
        i32.load8_u offset=24
        i32.const 1
        i32.and
        br_if $B11
        local.get $l2
        local.get $l2
        i32.load
        i32.load offset=28
        call_indirect $__indirect_function_table (type $t5)
        i32.eqz
        br_if $B11
        local.get $l2
        local.get $l2
        i32.load
        i32.load offset=316
        call_indirect $__indirect_function_table (type $t7)
      end
      local.get $l3
      i32.const 8
      i32.add
      call $f554
      drop
    end
    local.get $l3
    i32.const 32
    i32.add
    global.set $g0)