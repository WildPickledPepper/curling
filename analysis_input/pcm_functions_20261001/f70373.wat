  (func $f70373 (type $t418) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 f32) (param $p5 i32) (param $p6 i32) (param $p7 i32) (param $p8 i32) (result i32)
    (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32) (local $l33 f32) (local $l34 f32) (local $l35 f32) (local $l36 f32) (local $l37 f32) (local $l38 f32) (local $l39 f32) (local $l40 f32) (local $l41 f32) (local $l42 f32) (local $l43 f32) (local $l44 f32)
    global.get $g0
    i32.const 896
    i32.sub
    local.tee $l9
    global.set $g0
    block $B0
      block $B1
        local.get $p8
        i32.load8_u
        i32.const 16
        i32.and
        br_if $B1
        local.get $l9
        local.get $p1
        f32.load offset=4
        local.tee $l13
        local.get $l13
        f32.add
        local.tee $l17
        local.get $p1
        f32.load offset=8
        local.tee $l12
        f32.mul
        local.tee $l14
        local.get $p1
        f32.load
        local.tee $l18
        local.get $l18
        f32.add
        local.tee $l15
        local.get $p1
        f32.load offset=12
        local.tee $l19
        f32.mul
        local.tee $l16
        f32.sub
        f32.store offset=492
        local.get $l9
        local.get $l14
        local.get $l16
        f32.add
        f32.store offset=484
        local.get $l9
        f32.const 0x1p+0 (;=1;)
        local.get $l18
        local.get $l15
        f32.mul
        f32.sub
        local.tee $l18
        local.get $l13
        local.get $l17
        f32.mul
        local.tee $l14
        f32.sub
        f32.store offset=496
        local.get $l9
        local.get $l18
        local.get $l12
        local.get $l12
        local.get $l12
        f32.add
        local.tee $l16
        f32.mul
        local.tee $l20
        f32.sub
        f32.store offset=480
        local.get $l9
        local.get $l15
        local.get $l12
        f32.mul
        local.tee $l12
        local.get $l17
        local.get $l19
        f32.mul
        local.tee $l17
        f32.add
        f32.store offset=488
        local.get $l9
        local.get $l15
        local.get $l13
        f32.mul
        local.tee $l13
        local.get $l16
        local.get $l19
        f32.mul
        local.tee $l15
        f32.sub
        f32.store offset=476
        local.get $l9
        local.get $l12
        local.get $l17
        f32.sub
        f32.store offset=472
        local.get $l9
        local.get $l13
        local.get $l15
        f32.add
        f32.store offset=468
        local.get $l9
        f32.const 0x1p+0 (;=1;)
        local.get $l14
        f32.sub
        local.get $l20
        f32.sub
        f32.store offset=464
        local.get $p0
        local.get $p0
        i32.const 12
        i32.add
        local.get $p1
        i32.const 16
        i32.add
        local.get $p2
        local.get $l9
        i32.const 464
        i32.add
        i32.const 0
        i32.const 0
        call $f69889
        local.get $p0
        f32.load offset=24
        local.tee $l12
        local.get $l12
        f32.mul
        f32.lt
        i32.eqz
        br_if $B1
        local.get $p6
        i32.const 0
        i32.store
        local.get $p3
        f32.load
        local.set $l12
        local.get $p3
        f32.load offset=4
        local.set $l13
        local.get $p7
        local.get $p3
        f32.load offset=8
        f32.neg
        f32.store offset=8
        local.get $p7
        local.get $l13
        f32.neg
        f32.store offset=4
        local.get $p7
        local.get $l12
        f32.neg
        f32.store
        i32.const 1
        local.set $p2
        br $B0
      end
      local.get $p0
      f32.load offset=16
      local.set $l15
      local.get $p0
      f32.load offset=20
      local.set $l17
      local.get $p0
      f32.load
      local.set $l31
      local.get $p0
      f32.load offset=12
      local.set $l32
      local.get $p0
      f32.load offset=4
      local.set $l18
      local.get $p0
      f32.load offset=8
      local.set $l19
      local.get $p2
      f32.load
      local.set $l12
      local.get $p2
      f32.load offset=4
      local.set $l13
      local.get $l9
      local.get $p2
      f32.load offset=8
      local.tee $l14
      f32.store offset=28
      local.get $l9
      local.get $l13
      f32.store offset=24
      local.get $l9
      local.get $l12
      f32.store offset=20
      local.get $l9
      local.get $l14
      f32.neg
      f32.store offset=16
      local.get $l9
      local.get $l13
      f32.neg
      f32.store offset=12
      local.get $l9
      local.get $l12
      f32.neg
      f32.store offset=8
      local.get $l9
      i32.const 1
      i32.store8 offset=4
      local.get $l9
      i32.const 3024
      i32.const 3128744
      i32.const 198
      call $f70043
      local.tee $p2
      i32.store
      local.get $l17
      local.get $l19
      f32.sub
      local.set $l22
      local.get $l15
      local.get $l18
      f32.sub
      f32.const 0x1p-1 (;=0.5;)
      f32.mul
      local.set $l36
      local.get $l9
      i32.const 8
      i32.add
      local.get $l9
      i32.const 368
      i32.add
      call $f70399
      local.get $p1
      f32.load offset=12
      local.tee $l17
      local.get $l17
      f32.mul
      f32.const -0x1p-1 (;=-0.5;)
      f32.add
      local.set $l18
      local.get $p1
      f32.load offset=24
      local.set $l20
      local.get $p1
      f32.load offset=20
      local.set $l25
      local.get $p1
      f32.load offset=16
      local.set $l26
      local.get $p1
      f32.load offset=8
      local.set $l12
      local.get $p1
      f32.load offset=4
      local.set $l13
      local.get $p1
      f32.load
      local.set $l15
      i32.const 0
      local.set $p8
      loop $L2
        local.get $l9
        i32.const 368
        i32.add
        local.get $p8
        i32.const 3
        i32.mul
        local.tee $l10
        i32.const 3128800
        i32.add
        i32.load8_u
        i32.const 12
        i32.mul
        i32.add
        local.tee $p1
        f32.load offset=8
        local.set $l23
        local.get $p1
        f32.load
        local.set $l34
        local.get $p1
        f32.load offset=4
        local.set $l35
        local.get $l9
        i32.const 368
        i32.add
        local.get $l10
        i32.const 3128801
        i32.add
        i32.load8_u
        i32.const 12
        i32.mul
        i32.add
        local.tee $p1
        f32.load offset=8
        local.set $l21
        local.get $p1
        f32.load
        local.set $l24
        local.get $p1
        f32.load offset=4
        local.set $l29
        local.get $l9
        i32.const 464
        i32.add
        local.get $p8
        i32.const 36
        i32.mul
        i32.add
        local.tee $p1
        local.get $l20
        local.get $l9
        i32.const 368
        i32.add
        local.get $l10
        i32.const 3128802
        i32.add
        i32.load8_u
        i32.const 12
        i32.mul
        i32.add
        local.tee $l10
        f32.load offset=8
        local.tee $l19
        local.get $l19
        f32.add
        local.tee $l19
        local.get $l18
        f32.mul
        local.get $l17
        local.get $l10
        f32.load offset=4
        local.tee $l14
        local.get $l14
        f32.add
        local.tee $l14
        local.get $l15
        f32.mul
        local.get $l10
        f32.load
        local.tee $l16
        local.get $l16
        f32.add
        local.tee $l16
        local.get $l13
        f32.mul
        f32.sub
        f32.mul
        f32.add
        local.get $l12
        local.get $l16
        local.get $l15
        f32.mul
        local.get $l14
        local.get $l13
        f32.mul
        f32.add
        local.get $l19
        local.get $l12
        f32.mul
        f32.add
        local.tee $l30
        f32.mul
        f32.add
        f32.add
        f32.store offset=32
        local.get $p1
        local.get $l25
        local.get $l13
        local.get $l30
        f32.mul
        local.get $l14
        local.get $l18
        f32.mul
        local.get $l17
        local.get $l16
        local.get $l12
        f32.mul
        local.get $l19
        local.get $l15
        f32.mul
        f32.sub
        f32.mul
        f32.add
        f32.add
        f32.add
        f32.store offset=28
        local.get $p1
        local.get $l26
        local.get $l15
        local.get $l30
        f32.mul
        local.get $l16
        local.get $l18
        f32.mul
        local.get $l17
        local.get $l19
        local.get $l13
        f32.mul
        local.get $l14
        local.get $l12
        f32.mul
        f32.sub
        f32.mul
        f32.add
        f32.add
        f32.add
        f32.store offset=24
        local.get $p1
        local.get $l20
        local.get $l21
        local.get $l21
        f32.add
        local.tee $l19
        local.get $l18
        f32.mul
        local.get $l17
        local.get $l29
        local.get $l29
        f32.add
        local.tee $l14
        local.get $l15
        f32.mul
        local.get $l24
        local.get $l24
        f32.add
        local.tee $l16
        local.get $l13
        f32.mul
        f32.sub
        f32.mul
        f32.add
        local.get $l12
        local.get $l16
        local.get $l15
        f32.mul
        local.get $l14
        local.get $l13
        f32.mul
        f32.add
        local.get $l19
        local.get $l12
        f32.mul
        f32.add
        local.tee $l21
        f32.mul
        f32.add
        f32.add
        f32.store offset=20
        local.get $p1
        local.get $l25
        local.get $l13
        local.get $l21
        f32.mul
        local.get $l14
        local.get $l18
        f32.mul
        local.get $l17
        local.get $l16
        local.get $l12
        f32.mul
        local.get $l19
        local.get $l15
        f32.mul
        f32.sub
        f32.mul
        f32.add
        f32.add
        f32.add
        f32.store offset=16
        local.get $p1
        local.get $l26
        local.get $l15
        local.get $l21
        f32.mul
        local.get $l16
        local.get $l18
        f32.mul
        local.get $l17
        local.get $l19
        local.get $l13
        f32.mul
        local.get $l14
        local.get $l12
        f32.mul
        f32.sub
        f32.mul
        f32.add
        f32.add
        f32.add
        f32.store offset=12
        local.get $p1
        local.get $l20
        local.get $l23
        local.get $l23
        f32.add
        local.tee $l19
        local.get $l18
        f32.mul
        local.get $l17
        local.get $l35
        local.get $l35
        f32.add
        local.tee $l14
        local.get $l15
        f32.mul
        local.get $l34
        local.get $l34
        f32.add
        local.tee $l16
        local.get $l13
        f32.mul
        f32.sub
        f32.mul
        f32.add
        local.get $l12
        local.get $l16
        local.get $l15
        f32.mul
        local.get $l14
        local.get $l13
        f32.mul
        f32.add
        local.get $l19
        local.get $l12
        f32.mul
        f32.add
        local.tee $l23
        f32.mul
        f32.add
        f32.add
        f32.store offset=8
        local.get $p1
        local.get $l25
        local.get $l13
        local.get $l23
        f32.mul
        local.get $l14
        local.get $l18
        f32.mul
        local.get $l17
        local.get $l16
        local.get $l12
        f32.mul
        local.get $l19
        local.get $l15
        f32.mul
        f32.sub
        f32.mul
        f32.add
        f32.add
        f32.add
        f32.store offset=4
        local.get $p1
        local.get $l26
        local.get $l15
        local.get $l23
        f32.mul
        local.get $l16
        local.get $l18
        f32.mul
        local.get $l17
        local.get $l19
        local.get $l13
        f32.mul
        local.get $l14
        local.get $l12
        f32.mul
        f32.sub
        f32.mul
        f32.add
        f32.add
        f32.add
        f32.store
        local.get $p8
        i32.const 1
        i32.add
        local.tee $p8
        i32.const 12
        i32.ne
        br_if $L2
      end
      local.get $l22
      f32.const 0x1p-1 (;=0.5;)
      f32.mul
      local.set $l34
      local.get $l32
      local.get $l31
      f32.sub
      f32.const 0x1p-1 (;=0.5;)
      f32.mul
      local.set $l35
      i32.const 0
      local.set $p8
      local.get $l9
      i32.const 32
      i32.add
      local.set $l10
      loop $L3
        local.get $l9
        i32.const 464
        i32.add
        local.get $p8
        i32.const 36
        i32.mul
        i32.add
        local.tee $p1
        f32.load offset=12
        local.tee $l30
        local.get $p1
        f32.load
        local.tee $l14
        f32.sub
        local.tee $l12
        local.get $p1
        f32.load offset=28
        local.tee $l22
        local.get $p1
        f32.load offset=4
        local.tee $l16
        f32.sub
        local.tee $l13
        f32.mul
        local.get $p1
        f32.load offset=16
        local.tee $l32
        local.get $l16
        f32.sub
        local.tee $l15
        local.get $p1
        f32.load offset=24
        local.tee $l27
        local.get $l14
        f32.sub
        local.tee $l17
        f32.mul
        f32.sub
        local.tee $l37
        local.get $p3
        f32.load offset=8
        f32.mul
        local.get $p3
        f32.load
        local.get $l15
        local.get $p1
        f32.load offset=32
        local.tee $l28
        local.get $p1
        f32.load offset=8
        local.tee $l20
        f32.sub
        local.tee $l18
        f32.mul
        local.get $p1
        f32.load offset=20
        local.tee $l31
        local.get $l20
        f32.sub
        local.tee $l15
        local.get $l13
        f32.mul
        f32.sub
        local.tee $l33
        f32.mul
        local.get $p3
        f32.load offset=4
        local.get $l15
        local.get $l17
        f32.mul
        local.get $l12
        local.get $l18
        f32.mul
        f32.sub
        local.tee $l38
        f32.mul
        f32.add
        f32.add
        f32.const 0x0p+0 (;=0;)
        f32.gt
        i32.eqz
        if $I4
          local.get $l28
          local.get $l34
          f32.sub
          local.set $l21
          local.get $l22
          local.get $l36
          f32.sub
          local.set $l24
          local.get $l27
          local.get $l35
          f32.sub
          local.set $l29
          local.get $l31
          local.get $l34
          f32.sub
          local.set $l12
          local.get $l32
          local.get $l36
          f32.sub
          local.set $l13
          local.get $l30
          local.get $l35
          f32.sub
          local.set $l15
          local.get $l20
          local.get $l34
          f32.sub
          local.set $l17
          local.get $l16
          local.get $l36
          f32.sub
          local.set $l18
          local.get $l14
          local.get $l35
          f32.sub
          local.set $l19
          local.get $l35
          local.get $l14
          f32.add
          local.tee $l25
          local.set $l39
          local.get $l36
          local.get $l16
          f32.add
          local.tee $l26
          local.set $l40
          local.get $l34
          local.get $l20
          f32.add
          local.tee $l23
          local.set $l41
          local.get $l35
          local.get $l30
          f32.add
          local.tee $l30
          local.set $l42
          local.get $l36
          local.get $l32
          f32.add
          local.tee $l32
          local.set $l43
          local.get $l34
          local.get $l31
          f32.add
          local.tee $l31
          local.set $l44
          local.get $l35
          local.get $l27
          f32.add
          local.tee $l14
          local.set $l27
          local.get $l36
          local.get $l22
          f32.add
          local.tee $l16
          local.set $l22
          local.get $l34
          local.get $l28
          f32.add
          local.tee $l20
          local.set $l28
          local.get $l34
          local.get $l37
          f32.mul
          local.get $l35
          local.get $l33
          f32.mul
          local.get $l36
          local.get $l38
          f32.mul
          f32.add
          f32.add
          f32.const 0x0p+0 (;=0;)
          f32.ge
          i32.eqz
          if $I5
            local.get $l19
            local.set $l39
            local.get $l18
            local.set $l40
            local.get $l17
            local.set $l41
            local.get $l15
            local.set $l42
            local.get $l13
            local.set $l43
            local.get $l12
            local.set $l44
            local.get $l29
            local.set $l27
            local.get $l21
            local.set $l28
            local.get $l24
            local.set $l22
          end
          local.get $p2
          local.get $l27
          f32.store offset=24
          local.get $p2
          local.get $l42
          f32.store offset=12
          local.get $p2
          local.get $l41
          f32.store offset=8
          local.get $p2
          local.get $l40
          f32.store offset=4
          local.get $p2
          local.get $l39
          f32.store
          local.get $p2
          local.get $l28
          f32.store offset=32
          local.get $p2
          local.get $l22
          f32.store offset=28
          local.get $p2
          local.get $l44
          f32.store offset=20
          local.get $p2
          local.get $l43
          f32.store offset=16
          local.get $l10
          local.get $p8
          i32.store
          local.get $p2
          local.get $l20
          f32.store offset=68
          local.get $p2
          i32.const -64
          i32.sub
          local.get $l16
          f32.store
          local.get $p2
          local.get $l14
          f32.store offset=60
          local.get $p2
          local.get $l31
          f32.store offset=56
          local.get $p2
          local.get $l32
          f32.store offset=52
          local.get $p2
          local.get $l30
          f32.store offset=48
          local.get $p2
          local.get $l12
          f32.store offset=44
          local.get $p2
          local.get $l13
          f32.store offset=40
          local.get $p2
          local.get $l15
          f32.store offset=36
          local.get $l30
          local.get $l15
          f32.sub
          local.tee $l37
          local.get $l16
          local.get $l13
          f32.sub
          local.tee $l22
          f32.mul
          local.get $l32
          local.get $l13
          f32.sub
          local.tee $l33
          local.get $l14
          local.get $l15
          f32.sub
          local.tee $l27
          f32.mul
          f32.sub
          local.get $p3
          f32.load offset=8
          f32.mul
          local.get $l33
          local.get $l20
          local.get $l12
          f32.sub
          local.tee $l28
          f32.mul
          local.get $l31
          local.get $l12
          f32.sub
          local.tee $l33
          local.get $l22
          f32.mul
          f32.sub
          local.get $p3
          f32.load
          f32.mul
          local.get $l33
          local.get $l27
          f32.mul
          local.get $l37
          local.get $l28
          f32.mul
          f32.sub
          local.get $p3
          f32.load offset=4
          f32.mul
          f32.add
          f32.add
          f32.const 0x0p+0 (;=0;)
          f32.gt
          if $I6
            local.get $p2
            local.get $l31
            f32.store offset=68
            local.get $p2
            local.get $l32
            f32.store offset=64
            local.get $p2
            local.get $l30
            f32.store offset=60
            local.get $p2
            local.get $l20
            f32.store offset=56
            local.get $p2
            local.get $l16
            f32.store offset=52
            local.get $p2
            local.get $l14
            f32.store offset=48
          end
          local.get $l10
          local.get $p8
          i32.store offset=4
          local.get $p2
          local.get $l21
          f32.store offset=104
          local.get $p2
          local.get $l24
          f32.store offset=100
          local.get $p2
          local.get $l29
          f32.store offset=96
          local.get $p2
          local.get $l20
          f32.store offset=92
          local.get $p2
          local.get $l16
          f32.store offset=88
          local.get $p2
          local.get $l14
          f32.store offset=84
          local.get $p2
          local.get $l12
          f32.store offset=80
          local.get $p2
          local.get $l13
          f32.store offset=76
          local.get $p2
          local.get $l15
          f32.store offset=72
          local.get $l27
          local.get $l24
          local.get $l13
          f32.sub
          local.tee $l37
          f32.mul
          local.get $l29
          local.get $l15
          f32.sub
          local.tee $l33
          local.get $l22
          f32.mul
          f32.sub
          local.get $p3
          f32.load offset=8
          f32.mul
          local.get $l22
          local.get $l21
          local.get $l12
          f32.sub
          local.tee $l38
          f32.mul
          local.get $l37
          local.get $l28
          f32.mul
          f32.sub
          local.get $p3
          f32.load
          f32.mul
          local.get $l33
          local.get $l28
          f32.mul
          local.get $l27
          local.get $l38
          f32.mul
          f32.sub
          local.get $p3
          f32.load offset=4
          f32.mul
          f32.add
          f32.add
          f32.const 0x0p+0 (;=0;)
          f32.gt
          if $I7
            local.get $p2
            local.get $l20
            f32.store offset=104
            local.get $p2
            local.get $l16
            f32.store offset=100
            local.get $p2
            local.get $l14
            f32.store offset=96
            local.get $p2
            local.get $l21
            f32.store offset=92
            local.get $p2
            local.get $l24
            f32.store offset=88
            local.get $p2
            local.get $l29
            f32.store offset=84
          end
          local.get $l10
          local.get $p8
          i32.store offset=8
          local.get $p2
          local.get $l20
          f32.store offset=140
          local.get $p2
          local.get $l16
          f32.store offset=136
          local.get $p2
          local.get $l14
          f32.store offset=132
          local.get $p2
          local.get $l21
          f32.store offset=128
          local.get $p2
          local.get $l24
          f32.store offset=124
          local.get $p2
          local.get $l29
          f32.store offset=120
          local.get $p2
          local.get $l17
          f32.store offset=116
          local.get $p2
          local.get $l18
          f32.store offset=112
          local.get $p2
          local.get $l19
          f32.store offset=108
          local.get $l29
          local.get $l19
          f32.sub
          local.tee $l37
          local.get $l16
          local.get $l18
          f32.sub
          local.tee $l22
          f32.mul
          local.get $l14
          local.get $l19
          f32.sub
          local.tee $l27
          local.get $l24
          local.get $l18
          f32.sub
          local.tee $l33
          f32.mul
          f32.sub
          local.get $p3
          f32.load offset=8
          f32.mul
          local.get $l33
          local.get $l20
          local.get $l17
          f32.sub
          local.tee $l28
          f32.mul
          local.get $l22
          local.get $l21
          local.get $l17
          f32.sub
          local.tee $l33
          f32.mul
          f32.sub
          local.get $p3
          f32.load
          f32.mul
          local.get $l27
          local.get $l33
          f32.mul
          local.get $l37
          local.get $l28
          f32.mul
          f32.sub
          local.get $p3
          f32.load offset=4
          f32.mul
          f32.add
          f32.add
          f32.const 0x0p+0 (;=0;)
          f32.gt
          if $I8
            local.get $p2
            local.get $l21
            f32.store offset=140
            local.get $p2
            local.get $l24
            f32.store offset=136
            local.get $p2
            local.get $l29
            f32.store offset=132
            local.get $p2
            local.get $l20
            f32.store offset=128
            local.get $p2
            local.get $l16
            f32.store offset=124
            local.get $p2
            local.get $l14
            f32.store offset=120
          end
          local.get $l10
          local.get $p8
          i32.store offset=12
          local.get $p2
          local.get $l23
          f32.store offset=176
          local.get $p2
          local.get $l26
          f32.store offset=172
          local.get $p2
          local.get $l25
          f32.store offset=168
          local.get $p2
          local.get $l20
          f32.store offset=164
          local.get $p2
          local.get $l16
          f32.store offset=160
          local.get $p2
          local.get $l14
          f32.store offset=156
          local.get $p2
          local.get $l17
          f32.store offset=152
          local.get $p2
          local.get $l18
          f32.store offset=148
          local.get $p2
          local.get $l19
          f32.store offset=144
          local.get $l26
          local.get $l18
          f32.sub
          local.tee $l21
          local.get $l27
          f32.mul
          local.get $l25
          local.get $l19
          f32.sub
          local.tee $l24
          local.get $l22
          f32.mul
          f32.sub
          local.get $p3
          f32.load offset=8
          f32.mul
          local.get $l23
          local.get $l17
          f32.sub
          local.tee $l29
          local.get $l22
          f32.mul
          local.get $l21
          local.get $l28
          f32.mul
          f32.sub
          local.get $p3
          f32.load
          f32.mul
          local.get $l24
          local.get $l28
          f32.mul
          local.get $l29
          local.get $l27
          f32.mul
          f32.sub
          local.get $p3
          f32.load offset=4
          f32.mul
          f32.add
          f32.add
          f32.const 0x0p+0 (;=0;)
          f32.gt
          if $I9
            local.get $p2
            local.get $l20
            f32.store offset=176
            local.get $p2
            local.get $l16
            f32.store offset=172
            local.get $p2
            local.get $l14
            f32.store offset=168
            local.get $p2
            local.get $l23
            f32.store offset=164
            local.get $p2
            local.get $l26
            f32.store offset=160
            local.get $p2
            local.get $l25
            f32.store offset=156
          end
          local.get $l10
          local.get $p8
          i32.store offset=16
          local.get $p2
          local.get $l12
          f32.store offset=212
          local.get $p2
          local.get $l13
          f32.store offset=208
          local.get $p2
          local.get $l15
          f32.store offset=204
          local.get $p2
          local.get $l31
          f32.store offset=200
          local.get $p2
          local.get $l32
          f32.store offset=196
          local.get $p2
          local.get $l30
          f32.store offset=192
          local.get $p2
          local.get $l23
          f32.store offset=188
          local.get $p2
          local.get $l26
          f32.store offset=184
          local.get $p2
          local.get $l25
          f32.store offset=180
          local.get $l30
          local.get $l25
          f32.sub
          local.tee $l21
          local.get $l13
          local.get $l26
          f32.sub
          local.tee $l14
          f32.mul
          local.get $l15
          local.get $l25
          f32.sub
          local.tee $l16
          local.get $l32
          local.get $l26
          f32.sub
          local.tee $l24
          f32.mul
          f32.sub
          local.get $p3
          f32.load offset=8
          f32.mul
          local.get $l24
          local.get $l12
          local.get $l23
          f32.sub
          local.tee $l20
          f32.mul
          local.get $l14
          local.get $l31
          local.get $l23
          f32.sub
          local.tee $l24
          f32.mul
          f32.sub
          local.get $p3
          f32.load
          f32.mul
          local.get $l16
          local.get $l24
          f32.mul
          local.get $l21
          local.get $l20
          f32.mul
          f32.sub
          local.get $p3
          f32.load offset=4
          f32.mul
          f32.add
          f32.add
          f32.const 0x0p+0 (;=0;)
          f32.gt
          if $I10
            local.get $p2
            local.get $l31
            f32.store offset=212
            local.get $p2
            local.get $l32
            f32.store offset=208
            local.get $p2
            local.get $l30
            f32.store offset=204
            local.get $p2
            local.get $l12
            f32.store offset=200
            local.get $p2
            local.get $l13
            f32.store offset=196
            local.get $p2
            local.get $l15
            f32.store offset=192
          end
          local.get $l10
          local.get $p8
          i32.store offset=20
          local.get $p2
          local.get $l17
          f32.store offset=248
          local.get $p2
          local.get $l18
          f32.store offset=244
          local.get $p2
          local.get $l19
          f32.store offset=240
          local.get $p2
          local.get $l12
          f32.store offset=236
          local.get $p2
          local.get $l13
          f32.store offset=232
          local.get $p2
          local.get $l15
          f32.store offset=228
          local.get $p2
          local.get $l23
          f32.store offset=224
          local.get $p2
          local.get $l26
          f32.store offset=220
          local.get $p2
          local.get $l25
          f32.store offset=216
          local.get $l16
          local.get $l18
          local.get $l26
          f32.sub
          local.tee $l26
          f32.mul
          local.get $l19
          local.get $l25
          f32.sub
          local.tee $l25
          local.get $l14
          f32.mul
          f32.sub
          local.get $p3
          f32.load offset=8
          f32.mul
          local.get $l14
          local.get $l17
          local.get $l23
          f32.sub
          local.tee $l23
          f32.mul
          local.get $l26
          local.get $l20
          f32.mul
          f32.sub
          local.get $p3
          f32.load
          f32.mul
          local.get $l25
          local.get $l20
          f32.mul
          local.get $l16
          local.get $l23
          f32.mul
          f32.sub
          local.get $p3
          f32.load offset=4
          f32.mul
          f32.add
          f32.add
          f32.const 0x0p+0 (;=0;)
          f32.gt
          if $I11
            local.get $p2
            local.get $l12
            f32.store offset=248
            local.get $p2
            local.get $l13
            f32.store offset=244
            local.get $p2
            local.get $l15
            f32.store offset=240
            local.get $p2
            local.get $l17
            f32.store offset=236
            local.get $p2
            local.get $l18
            f32.store offset=232
            local.get $p2
            local.get $l19
            f32.store offset=228
          end
          local.get $l10
          local.get $p8
          i32.store offset=24
          local.get $l10
          i32.const 28
          i32.add
          local.set $l10
          local.get $p2
          i32.const 252
          i32.add
          local.set $p2
        end
        local.get $p8
        i32.const 1
        i32.add
        local.tee $p8
        i32.const 12
        i32.ne
        br_if $L3
      end
      local.get $l9
      i32.const 488
      i32.add
      local.tee $p8
      i64.const 0
      i64.store
      local.get $l9
      i32.const 496
      i32.add
      local.tee $l11
      i64.const 0
      i64.store
      local.get $l9
      i64.const 0
      i64.store offset=480
      local.get $l9
      i32.const 0
      i32.store16 offset=476
      local.get $l9
      i32.const -1
      i32.store offset=472
      local.get $l9
      i64.const 0
      i64.store offset=464
      local.get $l9
      i32.const 2139095039
      i32.store offset=504
      local.get $l9
      i32.load
      local.set $p1
      local.get $p0
      f32.load offset=12
      local.set $l12
      local.get $p0
      f32.load
      local.set $l13
      local.get $p0
      f32.load offset=16
      local.set $l15
      local.get $p0
      f32.load offset=4
      local.set $l17
      local.get $l9
      local.get $p0
      f32.load offset=8
      local.get $p0
      f32.load offset=20
      f32.add
      f32.const 0x1p-1 (;=0.5;)
      f32.mul
      f32.store offset=376
      local.get $l9
      local.get $l17
      local.get $l15
      f32.add
      f32.const 0x1p-1 (;=0.5;)
      f32.mul
      f32.store offset=372
      local.get $l9
      local.get $l13
      local.get $l12
      f32.add
      f32.const 0x1p-1 (;=0.5;)
      f32.mul
      f32.store offset=368
      local.get $l10
      local.get $l9
      i32.const 32
      i32.add
      i32.sub
      i32.const 2
      i32.shr_s
      local.get $p1
      local.get $l9
      i32.const 368
      i32.add
      local.get $p0
      f32.load offset=24
      local.get $p3
      local.get $p4
      i32.const 0
      local.get $l9
      i32.const 464
      i32.add
      local.get $l9
      i32.const 32
      i32.add
      i32.const 0
      i32.const 0
      i32.const 0
      i32.const 0
      call $f69963
      local.tee $p2
      if $I12
        local.get $p5
        local.get $l9
        f32.load offset=480
        f32.store
        local.get $p5
        local.get $l9
        f32.load offset=484
        f32.store offset=4
        local.get $p5
        local.get $p8
        f32.load
        f32.store offset=8
        local.get $l9
        f32.load offset=504
        local.set $p4
        local.get $p7
        local.get $l9
        f32.load offset=492
        f32.store
        local.get $p7
        local.get $l11
        f32.load
        f32.store offset=4
        local.get $p7
        local.get $l9
        f32.load offset=500
        f32.store offset=8
      end
      local.get $l9
      i32.load8_u offset=4
      if $I13
        local.get $p1
        call $f70044
      end
      local.get $p6
      local.get $p4
      f32.store
    end
    local.get $l9
    i32.const 896
    i32.add
    global.set $g0
    local.get $p2)
