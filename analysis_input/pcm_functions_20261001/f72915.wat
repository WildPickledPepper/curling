  (func $f72915 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i64) (local $l16 i64) (local $l17 f32) (local $l18 f32)
    block $B0
      local.get $p0
      i32.load offset=36
      if $I1
        block $B2
          local.get $p0
          i32.load offset=36
          local.tee $l4
          i32.load offset=16
          local.tee $l12
          i32.const 2
          i32.shl
          local.tee $l2
          local.get $l4
          i32.load offset=28
          local.tee $l13
          i32.const 20
          i32.mul
          local.tee $l3
          i32.add
          local.get $l4
          i32.load offset=4
          local.tee $l10
          i32.const 12
          i32.mul
          local.tee $l5
          i32.add
          i32.const 12
          i32.add
          local.tee $l7
          i32.eqz
          if $I3
            i32.const 0
            local.set $l7
            br $B2
          end
          call $f69753
          local.tee $l4
          local.get $l7
          i32.const 3217836
          i32.const 3217483
          i32.const 2527
          local.get $l4
          i32.load
          i32.load offset=8
          call_indirect $__indirect_function_table (type $t9)
          local.set $l7
          local.get $p0
          i32.load offset=36
          local.set $l4
        end
        local.get $p0
        local.get $l7
        i32.store offset=40
        local.get $l2
        local.get $l7
        i32.add
        local.tee $l11
        local.get $l3
        i32.add
        local.get $l4
        i32.load
        local.get $l5
        call $f483
        local.set $l14
        local.get $p0
        i32.load offset=36
        local.tee $l8
        i32.load offset=16
        local.tee $l5
        if $I4
          i32.const 0
          local.set $l4
          loop $L5
            i32.const 1
            local.set $l2
            block $B6
              local.get $l4
              i32.const 1
              i32.add
              local.tee $l3
              local.get $l5
              i32.ge_u
              br_if $B6
              local.get $l5
              local.get $l4
              i32.sub
              local.set $l6
              local.get $l8
              i32.load offset=12
              local.tee $l5
              local.get $l4
              i32.const 2
              i32.shl
              i32.add
              i32.load8_u offset=3
              local.set $l8
              loop $L7
                local.get $l5
                local.get $l3
                i32.const 2
                i32.shl
                i32.add
                i32.load8_u offset=3
                local.get $l8
                i32.const 255
                i32.and
                i32.ne
                br_if $B6
                local.get $l2
                i32.const 1
                i32.add
                local.tee $l2
                local.get $l4
                i32.add
                local.set $l3
                local.get $l2
                local.get $l6
                i32.ne
                br_if $L7
              end
              local.get $l6
              local.set $l2
            end
            local.get $l11
            local.get $l9
            i32.const 20
            i32.mul
            i32.add
            local.tee $l3
            local.get $l4
            i32.store16 offset=18
            local.get $l3
            local.get $l2
            i32.store16 offset=16
            local.get $l3
            local.get $l9
            i32.const 4
            i32.shl
            local.tee $l5
            local.get $p0
            i32.load offset=36
            i32.load offset=24
            i32.add
            f32.load
            f32.store
            local.get $l3
            local.get $p0
            i32.load offset=36
            i32.load offset=24
            local.get $l5
            i32.add
            f32.load offset=4
            f32.store offset=4
            local.get $l3
            local.get $p0
            i32.load offset=36
            i32.load offset=24
            local.get $l5
            i32.add
            f32.load offset=8
            f32.store offset=8
            local.get $l3
            local.get $p0
            i32.load offset=36
            i32.load offset=24
            local.get $l5
            i32.add
            f32.load offset=12
            f32.store offset=12
            block $B8
              local.get $l2
              i32.eqz
              br_if $B8
              local.get $l2
              i32.const 1
              i32.and
              if $I9 (result i32)
                local.get $l7
                local.get $l4
                i32.const 2
                i32.shl
                local.tee $l3
                i32.add
                local.get $p0
                i32.load offset=36
                i32.load offset=12
                local.get $l3
                i32.add
                i32.load8_u offset=2
                i32.store
                local.get $l4
                i32.const 1
                i32.add
                local.set $l4
                local.get $l2
                i32.const 1
                i32.sub
              else
                local.get $l2
              end
              local.set $l3
              local.get $l2
              i32.const 1
              i32.eq
              br_if $B8
              loop $L10
                local.get $l7
                local.get $l4
                i32.const 2
                i32.shl
                local.tee $l2
                i32.add
                local.get $p0
                i32.load offset=36
                i32.load offset=12
                local.get $l2
                i32.add
                i32.load8_u offset=2
                i32.store
                local.get $l7
                local.get $l2
                i32.const 4
                i32.add
                local.tee $l2
                i32.add
                local.get $p0
                i32.load offset=36
                i32.load offset=12
                local.get $l2
                i32.add
                i32.load8_u offset=2
                i32.store
                local.get $l4
                i32.const 2
                i32.add
                local.set $l4
                local.get $l3
                i32.const 2
                i32.sub
                local.tee $l3
                br_if $L10
              end
            end
            local.get $l9
            i32.const 1
            i32.add
            local.set $l9
            local.get $l4
            local.get $p0
            i32.load offset=36
            local.tee $l8
            i32.load offset=16
            local.tee $l5
            i32.lt_u
            br_if $L5
          end
        end
        local.get $p1
        i32.const 4
        i32.store offset=24
        local.get $p1
        local.get $l10
        i32.store offset=8
        local.get $p1
        local.get $l14
        i32.store offset=4
        local.get $p1
        i32.const 12
        i32.store
        local.get $p1
        i32.const 20
        i32.store offset=12
        local.get $p1
        local.get $l7
        i32.store offset=28
        local.get $p1
        local.get $l12
        i32.store offset=32
        local.get $p1
        local.get $l13
        i32.store offset=20
        local.get $p1
        local.get $l11
        i32.store offset=16
        global.get $g0
        i32.const 16
        i32.sub
        local.tee $l10
        global.set $g0
        block $B11
          local.get $p1
          i32.load offset=20
          local.tee $l2
          i32.const 2
          i32.lt_u
          br_if $B11
          local.get $p1
          i32.load offset=16
          local.set $l6
          local.get $l2
          i32.const 1
          i32.sub
          local.tee $l3
          i32.const 3
          i32.and
          local.set $l4
          block $B12
            local.get $l2
            i32.const 2
            i32.sub
            i32.const 3
            i32.lt_u
            if $I13
              i32.const 1
              local.set $l2
              i32.const 0
              local.set $l3
              br $B12
            end
            local.get $l3
            i32.const -4
            i32.and
            local.set $l7
            i32.const 0
            local.set $l3
            i32.const 1
            local.set $l2
            loop $L14
              local.get $l2
              i32.const 3
              i32.add
              local.get $l2
              i32.const 2
              i32.add
              local.get $l2
              i32.const 1
              i32.add
              local.get $l2
              local.get $l3
              local.get $l6
              local.get $l3
              i32.const 20
              i32.mul
              i32.add
              i32.load16_u offset=16
              local.get $l6
              local.get $l2
              i32.const 20
              i32.mul
              i32.add
              local.tee $l5
              i32.load16_u offset=16
              i32.lt_u
              select
              local.tee $l3
              local.get $l6
              local.get $l3
              i32.const 20
              i32.mul
              i32.add
              i32.load16_u offset=16
              local.get $l5
              i32.load16_u offset=36
              i32.lt_u
              select
              local.tee $l3
              local.get $l6
              local.get $l3
              i32.const 20
              i32.mul
              i32.add
              i32.load16_u offset=16
              local.get $l5
              i32.load16_u offset=56
              i32.lt_u
              select
              local.tee $l3
              local.get $l6
              local.get $l3
              i32.const 20
              i32.mul
              i32.add
              i32.load16_u offset=16
              local.get $l5
              i32.load16_u offset=76
              i32.lt_u
              select
              local.set $l3
              local.get $l2
              i32.const 4
              i32.add
              local.set $l2
              local.get $l7
              i32.const 4
              i32.sub
              local.tee $l7
              br_if $L14
            end
          end
          local.get $l4
          if $I15
            loop $L16
              local.get $l2
              local.get $l3
              local.get $l6
              local.get $l3
              i32.const 20
              i32.mul
              i32.add
              i32.load16_u offset=16
              local.get $l6
              local.get $l2
              i32.const 20
              i32.mul
              i32.add
              i32.load16_u offset=16
              i32.lt_u
              select
              local.set $l3
              local.get $l2
              i32.const 1
              i32.add
              local.set $l2
              local.get $l4
              i32.const 1
              i32.sub
              local.tee $l4
              br_if $L16
            end
          end
          local.get $l3
          i32.eqz
          br_if $B11
          local.get $p1
          i32.load offset=28
          local.set $l9
          local.get $p0
          local.get $p1
          i32.load offset=32
          i32.const 2
          i32.shl
          local.tee $l2
          if $I17 (result i32)
            call $f69753
            local.tee $l5
            local.get $l2
            i32.const 3216437
            i32.const 3215482
            i32.const 313
            local.get $l5
            i32.load
            i32.load offset=8
            call_indirect $__indirect_function_table (type $t9)
          else
            i32.const 0
          end
          i32.store offset=12
          local.get $l10
          i32.const 8
          i32.add
          local.tee $l11
          local.get $l6
          i32.const 8
          i32.add
          local.tee $l12
          i64.load align=4
          i64.store
          local.get $l10
          local.get $l6
          i64.load align=4
          i64.store
          local.get $l6
          local.get $l3
          i32.const 20
          i32.mul
          i32.add
          local.tee $l4
          i32.load16_u offset=18
          local.set $l14
          local.get $l4
          i32.const 16
          i32.add
          local.tee $l5
          i32.load16_u
          local.set $l2
          local.get $l6
          i32.const 16
          i32.add
          local.tee $l8
          i32.load16_u
          local.set $l13
          local.get $l6
          i32.load16_u offset=18
          local.set $l7
          local.get $l8
          local.get $l5
          i32.load
          i32.store
          local.get $l12
          local.get $l4
          i32.const 8
          i32.add
          local.tee $l8
          i64.load align=4
          i64.store align=4
          local.get $l6
          local.get $l4
          i64.load align=4
          i64.store align=4
          local.get $l11
          i64.load
          local.set $l15
          local.get $l10
          i64.load
          local.set $l16
          local.get $l4
          local.get $l7
          i32.store16 offset=18
          local.get $l5
          local.get $l13
          i32.store16
          local.get $l8
          local.get $l15
          i64.store align=4
          local.get $l4
          local.get $l16
          i64.store align=4
          block $B18
            local.get $p1
            i32.load offset=20
            i32.eqz
            br_if $B18
            local.get $p0
            i32.load offset=12
            local.get $l9
            local.get $l14
            i32.const 2
            i32.shl
            i32.add
            local.get $l2
            i32.const 2
            i32.shl
            call $f483
            drop
            local.get $l6
            i32.const 0
            i32.store16 offset=18
            i32.const 1
            local.set $l5
            local.get $p1
            i32.load offset=20
            i32.const 1
            i32.le_u
            br_if $B18
            local.get $l4
            i32.const 18
            i32.add
            local.set $l11
            local.get $l13
            i32.const 2
            i32.shl
            local.set $l12
            local.get $l9
            local.get $l7
            i32.const 2
            i32.shl
            i32.add
            local.set $l8
            loop $L19
              local.get $p0
              i32.load offset=12
              local.get $l2
              i32.const 65535
              i32.and
              i32.const 2
              i32.shl
              i32.add
              local.set $l4
              block $B20 (result i32)
                local.get $l3
                local.get $l5
                i32.eq
                if $I21
                  local.get $l4
                  local.get $l8
                  local.get $l12
                  call $f483
                  drop
                  local.get $l11
                  local.get $l2
                  i32.store16
                  local.get $l13
                  br $B20
                end
                local.get $l4
                local.get $l9
                local.get $l6
                local.get $l5
                i32.const 20
                i32.mul
                i32.add
                local.tee $l7
                i32.load16_u offset=18
                i32.const 2
                i32.shl
                i32.add
                local.get $l7
                i32.load16_u offset=16
                i32.const 2
                i32.shl
                call $f483
                drop
                local.get $l7
                local.get $l2
                i32.store16 offset=18
                local.get $l7
                i32.load16_u offset=16
              end
              local.get $l2
              i32.add
              local.set $l2
              local.get $l5
              i32.const 1
              i32.add
              local.tee $l5
              local.get $p1
              i32.load offset=20
              i32.lt_u
              br_if $L19
            end
          end
          local.get $p1
          local.get $p0
          i32.load offset=12
          i32.store offset=28
        end
        local.get $l10
        i32.const 16
        i32.add
        global.set $g0
        br $B0
      end
      local.get $p0
      local.get $p1
      call $f72913
    end
    local.get $p0
    i32.load offset=4
    i32.load8_u offset=37
    i32.const 1
    i32.and
    if $I22
      i32.const 0
      local.set $l3
      local.get $p1
      i32.load offset=8
      if $I23
        local.get $p1
        i32.load offset=4
        local.set $l6
        loop $L24
          local.get $p0
          f32.load offset=16
          local.set $l17
          local.get $p0
          f32.load offset=20
          local.set $l18
          local.get $l6
          local.get $l3
          i32.const 12
          i32.mul
          i32.add
          local.tee $l2
          local.get $l2
          f32.load offset=8
          local.get $p0
          f32.load offset=24
          f32.add
          f32.store offset=8
          local.get $l2
          local.get $l18
          local.get $l2
          f32.load offset=4
          f32.add
          f32.store offset=4
          local.get $l2
          local.get $l17
          local.get $l2
          f32.load
          f32.add
          f32.store
          local.get $l3
          i32.const 1
          i32.add
          local.tee $l3
          local.get $p1
          i32.load offset=8
          i32.lt_u
          br_if $L24
        end
      end
      local.get $p1
      i32.load offset=20
      if $I25
        local.get $p1
        i32.load offset=16
        local.set $l6
        i32.const 0
        local.set $l3
        loop $L26
          local.get $l6
          local.get $l3
          i32.const 20
          i32.mul
          i32.add
          local.tee $l2
          local.get $l2
          f32.load offset=12
          local.get $l2
          f32.load
          local.get $p0
          f32.load offset=16
          f32.mul
          local.get $l2
          f32.load offset=4
          local.get $p0
          f32.load offset=20
          f32.mul
          f32.add
          local.get $l2
          f32.load offset=8
          local.get $p0
          f32.load offset=24
          f32.mul
          f32.add
          f32.sub
          f32.store offset=12
          local.get $l3
          i32.const 1
          i32.add
          local.tee $l3
          local.get $p1
          i32.load offset=20
          i32.lt_u
          br_if $L26
        end
      end
    end)
