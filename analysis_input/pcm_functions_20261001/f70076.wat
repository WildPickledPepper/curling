  (func $f70076 (type $t29) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 i32) (param $p7 i32) (param $p8 i32) (param $p9 i32)
    (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 i32) (local $l17 i32) (local $l18 i32) (local $l19 i32) (local $l20 i32) (local $l21 i32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32) (local $l33 f32) (local $l34 f32) (local $l35 f32) (local $l36 f32) (local $l37 f32) (local $l38 f32) (local $l39 f32) (local $l40 f32) (local $l41 f32) (local $l42 f32) (local $l43 f32) (local $l44 f32) (local $l45 f32) (local $l46 f32) (local $l47 f32) (local $l48 f32) (local $l49 f32) (local $l50 f32) (local $l51 f32) (local $l52 f32) (local $l53 f32) (local $l54 f32) (local $l55 f32) (local $l56 f32) (local $l57 f32) (local $l58 f32) (local $l59 f32) (local $l60 f32) (local $l61 f32) (local $l62 f32) (local $l63 f32) (local $l64 f32) (local $l65 f32) (local $l66 f32) (local $l67 f32) (local $l68 f32)
    global.get $g0
    i32.const -64
    i32.add
    local.tee $l16
    global.set $g0
    local.get $p2
    i32.load16_u offset=16
    local.set $l13
    local.get $p0
    i32.load offset=32
    local.set $l14
    local.get $p4
    i32.load offset=40
    local.tee $l10
    f32.load offset=40
    local.set $l24
    local.get $l10
    f32.load offset=36
    local.set $l26
    local.get $l10
    f32.load offset=24
    local.set $l27
    local.get $l10
    f32.load offset=20
    local.set $l28
    local.get $l10
    f32.load offset=32
    local.set $l29
    local.get $l10
    f32.load offset=16
    local.set $l31
    local.get $p2
    f32.load offset=8
    local.set $l22
    local.get $l10
    f32.load offset=8
    local.set $l32
    local.get $p2
    f32.load
    local.set $l23
    local.get $l10
    f32.load
    local.set $l30
    local.get $p2
    f32.load offset=4
    local.set $l25
    local.get $l10
    f32.load offset=4
    local.set $l33
    local.get $l16
    local.tee $l12
    i32.const 0
    i32.store offset=60
    local.get $l12
    local.get $l23
    local.get $l29
    f32.mul
    local.get $l25
    local.get $l26
    f32.mul
    f32.add
    local.get $l22
    local.get $l24
    f32.mul
    f32.add
    local.tee $l24
    f32.const 0x1p+0 (;=1;)
    local.get $l23
    local.get $l30
    f32.mul
    local.get $l25
    local.get $l33
    f32.mul
    f32.add
    local.get $l22
    local.get $l32
    f32.mul
    f32.add
    local.tee $l26
    local.get $l26
    f32.mul
    local.get $l23
    local.get $l31
    f32.mul
    local.get $l25
    local.get $l28
    f32.mul
    f32.add
    local.get $l22
    local.get $l27
    f32.mul
    f32.add
    local.tee $l22
    local.get $l22
    f32.mul
    f32.add
    local.get $l24
    local.get $l24
    f32.mul
    f32.add
    f32.sqrt
    f32.div
    local.tee $l23
    f32.mul
    f32.store offset=56
    local.get $l12
    local.get $l22
    local.get $l23
    f32.mul
    f32.store offset=52
    local.get $l12
    local.get $l26
    local.get $l23
    f32.mul
    f32.store offset=48
    local.get $l12
    local.get $l12
    i32.const 48
    i32.add
    call $f69972
    local.get $p3
    i32.load16_u offset=16
    local.set $l10
    local.get $p1
    i32.load offset=32
    local.set $l20
    local.get $l12
    local.get $p2
    i32.load8_u offset=18
    local.tee $l21
    i32.const 4
    i32.shl
    i32.sub
    i32.const 16
    i32.sub
    local.tee $l16
    local.tee $l15
    global.set $g0
    local.get $l15
    local.get $p3
    i32.load8_u offset=18
    local.tee $l17
    i32.const 4
    i32.shl
    i32.const 16
    i32.add
    local.tee $l18
    i32.sub
    local.tee $l15
    local.tee $l19
    global.set $g0
    local.get $l19
    local.get $l17
    i32.const 15
    i32.add
    i32.const 496
    i32.and
    i32.sub
    local.tee $l17
    local.tee $l19
    global.set $g0
    local.get $l19
    local.get $l18
    i32.sub
    local.tee $l18
    global.set $g0
    local.get $p4
    local.get $l13
    local.get $l14
    i32.add
    local.get $l21
    local.get $p0
    i32.load offset=28
    local.get $l16
    local.get $p4
    i32.load
    i32.load offset=16
    call_indirect $__indirect_function_table (type $t6)
    local.get $p5
    local.get $l10
    local.get $l20
    i32.add
    local.get $p3
    i32.load8_u offset=18
    local.get $p1
    i32.load offset=28
    local.get $l15
    local.get $p5
    i32.load
    i32.load offset=16
    call_indirect $__indirect_function_table (type $t6)
    local.get $l12
    f32.load offset=40
    local.set $l45
    local.get $l12
    f32.load offset=24
    local.set $l46
    local.get $l12
    f32.load offset=36
    local.set $l47
    local.get $l12
    f32.load offset=20
    local.set $l48
    f32.const 0x1.fffffep+127 (;=3.40282e+38;)
    local.set $l31
    f32.const -0x1.fffffep+127 (;=-3.40282e+38;)
    local.set $l32
    local.get $l12
    f32.load offset=8
    local.set $l49
    local.get $l12
    f32.load offset=4
    local.set $l50
    local.get $l12
    f32.load offset=32
    local.set $l51
    local.get $l12
    f32.load offset=16
    local.set $l52
    local.get $l12
    f32.load
    local.set $l53
    f32.const -0x1.fffffep+127 (;=-3.40282e+38;)
    local.set $l37
    f32.const -0x1.fffffep+127 (;=-3.40282e+38;)
    local.set $l39
    f32.const 0x1.fffffep+127 (;=3.40282e+38;)
    local.set $l40
    f32.const 0x1.fffffep+127 (;=3.40282e+38;)
    local.set $l55
    local.get $p2
    i32.load8_u offset=18
    local.tee $p4
    if $I0
      f32.const 0x1.fffffep+127 (;=3.40282e+38;)
      local.set $l25
      f32.const 0x1.fffffep+127 (;=3.40282e+38;)
      local.set $l24
      f32.const -0x1.fffffep+127 (;=-3.40282e+38;)
      local.set $l26
      f32.const -0x1.fffffep+127 (;=-3.40282e+38;)
      local.set $l27
      loop $L1
        local.get $l16
        local.get $l11
        i32.const 4
        i32.shl
        i32.add
        local.tee $l10
        i32.const 0
        i32.store offset=12
        local.get $l10
        local.get $l10
        f32.load
        local.tee $l23
        local.get $l49
        f32.mul
        local.get $l10
        f32.load offset=4
        local.tee $l28
        local.get $l46
        f32.mul
        f32.add
        local.get $l10
        f32.load offset=8
        local.tee $l29
        local.get $l45
        f32.mul
        f32.add
        f32.store offset=8
        local.get $l10
        local.get $l23
        local.get $l50
        f32.mul
        local.get $l28
        local.get $l48
        f32.mul
        f32.add
        local.get $l29
        local.get $l47
        f32.mul
        f32.add
        local.tee $l22
        f32.store offset=4
        local.get $l10
        local.get $l23
        local.get $l53
        f32.mul
        local.get $l28
        local.get $l52
        f32.mul
        f32.add
        local.get $l29
        local.get $l51
        f32.mul
        f32.add
        local.tee $l23
        f32.store
        local.get $l26
        local.get $l22
        local.get $l22
        local.get $l26
        f32.lt
        select
        local.set $l26
        local.get $l27
        local.get $l23
        local.get $l23
        local.get $l27
        f32.lt
        select
        local.set $l27
        local.get $l25
        local.get $l22
        local.get $l22
        local.get $l25
        f32.gt
        select
        local.set $l25
        local.get $l24
        local.get $l23
        local.get $l23
        local.get $l24
        f32.gt
        select
        local.set $l24
        local.get $l11
        i32.const 1
        i32.add
        local.tee $l11
        local.get $p4
        i32.ne
        br_if $L1
      end
      local.get $l26
      f32.const 0x1p-23 (;=1.19209e-07;)
      f32.add
      local.set $l39
      local.get $l25
      f32.const -0x1p-23 (;=-1.19209e-07;)
      f32.add
      local.set $l55
      local.get $l24
      f32.const -0x1p-23 (;=-1.19209e-07;)
      f32.add
      local.set $l40
      local.get $l27
      f32.const 0x1p-23 (;=1.19209e-07;)
      f32.add
      local.set $l37
    end
    local.get $l15
    f32.load offset=8
    local.set $l56
    local.get $l15
    f32.load offset=4
    local.set $l57
    local.get $l15
    f32.load
    local.set $l58
    local.get $l16
    f32.load offset=8
    local.tee $l33
    local.get $l45
    f32.mul
    local.set $l59
    local.get $l33
    local.get $l46
    f32.mul
    local.set $l60
    local.get $l33
    local.get $l49
    f32.mul
    local.set $l61
    i32.const 0
    local.set $p4
    local.get $l12
    f32.load offset=56
    local.set $l41
    local.get $l12
    f32.load offset=52
    local.set $l42
    local.get $l12
    f32.load offset=48
    local.set $l43
    block $B2
      block $B3 (result f32)
        local.get $p3
        i32.load8_u offset=18
        local.tee $l13
        i32.eqz
        if $I4
          i32.const 0
          local.set $l14
          f32.const -0x1.fffffep+127 (;=-3.40282e+38;)
          local.set $l30
          f32.const 0x1.fffffep+127 (;=3.40282e+38;)
          br $B3
        end
        local.get $l33
        local.get $p9
        f32.load
        f32.add
        local.set $l54
        local.get $l56
        local.set $l34
        local.get $l57
        local.set $l38
        local.get $l58
        local.set $l35
        i32.const 0
        local.set $l14
        f32.const 0x1.fffffep+127 (;=3.40282e+38;)
        local.set $l29
        f32.const -0x1.fffffep+127 (;=-3.40282e+38;)
        local.set $l30
        loop $L5
          local.get $l15
          local.get $p4
          i32.const 4
          i32.shl
          local.tee $l11
          i32.add
          local.tee $l10
          f32.load offset=12
          local.set $l44
          local.get $l11
          local.get $l18
          i32.add
          local.get $l35
          local.get $p6
          f32.load offset=48
          f32.sub
          local.tee $l22
          local.get $p6
          f32.load
          f32.mul
          local.get $l38
          local.get $p6
          f32.load offset=52
          f32.sub
          local.tee $l23
          local.get $p6
          f32.load offset=4
          f32.mul
          f32.add
          local.get $l34
          local.get $p6
          f32.load offset=56
          f32.sub
          local.tee $l25
          local.get $p6
          f32.load offset=8
          f32.mul
          f32.add
          local.tee $l24
          local.get $l49
          f32.mul
          local.get $l22
          local.get $p6
          f32.load offset=16
          f32.mul
          local.get $l23
          local.get $p6
          f32.load offset=20
          f32.mul
          f32.add
          local.get $l25
          local.get $p6
          f32.load offset=24
          f32.mul
          f32.add
          local.tee $l26
          local.get $l46
          f32.mul
          f32.add
          local.get $l22
          local.get $p6
          f32.load offset=32
          f32.mul
          local.get $l23
          local.get $p6
          f32.load offset=36
          f32.mul
          f32.add
          local.get $l25
          local.get $p6
          f32.load offset=40
          f32.mul
          f32.add
          local.tee $l23
          local.get $l45
          f32.mul
          f32.add
          local.tee $l25
          local.get $l33
          f32.sub
          local.tee $l36
          f32.store
          local.get $l10
          i32.const 0
          i32.store offset=12
          local.get $l10
          local.get $l33
          f32.store offset=8
          local.get $l10
          local.get $l24
          local.get $l50
          f32.mul
          local.get $l26
          local.get $l48
          f32.mul
          f32.add
          local.get $l23
          local.get $l47
          f32.mul
          f32.add
          local.tee $l22
          f32.store offset=4
          local.get $l10
          local.get $l24
          local.get $l53
          f32.mul
          local.get $l26
          local.get $l52
          f32.mul
          f32.add
          local.get $l23
          local.get $l51
          f32.mul
          f32.add
          local.tee $l23
          f32.store
          local.get $p4
          local.get $l17
          i32.add
          local.set $l10
          block $B6
            local.get $l25
            local.get $l54
            f32.lt
            if $I7
              local.get $l10
              i32.const 1
              i32.store8
              local.get $l23
              local.get $l40
              f32.lt
              br_if $B6
              local.get $l23
              local.get $l37
              f32.gt
              br_if $B6
              local.get $l22
              local.get $l55
              f32.lt
              br_if $B6
              local.get $l22
              local.get $l39
              f32.gt
              br_if $B6
              local.get $p2
              i32.load8_u offset=18
              local.tee $p1
              i32.eqz
              br_if $B6
              local.get $l16
              local.get $p1
              i32.const 1
              i32.sub
              i32.const 4
              i32.shl
              i32.add
              local.tee $l10
              f32.load
              local.set $l26
              local.get $l10
              f32.load offset=4
              local.set $l25
              i32.const 0
              local.set $l10
              i32.const 0
              local.set $p0
              block $B8
                loop $L9
                  local.get $l23
                  local.get $l26
                  local.tee $l27
                  f32.eq
                  local.get $l22
                  local.get $l25
                  local.tee $l24
                  f32.eq
                  i32.and
                  br_if $B8
                  local.get $l23
                  local.get $l16
                  local.get $l10
                  i32.const 4
                  i32.shl
                  i32.add
                  local.tee $l11
                  f32.load
                  local.tee $l26
                  f32.eq
                  local.get $l22
                  local.get $l11
                  f32.load offset=4
                  local.tee $l25
                  f32.eq
                  i32.and
                  br_if $B8
                  block $B10
                    local.get $l22
                    local.get $l25
                    f32.lt
                    local.get $l22
                    local.get $l24
                    f32.lt
                    i32.eq
                    br_if $B10
                    local.get $l27
                    f32.const 0x1p-23 (;=1.19209e-07;)
                    f32.add
                    local.get $l25
                    local.get $l24
                    f32.sub
                    local.tee $l28
                    f32.mul
                    local.get $l22
                    local.get $l24
                    f32.sub
                    local.get $l26
                    local.get $l27
                    f32.sub
                    f32.mul
                    f32.add
                    local.tee $l24
                    local.get $l23
                    local.get $l28
                    f32.mul
                    local.tee $l27
                    local.get $l28
                    f32.const 0x0p+0 (;=0;)
                    f32.gt
                    local.tee $l11
                    select
                    local.get $l27
                    local.get $l24
                    local.get $l11
                    select
                    f32.ge
                    i32.eqz
                    br_if $B10
                    local.get $p0
                    i32.const 1
                    i32.eq
                    br_if $B6
                    local.get $p0
                    i32.const 1
                    i32.add
                    local.set $p0
                  end
                  local.get $l10
                  i32.const 1
                  i32.add
                  local.tee $l10
                  local.get $p1
                  i32.ne
                  br_if $L9
                end
                local.get $p0
                i32.eqz
                br_if $B6
              end
              local.get $p8
              i32.load
              local.tee $l10
              i32.const 64
              i32.eq
              br_if $B2
              local.get $p7
              local.get $l10
              i32.const 48
              i32.mul
              i32.add
              local.tee $l10
              local.get $l44
              f32.store offset=12
              local.get $l10
              local.get $l34
              f32.store offset=8
              local.get $l10
              local.get $l38
              f32.store offset=4
              local.get $l10
              local.get $l35
              f32.store
              local.get $p7
              local.get $p8
              i32.load
              i32.const 48
              i32.mul
              i32.add
              local.tee $l10
              local.get $l61
              local.get $l53
              local.get $l23
              f32.mul
              local.get $l50
              local.get $l22
              f32.mul
              f32.add
              f32.add
              f32.store offset=16
              local.get $l10
              i32.const 0
              i32.store offset=28
              local.get $l10
              local.get $l51
              local.get $l23
              f32.mul
              local.get $l47
              local.get $l22
              f32.mul
              f32.add
              local.get $l59
              f32.add
              f32.store offset=24
              local.get $l10
              local.get $l60
              local.get $l52
              local.get $l23
              f32.mul
              local.get $l48
              local.get $l22
              f32.mul
              f32.add
              f32.add
              f32.store offset=20
              local.get $p8
              local.get $p8
              i32.load
              local.tee $l10
              i32.const 1
              i32.add
              i32.store
              local.get $p7
              local.get $l10
              i32.const 48
              i32.mul
              i32.add
              local.tee $l10
              local.get $l43
              f32.store offset=32
              local.get $l10
              local.get $l36
              f32.store offset=44
              local.get $l10
              local.get $l41
              f32.store offset=40
              local.get $l10
              local.get $l42
              f32.store offset=36
              local.get $l14
              i32.const 1
              i32.add
              local.set $l14
              local.get $p3
              i32.load8_u offset=18
              local.set $l13
              br $B6
            end
            local.get $l10
            i32.const 0
            i32.store8
          end
          local.get $l32
          local.get $l22
          local.get $l22
          local.get $l32
          f32.lt
          select
          local.set $l32
          local.get $l30
          local.get $l23
          local.get $l23
          local.get $l30
          f32.lt
          select
          local.set $l30
          local.get $l31
          local.get $l22
          local.get $l22
          local.get $l31
          f32.gt
          select
          local.set $l31
          local.get $l29
          local.get $l23
          local.get $l23
          local.get $l29
          f32.gt
          select
          local.set $l29
          local.get $p4
          i32.const 1
          i32.add
          local.tee $p4
          local.get $l13
          i32.const 255
          i32.and
          i32.lt_u
          if $I11
            local.get $l15
            local.get $p4
            i32.const 4
            i32.shl
            i32.add
            local.tee $l10
            f32.load offset=8
            local.set $l34
            local.get $l10
            f32.load offset=4
            local.set $l38
            local.get $l10
            f32.load
            local.set $l35
            br $L5
          end
        end
        local.get $l32
        f32.const 0x1p-23 (;=1.19209e-07;)
        f32.add
        local.set $l32
        local.get $l30
        f32.const 0x1p-23 (;=1.19209e-07;)
        f32.add
        local.set $l30
        local.get $l31
        f32.const -0x1p-23 (;=-1.19209e-07;)
        f32.add
        local.set $l31
        local.get $l13
        local.set $p4
        local.get $l29
        f32.const -0x1p-23 (;=-1.19209e-07;)
        f32.add
      end
      local.set $l29
      local.get $l14
      local.get $p4
      i32.const 255
      i32.and
      i32.eq
      br_if $B2
      i32.const 0
      local.set $p1
      block $B12
        local.get $p2
        i32.load8_u offset=18
        local.tee $l14
        i32.eqz
        if $I13
          i32.const 0
          local.set $p5
          br $B12
        end
        local.get $p3
        f32.load
        local.tee $l22
        local.get $p5
        i32.load offset=40
        local.tee $l10
        f32.load
        f32.mul
        local.get $p3
        f32.load offset=4
        local.tee $l23
        local.get $l10
        f32.load offset=4
        f32.mul
        f32.add
        local.get $p3
        f32.load offset=8
        local.tee $l25
        local.get $l10
        f32.load offset=8
        f32.mul
        f32.add
        local.tee $l24
        f32.const 0x1p+0 (;=1;)
        local.get $l24
        local.get $l24
        f32.mul
        local.get $l22
        local.get $l10
        f32.load offset=16
        f32.mul
        local.get $l23
        local.get $l10
        f32.load offset=20
        f32.mul
        f32.add
        local.get $l25
        local.get $l10
        f32.load offset=24
        f32.mul
        f32.add
        local.tee $l24
        local.get $l24
        f32.mul
        f32.add
        local.get $l22
        local.get $l10
        f32.load offset=32
        f32.mul
        local.get $l23
        local.get $l10
        f32.load offset=36
        f32.mul
        f32.add
        local.get $l25
        local.get $l10
        f32.load offset=40
        f32.mul
        f32.add
        local.tee $l22
        local.get $l22
        f32.mul
        f32.add
        f32.sqrt
        f32.div
        local.tee $l23
        f32.mul
        local.tee $l34
        local.get $l43
        local.get $p6
        f32.load
        f32.mul
        local.get $l42
        local.get $p6
        f32.load offset=16
        f32.mul
        f32.add
        local.get $l41
        local.get $p6
        f32.load offset=32
        f32.mul
        f32.add
        local.tee $l36
        f32.mul
        local.get $l24
        local.get $l23
        f32.mul
        local.tee $l38
        local.get $l43
        local.get $p6
        f32.load offset=4
        f32.mul
        local.get $l42
        local.get $p6
        f32.load offset=20
        f32.mul
        f32.add
        local.get $l41
        local.get $p6
        f32.load offset=36
        f32.mul
        f32.add
        local.tee $l54
        f32.mul
        f32.add
        local.get $l22
        local.get $l23
        f32.mul
        local.tee $l35
        local.get $l43
        local.get $p6
        f32.load offset=8
        f32.mul
        local.get $l42
        local.get $p6
        f32.load offset=24
        f32.mul
        f32.add
        local.get $l41
        local.get $p6
        f32.load offset=40
        f32.mul
        f32.add
        local.tee $l40
        f32.mul
        f32.add
        local.set $l44
        i32.const 0
        local.set $p5
        loop $L14 (result i32)
          block $B15
            local.get $l29
            local.get $l16
            local.get $p1
            i32.const 4
            i32.shl
            i32.add
            local.tee $l13
            f32.load
            local.tee $l24
            f32.gt
            br_if $B15
            local.get $l24
            local.get $l30
            f32.gt
            br_if $B15
            local.get $l31
            local.get $l13
            f32.load offset=4
            local.tee $l22
            f32.gt
            br_if $B15
            local.get $l22
            local.get $l32
            f32.gt
            br_if $B15
            local.get $p4
            i32.const 255
            i32.and
            local.tee $p4
            i32.eqz
            br_if $B15
            local.get $l15
            local.get $p4
            i32.const 1
            i32.sub
            i32.const 4
            i32.shl
            i32.add
            local.tee $l10
            f32.load
            local.set $l26
            local.get $l10
            f32.load offset=4
            local.set $l23
            i32.const 0
            local.set $l10
            i32.const 0
            local.set $p0
            block $B16
              loop $L17
                local.get $l24
                local.get $l26
                local.tee $l27
                f32.eq
                local.get $l22
                local.get $l23
                local.tee $l25
                f32.eq
                i32.and
                br_if $B16
                local.get $l24
                local.get $l15
                local.get $l10
                i32.const 4
                i32.shl
                i32.add
                local.tee $l11
                f32.load
                local.tee $l26
                f32.eq
                local.get $l22
                local.get $l11
                f32.load offset=4
                local.tee $l23
                f32.eq
                i32.and
                br_if $B16
                block $B18
                  local.get $l22
                  local.get $l25
                  f32.lt
                  local.get $l22
                  local.get $l23
                  f32.lt
                  i32.eq
                  br_if $B18
                  local.get $l27
                  f32.const 0x1p-23 (;=1.19209e-07;)
                  f32.add
                  local.get $l23
                  local.get $l25
                  f32.sub
                  local.tee $l28
                  f32.mul
                  local.get $l22
                  local.get $l25
                  f32.sub
                  local.get $l26
                  local.get $l27
                  f32.sub
                  f32.mul
                  f32.add
                  local.tee $l25
                  local.get $l24
                  local.get $l28
                  f32.mul
                  local.tee $l27
                  local.get $l28
                  f32.const 0x0p+0 (;=0;)
                  f32.gt
                  local.tee $l11
                  select
                  local.get $l27
                  local.get $l25
                  local.get $l11
                  select
                  f32.ge
                  i32.eqz
                  br_if $B18
                  local.get $p0
                  i32.const 1
                  i32.eq
                  br_if $B15
                  local.get $p0
                  i32.const 1
                  i32.add
                  local.set $p0
                end
                local.get $l10
                i32.const 1
                i32.add
                local.tee $l10
                local.get $p4
                i32.ne
                br_if $L17
              end
              local.get $p0
              i32.eqz
              br_if $B15
            end
            local.get $l34
            local.get $l58
            local.get $p6
            f32.load offset=48
            local.get $l24
            local.get $l53
            f32.mul
            local.get $l22
            local.get $l50
            f32.mul
            f32.add
            local.get $l13
            f32.load offset=8
            local.tee $l26
            local.get $l49
            f32.mul
            f32.add
            local.tee $l23
            local.get $p6
            f32.load
            f32.mul
            local.get $l24
            local.get $l52
            f32.mul
            local.get $l22
            local.get $l48
            f32.mul
            f32.add
            local.get $l26
            local.get $l46
            f32.mul
            f32.add
            local.tee $l25
            local.get $p6
            f32.load offset=16
            f32.mul
            f32.add
            local.get $l24
            local.get $l51
            f32.mul
            local.get $l22
            local.get $l47
            f32.mul
            f32.add
            local.get $l26
            local.get $l45
            f32.mul
            f32.add
            local.tee $l22
            local.get $p6
            f32.load offset=32
            f32.mul
            f32.add
            f32.add
            local.tee $l26
            f32.sub
            f32.mul
            local.get $l38
            local.get $l57
            local.get $p6
            f32.load offset=52
            local.get $l23
            local.get $p6
            f32.load offset=4
            f32.mul
            local.get $l25
            local.get $p6
            f32.load offset=20
            f32.mul
            f32.add
            local.get $l22
            local.get $p6
            f32.load offset=36
            f32.mul
            f32.add
            f32.add
            local.tee $l27
            f32.sub
            f32.mul
            f32.add
            local.get $l35
            local.get $l56
            local.get $p6
            f32.load offset=56
            local.get $l23
            local.get $p6
            f32.load offset=8
            f32.mul
            local.get $l25
            local.get $p6
            f32.load offset=24
            f32.mul
            f32.add
            local.get $l22
            local.get $p6
            f32.load offset=40
            f32.mul
            f32.add
            f32.add
            local.tee $l28
            f32.sub
            f32.mul
            f32.add
            local.get $l44
            f32.div
            local.tee $l24
            local.get $p9
            f32.load
            f32.gt
            br_if $B15
            local.get $p8
            i32.load
            local.tee $l10
            i32.const 64
            i32.eq
            br_if $B2
            local.get $p7
            local.get $l10
            i32.const 48
            i32.mul
            i32.add
            local.tee $l10
            i32.const 0
            i32.store offset=12
            local.get $l10
            local.get $l28
            local.get $l40
            local.get $l24
            f32.mul
            f32.add
            f32.store offset=8
            local.get $l10
            local.get $l27
            local.get $l54
            local.get $l24
            f32.mul
            f32.add
            f32.store offset=4
            local.get $l10
            local.get $l26
            local.get $l36
            local.get $l24
            f32.mul
            f32.add
            f32.store
            local.get $p7
            local.get $p8
            i32.load
            i32.const 48
            i32.mul
            i32.add
            local.tee $l10
            local.get $l23
            f32.store offset=16
            local.get $l10
            i32.const 0
            i32.store offset=28
            local.get $l10
            local.get $l22
            f32.store offset=24
            local.get $l10
            local.get $l25
            f32.store offset=20
            local.get $p8
            local.get $p8
            i32.load
            local.tee $l10
            i32.const 1
            i32.add
            i32.store
            local.get $p7
            local.get $l10
            i32.const 48
            i32.mul
            i32.add
            local.tee $l10
            local.get $l43
            f32.store offset=32
            local.get $l10
            local.get $l24
            f32.store offset=44
            local.get $l10
            local.get $l41
            f32.store offset=40
            local.get $l10
            local.get $l42
            f32.store offset=36
            local.get $p5
            i32.const 1
            i32.add
            local.set $p5
            local.get $p2
            i32.load8_u offset=18
            local.set $l14
          end
          local.get $p1
          i32.const 1
          i32.add
          local.tee $p1
          local.get $l14
          i32.const 255
          i32.and
          i32.ge_u
          if $I19 (result i32)
            local.get $l14
          else
            local.get $p3
            i32.load8_u offset=18
            local.set $p4
            br $L14
          end
        end
        local.set $p1
      end
      local.get $p5
      local.get $p1
      i32.const 255
      i32.and
      i32.eq
      br_if $B2
      local.get $p3
      i32.load8_u offset=18
      local.tee $l13
      i32.eqz
      br_if $B2
      local.get $l13
      i32.const 1
      i32.sub
      local.set $l11
      local.get $p1
      local.set $p0
      i32.const 0
      local.set $l10
      loop $L20
        block $B21
          local.get $l17
          local.get $l10
          local.tee $p4
          i32.add
          i32.load8_u
          i32.eqz
          if $I22
            local.get $l11
            local.get $l17
            i32.add
            i32.load8_u
            i32.eqz
            br_if $B21
          end
          local.get $p0
          i32.const 255
          i32.and
          local.tee $l10
          i32.eqz
          if $I23
            i32.const 0
            local.set $p0
            br $B21
          end
          local.get $l15
          local.get $p4
          i32.const 4
          i32.shl
          local.tee $p0
          i32.add
          local.tee $l13
          f32.load offset=4
          local.tee $l26
          local.get $l15
          local.get $l11
          i32.const 4
          i32.shl
          local.tee $l11
          i32.add
          local.tee $l14
          f32.load offset=4
          local.tee $l28
          local.get $l26
          local.get $l28
          f32.gt
          select
          local.set $l38
          local.get $l13
          f32.load
          local.tee $l27
          local.get $l14
          f32.load
          local.tee $l29
          local.get $l27
          local.get $l29
          f32.gt
          select
          local.set $l32
          local.get $l26
          local.get $l28
          local.get $l26
          local.get $l28
          f32.lt
          select
          local.set $l30
          local.get $l27
          local.get $l29
          local.get $l27
          local.get $l29
          f32.lt
          select
          local.set $l31
          local.get $l28
          local.get $l26
          f32.sub
          local.set $l62
          local.get $l29
          local.get $l27
          f32.sub
          local.set $l63
          local.get $l33
          local.get $l11
          local.get $l18
          i32.add
          f32.load
          f32.add
          local.get $l33
          local.get $p0
          local.get $l18
          i32.add
          f32.load
          f32.add
          local.tee $l54
          f32.sub
          local.set $l40
          local.get $l16
          local.get $l10
          i32.const 1
          i32.sub
          i32.const 4
          i32.shl
          i32.add
          local.tee $l10
          f32.load offset=4
          local.set $l23
          local.get $l10
          f32.load
          local.set $l22
          i32.const 0
          local.set $l10
          loop $L24
            local.get $l22
            local.set $l25
            local.get $l23
            local.set $l24
            local.get $l16
            local.get $l10
            i32.const 4
            i32.shl
            i32.add
            local.tee $l11
            f32.load offset=4
            local.set $l23
            block $B25
              local.get $l31
              local.get $l11
              f32.load
              local.tee $l22
              local.get $l25
              local.get $l22
              local.get $l25
              f32.gt
              select
              f32.gt
              br_if $B25
              local.get $l22
              local.get $l25
              local.get $l22
              local.get $l25
              f32.lt
              select
              local.get $l32
              f32.gt
              br_if $B25
              local.get $l30
              local.get $l23
              local.get $l24
              local.get $l23
              local.get $l24
              f32.gt
              select
              f32.gt
              br_if $B25
              local.get $l23
              local.get $l24
              local.get $l23
              local.get $l24
              f32.lt
              select
              local.get $l38
              f32.gt
              br_if $B25
              local.get $l22
              local.get $l27
              f32.sub
              local.get $l24
              local.get $l26
              f32.sub
              f32.mul
              local.get $l23
              local.get $l26
              f32.sub
              local.get $l25
              local.get $l27
              f32.sub
              f32.mul
              f32.sub
              local.tee $l34
              local.get $l22
              local.get $l29
              f32.sub
              local.get $l24
              local.get $l28
              f32.sub
              f32.mul
              local.get $l23
              local.get $l28
              f32.sub
              local.get $l25
              local.get $l29
              f32.sub
              f32.mul
              f32.sub
              local.tee $l35
              f32.mul
              f32.const 0x0p+0 (;=0;)
              f32.lt
              i32.eqz
              br_if $B25
              local.get $l27
              local.get $l22
              f32.sub
              local.get $l28
              local.get $l23
              f32.sub
              f32.mul
              local.get $l29
              local.get $l22
              f32.sub
              local.get $l26
              local.get $l23
              f32.sub
              f32.mul
              f32.sub
              local.get $l27
              local.get $l25
              f32.sub
              local.get $l28
              local.get $l24
              f32.sub
              f32.mul
              local.get $l29
              local.get $l25
              f32.sub
              local.get $l26
              local.get $l24
              f32.sub
              f32.mul
              f32.sub
              f32.mul
              f32.const 0x0p+0 (;=0;)
              f32.lt
              i32.eqz
              br_if $B25
              local.get $l54
              local.get $l40
              local.get $l34
              local.get $l35
              local.get $l34
              f32.sub
              f32.div
              local.tee $l24
              f32.mul
              f32.sub
              local.tee $l25
              local.get $l33
              f32.sub
              local.tee $l34
              local.get $p9
              f32.load
              f32.gt
              br_if $B25
              local.get $p8
              i32.load
              local.tee $l11
              i32.const 64
              i32.eq
              br_if $B2
              local.get $p6
              f32.load offset=24
              local.set $l37
              local.get $p6
              f32.load offset=8
              local.set $l36
              local.get $p6
              f32.load offset=40
              local.set $l55
              local.get $p6
              f32.load offset=56
              local.set $l39
              local.get $p6
              f32.load offset=20
              local.set $l56
              local.get $p6
              f32.load offset=4
              local.set $l57
              local.get $p6
              f32.load offset=36
              local.set $l58
              local.get $p6
              f32.load offset=52
              local.set $l64
              local.get $p6
              f32.load offset=16
              local.set $l65
              local.get $p6
              f32.load
              local.set $l66
              local.get $p6
              f32.load offset=32
              local.set $l67
              local.get $p6
              f32.load offset=48
              local.set $l68
              local.get $p7
              local.get $l11
              i32.const 48
              i32.mul
              i32.add
              local.tee $l11
              i32.const 0
              i32.store offset=12
              local.get $l11
              local.get $l39
              local.get $l36
              local.get $l27
              local.get $l63
              local.get $l24
              f32.mul
              f32.sub
              local.tee $l35
              local.get $l53
              f32.mul
              local.get $l26
              local.get $l62
              local.get $l24
              f32.mul
              f32.sub
              local.tee $l24
              local.get $l50
              f32.mul
              f32.add
              local.tee $l39
              local.get $l25
              local.get $l49
              f32.mul
              f32.add
              local.tee $l44
              f32.mul
              local.get $l37
              local.get $l35
              local.get $l52
              f32.mul
              local.get $l24
              local.get $l48
              f32.mul
              f32.add
              local.tee $l37
              local.get $l25
              local.get $l46
              f32.mul
              f32.add
              local.tee $l36
              f32.mul
              f32.add
              local.get $l55
              local.get $l35
              local.get $l51
              f32.mul
              local.get $l24
              local.get $l47
              f32.mul
              f32.add
              local.tee $l24
              local.get $l25
              local.get $l45
              f32.mul
              f32.add
              local.tee $l25
              f32.mul
              f32.add
              f32.add
              f32.store offset=8
              local.get $l11
              local.get $l64
              local.get $l44
              local.get $l57
              f32.mul
              local.get $l36
              local.get $l56
              f32.mul
              f32.add
              local.get $l25
              local.get $l58
              f32.mul
              f32.add
              f32.add
              f32.store offset=4
              local.get $l11
              local.get $l68
              local.get $l44
              local.get $l66
              f32.mul
              local.get $l36
              local.get $l65
              f32.mul
              f32.add
              local.get $l25
              local.get $l67
              f32.mul
              f32.add
              f32.add
              f32.store
              local.get $p7
              local.get $p8
              i32.load
              i32.const 48
              i32.mul
              i32.add
              local.tee $l11
              local.get $l39
              local.get $l61
              f32.add
              f32.store offset=16
              local.get $l11
              i32.const 0
              i32.store offset=28
              local.get $l11
              local.get $l24
              local.get $l59
              f32.add
              f32.store offset=24
              local.get $l11
              local.get $l37
              local.get $l60
              f32.add
              f32.store offset=20
              local.get $p8
              local.get $p8
              i32.load
              local.tee $l11
              i32.const 1
              i32.add
              i32.store
              local.get $p7
              local.get $l11
              i32.const 48
              i32.mul
              i32.add
              local.tee $l11
              local.get $l43
              f32.store offset=32
              local.get $l11
              local.get $l34
              f32.store offset=44
              local.get $l11
              local.get $l41
              f32.store offset=40
              local.get $l11
              local.get $l42
              f32.store offset=36
              local.get $p2
              i32.load8_u offset=18
              local.set $p1
            end
            local.get $l10
            i32.const 1
            i32.add
            local.tee $l10
            local.get $p1
            i32.const 255
            i32.and
            i32.lt_u
            br_if $L24
          end
          local.get $p3
          i32.load8_u offset=18
          local.set $l13
          local.get $p1
          local.set $p0
        end
        local.get $p4
        local.tee $l11
        i32.const 1
        i32.add
        local.tee $l10
        local.get $l13
        i32.const 255
        i32.and
        i32.lt_u
        br_if $L20
      end
    end
    local.get $l12
    i32.const -64
    i32.sub
    global.set $g0)