  (func $f70552 (type $t18) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 i32) (param $p7 i32) (result i32)
    (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32) (local $l33 f32) (local $l34 f32) (local $l35 i32) (local $l36 i32) (local $l37 i32) (local $l38 i32) (local $l39 i32) (local $l40 i32) (local $l41 i32) (local $l42 i32) (local $l43 i32) (local $l44 i32) (local $l45 i32) (local $l46 i32) (local $l47 i32) (local $l48 i32) (local $l49 i32) (local $l50 i32)
    global.get $g0
    i32.const 144
    i32.sub
    local.tee $p5
    global.set $g0
    local.get $p0
    f32.load offset=8
    local.set $l8
    local.get $p2
    f32.load offset=20
    local.set $l12
    local.get $p3
    f32.load offset=20
    local.set $l13
    local.get $p2
    f32.load offset=16
    local.set $l21
    local.get $p3
    f32.load offset=16
    local.set $l30
    local.get $p2
    f32.load offset=8
    local.set $l14
    local.get $p2
    f32.load
    local.set $l9
    local.get $p2
    f32.load offset=4
    local.set $l15
    local.get $p2
    f32.load offset=12
    local.set $l10
    local.get $p5
    local.get $p3
    f32.load offset=24
    local.get $p2
    f32.load offset=24
    f32.sub
    local.tee $l22
    local.get $p1
    f32.load offset=8
    local.tee $l19
    local.get $p3
    f32.load
    local.tee $l23
    local.get $l23
    f32.add
    local.tee $l24
    local.get $p3
    f32.load offset=8
    local.tee $l25
    f32.mul
    local.get $p3
    f32.load offset=12
    local.tee $l20
    local.get $l20
    f32.add
    local.tee $l28
    local.get $p3
    f32.load offset=4
    local.tee $l27
    f32.mul
    f32.sub
    f32.mul
    local.tee $l11
    f32.sub
    local.tee $l31
    f32.store offset=92
    local.get $p5
    local.get $l13
    local.get $l12
    f32.sub
    local.tee $l12
    local.get $l19
    local.get $l25
    local.get $l28
    f32.mul
    local.get $l24
    local.get $l27
    f32.mul
    f32.add
    f32.mul
    local.tee $l13
    f32.sub
    local.tee $l27
    f32.store offset=88
    local.get $p5
    local.get $l11
    local.get $l22
    f32.add
    local.tee $l32
    f32.store offset=80
    local.get $p5
    local.get $l13
    local.get $l12
    f32.add
    local.tee $l33
    f32.store offset=76
    local.get $p5
    local.get $l11
    f32.const -0x1p+1 (;=-2;)
    f32.mul
    local.tee $l12
    f32.store offset=116
    local.get $p5
    local.get $l13
    f32.const -0x1p+1 (;=-2;)
    f32.mul
    local.tee $l13
    f32.store offset=112
    local.get $p5
    local.get $l8
    local.get $l14
    local.get $l9
    local.get $l9
    f32.add
    local.tee $l22
    f32.mul
    local.get $l15
    local.get $l10
    local.get $l10
    f32.add
    local.tee $l25
    f32.mul
    f32.sub
    f32.mul
    local.tee $l11
    f32.store offset=56
    local.get $p5
    local.get $l11
    f32.neg
    local.tee $l29
    f32.store offset=68
    local.get $p5
    local.get $l8
    local.get $l14
    local.get $l25
    f32.mul
    local.get $l22
    local.get $l15
    f32.mul
    f32.add
    f32.mul
    local.tee $l14
    f32.store offset=52
    local.get $p5
    i32.const -64
    i32.sub
    local.get $l14
    f32.neg
    local.tee $l26
    f32.store
    local.get $p5
    local.get $l30
    local.get $l21
    f32.sub
    local.tee $l21
    local.get $l19
    local.get $l23
    local.get $l24
    f32.mul
    local.get $l20
    local.get $l28
    f32.mul
    f32.const -0x1p+0 (;=-1;)
    f32.add
    f32.add
    f32.mul
    local.tee $l19
    f32.sub
    local.tee $l23
    f32.store offset=84
    local.get $p5
    local.get $l11
    f32.const -0x1p+1 (;=-2;)
    f32.mul
    local.tee $l16
    f32.store offset=104
    local.get $p5
    local.get $l14
    f32.const -0x1p+1 (;=-2;)
    f32.mul
    local.tee $l17
    f32.store offset=100
    local.get $p5
    local.get $l19
    f32.const -0x1p+1 (;=-2;)
    f32.mul
    local.tee $l15
    f32.store offset=108
    local.get $p5
    local.get $l8
    local.get $l9
    local.get $l22
    f32.mul
    local.get $l10
    local.get $l25
    f32.mul
    f32.const -0x1p+0 (;=-1;)
    f32.add
    f32.add
    f32.mul
    local.tee $l8
    f32.store offset=48
    local.get $p5
    local.get $l8
    f32.const -0x1p+1 (;=-2;)
    f32.mul
    local.tee $l18
    f32.store offset=96
    local.get $p5
    local.get $l19
    local.get $l21
    f32.add
    local.tee $l9
    f32.store offset=72
    local.get $p5
    local.get $l8
    f32.neg
    local.tee $l10
    f32.store offset=60
    local.get $p5
    local.get $l29
    local.get $l11
    f32.sub
    f32.store offset=8
    local.get $p5
    local.get $l26
    local.get $l14
    f32.sub
    f32.store offset=4
    local.get $p5
    local.get $l10
    local.get $l8
    f32.sub
    f32.store
    local.get $p5
    local.get $l31
    local.get $l32
    f32.sub
    f32.store offset=136
    local.get $p5
    local.get $l27
    local.get $l33
    f32.sub
    f32.store offset=132
    local.get $p5
    local.get $l23
    local.get $l9
    f32.sub
    f32.store offset=128
    block $B0
      local.get $p5
      i32.const 48
      i32.add
      local.get $p5
      local.get $p5
      i32.const 72
      i32.add
      local.get $p5
      i32.const 128
      i32.add
      local.get $p5
      i32.const 44
      i32.add
      local.get $p5
      i32.const 40
      i32.add
      call $f69892
      local.tee $l34
      local.get $p0
      f32.load offset=4
      local.get $p1
      f32.load offset=4
      f32.add
      local.tee $l29
      local.get $p4
      f32.load
      f32.add
      local.tee $l8
      local.get $l8
      f32.mul
      local.tee $l30
      f32.ge
      local.tee $l39
      br_if $B0
      local.get $p5
      local.get $l15
      local.get $l15
      f32.mul
      local.get $l13
      local.get $l13
      f32.mul
      f32.add
      local.get $l12
      local.get $l12
      f32.mul
      f32.add
      f32.sqrt
      local.tee $l8
      f32.store offset=132
      local.get $p5
      local.get $l18
      local.get $l18
      f32.mul
      local.get $l17
      local.get $l17
      f32.mul
      f32.add
      local.get $l16
      local.get $l16
      f32.mul
      f32.add
      f32.sqrt
      local.tee $l26
      f32.store offset=128
      local.get $l26
      f32.const 0x0p+0 (;=0;)
      f32.ne
      if $I1
        local.get $p5
        local.get $l16
        f32.const 0x1p+0 (;=1;)
        local.get $l26
        f32.div
        local.tee $l9
        f32.mul
        local.tee $l16
        f32.store offset=104
        local.get $p5
        local.get $l17
        local.get $l9
        f32.mul
        local.tee $l17
        f32.store offset=100
        local.get $p5
        local.get $l18
        local.get $l9
        f32.mul
        local.tee $l18
        f32.store offset=96
      end
      local.get $l8
      f32.const 0x0p+0 (;=0;)
      f32.ne
      if $I2
        local.get $p5
        f32.const 0x1p+0 (;=1;)
        local.get $l8
        f32.div
        local.tee $l9
        local.get $l12
        f32.mul
        local.tee $l12
        f32.store offset=116
        local.get $p5
        local.get $l9
        local.get $l13
        f32.mul
        local.tee $l13
        f32.store offset=112
        local.get $p5
        local.get $l15
        local.get $l9
        f32.mul
        local.tee $l15
        f32.store offset=108
      end
      local.get $l18
      local.get $l15
      f32.mul
      local.get $l17
      local.get $l13
      f32.mul
      f32.add
      local.get $l16
      local.get $l12
      f32.mul
      f32.add
      f32.abs
      f32.const 0x1.ffe5cap-1 (;=0.9998;)
      f32.gt
      if $I3
        local.get $p5
        local.get $l8
        f32.const 0x1.0624dep-10 (;=0.001;)
        f32.mul
        f32.store offset=36
        local.get $p5
        local.get $l26
        f32.const 0x1.0624dep-10 (;=0.001;)
        f32.mul
        local.tee $l24
        f32.store offset=32
        local.get $l16
        local.set $l11
        local.get $l17
        local.set $l14
        local.get $l18
        local.set $l12
        loop $L4
          local.get $p1
          local.get $p0
          i32.const 1
          local.get $l35
          i32.sub
          local.tee $p3
          select
          local.set $l40
          local.get $p5
          local.get $l35
          i32.const 12
          i32.mul
          i32.add
          local.tee $l37
          i32.const 8
          i32.add
          local.set $l41
          local.get $l37
          i32.const 4
          i32.add
          local.set $l42
          local.get $p5
          local.get $p3
          i32.const 12
          i32.mul
          i32.add
          local.tee $l38
          i32.const 8
          i32.add
          local.set $l43
          local.get $l38
          i32.const 4
          i32.add
          local.set $l44
          local.get $p5
          i32.const 48
          i32.add
          local.get $p3
          i32.const 24
          i32.mul
          i32.add
          local.tee $p4
          i32.const 20
          i32.add
          local.set $l45
          local.get $p4
          i32.const 8
          i32.add
          local.set $l46
          local.get $p4
          i32.const 16
          i32.add
          local.set $l47
          local.get $p4
          i32.const 4
          i32.or
          local.set $l48
          local.get $p4
          i32.const 12
          i32.add
          local.set $l49
          local.get $p5
          i32.const 128
          i32.add
          local.get $l35
          i32.const 2
          i32.shl
          i32.add
          local.set $l50
          local.get $p5
          i32.const 48
          i32.add
          local.get $l35
          i32.const 24
          i32.mul
          i32.add
          local.tee $p3
          f32.load offset=8
          local.set $l13
          local.get $p3
          f32.load offset=4
          local.set $l15
          local.get $p3
          f32.load
          local.set $l19
          local.get $l24
          f32.neg
          local.set $l23
          i32.const 0
          local.set $p3
          loop $L5
            local.get $l37
            local.get $l49
            local.get $p4
            local.get $p3
            select
            f32.load
            local.tee $l8
            f32.store
            local.get $l42
            local.get $l47
            local.get $l48
            local.get $p3
            select
            f32.load
            local.tee $l9
            f32.store
            local.get $l41
            local.get $l45
            local.get $l46
            local.get $p3
            select
            f32.load
            local.tee $l10
            f32.store
            block $B6
              local.get $l8
              local.get $l19
              f32.sub
              local.get $l12
              f32.mul
              local.get $l9
              local.get $l15
              f32.sub
              local.get $l14
              f32.mul
              f32.add
              local.get $l10
              local.get $l13
              f32.sub
              local.get $l11
              f32.mul
              f32.add
              local.tee $l8
              local.get $l23
              f32.ge
              i32.eqz
              br_if $B6
              local.get $l8
              local.get $l24
              local.get $l50
              f32.load
              f32.add
              f32.le
              i32.eqz
              br_if $B6
              local.get $l38
              local.get $l19
              local.get $l12
              local.get $l8
              f32.mul
              f32.add
              f32.store
              local.get $l44
              local.get $l15
              local.get $l14
              local.get $l8
              f32.mul
              f32.add
              f32.store
              local.get $l43
              local.get $l13
              local.get $l11
              local.get $l8
              f32.mul
              f32.add
              f32.store
              local.get $p5
              f32.load offset=12
              local.tee $l28
              local.get $p5
              f32.load
              f32.sub
              local.tee $l8
              local.get $l8
              f32.mul
              local.get $p5
              f32.load offset=16
              local.tee $l22
              local.get $p5
              f32.load offset=4
              f32.sub
              local.tee $l9
              local.get $l9
              f32.mul
              f32.add
              local.get $p5
              f32.load offset=20
              local.tee $l25
              local.get $p5
              f32.load offset=8
              f32.sub
              local.tee $l10
              local.get $l10
              f32.mul
              f32.add
              local.tee $l20
              f32.const 0x1.0c6f7ap-20 (;=1e-06;)
              f32.gt
              i32.eqz
              br_if $B6
              local.get $l20
              local.get $l30
              f32.lt
              i32.eqz
              br_if $B6
              local.get $p6
              i32.load offset=4096
              local.tee $p7
              i32.const 63
              i32.le_u
              if $I7
                local.get $l40
                f32.load offset=4
                local.set $l21
                local.get $p2
                f32.load offset=16
                local.set $l27
                local.get $p2
                f32.load offset=20
                local.set $l31
                local.get $p2
                f32.load offset=24
                local.set $l32
                local.get $p6
                local.get $p7
                i32.const 1
                i32.add
                i32.store offset=4096
                local.get $p6
                local.get $p7
                i32.const 6
                i32.shl
                i32.add
                local.tee $p7
                local.get $l10
                f32.const 0x1p+0 (;=1;)
                local.get $l20
                f32.sqrt
                local.tee $l33
                f32.div
                local.tee $l20
                f32.mul
                local.tee $l10
                f32.store offset=8
                local.get $p7
                local.get $l9
                local.get $l20
                f32.mul
                local.tee $l9
                f32.store offset=4
                local.get $p7
                local.get $l8
                local.get $l20
                f32.mul
                local.tee $l8
                f32.store
                local.get $p7
                i32.const -1
                i32.store offset=52
                local.get $p7
                local.get $l33
                local.get $l29
                f32.sub
                f32.store offset=12
                local.get $p7
                local.get $l32
                local.get $l25
                local.get $l10
                local.get $l21
                f32.mul
                f32.sub
                f32.add
                f32.store offset=24
                local.get $p7
                local.get $l31
                local.get $l22
                local.get $l9
                local.get $l21
                f32.mul
                f32.sub
                f32.add
                f32.store offset=20
                local.get $p7
                local.get $l27
                local.get $l28
                local.get $l8
                local.get $l21
                f32.mul
                f32.sub
                f32.add
                f32.store offset=16
              end
              local.get $l36
              i32.const 1
              i32.add
              local.set $l36
            end
            local.get $p3
            i32.const 1
            i32.add
            local.tee $p3
            i32.const 2
            i32.ne
            br_if $L5
          end
          local.get $l35
          i32.const 1
          i32.add
          local.tee $l35
          i32.const 2
          i32.ne
          if $I8
            local.get $p5
            i32.const 32
            i32.add
            local.get $l35
            i32.const 2
            i32.shl
            i32.add
            f32.load
            local.set $l24
            local.get $p5
            i32.const 96
            i32.add
            local.get $l35
            i32.const 12
            i32.mul
            i32.add
            local.tee $p3
            f32.load offset=8
            local.set $l11
            local.get $p3
            f32.load offset=4
            local.set $l14
            local.get $p3
            f32.load
            local.set $l12
            br $L4
          end
        end
        local.get $l36
        br_if $B0
      end
      block $B9
        local.get $p5
        f32.load offset=48
        local.tee $l9
        local.get $p5
        f32.load offset=44
        local.tee $l8
        local.get $p5
        f32.load offset=60
        local.get $l9
        f32.sub
        f32.mul
        f32.add
        local.tee $l12
        local.get $p5
        f32.load offset=72
        local.tee $l10
        local.get $p5
        f32.load offset=40
        local.tee $l9
        local.get $p5
        f32.load offset=84
        local.get $l10
        f32.sub
        f32.mul
        f32.add
        f32.sub
        local.tee $l10
        local.get $l10
        f32.mul
        local.get $p5
        f32.load offset=52
        local.tee $l11
        local.get $l8
        local.get $p5
        f32.load offset=64
        local.get $l11
        f32.sub
        f32.mul
        f32.add
        local.tee $l13
        local.get $p5
        f32.load offset=76
        local.tee $l11
        local.get $l9
        local.get $p5
        f32.load offset=88
        local.get $l11
        f32.sub
        f32.mul
        f32.add
        f32.sub
        local.tee $l11
        local.get $l11
        f32.mul
        f32.add
        local.get $p5
        f32.load offset=56
        local.tee $l14
        local.get $l8
        local.get $p5
        f32.load offset=68
        local.get $l14
        f32.sub
        f32.mul
        f32.add
        local.tee $l14
        local.get $p5
        f32.load offset=80
        local.tee $l8
        local.get $l9
        local.get $p5
        f32.load offset=92
        local.get $l8
        f32.sub
        f32.mul
        f32.add
        f32.sub
        local.tee $l8
        local.get $l8
        f32.mul
        f32.add
        local.tee $l9
        f32.const 0x1.0c6f7ap-20 (;=1e-06;)
        f32.lt
        if $I10
          local.get $l26
          f32.const 0x1.0c6f7ap-20 (;=1e-06;)
          f32.gt
          br_if $B9
          f32.const 0x1p+0 (;=1;)
          local.set $l18
          f32.const 0x0p+0 (;=0;)
          local.set $l16
          f32.const 0x0p+0 (;=0;)
          local.set $l17
          br $B9
        end
        local.get $l8
        f32.const 0x1p+0 (;=1;)
        local.get $l9
        f32.sqrt
        f32.div
        local.tee $l9
        f32.mul
        local.set $l16
        local.get $l11
        local.get $l9
        f32.mul
        local.set $l17
        local.get $l10
        local.get $l9
        f32.mul
        local.set $l18
      end
      local.get $p6
      i32.load offset=4096
      local.tee $p3
      i32.const 63
      i32.gt_u
      br_if $B0
      local.get $p0
      f32.load offset=4
      local.set $l8
      local.get $p2
      f32.load offset=16
      local.set $l9
      local.get $p2
      f32.load offset=20
      local.set $l10
      local.get $p2
      f32.load offset=24
      local.set $l11
      local.get $p6
      local.get $p3
      i32.const 1
      i32.add
      i32.store offset=4096
      local.get $p6
      local.get $p3
      i32.const 6
      i32.shl
      i32.add
      local.tee $p3
      local.get $l16
      f32.store offset=8
      local.get $p3
      local.get $l17
      f32.store offset=4
      local.get $p3
      local.get $l18
      f32.store
      local.get $p3
      i32.const -1
      i32.store offset=52
      local.get $p3
      local.get $l34
      f32.sqrt
      local.get $l29
      f32.sub
      f32.store offset=12
      local.get $p3
      local.get $l14
      local.get $l11
      f32.add
      local.get $l16
      local.get $l8
      f32.mul
      f32.sub
      f32.store offset=24
      local.get $p3
      local.get $l13
      local.get $l10
      f32.add
      local.get $l17
      local.get $l8
      f32.mul
      f32.sub
      f32.store offset=20
      local.get $p3
      local.get $l12
      local.get $l9
      f32.add
      local.get $l18
      local.get $l8
      f32.mul
      f32.sub
      f32.store offset=16
    end
    local.get $p5
    i32.const 144
    i32.add
    global.set $g0
    local.get $l39
    i32.eqz)
