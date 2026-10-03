  (func $f70708 (type $t233) (param $p0 i32) (param $p1 i32) (param $p2 i64) (param $p3 i64) (param $p4 i32) (result i32)
    (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l11
    global.set $g0
    block $B0
      local.get $p0
      i32.load offset=20
      local.tee $l5
      if $I1
        local.get $p0
        i32.load offset=16
        local.get $l5
        i32.const 1
        i32.sub
        local.tee $l5
        i32.const 2
        i32.shl
        i32.add
        i32.load
        local.set $l8
        local.get $p0
        local.get $l5
        i32.store offset=20
        br $B0
      end
      local.get $p0
      i32.const 28
      i32.add
      local.tee $l5
      local.get $l5
      i32.load
      local.tee $l8
      i32.const 1
      i32.add
      i32.store
    end
    local.get $l8
    i32.const 1
    i32.shl
    local.tee $l10
    local.get $p0
    i32.load offset=116
    i32.eq
    if $I2
      local.get $p0
      i32.const 104
      i32.add
      local.get $l10
      i32.const 2048
      i32.add
      local.tee $l6
      call $f70709
      local.get $l6
      local.get $p0
      i32.load offset=116
      local.tee $l5
      i32.gt_u
      if $I3
        loop $L4
          local.get $p0
          i32.load offset=104
          local.get $l5
          local.get $p0
          i32.load offset=124
          local.tee $l7
          i32.div_u
          local.tee $l9
          i32.const 2
          i32.shl
          i32.add
          i32.load
          local.get $l5
          local.get $l7
          local.get $l9
          i32.mul
          i32.sub
          i32.const 3
          i32.shl
          i32.add
          i64.const 2199023255040
          i64.store
          local.get $l5
          i32.const 1
          i32.add
          local.tee $l5
          local.get $l6
          i32.ne
          br_if $L4
        end
      end
      local.get $p0
      local.get $l6
      i32.store offset=116
      local.get $p0
      i32.const 128
      i32.add
      local.get $l6
      call $f70710
      local.get $l6
      local.get $p0
      i32.load offset=140
      local.tee $l5
      i32.gt_u
      if $I5
        loop $L6
          local.get $p0
          i32.load offset=128
          local.get $l5
          local.get $p0
          i32.load offset=148
          local.tee $l7
          i32.div_u
          local.tee $l9
          i32.const 2
          i32.shl
          i32.add
          i32.load
          local.get $l5
          local.get $l7
          local.get $l9
          i32.mul
          i32.sub
          i32.const 2
          i32.shl
          i32.add
          i32.const 0
          i32.store
          local.get $l5
          i32.const 1
          i32.add
          local.tee $l5
          local.get $l6
          i32.ne
          br_if $L6
        end
      end
      local.get $p0
      local.get $l6
      i32.store offset=140
      local.get $p0
      i32.const 44
      i32.add
      local.get $l6
      call $f70711
      local.get $l6
      local.get $p0
      i32.load offset=56
      local.tee $l5
      i32.gt_u
      if $I7
        loop $L8
          local.get $p0
          i32.load offset=44
          local.get $l5
          local.get $p0
          i32.load offset=64
          local.tee $l7
          i32.div_u
          local.tee $l9
          i32.const 2
          i32.shl
          i32.add
          i32.load
          local.get $l5
          local.get $l7
          local.get $l9
          i32.mul
          i32.sub
          i32.const 2
          i32.shl
          i32.add
          i32.const 0
          i32.store
          local.get $l5
          i32.const 1
          i32.add
          local.tee $l5
          local.get $l6
          i32.ne
          br_if $L8
        end
      end
      local.get $p0
      local.get $l6
      i32.store offset=56
    end
    local.get $p0
    i32.load offset=104
    local.get $l10
    local.get $p0
    i32.const 124
    i32.add
    local.tee $l5
    i32.load
    local.tee $l6
    i32.div_u
    local.tee $l7
    i32.const 2
    i32.shl
    i32.add
    i32.load
    local.get $l10
    local.get $l6
    local.get $l7
    i32.mul
    i32.sub
    i32.const 3
    i32.shl
    i32.add
    local.get $p2
    i64.store
    local.get $p0
    i32.load offset=104
    local.get $l10
    i32.const 1
    i32.or
    local.tee $l6
    local.get $l5
    i32.load
    local.tee $l5
    i32.div_u
    local.tee $l7
    i32.const 2
    i32.shl
    i32.add
    i32.load
    local.get $l6
    local.get $l5
    local.get $l7
    i32.mul
    i32.sub
    i32.const 3
    i32.shl
    i32.add
    local.get $p3
    i64.store
    local.get $p0
    i32.load offset=128
    local.get $l8
    local.get $p0
    i32.load offset=148
    local.tee $l5
    i32.div_u
    local.tee $l6
    i32.const 2
    i32.shl
    i32.add
    i32.load
    local.get $l8
    local.get $l5
    local.get $l6
    i32.mul
    i32.sub
    i32.const 2
    i32.shl
    i32.add
    local.get $p1
    i32.store
    local.get $p0
    i32.load offset=44
    local.get $l8
    local.get $p0
    i32.const -64
    i32.sub
    i32.load
    local.tee $l5
    i32.div_u
    local.tee $l6
    i32.const 2
    i32.shl
    i32.add
    i32.load
    local.get $l8
    local.get $l5
    local.get $l6
    i32.mul
    i32.sub
    i32.const 2
    i32.shl
    i32.add
    local.get $p4
    i32.store
    local.get $p0
    i32.const 640
    i32.add
    local.get $p2
    local.get $p3
    i32.const 0
    local.get $l8
    call $f70657
    local.get $p1
    if $I9
      local.get $p1
      i32.const -64
      i32.sub
      local.get $l8
      i32.store
    end
    block $B10
      local.get $p0
      i32.load offset=156
      local.tee $l5
      i32.const 5
      i32.shl
      local.get $l8
      i32.ne
      br_if $B10
      local.get $l10
      i32.const 33
      i32.add
      i32.const 5
      i32.shr_u
      local.tee $l6
      local.get $l5
      i32.const 2147483647
      i32.and
      i32.le_u
      br_if $B10
      call $f69753
      local.tee $l5
      local.get $l6
      i32.const 2
      i32.shl
      i32.const 3133968
      i32.const 3135509
      i32.const 438
      local.get $l5
      i32.load
      i32.load offset=8
      call_indirect $__indirect_function_table (type $t9)
      local.set $l5
      block $B11
        local.get $p0
        i32.load offset=152
        local.tee $l7
        i32.eqz
        br_if $B11
        local.get $l5
        local.get $l7
        local.get $p0
        i32.load offset=156
        i32.const 2
        i32.shl
        call $f483
        drop
        local.get $p0
        i32.load offset=156
        i32.const 0
        i32.lt_s
        br_if $B11
        local.get $p0
        i32.load offset=152
        local.tee $l7
        i32.eqz
        br_if $B11
        call $f69753
        local.tee $l9
        local.get $l7
        local.get $l9
        i32.load
        i32.load offset=12
        call_indirect $__indirect_function_table (type $t1)
      end
      local.get $l5
      local.get $p0
      i32.load offset=156
      local.tee $l7
      i32.const 2
      i32.shl
      i32.add
      i32.const 0
      local.get $l6
      local.get $l7
      i32.sub
      i32.const 2
      i32.shl
      call $f484
      drop
      local.get $p0
      local.get $l6
      i32.store offset=156
      local.get $p0
      local.get $l5
      i32.store offset=152
    end
    local.get $l8
    local.get $p0
    i32.load offset=88
    i32.const 2147483647
    i32.and
    i32.eq
    if $I12
      local.get $l11
      i32.const 0
      i32.store offset=12
      local.get $p0
      i32.const 80
      i32.add
      local.get $l10
      i32.const 2
      i32.add
      local.get $l11
      i32.const 12
      i32.add
      call $f70705
    end
    local.get $p0
    i32.load offset=152
    local.get $l8
    i32.const 3
    i32.shr_u
    i32.const 536870908
    i32.and
    i32.add
    local.tee $p0
    local.get $p0
    i32.load
    i32.const -2
    local.get $l8
    i32.rotl
    i32.and
    i32.store
    local.get $l11
    i32.const 16
    i32.add
    global.set $g0
    local.get $l8)