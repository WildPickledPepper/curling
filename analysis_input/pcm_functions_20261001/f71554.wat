  (func $f71554 (type $t8) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (result i32)
    (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i64) (local $l13 f32)
    local.get $p0
    local.get $p1
    local.get $p2
    call $f71726
    drop
    local.get $p0
    i32.const 3170644
    i32.store
    local.get $p0
    local.get $p2
    f32.load offset=16
    f32.store offset=64
    local.get $p0
    local.get $p2
    f32.load offset=20
    f32.store offset=68
    local.get $p0
    local.get $p2
    f32.load offset=24
    f32.store offset=72
    local.get $p0
    local.get $p2
    f32.load offset=28
    f32.store offset=76
    local.get $p0
    local.get $p2
    f32.load offset=32
    f32.store offset=80
    local.get $p0
    local.get $p2
    f32.load offset=36
    f32.store offset=84
    local.get $p2
    f32.load offset=40
    local.set $l13
    local.get $p0
    i32.const 0
    i32.store16 offset=92
    local.get $p0
    local.get $l13
    f32.store offset=88
    local.get $p2
    i32.load16_u offset=46
    local.set $l5
    local.get $p0
    i64.const 0
    i64.store offset=164 align=4
    local.get $p0
    i64.const -1
    i64.store offset=156 align=4
    local.get $p0
    i32.const 1
    i32.store8 offset=154
    local.get $p0
    i32.const 0
    i32.store16 offset=152
    local.get $p0
    i64.const 2199023255040
    i64.store offset=144
    local.get $p0
    i64.const 4575657221408423936
    i64.store offset=136 align=4
    local.get $p0
    i64.const 0
    i64.store offset=128 align=4
    local.get $p0
    i64.const 4593671619917905920
    i64.store offset=120 align=4
    local.get $p0
    i64.const 0
    i64.store offset=112 align=4
    local.get $p0
    local.get $p2
    i32.const 16
    i32.add
    i32.store offset=100
    local.get $p0
    i32.const 0
    i32.store offset=96
    local.get $p0
    local.get $l5
    i32.store16 offset=94
    local.get $p2
    i64.const 0
    i64.store offset=164 align=4
    local.get $p2
    local.get $p2
    i32.load8_u offset=8
    i32.const 2
    i32.and
    i32.store8 offset=173
    local.get $p2
    i32.load8_u offset=44
    i32.const 32
    i32.and
    if $I0
      local.get $p0
      local.get $p0
      i32.load16_u offset=92
      i32.const 64
      i32.or
      i32.store16 offset=92
    end
    block $B1
      local.get $p2
      i32.load offset=176
      i32.eqz
      br_if $B1
      local.get $p2
      i32.const 0
      call $f71621
      i32.eqz
      br_if $B1
      local.get $p2
      i32.load offset=176
      local.tee $l5
      i32.eqz
      br_if $B1
      block $B2
        local.get $l5
        i32.load8_u offset=12
        local.tee $l9
        i32.eqz
        br_if $B2
        i32.const 1
        local.set $l7
        local.get $l5
        f32.load
        f32.const 0x0p+0 (;=0;)
        f32.ne
        br_if $B2
        local.get $l5
        f32.load offset=4
        f32.const 0x0p+0 (;=0;)
        f32.ne
        br_if $B2
        local.get $l5
        f32.load offset=8
        f32.const 0x0p+0 (;=0;)
        f32.ne
        br_if $B2
        local.get $l5
        f32.load offset=16
        f32.const 0x0p+0 (;=0;)
        f32.ne
        br_if $B2
        local.get $l5
        f32.load offset=20
        f32.const 0x0p+0 (;=0;)
        f32.ne
        br_if $B2
        local.get $l5
        f32.load offset=24
        f32.const 0x0p+0 (;=0;)
        f32.ne
        br_if $B2
        local.get $l5
        f32.load offset=32
        f32.const 0x0p+0 (;=0;)
        f32.ne
        br_if $B2
        local.get $l5
        f32.load offset=36
        f32.const 0x0p+0 (;=0;)
        f32.ne
        br_if $B2
        local.get $l5
        f32.load offset=40
        f32.const 0x0p+0 (;=0;)
        f32.ne
        br_if $B2
        local.get $l5
        f32.load offset=48
        f32.const 0x0p+0 (;=0;)
        f32.ne
        br_if $B2
        local.get $l5
        f32.load offset=52
        f32.const 0x0p+0 (;=0;)
        f32.ne
        br_if $B2
        local.get $l5
        f32.load offset=56
        f32.const 0x0p+0 (;=0;)
        f32.ne
        local.set $l7
      end
      local.get $p0
      local.get $l9
      i32.store8 offset=154
      local.get $l5
      i32.const 0
      i32.store8 offset=12
    end
    block $B3 (result i32)
      i32.const 1
      local.get $p2
      f32.load offset=156
      f32.const 0x0p+0 (;=0;)
      f32.gt
      br_if $B3
      drop
      i32.const 1
      local.get $p2
      f32.load offset=80
      f32.const 0x0p+0 (;=0;)
      f32.ne
      br_if $B3
      drop
      i32.const 1
      local.get $p2
      f32.load offset=84
      f32.const 0x0p+0 (;=0;)
      f32.ne
      br_if $B3
      drop
      i32.const 1
      local.get $p2
      f32.load offset=88
      f32.const 0x0p+0 (;=0;)
      f32.ne
      br_if $B3
      drop
      i32.const 1
      local.get $p2
      f32.load offset=96
      f32.const 0x0p+0 (;=0;)
      f32.ne
      br_if $B3
      drop
      i32.const 1
      local.get $p2
      f32.load offset=100
      f32.const 0x0p+0 (;=0;)
      f32.ne
      br_if $B3
      drop
      i32.const 1
      local.get $p2
      f32.load offset=104
      f32.const 0x0p+0 (;=0;)
      f32.ne
      br_if $B3
      drop
      local.get $l7
    end
    local.set $l5
    local.get $p0
    i32.load offset=44
    local.tee $l4
    i32.load16_u offset=44
    i32.const 1
    i32.and
    local.set $l9
    local.get $p1
    i32.load offset=1000
    local.set $l11
    block $B4
      local.get $l4
      i32.load8_u offset=9
      i32.const 2
      i32.ne
      if $I5
        local.get $p0
        i32.const -64
        i32.sub
        local.set $l8
        block $B6
          local.get $l11
          local.tee $l4
          i32.load offset=4
          local.tee $l6
          if $I7
            local.get $l4
            i32.load
            local.get $l6
            i32.const 1
            i32.sub
            local.tee $l10
            i32.const 2
            i32.shl
            i32.add
            i32.load
            local.set $l6
            local.get $l4
            local.get $l10
            i32.store offset=4
            br $B6
          end
          local.get $l4
          local.get $l4
          i32.load offset=12
          local.tee $l6
          i32.const 1
          i32.add
          i32.store offset=12
        end
        local.get $l4
        i32.const 168
        i32.add
        local.get $l5
        local.get $l9
        i32.const 0
        local.get $l6
        i64.extend_i32_u
        i64.const 9
        i64.shl
        local.tee $l12
        call $f70650
        local.get $l6
        i32.const 5
        i32.shl
        local.tee $l6
        local.get $l4
        i32.load offset=184
        i32.add
        local.get $l8
        i32.store offset=28
        local.get $l4
        i32.const 640
        i32.add
        local.get $l5
        local.get $l9
        i32.const 0
        local.get $l12
        call $f70650
        local.get $l4
        i32.load offset=656
        local.get $l6
        i32.add
        local.get $l8
        i32.store offset=28
        local.get $p0
        local.get $l12
        i64.store offset=144
        br $B4
      end
      local.get $p0
      i32.load offset=164
      local.tee $l4
      i32.eqz
      br_if $B4
      local.get $p0
      block $B8 (result i32)
        local.get $l4
        i32.load
        local.tee $l8
        i32.const -2147483648
        i32.or
        local.get $l4
        i32.load offset=28
        local.tee $l10
        i32.eqz
        br_if $B8
        drop
        local.get $l4
        i32.load offset=24
        local.set $l6
        i32.const 0
        local.set $l4
        loop $L9
          local.get $l4
          local.get $l8
          i32.or
          local.get $p0
          local.get $l6
          local.get $l4
          i32.const 2
          i32.shl
          i32.add
          i32.load
          i32.eq
          br_if $B8
          drop
          local.get $l4
          i32.const 1
          i32.add
          local.tee $l4
          local.get $l10
          i32.ne
          br_if $L9
        end
        local.get $l8
        i32.const -2147483648
        i32.or
      end
      i32.const 1
      i32.shl
      i32.const 510
      i32.and
      i32.const 1
      i32.or
      i64.extend_i32_u
      local.get $p0
      i32.load offset=164
      i64.load offset=48
      i64.const 2199023255040
      i64.and
      i64.or
      i64.store offset=144
    end
    block $B10
      local.get $l7
      i32.eqz
      br_if $B10
      local.get $p0
      i32.load offset=44
      i32.load8_u offset=9
      i32.const 2
      i32.eq
      br_if $B10
      block $B11
        local.get $p0
        i64.load offset=144
        local.tee $l12
        i64.const 9
        i64.shr_u
        i32.wrap_i64
        local.tee $l8
        i32.const 32
        i32.add
        i32.const 5
        i32.shr_u
        local.tee $l4
        local.get $p1
        i32.const 2448
        i32.add
        i32.load
        i32.const 2147483647
        i32.and
        i32.le_u
        if $I12
          local.get $p1
          i32.load offset=2444
          local.set $l7
          br $B11
        end
        call $f69753
        local.tee $l7
        local.get $l4
        i32.const 2
        i32.shl
        i32.const 3171167
        i32.const 3171183
        i32.const 438
        local.get $l7
        i32.load
        i32.load offset=8
        call_indirect $__indirect_function_table (type $t9)
        local.set $l7
        block $B13
          local.get $p1
          i32.load offset=2444
          local.tee $l6
          i32.eqz
          br_if $B13
          local.get $l7
          local.get $l6
          local.get $p1
          i32.load offset=2448
          i32.const 2
          i32.shl
          call $f483
          drop
          local.get $p1
          i32.load offset=2448
          i32.const 0
          i32.lt_s
          br_if $B13
          local.get $p1
          i32.load offset=2444
          local.tee $l6
          i32.eqz
          br_if $B13
          call $f69753
          local.tee $l10
          local.get $l6
          local.get $l10
          i32.load
          i32.load offset=12
          call_indirect $__indirect_function_table (type $t1)
        end
        local.get $l7
        local.get $p1
        i32.load offset=2448
        local.tee $l6
        i32.const 2
        i32.shl
        i32.add
        i32.const 0
        local.get $l4
        local.get $l6
        i32.sub
        i32.const 2
        i32.shl
        call $f484
        drop
        local.get $p1
        local.get $l4
        i32.store offset=2448
        local.get $p1
        local.get $l7
        i32.store offset=2444
      end
      local.get $l7
      local.get $l12
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
      local.get $l8
      i32.shl
      i32.or
      i32.store
    end
    local.get $p3
    if $I14
      local.get $p0
      local.get $p0
      i32.load16_u offset=152
      i32.const 4096
      i32.or
      i32.store16 offset=152
    end
    block $B15
      local.get $l5
      if $I16
        local.get $p0
        call $f71555
        local.get $p1
        local.get $p0
        call $f71379
        br $B15
      end
      local.get $p0
      call $f71556
      local.get $p0
      i64.const -4294967298
      i64.store offset=156 align=4
      local.get $l11
      local.get $p0
      i64.load offset=144
      call $f70713
    end
    local.get $l9
    if $I17
      local.get $p0
      i32.load offset=168
      local.tee $l5
      if $I18
        local.get $l5
        local.get $p0
        i32.load offset=40
        i32.load offset=1136
        call $f71364
      end
      block $B19
        block $B20
          local.get $p2
          i32.load offset=176
          i32.eqz
          br_if $B20
          local.get $p2
          i32.const 1
          call $f71621
          i32.eqz
          br_if $B20
          local.get $p2
          i32.load offset=176
          br_if $B19
        end
        local.get $p2
        local.get $p1
        i32.load offset=2412
        call $f71602
        local.get $p0
        i32.load offset=40
        i32.load offset=1000
        local.get $p0
        i64.load offset=144
        call $f70714
        local.get $p0
        return
      end
      local.get $p0
      local.get $p0
      i32.load16_u offset=152
      i32.const 63483
      i32.and
      i32.const 4
      i32.or
      i32.store16 offset=152
    end
    local.get $p0)