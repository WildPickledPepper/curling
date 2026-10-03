  (func $f71529 (type $t7) (param $p0 i32)
    (local $l1 i32) (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32)
    local.get $p0
    i32.load offset=20
    drop
    local.get $p0
    i32.load offset=28
    local.tee $l3
    i32.const 2460
    i32.add
    i32.load
    local.tee $l1
    if $I0
      i32.const 0
      local.set $p0
      loop $L1
        local.get $l3
        i32.load offset=2456
        local.get $p0
        i32.const 3
        i32.shl
        i32.add
        i32.load offset=4
        local.tee $l2
        i32.load8_u offset=46
        i32.const 4
        i32.and
        i32.eqz
        if $I2
          local.get $l3
          i32.load offset=1000
          local.get $l2
          i32.load offset=60
          call $f70718
        end
        local.get $p0
        i32.const 1
        i32.add
        local.tee $p0
        local.get $l1
        i32.ne
        br_if $L1
      end
    end
    local.get $l3
    i32.load offset=1000
    local.set $p0
    i32.const 0
    local.set $l2
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l6
    global.set $g0
    local.get $p0
    i32.const 168
    i32.add
    local.tee $l4
    call $f70666
    local.get $l4
    call $f70667
    local.get $p0
    i32.load offset=508
    local.tee $l7
    if $I3
      loop $L4
        local.get $p0
        i32.load offset=208
        local.get $p0
        i32.load offset=504
        local.get $l2
        i32.const 2
        i32.shl
        i32.add
        i32.load
        local.tee $l1
        local.get $p0
        i32.load offset=228
        local.tee $l5
        i32.div_u
        local.tee $l8
        i32.const 2
        i32.shl
        i32.add
        i32.load
        local.get $l1
        local.get $l5
        local.get $l8
        i32.mul
        i32.sub
        i32.const 4
        i32.shl
        i32.add
        i32.load16_u offset=4
        i32.const 11
        i32.and
        i32.const 3
        i32.eq
        if $I5
          local.get $l4
          local.get $l1
          call $f70661
          local.get $l4
          local.get $l1
          call $f70660
          local.get $p0
          i32.load offset=508
          local.set $l7
        end
        local.get $l2
        i32.const 1
        i32.add
        local.tee $l2
        local.get $l7
        i32.lt_u
        br_if $L4
      end
    end
    i32.const 0
    local.set $l2
    local.get $l4
    local.get $p0
    i32.const 32
    i32.add
    i32.const 0
    i32.const 0
    local.get $p0
    i32.load offset=1224
    call $f70671
    local.get $p0
    i32.load offset=36
    if $I6
      loop $L7
        local.get $l6
        local.get $p0
        i32.load offset=32
        local.get $l2
        i32.const 3
        i32.shl
        i32.add
        i64.load
        i64.const 9
        i64.shr_u
        i32.wrap_i64
        local.tee $l1
        i32.store offset=12
        block $B8
          local.get $l1
          local.get $p0
          i32.load offset=12
          i32.eq
          if $I9
            local.get $p0
            local.get $l1
            i32.const 1
            i32.sub
            i32.store offset=12
            br $B8
          end
          local.get $p0
          i32.load offset=4
          local.tee $l5
          local.get $p0
          i32.load offset=8
          i32.const 2147483647
          i32.and
          i32.ge_u
          if $I10
            local.get $p0
            local.get $l6
            i32.const 12
            i32.add
            call $f72545
            br $B8
          end
          local.get $p0
          i32.load
          local.get $l5
          i32.const 2
          i32.shl
          i32.add
          local.get $l1
          i32.store
          local.get $p0
          local.get $p0
          i32.load offset=4
          i32.const 1
          i32.add
          i32.store offset=4
        end
        local.get $l2
        i32.const 1
        i32.add
        local.tee $l2
        local.get $p0
        i32.load offset=36
        i32.lt_u
        br_if $L7
      end
    end
    local.get $p0
    i32.const 0
    i32.store offset=36
    local.get $l6
    i32.const 16
    i32.add
    global.set $g0
    local.get $l3
    i32.load offset=1000
    local.tee $l3
    i32.load offset=284
    local.get $l3
    i32.load offset=420
    local.tee $p0
    i32.sub
    local.tee $l5
    if $I11
      local.get $l3
      i32.load offset=280
      local.get $p0
      i32.const 3
      i32.shl
      i32.add
      local.set $l4
      i32.const 0
      local.set $p0
      loop $L12
        block $B13
          local.get $l3
          i32.load offset=184
          local.get $l4
          local.get $p0
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
          local.tee $l2
          i32.load offset=28
          local.tee $l1
          i32.eqz
          br_if $B13
          local.get $l2
          i32.load8_u offset=4
          i32.const 2
          i32.and
          i32.eqz
          br_if $B13
          local.get $l1
          i32.const -64
          i32.add
          i32.const 1
          call $f71557
        end
        local.get $p0
        i32.const 1
        i32.add
        local.tee $p0
        local.get $l5
        i32.ne
        br_if $L12
      end
    end
    local.get $l3
    i32.load offset=296
    local.get $l3
    i32.load offset=424
    local.tee $p0
    i32.sub
    local.tee $l5
    if $I14
      local.get $l3
      i32.load offset=292
      local.get $p0
      i32.const 3
      i32.shl
      i32.add
      local.set $l4
      i32.const 0
      local.set $p0
      loop $L15
        block $B16
          local.get $l3
          i32.load offset=184
          local.get $l4
          local.get $p0
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
          local.tee $l2
          i32.load offset=28
          i32.load offset=16
          local.tee $l1
          i32.eqz
          br_if $B16
          local.get $l2
          i32.load8_u offset=4
          i32.const 2
          i32.and
          i32.eqz
          br_if $B16
          local.get $l1
          i32.const 1
          call $f71661
        end
        local.get $p0
        i32.const 1
        i32.add
        local.tee $p0
        local.get $l5
        i32.ne
        br_if $L15
      end
    end)