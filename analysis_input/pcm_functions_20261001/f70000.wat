  (func $f70000 (type $t0) (param $p0 i32) (param $p1 i32) (result i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32) (local $l33 f32) (local $l34 f32) (local $l35 f32) (local $l36 f32) (local $l37 f32) (local $l38 f32) (local $l39 f32) (local $l40 f32) (local $l41 f32) (local $l42 f32) (local $l43 f32) (local $l44 f32) (local $l45 f32) (local $l46 f32) (local $l47 f32) (local $l48 f32) (local $l49 f32) (local $l50 f32) (local $l51 f32)
    global.get $g0
    i32.const 192
    i32.sub
    local.tee $l2
    global.set $g0
    block $B0
      block $B1 (result f32)
        local.get $p0
        i32.load offset=184
        local.tee $l6
        block $B2 (result i32)
          local.get $p0
          i32.load offset=176
          local.tee $l3
          if $I3
            local.get $l3
            local.get $p1
            i32.const 12
            i32.mul
            i32.add
            local.tee $l3
            i32.load offset=8
            local.set $l5
            local.get $l3
            i32.load offset=4
            local.set $l7
            local.get $l3
            i32.load
            br $B2
          end
          local.get $p0
          i32.load offset=180
          local.get $p1
          i32.const 6
          i32.mul
          i32.add
          local.tee $l3
          i32.load16_u offset=4
          local.set $l5
          local.get $l3
          i32.load16_u offset=2
          local.set $l7
          local.get $l3
          i32.load16_u
        end
        i32.const 12
        i32.mul
        i32.add
        local.tee $l3
        f32.load offset=4
        local.tee $l12
        local.get $l6
        local.get $l7
        i32.const 12
        i32.mul
        i32.add
        local.tee $l7
        f32.load offset=4
        local.tee $l20
        f32.sub
        local.tee $l8
        local.get $l3
        f32.load offset=8
        local.tee $l13
        local.get $l6
        local.get $l5
        i32.const 12
        i32.mul
        i32.add
        local.tee $l6
        f32.load offset=8
        local.tee $l10
        f32.sub
        local.tee $l11
        f32.mul
        local.get $l13
        local.get $l7
        f32.load offset=8
        local.tee $l22
        f32.sub
        local.tee $l9
        local.get $l12
        local.get $l6
        f32.load offset=4
        local.tee $l24
        f32.sub
        local.tee $l14
        f32.mul
        f32.sub
        local.tee $l36
        local.get $p0
        f32.load offset=248
        local.tee $l26
        f32.mul
        local.get $l9
        local.get $l3
        f32.load
        local.tee $l27
        local.get $l6
        f32.load
        local.tee $l17
        f32.sub
        local.tee $l18
        f32.mul
        local.get $l27
        local.get $l7
        f32.load
        local.tee $l15
        f32.sub
        local.tee $l9
        local.get $l11
        f32.mul
        f32.sub
        local.tee $l37
        local.get $p0
        f32.load offset=252
        local.tee $l32
        f32.mul
        f32.add
        local.get $l9
        local.get $l14
        f32.mul
        local.get $l8
        local.get $l18
        f32.mul
        f32.sub
        local.tee $l38
        local.get $p0
        f32.load offset=256
        local.tee $l33
        f32.mul
        f32.add
        f32.const 0x0p+0 (;=0;)
        f32.gt
        i32.eqz
        if $I4
          local.get $l10
          local.set $l28
          local.get $l24
          local.set $l19
          local.get $l17
          local.set $l16
          local.get $l22
          local.set $l10
          local.get $l20
          local.set $l24
          local.get $l15
          local.set $l17
          local.get $l36
          local.set $l30
          local.get $l37
          local.set $l31
          local.get $l38
          br $B1
        end
        i32.const 0
        local.set $l5
        local.get $p0
        i32.load offset=268
        br_if $B0
        local.get $l37
        f32.neg
        local.set $l31
        local.get $l36
        f32.neg
        local.set $l30
        local.get $l22
        local.set $l28
        local.get $l20
        local.set $l19
        local.get $l15
        local.set $l16
        local.get $l38
        f32.neg
      end
      local.set $l40
      local.get $p0
      i32.const 248
      i32.add
      local.set $l4
      local.get $p0
      f32.load offset=508
      local.set $l34
      local.get $l2
      local.get $p0
      f32.load offset=260
      f32.store offset=188
      local.get $p0
      f32.load offset=520
      local.set $l22
      local.get $p0
      f32.load offset=516
      local.set $l15
      local.get $p0
      f32.load offset=512
      local.set $l25
      local.get $l2
      i32.const 0
      i32.store8 offset=187
      local.get $p0
      f32.load offset=528
      local.set $l8
      local.get $p0
      f32.load offset=524
      local.set $l11
      local.get $l2
      local.get $l13
      local.get $p0
      f32.load offset=532
      local.tee $l9
      f32.sub
      local.tee $l14
      f32.store offset=176
      local.get $l2
      local.get $l12
      local.get $l8
      f32.sub
      local.tee $l18
      f32.store offset=172
      local.get $l2
      local.get $l27
      local.get $l11
      f32.sub
      local.tee $l20
      f32.store offset=168
      local.get $l2
      local.get $l10
      local.get $l9
      f32.sub
      local.tee $l21
      f32.store offset=160
      local.get $l2
      local.get $l24
      local.get $l8
      f32.sub
      local.tee $l23
      f32.store offset=156
      local.get $l2
      local.get $l17
      local.get $l11
      f32.sub
      local.tee $l29
      f32.store offset=152
      local.get $l2
      local.get $l28
      local.get $l9
      f32.sub
      local.tee $l39
      f32.store offset=144
      local.get $l2
      local.get $l19
      local.get $l8
      f32.sub
      local.tee $l45
      f32.store offset=140
      local.get $l2
      local.get $l16
      local.get $l11
      f32.sub
      local.tee $l46
      f32.store offset=136
      local.get $l2
      local.get $l13
      local.get $l9
      f32.add
      local.tee $l41
      f32.store offset=128
      local.get $l2
      local.get $l12
      local.get $l8
      f32.add
      local.tee $l42
      f32.store offset=124
      local.get $l2
      local.get $l27
      local.get $l11
      f32.add
      local.tee $l27
      f32.store offset=120
      local.get $l2
      local.get $l9
      local.get $l10
      f32.add
      local.tee $l12
      f32.store offset=112
      local.get $l2
      local.get $l8
      local.get $l24
      f32.add
      local.tee $l13
      f32.store offset=108
      local.get $l2
      local.get $l11
      local.get $l17
      f32.add
      local.tee $l10
      f32.store offset=104
      local.get $l2
      local.get $l11
      local.get $l16
      f32.add
      local.tee $l16
      f32.store offset=88
      local.get $l2
      local.get $l9
      local.get $l28
      f32.add
      local.tee $l17
      f32.store offset=96
      local.get $l2
      local.get $l8
      local.get $l19
      f32.add
      local.tee $l35
      f32.store offset=92
      local.get $l2
      local.get $l27
      local.get $l10
      f32.sub
      local.tee $l24
      local.get $l17
      local.get $l12
      f32.sub
      local.tee $l17
      f32.mul
      local.get $l41
      local.get $l12
      f32.sub
      local.tee $l28
      local.get $l16
      local.get $l10
      f32.sub
      local.tee $l19
      f32.mul
      f32.sub
      local.tee $l43
      f32.store offset=76
      local.get $l2
      local.get $l28
      local.get $l35
      local.get $l13
      f32.sub
      local.tee $l16
      f32.mul
      local.get $l42
      local.get $l13
      f32.sub
      local.tee $l35
      local.get $l17
      f32.mul
      f32.sub
      local.tee $l47
      f32.store offset=72
      local.get $l2
      local.get $l35
      local.get $l19
      f32.mul
      local.get $l24
      local.get $l16
      f32.mul
      f32.sub
      local.tee $l48
      f32.store offset=80
      local.get $l2
      local.get $l20
      local.get $l29
      f32.sub
      local.tee $l12
      local.get $l39
      local.get $l21
      f32.sub
      local.tee $l13
      f32.mul
      local.get $l14
      local.get $l21
      f32.sub
      local.tee $l10
      local.get $l46
      local.get $l29
      f32.sub
      local.tee $l44
      f32.mul
      f32.sub
      local.tee $l49
      f32.store offset=60
      local.get $l2
      local.get $l10
      local.get $l45
      local.get $l23
      f32.sub
      local.tee $l50
      f32.mul
      local.get $l18
      local.get $l23
      f32.sub
      local.tee $l10
      local.get $l13
      f32.mul
      f32.sub
      local.tee $l51
      f32.store offset=56
      local.get $l2
      local.get $l10
      local.get $l44
      f32.mul
      local.get $l12
      local.get $l50
      f32.mul
      f32.sub
      local.tee $l44
      f32.store offset=64
      local.get $l26
      local.get $l25
      f32.mul
      local.get $l32
      local.get $l15
      f32.mul
      f32.add
      local.get $l33
      local.get $l22
      f32.mul
      f32.add
      local.set $l26
      local.get $l9
      local.get $l9
      f32.add
      local.set $l12
      local.get $l8
      local.get $l8
      f32.add
      local.set $l13
      local.get $l11
      local.get $l11
      f32.add
      local.set $l10
      block $B5 (result i32)
        local.get $l30
        local.get $l11
        f32.mul
        local.get $l31
        local.get $l8
        f32.mul
        f32.add
        local.get $l40
        local.get $l9
        f32.mul
        f32.add
        local.tee $l11
        f32.const 0x0p+0 (;=0;)
        f32.ge
        if $I6
          local.get $p0
          local.get $l2
          i32.const 120
          i32.add
          local.get $l2
          i32.const 104
          i32.add
          local.get $l2
          i32.const 88
          i32.add
          local.get $l2
          i32.const 72
          i32.add
          local.get $l4
          local.get $l34
          local.get $l26
          local.get $l2
          i32.const 188
          i32.add
          local.get $l2
          i32.const 187
          i32.add
          call $f70001
          br $B5
        end
        local.get $p0
        local.get $l2
        i32.const 168
        i32.add
        local.get $l2
        i32.const 152
        i32.add
        local.get $l2
        i32.const 136
        i32.add
        local.get $l2
        i32.const 56
        i32.add
        local.get $l4
        local.get $l34
        local.get $l26
        local.get $l2
        i32.const 188
        i32.add
        local.get $l2
        i32.const 187
        i32.add
        call $f70001
      end
      local.set $l5
      local.get $l15
      local.get $l42
      f32.sub
      local.set $l32
      local.get $l25
      local.get $l27
      f32.sub
      local.set $l33
      local.get $l15
      local.get $l18
      f32.sub
      local.set $l30
      local.get $l25
      local.get $l20
      f32.sub
      local.set $l31
      local.get $l2
      local.get $l10
      local.get $l16
      f32.mul
      local.get $l13
      local.get $l19
      f32.mul
      f32.sub
      local.tee $l25
      f32.store offset=48
      local.get $l2
      local.get $l12
      local.get $l19
      f32.mul
      local.get $l10
      local.get $l17
      f32.mul
      f32.sub
      local.tee $l19
      f32.store offset=44
      local.get $l2
      local.get $l13
      local.get $l17
      f32.mul
      local.get $l12
      local.get $l16
      f32.mul
      f32.sub
      local.tee $l16
      f32.store offset=40
      local.get $p0
      f32.load offset=516
      local.tee $l8
      local.get $l23
      f32.sub
      local.set $l23
      local.get $p0
      f32.load offset=512
      local.tee $l9
      local.get $l29
      f32.sub
      local.set $l29
      block $B7 (result f32)
        local.get $p0
        f32.load offset=520
        local.tee $l15
        local.get $l5
        br_if $B7
        drop
        local.get $l15
        local.get $l11
        local.get $l16
        local.get $p0
        f32.load offset=248
        f32.mul
        local.get $l19
        local.get $p0
        f32.load offset=252
        f32.mul
        f32.add
        local.get $l25
        local.get $p0
        f32.load offset=256
        f32.mul
        f32.add
        f32.mul
        f32.const 0x0p+0 (;=0;)
        f32.ge
        i32.eqz
        br_if $B7
        drop
        local.get $p0
        local.get $l2
        i32.const 152
        i32.add
        local.get $l2
        i32.const 104
        i32.add
        local.get $l2
        i32.const 136
        i32.add
        local.get $l2
        i32.const 88
        i32.add
        local.get $l2
        i32.const 40
        i32.add
        local.get $l4
        local.get $l34
        local.get $l26
        local.get $l2
        i32.const 188
        i32.add
        local.get $l2
        i32.const 187
        i32.add
        call $f70002
        local.get $p0
        f32.load offset=516
        local.set $l8
        local.get $p0
        f32.load offset=512
        local.set $l9
        local.get $p0
        f32.load offset=520
      end
      local.set $l17
      local.get $l32
      local.get $l43
      f32.mul
      local.set $l32
      local.get $l33
      local.get $l47
      f32.mul
      local.set $l33
      local.get $l22
      local.get $l41
      f32.sub
      local.set $l40
      local.get $l30
      local.get $l49
      f32.mul
      local.set $l30
      local.get $l31
      local.get $l51
      f32.mul
      local.set $l31
      local.get $l22
      local.get $l14
      f32.sub
      local.set $l43
      local.get $l19
      local.get $l23
      f32.mul
      local.set $l23
      local.get $l16
      local.get $l29
      f32.mul
      local.set $l29
      local.get $l15
      local.get $l21
      f32.sub
      local.set $l19
      local.get $l2
      local.get $l10
      local.get $l18
      local.get $l45
      f32.sub
      local.tee $l21
      f32.mul
      local.get $l13
      local.get $l20
      local.get $l46
      f32.sub
      local.tee $l15
      f32.mul
      f32.sub
      local.tee $l22
      f32.store offset=32
      local.get $l2
      local.get $l12
      local.get $l15
      f32.mul
      local.get $l10
      local.get $l14
      local.get $l39
      f32.sub
      local.tee $l16
      f32.mul
      f32.sub
      local.tee $l15
      f32.store offset=28
      local.get $l2
      local.get $l13
      local.get $l16
      f32.mul
      local.get $l12
      local.get $l21
      f32.mul
      f32.sub
      local.tee $l21
      f32.store offset=24
      local.get $l21
      local.get $l9
      local.get $l20
      f32.sub
      f32.mul
      local.set $l20
      local.get $l15
      local.get $l8
      local.get $l18
      f32.sub
      f32.mul
      local.set $l18
      local.get $l17
      local.get $l14
      f32.sub
      local.set $l14
      block $B8
        local.get $l5
        br_if $B8
        local.get $l11
        local.get $l21
        local.get $p0
        f32.load offset=248
        f32.mul
        local.get $l15
        local.get $p0
        f32.load offset=252
        f32.mul
        f32.add
        local.get $l22
        local.get $p0
        f32.load offset=256
        f32.mul
        f32.add
        f32.mul
        f32.const 0x0p+0 (;=0;)
        f32.ge
        i32.eqz
        br_if $B8
        local.get $p0
        local.get $l2
        i32.const 136
        i32.add
        local.get $l2
        i32.const 88
        i32.add
        local.get $l2
        i32.const 168
        i32.add
        local.get $l2
        i32.const 120
        i32.add
        local.get $l2
        i32.const 24
        i32.add
        local.get $l4
        local.get $l34
        local.get $l26
        local.get $l2
        i32.const 188
        i32.add
        local.get $l2
        i32.const 187
        i32.add
        call $f70002
        local.get $p0
        f32.load offset=520
        local.set $l17
        local.get $p0
        f32.load offset=516
        local.set $l8
        local.get $p0
        f32.load offset=512
        local.set $l9
      end
      local.get $l33
      local.get $l32
      f32.add
      local.set $l15
      local.get $l40
      local.get $l48
      f32.mul
      local.set $l21
      local.get $l31
      local.get $l30
      f32.add
      local.set $l16
      local.get $l43
      local.get $l44
      f32.mul
      local.set $l39
      local.get $l29
      local.get $l23
      f32.add
      local.set $l23
      local.get $l25
      local.get $l19
      f32.mul
      local.set $l25
      local.get $l18
      local.get $l20
      f32.add
      local.set $l18
      local.get $l22
      local.get $l14
      f32.mul
      local.set $l20
      local.get $l2
      local.get $l13
      local.get $l24
      f32.mul
      local.get $l10
      local.get $l35
      f32.mul
      f32.sub
      local.tee $l14
      f32.store offset=16
      local.get $l2
      local.get $l10
      local.get $l28
      f32.mul
      local.get $l12
      local.get $l24
      f32.mul
      f32.sub
      local.tee $l10
      f32.store offset=12
      local.get $l2
      local.get $l12
      local.get $l35
      f32.mul
      local.get $l13
      local.get $l28
      f32.mul
      f32.sub
      local.tee $l12
      f32.store offset=8
      local.get $l10
      local.get $l8
      local.get $l42
      f32.sub
      f32.mul
      local.get $l12
      local.get $l9
      local.get $l27
      f32.sub
      f32.mul
      f32.add
      local.set $l8
      local.get $l14
      local.get $l17
      local.get $l41
      f32.sub
      f32.mul
      local.set $l9
      block $B9
        local.get $l5
        br_if $B9
        local.get $l11
        local.get $l12
        local.get $p0
        f32.load offset=248
        f32.mul
        local.get $l10
        local.get $p0
        f32.load offset=252
        f32.mul
        f32.add
        local.get $l14
        local.get $p0
        f32.load offset=256
        f32.mul
        f32.add
        f32.mul
        f32.const 0x0p+0 (;=0;)
        f32.ge
        i32.eqz
        br_if $B9
        local.get $p0
        local.get $l2
        i32.const 168
        i32.add
        local.get $l2
        i32.const 120
        i32.add
        local.get $l2
        i32.const 152
        i32.add
        local.get $l2
        i32.const 104
        i32.add
        local.get $l2
        i32.const 8
        i32.add
        local.get $l4
        local.get $l34
        local.get $l26
        local.get $l2
        i32.const 188
        i32.add
        local.get $l2
        i32.const 187
        i32.add
        call $f70002
      end
      local.get $l21
      local.get $l15
      f32.add
      local.set $l12
      local.get $l39
      local.get $l16
      f32.add
      local.set $l13
      local.get $l23
      local.get $l25
      f32.add
      local.set $l10
      local.get $l20
      local.get $l18
      f32.add
      local.set $l14
      local.get $l9
      local.get $l8
      f32.add
      local.set $l9
      f32.const 0x0p+0 (;=0;)
      local.set $l8
      block $B10
        block $B11
          local.get $l11
          f32.const 0x0p+0 (;=0;)
          f32.lt
          if $I12
            local.get $l12
            f32.const 0x0p+0 (;=0;)
            f32.le
            br_if $B11
            local.get $l13
            f32.const 0x0p+0 (;=0;)
            f32.ge
            br_if $B11
            local.get $l10
            f32.const 0x0p+0 (;=0;)
            f32.ge
            br_if $B11
            local.get $l14
            f32.const 0x0p+0 (;=0;)
            f32.ge
            br_if $B11
            i32.const 1
            local.set $l4
            local.get $l9
            f32.const 0x0p+0 (;=0;)
            f32.ge
            br_if $B11
            br $B10
          end
          local.get $l12
          f32.const 0x0p+0 (;=0;)
          f32.ge
          br_if $B11
          local.get $l13
          f32.const 0x0p+0 (;=0;)
          f32.le
          br_if $B11
          local.get $l10
          f32.const 0x0p+0 (;=0;)
          f32.le
          br_if $B11
          local.get $l14
          f32.const 0x0p+0 (;=0;)
          f32.le
          br_if $B11
          i32.const 1
          local.set $l4
          local.get $l9
          f32.const 0x0p+0 (;=0;)
          f32.le
          i32.eqz
          br_if $B10
        end
        local.get $l2
        i32.load8_u offset=187
        i32.const 0
        i32.ne
        local.set $l4
        local.get $l2
        f32.load offset=188
        local.set $l8
      end
      i32.const 0
      local.set $l5
      local.get $l4
      i32.eqz
      br_if $B0
      local.get $l8
      local.get $p0
      f32.load offset=544
      f32.gt
      br_if $B0
      local.get $l36
      local.get $p0
      f32.load offset=248
      local.tee $l13
      f32.mul
      local.get $l37
      local.get $p0
      f32.load offset=252
      local.tee $l10
      f32.mul
      f32.add
      local.get $l38
      local.get $p0
      f32.load offset=256
      local.tee $l14
      f32.mul
      f32.add
      f32.abs
      f32.neg
      local.set $l9
      block $B13
        local.get $p0
        f32.load offset=540
        local.tee $l11
        local.get $l8
        local.get $l11
        local.get $l8
        local.get $l11
        f32.gt
        local.tee $l4
        select
        f32.const 0x1p+0 (;=1;)
        f32.max
        f32.const 0x1.0624dep-10 (;=0.001;)
        f32.mul
        local.tee $l12
        f32.sub
        local.get $l8
        f32.gt
        br_if $B13
        local.get $l9
        local.get $p0
        f32.load offset=536
        local.tee $l18
        f32.lt
        local.get $l11
        local.get $l12
        f32.add
        local.get $l8
        f32.gt
        i32.and
        br_if $B13
        local.get $l8
        f32.const 0x0p+0 (;=0;)
        f32.eq
        br_if $B13
        local.get $l9
        local.get $l18
        f32.eq
        local.get $l8
        local.get $l11
        f32.lt
        i32.and
        i32.eqz
        br_if $B0
      end
      local.get $p0
      local.get $l8
      f32.store offset=260
      local.get $p0
      local.get $p1
      i32.store offset=264
      local.get $p0
      local.get $l3
      f32.load
      f32.store offset=276
      local.get $p0
      local.get $l3
      f32.load offset=4
      f32.store offset=280
      local.get $p0
      local.get $l3
      f32.load offset=8
      f32.store offset=284
      local.get $p0
      local.get $l7
      f32.load
      f32.store offset=288
      local.get $p0
      local.get $l7
      f32.load offset=4
      f32.store offset=292
      local.get $p0
      local.get $l7
      f32.load offset=8
      f32.store offset=296
      local.get $p0
      local.get $l6
      f32.load
      f32.store offset=300
      local.get $p0
      local.get $l6
      f32.load offset=4
      f32.store offset=304
      local.get $l6
      f32.load offset=8
      local.set $l12
      local.get $p0
      local.get $l11
      local.get $l8
      local.get $l4
      select
      f32.store offset=540
      local.get $p0
      local.get $l12
      f32.store offset=308
      local.get $p0
      local.get $l9
      f32.store offset=536
      local.get $p0
      local.get $l38
      f32.store offset=320
      local.get $p0
      local.get $l37
      f32.store offset=316
      local.get $p0
      local.get $l36
      f32.store offset=312
      i32.const 1
      local.set $l5
      local.get $p0
      local.get $l8
      local.get $p0
      f32.load offset=328
      f32.mul
      local.get $p0
      f32.load offset=340
      f32.add
      local.tee $l11
      f32.store offset=64
      local.get $p0
      local.get $l8
      local.get $l14
      f32.mul
      f32.const 0x1p-1 (;=0.5;)
      f32.mul
      local.get $p0
      f32.load offset=232
      f32.add
      f32.store offset=40
      local.get $p0
      local.get $l8
      local.get $l10
      f32.mul
      f32.const 0x1p-1 (;=0.5;)
      f32.mul
      local.get $p0
      f32.load offset=228
      f32.add
      f32.store offset=36
      local.get $p0
      local.get $l8
      local.get $l13
      f32.mul
      f32.const 0x1p-1 (;=0.5;)
      f32.mul
      local.get $p0
      f32.load offset=224
      f32.add
      f32.store offset=32
      local.get $p0
      local.get $l8
      local.get $p0
      f32.load offset=336
      f32.mul
      local.get $p0
      f32.load offset=348
      f32.add
      local.tee $l9
      f32.store offset=72
      local.get $p0
      local.get $l8
      local.get $p0
      f32.load offset=332
      f32.mul
      local.get $p0
      f32.load offset=344
      f32.add
      local.tee $l8
      f32.store offset=68
      local.get $p0
      local.get $l11
      local.get $p0
      f32.load offset=352
      f32.mul
      local.get $l8
      local.get $p0
      f32.load offset=364
      f32.mul
      f32.add
      local.get $l9
      local.get $p0
      f32.load offset=376
      f32.mul
      f32.add
      f32.store offset=48
      local.get $p0
      local.get $l11
      local.get $p0
      f32.load offset=356
      f32.mul
      local.get $l8
      local.get $p0
      f32.load offset=368
      f32.mul
      f32.add
      local.get $l9
      local.get $p0
      f32.load offset=380
      f32.mul
      f32.add
      f32.store offset=52
      local.get $p0
      local.get $l11
      local.get $p0
      f32.load offset=360
      f32.mul
      local.get $l8
      local.get $p0
      f32.load offset=372
      f32.mul
      f32.add
      local.get $l9
      local.get $p0
      f32.load offset=384
      f32.mul
      f32.add
      f32.store offset=56
    end
    local.get $l2
    i32.const 192
    i32.add
    global.set $g0
    local.get $l5)
