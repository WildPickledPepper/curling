  (func $f68543 (type $t4) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32)
    (local $l4 f32) (local $l5 f32) (local $l6 f32) (local $l7 f32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 i32) (local $l29 i32) (local $l30 i32) (local $l31 i32) (local $l32 i32) (local $l33 i32) (local $l34 i32) (local $l35 i32) (local $l36 i32) (local $l37 i32) (local $l38 i32) (local $l39 i32) (local $l40 i32) (local $l41 i32) (local $l42 i32) (local $l43 i32) (local $l44 i32) (local $l45 i32) (local $l46 i32) (local $l47 i32) (local $l48 i32) (local $l49 i32) (local $l50 i32) (local $l51 i32) (local $l52 i32) (local $l53 i32) (local $l54 i32) (local $l55 i32) (local $l56 i32) (local $l57 i32) (local $l58 i32) (local $l59 i32) (local $l60 i32) (local $l61 i32) (local $l62 i32) (local $l63 i32) (local $l64 i32) (local $l65 i32) (local $l66 i32) (local $l67 i32) (local $l68 i64) (local $l69 f64) (local $l70 f64)
    local.get $p2
    local.set $l38
    global.get $g0
    i32.const 496
    i32.sub
    local.tee $l29
    global.set $g0
    local.get $p1
    local.tee $l42
    i32.load8_u offset=78
    local.set $l61
    local.get $p3
    local.tee $l37
    i32.load
    local.tee $l39
    block $B0 (result i32)
      i32.const 1
      local.get $p0
      local.tee $l40
      i32.load8_u offset=331
      br_if $B0
      drop
      i32.const 0
      local.get $l38
      i32.load8_u offset=20
      i32.eqz
      br_if $B0
      drop
      local.get $l40
      i32.load8_u offset=332
    end
    local.get $l39
    i32.load8_u offset=12
    i32.or
    i32.store8 offset=12
    block $B1
      local.get $l40
      i32.load offset=180
      local.tee $l48
      i32.eqz
      if $I2
        local.get $l37
        i32.load
        call $f68367
        block $B3
          local.get $l42
          i32.load8_u offset=76
          i32.eqz
          if $I4
            local.get $l38
            i32.load8_u
            i32.eqz
            br_if $B3
          end
          local.get $l37
          i32.load
          i32.load offset=4
          i32.const 0
          call $f68309
          local.get $l42
          i32.load offset=64
          local.get $l42
          i32.load offset=68
          local.get $l42
          i32.load offset=72
          local.get $l37
          i32.load
          i32.load offset=4
          local.get $l40
          i32.load8_u offset=256
          local.tee $l40
          i32.eqz
          call $f68330
          local.get $l40
          br_if $B3
          local.get $l42
          i32.load offset=64
          local.get $l42
          i32.load offset=68
          local.get $l42
          i32.load offset=72
          local.get $l38
          i32.load offset=32
          local.get $l37
          i32.load
          i32.load
          call $f68329
          local.get $l38
          i32.load8_u
          i32.eqz
          br_if $B3
          local.get $l38
          i32.load offset=4
          local.get $l37
          i32.load
          i32.load offset=4
          call $f68311
          local.get $l38
          i32.load offset=32
          local.get $l37
          i32.load
          local.tee $l42
          i32.load
          local.get $l42
          i32.load offset=4
          call $f68317
        end
        br $B1
      end
      block $B5
        local.get $l40
        i32.load offset=312
        local.tee $l39
        local.get $l39
        i32.load
        i32.load offset=84
        call_indirect $__indirect_function_table (type $t23)
        local.tee $l9
        f32.const 0x0p+0 (;=0;)
        f32.ne
        if $I6
          block $B7
            local.get $l40
            f64.load offset=64
            local.get $l9
            f64.promote_f32
            local.tee $l69
            f64.div
            local.tee $l70
            f32.demote_f64
            local.tee $l13
            f32.const 0x1.fffffep+127 (;=3.40282e+38;)
            f32.eq
            br_if $B7
            local.get $l70
            local.get $l13
            f64.promote_f32
            f64.gt
            i32.eqz
            br_if $B7
            block $B8 (result i32)
              local.get $l13
              f32.const 0x0p+0 (;=0;)
              f32.eq
              if $I9
                i32.const 1
                local.get $l13
                f32.const 0x1.fffffep+127 (;=3.40282e+38;)
                f32.lt
                br_if $B8
                drop
                i32.const -2147483647
                br $B8
              end
              local.get $l13
              i32.reinterpret_f32
              local.tee $l39
              i32.const 1
              i32.add
              local.get $l13
              f32.const 0x1.fffffep+127 (;=3.40282e+38;)
              f32.lt
              i32.eqz
              local.get $l13
              f32.const 0x0p+0 (;=0;)
              f32.ge
              i32.ne
              br_if $B8
              drop
              local.get $l39
              i32.const 1
              i32.sub
            end
            f32.reinterpret_i32
            local.set $l13
          end
          local.get $l29
          local.get $l13
          f32.store offset=424
          local.get $l40
          f64.load offset=232
          local.get $l69
          f64.div
          local.tee $l69
          f32.demote_f64
          local.tee $l9
          f32.const 0x1.fffffep+127 (;=3.40282e+38;)
          f32.eq
          br_if $B5
          local.get $l69
          local.get $l9
          f64.promote_f32
          f64.gt
          i32.eqz
          br_if $B5
          block $B10 (result i32)
            local.get $l9
            f32.const 0x0p+0 (;=0;)
            f32.eq
            if $I11
              i32.const 1
              local.get $l9
              f32.const 0x1.fffffep+127 (;=3.40282e+38;)
              f32.lt
              br_if $B10
              drop
              f32.const -0x1.p-149 (;=-1.4013e-45;)
              local.set $l9
              br $B5
            end
            local.get $l9
            i32.reinterpret_f32
            local.set $l39
            local.get $l9
            f32.const 0x1.fffffep+127 (;=3.40282e+38;)
            f32.lt
            i32.eqz
            local.get $l9
            f32.const 0x0p+0 (;=0;)
            f32.ge
            i32.ne
            if $I12
              local.get $l39
              i32.const 1
              i32.add
              f32.reinterpret_i32
              local.set $l9
              br $B5
            end
            local.get $l39
            i32.const 1
            i32.sub
          end
          f32.reinterpret_i32
          local.set $l9
          br $B5
        end
        local.get $l29
        i32.const 0
        i32.store offset=424
        f32.const 0x0p+0 (;=0;)
        local.set $l9
      end
      local.get $l29
      local.get $l9
      f32.store offset=428
      local.get $l29
      local.get $l40
      f32.load offset=252
      local.tee $l15
      f32.store offset=440
      local.get $l29
      local.get $l40
      f32.load offset=244
      local.tee $l17
      f32.store offset=432
      local.get $l29
      local.get $l40
      i32.load8_u offset=248
      i32.store8 offset=436
      local.get $l29
      local.get $l38
      i32.load8_u offset=21
      i32.store8 offset=444
      local.get $l29
      local.get $l40
      i32.load8_u offset=329
      i32.store8 offset=445
      local.get $l29
      local.get $l40
      f32.load offset=340
      local.tee $l19
      f32.store offset=448
      local.get $l40
      i32.load8_u offset=269
      local.tee $l31
      if $I13
        local.get $l48
        i32.load8_u offset=2086
        i32.const 0
        i32.ne
        local.set $l60
      end
      local.get $l38
      i32.load8_u offset=12
      local.set $l64
      local.get $l48
      i32.const 1240
      i32.add
      local.set $l45
      local.get $l40
      i32.load offset=192
      local.set $l39
      local.get $l40
      i32.load offset=212
      local.set $l41
      local.get $l40
      i32.load offset=188
      local.set $l33
      local.get $l37
      i32.load
      local.tee $l54
      i32.load offset=4
      local.set $l37
      local.get $l54
      i32.load
      local.set $l50
      local.get $l54
      i32.load offset=8
      local.set $l43
      local.get $l38
      i32.load8_u offset=20
      if $I14
        local.get $l41
        local.get $l48
        i32.load offset=1240
        local.tee $l31
        local.get $l45
        i32.add
        i32.const 0
        local.get $l31
        select
        local.tee $l31
        i32.load16_u offset=10
        local.get $l31
        i32.load16_u offset=8
        i32.add
        local.get $l31
        i32.load offset=16
        i32.add
        local.get $l31
        i32.load offset=36
        i32.add
        call $f68383
        local.get $l40
        i32.load8_u offset=269
        local.set $l31
        local.get $l29
        i32.const 0
        i32.store offset=256
        local.get $l29
        local.get $l9
        local.get $l48
        f32.load offset=1244
        local.get $l48
        f32.load offset=1248
        local.get $l48
        f32.load offset=1260
        local.get $l15
        f32.add
        local.get $l31
        local.get $l17
        local.get $l29
        i32.const 256
        i32.add
        local.get $l29
        local.get $l19
        call $f68341
        f32.store offset=456
        local.get $l48
        i32.load offset=1240
        local.tee $l31
        local.get $l45
        i32.add
        i32.const 0
        local.get $l31
        select
        local.get $l29
        i32.const 456
        i32.add
        local.get $l33
        local.get $l41
        call $f68384
        local.get $l40
        i32.load8_u offset=269
        local.set $l31
      end
      local.get $l29
      i32.const 0
      i32.store offset=256
      local.get $l29
      local.get $l13
      local.get $l48
      f32.load offset=1244
      local.get $l48
      f32.load offset=1248
      local.get $l48
      f32.load offset=1260
      local.get $l15
      f32.add
      local.get $l31
      i32.const 255
      i32.and
      i32.const 0
      i32.ne
      local.get $l17
      local.get $l29
      i32.const 256
      i32.add
      local.get $l29
      local.get $l19
      call $f68341
      f32.store offset=456
      local.get $l48
      i32.load offset=1240
      local.tee $l31
      local.get $l45
      i32.add
      i32.const 0
      local.get $l31
      select
      local.get $l29
      i32.const 456
      i32.add
      local.get $l33
      local.get $l39
      call $f68384
      local.get $l40
      local.get $l29
      f32.load offset=256
      f32.store offset=224
      local.get $l40
      i32.load offset=184
      local.set $l45
      block $B15
        local.get $l42
        i32.load8_u offset=76
        i32.eqz
        if $I16
          local.get $l38
          i32.load8_u
          i32.eqz
          br_if $B15
        end
        local.get $l38
        i32.const 28
        i32.const 24
        local.get $l64
        select
        i32.add
        i32.load
        local.tee $l33
        i32.eqz
        if $I17
          local.get $l42
          i32.load offset=8
          local.set $l33
        end
        block $B18
          local.get $l64
          local.get $l40
          i32.load8_u offset=256
          i32.or
          i32.eqz
          if $I19
            local.get $l38
            i32.load offset=32
            local.tee $l31
            br_if $B18
          end
          local.get $l33
          local.set $l31
        end
        local.get $l37
        i32.const 0
        call $f68309
        local.get $l42
        i32.load offset=68
        local.set $l53
        local.get $l42
        i32.load offset=72
        local.set $l34
        local.get $l45
        local.set $l28
        local.get $l50
        local.set $l36
        local.get $l37
        local.set $l30
        local.get $l40
        i32.load8_u offset=256
        i32.eqz
        local.set $l33
        local.get $l42
        i32.load offset=64
        local.tee $l51
        i32.const -1
        i32.ne
        if $I20
          local.get $l30
          i32.load offset=4
          local.tee $l46
          local.get $l30
          i32.const 4
          i32.add
          i32.add
          i32.const 0
          local.get $l46
          select
          local.set $l52
          local.get $l36
          i32.load offset=4
          local.tee $l46
          local.get $l36
          i32.const 4
          i32.add
          i32.add
          i32.const 0
          local.get $l46
          select
          local.set $l58
          i32.const 1
          local.set $l32
          block $B21 (result i32)
            local.get $l28
            i32.load offset=4
            local.get $l51
            i32.const 1
            i32.shl
            i32.add
            i32.load16_s
            local.tee $l46
            i32.const -1
            i32.eq
            if $I22
              local.get $l51
              i32.const 12
              i32.mul
              local.get $l31
              i32.load offset=4
              local.tee $l46
              local.get $l31
              i32.const 4
              i32.add
              i32.add
              i32.const 0
              local.get $l46
              select
              i32.add
              local.tee $l46
              i32.const 8
              i32.add
              local.set $l35
              local.get $l33
              local.set $l32
              local.get $l46
              i32.const 4
              i32.add
              br $B21
            end
            local.get $l39
            i32.load
            local.get $l46
            i32.const 2
            i32.shl
            i32.add
            local.tee $l46
            i32.const 8
            i32.add
            local.set $l35
            local.get $l46
            i32.const 4
            i32.add
          end
          local.set $l44
          local.get $l46
          f32.load
          local.set $l5
          local.get $l44
          f32.load
          local.set $l7
          local.get $l58
          local.get $l51
          i32.const 12
          i32.mul
          i32.add
          local.tee $l46
          local.get $l35
          f32.load
          f32.store offset=8
          local.get $l46
          local.get $l7
          f32.store offset=4
          local.get $l46
          local.get $l5
          f32.store
          local.get $l51
          local.get $l52
          i32.add
          local.get $l32
          i32.store8
        end
        block $B23
          local.get $l53
          i32.const -1
          i32.eq
          br_if $B23
          local.get $l30
          i32.load offset=12
          local.set $l46
          local.get $l36
          i32.load offset=12
          local.set $l51
          local.get $l53
          i32.const 1
          i32.shl
          local.tee $l52
          local.get $l28
          i32.load offset=12
          i32.add
          i32.load16_s
          local.set $l32
          local.get $l28
          i32.load offset=16
          local.set $l35
          local.get $l39
          i32.load
          local.set $l58
          block $B24 (result i32)
            block $B25
              local.get $l28
              i32.load offset=8
              local.get $l52
              i32.add
              i32.load16_u
              local.tee $l52
              i32.const 65535
              i32.ne
              br_if $B25
              local.get $l32
              i32.const -1
              i32.ne
              br_if $B25
              local.get $l53
              i32.const 4
              i32.shl
              local.get $l31
              i32.load offset=12
              local.tee $l32
              local.get $l31
              i32.const 12
              i32.add
              i32.add
              i32.const 0
              local.get $l32
              select
              i32.add
              local.tee $l32
              f32.load offset=12
              local.set $l5
              local.get $l32
              f32.load offset=8
              local.set $l7
              local.get $l32
              f32.load offset=4
              local.set $l8
              local.get $l32
              f32.load
              local.set $l10
              local.get $l33
              br $B24
            end
            local.get $l52
            i32.const 65535
            i32.ne
            if $I26
              local.get $l58
              local.get $l52
              i32.const 16
              i32.shl
              i32.const 16
              i32.shr_s
              i32.const 2
              i32.shl
              i32.add
              local.tee $l32
              f32.load offset=12
              local.tee $l5
              local.get $l32
              f32.load
              local.tee $l14
              local.get $l14
              f32.mul
              local.get $l32
              f32.load offset=4
              local.tee $l8
              local.get $l8
              f32.mul
              f32.add
              local.get $l32
              f32.load offset=8
              local.tee $l7
              local.get $l7
              f32.mul
              local.get $l5
              local.get $l5
              f32.mul
              f32.add
              f32.add
              local.tee $l5
              f32.sqrt
              local.tee $l10
              f32.div
              f32.const 0x1p+0 (;=1;)
              local.get $l5
              f32.const 0x1.4484cp-100 (;=1e-30;)
              f32.gt
              local.tee $l32
              select
              local.set $l5
              local.get $l7
              local.get $l10
              f32.div
              f32.const 0x0p+0 (;=0;)
              local.get $l32
              select
              local.set $l7
              local.get $l8
              local.get $l10
              f32.div
              f32.const 0x0p+0 (;=0;)
              local.get $l32
              select
              local.set $l8
              local.get $l14
              local.get $l10
              f32.div
              f32.const 0x0p+0 (;=0;)
              local.get $l32
              select
              local.set $l10
              i32.const 1
              br $B24
            end
            local.get $l32
            i32.const -1
            i32.eq
            br_if $B23
            local.get $l58
            local.get $l32
            i32.const 2
            i32.shl
            i32.add
            local.tee $l32
            f32.load offset=8
            f32.const 0x1.1df46ap-6 (;=0.0174533;)
            f32.mul
            f32.const 0x1p-1 (;=0.5;)
            f32.mul
            f32.const 0x1.45f306p-3 (;=0.159155;)
            f32.mul
            local.tee $l7
            f32.const -0x1p-2 (;=-0.25;)
            f32.add
            local.tee $l9
            call $f66998
            local.set $l15
            local.get $l32
            f32.load
            f32.const 0x1.1df46ap-6 (;=0.0174533;)
            f32.mul
            f32.const 0x1p-1 (;=0.5;)
            f32.mul
            f32.const 0x1.45f306p-3 (;=0.159155;)
            f32.mul
            local.tee $l8
            f32.const -0x1p-2 (;=-0.25;)
            f32.add
            local.tee $l20
            call $f66998
            local.set $l22
            local.get $l32
            f32.load offset=4
            f32.const 0x1.1df46ap-6 (;=0.0174533;)
            f32.mul
            f32.const 0x1p-1 (;=0.5;)
            f32.mul
            f32.const 0x1.45f306p-3 (;=0.159155;)
            f32.mul
            local.tee $l5
            f32.const -0x1p-2 (;=-0.25;)
            f32.add
            local.tee $l14
            call $f66998
            local.set $l13
            local.get $l35
            local.get $l53
            i32.const 1
            i32.shl
            i32.add
            i32.load16_s
            local.set $l52
            local.get $l7
            call $f66998
            local.set $l17
            local.get $l8
            call $f66998
            local.set $l19
            local.get $l52
            i32.const 5
            i32.shl
            local.tee $l52
            i32.const 3111964
            i32.add
            f32.load
            f32.const 0x1p-2 (;=0.25;)
            local.get $l5
            local.get $l5
            call $f66998
            f32.sub
            f32.abs
            f32.sub
            local.tee $l5
            local.get $l5
            local.get $l5
            f32.mul
            local.tee $l5
            local.get $l5
            f32.mul
            local.tee $l10
            local.get $l10
            f32.mul
            f32.const 0x1.3d419ap+5 (;=39.657;)
            f32.mul
            f32.const 0x1.921fb4p+2 (;=6.28319;)
            local.get $l5
            f32.const 0x1.4abbb8p+5 (;=41.3417;)
            f32.mul
            f32.sub
            local.get $l10
            f32.const 0x1.466844p+6 (;=81.6018;)
            local.get $l5
            f32.const 0x1.324644p+6 (;=76.5686;)
            f32.mul
            f32.sub
            f32.mul
            f32.add
            f32.add
            f32.mul
            local.tee $l10
            f32.const 0x1p-2 (;=0.25;)
            local.get $l8
            local.get $l19
            f32.sub
            f32.abs
            f32.sub
            local.tee $l5
            local.get $l5
            local.get $l5
            f32.mul
            local.tee $l5
            local.get $l5
            f32.mul
            local.tee $l8
            local.get $l8
            f32.mul
            f32.const 0x1.3d419ap+5 (;=39.657;)
            f32.mul
            f32.const 0x1.921fb4p+2 (;=6.28319;)
            local.get $l5
            f32.const 0x1.4abbb8p+5 (;=41.3417;)
            f32.mul
            f32.sub
            local.get $l8
            f32.const 0x1.466844p+6 (;=81.6018;)
            local.get $l5
            f32.const 0x1.324644p+6 (;=76.5686;)
            f32.mul
            f32.sub
            f32.mul
            f32.add
            f32.add
            f32.mul
            local.tee $l8
            f32.const 0x1p-2 (;=0.25;)
            local.get $l7
            local.get $l17
            f32.sub
            f32.abs
            f32.sub
            local.tee $l5
            local.get $l5
            local.get $l5
            f32.mul
            local.tee $l5
            local.get $l5
            f32.mul
            local.tee $l7
            local.get $l7
            f32.mul
            f32.const 0x1.3d419ap+5 (;=39.657;)
            f32.mul
            f32.const 0x1.921fb4p+2 (;=6.28319;)
            local.get $l5
            f32.const 0x1.4abbb8p+5 (;=41.3417;)
            f32.mul
            f32.sub
            local.get $l7
            f32.const 0x1.466844p+6 (;=81.6018;)
            local.get $l5
            f32.const 0x1.324644p+6 (;=76.5686;)
            f32.mul
            f32.sub
            f32.mul
            f32.add
            f32.add
            f32.mul
            local.tee $l17
            f32.mul
            local.tee $l19
            f32.mul
            f32.mul
            local.get $l52
            i32.const 16
            i32.or
            local.tee $l58
            i32.const 3111964
            i32.add
            f32.load
            f32.const 0x1p-2 (;=0.25;)
            local.get $l14
            local.get $l13
            f32.sub
            f32.abs
            f32.sub
            local.tee $l5
            local.get $l5
            local.get $l5
            f32.mul
            local.tee $l5
            local.get $l5
            f32.mul
            local.tee $l7
            local.get $l7
            f32.mul
            f32.const 0x1.3d419ap+5 (;=39.657;)
            f32.mul
            f32.const 0x1.921fb4p+2 (;=6.28319;)
            local.get $l5
            f32.const 0x1.4abbb8p+5 (;=41.3417;)
            f32.mul
            f32.sub
            local.get $l7
            f32.const 0x1.466844p+6 (;=81.6018;)
            local.get $l5
            f32.const 0x1.324644p+6 (;=76.5686;)
            f32.mul
            f32.sub
            f32.mul
            f32.add
            f32.add
            f32.mul
            local.tee $l14
            f32.mul
            f32.const 0x1p-2 (;=0.25;)
            local.get $l20
            local.get $l22
            f32.sub
            f32.abs
            f32.sub
            local.tee $l5
            local.get $l5
            local.get $l5
            f32.mul
            local.tee $l5
            local.get $l5
            f32.mul
            local.tee $l7
            local.get $l7
            f32.mul
            f32.const 0x1.3d419ap+5 (;=39.657;)
            f32.mul
            f32.const 0x1.921fb4p+2 (;=6.28319;)
            local.get $l5
            f32.const 0x1.4abbb8p+5 (;=41.3417;)
            f32.mul
            f32.sub
            local.get $l7
            f32.const 0x1.466844p+6 (;=81.6018;)
            local.get $l5
            f32.const 0x1.324644p+6 (;=76.5686;)
            f32.mul
            f32.sub
            f32.mul
            f32.add
            f32.add
            f32.mul
            local.tee $l20
            f32.const 0x1p-2 (;=0.25;)
            local.get $l9
            local.get $l15
            f32.sub
            f32.abs
            f32.sub
            local.tee $l5
            local.get $l5
            local.get $l5
            f32.mul
            local.tee $l5
            local.get $l5
            f32.mul
            local.tee $l7
            local.get $l7
            f32.mul
            f32.const 0x1.3d419ap+5 (;=39.657;)
            f32.mul
            f32.const 0x1.921fb4p+2 (;=6.28319;)
            local.get $l5
            f32.const 0x1.4abbb8p+5 (;=41.3417;)
            f32.mul
            f32.sub
            local.get $l7
            f32.const 0x1.466844p+6 (;=81.6018;)
            local.get $l5
            f32.const 0x1.324644p+6 (;=76.5686;)
            f32.mul
            f32.sub
            f32.mul
            f32.add
            f32.add
            f32.mul
            local.tee $l7
            f32.mul
            local.tee $l9
            f32.mul
            f32.add
            local.set $l5
            local.get $l58
            i32.const 3111960
            i32.add
            f32.load
            local.get $l14
            f32.mul
            local.get $l20
            local.get $l17
            f32.mul
            local.tee $l15
            f32.mul
            local.get $l52
            i32.const 3111960
            i32.add
            f32.load
            local.get $l10
            local.get $l8
            local.get $l7
            f32.mul
            local.tee $l20
            f32.mul
            f32.mul
            f32.add
            local.set $l7
            local.get $l58
            i32.const 3111956
            i32.add
            f32.load
            local.get $l14
            f32.mul
            local.get $l19
            f32.mul
            local.get $l52
            i32.const 3111956
            i32.add
            f32.load
            local.get $l10
            local.get $l9
            f32.mul
            f32.mul
            f32.add
            local.set $l8
            local.get $l52
            i32.const 3111952
            i32.add
            f32.load
            local.get $l10
            local.get $l15
            f32.mul
            f32.mul
            local.get $l58
            i32.const 3111952
            i32.add
            f32.load
            local.get $l14
            f32.mul
            local.get $l20
            f32.mul
            f32.add
            local.set $l10
            i32.const 1
          end
          local.set $l32
          local.get $l53
          i32.const 4
          i32.shl
          local.get $l51
          local.get $l36
          i32.const 12
          i32.add
          i32.add
          i32.const 0
          local.get $l51
          select
          i32.add
          local.tee $l51
          local.get $l5
          f32.store offset=12
          local.get $l51
          local.get $l7
          f32.store offset=8
          local.get $l51
          local.get $l8
          f32.store offset=4
          local.get $l51
          local.get $l10
          f32.store
          local.get $l46
          local.get $l30
          i32.const 12
          i32.add
          i32.add
          i32.const 0
          local.get $l46
          select
          local.get $l53
          i32.add
          local.get $l32
          i32.store8
        end
        local.get $l34
        i32.const -1
        i32.ne
        if $I27
          local.get $l30
          i32.load offset=20
          local.tee $l53
          local.get $l30
          i32.const 20
          i32.add
          i32.add
          i32.const 0
          local.get $l53
          select
          local.set $l30
          local.get $l36
          i32.load offset=20
          local.tee $l53
          local.get $l36
          i32.const 20
          i32.add
          i32.add
          i32.const 0
          local.get $l53
          select
          local.set $l53
          block $B28 (result i32)
            local.get $l28
            i32.load offset=20
            local.get $l34
            i32.const 1
            i32.shl
            i32.add
            i32.load16_s
            local.tee $l36
            i32.const -1
            i32.eq
            if $I29
              local.get $l34
              i32.const 12
              i32.mul
              local.get $l31
              i32.load offset=20
              local.tee $l36
              local.get $l31
              i32.const 20
              i32.add
              i32.add
              i32.const 0
              local.get $l36
              select
              i32.add
              local.tee $l36
              i32.const 8
              i32.add
              local.set $l28
              local.get $l36
              i32.const 4
              i32.add
              br $B28
            end
            local.get $l39
            i32.load
            local.get $l36
            i32.const 2
            i32.shl
            i32.add
            local.tee $l36
            i32.const 8
            i32.add
            local.set $l28
            i32.const 1
            local.set $l33
            local.get $l36
            i32.const 4
            i32.add
          end
          local.set $l51
          local.get $l36
          f32.load
          local.set $l5
          local.get $l51
          f32.load
          local.set $l7
          local.get $l53
          local.get $l34
          i32.const 12
          i32.mul
          i32.add
          local.tee $l36
          local.get $l28
          f32.load
          f32.store offset=8
          local.get $l36
          local.get $l7
          f32.store offset=4
          local.get $l36
          local.get $l5
          f32.store
          local.get $l30
          local.get $l34
          i32.add
          local.get $l33
          i32.store8
        end
        local.get $l38
        i32.load8_u
        if $I30
          local.get $l31
          local.set $l30
          local.get $l39
          local.set $l31
          local.get $l50
          local.set $l28
          local.get $l37
          local.set $l33
          local.get $l40
          i32.load8_u offset=256
          i32.eqz
          local.set $l36
          i32.const 0
          local.set $l35
          local.get $l38
          i32.load offset=4
          local.tee $l34
          if $I31
            local.get $l34
            i32.load offset=28
            local.tee $l35
            local.get $l34
            i32.const 28
            i32.add
            i32.add
            i32.const 0
            local.get $l35
            select
            local.set $l35
          end
          local.get $l28
          i32.load offset=24
          local.tee $l44
          if $I32
            local.get $l33
            i32.load offset=28
            local.tee $l34
            local.get $l33
            i32.const 28
            i32.add
            i32.add
            i32.const 0
            local.get $l34
            select
            local.set $l33
            local.get $l30
            i32.load offset=28
            local.tee $l34
            local.get $l30
            i32.const 28
            i32.add
            i32.add
            i32.const 0
            local.get $l34
            select
            local.set $l30
            local.get $l28
            i32.load offset=28
            local.tee $l34
            local.get $l28
            i32.const 28
            i32.add
            i32.add
            i32.const 0
            local.get $l34
            select
            local.set $l32
            local.get $l31
            i32.load
            local.set $l31
            i32.const 0
            local.set $l34
            loop $L33
              block $B34
                local.get $l35
                if $I35
                  local.get $l34
                  local.get $l35
                  i32.add
                  i32.load8_u
                  i32.eqz
                  br_if $B34
                end
                local.get $l32
                local.get $l34
                i32.const 2
                i32.shl
                local.tee $l28
                i32.add
                local.get $l28
                local.get $l30
                i32.add
                local.get $l31
                local.get $l45
                i32.load offset=24
                local.get $l34
                i32.const 1
                i32.shl
                i32.add
                i32.load16_s
                local.tee $l28
                i32.const 2
                i32.shl
                i32.add
                local.get $l28
                i32.const -1
                i32.eq
                select
                f32.load
                f32.store
                local.get $l33
                local.get $l34
                i32.add
                local.get $l28
                i32.const -1
                i32.ne
                local.get $l36
                i32.or
                i32.store8
              end
              local.get $l34
              i32.const 1
              i32.add
              local.tee $l34
              local.get $l44
              i32.ne
              br_if $L33
            end
          end
        end
        local.get $l42
        i32.load8_u offset=76
        i32.eqz
        br_if $B15
        local.get $l40
        f32.load offset=224
        local.set $l13
        local.get $l42
        i32.load offset=72
        local.set $l31
        local.get $l42
        i32.load offset=68
        local.set $l33
        local.get $l42
        i32.load offset=64
        local.set $l30
        local.get $l60
        local.get $l64
        i32.or
        if $I36
          local.get $l33
          local.set $l35
          local.get $l31
          local.set $l28
          local.get $l45
          local.set $l36
          local.get $l54
          i32.load offset=4
          local.set $l55
          local.get $l29
          local.set $l34
          local.get $l29
          i32.const 256
          i32.add
          local.set $l49
          local.get $l29
          i32.const 456
          i32.add
          local.set $l59
          local.get $l48
          local.tee $l32
          i32.const 2080
          i32.add
          local.set $l62
          local.get $l32
          i32.load offset=2080
          local.set $l46
          block $B37 (result f32)
            block $B38
              local.get $l30
              local.tee $l44
              i32.const -1
              i32.eq
              br_if $B38
              local.get $l55
              i32.load offset=4
              local.get $l55
              i32.const 4
              i32.add
              i32.add
              local.get $l44
              i32.add
              i32.load8_u
              i32.eqz
              br_if $B38
              local.get $l36
              i32.load offset=4
              local.get $l44
              i32.const 1
              i32.shl
              i32.add
              i32.load16_s
              local.tee $l44
              i32.const -1
              i32.eq
              br_if $B38
              local.get $l32
              i32.const 2072
              i32.add
              local.tee $l56
              local.get $l32
              i32.load offset=2072
              i32.add
              local.tee $l47
              local.get $l44
              i32.const 3
              i32.shl
              local.tee $l57
              i32.add
              f32.load
              local.set $l6
              local.get $l47
              local.get $l44
              i32.const 1
              i32.add
              local.tee $l66
              i32.const 3
              i32.shl
              local.tee $l63
              i32.add
              f32.load
              local.set $l4
              local.get $l34
              local.get $l47
              local.get $l44
              i32.const 2
              i32.add
              local.tee $l67
              i32.const 3
              i32.shl
              local.tee $l65
              i32.add
              f32.load
              f32.store offset=8
              local.get $l34
              local.get $l4
              f32.store offset=4
              local.get $l34
              local.get $l6
              f32.store
              local.get $l32
              i32.load offset=2072
              local.get $l56
              i32.add
              local.tee $l47
              local.get $l57
              i32.add
              f32.load offset=4
              local.set $l6
              local.get $l47
              local.get $l63
              i32.add
              f32.load offset=4
              local.set $l4
              local.get $l49
              local.get $l47
              local.get $l65
              i32.add
              f32.load offset=4
              f32.store offset=8
              local.get $l49
              local.get $l4
              f32.store offset=4
              local.get $l49
              local.get $l6
              f32.store
              block $B39 (result i32)
                local.get $l46
                i32.eqz
                if $I40
                  local.get $l34
                  i32.const 8
                  i32.add
                  local.set $l47
                  local.get $l34
                  i32.const 4
                  i32.add
                  local.set $l56
                  local.get $l34
                  br $B39
                end
                local.get $l62
                i32.load
                local.get $l62
                i32.add
                local.tee $l57
                local.get $l67
                i32.const 2
                i32.shl
                i32.add
                local.set $l47
                local.get $l57
                local.get $l66
                i32.const 2
                i32.shl
                i32.add
                local.set $l56
                local.get $l57
                local.get $l44
                i32.const 2
                i32.shl
                i32.add
              end
              local.set $l44
              local.get $l47
              f32.load
              local.set $l6
              local.get $l44
              f32.load
              local.set $l11
              local.get $l56
              f32.load
              br $B37
            end
            local.get $l34
            i32.const 0
            i32.store offset=8
            local.get $l34
            i64.const 0
            i64.store align=4
            local.get $l49
            i32.const 0
            i32.store offset=8
            local.get $l49
            i64.const 0
            i64.store align=4
            f32.const 0x0p+0 (;=0;)
          end
          local.set $l4
          local.get $l59
          local.get $l6
          f32.store offset=8
          local.get $l59
          local.get $l4
          f32.store offset=4
          local.get $l59
          local.get $l11
          f32.store
          block $B41
            block $B42
              local.get $l35
              i32.const -1
              i32.eq
              br_if $B42
              local.get $l55
              i32.load offset=12
              local.get $l55
              i32.const 12
              i32.add
              i32.add
              local.get $l35
              i32.add
              i32.load8_u
              i32.eqz
              br_if $B42
              local.get $l35
              i32.const 1
              i32.shl
              local.tee $l47
              local.get $l36
              i32.load offset=8
              i32.add
              i32.load16_s
              local.tee $l44
              i32.const -1
              i32.ne
              if $I43
                local.get $l32
                i32.const 2072
                i32.add
                local.tee $l63
                local.get $l32
                i32.load offset=2072
                i32.add
                local.tee $l35
                local.get $l44
                i32.const 3
                i32.shl
                local.tee $l65
                i32.add
                f32.load
                local.set $l6
                local.get $l35
                local.get $l44
                i32.const 1
                i32.add
                local.tee $l52
                i32.const 3
                i32.shl
                local.tee $l66
                i32.add
                f32.load
                local.set $l4
                local.get $l35
                local.get $l44
                i32.const 2
                i32.add
                local.tee $l51
                i32.const 3
                i32.shl
                local.tee $l67
                i32.add
                f32.load
                local.set $l11
                local.get $l34
                i32.const 24
                i32.add
                local.tee $l47
                local.get $l35
                local.get $l44
                i32.const 3
                i32.add
                local.tee $l53
                i32.const 3
                i32.shl
                local.tee $l58
                i32.add
                f32.load
                f32.store
                local.get $l34
                i32.const 20
                i32.add
                local.tee $l56
                local.get $l11
                f32.store
                local.get $l34
                i32.const 16
                i32.add
                local.tee $l57
                local.get $l4
                f32.store
                local.get $l34
                local.get $l6
                f32.store offset=12
                local.get $l32
                i32.load offset=2072
                local.get $l63
                i32.add
                local.tee $l35
                local.get $l65
                i32.add
                f32.load offset=4
                local.set $l6
                local.get $l35
                local.get $l66
                i32.add
                f32.load offset=4
                local.set $l4
                local.get $l35
                local.get $l67
                i32.add
                f32.load offset=4
                local.set $l11
                local.get $l49
                local.get $l35
                local.get $l58
                i32.add
                f32.load offset=4
                f32.store offset=24
                local.get $l49
                local.get $l11
                f32.store offset=20
                local.get $l49
                local.get $l4
                f32.store offset=16
                local.get $l49
                local.get $l6
                f32.store offset=12
                local.get $l46
                if $I44 (result i32)
                  local.get $l62
                  i32.load
                  local.get $l62
                  i32.add
                  local.tee $l35
                  local.get $l53
                  i32.const 2
                  i32.shl
                  i32.add
                  local.set $l47
                  local.get $l35
                  local.get $l51
                  i32.const 2
                  i32.shl
                  i32.add
                  local.set $l56
                  local.get $l35
                  local.get $l52
                  i32.const 2
                  i32.shl
                  i32.add
                  local.set $l57
                  local.get $l35
                  local.get $l44
                  i32.const 2
                  i32.shl
                  i32.add
                else
                  local.get $l34
                  i32.const 12
                  i32.add
                end
                f32.load
                local.set $l6
                local.get $l57
                f32.load
                local.set $l4
                local.get $l56
                f32.load
                local.set $l11
                local.get $l47
                f32.load
                local.set $l18
                br $B41
              end
              local.get $l36
              i32.load offset=12
              local.get $l47
              i32.add
              i32.load16_s
              local.tee $l44
              i32.const -1
              i32.eq
              br_if $B42
              local.get $l32
              i32.load offset=2072
              local.get $l32
              i32.const 2072
              i32.add
              i32.add
              local.tee $l47
              local.get $l44
              i32.const 2
              i32.add
              local.tee $l63
              i32.const 3
              i32.shl
              i32.add
              local.tee $l56
              f32.load offset=4
              local.set $l12
              local.get $l47
              local.get $l44
              i32.const 1
              i32.add
              local.tee $l65
              i32.const 3
              i32.shl
              i32.add
              local.tee $l57
              f32.load offset=4
              local.set $l21
              local.get $l47
              local.get $l44
              i32.const 3
              i32.shl
              i32.add
              local.tee $l47
              f32.load offset=4
              local.set $l24
              local.get $l36
              i32.load offset=16
              local.get $l35
              i32.const 1
              i32.shl
              i32.add
              i32.load16_s
              local.set $l35
              local.get $l47
              f32.load
              local.tee $l6
              local.set $l16
              local.get $l57
              f32.load
              local.tee $l18
              local.set $l20
              local.get $l56
              f32.load
              local.tee $l4
              local.set $l5
              local.get $l46
              if $I45
                local.get $l62
                i32.load
                local.get $l62
                i32.add
                local.tee $l47
                local.get $l63
                i32.const 2
                i32.shl
                i32.add
                f32.load
                local.set $l5
                local.get $l47
                local.get $l65
                i32.const 2
                i32.shl
                i32.add
                f32.load
                local.set $l20
                local.get $l47
                local.get $l44
                i32.const 2
                i32.shl
                i32.add
                f32.load
                local.set $l16
              end
              local.get $l4
              f32.const 0x1.1df46ap-6 (;=0.0174533;)
              f32.mul
              f32.const 0x1p-1 (;=0.5;)
              f32.mul
              f32.const 0x1.45f306p-3 (;=0.159155;)
              f32.mul
              local.tee $l11
              f32.const -0x1p-2 (;=-0.25;)
              f32.add
              local.tee $l27
              call $f66998
              local.set $l9
              local.get $l6
              f32.const 0x1.1df46ap-6 (;=0.0174533;)
              f32.mul
              f32.const 0x1p-1 (;=0.5;)
              f32.mul
              f32.const 0x1.45f306p-3 (;=0.159155;)
              f32.mul
              local.tee $l4
              f32.const -0x1p-2 (;=-0.25;)
              f32.add
              local.tee $l7
              call $f66998
              local.set $l8
              local.get $l18
              f32.const 0x1.1df46ap-6 (;=0.0174533;)
              f32.mul
              f32.const 0x1p-1 (;=0.5;)
              f32.mul
              f32.const 0x1.45f306p-3 (;=0.159155;)
              f32.mul
              local.tee $l6
              f32.const -0x1p-2 (;=-0.25;)
              f32.add
              local.tee $l10
              call $f66998
              local.set $l15
              local.get $l11
              call $f66998
              local.set $l25
              local.get $l4
              call $f66998
              local.set $l23
              local.get $l34
              f32.const 0x1p-2 (;=0.25;)
              local.get $l6
              local.get $l6
              call $f66998
              f32.sub
              f32.abs
              f32.sub
              local.tee $l6
              local.get $l6
              local.get $l6
              f32.mul
              local.tee $l6
              local.get $l6
              f32.mul
              local.tee $l18
              local.get $l18
              f32.mul
              f32.const 0x1.3d419ap+5 (;=39.657;)
              f32.mul
              f32.const 0x1.921fb4p+2 (;=6.28319;)
              local.get $l6
              f32.const 0x1.4abbb8p+5 (;=41.3417;)
              f32.mul
              f32.sub
              local.get $l18
              f32.const 0x1.466844p+6 (;=81.6018;)
              local.get $l6
              f32.const 0x1.324644p+6 (;=76.5686;)
              f32.mul
              f32.sub
              f32.mul
              f32.add
              f32.add
              f32.mul
              local.tee $l6
              f32.const 0x1p-2 (;=0.25;)
              local.get $l4
              local.get $l23
              f32.sub
              f32.abs
              f32.sub
              local.tee $l4
              local.get $l4
              local.get $l4
              f32.mul
              local.tee $l4
              local.get $l4
              f32.mul
              local.tee $l18
              local.get $l18
              f32.mul
              f32.const 0x1.3d419ap+5 (;=39.657;)
              f32.mul
              f32.const 0x1.921fb4p+2 (;=6.28319;)
              local.get $l4
              f32.const 0x1.4abbb8p+5 (;=41.3417;)
              f32.mul
              f32.sub
              local.get $l18
              f32.const 0x1.466844p+6 (;=81.6018;)
              local.get $l4
              f32.const 0x1.324644p+6 (;=76.5686;)
              f32.mul
              f32.sub
              f32.mul
              f32.add
              f32.add
              f32.mul
              local.tee $l23
              f32.const 0x1p-2 (;=0.25;)
              local.get $l11
              local.get $l25
              f32.sub
              f32.abs
              f32.sub
              local.tee $l4
              local.get $l4
              local.get $l4
              f32.mul
              local.tee $l4
              local.get $l4
              f32.mul
              local.tee $l11
              local.get $l11
              f32.mul
              f32.const 0x1.3d419ap+5 (;=39.657;)
              f32.mul
              f32.const 0x1.921fb4p+2 (;=6.28319;)
              local.get $l4
              f32.const 0x1.4abbb8p+5 (;=41.3417;)
              f32.mul
              f32.sub
              local.get $l11
              f32.const 0x1.466844p+6 (;=81.6018;)
              local.get $l4
              f32.const 0x1.324644p+6 (;=76.5686;)
              f32.mul
              f32.sub
              f32.mul
              f32.add
              f32.add
              f32.mul
              local.tee $l25
              f32.mul
              local.tee $l26
              f32.mul
              local.get $l35
              i32.const 5
              i32.shl
              local.tee $l35
              i32.const 3111964
              i32.add
              f32.load
              local.tee $l11
              f32.mul
              f32.const 0x1p-2 (;=0.25;)
              local.get $l7
              local.get $l8
              f32.sub
              f32.abs
              f32.sub
              local.tee $l4
              local.get $l4
              local.get $l4
              f32.mul
              local.tee $l4
              local.get $l4
              f32.mul
              local.tee $l18
              local.get $l18
              f32.mul
              f32.const 0x1.3d419ap+5 (;=39.657;)
              f32.mul
              f32.const 0x1.921fb4p+2 (;=6.28319;)
              local.get $l4
              f32.const 0x1.4abbb8p+5 (;=41.3417;)
              f32.mul
              f32.sub
              local.get $l18
              f32.const 0x1.466844p+6 (;=81.6018;)
              local.get $l4
              f32.const 0x1.324644p+6 (;=76.5686;)
              f32.mul
              f32.sub
              f32.mul
              f32.add
              f32.add
              f32.mul
              local.tee $l7
              f32.const 0x1p-2 (;=0.25;)
              local.get $l27
              local.get $l9
              f32.sub
              f32.abs
              f32.sub
              local.tee $l4
              local.get $l4
              local.get $l4
              f32.mul
              local.tee $l4
              local.get $l4
              f32.mul
              local.tee $l18
              local.get $l18
              f32.mul
              f32.const 0x1.3d419ap+5 (;=39.657;)
              f32.mul
              f32.const 0x1.921fb4p+2 (;=6.28319;)
              local.get $l4
              f32.const 0x1.4abbb8p+5 (;=41.3417;)
              f32.mul
              f32.sub
              local.get $l18
              f32.const 0x1.466844p+6 (;=81.6018;)
              local.get $l4
              f32.const 0x1.324644p+6 (;=76.5686;)
              f32.mul
              f32.sub
              f32.mul
              f32.add
              f32.add
              f32.mul
              local.tee $l27
              f32.mul
              local.tee $l8
              f32.const 0x1p-2 (;=0.25;)
              local.get $l10
              local.get $l15
              f32.sub
              f32.abs
              f32.sub
              local.tee $l4
              local.get $l4
              local.get $l4
              f32.mul
              local.tee $l4
              local.get $l4
              f32.mul
              local.tee $l18
              local.get $l18
              f32.mul
              f32.const 0x1.3d419ap+5 (;=39.657;)
              f32.mul
              f32.const 0x1.921fb4p+2 (;=6.28319;)
              local.get $l4
              f32.const 0x1.4abbb8p+5 (;=41.3417;)
              f32.mul
              f32.sub
              local.get $l18
              f32.const 0x1.466844p+6 (;=81.6018;)
              local.get $l4
              f32.const 0x1.324644p+6 (;=76.5686;)
              f32.mul
              f32.sub
              f32.mul
              f32.add
              f32.add
              f32.mul
              local.tee $l4
              local.get $l35
              i32.const 16
              i32.or
              local.tee $l44
              i32.const 3111964
              i32.add
              f32.load
              local.tee $l18
              f32.mul
              f32.mul
              f32.add
              f32.store offset=24
              local.get $l34
              local.get $l6
              local.get $l23
              local.get $l27
              f32.mul
              local.tee $l23
              f32.mul
              local.get $l35
              i32.const 3111960
              i32.add
              f32.load
              local.tee $l27
              f32.mul
              local.get $l7
              local.get $l25
              f32.mul
              local.tee $l10
              local.get $l4
              local.get $l44
              i32.const 3111960
              i32.add
              f32.load
              local.tee $l9
              f32.mul
              f32.mul
              f32.add
              f32.store offset=20
              local.get $l34
              local.get $l6
              local.get $l8
              f32.mul
              local.get $l35
              i32.const 3111956
              i32.add
              f32.load
              local.tee $l7
              f32.mul
              local.get $l26
              local.get $l4
              local.get $l44
              i32.const 3111956
              i32.add
              f32.load
              local.tee $l8
              f32.mul
              f32.mul
              f32.add
              f32.store offset=16
              local.get $l34
              local.get $l6
              local.get $l10
              f32.mul
              local.get $l35
              i32.const 3111952
              i32.add
              f32.load
              local.tee $l10
              f32.mul
              local.get $l23
              local.get $l4
              local.get $l44
              i32.const 3111952
              i32.add
              f32.load
              local.tee $l15
              f32.mul
              f32.mul
              f32.add
              f32.store offset=12
              local.get $l12
              f32.const 0x1.1df46ap-6 (;=0.0174533;)
              f32.mul
              f32.const 0x1p-1 (;=0.5;)
              f32.mul
              f32.const 0x1.45f306p-3 (;=0.159155;)
              f32.mul
              local.tee $l12
              f32.const -0x1p-2 (;=-0.25;)
              f32.add
              local.tee $l25
              call $f66998
              local.set $l23
              local.get $l24
              f32.const 0x1.1df46ap-6 (;=0.0174533;)
              f32.mul
              f32.const 0x1p-1 (;=0.5;)
              f32.mul
              f32.const 0x1.45f306p-3 (;=0.159155;)
              f32.mul
              local.tee $l4
              f32.const -0x1p-2 (;=-0.25;)
              f32.add
              local.tee $l24
              call $f66998
              local.set $l26
              local.get $l21
              f32.const 0x1.1df46ap-6 (;=0.0174533;)
              f32.mul
              f32.const 0x1p-1 (;=0.5;)
              f32.mul
              f32.const 0x1.45f306p-3 (;=0.159155;)
              f32.mul
              local.tee $l6
              f32.const -0x1p-2 (;=-0.25;)
              f32.add
              local.tee $l14
              call $f66998
              local.set $l22
              local.get $l12
              call $f66998
              local.set $l17
              local.get $l4
              call $f66998
              local.set $l19
              local.get $l49
              f32.const 0x1p-2 (;=0.25;)
              local.get $l6
              local.get $l6
              call $f66998
              f32.sub
              f32.abs
              f32.sub
              local.tee $l6
              local.get $l6
              local.get $l6
              f32.mul
              local.tee $l6
              local.get $l6
              f32.mul
              local.tee $l21
              local.get $l21
              f32.mul
              f32.const 0x1.3d419ap+5 (;=39.657;)
              f32.mul
              f32.const 0x1.921fb4p+2 (;=6.28319;)
              local.get $l6
              f32.const 0x1.4abbb8p+5 (;=41.3417;)
              f32.mul
              f32.sub
              local.get $l21
              f32.const 0x1.466844p+6 (;=81.6018;)
              local.get $l6
              f32.const 0x1.324644p+6 (;=76.5686;)
              f32.mul
              f32.sub
              f32.mul
              f32.add
              f32.add
              f32.mul
              local.tee $l6
              f32.const 0x1p-2 (;=0.25;)
              local.get $l4
              local.get $l19
              f32.sub
              f32.abs
              f32.sub
              local.tee $l4
              local.get $l4
              local.get $l4
              f32.mul
              local.tee $l4
              local.get $l4
              f32.mul
              local.tee $l21
              local.get $l21
              f32.mul
              f32.const 0x1.3d419ap+5 (;=39.657;)
              f32.mul
              f32.const 0x1.921fb4p+2 (;=6.28319;)
              local.get $l4
              f32.const 0x1.4abbb8p+5 (;=41.3417;)
              f32.mul
              f32.sub
              local.get $l21
              f32.const 0x1.466844p+6 (;=81.6018;)
              local.get $l4
              f32.const 0x1.324644p+6 (;=76.5686;)
              f32.mul
              f32.sub
              f32.mul
              f32.add
              f32.add
              f32.mul
              local.tee $l21
              f32.const 0x1p-2 (;=0.25;)
              local.get $l12
              local.get $l17
              f32.sub
              f32.abs
              f32.sub
              local.tee $l4
              local.get $l4
              local.get $l4
              f32.mul
              local.tee $l4
              local.get $l4
              f32.mul
              local.tee $l12
              local.get $l12
              f32.mul
              f32.const 0x1.3d419ap+5 (;=39.657;)
              f32.mul
              f32.const 0x1.921fb4p+2 (;=6.28319;)
              local.get $l4
              f32.const 0x1.4abbb8p+5 (;=41.3417;)
              f32.mul
              f32.sub
              local.get $l12
              f32.const 0x1.466844p+6 (;=81.6018;)
              local.get $l4
              f32.const 0x1.324644p+6 (;=76.5686;)
              f32.mul
              f32.sub
              f32.mul
              f32.add
              f32.add
              f32.mul
              local.tee $l17
              f32.mul
              local.tee $l19
              f32.mul
              local.get $l11
              f32.mul
              f32.const 0x1p-2 (;=0.25;)
              local.get $l24
              local.get $l26
              f32.sub
              f32.abs
              f32.sub
              local.tee $l4
              local.get $l4
              local.get $l4
              f32.mul
              local.tee $l4
              local.get $l4
              f32.mul
              local.tee $l12
              local.get $l12
              f32.mul
              f32.const 0x1.3d419ap+5 (;=39.657;)
              f32.mul
              f32.const 0x1.921fb4p+2 (;=6.28319;)
              local.get $l4
              f32.const 0x1.4abbb8p+5 (;=41.3417;)
              f32.mul
              f32.sub
              local.get $l12
              f32.const 0x1.466844p+6 (;=81.6018;)
              local.get $l4
              f32.const 0x1.324644p+6 (;=76.5686;)
              f32.mul
              f32.sub
              f32.mul
              f32.add
              f32.add
              f32.mul
              local.tee $l24
              f32.const 0x1p-2 (;=0.25;)
              local.get $l25
              local.get $l23
              f32.sub
              f32.abs
              f32.sub
              local.tee $l4
              local.get $l4
              local.get $l4
              f32.mul
              local.tee $l4
              local.get $l4
              f32.mul
              local.tee $l12
              local.get $l12
              f32.mul
              f32.const 0x1.3d419ap+5 (;=39.657;)
              f32.mul
              f32.const 0x1.921fb4p+2 (;=6.28319;)
              local.get $l4
              f32.const 0x1.4abbb8p+5 (;=41.3417;)
              f32.mul
              f32.sub
              local.get $l12
              f32.const 0x1.466844p+6 (;=81.6018;)
              local.get $l4
              f32.const 0x1.324644p+6 (;=76.5686;)
              f32.mul
              f32.sub
              f32.mul
              f32.add
              f32.add
              f32.mul
              local.tee $l25
              f32.mul
              local.tee $l23
              f32.const 0x1p-2 (;=0.25;)
              local.get $l14
              local.get $l22
              f32.sub
              f32.abs
              f32.sub
              local.tee $l4
              local.get $l4
              local.get $l4
              f32.mul
              local.tee $l4
              local.get $l4
              f32.mul
              local.tee $l12
              local.get $l12
              f32.mul
              f32.const 0x1.3d419ap+5 (;=39.657;)
              f32.mul
              f32.const 0x1.921fb4p+2 (;=6.28319;)
              local.get $l4
              f32.const 0x1.4abbb8p+5 (;=41.3417;)
              f32.mul
              f32.sub
              local.get $l12
              f32.const 0x1.466844p+6 (;=81.6018;)
              local.get $l4
              f32.const 0x1.324644p+6 (;=76.5686;)
              f32.mul
              f32.sub
              f32.mul
              f32.add
              f32.add
              f32.mul
              local.tee $l4
              local.get $l18
              f32.mul
              f32.mul
              f32.add
              f32.store offset=24
              local.get $l49
              local.get $l6
              local.get $l21
              local.get $l25
              f32.mul
              local.tee $l12
              f32.mul
              local.get $l27
              f32.mul
              local.get $l24
              local.get $l17
              f32.mul
              local.tee $l21
              local.get $l4
              local.get $l9
              f32.mul
              f32.mul
              f32.add
              f32.store offset=20
              local.get $l49
              local.get $l6
              local.get $l23
              f32.mul
              local.get $l7
              f32.mul
              local.get $l19
              local.get $l4
              local.get $l8
              f32.mul
              f32.mul
              f32.add
              f32.store offset=16
              local.get $l49
              local.get $l6
              local.get $l21
              f32.mul
              local.get $l10
              f32.mul
              local.get $l12
              local.get $l4
              local.get $l15
              f32.mul
              f32.mul
              f32.add
              f32.store offset=12
              local.get $l5
              f32.const 0x1.1df46ap-6 (;=0.0174533;)
              f32.mul
              f32.const 0x1p-1 (;=0.5;)
              f32.mul
              f32.const 0x1.45f306p-3 (;=0.159155;)
              f32.mul
              local.tee $l12
              f32.const -0x1p-2 (;=-0.25;)
              f32.add
              local.tee $l5
              call $f66998
              local.set $l24
              local.get $l16
              f32.const 0x1.1df46ap-6 (;=0.0174533;)
              f32.mul
              f32.const 0x1p-1 (;=0.5;)
              f32.mul
              f32.const 0x1.45f306p-3 (;=0.159155;)
              f32.mul
              local.tee $l4
              f32.const -0x1p-2 (;=-0.25;)
              f32.add
              local.tee $l16
              call $f66998
              local.set $l25
              local.get $l20
              f32.const 0x1.1df46ap-6 (;=0.0174533;)
              f32.mul
              f32.const 0x1p-1 (;=0.5;)
              f32.mul
              f32.const 0x1.45f306p-3 (;=0.159155;)
              f32.mul
              local.tee $l6
              f32.const -0x1p-2 (;=-0.25;)
              f32.add
              local.tee $l20
              call $f66998
              local.set $l23
              local.get $l12
              call $f66998
              local.set $l26
              local.get $l4
              call $f66998
              local.set $l14
              f32.const 0x1p-2 (;=0.25;)
              local.get $l6
              local.get $l6
              call $f66998
              f32.sub
              f32.abs
              f32.sub
              local.tee $l6
              local.get $l6
              local.get $l6
              f32.mul
              local.tee $l6
              local.get $l6
              f32.mul
              local.tee $l21
              local.get $l21
              f32.mul
              f32.const 0x1.3d419ap+5 (;=39.657;)
              f32.mul
              f32.const 0x1.921fb4p+2 (;=6.28319;)
              local.get $l6
              f32.const 0x1.4abbb8p+5 (;=41.3417;)
              f32.mul
              f32.sub
              local.get $l21
              f32.const 0x1.466844p+6 (;=81.6018;)
              local.get $l6
              f32.const 0x1.324644p+6 (;=76.5686;)
              f32.mul
              f32.sub
              f32.mul
              f32.add
              f32.add
              f32.mul
              local.tee $l6
              f32.const 0x1p-2 (;=0.25;)
              local.get $l4
              local.get $l14
              f32.sub
              f32.abs
              f32.sub
              local.tee $l4
              local.get $l4
              local.get $l4
              f32.mul
              local.tee $l4
              local.get $l4
              f32.mul
              local.tee $l21
              local.get $l21
              f32.mul
              f32.const 0x1.3d419ap+5 (;=39.657;)
              f32.mul
              f32.const 0x1.921fb4p+2 (;=6.28319;)
              local.get $l4
              f32.const 0x1.4abbb8p+5 (;=41.3417;)
              f32.mul
              f32.sub
              local.get $l21
              f32.const 0x1.466844p+6 (;=81.6018;)
              local.get $l4
              f32.const 0x1.324644p+6 (;=76.5686;)
              f32.mul
              f32.sub
              f32.mul
              f32.add
              f32.add
              f32.mul
              local.tee $l21
              f32.const 0x1p-2 (;=0.25;)
              local.get $l12
              local.get $l26
              f32.sub
              f32.abs
              f32.sub
              local.tee $l4
              local.get $l4
              local.get $l4
              f32.mul
              local.tee $l4
              local.get $l4
              f32.mul
              local.tee $l12
              local.get $l12
              f32.mul
              f32.const 0x1.3d419ap+5 (;=39.657;)
              f32.mul
              f32.const 0x1.921fb4p+2 (;=6.28319;)
              local.get $l4
              f32.const 0x1.4abbb8p+5 (;=41.3417;)
              f32.mul
              f32.sub
              local.get $l12
              f32.const 0x1.466844p+6 (;=81.6018;)
              local.get $l4
              f32.const 0x1.324644p+6 (;=76.5686;)
              f32.mul
              f32.sub
              f32.mul
              f32.add
              f32.add
              f32.mul
              local.tee $l26
              f32.mul
              local.tee $l14
              f32.mul
              local.get $l11
              f32.mul
              f32.const 0x1p-2 (;=0.25;)
              local.get $l16
              local.get $l25
              f32.sub
              f32.abs
              f32.sub
              local.tee $l4
              local.get $l4
              local.get $l4
              f32.mul
              local.tee $l4
              local.get $l4
              f32.mul
              local.tee $l11
              local.get $l11
              f32.mul
              f32.const 0x1.3d419ap+5 (;=39.657;)
              f32.mul
              f32.const 0x1.921fb4p+2 (;=6.28319;)
              local.get $l4
              f32.const 0x1.4abbb8p+5 (;=41.3417;)
              f32.mul
              f32.sub
              local.get $l11
              f32.const 0x1.466844p+6 (;=81.6018;)
              local.get $l4
              f32.const 0x1.324644p+6 (;=76.5686;)
              f32.mul
              f32.sub
              f32.mul
              f32.add
              f32.add
              f32.mul
              local.tee $l16
              f32.const 0x1p-2 (;=0.25;)
              local.get $l5
              local.get $l24
              f32.sub
              f32.abs
              f32.sub
              local.tee $l4
              local.get $l4
              local.get $l4
              f32.mul
              local.tee $l4
              local.get $l4
              f32.mul
              local.tee $l11
              local.get $l11
              f32.mul
              f32.const 0x1.3d419ap+5 (;=39.657;)
              f32.mul
              f32.const 0x1.921fb4p+2 (;=6.28319;)
              local.get $l4
              f32.const 0x1.4abbb8p+5 (;=41.3417;)
              f32.mul
              f32.sub
              local.get $l11
              f32.const 0x1.466844p+6 (;=81.6018;)
              local.get $l4
              f32.const 0x1.324644p+6 (;=76.5686;)
              f32.mul
              f32.sub
              f32.mul
              f32.add
              f32.add
              f32.mul
              local.tee $l5
              f32.mul
              local.tee $l24
              f32.const 0x1p-2 (;=0.25;)
              local.get $l20
              local.get $l23
              f32.sub
              f32.abs
              f32.sub
              local.tee $l4
              local.get $l4
              local.get $l4
              f32.mul
              local.tee $l4
              local.get $l4
              f32.mul
              local.tee $l11
              local.get $l11
              f32.mul
              f32.const 0x1.3d419ap+5 (;=39.657;)
              f32.mul
              f32.const 0x1.921fb4p+2 (;=6.28319;)
              local.get $l4
              f32.const 0x1.4abbb8p+5 (;=41.3417;)
              f32.mul
              f32.sub
              local.get $l11
              f32.const 0x1.466844p+6 (;=81.6018;)
              local.get $l4
              f32.const 0x1.324644p+6 (;=76.5686;)
              f32.mul
              f32.sub
              f32.mul
              f32.add
              f32.add
              f32.mul
              local.tee $l12
              local.get $l18
              f32.mul
              f32.mul
              f32.add
              local.set $l18
              local.get $l6
              local.get $l21
              local.get $l5
              f32.mul
              local.tee $l21
              f32.mul
              local.get $l27
              f32.mul
              local.get $l16
              local.get $l26
              f32.mul
              local.tee $l27
              local.get $l12
              local.get $l9
              f32.mul
              f32.mul
              f32.add
              local.set $l11
              local.get $l6
              local.get $l24
              f32.mul
              local.get $l7
              f32.mul
              local.get $l14
              local.get $l12
              local.get $l8
              f32.mul
              f32.mul
              f32.add
              local.set $l4
              local.get $l6
              local.get $l27
              f32.mul
              local.get $l10
              f32.mul
              local.get $l21
              local.get $l12
              local.get $l15
              f32.mul
              f32.mul
              f32.add
              local.set $l6
              br $B41
            end
            local.get $l34
            i64.const 0
            i64.store offset=12 align=4
            local.get $l34
            i64.const 4575657221408423936
            i64.store offset=20 align=4
            local.get $l49
            i64.const 4575657221408423936
            i64.store offset=20 align=4
            local.get $l49
            i64.const 0
            i64.store offset=12 align=4
            f32.const 0x1p+0 (;=1;)
            local.set $l18
            f32.const 0x0p+0 (;=0;)
            local.set $l6
            f32.const 0x0p+0 (;=0;)
            local.set $l4
            f32.const 0x0p+0 (;=0;)
            local.set $l11
          end
          local.get $l59
          local.get $l6
          f32.store offset=12
          local.get $l59
          local.get $l18
          f32.store offset=24
          local.get $l59
          local.get $l11
          f32.store offset=20
          local.get $l59
          local.get $l4
          f32.store offset=16
          block $B46 (result f32)
            block $B47
              local.get $l28
              i32.const -1
              i32.eq
              br_if $B47
              local.get $l55
              i32.load offset=20
              local.get $l55
              i32.const 20
              i32.add
              i32.add
              local.get $l28
              i32.add
              i32.load8_u
              i32.eqz
              br_if $B47
              local.get $l36
              i32.load offset=20
              local.get $l28
              i32.const 1
              i32.shl
              i32.add
              i32.load16_s
              local.tee $l55
              i32.const -1
              i32.eq
              br_if $B47
              local.get $l32
              i32.const 2072
              i32.add
              local.tee $l44
              local.get $l32
              i32.load offset=2072
              i32.add
              local.tee $l35
              local.get $l55
              i32.const 3
              i32.shl
              local.tee $l36
              i32.add
              f32.load
              local.set $l6
              local.get $l35
              local.get $l55
              i32.const 1
              i32.add
              local.tee $l57
              i32.const 3
              i32.shl
              local.tee $l47
              i32.add
              f32.load
              local.set $l4
              local.get $l34
              i32.const 36
              i32.add
              local.tee $l28
              local.get $l35
              local.get $l55
              i32.const 2
              i32.add
              local.tee $l63
              i32.const 3
              i32.shl
              local.tee $l56
              i32.add
              f32.load
              f32.store
              local.get $l34
              i32.const 32
              i32.add
              local.tee $l35
              local.get $l4
              f32.store
              local.get $l34
              local.get $l6
              f32.store offset=28
              local.get $l32
              i32.load offset=2072
              local.get $l44
              i32.add
              local.tee $l32
              local.get $l36
              i32.add
              f32.load offset=4
              local.set $l6
              local.get $l32
              local.get $l47
              i32.add
              f32.load offset=4
              local.set $l4
              local.get $l49
              local.get $l32
              local.get $l56
              i32.add
              f32.load offset=4
              f32.store offset=36
              local.get $l49
              local.get $l4
              f32.store offset=32
              local.get $l49
              local.get $l6
              f32.store offset=28
              local.get $l46
              if $I48 (result i32)
                local.get $l62
                i32.load
                local.get $l62
                i32.add
                local.tee $l34
                local.get $l63
                i32.const 2
                i32.shl
                i32.add
                local.set $l28
                local.get $l34
                local.get $l57
                i32.const 2
                i32.shl
                i32.add
                local.set $l35
                local.get $l34
                local.get $l55
                i32.const 2
                i32.shl
                i32.add
              else
                local.get $l34
                i32.const 28
                i32.add
              end
              local.set $l34
              local.get $l28
              f32.load
              local.set $l6
              local.get $l34
              f32.load
              local.set $l11
              local.get $l35
              f32.load
              br $B46
            end
            local.get $l34
            i64.const 4575657222473777152
            i64.store offset=28 align=4
            local.get $l34
            i32.const 1065353216
            i32.store offset=36
            local.get $l49
            i32.const 1065353216
            i32.store offset=36
            local.get $l49
            i64.const 4575657222473777152
            i64.store offset=28 align=4
            f32.const 0x1p+0 (;=1;)
            local.set $l11
            f32.const 0x1p+0 (;=1;)
            local.set $l6
            f32.const 0x1p+0 (;=1;)
          end
          local.set $l4
          local.get $l59
          local.get $l11
          f32.store offset=28
          local.get $l59
          local.get $l6
          f32.store offset=36
          local.get $l59
          local.get $l4
          f32.store offset=32
        end
        local.get $l64
        if $I49
          local.get $l29
          i32.const 456
          i32.add
          local.set $l32
          local.get $l54
          i32.load
          local.set $l36
          local.get $l30
          local.tee $l28
          i32.const -1
          i32.ne
          if $I50
            local.get $l32
            f32.load
            local.set $l7
            local.get $l32
            f32.load offset=4
            local.set $l8
            local.get $l36
            i32.load offset=4
            local.get $l36
            i32.const 4
            i32.add
            i32.add
            local.get $l28
            i32.const 12
            i32.mul
            i32.add
            local.tee $l28
            local.get $l28
            f32.load offset=8
            local.get $l32
            f32.load offset=8
            f32.sub
            f32.store offset=8
            local.get $l28
            local.get $l28
            f32.load offset=4
            local.get $l8
            f32.sub
            f32.store offset=4
            local.get $l28
            local.get $l28
            f32.load
            local.get $l7
            f32.sub
            f32.store
          end
          local.get $l33
          i32.const -1
          i32.ne
          if $I51
            local.get $l36
            i32.load offset=12
            local.get $l36
            i32.const 12
            i32.add
            i32.add
            local.get $l33
            i32.const 4
            i32.shl
            i32.add
            local.tee $l28
            local.get $l28
            f32.load offset=12
            local.tee $l7
            local.get $l32
            f32.load offset=24
            local.tee $l8
            f32.mul
            local.get $l28
            f32.load
            local.tee $l14
            local.get $l32
            i32.load offset=12
            i32.const -2147483648
            i32.xor
            f32.reinterpret_i32
            local.tee $l20
            f32.mul
            f32.sub
            local.get $l28
            f32.load offset=8
            local.tee $l9
            local.get $l32
            i32.load offset=20
            i32.const -2147483648
            i32.xor
            f32.reinterpret_i32
            local.tee $l15
            f32.mul
            f32.sub
            local.get $l28
            f32.load offset=4
            local.tee $l17
            local.get $l32
            i32.load offset=16
            i32.const -2147483648
            i32.xor
            f32.reinterpret_i32
            local.tee $l19
            f32.mul
            f32.sub
            local.tee $l10
            f32.const 0x1p+0 (;=1;)
            local.get $l10
            local.get $l10
            f32.mul
            local.get $l14
            local.get $l19
            f32.mul
            local.get $l9
            local.get $l8
            f32.mul
            f32.sub
            local.get $l7
            local.get $l15
            f32.mul
            f32.sub
            local.get $l17
            local.get $l20
            f32.mul
            f32.sub
            i32.reinterpret_f32
            i32.const -2147483648
            i32.xor
            f32.reinterpret_i32
            local.tee $l10
            local.get $l10
            f32.mul
            f32.add
            local.get $l17
            local.get $l15
            f32.mul
            local.get $l9
            local.get $l19
            f32.mul
            f32.sub
            local.get $l14
            local.get $l8
            f32.mul
            f32.sub
            local.get $l7
            local.get $l20
            f32.mul
            f32.sub
            i32.reinterpret_f32
            i32.const -2147483648
            i32.xor
            f32.reinterpret_i32
            local.tee $l22
            local.get $l22
            f32.mul
            local.get $l9
            local.get $l20
            f32.mul
            local.get $l14
            local.get $l15
            f32.mul
            f32.sub
            local.get $l17
            local.get $l8
            f32.mul
            f32.sub
            local.get $l7
            local.get $l19
            f32.mul
            f32.sub
            i32.reinterpret_f32
            i32.const -2147483648
            i32.xor
            f32.reinterpret_i32
            local.tee $l8
            local.get $l8
            f32.mul
            f32.add
            f32.add
            f32.sqrt
            f32.div
            local.tee $l7
            f32.mul
            f32.store offset=12
            local.get $l28
            local.get $l7
            local.get $l10
            f32.mul
            f32.store offset=8
            local.get $l28
            local.get $l7
            local.get $l8
            f32.mul
            f32.store offset=4
            local.get $l28
            local.get $l7
            local.get $l22
            f32.mul
            f32.store
          end
          local.get $l31
          i32.const -1
          i32.ne
          if $I52
            local.get $l32
            f32.load offset=32
            local.set $l7
            local.get $l32
            f32.load offset=28
            local.set $l8
            local.get $l36
            i32.load offset=20
            local.get $l36
            i32.const 20
            i32.add
            i32.add
            local.get $l31
            i32.const 12
            i32.mul
            i32.add
            local.tee $l28
            local.get $l28
            f32.load offset=8
            local.get $l32
            f32.load offset=36
            f32.sub
            f32.store offset=8
            local.get $l28
            local.get $l28
            f32.load offset=4
            local.get $l7
            f32.sub
            f32.store offset=4
            local.get $l28
            local.get $l28
            f32.load
            local.get $l8
            f32.sub
            f32.store
          end
        end
        local.get $l60
        i32.eqz
        br_if $B15
        local.get $l29
        i32.const 256
        i32.add
        local.set $l36
        local.get $l54
        i32.load
        local.set $l28
        local.get $l30
        i32.const -1
        i32.ne
        if $I53
          local.get $l36
          f32.load
          local.set $l5
          local.get $l29
          f32.load
          local.set $l16
          local.get $l36
          f32.load offset=4
          local.set $l7
          local.get $l29
          f32.load offset=4
          local.set $l8
          local.get $l28
          i32.load offset=4
          local.get $l28
          i32.const 4
          i32.add
          i32.add
          local.get $l30
          i32.const 12
          i32.mul
          i32.add
          local.tee $l30
          local.get $l30
          f32.load offset=8
          local.get $l29
          f32.load offset=8
          local.get $l36
          f32.load offset=8
          f32.sub
          local.get $l13
          f32.mul
          f32.add
          f32.store offset=8
          local.get $l30
          local.get $l30
          f32.load offset=4
          local.get $l8
          local.get $l7
          f32.sub
          local.get $l13
          f32.mul
          f32.add
          f32.store offset=4
          local.get $l30
          local.get $l30
          f32.load
          local.get $l16
          local.get $l5
          f32.sub
          local.get $l13
          f32.mul
          f32.add
          f32.store
        end
        local.get $l33
        i32.const -1
        i32.ne
        if $I54
          local.get $l28
          i32.load offset=12
          local.get $l28
          i32.const 12
          i32.add
          i32.add
          local.get $l33
          i32.const 4
          i32.shl
          i32.add
          local.tee $l30
          local.get $l30
          f32.load offset=12
          local.tee $l5
          local.get $l36
          f32.load offset=24
          local.tee $l16
          local.get $l29
          f32.load offset=24
          local.tee $l7
          f32.mul
          local.get $l29
          f32.load offset=12
          local.tee $l8
          local.get $l36
          i32.load offset=12
          i32.const -2147483648
          i32.xor
          f32.reinterpret_i32
          local.tee $l14
          f32.mul
          f32.sub
          local.get $l29
          f32.load offset=20
          local.tee $l20
          local.get $l36
          i32.load offset=20
          i32.const -2147483648
          i32.xor
          f32.reinterpret_i32
          local.tee $l10
          f32.mul
          f32.sub
          local.get $l29
          f32.load offset=16
          local.tee $l9
          local.get $l36
          i32.load offset=16
          i32.const -2147483648
          i32.xor
          f32.reinterpret_i32
          local.tee $l15
          f32.mul
          f32.sub
          local.tee $l17
          f32.const 0x1p+0 (;=1;)
          local.get $l9
          local.get $l10
          f32.mul
          local.get $l20
          local.get $l15
          f32.mul
          f32.sub
          local.get $l16
          local.get $l8
          f32.mul
          f32.sub
          local.get $l7
          local.get $l14
          f32.mul
          f32.sub
          i32.reinterpret_f32
          i32.const -2147483648
          i32.xor
          f32.reinterpret_i32
          local.get $l13
          f32.mul
          local.tee $l19
          local.get $l19
          f32.mul
          local.get $l20
          local.get $l14
          f32.mul
          local.get $l8
          local.get $l10
          f32.mul
          f32.sub
          local.get $l16
          local.get $l9
          f32.mul
          f32.sub
          local.get $l7
          local.get $l15
          f32.mul
          f32.sub
          i32.reinterpret_f32
          i32.const -2147483648
          i32.xor
          f32.reinterpret_i32
          local.get $l13
          f32.mul
          local.tee $l22
          local.get $l22
          f32.mul
          f32.add
          local.get $l17
          local.get $l17
          f32.mul
          local.get $l8
          local.get $l15
          f32.mul
          local.get $l16
          local.get $l20
          f32.mul
          f32.sub
          local.get $l7
          local.get $l10
          f32.mul
          f32.sub
          local.get $l9
          local.get $l14
          f32.mul
          f32.sub
          i32.reinterpret_f32
          i32.const -2147483648
          i32.xor
          f32.reinterpret_i32
          local.get $l13
          f32.mul
          local.tee $l10
          local.get $l10
          f32.mul
          f32.add
          f32.add
          f32.sqrt
          f32.div
          local.tee $l16
          f32.mul
          local.tee $l7
          f32.mul
          local.get $l30
          f32.load
          local.tee $l8
          local.get $l19
          local.get $l16
          f32.mul
          local.tee $l14
          f32.mul
          f32.sub
          local.get $l30
          f32.load offset=8
          local.tee $l20
          local.get $l10
          local.get $l16
          f32.mul
          local.tee $l10
          f32.mul
          f32.sub
          local.get $l30
          f32.load offset=4
          local.tee $l9
          local.get $l22
          local.get $l16
          f32.mul
          local.tee $l16
          f32.mul
          f32.sub
          local.tee $l15
          f32.const 0x1p+0 (;=1;)
          local.get $l20
          local.get $l16
          f32.mul
          local.get $l9
          local.get $l10
          f32.mul
          f32.sub
          local.get $l5
          local.get $l14
          f32.mul
          f32.sub
          local.get $l8
          local.get $l7
          f32.mul
          f32.sub
          i32.reinterpret_f32
          i32.const -2147483648
          i32.xor
          f32.reinterpret_i32
          local.tee $l17
          local.get $l17
          f32.mul
          local.get $l8
          local.get $l10
          f32.mul
          local.get $l20
          local.get $l14
          f32.mul
          f32.sub
          local.get $l5
          local.get $l16
          f32.mul
          f32.sub
          local.get $l9
          local.get $l7
          f32.mul
          f32.sub
          i32.reinterpret_f32
          i32.const -2147483648
          i32.xor
          f32.reinterpret_i32
          local.tee $l19
          local.get $l19
          f32.mul
          f32.add
          local.get $l15
          local.get $l15
          f32.mul
          local.get $l9
          local.get $l14
          f32.mul
          local.get $l5
          local.get $l10
          f32.mul
          f32.sub
          local.get $l20
          local.get $l7
          f32.mul
          f32.sub
          local.get $l8
          local.get $l16
          f32.mul
          f32.sub
          i32.reinterpret_f32
          i32.const -2147483648
          i32.xor
          f32.reinterpret_i32
          local.tee $l16
          local.get $l16
          f32.mul
          f32.add
          f32.add
          f32.sqrt
          f32.div
          local.tee $l5
          f32.mul
          f32.store offset=12
          local.get $l30
          local.get $l5
          local.get $l16
          f32.mul
          f32.store offset=8
          local.get $l30
          local.get $l5
          local.get $l19
          f32.mul
          f32.store offset=4
          local.get $l30
          local.get $l5
          local.get $l17
          f32.mul
          f32.store
        end
        local.get $l31
        i32.const -1
        i32.ne
        if $I55
          local.get $l36
          f32.load offset=32
          local.set $l5
          local.get $l29
          f32.load offset=32
          local.set $l16
          local.get $l36
          f32.load offset=28
          local.set $l7
          local.get $l29
          f32.load offset=28
          local.set $l8
          local.get $l28
          i32.load offset=20
          local.get $l28
          i32.const 20
          i32.add
          i32.add
          local.get $l31
          i32.const 12
          i32.mul
          i32.add
          local.tee $l30
          local.get $l30
          f32.load offset=8
          local.get $l29
          f32.load offset=36
          local.get $l36
          f32.load offset=36
          f32.sub
          local.get $l13
          f32.mul
          f32.add
          f32.store offset=8
          local.get $l30
          local.get $l30
          f32.load offset=4
          local.get $l16
          local.get $l5
          f32.sub
          local.get $l13
          f32.mul
          f32.add
          f32.store offset=4
          local.get $l30
          local.get $l30
          f32.load
          local.get $l8
          local.get $l7
          f32.sub
          local.get $l13
          f32.mul
          f32.add
          f32.store
        end
      end
      local.get $l29
      i32.const 256
      i32.add
      local.tee $l31
      i64.const 0
      i64.store align=4
      local.get $l31
      i64.const 0
      i64.store offset=40 align=4
      local.get $l31
      i64.const 0
      i64.store offset=80 align=4
      local.get $l31
      i64.const 0
      i64.store offset=120 align=4
      local.get $l31
      i64.const 0
      i64.store offset=16 align=4
      local.get $l31
      i64.const 0
      i64.store offset=8 align=4
      local.get $l31
      i64.const 4575657222473777152
      i64.store offset=32 align=4
      local.get $l31
      i64.const 4575657222473777152
      i64.store offset=24 align=4
      local.get $l31
      i64.const 0
      i64.store offset=48 align=4
      local.get $l31
      i64.const 0
      i64.store offset=56 align=4
      local.get $l31
      i64.const 4575657222473777152
      i64.store offset=72 align=4
      local.get $l31
      i32.const -64
      i32.sub
      i64.const 4575657222473777152
      i64.store align=4
      local.get $l31
      i64.const 0
      i64.store offset=88 align=4
      local.get $l31
      i64.const 0
      i64.store offset=96 align=4
      local.get $l31
      i64.const 4575657222473777152
      i64.store offset=112 align=4
      local.get $l31
      i64.const 4575657222473777152
      i64.store offset=104 align=4
      local.get $l31
      i64.const 0
      i64.store offset=136 align=4
      local.get $l31
      i64.const 0
      i64.store offset=128 align=4
      local.get $l31
      i32.const 0
      i32.store16 offset=160
      local.get $l31
      i64.const 4575657222473777152
      i64.store offset=152 align=4
      local.get $l31
      i64.const 4575657222473777152
      i64.store offset=144 align=4
      block $B56
        block $B57
          local.get $l38
          i32.load8_u offset=20
          if $I58
            local.get $l42
            i32.load offset=64
            local.get $l42
            i32.load offset=68
            local.get $l48
            local.get $l41
            local.get $l39
            local.get $l45
            local.get $l29
            i32.const 256
            i32.add
            call $f68370
            local.get $l29
            i32.const 1
            i32.store8 offset=444
            local.get $l48
            local.get $l29
            i32.const 424
            i32.add
            local.get $l41
            i32.load
            local.get $l39
            i32.load
            local.get $l29
            i32.const 256
            i32.add
            local.get $l43
            local.get $l40
            i32.load offset=196
            local.get $l61
            local.tee $l39
            i32.const 0
            i32.ne
            i32.const 0
            local.get $l40
            i32.load8_u offset=269
            call $f68347
            block $B59
              block $B60
                local.get $l38
                i32.load8_u
                i32.eqz
                br_if $B60
                local.get $l42
                i32.load offset=56
                local.tee $l41
                i32.const -1
                i32.eq
                br_if $B60
                local.get $l37
                i32.load offset=28
                local.get $l37
                i32.const 28
                i32.add
                i32.add
                local.get $l41
                i32.add
                i32.load8_u
                i32.eqz
                br_if $B60
                local.get $l43
                local.get $l50
                i32.load offset=28
                local.get $l50
                i32.const 28
                i32.add
                i32.add
                local.get $l41
                i32.const 2
                i32.shl
                i32.add
                f32.load
                f32.store offset=32
                br $B59
              end
              block $B61
                local.get $l39
                i32.eqz
                if $I62
                  local.get $l42
                  i32.load offset=16
                  local.tee $l39
                  i32.load offset=20
                  local.tee $l41
                  if $I63
                    local.get $l41
                    local.get $l39
                    i32.const 20
                    i32.add
                    i32.add
                    local.tee $l41
                    i32.load offset=40
                    local.get $l41
                    i32.const 40
                    i32.add
                    i32.add
                    i32.load
                    br_if $B61
                  end
                  local.get $l39
                  i32.load offset=40
                  i32.const -1
                  i32.eq
                  br_if $B61
                end
                local.get $l43
                local.get $l48
                i32.load8_u offset=2088
                f32.convert_i32_u
                f32.store offset=32
                br $B59
              end
              local.get $l43
              i32.const 1065353216
              i32.store offset=32
            end
            local.get $l64
            i32.eqz
            br_if $B57
            local.get $l43
            i64.const 0
            i64.store align=4
            local.get $l43
            i64.const 0
            i64.store offset=36 align=4
            local.get $l43
            i64.const 0
            i64.store offset=76 align=4
            local.get $l43
            i64.const 0
            i64.store offset=116 align=4
            local.get $l43
            i64.const 0
            i64.store offset=16 align=4
            local.get $l43
            i64.const 0
            i64.store offset=8 align=4
            local.get $l43
            i64.const 4575657221408423936
            i64.store offset=24 align=4
            local.get $l43
            i64.const 0
            i64.store offset=44 align=4
            local.get $l43
            i64.const 0
            i64.store offset=52 align=4
            local.get $l43
            i64.const 4575657222473777152
            i64.store offset=68 align=4
            local.get $l43
            i64.const 4575657222473777152
            i64.store offset=60 align=4
            local.get $l43
            i64.const 0
            i64.store offset=84 align=4
            local.get $l43
            i64.const 0
            i64.store offset=92 align=4
            local.get $l43
            i64.const 4575657222473777152
            i64.store offset=108 align=4
            local.get $l43
            i64.const 4575657222473777152
            i64.store offset=100 align=4
            local.get $l43
            i64.const 0
            i64.store offset=132 align=4
            local.get $l43
            i64.const 0
            i64.store offset=124 align=4
            local.get $l43
            i64.const 4575657222473777152
            i64.store offset=148 align=4
            local.get $l43
            i64.const 4575657222473777152
            i64.store offset=140 align=4
            local.get $l43
            i64.const 0
            i64.store offset=172 align=4
            local.get $l43
            i64.const 0
            i64.store offset=164 align=4
            local.get $l43
            i64.const 0
            i64.store offset=156 align=4
            local.get $l43
            i64.const 4575657222473777152
            i64.store offset=188 align=4
            local.get $l43
            i64.const 4575657222473777152
            i64.store offset=180 align=4
            local.get $l43
            i64.const 0
            i64.store offset=232 align=4
            local.get $l43
            i64.const 0
            i64.store offset=224 align=4
            local.get $l43
            i64.const 0
            i64.store offset=216 align=4
            local.get $l43
            i64.const 0
            i64.store offset=208 align=4
            local.get $l43
            i64.const 0
            i64.store offset=200 align=4
            local.get $l43
            i64.const 4575657222473777152
            i64.store offset=248 align=4
            local.get $l43
            i64.const 4575657222473777152
            i64.store offset=240 align=4
            br $B57
          end
          local.get $l61
          local.tee $l41
          local.get $l38
          i32.load8_u offset=21
          i32.or
          i32.eqz
          br_if $B56
          local.get $l42
          i32.load offset=64
          local.get $l42
          i32.load offset=68
          local.get $l48
          local.get $l39
          local.get $l39
          local.get $l45
          local.get $l29
          i32.const 256
          i32.add
          call $f68370
          local.get $l29
          i64.const 0
          i64.store offset=40
          local.get $l29
          i64.const 0
          i64.store offset=48
          local.get $l29
          i32.const 0
          i32.store offset=56
          local.get $l29
          i64.const 4575657222473777152
          i64.store offset=68 align=4
          local.get $l29
          i64.const 4575657222473777152
          i64.store offset=60 align=4
          local.get $l29
          i64.const 0
          i64.store offset=84 align=4
          local.get $l29
          i64.const 0
          i64.store offset=92 align=4
          local.get $l29
          i64.const 4575657222473777152
          i64.store offset=108 align=4
          local.get $l29
          i64.const 4575657222473777152
          i64.store offset=100 align=4
          local.get $l29
          i64.const 0
          i64.store offset=124 align=4
          local.get $l29
          i64.const 0
          i64.store offset=132 align=4
          local.get $l29
          i64.const 4575657222473777152
          i64.store offset=148 align=4
          local.get $l29
          i64.const 4575657222473777152
          i64.store offset=140 align=4
          local.get $l29
          i64.const 0
          i64.store offset=172 align=4
          local.get $l29
          i64.const 0
          i64.store offset=164 align=4
          local.get $l29
          i64.const 0
          i64.store offset=32
          local.get $l29
          i32.const 0
          i32.store
          local.get $l29
          i64.const 0
          i64.store offset=76 align=4
          local.get $l29
          i64.const 0
          i64.store offset=116 align=4
          local.get $l29
          i64.const 0
          i64.store offset=156 align=4
          local.get $l29
          i64.const 4575657222473777152
          i64.store offset=188 align=4
          local.get $l29
          i64.const 4575657222473777152
          i64.store offset=180 align=4
          local.get $l29
          i64.const 0
          i64.store offset=204 align=4
          local.get $l29
          i64.const 0
          i64.store offset=212 align=4
          local.get $l29
          i64.const 0
          i64.store offset=220 align=4
          local.get $l29
          i64.const 0
          i64.store offset=228 align=4
          local.get $l29
          i32.const 0
          i32.store offset=236
          local.get $l29
          i64.const 4575657222473777152
          i64.store offset=240
          local.get $l29
          i64.const 4575657222473777152
          i64.store offset=248
          local.get $l29
          i64.const 0
          i64.store offset=12 align=4
          local.get $l29
          i64.const 0
          i64.store offset=20 align=4
          local.get $l29
          i32.const 1065353216
          i32.store offset=28
          local.get $l29
          i64.const 0
          i64.store offset=196 align=4
          local.get $l29
          i64.const 0
          i64.store offset=4 align=4
          local.get $l48
          local.get $l29
          i32.const 424
          i32.add
          local.get $l39
          i32.load
          local.tee $l39
          local.get $l39
          local.get $l29
          i32.const 256
          i32.add
          local.get $l29
          local.get $l40
          i32.load offset=196
          local.get $l41
          i32.const 0
          i32.ne
          local.get $l41
          i32.eqz
          local.get $l40
          i32.load8_u offset=269
          call $f68347
        end
        local.get $l38
        i32.load8_u offset=21
        i32.eqz
        br_if $B56
        block $B64
          local.get $l40
          i32.load offset=196
          local.tee $l39
          i32.load8_u offset=200
          i32.eqz
          br_if $B64
          local.get $l42
          i32.load offset=64
          local.tee $l43
          i32.const -1
          i32.eq
          br_if $B64
          local.get $l38
          i64.load offset=36 align=4
          local.tee $l68
          i32.wrap_i64
          i32.load offset=24
          local.get $l68
          i64.const 32
          i64.shr_u
          i32.wrap_i64
          i32.const 40
          i32.mul
          i32.add
          local.tee $l41
          f32.load offset=28
          local.set $l9
          local.get $l41
          f32.load offset=36
          local.set $l15
          local.get $l41
          f32.load offset=32
          local.set $l17
          block $B65
            local.get $l42
            i32.load offset=72
            local.tee $l41
            i32.const -1
            i32.eq
            br_if $B65
            local.get $l37
            i32.load offset=4
            local.get $l37
            i32.const 4
            i32.add
            i32.add
            local.get $l41
            i32.add
            i32.load8_u
            i32.eqz
            br_if $B65
            local.get $l50
            i32.load offset=20
            local.get $l50
            i32.const 20
            i32.add
            i32.add
            local.get $l41
            i32.const 12
            i32.mul
            i32.add
            local.tee $l41
            f32.load offset=8
            local.set $l15
            local.get $l41
            f32.load offset=4
            local.set $l17
            local.get $l41
            f32.load
            local.set $l9
          end
          f32.const 0x1p+0 (;=1;)
          local.set $l13
          local.get $l61
          if $I66
            local.get $l42
            i32.load offset=16
            local.tee $l41
            i32.load offset=20
            local.get $l41
            i32.const 20
            i32.add
            i32.add
            f32.load offset=256
            local.set $l13
          end
          local.get $l39
          f32.load
          local.set $l19
          local.get $l39
          f32.load offset=4
          local.set $l22
          local.get $l50
          i32.load offset=4
          local.get $l50
          i32.const 4
          i32.add
          i32.add
          local.get $l43
          i32.const 12
          i32.mul
          i32.add
          local.tee $l41
          local.get $l15
          local.get $l13
          f32.mul
          f32.const 0x1p+0 (;=1;)
          local.get $l38
          i32.load8_u offset=20
          local.tee $l61
          select
          local.get $l39
          f32.load offset=8
          f32.mul
          f32.store offset=8
          local.get $l41
          local.get $l22
          local.get $l17
          local.get $l13
          f32.mul
          f32.const 0x1p+0 (;=1;)
          local.get $l61
          select
          f32.mul
          f32.store offset=4
          local.get $l41
          local.get $l19
          local.get $l9
          local.get $l13
          f32.mul
          f32.const 0x1p+0 (;=1;)
          local.get $l61
          select
          f32.mul
          f32.store
          local.get $l42
          i32.load offset=64
          local.get $l37
          i32.load offset=4
          local.tee $l39
          local.get $l37
          i32.const 4
          i32.add
          i32.add
          i32.const 0
          local.get $l39
          select
          i32.add
          i32.const 1
          i32.store8
          local.get $l40
          i32.load offset=196
          local.set $l39
        end
        local.get $l39
        i32.load8_u offset=201
        i32.eqz
        br_if $B56
        local.get $l42
        i32.load offset=68
        local.tee $l41
        i32.const -1
        i32.eq
        br_if $B56
        local.get $l39
        i64.load offset=12 align=4
        local.set $l68
        local.get $l50
        i32.load offset=12
        local.get $l50
        i32.const 12
        i32.add
        i32.add
        local.get $l41
        i32.const 4
        i32.shl
        i32.add
        local.tee $l50
        local.get $l39
        i64.load offset=20 align=4
        i64.store offset=8 align=4
        local.get $l50
        local.get $l68
        i64.store align=4
        local.get $l42
        i32.load offset=68
        local.get $l37
        i32.load offset=12
        local.tee $l39
        local.get $l37
        i32.const 12
        i32.add
        i32.add
        i32.const 0
        local.get $l39
        select
        i32.add
        i32.const 1
        i32.store8
      end
      local.get $l38
      i32.load8_u
      i32.eqz
      br_if $B1
      local.get $l48
      local.set $l38
      local.get $l42
      i32.load offset=4
      local.set $l33
      local.get $l40
      f32.load offset=224
      local.set $l26
      i32.const 0
      local.set $l37
      i32.const 0
      local.set $l42
      i32.const 0
      local.set $l40
      global.get $g0
      i32.const 16
      i32.sub
      local.tee $l35
      global.set $g0
      local.get $l35
      i32.const 1
      i32.store offset=12
      local.get $l35
      i32.const 3114520
      i32.store offset=8
      i32.const 1
      local.get $l64
      i32.const 0
      i32.ne
      local.tee $l41
      local.get $l60
      select
      if $I67
        local.get $l33
        local.get $l35
        i32.const 8
        i32.add
        call $f68328
        local.set $l37
        local.get $l33
        local.get $l35
        i32.const 8
        i32.add
        call $f68328
        local.set $l42
        local.get $l33
        local.get $l35
        i32.const 8
        i32.add
        call $f68328
        local.set $l40
        local.get $l45
        local.set $l30
        local.get $l54
        i32.load offset=4
        local.set $l44
        local.get $l42
        local.set $l33
        local.get $l40
        local.set $l45
        local.get $l37
        local.tee $l28
        i32.load offset=24
        local.tee $l61
        if $I68
          local.get $l38
          i32.const 2080
          i32.add
          local.set $l32
          local.get $l38
          i32.load offset=2080
          local.set $l31
          local.get $l45
          i32.const 28
          i32.add
          local.set $l36
          local.get $l33
          i32.const 28
          i32.add
          local.set $l39
          local.get $l28
          i32.const 28
          i32.add
          local.set $l48
          local.get $l38
          i32.const 2072
          i32.add
          local.set $l33
          local.get $l44
          i32.const 28
          i32.add
          local.set $l28
          i32.const 0
          local.set $l38
          loop $L69
            block $B70
              local.get $l28
              i32.load
              local.get $l28
              i32.add
              local.get $l38
              i32.add
              i32.load8_u
              i32.eqz
              br_if $B70
              local.get $l30
              i32.load offset=24
              local.get $l38
              i32.const 1
              i32.shl
              i32.add
              i32.load16_s
              local.tee $l44
              i32.const -1
              i32.eq
              br_if $B70
              local.get $l38
              i32.const 2
              i32.shl
              local.tee $l45
              local.get $l48
              i32.load
              local.get $l48
              i32.add
              i32.add
              local.get $l44
              i32.const 3
              i32.shl
              local.tee $l50
              local.get $l33
              i32.load
              local.get $l33
              i32.add
              i32.add
              f32.load
              f32.store
              local.get $l39
              i32.load
              local.get $l39
              i32.add
              local.get $l45
              i32.add
              local.get $l33
              i32.load
              local.get $l33
              i32.add
              local.get $l50
              i32.add
              f32.load offset=4
              f32.store
              local.get $l36
              i32.load
              local.get $l36
              i32.add
              local.get $l45
              i32.add
              block $B71 (result i32)
                local.get $l31
                if $I72
                  local.get $l32
                  i32.load
                  local.get $l32
                  i32.add
                  local.get $l44
                  i32.const 2
                  i32.shl
                  i32.add
                  br $B71
                end
                local.get $l33
                i32.load
                local.get $l33
                i32.add
                local.get $l50
                i32.add
              end
              f32.load
              f32.store
            end
            local.get $l38
            i32.const 1
            i32.add
            local.tee $l38
            local.get $l61
            i32.ne
            br_if $L69
          end
        end
      end
      local.get $l41
      if $I73
        local.get $l40
        local.set $l38
        local.get $l54
        i32.load offset=4
        local.set $l45
        local.get $l54
        i32.load
        local.tee $l33
        i32.load offset=24
        local.tee $l44
        if $I74
          local.get $l38
          i32.const 28
          i32.add
          local.set $l41
          local.get $l33
          i32.const 28
          i32.add
          local.set $l28
          local.get $l45
          i32.const 28
          i32.add
          local.set $l38
          i32.const 0
          local.set $l33
          loop $L75
            local.get $l38
            i32.load
            local.get $l38
            i32.add
            local.get $l33
            i32.add
            i32.load8_u
            if $I76
              local.get $l33
              i32.const 2
              i32.shl
              local.tee $l45
              local.get $l28
              i32.load
              local.get $l28
              i32.add
              i32.add
              local.tee $l30
              local.get $l30
              f32.load
              local.get $l41
              i32.load
              local.get $l41
              i32.add
              local.get $l45
              i32.add
              f32.load
              f32.sub
              f32.store
            end
            local.get $l33
            i32.const 1
            i32.add
            local.tee $l33
            local.get $l44
            i32.ne
            br_if $L75
          end
        end
      end
      local.get $l60
      if $I77
        local.get $l37
        local.set $l38
        local.get $l42
        local.set $l33
        local.get $l54
        i32.load offset=4
        local.set $l41
        local.get $l54
        i32.load
        local.tee $l45
        i32.load offset=24
        local.tee $l30
        if $I78
          local.get $l33
          i32.const 28
          i32.add
          local.set $l54
          local.get $l38
          i32.const 28
          i32.add
          local.set $l60
          local.get $l45
          i32.const 28
          i32.add
          local.set $l28
          local.get $l41
          i32.const 28
          i32.add
          local.set $l38
          i32.const 0
          local.set $l45
          loop $L79
            local.get $l38
            i32.load
            local.get $l38
            i32.add
            local.get $l45
            i32.add
            i32.load8_u
            if $I80
              local.get $l45
              i32.const 2
              i32.shl
              local.tee $l33
              local.get $l28
              i32.load
              local.get $l28
              i32.add
              i32.add
              local.tee $l41
              local.get $l60
              i32.load
              local.get $l60
              i32.add
              local.get $l33
              i32.add
              f32.load
              local.get $l54
              i32.load
              local.get $l54
              i32.add
              local.get $l33
              i32.add
              f32.load
              f32.sub
              local.get $l26
              f32.mul
              local.get $l41
              f32.load
              f32.add
              f32.store
            end
            local.get $l45
            i32.const 1
            i32.add
            local.tee $l45
            local.get $l30
            i32.ne
            br_if $L79
          end
        end
      end
      local.get $l37
      local.get $l35
      i32.const 8
      i32.add
      call $f68324
      local.get $l42
      local.get $l35
      i32.const 8
      i32.add
      call $f68324
      local.get $l40
      local.get $l35
      i32.const 8
      i32.add
      call $f68324
      local.get $l35
      i32.const 16
      i32.add
      global.set $g0
    end
    local.get $l29
    i32.const 496
    i32.add
    global.set $g0
    local.get $p1
    local.set $l33
    global.get $g0
    i32.const 1744
    i32.sub
    local.tee $l28
    global.set $g0
    block $B81
      local.get $p0
      local.tee $p1
      i32.load offset=180
      local.tee $l30
      i32.eqz
      br_if $B81
      local.get $p2
      i32.load offset=8
      i32.load offset=4
      i32.const -1
      i32.eq
      br_if $B81
      local.get $p2
      i32.load8_u offset=20
      i32.eqz
      br_if $B81
      local.get $p1
      i32.load offset=184
      local.set $l45
      local.get $l33
      i32.load8_u offset=78
      local.set $l38
      local.get $l30
      i32.load offset=1240
      local.set $l37
      local.get $p1
      i32.load offset=312
      local.tee $l31
      local.get $l31
      i32.load
      i32.load offset=84
      call_indirect $__indirect_function_table (type $t23)
      drop
      local.get $l28
      local.get $p1
      f32.load offset=252
      local.tee $l4
      f32.store offset=1728
      local.get $l28
      local.get $p1
      f32.load offset=244
      local.tee $l5
      f32.store offset=1720
      local.get $l28
      local.get $p1
      i32.load8_u offset=248
      i32.store8 offset=1724
      local.get $l28
      local.get $p1
      i32.load8_u offset=329
      i32.store8 offset=1733
      local.get $l28
      local.get $p1
      f32.load offset=340
      local.tee $l6
      f32.store offset=1736
      local.get $p1
      i32.load offset=208
      local.set $l40
      local.get $p3
      i32.load
      i32.load offset=8
      local.set $p3
      local.get $p1
      i32.load offset=212
      local.tee $l31
      local.get $l37
      local.get $l30
      i32.const 1240
      i32.add
      local.tee $l42
      i32.add
      i32.const 0
      local.get $l37
      select
      local.tee $l37
      i32.load16_u offset=10
      local.get $l37
      i32.load16_u offset=8
      i32.add
      local.get $l37
      i32.load offset=16
      i32.add
      local.get $l37
      i32.load offset=36
      i32.add
      call $f68383
      local.get $p1
      i32.const 269
      i32.add
      local.tee $l32
      i32.load8_u
      local.set $l37
      local.get $p2
      i32.load offset=8
      f32.load offset=8
      local.set $l7
      local.get $l28
      i32.const 0
      i32.store offset=1456
      local.get $l28
      local.get $l7
      local.get $l30
      f32.load offset=1244
      local.get $l30
      f32.load offset=1248
      local.get $l4
      local.get $l30
      f32.load offset=1260
      f32.add
      local.get $l37
      local.get $l5
      local.get $l28
      i32.const 1456
      i32.add
      local.get $l28
      i32.const 384
      i32.add
      local.get $l6
      call $f68341
      f32.store offset=176
      local.get $l30
      i32.load offset=1240
      local.tee $l37
      local.get $l42
      i32.add
      i32.const 0
      local.get $l37
      select
      local.get $l28
      i32.const 176
      i32.add
      local.get $l40
      local.get $l31
      call $f68384
      local.get $l28
      i32.const 1
      i32.store8 offset=1732
      local.get $l28
      local.get $p2
      i32.load offset=8
      f32.load offset=8
      local.tee $l4
      f32.store offset=1712
      local.get $l28
      local.get $l4
      f32.store offset=1716
      local.get $l28
      i32.const 1496
      i32.add
      i64.const 0
      i64.store
      local.get $l28
      i32.const 1504
      i32.add
      i64.const 0
      i64.store
      local.get $l28
      i32.const 1512
      i32.add
      i32.const 0
      i32.store
      local.get $l28
      i32.const 1524
      i32.add
      i64.const 4575657222473777152
      i64.store align=4
      local.get $l28
      i32.const 1516
      i32.add
      i64.const 4575657222473777152
      i64.store align=4
      local.get $l28
      i32.const 1540
      i32.add
      i64.const 0
      i64.store align=4
      local.get $l28
      i32.const 1548
      i32.add
      i64.const 0
      i64.store align=4
      local.get $l28
      i32.const 1564
      i32.add
      i64.const 4575657222473777152
      i64.store align=4
      local.get $l28
      i32.const 1556
      i32.add
      i64.const 4575657222473777152
      i64.store align=4
      local.get $l28
      i32.const 1580
      i32.add
      i64.const 0
      i64.store align=4
      local.get $l28
      i32.const 1588
      i32.add
      i64.const 0
      i64.store align=4
      local.get $l28
      i32.const 1604
      i32.add
      i64.const 4575657222473777152
      i64.store align=4
      local.get $l28
      i32.const 1596
      i32.add
      i64.const 4575657222473777152
      i64.store align=4
      local.get $l28
      i32.const 1628
      i32.add
      i64.const 0
      i64.store align=4
      local.get $l28
      i32.const 1620
      i32.add
      i64.const 0
      i64.store align=4
      local.get $l28
      i64.const 0
      i64.store offset=1488
      local.get $l28
      i32.const 0
      i32.store offset=1456
      local.get $l28
      i64.const 0
      i64.store offset=1532 align=4
      local.get $l28
      i64.const 0
      i64.store offset=1572 align=4
      local.get $l28
      i64.const 0
      i64.store offset=1612 align=4
      local.get $l28
      i32.const 1644
      i32.add
      i64.const 4575657222473777152
      i64.store align=4
      local.get $l28
      i32.const 1636
      i32.add
      i64.const 4575657222473777152
      i64.store align=4
      local.get $l28
      i32.const 1660
      i32.add
      i64.const 0
      i64.store align=4
      local.get $l28
      i32.const 1668
      i32.add
      i64.const 0
      i64.store align=4
      local.get $l28
      i32.const 1676
      i32.add
      i64.const 0
      i64.store align=4
      local.get $l28
      i32.const 1684
      i32.add
      i64.const 0
      i64.store align=4
      local.get $l28
      i32.const 1692
      i32.add
      i32.const 0
      i32.store
      local.get $l28
      i32.const 1696
      i32.add
      i64.const 4575657222473777152
      i64.store
      local.get $l28
      i32.const 1704
      i32.add
      i64.const 4575657222473777152
      i64.store
      local.get $l28
      i32.const 1468
      i32.add
      i64.const 0
      i64.store align=4
      local.get $l28
      i32.const 1476
      i32.add
      i64.const 0
      i64.store align=4
      local.get $l28
      i32.const 1484
      i32.add
      i32.const 1065353216
      i32.store
      local.get $l28
      i64.const 0
      i64.store offset=1652 align=4
      local.get $l28
      i64.const 0
      i64.store offset=1460 align=4
      local.get $l28
      i32.const 384
      i32.add
      call $f68289
      local.set $l37
      local.get $l33
      i32.load offset=64
      local.get $l33
      i32.load offset=68
      local.get $l30
      local.get $l31
      local.get $l31
      local.get $l45
      local.get $l28
      i32.const 8
      i32.add
      call $f68370
      local.get $l30
      local.get $l28
      i32.const 1712
      i32.add
      local.get $l31
      i32.load
      local.tee $l33
      local.get $l33
      local.get $l28
      i32.const 8
      i32.add
      local.get $l28
      i32.const 1456
      i32.add
      local.get $l28
      i32.const 176
      i32.add
      local.get $l38
      i32.const 0
      local.get $l32
      i32.load8_u
      call $f68347
      local.get $l28
      f32.load offset=176
      local.set $l12
      local.get $l28
      f32.load offset=180
      local.set $l14
      local.get $p3
      local.get $l28
      f32.load offset=184
      local.tee $l20
      f32.store offset=224
      local.get $p3
      local.get $l14
      f32.store offset=220
      local.get $p3
      local.get $l12
      f32.store offset=216
      local.get $l28
      i64.load offset=188 align=4
      local.set $l68
      local.get $p3
      local.get $l28
      i64.load offset=196 align=4
      i64.store offset=236 align=4
      local.get $p3
      local.get $l68
      i64.store offset=228 align=4
      local.get $l28
      f32.load offset=212
      local.set $l4
      local.get $p3
      local.get $l28
      i64.load offset=204 align=4
      i64.store offset=244 align=4
      local.get $p3
      local.get $l4
      f32.store offset=252
      block $B82
        local.get $l38
        i32.eqz
        br_if $B82
        local.get $p2
        i32.load offset=8
        i32.load offset=4
        i32.const 1
        i32.sub
        i32.const 4
        i32.gt_u
        br_if $B82
        local.get $l30
        local.get $l28
        i32.const 1712
        i32.add
        local.get $l31
        i32.load
        local.get $l28
        i32.const 1456
        i32.add
        local.get $l28
        i32.const 176
        i32.add
        local.get $l37
        local.get $p1
        i32.load8_u offset=269
        call $f68350
        block $B83 (result i32)
          local.get $p2
          i32.load offset=8
          i32.load offset=4
          local.tee $l30
          i32.const 2
          i32.ge_s
          if $I84
            local.get $p3
            f32.load offset=224
            local.get $l30
            i32.const 6
            i32.shl
            local.get $l37
            i32.add
            local.tee $l30
            i32.const 52
            i32.sub
            f32.load
            local.get $p3
            f32.load offset=252
            local.tee $l15
            f32.mul
            local.tee $l8
            local.get $l30
            i32.const 60
            i32.sub
            f32.load
            local.get $p3
            f32.load offset=244
            local.tee $l19
            f32.mul
            local.tee $l9
            local.get $p3
            f32.load offset=232
            local.tee $l4
            f32.const -0x1p+1 (;=-2;)
            f32.mul
            local.tee $l12
            local.get $p3
            f32.load offset=240
            local.tee $l7
            f32.mul
            local.tee $l18
            local.get $p3
            f32.load offset=228
            local.tee $l5
            local.get $p3
            f32.load offset=236
            local.tee $l6
            f32.const -0x1p+1 (;=-2;)
            f32.mul
            local.tee $l14
            f32.mul
            f32.sub
            f32.mul
            f32.add
            local.get $l8
            local.get $l5
            local.get $l5
            f32.const -0x1p+1 (;=-2;)
            f32.mul
            local.tee $l11
            f32.mul
            local.get $l4
            local.get $l4
            local.get $l4
            f32.add
            local.tee $l13
            f32.mul
            f32.sub
            f32.mul
            local.get $l30
            i32.const 56
            i32.sub
            f32.load
            local.get $p3
            f32.load offset=248
            local.tee $l21
            f32.mul
            local.tee $l10
            local.get $l4
            local.get $l6
            local.get $l6
            f32.add
            local.tee $l16
            f32.mul
            local.get $l7
            local.get $l11
            f32.mul
            local.tee $l17
            f32.sub
            f32.mul
            f32.add
            f32.add
            f32.add
            local.set $l20
            local.get $p3
            f32.load offset=220
            local.get $l10
            local.get $l9
            local.get $l5
            local.get $l13
            f32.mul
            local.get $l7
            local.get $l14
            f32.mul
            local.tee $l13
            f32.sub
            f32.mul
            f32.add
            local.get $l8
            local.get $l17
            local.get $l12
            local.get $l6
            f32.mul
            f32.sub
            f32.mul
            local.get $l10
            local.get $l6
            local.get $l14
            f32.mul
            local.get $l5
            local.get $l5
            local.get $l5
            f32.add
            local.tee $l17
            f32.mul
            f32.sub
            f32.mul
            f32.add
            f32.add
            f32.add
            local.set $l14
            local.get $p3
            f32.load offset=216
            local.get $l9
            local.get $l9
            local.get $l4
            local.get $l12
            f32.mul
            local.get $l6
            local.get $l16
            f32.mul
            f32.sub
            f32.mul
            f32.add
            local.get $l8
            local.get $l17
            local.get $l6
            f32.mul
            local.get $l18
            f32.sub
            f32.mul
            local.get $l10
            local.get $l13
            local.get $l4
            local.get $l11
            f32.mul
            f32.sub
            f32.mul
            f32.add
            f32.add
            f32.add
            local.set $l12
            local.get $l5
            local.get $l30
            i32.const 40
            i32.sub
            f32.load
            local.tee $l8
            f32.mul
            local.get $l6
            local.get $l30
            i32.const 48
            i32.sub
            f32.load
            local.tee $l9
            f32.mul
            f32.sub
            local.get $l7
            local.get $l30
            i32.const 44
            i32.sub
            f32.load
            local.tee $l10
            f32.mul
            f32.sub
            local.get $l4
            local.get $l30
            i32.const 36
            i32.sub
            f32.load
            local.tee $l11
            f32.mul
            f32.sub
            local.set $l18
            local.get $l6
            local.get $l10
            f32.mul
            local.get $l4
            local.get $l8
            f32.mul
            f32.sub
            local.get $l7
            local.get $l9
            f32.mul
            f32.sub
            local.get $l5
            local.get $l11
            f32.mul
            f32.sub
            local.set $l13
            local.get $l7
            local.get $l11
            f32.mul
            local.get $l5
            local.get $l9
            f32.mul
            f32.sub
            local.get $l6
            local.get $l8
            f32.mul
            f32.sub
            local.get $l4
            local.get $l10
            f32.mul
            f32.sub
            local.set $l16
            local.get $l4
            local.get $l9
            f32.mul
            local.get $l7
            local.get $l8
            f32.mul
            f32.sub
            local.get $l6
            local.get $l11
            f32.mul
            f32.sub
            local.get $l5
            local.get $l10
            f32.mul
            f32.sub
            local.set $l4
            local.get $l21
            local.get $l30
            i32.const 28
            i32.sub
            f32.load
            f32.mul
            local.set $l5
            local.get $l19
            local.get $l30
            i32.const 32
            i32.sub
            f32.load
            f32.mul
            local.set $l6
            local.get $l30
            i32.const 24
            i32.sub
            br $B83
          end
          local.get $p3
          f32.load offset=224
          local.get $l37
          f32.load offset=8
          local.get $p3
          f32.load offset=252
          local.tee $l15
          f32.mul
          local.tee $l8
          local.get $l37
          f32.load
          local.get $p3
          f32.load offset=244
          local.tee $l19
          f32.mul
          local.tee $l9
          local.get $p3
          f32.load offset=232
          local.tee $l4
          f32.const -0x1p+1 (;=-2;)
          f32.mul
          local.tee $l12
          local.get $p3
          f32.load offset=240
          local.tee $l7
          f32.mul
          local.tee $l18
          local.get $p3
          f32.load offset=228
          local.tee $l5
          local.get $p3
          f32.load offset=236
          local.tee $l6
          f32.const -0x1p+1 (;=-2;)
          f32.mul
          local.tee $l14
          f32.mul
          f32.sub
          f32.mul
          f32.add
          local.get $l8
          local.get $l5
          local.get $l5
          f32.const -0x1p+1 (;=-2;)
          f32.mul
          local.tee $l11
          f32.mul
          local.get $l4
          local.get $l4
          local.get $l4
          f32.add
          local.tee $l13
          f32.mul
          f32.sub
          f32.mul
          local.get $l37
          f32.load offset=4
          local.get $p3
          f32.load offset=248
          local.tee $l21
          f32.mul
          local.tee $l10
          local.get $l4
          local.get $l6
          local.get $l6
          f32.add
          local.tee $l16
          f32.mul
          local.get $l7
          local.get $l11
          f32.mul
          local.tee $l17
          f32.sub
          f32.mul
          f32.add
          f32.add
          f32.add
          local.set $l20
          local.get $p3
          f32.load offset=220
          local.get $l10
          local.get $l9
          local.get $l5
          local.get $l13
          f32.mul
          local.get $l7
          local.get $l14
          f32.mul
          local.tee $l13
          f32.sub
          f32.mul
          f32.add
          local.get $l8
          local.get $l17
          local.get $l12
          local.get $l6
          f32.mul
          f32.sub
          f32.mul
          local.get $l10
          local.get $l6
          local.get $l14
          f32.mul
          local.get $l5
          local.get $l5
          local.get $l5
          f32.add
          local.tee $l17
          f32.mul
          f32.sub
          f32.mul
          f32.add
          f32.add
          f32.add
          local.set $l14
          local.get $p3
          f32.load offset=216
          local.get $l9
          local.get $l9
          local.get $l4
          local.get $l12
          f32.mul
          local.get $l6
          local.get $l16
          f32.mul
          f32.sub
          f32.mul
          f32.add
          local.get $l8
          local.get $l17
          local.get $l6
          f32.mul
          local.get $l18
          f32.sub
          f32.mul
          local.get $l10
          local.get $l13
          local.get $l4
          local.get $l11
          f32.mul
          f32.sub
          f32.mul
          f32.add
          f32.add
          f32.add
          local.set $l12
          local.get $l5
          local.get $l37
          f32.load offset=20
          local.tee $l8
          f32.mul
          local.get $l6
          local.get $l37
          f32.load offset=12
          local.tee $l9
          f32.mul
          f32.sub
          local.get $l7
          local.get $l37
          f32.load offset=16
          local.tee $l10
          f32.mul
          f32.sub
          local.get $l4
          local.get $l37
          f32.load offset=24
          local.tee $l11
          f32.mul
          f32.sub
          local.set $l18
          local.get $l6
          local.get $l10
          f32.mul
          local.get $l4
          local.get $l8
          f32.mul
          f32.sub
          local.get $l7
          local.get $l9
          f32.mul
          f32.sub
          local.get $l5
          local.get $l11
          f32.mul
          f32.sub
          local.set $l13
          local.get $l7
          local.get $l11
          f32.mul
          local.get $l5
          local.get $l9
          f32.mul
          f32.sub
          local.get $l6
          local.get $l8
          f32.mul
          f32.sub
          local.get $l4
          local.get $l10
          f32.mul
          f32.sub
          local.set $l16
          local.get $l4
          local.get $l9
          f32.mul
          local.get $l7
          local.get $l8
          f32.mul
          f32.sub
          local.get $l6
          local.get $l11
          f32.mul
          f32.sub
          local.get $l5
          local.get $l10
          f32.mul
          f32.sub
          local.set $l4
          local.get $l19
          local.get $l37
          f32.load offset=28
          f32.mul
          local.set $l6
          local.get $l21
          local.get $l37
          f32.load offset=32
          f32.mul
          local.set $l5
          local.get $l37
          i32.const 36
          i32.add
        end
        f32.load
        local.set $l7
        local.get $p3
        local.get $l5
        f32.store offset=248
        local.get $p3
        local.get $l6
        f32.store offset=244
        local.get $p3
        local.get $l16
        f32.store offset=240
        local.get $p3
        local.get $l20
        f32.store offset=224
        local.get $p3
        local.get $l14
        f32.store offset=220
        local.get $p3
        local.get $l12
        f32.store offset=216
        local.get $p3
        local.get $l15
        local.get $l7
        f32.mul
        f32.store offset=252
        local.get $p3
        local.get $l4
        i32.reinterpret_f32
        i32.const -2147483648
        i32.xor
        i32.store offset=236
        local.get $p3
        local.get $l18
        i32.reinterpret_f32
        i32.const -2147483648
        i32.xor
        i32.store offset=232
        local.get $p3
        local.get $l13
        i32.reinterpret_f32
        i32.const -2147483648
        i32.xor
        i32.store offset=228
      end
      local.get $p1
      i32.load offset=196
      local.tee $p1
      f32.load
      local.set $l11
      local.get $p1
      f32.load offset=4
      local.set $l18
      local.get $p1
      f32.load offset=8
      local.set $l13
      local.get $p1
      i32.load offset=16
      local.set $l30
      local.get $p1
      i32.load offset=20
      local.set $p2
      local.get $p1
      i32.load offset=12
      local.set $l33
      local.get $p1
      f32.load offset=24
      local.set $l7
      local.get $p1
      f32.load offset=32
      local.set $l4
      local.get $p1
      f32.load offset=36
      local.set $l5
      local.get $p3
      f32.load offset=232
      local.set $l15
      local.get $p3
      f32.load offset=236
      local.set $l8
      local.get $p3
      f32.load offset=228
      local.set $l9
      local.get $p3
      f32.load offset=240
      local.set $l10
      local.get $p3
      f32.load offset=248
      local.set $l6
      local.get $p3
      f32.load offset=252
      local.set $l16
      local.get $p3
      f32.const 0x0p+0 (;=0;)
      f32.const 0x1p+0 (;=1;)
      local.get $p1
      f32.load offset=28
      local.tee $l19
      f32.div
      local.get $l19
      f32.abs
      f32.const 0x1.12e0bep-30 (;=1e-09;)
      f32.lt
      select
      local.tee $l19
      local.get $p3
      f32.load offset=244
      f32.mul
      f32.store offset=244
      local.get $p3
      local.get $l16
      f32.const 0x0p+0 (;=0;)
      f32.const 0x1p+0 (;=1;)
      local.get $l5
      f32.div
      local.get $l5
      f32.abs
      f32.const 0x1.12e0bep-30 (;=1e-09;)
      f32.lt
      select
      local.tee $l21
      f32.mul
      f32.store offset=252
      local.get $p3
      local.get $l6
      f32.const 0x0p+0 (;=0;)
      f32.const 0x1p+0 (;=1;)
      local.get $l4
      f32.div
      local.get $l4
      f32.abs
      f32.const 0x1.12e0bep-30 (;=1e-09;)
      f32.lt
      select
      local.tee $l16
      f32.mul
      f32.store offset=248
      local.get $p3
      local.get $l7
      local.get $l10
      f32.mul
      local.get $l9
      local.get $l33
      i32.const -2147483648
      i32.xor
      f32.reinterpret_i32
      local.tee $l4
      f32.mul
      f32.sub
      local.get $l8
      local.get $p2
      i32.const -2147483648
      i32.xor
      f32.reinterpret_i32
      local.tee $l5
      f32.mul
      f32.sub
      local.get $l15
      local.get $l30
      i32.const -2147483648
      i32.xor
      f32.reinterpret_i32
      local.tee $l6
      f32.mul
      f32.sub
      f32.store offset=240
      local.get $p3
      local.get $l9
      local.get $l6
      f32.mul
      local.get $l7
      local.get $l8
      f32.mul
      f32.sub
      local.get $l10
      local.get $l5
      f32.mul
      f32.sub
      local.get $l15
      local.get $l4
      f32.mul
      f32.sub
      i32.reinterpret_f32
      i32.const -2147483648
      i32.xor
      i32.store offset=236
      local.get $p3
      local.get $l8
      local.get $l4
      f32.mul
      local.get $l9
      local.get $l5
      f32.mul
      f32.sub
      local.get $l7
      local.get $l15
      f32.mul
      f32.sub
      local.get $l10
      local.get $l6
      f32.mul
      f32.sub
      i32.reinterpret_f32
      i32.const -2147483648
      i32.xor
      i32.store offset=232
      local.get $p3
      local.get $l15
      local.get $l5
      f32.mul
      local.get $l8
      local.get $l6
      f32.mul
      f32.sub
      local.get $l7
      local.get $l9
      f32.mul
      f32.sub
      local.get $l10
      local.get $l4
      f32.mul
      f32.sub
      i32.reinterpret_f32
      i32.const -2147483648
      i32.xor
      i32.store offset=228
      local.get $p3
      local.get $l12
      local.get $l11
      f32.sub
      local.tee $l15
      local.get $l7
      local.get $l6
      f32.const -0x1p+1 (;=-2;)
      f32.mul
      local.tee $l10
      f32.mul
      local.tee $l11
      local.get $l5
      f32.const -0x1p+1 (;=-2;)
      f32.mul
      local.tee $l12
      local.get $l4
      f32.mul
      f32.sub
      f32.mul
      local.get $l20
      local.get $l13
      f32.sub
      local.tee $l8
      f32.add
      local.get $l5
      local.get $l5
      f32.add
      local.tee $l13
      local.get $l6
      f32.mul
      local.get $l7
      local.get $l4
      f32.const -0x1p+1 (;=-2;)
      f32.mul
      local.tee $l20
      f32.mul
      local.tee $l17
      f32.sub
      local.get $l14
      local.get $l18
      f32.sub
      local.tee $l9
      f32.mul
      local.get $l20
      local.get $l4
      f32.mul
      local.get $l6
      local.get $l6
      f32.add
      local.tee $l14
      local.get $l6
      f32.mul
      f32.sub
      local.get $l8
      f32.mul
      f32.add
      f32.add
      local.get $l21
      f32.mul
      f32.store offset=224
      local.get $p3
      local.get $l9
      local.get $l15
      local.get $l14
      local.get $l4
      f32.mul
      local.get $l7
      local.get $l12
      f32.mul
      local.tee $l7
      f32.sub
      f32.mul
      f32.add
      local.get $l12
      local.get $l5
      f32.mul
      local.get $l4
      local.get $l4
      f32.add
      local.tee $l12
      local.get $l4
      f32.mul
      f32.sub
      local.get $l9
      f32.mul
      local.get $l17
      local.get $l10
      local.get $l5
      f32.mul
      f32.sub
      local.get $l8
      f32.mul
      f32.add
      f32.add
      local.get $l16
      f32.mul
      f32.store offset=220
      local.get $p3
      local.get $l15
      local.get $l15
      local.get $l10
      local.get $l6
      f32.mul
      local.get $l13
      local.get $l5
      f32.mul
      f32.sub
      f32.mul
      f32.add
      local.get $l7
      local.get $l20
      local.get $l6
      f32.mul
      f32.sub
      local.get $l9
      f32.mul
      local.get $l12
      local.get $l5
      f32.mul
      local.get $l11
      f32.sub
      local.get $l8
      f32.mul
      f32.add
      f32.add
      local.get $l19
      f32.mul
      f32.store offset=216
    end
    local.get $l28
    i32.const 1744
    i32.add
    global.set $g0
    local.get $p0
    i32.const 1
    i32.store8 offset=228)
