  (func $f70061 (type $t29) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 i32) (param $p7 i32) (param $p8 i32) (param $p9 i32)
    (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32) (local $l33 i32) (local $l34 i32) (local $l35 i32) (local $l36 i32) (local $l37 i32) (local $l38 i32) (local $l39 i32) (local $l40 i32) (local $l41 i32) (local $l42 i32) (local $l43 i32) (local $l44 i32) (local $l45 i32) (local $l46 i32) (local $l47 i32) (local $l48 i64)
    global.get $g0
    i32.const 96
    i32.sub
    local.tee $p9
    global.set $g0
    local.get $p6
    i32.load
    local.set $l39
    local.get $p9
    local.tee $l33
    i32.const 48
    i32.add
    local.get $p8
    call $f69972
    local.get $p3
    i32.load16_u offset=16
    local.set $l36
    local.get $p2
    i32.load offset=32
    local.set $l37
    local.get $p9
    local.get $p3
    i32.load8_u offset=18
    local.tee $l34
    i32.const 4
    i32.shl
    i32.const 16
    i32.add
    local.tee $l40
    i32.sub
    local.tee $l38
    local.tee $p9
    global.set $g0
    local.get $p9
    local.get $l40
    i32.sub
    local.tee $l41
    local.tee $p9
    global.set $g0
    local.get $p9
    local.get $l34
    i32.const 15
    i32.add
    i32.const 496
    i32.and
    i32.sub
    local.tee $l40
    global.set $g0
    local.get $l33
    local.get $p0
    i64.load offset=56
    i64.store offset=8
    local.get $l33
    local.get $p0
    i64.load offset=48
    i64.store
    local.get $l33
    i32.const 24
    i32.add
    local.tee $p9
    local.get $p0
    i64.load offset=72
    i64.store
    local.get $l33
    local.get $p0
    i32.const -64
    i32.sub
    i64.load
    i64.store offset=16
    local.get $l33
    i32.const 40
    i32.add
    local.tee $l35
    local.get $p0
    i64.load offset=88
    i64.store
    local.get $l33
    local.get $p0
    i64.load offset=80
    i64.store offset=32
    local.get $p4
    local.get $l36
    local.get $l37
    i32.add
    local.tee $l46
    local.get $l34
    local.get $p2
    i32.load offset=28
    local.get $l38
    local.get $p4
    i32.load
    i32.load offset=16
    call_indirect $__indirect_function_table (type $t6)
    local.get $l33
    i32.const 20
    i32.add
    local.tee $l34
    local.get $l33
    f32.load offset=16
    local.tee $l11
    local.get $l33
    f32.load offset=52
    local.tee $l16
    f32.mul
    local.get $l34
    f32.load
    local.tee $l10
    local.get $l33
    f32.load offset=68
    local.tee $l19
    f32.mul
    f32.add
    local.get $p9
    f32.load
    local.tee $l12
    local.get $l33
    f32.load offset=84
    local.tee $l18
    f32.mul
    f32.add
    local.tee $l13
    f32.store
    local.get $p9
    local.get $l11
    local.get $l33
    f32.load offset=56
    local.tee $l23
    f32.mul
    local.get $l10
    local.get $l33
    f32.load offset=72
    local.tee $l22
    f32.mul
    f32.add
    local.get $l12
    local.get $l33
    f32.load offset=88
    local.tee $l20
    f32.mul
    f32.add
    f32.store
    i32.const 0
    local.set $l36
    local.get $l33
    i32.const 0
    i32.store offset=12
    local.get $l33
    local.get $l23
    local.get $l33
    f32.load
    local.tee $l14
    f32.mul
    local.get $l22
    local.get $l33
    f32.load offset=4
    local.tee $l15
    f32.mul
    f32.add
    local.get $l20
    local.get $l33
    f32.load offset=8
    local.tee $l21
    f32.mul
    f32.add
    local.tee $l25
    f32.store offset=8
    local.get $l33
    local.get $l14
    local.get $l33
    f32.load offset=48
    local.tee $l17
    f32.mul
    local.get $l15
    local.get $l33
    f32.load offset=64
    local.tee $l24
    f32.mul
    f32.add
    local.get $l21
    local.get $l33
    f32.load offset=80
    local.tee $l26
    f32.mul
    f32.add
    local.tee $l27
    f32.store
    local.get $l33
    local.get $l14
    local.get $l16
    f32.mul
    local.get $l15
    local.get $l19
    f32.mul
    f32.add
    local.get $l21
    local.get $l18
    f32.mul
    f32.add
    local.tee $l15
    f32.store offset=4
    local.get $l33
    i32.const 0
    i32.store offset=28
    local.get $l33
    local.get $l11
    local.get $l17
    f32.mul
    local.get $l10
    local.get $l24
    f32.mul
    f32.add
    local.get $l12
    local.get $l26
    f32.mul
    f32.add
    local.tee $l14
    f32.store offset=16
    local.get $l35
    f32.load
    local.set $l11
    local.get $l33
    i32.const 36
    i32.add
    local.tee $p9
    f32.load
    local.set $l10
    local.get $l33
    f32.load offset=32
    local.set $l12
    local.get $l33
    i32.const 0
    i32.store offset=44
    local.get $l35
    local.get $l12
    local.get $l23
    f32.mul
    local.get $l10
    local.get $l22
    f32.mul
    f32.add
    local.get $l11
    local.get $l20
    f32.mul
    f32.add
    f32.store
    local.get $p9
    local.get $l12
    local.get $l16
    f32.mul
    local.get $l10
    local.get $l19
    f32.mul
    f32.add
    local.get $l11
    local.get $l18
    f32.mul
    f32.add
    local.tee $l18
    f32.store
    local.get $l33
    local.get $l12
    local.get $l17
    f32.mul
    local.get $l10
    local.get $l24
    f32.mul
    f32.add
    local.get $l11
    local.get $l26
    f32.mul
    f32.add
    local.tee $l11
    f32.store offset=32
    block $B0
      local.get $p3
      i32.load8_u offset=18
      i32.eqz
      br_if $B0
      f32.const -0x1.fffffep+127 (;=-3.40282e+38;)
      local.set $l16
      local.get $l15
      f32.const -0x1.fffffep+127 (;=-3.40282e+38;)
      f32.max
      local.tee $l10
      local.get $l13
      local.get $l10
      local.get $l13
      f32.gt
      select
      local.tee $l10
      local.get $l18
      local.get $l10
      local.get $l18
      f32.gt
      select
      f32.const 0x1p-23 (;=1.19209e-07;)
      f32.add
      local.set $l30
      f32.const 0x1.fffffep+127 (;=3.40282e+38;)
      local.set $l19
      local.get $l15
      f32.const 0x1.fffffep+127 (;=3.40282e+38;)
      f32.min
      local.tee $l10
      local.get $l13
      local.get $l10
      local.get $l13
      f32.lt
      select
      local.tee $l10
      local.get $l18
      local.get $l10
      local.get $l18
      f32.lt
      select
      f32.const -0x1p-23 (;=-1.19209e-07;)
      f32.add
      local.set $l31
      local.get $l27
      f32.const -0x1.fffffep+127 (;=-3.40282e+38;)
      f32.max
      local.tee $l10
      local.get $l14
      local.get $l10
      local.get $l14
      f32.gt
      select
      local.tee $l10
      local.get $l11
      local.get $l10
      local.get $l11
      f32.gt
      select
      f32.const 0x1p-23 (;=1.19209e-07;)
      f32.add
      local.set $l32
      local.get $l27
      f32.const 0x1.fffffep+127 (;=3.40282e+38;)
      f32.min
      local.tee $l10
      local.get $l14
      local.get $l10
      local.get $l14
      f32.lt
      select
      local.tee $l10
      local.get $l11
      local.get $l10
      local.get $l11
      f32.lt
      select
      f32.const -0x1p-23 (;=-1.19209e-07;)
      f32.add
      local.set $l27
      local.get $l25
      local.get $p7
      f32.load
      f32.add
      local.set $l26
      local.get $l39
      i32.const 5
      i32.add
      local.set $l42
      local.get $p5
      local.get $l39
      i32.const 6
      i32.shl
      i32.add
      local.set $l43
      i32.const 0
      local.set $l34
      f32.const 0x1.fffffep+127 (;=3.40282e+38;)
      local.set $l18
      f32.const -0x1.fffffep+127 (;=-3.40282e+38;)
      local.set $l23
      loop $L1
        local.get $l38
        local.get $l34
        i32.const 4
        i32.shl
        local.tee $l35
        i32.add
        local.tee $p9
        f32.load offset=12
        local.set $l24
        local.get $l33
        f32.load offset=80
        local.set $l10
        local.get $l33
        f32.load offset=48
        local.set $l22
        local.get $l33
        f32.load offset=64
        local.set $l20
        local.get $l33
        f32.load offset=84
        local.set $l11
        local.get $l33
        f32.load offset=52
        local.set $l15
        local.get $l33
        f32.load offset=68
        local.set $l21
        local.get $l35
        local.get $l41
        i32.add
        local.get $p9
        f32.load
        local.tee $l12
        local.get $l33
        f32.load offset=56
        f32.mul
        local.get $p9
        f32.load offset=4
        local.tee $l13
        local.get $l33
        f32.load offset=72
        f32.mul
        f32.add
        local.get $p9
        f32.load offset=8
        local.tee $l14
        local.get $l33
        f32.load offset=88
        f32.mul
        f32.add
        local.tee $l17
        local.get $l25
        f32.sub
        f32.store
        local.get $p9
        i32.const 0
        i32.store offset=12
        local.get $p9
        local.get $l25
        f32.store offset=8
        local.get $p9
        local.get $l12
        local.get $l15
        f32.mul
        local.get $l13
        local.get $l21
        f32.mul
        f32.add
        local.get $l14
        local.get $l11
        f32.mul
        f32.add
        local.tee $l11
        f32.store offset=4
        local.get $p9
        local.get $l12
        local.get $l22
        f32.mul
        local.get $l13
        local.get $l20
        f32.mul
        f32.add
        local.get $l14
        local.get $l10
        f32.mul
        f32.add
        local.tee $l10
        f32.store
        local.get $l16
        local.get $l11
        local.get $l11
        local.get $l16
        f32.lt
        select
        local.set $l16
        local.get $l23
        local.get $l10
        local.get $l10
        local.get $l23
        f32.lt
        select
        local.set $l23
        local.get $l19
        local.get $l11
        local.get $l11
        local.get $l19
        f32.gt
        select
        local.set $l19
        local.get $l18
        local.get $l10
        local.get $l10
        local.get $l18
        f32.gt
        select
        local.set $l18
        local.get $l34
        local.get $l40
        i32.add
        local.get $l17
        local.get $l26
        f32.lt
        if $I2 (result i32)
          block $B3
            local.get $l10
            local.get $l27
            f32.lt
            br_if $B3
            local.get $l10
            local.get $l32
            f32.gt
            br_if $B3
            local.get $l11
            local.get $l31
            f32.lt
            br_if $B3
            local.get $l11
            local.get $l30
            f32.gt
            br_if $B3
            block $B4
              local.get $l10
              local.get $l33
              f32.load offset=32
              local.tee $l15
              f32.eq
              local.get $l11
              local.get $l33
              f32.load offset=36
              local.tee $l22
              f32.eq
              i32.and
              local.tee $l37
              br_if $B4
              local.get $l10
              local.get $l33
              f32.load
              local.tee $l21
              f32.eq
              local.get $l11
              local.get $l33
              f32.load offset=4
              local.tee $l20
              f32.eq
              i32.and
              local.tee $p9
              br_if $B4
              block $B5 (result i32)
                i32.const 0
                local.get $l11
                local.get $l22
                f32.lt
                local.tee $l47
                local.get $l11
                local.get $l20
                f32.lt
                local.tee $l44
                i32.eq
                br_if $B5
                drop
                i32.const 0
                local.get $l15
                f32.const 0x1p-23 (;=1.19209e-07;)
                f32.add
                local.get $l20
                local.get $l22
                f32.sub
                local.tee $l17
                f32.mul
                local.get $l11
                local.get $l22
                f32.sub
                local.get $l21
                local.get $l15
                f32.sub
                f32.mul
                f32.add
                local.tee $l28
                local.get $l10
                local.get $l17
                f32.mul
                local.tee $l29
                local.get $l17
                f32.const 0x0p+0 (;=0;)
                f32.gt
                local.tee $l45
                select
                local.get $l29
                local.get $l28
                local.get $l45
                select
                f32.ge
                i32.eqz
                br_if $B5
                drop
                i32.const 1
              end
              local.set $l35
              local.get $p9
              br_if $B4
              local.get $l10
              local.get $l33
              f32.load offset=16
              local.tee $l28
              f32.eq
              local.get $l11
              local.get $l33
              f32.load offset=20
              local.tee $l17
              f32.eq
              i32.and
              local.tee $p9
              br_if $B4
              block $B6
                local.get $l44
                local.get $l11
                local.get $l17
                f32.lt
                local.tee $l45
                i32.eq
                br_if $B6
                local.get $l21
                f32.const 0x1p-23 (;=1.19209e-07;)
                f32.add
                local.get $l17
                local.get $l20
                f32.sub
                local.tee $l29
                f32.mul
                local.get $l11
                local.get $l20
                f32.sub
                local.get $l28
                local.get $l21
                f32.sub
                f32.mul
                f32.add
                local.tee $l20
                local.get $l10
                local.get $l29
                f32.mul
                local.tee $l21
                local.get $l29
                f32.const 0x0p+0 (;=0;)
                f32.gt
                local.tee $l44
                select
                local.get $l21
                local.get $l20
                local.get $l44
                select
                f32.ge
                i32.eqz
                br_if $B6
                local.get $l35
                br_if $B3
                local.get $l35
                i32.const 1
                i32.add
                local.set $l35
              end
              local.get $p9
              br_if $B4
              local.get $l37
              br_if $B4
              block $B7
                local.get $l45
                local.get $l47
                i32.eq
                br_if $B7
                local.get $l28
                f32.const 0x1p-23 (;=1.19209e-07;)
                f32.add
                local.get $l22
                local.get $l17
                f32.sub
                local.tee $l22
                f32.mul
                local.get $l11
                local.get $l17
                f32.sub
                local.get $l15
                local.get $l28
                f32.sub
                f32.mul
                f32.add
                local.tee $l20
                local.get $l10
                local.get $l22
                f32.mul
                local.tee $l15
                local.get $l22
                f32.const 0x0p+0 (;=0;)
                f32.gt
                local.tee $p9
                select
                local.get $l15
                local.get $l20
                local.get $p9
                select
                f32.ge
                i32.eqz
                br_if $B7
                local.get $l35
                i32.const 1
                i32.ne
                br_if $B4
                br $B3
              end
              local.get $l35
              i32.eqz
              br_if $B3
            end
            local.get $p0
            f32.load offset=56
            local.set $l21
            local.get $p0
            f32.load offset=48
            local.set $l17
            local.get $p0
            f32.load offset=52
            local.set $l28
            local.get $p8
            f32.load offset=4
            local.set $l22
            local.get $p8
            f32.load offset=8
            local.set $l20
            local.get $p8
            f32.load
            local.set $l15
            local.get $p5
            local.get $p6
            i32.load
            local.tee $l37
            i32.const 6
            i32.shl
            i32.add
            local.tee $p9
            local.get $p1
            i32.store offset=48
            local.get $p9
            local.get $l15
            f32.store offset=32
            local.get $p9
            local.get $l24
            f32.store offset=12
            local.get $p9
            local.get $l14
            f32.store offset=8
            local.get $p9
            local.get $l13
            f32.store offset=4
            local.get $p9
            local.get $l12
            f32.store
            local.get $p9
            local.get $l20
            f32.store offset=40
            local.get $p9
            local.get $l22
            f32.store offset=36
            local.get $p9
            i32.const 0
            i32.store offset=28
            local.get $p9
            local.get $l15
            local.get $l17
            local.get $l12
            f32.sub
            f32.mul
            local.get $l22
            local.get $l28
            local.get $l13
            f32.sub
            f32.mul
            f32.add
            local.get $l20
            local.get $l21
            local.get $l14
            f32.sub
            f32.mul
            f32.add
            local.tee $l21
            f32.neg
            f32.store offset=44
            local.get $p9
            local.get $l14
            local.get $l20
            local.get $l21
            f32.mul
            f32.add
            f32.store offset=24
            local.get $p9
            local.get $l13
            local.get $l22
            local.get $l21
            f32.mul
            f32.add
            f32.store offset=20
            local.get $p9
            local.get $l12
            local.get $l15
            local.get $l21
            f32.mul
            f32.add
            f32.store offset=16
            local.get $p6
            local.get $l37
            i32.const 1
            i32.add
            local.tee $p9
            i32.store
            local.get $l36
            i32.const 1
            i32.add
            local.set $l36
            local.get $p9
            local.get $l39
            i32.sub
            local.tee $p9
            i32.const 15
            i32.le_u
            br_if $B3
            local.get $l43
            local.get $p9
            call $f69977
            local.get $p6
            local.get $l42
            i32.store
          end
          i32.const 1
        else
          i32.const 0
        end
        i32.store8
        local.get $l34
        i32.const 1
        i32.add
        local.tee $l34
        local.get $p3
        i32.load8_u offset=18
        local.tee $p9
        i32.lt_u
        br_if $L1
      end
      local.get $p9
      local.get $l36
      i32.eq
      br_if $B0
      local.get $l16
      f32.const 0x1p-23 (;=1.19209e-07;)
      f32.add
      local.set $l20
      local.get $l23
      f32.const 0x1p-23 (;=1.19209e-07;)
      f32.add
      local.set $l23
      local.get $l19
      f32.const -0x1p-23 (;=-1.19209e-07;)
      f32.add
      local.set $l22
      local.get $l18
      f32.const -0x1p-23 (;=-1.19209e-07;)
      f32.add
      local.set $l18
      local.get $p3
      f32.load
      local.tee $l11
      local.get $p4
      i32.load offset=40
      local.tee $p9
      f32.load
      f32.mul
      local.get $p3
      f32.load offset=4
      local.tee $l10
      local.get $p9
      f32.load offset=4
      f32.mul
      f32.add
      local.get $p3
      f32.load offset=8
      local.tee $l12
      local.get $p9
      f32.load offset=8
      f32.mul
      f32.add
      local.tee $l13
      f32.const 0x1p+0 (;=1;)
      local.get $l13
      local.get $l13
      f32.mul
      local.get $l11
      local.get $p9
      f32.load offset=16
      f32.mul
      local.get $l10
      local.get $p9
      f32.load offset=20
      f32.mul
      f32.add
      local.get $l12
      local.get $p9
      f32.load offset=24
      f32.mul
      f32.add
      local.tee $l13
      local.get $l13
      f32.mul
      f32.add
      local.get $l11
      local.get $p9
      f32.load offset=32
      f32.mul
      local.get $l10
      local.get $p9
      f32.load offset=36
      f32.mul
      f32.add
      local.get $l12
      local.get $p9
      f32.load offset=40
      f32.mul
      f32.add
      local.tee $l11
      local.get $l11
      f32.mul
      f32.add
      f32.sqrt
      f32.div
      local.tee $l10
      f32.mul
      local.tee $l15
      local.get $p2
      i32.load offset=28
      local.get $l46
      i32.load8_u
      i32.const 12
      i32.mul
      i32.add
      local.tee $l34
      f32.load
      local.tee $l12
      local.get $p4
      i32.load offset=36
      local.tee $p9
      f32.load
      f32.mul
      local.get $l34
      f32.load offset=4
      local.tee $l14
      local.get $p9
      f32.load offset=16
      f32.mul
      f32.add
      local.get $l34
      f32.load offset=8
      local.tee $l16
      local.get $p9
      f32.load offset=32
      f32.mul
      f32.add
      f32.mul
      local.get $l13
      local.get $l10
      f32.mul
      local.tee $l21
      local.get $l12
      local.get $p9
      f32.load offset=4
      f32.mul
      local.get $l14
      local.get $p9
      f32.load offset=20
      f32.mul
      f32.add
      local.get $l16
      local.get $p9
      f32.load offset=36
      f32.mul
      f32.add
      f32.mul
      f32.add
      local.get $l11
      local.get $l10
      f32.mul
      local.tee $l17
      local.get $l12
      local.get $p9
      f32.load offset=8
      f32.mul
      local.get $l14
      local.get $p9
      f32.load offset=24
      f32.mul
      f32.add
      local.get $l16
      local.get $p9
      f32.load offset=40
      f32.mul
      f32.add
      f32.mul
      f32.add
      local.set $l24
      i32.const 0
      local.set $p0
      i32.const 0
      local.set $l37
      loop $L8
        block $B9
          local.get $l18
          local.get $l33
          local.get $l37
          i32.const 4
          i32.shl
          i32.add
          local.tee $p2
          f32.load
          local.tee $l13
          f32.gt
          br_if $B9
          local.get $l13
          local.get $l23
          f32.gt
          br_if $B9
          local.get $l22
          local.get $p2
          f32.load offset=4
          local.tee $l11
          f32.gt
          br_if $B9
          local.get $l11
          local.get $l20
          f32.gt
          br_if $B9
          local.get $p3
          i32.load8_u offset=18
          local.tee $l35
          i32.eqz
          br_if $B9
          local.get $l38
          local.get $l35
          i32.const 1
          i32.sub
          i32.const 4
          i32.shl
          i32.add
          local.tee $p9
          f32.load
          local.set $l14
          local.get $p9
          f32.load offset=4
          local.set $l10
          i32.const 0
          local.set $p9
          i32.const 0
          local.set $l36
          block $B10
            loop $L11
              local.get $l13
              local.get $l14
              local.tee $l16
              f32.eq
              local.get $l11
              local.get $l10
              local.tee $l12
              f32.eq
              i32.and
              br_if $B10
              local.get $l13
              local.get $l38
              local.get $p9
              i32.const 4
              i32.shl
              i32.add
              local.tee $l34
              f32.load
              local.tee $l14
              f32.eq
              local.get $l11
              local.get $l34
              f32.load offset=4
              local.tee $l10
              f32.eq
              i32.and
              br_if $B10
              block $B12
                local.get $l11
                local.get $l12
                f32.lt
                local.get $l10
                local.get $l11
                f32.gt
                i32.eq
                br_if $B12
                local.get $l16
                f32.const 0x1p-23 (;=1.19209e-07;)
                f32.add
                local.get $l10
                local.get $l12
                f32.sub
                local.tee $l19
                f32.mul
                local.get $l11
                local.get $l12
                f32.sub
                local.get $l14
                local.get $l16
                f32.sub
                f32.mul
                f32.add
                local.tee $l12
                local.get $l13
                local.get $l19
                f32.mul
                local.tee $l16
                local.get $l19
                f32.const 0x0p+0 (;=0;)
                f32.gt
                local.tee $l34
                select
                local.get $l16
                local.get $l12
                local.get $l34
                select
                f32.ge
                i32.eqz
                br_if $B12
                local.get $l36
                i32.const 1
                i32.eq
                br_if $B9
                local.get $l36
                i32.const 1
                i32.add
                local.set $l36
              end
              local.get $p9
              i32.const 1
              i32.add
              local.tee $p9
              local.get $l35
              i32.ne
              br_if $L11
            end
            local.get $l36
            i32.eqz
            br_if $B9
          end
          local.get $p0
          i32.const 1
          i32.add
          local.set $p0
          local.get $l15
          local.get $l13
          local.get $l33
          f32.load offset=48
          f32.mul
          local.get $l11
          local.get $l33
          f32.load offset=52
          f32.mul
          f32.add
          local.get $p2
          f32.load offset=8
          local.tee $l10
          local.get $l33
          f32.load offset=56
          f32.mul
          f32.add
          local.tee $l12
          f32.mul
          local.get $l21
          local.get $l13
          local.get $l33
          f32.load offset=64
          f32.mul
          local.get $l11
          local.get $l33
          f32.load offset=68
          f32.mul
          f32.add
          local.get $l10
          local.get $l33
          f32.load offset=72
          f32.mul
          f32.add
          local.tee $l14
          f32.mul
          f32.add
          local.get $l17
          local.get $l13
          local.get $l33
          f32.load offset=80
          f32.mul
          local.get $l11
          local.get $l33
          f32.load offset=84
          f32.mul
          f32.add
          local.get $l10
          local.get $l33
          f32.load offset=88
          f32.mul
          f32.add
          local.tee $l11
          f32.mul
          f32.add
          local.get $l24
          f32.sub
          local.tee $l10
          local.get $p7
          f32.load
          f32.gt
          br_if $B9
          local.get $p8
          f32.load offset=4
          local.set $l13
          local.get $p8
          f32.load offset=8
          local.set $l16
          local.get $p8
          f32.load
          local.set $l19
          local.get $p5
          local.get $p6
          i32.load
          local.tee $l34
          i32.const 6
          i32.shl
          i32.add
          local.tee $p9
          local.get $p1
          i32.store offset=48
          local.get $p9
          local.get $l19
          f32.store offset=32
          local.get $p9
          local.get $l12
          f32.store offset=16
          local.get $p9
          i32.const 0
          i32.store offset=12
          local.get $p9
          local.get $l11
          local.get $l17
          local.get $l10
          f32.mul
          f32.sub
          local.tee $l26
          f32.store offset=8
          local.get $p9
          local.get $l14
          local.get $l21
          local.get $l10
          f32.mul
          f32.sub
          local.tee $l27
          f32.store offset=4
          local.get $p9
          local.get $l12
          local.get $l15
          local.get $l10
          f32.mul
          f32.sub
          local.tee $l10
          f32.store
          local.get $p9
          local.get $l16
          f32.store offset=40
          local.get $p9
          local.get $l13
          f32.store offset=36
          local.get $p9
          i32.const 0
          i32.store offset=28
          local.get $p9
          local.get $l11
          f32.store offset=24
          local.get $p9
          local.get $l14
          f32.store offset=20
          local.get $p9
          local.get $l19
          local.get $l10
          local.get $l12
          f32.sub
          f32.mul
          local.get $l13
          local.get $l27
          local.get $l14
          f32.sub
          f32.mul
          f32.add
          local.get $l16
          local.get $l26
          local.get $l11
          f32.sub
          f32.mul
          f32.add
          f32.store offset=44
          local.get $p6
          local.get $l34
          i32.const 1
          i32.add
          local.tee $p9
          i32.store
          local.get $p9
          local.get $l39
          i32.sub
          local.tee $p9
          i32.const 16
          i32.lt_u
          br_if $B9
          local.get $l43
          local.get $p9
          call $f69977
          local.get $p6
          local.get $l42
          i32.store
        end
        local.get $l37
        i32.const 1
        i32.add
        local.tee $l37
        i32.const 3
        i32.ne
        br_if $L8
      end
      local.get $p0
      i32.const 3
      i32.eq
      br_if $B0
      local.get $p3
      i32.load8_u offset=18
      local.set $l35
      i32.const 2
      local.set $l34
      i32.const 0
      local.set $p2
      loop $L13
        local.get $l35
        i32.const 255
        i32.and
        local.set $p9
        i32.const 0
        local.set $l35
        local.get $p9
        if $I14
          local.get $l33
          local.get $p2
          i32.const 4
          i32.shl
          i32.add
          local.tee $l35
          f32.load offset=4
          local.tee $l14
          local.get $l33
          local.get $l34
          i32.const 4
          i32.shl
          i32.add
          local.tee $l34
          f32.load offset=4
          local.tee $l16
          local.get $l14
          local.get $l16
          f32.gt
          select
          local.set $l20
          local.get $l35
          f32.load
          local.tee $l19
          local.get $l34
          f32.load
          local.tee $l18
          local.get $l18
          local.get $l19
          f32.lt
          select
          local.set $l23
          local.get $l14
          local.get $l16
          local.get $l14
          local.get $l16
          f32.lt
          select
          local.set $l21
          local.get $l19
          local.get $l18
          local.get $l18
          local.get $l19
          f32.gt
          select
          local.set $l22
          local.get $p9
          i32.const 1
          i32.sub
          local.set $l34
          i32.const 0
          local.set $p9
          loop $L15
            block $B16
              local.get $p9
              local.get $l40
              i32.add
              i32.load8_u
              i32.eqz
              if $I17
                local.get $l34
                local.get $l40
                i32.add
                i32.load8_u
                i32.eqz
                br_if $B16
              end
              local.get $l38
              local.get $p9
              i32.const 4
              i32.shl
              local.tee $l36
              i32.add
              local.tee $l35
              f32.load
              local.tee $l11
              local.get $l38
              local.get $l34
              i32.const 4
              i32.shl
              local.tee $l37
              i32.add
              local.tee $l34
              f32.load
              local.tee $l10
              local.get $l10
              local.get $l11
              f32.gt
              select
              local.get $l23
              f32.gt
              br_if $B16
              local.get $l22
              local.get $l11
              local.get $l10
              local.get $l10
              local.get $l11
              f32.lt
              select
              f32.gt
              br_if $B16
              local.get $l35
              f32.load offset=4
              local.tee $l12
              local.get $l34
              f32.load offset=4
              local.tee $l13
              local.get $l12
              local.get $l13
              f32.lt
              select
              local.get $l20
              f32.gt
              br_if $B16
              local.get $l21
              local.get $l12
              local.get $l13
              local.get $l12
              local.get $l13
              f32.gt
              select
              f32.gt
              br_if $B16
              local.get $l19
              local.get $l11
              f32.sub
              local.get $l16
              local.get $l12
              f32.sub
              f32.mul
              local.get $l18
              local.get $l11
              f32.sub
              local.get $l14
              local.get $l12
              f32.sub
              f32.mul
              f32.sub
              local.tee $l15
              local.get $l19
              local.get $l10
              f32.sub
              local.get $l16
              local.get $l13
              f32.sub
              f32.mul
              local.get $l18
              local.get $l10
              f32.sub
              local.get $l14
              local.get $l13
              f32.sub
              f32.mul
              f32.sub
              local.tee $l17
              f32.mul
              f32.const 0x0p+0 (;=0;)
              f32.lt
              i32.eqz
              br_if $B16
              local.get $l11
              local.get $l19
              f32.sub
              local.get $l13
              local.get $l14
              f32.sub
              f32.mul
              local.get $l12
              local.get $l14
              f32.sub
              local.get $l10
              local.get $l19
              f32.sub
              f32.mul
              f32.sub
              local.get $l11
              local.get $l18
              f32.sub
              local.get $l13
              local.get $l16
              f32.sub
              f32.mul
              local.get $l12
              local.get $l16
              f32.sub
              local.get $l10
              local.get $l18
              f32.sub
              f32.mul
              f32.sub
              f32.mul
              f32.const 0x0p+0 (;=0;)
              f32.lt
              i32.eqz
              br_if $B16
              local.get $l25
              local.get $l36
              local.get $l41
              i32.add
              f32.load
              f32.add
              local.tee $l24
              local.get $l15
              f32.const 0x1p+0 (;=1;)
              local.get $l17
              local.get $l15
              f32.sub
              f32.div
              f32.mul
              local.tee $l17
              local.get $l25
              local.get $l37
              local.get $l41
              i32.add
              f32.load
              f32.add
              local.get $l24
              f32.sub
              f32.mul
              f32.sub
              local.tee $l15
              local.get $l25
              f32.sub
              local.tee $l24
              local.get $p7
              f32.load
              f32.gt
              br_if $B16
              local.get $l33
              f32.load offset=84
              local.set $l32
              local.get $l33
              f32.load offset=80
              local.set $l28
              local.get $l33
              f32.load offset=52
              local.set $l31
              local.get $l33
              f32.load offset=48
              local.set $l30
              local.get $l33
              f32.load offset=88
              local.set $l26
              local.get $l33
              f32.load offset=56
              local.set $l27
              local.get $p8
              f32.load offset=8
              local.set $l29
              local.get $p8
              i64.load
              local.set $l48
              local.get $p5
              local.get $p6
              i32.load
              local.tee $l35
              i32.const 6
              i32.shl
              i32.add
              local.tee $l34
              local.get $l11
              local.get $l10
              local.get $l11
              f32.sub
              local.get $l17
              f32.mul
              f32.sub
              local.tee $l11
              local.get $l33
              f32.load offset=64
              f32.mul
              local.get $l12
              local.get $l13
              local.get $l12
              f32.sub
              local.get $l17
              f32.mul
              f32.sub
              local.tee $l10
              local.get $l33
              f32.load offset=68
              f32.mul
              f32.add
              local.tee $l12
              local.get $l15
              local.get $l33
              f32.load offset=72
              local.tee $l13
              f32.mul
              f32.add
              f32.store offset=4
              local.get $l34
              local.get $l11
              local.get $l28
              f32.mul
              local.get $l10
              local.get $l32
              f32.mul
              f32.add
              local.tee $l17
              local.get $l15
              local.get $l26
              f32.mul
              f32.add
              f32.store offset=8
              local.get $l34
              i32.const 0
              i32.store offset=12
              local.get $l34
              local.get $l11
              local.get $l30
              f32.mul
              local.get $l10
              local.get $l31
              f32.mul
              f32.add
              local.tee $l11
              local.get $l25
              local.get $l27
              f32.mul
              f32.add
              f32.store offset=16
              local.get $l34
              local.get $l48
              i64.store offset=32
              local.get $l34
              local.get $p1
              i32.store offset=48
              local.get $l34
              local.get $l11
              local.get $l27
              local.get $l15
              f32.mul
              f32.add
              f32.store
              local.get $l34
              local.get $l12
              local.get $l25
              local.get $l13
              f32.mul
              f32.add
              f32.store offset=20
              local.get $l34
              local.get $l17
              local.get $l25
              local.get $l26
              f32.mul
              f32.add
              f32.store offset=24
              local.get $l34
              i32.const 0
              i32.store offset=28
              local.get $l34
              local.get $l24
              f32.store offset=44
              local.get $l34
              local.get $l29
              f32.store offset=40
              local.get $p6
              local.get $l35
              i32.const 1
              i32.add
              local.tee $l34
              i32.store
              local.get $l34
              local.get $l39
              i32.sub
              local.tee $l34
              i32.const 16
              i32.lt_u
              br_if $B16
              local.get $l43
              local.get $l34
              call $f69977
              local.get $p6
              local.get $l42
              i32.store
            end
            local.get $p9
            local.set $l34
            local.get $p9
            i32.const 1
            i32.add
            local.tee $p9
            local.get $p3
            i32.load8_u offset=18
            local.tee $l35
            i32.lt_u
            br_if $L15
          end
        end
        local.get $p2
        local.tee $l34
        i32.const 1
        i32.add
        local.tee $p9
        local.set $p2
        local.get $p9
        i32.const 3
        i32.ne
        br_if $L13
      end
    end
    local.get $l33
    i32.const 96
    i32.add
    global.set $g0)
