  (func $f70129 (type $t9) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (result i32)
    (local $l5 i32) (local $l6 f32) (local $l7 f32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32) (local $l33 f32) (local $l34 f32) (local $l35 f32) (local $l36 f32) (local $l37 f32) (local $l38 f32) (local $l39 f32) (local $l40 f32) (local $l41 f32) (local $l42 f32) (local $l43 f32) (local $l44 f32) (local $l45 f32) (local $l46 f32) (local $l47 f32) (local $l48 f32) (local $l49 f32) (local $l50 f32) (local $l51 f32) (local $l52 f32) (local $l53 f32) (local $l54 f32) (local $l55 f32) (local $l56 i64)
    global.get $g0
    i32.const 208
    i32.sub
    local.tee $l5
    global.set $g0
    local.get $p3
    f32.load offset=8
    local.set $l42
    local.get $p3
    f32.load offset=4
    local.set $l27
    block $B0
      block $B1
        local.get $p3
        f32.load
        local.tee $l46
        f32.const 0x1p+0 (;=1;)
        f32.ne
        br_if $B1
        local.get $l27
        f32.const 0x1p+0 (;=1;)
        f32.ne
        br_if $B1
        f32.const 0x1p+0 (;=1;)
        local.set $l27
        local.get $l42
        f32.const 0x1p+0 (;=1;)
        f32.ne
        br_if $B1
        local.get $l5
        local.get $p2
        f32.load offset=24
        f32.const -0x1p+1 (;=-2;)
        f32.mul
        local.tee $l12
        local.get $p2
        f32.load offset=12
        local.tee $l6
        local.get $l6
        f32.mul
        f32.const -0x1p-1 (;=-0.5;)
        f32.add
        local.tee $l20
        f32.mul
        local.get $l6
        local.get $p2
        f32.load offset=20
        f32.const -0x1p+1 (;=-2;)
        f32.mul
        local.tee $l7
        local.get $p2
        f32.load
        local.tee $l15
        f32.mul
        local.get $p2
        f32.load offset=16
        f32.const -0x1p+1 (;=-2;)
        f32.mul
        local.tee $l17
        local.get $p2
        f32.load offset=4
        local.tee $l10
        f32.mul
        f32.sub
        f32.mul
        f32.sub
        local.get $p2
        f32.load offset=8
        local.tee $l11
        local.get $l17
        local.get $l15
        f32.mul
        local.get $l7
        local.get $l10
        f32.mul
        f32.add
        local.get $l12
        local.get $l11
        f32.mul
        f32.add
        local.tee $l21
        f32.mul
        f32.add
        f32.store offset=192
        local.get $l5
        i32.const 188
        i32.add
        local.tee $p3
        local.get $l10
        local.get $l21
        f32.mul
        local.get $l7
        local.get $l20
        f32.mul
        local.get $l6
        local.get $l17
        local.get $l11
        f32.mul
        local.get $l12
        local.get $l15
        f32.mul
        f32.sub
        f32.mul
        f32.sub
        f32.add
        f32.store
        local.get $l5
        local.get $l6
        f32.store offset=180
        local.get $l5
        local.get $l11
        f32.neg
        f32.store offset=176
        local.get $l5
        local.get $l10
        f32.neg
        f32.store offset=172
        local.get $l5
        local.get $l15
        f32.neg
        f32.store offset=168
        local.get $l5
        local.get $l15
        local.get $l21
        f32.mul
        local.get $l17
        local.get $l20
        f32.mul
        local.get $l6
        local.get $l12
        local.get $l10
        f32.mul
        local.get $l7
        local.get $l11
        f32.mul
        f32.sub
        f32.mul
        f32.sub
        f32.add
        f32.store offset=184
        local.get $l5
        local.get $p0
        local.get $l5
        i32.const 168
        i32.add
        call $f70486
        local.get $l5
        local.get $l5
        f32.load offset=16
        local.tee $l7
        f32.store offset=120
        local.get $l5
        local.get $l5
        f32.load offset=20
        local.tee $l17
        f32.store offset=124
        local.get $l5
        local.get $l5
        f32.load offset=28
        local.tee $l20
        f32.store offset=132
        local.get $l5
        local.get $l5
        f32.load offset=32
        local.tee $l21
        f32.store offset=136
        local.get $l5
        local.get $l5
        f32.load
        local.tee $l10
        f32.store offset=104
        local.get $l5
        local.get $l5
        f32.load offset=4
        local.tee $l11
        f32.store offset=108
        local.get $l5
        local.get $l5
        f32.load offset=8
        local.tee $l12
        f32.store offset=112
        local.get $l5
        local.get $l5
        f32.load offset=12
        local.tee $l25
        f32.store offset=116
        local.get $l5
        local.get $l5
        f32.load offset=24
        local.tee $l18
        f32.store offset=128
        local.get $l5
        f32.load offset=36
        local.set $l15
        local.get $l5
        local.get $l5
        f32.load offset=40
        local.tee $l8
        f32.store offset=144
        local.get $l5
        local.get $l5
        f32.load offset=44
        local.tee $l16
        f32.store offset=148
        local.get $l5
        local.get $l5
        i64.load offset=52 align=4
        i64.store offset=156 align=4
        local.get $l5
        local.get $l15
        f32.store offset=140
        local.get $l5
        local.get $l5
        f32.load offset=48
        f32.store offset=152
        block $B2 (result f32)
          local.get $l12
          local.get $l25
          local.get $l20
          f32.mul
          local.get $l7
          local.get $l18
          f32.mul
          f32.sub
          local.tee $l13
          f32.mul
          local.get $l10
          local.get $l7
          local.get $l21
          f32.mul
          local.get $l17
          local.get $l20
          f32.mul
          f32.sub
          local.tee $l28
          f32.mul
          local.get $l11
          local.get $l17
          local.get $l18
          f32.mul
          local.tee $l27
          local.get $l25
          local.get $l21
          f32.mul
          local.tee $l22
          f32.sub
          f32.mul
          f32.add
          f32.add
          local.tee $l6
          f32.const 0x0p+0 (;=0;)
          f32.eq
          if $I3
            f32.const 0x0p+0 (;=0;)
            local.set $l7
            f32.const 0x0p+0 (;=0;)
            local.set $l27
            f32.const 0x1p+0 (;=1;)
            local.set $l23
            f32.const 0x0p+0 (;=0;)
            local.set $l10
            f32.const 0x0p+0 (;=0;)
            local.set $l11
            f32.const 0x0p+0 (;=0;)
            local.set $l18
            f32.const 0x1p+0 (;=1;)
            local.set $l19
            f32.const 0x1p+0 (;=1;)
            br $B2
          end
          local.get $l10
          local.get $l7
          f32.mul
          local.get $l11
          local.get $l25
          f32.mul
          f32.sub
          f32.const 0x1p+0 (;=1;)
          local.get $l6
          f32.div
          local.tee $l6
          f32.mul
          local.set $l19
          local.get $l10
          local.get $l21
          f32.mul
          local.get $l12
          local.get $l18
          f32.mul
          f32.sub
          local.get $l6
          f32.mul
          local.set $l23
          local.get $l6
          local.get $l22
          local.get $l27
          f32.sub
          f32.neg
          f32.mul
          local.set $l27
          local.get $l11
          local.get $l17
          f32.mul
          local.get $l12
          local.get $l7
          f32.mul
          f32.sub
          local.get $l6
          f32.mul
          local.set $l7
          local.get $l6
          local.get $l10
          local.get $l20
          f32.mul
          local.get $l11
          local.get $l18
          f32.mul
          f32.sub
          f32.neg
          f32.mul
          local.set $l18
          local.get $l6
          local.get $l10
          local.get $l17
          f32.mul
          local.get $l12
          local.get $l25
          f32.mul
          f32.sub
          f32.neg
          f32.mul
          local.set $l10
          local.get $l6
          local.get $l11
          local.get $l21
          f32.mul
          local.get $l12
          local.get $l20
          f32.mul
          f32.sub
          f32.neg
          f32.mul
          local.set $l9
          local.get $l13
          local.get $l6
          f32.mul
          local.set $l11
          local.get $l28
          local.get $l6
          f32.mul
        end
        local.set $l6
        local.get $l5
        local.get $l19
        f32.store offset=200
        local.get $l5
        local.get $l18
        f32.store offset=196
        local.get $p3
        local.get $l10
        f32.store
        local.get $l5
        local.get $l23
        f32.store offset=184
        local.get $l5
        local.get $l7
        f32.store offset=176
        local.get $l5
        local.get $l11
        f32.store offset=192
        local.get $l5
        local.get $l27
        f32.store offset=180
        local.get $l5
        local.get $l6
        f32.store offset=168
        local.get $l5
        local.get $l9
        f32.store offset=172
        local.get $l5
        local.get $l10
        local.get $l8
        f32.neg
        local.tee $l12
        f32.mul
        local.get $l15
        local.get $l7
        f32.mul
        f32.sub
        local.get $l16
        local.get $l19
        f32.mul
        f32.sub
        f32.neg
        f32.store offset=92
        local.get $l5
        local.get $l23
        local.get $l12
        f32.mul
        local.get $l15
        local.get $l9
        f32.mul
        f32.sub
        local.get $l16
        local.get $l18
        f32.mul
        f32.sub
        f32.neg
        f32.store offset=88
        local.get $l5
        i32.const 0
        i32.store16 offset=16
        local.get $l5
        local.get $p4
        i32.store offset=12
        local.get $l5
        i32.const 2
        i32.store offset=4
        local.get $l5
        i32.const 3125352
        i32.store
        local.get $l5
        local.get $l27
        local.get $l12
        f32.mul
        local.get $l15
        local.get $l6
        f32.mul
        f32.sub
        local.get $l16
        local.get $l11
        f32.mul
        f32.sub
        f32.neg
        f32.store offset=84
        local.get $l5
        local.get $l5
        i32.const 168
        i32.add
        i32.store offset=8
        local.get $p0
        i64.load offset=48 align=4
        local.set $l56
        local.get $l5
        local.get $p0
        f32.load offset=56
        f32.store offset=76
        local.get $l5
        local.get $l56
        i64.store offset=68 align=4
        local.get $l5
        i32.const 104
        i32.add
        i32.const 1
        local.get $p1
        local.get $l5
        i32.const 1
        call $f70121
        br $B0
      end
      local.get $l5
      i32.const 104
      i32.add
      local.get $p0
      local.get $p2
      local.get $p3
      call $f69940
      local.get $p3
      f32.load offset=20
      local.set $l6
      local.get $p3
      f32.load offset=24
      local.set $l23
      local.get $p3
      f32.load offset=16
      local.set $l16
      local.get $p0
      f32.load offset=16
      local.set $l15
      local.get $p0
      f32.load offset=20
      local.set $l10
      local.get $p0
      f32.load offset=40
      local.set $l29
      local.get $p0
      f32.load offset=44
      local.set $l19
      local.get $p2
      f32.load offset=20
      local.set $l8
      local.get $p0
      f32.load offset=28
      local.set $l11
      local.get $p2
      f32.load offset=24
      local.set $l13
      local.get $p0
      f32.load offset=32
      local.set $l12
      local.get $p2
      f32.load offset=4
      local.set $l9
      local.get $p2
      f32.load offset=12
      local.set $l28
      local.get $p2
      f32.load
      local.set $l22
      local.get $p2
      f32.load offset=8
      local.set $l7
      local.get $p3
      f32.load offset=8
      local.set $l31
      local.get $p3
      f32.load offset=4
      local.set $l32
      local.get $p3
      f32.load
      local.set $l33
      local.get $p3
      f32.load offset=12
      local.set $l14
      local.get $p0
      f32.load offset=8
      local.set $l17
      local.get $p0
      f32.load
      local.set $l20
      local.get $p0
      f32.load offset=4
      local.set $l21
      local.get $p0
      f32.load offset=12
      local.set $l25
      local.get $p0
      f32.load offset=36
      local.set $l26
      local.get $p2
      f32.load offset=16
      local.set $l24
      local.get $p0
      f32.load offset=24
      local.set $l18
      local.get $l5
      i32.const 0
      i32.store offset=92
      local.get $l5
      i32.const -64
      i32.sub
      local.get $l11
      local.get $l29
      f32.neg
      local.tee $l29
      f32.mul
      local.get $l18
      local.get $l26
      f32.mul
      f32.sub
      local.get $l12
      local.get $l19
      f32.mul
      f32.sub
      local.get $l18
      local.get $l24
      f32.mul
      local.get $l11
      local.get $l8
      f32.mul
      f32.add
      local.get $l12
      local.get $l13
      f32.mul
      f32.add
      f32.add
      f32.store
      local.get $l5
      local.get $l15
      local.get $l29
      f32.mul
      local.get $l25
      local.get $l26
      f32.mul
      f32.sub
      local.get $l10
      local.get $l19
      f32.mul
      f32.sub
      local.get $l25
      local.get $l24
      f32.mul
      local.get $l15
      local.get $l8
      f32.mul
      f32.add
      local.get $l10
      local.get $l13
      f32.mul
      f32.add
      f32.add
      f32.store offset=60
      local.get $l5
      local.get $l21
      local.get $l29
      f32.mul
      local.get $l20
      local.get $l26
      f32.mul
      f32.sub
      local.get $l17
      local.get $l19
      f32.mul
      f32.sub
      local.get $l20
      local.get $l24
      f32.mul
      local.get $l21
      local.get $l8
      f32.mul
      f32.add
      local.get $l17
      local.get $l13
      f32.mul
      f32.add
      f32.add
      f32.store offset=56
      local.get $l5
      local.get $l18
      local.get $l7
      local.get $l22
      local.get $l22
      f32.add
      local.tee $l19
      f32.mul
      local.tee $l47
      local.get $l28
      local.get $l9
      local.get $l9
      f32.add
      local.tee $l24
      f32.mul
      local.tee $l48
      f32.add
      local.tee $l29
      local.get $l6
      local.get $l14
      local.get $l14
      f32.add
      local.tee $l8
      f32.mul
      local.tee $l36
      local.get $l23
      local.get $l16
      local.get $l16
      f32.add
      local.tee $l34
      f32.mul
      local.tee $l30
      f32.add
      local.tee $l13
      local.get $l33
      local.get $l13
      f32.mul
      local.tee $l43
      f32.mul
      local.get $l34
      local.get $l6
      f32.mul
      local.tee $l40
      local.get $l8
      local.get $l23
      f32.mul
      local.tee $l41
      f32.sub
      local.tee $l26
      local.get $l26
      local.get $l32
      f32.mul
      local.tee $l44
      f32.mul
      f32.add
      f32.const 0x1p+0 (;=1;)
      local.get $l14
      local.get $l8
      f32.mul
      f32.sub
      local.tee $l49
      local.get $l16
      local.get $l34
      f32.mul
      local.tee $l37
      f32.sub
      local.tee $l14
      local.get $l14
      local.get $l31
      f32.mul
      local.tee $l34
      f32.mul
      f32.add
      local.tee $l35
      f32.mul
      f32.const 0x1p+0 (;=1;)
      local.get $l9
      local.get $l24
      f32.mul
      local.tee $l50
      f32.sub
      local.get $l7
      local.get $l7
      local.get $l7
      f32.add
      local.tee $l38
      f32.mul
      local.tee $l51
      f32.sub
      local.tee $l45
      local.get $l13
      local.get $l33
      f32.const 0x1p+0 (;=1;)
      local.get $l37
      f32.sub
      local.get $l6
      local.get $l6
      local.get $l6
      f32.add
      local.tee $l39
      f32.mul
      local.tee $l52
      f32.sub
      local.tee $l6
      f32.mul
      local.tee $l37
      f32.mul
      local.get $l26
      local.get $l32
      local.get $l8
      local.get $l16
      f32.mul
      local.tee $l8
      local.get $l39
      local.get $l23
      f32.mul
      local.tee $l53
      f32.add
      local.tee $l16
      f32.mul
      local.tee $l39
      f32.mul
      f32.add
      local.get $l14
      local.get $l31
      local.get $l36
      local.get $l30
      f32.sub
      local.tee $l23
      f32.mul
      local.tee $l36
      f32.mul
      f32.add
      local.tee $l30
      f32.mul
      local.get $l19
      local.get $l9
      f32.mul
      local.tee $l54
      local.get $l38
      local.get $l28
      f32.mul
      local.tee $l55
      f32.sub
      local.tee $l38
      local.get $l13
      local.get $l33
      local.get $l8
      local.get $l53
      f32.sub
      local.tee $l9
      f32.mul
      local.tee $l33
      f32.mul
      local.get $l26
      local.get $l32
      local.get $l49
      local.get $l52
      f32.sub
      local.tee $l8
      f32.mul
      local.tee $l32
      f32.mul
      f32.add
      local.get $l14
      local.get $l31
      local.get $l40
      local.get $l41
      f32.add
      local.tee $l13
      f32.mul
      local.tee $l31
      f32.mul
      f32.add
      local.tee $l14
      f32.mul
      f32.add
      f32.add
      local.tee $l26
      f32.mul
      local.get $l11
      local.get $l24
      local.get $l7
      f32.mul
      local.tee $l40
      local.get $l19
      local.get $l28
      f32.mul
      local.tee $l41
      f32.sub
      local.tee $l7
      local.get $l35
      f32.mul
      local.get $l54
      local.get $l55
      f32.add
      local.tee $l28
      local.get $l30
      f32.mul
      f32.const 0x1p+0 (;=1;)
      local.get $l22
      local.get $l19
      f32.mul
      f32.sub
      local.tee $l24
      local.get $l51
      f32.sub
      local.tee $l19
      local.get $l14
      f32.mul
      f32.add
      f32.add
      local.tee $l22
      f32.mul
      f32.add
      local.get $l12
      local.get $l24
      local.get $l50
      f32.sub
      local.tee $l24
      local.get $l35
      f32.mul
      local.get $l47
      local.get $l48
      f32.sub
      local.tee $l35
      local.get $l30
      f32.mul
      local.get $l40
      local.get $l41
      f32.add
      local.tee $l30
      local.get $l14
      f32.mul
      f32.add
      f32.add
      local.tee $l14
      f32.mul
      f32.add
      f32.store offset=52
      local.get $l5
      local.get $l10
      local.get $l14
      f32.mul
      local.get $l25
      local.get $l26
      f32.mul
      local.get $l15
      local.get $l22
      f32.mul
      f32.add
      f32.add
      f32.store offset=48
      local.get $l5
      local.get $l17
      local.get $l14
      f32.mul
      local.get $l20
      local.get $l26
      f32.mul
      local.get $l21
      local.get $l22
      f32.mul
      f32.add
      f32.add
      f32.store offset=44
      local.get $l5
      local.get $l18
      local.get $l29
      local.get $l9
      local.get $l43
      f32.mul
      local.get $l8
      local.get $l44
      f32.mul
      f32.add
      local.get $l13
      local.get $l34
      f32.mul
      f32.add
      local.tee $l22
      f32.mul
      local.get $l45
      local.get $l9
      local.get $l37
      f32.mul
      local.get $l8
      local.get $l39
      f32.mul
      f32.add
      local.get $l13
      local.get $l36
      f32.mul
      f32.add
      local.tee $l14
      f32.mul
      local.get $l38
      local.get $l9
      local.get $l33
      f32.mul
      local.get $l8
      local.get $l32
      f32.mul
      f32.add
      local.get $l13
      local.get $l31
      f32.mul
      f32.add
      local.tee $l9
      f32.mul
      f32.add
      f32.add
      local.tee $l8
      f32.mul
      local.get $l11
      local.get $l7
      local.get $l22
      f32.mul
      local.get $l28
      local.get $l14
      f32.mul
      local.get $l19
      local.get $l9
      f32.mul
      f32.add
      f32.add
      local.tee $l13
      f32.mul
      f32.add
      local.get $l12
      local.get $l24
      local.get $l22
      f32.mul
      local.get $l35
      local.get $l14
      f32.mul
      local.get $l30
      local.get $l9
      f32.mul
      f32.add
      f32.add
      local.tee $l9
      f32.mul
      f32.add
      f32.store offset=40
      local.get $l5
      local.get $l10
      local.get $l9
      f32.mul
      local.get $l25
      local.get $l8
      f32.mul
      local.get $l15
      local.get $l13
      f32.mul
      f32.add
      f32.add
      f32.store offset=36
      local.get $l5
      local.get $l17
      local.get $l9
      f32.mul
      local.get $l20
      local.get $l8
      f32.mul
      local.get $l21
      local.get $l13
      f32.mul
      f32.add
      f32.add
      f32.store offset=32
      local.get $l5
      local.get $l18
      local.get $l29
      local.get $l6
      local.get $l43
      f32.mul
      local.get $l16
      local.get $l44
      f32.mul
      f32.add
      local.get $l23
      local.get $l34
      f32.mul
      f32.add
      local.tee $l9
      f32.mul
      local.get $l45
      local.get $l6
      local.get $l37
      f32.mul
      local.get $l16
      local.get $l39
      f32.mul
      f32.add
      local.get $l23
      local.get $l36
      f32.mul
      f32.add
      local.tee $l8
      f32.mul
      local.get $l38
      local.get $l6
      local.get $l33
      f32.mul
      local.get $l16
      local.get $l32
      f32.mul
      f32.add
      local.get $l23
      local.get $l31
      f32.mul
      f32.add
      local.tee $l6
      f32.mul
      f32.add
      f32.add
      local.tee $l16
      f32.mul
      local.get $l11
      local.get $l7
      local.get $l9
      f32.mul
      local.get $l28
      local.get $l8
      f32.mul
      local.get $l19
      local.get $l6
      f32.mul
      f32.add
      f32.add
      local.tee $l7
      f32.mul
      f32.add
      local.get $l12
      local.get $l24
      local.get $l9
      f32.mul
      local.get $l35
      local.get $l8
      f32.mul
      local.get $l30
      local.get $l6
      f32.mul
      f32.add
      f32.add
      local.tee $l6
      f32.mul
      f32.add
      f32.store offset=28
      local.get $l5
      local.get $l6
      local.get $l10
      f32.mul
      local.get $l25
      local.get $l16
      f32.mul
      local.get $l15
      local.get $l7
      f32.mul
      f32.add
      f32.add
      f32.store offset=24
      local.get $l5
      local.get $l46
      local.get $l27
      f32.mul
      local.get $l42
      f32.mul
      f32.const 0x0p+0 (;=0;)
      f32.lt
      i32.store8 offset=17
      local.get $l5
      i32.const 0
      i32.store8 offset=16
      local.get $l5
      local.get $p4
      i32.store offset=12
      local.get $l5
      i32.const 2
      i32.store offset=4
      local.get $l5
      i64.const 0
      i64.store offset=84 align=4
      local.get $l5
      i32.const 3125372
      i32.store
      local.get $l5
      local.get $l17
      local.get $l6
      f32.mul
      local.get $l20
      local.get $l16
      f32.mul
      local.get $l21
      local.get $l7
      f32.mul
      f32.add
      f32.add
      f32.store offset=20
      local.get $l5
      local.get $l5
      i32.const 168
      i32.add
      i32.store offset=8
      local.get $p0
      i64.load offset=48 align=4
      local.set $l56
      local.get $l5
      local.get $p0
      f32.load offset=56
      f32.store offset=76
      local.get $l5
      local.get $l56
      i64.store offset=68 align=4
      local.get $l5
      i32.const 104
      i32.add
      i32.const 1
      local.get $p1
      local.get $l5
      i32.const 1
      call $f70121
    end
    local.get $l5
    i32.load8_u offset=16
    local.set $p0
    local.get $l5
    i32.const 208
    i32.add
    global.set $g0
    local.get $p0
    i32.const 255
    i32.and
    i32.const 0
    i32.ne)
