  (func $f70936 (type $t441) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 f32) (param $p4 f32) (param $p5 f32) (param $p6 f32) (param $p7 f32) (param $p8 i32)
    (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 i32) (local $l17 i32) (local $l18 i32) (local $l19 i32) (local $l20 i32) (local $l21 i32) (local $l22 i32) (local $l23 i32) (local $l24 i32) (local $l25 i32) (local $l26 i32) (local $l27 i32) (local $l28 i32) (local $l29 i32) (local $l30 i32) (local $l31 i32) (local $l32 i32) (local $l33 i32) (local $l34 i32) (local $l35 f32) (local $l36 f32) (local $l37 f32) (local $l38 f32) (local $l39 f32) (local $l40 f32) (local $l41 f32) (local $l42 f32) (local $l43 f32) (local $l44 f32) (local $l45 f32) (local $l46 f32) (local $l47 f32) (local $l48 f32) (local $l49 f32) (local $l50 f32) (local $l51 f32) (local $l52 f32) (local $l53 f32) (local $l54 f32) (local $l55 f32) (local $l56 f32) (local $l57 f32) (local $l58 f32) (local $l59 f32) (local $l60 f32) (local $l61 f32) (local $l62 f32) (local $l63 f32) (local $l64 f32) (local $l65 f32) (local $l66 f32) (local $l67 f32) (local $l68 f32) (local $l69 f32) (local $l70 f32) (local $l71 f32) (local $l72 f32) (local $l73 f32) (local $l74 f32) (local $l75 f32) (local $l76 f32) (local $l77 f32) (local $l78 f32) (local $l79 f32) (local $l80 f32) (local $l81 f32) (local $l82 f32) (local $l83 f32) (local $l84 f32) (local $l85 f32) (local $l86 f32) (local $l87 f32) (local $l88 f32) (local $l89 f32) (local $l90 f32) (local $l91 f32) (local $l92 f32) (local $l93 f32) (local $l94 f32) (local $l95 f32) (local $l96 f32) (local $l97 f32) (local $l98 f32) (local $l99 f32) (local $l100 f32) (local $l101 f32) (local $l102 f32) (local $l103 f32) (local $l104 f32) (local $l105 f32) (local $l106 f32) (local $l107 f32) (local $l108 f32) (local $l109 f32) (local $l110 f32) (local $l111 f32) (local $l112 f32) (local $l113 f32) (local $l114 f32) (local $l115 f32) (local $l116 f32) (local $l117 f32) (local $l118 f32) (local $l119 f32) (local $l120 f32) (local $l121 f32) (local $l122 f32) (local $l123 f32) (local $l124 f32) (local $l125 f32) (local $l126 f32) (local $l127 f32) (local $l128 f32) (local $l129 f32) (local $l130 f32) (local $l131 f32) (local $l132 f32) (local $l133 f32) (local $l134 f32) (local $l135 i64) (local $l136 i64)
    global.get $g0
    i32.const 32
    i32.sub
    local.tee $l17
    global.set $g0
    local.get $p2
    i32.const 4112
    i32.add
    i32.const 0
    i32.store
    local.get $l17
    i32.const 1065353216
    i32.store offset=28
    local.get $l17
    i32.const 1065353216
    i32.store offset=24
    local.get $l17
    i32.const 1065353216
    i32.store offset=20
    local.get $l17
    i32.const 1065353216
    i32.store offset=16
    local.get $p2
    i32.const 16
    i32.add
    local.set $l28
    local.get $p0
    block $B0 (result f32)
      local.get $p0
      i32.load offset=100
      i32.const 8
      i32.ne
      if $I1
        f32.const 0x0p+0 (;=0;)
        local.get $p0
        i32.load offset=20
        i32.load8_u offset=62
        br_if $B0
        drop
      end
      local.get $p0
      f32.load offset=4
    end
    f32.store offset=4
    local.get $p0
    block $B2 (result f32)
      local.get $p0
      i32.load offset=104
      i32.const 8
      i32.ne
      if $I3
        f32.const 0x0p+0 (;=0;)
        local.get $p0
        i32.load offset=24
        i32.load8_u offset=62
        br_if $B2
        drop
      end
      local.get $p0
      f32.load offset=12
    end
    f32.store offset=12
    local.get $l17
    i32.const 0
    i32.store8 offset=15
    local.get $l17
    i32.const 0
    i32.store8 offset=14
    local.get $p0
    local.get $l28
    local.get $p1
    local.get $l17
    i32.const 15
    i32.add
    local.get $l17
    i32.const 14
    i32.add
    local.get $l17
    i32.const 28
    i32.add
    local.get $l17
    i32.const 24
    i32.add
    local.get $l17
    i32.const 20
    i32.add
    local.get $l17
    i32.const 16
    i32.add
    local.get $p0
    f32.load offset=160
    call $f71234
    i32.store offset=116
    local.get $p0
    local.get $l28
    i32.store offset=112
    local.get $p0
    local.get $p0
    i32.load8_u offset=121
    local.get $l17
    i32.load8_u offset=14
    i32.const 1
    i32.and
    i32.or
    i32.store8 offset=121
    local.get $p0
    local.get $l17
    i32.load8_u offset=15
    i32.store8 offset=120
    local.get $p0
    local.get $l17
    f32.load offset=28
    local.get $p0
    f32.load
    f32.mul
    f32.store
    local.get $p0
    local.get $l17
    f32.load offset=24
    local.get $p0
    f32.load offset=8
    f32.mul
    f32.store offset=8
    local.get $p0
    local.get $l17
    f32.load offset=20
    local.get $p0
    f32.load offset=4
    f32.mul
    f32.store offset=4
    local.get $p0
    local.get $l17
    f32.load offset=16
    local.get $p0
    f32.load offset=12
    f32.mul
    f32.store offset=12
    i32.const 0
    local.set $l28
    global.get $g0
    i32.const 32
    i32.sub
    local.tee $l14
    global.set $g0
    local.get $p2
    i32.const 4128
    i32.add
    local.tee $p2
    i64.const 0
    i64.store offset=7684 align=4
    local.get $p0
    i32.load8_u offset=121
    local.set $l24
    local.get $p0
    i32.load8_u offset=122
    local.set $l30
    local.get $p0
    i32.load offset=100
    local.set $l11
    local.get $p0
    i32.load offset=104
    local.set $l19
    local.get $p0
    i32.load offset=16
    local.tee $p1
    i32.const 0
    i32.store16 offset=22
    block $B4
      local.get $p0
      i32.load offset=116
      local.tee $l10
      i32.eqz
      if $I5
        local.get $p0
        i32.const 0
        i32.store8 offset=136
        local.get $p0
        i32.const 0
        i32.store offset=132
        local.get $p1
        i32.const 0
        i32.store offset=24
        br $B4
      end
      local.get $l11
      local.get $l19
      i32.or
      local.set $l11
      local.get $l24
      i32.const 255
      i32.and
      i32.eqz
      if $I6
        local.get $p2
        local.get $p0
        i32.load offset=132
        local.get $p0
        i32.load8_u offset=136
        local.get $p0
        i32.const 44
        i32.add
        local.get $p0
        i32.const 72
        i32.add
        local.get $p7
        call $f71233
        drop
        local.get $p0
        i32.load offset=116
        local.set $l10
      end
      local.get $l11
      i32.const 8
      i32.and
      local.set $l23
      local.get $p2
      local.get $p0
      i32.load offset=112
      local.get $l10
      call $f71216
      drop
      local.get $p2
      local.get $p0
      i32.load offset=112
      local.get $p0
      i32.const 44
      i32.add
      local.tee $l20
      local.get $p0
      i32.const 72
      i32.add
      local.tee $l21
      i32.const 0
      i32.const 0
      call $f71217
      drop
      local.get $p2
      local.get $p0
      i32.load offset=112
      local.get $l20
      local.get $l21
      local.get $p7
      i32.const 0
      local.get $p0
      f32.load offset=124
      local.get $p6
      f32.add
      call $f71218
      block $B7 (result i32)
        local.get $p2
        i32.load offset=7688
        local.tee $l27
        if $I8 (result i32)
          i32.const 7
          i32.const 6
          local.get $l23
          select
          local.set $l25
          i32.const 112
          i32.const 48
          local.get $l23
          select
          local.set $l26
          local.get $p0
          f32.load offset=164
          local.tee $p7
          local.get $p0
          f32.load offset=168
          local.tee $p6
          local.get $p6
          local.get $p7
          f32.lt
          select
          local.set $p7
          i32.const 0
          local.set $l10
          loop $L9
            local.get $p2
            local.get $l10
            i32.const 2
            i32.shl
            i32.add
            local.tee $l11
            i32.const 7424
            i32.add
            i32.load
            i32.const 65535
            i32.ne
            local.set $l22
            block $B10
              local.get $l11
              i32.const 7296
              i32.add
              i32.load
              local.tee $l11
              i32.eqz
              br_if $B10
              local.get $l13
              local.get $l11
              local.get $l26
              i32.mul
              i32.add
              local.get $l11
              i32.const 2
              i32.shl
              i32.const 12
              i32.add
              i32.const -16
              i32.and
              i32.add
              i32.const 80
              i32.add
              local.set $l13
              local.get $p2
              local.get $l10
              i32.const 104
              i32.mul
              i32.add
              local.tee $l11
              i32.const 2817
              i32.add
              i32.load8_u
              i32.const 1
              i32.and
              br_if $B10
              local.get $l11
              i32.const 2818
              i32.add
              i32.load16_u
              local.tee $l11
              i32.const 1
              i32.shl
              local.get $l11
              i32.const 1
              i32.eq
              local.get $p7
              f32.const 0x0p+0 (;=0;)
              f32.gt
              i32.and
              i32.or
              local.get $l25
              i32.shl
              local.get $l13
              i32.add
              local.set $l13
            end
            local.get $l12
            local.get $l22
            i32.add
            local.set $l12
            local.get $l10
            i32.const 1
            i32.add
            local.tee $l10
            local.get $l27
            i32.ne
            br_if $L9
          end
          local.get $l12
          i32.const 104
          i32.mul
          i32.const 15
          i32.add
          local.set $l11
          i32.const 0
          local.set $l10
          local.get $l13
          i32.const 15
          i32.add
          i32.const -16
          i32.and
          local.tee $l31
          if $I11
            i32.const 0
            local.get $p8
            local.get $l31
            i32.const 16
            i32.add
            local.get $p8
            i32.load
            i32.load
            call_indirect $__indirect_function_table (type $t0)
            local.tee $l10
            local.get $l10
            i32.const -1
            i32.eq
            select
            local.set $l10
          end
          local.get $l11
          i32.const -16
          i32.and
          local.set $l22
          block $B12
            local.get $l31
            i32.eqz
            local.get $l10
            i32.const 0
            i32.ne
            i32.or
            local.tee $l13
            i32.eqz
            br_if $B12
            local.get $l22
            i32.eqz
            br_if $B12
            i32.const 0
            local.get $p8
            local.get $l22
            local.get $p8
            i32.load
            i32.load offset=4
            call_indirect $__indirect_function_table (type $t0)
            local.tee $l11
            local.get $l11
            i32.const -1
            i32.eq
            select
            local.set $l29
          end
          local.get $l10
          i32.const 0
          local.get $l31
          select
          local.set $l28
          i32.const 0
          local.get $l13
          i32.eqz
          br_if $B7
          drop
          local.get $l22
          i32.eqz
        else
          i32.const 1
        end
        local.set $l10
        local.get $l10
        local.get $l29
        i32.const 0
        i32.ne
        i32.or
      end
      local.set $l11
      local.get $p0
      i32.const 0
      i32.store8 offset=136
      local.get $p0
      i32.const 0
      i32.store offset=132
      local.get $p1
      i32.const 0
      i32.store16 offset=22
      local.get $p1
      i32.const 0
      i32.store offset=24
      local.get $l11
      i32.eqz
      br_if $B4
      local.get $p0
      local.get $l29
      i32.store offset=132
      local.get $p1
      local.get $l28
      i32.store offset=24
      local.get $p0
      local.get $l12
      i32.store8 offset=136
      local.get $p1
      local.get $l31
      i32.const 4
      i32.shr_u
      i32.store16 offset=22
      local.get $p1
      local.get $p0
      i32.load offset=140
      i32.store offset=28
      i32.const 0
      local.set $l12
      local.get $p1
      local.get $p0
      i32.load16_u offset=116
      i32.const 0
      local.get $p0
      i32.load offset=140
      select
      i32.store16 offset=20
      block $B13
        local.get $l29
        i32.eqz
        br_if $B13
        local.get $p2
        i32.load offset=7688
        local.tee $l11
        i32.eqz
        br_if $B13
        local.get $l29
        local.set $l10
        loop $L14
          local.get $p2
          local.get $l12
          i32.const 2
          i32.shl
          i32.add
          i32.const 7296
          i32.add
          i32.load
          if $I15
            local.get $l10
            local.get $p2
            local.get $l12
            i32.const 104
            i32.mul
            i32.add
            local.tee $l11
            i32.const 2816
            i32.add
            i32.load8_u
            i32.store8
            local.get $l10
            local.get $l11
            i32.const 2817
            i32.add
            i32.load8_u
            i32.store8 offset=1
            local.get $l10
            local.get $l11
            i32.const 2818
            i32.add
            i32.load16_u
            i32.store16 offset=2
            local.get $l10
            local.get $l11
            i32.const 2832
            i32.add
            f32.load
            f32.store offset=16
            local.get $l10
            local.get $l11
            i32.const 2836
            i32.add
            f32.load
            f32.store offset=20
            local.get $l10
            local.get $l11
            i32.const 2840
            i32.add
            f32.load
            f32.store offset=24
            local.get $l10
            local.get $l11
            i32.const 2844
            i32.add
            f32.load
            f32.store offset=28
            local.get $l10
            local.get $l11
            i32.const 2848
            i32.add
            f32.load
            f32.store offset=32
            local.get $l10
            local.get $l11
            i32.const 2852
            i32.add
            f32.load
            f32.store offset=36
            local.get $l10
            local.get $l11
            i32.const 2856
            i32.add
            f32.load
            f32.store offset=40
            local.get $l10
            local.get $l11
            i32.const 2860
            i32.add
            f32.load
            f32.store offset=44
            local.get $l10
            local.get $l11
            i32.const 2864
            i32.add
            f32.load
            f32.store offset=48
            local.get $l10
            local.get $l11
            i32.const 2868
            i32.add
            f32.load
            f32.store offset=52
            local.get $l10
            local.get $l11
            i32.const 2872
            i32.add
            f32.load
            f32.store offset=56
            local.get $l10
            local.get $l11
            i32.const 2876
            i32.add
            f32.load
            f32.store offset=60
            local.get $l10
            local.get $l11
            i32.const 2880
            i32.add
            f32.load
            f32.store offset=64
            local.get $l10
            local.get $l11
            i32.const 2884
            i32.add
            f32.load
            f32.store offset=68
            local.get $l10
            local.get $l11
            i32.const 2888
            i32.add
            f32.load
            f32.store offset=72
            local.get $l10
            local.get $l11
            i32.const 2892
            i32.add
            f32.load
            f32.store offset=76
            local.get $l10
            local.get $l11
            i32.const 2896
            i32.add
            f32.load
            f32.store offset=80
            local.get $l10
            local.get $l11
            i32.const 2900
            i32.add
            f32.load
            f32.store offset=84
            local.get $l10
            local.get $l11
            i32.const 2904
            i32.add
            f32.load
            f32.store offset=88
            local.get $l10
            local.get $l11
            i32.const 2908
            i32.add
            f32.load
            f32.store offset=92
            local.get $l10
            local.get $l11
            i32.const 2912
            i32.add
            f32.load
            f32.store offset=96
            local.get $l10
            local.get $l11
            i32.const 2916
            i32.add
            f32.load
            f32.store offset=100
            local.get $l10
            local.get $l11
            i32.const 2820
            i32.add
            f32.load
            f32.store offset=4
            local.get $l10
            local.get $l11
            i32.const 2824
            i32.add
            f32.load
            f32.store offset=8
            local.get $l10
            local.get $l11
            i32.const 2828
            i32.add
            f32.load
            f32.store offset=12
            local.get $l10
            i32.const 104
            i32.add
            local.set $l10
            local.get $p2
            i32.load offset=7688
            local.set $l11
          end
          local.get $l12
          i32.const 1
          i32.add
          local.tee $l12
          local.get $l11
          i32.lt_u
          br_if $L14
        end
      end
      local.get $l28
      i32.eqz
      br_if $B4
      block $B16
        local.get $l23
        if $I17
          local.get $p0
          i32.load offset=20
          local.set $l10
          local.get $p0
          i32.load offset=28
          local.set $l11
          local.get $p0
          i32.load offset=36
          local.set $l12
          local.get $l14
          local.get $p1
          i32.load16_u offset=8
          i32.store16 offset=28
          local.get $l14
          local.get $l12
          i32.store offset=24
          local.get $l14
          local.get $l11
          i32.store offset=20
          local.get $l14
          local.get $l10
          i32.store offset=16
          local.get $p0
          i32.load offset=24
          local.set $l10
          local.get $p0
          i32.load offset=32
          local.set $l11
          local.get $p0
          i32.load offset=40
          local.set $l12
          local.get $l14
          local.get $p1
          i32.load16_u offset=10
          i32.store16 offset=12
          local.get $l14
          local.get $l12
          i32.store offset=8
          local.get $l14
          local.get $l11
          i32.store offset=4
          local.get $l14
          local.get $l10
          i32.store
          local.get $p0
          i32.load offset=112
          local.set $l18
          local.get $p2
          local.set $p1
          local.get $l28
          local.set $p2
          local.get $p3
          local.set $l36
          local.get $p0
          f32.load
          local.set $l85
          local.get $p0
          f32.load offset=4
          local.set $l86
          local.get $p0
          f32.load offset=8
          local.set $l87
          local.get $p0
          f32.load offset=12
          local.set $l88
          local.get $p0
          f32.load offset=124
          local.set $l131
          local.get $p0
          f32.load offset=128
          drop
          local.get $p0
          f32.load offset=164
          local.set $l98
          local.get $p0
          f32.load offset=168
          local.set $l89
          i32.const 0
          local.set $l19
          i32.const 0
          local.set $l27
          i32.const 0
          local.set $l30
          global.get $g0
          i32.const 272
          i32.sub
          local.tee $l9
          global.set $g0
          local.get $l14
          i32.const 16
          i32.add
          local.tee $l12
          i32.load16_u offset=12
          local.tee $p8
          i32.const 65535
          i32.eq
          if $I18
            local.get $l12
            i32.load
            i32.load8_u offset=62
            i32.const 0
            i32.ne
            local.set $l30
          end
          local.get $l14
          i32.load16_u offset=12
          local.tee $p0
          i32.const 65535
          i32.eq
          if $I19
            local.get $l14
            i32.load
            i32.load8_u offset=62
            i32.const 0
            i32.ne
            local.set $l27
          end
          block $B20
            local.get $p8
            i32.const 65535
            i32.eq
            if $I21
              local.get $l12
              i32.load offset=8
              f32.load offset=28
              local.set $l35
              br $B20
            end
            local.get $l12
            i32.load
            local.tee $p0
            local.get $p8
            local.get $p0
            i32.load
            i32.load offset=124
            call_indirect $__indirect_function_table (type $t13)
            local.set $l35
            local.get $l14
            i32.load16_u offset=12
            local.set $p0
          end
          block $B22 (result f32)
            local.get $p0
            i32.const 65535
            i32.and
            local.tee $p8
            i32.const 65535
            i32.eq
            if $I23
              local.get $l14
              i32.load offset=8
              f32.load offset=28
              br $B22
            end
            local.get $l14
            i32.load
            local.tee $p0
            local.get $p8
            local.get $p0
            i32.load
            i32.load offset=124
            call_indirect $__indirect_function_table (type $t13)
          end
          local.set $l39
          block $B24
            local.get $l12
            i32.load16_u offset=12
            local.tee $p8
            i32.const 65535
            i32.eq
            if $I25
              local.get $l12
              i32.load offset=8
              local.tee $p8
              f32.load offset=24
              local.set $l40
              local.get $p8
              f32.load offset=8
              local.set $l37
              local.get $p8
              i64.load offset=16 align=4
              local.set $l135
              local.get $p8
              i64.load align=4
              local.set $l136
              local.get $l9
              i32.const 0
              i32.store offset=124
              local.get $l9
              local.get $l40
              f32.store offset=120
              local.get $l9
              i32.const 0
              i32.store offset=108
              local.get $l9
              local.get $l136
              i64.store offset=96
              local.get $l9
              local.get $l135
              i64.store offset=112
              local.get $l9
              local.get $l37
              f32.store offset=104
              br $B24
            end
            local.get $l9
            i32.const 96
            i32.add
            local.get $l12
            i32.load
            local.tee $p0
            local.get $p8
            local.get $p0
            i32.load
            i32.load offset=116
            call_indirect $__indirect_function_table (type $t2)
          end
          block $B26
            local.get $l14
            i32.load16_u offset=12
            local.tee $p8
            i32.const 65535
            i32.eq
            if $I27
              local.get $l14
              i32.load offset=8
              local.tee $p8
              f32.load offset=24
              local.set $l40
              local.get $p8
              f32.load offset=8
              local.set $l37
              local.get $p8
              i64.load offset=16 align=4
              local.set $l135
              local.get $p8
              i64.load align=4
              local.set $l136
              local.get $l9
              i32.const 0
              i32.store offset=92
              local.get $l9
              local.get $l40
              f32.store offset=88
              local.get $l9
              i32.const 0
              i32.store offset=76
              local.get $l9
              local.get $l136
              i64.store offset=64
              local.get $l9
              local.get $l135
              i64.store offset=80
              local.get $l9
              local.get $l37
              f32.store offset=72
              br $B26
            end
            local.get $l9
            i32.const -64
            i32.sub
            local.get $l14
            i32.load
            local.tee $p0
            local.get $p8
            local.get $p0
            i32.load
            i32.load offset=116
            call_indirect $__indirect_function_table (type $t2)
          end
          local.get $l9
          local.get $l85
          f32.store offset=48
          local.get $l9
          local.get $l87
          f32.store offset=32
          local.get $l9
          local.get $l86
          f32.store offset=16
          local.get $l9
          local.get $l88
          f32.store
          local.get $p1
          i32.load offset=7688
          local.tee $p8
          if $I28
            local.get $l98
            f32.const 0x0p+0 (;=0;)
            f32.gt
            local.get $l89
            f32.const 0x0p+0 (;=0;)
            f32.gt
            i32.or
            local.set $l11
            local.get $l35
            local.get $l39
            local.get $l35
            local.get $l39
            f32.gt
            select
            local.set $l132
            local.get $l36
            f32.const 0x1.99999ap-1 (;=0.8;)
            f32.mul
            local.tee $l92
            f32.neg
            local.set $l133
            local.get $l21
            f32.load offset=24
            local.set $l99
            local.get $l21
            f32.load offset=20
            local.set $l100
            local.get $l20
            f32.load offset=24
            local.set $l101
            local.get $l20
            f32.load offset=20
            local.set $l102
            local.get $l9
            i32.const 224
            i32.add
            local.set $l22
            local.get $l9
            i32.const 256
            i32.add
            local.set $l23
            local.get $l21
            f32.load offset=16
            local.set $l103
            local.get $l20
            f32.load offset=16
            local.set $l104
            loop $L29
              local.get $p1
              local.get $l19
              i32.const 2
              i32.shl
              i32.add
              local.tee $p0
              i32.const 7296
              i32.add
              i32.load
              local.tee $l24
              if $I30
                f32.const 0x1p+0 (;=1;)
                local.set $l35
                local.get $l18
                local.get $p1
                local.get $p0
                i32.const 7424
                i32.add
                local.tee $l25
                i32.load
                i32.const 44
                i32.mul
                i32.add
                i32.load16_u
                i32.const 6
                i32.shl
                i32.add
                local.tee $l26
                i32.load8_u offset=48
                local.tee $p0
                i32.const 4
                i32.and
                if $I31
                  f32.const 0x1p+0 (;=1;)
                  local.get $p1
                  local.get $l19
                  i32.const 104
                  i32.mul
                  i32.add
                  i32.const 2818
                  i32.add
                  i32.load16_u
                  f32.convert_i32_u
                  f32.div
                  local.set $l35
                end
                local.get $l26
                f32.load offset=60
                local.set $l65
                local.get $l26
                f32.load offset=44
                local.set $l39
                local.get $l26
                f32.load offset=56
                local.set $l36
                local.get $p2
                local.get $l24
                i32.store8 offset=2
                local.get $l35
                local.get $l36
                f32.mul
                local.set $l36
                local.get $l35
                local.get $l39
                f32.mul
                local.set $l35
                i32.const 0
                local.set $p8
                local.get $p0
                i32.const 1
                i32.and
                local.tee $l10
                i32.eqz
                if $I32
                  local.get $p1
                  local.get $l19
                  i32.const 104
                  i32.mul
                  i32.add
                  i32.const 2818
                  i32.add
                  i32.load8_u
                  i32.const 1
                  i32.shl
                  local.set $p8
                end
                local.get $p2
                i32.const 80
                i32.add
                local.set $p0
                local.get $p2
                local.get $l87
                f32.store offset=28
                local.get $p2
                local.get $l85
                f32.store offset=24
                local.get $p2
                local.get $l36
                f32.store offset=20
                local.get $p2
                local.get $l35
                f32.store offset=16
                local.get $p2
                i32.const 3
                i32.store16
                local.get $p2
                local.get $p8
                i32.store8 offset=3
                local.get $p2
                local.get $l88
                f32.store offset=8
                local.get $p2
                local.get $l86
                f32.store offset=4
                local.get $l18
                local.get $p1
                local.get $l25
                i32.load
                i32.const 44
                i32.mul
                i32.add
                i32.load16_u
                i32.const 6
                i32.shl
                i32.add
                local.tee $p8
                f32.load
                local.set $l39
                local.get $p8
                f32.load offset=4
                local.set $l35
                local.get $p8
                f32.load offset=8
                local.set $l36
                local.get $p2
                local.get $l132
                f32.store offset=44
                local.get $p2
                local.get $l36
                f32.store offset=40
                local.get $p2
                local.get $l35
                f32.store offset=36
                local.get $p2
                local.get $l39
                f32.store offset=32
                local.get $l35
                f32.neg
                local.set $l105
                local.get $l36
                f32.neg
                local.set $l106
                f32.const 0x0p+0 (;=0;)
                local.set $l68
                block $B33
                  local.get $l25
                  i32.load
                  local.tee $p8
                  i32.const 65535
                  i32.eq
                  if $I34
                    f32.const 0x0p+0 (;=0;)
                    local.set $l64
                    br $B33
                  end
                  local.get $l39
                  f32.neg
                  local.set $l134
                  f32.const 0x0p+0 (;=0;)
                  local.set $l64
                  loop $L35
                    local.get $p1
                    local.get $p8
                    i32.const 44
                    i32.mul
                    i32.add
                    local.tee $l16
                    i32.load8_u offset=5
                    local.tee $l33
                    if $I36
                      local.get $l18
                      local.get $l16
                      i32.load16_u
                      i32.const 6
                      i32.shl
                      i32.add
                      local.set $l34
                      i32.const 0
                      local.set $l13
                      local.get $p0
                      local.set $p8
                      loop $L37
                        local.get $l35
                        local.get $l34
                        local.get $l13
                        i32.const 6
                        i32.shl
                        i32.add
                        local.tee $p0
                        f32.load offset=16
                        local.tee $l40
                        local.get $l103
                        f32.sub
                        local.tee $l37
                        f32.mul
                        local.set $l38
                        local.get $l39
                        local.get $p0
                        f32.load offset=20
                        local.tee $l45
                        local.get $l100
                        f32.sub
                        local.tee $l41
                        f32.mul
                        local.set $l48
                        local.get $l39
                        local.get $p0
                        f32.load offset=24
                        local.tee $l56
                        local.get $l99
                        f32.sub
                        local.tee $l43
                        f32.mul
                        local.get $l36
                        local.get $l37
                        f32.mul
                        f32.sub
                        local.set $l42
                        local.get $l35
                        local.get $l43
                        f32.mul
                        local.set $l54
                        local.get $l36
                        local.get $l41
                        f32.mul
                        local.set $l62
                        local.get $p0
                        f32.load offset=12
                        local.set $p3
                        local.get $l36
                        local.get $l45
                        local.get $l102
                        f32.sub
                        local.tee $l37
                        f32.mul
                        local.get $l35
                        local.get $l56
                        local.get $l101
                        f32.sub
                        local.tee $l41
                        f32.mul
                        f32.sub
                        local.tee $l43
                        local.set $l45
                        local.get $l39
                        local.get $l41
                        f32.mul
                        local.get $l36
                        local.get $l40
                        local.get $l104
                        f32.sub
                        local.tee $l40
                        f32.mul
                        f32.sub
                        local.tee $l52
                        local.set $l41
                        local.get $l35
                        local.get $l40
                        f32.mul
                        local.get $l39
                        local.get $l37
                        f32.mul
                        f32.sub
                        local.tee $l61
                        local.set $l56
                        local.get $l12
                        i32.load16_u offset=12
                        i32.const 65535
                        i32.eq
                        if $I38
                          local.get $l43
                          local.get $l12
                          i32.load offset=4
                          local.tee $l15
                          f32.load offset=36
                          f32.mul
                          local.get $l52
                          local.get $l15
                          f32.load offset=48
                          f32.mul
                          f32.add
                          local.get $l61
                          local.get $l15
                          f32.load offset=60
                          f32.mul
                          f32.add
                          local.set $l56
                          local.get $l43
                          local.get $l15
                          f32.load offset=28
                          f32.mul
                          local.get $l52
                          local.get $l15
                          f32.load offset=40
                          f32.mul
                          f32.add
                          local.get $l61
                          local.get $l15
                          f32.load offset=52
                          f32.mul
                          f32.add
                          local.set $l45
                          local.get $l43
                          local.get $l15
                          f32.load offset=32
                          f32.mul
                          local.get $l52
                          local.get $l15
                          f32.load offset=44
                          f32.mul
                          f32.add
                          local.get $l61
                          local.get $l15
                          f32.load offset=56
                          f32.mul
                          f32.add
                          local.set $l41
                        end
                        local.get $l38
                        local.get $l48
                        f32.sub
                        local.set $l37
                        local.get $l62
                        local.get $l54
                        f32.sub
                        local.set $l38
                        local.get $p3
                        local.get $l131
                        f32.sub
                        local.set $l40
                        local.get $l9
                        i32.const 0
                        i32.store offset=204
                        local.get $l9
                        local.get $l56
                        f32.store offset=200
                        local.get $l9
                        local.get $l41
                        f32.store offset=196
                        local.get $l9
                        local.get $l45
                        f32.store offset=192
                        local.get $l9
                        i32.const 0
                        i32.store offset=188
                        local.get $l9
                        local.get $l36
                        f32.store offset=184
                        local.get $l9
                        local.get $l35
                        f32.store offset=180
                        local.get $l9
                        local.get $l39
                        f32.store offset=176
                        local.get $l42
                        f32.neg
                        local.set $l48
                        block $B39 (result f32)
                          local.get $l14
                          i32.load16_u offset=12
                          i32.const 65535
                          i32.eq
                          if $I40
                            local.get $l14
                            i32.load offset=4
                            local.tee $l15
                            f32.load offset=48
                            local.get $l48
                            f32.mul
                            local.get $l38
                            local.get $l15
                            f32.load offset=36
                            f32.mul
                            f32.sub
                            local.get $l37
                            local.get $l15
                            f32.load offset=60
                            f32.mul
                            f32.sub
                            local.set $l54
                            local.get $l15
                            f32.load offset=40
                            local.get $l48
                            f32.mul
                            local.get $l38
                            local.get $l15
                            f32.load offset=28
                            f32.mul
                            f32.sub
                            local.get $l37
                            local.get $l15
                            f32.load offset=52
                            f32.mul
                            f32.sub
                            local.set $p3
                            local.get $l15
                            f32.load offset=44
                            local.get $l48
                            f32.mul
                            local.get $l38
                            local.get $l15
                            f32.load offset=32
                            f32.mul
                            f32.sub
                            local.get $l37
                            local.get $l15
                            f32.load offset=56
                            f32.mul
                            f32.sub
                            br $B39
                          end
                          local.get $l38
                          f32.neg
                          local.set $p3
                          local.get $l37
                          f32.neg
                          local.set $l54
                          local.get $l48
                        end
                        local.set $l62
                        local.get $l9
                        i32.const 0
                        i32.store offset=172
                        local.get $l9
                        i32.const 0
                        i32.store offset=156
                        local.get $l9
                        local.get $l106
                        f32.store offset=152
                        local.get $l9
                        local.get $l105
                        f32.store offset=148
                        local.get $l9
                        local.get $l134
                        f32.store offset=144
                        local.get $l9
                        local.get $p3
                        f32.store offset=160
                        local.get $l9
                        local.get $l62
                        f32.store offset=164
                        local.get $l9
                        local.get $l54
                        f32.store offset=168
                        local.get $l9
                        i32.const 128
                        i32.add
                        local.get $l12
                        local.get $l9
                        i32.const 176
                        i32.add
                        local.get $l9
                        i32.const 240
                        i32.add
                        local.get $l9
                        i32.const 48
                        i32.add
                        local.get $l9
                        i32.const 16
                        i32.add
                        local.get $l14
                        local.get $l9
                        i32.const 144
                        i32.add
                        local.get $l9
                        i32.const 208
                        i32.add
                        local.get $l9
                        i32.const 32
                        i32.add
                        local.get $l9
                        call $f70934
                        local.get $p0
                        f32.load offset=40
                        local.set $p7
                        local.get $p0
                        f32.load offset=36
                        local.set $p6
                        local.get $p0
                        f32.load offset=32
                        local.set $l71
                        local.get $l9
                        f32.load offset=104
                        local.set $l77
                        local.get $l9
                        f32.load offset=120
                        local.set $l72
                        local.get $l9
                        f32.load offset=72
                        local.set $l73
                        local.get $l9
                        f32.load offset=88
                        local.set $l74
                        local.get $l9
                        f32.load offset=96
                        local.set $l75
                        local.get $l9
                        f32.load offset=112
                        local.set $l76
                        local.get $l9
                        f32.load offset=64
                        local.set $l81
                        local.get $l9
                        f32.load offset=80
                        local.set $l82
                        local.get $l9
                        f32.load offset=100
                        local.set $l83
                        local.get $l9
                        f32.load offset=116
                        local.set $l84
                        local.get $l9
                        f32.load offset=68
                        local.set $l90
                        local.get $l9
                        f32.load offset=84
                        local.set $l91
                        local.get $l9
                        f32.load offset=128
                        local.set $l48
                        local.get $p8
                        local.get $l133
                        f32.store offset=36
                        local.get $p8
                        local.get $l54
                        f32.neg
                        f32.store offset=24
                        local.get $p8
                        local.get $l62
                        f32.neg
                        f32.store offset=20
                        local.get $p8
                        local.get $p3
                        f32.neg
                        f32.store offset=16
                        local.get $p8
                        local.get $l40
                        f32.store offset=12
                        local.get $p8
                        local.get $l56
                        f32.store offset=8
                        local.get $p8
                        local.get $l41
                        f32.store offset=4
                        local.get $p8
                        local.get $l45
                        f32.store
                        local.get $p8
                        f32.const 0x1p+0 (;=1;)
                        local.get $l48
                        f32.const 0x1.a36e2ep-14 (;=0.0001;)
                        f32.add
                        f32.div
                        f32.const 0x0p+0 (;=0;)
                        local.get $l48
                        f32.const 0x1p-23 (;=1.19209e-07;)
                        f32.gt
                        select
                        local.tee $l45
                        f32.store offset=28
                        local.get $p8
                        local.get $l39
                        local.get $l81
                        f32.mul
                        local.get $l38
                        local.get $l82
                        f32.mul
                        f32.add
                        local.tee $l38
                        local.get $l35
                        local.get $l90
                        f32.mul
                        local.get $l42
                        local.get $l91
                        f32.mul
                        f32.add
                        local.tee $l41
                        f32.add
                        local.get $l36
                        local.get $l73
                        f32.mul
                        local.get $l37
                        local.get $l74
                        f32.mul
                        f32.add
                        local.tee $l37
                        f32.add
                        local.get $l39
                        local.get $l71
                        f32.mul
                        local.get $l35
                        local.get $p6
                        f32.mul
                        f32.add
                        local.get $l36
                        local.get $p7
                        f32.mul
                        f32.add
                        local.get $l65
                        local.get $l39
                        local.get $l75
                        f32.mul
                        local.get $l43
                        local.get $l76
                        f32.mul
                        f32.add
                        local.tee $l56
                        local.get $l38
                        f32.sub
                        local.get $l35
                        local.get $l83
                        f32.mul
                        local.get $l52
                        local.get $l84
                        f32.mul
                        f32.add
                        local.tee $l38
                        local.get $l41
                        f32.sub
                        f32.add
                        local.get $l36
                        local.get $l77
                        f32.mul
                        local.get $l61
                        local.get $l72
                        f32.mul
                        f32.add
                        local.tee $l41
                        local.get $l37
                        f32.sub
                        f32.add
                        local.tee $l37
                        f32.neg
                        local.tee $l43
                        f32.mul
                        f32.const 0x0p+0 (;=0;)
                        local.get $p5
                        local.get $l37
                        f32.gt
                        select
                        f32.const 0x0p+0 (;=0;)
                        local.get $l65
                        f32.const 0x0p+0 (;=0;)
                        f32.gt
                        select
                        f32.const 0x0p+0 (;=0;)
                        local.get $l40
                        local.get $p4
                        f32.mul
                        local.get $l43
                        f32.lt
                        select
                        f32.add
                        local.tee $l43
                        local.get $l56
                        local.get $l38
                        f32.add
                        local.get $l41
                        f32.add
                        f32.sub
                        local.get $l43
                        local.get $l30
                        select
                        local.tee $l38
                        f32.add
                        local.get $l38
                        local.get $l27
                        select
                        local.tee $l38
                        f32.store offset=32
                        local.get $p8
                        local.get $l9
                        i64.load offset=240
                        i64.store offset=48
                        local.get $p8
                        local.get $l9
                        i64.load offset=248
                        i64.store offset=56
                        local.get $p8
                        local.get $l23
                        i64.load
                        i64.store offset=80
                        local.get $p8
                        local.get $l23
                        i64.load offset=8
                        i64.store offset=88
                        local.get $p8
                        local.get $l9
                        i64.load offset=208
                        i64.store offset=64
                        local.get $p8
                        local.get $l9
                        i64.load offset=216
                        i64.store offset=72
                        local.get $p8
                        local.get $l22
                        i64.load
                        i64.store offset=96
                        local.get $p8
                        local.get $l22
                        i64.load offset=8
                        i64.store offset=104
                        local.get $l64
                        local.get $l45
                        local.get $l38
                        local.get $l92
                        local.get $l40
                        f32.mul
                        f32.sub
                        f32.mul
                        local.get $l37
                        local.get $l45
                        f32.mul
                        f32.sub
                        local.tee $l40
                        f32.const 0x0p+0 (;=0;)
                        local.get $l40
                        f32.const 0x0p+0 (;=0;)
                        f32.gt
                        select
                        f32.add
                        local.set $l64
                        local.get $l68
                        local.get $p0
                        f32.load offset=12
                        local.tee $l40
                        local.get $l40
                        local.get $l68
                        f32.gt
                        select
                        local.set $l68
                        local.get $p8
                        i32.const 112
                        i32.add
                        local.tee $p0
                        local.set $p8
                        local.get $l13
                        i32.const 1
                        i32.add
                        local.tee $l13
                        local.get $l33
                        i32.ne
                        br_if $L37
                      end
                    end
                    local.get $l16
                    i32.load16_u offset=2
                    local.tee $p8
                    i32.const 65535
                    i32.ne
                    br_if $L35
                  end
                end
                local.get $p2
                local.get $l64
                local.get $l24
                f32.convert_i32_u
                f32.div
                f32.store offset=52
                local.get $p0
                i32.const 0
                local.get $l24
                i32.const 2
                i32.shl
                local.tee $p8
                call $f484
                local.set $p0
                local.get $p2
                i32.const 0
                i32.store offset=56
                local.get $p0
                local.get $p8
                i32.const 12
                i32.add
                i32.const -16
                i32.and
                i32.add
                local.set $p0
                block $B41
                  local.get $l10
                  br_if $B41
                  local.get $l9
                  f32.load offset=72
                  local.set $l40
                  local.get $l9
                  f32.load offset=104
                  local.set $l37
                  local.get $l9
                  f32.load offset=64
                  local.set $l38
                  local.get $l9
                  f32.load offset=96
                  local.set $l45
                  local.get $l9
                  f32.load offset=68
                  local.set $l41
                  local.get $l9
                  f32.load offset=100
                  local.set $l56
                  local.get $p2
                  local.get $l29
                  local.get $l32
                  i32.const 104
                  i32.mul
                  i32.add
                  i32.store offset=60
                  local.get $p1
                  local.get $l19
                  i32.const 104
                  i32.mul
                  i32.add
                  local.tee $l16
                  i32.const 2818
                  i32.add
                  local.tee $l24
                  i32.load16_u
                  local.tee $l13
                  i32.eqz
                  br_if $B41
                  f32.const 0x0p+0 (;=0;)
                  local.get $l92
                  local.get $l10
                  select
                  local.set $l71
                  local.get $l39
                  local.get $l56
                  local.get $l41
                  f32.sub
                  local.tee $l41
                  local.get $l35
                  local.get $l39
                  local.get $l45
                  local.get $l38
                  f32.sub
                  local.tee $l45
                  f32.mul
                  local.get $l35
                  local.get $l41
                  f32.mul
                  f32.add
                  local.get $l36
                  local.get $l37
                  local.get $l40
                  f32.sub
                  local.tee $l38
                  f32.mul
                  f32.add
                  local.tee $l40
                  f32.mul
                  f32.sub
                  local.tee $l37
                  local.get $l106
                  local.get $l39
                  local.get $l39
                  f32.abs
                  f32.const 0x1.6a09e6p-1 (;=0.707107;)
                  f32.lt
                  local.tee $p8
                  select
                  local.get $l38
                  local.get $l36
                  local.get $l40
                  f32.mul
                  f32.sub
                  local.tee $l38
                  local.get $l38
                  f32.mul
                  local.get $l45
                  local.get $l39
                  local.get $l40
                  f32.mul
                  f32.sub
                  local.tee $l40
                  local.get $l40
                  f32.mul
                  local.get $l37
                  local.get $l37
                  f32.mul
                  f32.add
                  f32.add
                  f32.const 0x1.a36e2ep-14 (;=0.0001;)
                  f32.gt
                  local.tee $l15
                  select
                  local.tee $l37
                  f32.const 0x1p+0 (;=1;)
                  local.get $l38
                  local.get $l35
                  f32.const 0x0p+0 (;=0;)
                  local.get $p8
                  select
                  local.get $l15
                  select
                  local.tee $l38
                  local.get $l38
                  f32.mul
                  local.get $l40
                  f32.const 0x0p+0 (;=0;)
                  local.get $l105
                  local.get $p8
                  select
                  local.get $l15
                  select
                  local.tee $l45
                  local.get $l45
                  f32.mul
                  local.get $l37
                  local.get $l37
                  f32.mul
                  f32.add
                  f32.add
                  f32.sqrt
                  f32.div
                  local.tee $l41
                  f32.mul
                  local.tee $l40
                  f32.mul
                  local.get $l35
                  local.get $l45
                  local.get $l41
                  f32.mul
                  local.tee $l37
                  f32.mul
                  f32.sub
                  local.tee $l45
                  f32.neg
                  local.set $l81
                  local.get $l36
                  local.get $l37
                  f32.mul
                  local.get $l39
                  local.get $l38
                  local.get $l41
                  f32.mul
                  local.tee $l38
                  f32.mul
                  f32.sub
                  local.tee $l39
                  f32.neg
                  local.set $l82
                  local.get $l35
                  local.get $l38
                  f32.mul
                  local.get $l36
                  local.get $l40
                  f32.mul
                  f32.sub
                  local.tee $l35
                  f32.neg
                  local.set $l83
                  local.get $l38
                  f32.neg
                  local.set $l84
                  local.get $l40
                  f32.neg
                  local.set $l90
                  local.get $l37
                  f32.neg
                  local.set $l91
                  f32.const 0x1p-1 (;=0.5;)
                  f32.const 0x1p+0 (;=1;)
                  local.get $l13
                  i32.const 2
                  i32.eq
                  select
                  f32.const 0x1p+0 (;=1;)
                  local.get $l26
                  i32.load8_u offset=48
                  i32.const 4
                  i32.and
                  select
                  local.set $l77
                  i32.const 0
                  local.set $l15
                  loop $L42
                    local.get $p0
                    local.set $p8
                    local.get $l37
                    local.get $l21
                    f32.load offset=4
                    local.tee $l43
                    local.get $l16
                    local.get $l15
                    i32.const 12
                    i32.mul
                    i32.add
                    local.tee $p0
                    i32.const 2880
                    i32.add
                    f32.load
                    local.tee $l36
                    local.get $l36
                    f32.add
                    local.tee $l52
                    local.get $l21
                    f32.load
                    local.tee $l61
                    f32.mul
                    local.get $l43
                    local.get $p0
                    i32.const 2884
                    i32.add
                    f32.load
                    local.tee $l36
                    local.get $l36
                    f32.add
                    local.tee $l42
                    f32.mul
                    f32.add
                    local.get $p0
                    i32.const 2888
                    i32.add
                    f32.load
                    local.tee $l36
                    local.get $l36
                    f32.add
                    local.tee $l48
                    local.get $l21
                    f32.load offset=8
                    local.tee $l54
                    f32.mul
                    f32.add
                    local.tee $l62
                    f32.mul
                    local.get $l42
                    local.get $l21
                    f32.load offset=12
                    local.tee $l36
                    local.get $l36
                    f32.mul
                    f32.const -0x1p-1 (;=-0.5;)
                    f32.add
                    local.tee $p3
                    f32.mul
                    local.get $l36
                    local.get $l52
                    local.get $l54
                    f32.mul
                    local.get $l48
                    local.get $l61
                    f32.mul
                    f32.sub
                    f32.mul
                    f32.add
                    f32.add
                    local.tee $l41
                    f32.mul
                    local.set $l72
                    local.get $l40
                    local.get $l61
                    local.get $l62
                    f32.mul
                    local.get $l52
                    local.get $p3
                    f32.mul
                    local.get $l36
                    local.get $l48
                    local.get $l43
                    f32.mul
                    local.get $l42
                    local.get $l54
                    f32.mul
                    f32.sub
                    f32.mul
                    f32.add
                    f32.add
                    local.tee $l56
                    f32.mul
                    local.set $l73
                    local.get $l37
                    local.get $l48
                    local.get $p3
                    f32.mul
                    local.get $l36
                    local.get $l42
                    local.get $l61
                    f32.mul
                    local.get $l52
                    local.get $l43
                    f32.mul
                    f32.sub
                    f32.mul
                    f32.add
                    local.get $l54
                    local.get $l62
                    f32.mul
                    f32.add
                    local.tee $l36
                    f32.mul
                    local.get $l38
                    local.get $l56
                    f32.mul
                    f32.sub
                    local.set $l74
                    local.get $l40
                    local.get $l36
                    f32.mul
                    local.set $l75
                    local.get $l38
                    local.get $l41
                    f32.mul
                    local.set $l76
                    local.get $l40
                    local.get $l20
                    f32.load
                    local.tee $l42
                    local.get $l42
                    local.get $p0
                    i32.const 2856
                    i32.add
                    f32.load
                    local.tee $l43
                    local.get $l43
                    f32.add
                    local.tee $l48
                    f32.mul
                    local.get $p0
                    i32.const 2860
                    i32.add
                    f32.load
                    local.tee $l43
                    local.get $l43
                    f32.add
                    local.tee $l54
                    local.get $l20
                    f32.load offset=4
                    local.tee $l62
                    f32.mul
                    f32.add
                    local.get $p0
                    i32.const 2864
                    i32.add
                    f32.load
                    local.tee $l43
                    local.get $l43
                    f32.add
                    local.tee $p3
                    local.get $l20
                    f32.load offset=8
                    local.tee $l64
                    f32.mul
                    f32.add
                    local.tee $l65
                    f32.mul
                    local.get $l48
                    local.get $l20
                    f32.load offset=12
                    local.tee $l43
                    local.get $l43
                    f32.mul
                    f32.const -0x1p-1 (;=-0.5;)
                    f32.add
                    local.tee $p7
                    f32.mul
                    local.get $l43
                    local.get $p3
                    local.get $l62
                    f32.mul
                    local.get $l54
                    local.get $l64
                    f32.mul
                    f32.sub
                    f32.mul
                    f32.add
                    f32.add
                    local.tee $l52
                    f32.mul
                    local.get $l37
                    local.get $l62
                    local.get $l65
                    f32.mul
                    local.get $l54
                    local.get $p7
                    f32.mul
                    local.get $l43
                    local.get $l48
                    local.get $l64
                    f32.mul
                    local.get $p3
                    local.get $l42
                    f32.mul
                    f32.sub
                    f32.mul
                    f32.add
                    f32.add
                    local.tee $l61
                    f32.mul
                    f32.sub
                    local.set $p6
                    local.get $l37
                    local.get $p3
                    local.get $p7
                    f32.mul
                    local.get $l43
                    local.get $l54
                    local.get $l42
                    f32.mul
                    local.get $l48
                    local.get $l62
                    f32.mul
                    f32.sub
                    f32.mul
                    f32.add
                    local.get $l64
                    local.get $l65
                    f32.mul
                    f32.add
                    local.tee $l43
                    f32.mul
                    local.get $l38
                    local.get $l52
                    f32.mul
                    f32.sub
                    local.set $l42
                    local.get $l38
                    local.get $l61
                    f32.mul
                    local.get $l40
                    local.get $l43
                    f32.mul
                    f32.sub
                    local.set $l48
                    block $B43
                      local.get $l12
                      i32.load16_u offset=12
                      i32.const 65535
                      i32.ne
                      if $I44
                        local.get $l42
                        local.set $p3
                        local.get $p6
                        local.set $l64
                        br $B43
                      end
                      local.get $l48
                      local.get $l12
                      i32.load offset=4
                      local.tee $p0
                      f32.load offset=36
                      f32.mul
                      local.get $l42
                      local.get $p0
                      f32.load offset=48
                      f32.mul
                      f32.add
                      local.get $p6
                      local.get $p0
                      f32.load offset=60
                      f32.mul
                      f32.add
                      local.set $l64
                      local.get $l48
                      local.get $p0
                      f32.load offset=32
                      f32.mul
                      local.get $l42
                      local.get $p0
                      f32.load offset=44
                      f32.mul
                      f32.add
                      local.get $p6
                      local.get $p0
                      f32.load offset=56
                      f32.mul
                      f32.add
                      local.set $p3
                      local.get $l48
                      local.get $p0
                      f32.load offset=28
                      f32.mul
                      local.get $l42
                      local.get $p0
                      f32.load offset=40
                      f32.mul
                      f32.add
                      local.get $p6
                      local.get $p0
                      f32.load offset=52
                      f32.mul
                      f32.add
                      local.set $l48
                    end
                    local.get $l73
                    local.get $l72
                    f32.sub
                    local.set $l42
                    local.get $l76
                    local.get $l75
                    f32.sub
                    local.set $l54
                    local.get $l9
                    i32.const 0
                    i32.store offset=204
                    local.get $l9
                    local.get $l64
                    f32.store offset=200
                    local.get $l9
                    local.get $p3
                    f32.store offset=196
                    local.get $l9
                    local.get $l48
                    f32.store offset=192
                    local.get $l9
                    i32.const 0
                    i32.store offset=188
                    local.get $l9
                    local.get $l38
                    f32.store offset=184
                    local.get $l9
                    local.get $l40
                    f32.store offset=180
                    local.get $l9
                    local.get $l37
                    f32.store offset=176
                    local.get $l74
                    f32.neg
                    local.set $l62
                    block $B45 (result f32)
                      local.get $l14
                      i32.load16_u offset=12
                      i32.const 65535
                      i32.eq
                      if $I46
                        local.get $l14
                        i32.load offset=4
                        local.tee $p0
                        f32.load offset=48
                        local.get $l62
                        f32.mul
                        local.get $l54
                        local.get $p0
                        f32.load offset=36
                        f32.mul
                        f32.sub
                        local.get $l42
                        local.get $p0
                        f32.load offset=60
                        f32.mul
                        f32.sub
                        local.set $l65
                        local.get $p0
                        f32.load offset=44
                        local.get $l62
                        f32.mul
                        local.get $l54
                        local.get $p0
                        f32.load offset=32
                        f32.mul
                        f32.sub
                        local.get $l42
                        local.get $p0
                        f32.load offset=56
                        f32.mul
                        f32.sub
                        local.set $p7
                        local.get $p0
                        f32.load offset=40
                        local.get $l62
                        f32.mul
                        local.get $l54
                        local.get $p0
                        f32.load offset=28
                        f32.mul
                        f32.sub
                        local.get $l42
                        local.get $p0
                        f32.load offset=52
                        f32.mul
                        f32.sub
                        br $B45
                      end
                      local.get $l42
                      f32.neg
                      local.set $l65
                      local.get $l62
                      local.set $p7
                      local.get $l54
                      f32.neg
                    end
                    local.set $p6
                    local.get $l99
                    local.get $l36
                    f32.add
                    local.set $l54
                    local.get $l101
                    local.get $l43
                    f32.add
                    local.set $l62
                    local.get $l100
                    local.get $l41
                    f32.add
                    local.set $l72
                    local.get $l102
                    local.get $l61
                    f32.add
                    local.set $l73
                    local.get $l103
                    local.get $l56
                    f32.add
                    local.set $l74
                    local.get $l104
                    local.get $l52
                    f32.add
                    local.set $l75
                    local.get $l9
                    i32.const 0
                    i32.store offset=172
                    local.get $l9
                    local.get $l65
                    f32.store offset=168
                    local.get $l9
                    local.get $p7
                    f32.store offset=164
                    local.get $l9
                    local.get $p6
                    f32.store offset=160
                    local.get $l9
                    i32.const 0
                    i32.store offset=156
                    local.get $l9
                    local.get $l84
                    f32.store offset=152
                    local.get $l9
                    local.get $l90
                    f32.store offset=148
                    local.get $l9
                    local.get $l91
                    f32.store offset=144
                    local.get $l9
                    i32.const 128
                    i32.add
                    local.get $l12
                    local.get $l9
                    i32.const 176
                    i32.add
                    local.get $l9
                    i32.const 240
                    i32.add
                    local.get $l9
                    i32.const 48
                    i32.add
                    local.get $l9
                    i32.const 16
                    i32.add
                    local.get $l14
                    local.get $l9
                    i32.const 144
                    i32.add
                    local.get $l9
                    i32.const 208
                    i32.add
                    local.get $l9
                    i32.const 32
                    i32.add
                    local.get $l9
                    call $f70934
                    local.get $l9
                    f32.load offset=128
                    local.tee $l42
                    f32.const 0x1p-23 (;=1.19209e-07;)
                    f32.gt
                    local.set $l13
                    f32.const 0x1.99999ap-1 (;=0.8;)
                    local.get $l42
                    f32.const 0x1.a36e2ep-14 (;=0.0001;)
                    f32.add
                    f32.div
                    local.set $l76
                    local.get $l37
                    local.get $l18
                    local.get $p1
                    local.get $l25
                    i32.load
                    i32.const 44
                    i32.mul
                    i32.add
                    i32.load16_u
                    i32.const 6
                    i32.shl
                    i32.add
                    local.tee $p0
                    f32.load offset=32
                    f32.mul
                    local.get $l40
                    local.get $p0
                    f32.load offset=36
                    f32.mul
                    f32.add
                    local.get $l38
                    local.get $p0
                    f32.load offset=40
                    f32.mul
                    f32.add
                    local.set $l42
                    local.get $l30
                    if $I47
                      local.get $l42
                      local.get $l9
                      f32.load offset=96
                      local.get $l37
                      f32.mul
                      local.get $l9
                      f32.load offset=112
                      local.get $l48
                      f32.mul
                      f32.add
                      local.get $l9
                      f32.load offset=100
                      local.get $l40
                      f32.mul
                      local.get $l9
                      f32.load offset=116
                      local.get $p3
                      f32.mul
                      f32.add
                      f32.add
                      local.get $l9
                      f32.load offset=104
                      local.get $l38
                      f32.mul
                      local.get $l9
                      f32.load offset=120
                      local.get $l64
                      f32.mul
                      f32.add
                      f32.add
                      f32.sub
                      local.set $l42
                    end
                    local.get $l62
                    local.get $l54
                    f32.sub
                    local.set $l48
                    local.get $l73
                    local.get $l72
                    f32.sub
                    local.set $l54
                    local.get $l75
                    local.get $l74
                    f32.sub
                    local.set $l62
                    local.get $l76
                    f32.const 0x0p+0 (;=0;)
                    local.get $l13
                    select
                    local.set $p3
                    local.get $l27
                    if $I48
                      local.get $l42
                      local.get $l9
                      f32.load offset=80
                      local.get $p6
                      f32.mul
                      local.get $l37
                      local.get $l9
                      f32.load offset=64
                      f32.mul
                      f32.sub
                      local.get $l9
                      f32.load offset=84
                      local.get $p7
                      f32.mul
                      local.get $l40
                      local.get $l9
                      f32.load offset=68
                      f32.mul
                      f32.sub
                      f32.add
                      local.get $l9
                      f32.load offset=88
                      local.get $l65
                      f32.mul
                      local.get $l38
                      local.get $l9
                      f32.load offset=72
                      f32.mul
                      f32.sub
                      f32.add
                      f32.sub
                      local.set $l42
                    end
                    local.get $p8
                    local.get $l38
                    f32.store offset=8
                    local.get $p8
                    local.get $l40
                    f32.store offset=4
                    local.get $p8
                    local.get $l37
                    f32.store
                    local.get $p8
                    local.get $l38
                    local.get $l48
                    f32.mul
                    local.get $l37
                    local.get $l62
                    f32.mul
                    local.get $l40
                    local.get $l54
                    f32.mul
                    f32.add
                    f32.add
                    f32.store offset=12
                    local.get $l9
                    i64.load offset=192
                    local.set $l135
                    local.get $l9
                    f32.load offset=200
                    local.set $l64
                    local.get $p8
                    local.get $l42
                    f32.store offset=28
                    local.get $p8
                    local.get $l64
                    f32.store offset=24
                    local.get $p8
                    local.get $l135
                    i64.store offset=16
                    local.get $l9
                    f32.load offset=160
                    local.set $l42
                    local.get $l9
                    f32.load offset=164
                    local.set $l64
                    local.get $l9
                    f32.load offset=168
                    local.set $l65
                    local.get $p8
                    i32.const 0
                    i32.store offset=52
                    local.get $p8
                    local.get $p3
                    f32.store offset=44
                    local.get $p8
                    local.get $l71
                    f32.store offset=48
                    local.get $p8
                    local.get $l65
                    f32.neg
                    f32.store offset=40
                    local.get $p8
                    local.get $l64
                    f32.neg
                    f32.store offset=36
                    local.get $p8
                    local.get $l42
                    f32.neg
                    f32.store offset=32
                    local.get $p8
                    local.get $l9
                    i64.load offset=240
                    i64.store offset=64
                    local.get $p8
                    local.get $l9
                    i64.load offset=248
                    i64.store offset=72
                    local.get $p8
                    local.get $l9
                    i64.load offset=208
                    i64.store offset=80
                    local.get $p8
                    local.get $l9
                    i64.load offset=216
                    i64.store offset=88
                    local.get $p8
                    local.get $l23
                    i64.load
                    i64.store offset=96
                    local.get $p8
                    local.get $l23
                    i32.const 8
                    i32.add
                    local.tee $l13
                    i64.load
                    i64.store offset=104
                    local.get $p8
                    local.get $l22
                    i64.load
                    i64.store offset=112
                    local.get $p8
                    local.get $l22
                    i32.const 8
                    i32.add
                    local.tee $l33
                    i64.load
                    i64.store offset=120
                    local.get $p8
                    local.get $l77
                    f32.store offset=56
                    local.get $l35
                    local.get $l41
                    f32.mul
                    local.set $l42
                    local.get $l39
                    local.get $l56
                    f32.mul
                    local.set $p3
                    local.get $l35
                    local.get $l36
                    f32.mul
                    local.get $l45
                    local.get $l56
                    f32.mul
                    f32.sub
                    local.set $l64
                    local.get $l39
                    local.get $l36
                    f32.mul
                    local.set $l65
                    local.get $l45
                    local.get $l41
                    f32.mul
                    local.set $p7
                    local.get $l39
                    local.get $l52
                    f32.mul
                    local.get $l35
                    local.get $l61
                    f32.mul
                    f32.sub
                    local.set $l41
                    local.get $l35
                    local.get $l43
                    f32.mul
                    local.get $l45
                    local.get $l52
                    f32.mul
                    f32.sub
                    local.set $l52
                    local.get $l45
                    local.get $l61
                    f32.mul
                    local.get $l39
                    local.get $l43
                    f32.mul
                    f32.sub
                    local.set $l36
                    block $B49
                      local.get $l12
                      i32.load16_u offset=12
                      i32.const 65535
                      i32.ne
                      if $I50
                        local.get $l52
                        local.set $l56
                        local.get $l41
                        local.set $l43
                        br $B49
                      end
                      local.get $l36
                      local.get $l12
                      i32.load offset=4
                      local.tee $p0
                      f32.load offset=36
                      f32.mul
                      local.get $l52
                      local.get $p0
                      f32.load offset=48
                      f32.mul
                      f32.add
                      local.get $l41
                      local.get $p0
                      f32.load offset=60
                      f32.mul
                      f32.add
                      local.set $l43
                      local.get $l36
                      local.get $p0
                      f32.load offset=32
                      f32.mul
                      local.get $l52
                      local.get $p0
                      f32.load offset=44
                      f32.mul
                      f32.add
                      local.get $l41
                      local.get $p0
                      f32.load offset=56
                      f32.mul
                      f32.add
                      local.set $l56
                      local.get $l36
                      local.get $p0
                      f32.load offset=28
                      f32.mul
                      local.get $l52
                      local.get $p0
                      f32.load offset=40
                      f32.mul
                      f32.add
                      local.get $l41
                      local.get $p0
                      f32.load offset=52
                      f32.mul
                      f32.add
                      local.set $l36
                    end
                    local.get $p3
                    local.get $l42
                    f32.sub
                    local.set $l41
                    local.get $p7
                    local.get $l65
                    f32.sub
                    local.set $l42
                    local.get $l9
                    i32.const 0
                    i32.store offset=204
                    local.get $l9
                    local.get $l43
                    f32.store offset=200
                    local.get $l9
                    local.get $l56
                    f32.store offset=196
                    local.get $l9
                    local.get $l36
                    f32.store offset=192
                    local.get $l9
                    i32.const 0
                    i32.store offset=188
                    local.get $l9
                    local.get $l45
                    f32.store offset=184
                    local.get $l9
                    local.get $l39
                    f32.store offset=180
                    local.get $l9
                    local.get $l35
                    f32.store offset=176
                    local.get $l64
                    f32.neg
                    local.set $p3
                    block $B51 (result f32)
                      local.get $l14
                      i32.load16_u offset=12
                      i32.const 65535
                      i32.eq
                      if $I52
                        local.get $l14
                        i32.load offset=4
                        local.tee $p0
                        f32.load offset=48
                        local.get $p3
                        f32.mul
                        local.get $l42
                        local.get $p0
                        f32.load offset=36
                        f32.mul
                        f32.sub
                        local.get $l41
                        local.get $p0
                        f32.load offset=60
                        f32.mul
                        f32.sub
                        local.set $l52
                        local.get $p0
                        f32.load offset=44
                        local.get $p3
                        f32.mul
                        local.get $l42
                        local.get $p0
                        f32.load offset=32
                        f32.mul
                        f32.sub
                        local.get $l41
                        local.get $p0
                        f32.load offset=56
                        f32.mul
                        f32.sub
                        local.set $l61
                        local.get $p0
                        f32.load offset=40
                        local.get $p3
                        f32.mul
                        local.get $l42
                        local.get $p0
                        f32.load offset=28
                        f32.mul
                        f32.sub
                        local.get $l41
                        local.get $p0
                        f32.load offset=52
                        f32.mul
                        f32.sub
                        br $B51
                      end
                      local.get $l41
                      f32.neg
                      local.set $l52
                      local.get $p3
                      local.set $l61
                      local.get $l42
                      f32.neg
                    end
                    local.set $l42
                    local.get $l9
                    i32.const 0
                    i32.store offset=172
                    local.get $l9
                    local.get $l52
                    f32.store offset=168
                    local.get $l9
                    local.get $l61
                    f32.store offset=164
                    local.get $l9
                    local.get $l42
                    f32.store offset=160
                    local.get $l9
                    i32.const 0
                    i32.store offset=156
                    local.get $l9
                    local.get $l81
                    f32.store offset=152
                    local.get $l9
                    local.get $l82
                    f32.store offset=148
                    local.get $l9
                    local.get $l83
                    f32.store offset=144
                    local.get $l9
                    i32.const 128
                    i32.add
                    local.get $l12
                    local.get $l9
                    i32.const 176
                    i32.add
                    local.get $l9
                    i32.const 240
                    i32.add
                    local.get $l9
                    i32.const 48
                    i32.add
                    local.get $l9
                    i32.const 16
                    i32.add
                    local.get $l14
                    local.get $l9
                    i32.const 144
                    i32.add
                    local.get $l9
                    i32.const 208
                    i32.add
                    local.get $l9
                    i32.const 32
                    i32.add
                    local.get $l9
                    call $f70934
                    local.get $l9
                    f32.load offset=128
                    local.tee $l41
                    f32.const 0x1p-23 (;=1.19209e-07;)
                    f32.gt
                    local.set $l34
                    f32.const 0x1.99999ap-1 (;=0.8;)
                    local.get $l41
                    f32.const 0x1.a36e2ep-14 (;=0.0001;)
                    f32.add
                    f32.div
                    local.set $p3
                    local.get $l35
                    local.get $l18
                    local.get $p1
                    local.get $l25
                    i32.load
                    i32.const 44
                    i32.mul
                    i32.add
                    i32.load16_u
                    i32.const 6
                    i32.shl
                    i32.add
                    local.tee $p0
                    f32.load offset=32
                    f32.mul
                    local.get $l39
                    local.get $p0
                    f32.load offset=36
                    f32.mul
                    f32.add
                    local.get $l45
                    local.get $p0
                    f32.load offset=40
                    f32.mul
                    f32.add
                    local.set $l41
                    local.get $l30
                    if $I53
                      local.get $l41
                      local.get $l9
                      f32.load offset=96
                      local.get $l35
                      f32.mul
                      local.get $l9
                      f32.load offset=112
                      local.get $l36
                      f32.mul
                      f32.add
                      local.get $l9
                      f32.load offset=100
                      local.get $l39
                      f32.mul
                      local.get $l9
                      f32.load offset=116
                      local.get $l56
                      f32.mul
                      f32.add
                      f32.add
                      local.get $l9
                      f32.load offset=104
                      local.get $l45
                      f32.mul
                      local.get $l9
                      f32.load offset=120
                      local.get $l43
                      f32.mul
                      f32.add
                      f32.add
                      f32.sub
                      local.set $l41
                    end
                    local.get $p3
                    f32.const 0x0p+0 (;=0;)
                    local.get $l34
                    select
                    local.set $p3
                    local.get $l27
                    if $I54
                      local.get $l41
                      local.get $l9
                      f32.load offset=80
                      local.get $l42
                      f32.mul
                      local.get $l35
                      local.get $l9
                      f32.load offset=64
                      f32.mul
                      f32.sub
                      local.get $l9
                      f32.load offset=84
                      local.get $l61
                      f32.mul
                      local.get $l39
                      local.get $l9
                      f32.load offset=68
                      f32.mul
                      f32.sub
                      f32.add
                      local.get $l9
                      f32.load offset=88
                      local.get $l52
                      f32.mul
                      local.get $l45
                      local.get $l9
                      f32.load offset=72
                      f32.mul
                      f32.sub
                      f32.add
                      f32.sub
                      local.set $l41
                    end
                    local.get $p8
                    i32.const 256
                    i32.add
                    local.set $p0
                    local.get $p8
                    i32.const 0
                    i32.store offset=180
                    local.get $p8
                    local.get $p3
                    f32.store offset=172
                    local.get $p8
                    local.get $l41
                    f32.store offset=156
                    local.get $p8
                    local.get $l43
                    f32.store offset=152
                    local.get $p8
                    local.get $l56
                    f32.store offset=148
                    local.get $p8
                    local.get $l36
                    f32.store offset=144
                    local.get $p8
                    local.get $l45
                    f32.store offset=136
                    local.get $p8
                    local.get $l39
                    f32.store offset=132
                    local.get $p8
                    local.get $l35
                    f32.store offset=128
                    local.get $p8
                    local.get $l71
                    f32.store offset=176
                    local.get $p8
                    local.get $l52
                    f32.neg
                    f32.store offset=168
                    local.get $p8
                    local.get $l61
                    f32.neg
                    f32.store offset=164
                    local.get $p8
                    local.get $l42
                    f32.neg
                    f32.store offset=160
                    local.get $p8
                    local.get $l45
                    local.get $l48
                    f32.mul
                    local.get $l35
                    local.get $l62
                    f32.mul
                    local.get $l39
                    local.get $l54
                    f32.mul
                    f32.add
                    f32.add
                    f32.store offset=140
                    local.get $p8
                    local.get $l9
                    i64.load offset=248
                    i64.store offset=200
                    local.get $p8
                    local.get $l9
                    i64.load offset=240
                    i64.store offset=192
                    local.get $p8
                    local.get $l9
                    i64.load offset=216
                    i64.store offset=216
                    local.get $p8
                    local.get $l9
                    i64.load offset=208
                    i64.store offset=208
                    local.get $p8
                    local.get $l13
                    i64.load
                    i64.store offset=232
                    local.get $p8
                    local.get $l23
                    i64.load
                    i64.store offset=224
                    local.get $l33
                    i64.load
                    local.set $l135
                    local.get $l22
                    i64.load
                    local.set $l136
                    local.get $p8
                    local.get $l77
                    f32.store offset=184
                    local.get $p8
                    local.get $l136
                    i64.store offset=240
                    local.get $p8
                    local.get $l135
                    i64.store offset=248
                    local.get $l15
                    i32.const 1
                    i32.add
                    local.tee $l15
                    local.get $l24
                    i32.load16_u
                    local.tee $l13
                    i32.lt_u
                    br_if $L42
                  end
                  local.get $l11
                  local.get $l13
                  i32.const 1
                  i32.eq
                  i32.and
                  i32.eqz
                  br_if $B41
                  local.get $p2
                  local.get $p2
                  i32.load8_u offset=3
                  i32.const 1
                  i32.add
                  i32.store8 offset=3
                  local.get $l68
                  f32.neg
                  f32.const 0x0p+0 (;=0;)
                  f32.max
                  local.get $l98
                  f32.mul
                  f32.sqrt
                  local.set $l48
                  local.get $l21
                  f32.load offset=8
                  local.tee $l40
                  local.get $l20
                  f32.load
                  local.tee $l35
                  local.get $l16
                  i32.const 2908
                  i32.add
                  f32.load
                  local.tee $l39
                  f32.mul
                  local.get $l20
                  f32.load offset=12
                  local.tee $l36
                  local.get $l16
                  i32.const 2912
                  i32.add
                  f32.load
                  local.tee $l37
                  f32.mul
                  local.get $l16
                  i32.const 2916
                  i32.add
                  f32.load
                  local.tee $l38
                  local.get $l20
                  f32.load offset=8
                  local.tee $l45
                  f32.mul
                  f32.add
                  f32.add
                  local.get $l16
                  i32.const 2904
                  i32.add
                  f32.load
                  local.tee $l41
                  local.get $l20
                  f32.load offset=4
                  local.tee $l56
                  f32.mul
                  f32.sub
                  local.tee $l43
                  f32.mul
                  local.get $l36
                  local.get $l38
                  f32.mul
                  local.get $l41
                  local.get $l35
                  f32.mul
                  f32.sub
                  local.get $l56
                  local.get $l39
                  f32.mul
                  f32.sub
                  local.get $l37
                  local.get $l45
                  f32.mul
                  f32.sub
                  local.tee $l52
                  local.get $l21
                  f32.load offset=12
                  local.tee $l61
                  f32.mul
                  local.get $l21
                  f32.load
                  local.tee $l68
                  local.get $l36
                  local.get $l41
                  f32.mul
                  local.get $l38
                  local.get $l35
                  f32.mul
                  f32.add
                  local.get $l56
                  local.get $l37
                  f32.mul
                  f32.add
                  local.get $l39
                  local.get $l45
                  f32.mul
                  f32.sub
                  local.tee $l42
                  f32.mul
                  f32.add
                  local.get $l38
                  local.get $l56
                  f32.mul
                  local.get $l36
                  local.get $l39
                  f32.mul
                  f32.add
                  local.get $l41
                  local.get $l45
                  f32.mul
                  f32.add
                  local.get $l35
                  local.get $l37
                  f32.mul
                  f32.sub
                  local.tee $l37
                  local.get $l21
                  f32.load offset=4
                  local.tee $l38
                  f32.mul
                  f32.add
                  f32.add
                  local.tee $l35
                  local.get $l35
                  f32.mul
                  local.get $l68
                  local.get $l52
                  f32.mul
                  local.get $l42
                  local.get $l61
                  f32.mul
                  f32.sub
                  local.get $l37
                  local.get $l40
                  f32.mul
                  f32.sub
                  local.get $l43
                  local.get $l38
                  f32.mul
                  f32.add
                  local.get $l18
                  local.get $p1
                  local.get $l25
                  i32.load
                  i32.const 44
                  i32.mul
                  i32.add
                  i32.load16_u
                  i32.const 6
                  i32.shl
                  i32.add
                  local.tee $p0
                  f32.load
                  local.tee $l45
                  f32.mul
                  local.tee $l39
                  local.get $l39
                  f32.mul
                  local.get $l42
                  local.get $l40
                  f32.mul
                  local.get $l52
                  local.get $l38
                  f32.mul
                  local.get $l61
                  local.get $l37
                  f32.mul
                  f32.sub
                  local.get $l68
                  local.get $l43
                  f32.mul
                  f32.sub
                  f32.add
                  local.get $p0
                  f32.load offset=4
                  local.tee $l41
                  f32.mul
                  local.tee $l36
                  local.get $l36
                  f32.mul
                  f32.add
                  local.get $l68
                  local.get $l37
                  f32.mul
                  local.get $l52
                  local.get $l40
                  f32.mul
                  local.get $l61
                  local.get $l43
                  f32.mul
                  f32.sub
                  local.get $l42
                  local.get $l38
                  f32.mul
                  f32.sub
                  f32.add
                  local.get $p0
                  f32.load offset=8
                  local.tee $l56
                  f32.mul
                  local.tee $l40
                  local.get $l40
                  f32.mul
                  f32.add
                  f32.add
                  f32.sqrt
                  local.tee $l37
                  f32.const 0x0p+0 (;=0;)
                  f32.ne
                  if $I55
                    local.get $l35
                    f32.const 0x1p+0 (;=1;)
                    local.get $l37
                    f32.div
                    local.tee $l38
                    f32.mul
                    local.set $l35
                    local.get $l40
                    local.get $l38
                    f32.mul
                    local.set $l40
                    local.get $l39
                    local.get $l38
                    f32.mul
                    local.set $l39
                    local.get $l36
                    local.get $l38
                    f32.mul
                    local.set $l36
                  end
                  local.get $l48
                  local.get $l89
                  f32.lt
                  local.set $l15
                  local.get $l45
                  local.get $l39
                  f32.mul
                  local.get $l41
                  local.get $l36
                  f32.mul
                  f32.add
                  local.get $l56
                  local.get $l40
                  f32.mul
                  f32.add
                  local.get $l35
                  f32.const 0x0p+0 (;=0;)
                  f32.mul
                  f32.add
                  local.get $l35
                  f32.div
                  f32.const 0x0p+0 (;=0;)
                  local.get $l37
                  f32.const -0x1.0c6f7ap-20 (;=-1e-06;)
                  f32.add
                  f32.const 0x0p+0 (;=0;)
                  f32.ge
                  select
                  call $f18178
                  local.set $l40
                  block $B56 (result f32)
                    local.get $l12
                    i32.load16_u offset=12
                    i32.const 65535
                    i32.eq
                    if $I57
                      local.get $p2
                      f32.load offset=32
                      local.tee $l35
                      local.get $l12
                      i32.load offset=4
                      local.tee $p0
                      f32.load offset=36
                      f32.mul
                      local.get $p2
                      f32.load offset=36
                      local.tee $l36
                      local.get $p0
                      f32.load offset=48
                      f32.mul
                      f32.add
                      local.get $p2
                      f32.load offset=40
                      local.tee $l39
                      local.get $p0
                      f32.load offset=60
                      f32.mul
                      f32.add
                      local.set $l37
                      local.get $l35
                      local.get $p0
                      f32.load offset=32
                      f32.mul
                      local.get $l36
                      local.get $p0
                      f32.load offset=44
                      f32.mul
                      f32.add
                      local.get $l39
                      local.get $p0
                      f32.load offset=56
                      f32.mul
                      f32.add
                      local.set $l38
                      local.get $l35
                      local.get $p0
                      f32.load offset=28
                      f32.mul
                      local.get $l36
                      local.get $p0
                      f32.load offset=40
                      f32.mul
                      f32.add
                      local.get $l39
                      local.get $p0
                      f32.load offset=52
                      f32.mul
                      f32.add
                      br $B56
                    end
                    local.get $p2
                    f32.load offset=36
                    local.tee $l36
                    local.set $l38
                    local.get $p2
                    f32.load offset=40
                    local.tee $l39
                    local.set $l37
                    local.get $p2
                    f32.load offset=32
                    local.tee $l35
                  end
                  local.set $l45
                  local.get $l89
                  local.get $l48
                  local.get $l15
                  select
                  local.set $l41
                  local.get $l9
                  i64.const 0
                  i64.store offset=248
                  local.get $l9
                  i64.const 0
                  i64.store offset=240
                  local.get $l9
                  i32.const 0
                  i32.store offset=268
                  local.get $l9
                  local.get $l37
                  f32.store offset=264
                  local.get $l9
                  local.get $l38
                  f32.store offset=260
                  local.get $l9
                  local.get $l45
                  f32.store offset=256
                  local.get $l36
                  f32.neg
                  local.set $l36
                  block $B58
                    local.get $l14
                    i32.load16_u offset=12
                    i32.const 65535
                    i32.ne
                    if $I59
                      local.get $l39
                      f32.neg
                      local.set $l37
                      local.get $l35
                      f32.neg
                      local.set $l38
                      br $B58
                    end
                    local.get $l14
                    i32.load offset=4
                    local.tee $p0
                    f32.load offset=48
                    local.get $l36
                    f32.mul
                    local.get $l35
                    local.get $p0
                    f32.load offset=36
                    f32.mul
                    f32.sub
                    local.get $l39
                    local.get $p0
                    f32.load offset=60
                    f32.mul
                    f32.sub
                    local.set $l37
                    local.get $p0
                    f32.load offset=40
                    local.get $l36
                    f32.mul
                    local.get $l35
                    local.get $p0
                    f32.load offset=28
                    f32.mul
                    f32.sub
                    local.get $l39
                    local.get $p0
                    f32.load offset=52
                    f32.mul
                    f32.sub
                    local.set $l38
                    local.get $p0
                    f32.load offset=44
                    local.get $l36
                    f32.mul
                    local.get $l35
                    local.get $p0
                    f32.load offset=32
                    f32.mul
                    f32.sub
                    local.get $l39
                    local.get $p0
                    f32.load offset=56
                    f32.mul
                    f32.sub
                    local.set $l36
                  end
                  local.get $p8
                  i32.const 384
                  i32.add
                  local.set $p0
                  local.get $l9
                  i64.const 0
                  i64.store offset=216
                  local.get $l9
                  i64.const 0
                  i64.store offset=208
                  local.get $l9
                  i32.const 0
                  i32.store offset=236
                  local.get $l9
                  local.get $l37
                  f32.store offset=232
                  local.get $l9
                  local.get $l36
                  f32.store offset=228
                  local.get $l9
                  local.get $l38
                  f32.store offset=224
                  local.get $l12
                  local.get $l9
                  i32.const 240
                  i32.add
                  local.get $l9
                  i32.const 176
                  i32.add
                  local.get $l85
                  local.get $l86
                  local.get $l14
                  local.get $l9
                  i32.const 208
                  i32.add
                  local.get $l9
                  i32.const 144
                  i32.add
                  local.get $l87
                  local.get $l88
                  call $f70933
                  local.set $l35
                  local.get $p8
                  local.get $l40
                  f32.neg
                  f32.store offset=268
                  local.get $p8
                  i32.const 0
                  i32.store offset=264
                  local.get $p8
                  i64.const 0
                  i64.store offset=256
                  local.get $l9
                  i64.load offset=256
                  local.set $l135
                  local.get $l9
                  f32.load offset=264
                  local.set $l39
                  local.get $p8
                  i32.const 0
                  i32.store offset=284
                  local.get $p8
                  local.get $l39
                  f32.store offset=280
                  local.get $p8
                  local.get $l135
                  i64.store offset=272
                  local.get $l9
                  f32.load offset=224
                  local.set $l39
                  local.get $l9
                  f32.load offset=228
                  local.set $l36
                  local.get $l9
                  f32.load offset=232
                  local.set $l40
                  local.get $p8
                  local.get $l41
                  f32.store offset=312
                  local.get $p8
                  i32.const 0
                  i32.store offset=308
                  local.get $p8
                  local.get $l71
                  f32.store offset=304
                  local.get $p8
                  f32.const 0x1.99999ap-1 (;=0.8;)
                  local.get $l35
                  f32.const 0x1.a36e2ep-14 (;=0.0001;)
                  f32.add
                  f32.div
                  f32.const 0x0p+0 (;=0;)
                  local.get $l35
                  f32.const 0x1p-23 (;=1.19209e-07;)
                  f32.gt
                  select
                  f32.store offset=300
                  local.get $p8
                  local.get $l40
                  f32.neg
                  f32.store offset=296
                  local.get $p8
                  local.get $l36
                  f32.neg
                  f32.store offset=292
                  local.get $p8
                  local.get $l39
                  f32.neg
                  f32.store offset=288
                  local.get $l9
                  i64.load offset=176
                  local.set $l135
                  local.get $l9
                  f32.load offset=184
                  local.set $l35
                  local.get $p8
                  i32.const 0
                  i32.store offset=332
                  local.get $p8
                  local.get $l35
                  f32.store offset=328
                  local.get $p8
                  local.get $l135
                  i64.store offset=320
                  local.get $l9
                  i64.load offset=144
                  local.set $l135
                  local.get $l9
                  f32.load offset=152
                  local.set $l35
                  local.get $p8
                  i32.const 0
                  i32.store offset=348
                  local.get $p8
                  local.get $l35
                  f32.store offset=344
                  local.get $p8
                  local.get $l135
                  i64.store offset=336
                  local.get $l9
                  i64.load offset=192
                  local.set $l135
                  local.get $l9
                  f32.load offset=200
                  local.set $l35
                  local.get $p8
                  i32.const 0
                  i32.store offset=364
                  local.get $p8
                  local.get $l35
                  f32.store offset=360
                  local.get $p8
                  local.get $l135
                  i64.store offset=352
                  local.get $l9
                  i64.load offset=160
                  local.set $l135
                  local.get $l9
                  f32.load offset=168
                  local.set $l35
                  local.get $p8
                  i32.const 0
                  i32.store offset=380
                  local.get $p8
                  local.get $l35
                  f32.store offset=376
                  local.get $p8
                  local.get $l135
                  i64.store offset=368
                end
                local.get $l32
                i32.const 1
                i32.add
                local.set $l32
                local.get $p1
                i32.load offset=7688
                local.set $p8
                local.get $p0
                local.set $p2
              end
              local.get $l19
              i32.const 1
              i32.add
              local.tee $l19
              local.get $p8
              i32.lt_u
              br_if $L29
            end
          end
          local.get $l9
          i32.const 272
          i32.add
          global.set $g0
          br $B16
        end
        local.get $p2
        i32.load offset=7688
        local.tee $l10
        i32.eqz
        br_if $B16
        i32.const 5
        i32.const 1
        local.get $l19
        i32.const 4
        i32.eq
        local.get $l19
        i32.const 2
        i32.eq
        i32.or
        select
        local.set $l33
        f32.const 0x0p+0 (;=0;)
        local.get $p3
        f32.const 0x1.99999ap-1 (;=0.8;)
        f32.mul
        local.tee $p7
        local.get $l24
        i32.const 255
        i32.and
        select
        local.set $l68
        local.get $p0
        f32.load offset=68
        local.tee $l99
        local.get $p0
        f32.load offset=96
        local.tee $l100
        f32.sub
        local.set $l101
        local.get $p0
        i32.const -64
        i32.sub
        f32.load
        local.tee $l102
        local.get $p0
        f32.load offset=92
        local.tee $l103
        f32.sub
        local.set $l104
        local.get $p0
        f32.load offset=60
        local.tee $l105
        local.get $p0
        f32.load offset=88
        local.tee $l106
        f32.sub
        local.set $l98
        local.get $p0
        f32.load offset=164
        local.tee $l132
        f32.const 0x0p+0 (;=0;)
        f32.gt
        local.get $p0
        f32.load offset=168
        local.tee $l90
        f32.const 0x0p+0 (;=0;)
        f32.gt
        i32.or
        local.set $l34
        local.get $p0
        i32.load offset=36
        local.tee $l11
        f32.load offset=28
        local.tee $p6
        local.get $p0
        i32.load offset=40
        local.tee $l12
        f32.load offset=28
        local.tee $p3
        local.get $p3
        local.get $p6
        f32.lt
        select
        local.set $l133
        local.get $p0
        f32.load offset=84
        local.tee $l107
        local.get $l107
        f32.mul
        f32.const -0x1p-1 (;=-0.5;)
        f32.add
        local.set $l71
        local.get $p0
        f32.load offset=56
        local.tee $l108
        local.get $l108
        f32.mul
        f32.const -0x1p-1 (;=-0.5;)
        f32.add
        local.set $l72
        local.get $p0
        f32.load
        local.get $l11
        f32.load offset=32
        f32.mul
        local.set $l73
        local.get $p0
        f32.load offset=80
        local.set $l109
        local.get $p0
        f32.load offset=76
        local.set $l110
        local.get $p0
        f32.load offset=72
        local.set $l111
        local.get $p0
        f32.load offset=52
        local.set $l112
        local.get $p0
        f32.load offset=48
        local.set $l113
        local.get $p0
        f32.load offset=44
        local.set $l114
        local.get $p0
        f32.load offset=124
        local.set $l134
        local.get $p0
        f32.load offset=12
        local.set $l93
        local.get $p0
        f32.load offset=4
        local.set $l94
        local.get $p0
        i32.load offset=112
        local.set $l25
        local.get $p0
        i32.load offset=108
        local.set $l32
        local.get $p0
        i32.load offset=24
        i32.load8_u offset=62
        local.set $l27
        local.get $l11
        f32.load offset=8
        local.tee $l74
        local.get $l12
        f32.load offset=8
        local.tee $l75
        f32.sub
        local.set $l91
        local.get $l11
        f32.load offset=4
        local.tee $l76
        local.get $l12
        f32.load offset=4
        local.tee $l77
        f32.sub
        local.set $l85
        local.get $l11
        f32.load
        local.tee $l81
        local.get $l12
        f32.load
        local.tee $l82
        f32.sub
        local.set $l86
        local.get $p7
        f32.neg
        local.set $l131
        local.get $p0
        i32.load offset=32
        local.tee $l16
        f32.load offset=60
        local.set $l115
        local.get $l16
        f32.load offset=56
        local.set $l116
        local.get $l16
        f32.load offset=52
        local.set $l117
        local.get $l16
        f32.load offset=48
        local.set $l118
        local.get $l16
        f32.load offset=44
        local.set $l119
        local.get $l16
        f32.load offset=40
        local.set $l120
        local.get $l16
        f32.load offset=36
        local.set $l121
        local.get $l16
        f32.load offset=32
        local.set $l122
        local.get $p0
        i32.load offset=28
        local.tee $l18
        f32.load offset=60
        local.set $l123
        local.get $l18
        f32.load offset=56
        local.set $l124
        local.get $l18
        f32.load offset=52
        local.set $l125
        local.get $l18
        f32.load offset=48
        local.set $l126
        local.get $l18
        f32.load offset=44
        local.set $l127
        local.get $l18
        f32.load offset=40
        local.set $l128
        local.get $l18
        f32.load offset=36
        local.set $l129
        local.get $l18
        f32.load offset=32
        local.set $l130
        local.get $l12
        f32.load offset=24
        local.set $l35
        local.get $l12
        f32.load offset=20
        local.set $l37
        local.get $l11
        f32.load offset=24
        local.set $l38
        local.get $l11
        f32.load offset=20
        local.set $l39
        local.get $l12
        f32.load offset=32
        local.get $p0
        f32.load offset=8
        f32.neg
        f32.mul
        local.tee $l87
        f32.neg
        local.set $l36
        local.get $l16
        f32.load offset=28
        local.set $l40
        local.get $l18
        f32.load offset=28
        local.set $l45
        local.get $l12
        f32.load offset=16
        local.set $l48
        local.get $l11
        f32.load offset=16
        local.set $l54
        i32.const 0
        local.set $l21
        local.get $p0
        i32.load offset=20
        i32.load8_u offset=62
        local.set $l22
        local.get $l28
        local.set $p1
        i32.const 0
        local.set $l23
        loop $L60
          local.get $p2
          local.get $l23
          i32.const 2
          i32.shl
          i32.add
          local.tee $p8
          i32.const 7296
          i32.add
          i32.load
          local.tee $l20
          if $I61
            local.get $l25
            local.get $p2
            local.get $p8
            i32.const 7424
            i32.add
            local.tee $l24
            i32.load
            i32.const 44
            i32.mul
            i32.add
            i32.load16_u
            i32.const 6
            i32.shl
            i32.add
            local.tee $l19
            f32.load offset=60
            local.set $l66
            local.get $p1
            local.get $l36
            f32.store offset=48
            local.get $p1
            local.get $l73
            f32.store offset=12
            local.get $p1
            local.get $l32
            i32.store offset=64
            local.get $p1
            local.get $l30
            i32.store8 offset=1
            local.get $l25
            local.get $p2
            local.get $l24
            i32.load
            i32.const 44
            i32.mul
            i32.add
            i32.load16_u
            i32.const 6
            i32.shl
            i32.add
            local.tee $l10
            f32.load
            local.set $p7
            local.get $l10
            f32.load offset=4
            local.set $p6
            local.get $l10
            f32.load offset=8
            local.set $p3
            local.get $p1
            local.get $l133
            f32.store offset=44
            local.get $p1
            local.get $p3
            f32.store offset=40
            local.get $p1
            local.get $p6
            f32.store offset=36
            local.get $p1
            local.get $p7
            f32.store offset=32
            local.get $l87
            local.get $p7
            local.get $p7
            f32.mul
            local.get $p6
            local.get $p6
            f32.mul
            f32.add
            local.get $p3
            local.get $p3
            f32.mul
            f32.add
            local.tee $l46
            f32.mul
            local.set $l83
            local.get $l73
            local.get $l46
            f32.mul
            local.set $l84
            local.get $p1
            i32.const 80
            i32.add
            local.set $l10
            f32.const 0x1.fffffep+127 (;=3.40282e+38;)
            local.set $l69
            local.get $l24
            i32.load
            local.tee $l11
            i32.const 65535
            i32.ne
            if $I62
              local.get $l82
              local.get $p7
              f32.mul
              local.get $l77
              local.get $p6
              f32.mul
              f32.add
              local.get $l75
              local.get $p3
              f32.mul
              f32.add
              local.set $l78
              local.get $l81
              local.get $p7
              f32.mul
              local.get $l76
              local.get $p6
              f32.mul
              f32.add
              local.get $l74
              local.get $p3
              f32.mul
              f32.add
              local.set $l79
              loop $L63
                local.get $p2
                local.get $l11
                i32.const 44
                i32.mul
                i32.add
                local.tee $l26
                i32.load8_u offset=5
                local.tee $l13
                if $I64
                  local.get $l25
                  local.get $l26
                  i32.load16_u
                  i32.const 6
                  i32.shl
                  i32.add
                  local.set $p0
                  i32.const 0
                  local.set $l12
                  loop $L65
                    local.get $p0
                    local.get $l12
                    i32.const 6
                    i32.shl
                    i32.add
                    local.tee $l11
                    f32.load offset=40
                    local.set $l67
                    local.get $l11
                    f32.load offset=36
                    local.set $l70
                    local.get $l11
                    f32.load offset=32
                    local.set $l80
                    local.get $l11
                    f32.load offset=20
                    local.set $l47
                    local.get $l11
                    f32.load offset=24
                    local.set $l53
                    local.get $l11
                    f32.load offset=16
                    local.set $l49
                    local.get $l11
                    f32.load offset=12
                    local.set $l46
                    local.get $l10
                    local.get $l131
                    f32.store offset=36
                    local.get $l10
                    local.get $l46
                    local.get $l134
                    f32.sub
                    local.tee $l46
                    f32.store offset=12
                    local.get $l10
                    local.get $l115
                    local.get $p6
                    local.get $l49
                    local.get $l106
                    f32.sub
                    local.tee $l51
                    f32.mul
                    local.get $p7
                    local.get $l47
                    local.get $l103
                    f32.sub
                    local.tee $l50
                    f32.mul
                    f32.sub
                    local.tee $l44
                    f32.mul
                    local.get $l121
                    local.get $p3
                    local.get $l50
                    f32.mul
                    local.get $p6
                    local.get $l53
                    local.get $l100
                    f32.sub
                    local.tee $l59
                    f32.mul
                    f32.sub
                    local.tee $l50
                    f32.mul
                    local.get $l118
                    local.get $p7
                    local.get $l59
                    f32.mul
                    local.get $p3
                    local.get $l51
                    f32.mul
                    f32.sub
                    local.tee $l51
                    f32.mul
                    f32.add
                    f32.add
                    local.tee $l59
                    f32.store offset=24
                    local.get $l10
                    local.get $l116
                    local.get $l44
                    f32.mul
                    local.get $l122
                    local.get $l50
                    f32.mul
                    local.get $l119
                    local.get $l51
                    f32.mul
                    f32.add
                    f32.add
                    local.tee $l60
                    f32.store offset=20
                    local.get $l10
                    local.get $l117
                    local.get $l44
                    f32.mul
                    local.get $l40
                    local.get $l50
                    f32.mul
                    local.get $l120
                    local.get $l51
                    f32.mul
                    f32.add
                    f32.add
                    local.tee $l57
                    f32.store offset=16
                    local.get $l10
                    local.get $l123
                    local.get $p6
                    local.get $l49
                    local.get $l105
                    f32.sub
                    local.tee $l49
                    f32.mul
                    local.get $p7
                    local.get $l47
                    local.get $l102
                    f32.sub
                    local.tee $l55
                    f32.mul
                    f32.sub
                    local.tee $l47
                    f32.mul
                    local.get $l129
                    local.get $p3
                    local.get $l55
                    f32.mul
                    local.get $p6
                    local.get $l53
                    local.get $l99
                    f32.sub
                    local.tee $l55
                    f32.mul
                    f32.sub
                    local.tee $l53
                    f32.mul
                    local.get $l126
                    local.get $p7
                    local.get $l55
                    f32.mul
                    local.get $p3
                    local.get $l49
                    f32.mul
                    f32.sub
                    local.tee $l49
                    f32.mul
                    f32.add
                    f32.add
                    local.tee $l55
                    f32.store offset=8
                    local.get $l10
                    local.get $l124
                    local.get $l47
                    f32.mul
                    local.get $l130
                    local.get $l53
                    f32.mul
                    local.get $l127
                    local.get $l49
                    f32.mul
                    f32.add
                    f32.add
                    local.tee $l58
                    f32.store offset=4
                    local.get $l10
                    local.get $l125
                    local.get $l47
                    f32.mul
                    local.get $l45
                    local.get $l53
                    f32.mul
                    local.get $l128
                    local.get $l49
                    f32.mul
                    f32.add
                    f32.add
                    local.tee $l63
                    f32.store
                    local.get $l10
                    f32.const 0x1p+0 (;=1;)
                    local.get $l84
                    local.get $l94
                    local.get $l55
                    local.get $l55
                    f32.mul
                    local.get $l63
                    local.get $l63
                    f32.mul
                    local.get $l58
                    local.get $l58
                    f32.mul
                    f32.add
                    f32.add
                    f32.mul
                    f32.add
                    local.get $l93
                    local.get $l59
                    local.get $l59
                    f32.mul
                    local.get $l57
                    local.get $l57
                    f32.mul
                    local.get $l60
                    local.get $l60
                    f32.mul
                    f32.add
                    f32.add
                    f32.mul
                    local.get $l83
                    f32.sub
                    f32.add
                    local.tee $l59
                    f32.div
                    f32.const 0x0p+0 (;=0;)
                    local.get $l59
                    f32.const 0x0p+0 (;=0;)
                    f32.gt
                    select
                    f32.store offset=28
                    local.get $l10
                    local.get $l78
                    local.get $l35
                    local.get $l44
                    f32.mul
                    local.get $l48
                    local.get $l50
                    f32.mul
                    local.get $l37
                    local.get $l51
                    f32.mul
                    f32.add
                    f32.add
                    f32.add
                    local.tee $l44
                    local.get $p7
                    local.get $l80
                    f32.mul
                    local.get $p6
                    local.get $l70
                    f32.mul
                    f32.add
                    local.get $p3
                    local.get $l67
                    f32.mul
                    f32.add
                    local.get $l66
                    local.get $l79
                    local.get $l38
                    local.get $l47
                    f32.mul
                    local.get $l54
                    local.get $l53
                    f32.mul
                    local.get $l39
                    local.get $l49
                    f32.mul
                    f32.add
                    f32.add
                    f32.add
                    local.tee $l50
                    local.get $l44
                    f32.sub
                    local.tee $l44
                    f32.neg
                    local.tee $l51
                    f32.mul
                    f32.const 0x0p+0 (;=0;)
                    local.get $p5
                    local.get $l44
                    f32.gt
                    select
                    f32.const 0x0p+0 (;=0;)
                    local.get $l66
                    f32.const 0x0p+0 (;=0;)
                    f32.gt
                    select
                    f32.const 0x0p+0 (;=0;)
                    local.get $l46
                    local.get $p4
                    f32.mul
                    local.get $l51
                    f32.lt
                    select
                    f32.add
                    local.tee $l44
                    local.get $l50
                    f32.sub
                    local.get $l44
                    local.get $l22
                    select
                    local.tee $l44
                    f32.add
                    local.get $l44
                    local.get $l27
                    i32.const 255
                    i32.and
                    select
                    f32.store offset=32
                    local.get $l46
                    local.get $l69
                    local.get $l46
                    local.get $l69
                    f32.lt
                    select
                    local.set $l69
                    local.get $l10
                    i32.const 48
                    i32.add
                    local.set $l10
                    local.get $l12
                    i32.const 1
                    i32.add
                    local.tee $l12
                    local.get $l13
                    i32.ne
                    br_if $L65
                  end
                end
                local.get $l26
                i32.load16_u offset=2
                local.tee $l11
                i32.const 65535
                i32.ne
                br_if $L63
              end
            end
            local.get $l10
            i32.const 0
            local.get $l20
            i32.const 2
            i32.shl
            local.tee $l11
            call $f484
            local.set $l10
            local.get $l11
            i32.const 12
            i32.add
            i32.const -16
            i32.and
            local.set $l11
            local.get $l19
            f32.load offset=56
            local.set $l46
            local.get $l19
            f32.load offset=44
            local.set $l44
            block $B66 (result i32)
              block $B67
                block $B68
                  local.get $l19
                  i32.load8_u offset=48
                  i32.const 1
                  i32.and
                  if $I69
                    local.get $p1
                    local.get $l20
                    i32.store8 offset=2
                    br $B68
                  end
                  local.get $p2
                  local.get $l23
                  i32.const 104
                  i32.mul
                  i32.add
                  i32.const 2818
                  i32.add
                  local.tee $l13
                  i32.load16_u
                  local.set $l12
                  local.get $p1
                  local.get $l20
                  i32.store8 offset=2
                  local.get $l12
                  br_if $B67
                end
                i32.const 0
                local.set $l13
                i32.const 0
                br $B66
              end
              local.get $l13
              i32.load8_u
              i32.const 1
              i32.shl
              local.set $l13
              i32.const 1
            end
            local.set $l12
            local.get $l10
            local.get $l11
            i32.add
            local.set $l11
            local.get $p1
            local.get $l87
            f32.store offset=28
            local.get $p1
            local.get $l73
            f32.store offset=24
            local.get $p1
            local.get $l46
            f32.store offset=20
            local.get $p1
            local.get $l44
            f32.store offset=16
            local.get $p1
            local.get $l33
            i32.store8
            local.get $p1
            local.get $l13
            i32.store8 offset=3
            local.get $p1
            i32.const 0
            i32.store offset=56
            local.get $p1
            local.get $l93
            f32.store offset=8
            local.get $p1
            local.get $l94
            f32.store offset=4
            block $B70
              local.get $l12
              i32.eqz
              br_if $B70
              local.get $p1
              local.get $l29
              local.get $l21
              i32.const 104
              i32.mul
              i32.add
              i32.store offset=60
              local.get $p2
              local.get $l23
              i32.const 104
              i32.mul
              i32.add
              local.tee $p0
              i32.const 2818
              i32.add
              local.tee $l26
              i32.load16_u
              local.tee $l13
              i32.eqz
              br_if $B70
              local.get $l75
              local.get $p7
              local.get $l85
              local.get $p6
              local.get $l86
              local.get $p7
              f32.mul
              local.get $l85
              local.get $p6
              f32.mul
              f32.add
              local.get $l91
              local.get $p3
              f32.mul
              f32.add
              local.tee $l46
              f32.mul
              f32.sub
              local.tee $l44
              local.get $p3
              f32.neg
              local.get $p7
              local.get $p7
              f32.abs
              f32.const 0x1.6a09e6p-1 (;=0.707107;)
              f32.lt
              local.tee $l10
              select
              local.get $l91
              local.get $p3
              local.get $l46
              f32.mul
              f32.sub
              local.tee $l50
              local.get $l50
              f32.mul
              local.get $l86
              local.get $p7
              local.get $l46
              f32.mul
              f32.sub
              local.tee $l46
              local.get $l46
              f32.mul
              local.get $l44
              local.get $l44
              f32.mul
              f32.add
              f32.add
              f32.const 0x1.a36e2ep-14 (;=0.0001;)
              f32.gt
              local.tee $l12
              select
              local.tee $l44
              f32.const 0x1p+0 (;=1;)
              local.get $l50
              local.get $p6
              f32.const 0x0p+0 (;=0;)
              local.get $l10
              select
              local.get $l12
              select
              local.tee $l50
              local.get $l50
              f32.mul
              local.get $l46
              f32.const 0x0p+0 (;=0;)
              local.get $p6
              f32.neg
              local.get $l10
              select
              local.get $l12
              select
              local.tee $l51
              local.get $l51
              f32.mul
              local.get $l44
              local.get $l44
              f32.mul
              f32.add
              f32.add
              f32.sqrt
              f32.div
              local.tee $l47
              f32.mul
              local.tee $l46
              f32.mul
              local.get $p6
              local.get $l51
              local.get $l47
              f32.mul
              local.tee $l44
              f32.mul
              f32.sub
              local.tee $l51
              f32.const 0x1p+0 (;=1;)
              local.get $l51
              local.get $l51
              f32.mul
              local.get $p6
              local.get $l50
              local.get $l47
              f32.mul
              local.tee $l50
              f32.mul
              local.get $p3
              local.get $l46
              f32.mul
              f32.sub
              local.tee $l47
              local.get $l47
              f32.mul
              local.get $p3
              local.get $l44
              f32.mul
              local.get $p7
              local.get $l50
              f32.mul
              f32.sub
              local.tee $l53
              local.get $l53
              f32.mul
              f32.add
              f32.add
              f32.sqrt
              f32.div
              local.tee $l49
              f32.mul
              local.tee $l51
              f32.mul
              local.get $l82
              local.get $l47
              local.get $l49
              f32.mul
              local.tee $l47
              f32.mul
              local.get $l77
              local.get $l53
              local.get $l49
              f32.mul
              local.tee $l53
              f32.mul
              f32.add
              f32.add
              local.set $l41
              local.get $l74
              local.get $l51
              f32.mul
              local.get $l81
              local.get $l47
              f32.mul
              local.get $l76
              local.get $l53
              f32.mul
              f32.add
              f32.add
              local.set $l42
              local.get $l75
              local.get $l50
              f32.mul
              local.get $l82
              local.get $l44
              f32.mul
              local.get $l77
              local.get $l46
              f32.mul
              f32.add
              f32.add
              local.set $l43
              local.get $l74
              local.get $l50
              f32.mul
              local.get $l81
              local.get $l44
              f32.mul
              local.get $l76
              local.get $l46
              f32.mul
              f32.add
              f32.add
              local.set $l52
              f32.const 0x1p-1 (;=0.5;)
              f32.const 0x1p+0 (;=1;)
              local.get $l13
              i32.const 2
              i32.eq
              select
              f32.const 0x1p+0 (;=1;)
              local.get $l19
              i32.load8_u offset=48
              i32.const 4
              i32.and
              select
              local.set $l88
              i32.const 0
              local.set $l12
              loop $L71
                local.get $l11
                local.set $l10
                local.get $l109
                local.get $l111
                local.get $p0
                local.get $l12
                i32.const 12
                i32.mul
                i32.add
                local.tee $l11
                i32.const 2880
                i32.add
                f32.load
                local.tee $l60
                f32.mul
                local.get $l110
                local.get $l11
                i32.const 2884
                i32.add
                f32.load
                local.tee $l57
                f32.mul
                f32.add
                local.get $l109
                local.get $l11
                i32.const 2888
                i32.add
                f32.load
                local.tee $l55
                f32.mul
                f32.add
                local.tee $l58
                f32.mul
                local.get $l71
                local.get $l55
                f32.mul
                local.get $l107
                local.get $l111
                local.get $l57
                f32.mul
                local.get $l110
                local.get $l60
                f32.mul
                f32.sub
                f32.mul
                f32.add
                f32.add
                local.tee $l49
                local.get $l49
                f32.add
                local.set $l49
                local.get $l110
                local.get $l58
                f32.mul
                local.get $l71
                local.get $l57
                f32.mul
                local.get $l107
                local.get $l109
                local.get $l60
                f32.mul
                local.get $l111
                local.get $l55
                f32.mul
                f32.sub
                f32.mul
                f32.add
                f32.add
                local.tee $l59
                local.get $l59
                f32.add
                local.set $l59
                local.get $l111
                local.get $l58
                f32.mul
                local.get $l71
                local.get $l60
                f32.mul
                local.get $l107
                local.get $l110
                local.get $l55
                f32.mul
                local.get $l109
                local.get $l57
                f32.mul
                f32.sub
                f32.mul
                f32.add
                f32.add
                local.tee $l60
                local.get $l60
                f32.add
                local.set $l60
                local.get $l112
                local.get $l114
                local.get $l11
                i32.const 2856
                i32.add
                f32.load
                local.tee $l58
                f32.mul
                local.get $l113
                local.get $l11
                i32.const 2860
                i32.add
                f32.load
                local.tee $l63
                f32.mul
                f32.add
                local.get $l112
                local.get $l11
                i32.const 2864
                i32.add
                f32.load
                local.tee $l66
                f32.mul
                f32.add
                local.tee $l67
                f32.mul
                local.get $l72
                local.get $l66
                f32.mul
                local.get $l108
                local.get $l114
                local.get $l63
                f32.mul
                local.get $l113
                local.get $l58
                f32.mul
                f32.sub
                f32.mul
                f32.add
                f32.add
                local.tee $l57
                local.get $l57
                f32.add
                local.set $l57
                local.get $l113
                local.get $l67
                f32.mul
                local.get $l72
                local.get $l63
                f32.mul
                local.get $l108
                local.get $l112
                local.get $l58
                f32.mul
                local.get $l114
                local.get $l66
                f32.mul
                f32.sub
                f32.mul
                f32.add
                f32.add
                local.tee $l55
                local.get $l55
                f32.add
                local.set $l55
                local.get $l84
                local.get $l94
                local.get $l123
                local.get $l46
                local.get $l114
                local.get $l67
                f32.mul
                local.get $l72
                local.get $l58
                f32.mul
                local.get $l108
                local.get $l113
                local.get $l66
                f32.mul
                local.get $l112
                local.get $l63
                f32.mul
                f32.sub
                f32.mul
                f32.add
                f32.add
                local.tee $l58
                local.get $l58
                f32.add
                local.tee $l58
                f32.mul
                local.get $l44
                local.get $l55
                f32.mul
                f32.sub
                local.tee $l66
                f32.mul
                local.get $l129
                local.get $l50
                local.get $l55
                f32.mul
                local.get $l46
                local.get $l57
                f32.mul
                f32.sub
                local.tee $l67
                f32.mul
                local.get $l126
                local.get $l44
                local.get $l57
                f32.mul
                local.get $l50
                local.get $l58
                f32.mul
                f32.sub
                local.tee $l70
                f32.mul
                f32.add
                f32.add
                local.tee $l95
                local.get $l95
                f32.mul
                local.get $l125
                local.get $l66
                f32.mul
                local.get $l45
                local.get $l67
                f32.mul
                local.get $l128
                local.get $l70
                f32.mul
                f32.add
                f32.add
                local.tee $l96
                local.get $l96
                f32.mul
                local.get $l124
                local.get $l66
                f32.mul
                local.get $l130
                local.get $l67
                f32.mul
                local.get $l127
                local.get $l70
                f32.mul
                f32.add
                f32.add
                local.tee $l97
                local.get $l97
                f32.mul
                f32.add
                f32.add
                f32.mul
                f32.add
                local.get $l93
                local.get $l115
                local.get $l46
                local.get $l60
                f32.mul
                local.get $l44
                local.get $l59
                f32.mul
                f32.sub
                local.tee $l80
                f32.mul
                local.get $l121
                local.get $l50
                local.get $l59
                f32.mul
                local.get $l46
                local.get $l49
                f32.mul
                f32.sub
                local.tee $l78
                f32.mul
                local.get $l118
                local.get $l44
                local.get $l49
                f32.mul
                local.get $l50
                local.get $l60
                f32.mul
                f32.sub
                local.tee $l79
                f32.mul
                f32.add
                f32.add
                local.tee $l65
                local.get $l65
                f32.mul
                local.get $l117
                local.get $l80
                f32.mul
                local.get $l40
                local.get $l78
                f32.mul
                local.get $l120
                local.get $l79
                f32.mul
                f32.add
                f32.add
                local.tee $l89
                local.get $l89
                f32.mul
                local.get $l116
                local.get $l80
                f32.mul
                local.get $l122
                local.get $l78
                f32.mul
                local.get $l119
                local.get $l79
                f32.mul
                f32.add
                f32.add
                local.tee $l92
                local.get $l92
                f32.mul
                f32.add
                f32.add
                f32.mul
                local.get $l83
                f32.sub
                f32.add
                local.tee $l63
                f32.const 0x0p+0 (;=0;)
                f32.gt
                local.set $l13
                f32.const 0x1.99999ap-1 (;=0.8;)
                local.get $l63
                f32.div
                local.set $l56
                local.get $l44
                local.get $l25
                local.get $p8
                local.get $l12
                i32.const 1
                i32.shl
                i32.add
                i32.const 7556
                i32.add
                i32.load16_u
                local.tee $l11
                i32.const 65535
                i32.eq
                if $I72 (result i32)
                  local.get $p2
                  local.get $l24
                  i32.load
                  i32.const 44
                  i32.mul
                  i32.add
                  i32.load16_u
                else
                  local.get $l11
                end
                i32.const 65535
                i32.and
                i32.const 6
                i32.shl
                i32.add
                local.tee $l11
                f32.load offset=32
                local.tee $l61
                f32.mul
                local.get $l46
                local.get $l11
                f32.load offset=36
                local.tee $l62
                f32.mul
                f32.add
                local.get $l50
                local.get $l11
                f32.load offset=40
                local.tee $l64
                f32.mul
                f32.add
                local.set $l63
                local.get $l22
                if $I73
                  local.get $l63
                  local.get $l52
                  local.get $l38
                  local.get $l66
                  f32.mul
                  local.get $l54
                  local.get $l67
                  f32.mul
                  local.get $l39
                  local.get $l70
                  f32.mul
                  f32.add
                  f32.add
                  f32.add
                  f32.sub
                  local.set $l63
                end
                local.get $l101
                local.get $l57
                local.get $l49
                f32.sub
                f32.add
                local.set $l66
                local.get $l104
                local.get $l55
                local.get $l59
                f32.sub
                f32.add
                local.set $l67
                local.get $l98
                local.get $l58
                local.get $l60
                f32.sub
                f32.add
                local.set $l70
                local.get $l10
                local.get $l88
                f32.store offset=56
                local.get $l10
                i32.const 0
                i32.store offset=52
                local.get $l10
                local.get $l56
                f32.const 0x0p+0 (;=0;)
                local.get $l13
                select
                f32.store offset=44
                local.get $l10
                local.get $l65
                f32.store offset=40
                local.get $l10
                local.get $l92
                f32.store offset=36
                local.get $l10
                local.get $l89
                f32.store offset=32
                local.get $l10
                local.get $l27
                i32.const 255
                i32.and
                local.tee $l13
                if $I74 (result f32)
                  local.get $l43
                  local.get $l35
                  local.get $l80
                  f32.mul
                  local.get $l48
                  local.get $l78
                  f32.mul
                  local.get $l37
                  local.get $l79
                  f32.mul
                  f32.add
                  f32.add
                  f32.add
                  local.get $l63
                  f32.add
                else
                  local.get $l63
                end
                f32.store offset=28
                local.get $l10
                local.get $l95
                f32.store offset=24
                local.get $l10
                local.get $l97
                f32.store offset=20
                local.get $l10
                local.get $l96
                f32.store offset=16
                local.get $l10
                local.get $l50
                f32.store offset=8
                local.get $l10
                local.get $l46
                f32.store offset=4
                local.get $l10
                local.get $l44
                f32.store
                local.get $l10
                local.get $l68
                f32.store offset=48
                local.get $l10
                local.get $l50
                local.get $l66
                f32.mul
                local.get $l44
                local.get $l70
                f32.mul
                local.get $l46
                local.get $l67
                f32.mul
                f32.add
                f32.add
                f32.store offset=12
                local.get $l84
                local.get $l94
                local.get $l123
                local.get $l53
                local.get $l58
                f32.mul
                local.get $l47
                local.get $l55
                f32.mul
                f32.sub
                local.tee $l63
                f32.mul
                local.get $l129
                local.get $l51
                local.get $l55
                f32.mul
                local.get $l53
                local.get $l57
                f32.mul
                f32.sub
                local.tee $l55
                f32.mul
                local.get $l126
                local.get $l47
                local.get $l57
                f32.mul
                local.get $l51
                local.get $l58
                f32.mul
                f32.sub
                local.tee $l57
                f32.mul
                f32.add
                f32.add
                local.tee $l80
                local.get $l80
                f32.mul
                local.get $l125
                local.get $l63
                f32.mul
                local.get $l45
                local.get $l55
                f32.mul
                local.get $l128
                local.get $l57
                f32.mul
                f32.add
                f32.add
                local.tee $l78
                local.get $l78
                f32.mul
                local.get $l124
                local.get $l63
                f32.mul
                local.get $l130
                local.get $l55
                f32.mul
                local.get $l127
                local.get $l57
                f32.mul
                f32.add
                f32.add
                local.tee $l79
                local.get $l79
                f32.mul
                f32.add
                f32.add
                f32.mul
                f32.add
                local.get $l93
                local.get $l115
                local.get $l53
                local.get $l60
                f32.mul
                local.get $l47
                local.get $l59
                f32.mul
                f32.sub
                local.tee $l58
                f32.mul
                local.get $l121
                local.get $l51
                local.get $l59
                f32.mul
                local.get $l53
                local.get $l49
                f32.mul
                f32.sub
                local.tee $l59
                f32.mul
                local.get $l118
                local.get $l47
                local.get $l49
                f32.mul
                local.get $l51
                local.get $l60
                f32.mul
                f32.sub
                local.tee $l60
                f32.mul
                f32.add
                f32.add
                local.tee $l95
                local.get $l95
                f32.mul
                local.get $l117
                local.get $l58
                f32.mul
                local.get $l40
                local.get $l59
                f32.mul
                local.get $l120
                local.get $l60
                f32.mul
                f32.add
                f32.add
                local.tee $l96
                local.get $l96
                f32.mul
                local.get $l116
                local.get $l58
                f32.mul
                local.get $l122
                local.get $l59
                f32.mul
                local.get $l119
                local.get $l60
                f32.mul
                f32.add
                f32.add
                local.tee $l97
                local.get $l97
                f32.mul
                f32.add
                f32.add
                f32.mul
                local.get $l83
                f32.sub
                f32.add
                local.tee $l49
                f32.const 0x0p+0 (;=0;)
                f32.gt
                local.set $l11
                f32.const 0x1.99999ap-1 (;=0.8;)
                local.get $l49
                f32.div
                local.set $l65
                local.get $l47
                local.get $l61
                f32.mul
                local.get $l53
                local.get $l62
                f32.mul
                f32.add
                local.get $l51
                local.get $l64
                f32.mul
                f32.add
                local.set $l49
                local.get $l22
                if $I75
                  local.get $l49
                  local.get $l42
                  local.get $l38
                  local.get $l63
                  f32.mul
                  local.get $l54
                  local.get $l55
                  f32.mul
                  local.get $l39
                  local.get $l57
                  f32.mul
                  f32.add
                  f32.add
                  f32.add
                  f32.sub
                  local.set $l49
                end
                local.get $l65
                f32.const 0x0p+0 (;=0;)
                local.get $l11
                select
                local.set $l57
                local.get $l10
                i32.const 128
                i32.add
                local.set $l11
                local.get $l10
                local.get $l88
                f32.store offset=120
                local.get $l10
                i32.const 0
                i32.store offset=116
                local.get $l10
                local.get $l57
                f32.store offset=108
                local.get $l10
                local.get $l95
                f32.store offset=104
                local.get $l10
                local.get $l97
                f32.store offset=100
                local.get $l10
                local.get $l96
                f32.store offset=96
                local.get $l10
                local.get $l13
                if $I76 (result f32)
                  local.get $l41
                  local.get $l35
                  local.get $l58
                  f32.mul
                  local.get $l48
                  local.get $l59
                  f32.mul
                  local.get $l37
                  local.get $l60
                  f32.mul
                  f32.add
                  f32.add
                  f32.add
                  local.get $l49
                  f32.add
                else
                  local.get $l49
                end
                f32.store offset=92
                local.get $l10
                local.get $l80
                f32.store offset=88
                local.get $l10
                local.get $l79
                f32.store offset=84
                local.get $l10
                local.get $l78
                f32.store offset=80
                local.get $l10
                local.get $l51
                f32.store offset=72
                local.get $l10
                local.get $l53
                f32.store offset=68
                local.get $l10
                local.get $l47
                f32.store offset=64
                local.get $l10
                local.get $l68
                f32.store offset=112
                local.get $l10
                local.get $l51
                local.get $l66
                f32.mul
                local.get $l47
                local.get $l70
                f32.mul
                local.get $l53
                local.get $l67
                f32.mul
                f32.add
                f32.add
                f32.store offset=76
                local.get $l12
                i32.const 1
                i32.add
                local.tee $l12
                local.get $l26
                i32.load16_u
                local.tee $l19
                i32.lt_u
                br_if $L71
              end
              local.get $l34
              local.get $l19
              i32.const 1
              i32.eq
              i32.and
              i32.eqz
              br_if $B70
              local.get $p1
              local.get $p1
              i32.load8_u offset=3
              i32.const 1
              i32.add
              i32.store8 offset=3
              local.get $l132
              local.get $l69
              f32.neg
              f32.const 0x0p+0 (;=0;)
              f32.max
              f32.mul
              f32.sqrt
              local.set $l66
              local.get $l16
              f32.load offset=8
              local.tee $l51
              local.get $l18
              f32.load
              local.tee $l46
              local.get $p0
              i32.const 2908
              i32.add
              f32.load
              local.tee $l44
              f32.mul
              local.get $l18
              f32.load offset=12
              local.tee $l50
              local.get $p0
              i32.const 2912
              i32.add
              f32.load
              local.tee $l47
              f32.mul
              local.get $p0
              i32.const 2916
              i32.add
              f32.load
              local.tee $l53
              local.get $l18
              f32.load offset=8
              local.tee $l49
              f32.mul
              f32.add
              f32.add
              local.get $p0
              i32.const 2904
              i32.add
              f32.load
              local.tee $l69
              local.get $l18
              f32.load offset=4
              local.tee $l59
              f32.mul
              f32.sub
              local.tee $l60
              f32.mul
              local.get $l50
              local.get $l53
              f32.mul
              local.get $l69
              local.get $l46
              f32.mul
              f32.sub
              local.get $l59
              local.get $l44
              f32.mul
              f32.sub
              local.get $l47
              local.get $l49
              f32.mul
              f32.sub
              local.tee $l57
              local.get $l16
              f32.load offset=12
              local.tee $l55
              f32.mul
              local.get $l16
              f32.load
              local.tee $l58
              local.get $l50
              local.get $l69
              f32.mul
              local.get $l53
              local.get $l46
              f32.mul
              f32.add
              local.get $l59
              local.get $l47
              f32.mul
              f32.add
              local.get $l44
              local.get $l49
              f32.mul
              f32.sub
              local.tee $l63
              f32.mul
              f32.add
              local.get $l53
              local.get $l59
              f32.mul
              local.get $l50
              local.get $l44
              f32.mul
              f32.add
              local.get $l69
              local.get $l49
              f32.mul
              f32.add
              local.get $l46
              local.get $l47
              f32.mul
              f32.sub
              local.tee $l47
              local.get $l16
              f32.load offset=4
              local.tee $l53
              f32.mul
              f32.add
              f32.add
              local.tee $l46
              local.get $l46
              f32.mul
              local.get $l58
              local.get $l57
              f32.mul
              local.get $l63
              local.get $l55
              f32.mul
              f32.sub
              local.get $l47
              local.get $l51
              f32.mul
              f32.sub
              local.get $l60
              local.get $l53
              f32.mul
              f32.add
              local.get $l25
              local.get $p2
              local.get $l24
              i32.load
              i32.const 44
              i32.mul
              i32.add
              i32.load16_u
              i32.const 6
              i32.shl
              i32.add
              local.tee $l11
              f32.load
              local.tee $l67
              f32.mul
              local.tee $l44
              local.get $l44
              f32.mul
              local.get $l63
              local.get $l51
              f32.mul
              local.get $l57
              local.get $l53
              f32.mul
              local.get $l55
              local.get $l47
              f32.mul
              f32.sub
              local.get $l58
              local.get $l60
              f32.mul
              f32.sub
              f32.add
              local.get $l11
              f32.load offset=4
              local.tee $l70
              f32.mul
              local.tee $l50
              local.get $l50
              f32.mul
              f32.add
              local.get $l58
              local.get $l47
              f32.mul
              local.get $l57
              local.get $l51
              f32.mul
              local.get $l55
              local.get $l60
              f32.mul
              f32.sub
              local.get $l63
              local.get $l53
              f32.mul
              f32.sub
              f32.add
              local.get $l11
              f32.load offset=8
              local.tee $l55
              f32.mul
              local.tee $l51
              local.get $l51
              f32.mul
              f32.add
              f32.add
              f32.sqrt
              local.tee $l57
              f32.const 0x0p+0 (;=0;)
              f32.ne
              if $I77
                local.get $l46
                f32.const 0x1p+0 (;=1;)
                local.get $l57
                f32.div
                local.tee $l47
                f32.mul
                local.set $l46
                local.get $l50
                local.get $l47
                f32.mul
                local.set $l50
                local.get $l44
                local.get $l47
                f32.mul
                local.set $l44
                local.get $l51
                local.get $l47
                f32.mul
                local.set $l51
              end
              local.get $l94
              local.get $l129
              local.get $p7
              f32.mul
              local.get $l126
              local.get $p6
              f32.mul
              f32.add
              local.get $l123
              local.get $p3
              f32.mul
              f32.add
              local.tee $l47
              local.get $l47
              f32.mul
              local.get $l45
              local.get $p7
              f32.mul
              local.get $l128
              local.get $p6
              f32.mul
              f32.add
              local.get $l125
              local.get $p3
              f32.mul
              f32.add
              local.tee $l53
              local.get $l53
              f32.mul
              local.get $l130
              local.get $p7
              f32.mul
              local.get $l127
              local.get $p6
              f32.mul
              f32.add
              local.get $l124
              local.get $p3
              f32.mul
              f32.add
              local.tee $l49
              local.get $l49
              f32.mul
              f32.add
              f32.add
              f32.mul
              local.get $l93
              local.get $l121
              local.get $p7
              f32.mul
              local.get $l118
              local.get $p6
              f32.mul
              f32.add
              local.get $l115
              local.get $p3
              f32.mul
              f32.add
              local.tee $l69
              local.get $l69
              f32.mul
              local.get $l40
              local.get $p7
              f32.mul
              local.get $l120
              local.get $p6
              f32.mul
              f32.add
              local.get $l117
              local.get $p3
              f32.mul
              f32.add
              local.tee $l59
              local.get $l59
              f32.mul
              local.get $l122
              local.get $p7
              f32.mul
              local.get $l119
              local.get $p6
              f32.mul
              f32.add
              local.get $l116
              local.get $p3
              f32.mul
              f32.add
              local.tee $l60
              local.get $l60
              f32.mul
              f32.add
              f32.add
              f32.mul
              f32.add
              local.tee $l58
              f32.const 0x0p+0 (;=0;)
              f32.gt
              local.set $l12
              local.get $l67
              local.get $l44
              f32.mul
              local.get $l70
              local.get $l50
              f32.mul
              f32.add
              local.get $l55
              local.get $l51
              f32.mul
              f32.add
              local.get $l46
              f32.const 0x0p+0 (;=0;)
              f32.mul
              f32.add
              local.get $l46
              f32.div
              f32.const 0x0p+0 (;=0;)
              local.get $l57
              f32.const -0x1.0c6f7ap-20 (;=-1e-06;)
              f32.add
              f32.const 0x0p+0 (;=0;)
              f32.ge
              select
              call $f18178
              local.set $l44
              local.get $l10
              i32.const 192
              i32.add
              local.set $l11
              local.get $l10
              local.get $l90
              local.get $l66
              local.get $l66
              local.get $l90
              f32.lt
              select
              f32.store offset=184
              local.get $l10
              i32.const 0
              i32.store offset=180
              local.get $l10
              local.get $l68
              f32.store offset=176
              local.get $l10
              f32.const 0x1.99999ap-1 (;=0.8;)
              local.get $l58
              f32.div
              f32.const 0x0p+0 (;=0;)
              local.get $l12
              select
              f32.store offset=172
              local.get $l10
              local.get $l69
              f32.store offset=168
              local.get $l10
              local.get $l60
              f32.store offset=164
              local.get $l10
              local.get $l59
              f32.store offset=160
              local.get $l10
              local.get $l48
              local.get $p7
              f32.mul
              local.get $l37
              local.get $p6
              f32.mul
              f32.add
              local.get $l35
              local.get $p3
              f32.mul
              f32.add
              local.get $l54
              local.get $p7
              f32.mul
              local.get $l39
              local.get $p6
              f32.mul
              f32.add
              local.get $l38
              local.get $p3
              f32.mul
              f32.add
              f32.const 0x0p+0 (;=0;)
              local.get $l22
              select
              local.get $l13
              select
              f32.store offset=156
              local.get $l10
              local.get $l47
              f32.store offset=152
              local.get $l10
              local.get $l49
              f32.store offset=148
              local.get $l10
              local.get $l53
              f32.store offset=144
              local.get $l10
              i32.const 0
              i32.store offset=136
              local.get $l10
              i64.const 0
              i64.store offset=128
              local.get $l10
              local.get $l44
              f32.neg
              f32.store offset=140
            end
            local.get $l21
            i32.const 1
            i32.add
            local.set $l21
            local.get $p2
            i32.load offset=7688
            local.set $l10
            local.get $l11
            local.set $p1
          end
          local.get $l23
          i32.const 1
          i32.add
          local.tee $l23
          local.get $l10
          i32.lt_u
          br_if $L60
        end
      end
      local.get $l28
      local.get $l31
      i32.add
      i32.const 0
      i32.store
    end
    local.get $l14
    i32.const 32
    i32.add
    global.set $g0
    local.get $l17
    i32.const 32
    i32.add
    global.set $g0)
