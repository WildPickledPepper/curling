  (func $f70555 (type $t18) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 i32) (param $p7 i32) (result i32)
    (local $l8 i32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32) (local $l33 f32) (local $l34 f32) (local $l35 f32) (local $l36 f32) (local $l37 f32) (local $l38 f32) (local $l39 f32) (local $l40 f32) (local $l41 f32) (local $l42 f32) (local $l43 f32) (local $l44 f32) (local $l45 f32) (local $l46 f32) (local $l47 f32) (local $l48 f32) (local $l49 f32) (local $l50 f32) (local $l51 f32) (local $l52 f32) (local $l53 f32) (local $l54 f32) (local $l55 f32) (local $l56 f32) (local $l57 f32) (local $l58 f32) (local $l59 f32) (local $l60 f32) (local $l61 f32) (local $l62 f32) (local $l63 f32) (local $l64 f32) (local $l65 f32) (local $l66 f32) (local $l67 f32) (local $l68 f32)
    global.get $g0
    i32.const 224
    i32.sub
    local.tee $l8
    global.set $g0
    local.get $p5
    i32.load8_u offset=6
    local.set $p7
    local.get $l8
    local.get $p2
    f32.load offset=4
    local.tee $l10
    local.get $l10
    f32.add
    local.tee $l11
    local.get $p2
    f32.load offset=8
    local.tee $l9
    f32.mul
    local.tee $l18
    local.get $p2
    f32.load
    local.tee $l12
    local.get $l12
    f32.add
    local.tee $l13
    local.get $p2
    f32.load offset=12
    local.tee $l14
    f32.mul
    local.tee $l20
    f32.sub
    local.tee $l30
    f32.store offset=76
    local.get $l8
    local.get $l18
    local.get $l20
    f32.add
    local.tee $l18
    f32.store offset=68
    local.get $l8
    f32.const 0x1p+0 (;=1;)
    local.get $l12
    local.get $l13
    f32.mul
    f32.sub
    local.tee $l12
    local.get $l10
    local.get $l11
    f32.mul
    local.tee $l15
    f32.sub
    local.tee $l31
    f32.store offset=80
    local.get $l8
    i32.const -64
    i32.sub
    local.get $l12
    local.get $l9
    local.get $l9
    local.get $l9
    f32.add
    local.tee $l21
    f32.mul
    local.tee $l17
    f32.sub
    local.tee $l20
    f32.store
    local.get $l8
    local.get $l13
    local.get $l9
    f32.mul
    local.tee $l9
    local.get $l11
    local.get $l14
    f32.mul
    local.tee $l11
    f32.add
    local.tee $l32
    f32.store offset=72
    local.get $l8
    local.get $l13
    local.get $l10
    f32.mul
    local.tee $l10
    local.get $l21
    local.get $l14
    f32.mul
    local.tee $l13
    f32.sub
    local.tee $l21
    f32.store offset=60
    local.get $l8
    local.get $l9
    local.get $l11
    f32.sub
    local.tee $l9
    f32.store offset=56
    local.get $l8
    local.get $l10
    local.get $l13
    f32.add
    local.tee $l10
    f32.store offset=52
    local.get $l8
    f32.const 0x1p+0 (;=1;)
    local.get $l15
    f32.sub
    local.get $l17
    f32.sub
    local.tee $l13
    f32.store offset=48
    local.get $l8
    local.get $p2
    f32.load offset=16
    local.tee $l36
    f32.store offset=84
    local.get $l8
    local.get $p2
    f32.load offset=20
    local.tee $l37
    f32.store offset=88
    local.get $l8
    local.get $p2
    f32.load offset=24
    local.tee $l38
    f32.store offset=92
    local.get $l8
    local.get $p3
    f32.load offset=4
    local.tee $l12
    local.get $l12
    f32.add
    local.tee $l15
    local.get $p3
    f32.load offset=8
    local.tee $l11
    f32.mul
    local.tee $l17
    local.get $p3
    f32.load
    local.tee $l16
    local.get $l16
    f32.add
    local.tee $l14
    local.get $p3
    f32.load offset=12
    local.tee $l19
    f32.mul
    local.tee $l29
    f32.sub
    local.tee $l34
    f32.store offset=28
    local.get $l8
    local.get $l17
    local.get $l29
    f32.add
    local.tee $l17
    f32.store offset=20
    local.get $l8
    f32.const 0x1p+0 (;=1;)
    local.get $l16
    local.get $l14
    f32.mul
    f32.sub
    local.tee $l16
    local.get $l12
    local.get $l15
    f32.mul
    local.tee $l33
    f32.sub
    local.tee $l29
    f32.store offset=32
    local.get $l8
    local.get $l16
    local.get $l11
    local.get $l11
    local.get $l11
    f32.add
    local.tee $l22
    f32.mul
    local.tee $l39
    f32.sub
    local.tee $l16
    f32.store offset=16
    local.get $l8
    local.get $l14
    local.get $l11
    f32.mul
    local.tee $l11
    local.get $l15
    local.get $l19
    f32.mul
    local.tee $l15
    f32.add
    local.tee $l35
    f32.store offset=24
    local.get $l8
    local.get $l14
    local.get $l12
    f32.mul
    local.tee $l14
    local.get $l22
    local.get $l19
    f32.mul
    local.tee $l22
    f32.sub
    local.tee $l19
    f32.store offset=12
    local.get $l8
    local.get $l11
    local.get $l15
    f32.sub
    local.tee $l12
    f32.store offset=8
    local.get $l8
    local.get $l14
    local.get $l22
    f32.add
    local.tee $l14
    f32.store offset=4
    local.get $l8
    f32.const 0x1p+0 (;=1;)
    local.get $l33
    f32.sub
    local.get $l39
    f32.sub
    local.tee $l15
    f32.store
    local.get $l8
    local.get $p3
    f32.load offset=16
    local.tee $l40
    f32.store offset=36
    local.get $l8
    local.get $p3
    f32.load offset=20
    local.tee $l41
    f32.store offset=40
    local.get $l8
    local.get $p3
    f32.load offset=24
    local.tee $l42
    f32.store offset=44
    local.get $p4
    f32.load
    local.set $l11
    local.get $l8
    local.get $l13
    local.get $l40
    local.get $l36
    f32.sub
    local.tee $l33
    f32.mul
    local.get $l10
    local.get $l41
    local.get $l37
    f32.sub
    local.tee $l22
    f32.mul
    f32.add
    local.get $l9
    local.get $l42
    local.get $l38
    f32.sub
    local.tee $l39
    f32.mul
    f32.add
    local.tee $l43
    f32.store offset=192
    local.get $l8
    local.get $l11
    local.get $p0
    f32.load offset=4
    local.tee $l23
    local.get $l9
    local.get $l12
    f32.mul
    local.get $l13
    local.get $l15
    f32.mul
    local.get $l10
    local.get $l14
    f32.mul
    f32.add
    f32.add
    local.tee $l60
    f32.abs
    f32.const 0x1.0c6f7ap-20 (;=1e-06;)
    f32.add
    local.tee $l48
    local.get $p1
    f32.load offset=4
    local.tee $l24
    f32.mul
    f32.add
    local.get $l9
    local.get $l17
    f32.mul
    local.get $l13
    local.get $l19
    f32.mul
    local.get $l10
    local.get $l16
    f32.mul
    f32.add
    f32.add
    local.tee $l61
    f32.abs
    f32.const 0x1.0c6f7ap-20 (;=1e-06;)
    f32.add
    local.tee $l49
    local.get $p1
    f32.load offset=8
    local.tee $l25
    f32.mul
    f32.add
    local.get $l9
    local.get $l29
    f32.mul
    local.get $l13
    local.get $l35
    f32.mul
    local.get $l10
    local.get $l34
    f32.mul
    f32.add
    f32.add
    local.tee $l62
    f32.abs
    f32.const 0x1.0c6f7ap-20 (;=1e-06;)
    f32.add
    local.tee $l50
    local.get $p1
    f32.load offset=12
    local.tee $l26
    f32.mul
    f32.add
    local.get $l43
    f32.abs
    f32.sub
    f32.add
    local.tee $l51
    f32.store offset=160
    block $B0 (result i32)
      i32.const 1
      local.get $l51
      i32.reinterpret_f32
      i32.const 0
      i32.lt_s
      br_if $B0
      drop
      local.get $l8
      local.get $l21
      local.get $l33
      f32.mul
      local.get $l20
      local.get $l22
      f32.mul
      f32.add
      local.get $l18
      local.get $l39
      f32.mul
      f32.add
      local.tee $l44
      f32.store offset=196
      local.get $l8
      local.get $l11
      local.get $l18
      local.get $l29
      f32.mul
      local.get $l21
      local.get $l35
      f32.mul
      local.get $l20
      local.get $l34
      f32.mul
      f32.add
      f32.add
      local.tee $l63
      f32.abs
      f32.const 0x1.0c6f7ap-20 (;=1e-06;)
      f32.add
      local.tee $l52
      local.get $l26
      f32.mul
      local.get $l18
      local.get $l17
      f32.mul
      local.get $l21
      local.get $l19
      f32.mul
      local.get $l20
      local.get $l16
      f32.mul
      f32.add
      f32.add
      local.tee $l64
      f32.abs
      f32.const 0x1.0c6f7ap-20 (;=1e-06;)
      f32.add
      local.tee $l53
      local.get $l25
      f32.mul
      local.get $l18
      local.get $l12
      f32.mul
      local.get $l21
      local.get $l15
      f32.mul
      local.get $l20
      local.get $l14
      f32.mul
      f32.add
      f32.add
      local.tee $l65
      f32.abs
      f32.const 0x1.0c6f7ap-20 (;=1e-06;)
      f32.add
      local.tee $l54
      local.get $l24
      f32.mul
      local.get $p0
      f32.load offset=8
      local.tee $l27
      f32.add
      f32.add
      f32.add
      local.get $l44
      f32.abs
      f32.sub
      f32.add
      local.tee $l55
      f32.store offset=164
      i32.const 1
      local.get $l55
      i32.reinterpret_f32
      i32.const 0
      i32.lt_s
      br_if $B0
      drop
      local.get $l8
      local.get $l32
      local.get $l33
      f32.mul
      local.get $l30
      local.get $l22
      f32.mul
      f32.add
      local.get $l31
      local.get $l39
      f32.mul
      f32.add
      local.tee $l45
      f32.store offset=200
      local.get $l8
      local.get $l11
      local.get $l31
      local.get $l29
      f32.mul
      local.get $l32
      local.get $l35
      f32.mul
      local.get $l30
      local.get $l34
      f32.mul
      f32.add
      f32.add
      local.tee $l66
      f32.abs
      f32.const 0x1.0c6f7ap-20 (;=1e-06;)
      f32.add
      local.tee $l56
      local.get $l26
      f32.mul
      local.get $l31
      local.get $l17
      f32.mul
      local.get $l32
      local.get $l19
      f32.mul
      local.get $l30
      local.get $l16
      f32.mul
      f32.add
      f32.add
      local.tee $l67
      f32.abs
      f32.const 0x1.0c6f7ap-20 (;=1e-06;)
      f32.add
      local.tee $l57
      local.get $l25
      f32.mul
      local.get $l31
      local.get $l12
      f32.mul
      local.get $l32
      local.get $l15
      f32.mul
      local.get $l30
      local.get $l14
      f32.mul
      f32.add
      f32.add
      local.tee $l68
      f32.abs
      f32.const 0x1.0c6f7ap-20 (;=1e-06;)
      f32.add
      local.tee $l58
      local.get $l24
      f32.mul
      local.get $p0
      f32.load offset=12
      local.tee $l28
      f32.add
      f32.add
      f32.add
      local.get $l45
      f32.abs
      f32.sub
      f32.add
      local.tee $l59
      f32.store offset=168
      i32.const 1
      local.get $l59
      i32.reinterpret_f32
      i32.const 0
      i32.lt_s
      br_if $B0
      drop
      local.get $l8
      local.get $l15
      local.get $l33
      f32.mul
      local.get $l14
      local.get $l22
      f32.mul
      f32.add
      local.get $l12
      local.get $l39
      f32.mul
      f32.add
      local.tee $l46
      f32.store offset=204
      local.get $l8
      local.get $l11
      local.get $l24
      local.get $l48
      local.get $l23
      f32.mul
      f32.add
      local.get $l54
      local.get $l27
      f32.mul
      f32.add
      local.get $l58
      local.get $l28
      f32.mul
      f32.add
      local.get $l46
      f32.abs
      f32.sub
      f32.add
      local.tee $l46
      f32.store offset=172
      i32.const 1
      local.get $l46
      i32.reinterpret_f32
      i32.const 0
      i32.lt_s
      br_if $B0
      drop
      local.get $l8
      local.get $l19
      local.get $l33
      f32.mul
      local.get $l16
      local.get $l22
      f32.mul
      f32.add
      local.get $l17
      local.get $l39
      f32.mul
      f32.add
      local.tee $l47
      f32.store offset=208
      local.get $l8
      local.get $l11
      local.get $l49
      local.get $l23
      f32.mul
      local.get $l25
      f32.add
      local.get $l53
      local.get $l27
      f32.mul
      f32.add
      local.get $l57
      local.get $l28
      f32.mul
      f32.add
      local.get $l47
      f32.abs
      f32.sub
      f32.add
      local.tee $l47
      f32.store offset=176
      i32.const 1
      local.get $l47
      i32.reinterpret_f32
      i32.const 0
      i32.lt_s
      br_if $B0
      drop
      local.get $l8
      local.get $l35
      local.get $l33
      f32.mul
      local.get $l34
      local.get $l22
      f32.mul
      f32.add
      local.get $l29
      local.get $l39
      f32.mul
      f32.add
      local.tee $l33
      f32.store offset=212
      local.get $l8
      local.get $l11
      local.get $l50
      local.get $l23
      f32.mul
      local.get $l26
      f32.add
      local.get $l52
      local.get $l27
      f32.mul
      f32.add
      local.get $l56
      local.get $l28
      f32.mul
      f32.add
      local.get $l33
      f32.abs
      f32.sub
      f32.add
      local.tee $l33
      f32.store offset=180
      i32.const 1
      local.get $l33
      i32.reinterpret_f32
      i32.const 0
      i32.lt_s
      br_if $B0
      drop
      block $B1
        block $B2
          local.get $p7
          i32.eqz
          if $I3
            local.get $l65
            local.get $l45
            f32.mul
            local.get $l68
            local.get $l44
            f32.mul
            f32.sub
            f32.abs
            local.get $l49
            local.get $l26
            f32.mul
            local.get $l50
            local.get $l25
            f32.mul
            local.get $l11
            local.get $l58
            local.get $l27
            f32.mul
            f32.add
            local.get $l54
            local.get $l28
            f32.mul
            f32.add
            f32.add
            f32.add
            f32.gt
            br_if $B1
            local.get $l64
            local.get $l45
            f32.mul
            local.get $l67
            local.get $l44
            f32.mul
            f32.sub
            f32.abs
            local.get $l48
            local.get $l26
            f32.mul
            local.get $l50
            local.get $l24
            f32.mul
            local.get $l11
            local.get $l57
            local.get $l27
            f32.mul
            f32.add
            local.get $l53
            local.get $l28
            f32.mul
            f32.add
            f32.add
            f32.add
            f32.gt
            br_if $B1
            local.get $l63
            local.get $l45
            f32.mul
            local.get $l66
            local.get $l44
            f32.mul
            f32.sub
            f32.abs
            local.get $l48
            local.get $l25
            f32.mul
            local.get $l49
            local.get $l24
            f32.mul
            local.get $l11
            local.get $l56
            local.get $l27
            f32.mul
            f32.add
            local.get $l52
            local.get $l28
            f32.mul
            f32.add
            f32.add
            f32.add
            f32.gt
            br_if $B1
            local.get $l68
            local.get $l43
            f32.mul
            local.get $l60
            local.get $l45
            f32.mul
            f32.sub
            f32.abs
            local.get $l53
            local.get $l26
            f32.mul
            local.get $l52
            local.get $l25
            f32.mul
            local.get $l11
            local.get $l58
            local.get $l23
            f32.mul
            f32.add
            local.get $l48
            local.get $l28
            f32.mul
            f32.add
            f32.add
            f32.add
            f32.gt
            br_if $B1
            local.get $l67
            local.get $l43
            f32.mul
            local.get $l61
            local.get $l45
            f32.mul
            f32.sub
            f32.abs
            local.get $l54
            local.get $l26
            f32.mul
            local.get $l52
            local.get $l24
            f32.mul
            local.get $l11
            local.get $l57
            local.get $l23
            f32.mul
            f32.add
            local.get $l49
            local.get $l28
            f32.mul
            f32.add
            f32.add
            f32.add
            f32.gt
            br_if $B1
            local.get $l66
            local.get $l43
            f32.mul
            local.get $l62
            local.get $l45
            f32.mul
            f32.sub
            f32.abs
            local.get $l54
            local.get $l25
            f32.mul
            local.get $l53
            local.get $l24
            f32.mul
            local.get $l11
            local.get $l56
            local.get $l23
            f32.mul
            f32.add
            local.get $l50
            local.get $l28
            f32.mul
            f32.add
            f32.add
            f32.add
            f32.gt
            br_if $B1
            local.get $l60
            local.get $l44
            f32.mul
            local.get $l65
            local.get $l43
            f32.mul
            f32.sub
            f32.abs
            local.get $l57
            local.get $l26
            f32.mul
            local.get $l56
            local.get $l25
            f32.mul
            local.get $l11
            local.get $l54
            local.get $l23
            f32.mul
            f32.add
            local.get $l48
            local.get $l27
            f32.mul
            f32.add
            f32.add
            f32.add
            f32.gt
            br_if $B1
            local.get $l61
            local.get $l44
            f32.mul
            local.get $l64
            local.get $l43
            f32.mul
            f32.sub
            f32.abs
            local.get $l58
            local.get $l26
            f32.mul
            local.get $l56
            local.get $l24
            f32.mul
            local.get $l11
            local.get $l53
            local.get $l23
            f32.mul
            f32.add
            local.get $l49
            local.get $l27
            f32.mul
            f32.add
            f32.add
            f32.add
            f32.gt
            br_if $B1
            local.get $l62
            local.get $l44
            f32.mul
            local.get $l63
            local.get $l43
            f32.mul
            f32.sub
            f32.abs
            local.get $l58
            local.get $l25
            f32.mul
            local.get $l57
            local.get $l24
            f32.mul
            local.get $l11
            local.get $l52
            local.get $l23
            f32.mul
            f32.add
            local.get $l50
            local.get $l27
            f32.mul
            f32.add
            f32.add
            f32.add
            f32.gt
            br_if $B1
            br $B2
          end
          local.get $p7
          i32.const 2
          i32.shl
          local.get $l8
          i32.add
          i32.const 156
          i32.add
          local.tee $p3
          local.get $p3
          f32.load
          f32.const 0x1.ff7ceep-1 (;=0.999;)
          f32.mul
          f32.store
          local.get $l8
          f32.load offset=180
          local.set $l33
          local.get $l8
          f32.load offset=176
          local.set $l47
          local.get $l8
          f32.load offset=172
          local.set $l46
          local.get $l8
          f32.load offset=168
          local.set $l59
          local.get $l8
          f32.load offset=164
          local.set $l55
          local.get $l8
          f32.load offset=160
          local.set $l51
        end
        local.get $p1
        i32.const 4
        i32.add
        local.set $p4
        local.get $p0
        i32.const 4
        i32.add
        local.set $p0
        i32.const 5
        i32.const 4
        i32.const 3
        i32.const 2
        local.get $l55
        local.get $l51
        f32.const 0x1.fffffep+127 (;=3.40282e+38;)
        local.get $l51
        f32.const 0x1.fffffep+127 (;=3.40282e+38;)
        f32.lt
        select
        f32.const 0x1.fffffep+127 (;=3.40282e+38;)
        local.get $l51
        f32.const 0x0p+0 (;=0;)
        f32.ge
        select
        local.tee $l22
        f32.lt
        local.get $l55
        f32.const 0x0p+0 (;=0;)
        f32.ge
        i32.and
        local.tee $p3
        local.get $l59
        local.get $l55
        local.get $l22
        local.get $p3
        select
        local.tee $l22
        f32.lt
        local.get $l59
        f32.const 0x0p+0 (;=0;)
        f32.ge
        i32.and
        local.tee $p3
        select
        local.get $l46
        local.get $l59
        local.get $l22
        local.get $p3
        select
        local.tee $l22
        f32.lt
        local.get $l46
        f32.const 0x0p+0 (;=0;)
        f32.ge
        i32.and
        local.tee $p3
        select
        local.get $l47
        local.get $l46
        local.get $l22
        local.get $p3
        select
        local.tee $l22
        f32.lt
        local.get $l47
        f32.const 0x0p+0 (;=0;)
        f32.ge
        i32.and
        local.tee $p3
        select
        local.tee $p2
        local.get $l33
        local.get $l47
        local.get $l22
        local.get $p3
        select
        f32.lt
        select
        local.get $p2
        local.get $l33
        f32.const 0x0p+0 (;=0;)
        f32.ge
        select
        local.tee $p3
        i32.const 1
        i32.add
        local.set $p7
        local.get $l8
        i32.const 192
        i32.add
        local.get $p3
        i32.const 2
        i32.shl
        i32.add
        i32.load
        i32.const -2147483648
        i32.and
        local.set $p1
        i32.const 0
        local.set $p2
        block $B4
          block $B5
            block $B6
              block $B7
                block $B8
                  block $B9
                    block $B10
                      local.get $p3
                      br_table $B10 $B9 $B8 $B7 $B6 $B5 $B4
                    end
                    block $B11
                      local.get $p1
                      if $I12
                        local.get $l8
                        local.get $l9
                        f32.store offset=104
                        local.get $l38
                        local.get $l9
                        local.get $l23
                        f32.mul
                        f32.sub
                        local.set $l12
                        local.get $l8
                        local.get $l10
                        f32.store offset=100
                        local.get $l37
                        local.get $l10
                        local.get $l23
                        f32.mul
                        f32.sub
                        local.set $l14
                        local.get $l8
                        local.get $l13
                        f32.store offset=96
                        local.get $l36
                        local.get $l13
                        local.get $l23
                        f32.mul
                        f32.sub
                        local.set $l15
                        br $B11
                      end
                      local.get $l8
                      local.get $l9
                      f32.neg
                      local.tee $l17
                      f32.store offset=104
                      local.get $l8
                      local.get $l10
                      f32.neg
                      local.tee $l16
                      f32.store offset=100
                      local.get $l8
                      local.get $l13
                      f32.neg
                      local.tee $l19
                      f32.store offset=96
                      local.get $l38
                      local.get $l9
                      local.get $l23
                      f32.mul
                      f32.add
                      local.set $l12
                      local.get $l37
                      local.get $l10
                      local.get $l23
                      f32.mul
                      f32.add
                      local.set $l14
                      local.get $l36
                      local.get $l13
                      local.get $l23
                      f32.mul
                      f32.add
                      local.set $l15
                      local.get $l18
                      f32.neg
                      local.set $l18
                      local.get $l20
                      f32.neg
                      local.set $l20
                      local.get $l21
                      f32.neg
                      local.set $l21
                      local.get $l19
                      local.set $l13
                      local.get $l16
                      local.set $l10
                      local.get $l17
                      local.set $l9
                    end
                    local.get $l8
                    local.get $l12
                    f32.store offset=156
                    local.get $l8
                    local.get $l14
                    f32.store offset=152
                    local.get $l8
                    local.get $l31
                    f32.store offset=144
                    local.get $l8
                    local.get $l30
                    f32.store offset=140
                    local.get $l8
                    local.get $l18
                    f32.store offset=132
                    local.get $l8
                    local.get $l20
                    f32.store offset=128
                    local.get $l8
                    local.get $l15
                    f32.store offset=148
                    local.get $l8
                    local.get $l32
                    f32.store offset=136
                    local.get $l8
                    local.get $l21
                    f32.store offset=124
                    local.get $l8
                    local.get $l9
                    f32.store offset=120
                    local.get $l8
                    local.get $l10
                    f32.store offset=116
                    local.get $l8
                    local.get $l13
                    f32.store offset=112
                    local.get $p6
                    local.get $l8
                    i32.const 96
                    i32.add
                    local.get $l27
                    local.get $l28
                    local.get $p4
                    local.get $l8
                    i32.const 112
                    i32.add
                    local.get $l8
                    local.get $l11
                    call $f70165
                    local.set $p2
                    br $B4
                  end
                  local.get $l8
                  local.get $l9
                  f32.store offset=144
                  local.get $l8
                  local.get $l10
                  f32.store offset=140
                  local.get $l8
                  local.get $l13
                  f32.store offset=136
                  block $B13
                    local.get $p1
                    if $I14
                      local.get $l38
                      local.get $l18
                      local.get $l27
                      f32.mul
                      f32.sub
                      local.set $l9
                      local.get $l37
                      local.get $l20
                      local.get $l27
                      f32.mul
                      f32.sub
                      local.set $l10
                      local.get $l36
                      local.get $l21
                      local.get $l27
                      f32.mul
                      f32.sub
                      local.set $l13
                      br $B13
                    end
                    local.get $l38
                    local.get $l18
                    local.get $l27
                    f32.mul
                    f32.add
                    local.set $l9
                    local.get $l37
                    local.get $l20
                    local.get $l27
                    f32.mul
                    f32.add
                    local.set $l10
                    local.get $l36
                    local.get $l21
                    local.get $l27
                    f32.mul
                    f32.add
                    local.set $l13
                    local.get $l31
                    f32.neg
                    local.set $l31
                    local.get $l30
                    f32.neg
                    local.set $l30
                    local.get $l32
                    f32.neg
                    local.set $l32
                    local.get $l18
                    f32.neg
                    local.set $l18
                    local.get $l20
                    f32.neg
                    local.set $l20
                    local.get $l21
                    f32.neg
                    local.set $l21
                  end
                  local.get $l8
                  local.get $l9
                  f32.store offset=156
                  local.get $l8
                  local.get $l10
                  f32.store offset=152
                  local.get $l8
                  local.get $l31
                  f32.store offset=132
                  local.get $l8
                  local.get $l30
                  f32.store offset=128
                  local.get $l8
                  local.get $l18
                  f32.store offset=104
                  local.get $l8
                  local.get $l20
                  f32.store offset=100
                  local.get $l8
                  local.get $l21
                  f32.store offset=96
                  local.get $l8
                  local.get $l13
                  f32.store offset=148
                  local.get $l8
                  local.get $l32
                  f32.store offset=124
                  local.get $l8
                  local.get $l18
                  f32.store offset=120
                  local.get $l8
                  local.get $l20
                  f32.store offset=116
                  local.get $l8
                  local.get $l21
                  f32.store offset=112
                  local.get $p6
                  local.get $l8
                  i32.const 96
                  i32.add
                  local.get $l28
                  local.get $l23
                  local.get $p4
                  local.get $l8
                  i32.const 112
                  i32.add
                  local.get $l8
                  local.get $l11
                  call $f70165
                  local.set $p2
                  br $B4
                end
                local.get $l8
                local.get $l18
                f32.store offset=144
                local.get $l8
                local.get $l20
                f32.store offset=140
                local.get $l8
                local.get $l21
                f32.store offset=136
                block $B15
                  local.get $p1
                  if $I16
                    local.get $l38
                    local.get $l31
                    local.get $l28
                    f32.mul
                    f32.sub
                    local.set $l12
                    local.get $l37
                    local.get $l30
                    local.get $l28
                    f32.mul
                    f32.sub
                    local.set $l14
                    local.get $l36
                    local.get $l32
                    local.get $l28
                    f32.mul
                    f32.sub
                    local.set $l18
                    br $B15
                  end
                  local.get $l38
                  local.get $l31
                  local.get $l28
                  f32.mul
                  f32.add
                  local.set $l12
                  local.get $l37
                  local.get $l30
                  local.get $l28
                  f32.mul
                  f32.add
                  local.set $l14
                  local.get $l36
                  local.get $l32
                  local.get $l28
                  f32.mul
                  f32.add
                  local.set $l18
                  local.get $l9
                  f32.neg
                  local.set $l9
                  local.get $l10
                  f32.neg
                  local.set $l10
                  local.get $l13
                  f32.neg
                  local.set $l13
                  local.get $l31
                  f32.neg
                  local.set $l31
                  local.get $l30
                  f32.neg
                  local.set $l30
                  local.get $l32
                  f32.neg
                  local.set $l32
                end
                local.get $l8
                local.get $l12
                f32.store offset=156
                local.get $l8
                local.get $l14
                f32.store offset=152
                local.get $l8
                local.get $l9
                f32.store offset=132
                local.get $l8
                local.get $l10
                f32.store offset=128
                local.get $l8
                local.get $l31
                f32.store offset=104
                local.get $l8
                local.get $l30
                f32.store offset=100
                local.get $l8
                local.get $l32
                f32.store offset=96
                local.get $l8
                local.get $l18
                f32.store offset=148
                local.get $l8
                local.get $l13
                f32.store offset=124
                local.get $l8
                local.get $l31
                f32.store offset=120
                local.get $l8
                local.get $l30
                f32.store offset=116
                local.get $l8
                local.get $l32
                f32.store offset=112
                local.get $p6
                local.get $l8
                i32.const 96
                i32.add
                local.get $l23
                local.get $l27
                local.get $p4
                local.get $l8
                i32.const 112
                i32.add
                local.get $l8
                local.get $l11
                call $f70165
                local.set $p2
                br $B4
              end
              block $B17 (result f32)
                local.get $p1
                if $I18
                  local.get $l8
                  local.get $l15
                  f32.store offset=96
                  local.get $l8
                  local.get $l15
                  f32.neg
                  f32.store offset=112
                  local.get $l8
                  local.get $l12
                  f32.store offset=104
                  local.get $l42
                  local.get $l12
                  local.get $l24
                  f32.mul
                  f32.add
                  local.set $l9
                  local.get $l8
                  local.get $l14
                  f32.store offset=100
                  local.get $l41
                  local.get $l14
                  local.get $l24
                  f32.mul
                  f32.add
                  local.set $l10
                  local.get $l17
                  f32.neg
                  local.set $l17
                  local.get $l16
                  f32.neg
                  local.set $l16
                  local.get $l19
                  f32.neg
                  local.set $l19
                  local.get $l12
                  f32.neg
                  local.set $l12
                  local.get $l14
                  f32.neg
                  local.set $l14
                  local.get $l40
                  local.get $l15
                  local.get $l24
                  f32.mul
                  f32.add
                  br $B17
                end
                local.get $l8
                local.get $l12
                f32.neg
                f32.store offset=104
                local.get $l8
                local.get $l14
                f32.neg
                f32.store offset=100
                local.get $l8
                local.get $l15
                f32.store offset=112
                local.get $l8
                local.get $l15
                f32.neg
                f32.store offset=96
                local.get $l42
                local.get $l12
                local.get $l24
                f32.mul
                f32.sub
                local.set $l9
                local.get $l41
                local.get $l14
                local.get $l24
                f32.mul
                f32.sub
                local.set $l10
                local.get $l40
                local.get $l15
                local.get $l24
                f32.mul
                f32.sub
              end
              local.set $l13
              local.get $l8
              local.get $l9
              f32.store offset=156
              local.get $l8
              local.get $l10
              f32.store offset=152
              local.get $l8
              local.get $l29
              f32.store offset=144
              local.get $l8
              local.get $l34
              f32.store offset=140
              local.get $l8
              local.get $l17
              f32.store offset=132
              local.get $l8
              local.get $l16
              f32.store offset=128
              local.get $l8
              local.get $l13
              f32.store offset=148
              local.get $l8
              local.get $l35
              f32.store offset=136
              local.get $l8
              local.get $l19
              f32.store offset=124
              local.get $l8
              local.get $l12
              f32.store offset=120
              local.get $l8
              local.get $l14
              f32.store offset=116
              local.get $p6
              local.get $l8
              i32.const 96
              i32.add
              local.get $l25
              local.get $l26
              local.get $p0
              local.get $l8
              i32.const 112
              i32.add
              local.get $l8
              i32.const 48
              i32.add
              local.get $l11
              call $f70165
              local.set $p2
              br $B4
            end
            local.get $l8
            local.get $l12
            f32.store offset=144
            local.get $l8
            local.get $l14
            f32.store offset=140
            local.get $l8
            local.get $l15
            f32.store offset=136
            block $B19 (result f32)
              local.get $p1
              if $I20
                local.get $l8
                local.get $l35
                f32.neg
                f32.store offset=124
                local.get $l8
                local.get $l17
                f32.store offset=104
                local.get $l8
                local.get $l17
                f32.neg
                f32.store offset=120
                local.get $l8
                local.get $l16
                f32.store offset=100
                local.get $l8
                local.get $l16
                f32.neg
                f32.store offset=116
                local.get $l8
                local.get $l19
                f32.store offset=96
                local.get $l8
                local.get $l19
                f32.neg
                f32.store offset=112
                local.get $l42
                local.get $l17
                local.get $l25
                f32.mul
                f32.add
                local.set $l9
                local.get $l41
                local.get $l16
                local.get $l25
                f32.mul
                f32.add
                local.set $l10
                local.get $l29
                f32.neg
                local.set $l29
                local.get $l34
                f32.neg
                local.set $l34
                local.get $l40
                local.get $l19
                local.get $l25
                f32.mul
                f32.add
                br $B19
              end
              local.get $l8
              local.get $l12
              f32.store offset=144
              local.get $l8
              local.get $l14
              f32.store offset=140
              local.get $l8
              local.get $l15
              f32.store offset=136
              local.get $l8
              local.get $l35
              f32.store offset=124
              local.get $l8
              local.get $l17
              f32.store offset=120
              local.get $l8
              local.get $l17
              f32.neg
              f32.store offset=104
              local.get $l8
              local.get $l16
              f32.store offset=116
              local.get $l8
              local.get $l16
              f32.neg
              f32.store offset=100
              local.get $l8
              local.get $l19
              f32.store offset=112
              local.get $l8
              local.get $l19
              f32.neg
              f32.store offset=96
              local.get $l42
              local.get $l17
              local.get $l25
              f32.mul
              f32.sub
              local.set $l9
              local.get $l41
              local.get $l16
              local.get $l25
              f32.mul
              f32.sub
              local.set $l10
              local.get $l40
              local.get $l19
              local.get $l25
              f32.mul
              f32.sub
            end
            local.set $l13
            local.get $l8
            local.get $l9
            f32.store offset=156
            local.get $l8
            local.get $l10
            f32.store offset=152
            local.get $l8
            local.get $l29
            f32.store offset=132
            local.get $l8
            local.get $l34
            f32.store offset=128
            local.get $l8
            local.get $l13
            f32.store offset=148
            local.get $p6
            local.get $l8
            i32.const 96
            i32.add
            local.get $l26
            local.get $l24
            local.get $p0
            local.get $l8
            i32.const 112
            i32.add
            local.get $l8
            i32.const 48
            i32.add
            local.get $l11
            call $f70165
            local.set $p2
            br $B4
          end
          local.get $l8
          local.get $l17
          f32.store offset=144
          local.get $l8
          local.get $l16
          f32.store offset=140
          local.get $l8
          local.get $l19
          f32.store offset=136
          local.get $l29
          f32.neg
          local.set $l9
          local.get $l34
          f32.neg
          local.set $l10
          local.get $l35
          f32.neg
          local.set $l13
          block $B21 (result f32)
            local.get $p1
            if $I22
              local.get $l42
              local.get $l29
              local.get $l26
              f32.mul
              f32.add
              local.set $l18
              local.get $l41
              local.get $l34
              local.get $l26
              f32.mul
              f32.add
              local.set $l20
              local.get $l12
              f32.neg
              local.set $l12
              local.get $l14
              f32.neg
              local.set $l14
              local.get $l15
              f32.neg
              local.set $l15
              local.get $l34
              local.set $l16
              local.get $l29
              local.set $l19
              local.get $l40
              local.get $l35
              local.tee $l17
              local.get $l26
              f32.mul
              f32.add
              br $B21
            end
            local.get $l42
            local.get $l29
            local.get $l26
            f32.mul
            f32.sub
            local.set $l18
            local.get $l41
            local.get $l34
            local.get $l26
            f32.mul
            f32.sub
            local.set $l20
            local.get $l13
            local.set $l17
            local.get $l10
            local.set $l16
            local.get $l9
            local.set $l19
            local.get $l34
            local.set $l10
            local.get $l29
            local.set $l9
            local.get $l40
            local.get $l35
            local.tee $l13
            local.get $l26
            f32.mul
            f32.sub
          end
          local.set $l21
          local.get $l8
          local.get $l18
          f32.store offset=156
          local.get $l8
          local.get $l20
          f32.store offset=152
          local.get $l8
          local.get $l12
          f32.store offset=132
          local.get $l8
          local.get $l14
          f32.store offset=128
          local.get $l8
          local.get $l19
          f32.store offset=104
          local.get $l8
          local.get $l16
          f32.store offset=100
          local.get $l8
          local.get $l17
          f32.store offset=96
          local.get $l8
          local.get $l21
          f32.store offset=148
          local.get $l8
          local.get $l15
          f32.store offset=124
          local.get $l8
          local.get $l9
          f32.store offset=120
          local.get $l8
          local.get $l10
          f32.store offset=116
          local.get $l8
          local.get $l13
          f32.store offset=112
          local.get $p6
          local.get $l8
          i32.const 96
          i32.add
          local.get $l24
          local.get $l25
          local.get $p0
          local.get $l8
          i32.const 112
          i32.add
          local.get $l8
          i32.const 48
          i32.add
          local.get $l11
          call $f70165
          local.set $p2
        end
        local.get $p2
        i32.eqz
        br $B0
      end
      i32.const 0
      local.set $p7
      i32.const 1
    end
    local.set $p3
    local.get $p5
    i32.const 0
    local.get $p7
    local.get $p3
    select
    i32.store8 offset=6
    local.get $l8
    i32.const 224
    i32.add
    global.set $g0
    local.get $p3
    i32.const 1
    i32.xor)
