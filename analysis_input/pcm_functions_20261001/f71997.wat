  (func $f71997 (type $t6) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32)
    (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32)
    local.get $p0
    i32.const 4932
    i32.add
    local.set $l5
    global.get $g0
    i32.const 288
    i32.sub
    local.tee $l10
    global.set $g0
    block $B0
      local.get $p2
      i32.eqz
      if $I1
        global.get $g0
        i32.const 16
        i32.sub
        local.tee $l6
        global.set $g0
        local.get $p1
        local.tee $l8
        local.get $p0
        local.tee $p2
        i32.store
        local.get $p1
        i32.load offset=4
        local.set $l9
        block $B2
          local.get $p0
          i32.load8_u offset=4785
          i32.eqz
          if $I3
            local.get $l8
            local.get $l9
            i32.const 268435455
            i32.and
            i32.const -2147483648
            i32.or
            i32.store offset=4
            local.get $p2
            i32.const 16
            i32.add
            local.get $l8
            local.get $p3
            local.get $p4
            call $f72015
            br $B2
          end
          local.get $l9
          i32.const 1073741823
          i32.and
          local.set $p2
          local.get $l9
          i32.const -1073741824
          i32.ge_u
          if $I4
            local.get $l8
            local.get $p2
            i32.const -2147483648
            i32.or
            i32.store offset=4
            local.get $l9
            i32.const 268435456
            i32.and
            br_if $B2
            local.get $l5
            local.get $l8
            call $f71988
            br $B2
          end
          local.get $l8
          local.get $p2
          i32.const 1073741824
          i32.or
          i32.store offset=4
          local.get $l6
          local.get $l8
          i32.store offset=8
          local.get $l5
          local.get $l6
          i32.const 8
          i32.add
          local.get $l6
          i32.const 15
          i32.add
          call $f71989
          local.set $l8
          local.get $l6
          i32.load8_u offset=15
          br_if $B2
          local.get $l8
          local.get $l6
          i32.load offset=8
          i32.store
        end
        local.get $l6
        i32.const 16
        i32.add
        global.set $g0
        local.get $p1
        block $B5 (result i32)
          block $B6
            local.get $p1
            f32.load offset=260
            f32.const 0x0p+0 (;=0;)
            f32.ne
            br_if $B6
            local.get $p1
            f32.load offset=236
            f32.const 0x0p+0 (;=0;)
            f32.ne
            br_if $B6
            local.get $p1
            f32.load offset=240
            f32.const 0x0p+0 (;=0;)
            f32.ne
            br_if $B6
            local.get $p1
            f32.load offset=244
            f32.const 0x0p+0 (;=0;)
            f32.ne
            br_if $B6
            local.get $p1
            f32.load offset=248
            f32.const 0x0p+0 (;=0;)
            f32.ne
            br_if $B6
            local.get $p1
            f32.load offset=252
            f32.const 0x0p+0 (;=0;)
            f32.ne
            br_if $B6
            i32.const 1
            local.get $p1
            f32.load offset=256
            f32.const 0x0p+0 (;=0;)
            f32.eq
            br_if $B5
            drop
          end
          i32.const 0
        end
        i32.store offset=264
        local.get $p0
        i32.load8_u offset=4785
        i32.eqz
        br_if $B0
        local.get $l10
        i32.const 1
        i32.store8 offset=272
        local.get $l10
        i64.const 274877906944
        i64.store offset=280
        local.get $l10
        local.get $l10
        i32.const 16
        i32.add
        i32.store offset=276
        i32.const 0
        local.set $p0
        block $B7
          local.get $p1
          local.get $l10
          i32.const 12
          i32.add
          i32.const 0
          call $f72634
          local.tee $l5
          i32.eqz
          br_if $B7
          local.get $p1
          i32.load offset=4
          i32.const -1073741824
          i32.and
          local.set $l9
          local.get $p1
          i32.load
          local.set $l8
          local.get $l5
          i32.const 1
          i32.and
          local.set $p2
          local.get $l5
          i32.const 1
          i32.ne
          if $I8
            local.get $l5
            i32.const -2
            i32.and
            local.set $p1
            loop $L9
              local.get $p0
              i32.const 2
              i32.shl
              local.tee $l5
              local.get $l10
              i32.load offset=12
              i32.add
              i32.load
              i32.const 32
              i32.add
              local.tee $p4
              i32.load offset=4
              local.tee $p3
              i32.const 251658240
              i32.and
              i32.const 16777216
              i32.eq
              if $I10
                local.get $p4
                local.get $l8
                i32.store
                local.get $p4
                local.get $p3
                i32.const 1073741823
                i32.and
                local.get $l9
                i32.or
                i32.store offset=4
              end
              local.get $l10
              i32.load offset=12
              local.get $l5
              i32.const 4
              i32.or
              i32.add
              i32.load
              i32.const 32
              i32.add
              local.tee $l5
              i32.load offset=4
              local.tee $p4
              i32.const 251658240
              i32.and
              i32.const 16777216
              i32.eq
              if $I11
                local.get $l5
                local.get $l8
                i32.store
                local.get $l5
                local.get $p4
                i32.const 1073741823
                i32.and
                local.get $l9
                i32.or
                i32.store offset=4
              end
              local.get $p0
              i32.const 2
              i32.add
              local.set $p0
              local.get $p1
              i32.const 2
              i32.sub
              local.tee $p1
              br_if $L9
            end
          end
          local.get $p2
          i32.eqz
          br_if $B7
          local.get $l10
          i32.load offset=12
          local.get $p0
          i32.const 2
          i32.shl
          i32.add
          i32.load
          i32.const 32
          i32.add
          local.tee $p0
          i32.load offset=4
          local.tee $p2
          i32.const 251658240
          i32.and
          i32.const 16777216
          i32.ne
          br_if $B7
          local.get $p0
          local.get $l8
          i32.store
          local.get $p0
          local.get $p2
          i32.const 1073741823
          i32.and
          local.get $l9
          i32.or
          i32.store offset=4
        end
        local.get $l10
        i32.load offset=284
        local.tee $p0
        i32.const 0
        i32.lt_s
        br_if $B0
        local.get $p0
        i32.const 2147483647
        i32.and
        i32.eqz
        br_if $B0
        local.get $l10
        i32.load offset=276
        local.tee $p0
        local.get $l10
        i32.const 16
        i32.add
        i32.eq
        br_if $B0
        local.get $p0
        i32.eqz
        br_if $B0
        call $f69753
        local.tee $p2
        local.get $p0
        local.get $p2
        i32.load
        i32.load offset=12
        call_indirect $__indirect_function_table (type $t1)
        br $B0
      end
      global.get $g0
      i32.const 288
      i32.sub
      local.tee $l7
      global.set $g0
      local.get $p1
      local.tee $p2
      local.get $p0
      i32.store
      local.get $p1
      i32.load offset=4
      local.set $l6
      block $B12
        local.get $p0
        i32.load8_u offset=4785
        i32.eqz
        if $I13
          local.get $p2
          local.get $l6
          i32.const 268435455
          i32.and
          i32.const -2147483648
          i32.or
          i32.store offset=4
          local.get $l7
          i32.const 1
          i32.store8 offset=272
          local.get $l7
          i64.const 274877906944
          i64.store offset=280
          local.get $l7
          local.get $l7
          i32.const 16
          i32.add
          i32.store offset=276
          local.get $p2
          i32.const 16
          i32.add
          call $f71725
          drop
          i32.const 0
          local.set $p0
          block $B14
            local.get $p2
            local.get $l7
            i32.const 12
            i32.add
            i32.const 0
            call $f72634
            local.tee $l5
            i32.eqz
            br_if $B14
            local.get $p2
            i32.load
            local.set $l9
            local.get $l5
            i32.const 1
            i32.and
            local.set $l8
            local.get $l5
            i32.const 1
            i32.ne
            if $I15
              local.get $l5
              i32.const -2
              i32.and
              local.set $p2
              loop $L16
                local.get $p0
                i32.const 2
                i32.shl
                local.tee $l5
                local.get $l7
                i32.load offset=12
                i32.add
                i32.load
                i32.const 32
                i32.add
                local.tee $l6
                i32.load offset=4
                local.tee $p4
                i32.const 251658240
                i32.and
                i32.const 16777216
                i32.eq
                if $I17
                  local.get $l6
                  local.get $l9
                  i32.store
                  local.get $l6
                  local.get $p4
                  i32.const 1073741823
                  i32.and
                  i32.const -2147483648
                  i32.or
                  i32.store offset=4
                end
                local.get $l7
                i32.load offset=12
                local.get $l5
                i32.const 4
                i32.or
                i32.add
                i32.load
                i32.const 32
                i32.add
                local.tee $l5
                i32.load offset=4
                local.tee $l6
                i32.const 251658240
                i32.and
                i32.const 16777216
                i32.eq
                if $I18
                  local.get $l5
                  local.get $l9
                  i32.store
                  local.get $l5
                  local.get $l6
                  i32.const 1073741823
                  i32.and
                  i32.const -2147483648
                  i32.or
                  i32.store offset=4
                end
                local.get $p0
                i32.const 2
                i32.add
                local.set $p0
                local.get $p2
                i32.const 2
                i32.sub
                local.tee $p2
                br_if $L16
              end
            end
            local.get $l8
            i32.eqz
            br_if $B14
            local.get $l7
            i32.load offset=12
            local.get $p0
            i32.const 2
            i32.shl
            i32.add
            i32.load
            i32.const 32
            i32.add
            local.tee $p0
            i32.load offset=4
            local.tee $l6
            i32.const 251658240
            i32.and
            i32.const 16777216
            i32.ne
            br_if $B14
            local.get $p0
            local.get $l9
            i32.store
            local.get $p0
            local.get $l6
            i32.const 1073741823
            i32.and
            i32.const -2147483648
            i32.or
            i32.store offset=4
          end
          local.get $l7
          i32.load offset=284
          local.tee $p0
          i32.const 0
          i32.lt_s
          br_if $B12
          local.get $p0
          i32.const 2147483647
          i32.and
          i32.eqz
          br_if $B12
          local.get $l7
          i32.load offset=276
          local.tee $p0
          local.get $l7
          i32.const 16
          i32.add
          i32.eq
          br_if $B12
          local.get $p0
          i32.eqz
          br_if $B12
          call $f69753
          local.tee $l6
          local.get $p0
          local.get $l6
          i32.load
          i32.load offset=12
          call_indirect $__indirect_function_table (type $t1)
          br $B12
        end
        local.get $l6
        i32.const 1073741823
        i32.and
        local.set $p0
        block $B19
          local.get $l6
          i32.const -1073741824
          i32.ge_u
          if $I20
            local.get $p2
            local.get $p0
            i32.const -2147483648
            i32.or
            i32.store offset=4
            local.get $l6
            i32.const 268435456
            i32.and
            br_if $B19
            local.get $l5
            local.get $p2
            call $f71988
            br $B19
          end
          local.get $p2
          local.get $p0
          i32.const 1073741824
          i32.or
          i32.store offset=4
          local.get $l7
          local.get $p2
          i32.store offset=16
          local.get $l5
          local.get $l7
          i32.const 16
          i32.add
          local.get $l7
          i32.const 12
          i32.add
          call $f71989
          local.set $p0
          local.get $l7
          i32.load8_u offset=12
          br_if $B19
          local.get $p0
          local.get $l7
          i32.load offset=16
          i32.store
        end
        local.get $l7
        i32.const 1
        i32.store8 offset=272
        local.get $l7
        i64.const 274877906944
        i64.store offset=280
        local.get $l7
        local.get $l7
        i32.const 16
        i32.add
        i32.store offset=276
        i32.const 0
        local.set $p0
        block $B21
          local.get $p2
          local.get $l7
          i32.const 12
          i32.add
          i32.const 0
          call $f72634
          local.tee $l5
          i32.eqz
          br_if $B21
          local.get $p2
          i32.load offset=4
          i32.const -1073741824
          i32.and
          local.set $l9
          local.get $p2
          i32.load
          local.set $l8
          local.get $l5
          i32.const 1
          i32.and
          local.set $p3
          local.get $l5
          i32.const 1
          i32.ne
          if $I22
            local.get $l5
            i32.const -2
            i32.and
            local.set $p2
            loop $L23
              local.get $p0
              i32.const 2
              i32.shl
              local.tee $l5
              local.get $l7
              i32.load offset=12
              i32.add
              i32.load
              i32.const 32
              i32.add
              local.tee $l6
              i32.load offset=4
              local.tee $p4
              i32.const 251658240
              i32.and
              i32.const 16777216
              i32.eq
              if $I24
                local.get $l6
                local.get $l8
                i32.store
                local.get $l6
                local.get $p4
                i32.const 1073741823
                i32.and
                local.get $l9
                i32.or
                i32.store offset=4
              end
              local.get $l7
              i32.load offset=12
              local.get $l5
              i32.const 4
              i32.or
              i32.add
              i32.load
              i32.const 32
              i32.add
              local.tee $l5
              i32.load offset=4
              local.tee $l6
              i32.const 251658240
              i32.and
              i32.const 16777216
              i32.eq
              if $I25
                local.get $l5
                local.get $l8
                i32.store
                local.get $l5
                local.get $l6
                i32.const 1073741823
                i32.and
                local.get $l9
                i32.or
                i32.store offset=4
              end
              local.get $p0
              i32.const 2
              i32.add
              local.set $p0
              local.get $p2
              i32.const 2
              i32.sub
              local.tee $p2
              br_if $L23
            end
          end
          local.get $p3
          i32.eqz
          br_if $B21
          local.get $l7
          i32.load offset=12
          local.get $p0
          i32.const 2
          i32.shl
          i32.add
          i32.load
          i32.const 32
          i32.add
          local.tee $p0
          i32.load offset=4
          local.tee $l6
          i32.const 251658240
          i32.and
          i32.const 16777216
          i32.ne
          br_if $B21
          local.get $p0
          local.get $l8
          i32.store
          local.get $p0
          local.get $l6
          i32.const 1073741823
          i32.and
          local.get $l9
          i32.or
          i32.store offset=4
        end
        local.get $l7
        i32.load offset=284
        local.tee $p0
        i32.const 0
        i32.lt_s
        br_if $B12
        local.get $p0
        i32.const 2147483647
        i32.and
        i32.eqz
        br_if $B12
        local.get $l7
        i32.load offset=276
        local.tee $p0
        local.get $l7
        i32.const 16
        i32.add
        i32.eq
        br_if $B12
        local.get $p0
        i32.eqz
        br_if $B12
        call $f69753
        local.tee $l6
        local.get $p0
        local.get $l6
        i32.load
        i32.load offset=12
        call_indirect $__indirect_function_table (type $t1)
      end
      local.get $l7
      i32.const 288
      i32.add
      global.set $g0
      local.get $p1
      block $B26 (result i32)
        block $B27
          local.get $p1
          f32.load offset=260
          f32.const 0x0p+0 (;=0;)
          f32.ne
          br_if $B27
          local.get $p1
          f32.load offset=236
          f32.const 0x0p+0 (;=0;)
          f32.ne
          br_if $B27
          local.get $p1
          f32.load offset=240
          f32.const 0x0p+0 (;=0;)
          f32.ne
          br_if $B27
          local.get $p1
          f32.load offset=244
          f32.const 0x0p+0 (;=0;)
          f32.ne
          br_if $B27
          local.get $p1
          f32.load offset=248
          f32.const 0x0p+0 (;=0;)
          f32.ne
          br_if $B27
          local.get $p1
          f32.load offset=252
          f32.const 0x0p+0 (;=0;)
          f32.ne
          br_if $B27
          i32.const 1
          local.get $p1
          f32.load offset=256
          f32.const 0x0p+0 (;=0;)
          f32.eq
          br_if $B26
          drop
        end
        i32.const 0
      end
      i32.store offset=264
    end
    local.get $l10
    i32.const 288
    i32.add
    global.set $g0)