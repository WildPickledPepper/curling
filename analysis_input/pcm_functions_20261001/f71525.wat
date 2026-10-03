  (func $f71525 (type $t7) (param $p0 i32)
    (local $l1 i32) (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32)
    local.get $p0
    i32.load offset=28
    local.set $l4
    local.get $p0
    i32.load offset=20
    drop
    global.get $g0
    i32.const 48
    i32.sub
    local.tee $l9
    global.set $g0
    local.get $l4
    i32.load offset=1000
    local.tee $p0
    i32.load offset=432
    local.tee $l6
    if $I0
      local.get $p0
      i32.load offset=428
      local.set $l7
      loop $L1
        block $B2
          local.get $p0
          i32.load offset=184
          local.get $l7
          local.get $l3
          i32.const 3
          i32.shl
          i32.add
          i64.load
          i64.const 9
          i64.shr_u
          i32.wrap_i64
          i32.const 5
          i32.shl
          i32.add
          local.tee $l1
          i32.load offset=28
          local.tee $l2
          i32.eqz
          br_if $B2
          local.get $l1
          i32.load8_u offset=4
          i32.const 2
          i32.and
          br_if $B2
          local.get $l2
          i32.const -64
          i32.add
          i32.const 0
          call $f71557
        end
        local.get $l3
        i32.const 1
        i32.add
        local.tee $l3
        local.get $l6
        i32.ne
        br_if $L1
      end
    end
    local.get $p0
    i32.load offset=444
    local.tee $l6
    if $I3
      local.get $p0
      i32.load offset=440
      local.set $l7
      i32.const 0
      local.set $l3
      loop $L4
        block $B5
          local.get $p0
          i32.load offset=184
          local.get $l7
          local.get $l3
          i32.const 3
          i32.shl
          i32.add
          i64.load
          i64.const 9
          i64.shr_u
          i32.wrap_i64
          i32.const 5
          i32.shl
          i32.add
          local.tee $l1
          i32.load offset=28
          i32.load offset=16
          local.tee $l2
          i32.eqz
          br_if $B5
          local.get $l1
          i32.load8_u offset=4
          i32.const 2
          i32.and
          br_if $B5
          local.get $l2
          i32.const 0
          call $f71661
        end
        local.get $l3
        i32.const 1
        i32.add
        local.tee $l3
        local.get $l6
        i32.ne
        br_if $L4
      end
    end
    block $B6
      local.get $l4
      i32.load offset=1000
      local.tee $l5
      i32.const 1064
      i32.add
      i32.load
      local.tee $l6
      i32.eqz
      br_if $B6
      local.get $l5
      i32.const 1060
      i32.add
      i32.load
      local.set $l7
      i32.const 0
      local.set $l3
      local.get $l5
      local.set $p0
      loop $L7
        block $B8
          local.get $p0
          i32.load offset=44
          local.get $l7
          local.get $l3
          i32.const 2
          i32.shl
          i32.add
          i32.load
          local.tee $l1
          local.get $p0
          i32.const -64
          i32.sub
          i32.load
          local.tee $p0
          i32.div_u
          local.tee $l2
          i32.const 2
          i32.shl
          i32.add
          i32.load
          local.get $l1
          local.get $p0
          local.get $l2
          i32.mul
          i32.sub
          i32.const 2
          i32.shl
          i32.add
          i32.load
          local.tee $p0
          i32.eqz
          br_if $B8
          local.get $p0
          i32.load8_u offset=21
          i32.const 32
          i32.and
          i32.eqz
          br_if $B8
          local.get $l5
          i32.load offset=680
          local.get $l1
          local.get $l5
          i32.load offset=700
          local.tee $l2
          i32.div_u
          local.tee $l8
          i32.const 2
          i32.shl
          i32.add
          i32.load
          local.get $l1
          local.get $l2
          local.get $l8
          i32.mul
          i32.sub
          i32.const 4
          i32.shl
          i32.add
          i32.load8_u offset=4
          i32.const 4
          i32.and
          br_if $B8
          local.get $p0
          call $f71420
          i32.eqz
          br_if $B8
          local.get $p0
          i32.load8_u offset=20
          local.tee $l1
          i32.const 2
          i32.gt_u
          br_if $B8
          local.get $l4
          local.get $l1
          i32.const 2
          i32.shl
          i32.add
          i32.const 88
          i32.add
          local.tee $l8
          i32.load
          local.tee $l2
          i32.const 2
          i32.ge_u
          if $I9
            local.get $l4
            local.get $l1
            i32.const 12
            i32.mul
            i32.add
            i32.const 52
            i32.add
            local.tee $l12
            i32.load
            local.tee $l10
            local.get $l2
            i32.const 1
            i32.sub
            local.tee $l2
            i32.const 2
            i32.shl
            i32.add
            local.tee $l11
            i32.load
            local.set $l1
            local.get $l11
            local.get $l10
            local.get $p0
            i32.load offset=8
            local.tee $p0
            i32.const 2
            i32.shl
            local.tee $l11
            i32.add
            i32.load
            local.tee $l10
            i32.store
            local.get $l12
            i32.load
            local.get $l11
            i32.add
            local.get $l1
            i32.store
            local.get $l1
            local.get $p0
            i32.store offset=8
            local.get $l10
            local.get $l2
            i32.store offset=8
            local.get $l8
            i32.load
            local.set $l2
          end
          local.get $l8
          local.get $l2
          i32.const 1
          i32.sub
          i32.store
        end
        local.get $l3
        i32.const 1
        i32.add
        local.tee $l3
        local.get $l6
        i32.eq
        br_if $B6
        local.get $l4
        i32.load offset=1000
        local.set $p0
        br $L7
      end
      unreachable
    end
    local.get $l9
    i32.const 8
    i32.add
    local.get $l4
    i32.load offset=976
    i32.load offset=1024
    local.tee $l3
    local.get $l3
    i32.load
    i32.load offset=84
    call_indirect $__indirect_function_table (type $t1)
    local.get $l9
    i32.const 8
    i32.add
    local.set $l3
    local.get $l4
    i32.load offset=2168
    local.tee $l4
    i32.load offset=28
    local.tee $l1
    if $I10
      local.get $l4
      i32.load offset=16
      local.set $l4
      loop $L11
        local.get $l1
        i32.const 1
        i32.sub
        local.set $l1
        block $B12
          local.get $l4
          i32.load
          local.tee $p0
          i32.load offset=44
          i32.const 1032
          i32.and
          i32.const 1032
          i32.ne
          br_if $B12
          local.get $p0
          i32.load offset=28
          call $f71419
          local.set $l2
          local.get $p0
          i32.load offset=32
          call $f71419
          local.set $l5
          local.get $l2
          i32.load offset=156
          i32.const -2
          i32.ge_u
          if $I13
            local.get $l5
            i32.eqz
            br_if $B12
            local.get $l5
            i32.load offset=156
            i32.const -3
            i32.gt_u
            br_if $B12
          end
          local.get $p0
          i32.const 8
          i32.const 0
          i32.const 0
          i32.const 0
          local.get $l3
          call $f71637
        end
        local.get $l4
        i32.const 4
        i32.add
        local.set $l4
        local.get $l1
        br_if $L11
      end
    end
    local.get $l9
    i32.const 48
    i32.add
    global.set $g0)