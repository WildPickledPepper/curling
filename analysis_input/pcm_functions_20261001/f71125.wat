  (func $f71125 (type $t29) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 i32) (param $p7 i32) (param $p8 i32) (param $p9 i32)
    (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32) (local $l33 f32) (local $l34 f32) (local $l35 f32) (local $l36 f32) (local $l37 f32) (local $l38 f32) (local $l39 f32) (local $l40 f32) (local $l41 f32) (local $l42 f32) (local $l43 f32) (local $l44 f32) (local $l45 f32) (local $l46 i64) (local $l47 i64)
    global.get $g0
    i32.const 160
    i32.sub
    local.tee $l11
    global.set $g0
    local.get $p0
    i32.const 112
    i32.add
    local.set $l10
    block $B0
      local.get $p2
      local.get $p0
      i32.load offset=444
      local.tee $l12
      local.get $p3
      i32.const 80
      i32.mul
      i32.add
      i32.load offset=72
      i32.eq
      if $I1
        local.get $p5
        f32.load offset=20
        local.set $l14
        local.get $p5
        f32.load offset=24
        local.set $l15
        local.get $p5
        f32.load
        local.set $l16
        local.get $p5
        f32.load offset=4
        local.set $l18
        local.get $p5
        f32.load offset=8
        local.set $l19
        local.get $p5
        f32.load offset=16
        local.set $l20
        local.get $p6
        f32.load offset=20
        local.set $l21
        local.get $p6
        f32.load
        local.set $l22
        local.get $p6
        f32.load offset=4
        local.set $l23
        local.get $p6
        f32.load offset=8
        local.set $l24
        local.get $p6
        f32.load offset=16
        local.set $l25
        local.get $l11
        local.get $p6
        f32.load offset=24
        f32.neg
        f32.store offset=152
        local.get $l11
        local.get $l21
        f32.neg
        f32.store offset=148
        local.get $l11
        i32.const 0
        i32.store offset=156
        local.get $l11
        i32.const 0
        i32.store offset=140
        local.get $l11
        local.get $l25
        f32.neg
        f32.store offset=144
        local.get $l11
        local.get $l24
        f32.neg
        f32.store offset=136
        local.get $l11
        local.get $l23
        f32.neg
        f32.store offset=132
        local.get $l11
        local.get $l22
        f32.neg
        f32.store offset=128
        local.get $l11
        i32.const 96
        i32.add
        local.get $p0
        i32.load offset=396
        local.get $p3
        i32.const 96
        i32.mul
        i32.add
        local.get $l10
        local.get $p3
        call $f70976
        i32.const 120
        i32.add
        local.get $p3
        i32.const 76
        i32.mul
        local.tee $l12
        local.get $p0
        i32.const 384
        i32.add
        local.tee $p6
        i32.load
        i32.add
        local.get $l11
        i32.const 128
        i32.add
        call $f71003
        local.get $l11
        local.get $l15
        local.get $l11
        f32.load offset=120
        f32.sub
        f32.store offset=88
        local.get $l11
        local.get $l14
        local.get $l11
        f32.load offset=116
        f32.sub
        f32.store offset=84
        local.get $l11
        i32.const 0
        i32.store offset=92
        local.get $l11
        i32.const 0
        i32.store offset=76
        local.get $l11
        local.get $l20
        local.get $l11
        f32.load offset=112
        f32.sub
        f32.store offset=80
        local.get $l11
        local.get $l19
        local.get $l11
        f32.load offset=104
        f32.sub
        f32.store offset=72
        local.get $l11
        local.get $l18
        local.get $l11
        f32.load offset=100
        f32.sub
        f32.store offset=68
        local.get $l11
        local.get $l16
        local.get $l11
        f32.load offset=96
        f32.sub
        f32.store offset=64
        local.get $l11
        i32.const 56
        i32.add
        local.tee $l13
        i64.const 0
        i64.store
        local.get $l11
        i32.const 48
        i32.add
        local.tee $p5
        i64.const 0
        i64.store
        local.get $l11
        i64.const 0
        i64.store offset=40
        local.get $l11
        i64.const 0
        i64.store offset=32
        local.get $p2
        local.get $l10
        local.get $p4
        local.get $l11
        i32.const -64
        i32.sub
        call $f71009
        local.get $l11
        local.get $p1
        local.get $p2
        local.get $l10
        local.get $p4
        local.get $p9
        call $f71008
        local.get $p5
        local.get $l11
        f32.load offset=16
        f32.store
        local.get $l11
        i32.const 52
        i32.add
        local.tee $p2
        local.get $l11
        i64.load offset=20 align=4
        i64.store align=4
        local.get $l11
        i32.const 0
        i32.store offset=44
        local.get $l11
        i32.const 0
        i32.store offset=60
        local.get $l11
        local.get $l11
        f32.load
        f32.store offset=32
        local.get $l11
        local.get $l11
        i64.load offset=4 align=4
        i64.store offset=36 align=4
        local.get $l11
        local.get $l10
        local.get $p3
        call $f70976
        i32.const 120
        i32.add
        local.get $p0
        i32.load offset=348
        local.get $p3
        i32.const 112
        i32.mul
        i32.add
        local.get $p0
        i32.load offset=360
        local.get $p3
        i32.const 36
        i32.mul
        i32.add
        local.get $p6
        i32.load
        local.get $l12
        i32.add
        local.get $l11
        i32.const 128
        i32.add
        local.get $p9
        local.get $l11
        i32.const 32
        i32.add
        call $f70997
        local.get $l11
        f32.load offset=24
        local.set $l14
        local.get $l11
        i64.load offset=16
        local.set $l46
        local.get $l11
        i64.load
        local.set $l47
        local.get $l11
        f32.load offset=8
        local.set $l15
        local.get $p7
        local.get $p5
        f32.load
        f32.store
        local.get $p7
        local.get $p2
        f32.load
        f32.store offset=4
        local.get $p7
        local.get $l13
        f32.load
        f32.store offset=8
        local.get $p7
        local.get $l11
        f32.load offset=32
        f32.store offset=16
        local.get $p7
        local.get $l11
        f32.load offset=36
        f32.store offset=20
        local.get $p7
        local.get $l11
        f32.load offset=40
        f32.store offset=24
        local.get $p8
        local.get $l15
        f32.store offset=24
        local.get $p8
        local.get $l47
        i64.store offset=16
        local.get $p8
        local.get $l14
        f32.store offset=8
        local.get $p8
        local.get $l46
        i64.store
        br $B0
      end
      global.get $g0
      i32.const 9344
      i32.sub
      local.tee $p4
      global.set $g0
      local.get $p2
      local.set $p1
      local.get $p2
      local.get $p3
      i32.ne
      if $I2
        local.get $p2
        local.set $p0
        local.get $p3
        local.set $p1
        loop $L3
          block $B4
            local.get $p0
            local.get $p1
            i32.lt_u
            if $I5
              local.get $l12
              local.get $p1
              i32.const 80
              i32.mul
              i32.add
              i32.load offset=72
              local.set $p1
              br $B4
            end
            local.get $l12
            local.get $p0
            i32.const 80
            i32.mul
            i32.add
            i32.load offset=72
            local.set $p0
          end
          local.get $p0
          local.get $p1
          i32.ne
          br_if $L3
        end
      end
      local.get $p5
      f32.load offset=20
      local.set $l18
      local.get $p5
      f32.load
      local.set $l17
      local.get $p5
      f32.load offset=4
      local.set $l19
      local.get $p5
      f32.load offset=8
      local.set $l20
      local.get $p5
      f32.load offset=16
      local.set $l23
      local.get $p4
      local.get $p5
      f32.load offset=24
      f32.neg
      local.tee $l24
      f32.store offset=120
      local.get $p4
      local.get $l18
      f32.neg
      local.tee $l18
      f32.store offset=116
      i32.const 0
      local.set $p0
      local.get $p4
      i32.const 0
      i32.store offset=124
      local.get $p4
      local.get $l23
      f32.neg
      local.tee $l23
      f32.store offset=112
      local.get $p4
      i32.const 0
      i32.store offset=108
      local.get $p4
      local.get $l20
      f32.neg
      local.tee $l20
      f32.store offset=104
      local.get $p4
      local.get $l19
      f32.neg
      local.tee $l19
      f32.store offset=100
      local.get $p4
      local.get $l17
      f32.neg
      local.tee $l17
      f32.store offset=96
      local.get $p6
      f32.load offset=20
      local.set $l14
      local.get $p6
      f32.load offset=24
      local.set $l15
      local.get $p6
      f32.load offset=16
      local.set $l16
      local.get $p6
      f32.load offset=8
      local.set $l21
      local.get $p6
      f32.load offset=4
      local.set $l22
      local.get $p6
      f32.load
      local.set $l25
      local.get $p4
      i32.const 128
      i32.add
      local.get $p2
      i32.const 5
      i32.shl
      i32.add
      local.tee $p5
      i32.const 0
      i32.store offset=28
      local.get $p5
      local.get $l24
      f32.store offset=24
      local.get $p5
      local.get $l18
      f32.store offset=20
      local.get $p5
      local.get $l23
      f32.store offset=16
      local.get $p5
      i32.const 0
      i32.store offset=12
      local.get $p5
      local.get $l20
      f32.store offset=8
      local.get $p5
      local.get $l19
      f32.store offset=4
      local.get $p5
      local.get $l17
      f32.store
      local.get $p4
      local.get $l15
      f32.neg
      local.tee $l15
      f32.store offset=88
      local.get $p4
      local.get $l14
      f32.neg
      local.tee $l14
      f32.store offset=84
      local.get $p4
      i32.const 128
      i32.add
      local.get $p3
      i32.const 5
      i32.shl
      i32.add
      local.tee $p5
      local.get $l25
      f32.neg
      local.tee $l25
      f32.store
      local.get $p5
      local.get $l22
      f32.neg
      local.tee $l22
      f32.store offset=4
      local.get $p5
      local.get $l21
      f32.neg
      local.tee $l21
      f32.store offset=8
      local.get $p5
      local.get $l16
      f32.neg
      local.tee $l16
      f32.store offset=16
      local.get $p5
      local.get $l14
      f32.store offset=20
      local.get $p5
      local.get $l15
      f32.store offset=24
      local.get $p5
      i32.const 0
      i32.store offset=28
      local.get $p5
      i32.const 0
      i32.store offset=12
      local.get $p4
      i32.const 0
      i32.store offset=92
      local.get $p4
      i32.const 0
      i32.store offset=76
      local.get $p4
      local.get $l16
      f32.store offset=80
      local.get $p4
      local.get $l21
      f32.store offset=72
      local.get $p4
      local.get $l22
      f32.store offset=68
      local.get $p4
      local.get $l25
      f32.store offset=64
      local.get $p1
      local.get $p2
      i32.ne
      if $I6
        loop $L7
          local.get $p4
          i32.const 32
          i32.add
          local.get $l10
          i32.load offset=284
          local.get $p2
          i32.const 96
          i32.mul
          i32.add
          local.get $l10
          local.get $p2
          call $f70976
          i32.const 120
          i32.add
          local.get $l10
          i32.load offset=272
          local.get $p2
          i32.const 76
          i32.mul
          i32.add
          local.get $p4
          i32.const 96
          i32.add
          call $f71003
          local.get $p4
          i32.const 0
          i32.store offset=108
          local.get $p4
          i32.const 0
          i32.store offset=124
          local.get $p4
          local.get $p4
          f32.load offset=32
          local.tee $l17
          f32.store offset=96
          local.get $p4
          local.get $p4
          f32.load offset=36
          local.tee $l19
          f32.store offset=100
          local.get $p4
          local.get $p4
          f32.load offset=40
          local.tee $l20
          f32.store offset=104
          local.get $p4
          local.get $p4
          f32.load offset=48
          local.tee $l23
          f32.store offset=112
          local.get $p4
          local.get $p4
          f32.load offset=52
          local.tee $l18
          f32.store offset=116
          local.get $p4
          local.get $p4
          f32.load offset=56
          local.tee $l24
          f32.store offset=120
          local.get $l12
          local.get $p2
          i32.const 80
          i32.mul
          i32.add
          i32.load offset=72
          local.set $p5
          local.get $p4
          i32.const 8320
          i32.add
          local.get $p0
          i32.const 2
          i32.shl
          i32.add
          local.get $p2
          i32.store
          local.get $p4
          i32.const 128
          i32.add
          local.get $p5
          i32.const 5
          i32.shl
          i32.add
          local.tee $p2
          i32.const 0
          i32.store offset=28
          local.get $p2
          local.get $l23
          f32.store offset=16
          local.get $p2
          i32.const 0
          i32.store offset=12
          local.get $p2
          local.get $l20
          f32.store offset=8
          local.get $p2
          local.get $l19
          f32.store offset=4
          local.get $p2
          local.get $l17
          f32.store
          local.get $p2
          local.get $l24
          f32.store offset=24
          local.get $p2
          local.get $l18
          f32.store offset=20
          local.get $p0
          i32.const 1
          i32.add
          local.set $p0
          local.get $p1
          local.get $p5
          local.tee $p2
          i32.ne
          br_if $L7
        end
      end
      block $B8
        local.get $p1
        local.get $p3
        i32.ne
        if $I9
          local.get $p0
          local.set $p5
          loop $L10
            local.get $p4
            i32.const 32
            i32.add
            local.get $l10
            i32.load offset=284
            local.get $p3
            i32.const 96
            i32.mul
            i32.add
            local.get $l10
            local.get $p3
            call $f70976
            i32.const 120
            i32.add
            local.get $l10
            i32.load offset=272
            local.get $p3
            i32.const 76
            i32.mul
            i32.add
            local.get $p4
            i32.const -64
            i32.sub
            call $f71003
            local.get $p4
            i32.const 0
            i32.store offset=76
            local.get $p4
            i32.const 0
            i32.store offset=92
            local.get $p4
            local.get $p4
            f32.load offset=32
            local.tee $l14
            f32.store offset=64
            local.get $p4
            local.get $p4
            f32.load offset=36
            local.tee $l15
            f32.store offset=68
            local.get $p4
            local.get $p4
            f32.load offset=40
            local.tee $l16
            f32.store offset=72
            local.get $p4
            local.get $p4
            f32.load offset=48
            local.tee $l21
            f32.store offset=80
            local.get $p4
            local.get $p4
            f32.load offset=52
            local.tee $l22
            f32.store offset=84
            local.get $p4
            local.get $p4
            f32.load offset=56
            local.tee $l25
            f32.store offset=88
            local.get $l12
            local.get $p3
            i32.const 80
            i32.mul
            i32.add
            i32.load offset=72
            local.set $p6
            local.get $p4
            i32.const 8320
            i32.add
            local.get $p5
            i32.const 2
            i32.shl
            i32.add
            local.get $p3
            i32.store
            local.get $p4
            i32.const 128
            i32.add
            local.get $p6
            i32.const 5
            i32.shl
            i32.add
            local.tee $p2
            i32.const 0
            i32.store offset=28
            local.get $p2
            local.get $l21
            f32.store offset=16
            local.get $p2
            i32.const 0
            i32.store offset=12
            local.get $p2
            local.get $l16
            f32.store offset=8
            local.get $p2
            local.get $l15
            f32.store offset=4
            local.get $p2
            local.get $l14
            f32.store
            local.get $p2
            local.get $l25
            f32.store offset=24
            local.get $p2
            local.get $l22
            f32.store offset=20
            local.get $p5
            i32.const 1
            i32.add
            local.set $p5
            local.get $p1
            local.get $p6
            local.tee $p3
            i32.ne
            br_if $L10
          end
          local.get $p4
          f32.load offset=120
          local.set $l24
          local.get $p4
          f32.load offset=116
          local.set $l18
          local.get $p4
          f32.load offset=112
          local.set $l23
          local.get $p4
          f32.load offset=104
          local.set $l20
          local.get $p4
          f32.load offset=100
          local.set $l19
          local.get $p4
          f32.load offset=96
          local.set $l17
          br $B8
        end
        local.get $p4
        f32.load offset=88
        local.set $l25
        local.get $p4
        f32.load offset=84
        local.set $l22
        local.get $p4
        f32.load offset=80
        local.set $l21
        local.get $p4
        f32.load offset=72
        local.set $l16
        local.get $p4
        f32.load offset=68
        local.set $l15
        local.get $p4
        f32.load offset=64
        local.set $l14
        local.get $p0
        local.set $p5
      end
      local.get $p4
      i32.const 128
      i32.add
      local.get $p1
      i32.const 5
      i32.shl
      i32.add
      local.tee $p2
      i32.const 0
      i32.store offset=28
      local.get $p2
      local.get $l23
      local.get $l21
      f32.add
      f32.store offset=16
      local.get $p2
      i32.const 0
      i32.store offset=12
      local.get $p2
      local.get $l20
      local.get $l16
      f32.add
      f32.store offset=8
      local.get $p2
      local.get $l19
      local.get $l15
      f32.add
      f32.store offset=4
      local.get $p2
      local.get $l17
      local.get $l14
      f32.add
      f32.store
      local.get $p2
      local.get $l24
      local.get $l25
      f32.add
      f32.store offset=24
      local.get $p2
      local.get $l18
      local.get $l22
      f32.add
      f32.store offset=20
      local.get $p5
      local.set $p3
      local.get $p1
      if $I11
        loop $L12
          local.get $p4
          i32.const 32
          i32.add
          local.get $l10
          i32.load offset=284
          local.get $p1
          i32.const 96
          i32.mul
          i32.add
          local.get $l10
          local.get $p1
          call $f70976
          i32.const 120
          i32.add
          local.get $l10
          i32.load offset=260
          local.get $p1
          i32.const 76
          i32.mul
          i32.add
          local.get $p4
          i32.const 128
          i32.add
          local.get $p1
          i32.const 5
          i32.shl
          i32.add
          call $f71003
          local.get $p4
          i32.const 128
          i32.add
          local.get $l12
          local.get $p1
          i32.const 80
          i32.mul
          i32.add
          i32.load offset=72
          local.tee $p6
          i32.const 5
          i32.shl
          i32.add
          local.tee $p2
          local.get $p4
          f32.load offset=32
          f32.store
          local.get $p2
          i32.const 0
          i32.store offset=12
          local.get $p2
          local.get $p4
          i64.load offset=36 align=4
          i64.store offset=4 align=4
          local.get $p2
          local.get $p4
          f32.load offset=48
          f32.store offset=16
          local.get $p2
          i32.const 0
          i32.store offset=28
          local.get $p2
          local.get $p4
          i64.load offset=52 align=4
          i64.store offset=20 align=4
          local.get $p4
          i32.const 8320
          i32.add
          local.get $p3
          i32.const 2
          i32.shl
          i32.add
          local.get $p1
          i32.store
          local.get $p3
          i32.const 1
          i32.add
          local.set $p3
          local.get $p6
          local.tee $p1
          br_if $L12
        end
      end
      block $B13 (result f32)
        local.get $l10
        i32.load offset=364
        i32.load8_u
        i32.const 1
        i32.and
        i32.eqz
        if $I14
          local.get $p4
          f32.load offset=148
          local.set $l24
          local.get $p4
          f32.load offset=144
          local.set $l14
          local.get $p4
          f32.load offset=136
          local.set $l15
          local.get $p4
          f32.load offset=132
          local.set $l18
          local.get $p4
          f32.load offset=128
          local.set $l16
          local.get $p4
          f32.load offset=152
          br $B13
        end
        local.get $p4
        i64.const 0
        i64.store offset=152
        local.get $p4
        i64.const 0
        i64.store offset=144
        local.get $p4
        i64.const 0
        i64.store offset=136
        local.get $p4
        i64.const 0
        i64.store offset=128
        f32.const 0x0p+0 (;=0;)
        local.set $l24
        f32.const 0x0p+0 (;=0;)
        local.set $l14
        f32.const 0x0p+0 (;=0;)
        local.set $l15
        f32.const 0x0p+0 (;=0;)
        local.set $l18
        f32.const 0x0p+0 (;=0;)
        local.set $l16
        f32.const 0x0p+0 (;=0;)
      end
      local.set $l17
      local.get $l10
      f32.load offset=468
      local.set $l29
      local.get $l10
      f32.load offset=456
      local.set $l30
      local.get $l10
      f32.load offset=444
      local.set $l31
      local.get $l10
      f32.load offset=472
      local.set $l32
      local.get $l10
      f32.load offset=460
      local.set $l33
      local.get $l10
      f32.load offset=448
      local.set $l34
      local.get $l10
      f32.load offset=476
      local.set $l35
      local.get $l10
      f32.load offset=464
      local.set $l36
      local.get $l10
      f32.load offset=452
      local.set $l37
      local.get $l10
      f32.load offset=416
      local.set $l20
      local.get $l10
      f32.load offset=412
      local.set $l19
      local.get $l10
      f32.load offset=504
      local.set $l23
      local.get $l10
      f32.load offset=492
      local.set $l38
      local.get $l10
      f32.load offset=480
      local.set $l39
      local.get $l10
      f32.load offset=428
      local.set $l25
      local.get $l10
      f32.load offset=424
      local.set $l26
      local.get $l10
      f32.load offset=420
      local.set $l27
      local.get $l10
      f32.load offset=508
      local.set $l40
      local.get $l10
      f32.load offset=496
      local.set $l41
      local.get $l10
      f32.load offset=484
      local.set $l42
      local.get $l10
      f32.load offset=408
      local.set $l28
      local.get $p4
      local.get $l10
      f32.load offset=436
      local.tee $l43
      local.get $l24
      f32.neg
      local.tee $l21
      f32.mul
      local.get $l14
      local.get $l10
      f32.load offset=432
      local.tee $l44
      f32.mul
      f32.sub
      local.get $l17
      local.get $l10
      f32.load offset=440
      local.tee $l45
      f32.mul
      f32.sub
      local.get $l10
      f32.load offset=500
      local.get $l18
      f32.neg
      local.tee $l22
      f32.mul
      local.get $l16
      local.get $l10
      f32.load offset=488
      f32.mul
      f32.sub
      local.get $l15
      local.get $l10
      f32.load offset=512
      f32.mul
      f32.sub
      f32.add
      local.tee $l24
      f32.store offset=56
      local.get $p4
      local.get $l26
      local.get $l21
      f32.mul
      local.get $l14
      local.get $l27
      f32.mul
      f32.sub
      local.get $l17
      local.get $l25
      f32.mul
      f32.sub
      local.get $l41
      local.get $l22
      f32.mul
      local.get $l16
      local.get $l42
      f32.mul
      f32.sub
      local.get $l15
      local.get $l40
      f32.mul
      f32.sub
      f32.add
      local.tee $l18
      f32.store offset=52
      local.get $p4
      i32.const 0
      i32.store offset=60
      local.get $p4
      i32.const 0
      i32.store offset=44
      local.get $p4
      local.get $l19
      local.get $l21
      f32.mul
      local.get $l14
      local.get $l28
      f32.mul
      f32.sub
      local.get $l17
      local.get $l20
      f32.mul
      f32.sub
      local.get $l38
      local.get $l22
      f32.mul
      local.get $l16
      local.get $l39
      f32.mul
      f32.sub
      local.get $l15
      local.get $l23
      f32.mul
      f32.sub
      f32.add
      local.tee $l23
      f32.store offset=48
      local.get $p4
      local.get $l25
      local.get $l22
      f32.mul
      local.get $l16
      local.get $l20
      f32.mul
      f32.sub
      local.get $l15
      local.get $l45
      f32.mul
      f32.sub
      local.get $l36
      local.get $l21
      f32.mul
      local.get $l14
      local.get $l37
      f32.mul
      f32.sub
      local.get $l17
      local.get $l35
      f32.mul
      f32.sub
      f32.add
      local.tee $l20
      f32.store offset=40
      local.get $p4
      local.get $l26
      local.get $l22
      f32.mul
      local.get $l16
      local.get $l19
      f32.mul
      f32.sub
      local.get $l15
      local.get $l43
      f32.mul
      f32.sub
      local.get $l33
      local.get $l21
      f32.mul
      local.get $l14
      local.get $l34
      f32.mul
      f32.sub
      local.get $l17
      local.get $l32
      f32.mul
      f32.sub
      f32.add
      local.tee $l19
      f32.store offset=36
      local.get $p4
      local.get $l27
      local.get $l22
      f32.mul
      local.get $l16
      local.get $l28
      f32.mul
      f32.sub
      local.get $l15
      local.get $l44
      f32.mul
      f32.sub
      local.get $l30
      local.get $l21
      f32.mul
      local.get $l14
      local.get $l31
      f32.mul
      f32.sub
      local.get $l17
      local.get $l29
      f32.mul
      f32.sub
      f32.add
      local.tee $l17
      f32.store offset=32
      local.get $p3
      local.get $p5
      i32.gt_u
      if $I15
        loop $L16
          local.get $p4
          local.get $l10
          local.get $p4
          i32.const 8320
          i32.add
          local.get $p3
          i32.const 1
          i32.sub
          local.tee $p3
          i32.const 2
          i32.shl
          i32.add
          i32.load
          local.tee $p1
          call $f70976
          i32.const 120
          i32.add
          local.get $l10
          i32.load offset=236
          local.get $p1
          i32.const 112
          i32.mul
          i32.add
          local.get $l10
          i32.load offset=248
          local.get $p1
          i32.const 36
          i32.mul
          i32.add
          local.get $l10
          i32.load offset=272
          local.get $p1
          i32.const 76
          i32.mul
          i32.add
          local.get $p4
          i32.const 128
          i32.add
          local.get $p1
          i32.const 5
          i32.shl
          i32.add
          local.get $p9
          local.get $p4
          i32.const 32
          i32.add
          call $f70997
          local.get $p4
          i32.const 0
          i32.store offset=44
          local.get $p4
          i32.const 0
          i32.store offset=60
          local.get $p4
          local.get $p4
          f32.load
          local.tee $l17
          f32.store offset=32
          local.get $p4
          local.get $p4
          f32.load offset=4
          local.tee $l19
          f32.store offset=36
          local.get $p4
          local.get $p4
          f32.load offset=8
          local.tee $l20
          f32.store offset=40
          local.get $p4
          local.get $p4
          f32.load offset=16
          local.tee $l23
          f32.store offset=48
          local.get $p4
          local.get $p4
          f32.load offset=20
          local.tee $l18
          f32.store offset=52
          local.get $p4
          local.get $p4
          f32.load offset=24
          local.tee $l24
          f32.store offset=56
          local.get $p3
          local.get $p5
          i32.gt_u
          br_if $L16
        end
      end
      local.get $l24
      local.set $l14
      local.get $l18
      local.set $l15
      local.get $l23
      local.set $l16
      local.get $l20
      local.set $l21
      local.get $l19
      local.set $l22
      local.get $l17
      local.set $l25
      local.get $p0
      local.get $p5
      i32.lt_u
      if $I17
        loop $L18
          local.get $p4
          local.get $l10
          local.get $p4
          i32.const 8320
          i32.add
          local.get $p5
          i32.const 1
          i32.sub
          local.tee $p5
          i32.const 2
          i32.shl
          i32.add
          i32.load
          local.tee $p1
          call $f70976
          i32.const 120
          i32.add
          local.get $l10
          i32.load offset=236
          local.get $p1
          i32.const 112
          i32.mul
          i32.add
          local.get $l10
          i32.load offset=248
          local.get $p1
          i32.const 36
          i32.mul
          i32.add
          local.get $l10
          i32.load offset=272
          local.get $p1
          i32.const 76
          i32.mul
          i32.add
          local.get $p4
          i32.const 128
          i32.add
          local.get $p1
          i32.const 5
          i32.shl
          i32.add
          local.get $p9
          local.get $p4
          i32.const 32
          i32.add
          call $f70997
          local.get $p0
          local.get $p5
          i32.lt_u
          br_if $L18
        end
        local.get $p4
        f32.load offset=24
        local.set $l14
        local.get $p4
        f32.load offset=20
        local.set $l15
        local.get $p4
        f32.load offset=16
        local.set $l16
        local.get $p4
        f32.load offset=8
        local.set $l21
        local.get $p4
        f32.load offset=4
        local.set $l22
        local.get $p4
        f32.load offset=56
        local.set $l24
        local.get $p4
        f32.load offset=52
        local.set $l18
        local.get $p4
        f32.load offset=48
        local.set $l23
        local.get $p4
        f32.load offset=40
        local.set $l20
        local.get $p4
        f32.load offset=36
        local.set $l19
        local.get $p4
        f32.load offset=32
        local.set $l17
        local.get $p4
        f32.load
        local.set $l25
      end
      local.get $p7
      local.get $p0
      if $I19 (result f32)
        loop $L20
          local.get $p4
          local.get $l10
          local.get $p4
          i32.const 8320
          i32.add
          local.get $p0
          i32.const 1
          i32.sub
          local.tee $p0
          i32.const 2
          i32.shl
          i32.add
          i32.load
          local.tee $p1
          call $f70976
          i32.const 120
          i32.add
          local.get $l10
          i32.load offset=236
          local.get $p1
          i32.const 112
          i32.mul
          i32.add
          local.get $l10
          i32.load offset=248
          local.get $p1
          i32.const 36
          i32.mul
          i32.add
          local.get $l10
          i32.load offset=272
          local.get $p1
          i32.const 76
          i32.mul
          i32.add
          local.get $p4
          i32.const 128
          i32.add
          local.get $p1
          i32.const 5
          i32.shl
          i32.add
          local.get $p9
          local.get $p4
          i32.const 32
          i32.add
          call $f70997
          local.get $p0
          br_if $L20
        end
        local.get $p4
        f32.load offset=24
        local.set $l24
        local.get $p4
        f32.load offset=20
        local.set $l18
        local.get $p4
        f32.load offset=16
        local.set $l23
        local.get $p4
        f32.load offset=8
        local.set $l20
        local.get $p4
        f32.load offset=4
        local.set $l19
        local.get $p4
        f32.load
      else
        local.get $l17
      end
      f32.store offset=16
      local.get $p7
      local.get $l24
      f32.store offset=8
      local.get $p7
      local.get $l18
      f32.store offset=4
      local.get $p7
      local.get $l23
      f32.store
      local.get $p7
      local.get $l20
      f32.store offset=24
      local.get $p7
      local.get $l19
      f32.store offset=20
      local.get $p8
      local.get $l21
      f32.store offset=24
      local.get $p8
      local.get $l22
      f32.store offset=20
      local.get $p8
      local.get $l25
      f32.store offset=16
      local.get $p8
      local.get $l14
      f32.store offset=8
      local.get $p8
      local.get $l15
      f32.store offset=4
      local.get $p8
      local.get $l16
      f32.store
      local.get $p4
      i32.const 9344
      i32.add
      global.set $g0
    end
    local.get $l11
    i32.const 160
    i32.add
    global.set $g0)
