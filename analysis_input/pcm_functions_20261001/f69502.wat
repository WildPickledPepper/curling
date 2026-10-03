  (func $f69502 (type $t0) (param $p0 i32) (param $p1 i32) (result i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 f32) (local $l13 i64)
    global.get $g0
    i32.const 160
    i32.sub
    local.tee $l5
    global.set $g0
    i32.const 1
    local.set $l7
    block $B0
      local.get $p1
      i32.load
      local.tee $l2
      i32.eqz
      br_if $B0
      local.get $l2
      i32.load offset=12
      i32.eqz
      br_if $B0
      local.get $l2
      i32.const 8
      i32.add
      local.tee $l7
      local.get $l7
      i32.load
      i32.const 1
      i32.add
      i32.store
      local.get $l5
      local.get $p1
      i32.load
      local.tee $l2
      i32.store offset=56
      local.get $p0
      i32.const 412
      i32.add
      local.set $l7
      global.get $g0
      i32.const 112
      i32.sub
      local.tee $l9
      global.set $g0
      local.get $l5
      i32.const 56
      i32.add
      local.tee $l8
      i32.load
      local.set $l6
      block $B1
        local.get $p0
        i32.load offset=772
        if $I2
          local.get $l6
          i32.eqz
          br_if $B1
          local.get $l6
          i32.load offset=12
          local.tee $l11
          if $I3
            local.get $l11
            i32.const 0
            i32.store offset=228
            local.get $l11
            call $f69551
            local.get $l8
            i32.load
            local.tee $l6
            i32.eqz
            br_if $B1
          end
          local.get $l6
          i32.load offset=12
          local.tee $l6
          i32.eqz
          br_if $B1
          local.get $l6
          i32.const 0
          i32.store offset=220
          local.get $l6
          call $f69550
          br $B1
        end
        i32.const 36
        local.set $l11
        block $B4
          block $B5
            local.get $l6
            i32.eqz
            br_if $B5
            local.get $l6
            i32.load offset=12
            local.tee $l3
            if $I6
              local.get $l3
              i32.load offset=244
              if $I7
                local.get $l3
                i32.const 0
                i32.store offset=228
                local.get $l3
                call $f69551
                local.get $l8
                i32.load
                local.tee $l6
                i32.eqz
                br_if $B1
                local.get $l6
                i32.load offset=12
                local.tee $l6
                i32.eqz
                br_if $B1
                local.get $l6
                i32.const 0
                i32.store offset=220
                local.get $l6
                call $f69550
                br $B1
              end
              local.get $l3
              local.get $l7
              f32.load offset=52
              f32.store offset=228
              local.get $l3
              call $f69551
              local.get $l8
              i32.load
              local.tee $l6
              i32.eqz
              br_if $B5
            end
            local.get $l6
            i32.load offset=12
            local.tee $l6
            i32.eqz
            br_if $B5
            local.get $l7
            f32.load offset=56
            local.set $l12
            global.get $g0
            i32.const 112
            i32.sub
            local.tee $l4
            global.set $g0
            local.get $l6
            local.get $l12
            f32.store offset=60
            local.get $l6
            i32.const 130
            i32.add
            local.tee $l3
            local.get $l3
            i32.load16_u
            i32.const 65279
            i32.and
            local.get $l6
            i32.load offset=148
            local.tee $l3
            i32.eqz
            i32.const 8
            i32.shl
            i32.or
            i32.store16
            local.get $l6
            i32.const 132
            i32.add
            local.tee $l6
            local.get $l6
            i32.load16_u
            local.tee $l6
            i32.const 512
            i32.and
            i32.const 512
            local.get $l3
            select
            local.get $l6
            i32.const 65023
            i32.and
            i32.or
            i32.store16
            i32.const 0
            local.set $l6
            block $B8
              local.get $l3
              i32.eqz
              br_if $B8
              local.get $l3
              f32.const 0x0p+0 (;=0;)
              local.get $l12
              f32.const 0x1.68p+8 (;=360;)
              f32.min
              local.get $l12
              f32.const 0x0p+0 (;=0;)
              f32.lt
              select
              call $f69309
              local.tee $l3
              i32.eqz
              br_if $B8
              local.get $l4
              local.get $l3
              call $f69541
              i32.store offset=12
              local.get $l4
              i32.const 321820
              i32.store offset=8
              local.get $l4
              i32.const 214
              i32.store offset=4
              local.get $l4
              i32.const 103683
              i32.store
              local.get $l4
              i32.const 16
              i32.add
              i32.const 293712
              local.get $l4
              call $f569
              local.get $l4
              i32.const 403047
              i32.store offset=108
              local.get $l4
              i32.const 403047
              i32.store offset=104
              local.get $l4
              i64.const 0
              i64.store offset=96
              local.get $l4
              i32.const 403047
              i32.store offset=60
              local.get $l4
              i32.const 403047
              i32.store offset=56
              local.get $l4
              i32.const 403047
              i32.store offset=52
              local.get $l4
              i64.const 0
              i64.store offset=84 align=4
              local.get $l4
              i64.const 1
              i64.store offset=76 align=4
              local.get $l4
              i64.const -4294967281
              i64.store offset=68 align=4
              local.get $l4
              i32.const 403047
              i32.store offset=64
              local.get $l4
              i32.const 1
              i32.store8 offset=92
              local.get $l4
              local.get $l4
              i32.const 16
              i32.add
              local.get $l4
              i32.load offset=16
              local.get $l4
              i32.load8_u offset=36
              i32.const 1
              i32.eq
              select
              i32.store offset=48
              local.get $l4
              i32.const 48
              i32.add
              call $f83275
              local.get $l4
              i32.load8_u offset=36
              i32.eqz
              if $I9
                local.get $l4
                i32.load offset=16
                local.get $l4
                i32.load offset=40
                i32.const 403047
                i32.const 518
                call $f83342
              end
              local.get $l3
              local.set $l6
            end
            local.get $l4
            i32.const 112
            i32.add
            global.set $g0
            local.get $l6
            local.tee $l11
            i32.eqz
            br_if $B4
          end
          local.get $l9
          local.get $l11
          call $f69453
          i32.store offset=12
          local.get $l9
          i32.const 321757
          i32.store offset=8
          local.get $l9
          i32.const 993
          i32.store offset=4
          local.get $l9
          i32.const 103865
          i32.store
          local.get $l9
          i32.const 16
          i32.add
          i32.const 293712
          local.get $l9
          call $f569
          local.get $l9
          i32.const 403047
          i32.store offset=108
          local.get $l9
          i32.const 403047
          i32.store offset=104
          local.get $l9
          i64.const 0
          i64.store offset=96
          local.get $l9
          i32.const 403047
          i32.store offset=60
          local.get $l9
          i32.const 403047
          i32.store offset=56
          local.get $l9
          i32.const 403047
          i32.store offset=52
          local.get $l9
          i64.const 0
          i64.store offset=84 align=4
          local.get $l9
          i64.const 1
          i64.store offset=76 align=4
          local.get $l9
          i64.const -4294967281
          i64.store offset=68 align=4
          local.get $l9
          i32.const 403047
          i32.store offset=64
          local.get $l9
          i32.const 1
          i32.store8 offset=92
          local.get $l9
          local.get $l9
          i32.const 16
          i32.add
          local.get $l9
          i32.load offset=16
          local.get $l9
          i32.load8_u offset=36
          i32.const 1
          i32.eq
          select
          i32.store offset=48
          local.get $l9
          i32.const 48
          i32.add
          call $f83275
          local.get $l9
          i32.load8_u offset=36
          br_if $B4
          local.get $l9
          i32.load offset=16
          local.get $l9
          i32.load offset=40
          i32.const 403047
          i32.const 518
          call $f83342
        end
        local.get $l8
        i32.load
        local.tee $l6
        i32.eqz
        br_if $B1
        local.get $l6
        i32.load offset=12
        local.tee $l6
        i32.eqz
        br_if $B1
        local.get $l6
        local.get $l7
        f32.load offset=60
        f32.store offset=220
        local.get $l6
        call $f69550
      end
      local.get $p0
      i32.load offset=776
      local.tee $l6
      if $I10
        local.get $l6
        local.get $l7
        f32.load offset=52
        f32.store offset=128
        local.get $p0
        i32.load offset=776
        local.get $l7
        f32.load offset=56
        f32.store offset=136
        local.get $p0
        i32.load offset=776
        local.get $l7
        f32.load offset=60
        f32.store offset=140
      end
      local.get $p0
      i32.load offset=780
      local.tee $l6
      if $I11
        local.get $l6
        local.get $l7
        f32.load offset=52
        f32.store offset=128
        local.get $p0
        i32.load offset=780
        local.get $l7
        f32.load offset=56
        f32.store offset=136
        local.get $p0
        i32.load offset=780
        local.get $l7
        f32.load offset=60
        f32.store offset=140
      end
      local.get $l9
      i32.const 112
      i32.add
      global.set $g0
      local.get $l2
      if $I12
        local.get $l2
        i32.const 8
        i32.add
        local.tee $l3
        local.get $l3
        i32.load
        i32.const 1
        i32.sub
        local.tee $l3
        i32.store
        local.get $l3
        i32.eqz
        if $I13
          local.get $l2
          i32.const 4
          i32.add
          local.tee $l2
          i32.load
          local.set $l3
          local.get $l2
          i32.const 4
          i32.sub
          local.tee $l2
          local.get $l2
          i32.load
          i32.load
          call_indirect $__indirect_function_table (type $t5)
          drop
          local.get $l2
          local.get $l3
          i32.const 403047
          i32.const 76
          call $f83342
        end
        local.get $l5
        i32.const 0
        i32.store offset=56
      end
      local.get $p1
      i32.load
      local.tee $l2
      if $I14 (result i32)
        local.get $l2
        i32.const 8
        i32.add
        local.tee $l2
        local.get $l2
        i32.load
        i32.const 1
        i32.add
        i32.store
        local.get $p1
        i32.load
      else
        i32.const 0
      end
      local.set $l2
      block $B15
        block $B16
          block $B17
            block $B18
              local.get $p0
              i32.load offset=772
              if $I19
                local.get $p0
                i32.load offset=776
                br_if $B18
              end
              local.get $l2
              i32.eqz
              br_if $B15
              local.get $l2
              i32.load offset=12
              local.tee $l3
              i32.eqz
              br_if $B16
              local.get $l3
              i32.load offset=244
              if $I20
                f32.const 0x1p+0 (;=1;)
                local.set $l12
                local.get $p0
                i32.load offset=780
                br_if $B17
              end
              local.get $p0
              f32.load offset=632
              f32.const 0x0p+0 (;=0;)
              local.get $l3
              f32.load offset=228
              local.get $l3
              f32.load offset=232
              f32.add
              local.tee $l12
              f32.const 0x1p+0 (;=1;)
              f32.min
              local.get $l12
              f32.const 0x0p+0 (;=0;)
              f32.lt
              select
              local.tee $l12
              f32.mul
              f32.const 0x1p+0 (;=1;)
              local.get $l12
              f32.sub
              f32.add
              local.set $l12
              br $B17
            end
            local.get $l2
            i32.eqz
            br_if $B15
            f32.const 0x1p+0 (;=1;)
            local.set $l12
            local.get $l2
            i32.load offset=12
            local.tee $l3
            i32.eqz
            br_if $B16
          end
          local.get $l3
          local.get $l12
          f32.store offset=236
          local.get $l3
          call $f69548
        end
        local.get $l2
        i32.const 8
        i32.add
        local.tee $l3
        local.get $l3
        i32.load
        i32.const 1
        i32.sub
        local.tee $l3
        i32.store
        local.get $l3
        br_if $B15
        local.get $l2
        i32.const 4
        i32.add
        local.tee $l2
        i32.load
        local.set $l3
        local.get $l2
        i32.const 4
        i32.sub
        local.tee $l2
        local.get $l2
        i32.load
        i32.load
        call_indirect $__indirect_function_table (type $t5)
        drop
        local.get $l2
        local.get $l3
        i32.const 403047
        i32.const 76
        call $f83342
      end
      block $B21
        local.get $p1
        i32.load
        local.tee $l2
        i32.eqz
        if $I22
          local.get $l5
          i32.const 0
          i32.store offset=48
          local.get $p0
          local.get $l7
          local.get $l5
          i32.const 48
          i32.add
          call $f69505
          br $B21
        end
        local.get $l2
        i32.const 8
        i32.add
        local.tee $l2
        local.get $l2
        i32.load
        i32.const 1
        i32.add
        i32.store
        local.get $l5
        local.get $p1
        i32.load
        local.tee $l2
        i32.store offset=48
        local.get $p0
        local.get $l7
        local.get $l5
        i32.const 48
        i32.add
        call $f69505
        local.get $l2
        i32.eqz
        br_if $B21
        local.get $l2
        i32.const 8
        i32.add
        local.tee $l3
        local.get $l3
        i32.load
        i32.const 1
        i32.sub
        local.tee $l3
        i32.store
        local.get $l3
        i32.eqz
        if $I23
          local.get $l2
          i32.const 4
          i32.add
          local.tee $l2
          i32.load
          local.set $l3
          local.get $l2
          i32.const 4
          i32.sub
          local.tee $l2
          local.get $l2
          i32.load
          i32.load
          call_indirect $__indirect_function_table (type $t5)
          drop
          local.get $l2
          local.get $l3
          i32.const 403047
          i32.const 76
          call $f83342
        end
        local.get $l5
        i32.const 0
        i32.store offset=48
      end
      block $B24
        block $B25
          block $B26
            local.get $p1
            i32.load
            local.tee $l2
            i32.eqz
            br_if $B26
            local.get $l2
            i32.const 8
            i32.add
            local.tee $l2
            local.get $l2
            i32.load
            i32.const 1
            i32.add
            i32.store
            local.get $p1
            i32.load
            local.tee $l2
            i32.eqz
            br_if $B26
            local.get $l2
            i32.load offset=12
            local.tee $l3
            if $I27
              local.get $p0
              i32.const 424
              i32.add
              local.set $l9
              global.get $g0
              i32.const 112
              i32.sub
              local.tee $l4
              global.set $g0
              local.get $l7
              local.tee $l8
              if $I28
                local.get $l3
                i32.const 132
                i32.add
                local.tee $l10
                local.get $l10
                i32.load16_u
                local.tee $l10
                i32.const 512
                i32.and
                i32.const 512
                local.get $l3
                i32.load offset=148
                local.tee $l6
                select
                local.get $l10
                i32.const 65023
                i32.and
                i32.or
                i32.store16
                local.get $l8
                i32.load offset=8
                local.set $l10
                local.get $l8
                i64.load align=4
                local.set $l13
                local.get $l3
                i32.const 130
                i32.add
                local.tee $l11
                local.get $l6
                i32.eqz
                local.get $l11
                i32.load16_u
                i32.const 65534
                i32.and
                i32.or
                i32.store16
                local.get $l3
                local.get $l13
                i64.store offset=4 align=4
                local.get $l3
                local.get $l10
                i32.store offset=12
              end
              local.get $l3
              i32.load offset=148
              local.set $l10
              local.get $l9
              if $I29
                local.get $l3
                i32.const 132
                i32.add
                local.tee $l6
                local.get $l6
                i32.load16_u
                local.tee $l6
                i32.const 512
                i32.and
                i32.const 512
                local.get $l10
                select
                local.get $l6
                i32.const 65023
                i32.and
                i32.or
                i32.store16
                local.get $l3
                local.get $l9
                i64.load align=4
                i64.store offset=16 align=4
                local.get $l3
                local.get $l9
                i32.load offset=8
                i32.store offset=24
                local.get $l3
                i32.const 130
                i32.add
                local.tee $l3
                local.get $l3
                i32.load16_u
                i32.const 65533
                i32.and
                local.get $l10
                i32.eqz
                i32.const 1
                i32.shl
                i32.or
                i32.store16
              end
              block $B30
                local.get $l10
                i32.eqz
                br_if $B30
                local.get $l10
                local.get $l8
                local.get $l9
                call $f69307
                local.tee $l8
                i32.eqz
                br_if $B30
                local.get $l4
                local.get $l8
                call $f69541
                i32.store offset=12
                local.get $l4
                i32.const 307047
                i32.store offset=8
                local.get $l4
                i32.const 163
                i32.store offset=4
                local.get $l4
                i32.const 103683
                i32.store
                local.get $l4
                i32.const 16
                i32.add
                i32.const 293712
                local.get $l4
                call $f569
                local.get $l4
                i32.const 403047
                i32.store offset=108
                local.get $l4
                i32.const 403047
                i32.store offset=104
                local.get $l4
                i64.const 0
                i64.store offset=96
                local.get $l4
                i32.const 403047
                i32.store offset=60
                local.get $l4
                i32.const 403047
                i32.store offset=56
                local.get $l4
                i32.const 403047
                i32.store offset=52
                local.get $l4
                i64.const 0
                i64.store offset=84 align=4
                local.get $l4
                i64.const 1
                i64.store offset=76 align=4
                local.get $l4
                i64.const -4294967281
                i64.store offset=68 align=4
                local.get $l4
                i32.const 403047
                i32.store offset=64
                local.get $l4
                i32.const 1
                i32.store8 offset=92
                local.get $l4
                local.get $l4
                i32.const 16
                i32.add
                local.get $l4
                i32.load offset=16
                local.get $l4
                i32.load8_u offset=36
                i32.const 1
                i32.eq
                select
                i32.store offset=48
                local.get $l4
                i32.const 48
                i32.add
                call $f83275
                local.get $l4
                i32.load8_u offset=36
                i32.eqz
                if $I31
                  local.get $l4
                  i32.load offset=16
                  local.get $l4
                  i32.load offset=40
                  i32.const 403047
                  i32.const 518
                  call $f83342
                end
              end
              local.get $l4
              i32.const 112
              i32.add
              global.set $g0
            end
            local.get $l2
            i32.const 8
            i32.add
            local.tee $l3
            local.get $l3
            i32.load
            i32.const 1
            i32.sub
            local.tee $l3
            i32.store
            local.get $l3
            i32.eqz
            if $I32
              local.get $l2
              i32.const 4
              i32.add
              local.tee $l2
              i32.load
              local.set $l3
              local.get $l2
              i32.const 4
              i32.sub
              local.tee $l2
              local.get $l2
              i32.load
              i32.load
              call_indirect $__indirect_function_table (type $t5)
              drop
              local.get $l2
              local.get $l3
              i32.const 403047
              i32.const 76
              call $f83342
            end
            local.get $p1
            i32.load
            local.tee $l2
            br_if $B25
          end
          local.get $l5
          i32.const 0
          i32.store offset=40
          local.get $p0
          local.get $l7
          local.get $l5
          i32.const 40
          i32.add
          call $f69506
          br $B24
        end
        local.get $l2
        i32.const 8
        i32.add
        local.tee $l2
        local.get $l2
        i32.load
        i32.const 1
        i32.add
        i32.store
        local.get $l5
        local.get $p1
        i32.load
        local.tee $l2
        i32.store offset=40
        local.get $p0
        local.get $l7
        local.get $l5
        i32.const 40
        i32.add
        call $f69506
        local.get $l2
        i32.eqz
        br_if $B24
        local.get $l2
        i32.const 8
        i32.add
        local.tee $l3
        local.get $l3
        i32.load
        i32.const 1
        i32.sub
        local.tee $l3
        i32.store
        local.get $l3
        i32.eqz
        if $I33
          local.get $l2
          i32.const 4
          i32.add
          local.tee $l2
          i32.load
          local.set $l3
          local.get $l2
          i32.const 4
          i32.sub
          local.tee $l2
          local.get $l2
          i32.load
          i32.load
          call_indirect $__indirect_function_table (type $t5)
          drop
          local.get $l2
          local.get $l3
          i32.const 403047
          i32.const 76
          call $f83342
        end
        local.get $l5
        i32.const 0
        i32.store offset=40
      end
      block $B34
        local.get $p1
        i32.load
        local.tee $l2
        i32.eqz
        if $I35
          local.get $l5
          i32.const 0
          i32.store offset=32
          local.get $p0
          local.get $l7
          local.get $l5
          i32.const 32
          i32.add
          call $f69507
          br $B34
        end
        local.get $l2
        i32.const 8
        i32.add
        local.tee $l2
        local.get $l2
        i32.load
        i32.const 1
        i32.add
        i32.store
        local.get $l5
        local.get $p1
        i32.load
        local.tee $l2
        i32.store offset=32
        local.get $p0
        local.get $l7
        local.get $l5
        i32.const 32
        i32.add
        call $f69507
        local.get $l2
        i32.eqz
        br_if $B34
        local.get $l2
        i32.const 8
        i32.add
        local.tee $l3
        local.get $l3
        i32.load
        i32.const 1
        i32.sub
        local.tee $l3
        i32.store
        local.get $l3
        i32.eqz
        if $I36
          local.get $l2
          i32.const 4
          i32.add
          local.tee $l2
          i32.load
          local.set $l3
          local.get $l2
          i32.const 4
          i32.sub
          local.tee $l2
          local.get $l2
          i32.load
          i32.load
          call_indirect $__indirect_function_table (type $t5)
          drop
          local.get $l2
          local.get $l3
          i32.const 403047
          i32.const 76
          call $f83342
        end
        local.get $l5
        i32.const 0
        i32.store offset=32
      end
      local.get $p1
      i32.load
      i32.const 8
      i32.add
      local.tee $l2
      local.get $l2
      i32.load
      i32.const 1
      i32.add
      i32.store
      local.get $p1
      i32.load
      local.tee $l2
      i32.load offset=12
      local.tee $l3
      local.get $p0
      f32.load offset=492
      f32.store offset=212
      local.get $l3
      call $f69549
      local.get $l2
      i32.const 8
      i32.add
      local.tee $l3
      local.get $l3
      i32.load
      i32.const 1
      i32.sub
      local.tee $l3
      i32.store
      local.get $l3
      i32.eqz
      if $I37
        local.get $l2
        i32.const 4
        i32.add
        local.tee $l2
        i32.load
        local.set $l3
        local.get $l2
        i32.const 4
        i32.sub
        local.tee $l2
        local.get $l2
        i32.load
        i32.load
        call_indirect $__indirect_function_table (type $t5)
        drop
        local.get $l2
        local.get $l3
        i32.const 403047
        i32.const 76
        call $f83342
      end
      block $B38
        block $B39
          block $B40
            local.get $p1
            i32.load
            local.tee $l2
            i32.eqz
            br_if $B40
            local.get $l2
            i32.const 8
            i32.add
            local.tee $l2
            local.get $l2
            i32.load
            i32.const 1
            i32.add
            i32.store
            local.get $p1
            i32.load
            local.tee $l2
            i32.eqz
            br_if $B40
            block $B41
              local.get $l2
              i32.load offset=12
              local.tee $l3
              i32.eqz
              br_if $B41
              block $B42
                local.get $l3
                i32.load offset=244
                i32.eqz
                br_if $B42
                local.get $p0
                i32.load offset=780
                i32.eqz
                br_if $B42
                local.get $l3
                local.get $p0
                i32.const 636
                i32.add
                local.tee $l8
                f32.load
                local.get $l3
                f32.load offset=248
                f32.mul
                f32.store offset=200
                local.get $l3
                call $f69548
                local.get $p0
                i32.load offset=780
                f32.const 0x0p+0 (;=0;)
                local.get $l8
                f32.load
                local.get $p0
                i32.load8_u offset=640
                select
                f32.store offset=152
                br $B41
              end
              local.get $l3
              local.get $p0
              f32.load offset=636
              f32.store offset=200
              local.get $l3
              call $f69548
            end
            local.get $l2
            i32.const 8
            i32.add
            local.tee $l3
            local.get $l3
            i32.load
            i32.const 1
            i32.sub
            local.tee $l3
            i32.store
            local.get $l3
            i32.eqz
            if $I43
              local.get $l2
              i32.const 4
              i32.add
              local.tee $l2
              i32.load
              local.set $l3
              local.get $l2
              i32.const 4
              i32.sub
              local.tee $l2
              local.get $l2
              i32.load
              i32.load
              call_indirect $__indirect_function_table (type $t5)
              drop
              local.get $l2
              local.get $l3
              i32.const 403047
              i32.const 76
              call $f83342
            end
            local.get $p1
            i32.load
            local.tee $l2
            i32.eqz
            br_if $B40
            local.get $l2
            i32.const 8
            i32.add
            local.tee $l2
            local.get $l2
            i32.load
            i32.const 1
            i32.add
            i32.store
            local.get $p1
            i32.load
            local.tee $l2
            i32.eqz
            br_if $B40
            local.get $l2
            i32.load offset=12
            local.tee $l3
            if $I44
              local.get $l3
              local.get $p0
              i32.load8_u offset=640
              i32.const 0
              i32.ne
              call $f69557
            end
            local.get $l2
            i32.const 8
            i32.add
            local.tee $l3
            local.get $l3
            i32.load
            i32.const 1
            i32.sub
            local.tee $l3
            i32.store
            local.get $l3
            i32.eqz
            if $I45
              local.get $l2
              i32.const 4
              i32.add
              local.tee $l2
              i32.load
              local.set $l3
              local.get $l2
              i32.const 4
              i32.sub
              local.tee $l2
              local.get $l2
              i32.load
              i32.load
              call_indirect $__indirect_function_table (type $t5)
              drop
              local.get $l2
              local.get $l3
              i32.const 403047
              i32.const 76
              call $f83342
            end
            local.get $p1
            i32.load
            local.tee $l2
            br_if $B39
          end
          local.get $l5
          i32.const 0
          i32.store offset=24
          local.get $l7
          local.get $l5
          i32.const 24
          i32.add
          call $f69508
          br $B38
        end
        local.get $l2
        i32.const 8
        i32.add
        local.tee $l2
        local.get $l2
        i32.load
        i32.const 1
        i32.add
        i32.store
        local.get $l5
        local.get $p1
        i32.load
        local.tee $l2
        i32.store offset=24
        local.get $l7
        local.get $l5
        i32.const 24
        i32.add
        call $f69508
        local.get $l2
        i32.eqz
        br_if $B38
        local.get $l2
        i32.const 8
        i32.add
        local.tee $l7
        local.get $l7
        i32.load
        i32.const 1
        i32.sub
        local.tee $l7
        i32.store
        local.get $l7
        i32.eqz
        if $I46
          local.get $l2
          i32.const 4
          i32.add
          local.tee $l7
          i32.load
          local.set $l2
          local.get $l7
          i32.const 4
          i32.sub
          local.tee $l7
          local.get $l7
          i32.load
          i32.load
          call_indirect $__indirect_function_table (type $t5)
          drop
          local.get $l7
          local.get $l2
          i32.const 403047
          i32.const 76
          call $f83342
        end
        local.get $l5
        i32.const 0
        i32.store offset=24
      end
      local.get $p1
      i32.load
      i32.load offset=12
      local.set $l7
      block $B47
        local.get $p0
        i32.load offset=772
        if $I48
          local.get $l7
          i32.eqz
          br_if $B47
          local.get $l7
          local.get $l7
          i32.load offset=252
          i32.const 2
          i32.or
          i32.store offset=252
          br $B47
        end
        local.get $l7
        i32.eqz
        br_if $B47
        local.get $l7
        local.get $l7
        i32.load offset=252
        i32.const -3
        i32.and
        i32.store offset=252
      end
      local.get $p1
      i32.load
      local.set $p1
      local.get $l5
      i32.const 1
      i32.store8 offset=23
      local.get $p1
      i32.load offset=12
      local.set $p0
      local.get $l5
      i32.const 23
      i32.add
      local.set $p1
      global.get $g0
      i32.const 112
      i32.sub
      local.tee $l8
      global.set $g0
      block $B49
        local.get $p0
        i32.load offset=148
        local.tee $p0
        i32.eqz
        if $I50
          local.get $p1
          i32.const 1
          i32.store8
          i32.const 0
          local.set $p1
          br $B49
        end
        global.get $g0
        i32.const 16
        i32.sub
        local.tee $l7
        global.set $g0
        block $B51
          block $B52
            block $B53
              local.get $p0
              i32.const 26
              i32.shr_u
              i32.const 60
              i32.and
              i32.const 4696144
              i32.add
              i32.load
              local.tee $l6
              i32.eqz
              br_if $B53
              local.get $l6
              i32.load offset=132
              local.get $p0
              i32.const 14
              i32.shr_u
              i32.const 16380
              i32.and
              i32.add
              i32.load
              local.tee $l6
              i32.eqz
              br_if $B53
              local.get $l6
              i32.load8_u offset=16
              br_if $B53
              local.get $l6
              i32.load offset=12
              local.get $p0
              i32.const 65535
              i32.and
              i32.eq
              br_if $B52
            end
            local.get $l7
            i32.const 126185
            i32.store offset=4
            i32.const 36
            local.set $p0
            local.get $l7
            i32.const 36
            i32.store
            i32.const 393450
            local.get $l7
            call $f1289
            br $B51
          end
          i32.const 0
          local.set $p0
          local.get $p1
          i32.eqz
          br_if $B51
          local.get $p1
          local.get $l6
          i32.load8_u offset=186
          i32.store8
        end
        local.get $l7
        i32.const 16
        i32.add
        global.set $g0
        local.get $p0
        local.tee $p1
        i32.eqz
        if $I54
          i32.const 0
          local.set $p1
          br $B49
        end
        local.get $l8
        local.get $p1
        call $f69541
        i32.store offset=12
        local.get $l8
        i32.const 307088
        i32.store offset=8
        local.get $l8
        i32.const 289
        i32.store offset=4
        local.get $l8
        i32.const 103683
        i32.store
        local.get $l8
        i32.const 16
        i32.add
        i32.const 293712
        local.get $l8
        call $f569
        local.get $l8
        i32.const 403047
        i32.store offset=108
        local.get $l8
        i32.const 403047
        i32.store offset=104
        local.get $l8
        i64.const 0
        i64.store offset=96
        local.get $l8
        i32.const 403047
        i32.store offset=60
        local.get $l8
        i32.const 403047
        i32.store offset=56
        local.get $l8
        i32.const 403047
        i32.store offset=52
        local.get $l8
        i64.const 0
        i64.store offset=84 align=4
        local.get $l8
        i64.const 1
        i64.store offset=76 align=4
        local.get $l8
        i64.const -4294967281
        i64.store offset=68 align=4
        local.get $l8
        i32.const 403047
        i32.store offset=64
        local.get $l8
        i32.const 1
        i32.store8 offset=92
        local.get $l8
        local.get $l8
        i32.const 16
        i32.add
        local.get $l8
        i32.load offset=16
        local.get $l8
        i32.load8_u offset=36
        i32.const 1
        i32.eq
        select
        i32.store offset=48
        local.get $l8
        i32.const 48
        i32.add
        call $f83275
        local.get $l8
        i32.load8_u offset=36
        br_if $B49
        local.get $l8
        i32.load offset=16
        local.get $l8
        i32.load offset=40
        i32.const 403047
        i32.const 518
        call $f83342
      end
      local.get $l8
      i32.const 112
      i32.add
      global.set $g0
      block $B55
        local.get $p1
        i32.eqz
        br_if $B55
        local.get $l5
        local.get $p1
        call $f69453
        i32.store offset=12
        local.get $l5
        i32.const 307124
        i32.store offset=8
        local.get $l5
        i32.const 1318
        i32.store offset=4
        local.get $l5
        i32.const 103865
        i32.store
        local.get $l5
        i32.const -64
        i32.sub
        i32.const 293712
        local.get $l5
        call $f569
        local.get $l5
        i32.const 403047
        i32.store offset=156
        local.get $l5
        i32.const 403047
        i32.store offset=152
        local.get $l5
        i64.const 0
        i64.store offset=144
        local.get $l5
        i32.const 403047
        i32.store offset=108
        local.get $l5
        i32.const 403047
        i32.store offset=104
        local.get $l5
        i32.const 403047
        i32.store offset=100
        local.get $l5
        i64.const 0
        i64.store offset=132 align=4
        local.get $l5
        i64.const 1
        i64.store offset=124 align=4
        local.get $l5
        i64.const -4294967281
        i64.store offset=116 align=4
        local.get $l5
        i32.const 403047
        i32.store offset=112
        local.get $l5
        i32.const 1
        i32.store8 offset=140
        local.get $l5
        local.get $l5
        i32.const -64
        i32.sub
        local.get $l5
        i32.load offset=64
        local.get $l5
        i32.load8_u offset=84
        i32.const 1
        i32.eq
        select
        i32.store offset=96
        local.get $l5
        i32.const 96
        i32.add
        call $f83275
        local.get $l5
        i32.load8_u offset=84
        br_if $B55
        local.get $l5
        i32.load offset=64
        local.get $l5
        i32.load offset=88
        i32.const 403047
        i32.const 518
        call $f83342
      end
      local.get $l5
      i32.load8_u offset=23
      i32.const 0
      i32.ne
      local.set $l7
    end
    local.get $l5
    i32.const 160
    i32.add
    global.set $g0
    local.get $l7)
