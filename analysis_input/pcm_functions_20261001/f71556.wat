  (func $f71556 (type $t7) (param $p0 i32)
    (local $l1 i32) (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i64)
    local.get $p0
    i32.load offset=28
    local.tee $l4
    if $I0
      loop $L1
        local.get $l2
        local.tee $l1
        i32.const 1
        i32.add
        local.set $l2
        block $B2
          local.get $p0
          i32.load offset=20
          local.get $l1
          i32.const 2
          i32.shl
          i32.add
          i32.load
          local.tee $l1
          i32.load8_u offset=20
          local.tee $l3
          i32.eqz
          br_if $B2
          local.get $l1
          i32.load8_u offset=21
          i32.const 32
          i32.and
          i32.eqz
          br_if $B2
          local.get $l3
          i32.const 2
          i32.eq
          br_if $B2
          local.get $l1
          call $f71420
          i32.eqz
          br_if $B2
          local.get $l1
          i32.load8_u offset=20
          i32.const 2
          i32.gt_u
          br_if $B2
          local.get $p0
          i32.load offset=40
          local.get $l1
          call $f71387
        end
        local.get $l2
        local.get $l4
        i32.ne
        br_if $L1
      end
    end
    local.get $p0
    i32.load offset=44
    local.set $l2
    block $B3
      local.get $p0
      i32.load8_u offset=152
      i32.const 8
      i32.and
      br_if $B3
      local.get $l2
      i32.const 0
      i32.store offset=104
      local.get $l2
      i64.const 0
      i64.store offset=96 align=4
      local.get $l2
      i32.const 0
      i32.store offset=88
      local.get $l2
      i64.const 0
      i64.store offset=80 align=4
      local.get $p0
      i32.load offset=44
      local.tee $l3
      i32.load offset=176
      local.set $l1
      local.get $p0
      i32.load offset=100
      i32.load8_u offset=28
      i32.const 128
      i32.and
      i32.eqz
      if $I4
        local.get $l2
        i32.load8_u offset=173
        local.set $l4
        block $B5
          local.get $l1
          i32.eqz
          br_if $B5
          local.get $l3
          i32.const 0
          call $f71621
          i32.eqz
          br_if $B5
          local.get $l3
          i32.load offset=176
          local.tee $l1
          i32.eqz
          br_if $B5
          local.get $l1
          i32.const 0
          i32.store offset=56
          local.get $l1
          i64.const 0
          i64.store offset=48 align=4
          local.get $l1
          i32.const 0
          i32.store offset=40
          local.get $l1
          i64.const 0
          i64.store offset=32 align=4
          local.get $l1
          i32.const 0
          i32.store offset=24
          local.get $l1
          i64.const 0
          i64.store offset=16 align=4
          local.get $l1
          i32.const 0
          i32.store offset=8
          local.get $l1
          i64.const 0
          i64.store align=4
        end
        local.get $l4
        i32.const 255
        i32.and
        i32.eqz
        if $I6
          local.get $p0
          i32.const 1
          i32.store8 offset=154
          br $B3
        end
        local.get $p0
        i32.const 0
        i32.store8 offset=154
        br $B3
      end
      block $B7
        local.get $l1
        i32.eqz
        br_if $B7
        local.get $l3
        i32.const 0
        call $f71621
        i32.eqz
        br_if $B7
        local.get $l3
        i32.load offset=176
        local.tee $l1
        i32.eqz
        br_if $B7
        local.get $l1
        i32.const 0
        i32.store offset=56
        local.get $l1
        i64.const 0
        i64.store offset=48 align=4
        local.get $l1
        i32.const 0
        i32.store offset=40
        local.get $l1
        i64.const 0
        i64.store offset=32 align=4
      end
      local.get $p0
      local.get $p0
      i32.load8_u offset=154
      i32.const 251
      i32.and
      i32.store8 offset=154
    end
    local.get $p0
    i32.load offset=44
    i32.load8_u offset=9
    i32.const 2
    i32.ne
    if $I8
      local.get $p0
      i32.load offset=40
      local.set $l1
      global.get $g0
      i32.const 16
      i32.sub
      local.tee $l4
      global.set $g0
      local.get $p0
      i32.load16_u offset=152
      local.set $l3
      local.get $l1
      i32.load offset=2344
      if $I9
        local.get $p0
        local.get $l3
        i32.const 128
        i32.and
        if $I10 (result i32)
          local.get $p0
          local.get $l3
          i32.const 65407
          i32.and
          i32.store16 offset=152
          local.get $l1
          i32.const 0
          i32.store8 offset=2280
          local.get $p0
          i32.load16_u offset=152
        else
          local.get $l3
        end
        i32.const 64
        i32.or
        local.tee $l3
        i32.store16 offset=152
      end
      local.get $l3
      i32.const 16
      i32.and
      i32.eqz
      if $I11
        local.get $l4
        local.get $p0
        i32.load offset=44
        i32.store offset=8
        local.get $l1
        i32.const 2200
        i32.add
        local.get $l4
        i32.const 8
        i32.add
        local.get $l4
        i32.const 15
        i32.add
        call $f71404
        local.set $l3
        local.get $l4
        i32.load8_u offset=15
        i32.eqz
        if $I12
          local.get $l3
          local.get $l4
          i32.load offset=8
          i32.store
        end
        local.get $p0
        local.get $p0
        i32.load16_u offset=152
        i32.const 16
        i32.or
        i32.store16 offset=152
      end
      local.get $l4
      i32.const 16
      i32.add
      global.set $g0
    end
    local.get $l2
    i32.load8_u offset=44
    i32.const 16
    i32.and
    if $I13
      local.get $p0
      i32.load offset=40
      local.get $p0
      call $f71569
    end
    local.get $p0
    i32.load offset=32
    local.tee $l2
    if $I14
      loop $L15
        local.get $l2
        call $f71456
        local.get $l2
        i32.load
        local.tee $l2
        br_if $L15
      end
    end
    block $B16
      local.get $p0
      i32.load offset=44
      local.tee $l2
      i32.load8_u offset=44
      i32.const 32
      i32.and
      i32.eqz
      br_if $B16
      block $B17 (result i32)
        local.get $l2
        i32.load8_u offset=9
        i32.const 2
        i32.eq
        if $I18
          local.get $p0
          i64.load offset=144
          local.tee $l5
          i64.const 9
          i64.shr_u
          i32.wrap_i64
          local.tee $l2
          i32.const -1
          i32.eq
          br_if $B16
          local.get $p0
          i32.load offset=40
          local.tee $l1
          i32.const 4732
          i32.add
          i32.load
          i32.const 5
          i32.shl
          local.get $l2
          i32.le_u
          br_if $B16
          local.get $l1
          i32.const 4728
          i32.add
          br $B17
        end
        local.get $p0
        i64.load offset=144
        local.tee $l5
        i64.const 9
        i64.shr_u
        i32.wrap_i64
        local.tee $l2
        local.get $p0
        i32.load offset=40
        local.tee $l1
        i32.const 4720
        i32.add
        i32.load
        i32.const 5
        i32.shl
        i32.ge_u
        br_if $B16
        local.get $l1
        i32.const 4716
        i32.add
      end
      i32.load
      local.get $l5
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
      i32.const -2
      local.get $l2
      i32.rotl
      i32.and
      i32.store
    end)