  (func $f71555 (type $t7) (param $p0 i32)
    (local $l1 i32) (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i64)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l5
    global.set $g0
    block $B0
      local.get $p0
      i32.load offset=44
      local.tee $l1
      i32.load8_u offset=9
      i32.const 2
      i32.ne
      if $I1 (result i32)
        local.get $p0
        i32.const 92
        i32.add
        local.tee $l1
        local.get $l1
        i32.load16_u
        i32.const 65534
        i32.and
        i32.store16
        local.get $p0
        i32.load offset=40
        local.set $l1
        global.get $g0
        i32.const 16
        i32.sub
        local.tee $l2
        global.set $g0
        block $B2
          local.get $l1
          i32.load offset=2344
          i32.eqz
          br_if $B2
          local.get $p0
          i32.load16_u offset=152
          local.tee $l3
          i32.const 64
          i32.and
          if $I3
            local.get $p0
            local.get $l3
            i32.const 65471
            i32.and
            i32.store16 offset=152
            local.get $l1
            i32.const 0
            i32.store8 offset=2281
            local.get $p0
            i32.load16_u offset=152
            local.set $l3
          end
          local.get $p0
          local.get $l3
          i32.const 128
          i32.or
          i32.store16 offset=152
          local.get $l3
          i32.const 32
          i32.and
          br_if $B2
          local.get $l2
          local.get $p0
          i32.load offset=44
          i32.store offset=8
          local.get $l1
          i32.const 2240
          i32.add
          local.get $l2
          i32.const 8
          i32.add
          local.get $l2
          i32.const 15
          i32.add
          call $f71404
          local.set $l1
          local.get $l2
          i32.load8_u offset=15
          i32.eqz
          if $I4
            local.get $l1
            local.get $l2
            i32.load offset=8
            i32.store
          end
          local.get $p0
          local.get $p0
          i32.load16_u offset=152
          i32.const 32
          i32.or
          i32.store16 offset=152
        end
        local.get $l2
        i32.const 16
        i32.add
        global.set $g0
        local.get $p0
        i32.load offset=44
      else
        local.get $l1
      end
      i32.load8_u offset=44
      i32.const 16
      i32.and
      i32.eqz
      br_if $B0
      local.get $p0
      i32.load offset=40
      local.set $l1
      local.get $l5
      local.get $p0
      i32.store offset=8
      local.get $l1
      i32.const 4624
      i32.add
      local.get $l5
      i32.const 8
      i32.add
      local.get $l5
      i32.const 15
      i32.add
      call $f71568
      local.set $l1
      local.get $l5
      i32.load8_u offset=15
      br_if $B0
      local.get $l1
      local.get $l5
      i32.load offset=8
      i32.store
    end
    block $B5
      local.get $p0
      i32.load offset=156
      i32.const -3
      i32.gt_u
      br_if $B5
      local.get $p0
      i32.load offset=44
      i32.load16_u offset=44
      i32.const 3
      i32.and
      i32.const 3
      i32.eq
      br_if $B5
      local.get $p0
      i32.load8_u offset=153
      i32.const 16
      i32.and
      br_if $B5
      local.get $p0
      i32.load offset=32
      local.tee $l1
      i32.eqz
      br_if $B5
      loop $L6
        local.get $l1
        call $f71455
        local.get $l1
        i32.load
        local.tee $l1
        br_if $L6
      end
    end
    local.get $p0
    i32.load offset=28
    local.tee $l6
    if $I7
      i32.const 0
      local.set $l1
      loop $L8
        local.get $l1
        local.tee $l2
        i32.const 1
        i32.add
        local.set $l1
        block $B9
          local.get $p0
          i32.load offset=20
          local.get $l2
          i32.const 2
          i32.shl
          i32.add
          i32.load
          local.tee $l2
          i32.load8_u offset=20
          i32.const 253
          i32.and
          i32.eqz
          br_if $B9
          local.get $l2
          i32.load8_u offset=21
          i32.const 32
          i32.and
          br_if $B9
          local.get $l2
          call $f71361
          i32.eqz
          br_if $B9
          local.get $l2
          i32.load8_u offset=20
          i32.const 2
          i32.gt_u
          br_if $B9
          local.get $p0
          i32.load offset=40
          local.tee $l3
          local.get $l2
          i32.load8_u offset=20
          local.tee $l8
          i32.const 2
          i32.shl
          i32.add
          i32.const 88
          i32.add
          local.tee $l10
          i32.load
          local.tee $l7
          local.get $l3
          local.get $l8
          i32.const 12
          i32.mul
          i32.add
          local.tee $l3
          i32.load offset=56
          i32.lt_u
          if $I10
            local.get $l3
            i32.const 52
            i32.add
            local.tee $l8
            i32.load
            local.tee $l4
            local.get $l7
            i32.const 2
            i32.shl
            i32.add
            local.tee $l9
            i32.load
            local.set $l3
            local.get $l9
            local.get $l4
            local.get $l2
            i32.load offset=8
            local.tee $l2
            i32.const 2
            i32.shl
            local.tee $l9
            i32.add
            i32.load
            local.tee $l4
            i32.store
            local.get $l8
            i32.load
            local.get $l9
            i32.add
            local.get $l3
            i32.store
            local.get $l3
            local.get $l2
            i32.store offset=8
            local.get $l4
            local.get $l7
            i32.store offset=8
            local.get $l10
            i32.load
            local.set $l7
          end
          local.get $l10
          local.get $l7
          i32.const 1
          i32.add
          i32.store
        end
        local.get $l1
        local.get $l6
        i32.ne
        br_if $L8
      end
    end
    block $B11
      local.get $p0
      i32.load offset=44
      local.tee $l1
      i32.load8_u offset=44
      i32.const 32
      i32.and
      i32.eqz
      br_if $B11
      block $B12
        local.get $l1
        i32.load8_u offset=9
        i32.const 2
        i32.eq
        if $I13
          local.get $p0
          i64.load offset=144
          local.tee $l11
          i64.const 9
          i64.shr_u
          i32.wrap_i64
          local.tee $l6
          i32.const -1
          i32.eq
          br_if $B11
          local.get $l6
          i32.const 32
          i32.add
          i32.const 5
          i32.shr_u
          local.tee $l3
          local.get $p0
          i32.load offset=40
          local.tee $l2
          i32.const 4732
          i32.add
          i32.load
          i32.const 2147483647
          i32.and
          i32.le_u
          if $I14
            local.get $l2
            i32.load offset=4728
            local.set $l1
            br $B12
          end
          call $f69753
          local.tee $l1
          local.get $l3
          i32.const 2
          i32.shl
          i32.const 3171167
          i32.const 3171183
          i32.const 438
          local.get $l1
          i32.load
          i32.load offset=8
          call_indirect $__indirect_function_table (type $t9)
          local.set $l1
          block $B15
            local.get $l2
            i32.load offset=4728
            local.tee $p0
            i32.eqz
            br_if $B15
            local.get $l1
            local.get $p0
            local.get $l2
            i32.load offset=4732
            i32.const 2
            i32.shl
            call $f483
            drop
            local.get $l2
            i32.load offset=4732
            i32.const 0
            i32.lt_s
            br_if $B15
            local.get $l2
            i32.load offset=4728
            local.tee $p0
            i32.eqz
            br_if $B15
            call $f69753
            local.tee $l4
            local.get $p0
            local.get $l4
            i32.load
            i32.load offset=12
            call_indirect $__indirect_function_table (type $t1)
          end
          local.get $l1
          local.get $l2
          i32.load offset=4732
          local.tee $p0
          i32.const 2
          i32.shl
          i32.add
          i32.const 0
          local.get $l3
          local.get $p0
          i32.sub
          i32.const 2
          i32.shl
          call $f484
          drop
          local.get $l2
          local.get $l3
          i32.store offset=4732
          local.get $l2
          local.get $l1
          i32.store offset=4728
          br $B12
        end
        local.get $p0
        i64.load offset=144
        local.tee $l11
        i64.const 9
        i64.shr_u
        i32.wrap_i64
        local.tee $l6
        i32.const 32
        i32.add
        i32.const 5
        i32.shr_u
        local.tee $l3
        local.get $p0
        i32.load offset=40
        local.tee $l2
        i32.const 4720
        i32.add
        i32.load
        i32.const 2147483647
        i32.and
        i32.le_u
        if $I16
          local.get $l2
          i32.load offset=4716
          local.set $l1
          br $B12
        end
        call $f69753
        local.tee $l1
        local.get $l3
        i32.const 2
        i32.shl
        i32.const 3171167
        i32.const 3171183
        i32.const 438
        local.get $l1
        i32.load
        i32.load offset=8
        call_indirect $__indirect_function_table (type $t9)
        local.set $l1
        block $B17
          local.get $l2
          i32.load offset=4716
          local.tee $p0
          i32.eqz
          br_if $B17
          local.get $l1
          local.get $p0
          local.get $l2
          i32.load offset=4720
          i32.const 2
          i32.shl
          call $f483
          drop
          local.get $l2
          i32.load offset=4720
          i32.const 0
          i32.lt_s
          br_if $B17
          local.get $l2
          i32.load offset=4716
          local.tee $p0
          i32.eqz
          br_if $B17
          call $f69753
          local.tee $l4
          local.get $p0
          local.get $l4
          i32.load
          i32.load offset=12
          call_indirect $__indirect_function_table (type $t1)
        end
        local.get $l1
        local.get $l2
        i32.load offset=4720
        local.tee $p0
        i32.const 2
        i32.shl
        i32.add
        i32.const 0
        local.get $l3
        local.get $p0
        i32.sub
        i32.const 2
        i32.shl
        call $f484
        drop
        local.get $l2
        local.get $l3
        i32.store offset=4720
        local.get $l2
        local.get $l1
        i32.store offset=4716
      end
      local.get $l1
      local.get $l11
      i64.const 14
      i64.shr_u
      i32.wrap_i64
      i32.const 134217727
      i32.and
      i32.const 2
      i32.shl
      i32.add
      local.tee $l1
      local.get $l1
      i32.load
      i32.const 1
      local.get $l6
      i32.shl
      i32.or
      i32.store
    end
    local.get $l5
    i32.const 16
    i32.add
    global.set $g0)