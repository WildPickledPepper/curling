  (func $f70553 (type $t18) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 i32) (param $p7 i32) (result i32)
    (local $l8 i32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32) (local $l33 f32) (local $l34 f32) (local $l35 f32) (local $l36 f32) (local $l37 f32) (local $l38 f32) (local $l39 f32) (local $l40 f32) (local $l41 f32) (local $l42 f32) (local $l43 f32) (local $l44 f32) (local $l45 f32) (local $l46 f32)
    global.get $g0
    i32.const 320
    i32.sub
    local.tee $l8
    global.set $g0
    local.get $p2
    f32.load offset=20
    local.set $l9
    local.get $p2
    f32.load offset=16
    local.set $l10
    local.get $l8
    local.get $p2
    f32.load offset=24
    local.tee $l15
    local.get $p0
    local.tee $p7
    f32.load offset=8
    local.tee $l13
    local.get $p2
    f32.load
    local.tee $l16
    local.get $l16
    f32.add
    local.tee $l14
    local.get $p2
    f32.load offset=8
    local.tee $l18
    f32.mul
    local.get $p2
    f32.load offset=12
    local.tee $l11
    local.get $l11
    f32.add
    local.tee $l12
    local.get $p2
    f32.load offset=4
    local.tee $l17
    f32.mul
    f32.sub
    f32.mul
    local.tee $l19
    f32.sub
    f32.store offset=124
    local.get $l8
    local.get $l9
    local.get $l13
    local.get $l18
    local.get $l12
    f32.mul
    local.get $l14
    local.get $l17
    f32.mul
    f32.add
    f32.mul
    local.tee $l18
    f32.sub
    f32.store offset=120
    local.get $l8
    local.get $l19
    local.get $l15
    f32.add
    f32.store offset=112
    local.get $l8
    local.get $l9
    local.get $l18
    f32.add
    f32.store offset=108
    local.get $l8
    local.get $l10
    local.get $l13
    local.get $l16
    local.get $l14
    f32.mul
    local.get $l11
    local.get $l12
    f32.mul
    f32.const -0x1p+0 (;=-1;)
    f32.add
    f32.add
    f32.mul
    local.tee $l9
    f32.sub
    f32.store offset=116
    local.get $l8
    local.get $l10
    local.get $l9
    f32.add
    f32.store offset=104
    local.get $p4
    f32.load
    local.set $l12
    local.get $p0
    f32.load offset=4
    local.set $l15
    local.get $l8
    local.get $p3
    f32.load offset=4
    local.tee $l10
    local.get $l10
    f32.add
    local.tee $l16
    local.get $p3
    f32.load offset=8
    local.tee $l9
    f32.mul
    local.tee $l18
    local.get $p3
    f32.load
    local.tee $l14
    local.get $l14
    f32.add
    local.tee $l13
    local.get $p3
    f32.load offset=12
    local.tee $l11
    f32.mul
    local.tee $l17
    f32.sub
    f32.store offset=68
    local.get $l8
    local.get $l18
    local.get $l17
    f32.add
    f32.store offset=60
    local.get $l8
    f32.const 0x1p+0 (;=1;)
    local.get $l14
    local.get $l13
    f32.mul
    f32.sub
    local.tee $l14
    local.get $l10
    local.get $l16
    f32.mul
    local.tee $l18
    f32.sub
    f32.store offset=72
    local.get $l8
    local.get $l14
    local.get $l9
    local.get $l9
    local.get $l9
    f32.add
    local.tee $l17
    f32.mul
    local.tee $l19
    f32.sub
    f32.store offset=56
    local.get $l8
    local.get $l13
    local.get $l9
    f32.mul
    local.tee $l9
    local.get $l16
    local.get $l11
    f32.mul
    local.tee $l16
    f32.add
    f32.store offset=64
    local.get $l8
    local.get $l13
    local.get $l10
    f32.mul
    local.tee $l10
    local.get $l17
    local.get $l11
    f32.mul
    local.tee $l13
    f32.sub
    f32.store offset=52
    local.get $l8
    local.get $l9
    local.get $l16
    f32.sub
    f32.store offset=48
    local.get $l8
    local.get $l10
    local.get $l13
    f32.add
    f32.store offset=44
    local.get $l8
    f32.const 0x1p+0 (;=1;)
    local.get $l18
    f32.sub
    local.get $l19
    f32.sub
    f32.store offset=40
    local.get $l8
    local.get $p3
    f32.load offset=16
    f32.store offset=76
    local.get $l8
    local.get $p3
    f32.load offset=20
    f32.store offset=80
    local.get $l8
    local.get $p3
    f32.load offset=24
    f32.store offset=84
    local.get $l8
    local.get $p1
    f32.load offset=4
    f32.store offset=88
    local.get $l8
    local.get $p1
    f32.load offset=8
    f32.store offset=92
    local.get $l8
    local.get $p1
    f32.load offset=12
    f32.store offset=96
    i32.const 0
    local.set $p3
    block $B0
      local.get $l8
      i32.const 104
      i32.add
      local.get $l8
      i32.const 116
      i32.add
      local.get $l8
      i32.const 76
      i32.add
      local.tee $p1
      local.get $l8
      i32.const 88
      i32.add
      local.tee $p0
      local.get $l8
      i32.const 40
      i32.add
      local.get $l8
      i32.const 36
      i32.add
      local.get $l8
      i32.const 24
      i32.add
      call $f69889
      local.tee $l21
      local.get $l15
      local.get $l12
      f32.add
      local.tee $l9
      local.get $l9
      f32.mul
      f32.ge
      br_if $B0
      block $B1
        block $B2
          local.get $l21
          f32.const 0x0p+0 (;=0;)
          f32.eq
          if $I3
            local.get $l8
            f32.load offset=72
            local.set $l20
            local.get $l8
            f32.load offset=68
            local.set $l22
            local.get $l8
            f32.load offset=60
            local.set $l18
            local.get $l8
            f32.load offset=56
            local.set $l17
            local.get $l8
            f32.load offset=64
            local.set $l25
            local.get $l8
            f32.load offset=52
            local.set $l19
            local.get $l8
            f32.load offset=84
            local.set $l35
            local.get $l8
            f32.load offset=80
            local.set $l36
            local.get $l8
            f32.load offset=76
            local.set $l38
            local.get $l8
            f32.load offset=124
            local.set $l29
            local.get $l8
            f32.load offset=120
            local.set $l30
            local.get $l8
            f32.load offset=116
            local.set $l31
            local.get $l8
            f32.load offset=48
            local.set $l16
            local.get $l8
            f32.load offset=112
            local.set $l24
            local.get $l8
            f32.load offset=44
            local.set $l14
            local.get $l8
            f32.load offset=108
            local.set $l23
            local.get $l8
            f32.load offset=40
            local.set $l11
            local.get $l8
            f32.load offset=104
            local.set $l27
            br $B2
          end
          local.get $l8
          f32.load offset=72
          local.set $l20
          local.get $l8
          f32.load offset=60
          local.set $l18
          local.get $l8
          f32.load offset=68
          local.set $l22
          local.get $l8
          f32.load offset=56
          local.set $l17
          local.get $l8
          f32.load offset=112
          local.set $l24
          local.get $l8
          f32.load offset=124
          local.set $l29
          local.get $l8
          f32.load offset=84
          local.set $l35
          local.get $l8
          f32.load offset=48
          local.set $l16
          local.get $l8
          f32.load offset=108
          local.set $l23
          local.get $l8
          f32.load offset=120
          local.set $l30
          local.get $l8
          f32.load offset=80
          local.set $l36
          local.get $l8
          f32.load offset=44
          local.set $l14
          local.get $l8
          f32.load offset=36
          local.set $l9
          local.get $l8
          f32.load offset=104
          local.set $l27
          local.get $l8
          f32.load offset=116
          local.set $l31
          local.get $l8
          local.get $l8
          f32.load offset=24
          local.tee $l10
          local.get $l8
          f32.load offset=40
          local.tee $l11
          f32.mul
          local.get $l8
          f32.load offset=28
          local.tee $l13
          local.get $l8
          f32.load offset=52
          local.tee $l19
          f32.mul
          f32.add
          local.get $l8
          f32.load offset=32
          local.tee $l12
          local.get $l8
          f32.load offset=64
          local.tee $l25
          f32.mul
          f32.add
          local.get $l8
          f32.load offset=76
          local.tee $l38
          f32.add
          local.tee $l15
          f32.store offset=24
          local.get $l8
          local.get $l36
          local.get $l10
          local.get $l14
          f32.mul
          local.get $l13
          local.get $l17
          f32.mul
          f32.add
          local.get $l12
          local.get $l22
          f32.mul
          f32.add
          f32.add
          local.tee $l26
          f32.store offset=28
          local.get $l8
          local.get $l35
          local.get $l10
          local.get $l16
          f32.mul
          local.get $l13
          local.get $l18
          f32.mul
          f32.add
          local.get $l12
          local.get $l20
          f32.mul
          f32.add
          f32.add
          local.tee $l10
          f32.store offset=32
          local.get $l27
          local.get $l9
          local.get $l31
          local.get $l27
          f32.sub
          f32.mul
          f32.add
          local.get $l15
          f32.sub
          local.tee $l12
          local.get $l12
          f32.mul
          local.get $l23
          local.get $l9
          local.get $l30
          local.get $l23
          f32.sub
          f32.mul
          f32.add
          local.get $l26
          f32.sub
          local.tee $l13
          local.get $l13
          f32.mul
          f32.add
          local.get $l24
          local.get $l9
          local.get $l29
          local.get $l24
          f32.sub
          f32.mul
          f32.add
          local.get $l10
          f32.sub
          local.tee $l9
          local.get $l9
          f32.mul
          f32.add
          f32.sqrt
          local.tee $l10
          f32.const 0x0p+0 (;=0;)
          f32.gt
          i32.eqz
          br_if $B2
          local.get $l8
          local.get $l9
          f32.const 0x1p+0 (;=1;)
          local.get $l10
          f32.div
          local.tee $l16
          f32.mul
          local.tee $l10
          f32.store offset=16
          local.get $l8
          local.get $l13
          local.get $l16
          f32.mul
          local.tee $l13
          f32.store offset=12
          local.get $l8
          local.get $l12
          local.get $l16
          f32.mul
          local.tee $l16
          f32.store offset=8
          local.get $p6
          local.get $l8
          i32.const 104
          i32.add
          local.get $p7
          f32.load offset=4
          local.get $l8
          i32.const 40
          i32.add
          local.get $l8
          i32.const 8
          i32.add
          local.get $p4
          f32.load
          call $f70166
          local.get $p6
          i32.load offset=4096
          i32.const 2
          i32.eq
          br_if $B1
          local.get $p4
          f32.load
          local.set $l24
          local.get $p7
          f32.load offset=4
          local.set $l22
          i32.const 4117344
          local.set $p3
          local.get $l8
          i32.const 224
          i32.add
          local.get $p1
          local.get $p0
          local.get $l8
          i32.const 40
          i32.add
          local.get $l8
          i32.const 52
          i32.add
          local.get $l8
          i32.const -64
          i32.sub
          call $f70389
          local.get $l8
          local.get $l8
          f32.load offset=104
          local.tee $l12
          f32.store offset=208
          local.get $l8
          local.get $l8
          f32.load offset=108
          local.tee $l15
          f32.store offset=212
          local.get $l8
          local.get $l8
          f32.load offset=112
          local.tee $l18
          f32.store offset=216
          local.get $l8
          local.get $l8
          f32.load offset=116
          local.tee $l17
          f32.store offset=192
          local.get $l8
          local.get $l8
          f32.load offset=120
          local.tee $l19
          f32.store offset=196
          local.get $l8
          local.get $l8
          f32.load offset=124
          local.tee $l20
          f32.store offset=200
          local.get $l17
          local.get $l12
          f32.sub
          local.tee $l9
          local.get $l9
          f32.mul
          local.get $l19
          local.get $l15
          f32.sub
          local.tee $l14
          local.get $l14
          f32.mul
          f32.add
          local.get $l20
          local.get $l18
          f32.sub
          local.tee $l11
          local.get $l11
          f32.mul
          f32.add
          f32.sqrt
          local.tee $l23
          f32.const 0x0p+0 (;=0;)
          f32.gt
          if $I4
            local.get $l8
            local.get $l18
            local.get $l11
            f32.const 0x1.47ae14p-7 (;=0.01;)
            local.get $l23
            f32.div
            local.tee $l23
            f32.mul
            local.tee $l11
            f32.sub
            local.tee $l18
            f32.store offset=216
            local.get $l8
            local.get $l15
            local.get $l14
            local.get $l23
            f32.mul
            local.tee $l14
            f32.sub
            local.tee $l15
            f32.store offset=212
            local.get $l8
            local.get $l12
            local.get $l9
            local.get $l23
            f32.mul
            local.tee $l9
            f32.sub
            local.tee $l12
            f32.store offset=208
            local.get $l8
            local.get $l20
            local.get $l11
            f32.add
            local.tee $l11
            f32.store offset=200
            local.get $l11
            local.get $l18
            f32.sub
            local.set $l11
            local.get $l8
            local.get $l19
            local.get $l14
            f32.add
            local.tee $l14
            f32.store offset=196
            local.get $l14
            local.get $l15
            f32.sub
            local.set $l14
            local.get $l8
            local.get $l17
            local.get $l9
            f32.add
            local.tee $l9
            f32.store offset=192
            local.get $l9
            local.get $l12
            f32.sub
            local.set $l9
          end
          local.get $l8
          local.get $l14
          f32.store offset=180
          local.get $l8
          local.get $l9
          f32.store offset=176
          local.get $l8
          local.get $l11
          f32.store offset=184
          local.get $l8
          local.get $l13
          local.get $l9
          f32.mul
          local.get $l16
          local.get $l14
          f32.mul
          f32.sub
          local.tee $l17
          f32.neg
          f32.store offset=168
          local.get $l8
          local.get $l10
          local.get $l14
          f32.mul
          local.get $l13
          local.get $l11
          f32.mul
          f32.sub
          local.tee $l14
          f32.neg
          f32.store offset=160
          local.get $l8
          local.get $l16
          local.get $l11
          f32.mul
          local.get $l10
          local.get $l9
          f32.mul
          f32.sub
          local.tee $l11
          f32.neg
          local.tee $l9
          f32.store offset=164
          local.get $l8
          local.get $l15
          local.get $l9
          f32.mul
          local.get $l14
          local.get $l12
          f32.mul
          f32.sub
          local.get $l18
          local.get $l17
          f32.mul
          f32.sub
          f32.neg
          f32.store offset=172
          local.get $l17
          f32.abs
          local.set $l9
          block $B5 (result i32)
            block $B6
              block $B7
                local.get $l11
                f32.abs
                local.tee $l11
                local.get $l14
                f32.abs
                local.tee $l14
                f32.gt
                i32.eqz
                br_if $B7
                local.get $l9
                local.get $l11
                f32.lt
                i32.eqz
                br_if $B7
                i32.const 0
                local.set $p0
                i32.const 2
                local.set $p2
                br $B6
              end
              i32.const 2
              local.set $p5
              i32.const 0
              local.set $p2
              i32.const 1
              local.tee $p0
              local.get $l9
              local.get $l14
              f32.gt
              i32.eqz
              br_if $B5
              drop
            end
            local.get $p0
            local.set $p5
            local.get $p2
          end
          local.set $p0
          f32.const 0x1p+0 (;=1;)
          local.get $p5
          i32.const 2
          i32.shl
          local.tee $p2
          local.get $l8
          i32.const 176
          i32.add
          i32.add
          f32.load
          local.get $p0
          i32.const 2
          i32.shl
          local.tee $p1
          local.get $l8
          i32.const 8
          i32.add
          i32.add
          f32.load
          f32.mul
          local.get $l8
          i32.const 176
          i32.add
          local.get $p1
          i32.add
          f32.load
          local.get $l8
          i32.const 8
          i32.add
          local.get $p2
          i32.add
          f32.load
          f32.mul
          f32.sub
          f32.div
          local.set $l14
          local.get $l22
          local.get $l24
          f32.add
          local.set $l20
          local.get $l10
          f32.neg
          local.set $l11
          local.get $l13
          f32.neg
          local.set $l12
          local.get $l16
          f32.neg
          local.set $l15
          i32.const 0
          local.set $p1
          loop $L8
            local.get $p3
            i32.load8_u
            local.set $p2
            local.get $p3
            i32.load8_u offset=1
            local.set $p4
            local.get $l8
            local.get $l11
            f32.store offset=136
            local.get $l8
            local.get $l12
            f32.store offset=132
            local.get $l8
            local.get $l15
            f32.store offset=128
            block $B9
              local.get $l8
              i32.const 208
              i32.add
              local.get $l8
              i32.const 192
              i32.add
              local.get $l8
              i32.const 176
              i32.add
              local.get $l8
              i32.const 160
              i32.add
              local.get $p0
              local.get $p5
              local.get $l14
              local.get $l8
              i32.const 128
              i32.add
              local.get $l8
              i32.const 224
              i32.add
              local.get $p2
              i32.const 12
              i32.mul
              i32.add
              local.get $l8
              i32.const 224
              i32.add
              local.get $p4
              i32.const 12
              i32.mul
              i32.add
              local.get $l8
              i32.const 140
              i32.add
              local.get $l8
              i32.const 144
              i32.add
              call $f70167
              i32.eqz
              br_if $B9
              local.get $l8
              f32.load offset=140
              local.tee $l9
              local.get $l20
              f32.lt
              i32.eqz
              br_if $B9
              local.get $p6
              i32.load offset=4096
              local.tee $p2
              i32.const 63
              i32.gt_u
              br_if $B9
              local.get $l8
              f32.load offset=148
              local.set $l18
              local.get $l8
              f32.load offset=152
              local.set $l17
              local.get $l8
              f32.load offset=144
              local.set $l19
              local.get $p6
              local.get $p2
              i32.const 1
              i32.add
              i32.store offset=4096
              local.get $p6
              local.get $p2
              i32.const 6
              i32.shl
              i32.add
              local.tee $p2
              local.get $l19
              local.get $l16
              local.get $l9
              f32.mul
              f32.sub
              f32.store offset=16
              local.get $p2
              local.get $l10
              f32.store offset=8
              local.get $p2
              local.get $l13
              f32.store offset=4
              local.get $p2
              local.get $l16
              f32.store
              local.get $p2
              i32.const -1
              i32.store offset=52
              local.get $p2
              local.get $l9
              local.get $l22
              f32.sub
              f32.store offset=12
              local.get $p2
              local.get $l17
              local.get $l10
              local.get $l9
              f32.mul
              f32.sub
              f32.store offset=24
              local.get $p2
              local.get $l18
              local.get $l13
              local.get $l9
              f32.mul
              f32.sub
              f32.store offset=20
            end
            local.get $p3
            i32.const 2
            i32.add
            local.set $p3
            local.get $p1
            i32.const 1
            i32.add
            local.tee $p1
            i32.const 12
            i32.ne
            br_if $L8
          end
          local.get $p6
          i32.load offset=4096
          br_if $B1
          local.get $p7
          f32.load offset=4
          local.set $l9
          local.get $p6
          local.get $l10
          f32.store offset=8
          local.get $p6
          local.get $l13
          f32.store offset=4
          local.get $p6
          local.get $l16
          f32.store
          local.get $p6
          i32.const 1
          i32.store offset=4096
          local.get $p6
          local.get $l8
          f32.load offset=24
          f32.store offset=16
          local.get $p6
          local.get $l8
          f32.load offset=28
          f32.store offset=20
          local.get $l8
          f32.load offset=32
          local.set $l10
          local.get $p6
          i32.const -1
          i32.store offset=52
          local.get $p6
          local.get $l21
          f32.sqrt
          local.get $l9
          f32.sub
          f32.store offset=12
          local.get $p6
          local.get $l10
          f32.store offset=24
          br $B1
        end
        local.get $p7
        f32.load offset=4
        local.tee $l26
        local.get $l27
        local.get $l11
        f32.mul
        local.get $l23
        local.get $l14
        f32.mul
        f32.add
        local.get $l24
        local.get $l16
        f32.mul
        f32.add
        local.tee $l9
        local.get $l11
        local.get $l31
        f32.mul
        local.get $l14
        local.get $l30
        f32.mul
        f32.add
        local.get $l16
        local.get $l29
        f32.mul
        f32.add
        local.tee $l10
        local.get $l9
        local.get $l10
        f32.gt
        local.tee $p2
        select
        f32.add
        local.tee $l21
        local.get $l11
        local.get $l38
        f32.mul
        local.get $l14
        local.get $l36
        f32.mul
        f32.add
        local.get $l16
        local.get $l35
        f32.mul
        f32.add
        local.tee $l13
        local.get $l8
        f32.load offset=88
        local.tee $l43
        local.get $l11
        local.get $l11
        f32.mul
        local.get $l14
        local.get $l14
        f32.mul
        f32.add
        local.get $l16
        local.get $l16
        f32.mul
        f32.add
        f32.abs
        f32.mul
        local.get $l8
        f32.load offset=92
        local.tee $l44
        local.get $l11
        local.get $l19
        f32.mul
        local.get $l14
        local.get $l17
        f32.mul
        f32.add
        local.get $l16
        local.get $l18
        f32.mul
        f32.add
        f32.abs
        local.tee $l15
        f32.mul
        f32.add
        local.get $l8
        f32.load offset=96
        local.tee $l45
        local.get $l11
        local.get $l25
        f32.mul
        local.get $l14
        local.get $l22
        f32.mul
        f32.add
        local.get $l16
        local.get $l20
        f32.mul
        f32.add
        f32.abs
        local.tee $l32
        f32.mul
        f32.add
        local.tee $l12
        f32.sub
        local.tee $l41
        f32.lt
        br_if $B0
        local.get $l13
        local.get $l12
        f32.add
        local.tee $l13
        local.get $l10
        local.get $l9
        local.get $p2
        select
        local.get $l26
        f32.sub
        local.tee $l12
        f32.lt
        br_if $B0
        local.get $l26
        local.get $l27
        local.get $l19
        f32.mul
        local.get $l23
        local.get $l17
        f32.mul
        f32.add
        local.get $l24
        local.get $l18
        f32.mul
        f32.add
        local.tee $l9
        local.get $l31
        local.get $l19
        f32.mul
        local.get $l30
        local.get $l17
        f32.mul
        f32.add
        local.get $l29
        local.get $l18
        f32.mul
        f32.add
        local.tee $l10
        local.get $l9
        local.get $l10
        f32.gt
        local.tee $p2
        select
        f32.add
        local.tee $l37
        local.get $l38
        local.get $l19
        f32.mul
        local.get $l36
        local.get $l17
        f32.mul
        f32.add
        local.get $l35
        local.get $l18
        f32.mul
        f32.add
        local.tee $l33
        local.get $l45
        local.get $l25
        local.get $l19
        f32.mul
        local.get $l22
        local.get $l17
        f32.mul
        f32.add
        local.get $l20
        local.get $l18
        f32.mul
        f32.add
        f32.abs
        local.tee $l28
        f32.mul
        local.get $l43
        local.get $l15
        f32.mul
        local.get $l44
        local.get $l19
        local.get $l19
        f32.mul
        local.get $l17
        local.get $l17
        f32.mul
        f32.add
        local.get $l18
        local.get $l18
        f32.mul
        f32.add
        f32.abs
        f32.mul
        f32.add
        f32.add
        local.tee $l15
        f32.sub
        local.tee $l34
        f32.lt
        br_if $B0
        local.get $l33
        local.get $l15
        f32.add
        local.tee $l15
        local.get $l10
        local.get $l9
        local.get $p2
        select
        local.get $l26
        f32.sub
        local.tee $l9
        f32.lt
        br_if $B0
        local.get $l18
        local.set $l33
        local.get $l17
        local.set $l39
        local.get $l19
        local.set $l42
        local.get $l37
        local.get $l34
        f32.sub
        local.tee $l10
        local.get $l15
        local.get $l9
        f32.sub
        local.tee $l9
        local.get $l9
        local.get $l10
        f32.gt
        select
        local.tee $l15
        local.get $l21
        local.get $l41
        f32.sub
        local.tee $l9
        local.get $l13
        local.get $l12
        f32.sub
        local.tee $l10
        local.get $l9
        local.get $l10
        f32.lt
        select
        local.tee $l9
        f32.const 0x1.fffffep+127 (;=3.40282e+38;)
        local.get $l9
        f32.const 0x1.fffffep+127 (;=3.40282e+38;)
        f32.lt
        local.tee $p2
        select
        local.tee $l9
        f32.lt
        i32.eqz
        if $I10
          local.get $l11
          f32.const 0x0p+0 (;=0;)
          local.get $p2
          select
          local.set $l42
          local.get $l14
          f32.const 0x0p+0 (;=0;)
          local.get $p2
          select
          local.set $l39
          local.get $l16
          f32.const 0x0p+0 (;=0;)
          local.get $p2
          select
          local.set $l33
          local.get $l9
          local.set $l15
        end
        local.get $l26
        local.get $l27
        local.get $l25
        f32.mul
        local.get $l23
        local.get $l22
        f32.mul
        f32.add
        local.get $l24
        local.get $l20
        f32.mul
        f32.add
        local.tee $l9
        local.get $l31
        local.get $l25
        f32.mul
        local.get $l30
        local.get $l22
        f32.mul
        f32.add
        local.get $l29
        local.get $l20
        f32.mul
        f32.add
        local.tee $l10
        local.get $l9
        local.get $l10
        f32.gt
        local.tee $p2
        select
        f32.add
        local.tee $l21
        local.get $l38
        local.get $l25
        f32.mul
        local.get $l36
        local.get $l22
        f32.mul
        f32.add
        local.get $l35
        local.get $l20
        f32.mul
        f32.add
        local.tee $l13
        local.get $l45
        local.get $l25
        local.get $l25
        f32.mul
        local.get $l22
        local.get $l22
        f32.mul
        f32.add
        local.get $l20
        local.get $l20
        f32.mul
        f32.add
        f32.abs
        f32.mul
        local.get $l43
        local.get $l32
        f32.mul
        local.get $l44
        local.get $l28
        f32.mul
        f32.add
        f32.add
        local.tee $l12
        f32.sub
        local.tee $l32
        f32.lt
        br_if $B0
        local.get $l13
        local.get $l12
        f32.add
        local.tee $l13
        local.get $l10
        local.get $l9
        local.get $p2
        select
        local.get $l26
        f32.sub
        local.tee $l9
        f32.lt
        br_if $B0
        local.get $l20
        local.set $l28
        local.get $l22
        local.set $l34
        local.get $l25
        local.set $l40
        local.get $l21
        local.get $l32
        f32.sub
        local.tee $l10
        local.get $l13
        local.get $l9
        f32.sub
        local.tee $l9
        local.get $l9
        local.get $l10
        f32.gt
        select
        local.tee $l37
        local.get $l15
        f32.lt
        i32.eqz
        if $I11
          local.get $l15
          local.set $l37
          local.get $l39
          local.set $l34
          local.get $l42
          local.set $l40
          local.get $l33
          local.set $l28
        end
        f32.const 0x0p+0 (;=0;)
        local.set $l32
        f32.const 0x0p+0 (;=0;)
        local.set $l41
        f32.const 0x0p+0 (;=0;)
        local.set $l33
        local.get $l31
        local.get $l27
        f32.sub
        local.tee $l9
        local.get $l9
        f32.mul
        local.get $l30
        local.get $l23
        f32.sub
        local.tee $l10
        local.get $l10
        f32.mul
        f32.add
        local.get $l29
        local.get $l24
        f32.sub
        local.tee $l13
        local.get $l13
        f32.mul
        f32.add
        local.tee $l12
        f32.const 0x0p+0 (;=0;)
        f32.gt
        if $I12
          local.get $l13
          f32.const 0x1p+0 (;=1;)
          local.get $l12
          f32.sqrt
          f32.div
          local.tee $l12
          f32.mul
          local.set $l33
          local.get $l10
          local.get $l12
          f32.mul
          local.set $l41
          local.get $l9
          local.get $l12
          f32.mul
          local.set $l32
        end
        i32.const 1
        local.set $p5
        block $B13
          block $B14
            loop $L15
              local.get $l32
              local.get $l8
              i32.const 40
              i32.add
              local.get $p3
              i32.const 12
              i32.mul
              i32.add
              local.tee $p2
              f32.load offset=4
              local.tee $l9
              f32.mul
              local.get $l41
              local.get $p2
              f32.load
              local.tee $l10
              f32.mul
              f32.sub
              local.set $l15
              local.get $l33
              local.get $l10
              f32.mul
              local.get $l32
              local.get $p2
              f32.load offset=8
              local.tee $l10
              f32.mul
              f32.sub
              local.set $l12
              block $B16
                block $B17
                  local.get $l41
                  local.get $l10
                  f32.mul
                  local.get $l33
                  local.get $l9
                  f32.mul
                  f32.sub
                  local.tee $l21
                  f32.abs
                  f32.const 0x1.0c6f7ap-20 (;=1e-06;)
                  f32.gt
                  br_if $B17
                  local.get $l12
                  f32.abs
                  f32.const 0x1.0c6f7ap-20 (;=1e-06;)
                  f32.gt
                  br_if $B17
                  local.get $l15
                  f32.abs
                  f32.const 0x1.0c6f7ap-20 (;=1e-06;)
                  f32.gt
                  i32.eqz
                  br_if $B16
                end
                f32.const 0x0p+0 (;=0;)
                local.set $l9
                f32.const 0x0p+0 (;=0;)
                local.set $l10
                f32.const 0x0p+0 (;=0;)
                local.set $l13
                local.get $l15
                local.get $l15
                f32.mul
                local.get $l21
                local.get $l21
                f32.mul
                local.get $l12
                local.get $l12
                f32.mul
                f32.add
                f32.add
                local.tee $l39
                f32.const 0x0p+0 (;=0;)
                f32.gt
                if $I18
                  local.get $l15
                  f32.const 0x1p+0 (;=1;)
                  local.get $l39
                  f32.sqrt
                  f32.div
                  local.tee $l9
                  f32.mul
                  local.set $l13
                  local.get $l12
                  local.get $l9
                  f32.mul
                  local.set $l10
                  local.get $l21
                  local.get $l9
                  f32.mul
                  local.set $l9
                end
                local.get $l26
                local.get $l27
                local.get $l9
                f32.mul
                local.get $l23
                local.get $l10
                f32.mul
                f32.add
                local.get $l24
                local.get $l13
                f32.mul
                f32.add
                local.tee $l12
                local.get $l31
                local.get $l9
                f32.mul
                local.get $l30
                local.get $l10
                f32.mul
                f32.add
                local.get $l29
                local.get $l13
                f32.mul
                f32.add
                local.tee $l15
                local.get $l12
                local.get $l15
                f32.gt
                local.tee $p2
                select
                f32.add
                local.tee $l42
                local.get $l38
                local.get $l9
                f32.mul
                local.get $l36
                local.get $l10
                f32.mul
                f32.add
                local.get $l35
                local.get $l13
                f32.mul
                f32.add
                local.tee $l21
                local.get $l45
                local.get $l25
                local.get $l9
                f32.mul
                local.get $l22
                local.get $l10
                f32.mul
                f32.add
                local.get $l20
                local.get $l13
                f32.mul
                f32.add
                f32.abs
                f32.mul
                local.get $l43
                local.get $l11
                local.get $l9
                f32.mul
                local.get $l14
                local.get $l10
                f32.mul
                f32.add
                local.get $l16
                local.get $l13
                f32.mul
                f32.add
                f32.abs
                f32.mul
                local.get $l44
                local.get $l19
                local.get $l9
                f32.mul
                local.get $l17
                local.get $l10
                f32.mul
                f32.add
                local.get $l18
                local.get $l13
                f32.mul
                f32.add
                f32.abs
                f32.mul
                f32.add
                f32.add
                local.tee $l39
                f32.sub
                local.tee $l46
                f32.lt
                br_if $B14
                local.get $l21
                local.get $l39
                f32.add
                local.tee $l21
                local.get $l15
                local.get $l12
                local.get $p2
                select
                local.get $l26
                f32.sub
                local.tee $l12
                f32.lt
                br_if $B14
                local.get $l42
                local.get $l46
                f32.sub
                local.tee $l15
                local.get $l21
                local.get $l12
                f32.sub
                local.tee $l12
                local.get $l12
                local.get $l15
                f32.gt
                select
                local.tee $l12
                local.get $l37
                local.get $l12
                local.get $l37
                f32.lt
                local.tee $p2
                select
                local.set $l37
                local.get $l13
                local.get $l28
                local.get $p2
                select
                local.set $l28
                local.get $l10
                local.get $l34
                local.get $p2
                select
                local.set $l34
                local.get $l9
                local.get $l40
                local.get $p2
                select
                local.set $l40
              end
              local.get $p3
              i32.const 2
              i32.lt_u
              local.set $p5
              local.get $p3
              i32.const 1
              i32.add
              local.tee $p3
              i32.const 3
              i32.ne
              br_if $L15
            end
            local.get $l8
            local.get $l28
            f32.neg
            local.get $l28
            local.get $l27
            local.get $l31
            f32.add
            f32.const 0x1p-1 (;=0.5;)
            f32.mul
            local.get $l38
            f32.sub
            local.get $l40
            f32.mul
            local.get $l23
            local.get $l30
            f32.add
            f32.const 0x1p-1 (;=0.5;)
            f32.mul
            local.get $l36
            f32.sub
            local.get $l34
            f32.mul
            f32.add
            local.get $l24
            local.get $l29
            f32.add
            f32.const 0x1p-1 (;=0.5;)
            f32.mul
            local.get $l35
            f32.sub
            local.get $l28
            f32.mul
            f32.add
            f32.const 0x0p+0 (;=0;)
            f32.lt
            local.tee $p3
            select
            f32.store offset=136
            local.get $l8
            local.get $l34
            f32.neg
            local.get $l34
            local.get $p3
            select
            f32.store offset=132
            local.get $l8
            local.get $l40
            f32.neg
            local.get $l40
            local.get $p3
            select
            local.tee $l13
            f32.store offset=128
            br $B13
          end
          i32.const 0
          local.set $p3
          local.get $p5
          i32.const 1
          i32.and
          br_if $B0
        end
        local.get $p6
        local.get $l8
        i32.const 104
        i32.add
        local.get $l26
        local.get $l8
        i32.const 40
        i32.add
        local.get $l8
        i32.const 128
        i32.add
        local.get $p4
        f32.load
        call $f70166
        i32.const 1
        local.set $p3
        local.get $p6
        i32.load offset=4096
        i32.const 2
        i32.eq
        br_if $B0
        local.get $p7
        f32.load offset=4
        local.set $l18
        i32.const 4117344
        local.set $p3
        local.get $l8
        i32.const 224
        i32.add
        local.get $p1
        local.get $p0
        local.get $l8
        i32.const 40
        i32.add
        local.get $l8
        i32.const 52
        i32.add
        local.get $l8
        i32.const -64
        i32.sub
        call $f70389
        local.get $l8
        local.get $l8
        f32.load offset=104
        local.tee $l12
        f32.store offset=208
        local.get $l8
        local.get $l8
        f32.load offset=108
        local.tee $l15
        f32.store offset=212
        local.get $l8
        local.get $l8
        f32.load offset=112
        local.tee $l17
        f32.store offset=216
        local.get $l8
        local.get $l8
        f32.load offset=116
        local.tee $l16
        f32.store offset=192
        local.get $l8
        local.get $l8
        f32.load offset=120
        local.tee $l14
        f32.store offset=196
        local.get $l8
        local.get $l8
        f32.load offset=124
        local.tee $l19
        f32.store offset=200
        local.get $l16
        local.get $l12
        f32.sub
        local.tee $l10
        local.get $l10
        f32.mul
        local.get $l14
        local.get $l15
        f32.sub
        local.tee $l9
        local.get $l9
        f32.mul
        f32.add
        local.get $l19
        local.get $l17
        f32.sub
        local.tee $l11
        local.get $l11
        f32.mul
        f32.add
        f32.sqrt
        local.tee $l20
        f32.const 0x0p+0 (;=0;)
        f32.gt
        if $I19
          local.get $l8
          local.get $l17
          local.get $l11
          f32.const 0x1.47ae14p-7 (;=0.01;)
          local.get $l20
          f32.div
          local.tee $l20
          f32.mul
          local.tee $l11
          f32.sub
          local.tee $l17
          f32.store offset=216
          local.get $l8
          local.get $l15
          local.get $l9
          local.get $l20
          f32.mul
          local.tee $l9
          f32.sub
          local.tee $l15
          f32.store offset=212
          local.get $l8
          local.get $l12
          local.get $l10
          local.get $l20
          f32.mul
          local.tee $l10
          f32.sub
          local.tee $l12
          f32.store offset=208
          local.get $l8
          local.get $l19
          local.get $l11
          f32.add
          local.tee $l11
          f32.store offset=200
          local.get $l11
          local.get $l17
          f32.sub
          local.set $l11
          local.get $l8
          local.get $l14
          local.get $l9
          f32.add
          local.tee $l9
          f32.store offset=196
          local.get $l8
          local.get $l16
          local.get $l10
          f32.add
          local.tee $l10
          f32.store offset=192
          local.get $l10
          local.get $l12
          f32.sub
          local.set $l10
          local.get $l9
          local.get $l15
          f32.sub
          local.set $l9
        end
        local.get $l8
        local.get $l10
        f32.store offset=176
        local.get $l8
        f32.load offset=136
        local.set $l16
        local.get $l8
        local.get $l11
        f32.store offset=184
        local.get $l8
        local.get $l9
        f32.store offset=180
        local.get $l8
        local.get $l11
        local.get $l13
        f32.mul
        local.get $l10
        local.get $l16
        f32.mul
        f32.sub
        local.tee $l19
        f32.store offset=164
        local.get $l8
        local.get $l9
        local.get $l16
        f32.mul
        local.get $l11
        local.get $l8
        f32.load offset=132
        local.tee $l14
        f32.mul
        f32.sub
        local.tee $l11
        f32.store offset=160
        local.get $l8
        local.get $l10
        local.get $l14
        f32.mul
        local.get $l9
        local.get $l13
        f32.mul
        f32.sub
        local.tee $l9
        f32.store offset=168
        local.get $l8
        local.get $l17
        local.get $l9
        f32.mul
        local.get $l12
        local.get $l11
        f32.mul
        local.get $l15
        local.get $l19
        f32.mul
        f32.add
        f32.add
        f32.neg
        f32.store offset=172
        local.get $l9
        f32.abs
        local.set $l9
        f32.const 0x1p+0 (;=1;)
        block $B20 (result i32)
          block $B21
            block $B22
              local.get $l19
              f32.abs
              local.tee $l10
              local.get $l11
              f32.abs
              local.tee $l11
              f32.gt
              i32.eqz
              br_if $B22
              local.get $l9
              local.get $l10
              f32.lt
              i32.eqz
              br_if $B22
              i32.const 0
              local.set $p4
              i32.const 2
              local.set $p2
              br $B21
            end
            i32.const 2
            local.set $p0
            i32.const 0
            local.set $p2
            i32.const 1
            local.tee $p4
            local.get $l9
            local.get $l11
            f32.gt
            i32.eqz
            br_if $B20
            drop
          end
          local.get $p4
          local.set $p0
          local.get $p2
        end
        local.tee $p4
        i32.const 2
        i32.shl
        local.tee $p2
        local.get $l8
        i32.const 176
        i32.add
        i32.add
        f32.load
        local.get $p0
        i32.const 2
        i32.shl
        local.tee $p1
        local.get $l8
        i32.const 128
        i32.add
        i32.add
        f32.load
        f32.mul
        local.get $l8
        i32.const 176
        i32.add
        local.get $p1
        i32.add
        f32.load
        local.get $l8
        i32.const 128
        i32.add
        local.get $p2
        i32.add
        f32.load
        f32.mul
        f32.sub
        f32.div
        local.set $l10
        i32.const 0
        local.set $p2
        loop $L23
          block $B24
            local.get $l8
            i32.const 208
            i32.add
            local.get $l8
            i32.const 192
            i32.add
            local.get $l8
            i32.const 176
            i32.add
            local.get $l8
            i32.const 160
            i32.add
            local.get $p4
            local.get $p0
            local.get $l10
            local.get $l8
            i32.const 128
            i32.add
            local.get $l8
            i32.const 224
            i32.add
            local.get $p3
            i32.load8_u
            i32.const 12
            i32.mul
            i32.add
            local.get $l8
            i32.const 224
            i32.add
            local.get $p3
            i32.load8_u offset=1
            i32.const 12
            i32.mul
            i32.add
            local.get $l8
            i32.const 8
            i32.add
            local.get $l8
            i32.const 144
            i32.add
            call $f70167
            i32.eqz
            br_if $B24
            local.get $p6
            i32.load offset=4096
            local.tee $p1
            i32.const 63
            i32.gt_u
            br_if $B24
            local.get $l8
            f32.load offset=8
            local.set $l9
            local.get $l8
            f32.load offset=148
            local.set $l11
            local.get $l8
            f32.load offset=152
            local.set $l12
            local.get $l8
            f32.load offset=144
            local.set $l15
            local.get $p6
            local.get $p1
            i32.const 1
            i32.add
            i32.store offset=4096
            local.get $p6
            local.get $p1
            i32.const 6
            i32.shl
            i32.add
            local.tee $p1
            local.get $l15
            local.get $l13
            local.get $l9
            f32.mul
            f32.sub
            f32.store offset=16
            local.get $p1
            local.get $l16
            f32.store offset=8
            local.get $p1
            local.get $l14
            f32.store offset=4
            local.get $p1
            local.get $l13
            f32.store
            local.get $p1
            i32.const -1
            i32.store offset=52
            local.get $p1
            local.get $l18
            local.get $l9
            f32.add
            f32.neg
            f32.store offset=12
            local.get $p1
            local.get $l12
            local.get $l16
            local.get $l9
            f32.mul
            f32.sub
            f32.store offset=24
            local.get $p1
            local.get $l11
            local.get $l14
            local.get $l9
            f32.mul
            f32.sub
            f32.store offset=20
          end
          local.get $p3
          i32.const 2
          i32.add
          local.set $p3
          local.get $p2
          i32.const 1
          i32.add
          local.tee $p2
          i32.const 12
          i32.ne
          br_if $L23
        end
        local.get $p6
        i32.load offset=4096
        br_if $B1
        local.get $p7
        f32.load offset=4
        local.set $l9
        local.get $l8
        f32.load offset=116
        local.set $l10
        local.get $l8
        f32.load offset=104
        local.set $l11
        local.get $l8
        f32.load offset=120
        local.set $l12
        local.get $l8
        f32.load offset=108
        local.set $l15
        local.get $l8
        f32.load offset=124
        local.set $l18
        local.get $l8
        f32.load offset=112
        local.set $l17
        local.get $p6
        local.get $l16
        f32.store offset=8
        local.get $p6
        local.get $l14
        f32.store offset=4
        local.get $p6
        local.get $l13
        f32.store
        i32.const 1
        local.set $p3
        local.get $p6
        i32.const 1
        i32.store offset=4096
        local.get $p6
        i32.const -1
        i32.store offset=52
        local.get $p6
        local.get $l17
        local.get $l18
        f32.add
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        f32.store offset=24
        local.get $p6
        local.get $l15
        local.get $l12
        f32.add
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        f32.store offset=20
        local.get $p6
        local.get $l11
        local.get $l10
        f32.add
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        f32.store offset=16
        local.get $p6
        local.get $l37
        local.get $l9
        f32.add
        f32.neg
        f32.store offset=12
        br $B0
      end
      i32.const 1
      local.set $p3
    end
    local.get $l8
    i32.const 320
    i32.add
    global.set $g0
    local.get $p3)
