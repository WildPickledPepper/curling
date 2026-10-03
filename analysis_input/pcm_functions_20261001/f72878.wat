  (func $f72878 (type $t9) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (result i32)
    (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 i32) (local $l17 i32) (local $l18 i32) (local $l19 i32) (local $l20 i32) (local $l21 i32) (local $l22 i32) (local $l23 i32) (local $l24 i32) (local $l25 i32) (local $l26 i32) (local $l27 i32) (local $l28 i32) (local $l29 i32) (local $l30 i32) (local $l31 i32) (local $l32 i32) (local $l33 i32) (local $l34 i32) (local $l35 i32) (local $l36 f32) (local $l37 f32) (local $l38 f32) (local $l39 f32) (local $l40 f32) (local $l41 f32) (local $l42 f32) (local $l43 f32) (local $l44 f32) (local $l45 f32) (local $l46 f32) (local $l47 f32) (local $l48 i64) (local $l49 f64)
    global.get $g0
    i32.const 32
    i32.sub
    local.tee $l26
    global.set $g0
    block $B0 (result i32)
      block $B1
        block $B2
          local.get $p1
          i32.load offset=8
          local.tee $l9
          i32.const 3
          i32.lt_u
          br_if $B2
          local.get $l9
          i32.const 65536
          i32.ge_u
          if $I3
            local.get $p1
            i32.load8_u offset=36
            i32.const 1
            i32.and
            br_if $B2
          end
          local.get $p1
          i32.load offset=4
          i32.eqz
          br_if $B2
          local.get $p1
          i32.load
          i32.const 12
          i32.lt_u
          br_if $B2
          local.get $p1
          i32.load16_u offset=40
          i32.const 4
          i32.lt_u
          br_if $B2
          block $B4
            local.get $p1
            i32.load offset=16
            if $I5
              local.get $p1
              i32.load offset=20
              i32.const 4
              i32.lt_u
              br_if $B2
              local.get $p1
              i32.load offset=28
              i32.eqz
              br_if $B2
              local.get $p1
              i32.load offset=24
              i32.const 2
              i32.const 4
              local.get $p1
              i32.load16_u offset=36
              local.tee $l9
              i32.const 1
              i32.and
              select
              i32.lt_u
              br_if $B2
              local.get $p1
              i32.load offset=12
              i32.const 19
              i32.gt_u
              br_if $B4
              br $B2
            end
            local.get $p1
            i32.load16_u offset=36
            local.tee $l9
            i32.const 2
            i32.and
            i32.eqz
            br_if $B2
          end
          local.get $p1
          i32.load16_u offset=38
          local.set $l8
          local.get $l9
          i32.const 32
          i32.and
          if $I6
            local.get $l8
            i32.const 4
            i32.sub
            i32.const 65535
            i32.and
            i32.const 253
            i32.ge_u
            br_if $B2
            br $B1
          end
          local.get $l8
          i32.const 8
          i32.sub
          i32.const 65535
          i32.and
          i32.const 249
          i32.lt_u
          br_if $B1
        end
        i32.const 4700888
        i32.load
        i32.const 4
        i32.const 3215716
        i32.const 73
        i32.const 3215777
        i32.const 0
        call $f69760
        i32.const 0
        br $B0
      end
      local.get $p4
      local.set $l12
      i32.const 0
      local.set $l8
      global.get $g0
      i32.const 32
      i32.sub
      local.tee $p4
      local.set $l23
      local.get $p4
      global.set $g0
      local.get $p4
      local.get $p1
      local.tee $l15
      i32.load offset=8
      local.tee $l11
      i32.const 12
      i32.mul
      i32.const 15
      i32.add
      i32.const -16
      i32.and
      i32.sub
      local.tee $l7
      local.tee $l14
      global.set $g0
      block $B7
        local.get $l11
        i32.eqz
        br_if $B7
        local.get $l15
        i32.load
        local.set $l13
        local.get $l11
        i32.const 1
        i32.sub
        local.set $l10
        local.get $l15
        i32.load offset=4
        local.set $p1
        block $B8
          local.get $l11
          i32.const 3
          i32.and
          local.tee $l5
          i32.eqz
          if $I9
            local.get $l7
            local.set $p4
            local.get $l11
            local.set $l9
            br $B8
          end
          local.get $l7
          local.set $p4
          local.get $l11
          local.set $l9
          loop $L10
            local.get $p4
            local.get $p1
            i64.load align=1
            i64.store align=1
            local.get $p4
            local.get $p1
            i32.load offset=8 align=1
            i32.store offset=8 align=1
            local.get $p1
            local.get $l13
            i32.add
            local.set $p1
            local.get $p4
            i32.const 12
            i32.add
            local.set $p4
            local.get $l9
            i32.const 1
            i32.sub
            local.set $l9
            local.get $l5
            i32.const 1
            i32.sub
            local.tee $l5
            br_if $L10
          end
        end
        local.get $l10
        i32.const 3
        i32.lt_u
        br_if $B7
        loop $L11
          local.get $p4
          local.get $p1
          i64.load align=1
          i64.store align=1
          local.get $p4
          local.get $p1
          i32.load offset=8 align=1
          i32.store offset=8 align=1
          local.get $p4
          local.get $p1
          local.get $l13
          i32.add
          local.tee $p1
          i32.load offset=8 align=1
          i32.store offset=20 align=1
          local.get $p4
          local.get $p1
          i64.load align=1
          i64.store offset=12 align=1
          local.get $p4
          local.get $p1
          local.get $l13
          i32.add
          local.tee $p1
          i32.load offset=8 align=1
          i32.store offset=32 align=1
          local.get $p4
          local.get $p1
          i64.load align=1
          i64.store offset=24 align=1
          local.get $p4
          local.get $p1
          local.get $l13
          i32.add
          local.tee $p1
          i64.load align=1
          i64.store offset=36 align=1
          local.get $p4
          local.get $p1
          i32.load offset=8 align=1
          i32.store offset=44 align=1
          local.get $p4
          i32.const 48
          i32.add
          local.set $p4
          local.get $p1
          local.get $l13
          i32.add
          local.set $p1
          local.get $l9
          i32.const 4
          i32.sub
          local.tee $l9
          br_if $L11
        end
      end
      i32.const 0
      local.set $l5
      block $B12
        local.get $l15
        i32.load offset=28
        local.tee $p4
        i32.eqz
        br_if $B12
        local.get $l14
        local.get $l15
        i32.load offset=32
        local.tee $l9
        i32.const 2
        i32.shl
        local.tee $p1
        i32.const 15
        i32.add
        i32.const -16
        i32.and
        i32.sub
        local.tee $l8
        local.tee $l14
        global.set $g0
        local.get $l15
        i32.load8_u offset=36
        i32.const 1
        i32.and
        if $I13
          local.get $p1
          local.get $l8
          i32.add
          local.tee $l10
          local.get $l8
          i32.le_u
          br_if $B12
          local.get $l15
          i32.load offset=24
          local.set $l13
          block $B14
            local.get $l9
            i32.const 2
            i32.shl
            i32.const 1
            i32.sub
            local.tee $l6
            i32.const 2
            i32.shr_u
            i32.const 1
            i32.add
            i32.const 7
            i32.and
            local.tee $l9
            i32.eqz
            if $I15
              local.get $l8
              local.set $p1
              br $B14
            end
            local.get $l8
            local.set $p1
            loop $L16
              local.get $p1
              local.get $p4
              i32.load16_u
              i32.store
              local.get $p4
              local.get $l13
              i32.add
              local.set $p4
              local.get $p1
              i32.const 4
              i32.add
              local.set $p1
              local.get $l9
              i32.const 1
              i32.sub
              local.tee $l9
              br_if $L16
            end
          end
          local.get $l6
          i32.const 28
          i32.lt_u
          br_if $B12
          loop $L17
            local.get $p1
            local.get $p4
            i32.load16_u
            i32.store
            local.get $p1
            local.get $p4
            local.get $l13
            i32.add
            local.tee $p4
            i32.load16_u
            i32.store offset=4
            local.get $p1
            local.get $p4
            local.get $l13
            i32.add
            local.tee $p4
            i32.load16_u
            i32.store offset=8
            local.get $p1
            local.get $p4
            local.get $l13
            i32.add
            local.tee $p4
            i32.load16_u
            i32.store offset=12
            local.get $p1
            local.get $p4
            local.get $l13
            i32.add
            local.tee $p4
            i32.load16_u
            i32.store offset=16
            local.get $p1
            local.get $p4
            local.get $l13
            i32.add
            local.tee $p4
            i32.load16_u
            i32.store offset=20
            local.get $p1
            local.get $p4
            local.get $l13
            i32.add
            local.tee $p4
            i32.load16_u
            i32.store offset=24
            local.get $p1
            local.get $p4
            local.get $l13
            i32.add
            local.tee $p4
            i32.load16_u
            i32.store offset=28
            local.get $p4
            local.get $l13
            i32.add
            local.set $p4
            local.get $p1
            i32.const 32
            i32.add
            local.tee $p1
            local.get $l10
            i32.lt_u
            br_if $L17
          end
          br $B12
        end
        local.get $l9
        i32.eqz
        br_if $B12
        local.get $l15
        i32.load offset=24
        local.set $l13
        local.get $l9
        i32.const 1
        i32.sub
        local.set $l6
        block $B18
          local.get $l9
          i32.const 3
          i32.and
          local.tee $l10
          i32.eqz
          if $I19
            local.get $l8
            local.set $p1
            br $B18
          end
          local.get $l8
          local.set $p1
          loop $L20
            local.get $p1
            local.get $p4
            i32.load align=1
            i32.store align=1
            local.get $p4
            local.get $l13
            i32.add
            local.set $p4
            local.get $p1
            i32.const 4
            i32.add
            local.set $p1
            local.get $l9
            i32.const 1
            i32.sub
            local.set $l9
            local.get $l10
            i32.const 1
            i32.sub
            local.tee $l10
            br_if $L20
          end
        end
        local.get $l6
        i32.const 3
        i32.lt_u
        br_if $B12
        loop $L21
          local.get $p1
          local.get $p4
          i32.load align=1
          i32.store align=1
          local.get $p1
          local.get $p4
          local.get $l13
          i32.add
          local.tee $p4
          i32.load align=1
          i32.store offset=4 align=1
          local.get $p1
          local.get $p4
          local.get $l13
          i32.add
          local.tee $p4
          i32.load align=1
          i32.store offset=8 align=1
          local.get $p1
          local.get $p4
          local.get $l13
          i32.add
          local.tee $p4
          i32.load align=1
          i32.store offset=12 align=1
          local.get $p1
          i32.const 16
          i32.add
          local.set $p1
          local.get $p4
          local.get $l13
          i32.add
          local.set $p4
          local.get $l9
          i32.const 4
          i32.sub
          local.tee $l9
          br_if $L21
        end
      end
      local.get $l15
      i32.load offset=20
      local.set $l6
      block $B22
        local.get $l15
        i32.load offset=16
        local.tee $p1
        i32.eqz
        br_if $B22
        local.get $l14
        local.get $l6
        i32.const 20
        i32.mul
        i32.const 15
        i32.add
        i32.const -16
        i32.and
        i32.sub
        local.tee $l5
        global.set $g0
        local.get $l6
        i32.eqz
        if $I23
          i32.const 0
          local.set $l6
          br $B22
        end
        local.get $l15
        i32.load offset=12
        local.set $l13
        local.get $l6
        i32.const 1
        i32.sub
        local.set $l14
        block $B24
          local.get $l6
          i32.const 3
          i32.and
          local.tee $l10
          i32.eqz
          if $I25
            local.get $l5
            local.set $p4
            local.get $l6
            local.set $l9
            br $B24
          end
          local.get $l5
          local.set $p4
          local.get $l6
          local.set $l9
          loop $L26
            local.get $p4
            local.get $p1
            i64.load align=1
            i64.store align=1
            local.get $p4
            local.get $p1
            i32.load offset=16 align=1
            i32.store offset=16 align=1
            local.get $p4
            local.get $p1
            i64.load offset=8 align=1
            i64.store offset=8 align=1
            local.get $p1
            local.get $l13
            i32.add
            local.set $p1
            local.get $p4
            i32.const 20
            i32.add
            local.set $p4
            local.get $l9
            i32.const 1
            i32.sub
            local.set $l9
            local.get $l10
            i32.const 1
            i32.sub
            local.tee $l10
            br_if $L26
          end
        end
        local.get $l14
        i32.const 3
        i32.ge_u
        if $I27
          loop $L28
            local.get $p4
            local.get $p1
            i64.load align=1
            i64.store align=1
            local.get $p4
            local.get $p1
            i32.load offset=16 align=1
            i32.store offset=16 align=1
            local.get $p4
            local.get $p1
            i64.load offset=8 align=1
            i64.store offset=8 align=1
            local.get $p4
            local.get $p1
            local.get $l13
            i32.add
            local.tee $p1
            i32.load offset=16 align=1
            i32.store offset=36 align=1
            local.get $p4
            local.get $p1
            i64.load offset=8 align=1
            i64.store offset=28 align=1
            local.get $p4
            local.get $p1
            i64.load align=1
            i64.store offset=20 align=1
            local.get $p4
            local.get $p1
            local.get $l13
            i32.add
            local.tee $p1
            i32.load offset=16 align=1
            i32.store offset=56 align=1
            local.get $p4
            local.get $p1
            i64.load offset=8 align=1
            i64.store offset=48 align=1
            local.get $p4
            local.get $p1
            i64.load align=1
            i64.store offset=40 align=1
            local.get $p4
            local.get $p1
            local.get $l13
            i32.add
            local.tee $p1
            i64.load align=1
            i64.store offset=60 align=1
            local.get $p4
            local.get $p1
            i64.load offset=8 align=1
            i64.store offset=68 align=1
            local.get $p4
            local.get $p1
            i32.load offset=16 align=1
            i32.store offset=76 align=1
            local.get $p4
            i32.const 80
            i32.add
            local.set $p4
            local.get $p1
            local.get $l13
            i32.add
            local.set $p1
            local.get $l9
            i32.const 4
            i32.sub
            local.tee $l9
            br_if $L28
          end
        end
        local.get $l12
        br_if $B22
        local.get $l6
        i32.const 2
        i32.lt_u
        br_if $B22
        local.get $l14
        i32.const 3
        i32.and
        local.set $l9
        block $B29
          local.get $l6
          i32.const 2
          i32.sub
          i32.const 3
          i32.lt_u
          if $I30
            i32.const 0
            local.set $p1
            i32.const 1
            local.set $p4
            br $B29
          end
          local.get $l14
          i32.const -4
          i32.and
          local.set $l10
          i32.const 0
          local.set $p1
          i32.const 1
          local.set $p4
          loop $L31
            local.get $p4
            i32.const 3
            i32.add
            local.get $p4
            i32.const 2
            i32.add
            local.get $p4
            i32.const 1
            i32.add
            local.get $p4
            local.get $p1
            local.get $l5
            local.get $p4
            i32.const 20
            i32.mul
            i32.add
            local.tee $l13
            i32.load16_u offset=16
            local.get $l5
            local.get $p1
            i32.const 20
            i32.mul
            i32.add
            i32.load16_u offset=16
            i32.gt_u
            select
            local.tee $p1
            local.get $l13
            i32.load16_u offset=36
            local.get $l5
            local.get $p1
            i32.const 20
            i32.mul
            i32.add
            i32.load16_u offset=16
            i32.gt_u
            select
            local.tee $p1
            local.get $l13
            i32.load16_u offset=56
            local.get $l5
            local.get $p1
            i32.const 20
            i32.mul
            i32.add
            i32.load16_u offset=16
            i32.gt_u
            select
            local.tee $p1
            local.get $l13
            i32.load16_u offset=76
            local.get $l5
            local.get $p1
            i32.const 20
            i32.mul
            i32.add
            i32.load16_u offset=16
            i32.gt_u
            select
            local.set $p1
            local.get $p4
            i32.const 4
            i32.add
            local.set $p4
            local.get $l10
            i32.const 4
            i32.sub
            local.tee $l10
            br_if $L31
          end
        end
        local.get $l9
        if $I32
          loop $L33
            local.get $p4
            local.get $p1
            local.get $l5
            local.get $p4
            i32.const 20
            i32.mul
            i32.add
            i32.load16_u offset=16
            local.get $l5
            local.get $p1
            i32.const 20
            i32.mul
            i32.add
            i32.load16_u offset=16
            i32.gt_u
            select
            local.set $p1
            local.get $p4
            i32.const 1
            i32.add
            local.set $p4
            local.get $l9
            i32.const 1
            i32.sub
            local.tee $l9
            br_if $L33
          end
        end
        local.get $p1
        i32.eqz
        br_if $B22
        local.get $l23
        i32.const 24
        i32.add
        local.tee $l13
        local.get $l5
        i32.const 16
        i32.add
        local.tee $l9
        i32.load
        i32.store
        local.get $l23
        i32.const 16
        i32.add
        local.tee $l10
        local.get $l5
        i32.const 8
        i32.add
        local.tee $l14
        i64.load align=4
        i64.store
        local.get $l23
        local.get $l5
        i64.load align=4
        i64.store offset=8
        local.get $l9
        local.get $l5
        local.get $p1
        i32.const 20
        i32.mul
        i32.add
        local.tee $p4
        i32.const 16
        i32.add
        local.tee $p1
        i32.load
        i32.store
        local.get $l14
        local.get $p4
        i32.const 8
        i32.add
        local.tee $l9
        i64.load align=4
        i64.store align=4
        local.get $l5
        local.get $p4
        i64.load align=4
        i64.store align=4
        local.get $p1
        local.get $l13
        i32.load
        i32.store
        local.get $l9
        local.get $l10
        i64.load
        i64.store align=4
        local.get $p4
        local.get $l23
        i64.load offset=8
        i64.store align=4
      end
      block $B34
        block $B35 (result i32)
          local.get $l15
          i32.load offset=32
          local.set $p4
          local.get $l6
          local.set $l24
          local.get $l15
          i32.load16_u offset=36
          i32.const 16
          i32.and
          i32.eqz
          local.set $l13
          local.get $p0
          i64.const 0
          i64.store align=4
          local.get $p0
          i32.const 24
          i32.add
          local.tee $l25
          i32.const 0
          i32.store
          local.get $p0
          i64.const 0
          i64.store offset=16 align=4
          local.get $p0
          i32.const 8
          i32.add
          local.tee $l10
          i64.const 0
          i64.store align=4
          local.get $p0
          i32.load offset=28
          local.get $l11
          i32.store8 offset=38
          local.get $p0
          i32.load offset=28
          i32.load8_u offset=38
          local.set $p1
          local.get $p0
          call $f69753
          local.tee $l17
          local.get $p1
          i32.const 12
          i32.mul
          i32.const 12
          i32.add
          i32.const 3214872
          i32.const 3214126
          i32.const 118
          local.get $l17
          i32.load
          i32.load offset=8
          call_indirect $__indirect_function_table (type $t9)
          local.tee $p1
          i32.store
          local.get $p1
          local.get $l7
          local.get $p0
          i32.load offset=28
          i32.load8_u offset=38
          i32.const 12
          i32.mul
          call $f483
          drop
          local.get $p0
          i32.load offset=28
          i32.const 0
          i32.store8 offset=39
          local.get $l10
          i32.load
          local.tee $l7
          if $I36
            call $f69753
            local.tee $p1
            local.get $l7
            local.get $p1
            i32.load
            i32.load offset=12
            call_indirect $__indirect_function_table (type $t1)
          end
          local.get $p0
          i32.const 0
          i32.store offset=8
          local.get $p0
          i32.load offset=4
          local.tee $l7
          if $I37
            call $f69753
            local.tee $p1
            local.get $l7
            local.get $p1
            i32.load
            i32.load offset=12
            call_indirect $__indirect_function_table (type $t1)
          end
          local.get $p0
          i32.const 0
          i32.store offset=4
          local.get $l24
          i32.const 256
          i32.ge_u
          if $I38
            i32.const 4700888
            i32.load
            i32.const 32
            i32.const 3214126
            i32.const 128
            i32.const 3214185
            i32.const 0
            call $f69760
            i32.const 0
            br $B35
          end
          local.get $p0
          i32.load offset=28
          local.get $l24
          i32.store8 offset=39
          local.get $p0
          local.get $p0
          i32.load offset=28
          i32.load8_u offset=39
          local.tee $p1
          if $I39 (result i32)
            call $f69753
            local.tee $l7
            local.get $p1
            i32.const 20
            i32.mul
            i32.const 3214872
            i32.const 3214126
            i32.const 134
            local.get $l7
            i32.load
            i32.load offset=8
            call_indirect $__indirect_function_table (type $t9)
          else
            i32.const 0
          end
          i32.store offset=4
          i32.const 0
          local.set $l7
          local.get $p4
          if $I40
            call $f69753
            local.tee $l7
            local.get $p4
            i32.const 3214916
            i32.const 3214888
            i32.const 4700888
            i32.load
            local.tee $p1
            local.get $p1
            i32.load
            i32.load offset=20
            call_indirect $__indirect_function_table (type $t5)
            select
            i32.const 3214126
            i32.const 136
            local.get $l7
            i32.load
            i32.load offset=8
            call_indirect $__indirect_function_table (type $t9)
            local.set $l7
          end
          local.get $p0
          local.get $l7
          i32.store offset=8
          block $B41
            local.get $l24
            i32.eqz
            br_if $B41
            local.get $l7
            local.set $p1
            loop $L42
              local.get $l21
              i32.const 20
              i32.mul
              local.tee $l18
              local.get $p0
              i32.load offset=4
              i32.add
              local.get $p1
              local.get $l7
              i32.sub
              i32.store16 offset=16
              local.get $p0
              i32.load offset=4
              local.get $l18
              i32.add
              local.get $l5
              local.get $l18
              i32.add
              local.tee $l22
              i32.load16_u offset=16
              local.tee $l16
              i32.store8 offset=18
              block $B43
                local.get $l16
                i32.eqz
                br_if $B43
                local.get $l22
                i32.const 18
                i32.add
                local.set $l10
                local.get $l16
                i32.const 3
                i32.and
                local.set $l17
                i32.const 0
                local.set $l7
                local.get $l16
                i32.const 1
                i32.sub
                i32.const 3
                i32.ge_u
                if $I44
                  local.get $l16
                  i32.const 65532
                  i32.and
                  local.set $l19
                  loop $L45
                    local.get $p1
                    local.get $l7
                    i32.add
                    local.get $l8
                    local.get $l7
                    local.get $l10
                    i32.load16_u
                    i32.add
                    i32.const 2
                    i32.shl
                    i32.add
                    i32.load
                    i32.store8
                    local.get $p1
                    local.get $l7
                    i32.const 1
                    i32.or
                    local.tee $l14
                    i32.add
                    local.get $l8
                    local.get $l14
                    local.get $l10
                    i32.load16_u
                    i32.add
                    i32.const 2
                    i32.shl
                    i32.add
                    i32.load
                    i32.store8
                    local.get $p1
                    local.get $l7
                    i32.const 2
                    i32.or
                    local.tee $l14
                    i32.add
                    local.get $l8
                    local.get $l14
                    local.get $l10
                    i32.load16_u
                    i32.add
                    i32.const 2
                    i32.shl
                    i32.add
                    i32.load
                    i32.store8
                    local.get $p1
                    local.get $l7
                    i32.const 3
                    i32.or
                    local.tee $l14
                    i32.add
                    local.get $l8
                    local.get $l14
                    local.get $l10
                    i32.load16_u
                    i32.add
                    i32.const 2
                    i32.shl
                    i32.add
                    i32.load
                    i32.store8
                    local.get $l7
                    i32.const 4
                    i32.add
                    local.set $l7
                    local.get $l19
                    i32.const 4
                    i32.sub
                    local.tee $l19
                    br_if $L45
                  end
                end
                local.get $l17
                i32.eqz
                br_if $B43
                loop $L46
                  local.get $p1
                  local.get $l7
                  i32.add
                  local.get $l8
                  local.get $l7
                  local.get $l10
                  i32.load16_u
                  i32.add
                  i32.const 2
                  i32.shl
                  i32.add
                  i32.load
                  i32.store8
                  local.get $l7
                  i32.const 1
                  i32.add
                  local.set $l7
                  local.get $l17
                  i32.const 1
                  i32.sub
                  local.tee $l17
                  br_if $L46
                end
              end
              local.get $l22
              i64.load align=4
              local.set $l48
              local.get $p0
              i32.load offset=4
              local.get $l18
              i32.add
              local.tee $l7
              local.get $l22
              i64.load offset=8 align=4
              i64.store offset=8 align=4
              local.get $l7
              local.get $l48
              i64.store align=4
              local.get $l21
              i32.const 1
              i32.add
              local.tee $l21
              local.get $l24
              i32.eq
              br_if $B41
              local.get $p1
              local.get $l16
              i32.add
              local.set $p1
              local.get $p0
              i32.load offset=8
              local.set $l7
              br $L42
            end
            unreachable
          end
          i32.const 0
          local.set $l7
          block $B47
            local.get $p0
            local.get $l24
            local.get $l12
            i32.eqz
            call $f72870
            i32.eqz
            br_if $B47
            block $B48
              block $B49
                local.get $l12
                if $I50
                  local.get $l12
                  local.get $p4
                  local.get $p0
                  i32.load offset=8
                  local.get $p0
                  i32.const 12
                  i32.add
                  local.get $p0
                  i32.const 20
                  i32.add
                  local.get $l25
                  local.get $l12
                  i32.load
                  i32.load offset=16
                  call_indirect $__indirect_function_table (type $t10)
                  br_if $B49
                end
                i32.const 0
                local.set $l5
                i32.const 0
                local.set $l18
                i32.const 0
                local.set $l19
                i32.const 0
                local.set $l25
                global.get $g0
                i32.const 48
                i32.sub
                local.tee $l32
                global.set $g0
                block $B51
                  local.get $p4
                  local.tee $l10
                  i32.const 1
                  i32.and
                  if $I52
                    i32.const 4700888
                    i32.load
                    i32.const 32
                    i32.const 3214126
                    i32.const 566
                    i32.const 3214799
                    i32.const 0
                    call $f69760
                    br $B51
                  end
                  local.get $p0
                  i32.load offset=28
                  i32.load8_u offset=39
                  local.set $l33
                  local.get $p0
                  i32.load offset=12
                  local.tee $l5
                  if $I53
                    call $f69753
                    local.tee $p4
                    local.get $l5
                    local.get $p4
                    i32.load
                    i32.load offset=12
                    call_indirect $__indirect_function_table (type $t1)
                  end
                  local.get $p0
                  i32.const 0
                  i32.store offset=12
                  local.get $p0
                  local.get $l10
                  if $I54 (result i32)
                    call $f69753
                    local.tee $l5
                    local.get $l10
                    i32.const 3214916
                    i32.const 3214888
                    i32.const 4700888
                    i32.load
                    local.tee $p4
                    local.get $p4
                    i32.load
                    i32.load offset=20
                    call_indirect $__indirect_function_table (type $t5)
                    select
                    i32.const 3214126
                    i32.const 574
                    local.get $l5
                    i32.load
                    i32.load offset=8
                    call_indirect $__indirect_function_table (type $t9)
                  else
                    i32.const 0
                  end
                  i32.store offset=12
                  i32.const -1
                  local.get $l10
                  i32.const 5
                  i32.shl
                  local.get $l10
                  i32.const 3
                  i32.shl
                  local.tee $l5
                  i32.const 1073741816
                  i32.and
                  local.get $l5
                  i32.ne
                  select
                  local.tee $l5
                  if $I55
                    call $f69753
                    local.tee $p4
                    local.get $l5
                    i32.const 3215016
                    i32.const 3214888
                    i32.const 4700888
                    i32.load
                    local.tee $l12
                    local.get $l12
                    i32.load
                    i32.load offset=20
                    call_indirect $__indirect_function_table (type $t5)
                    select
                    i32.const 3214126
                    i32.const 576
                    local.get $p4
                    i32.load
                    i32.load offset=8
                    call_indirect $__indirect_function_table (type $t9)
                    local.set $l18
                  end
                  local.get $l18
                  local.get $l10
                  i32.const 2
                  i32.shl
                  local.tee $l5
                  i32.add
                  local.tee $l6
                  local.get $l5
                  i32.add
                  local.tee $l11
                  local.get $l5
                  i32.add
                  local.tee $l9
                  local.get $l5
                  i32.add
                  local.tee $l34
                  local.get $l5
                  i32.add
                  local.tee $l35
                  local.get $l5
                  i32.add
                  local.set $l27
                  local.get $l10
                  if $I56
                    call $f69753
                    local.tee $p4
                    local.get $l10
                    i32.const 3215114
                    i32.const 3214888
                    i32.const 4700888
                    i32.load
                    local.tee $l12
                    local.get $l12
                    i32.load
                    i32.load offset=20
                    call_indirect $__indirect_function_table (type $t5)
                    select
                    i32.const 3214126
                    i32.const 588
                    local.get $p4
                    i32.load
                    i32.load offset=8
                    call_indirect $__indirect_function_table (type $t9)
                    local.set $l25
                  end
                  local.get $l5
                  local.get $l27
                  i32.add
                  local.set $l20
                  local.get $l33
                  if $I57
                    local.get $l18
                    local.set $l12
                    local.get $l6
                    local.set $p1
                    local.get $l11
                    local.set $l8
                    i32.const 0
                    local.set $p4
                    local.get $l25
                    local.set $l14
                    local.get $l9
                    local.set $l16
                    loop $L58
                      local.get $p0
                      i32.load offset=4
                      local.get $l19
                      i32.const 20
                      i32.mul
                      i32.add
                      local.tee $l5
                      i32.load8_u offset=18
                      local.tee $l30
                      if $I59
                        local.get $p0
                        i32.load offset=8
                        local.get $l5
                        i32.load16_u offset=16
                        i32.add
                        local.set $l22
                        i32.const 0
                        local.set $l5
                        loop $L60
                          local.get $l12
                          local.get $l22
                          i32.const 0
                          local.get $l5
                          i32.const 1
                          i32.add
                          local.tee $l17
                          local.get $l17
                          local.get $l30
                          i32.eq
                          local.tee $l31
                          select
                          i32.add
                          i32.load8_u
                          local.tee $l28
                          local.get $l5
                          local.get $l22
                          i32.add
                          i32.load8_u
                          local.tee $l29
                          local.get $l28
                          local.get $l29
                          i32.lt_u
                          local.tee $l21
                          select
                          i32.store
                          local.get $p1
                          local.get $l29
                          local.get $l28
                          local.get $l21
                          select
                          i32.store
                          local.get $l8
                          local.get $l19
                          i32.store
                          local.get $l16
                          local.get $l5
                          i32.store
                          local.get $l14
                          local.get $l21
                          i32.store8
                          local.get $l20
                          local.get $p4
                          i32.const 2
                          i32.shl
                          i32.add
                          local.get $p4
                          i32.store
                          local.get $p4
                          i32.const 1
                          i32.add
                          local.set $p4
                          local.get $l14
                          i32.const 1
                          i32.add
                          local.set $l14
                          local.get $l16
                          i32.const 4
                          i32.add
                          local.set $l16
                          local.get $l8
                          i32.const 4
                          i32.add
                          local.set $l8
                          local.get $p1
                          i32.const 4
                          i32.add
                          local.set $p1
                          local.get $l12
                          i32.const 4
                          i32.add
                          local.set $l12
                          local.get $l17
                          local.set $l5
                          local.get $l31
                          i32.eqz
                          br_if $L60
                        end
                      end
                      local.get $l19
                      i32.const 1
                      i32.add
                      local.tee $l19
                      local.get $l33
                      i32.ne
                      br_if $L58
                    end
                  end
                  local.get $l32
                  i32.const 8
                  i32.add
                  call $f69791
                  local.tee $l30
                  local.get $l6
                  local.get $l10
                  i32.const 1
                  call $f69795
                  local.get $l18
                  local.get $l10
                  i32.const 1
                  call $f69795
                  i32.load offset=8
                  local.set $l31
                  local.get $p0
                  i32.load offset=24
                  local.tee $l5
                  if $I61
                    call $f69753
                    local.tee $p4
                    local.get $l5
                    local.get $p4
                    i32.load
                    i32.load offset=12
                    call_indirect $__indirect_function_table (type $t1)
                  end
                  local.get $p0
                  i32.const 0
                  i32.store offset=24
                  local.get $p0
                  i32.const -1
                  local.get $l10
                  local.get $l10
                  i32.add
                  local.tee $l5
                  local.get $l5
                  local.get $l10
                  i32.lt_u
                  select
                  local.tee $l5
                  if $I62 (result i32)
                    call $f69753
                    local.tee $p4
                    local.get $l5
                    i32.const 3215196
                    i32.const 3214888
                    i32.const 4700888
                    i32.load
                    local.tee $l12
                    local.get $l12
                    i32.load
                    i32.load offset=20
                    call_indirect $__indirect_function_table (type $t5)
                    select
                    i32.const 3214126
                    i32.const 634
                    local.get $p4
                    i32.load
                    i32.load offset=8
                    call_indirect $__indirect_function_table (type $t9)
                  else
                    i32.const 0
                  end
                  i32.store offset=24
                  local.get $p0
                  i32.load offset=20
                  local.tee $p4
                  if $I63
                    call $f69753
                    local.tee $l12
                    local.get $p4
                    local.get $l12
                    i32.load
                    i32.load offset=12
                    call_indirect $__indirect_function_table (type $t1)
                  end
                  i32.const 0
                  local.set $l29
                  local.get $p0
                  i32.const 0
                  i32.store offset=20
                  local.get $p0
                  local.get $l5
                  if $I64 (result i32)
                    call $f69753
                    local.tee $p4
                    local.get $l5
                    i32.const 3215196
                    i32.const 3214888
                    i32.const 4700888
                    i32.load
                    local.tee $l12
                    local.get $l12
                    i32.load
                    i32.load offset=20
                    call_indirect $__indirect_function_table (type $t5)
                    select
                    i32.const 3214126
                    i32.const 638
                    local.get $p4
                    i32.load
                    i32.load offset=8
                    call_indirect $__indirect_function_table (type $t9)
                  else
                    i32.const 0
                  end
                  i32.store offset=20
                  local.get $p0
                  i32.load offset=28
                  i32.const 0
                  i32.store16 offset=36
                  block $B65
                    local.get $l10
                    if $I66
                      local.get $p0
                      i32.load offset=24
                      local.set $l17
                      i32.const 0
                      local.set $l5
                      i32.const -1
                      local.set $l19
                      i32.const -1
                      local.set $l22
                      i32.const -1
                      local.set $l21
                      i32.const 0
                      local.set $l16
                      loop $L67
                        local.get $l25
                        local.get $l31
                        local.get $l5
                        i32.const 2
                        i32.shl
                        local.tee $l12
                        i32.add
                        i32.load
                        local.tee $p4
                        i32.add
                        i32.load8_u
                        local.set $l28
                        local.get $l6
                        local.get $p4
                        i32.const 2
                        i32.shl
                        local.tee $p4
                        i32.add
                        i32.load
                        local.set $l8
                        local.get $p4
                        local.get $l9
                        i32.add
                        i32.load
                        local.set $l14
                        local.get $p4
                        local.get $l11
                        i32.add
                        i32.load
                        local.set $p1
                        block $B68 (result i32)
                          local.get $l21
                          local.get $p4
                          local.get $l18
                          i32.add
                          i32.load
                          local.tee $p4
                          i32.eq
                          local.get $l8
                          local.get $l22
                          i32.eq
                          i32.and
                          i32.eqz
                          if $I69
                            local.get $l16
                            i32.const 1
                            i32.ne
                            i32.const 0
                            local.get $l5
                            select
                            i32.eqz
                            if $I70
                              local.get $l17
                              local.get $p4
                              local.get $l8
                              local.get $l28
                              i32.const 255
                              i32.and
                              local.tee $l16
                              select
                              i32.store16 offset=2
                              local.get $l17
                              local.get $l8
                              local.get $p4
                              local.get $l16
                              select
                              i32.store16
                              local.get $l17
                              i32.const 4
                              i32.add
                              local.set $l17
                              local.get $l29
                              i32.const 1
                              i32.add
                              local.tee $l29
                              i32.const 65535
                              i32.and
                              local.set $l28
                              local.get $p4
                              local.set $l21
                              local.get $l8
                              local.set $l22
                              local.get $p1
                              local.set $l19
                              i32.const 0
                              br $B68
                            end
                            i32.const 0
                            local.set $l5
                            i32.const 4700888
                            i32.load
                            i32.const 32
                            i32.const 3214126
                            i32.const 674
                            i32.const 3214799
                            i32.const 0
                            call $f69760
                            br $B65
                          end
                          local.get $l29
                          i32.const 65535
                          i32.and
                          local.tee $l28
                          i32.const 1
                          i32.shl
                          local.tee $p4
                          local.get $p0
                          i32.load offset=12
                          i32.add
                          i32.const 2
                          i32.sub
                          local.get $l19
                          i32.store8
                          local.get $p4
                          local.get $p0
                          i32.load offset=12
                          i32.add
                          i32.const 1
                          i32.sub
                          local.get $p1
                          i32.store8
                          local.get $l16
                          i32.const 1
                          i32.add
                        end
                        local.set $l16
                        local.get $p0
                        i32.load offset=20
                        local.get $l14
                        local.get $p0
                        i32.load offset=4
                        local.get $p1
                        i32.const 20
                        i32.mul
                        i32.add
                        i32.load16_u offset=16
                        i32.add
                        i32.const 1
                        i32.shl
                        i32.add
                        local.get $l5
                        i32.const 1
                        i32.shr_u
                        i32.store16
                        local.get $l12
                        local.get $l34
                        i32.add
                        local.get $p1
                        i32.store
                        local.get $l12
                        local.get $l35
                        i32.add
                        local.get $l14
                        i32.store
                        local.get $l12
                        local.get $l27
                        i32.add
                        local.get $l28
                        i32.const 1
                        i32.sub
                        i32.store
                        local.get $l5
                        i32.const 1
                        i32.add
                        local.tee $l5
                        local.get $l10
                        i32.ne
                        br_if $L67
                      end
                    end
                    local.get $p0
                    i32.load offset=28
                    local.get $l29
                    i32.store16 offset=36
                    block $B71
                      local.get $l13
                      i32.eqz
                      br_if $B71
                      local.get $l30
                      local.get $l35
                      local.get $l10
                      i32.const 1
                      call $f69795
                      local.get $l34
                      local.get $l10
                      i32.const 1
                      call $f69795
                      local.set $l5
                      block $B72
                        local.get $l10
                        i32.eqz
                        br_if $B72
                        local.get $l5
                        i32.load offset=8
                        local.set $p4
                        local.get $l10
                        i32.const 3
                        i32.and
                        local.set $p1
                        i32.const 0
                        local.set $l5
                        local.get $l10
                        i32.const 1
                        i32.sub
                        i32.const 3
                        i32.ge_u
                        if $I73
                          local.get $l10
                          i32.const -4
                          i32.and
                          local.set $l8
                          loop $L74
                            local.get $l20
                            local.get $l5
                            i32.const 2
                            i32.shl
                            local.tee $l12
                            i32.add
                            local.get $l27
                            local.get $p4
                            local.get $l12
                            i32.add
                            i32.load
                            i32.const 2
                            i32.shl
                            i32.add
                            i32.load
                            i32.store
                            local.get $l20
                            local.get $l12
                            i32.const 4
                            i32.or
                            local.tee $l14
                            i32.add
                            local.get $l27
                            local.get $p4
                            local.get $l14
                            i32.add
                            i32.load
                            i32.const 2
                            i32.shl
                            i32.add
                            i32.load
                            i32.store
                            local.get $l20
                            local.get $l12
                            i32.const 8
                            i32.or
                            local.tee $l14
                            i32.add
                            local.get $l27
                            local.get $p4
                            local.get $l14
                            i32.add
                            i32.load
                            i32.const 2
                            i32.shl
                            i32.add
                            i32.load
                            i32.store
                            local.get $l20
                            local.get $l12
                            i32.const 12
                            i32.or
                            local.tee $l12
                            i32.add
                            local.get $l27
                            local.get $p4
                            local.get $l12
                            i32.add
                            i32.load
                            i32.const 2
                            i32.shl
                            i32.add
                            i32.load
                            i32.store
                            local.get $l5
                            i32.const 4
                            i32.add
                            local.set $l5
                            local.get $l8
                            i32.const 4
                            i32.sub
                            local.tee $l8
                            br_if $L74
                          end
                        end
                        local.get $p1
                        i32.eqz
                        br_if $B72
                        loop $L75
                          local.get $l20
                          local.get $l5
                          i32.const 2
                          i32.shl
                          local.tee $l12
                          i32.add
                          local.get $l27
                          local.get $p4
                          local.get $l12
                          i32.add
                          i32.load
                          i32.const 2
                          i32.shl
                          i32.add
                          i32.load
                          i32.store
                          local.get $l5
                          i32.const 1
                          i32.add
                          local.set $l5
                          local.get $p1
                          i32.const 1
                          i32.sub
                          local.tee $p1
                          br_if $L75
                        end
                      end
                      block $B76 (result i32)
                        local.get $p0
                        i32.load offset=28
                        i32.load16_u offset=36
                        i32.const 32767
                        i32.and
                        local.tee $l5
                        i32.eqz
                        if $I77
                          i32.const 0
                          local.set $p4
                          i32.const 0
                          br $B76
                        end
                        call $f69753
                        local.tee $p4
                        local.get $l5
                        i32.const 3
                        i32.shl
                        i32.const 3215298
                        i32.const 3214888
                        i32.const 4700888
                        i32.load
                        local.tee $l5
                        local.get $l5
                        i32.load
                        i32.load offset=20
                        call_indirect $__indirect_function_table (type $t5)
                        select
                        i32.const 3214126
                        i32.const 724
                        local.get $p4
                        i32.load
                        i32.load offset=8
                        call_indirect $__indirect_function_table (type $t9)
                        local.set $p4
                        local.get $p0
                        i32.load offset=28
                        i32.load16_u offset=36
                        i32.const 32767
                        i32.and
                        i32.const 3
                        i32.shl
                      end
                      local.set $l5
                      local.get $p4
                      i32.const 0
                      local.get $l5
                      call $f484
                      local.set $l5
                      block $B78
                        local.get $l10
                        i32.eqz
                        br_if $B78
                        local.get $l10
                        i32.const 3
                        i32.and
                        local.set $p4
                        local.get $l10
                        i32.const 1
                        i32.sub
                        i32.const 3
                        i32.ge_u
                        if $I79
                          local.get $l10
                          i32.const -4
                          i32.and
                          local.set $l12
                          loop $L80
                            local.get $l5
                            local.get $l20
                            i32.load
                            i32.const 3
                            i32.shl
                            i32.add
                            local.tee $p1
                            local.get $p1
                            i32.load16_u offset=2
                            i32.const 1
                            i32.add
                            i32.store16 offset=2
                            local.get $l5
                            local.get $l20
                            i32.load offset=4
                            i32.const 3
                            i32.shl
                            i32.add
                            local.tee $p1
                            local.get $p1
                            i32.load16_u offset=2
                            i32.const 1
                            i32.add
                            i32.store16 offset=2
                            local.get $l5
                            local.get $l20
                            i32.load offset=8
                            i32.const 3
                            i32.shl
                            i32.add
                            local.tee $p1
                            local.get $p1
                            i32.load16_u offset=2
                            i32.const 1
                            i32.add
                            i32.store16 offset=2
                            local.get $l5
                            local.get $l20
                            i32.load offset=12
                            i32.const 3
                            i32.shl
                            i32.add
                            local.tee $p1
                            local.get $p1
                            i32.load16_u offset=2
                            i32.const 1
                            i32.add
                            i32.store16 offset=2
                            local.get $l20
                            i32.const 16
                            i32.add
                            local.set $l20
                            local.get $l12
                            i32.const 4
                            i32.sub
                            local.tee $l12
                            br_if $L80
                          end
                        end
                        local.get $p4
                        i32.eqz
                        br_if $B78
                        loop $L81
                          local.get $l5
                          local.get $l20
                          i32.load
                          i32.const 3
                          i32.shl
                          i32.add
                          local.tee $l12
                          local.get $l12
                          i32.load16_u offset=2
                          i32.const 1
                          i32.add
                          i32.store16 offset=2
                          local.get $l20
                          i32.const 4
                          i32.add
                          local.set $l20
                          local.get $p4
                          i32.const 1
                          i32.sub
                          local.tee $p4
                          br_if $L81
                        end
                      end
                      block $B82
                        local.get $p0
                        i32.load offset=28
                        i32.load16_u offset=36
                        i32.const 32767
                        i32.and
                        local.tee $l12
                        if $I83
                          i32.const 0
                          local.set $p4
                          loop $L84
                            local.get $l5
                            local.get $p4
                            i32.const 3
                            i32.shl
                            i32.add
                            i32.load16_u offset=2
                            i32.const 2
                            i32.eq
                            if $I85
                              local.get $l12
                              local.get $p4
                              i32.const 1
                              i32.add
                              local.tee $p4
                              i32.ne
                              br_if $L84
                              br $B82
                            end
                          end
                          i32.const 0
                          local.set $l5
                          i32.const 4700888
                          i32.load
                          i32.const 32
                          i32.const 3214126
                          i32.const 738
                          i32.const 3214799
                          i32.const 0
                          call $f69760
                          br $B65
                        end
                        local.get $l5
                        i32.eqz
                        br_if $B71
                      end
                      call $f69753
                      local.tee $p4
                      local.get $l5
                      local.get $p4
                      i32.load
                      i32.load offset=12
                      call_indirect $__indirect_function_table (type $t1)
                    end
                    local.get $l18
                    if $I86
                      call $f69753
                      local.tee $l5
                      local.get $l18
                      local.get $l5
                      i32.load
                      i32.load offset=12
                      call_indirect $__indirect_function_table (type $t1)
                    end
                    i32.const 1
                    local.set $l5
                    local.get $l25
                    i32.eqz
                    br_if $B65
                    call $f69753
                    local.tee $p4
                    local.get $l25
                    local.get $p4
                    i32.load
                    i32.load offset=12
                    call_indirect $__indirect_function_table (type $t1)
                  end
                  local.get $l30
                  call $f69792
                  drop
                end
                local.get $l32
                i32.const 48
                i32.add
                global.set $g0
                local.get $l5
                br_if $B48
                br $B47
              end
              local.get $p0
              i32.load offset=28
              local.get $p4
              i32.const 1
              i32.shr_u
              i32.store16 offset=36
            end
            local.get $l24
            if $I87
              i32.const 0
              local.set $l14
              loop $L88
                local.get $p0
                i32.load offset=4
                local.set $l16
                i32.const 255
                local.set $l10
                block $B89
                  local.get $p0
                  i32.load offset=28
                  i32.load8_u offset=38
                  local.tee $p1
                  i32.eqz
                  br_if $B89
                  local.get $p1
                  i32.const 1
                  i32.and
                  local.set $l18
                  local.get $l16
                  local.get $l14
                  i32.const 20
                  i32.mul
                  i32.add
                  local.tee $l7
                  f32.load offset=8
                  local.set $l44
                  local.get $l7
                  f32.load offset=4
                  local.set $l45
                  local.get $l7
                  f32.load
                  local.set $l46
                  local.get $p0
                  i32.load
                  local.set $l7
                  block $B90
                    local.get $p1
                    i32.const 1
                    i32.eq
                    if $I91
                      f32.const 0x1.fffffep+127 (;=3.40282e+38;)
                      local.set $l42
                      i32.const 0
                      local.set $p1
                      br $B90
                    end
                    local.get $p1
                    i32.const 254
                    i32.and
                    local.set $l8
                    f32.const 0x1.fffffep+127 (;=3.40282e+38;)
                    local.set $l42
                    i32.const 0
                    local.set $p1
                    loop $L92
                      local.get $l7
                      f32.load offset=12
                      local.get $l46
                      f32.mul
                      local.get $l7
                      f32.load offset=16
                      local.get $l45
                      f32.mul
                      f32.add
                      local.get $l7
                      f32.load offset=20
                      local.get $l44
                      f32.mul
                      f32.add
                      local.tee $l47
                      local.get $l7
                      f32.load
                      local.get $l46
                      f32.mul
                      local.get $l7
                      f32.load offset=4
                      local.get $l45
                      f32.mul
                      f32.add
                      local.get $l7
                      f32.load offset=8
                      local.get $l44
                      f32.mul
                      f32.add
                      local.tee $l41
                      local.get $l42
                      local.get $l41
                      local.get $l42
                      f32.lt
                      local.tee $l17
                      select
                      local.tee $l42
                      local.get $l42
                      local.get $l47
                      f32.gt
                      local.tee $l19
                      select
                      local.set $l42
                      local.get $p1
                      i32.const 1
                      i32.or
                      local.get $p1
                      local.get $l10
                      local.get $l17
                      select
                      local.get $l19
                      select
                      local.set $l10
                      local.get $p1
                      i32.const 2
                      i32.add
                      local.set $p1
                      local.get $l7
                      i32.const 24
                      i32.add
                      local.set $l7
                      local.get $l8
                      i32.const 2
                      i32.sub
                      local.tee $l8
                      i32.const 255
                      i32.and
                      br_if $L92
                    end
                  end
                  local.get $l18
                  i32.eqz
                  br_if $B89
                  local.get $p1
                  local.get $l10
                  local.get $l7
                  f32.load
                  local.get $l46
                  f32.mul
                  local.get $l7
                  f32.load offset=4
                  local.get $l45
                  f32.mul
                  f32.add
                  local.get $l7
                  f32.load offset=8
                  local.get $l44
                  f32.mul
                  f32.add
                  local.get $l42
                  f32.lt
                  select
                  local.set $l10
                end
                local.get $l16
                local.get $l14
                i32.const 20
                i32.mul
                i32.add
                local.get $l10
                i32.store8 offset=19
                local.get $l14
                i32.const 1
                i32.add
                local.tee $l14
                local.get $l24
                i32.ne
                br_if $L88
              end
            end
            i32.const 1
            local.set $l7
            local.get $l13
            i32.eqz
            br_if $B47
            local.get $p0
            call $f72871
            br $B35
          end
          local.get $l7
        end
        local.tee $p4
        i32.eqz
        if $I93
          i32.const 4700888
          i32.load
          i32.const 32
          i32.const 3215716
          i32.const 312
          i32.const 3216007
          i32.const 0
          call $f69760
          br $B34
        end
        local.get $l15
        i32.load16_u offset=36
        i32.const 64
        i32.and
        i32.const 6
        i32.shr_u
        local.set $l9
        i32.const 0
        local.set $l8
        global.get $g0
        i32.const 272
        i32.sub
        local.tee $p1
        global.set $g0
        block $B94
          block $B95
            block $B96
              local.get $p0
              f32.load offset=112
              f32.const 0x0p+0 (;=0;)
              f32.le
              if $I97
                local.get $p1
                i64.const 0
                i64.store offset=86 align=2
                local.get $p1
                i32.const 16711935
                i32.store offset=94 align=2
                local.get $p1
                i64.const 0
                i64.store offset=80
                local.get $p1
                local.get $p0
                i32.load8_u offset=82
                local.tee $l5
                i32.store offset=64
                local.get $p0
                i32.load
                local.set $l6
                local.get $p1
                i32.const 12
                i32.store offset=56
                local.get $p1
                local.get $l6
                i32.store offset=60
                local.get $p1
                local.get $p0
                i32.load offset=4
                i32.store offset=72
                local.get $p1
                i32.const 20
                i32.store offset=68
                local.get $p1
                local.get $p0
                i32.load offset=28
                i32.load8_u offset=39
                i32.store offset=76
                local.get $p1
                local.get $p0
                i32.load offset=8
                i32.store offset=84
                local.get $l5
                i32.eqz
                br_if $B95
                local.get $l5
                i32.const 1
                i32.and
                local.set $l12
                local.get $l5
                i32.const 1
                i32.eq
                br_if $B96
                local.get $l5
                i32.const 254
                i32.and
                local.set $l11
                loop $L98
                  local.get $l6
                  local.get $l8
                  i32.const 1
                  i32.or
                  i32.const 12
                  i32.mul
                  i32.add
                  local.tee $l7
                  f32.load offset=8
                  local.get $l6
                  local.get $l8
                  i32.const 12
                  i32.mul
                  i32.add
                  local.tee $l15
                  f32.load offset=8
                  local.get $l37
                  f32.add
                  f32.add
                  local.set $l37
                  local.get $l7
                  f32.load offset=4
                  local.get $l15
                  f32.load offset=4
                  local.get $l38
                  f32.add
                  f32.add
                  local.set $l38
                  local.get $l7
                  f32.load
                  local.get $l15
                  f32.load
                  local.get $l36
                  f32.add
                  f32.add
                  local.set $l36
                  local.get $l8
                  i32.const 2
                  i32.add
                  local.set $l8
                  local.get $l11
                  i32.const 2
                  i32.sub
                  local.tee $l11
                  br_if $L98
                end
                br $B96
              end
              local.get $p1
              i32.const 272
              i32.add
              global.set $g0
              br $B94
            end
            local.get $l12
            i32.eqz
            br_if $B95
            local.get $l6
            local.get $l8
            i32.const 12
            i32.mul
            i32.add
            local.tee $l8
            f32.load
            local.get $l36
            f32.add
            local.set $l36
            local.get $l8
            f32.load offset=4
            local.get $l38
            f32.add
            local.set $l38
            local.get $l8
            f32.load offset=8
            local.get $l37
            f32.add
            local.set $l37
          end
          local.get $p1
          f32.const 0x1p+0 (;=1;)
          local.get $l5
          f32.convert_i32_u
          f32.div
          local.tee $l41
          local.get $l37
          f32.mul
          f32.store offset=48
          local.get $p1
          local.get $l41
          local.get $l38
          f32.mul
          f32.store offset=44
          local.get $p1
          local.get $l41
          local.get $l36
          f32.mul
          f32.store offset=40
          block $B99
            local.get $l9
            if $I100
              local.get $p1
              i32.const 56
              i32.add
              local.get $p1
              i32.const 104
              i32.add
              local.get $p1
              i32.const 40
              i32.add
              call $f72879
              drop
              br $B99
            end
            local.get $p1
            i32.const 56
            i32.add
            local.get $p1
            i32.const 104
            i32.add
            local.get $p1
            i32.const 40
            i32.add
            call $f72880
            drop
          end
          local.get $p0
          local.get $p1
          f64.load offset=128
          f32.demote_f64
          local.tee $l37
          f32.store offset=116
          local.get $p0
          local.get $p1
          f64.load offset=152
          f32.demote_f64
          local.tee $l38
          f32.store offset=120
          local.get $p0
          local.get $p1
          f64.load offset=176
          f32.demote_f64
          local.tee $l36
          f32.store offset=124
          local.get $p0
          local.get $p1
          f64.load offset=136
          f32.demote_f64
          local.tee $l41
          f32.store offset=128
          local.get $p0
          local.get $p1
          f64.load offset=160
          f32.demote_f64
          local.tee $l39
          f32.store offset=132
          local.get $p0
          local.get $p1
          f64.load offset=184
          f32.demote_f64
          local.tee $l40
          f32.store offset=136
          local.get $p0
          local.get $p1
          f64.load offset=144
          f32.demote_f64
          local.tee $l43
          f32.store offset=140
          local.get $p0
          local.get $p1
          f64.load offset=168
          f32.demote_f64
          local.tee $l42
          f32.store offset=144
          local.get $p0
          local.get $p1
          f64.load offset=192
          f32.demote_f64
          local.tee $l44
          f32.store offset=148
          local.get $p0
          local.get $p1
          f32.load offset=104
          local.tee $l45
          f32.store offset=68
          local.get $p0
          local.get $p1
          f32.load offset=108
          local.tee $l46
          f32.store offset=72
          local.get $p0
          local.get $p1
          f32.load offset=112
          local.tee $l47
          f32.store offset=76
          block $B101
            block $B102
              local.get $l37
              i32.reinterpret_f32
              i32.const 2139095040
              i32.and
              i32.const 2139095040
              i32.eq
              br_if $B102
              local.get $l38
              i32.reinterpret_f32
              i32.const 2139095040
              i32.and
              i32.const 2139095040
              i32.eq
              br_if $B102
              local.get $l36
              i32.reinterpret_f32
              i32.const 2139095040
              i32.and
              i32.const 2139095040
              i32.eq
              br_if $B102
              local.get $l41
              i32.reinterpret_f32
              i32.const 2139095040
              i32.and
              i32.const 2139095040
              i32.eq
              br_if $B102
              local.get $l39
              i32.reinterpret_f32
              i32.const 2139095040
              i32.and
              i32.const 2139095040
              i32.eq
              br_if $B102
              local.get $l40
              i32.reinterpret_f32
              i32.const 2139095040
              i32.and
              i32.const 2139095040
              i32.eq
              br_if $B102
              local.get $l43
              i32.reinterpret_f32
              i32.const 2139095040
              i32.and
              i32.const 2139095040
              i32.eq
              br_if $B102
              local.get $l42
              i32.reinterpret_f32
              i32.const 2139095040
              i32.and
              i32.const 2139095040
              i32.eq
              br_if $B102
              local.get $l44
              i32.reinterpret_f32
              i32.const 2139095040
              i32.and
              i32.const 2139095040
              i32.eq
              br_if $B102
              local.get $l45
              i32.reinterpret_f32
              i32.const 2139095040
              i32.and
              i32.const 2139095040
              i32.eq
              br_if $B102
              local.get $l46
              i32.reinterpret_f32
              i32.const 2139095040
              i32.and
              i32.const 2139095040
              i32.eq
              br_if $B102
              local.get $l47
              i32.reinterpret_f32
              i32.const 2139095040
              i32.and
              i32.const 2139095040
              i32.eq
              br_if $B102
              local.get $p1
              f64.load offset=120
              local.tee $l49
              f32.demote_f64
              local.tee $l37
              i32.reinterpret_f32
              i32.const 2139095040
              i32.and
              i32.const 2139095040
              i32.eq
              br_if $B102
              local.get $p0
              local.get $l49
              f64.const 0x0p+0 (;=0;)
              f64.lt
              if $I103 (result f32)
                i32.const 4700888
                i32.load
                i32.const 2
                i32.const 3215716
                i32.const 233
                i32.const 3215830
                i32.const 0
                call $f69760
                local.get $p1
                local.get $p1
                f64.load offset=120
                f64.neg
                f64.store offset=120
                local.get $p0
                i32.const 116
                i32.add
                local.tee $l9
                f32.load offset=16
                local.set $l37
                local.get $l9
                f32.load offset=20
                local.set $l38
                local.get $l9
                f32.load offset=28
                local.set $l36
                local.get $l9
                f32.load offset=32
                local.set $l41
                local.get $l9
                f32.load
                local.set $l39
                local.get $l9
                f32.load offset=4
                local.set $l40
                local.get $l9
                f32.load offset=8
                local.set $l43
                local.get $l9
                f32.load offset=12
                local.set $l42
                local.get $p1
                local.get $l9
                f32.load offset=24
                f32.neg
                f32.store offset=24
                local.get $p1
                local.get $l42
                f32.neg
                f32.store offset=12
                local.get $p1
                local.get $l43
                f32.neg
                f32.store offset=8
                local.get $p1
                local.get $l40
                f32.neg
                f32.store offset=4
                local.get $p1
                local.get $l39
                f32.neg
                f32.store
                local.get $p1
                local.get $l41
                f32.neg
                f32.store offset=32
                local.get $p1
                local.get $l36
                f32.neg
                f32.store offset=28
                local.get $p1
                local.get $l38
                f32.neg
                f32.store offset=20
                local.get $p1
                local.get $l37
                f32.neg
                f32.store offset=16
                local.get $p0
                local.get $p1
                f32.load
                f32.store offset=116
                local.get $p0
                local.get $p1
                f32.load offset=4
                f32.store offset=120
                local.get $p0
                local.get $p1
                f32.load offset=8
                f32.store offset=124
                local.get $p0
                local.get $p1
                f32.load offset=12
                f32.store offset=128
                local.get $p0
                local.get $p1
                f32.load offset=16
                f32.store offset=132
                local.get $p0
                local.get $p1
                f32.load offset=20
                f32.store offset=136
                local.get $p0
                local.get $p1
                f32.load offset=24
                f32.store offset=140
                local.get $p0
                local.get $p1
                f32.load offset=28
                f32.store offset=144
                local.get $p0
                local.get $p1
                f32.load offset=32
                f32.store offset=148
                local.get $p1
                f64.load offset=120
                f32.demote_f64
              else
                local.get $l37
              end
              f32.store offset=112
              br $B101
            end
            i32.const 4700888
            i32.load
            i32.const 32
            i32.const 3215716
            i32.const 242
            i32.const 3215952
            i32.const 0
            call $f69760
          end
          local.get $p1
          i32.const 272
          i32.add
          global.set $g0
        end
      end
      local.get $l23
      i32.const 32
      i32.add
      global.set $g0
      i32.const 0
      local.get $p4
      i32.eqz
      br_if $B0
      drop
      local.get $l26
      i32.const 8
      i32.add
      local.get $p0
      i32.const 82
      i32.add
      local.tee $p1
      i32.load8_u
      local.get $p0
      i32.load
      call $f70401
      local.get $l26
      f32.load offset=24
      local.set $l37
      local.get $l26
      f32.load offset=20
      local.set $l38
      local.get $l26
      f32.load offset=8
      local.set $l36
      local.get $l26
      f32.load offset=12
      local.set $l41
      local.get $p0
      i32.const -64
      i32.sub
      local.get $l26
      f32.load offset=28
      local.tee $l39
      local.get $l26
      f32.load offset=16
      local.tee $l40
      f32.sub
      f32.const 0x1p-1 (;=0.5;)
      f32.mul
      f32.store
      local.get $p0
      local.get $l37
      local.get $l41
      f32.sub
      f32.const 0x1p-1 (;=0.5;)
      f32.mul
      f32.store offset=60
      local.get $p0
      local.get $l38
      local.get $l36
      f32.sub
      f32.const 0x1p-1 (;=0.5;)
      f32.mul
      f32.store offset=56
      local.get $p0
      local.get $l40
      local.get $l39
      f32.add
      f32.const 0x1p-1 (;=0.5;)
      f32.mul
      f32.store offset=52
      local.get $p0
      local.get $l41
      local.get $l37
      f32.add
      f32.const 0x1p-1 (;=0.5;)
      f32.mul
      f32.store offset=48
      local.get $p0
      local.get $l36
      local.get $l38
      f32.add
      f32.const 0x1p-1 (;=0.5;)
      f32.mul
      f32.store offset=44
      local.get $p2
      local.get $p1
      i32.load8_u
      i32.lt_u
      if $I104
        global.get $g0
        i32.const 16
        i32.sub
        local.tee $p4
        global.set $g0
        local.get $p0
        i32.load offset=108
        local.tee $p1
        if $I105
          local.get $p1
          call $f69919
          local.set $p1
          call $f69753
          local.tee $p2
          local.get $p1
          local.get $p2
          i32.load
          i32.load offset=12
          call_indirect $__indirect_function_table (type $t1)
        end
        call $f69753
        local.tee $p1
        i32.const 28
        i32.const 3216870
        i32.const 3216558
        i32.const 4700888
        i32.load
        local.tee $p2
        local.get $p2
        i32.load
        i32.load offset=20
        call_indirect $__indirect_function_table (type $t5)
        select
        i32.const 3215716
        i32.const 388
        local.get $p1
        i32.load
        i32.load offset=8
        call_indirect $__indirect_function_table (type $t9)
        local.tee $p1
        call $f69918
        local.get $p0
        local.get $p1
        i32.store offset=108
        local.get $p0
        i32.load
        local.set $p2
        local.get $p4
        local.get $p1
        i32.store offset=4
        local.get $p4
        local.get $p2
        i32.store offset=8
        local.get $p4
        local.get $p0
        i32.const 44
        i32.add
        i32.store
        i32.const 0
        local.set $p2
        i32.const 0
        local.set $l7
        i32.const 0
        local.set $l15
        global.get $g0
        i32.const 256
        i32.sub
        local.tee $l8
        global.set $g0
        local.get $p4
        i32.load offset=4
        local.get $p0
        i32.load offset=28
        i32.load8_u offset=38
        local.tee $p1
        i32.store offset=8
        local.get $p1
        i32.const 2
        i32.shl
        local.tee $l5
        i32.const 12
        i32.add
        i32.const 2032
        i32.and
        local.tee $l6
        local.get $p0
        i32.load offset=28
        i32.load16_u offset=36
        i32.const 1
        i32.shl
        i32.const 65534
        i32.and
        i32.add
        local.tee $l12
        if $I106
          call $f69753
          local.tee $p2
          local.get $l12
          i32.const 3216437
          i32.const 3215418
          i32.const 118
          local.get $p2
          i32.load
          i32.load offset=8
          call_indirect $__indirect_function_table (type $t9)
          local.set $p2
        end
        local.get $p4
        i32.load offset=4
        local.get $p2
        i32.store offset=24
        local.get $p4
        i32.load offset=4
        local.tee $p2
        local.get $p2
        i32.load offset=24
        i32.store offset=16
        local.get $p4
        i32.load offset=4
        local.tee $p2
        local.get $p2
        i32.load offset=24
        local.get $l6
        i32.add
        i32.store offset=20
        local.get $p4
        i32.load offset=4
        i32.load offset=16
        i32.const 0
        local.get $l5
        call $f484
        drop
        local.get $l8
        i32.const 0
        local.get $p1
        call $f484
        local.set $l14
        local.get $p0
        i32.load offset=28
        local.tee $p1
        i32.load8_u offset=39
        if $I107
          loop $L108
            local.get $p0
            i32.load offset=4
            local.get $l7
            i32.const 20
            i32.mul
            i32.add
            local.tee $p2
            i32.load8_u offset=18
            local.tee $l8
            if $I109
              local.get $p0
              i32.load offset=8
              local.get $p2
              i32.load16_u offset=16
              i32.add
              local.set $p2
              local.get $l8
              i32.const 1
              i32.and
              local.set $l6
              i32.const 0
              local.set $p1
              local.get $l8
              i32.const 1
              i32.ne
              if $I110
                local.get $l8
                i32.const 254
                i32.and
                local.set $l8
                loop $L111
                  local.get $p4
                  i32.load offset=4
                  i32.load offset=16
                  local.get $p1
                  local.get $p2
                  i32.add
                  i32.load8_u
                  i32.const 2
                  i32.shl
                  i32.add
                  local.tee $l5
                  local.get $l5
                  i32.load16_u
                  i32.const 1
                  i32.add
                  i32.store16
                  local.get $p4
                  i32.load offset=4
                  i32.load offset=16
                  local.get $p2
                  local.get $p1
                  i32.const 1
                  i32.or
                  i32.add
                  i32.load8_u
                  i32.const 2
                  i32.shl
                  i32.add
                  local.tee $l5
                  local.get $l5
                  i32.load16_u
                  i32.const 1
                  i32.add
                  i32.store16
                  local.get $p1
                  i32.const 2
                  i32.add
                  local.set $p1
                  local.get $l8
                  i32.const 2
                  i32.sub
                  local.tee $l8
                  br_if $L111
                end
              end
              local.get $l6
              if $I112
                local.get $p4
                i32.load offset=4
                i32.load offset=16
                local.get $p1
                local.get $p2
                i32.add
                i32.load8_u
                i32.const 2
                i32.shl
                i32.add
                local.tee $p1
                local.get $p1
                i32.load16_u
                i32.const 1
                i32.add
                i32.store16
              end
              local.get $p0
              i32.load offset=28
              local.set $p1
            end
            local.get $l7
            i32.const 1
            i32.add
            local.tee $l7
            local.get $p1
            i32.load8_u offset=39
            i32.lt_u
            br_if $L108
          end
        end
        local.get $p4
        i32.load offset=4
        call $f69920
        local.get $p4
        i32.load offset=4
        local.tee $p1
        local.get $p1
        i32.load offset=16
        local.get $p1
        i32.load offset=8
        i32.const 2
        i32.shl
        i32.add
        i32.const 4
        i32.sub
        local.tee $p1
        i32.load16_u
        local.get $p1
        i32.load16_u offset=2
        i32.add
        i32.store offset=12
        local.get $p0
        i32.load offset=28
        local.tee $p1
        i32.load8_u offset=39
        if $I113
          local.get $p0
          i32.load offset=4
          local.set $l13
          loop $L114
            local.get $l13
            local.get $l15
            i32.const 20
            i32.mul
            local.tee $l19
            i32.add
            local.tee $p2
            i32.load8_u offset=18
            local.tee $l23
            if $I115
              local.get $p0
              i32.load offset=8
              local.get $p2
              i32.load16_u offset=16
              i32.add
              local.set $l16
              i32.const 0
              local.set $p1
              loop $L116
                local.get $p1
                i32.const 1
                i32.add
                local.set $l9
                local.get $l14
                local.get $p1
                local.get $l16
                i32.add
                i32.load8_u
                local.tee $l7
                i32.add
                local.tee $l22
                i32.load8_u
                i32.eqz
                if $I117
                  local.get $l16
                  i32.const 0
                  local.get $l9
                  local.get $l9
                  local.get $l23
                  i32.eq
                  select
                  i32.add
                  i32.load8_u
                  local.set $l11
                  i32.const 1
                  local.set $l10
                  local.get $p4
                  i32.load offset=4
                  local.tee $p2
                  i32.load offset=20
                  local.set $l8
                  local.get $l7
                  i32.const 2
                  i32.shl
                  local.tee $l21
                  local.get $p2
                  i32.load offset=16
                  i32.add
                  local.tee $p2
                  local.get $p2
                  i32.load16_u offset=2
                  local.tee $p2
                  i32.const 1
                  i32.add
                  i32.store16 offset=2
                  local.get $p2
                  local.get $l8
                  i32.add
                  local.get $l11
                  i32.store8
                  local.get $p0
                  i32.load offset=12
                  local.tee $l12
                  local.get $p0
                  i32.load offset=20
                  local.tee $l17
                  local.get $p1
                  local.get $p0
                  i32.load offset=4
                  local.tee $l13
                  local.get $l19
                  i32.add
                  i32.load16_u offset=16
                  i32.add
                  i32.const 1
                  i32.shl
                  i32.add
                  i32.load16_u
                  i32.const 1
                  i32.shl
                  i32.const 65534
                  i32.and
                  local.tee $p1
                  i32.const 1
                  i32.or
                  i32.add
                  i32.load8_u
                  local.get $p1
                  local.get $l12
                  i32.add
                  i32.load8_u
                  local.tee $p1
                  local.get $p1
                  local.get $l15
                  i32.eq
                  select
                  local.tee $l18
                  i32.const 255
                  i32.and
                  local.tee $p1
                  local.get $l15
                  i32.ne
                  if $I118
                    loop $L119
                      local.get $l13
                      local.get $p1
                      i32.const 20
                      i32.mul
                      local.tee $l24
                      i32.add
                      local.tee $p1
                      i32.load16_u offset=16
                      local.set $l6
                      block $B120
                        local.get $p1
                        i32.load8_u offset=18
                        local.tee $l8
                        i32.eqz
                        br_if $B120
                        local.get $p0
                        i32.load offset=8
                        local.get $l6
                        i32.add
                        local.set $l5
                        i32.const 0
                        local.set $p1
                        loop $L121
                          local.get $p1
                          i32.const 1
                          i32.add
                          local.set $p2
                          local.get $l7
                          local.get $p1
                          local.get $l5
                          i32.add
                          i32.load8_u
                          i32.eq
                          if $I122
                            local.get $l11
                            local.get $l5
                            local.get $p2
                            local.get $l8
                            i32.rem_u
                            i32.add
                            i32.load8_u
                            local.tee $l11
                            i32.eq
                            if $I123
                              local.get $l5
                              local.get $p1
                              local.get $l8
                              local.get $p1
                              select
                              i32.const 1
                              i32.sub
                              local.tee $p1
                              i32.add
                              i32.load8_u
                              local.set $l11
                            end
                            local.get $p4
                            i32.load offset=4
                            local.tee $p2
                            i32.load offset=20
                            local.set $l8
                            local.get $p2
                            i32.load offset=16
                            local.get $l21
                            i32.add
                            local.tee $p2
                            local.get $p2
                            i32.load16_u offset=2
                            local.tee $p2
                            i32.const 1
                            i32.add
                            i32.store16 offset=2
                            local.get $p2
                            local.get $l8
                            i32.add
                            local.get $l11
                            i32.store8
                            local.get $l10
                            i32.const 1
                            i32.add
                            local.set $l10
                            local.get $p1
                            local.get $p0
                            i32.load offset=4
                            local.tee $l13
                            local.get $l24
                            i32.add
                            i32.load16_u offset=16
                            i32.add
                            local.set $l6
                            local.get $p0
                            i32.load offset=12
                            local.set $l12
                            local.get $p0
                            i32.load offset=20
                            local.set $l17
                            br $B120
                          end
                          local.get $p2
                          local.tee $p1
                          local.get $l8
                          i32.ne
                          br_if $L121
                        end
                      end
                      local.get $l15
                      local.get $l12
                      local.get $l17
                      local.get $l6
                      i32.const 1
                      i32.shl
                      i32.add
                      i32.load16_u
                      i32.const 1
                      i32.shl
                      i32.const 65534
                      i32.and
                      local.tee $p1
                      i32.const 1
                      i32.or
                      i32.add
                      i32.load8_u
                      local.get $p1
                      local.get $l12
                      i32.add
                      i32.load8_u
                      local.tee $p1
                      local.get $p1
                      local.get $l18
                      i32.const 255
                      i32.and
                      i32.eq
                      select
                      local.tee $l18
                      i32.const 255
                      i32.and
                      local.tee $p1
                      i32.ne
                      br_if $L119
                    end
                  end
                  local.get $l22
                  local.get $l10
                  i32.store8
                end
                local.get $l9
                local.tee $p1
                local.get $l23
                i32.ne
                br_if $L116
              end
              local.get $p0
              i32.load offset=28
              local.set $p1
            end
            local.get $l15
            i32.const 1
            i32.add
            local.tee $l15
            local.get $p1
            i32.load8_u offset=39
            i32.lt_u
            br_if $L114
          end
        end
        local.get $p4
        i32.load offset=4
        call $f69920
        local.get $l14
        i32.const 256
        i32.add
        global.set $g0
        i32.const 0
        local.set $l11
        i32.const 0
        local.set $l8
        global.get $g0
        i32.const 208
        i32.sub
        local.tee $l6
        global.set $g0
        local.get $p4
        i32.load offset=4
        i32.const 16
        i32.store16
        local.get $p4
        i32.load offset=4
        i32.const 1536
        i32.store16 offset=2
        local.get $p4
        i32.load offset=4
        local.tee $l7
        i32.load16_u offset=2
        local.tee $p2
        if $I124 (result i32)
          call $f69753
          local.tee $l11
          local.get $p2
          i32.const 1
          i32.shl
          i32.const 3216668
          i32.const 3216558
          i32.const 4700888
          i32.load
          local.tee $l7
          local.get $l7
          i32.load
          i32.load offset=20
          call_indirect $__indirect_function_table (type $t5)
          select
          i32.const 3215418
          i32.const 69
          local.get $l11
          i32.load
          i32.load offset=8
          call_indirect $__indirect_function_table (type $t9)
          local.set $l11
          local.get $p4
          i32.load offset=4
        else
          local.get $l7
        end
        local.get $l11
        i32.store offset=4
        local.get $l6
        i32.const 0
        i32.store offset=168
        local.get $l6
        i64.const 0
        i64.store offset=160
        local.get $l6
        i32.const 0
        i32.store offset=152
        local.get $l6
        i64.const 0
        i64.store offset=144
        local.get $l6
        i32.const 200
        i32.add
        local.set $l22
        local.get $l6
        i32.const 192
        i32.add
        local.set $l21
        loop $L125
          local.get $l8
          i32.const 4
          i32.shl
          local.set $l25
          f32.const 0x1p+0 (;=1;)
          local.get $l8
          f32.convert_i32_u
          f32.const 0x1.ep+2 (;=7.5;)
          f32.div
          f32.sub
          local.tee $l41
          local.get $l41
          f32.mul
          local.set $l43
          local.get $l8
          local.set $l5
          loop $L126
            f32.const 0x1p+0 (;=1;)
            local.set $l39
            block $B127
              local.get $l43
              f32.const 0x1p+0 (;=1;)
              local.get $l5
              f32.convert_i32_u
              f32.const 0x1.ep+2 (;=7.5;)
              f32.div
              f32.sub
              local.tee $l40
              local.get $l40
              f32.mul
              f32.const 0x1p+0 (;=1;)
              f32.add
              f32.add
              f32.sqrt
              local.tee $l36
              f32.const 0x0p+0 (;=0;)
              f32.gt
              i32.eqz
              if $I128
                local.get $l41
                local.set $l36
                br $B127
              end
              local.get $l41
              f32.const 0x1p+0 (;=1;)
              local.get $l36
              f32.div
              local.tee $l39
              f32.mul
              local.set $l36
              local.get $l40
              local.get $l39
              f32.mul
              local.set $l40
            end
            local.get $l6
            local.get $l39
            f32.store offset=140
            local.get $l6
            local.get $l40
            f32.store offset=136
            local.get $l6
            local.get $l36
            f32.store offset=132
            local.get $l6
            local.get $l40
            f32.store offset=124
            local.get $l6
            local.get $l36
            f32.store offset=120
            local.get $l6
            local.get $l36
            f32.store offset=116
            local.get $l6
            local.get $l39
            f32.store offset=112
            local.get $l6
            local.get $l40
            f32.store offset=108
            local.get $l6
            local.get $l36
            f32.store offset=104
            local.get $l6
            local.get $l40
            f32.store offset=96
            local.get $l6
            local.get $l40
            f32.store offset=92
            local.get $l6
            local.get $l36
            f32.store offset=88
            local.get $l6
            local.get $l39
            f32.store offset=84
            local.get $l6
            local.get $l40
            f32.store offset=80
            local.get $l6
            local.get $l36
            f32.store offset=76
            local.get $l6
            local.get $l39
            f32.store offset=68
            local.get $l6
            local.get $l36
            f32.store offset=64
            local.get $l6
            local.get $l40
            f32.store offset=60
            local.get $l6
            local.get $l36
            f32.store offset=52
            local.get $l6
            local.get $l40
            f32.store offset=48
            local.get $l6
            local.get $l40
            f32.store offset=44
            local.get $l6
            local.get $l39
            f32.store offset=40
            local.get $l6
            local.get $l36
            f32.store offset=36
            local.get $l6
            local.get $l40
            f32.store offset=32
            local.get $l6
            local.get $l36
            f32.store offset=24
            local.get $l6
            local.get $l36
            f32.store offset=20
            local.get $l6
            local.get $l40
            f32.store offset=16
            local.get $l6
            local.get $l39
            f32.store offset=12
            local.get $l6
            local.get $l36
            f32.store offset=8
            local.get $l6
            local.get $l40
            f32.store offset=4
            local.get $l6
            local.get $l39
            f32.neg
            local.tee $l39
            f32.store offset=128
            local.get $l6
            local.get $l39
            f32.store offset=100
            local.get $l6
            local.get $l39
            f32.store offset=72
            local.get $l6
            local.get $l39
            f32.store offset=56
            local.get $l6
            local.get $l39
            f32.store offset=28
            local.get $l6
            local.get $l39
            f32.store
            local.get $p4
            i32.load offset=8
            local.set $l15
            local.get $p4
            i32.load offset=4
            local.tee $l14
            i32.load offset=20
            local.set $l10
            local.get $l14
            i32.load offset=16
            local.set $l24
            i32.const 0
            local.set $l12
            loop $L129
              local.get $l6
              i32.const 160
              i32.add
              local.get $l12
              i32.add
              local.tee $l23
              i32.load8_u
              local.set $p1
              local.get $l22
              i64.const 0
              i64.store
              local.get $l21
              i64.const 0
              i64.store
              local.get $l6
              i64.const 0
              i64.store offset=184
              local.get $l6
              i64.const 0
              i64.store offset=176
              local.get $l15
              local.get $p1
              i32.const 12
              i32.mul
              i32.add
              local.tee $l11
              f32.load
              local.get $l39
              f32.mul
              local.get $l11
              f32.load offset=4
              local.get $l40
              f32.mul
              f32.add
              local.get $l11
              f32.load offset=8
              local.get $l36
              f32.mul
              f32.add
              local.set $l37
              loop $L130
                local.get $l24
                local.get $p1
                local.tee $l9
                i32.const 255
                i32.and
                local.tee $l16
                i32.const 2
                i32.shl
                i32.add
                local.tee $l11
                i32.load16_u
                local.tee $l13
                if $I131
                  local.get $l11
                  i32.load16_u offset=2
                  local.set $l17
                  i32.const 0
                  local.set $l11
                  loop $L132
                    block $B133
                      local.get $l39
                      local.get $l15
                      local.get $l10
                      local.get $l11
                      local.get $l17
                      i32.add
                      i32.add
                      i32.load8_u
                      local.tee $p2
                      i32.const 12
                      i32.mul
                      i32.add
                      local.tee $l7
                      f32.load
                      f32.mul
                      local.get $l40
                      local.get $l7
                      f32.load offset=4
                      f32.mul
                      f32.add
                      local.get $l36
                      local.get $l7
                      f32.load offset=8
                      f32.mul
                      f32.add
                      local.tee $l38
                      local.get $l37
                      f32.lt
                      i32.eqz
                      br_if $B133
                      local.get $l6
                      i32.const 176
                      i32.add
                      local.get $p2
                      i32.const 3
                      i32.shr_u
                      i32.const 28
                      i32.and
                      i32.add
                      local.tee $l7
                      i32.load
                      local.tee $l18
                      i32.const 1
                      local.get $p2
                      i32.shl
                      local.tee $l19
                      i32.and
                      br_if $B133
                      local.get $l7
                      local.get $l18
                      local.get $l19
                      i32.or
                      i32.store
                      local.get $l38
                      local.set $l37
                      local.get $p2
                      local.set $p1
                    end
                    local.get $l11
                    i32.const 1
                    i32.add
                    local.tee $l11
                    local.get $l13
                    i32.ne
                    br_if $L132
                  end
                  local.get $p1
                  i32.const 255
                  i32.and
                  local.get $l16
                  i32.ne
                  br_if $L130
                end
              end
              local.get $l23
              local.get $l9
              i32.store8
              local.get $l6
              i32.const 144
              i32.add
              local.get $l12
              i32.add
              local.tee $l23
              i32.load8_u
              local.set $p1
              local.get $l22
              i64.const 0
              i64.store
              local.get $l21
              i64.const 0
              i64.store
              local.get $l6
              i64.const 0
              i64.store offset=184
              local.get $l6
              i64.const 0
              i64.store offset=176
              local.get $l39
              local.get $l15
              local.get $p1
              i32.const 12
              i32.mul
              i32.add
              local.tee $l11
              f32.load
              f32.mul
              local.get $l40
              local.get $l11
              f32.load offset=4
              f32.mul
              f32.add
              local.get $l36
              local.get $l11
              f32.load offset=8
              f32.mul
              f32.add
              f32.neg
              local.set $l37
              loop $L134
                local.get $l24
                local.get $p1
                local.tee $l9
                i32.const 255
                i32.and
                local.tee $l16
                i32.const 2
                i32.shl
                i32.add
                local.tee $l11
                i32.load16_u
                local.tee $l13
                if $I135
                  local.get $l11
                  i32.load16_u offset=2
                  local.set $l17
                  i32.const 0
                  local.set $l11
                  loop $L136
                    block $B137
                      local.get $l37
                      local.get $l39
                      local.get $l15
                      local.get $l10
                      local.get $l11
                      local.get $l17
                      i32.add
                      i32.add
                      i32.load8_u
                      local.tee $p2
                      i32.const 12
                      i32.mul
                      i32.add
                      local.tee $l7
                      f32.load
                      f32.mul
                      local.get $l40
                      local.get $l7
                      f32.load offset=4
                      f32.mul
                      f32.add
                      local.get $l36
                      local.get $l7
                      f32.load offset=8
                      f32.mul
                      f32.add
                      f32.neg
                      local.tee $l38
                      f32.gt
                      i32.eqz
                      br_if $B137
                      local.get $l6
                      i32.const 176
                      i32.add
                      local.get $p2
                      i32.const 3
                      i32.shr_u
                      i32.const 28
                      i32.and
                      i32.add
                      local.tee $l7
                      i32.load
                      local.tee $l18
                      i32.const 1
                      local.get $p2
                      i32.shl
                      local.tee $l19
                      i32.and
                      br_if $B137
                      local.get $l7
                      local.get $l18
                      local.get $l19
                      i32.or
                      i32.store
                      local.get $l38
                      local.set $l37
                      local.get $p2
                      local.set $p1
                    end
                    local.get $l11
                    i32.const 1
                    i32.add
                    local.tee $l11
                    local.get $l13
                    i32.ne
                    br_if $L136
                  end
                  local.get $p1
                  i32.const 255
                  i32.and
                  local.get $l16
                  i32.ne
                  br_if $L134
                end
              end
              local.get $l23
              local.get $l9
              i32.store8
              local.get $l12
              i32.const 1
              i32.add
              local.tee $l12
              i32.const 12
              i32.ne
              if $I138
                local.get $l6
                local.get $l12
                i32.const 12
                i32.mul
                i32.add
                local.tee $l11
                f32.load offset=8
                local.set $l36
                local.get $l11
                f32.load offset=4
                local.set $l40
                local.get $l11
                f32.load
                local.set $l39
                br $L129
              end
            end
            local.get $l5
            local.get $l25
            i32.add
            local.set $l10
            local.get $l5
            i32.const 4
            i32.shl
            local.get $l8
            i32.add
            local.set $l13
            i32.const 0
            local.set $l11
            loop $L139
              local.get $l13
              local.get $l11
              i32.const 8
              i32.shl
              local.tee $l7
              i32.add
              local.tee $p2
              local.get $l14
              i32.load offset=4
              i32.add
              local.get $l6
              i32.const 160
              i32.add
              local.get $l11
              i32.add
              i32.load8_u
              i32.store8
              local.get $p4
              i32.load offset=4
              local.tee $l15
              i32.load offset=4
              local.get $p2
              local.get $l15
              i32.load16_u offset=2
              i32.add
              i32.add
              local.get $l6
              i32.const 144
              i32.add
              local.get $l11
              i32.add
              i32.load8_u
              i32.store8
              local.get $l7
              local.get $l10
              i32.add
              local.tee $l7
              local.get $p4
              i32.load offset=4
              i32.load offset=4
              i32.add
              local.get $l11
              i32.const 6
              i32.add
              local.tee $p2
              local.get $l6
              i32.const 160
              i32.add
              i32.add
              i32.load8_u
              i32.store8
              local.get $p4
              i32.load offset=4
              local.tee $l15
              i32.load offset=4
              local.get $l7
              local.get $l15
              i32.load16_u offset=2
              i32.add
              i32.add
              local.get $l6
              i32.const 144
              i32.add
              local.get $p2
              i32.add
              i32.load8_u
              i32.store8
              local.get $l11
              i32.const 1
              i32.add
              local.tee $l11
              i32.const 6
              i32.ne
              if $I140
                local.get $p4
                i32.load offset=4
                local.set $l14
                br $L139
              end
            end
            local.get $l5
            i32.const 1
            i32.add
            local.tee $l5
            i32.const 16
            i32.ne
            br_if $L126
          end
          local.get $l8
          i32.const 1
          i32.add
          local.tee $l8
          i32.const 16
          i32.ne
          br_if $L125
        end
        local.get $l6
        i32.const 208
        i32.add
        global.set $g0
        local.get $p4
        i32.const 16
        i32.add
        global.set $g0
      end
      local.get $p3
      i32.eqz
      if $I141
        i32.const 0
        local.set $p2
        global.get $g0
        i32.const 16
        i32.sub
        local.set $p3
        local.get $p0
        i32.const 2139095039
        i32.store offset=92
        local.get $p0
        i32.load offset=4
        local.set $l7
        block $B142
          local.get $p0
          i32.load8_u offset=83
          local.tee $l11
          i32.eqz
          if $I143
            local.get $p0
            f32.load offset=76
            local.set $l42
            local.get $p0
            f32.load offset=72
            local.set $l44
            local.get $p0
            f32.load offset=68
            local.set $l45
            f32.const 0x1.fffffep+127 (;=3.40282e+38;)
            local.set $l38
            br $B142
          end
          local.get $p0
          f32.load offset=76
          local.set $l42
          local.get $p0
          f32.load offset=72
          local.set $l44
          local.get $p0
          f32.load offset=68
          local.set $l45
          f32.const 0x1.fffffep+127 (;=3.40282e+38;)
          local.set $l38
          loop $L144
            local.get $l38
            local.get $l7
            local.get $p2
            i32.const 20
            i32.mul
            i32.add
            local.tee $p1
            f32.load offset=12
            local.get $l45
            local.get $p1
            f32.load
            f32.mul
            local.get $l44
            local.get $p1
            f32.load offset=4
            f32.mul
            f32.add
            local.get $l42
            local.get $p1
            f32.load offset=8
            f32.mul
            f32.add
            f32.add
            f32.abs
            local.tee $l37
            f32.gt
            if $I145
              local.get $p0
              local.get $l37
              f32.store offset=92
              local.get $l37
              local.set $l38
            end
            local.get $p2
            i32.const 1
            i32.add
            local.tee $p2
            local.get $l11
            i32.ne
            br_if $L144
          end
        end
        local.get $p0
        f32.load offset=56
        local.set $l37
        local.get $p0
        f32.load offset=60
        local.set $l40
        local.get $p0
        f32.load offset=48
        local.set $l41
        local.get $p0
        f32.load offset=44
        local.set $l36
        local.get $p3
        local.get $p0
        f32.load offset=52
        local.tee $l39
        local.get $p0
        i32.const -64
        i32.sub
        f32.load
        local.tee $l43
        f32.add
        local.get $l39
        local.get $l43
        f32.sub
        f32.sub
        local.tee $l39
        f32.store offset=8
        local.get $p3
        local.get $l41
        local.get $l40
        f32.add
        local.get $l41
        local.get $l40
        f32.sub
        f32.sub
        local.tee $l40
        f32.store offset=4
        local.get $p3
        local.get $l36
        local.get $l37
        f32.add
        local.get $l36
        local.get $l37
        f32.sub
        f32.sub
        local.tee $l37
        f32.store
        local.get $p3
        i32.const 2
        local.get $l37
        local.get $l40
        f32.lt
        local.tee $p1
        local.get $l39
        local.get $p3
        local.get $p1
        i32.const 2
        i32.shl
        i32.or
        f32.load
        f32.gt
        select
        local.tee $l8
        local.get $l8
        i32.const 1
        i32.shr_u
        i32.add
        i32.const 1
        i32.add
        local.tee $p1
        local.get $p1
        i32.const 3
        i32.and
        local.tee $p1
        i32.const 1
        i32.shr_u
        i32.add
        i32.const 1
        i32.add
        i32.const 3
        i32.and
        local.tee $p2
        i32.const 2
        i32.shl
        i32.add
        f32.load
        local.set $l37
        local.get $p3
        local.get $p1
        i32.const 2
        i32.shl
        i32.add
        f32.load
        local.set $l40
        local.get $p0
        i32.const 2139095039
        i32.store offset=104
        local.get $p0
        i32.const 96
        i32.add
        local.tee $l9
        i64.const 9187343237679939583
        i64.store align=4
        local.get $p1
        local.get $p2
        local.get $l37
        local.get $l40
        f32.gt
        local.tee $p3
        select
        local.set $l5
        local.get $p2
        local.get $p1
        local.get $p3
        select
        local.set $l6
        block $B146
          local.get $l11
          if $I147
            local.get $l9
            local.get $l8
            i32.const 2
            i32.shl
            local.tee $p4
            i32.add
            local.set $p3
            local.get $l38
            f32.const 0x1.bb67aep+0 (;=1.73205;)
            f32.div
            local.set $l37
            i32.const 0
            local.set $p2
            loop $L148
              block $B149
                local.get $l7
                local.get $p2
                i32.const 20
                i32.mul
                i32.add
                local.tee $p1
                local.get $p4
                i32.add
                f32.load
                local.tee $l38
                f32.const -0x1.ad7f2ap-24 (;=-1e-07;)
                f32.gt
                local.get $l38
                f32.const 0x1.ad7f2ap-24 (;=1e-07;)
                f32.lt
                i32.and
                br_if $B149
                f32.const 0x1p+0 (;=1;)
                local.get $l38
                f32.div
                local.tee $l38
                local.get $l37
                local.get $p1
                local.get $l5
                i32.const 2
                i32.shl
                i32.add
                f32.load
                f32.mul
                local.tee $l40
                local.get $l37
                local.get $p1
                local.get $l6
                i32.const 2
                i32.shl
                i32.add
                f32.load
                f32.mul
                local.tee $l41
                local.get $p1
                f32.load offset=12
                f32.neg
                local.get $l45
                local.get $p1
                f32.load
                f32.mul
                local.get $l44
                local.get $p1
                f32.load offset=4
                f32.mul
                f32.add
                local.get $l42
                local.get $p1
                f32.load offset=8
                f32.mul
                f32.add
                f32.sub
                local.tee $l36
                f32.add
                local.tee $l39
                f32.add
                f32.mul
                f32.abs
                local.tee $l43
                local.get $l37
                local.get $l37
                local.get $l43
                f32.lt
                select
                local.tee $l43
                local.get $l38
                local.get $l40
                local.get $l36
                local.get $l41
                f32.sub
                local.tee $l41
                f32.add
                f32.mul
                f32.abs
                local.tee $l36
                local.get $l37
                local.get $l36
                local.get $l37
                f32.gt
                select
                local.tee $l36
                local.get $l38
                local.get $l41
                local.get $l40
                f32.sub
                f32.mul
                f32.abs
                local.tee $l41
                local.get $l37
                local.get $l37
                local.get $l41
                f32.lt
                select
                local.tee $l41
                local.get $p3
                f32.load
                local.tee $l46
                local.get $l41
                local.get $l46
                f32.lt
                local.tee $p1
                select
                local.tee $l41
                local.get $l36
                local.get $l41
                f32.lt
                local.tee $l9
                select
                local.tee $l41
                local.get $l41
                local.get $l43
                f32.gt
                local.tee $l15
                select
                local.set $l41
                local.get $l38
                local.get $l39
                local.get $l40
                f32.sub
                f32.mul
                f32.abs
                local.tee $l38
                local.get $l37
                local.get $l37
                local.get $l38
                f32.lt
                select
                local.set $l38
                block $B150
                  local.get $p1
                  br_if $B150
                  local.get $l9
                  br_if $B150
                  local.get $l15
                  br_if $B150
                  local.get $l38
                  local.get $l41
                  f32.lt
                  i32.eqz
                  br_if $B149
                end
                local.get $p3
                local.get $l38
                local.get $l41
                local.get $l38
                local.get $l41
                f32.lt
                select
                f32.store
              end
              local.get $p2
              i32.const 1
              i32.add
              local.tee $p2
              local.get $l11
              i32.ne
              br_if $L148
            end
            local.get $p0
            local.get $l6
            i32.const 2
            i32.shl
            local.tee $l9
            i32.add
            i32.const 96
            i32.add
            local.set $p4
            i32.const 0
            local.set $p2
            loop $L151
              local.get $l7
              local.get $p2
              i32.const 20
              i32.mul
              i32.add
              local.tee $p1
              local.get $l9
              i32.add
              f32.load
              local.tee $l36
              local.get $p1
              local.get $l5
              i32.const 2
              i32.shl
              i32.add
              f32.load
              local.tee $l39
              f32.sub
              local.set $l38
              local.get $p3
              f32.load
              local.get $p1
              local.get $l8
              i32.const 2
              i32.shl
              i32.add
              f32.load
              f32.mul
              local.set $l40
              local.get $p1
              f32.load offset=12
              f32.neg
              local.get $l45
              local.get $p1
              f32.load
              f32.mul
              local.get $l44
              local.get $p1
              f32.load offset=4
              f32.mul
              f32.add
              local.get $l42
              local.get $p1
              f32.load offset=8
              f32.mul
              f32.add
              f32.sub
              local.set $l41
              block $B152
                local.get $l36
                local.get $l39
                f32.add
                local.tee $l36
                f32.const -0x1.ad7f2ap-24 (;=-1e-07;)
                f32.gt
                local.get $l36
                f32.const 0x1.ad7f2ap-24 (;=1e-07;)
                f32.lt
                i32.and
                br_if $B152
                local.get $l41
                local.get $l40
                f32.sub
                local.get $l36
                f32.div
                f32.abs
                local.tee $l39
                local.get $l37
                local.get $l37
                local.get $l39
                f32.lt
                select
                local.tee $l39
                local.get $p4
                f32.load
                local.tee $l43
                local.get $l39
                local.get $l43
                f32.lt
                local.tee $p1
                select
                local.set $l39
                i32.const 1
                local.get $p1
                local.get $l39
                local.get $l41
                local.get $l40
                f32.add
                local.get $l36
                f32.div
                f32.abs
                local.tee $l36
                local.get $l37
                local.get $l36
                local.get $l37
                f32.gt
                select
                local.tee $l36
                f32.gt
                select
                i32.eqz
                br_if $B152
                local.get $p4
                local.get $l36
                local.get $l39
                local.get $l36
                local.get $l39
                f32.lt
                select
                f32.store
              end
              block $B153
                local.get $l38
                f32.const 0x1.ad7f2ap-24 (;=1e-07;)
                f32.lt
                local.get $l38
                f32.const -0x1.ad7f2ap-24 (;=-1e-07;)
                f32.gt
                i32.and
                br_if $B153
                local.get $l41
                local.get $l40
                f32.sub
                local.get $l38
                f32.div
                f32.abs
                local.tee $l36
                local.get $l37
                local.get $l36
                local.get $l37
                f32.gt
                select
                local.tee $l36
                local.get $p4
                f32.load
                local.tee $l39
                local.get $l36
                local.get $l39
                f32.lt
                local.tee $p1
                select
                local.set $l36
                i32.const 1
                local.get $p1
                local.get $l36
                local.get $l41
                local.get $l40
                f32.add
                local.get $l38
                f32.div
                f32.abs
                local.tee $l38
                local.get $l37
                local.get $l37
                local.get $l38
                f32.lt
                select
                local.tee $l38
                f32.gt
                select
                i32.eqz
                br_if $B153
                local.get $p4
                local.get $l38
                local.get $l36
                local.get $l36
                local.get $l38
                f32.gt
                select
                f32.store
              end
              local.get $p2
              i32.const 1
              i32.add
              local.tee $p2
              local.get $l11
              i32.ne
              br_if $L151
            end
            br $B146
          end
          local.get $p0
          local.get $l6
          i32.const 2
          i32.shl
          i32.add
          i32.const 96
          i32.add
          local.set $p4
        end
        local.get $p0
        local.get $l5
        i32.const 2
        i32.shl
        i32.add
        local.get $p4
        f32.load
        f32.store offset=96
      end
      i32.const 1
    end
    local.set $l9
    local.get $l26
    i32.const 32
    i32.add
    global.set $g0
    local.get $l9)
