  (func $f72132 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32)
    global.get $g0
    i32.const 32
    i32.sub
    local.tee $l9
    local.set $l6
    local.get $l9
    global.set $g0
    local.get $p1
    local.get $p1
    i32.load
    i32.load offset=76
    call_indirect $__indirect_function_table (type $t5)
    local.set $l3
    local.get $p1
    local.get $p1
    i32.load
    i32.load offset=100
    call_indirect $__indirect_function_table (type $t5)
    local.tee $l2
    i32.load offset=88
    if $I0 (result i32)
      local.get $l2
      i32.load offset=84
      i32.load
    else
      i32.const 0
    end
    local.tee $l4
    call $f72133
    i32.const 1
    local.set $l10
    block $B1
      local.get $l4
      f32.load offset=284
      f32.const 0x0p+0 (;=0;)
      f32.ne
      br_if $B1
      local.get $l4
      f32.load offset=288
      f32.const 0x0p+0 (;=0;)
      f32.ne
      br_if $B1
      local.get $l4
      f32.load offset=292
      f32.const 0x0p+0 (;=0;)
      f32.ne
      br_if $B1
      local.get $l4
      f32.load offset=296
      f32.const 0x0p+0 (;=0;)
      f32.ne
      br_if $B1
      local.get $l4
      f32.load offset=300
      f32.const 0x0p+0 (;=0;)
      f32.ne
      br_if $B1
      local.get $l4
      f32.load offset=304
      f32.const 0x0p+0 (;=0;)
      f32.ne
      local.set $l10
    end
    local.get $p0
    local.get $l4
    call $f72134
    local.get $p1
    local.get $p1
    i32.load
    i32.load offset=100
    call_indirect $__indirect_function_table (type $t5)
    local.tee $l13
    local.set $l5
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l7
    global.set $g0
    local.get $l5
    local.get $p0
    i32.const 16
    i32.add
    local.tee $l8
    local.tee $l2
    i32.store
    block $B2
      local.get $l2
      i32.load8_u offset=4785
      i32.eqz
      if $I3
        local.get $l5
        local.get $l5
        i32.load offset=4
        i32.const 268435455
        i32.and
        i32.const -2147483648
        i32.or
        i32.store offset=4
        local.get $l2
        i32.const 16
        i32.add
        local.get $l5
        i32.const 12
        i32.add
        local.get $l5
        call $f72042
        i32.const 16
        i32.add
        call $f71406
        br $B2
      end
      local.get $l2
      i32.const 5012
      i32.add
      local.set $l11
      local.get $l5
      i32.load offset=4
      local.tee $l2
      i32.const 1073741823
      i32.and
      local.set $l14
      local.get $l2
      i32.const -1073741824
      i32.ge_u
      if $I4
        local.get $l5
        local.get $l14
        i32.const -2147483648
        i32.or
        i32.store offset=4
        local.get $l2
        i32.const 268435456
        i32.and
        br_if $B2
        local.get $l11
        local.get $l5
        call $f71988
        br $B2
      end
      local.get $l5
      local.get $l14
      i32.const 1073741824
      i32.or
      i32.store offset=4
      local.get $l7
      local.get $l5
      i32.store offset=8
      local.get $l11
      local.get $l7
      i32.const 8
      i32.add
      local.get $l7
      i32.const 15
      i32.add
      call $f71989
      local.set $l2
      local.get $l7
      i32.load8_u offset=15
      br_if $B2
      local.get $l2
      local.get $l7
      i32.load offset=8
      i32.store
    end
    local.get $l5
    local.get $l5
    f32.load offset=56
    f32.const 0x0p+0 (;=0;)
    f32.eq
    i32.store8 offset=60
    local.get $l7
    i32.const 16
    i32.add
    global.set $g0
    local.get $l13
    i32.load offset=12
    local.tee $l5
    if $I5
      local.get $l4
      local.get $l5
      local.get $l4
      i32.const -64
      i32.sub
      i32.load
      call $f71656
      i32.store offset=364
    end
    local.get $l4
    i32.const 0
    i32.store offset=368
    local.get $l4
    local.get $l4
    i32.load
    i32.load offset=272
    call_indirect $__indirect_function_table (type $t5)
    local.tee $l2
    if $I6
      local.get $l8
      local.get $l2
      local.get $l2
      i32.load
      i32.load offset=48
      call_indirect $__indirect_function_table (type $t5)
      call $f72007
    end
    local.get $l4
    i32.load offset=16
    if $I7
      local.get $l4
      i32.const 12
      i32.add
      call $f71928
    end
    local.get $l6
    local.get $l3
    i32.const 2
    i32.shl
    local.tee $l2
    i32.const 1024
    i32.gt_u
    i32.store8 offset=20
    block $B8
      local.get $l2
      i32.const 1025
      i32.ge_u
      if $I9
        local.get $l2
        i32.const 3184128
        i32.const 888
        call $f70043
        local.set $l2
        br $B8
      end
      local.get $l9
      local.get $l2
      i32.const 15
      i32.add
      i32.const -16
      i32.and
      i32.sub
      local.tee $l2
      global.set $g0
    end
    local.get $l6
    local.get $l2
    i32.store offset=16
    local.get $l2
    local.get $l4
    i32.store
    local.get $l3
    i32.const 1
    i32.sub
    local.tee $l11
    if $I10
      i32.const 1
      local.set $l9
      loop $L11
        i32.const 0
        local.set $l2
        i32.const 0
        local.set $l7
        local.get $l6
        i32.load offset=16
        local.get $l12
        i32.const 2
        i32.shl
        i32.add
        i32.load
        local.tee $l8
        i32.load offset=356
        if $I12
          local.get $l8
          i32.load offset=352
          local.set $l7
        end
        local.get $l8
        local.get $l8
        i32.load
        i32.load offset=280
        call_indirect $__indirect_function_table (type $t5)
        if $I13
          loop $L14
            local.get $l7
            local.get $l2
            i32.const 2
            i32.shl
            i32.add
            i32.load
            local.tee $l3
            call $f72133
            block $B15 (result i32)
              i32.const 1
              local.get $l10
              i32.const 1
              i32.and
              br_if $B15
              drop
              i32.const 1
              local.get $l3
              f32.load offset=284
              f32.const 0x0p+0 (;=0;)
              f32.ne
              br_if $B15
              drop
              i32.const 1
              local.get $l3
              f32.load offset=288
              f32.const 0x0p+0 (;=0;)
              f32.ne
              br_if $B15
              drop
              i32.const 1
              local.get $l3
              f32.load offset=292
              f32.const 0x0p+0 (;=0;)
              f32.ne
              br_if $B15
              drop
              i32.const 1
              local.get $l3
              f32.load offset=296
              f32.const 0x0p+0 (;=0;)
              f32.ne
              br_if $B15
              drop
              i32.const 1
              local.get $l3
              f32.load offset=300
              f32.const 0x0p+0 (;=0;)
              f32.ne
              br_if $B15
              drop
              local.get $l3
              f32.load offset=304
              f32.const 0x0p+0 (;=0;)
              f32.ne
            end
            local.set $l10
            local.get $p0
            local.get $l3
            call $f72135
            local.get $l6
            i32.load offset=16
            local.get $l9
            i32.const 2
            i32.shl
            i32.add
            local.get $l3
            i32.store
            local.get $l9
            i32.const 1
            i32.add
            local.set $l9
            local.get $l8
            local.get $l8
            i32.load
            i32.load offset=280
            call_indirect $__indirect_function_table (type $t5)
            local.get $l2
            i32.const 1
            i32.add
            local.tee $l2
            i32.gt_u
            br_if $L14
          end
        end
        local.get $l12
        i32.const 1
        i32.add
        local.tee $l12
        local.get $l11
        i32.ne
        br_if $L11
      end
    end
    block $B16
      local.get $l10
      i32.const 1
      i32.and
      i32.eqz
      br_if $B16
      local.get $l13
      f32.load offset=56
      f32.const 0x0p+0 (;=0;)
      f32.ne
      br_if $B16
      local.get $l13
      i32.const 1
      i32.const 0
      call $f72477
    end
    local.get $l6
    local.get $p1
    i32.store offset=4
    local.get $p0
    i32.const 5944
    i32.add
    local.get $l6
    i32.const 4
    i32.add
    local.get $l6
    i32.const 31
    i32.add
    call $f72047
    local.set $l3
    local.get $l6
    i32.load8_u offset=31
    i32.eqz
    if $I17
      local.get $l3
      local.get $l6
      i32.load offset=4
      i32.store
    end
    block $B18
      local.get $l5
      i32.eqz
      br_if $B18
      local.get $l5
      call $f71660
      local.get $l6
      i32.load offset=16
      local.get $l4
      i32.store
      local.get $l11
      i32.eqz
      br_if $B18
      i32.const 1
      local.set $l8
      i32.const 0
      local.set $l12
      loop $L19
        i32.const 0
        local.set $l7
        local.get $l6
        i32.load offset=16
        local.get $l12
        i32.const 2
        i32.shl
        i32.add
        i32.load
        local.tee $l10
        i32.load offset=356
        if $I20
          local.get $l10
          i32.load offset=352
          local.set $l7
        end
        i32.const 0
        local.set $l9
        local.get $l10
        local.get $l10
        i32.load
        i32.load offset=280
        call_indirect $__indirect_function_table (type $t5)
        if $I21
          loop $L22
            local.get $l7
            local.get $l9
            i32.const 2
            i32.shl
            i32.add
            i32.load
            local.tee $l3
            block $B23 (result i32)
              local.get $l3
              local.get $l3
              i32.load
              i32.load offset=284
              call_indirect $__indirect_function_table (type $t5)
              local.set $l14
              local.get $l5
              i32.load
              local.tee $l2
              local.get $l14
              local.get $l2
              i32.load
              i32.load offset=32
              call_indirect $__indirect_function_table (type $t0)
            end
            i32.store offset=368
            block $B24
              local.get $p1
              i32.load16_u offset=4
              i32.const 12
              i32.ne
              br_if $B24
              local.get $l3
              local.get $l3
              i32.load
              i32.load offset=272
              call_indirect $__indirect_function_table (type $t5)
              local.tee $l2
              local.get $l2
              i32.load
              i32.load offset=48
              call_indirect $__indirect_function_table (type $t5)
              i32.const 79
              i32.store8 offset=285
              block $B25
                block $B26
                  local.get $l2
                  local.get $l2
                  i32.load
                  i32.load offset=60
                  call_indirect $__indirect_function_table (type $t5)
                  br_table $B24 $B25 $B25 $B25 $B26 $B25
                end
                i32.const 4700888
                i32.load
                i32.const 2
                i32.const 3184128
                i32.const 957
                i32.const 3185532
                i32.const 0
                call $f69760
                local.get $l2
                i32.const 0
                local.get $l2
                i32.load
                i32.load offset=56
                call_indirect $__indirect_function_table (type $t1)
                local.get $l3
                i32.const 0
                i32.store offset=368
              end
              local.get $l2
              i32.const 3
              local.get $l2
              i32.load
              i32.load offset=68
              call_indirect $__indirect_function_table (type $t0)
              local.get $l2
              i32.const 4
              local.get $l2
              i32.load
              i32.load offset=68
              call_indirect $__indirect_function_table (type $t0)
              i32.or
              local.get $l2
              i32.const 5
              local.get $l2
              i32.load
              i32.load offset=68
              call_indirect $__indirect_function_table (type $t0)
              i32.or
              local.get $l2
              i32.const 1
              local.get $l2
              i32.load
              i32.load offset=68
              call_indirect $__indirect_function_table (type $t0)
              i32.or
              local.get $l2
              i32.const 2
              local.get $l2
              i32.load
              i32.load offset=68
              call_indirect $__indirect_function_table (type $t0)
              i32.or
              local.get $l2
              i32.const 0
              local.get $l2
              i32.load
              i32.load offset=68
              call_indirect $__indirect_function_table (type $t0)
              i32.or
              i32.const 255
              i32.and
              br_if $B24
              i32.const 4700888
              i32.load
              i32.const 2
              i32.const 3184128
              i32.const 978
              i32.const 3185630
              i32.const 0
              call $f69760
              local.get $l2
              i32.const 0
              local.get $l2
              i32.load
              i32.load offset=56
              call_indirect $__indirect_function_table (type $t1)
              local.get $l3
              i32.const 0
              i32.store offset=368
            end
            local.get $l6
            i32.load offset=16
            local.get $l8
            i32.const 2
            i32.shl
            i32.add
            local.get $l3
            i32.store
            local.get $l8
            i32.const 1
            i32.add
            local.set $l8
            local.get $l10
            local.get $l10
            i32.load
            i32.load offset=280
            call_indirect $__indirect_function_table (type $t5)
            local.get $l9
            i32.const 1
            i32.add
            local.tee $l9
            i32.gt_u
            br_if $L22
          end
        end
        local.get $l12
        i32.const 1
        i32.add
        local.tee $l12
        local.get $l11
        i32.ne
        br_if $L19
      end
    end
    block $B27
      local.get $p1
      i32.load16_u offset=4
      i32.const 12
      i32.ne
      br_if $B27
      local.get $l13
      i32.const 12
      i32.add
      local.set $l3
      local.get $l13
      i32.load8_u offset=48
      i32.const 1
      i32.and
      if $I28
        local.get $l4
        i32.const -64
        i32.sub
        i32.load
        local.tee $l2
        if $I29
          local.get $l2
          i32.load offset=100
          i32.const 1
          i32.store8 offset=159
        end
      end
      local.get $p0
      i32.const 32
      i32.add
      local.set $p0
      global.get $g0
      i32.const 16
      i32.sub
      local.tee $l2
      global.set $g0
      local.get $l3
      i32.load
      local.tee $l3
      if $I30
        local.get $l3
        i32.load
        local.set $l4
        local.get $p0
        i32.load offset=1012
        local.set $p0
        local.get $l2
        local.get $l3
        i64.load offset=48
        i64.store offset=8
        local.get $p0
        local.get $l4
        local.get $l2
        i32.const 8
        i32.add
        local.get $p0
        i32.load
        i32.load offset=32
        call_indirect $__indirect_function_table (type $t2)
      end
      local.get $l2
      i32.const 16
      i32.add
      global.set $g0
      local.get $p1
      i32.load offset=124
      i32.eqz
      br_if $B27
      i32.const 0
      local.set $l3
      loop $L31
        local.get $l5
        local.get $p1
        i32.load offset=120
        local.get $l3
        i32.const 2
        i32.shl
        i32.add
        i32.load
        local.tee $l2
        local.get $l2
        i32.load
        i32.load offset=104
        call_indirect $__indirect_function_table (type $t5)
        i32.load offset=88
        call $f71657
        local.get $l3
        i32.const 1
        i32.add
        local.tee $l3
        local.get $p1
        i32.load offset=124
        i32.lt_u
        br_if $L31
      end
    end
    local.get $l6
    i32.load8_u offset=20
    if $I32
      local.get $l6
      i32.load offset=16
      call $f70044
    end
    local.get $l6
    i32.const 32
    i32.add
    global.set $g0)