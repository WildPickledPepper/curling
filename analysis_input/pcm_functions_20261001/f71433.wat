  (func $f71433 (type $t15) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 i32)
    (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i64)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l12
    global.set $g0
    block $B0
      local.get $p0
      i32.load offset=2392
      local.tee $l7
      i32.load offset=12
      local.tee $l9
      local.get $l7
      i32.load offset=8
      local.tee $l11
      i32.const 12
      i32.mul
      i32.add
      local.tee $l10
      i32.load offset=4
      local.tee $l8
      if $I1
        local.get $l10
        local.get $l8
        i32.load
        i32.store offset=4
        br $B0
      end
      block $B2
        local.get $l10
        i32.load offset=8
        local.tee $l8
        local.get $l7
        i32.load
        i32.eq
        br_if $B2
        local.get $l7
        i32.load offset=4
        local.set $l13
        local.get $l10
        local.get $l8
        i32.const 1
        i32.add
        i32.store offset=8
        local.get $l9
        local.get $l11
        i32.const 12
        i32.mul
        i32.add
        i32.load
        local.tee $l10
        i32.eqz
        br_if $B2
        local.get $l10
        local.get $l8
        local.get $l13
        i32.mul
        i32.add
        local.set $l8
        br $B0
      end
      local.get $l7
      call $f71372
      local.set $l8
    end
    local.get $l8
    local.get $p0
    local.get $p1
    local.get $p6
    call $f71554
    drop
    block $B3
      local.get $l8
      i32.load offset=100
      i32.load8_u offset=28
      i32.const 32
      i32.and
      i32.eqz
      br_if $B3
      local.get $l8
      i32.load offset=156
      i32.const -3
      i32.gt_u
      br_if $B3
      block $B4
        local.get $l8
        i32.load offset=44
        i32.load8_u offset=9
        i32.const 2
        i32.eq
        if $I5
          local.get $l8
          i64.load offset=144
          local.tee $l14
          i64.const 9
          i64.shr_u
          i32.wrap_i64
          local.tee $l10
          i32.const -1
          i32.eq
          br_if $B3
          local.get $l10
          i32.const 32
          i32.add
          i32.const 5
          i32.shr_u
          local.tee $p6
          local.get $p0
          i32.const 4732
          i32.add
          i32.load
          i32.const 2147483647
          i32.and
          i32.le_u
          if $I6
            local.get $p0
            i32.load offset=4728
            local.set $l7
            br $B4
          end
          call $f69753
          local.tee $l7
          local.get $p6
          i32.const 2
          i32.shl
          i32.const 3158048
          i32.const 3160746
          i32.const 438
          local.get $l7
          i32.load
          i32.load offset=8
          call_indirect $__indirect_function_table (type $t9)
          local.set $l7
          block $B7
            local.get $p0
            i32.load offset=4728
            local.tee $l9
            i32.eqz
            br_if $B7
            local.get $l7
            local.get $l9
            local.get $p0
            i32.load offset=4732
            i32.const 2
            i32.shl
            call $f483
            drop
            local.get $p0
            i32.load offset=4732
            i32.const 0
            i32.lt_s
            br_if $B7
            local.get $p0
            i32.load offset=4728
            local.tee $l9
            i32.eqz
            br_if $B7
            call $f69753
            local.tee $l11
            local.get $l9
            local.get $l11
            i32.load
            i32.load offset=12
            call_indirect $__indirect_function_table (type $t1)
          end
          local.get $l7
          local.get $p0
          i32.load offset=4732
          local.tee $l9
          i32.const 2
          i32.shl
          i32.add
          i32.const 0
          local.get $p6
          local.get $l9
          i32.sub
          i32.const 2
          i32.shl
          call $f484
          drop
          local.get $p0
          local.get $p6
          i32.store offset=4732
          local.get $p0
          local.get $l7
          i32.store offset=4728
          br $B4
        end
        local.get $l8
        i64.load offset=144
        local.tee $l14
        i64.const 9
        i64.shr_u
        i32.wrap_i64
        local.tee $l10
        i32.const 32
        i32.add
        i32.const 5
        i32.shr_u
        local.tee $p6
        local.get $p0
        i32.const 4720
        i32.add
        i32.load
        i32.const 2147483647
        i32.and
        i32.le_u
        if $I8
          local.get $p0
          i32.load offset=4716
          local.set $l7
          br $B4
        end
        call $f69753
        local.tee $l7
        local.get $p6
        i32.const 2
        i32.shl
        i32.const 3158048
        i32.const 3160746
        i32.const 438
        local.get $l7
        i32.load
        i32.load offset=8
        call_indirect $__indirect_function_table (type $t9)
        local.set $l7
        block $B9
          local.get $p0
          i32.load offset=4716
          local.tee $l9
          i32.eqz
          br_if $B9
          local.get $l7
          local.get $l9
          local.get $p0
          i32.load offset=4720
          i32.const 2
          i32.shl
          call $f483
          drop
          local.get $p0
          i32.load offset=4720
          i32.const 0
          i32.lt_s
          br_if $B9
          local.get $p0
          i32.load offset=4716
          local.tee $l9
          i32.eqz
          br_if $B9
          call $f69753
          local.tee $l11
          local.get $l9
          local.get $l11
          i32.load
          i32.load offset=12
          call_indirect $__indirect_function_table (type $t1)
        end
        local.get $l7
        local.get $p0
        i32.load offset=4720
        local.tee $l9
        i32.const 2
        i32.shl
        i32.add
        i32.const 0
        local.get $p6
        local.get $l9
        i32.sub
        i32.const 2
        i32.shl
        call $f484
        drop
        local.get $p0
        local.get $p6
        i32.store offset=4720
        local.get $p0
        local.get $l7
        i32.store offset=4716
      end
      local.get $l7
      local.get $l14
      i64.const 14
      i64.shr_u
      i32.wrap_i64
      i32.const 134217727
      i32.and
      i32.const 2
      i32.shl
      i32.add
      local.tee $l7
      local.get $l7
      i32.load
      i32.const 1
      local.get $l10
      i32.shl
      i32.or
      i32.store
    end
    local.get $l8
    i64.load offset=144
    local.tee $l14
    i64.const 2199023255040
    i64.and
    i64.const 2199023255040
    i64.ne
    if $I10
      local.get $p0
      i32.load offset=1012
      local.set $l7
      local.get $l12
      local.get $l14
      i64.store offset=8
      local.get $l7
      local.get $l8
      i32.const -64
      i32.sub
      local.get $l12
      i32.const 8
      i32.add
      local.get $l7
      i32.load
      i32.load offset=24
      call_indirect $__indirect_function_table (type $t2)
    end
    block $B11
      block $B12
        local.get $p1
        i32.load offset=176
        i32.eqz
        br_if $B12
        local.get $p1
        i32.const 1
        call $f71621
        i32.eqz
        br_if $B12
        local.get $p1
        i32.load offset=176
        i32.eqz
        br_if $B12
        local.get $p1
        i32.const 1
        call $f71621
        drop
        local.get $p1
        i32.load offset=176
        i32.load8_u offset=31
        i32.const 1
        i32.ne
        br_if $B12
        local.get $p0
        local.get $p0
        i32.load offset=2672
        i32.const 1
        i32.add
        i32.store offset=2672
        br $B11
      end
      local.get $p0
      local.get $p0
      i32.load offset=2668
      i32.const 1
      i32.add
      i32.store offset=2668
    end
    local.get $p0
    local.get $p2
    local.get $p3
    local.get $p4
    local.get $l8
    local.get $p5
    call $f71428
    local.get $l12
    i32.const 16
    i32.add
    global.set $g0)