  (func $f71614 (type $t2) (param $p0 i32) (param $p1 i32) (param $p2 i32)
    (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i64)
    block $B0
      local.get $p2
      i32.load16_u
      local.tee $l3
      local.get $p0
      i32.load16_u offset=44
      local.tee $l10
      i32.eq
      br_if $B0
      local.get $p0
      local.get $l3
      i32.store16 offset=44
      local.get $l3
      i32.const 1
      i32.and
      local.tee $l3
      local.get $l10
      i32.const 1
      i32.and
      local.tee $l7
      i32.eqz
      i32.and
      local.set $l11
      block $B1
        local.get $p0
        i32.load
        local.tee $l5
        i32.eqz
        br_if $B1
        local.get $p2
        i32.load16_u
        i32.const 16
        i32.and
        local.tee $l9
        local.get $l10
        i32.const 16
        i32.and
        i32.ne
        if $I2
          global.get $g0
          i32.const 16
          i32.sub
          local.tee $l6
          global.set $g0
          block $B3
            local.get $l5
            local.tee $l4
            i32.load offset=156
            i32.const -3
            i32.gt_u
            br_if $B3
            local.get $l4
            i32.load offset=40
            local.set $l8
            local.get $l9
            i32.const 16
            i32.and
            if $I4
              local.get $l6
              local.get $l4
              i32.store offset=8
              local.get $l8
              i32.const 4624
              i32.add
              local.get $l6
              i32.const 8
              i32.add
              local.get $l6
              i32.const 15
              i32.add
              call $f71568
              local.set $l4
              local.get $l6
              i32.load8_u offset=15
              br_if $B3
              local.get $l4
              local.get $l6
              i32.load offset=8
              i32.store
              br $B3
            end
            local.get $l8
            local.get $l4
            call $f71569
          end
          local.get $l6
          i32.const 16
          i32.add
          global.set $g0
        end
        block $B5
          local.get $l11
          if $I6
            local.get $p0
            i32.load offset=176
            local.tee $l3
            i32.eqz
            if $I7
              local.get $p1
              i32.load offset=288
              local.tee $l3
              i32.eqz
              if $I8
                local.get $p1
                call $f71601
                local.get $p1
                i32.load offset=288
                local.set $l3
              end
              local.get $p1
              local.get $l3
              i32.load
              i32.store offset=288
              local.get $p1
              local.get $p1
              i32.load offset=280
              i32.const 1
              i32.add
              i32.store offset=280
            end
            local.get $l3
            i64.const 0
            i64.store offset=24 align=1
            local.get $l3
            i64.const 0
            i64.store align=1
            local.get $l3
            i32.const 56
            i32.add
            local.tee $p1
            i64.const 0
            i64.store align=1
            local.get $l3
            i32.const 48
            i32.add
            local.tee $l7
            i64.const 0
            i64.store align=1
            local.get $l3
            i32.const 40
            i32.add
            local.tee $l9
            i64.const 0
            i64.store align=1
            local.get $l3
            i32.const 32
            i32.add
            local.tee $l8
            i64.const 0
            i64.store align=1
            local.get $l3
            i64.const 0
            i64.store offset=16 align=1
            local.get $l3
            i64.const 0
            i64.store offset=8 align=1
            local.get $l3
            i32.const 1
            i32.store8 offset=31
            local.get $l3
            i32.const 0
            i32.store8 offset=28
            local.get $l7
            local.get $p0
            i32.const 120
            i32.add
            local.tee $l4
            f32.load
            f32.store
            local.get $l3
            local.get $p0
            f32.load offset=124
            f32.store offset=52
            local.get $l8
            local.get $p0
            i32.const 128
            i32.add
            local.tee $l7
            f32.load
            f32.store
            local.get $l3
            local.get $p0
            f32.load offset=132
            f32.store offset=36
            local.get $l9
            local.get $p0
            i32.const 136
            i32.add
            local.tee $l8
            f32.load
            f32.store
            local.get $l3
            local.get $p0
            f32.load offset=140
            f32.store offset=44
            local.get $p1
            local.get $p0
            i32.const 112
            i32.add
            local.tee $l9
            f32.load
            f32.store
            local.get $l3
            local.get $p0
            f32.load offset=116
            f32.store offset=60
            local.get $l8
            i64.const 0
            i64.store
            local.get $l7
            i64.const 0
            i64.store
            local.get $l4
            i64.const 0
            i64.store
            local.get $p0
            local.get $l3
            i32.store offset=176
            local.get $l9
            i64.const 9187343237679939583
            i64.store
            local.get $l5
            local.tee $p1
            i32.load offset=156
            i32.const -3
            i32.le_u
            if $I9
              local.get $p1
              i32.load offset=40
              local.get $p1
              call $f71382
            end
            local.get $p1
            i32.load offset=168
            local.tee $l4
            if $I10
              local.get $l4
              local.get $p1
              i32.load offset=40
              i32.load offset=1136
              call $f71364
            end
            local.get $p1
            i32.const 5
            i32.const 4
            call $f71326
            local.get $p1
            i32.load offset=40
            i32.load offset=1000
            local.tee $l4
            i32.const 168
            i32.add
            local.get $p1
            i64.load offset=144
            local.tee $l12
            call $f70673
            local.get $l4
            i32.const 640
            i32.add
            local.get $l12
            call $f70673
            local.get $p1
            i32.load offset=32
            local.tee $p1
            if $I11
              loop $L12
                local.get $p1
                call $f71459
                local.get $p1
                i32.load
                local.tee $p1
                br_if $L12
              end
            end
            br $B5
          end
          local.get $l7
          local.get $l3
          i32.eqz
          i32.and
          i32.eqz
          br_if $B5
          local.get $p0
          i32.load offset=176
          local.tee $l3
          if $I13
            local.get $p0
            local.get $l3
            f32.load offset=44
            f32.store offset=140
            local.get $p0
            local.get $l3
            f32.load offset=32
            f32.store offset=128
            local.get $p0
            local.get $l3
            f32.load offset=36
            f32.store offset=132
            local.get $p0
            local.get $l3
            f32.load offset=40
            f32.store offset=136
            local.get $p0
            local.get $l3
            f32.load offset=48
            f32.store offset=120
            local.get $p0
            local.get $l3
            f32.load offset=52
            f32.store offset=124
            local.get $p0
            local.get $l3
            f32.load offset=56
            f32.store offset=112
            local.get $p0
            local.get $l3
            f32.load offset=60
            f32.store offset=116
            local.get $p1
            local.get $p1
            i32.load offset=280
            i32.const 1
            i32.sub
            i32.store offset=280
            local.get $l3
            local.get $p1
            i32.load offset=288
            i32.store
            local.get $p1
            local.get $l3
            i32.store offset=288
            local.get $p0
            i32.const 0
            i32.store offset=176
          end
          local.get $l5
          local.tee $p1
          i32.load offset=40
          i32.load offset=1000
          local.tee $l4
          i32.const 168
          i32.add
          local.get $p1
          i64.load offset=144
          local.tee $l12
          call $f70674
          local.get $l4
          i32.const 640
          i32.add
          local.get $l12
          call $f70674
          local.get $p1
          i32.load offset=44
          local.tee $l3
          i32.load offset=176
          local.set $l4
          block $B14
            local.get $p1
            i32.load offset=100
            i32.load8_u offset=28
            i32.const 128
            i32.and
            i32.eqz
            if $I15
              block $B16
                local.get $l4
                i32.eqz
                br_if $B16
                local.get $l3
                i32.const 0
                call $f71621
                i32.eqz
                br_if $B16
                local.get $l3
                i32.load offset=176
                local.tee $l4
                i32.eqz
                br_if $B16
                local.get $l4
                i32.const 0
                i32.store offset=56
                local.get $l4
                i64.const 0
                i64.store offset=48 align=4
                local.get $l4
                i32.const 0
                i32.store offset=40
                local.get $l4
                i64.const 0
                i64.store offset=32 align=4
                local.get $l4
                i32.const 0
                i32.store offset=24
                local.get $l4
                i64.const 0
                i64.store offset=16 align=4
                local.get $l4
                i32.const 0
                i32.store offset=8
                local.get $l4
                i64.const 0
                i64.store align=4
              end
              local.get $p1
              i32.const 1
              i32.store8 offset=154
              br $B14
            end
            block $B17
              local.get $l4
              i32.eqz
              br_if $B17
              local.get $l3
              i32.const 0
              call $f71621
              i32.eqz
              br_if $B17
              local.get $l3
              i32.load offset=176
              local.tee $l4
              i32.eqz
              br_if $B17
              local.get $l4
              i32.const 0
              i32.store offset=56
              local.get $l4
              i64.const 0
              i64.store offset=48 align=4
              local.get $l4
              i32.const 0
              i32.store offset=40
              local.get $l4
              i64.const 0
              i64.store offset=32 align=4
            end
            local.get $p1
            local.get $p1
            i32.load8_u offset=154
            i32.const 251
            i32.and
            i32.store8 offset=154
          end
          local.get $p1
          i32.load offset=168
          local.tee $l4
          if $I18
            local.get $l4
            local.get $p1
            i32.load offset=40
            i32.load offset=1136
            call $f71364
          end
          local.get $p1
          i32.const 5
          i32.const 6
          call $f71326
          local.get $p1
          local.get $p1
          i32.load16_u offset=152
          i32.const 63995
          i32.and
          i32.store16 offset=152
          local.get $p1
          i32.load offset=156
          i32.const -3
          i32.le_u
          if $I19
            local.get $p1
            i32.load offset=40
            local.get $p1
            call $f71382
          end
          local.get $p1
          i32.load offset=32
          local.tee $p1
          if $I20
            loop $L21
              local.get $p1
              call $f71459
              local.get $p1
              i32.load
              local.tee $p1
              br_if $L21
            end
          end
        end
        local.get $l10
        i32.const 32
        i32.and
        local.tee $l3
        local.get $p2
        i32.load16_u
        i32.const 32
        i32.and
        i32.eq
        br_if $B1
        local.get $l3
        if $I22
          local.get $l5
          i64.load offset=144
          local.tee $l12
          i64.const 9
          i64.shr_u
          i32.wrap_i64
          local.set $l3
          local.get $l5
          i32.load offset=40
          local.set $p1
          block $B23
            block $B24 (result i32)
              local.get $l5
              i32.load offset=44
              i32.load8_u offset=9
              i32.const 2
              i32.eq
              if $I25
                local.get $p1
                i32.const 4732
                i32.add
                i32.load
                i32.const 5
                i32.shl
                local.get $l3
                i32.le_u
                br_if $B23
                local.get $p1
                i32.const 4728
                i32.add
                br $B24
              end
              local.get $p1
              i32.const 4720
              i32.add
              i32.load
              i32.const 5
              i32.shl
              local.get $l3
              i32.le_u
              br_if $B23
              local.get $p1
              i32.const 4716
              i32.add
            end
            i32.load
            local.get $l12
            i64.const 14
            i64.shr_u
            i32.wrap_i64
            i32.const 134217727
            i32.and
            i32.const 2
            i32.shl
            i32.add
            local.tee $p1
            local.get $p1
            i32.load
            i32.const -2
            local.get $l3
            i32.rotl
            i32.and
            i32.store
          end
          local.get $l5
          i32.const 92
          i32.add
          local.tee $l3
          local.get $l3
          i32.load16_u
          i32.const 65471
          i32.and
          i32.store16
          br $B1
        end
        local.get $l11
        i32.eqz
        if $I26
          block $B27
            local.get $l5
            i64.load offset=144
            i64.const 9
            i64.shr_u
            i32.wrap_i64
            local.tee $p1
            i32.const 32
            i32.add
            i32.const 5
            i32.shr_u
            local.tee $l4
            local.get $l5
            i32.load offset=40
            local.tee $l3
            i32.const 4728
            i32.add
            local.get $l3
            i32.const 4716
            i32.add
            local.get $l5
            i32.load offset=44
            i32.load8_u offset=9
            i32.const 2
            i32.eq
            select
            local.tee $l6
            i32.load offset=4
            i32.const 2147483647
            i32.and
            i32.le_u
            if $I28
              local.get $l6
              i32.load
              local.set $l7
              br $B27
            end
            call $f69753
            local.tee $l7
            local.get $l4
            i32.const 2
            i32.shl
            i32.const 3171275
            i32.const 3171240
            i32.const 438
            local.get $l7
            i32.load
            i32.load offset=8
            call_indirect $__indirect_function_table (type $t9)
            local.set $l7
            block $B29
              local.get $l6
              i32.load
              local.tee $l8
              i32.eqz
              br_if $B29
              local.get $l7
              local.get $l8
              local.get $l6
              i32.load offset=4
              i32.const 2
              i32.shl
              call $f483
              drop
              local.get $l6
              i32.load offset=4
              i32.const 0
              i32.lt_s
              br_if $B29
              local.get $l6
              i32.load
              local.tee $l8
              i32.eqz
              br_if $B29
              call $f69753
              local.tee $l9
              local.get $l8
              local.get $l9
              i32.load
              i32.load offset=12
              call_indirect $__indirect_function_table (type $t1)
            end
            local.get $l7
            local.get $l6
            i32.load offset=4
            local.tee $l8
            i32.const 2
            i32.shl
            i32.add
            i32.const 0
            local.get $l4
            local.get $l8
            i32.sub
            i32.const 2
            i32.shl
            call $f484
            drop
            local.get $l6
            local.get $l4
            i32.store offset=4
            local.get $l6
            local.get $l7
            i32.store
          end
          local.get $l7
          local.get $p1
          i32.const 3
          i32.shr_u
          i32.const 536870908
          i32.and
          i32.add
          local.tee $l6
          local.get $l6
          i32.load
          i32.const 1
          local.get $p1
          i32.shl
          i32.or
          i32.store
        end
        local.get $l5
        i32.const 92
        i32.add
        local.tee $l3
        local.get $l3
        i32.load16_u
        i32.const 64
        i32.or
        i32.store16
      end
      local.get $l11
      if $I30
        local.get $p0
        call $f71615
      end
      local.get $l5
      i32.eqz
      br_if $B0
      local.get $p2
      i32.load16_u
      i32.const 3
      i32.and
      local.set $p0
      block $B31
        local.get $l10
        i32.const 3
        i32.and
        local.tee $p2
        i32.const 3
        i32.eq
        br_if $B31
        local.get $p0
        i32.const 3
        i32.ne
        br_if $B31
        local.get $l5
        i32.load offset=32
        local.tee $l5
        if $I32
          loop $L33
            local.get $l5
            call $f71456
            local.get $l5
            i32.load
            local.tee $l5
            br_if $L33
          end
        end
        return
      end
      local.get $p0
      i32.const 3
      i32.eq
      br_if $B0
      local.get $p2
      i32.const 3
      i32.ne
      br_if $B0
      local.get $l5
      call $f71570
    end)
