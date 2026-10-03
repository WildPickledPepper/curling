  (func $f70483 (type $t171) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 f32) (param $p7 i32) (param $p8 i32) (param $p9 f32) (param $p10 i32) (param $p11 f32) (result f32)
    (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 i32) (local $l17 i32) (local $l18 i32) (local $l19 i32) (local $l20 i32) (local $l21 i32) (local $l22 i32) (local $l23 i32) (local $l24 i32) (local $l25 i32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32) (local $l33 f32) (local $l34 f32) (local $l35 f32) (local $l36 f32) (local $l37 f32) (local $l38 f32) (local $l39 f32) (local $l40 f32) (local $l41 f32) (local $l42 f32) (local $l43 f32) (local $l44 f32) (local $l45 f32) (local $l46 f32) (local $l47 f32)
    global.get $g0
    i32.const 720
    i32.sub
    local.tee $l12
    global.set $g0
    local.get $p1
    i32.load
    local.tee $l13
    i32.load offset=4
    local.set $l14
    local.get $l12
    local.get $l13
    i32.store offset=672
    local.get $l12
    local.get $l14
    i32.store offset=668
    local.get $l12
    f32.const 0x1p+0 (;=1;)
    local.get $l13
    f32.load offset=8
    f32.div
    f32.store offset=660
    local.get $l12
    f32.const 0x1p+0 (;=1;)
    local.get $l13
    f32.load offset=12
    f32.div
    f32.store offset=656
    local.get $l12
    f32.const 0x1p+0 (;=1;)
    local.get $l13
    f32.load offset=16
    f32.div
    f32.store offset=664
    local.get $l12
    i64.const 274877906944
    i64.store offset=648
    local.get $l12
    i32.const 1
    i32.store8 offset=640
    local.get $l12
    local.get $l12
    i32.const 384
    i32.add
    i32.store offset=644
    local.get $l12
    i32.const 3132216
    i32.store offset=376
    local.get $l12
    local.get $l12
    i32.const 384
    i32.add
    i32.store offset=380
    local.get $p4
    f32.load offset=24
    local.set $p9
    local.get $p2
    f32.load offset=24
    local.set $l26
    local.get $p4
    f32.load offset=16
    local.set $l28
    local.get $p2
    f32.load offset=16
    local.set $l27
    local.get $l12
    local.get $p2
    f32.load offset=20
    local.get $p4
    f32.load offset=20
    f32.sub
    local.tee $l33
    f32.store offset=364
    local.get $l12
    local.get $l26
    local.get $p9
    f32.sub
    local.tee $p9
    f32.store offset=368
    local.get $l12
    local.get $l27
    local.get $l28
    f32.sub
    local.tee $l26
    f32.store offset=360
    local.get $p5
    f32.load offset=20
    local.set $l28
    local.get $p3
    f32.load offset=20
    local.set $l27
    local.get $p5
    f32.load offset=16
    local.set $l31
    local.get $p3
    f32.load offset=16
    local.set $l29
    local.get $l12
    local.get $p3
    f32.load offset=24
    local.get $p5
    f32.load offset=24
    f32.sub
    local.tee $l30
    f32.store offset=352
    local.get $l12
    local.get $l27
    local.get $l28
    f32.sub
    local.tee $l28
    f32.store offset=348
    local.get $l12
    local.get $l29
    local.get $l31
    f32.sub
    local.tee $l27
    f32.store offset=344
    local.get $p0
    i32.const 68
    i32.add
    local.tee $l16
    f32.load
    local.set $l31
    local.get $p0
    i32.const 80
    i32.add
    local.tee $l13
    f32.load
    local.set $l29
    local.get $p0
    f32.load offset=64
    local.set $l32
    local.get $p0
    f32.load offset=76
    local.set $l36
    local.get $l12
    local.get $p9
    local.get $l30
    f32.sub
    local.tee $l41
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    local.tee $p9
    f32.abs
    local.get $p0
    i32.const 72
    i32.add
    local.tee $l18
    f32.load
    f32.add
    local.get $p6
    f32.add
    local.tee $l30
    local.get $p9
    local.get $p0
    i32.const 84
    i32.add
    local.tee $l14
    f32.load
    f32.add
    local.tee $p9
    f32.add
    f32.store offset=340
    local.get $l12
    local.get $l31
    local.get $l33
    local.get $l28
    f32.sub
    local.tee $l42
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    local.tee $l28
    f32.abs
    f32.add
    local.get $p6
    f32.add
    local.tee $l33
    local.get $l28
    local.get $l29
    f32.add
    local.tee $l28
    f32.add
    f32.store offset=336
    local.get $l12
    local.get $l32
    local.get $l26
    local.get $l27
    f32.sub
    local.tee $l43
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    local.tee $l26
    f32.abs
    f32.add
    local.get $p6
    f32.add
    local.tee $l27
    local.get $l26
    local.get $l36
    f32.add
    local.tee $l26
    f32.add
    f32.store offset=332
    local.get $l12
    local.get $p9
    local.get $l30
    f32.sub
    f32.store offset=328
    local.get $l12
    local.get $l28
    local.get $l33
    f32.sub
    f32.store offset=324
    local.get $l12
    local.get $l26
    local.get $l27
    f32.sub
    f32.store offset=320
    local.get $l12
    i32.const 656
    i32.add
    local.get $p3
    local.get $l12
    i32.const 320
    i32.add
    i32.const 1
    local.get $l12
    i32.const 376
    i32.add
    call $f70450
    local.get $l12
    i32.const 0
    i32.store offset=312
    local.get $l12
    i64.const 0
    i64.store offset=304
    local.get $l12
    i32.load offset=648
    local.set $l15
    local.get $l12
    i32.const 0
    i32.store offset=80
    local.get $l12
    i32.const 304
    i32.add
    local.get $l15
    local.get $l12
    i32.const 80
    i32.add
    call $f70631
    local.get $l12
    i32.const 0
    i32.store offset=296
    local.get $l12
    i64.const 0
    i64.store offset=288
    local.get $l12
    i32.load offset=648
    local.set $l15
    local.get $l12
    i32.const 0
    i32.store offset=80
    local.get $l12
    i32.const 288
    i32.add
    local.get $l15
    local.get $l12
    i32.const 80
    i32.add
    call $f70631
    local.get $l12
    i32.load offset=304
    local.set $l15
    local.get $l12
    i32.load offset=288
    local.set $l19
    local.get $l12
    local.get $p0
    f32.load offset=76
    f32.store offset=272
    local.get $l12
    local.get $l13
    f32.load
    f32.store offset=276
    local.get $l12
    local.get $l14
    f32.load
    f32.store offset=280
    local.get $l12
    i32.load offset=648
    local.tee $l22
    if $I0
      local.get $p1
      i32.const 8
      i32.add
      local.set $l23
      local.get $l18
      f32.load
      local.get $p6
      f32.add
      f32.const 0x1.19999ap+0 (;=1.1;)
      f32.mul
      local.set $l44
      local.get $l16
      f32.load
      local.get $p6
      f32.add
      f32.const 0x1.19999ap+0 (;=1.1;)
      f32.mul
      local.set $l46
      local.get $p0
      f32.load offset=64
      local.get $p6
      f32.add
      f32.const 0x1.19999ap+0 (;=1.1;)
      f32.mul
      local.set $l47
      local.get $l12
      i32.load offset=644
      local.set $l24
      i32.const 0
      local.set $l18
      loop $L1
        local.get $l12
        i32.const 656
        i32.add
        local.get $l23
        local.get $l12
        i32.const 80
        i32.add
        i32.const 0
        i32.const 0
        local.get $l24
        local.get $l18
        i32.const 2
        i32.shl
        i32.add
        local.tee $l25
        i32.load
        i32.const 1
        i32.const 1
        call $f70452
        local.get $l12
        f32.load offset=92
        local.tee $p9
        local.get $l12
        f32.load offset=80
        local.tee $l26
        f32.sub
        local.tee $l35
        local.get $l12
        f32.load offset=108
        local.tee $l28
        local.get $l12
        f32.load offset=84
        local.tee $l27
        f32.sub
        local.tee $l37
        f32.mul
        local.get $l12
        f32.load offset=96
        local.tee $l33
        local.get $l27
        f32.sub
        local.tee $l38
        local.get $l12
        f32.load offset=104
        local.tee $l31
        local.get $l26
        f32.sub
        local.tee $l34
        f32.mul
        f32.sub
        local.tee $l29
        f32.neg
        local.set $l30
        local.get $l12
        f32.load offset=100
        local.tee $l32
        local.get $l12
        f32.load offset=88
        local.tee $l36
        f32.sub
        local.tee $l40
        local.get $l34
        f32.mul
        local.get $l35
        local.get $l12
        f32.load offset=112
        local.tee $l34
        local.get $l36
        f32.sub
        local.tee $l45
        f32.mul
        f32.sub
        local.tee $l35
        f32.neg
        local.set $l39
        local.get $l38
        local.get $l45
        f32.mul
        local.get $l40
        local.get $l37
        f32.mul
        f32.sub
        local.tee $l37
        f32.neg
        local.set $l38
        local.get $l29
        local.get $l29
        f32.mul
        local.get $l37
        local.get $l37
        f32.mul
        local.get $l35
        local.get $l35
        f32.mul
        f32.add
        f32.add
        f32.sqrt
        local.tee $l29
        f32.const 0x0p+0 (;=0;)
        f32.gt
        if $I2
          f32.const 0x1p+0 (;=1;)
          local.get $l29
          f32.div
          local.tee $l29
          local.get $l30
          f32.mul
          local.set $l30
          local.get $l29
          local.get $l38
          f32.mul
          local.set $l38
          local.get $l29
          local.get $l39
          f32.mul
          local.set $l39
        end
        block $B3
          local.get $l43
          local.get $l38
          f32.mul
          local.get $l42
          local.get $l39
          f32.mul
          f32.add
          local.get $l41
          local.get $l30
          f32.mul
          f32.add
          local.get $p11
          f32.ge
          i32.eqz
          br_if $B3
          local.get $l12
          local.get $l44
          f32.store offset=8
          local.get $l12
          local.get $l46
          f32.store offset=4
          local.get $l12
          local.get $l47
          f32.store
          local.get $l12
          local.get $l36
          f32.const 0x1.fffffep+125 (;=8.50706e+37;)
          f32.min
          local.tee $l29
          local.get $l32
          local.get $l29
          local.get $l32
          f32.lt
          select
          local.tee $l29
          local.get $l34
          local.get $l29
          local.get $l34
          f32.lt
          select
          local.tee $l29
          local.get $l36
          f32.const -0x1.fffffep+125 (;=-8.50706e+37;)
          f32.max
          local.tee $l30
          local.get $l32
          local.get $l30
          local.get $l32
          f32.gt
          select
          local.tee $l30
          local.get $l34
          local.get $l30
          local.get $l34
          f32.gt
          select
          local.tee $l30
          f32.add
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          f32.store offset=224
          local.get $l12
          local.get $l27
          f32.const 0x1.fffffep+125 (;=8.50706e+37;)
          f32.min
          local.tee $l32
          local.get $l33
          local.get $l32
          local.get $l33
          f32.lt
          select
          local.tee $l32
          local.get $l28
          local.get $l28
          local.get $l32
          f32.gt
          select
          local.tee $l32
          local.get $l27
          f32.const -0x1.fffffep+125 (;=-8.50706e+37;)
          f32.max
          local.tee $l27
          local.get $l33
          local.get $l27
          local.get $l33
          f32.gt
          select
          local.tee $l27
          local.get $l28
          local.get $l27
          local.get $l28
          f32.gt
          select
          local.tee $l28
          f32.add
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          f32.store offset=220
          local.get $l12
          local.get $l26
          f32.const 0x1.fffffep+125 (;=8.50706e+37;)
          f32.min
          local.tee $l27
          local.get $p9
          local.get $p9
          local.get $l27
          f32.gt
          select
          local.tee $l27
          local.get $l31
          local.get $l27
          local.get $l31
          f32.lt
          select
          local.tee $l27
          local.get $l26
          f32.const -0x1.fffffep+125 (;=-8.50706e+37;)
          f32.max
          local.tee $l26
          local.get $p9
          local.get $p9
          local.get $l26
          f32.lt
          select
          local.tee $p9
          local.get $l31
          local.get $p9
          local.get $l31
          f32.gt
          select
          local.tee $p9
          f32.add
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          f32.store offset=216
          local.get $l12
          local.get $l30
          local.get $l29
          f32.sub
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          f32.const 0x1.47ae14p-7 (;=0.01;)
          f32.add
          f32.const 0x1.19999ap+0 (;=1.1;)
          f32.mul
          f32.store offset=712
          local.get $l12
          local.get $l28
          local.get $l32
          f32.sub
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          f32.const 0x1.47ae14p-7 (;=0.01;)
          f32.add
          f32.const 0x1.19999ap+0 (;=1.1;)
          f32.mul
          f32.store offset=708
          local.get $l12
          local.get $p9
          local.get $l27
          f32.sub
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          f32.const 0x1.47ae14p-7 (;=0.01;)
          f32.add
          f32.const 0x1.19999ap+0 (;=1.1;)
          f32.mul
          f32.store offset=704
          local.get $l12
          i32.const 272
          i32.add
          local.get $l12
          local.get $l12
          i32.const 216
          i32.add
          local.get $l12
          i32.const 704
          i32.add
          local.get $l12
          i32.const 360
          i32.add
          local.get $l12
          i32.const 344
          i32.add
          call $f70620
          local.tee $l26
          f32.const 0x1p+0 (;=1;)
          f32.le
          i32.eqz
          br_if $B3
          i32.const 0
          local.set $l21
          block $B4
            local.get $l17
            local.tee $l13
            i32.eqz
            br_if $B4
            loop $L5
              local.get $l26
              local.get $l19
              local.get $l13
              i32.const 1
              i32.sub
              local.tee $l14
              i32.const 2
              i32.shl
              local.tee $l16
              i32.add
              f32.load
              local.tee $p9
              f32.ge
              if $I6
                local.get $l13
                local.set $l21
                br $B4
              end
              local.get $l19
              local.get $l13
              i32.const 2
              i32.shl
              local.tee $l13
              i32.add
              local.get $p9
              f32.store
              local.get $l13
              local.get $l15
              i32.add
              local.get $l15
              local.get $l16
              i32.add
              i32.load
              i32.store
              local.get $l14
              local.tee $l13
              br_if $L5
            end
          end
          local.get $l15
          local.get $l21
          i32.const 2
          i32.shl
          local.tee $l13
          i32.add
          local.get $l25
          i32.load
          i32.store
          local.get $l13
          local.get $l19
          i32.add
          local.get $l26
          f32.store
          local.get $l17
          i32.const 1
          i32.add
          local.set $l17
        end
        local.get $l18
        i32.const 1
        i32.add
        local.tee $l18
        local.get $l22
        i32.ne
        br_if $L1
      end
    end
    local.get $p7
    i32.const 0
    i32.store offset=8
    local.get $p7
    i64.const 0
    i64.store align=4
    local.get $p8
    i32.const 0
    i32.store offset=8
    local.get $p8
    i64.const 0
    i64.store align=4
    local.get $p0
    f32.load offset=4
    local.set $p11
    local.get $l12
    local.get $p0
    f32.load offset=32
    local.get $p3
    f32.load offset=24
    local.tee $l34
    f32.sub
    local.tee $p9
    local.get $p9
    f32.add
    local.tee $l31
    local.get $p3
    f32.load offset=12
    local.tee $p9
    local.get $p9
    f32.mul
    f32.const -0x1p-1 (;=-0.5;)
    f32.add
    local.tee $l33
    f32.mul
    local.get $p9
    local.get $p0
    f32.load offset=28
    local.get $p3
    f32.load offset=20
    local.tee $l35
    f32.sub
    local.tee $l26
    local.get $l26
    f32.add
    local.tee $l29
    local.get $p3
    f32.load
    local.tee $l26
    f32.mul
    local.get $p0
    f32.load offset=24
    local.get $p3
    f32.load offset=16
    local.tee $l37
    f32.sub
    local.tee $l28
    local.get $l28
    f32.add
    local.tee $l30
    local.get $p3
    f32.load offset=4
    local.tee $l28
    f32.mul
    f32.sub
    f32.mul
    f32.sub
    local.get $p3
    f32.load offset=8
    local.tee $l27
    local.get $l30
    local.get $l26
    f32.mul
    local.get $l29
    local.get $l28
    f32.mul
    f32.add
    local.get $l31
    local.get $l27
    f32.mul
    f32.add
    local.tee $l32
    f32.mul
    f32.add
    f32.store offset=264
    local.get $l12
    local.get $l28
    local.get $l32
    f32.mul
    local.get $l29
    local.get $l33
    f32.mul
    local.get $p9
    local.get $l30
    local.get $l27
    f32.mul
    local.get $l31
    local.get $l26
    f32.mul
    f32.sub
    f32.mul
    f32.sub
    f32.add
    f32.store offset=260
    local.get $l12
    local.get $l26
    local.get $l32
    f32.mul
    local.get $l30
    local.get $l33
    f32.mul
    local.get $p9
    local.get $l31
    local.get $l28
    f32.mul
    local.get $l29
    local.get $l27
    f32.mul
    f32.sub
    f32.mul
    f32.sub
    f32.add
    f32.store offset=256
    f32.const 0x1.fffffep+127 (;=3.40282e+38;)
    local.set $l39
    i32.const -1
    local.set $l16
    f32.const 0x0p+0 (;=0;)
    local.set $l36
    block $B7
      local.get $l17
      i32.eqz
      if $I8
        f32.const 0x0p+0 (;=0;)
        local.set $l37
        f32.const 0x0p+0 (;=0;)
        local.set $l38
        f32.const 0x0p+0 (;=0;)
        local.set $l40
        f32.const 0x0p+0 (;=0;)
        local.set $l34
        f32.const 0x0p+0 (;=0;)
        local.set $l35
        br $B7
      end
      local.get $l33
      local.get $p4
      f32.load offset=24
      local.get $l34
      f32.sub
      local.tee $l31
      local.get $l31
      f32.add
      local.tee $l31
      f32.mul
      local.get $p9
      local.get $l26
      local.get $p4
      f32.load offset=20
      local.get $l35
      f32.sub
      local.tee $l29
      local.get $l29
      f32.add
      local.tee $l29
      f32.mul
      local.get $l28
      local.get $p4
      f32.load offset=16
      local.get $l37
      f32.sub
      local.tee $l30
      local.get $l30
      f32.add
      local.tee $l30
      f32.mul
      f32.sub
      f32.mul
      f32.sub
      local.get $l27
      local.get $l26
      local.get $l30
      f32.mul
      local.get $l28
      local.get $l29
      f32.mul
      f32.add
      local.get $l27
      local.get $l31
      f32.mul
      f32.add
      local.tee $l32
      f32.mul
      f32.add
      local.set $l41
      local.get $l28
      local.get $l32
      f32.mul
      local.get $l33
      local.get $l29
      f32.mul
      local.get $p9
      local.get $l27
      local.get $l30
      f32.mul
      local.get $l26
      local.get $l31
      f32.mul
      f32.sub
      f32.mul
      f32.sub
      f32.add
      local.set $l42
      local.get $l26
      local.get $l32
      f32.mul
      local.get $l33
      local.get $l30
      f32.mul
      local.get $p9
      local.get $l28
      local.get $l31
      f32.mul
      local.get $l27
      local.get $l29
      f32.mul
      f32.sub
      f32.mul
      f32.sub
      f32.add
      local.set $l43
      local.get $p11
      local.get $p11
      f32.add
      local.set $l44
      local.get $p11
      local.get $p11
      f32.mul
      local.set $l45
      f32.const 0x0p+0 (;=0;)
      local.set $l35
      f32.const 0x0p+0 (;=0;)
      local.set $l34
      f32.const 0x0p+0 (;=0;)
      local.set $l40
      f32.const 0x0p+0 (;=0;)
      local.set $l38
      f32.const 0x0p+0 (;=0;)
      local.set $l37
      loop $L9
        local.get $l12
        i32.const 656
        i32.add
        local.get $p5
        local.get $l12
        i32.const 216
        i32.add
        i32.const 0
        i32.const 0
        local.get $l15
        local.get $l20
        i32.const 2
        i32.shl
        i32.add
        local.tee $l19
        i32.load
        i32.const 0
        i32.const 0
        call $f70452
        local.get $l12
        i32.const 0
        i32.store8 offset=112
        local.get $l12
        i32.const 5
        i32.store offset=108
        local.get $l12
        i32.const 0
        i32.store offset=172
        local.get $l12
        local.get $l12
        f32.load offset=248
        local.tee $p9
        f32.store offset=168
        local.get $l12
        local.get $l12
        f32.load offset=244
        local.tee $l26
        f32.store offset=164
        local.get $l12
        local.get $l12
        f32.load offset=240
        local.tee $l28
        f32.store offset=160
        local.get $l12
        i32.const 0
        i32.store offset=156
        local.get $l12
        local.get $l12
        f32.load offset=236
        local.tee $l27
        f32.store offset=152
        local.get $l12
        local.get $l12
        f32.load offset=232
        local.tee $l33
        f32.store offset=148
        local.get $l12
        local.get $l12
        f32.load offset=228
        local.tee $l31
        f32.store offset=144
        local.get $l12
        i32.const 0
        i32.store offset=140
        local.get $l12
        local.get $l12
        f32.load offset=224
        local.tee $l29
        f32.store offset=136
        local.get $l12
        local.get $l12
        f32.load offset=220
        local.tee $l30
        f32.store offset=132
        local.get $l12
        local.get $l12
        f32.load offset=216
        local.tee $l32
        f32.store offset=128
        local.get $l12
        i32.const 0
        i32.store offset=92
        local.get $l12
        local.get $p9
        local.get $l29
        local.get $l27
        f32.add
        f32.add
        f32.const 0x1.55553ep-2 (;=0.333333;)
        f32.mul
        f32.store offset=88
        local.get $l12
        local.get $l26
        local.get $l30
        local.get $l33
        f32.add
        f32.add
        f32.const 0x1.55553ep-2 (;=0.333333;)
        f32.mul
        f32.store offset=84
        local.get $l12
        local.get $l28
        local.get $l32
        local.get $l31
        f32.add
        f32.add
        f32.const 0x1.55553ep-2 (;=0.333333;)
        f32.mul
        f32.store offset=80
        local.get $l12
        i32.const 2139095039
        i32.store offset=104
        local.get $l12
        i64.const 9187343235540844544
        i64.store offset=96
        local.get $p1
        i32.load
        local.set $l14
        local.get $p0
        i32.load
        local.set $l13
        local.get $l12
        i32.const 0
        i32.store8 offset=72
        local.get $l12
        i64.const 4575657221408423936
        i64.store offset=64
        local.get $l12
        i64.const 0
        i64.store offset=56
        local.get $l12
        i64.const 4575657221408423936
        i64.store offset=48
        local.get $l12
        i64.const 0
        i64.store offset=40
        local.get $l12
        i64.const 4575657222473777152
        i64.store offset=32
        local.get $l12
        i64.const 0
        i64.store offset=24
        local.get $l12
        i64.const 1065353216
        i64.store offset=16
        local.get $l12
        i64.const 0
        i64.store offset=8
        local.get $l12
        i64.const 1065353216
        i64.store
        block $B10
          local.get $l13
          local.get $l14
          local.get $p2
          local.get $p3
          local.get $p4
          local.get $p5
          local.get $p6
          local.get $l12
          i32.const 200
          i32.add
          local.get $l12
          i32.const 184
          i32.add
          local.get $l12
          local.get $l12
          i32.const 80
          i32.add
          f32.const 0x0p+0 (;=0;)
          local.get $l13
          i32.load
          i32.const 2
          i32.shl
          i32.const 4117728
          i32.add
          i32.load
          call_indirect $__indirect_function_table (type $t216)
          local.tee $p9
          f32.const 0x0p+0 (;=0;)
          f32.le
          i32.eqz
          br_if $B10
          local.get $l12
          f32.load offset=240
          local.set $l27
          local.get $l12
          f32.load offset=244
          local.set $l33
          local.get $l12
          f32.load offset=248
          local.set $l31
          local.get $l12
          f32.load offset=216
          local.set $p9
          local.get $l12
          f32.load offset=228
          local.set $l29
          local.get $l12
          f32.load offset=220
          local.set $l26
          local.get $l12
          f32.load offset=232
          local.set $l30
          local.get $l12
          local.get $l12
          f32.load offset=224
          local.tee $l28
          local.get $l12
          f32.load offset=236
          local.get $l28
          f32.sub
          local.tee $l32
          f32.add
          f32.store offset=8
          local.get $l12
          local.get $l26
          local.get $l30
          local.get $l26
          f32.sub
          local.tee $l30
          f32.add
          f32.store offset=4
          local.get $l12
          local.get $p9
          local.get $l29
          local.get $p9
          f32.sub
          local.tee $l29
          f32.add
          f32.store
          local.get $l12
          local.get $l28
          local.get $l31
          local.get $l28
          f32.sub
          local.tee $l31
          f32.add
          f32.store offset=712
          local.get $l12
          local.get $l26
          local.get $l33
          local.get $l26
          f32.sub
          local.tee $l28
          f32.add
          f32.store offset=708
          local.get $l12
          local.get $p9
          local.get $l27
          local.get $p9
          f32.sub
          local.tee $l26
          f32.add
          f32.store offset=704
          local.get $l12
          i32.const 680
          i32.add
          local.get $l12
          i32.const 256
          i32.add
          local.get $l12
          i32.const 216
          i32.add
          local.get $l12
          local.get $l12
          i32.const 704
          i32.add
          local.get $l12
          i32.const 700
          i32.add
          local.get $l12
          i32.const 696
          i32.add
          call $f69887
          f32.const 0x0p+0 (;=0;)
          local.set $p9
          local.get $l12
          f32.load offset=680
          local.get $l12
          f32.load offset=256
          f32.sub
          local.tee $l27
          local.get $l27
          f32.mul
          local.get $l12
          f32.load offset=684
          local.get $l12
          f32.load offset=260
          f32.sub
          local.tee $l27
          local.get $l27
          f32.mul
          f32.add
          local.get $l12
          f32.load offset=688
          local.get $l12
          f32.load offset=264
          f32.sub
          local.tee $l27
          local.get $l27
          f32.mul
          f32.add
          local.tee $l27
          local.get $l45
          f32.lt
          i32.eqz
          br_if $B10
          local.get $l44
          local.get $l27
          f32.sqrt
          local.tee $p9
          f32.sub
          f32.neg
          local.get $p9
          local.get $p11
          f32.sub
          local.get $l41
          local.get $l29
          local.get $l28
          f32.mul
          local.get $l30
          local.get $l26
          f32.mul
          f32.sub
          local.tee $p9
          f32.mul
          local.get $l43
          local.get $l30
          local.get $l31
          f32.mul
          local.get $l32
          local.get $l28
          f32.mul
          f32.sub
          local.tee $l28
          f32.mul
          local.get $l42
          local.get $l32
          local.get $l26
          f32.mul
          local.get $l29
          local.get $l31
          f32.mul
          f32.sub
          local.tee $l26
          f32.mul
          f32.add
          f32.add
          local.get $l28
          local.get $l12
          f32.load offset=216
          f32.mul
          local.get $l26
          local.get $l12
          f32.load offset=220
          f32.mul
          f32.add
          local.get $p9
          local.get $l12
          f32.load offset=224
          f32.mul
          f32.add
          f32.sub
          f32.const 0x0p+0 (;=0;)
          f32.gt
          select
          local.set $p9
        end
        local.get $p9
        local.get $l39
        f32.lt
        if $I11
          local.get $l12
          f32.load offset=228
          local.get $l12
          f32.load offset=216
          local.tee $l26
          f32.sub
          local.tee $l28
          local.get $l12
          f32.load offset=244
          local.get $l12
          f32.load offset=220
          local.tee $l27
          f32.sub
          local.tee $l33
          f32.mul
          local.get $l12
          f32.load offset=232
          local.get $l27
          f32.sub
          local.tee $l27
          local.get $l12
          f32.load offset=240
          local.get $l26
          f32.sub
          local.tee $l26
          f32.mul
          f32.sub
          local.tee $l36
          local.get $l36
          f32.mul
          local.get $l27
          local.get $l12
          f32.load offset=248
          local.get $l12
          f32.load offset=224
          local.tee $l31
          f32.sub
          local.tee $l29
          f32.mul
          local.get $l12
          f32.load offset=236
          local.get $l31
          f32.sub
          local.tee $l27
          local.get $l33
          f32.mul
          f32.sub
          local.tee $l34
          local.get $l34
          f32.mul
          local.get $l27
          local.get $l26
          f32.mul
          local.get $l28
          local.get $l29
          f32.mul
          f32.sub
          local.tee $l35
          local.get $l35
          f32.mul
          f32.add
          f32.add
          f32.sqrt
          local.tee $l26
          f32.const 0x0p+0 (;=0;)
          f32.gt
          if $I12
            local.get $l36
            f32.const 0x1p+0 (;=1;)
            local.get $l26
            f32.div
            local.tee $l26
            f32.mul
            local.set $l36
            local.get $l35
            local.get $l26
            f32.mul
            local.set $l35
            local.get $l34
            local.get $l26
            f32.mul
            local.set $l34
          end
          local.get $l19
          i32.load
          local.set $l16
          local.get $l12
          f32.load offset=192
          local.set $l40
          local.get $l12
          f32.load offset=188
          local.set $l38
          local.get $l12
          f32.load offset=184
          local.set $l37
          local.get $p9
          local.set $l39
        end
        local.get $l20
        i32.const 1
        i32.add
        local.tee $l20
        local.get $l17
        i32.ne
        br_if $L9
      end
    end
    local.get $p7
    local.get $l36
    local.get $l36
    f32.add
    local.tee $l26
    local.get $p3
    f32.load offset=12
    local.tee $p9
    local.get $p9
    f32.mul
    f32.const -0x1p-1 (;=-0.5;)
    f32.add
    local.tee $l30
    f32.mul
    local.get $p9
    local.get $l35
    local.get $l35
    f32.add
    local.tee $l28
    local.get $p3
    f32.load
    local.tee $l27
    f32.mul
    local.get $l34
    local.get $l34
    f32.add
    local.tee $l33
    local.get $p3
    f32.load offset=4
    local.tee $l31
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $p3
    f32.load offset=8
    local.tee $l29
    local.get $l33
    local.get $l27
    f32.mul
    local.get $l28
    local.get $l31
    f32.mul
    f32.add
    local.get $l26
    local.get $l29
    f32.mul
    f32.add
    local.tee $l32
    f32.mul
    f32.add
    f32.store offset=8
    local.get $p7
    local.get $l31
    local.get $l32
    f32.mul
    local.get $l28
    local.get $l30
    f32.mul
    local.get $p9
    local.get $l33
    local.get $l29
    f32.mul
    local.get $l26
    local.get $l27
    f32.mul
    f32.sub
    f32.mul
    f32.add
    f32.add
    f32.store offset=4
    local.get $p7
    local.get $l27
    local.get $l32
    f32.mul
    local.get $l33
    local.get $l30
    f32.mul
    local.get $p9
    local.get $l26
    local.get $l31
    f32.mul
    local.get $l28
    local.get $l29
    f32.mul
    f32.sub
    f32.mul
    f32.add
    f32.add
    f32.store
    local.get $p8
    local.get $l40
    f32.store offset=8
    local.get $p8
    local.get $l38
    f32.store offset=4
    local.get $p8
    local.get $l37
    f32.store
    local.get $p10
    local.get $l16
    i32.store
    block $B13
      local.get $l12
      i32.load offset=296
      local.tee $l13
      i32.const 0
      i32.lt_s
      br_if $B13
      local.get $l13
      i32.const 2147483647
      i32.and
      i32.eqz
      br_if $B13
      local.get $l12
      i32.load offset=288
      local.tee $l13
      i32.eqz
      br_if $B13
      call $f69753
      local.tee $l14
      local.get $l13
      local.get $l14
      i32.load
      i32.load offset=12
      call_indirect $__indirect_function_table (type $t1)
    end
    block $B14
      local.get $l12
      i32.load offset=312
      local.tee $l13
      i32.const 0
      i32.lt_s
      br_if $B14
      local.get $l13
      i32.const 2147483647
      i32.and
      i32.eqz
      br_if $B14
      local.get $l12
      i32.load offset=304
      local.tee $l13
      i32.eqz
      br_if $B14
      call $f69753
      local.tee $l14
      local.get $l13
      local.get $l14
      i32.load
      i32.load offset=12
      call_indirect $__indirect_function_table (type $t1)
    end
    block $B15
      local.get $l12
      i32.load offset=652
      local.tee $l13
      i32.const 0
      i32.lt_s
      br_if $B15
      local.get $l13
      i32.const 2147483647
      i32.and
      i32.eqz
      br_if $B15
      local.get $l12
      i32.load offset=644
      local.tee $l13
      local.get $l12
      i32.const 384
      i32.add
      i32.eq
      br_if $B15
      local.get $l13
      i32.eqz
      br_if $B15
      call $f69753
      local.tee $l14
      local.get $l13
      local.get $l14
      i32.load
      i32.load offset=12
      call_indirect $__indirect_function_table (type $t1)
    end
    local.get $l12
    i32.const 720
    i32.add
    global.set $g0
    local.get $l39)
