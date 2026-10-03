  (func $f71770 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 i32) (local $l17 i32) (local $l18 i32) (local $l19 i32) (local $l20 i32) (local $l21 i64) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32)
    global.get $g0
    i32.const 32
    i32.sub
    local.tee $l11
    global.set $g0
    block $B0
      local.get $p0
      i32.load offset=4
      local.tee $l4
      i32.eqz
      br_if $B0
      local.get $p1
      i32.load offset=8
      local.set $l2
      local.get $p0
      i32.load offset=284
      local.set $l5
      local.get $p1
      i32.load offset=12
      local.set $l3
      local.get $l11
      local.get $p1
      i64.load align=4
      i64.store offset=8
      local.get $l11
      local.get $l5
      local.get $l2
      i32.sub
      i32.store offset=24
      local.get $l11
      local.get $l3
      i32.store offset=20
      local.get $l11
      local.get $l2
      i32.store offset=16
      local.get $p0
      i32.load8_u offset=336
      i32.eqz
      if $I1
        block $B2
          local.get $l4
          i32.load offset=4
          local.tee $l2
          local.get $l11
          i32.const 8
          i32.add
          local.tee $l3
          i32.load offset=8
          i32.add
          i32.const 2
          i32.shl
          local.tee $l5
          i32.eqz
          if $I3
            i32.const 0
            local.set $l5
            br $B2
          end
          call $f69753
          local.tee $l2
          local.get $l5
          i32.const 3176237
          i32.const 3175524
          i32.const 840
          local.get $l2
          i32.load
          i32.load offset=8
          call_indirect $__indirect_function_table (type $t9)
          local.set $l5
          local.get $l4
          i32.load offset=4
          local.set $l2
        end
        local.get $l5
        local.get $l4
        i32.load
        local.get $l2
        i32.const 2
        i32.shl
        call $f483
        local.set $l2
        local.get $l4
        i32.load
        local.tee $l5
        if $I4
          call $f69753
          local.tee $p1
          local.get $l5
          local.get $p1
          i32.load
          i32.load offset=12
          call_indirect $__indirect_function_table (type $t1)
        end
        local.get $l4
        local.get $l2
        i32.store
        local.get $l4
        local.get $l4
        i32.load offset=44
        local.get $l3
        i32.load offset=8
        i32.add
        i32.store offset=44
        block $B5
          local.get $l3
          i32.load offset=8
          i32.eqz
          br_if $B5
          local.get $l2
          local.get $l4
          i32.load offset=4
          i32.const 2
          i32.shl
          i32.add
          local.get $l3
          i32.load offset=12
          i32.load
          local.get $l3
          i32.load offset=16
          i32.add
          i32.store
          i32.const 1
          local.set $l2
          local.get $l3
          i32.load offset=8
          i32.const 1
          i32.le_u
          br_if $B5
          loop $L6
            local.get $l4
            i32.load
            local.get $l4
            i32.load offset=4
            local.get $l2
            i32.add
            i32.const 2
            i32.shl
            i32.add
            local.get $l3
            i32.load offset=12
            local.get $l2
            i32.const 2
            i32.shl
            i32.add
            i32.load
            local.get $l3
            i32.load offset=16
            i32.add
            i32.store
            local.get $l2
            i32.const 1
            i32.add
            local.tee $l2
            local.get $l3
            i32.load offset=8
            i32.lt_u
            br_if $L6
          end
        end
        local.get $l4
        i32.load offset=40
        local.get $l3
        i32.load
        i32.add
        i32.const 1
        i32.add
        local.tee $l2
        i32.const 5
        i32.shr_u
        local.get $l2
        i32.const 31
        i32.and
        i32.const 0
        i32.ne
        i32.add
        local.tee $l2
        local.get $l4
        i32.load offset=56
        i32.gt_u
        if $I7
          call $f69753
          local.tee $l5
          local.get $l2
          i32.const 2
          i32.shl
          i32.const 3176237
          i32.const 3175524
          i32.const 337
          local.get $l5
          i32.load
          i32.load offset=8
          call_indirect $__indirect_function_table (type $t9)
          local.tee $l5
          local.get $l4
          i32.load offset=56
          local.tee $p1
          i32.const 2
          i32.shl
          i32.add
          i32.const 0
          local.get $l2
          local.get $p1
          i32.sub
          i32.const 2
          i32.shl
          call $f484
          drop
          local.get $l5
          local.get $l4
          i32.load offset=52
          local.get $l4
          i32.load offset=56
          i32.const 2
          i32.shl
          call $f483
          local.set $l5
          local.get $l4
          i32.load offset=52
          local.tee $p1
          if $I8
            call $f69753
            local.tee $p0
            local.get $p1
            local.get $p0
            i32.load
            i32.load offset=12
            call_indirect $__indirect_function_table (type $t1)
          end
          local.get $l4
          local.get $l2
          i32.store offset=56
          local.get $l4
          local.get $l5
          i32.store offset=52
        end
        local.get $l4
        i32.load offset=36
        i32.eqz
        if $I9
          block $B10
            local.get $l4
            i32.load offset=40
            local.tee $p1
            i32.const 2
            i32.shl
            local.tee $l2
            i32.eqz
            if $I11
              i32.const 0
              local.set $l2
              br $B10
            end
            call $f69753
            local.tee $l5
            local.get $l2
            i32.const 3176237
            i32.const 3175524
            i32.const 859
            local.get $l5
            i32.load
            i32.load offset=8
            call_indirect $__indirect_function_table (type $t9)
            local.set $l2
            local.get $l4
            i32.load offset=40
            local.set $p1
          end
          local.get $l4
          local.get $l2
          i32.store offset=36
          local.get $p1
          local.get $l2
          local.get $l4
          i32.load offset=8
          local.tee $l5
          local.get $l5
          local.get $l5
          call $f71748
        end
        block $B12
          block $B13
            local.get $l4
            i32.load offset=8
            local.tee $l2
            f32.load
            local.get $l3
            i32.load offset=4
            local.tee $l5
            f32.load
            f32.gt
            br_if $B13
            local.get $l2
            f32.load offset=4
            local.get $l5
            f32.load offset=4
            f32.gt
            br_if $B13
            local.get $l2
            f32.load offset=8
            local.get $l5
            f32.load offset=8
            f32.gt
            br_if $B13
            local.get $l2
            f32.load offset=12
            local.get $l5
            f32.load offset=12
            f32.lt
            br_if $B13
            local.get $l2
            f32.load offset=16
            local.get $l5
            f32.load offset=16
            f32.lt
            br_if $B13
            local.get $l2
            f32.load offset=20
            local.get $l5
            f32.load offset=20
            f32.lt
            br_if $B13
            local.get $l2
            i32.load8_u offset=24
            i32.const 1
            i32.and
            br_if $B13
            local.get $l2
            local.set $p0
            i32.const 0
            local.set $p1
            local.get $l4
            i32.load offset=8
            local.set $l6
            local.get $l3
            i32.load offset=4
            local.tee $l8
            f32.load
            local.set $l22
            loop $L14
              local.get $p1
              local.set $l2
              block $B15
                local.get $l6
                local.get $p0
                local.tee $l7
                i32.load offset=24
                local.tee $l10
                i32.const 1
                i32.shr_u
                local.tee $p1
                i32.const 28
                i32.mul
                local.tee $l5
                i32.add
                local.tee $p0
                f32.load
                local.get $l22
                f32.gt
                br_if $B15
                local.get $l5
                local.get $l6
                i32.add
                local.tee $l5
                f32.load offset=4
                local.get $l8
                f32.load offset=4
                f32.gt
                br_if $B15
                local.get $l5
                f32.load offset=8
                local.get $l8
                f32.load offset=8
                f32.gt
                br_if $B15
                local.get $l5
                f32.load offset=12
                local.get $l8
                f32.load offset=12
                f32.lt
                br_if $B15
                local.get $l5
                f32.load offset=16
                local.get $l8
                f32.load offset=16
                f32.lt
                br_if $B15
                local.get $l5
                f32.load offset=20
                local.get $l8
                f32.load offset=20
                f32.lt
                i32.eqz
                br_if $L14
              end
              block $B16
                local.get $p0
                f32.load offset=28
                local.get $l22
                f32.gt
                br_if $B16
                local.get $p0
                i32.const 28
                i32.add
                local.tee $p0
                f32.load offset=4
                local.get $l8
                f32.load offset=4
                f32.gt
                br_if $B16
                local.get $p0
                f32.load offset=8
                local.get $l8
                f32.load offset=8
                f32.gt
                br_if $B16
                local.get $p0
                f32.load offset=12
                local.get $l8
                f32.load offset=12
                f32.lt
                br_if $B16
                local.get $p0
                f32.load offset=16
                local.get $l8
                f32.load offset=16
                f32.lt
                br_if $B16
                local.get $p0
                f32.load offset=20
                local.get $l8
                f32.load offset=20
                f32.lt
                br_if $B16
                local.get $p1
                i32.const 1
                i32.add
                local.set $p1
                br $L14
              end
            end
            block $B17
              local.get $l10
              i32.const 1
              i32.and
              if $I18
                local.get $l4
                local.get $l7
                local.get $l3
                local.get $l2
                call $f71771
                br $B17
              end
              local.get $l4
              local.get $l7
              local.get $l3
              local.get $l2
              call $f71772
            end
            br $B12
          end
          block $B19
            local.get $l2
            i32.load8_u offset=24
            i32.const 1
            i32.and
            if $I20
              local.get $l4
              local.get $l2
              local.get $l3
              i32.const 0
              call $f71771
              br $B19
            end
            local.get $l4
            local.get $l2
            local.get $l3
            i32.const 0
            call $f71772
          end
          local.get $l3
          i32.load offset=4
          local.tee $l5
          f32.load
          local.set $l22
          local.get $l5
          f32.load offset=4
          local.set $l23
          local.get $l4
          i32.load offset=8
          local.tee $l2
          local.get $l2
          f32.load offset=8
          local.tee $l24
          local.get $l5
          f32.load offset=8
          local.tee $l25
          local.get $l24
          local.get $l25
          f32.lt
          select
          f32.store offset=8
          local.get $l2
          local.get $l2
          f32.load offset=4
          local.tee $l24
          local.get $l23
          local.get $l23
          local.get $l24
          f32.gt
          select
          f32.store offset=4
          local.get $l2
          local.get $l2
          f32.load
          local.tee $l23
          local.get $l22
          local.get $l22
          local.get $l23
          f32.gt
          select
          f32.store
          local.get $l5
          f32.load offset=16
          local.set $l22
          local.get $l5
          f32.load offset=12
          local.set $l23
          local.get $l2
          i32.const 20
          i32.add
          local.tee $p1
          local.get $p1
          f32.load
          local.tee $l24
          local.get $l5
          f32.load offset=20
          local.tee $l25
          local.get $l24
          local.get $l25
          f32.gt
          select
          f32.store
          local.get $l2
          i32.const 16
          i32.add
          local.tee $l5
          local.get $l5
          f32.load
          local.tee $l24
          local.get $l22
          local.get $l22
          local.get $l24
          f32.lt
          select
          f32.store
          local.get $l2
          local.get $l2
          f32.load offset=12
          local.tee $l22
          local.get $l23
          local.get $l22
          local.get $l23
          f32.gt
          select
          f32.store offset=12
        end
        local.get $l4
        local.get $l4
        i32.load offset=4
        local.get $l3
        i32.load offset=8
        i32.add
        i32.store offset=4
        br $B0
      end
      local.get $p0
      i32.load offset=48
      local.set $p1
      global.get $g0
      i32.const 32
      i32.sub
      local.tee $l10
      global.set $g0
      local.get $p0
      i32.const 52
      i32.add
      local.tee $l7
      i32.load offset=204
      local.tee $l12
      local.get $l7
      i32.load offset=208
      i32.eq
      if $I21
        local.get $l12
        i32.const 1
        i32.shl
        local.tee $l8
        i32.const 24
        i32.mul
        i32.const 24
        i32.add
        local.tee $l4
        if $I22 (result i32)
          call $f69753
          local.tee $p0
          local.get $l4
          i32.const 3178132
          i32.const 3177808
          i32.const 201
          local.get $p0
          i32.load
          i32.load offset=8
          call_indirect $__indirect_function_table (type $t9)
        else
          i32.const 0
        end
        local.get $l7
        i32.load offset=196
        local.get $l7
        i32.load offset=208
        i32.const 24
        i32.mul
        call $f483
        local.set $l4
        local.get $l7
        i32.load offset=196
        local.tee $p0
        if $I23
          call $f69753
          local.tee $l3
          local.get $p0
          local.get $l3
          i32.load
          i32.load offset=12
          call_indirect $__indirect_function_table (type $t1)
        end
        local.get $l7
        local.get $l4
        i32.store offset=196
        local.get $l8
        i32.const 3
        i32.shl
        local.tee $l4
        if $I24 (result i32)
          call $f69753
          local.tee $p0
          local.get $l4
          i32.const 3178132
          i32.const 3177808
          i32.const 208
          local.get $p0
          i32.load
          i32.load offset=8
          call_indirect $__indirect_function_table (type $t9)
        else
          i32.const 0
        end
        local.tee $p0
        local.get $l7
        i32.load offset=200
        local.get $l7
        i32.load offset=208
        i32.const 3
        i32.shl
        call $f483
        local.set $l4
        local.get $l7
        i32.load offset=200
        local.tee $l3
        if $I25
          call $f69753
          local.tee $l2
          local.get $l3
          local.get $l2
          i32.load
          i32.load offset=12
          call_indirect $__indirect_function_table (type $t1)
        end
        local.get $l7
        local.get $l4
        i32.store offset=200
        block $B26
          local.get $l7
          i32.load offset=208
          local.tee $l4
          local.get $l8
          i32.ge_u
          br_if $B26
          loop $L27
            local.get $p0
            local.get $l4
            i32.const 3
            i32.shl
            local.tee $l3
            i32.add
            i32.const 0
            i32.store offset=4
            call $f69753
            local.tee $p0
            i32.const 64
            i32.const 3178780
            i32.const 3178240
            i32.const 4700888
            i32.load
            local.tee $l2
            local.get $l2
            i32.load
            i32.load offset=20
            call_indirect $__indirect_function_table (type $t5)
            select
            i32.const 3177808
            i32.const 217
            local.get $p0
            i32.load
            i32.load offset=8
            call_indirect $__indirect_function_table (type $t9)
            local.tee $p0
            call $f71774
            local.get $l7
            i32.load offset=200
            local.get $l3
            i32.add
            local.get $p0
            i32.store
            local.get $l4
            i32.const 1
            i32.add
            local.tee $l4
            local.get $l8
            i32.eq
            br_if $B26
            local.get $l7
            i32.load offset=200
            local.set $p0
            br $L27
          end
          unreachable
        end
        local.get $l7
        local.get $l8
        i32.store offset=208
        local.get $l7
        i32.load offset=204
        local.set $l12
      end
      local.get $l7
      local.get $l12
      i32.const 1
      i32.add
      i32.store offset=204
      local.get $l7
      i32.load offset=124
      i32.load offset=12
      local.set $l2
      local.get $l11
      i32.const 8
      i32.add
      local.tee $l8
      i32.load offset=16
      local.set $l5
      local.get $l12
      i32.const 3
      i32.shl
      local.tee $l9
      local.get $l7
      i32.load offset=200
      i32.add
      local.get $p1
      i32.store offset=4
      local.get $l7
      i32.load offset=200
      local.get $l9
      i32.add
      i32.load
      local.tee $l4
      local.get $l8
      local.tee $p0
      i32.load offset=8
      i32.const 2
      i32.shl
      local.tee $l3
      if $I28 (result i32)
        call $f69753
        local.tee $l6
        local.get $l3
        i32.const 3176237
        i32.const 3175524
        i32.const 168
        local.get $l6
        i32.load
        i32.load offset=8
        call_indirect $__indirect_function_table (type $t9)
      else
        i32.const 0
      end
      local.tee $l3
      i32.store
      local.get $l4
      local.get $p0
      i32.load offset=8
      i32.store offset=4
      local.get $l3
      local.get $p0
      i32.load offset=12
      local.get $p0
      i32.load offset=8
      i32.const 2
      i32.shl
      call $f483
      drop
      local.get $p0
      i32.load
      local.set $l3
      call $f69753
      local.tee $l6
      i32.const -1
      i32.const -1
      local.get $l3
      i64.extend_i32_u
      i64.const 28
      i64.mul
      local.tee $l21
      i32.wrap_i64
      local.tee $l9
      i32.const 4
      i32.add
      local.tee $l13
      local.get $l9
      local.get $l13
      i32.gt_u
      select
      local.get $l21
      i64.const 32
      i64.shr_u
      i32.wrap_i64
      select
      i32.const 3177145
      i32.const 3176295
      i32.const 4700888
      i32.load
      local.tee $l9
      local.get $l9
      i32.load
      i32.load offset=20
      call_indirect $__indirect_function_table (type $t5)
      select
      i32.const 3175524
      i32.const 173
      local.get $l6
      i32.load
      i32.load offset=8
      call_indirect $__indirect_function_table (type $t9)
      local.tee $l6
      local.get $l3
      i32.store
      local.get $l4
      local.get $l6
      i32.const 4
      i32.add
      local.tee $l3
      i32.store offset=8
      local.get $l4
      local.get $p0
      i32.load
      i32.store offset=40
      local.get $l3
      local.get $p0
      i32.load offset=4
      local.get $p0
      i32.load
      i32.const 28
      i32.mul
      call $f483
      drop
      local.get $l7
      i32.load offset=196
      local.get $l12
      i32.const 24
      i32.mul
      i32.add
      local.tee $l9
      local.get $l8
      i32.load offset=4
      local.tee $l6
      f32.load
      f32.store
      local.get $l9
      local.get $l6
      f32.load offset=4
      f32.store offset=4
      local.get $l9
      local.get $l6
      f32.load offset=8
      f32.store offset=8
      local.get $l9
      local.get $l6
      f32.load offset=12
      f32.store offset=12
      local.get $l9
      local.get $l6
      f32.load offset=16
      f32.store offset=16
      local.get $l9
      local.get $l6
      f32.load offset=20
      f32.store offset=20
      local.get $l7
      i32.const 184
      i32.add
      local.tee $p0
      local.get $l8
      i32.load offset=8
      local.get $l4
      call $f71832
      i32.const 0
      local.set $l9
      local.get $l10
      i32.const 0
      i32.store offset=20
      local.get $l10
      local.get $l7
      i32.load offset=204
      i32.store offset=12
      local.get $l7
      i32.load offset=196
      local.set $l6
      local.get $l10
      i32.const 4
      i32.store offset=8
      local.get $l10
      local.get $l6
      i32.store offset=16
      local.get $l7
      i32.load offset=168
      local.get $l10
      i32.const 8
      i32.add
      call $f71768
      local.get $l7
      i32.const 172
      i32.add
      local.get $l7
      i32.load offset=204
      local.get $l7
      i32.load offset=168
      call $f71832
      local.get $l10
      i32.const 0
      i32.store offset=16
      local.get $l10
      i64.const 0
      i64.store offset=8
      local.get $l10
      i32.load offset=20
      local.tee $l6
      if $I29
        call $f69753
        local.tee $l3
        local.get $l6
        local.get $l3
        i32.load
        i32.load offset=12
        call_indirect $__indirect_function_table (type $t1)
      end
      local.get $l8
      i32.load offset=8
      if $I30
        local.get $l2
        local.get $l5
        i32.const 3
        i32.shl
        i32.add
        local.set $l5
        local.get $l7
        i32.const 128
        i32.add
        local.set $l3
        loop $L31
          i32.const -1
          local.set $l2
          local.get $l9
          local.get $l7
          i32.load offset=188
          i32.lt_u
          if $I32
            local.get $p0
            i32.load
            local.get $l9
            i32.const 2
            i32.shl
            i32.add
            i32.load
            local.set $l2
          end
          local.get $l10
          local.get $l5
          local.get $l9
          i32.const 3
          i32.shl
          i32.add
          i64.load align=4
          i64.store offset=8
          local.get $l10
          i32.const 8
          i32.add
          local.set $l14
          local.get $l10
          i32.const 31
          i32.add
          local.set $l16
          i32.const 0
          local.set $l15
          block $B33
            block $B34
              block $B35
                local.get $l3
                i32.load offset=20
                local.tee $l6
                i32.eqz
                br_if $B35
                local.get $l3
                i32.load offset=12
                local.get $l14
                i32.load
                local.tee $l18
                i64.extend_i32_u
                local.tee $l21
                local.get $l14
                i32.load offset=4
                local.tee $l19
                i64.extend_i32_u
                i64.const 32
                i64.shl
                i64.or
                local.get $l21
                i64.const 32
                i64.shl
                i64.const -1
                i64.xor
                i64.add
                local.tee $l21
                i64.const 22
                i64.shr_u
                local.get $l21
                i64.xor
                local.tee $l21
                local.get $l21
                i64.const 13
                i64.shl
                i64.const -1
                i64.xor
                i64.add
                local.tee $l21
                i64.const 8
                i64.shr_u
                local.get $l21
                i64.xor
                i64.const 9
                i64.mul
                local.tee $l21
                i64.const 15
                i64.shr_u
                local.get $l21
                i64.xor
                local.tee $l21
                local.get $l21
                i64.const 27
                i64.shl
                i64.const -1
                i64.xor
                i64.add
                local.tee $l21
                i64.const 31
                i64.shr_u
                local.get $l21
                i64.xor
                i32.wrap_i64
                local.get $l6
                i32.const 1
                i32.sub
                i32.and
                local.tee $l15
                i32.const 2
                i32.shl
                i32.add
                i32.load
                local.tee $l6
                i32.const -1
                i32.eq
                br_if $B35
                local.get $l3
                i32.const 4
                i32.add
                local.set $l17
                local.get $l3
                i32.load offset=4
                local.set $l20
                loop $L36
                  local.get $l18
                  local.get $l20
                  local.get $l6
                  i32.const 20
                  i32.mul
                  i32.add
                  local.tee $l13
                  i32.load
                  i32.eq
                  if $I37
                    local.get $l13
                    i32.load offset=4
                    local.get $l19
                    i32.eq
                    br_if $B34
                  end
                  local.get $l3
                  i32.load offset=8
                  local.get $l6
                  i32.const 2
                  i32.shl
                  i32.add
                  i32.load
                  local.tee $l6
                  i32.const -1
                  i32.ne
                  br_if $L36
                end
              end
              local.get $l16
              i32.const 0
              i32.store8
              local.get $l3
              i32.load offset=36
              local.get $l3
              i32.load offset=16
              i32.eq
              if $I38
                local.get $l3
                i32.load offset=20
                local.tee $l6
                local.get $l6
                i32.const 1
                i32.shl
                i32.const 16
                local.get $l6
                select
                local.tee $l13
                i32.lt_u
                if $I39
                  local.get $l3
                  local.get $l13
                  call $f71860
                  local.get $l3
                  i32.load offset=20
                  local.set $l6
                end
                local.get $l14
                i64.load32_u
                local.tee $l21
                local.get $l14
                i64.load32_u offset=4
                i64.const 32
                i64.shl
                i64.or
                local.get $l21
                i64.const 32
                i64.shl
                i64.const -1
                i64.xor
                i64.add
                local.tee $l21
                i64.const 22
                i64.shr_u
                local.get $l21
                i64.xor
                local.tee $l21
                local.get $l21
                i64.const 13
                i64.shl
                i64.const -1
                i64.xor
                i64.add
                local.tee $l21
                i64.const 8
                i64.shr_u
                local.get $l21
                i64.xor
                i64.const 9
                i64.mul
                local.tee $l21
                i64.const 15
                i64.shr_u
                local.get $l21
                i64.xor
                local.tee $l21
                local.get $l21
                i64.const 27
                i64.shl
                i64.const -1
                i64.xor
                i64.add
                local.tee $l21
                i64.const 31
                i64.shr_u
                local.get $l21
                i64.xor
                i32.wrap_i64
                local.get $l6
                i32.const 1
                i32.sub
                i32.and
                local.set $l15
              end
              local.get $l3
              local.get $l3
              i32.load offset=28
              local.tee $l6
              i32.const 1
              i32.add
              i32.store offset=28
              local.get $l3
              i32.load offset=8
              local.get $l6
              i32.const 2
              i32.shl
              i32.add
              local.get $l15
              i32.const 2
              i32.shl
              local.tee $l13
              local.get $l3
              i32.load offset=12
              i32.add
              i32.load
              i32.store
              local.get $l3
              i32.load offset=12
              local.get $l13
              i32.add
              local.get $l6
              i32.store
              local.get $l3
              local.get $l3
              i32.load offset=36
              i32.const 1
              i32.add
              i32.store offset=36
              local.get $l3
              local.get $l3
              i32.load offset=32
              i32.const 1
              i32.add
              i32.store offset=32
              local.get $l3
              i32.const 4
              i32.add
              local.set $l17
              br $B33
            end
            local.get $l16
            i32.const 1
            i32.store8
          end
          local.get $l17
          i32.load
          local.get $l6
          i32.const 20
          i32.mul
          i32.add
          local.set $l6
          local.get $l10
          i32.load8_u offset=31
          i32.eqz
          if $I40
            local.get $l10
            i64.load offset=8
            local.set $l21
            local.get $l6
            local.get $p1
            i32.store offset=8
            local.get $l6
            local.get $l21
            i64.store align=4
            local.get $l6
            local.get $l12
            i32.store offset=16
            local.get $l6
            local.get $l2
            i32.store offset=12
          end
          local.get $l9
          i32.const 1
          i32.add
          local.tee $l9
          local.get $l8
          i32.load offset=8
          i32.lt_u
          br_if $L31
        end
      end
      local.get $l8
      i32.load offset=16
      local.set $l3
      i32.const 0
      local.set $p0
      local.get $l4
      i32.load offset=4
      if $I41
        loop $L42
          local.get $l4
          i32.load
          local.get $p0
          i32.const 2
          i32.shl
          i32.add
          local.tee $p1
          local.get $p1
          i32.load
          local.get $l3
          i32.add
          i32.store
          local.get $p0
          i32.const 1
          i32.add
          local.tee $p0
          local.get $l4
          i32.load offset=4
          i32.lt_u
          br_if $L42
        end
      end
      local.get $l10
      i32.const 32
      i32.add
      global.set $g0
    end
    local.get $l11
    i32.const 32
    i32.add
    global.set $g0)