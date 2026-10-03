  (func $f71128 (type $t18) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 i32) (param $p7 i32) (result i32)
    (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 i32) (local $l17 i32) (local $l18 i32) (local $l19 i32) (local $l20 i32) (local $l21 i32) (local $l22 i32) (local $l23 i32) (local $l24 i32) (local $l25 i32) (local $l26 i32) (local $l27 i32) (local $l28 i32) (local $l29 i32) (local $l30 i32) (local $l31 i32) (local $l32 i32) (local $l33 i32) (local $l34 i32) (local $l35 i32) (local $l36 f32) (local $l37 f32) (local $l38 f32) (local $l39 f32)
    global.get $g0
    i32.const 560
    i32.sub
    local.tee $l9
    global.set $g0
    local.get $p0
    i32.load offset=468
    local.set $l19
    local.get $p0
    f32.load offset=464
    local.set $l38
    local.get $p0
    i32.const 448
    i32.add
    local.tee $l10
    i32.load
    local.set $l15
    local.get $l9
    i64.const 0
    i64.store offset=488
    local.get $l9
    i64.const 0
    i64.store offset=496
    local.get $l9
    i32.const 0
    i32.store offset=504
    local.get $l9
    i64.const 0
    i64.store offset=512
    local.get $l9
    i64.const 0
    i64.store offset=520
    local.get $l9
    i32.const 0
    i32.store offset=528
    local.get $l9
    i64.const 0
    i64.store offset=536
    local.get $l9
    i32.const 3149436
    i32.store offset=532
    local.get $l9
    i64.const 0
    i64.store offset=544
    local.get $l9
    i64.const 0
    i64.store offset=552
    local.get $l9
    i32.const 3149436
    i32.store offset=484
    local.get $l9
    i32.const 3149412
    i32.store offset=480
    local.get $l9
    i32.const 3149436
    i32.store offset=508
    i32.const 1
    local.set $l14
    local.get $p3
    i32.load offset=56
    local.tee $l20
    local.get $l15
    i32.const 5
    i32.shl
    local.tee $l28
    i32.const 1
    call $f71713
    local.set $l26
    local.get $l20
    local.get $l28
    i32.const 1
    call $f71713
    local.set $l25
    local.get $l20
    local.get $p2
    i32.const 3
    i32.shl
    i32.const 1
    call $f71713
    local.set $l18
    local.get $p3
    i32.load offset=44
    local.set $l32
    local.get $p3
    i32.load offset=48
    local.set $l29
    local.get $l9
    i64.const 0
    i64.store offset=472
    local.get $l9
    i64.const 0
    i64.store offset=464
    local.get $l9
    i64.const 0
    i64.store offset=456
    local.get $l9
    i64.const 0
    i64.store offset=448
    local.get $l9
    i32.const 336
    i32.add
    i32.const 0
    i32.const 112
    call $f484
    drop
    local.get $l9
    i64.const 0
    i64.store offset=436 align=4
    local.get $l9
    i64.const 1065353216
    i64.store offset=428 align=4
    local.get $l9
    i64.const 0
    i64.store offset=420 align=4
    local.get $l9
    i32.const -8388609
    i32.store offset=404
    local.get $l9
    i64.const 2139095039
    i64.store offset=412 align=4
    local.get $l9
    local.get $l25
    i32.store offset=332
    local.get $l9
    local.get $l26
    i32.store offset=328
    local.get $l9
    i32.const 0
    i32.store8 offset=296
    local.get $l20
    local.get $p2
    i32.const 5
    i32.shl
    i32.const 1
    call $f71713
    local.set $l21
    local.get $l20
    local.get $l10
    i32.load
    i32.const 5
    i32.shl
    i32.const 1
    i32.sub
    i32.const 1
    call $f71713
    local.set $l30
    local.get $l9
    local.get $p0
    i32.store offset=240
    local.get $l9
    i32.const 0
    i32.store offset=236
    local.get $l9
    i32.const 240
    i32.add
    local.get $l38
    local.get $l9
    i32.const 480
    i32.add
    local.get $l30
    local.get $l9
    i32.const 236
    i32.add
    local.get $p6
    i64.const 0
    local.get $l26
    local.get $l25
    call $f71208
    drop
    local.get $l9
    i32.const 228
    i32.add
    local.tee $l10
    i64.const 0
    i64.store align=4
    local.get $l9
    i32.const 220
    i32.add
    local.tee $l15
    i64.const 0
    i64.store align=4
    local.get $l9
    i64.const 0
    i64.store offset=212 align=4
    local.get $l9
    local.get $p0
    i32.load offset=228
    i32.store offset=192
    local.get $l9
    local.get $p0
    i32.load offset=240
    i32.store offset=196
    local.get $l9
    local.get $p0
    i32.load offset=252
    i32.store offset=200
    local.get $l9
    local.get $p0
    i32.load offset=264
    i32.store offset=204
    local.get $l15
    local.get $p0
    i32.load offset=144
    i32.store
    local.get $l9
    local.get $p0
    i32.load offset=156
    i32.store offset=216
    local.get $l10
    local.get $p0
    i32.load offset=180
    i32.store
    local.get $l9
    local.get $p0
    i32.load offset=192
    i32.store offset=224
    local.get $l9
    local.get $p0
    i32.load offset=480
    i32.store offset=208
    local.get $l9
    i32.const 32
    i32.add
    local.set $l11
    local.get $l9
    i32.const 448
    i32.add
    local.set $l15
    local.get $l9
    i32.const 336
    i32.add
    local.set $l22
    local.get $l9
    i32.const 480
    i32.add
    local.set $l23
    global.get $g0
    i32.const 1088
    i32.sub
    local.tee $l8
    global.set $g0
    local.get $p2
    if $I0
      f32.const 0x1p+0 (;=1;)
      local.get $p0
      f32.load offset=464
      local.tee $l36
      f32.div
      local.set $l37
      loop $L1
        local.get $p1
        local.get $l24
        i32.const 12
        i32.mul
        i32.add
        local.tee $l10
        i32.load offset=8
        local.set $l13
        local.get $l11
        local.get $l21
        local.get $l24
        i32.const 5
        i32.shl
        i32.add
        local.tee $l17
        i32.store offset=16
        local.get $l11
        local.get $l13
        f32.load
        f32.store offset=120
        local.get $l11
        local.get $l13
        f32.load offset=4
        f32.store offset=124
        local.get $l11
        local.get $p0
        i32.load offset=20
        i32.load offset=168
        local.get $l13
        i32.load offset=40
        i32.const 5
        i32.shl
        i32.add
        i32.store offset=132
        local.get $l11
        local.get $l13
        i32.load8_u offset=11
        i32.const 1
        i32.and
        i32.store8 offset=136
        local.get $l11
        local.get $l13
        i32.load8_u offset=10
        i32.const 7
        i32.shr_u
        i32.store8 offset=137
        local.get $l11
        local.get $l13
        i32.load8_u offset=10
        i32.const 5
        i32.shr_u
        i32.const 1
        i32.and
        i32.store8 offset=138
        local.get $l11
        local.get $l13
        i32.load16_u offset=10
        i32.const 9
        i32.shr_u
        i32.const 1
        i32.and
        i32.store8 offset=139
        local.get $l11
        local.get $l13
        f32.load offset=44
        f32.store offset=128
        local.get $l8
        i32.const 128
        i32.add
        i32.const 0
        i32.const 960
        call $f484
        drop
        local.get $l8
        i32.const 2139095039
        i32.store offset=1068
        local.get $l8
        i32.const -8388609
        i32.store offset=1052
        local.get $l8
        i32.const 2139095039
        i32.store offset=988
        local.get $l8
        i32.const -8388609
        i32.store offset=972
        local.get $l8
        i32.const 2139095039
        i32.store offset=908
        local.get $l8
        i32.const -8388609
        i32.store offset=892
        local.get $l8
        i32.const 2139095039
        i32.store offset=828
        local.get $l8
        i32.const -8388609
        i32.store offset=812
        local.get $l8
        i32.const 2139095039
        i32.store offset=748
        local.get $l8
        i32.const -8388609
        i32.store offset=732
        local.get $l8
        i32.const 2139095039
        i32.store offset=668
        local.get $l8
        i32.const -8388609
        i32.store offset=652
        local.get $l8
        i32.const 2139095039
        i32.store offset=588
        local.get $l8
        i32.const -8388609
        i32.store offset=572
        local.get $l8
        i32.const 2139095039
        i32.store offset=508
        local.get $l8
        i32.const -8388609
        i32.store offset=492
        local.get $l8
        i32.const 2139095039
        i32.store offset=428
        local.get $l8
        i32.const -8388609
        i32.store offset=412
        local.get $l8
        i32.const 2139095039
        i32.store offset=348
        local.get $l8
        i32.const -8388609
        i32.store offset=332
        local.get $l8
        i32.const 2139095039
        i32.store offset=268
        local.get $l8
        i32.const -8388609
        i32.store offset=252
        local.get $l8
        i32.const 2139095039
        i32.store offset=188
        local.get $l8
        i32.const -8388609
        i32.store offset=172
        local.get $l11
        i64.const 4575657222473777152
        i64.store offset=4 align=4
        local.get $l11
        i32.const 1065353216
        i32.store offset=12
        local.get $l11
        i32.const 1065353216
        i32.store
        local.get $l8
        block $B2 (result f32)
          local.get $l13
          i32.load offset=24
          if $I3
            local.get $l8
            local.get $l13
            i32.load offset=32
            local.tee $l16
            f32.load
            f32.store offset=96
            local.get $l8
            local.get $l16
            f32.load offset=4
            f32.store offset=100
            local.get $l8
            local.get $l16
            f32.load offset=8
            f32.store offset=104
            local.get $l8
            local.get $l16
            f32.load offset=12
            f32.store offset=108
            local.get $l8
            local.get $l16
            f32.load offset=16
            f32.store offset=112
            local.get $l8
            local.get $l16
            f32.load offset=20
            f32.store offset=116
            local.get $l16
            f32.load offset=24
            br $B2
          end
          local.get $l8
          i64.const 0
          i64.store offset=112
          local.get $l8
          i64.const 4575657221408423936
          i64.store offset=104
          local.get $l8
          i64.const 0
          i64.store offset=96
          f32.const 0x0p+0 (;=0;)
        end
        f32.store offset=120
        local.get $l8
        block $B4 (result f32)
          local.get $l13
          i32.load offset=28
          if $I5
            local.get $l8
            local.get $l13
            i32.load offset=36
            local.tee $l16
            f32.load
            f32.store offset=64
            local.get $l8
            local.get $l16
            f32.load offset=4
            f32.store offset=68
            local.get $l8
            local.get $l16
            f32.load offset=8
            f32.store offset=72
            local.get $l8
            local.get $l16
            f32.load offset=12
            f32.store offset=76
            local.get $l8
            local.get $l16
            f32.load offset=16
            f32.store offset=80
            local.get $l8
            local.get $l16
            f32.load offset=20
            f32.store offset=84
            local.get $l16
            f32.load offset=24
            br $B4
          end
          local.get $l8
          i64.const 0
          i64.store offset=80
          local.get $l8
          i64.const 4575657221408423936
          i64.store offset=72
          local.get $l8
          i64.const 0
          i64.store offset=64
          f32.const 0x0p+0 (;=0;)
        end
        f32.store offset=88
        local.get $l8
        i32.const 0
        i32.store offset=56
        local.get $l8
        i64.const 0
        i64.store offset=48
        local.get $l8
        i32.const 128
        i32.add
        local.get $l8
        i32.const 48
        i32.add
        i32.const 12
        local.get $l8
        local.get $l13
        i32.load offset=20
        local.get $l8
        i32.const 96
        i32.add
        local.get $l8
        i32.const -64
        i32.sub
        local.get $l13
        i32.load16_u offset=10
        i32.const 512
        i32.and
        i32.const 9
        i32.shr_u
        local.get $l8
        i32.const 32
        i32.add
        local.get $l8
        i32.const 16
        i32.add
        local.get $l13
        i32.load offset=12
        call_indirect $__indirect_function_table (type $t32)
        local.set $l13
        local.get $l11
        local.get $l8
        f32.load offset=48
        f32.store offset=140
        local.get $l11
        local.get $l8
        f32.load offset=52
        f32.store offset=144
        local.get $l11
        local.get $l8
        f32.load offset=56
        f32.store offset=148
        local.get $l11
        local.get $l8
        f32.load offset=96
        f32.store offset=36
        local.get $l11
        local.get $l8
        f32.load offset=100
        f32.store offset=40
        local.get $l11
        local.get $l8
        f32.load offset=104
        f32.store offset=44
        local.get $l11
        local.get $l8
        f32.load offset=108
        f32.store offset=48
        local.get $l11
        local.get $l8
        f32.load offset=112
        f32.store offset=52
        local.get $l11
        local.get $l8
        f32.load offset=116
        f32.store offset=56
        local.get $l11
        local.get $l8
        f32.load offset=120
        f32.store offset=60
        local.get $l11
        local.get $l8
        f32.load offset=64
        f32.store offset=64
        local.get $l11
        local.get $l8
        f32.load offset=68
        f32.store offset=68
        local.get $l11
        local.get $l8
        f32.load offset=72
        f32.store offset=72
        local.get $l11
        local.get $l8
        f32.load offset=76
        f32.store offset=76
        local.get $l11
        local.get $l8
        f32.load offset=80
        f32.store offset=80
        local.get $l11
        local.get $l8
        f32.load offset=84
        f32.store offset=84
        local.get $l8
        f32.load offset=88
        local.set $l39
        local.get $l11
        local.get $l13
        i32.store offset=116
        local.get $l11
        local.get $l39
        f32.store offset=88
        local.get $l11
        local.get $l8
        i32.const 128
        i32.add
        i32.store offset=112
        local.get $l10
        i32.load offset=4
        local.set $l13
        block $B6
          block $B7 (result i32)
            block $B8
              local.get $l10
              i32.load
              local.tee $l16
              i32.const -2147483648
              i32.eq
              br_if $B8
              local.get $l13
              i32.const -2147483648
              i32.eq
              br_if $B8
              local.get $l17
              local.get $l13
              i32.store16 offset=10
              local.get $l17
              local.get $l16
              i32.store16 offset=8
              local.get $l17
              local.get $p0
              i32.store
              local.get $l17
              local.get $p0
              i32.store offset=4
              i32.const 8
              local.set $l16
              i32.const 8
              br $B7
            end
            local.get $l16
            i32.const -2147483648
            i32.eq
            if $I9
              local.get $l17
              local.get $l13
              i32.store16 offset=10
              local.get $l17
              i32.const 65535
              i32.store16 offset=8
              local.get $l17
              local.get $l15
              i32.store
              local.get $l17
              local.get $p0
              i32.store offset=4
              i32.const 8
              local.set $l16
              i32.const 2
              br $B7
            end
            local.get $l13
            i32.const -2147483648
            i32.ne
            br_if $B6
            local.get $l17
            i32.const 65535
            i32.store16 offset=10
            local.get $l17
            local.get $l16
            i32.store16 offset=8
            local.get $l17
            local.get $p0
            i32.store
            local.get $l17
            local.get $l15
            i32.store offset=4
            i32.const 2
            local.set $l16
            i32.const 8
          end
          local.set $l13
          local.get $l11
          local.get $l16
          i32.store offset=96
          local.get $l11
          local.get $l13
          i32.store offset=92
        end
        local.get $l11
        local.get $l17
        i32.load
        i32.store offset=20
        local.get $l17
        i32.load offset=4
        local.set $l13
        local.get $l11
        local.get $l22
        i32.store offset=32
        local.get $l11
        local.get $l22
        i32.store offset=28
        local.get $l11
        local.get $l13
        i32.store offset=24
        local.get $l11
        local.get $l23
        local.get $l36
        local.get $l37
        local.get $l26
        call $f71176
        drop
        local.get $l24
        i32.const 1
        i32.add
        local.tee $l24
        local.get $p2
        i32.ne
        br_if $L1
      end
    end
    local.get $l8
    i32.const 1088
    i32.add
    global.set $g0
    block $B10
      local.get $p2
      i32.eqz
      br_if $B10
      local.get $p2
      i32.const 7
      i32.and
      local.set $l15
      local.get $p2
      i32.const 1
      i32.sub
      i32.const 7
      i32.ge_u
      if $I11
        local.get $p2
        i32.const -8
        i32.and
        local.set $l8
        loop $L12
          local.get $l18
          local.get $l12
          i32.const 2
          i32.shl
          local.tee $l10
          i32.add
          i32.const 2139095039
          i32.store
          local.get $l18
          local.get $l10
          i32.const 4
          i32.or
          i32.add
          i32.const 2139095039
          i32.store
          local.get $l18
          local.get $l10
          i32.const 8
          i32.or
          i32.add
          i32.const 2139095039
          i32.store
          local.get $l18
          local.get $l10
          i32.const 12
          i32.or
          i32.add
          i32.const 2139095039
          i32.store
          local.get $l18
          local.get $l10
          i32.const 16
          i32.or
          i32.add
          i32.const 2139095039
          i32.store
          local.get $l18
          local.get $l10
          i32.const 20
          i32.or
          i32.add
          i32.const 2139095039
          i32.store
          local.get $l18
          local.get $l10
          i32.const 24
          i32.or
          i32.add
          i32.const 2139095039
          i32.store
          local.get $l18
          local.get $l10
          i32.const 28
          i32.or
          i32.add
          i32.const 2139095039
          i32.store
          local.get $l12
          i32.const 8
          i32.add
          local.set $l12
          local.get $l8
          i32.const 8
          i32.sub
          local.tee $l8
          br_if $L12
        end
      end
      local.get $l15
      i32.eqz
      br_if $B10
      loop $L13
        local.get $l18
        local.get $l12
        i32.const 2
        i32.shl
        i32.add
        i32.const 2139095039
        i32.store
        local.get $l12
        i32.const 1
        i32.add
        local.set $l12
        local.get $l15
        i32.const 1
        i32.sub
        local.tee $l15
        br_if $L13
      end
    end
    block $B14
      local.get $p7
      i32.eqz
      br_if $B14
      local.get $p0
      i32.const 112
      i32.add
      local.set $l22
      f32.const 0x1p+0 (;=1;)
      local.get $l38
      f32.div
      local.set $l37
      local.get $l19
      i32.const 2
      i32.shl
      local.set $l33
      local.get $l19
      i32.const -4
      i32.and
      local.set $l13
      local.get $l19
      i32.const 3
      i32.and
      local.set $l16
      local.get $l19
      i32.const -2
      i32.and
      local.set $l17
      local.get $l19
      i32.const 1
      i32.and
      local.set $l34
      local.get $l19
      i32.const 1
      i32.sub
      local.set $l31
      block $B15
        loop $L16
          i32.const 0
          local.set $l10
          block $B17
            block $B18
              local.get $p2
              i32.eqz
              br_if $B18
              loop $L19
                block $B20
                  local.get $l21
                  local.get $l10
                  i32.const 5
                  i32.shl
                  i32.add
                  i32.load offset=24
                  local.tee $l8
                  i32.load8_u offset=1
                  i32.eqz
                  br_if $B20
                  local.get $l8
                  i32.const 48
                  i32.add
                  local.set $l14
                  i32.const 1
                  local.set $l12
                  loop $L21
                    local.get $l14
                    i32.const 0
                    i32.store offset=88
                    local.get $l12
                    local.get $l8
                    i32.load8_u offset=1
                    i32.ge_u
                    br_if $B20
                    local.get $l14
                    i32.const 160
                    i32.add
                    local.set $l14
                    local.get $l12
                    i32.const 1
                    i32.add
                    local.set $l12
                    br $L21
                  end
                  unreachable
                end
                local.get $l10
                i32.const 1
                i32.add
                local.tee $l10
                local.get $p2
                i32.ne
                br_if $L19
              end
              i32.const 0
              local.set $l10
              local.get $p2
              i32.eqz
              br_if $B18
              loop $L22
                local.get $l21
                local.get $l10
                i32.const 5
                i32.shl
                i32.add
                local.get $l9
                i32.const 296
                i32.add
                call $f71046
                local.get $l10
                i32.const 1
                i32.add
                local.tee $l10
                local.get $p2
                i32.ne
                br_if $L22
              end
              i32.const 0
              local.set $l10
              local.get $p2
              i32.eqz
              br_if $B18
              loop $L23
                local.get $l21
                local.get $l10
                i32.const 5
                i32.shl
                i32.add
                local.get $l9
                i32.const 296
                i32.add
                call $f71046
                local.get $l10
                i32.const 1
                i32.add
                local.tee $l10
                local.get $p2
                i32.ne
                br_if $L23
              end
              i32.const 0
              local.set $l10
              local.get $p2
              i32.eqz
              br_if $B18
              loop $L24
                local.get $l21
                local.get $l10
                i32.const 5
                i32.shl
                i32.add
                local.get $l9
                i32.const 296
                i32.add
                call $f71046
                local.get $l10
                i32.const 1
                i32.add
                local.tee $l10
                local.get $p2
                i32.ne
                br_if $L24
              end
              i32.const 0
              local.set $l10
              local.get $p2
              i32.eqz
              br_if $B18
              loop $L25
                local.get $l21
                local.get $l10
                i32.const 5
                i32.shl
                i32.add
                local.get $l9
                i32.const 296
                i32.add
                call $f71046
                local.get $l10
                i32.const 1
                i32.add
                local.tee $l10
                local.get $p2
                i32.ne
                br_if $L25
              end
              i32.const 0
              local.set $l10
              local.get $p2
              i32.eqz
              br_if $B18
              loop $L26
                block $B27
                  local.get $l21
                  local.get $l10
                  i32.const 5
                  i32.shl
                  i32.add
                  i32.load offset=24
                  local.tee $l8
                  i32.eqz
                  br_if $B27
                  local.get $l8
                  i32.load8_u offset=1
                  i32.eqz
                  br_if $B27
                  i32.const 160
                  i32.const 96
                  local.get $l8
                  i32.load8_u
                  i32.const 4
                  i32.eq
                  select
                  local.set $l11
                  local.get $l8
                  i32.const 48
                  i32.add
                  local.set $l12
                  i32.const 1
                  local.set $l14
                  loop $L28
                    local.get $l12
                    local.get $l12
                    f32.load offset=28
                    f32.store offset=12
                    local.get $l14
                    local.get $l8
                    i32.load8_u offset=1
                    i32.ge_u
                    br_if $B27
                    local.get $l11
                    local.get $l12
                    i32.add
                    local.set $l12
                    local.get $l14
                    i32.const 1
                    i32.add
                    local.set $l14
                    br $L28
                  end
                  unreachable
                end
                local.get $l10
                i32.const 1
                i32.add
                local.tee $l10
                local.get $p2
                i32.ne
                br_if $L26
              end
              local.get $p0
              local.get $l25
              call $f70971
              i32.const 0
              local.set $l10
              local.get $p2
              i32.eqz
              br_if $B15
              loop $L29
                local.get $l21
                local.get $l10
                i32.const 5
                i32.shl
                i32.add
                local.tee $l12
                local.get $l9
                i32.const 296
                i32.add
                call $f71046
                local.get $l12
                call $f71029
                local.get $l10
                i32.const 1
                i32.add
                local.tee $l10
                local.get $p2
                i32.ne
                br_if $L29
              end
              local.get $p2
              i32.eqz
              br_if $B15
              i32.const 0
              local.set $l10
              i32.const 1
              local.set $l15
              loop $L30
                local.get $l29
                local.get $l10
                i32.const 2
                i32.shl
                local.tee $l8
                i32.add
                local.get $l38
                local.get $l37
                local.get $p0
                i32.load offset=20
                i32.load offset=168
                local.get $p1
                i32.load offset=8
                i32.load offset=40
                i32.const 5
                i32.shl
                i32.add
                local.tee $l12
                f32.load
                f32.mul
                local.tee $l36
                local.get $l36
                f32.mul
                local.get $l37
                local.get $l12
                f32.load offset=4
                f32.mul
                local.tee $l36
                local.get $l36
                f32.mul
                f32.add
                local.get $l37
                local.get $l12
                f32.load offset=8
                f32.mul
                local.tee $l36
                local.get $l36
                f32.mul
                f32.add
                f32.sqrt
                f32.mul
                local.tee $l36
                f32.store
                local.get $l8
                local.get $l18
                i32.add
                local.tee $l12
                f32.load
                local.set $l39
                local.get $l12
                local.get $l36
                f32.store
                i32.const 0
                local.get $l15
                local.get $l39
                local.get $l36
                f32.sub
                f32.abs
                f32.const 0x1.4f8b58p-17 (;=1e-05;)
                f32.gt
                select
                local.set $l15
                local.get $l10
                i32.const 1
                i32.add
                local.tee $l10
                local.get $p2
                i32.ne
                br_if $L30
              end
              local.get $l15
              i32.const 1
              i32.and
              local.tee $l24
              br_if $B15
              i32.const 0
              local.set $l23
              local.get $p3
              i32.load offset=24
              i32.const 0
              local.get $l33
              call $f484
              local.set $l15
              local.get $p2
              i32.eqz
              br_if $B17
              loop $L31
                block $B32
                  local.get $l19
                  i32.eqz
                  br_if $B32
                  local.get $l29
                  local.get $l23
                  i32.const 2
                  i32.shl
                  i32.add
                  local.set $l8
                  local.get $l32
                  local.get $l19
                  local.get $l23
                  i32.mul
                  i32.const 2
                  i32.shl
                  i32.add
                  local.set $l14
                  i32.const 0
                  local.set $l10
                  local.get $l17
                  local.set $l11
                  local.get $l31
                  if $I33
                    loop $L34
                      local.get $l15
                      local.get $l10
                      i32.const 2
                      i32.shl
                      local.tee $l12
                      i32.add
                      local.tee $l27
                      local.get $l27
                      f32.load
                      local.get $l12
                      local.get $l14
                      i32.add
                      f32.load
                      local.get $l8
                      f32.load
                      f32.mul
                      f32.add
                      f32.store
                      local.get $l15
                      local.get $l12
                      i32.const 4
                      i32.or
                      local.tee $l12
                      i32.add
                      local.tee $l27
                      local.get $l27
                      f32.load
                      local.get $l12
                      local.get $l14
                      i32.add
                      f32.load
                      local.get $l8
                      f32.load
                      f32.mul
                      f32.add
                      f32.store
                      local.get $l10
                      i32.const 2
                      i32.add
                      local.set $l10
                      local.get $l11
                      i32.const 2
                      i32.sub
                      local.tee $l11
                      br_if $L34
                    end
                  end
                  local.get $l34
                  i32.eqz
                  br_if $B32
                  local.get $l15
                  local.get $l10
                  i32.const 2
                  i32.shl
                  local.tee $l10
                  i32.add
                  local.tee $l12
                  local.get $l12
                  f32.load
                  local.get $l10
                  local.get $l14
                  i32.add
                  f32.load
                  local.get $l8
                  f32.load
                  f32.mul
                  f32.add
                  f32.store
                end
                local.get $p2
                local.get $l23
                i32.const 1
                i32.add
                local.tee $l23
                i32.ne
                br_if $L31
              end
              br $B17
            end
            local.get $p0
            local.get $l25
            call $f70971
            br $B15
          end
          block $B35
            local.get $l19
            i32.eqz
            br_if $B35
            i32.const 0
            local.set $l10
            local.get $l13
            local.set $l8
            local.get $l31
            i32.const 3
            i32.ge_u
            if $I36
              loop $L37
                local.get $l15
                local.get $l10
                i32.const 2
                i32.shl
                local.tee $l12
                i32.add
                local.tee $l14
                local.get $p5
                local.get $l12
                i32.add
                f32.load
                local.get $l14
                f32.load
                f32.sub
                f32.store
                local.get $l15
                local.get $l12
                i32.const 4
                i32.or
                local.tee $l14
                i32.add
                local.tee $l11
                local.get $p5
                local.get $l14
                i32.add
                f32.load
                local.get $l11
                f32.load
                f32.sub
                f32.store
                local.get $l15
                local.get $l12
                i32.const 8
                i32.or
                local.tee $l14
                i32.add
                local.tee $l11
                local.get $p5
                local.get $l14
                i32.add
                f32.load
                local.get $l11
                f32.load
                f32.sub
                f32.store
                local.get $l15
                local.get $l12
                i32.const 12
                i32.or
                local.tee $l12
                i32.add
                local.tee $l14
                local.get $p5
                local.get $l12
                i32.add
                f32.load
                local.get $l14
                f32.load
                f32.sub
                f32.store
                local.get $l10
                i32.const 4
                i32.add
                local.set $l10
                local.get $l8
                i32.const 4
                i32.sub
                local.tee $l8
                br_if $L37
              end
            end
            local.get $l16
            local.tee $l12
            i32.eqz
            br_if $B35
            loop $L38
              local.get $l15
              local.get $l10
              i32.const 2
              i32.shl
              local.tee $l8
              i32.add
              local.tee $l14
              local.get $p5
              local.get $l8
              i32.add
              f32.load
              local.get $l14
              f32.load
              f32.sub
              f32.store
              local.get $l10
              i32.const 1
              i32.add
              local.set $l10
              local.get $l12
              i32.const 1
              i32.sub
              local.tee $l12
              br_if $L38
            end
          end
          local.get $l9
          i32.const 247
          i32.store8 offset=24
          local.get $p0
          local.get $p4
          local.get $l9
          i32.const 24
          i32.add
          local.get $p0
          i32.load
          i32.load offset=36
          call_indirect $__indirect_function_table (type $t3)
          drop
          local.get $l9
          i32.const 8
          i32.store8 offset=16
          local.get $p0
          local.get $p3
          local.get $l9
          i32.const 16
          i32.add
          local.get $p0
          i32.load
          i32.load offset=36
          call_indirect $__indirect_function_table (type $t3)
          drop
          local.get $p0
          i32.load offset=312
          i32.const 0
          local.get $p0
          i32.load offset=448
          i32.const 5
          i32.shl
          call $f484
          drop
          local.get $p0
          i32.load offset=168
          i32.const 0
          local.get $p0
          i32.load offset=468
          i32.const 2
          i32.shl
          call $f484
          drop
          local.get $p0
          i32.const 0
          i32.store8 offset=489
          local.get $l22
          local.get $l9
          i32.const 192
          i32.add
          call $f71022
          local.get $l22
          local.get $p6
          local.get $l9
          i32.const 192
          i32.add
          call $f71018
          local.get $l22
          local.get $l9
          i32.const 192
          i32.add
          call $f71204
          local.get $p0
          local.get $l22
          local.get $l9
          i32.const 192
          i32.add
          call $f71207
          local.get $p0
          i32.load offset=264
          i32.const 0
          local.get $l28
          call $f484
          drop
          local.get $l35
          i32.const 1
          i32.add
          local.tee $l35
          local.get $p7
          i32.lt_u
          br_if $L16
        end
        local.get $l24
        local.set $l14
        br $B14
      end
      i32.const 1
      local.set $l14
    end
    local.get $l20
    local.get $l30
    call $f71715
    local.get $l20
    local.get $l18
    call $f71715
    local.get $l20
    local.get $l26
    call $f71715
    local.get $l20
    local.get $l25
    call $f71715
    local.get $l20
    local.get $l21
    call $f71715
    i32.const 0
    local.set $p2
    local.get $l9
    i32.const 480
    i32.add
    local.tee $p1
    i32.const 1
    local.get $p1
    i32.load offset=76
    i32.sub
    local.tee $p3
    i32.store offset=76
    local.get $p1
    i32.load offset=16
    local.tee $p5
    if $I39
      loop $L40
        local.get $p1
        i32.load offset=12
        local.get $p2
        i32.const 2
        i32.shl
        i32.add
        i32.load
        local.tee $p3
        if $I41
          call $f69753
          local.tee $p5
          local.get $p3
          local.get $p5
          i32.load
          i32.load offset=12
          call_indirect $__indirect_function_table (type $t1)
          local.get $p1
          i32.load offset=16
          local.set $p5
        end
        local.get $p2
        i32.const 1
        i32.add
        local.tee $p2
        local.get $p5
        i32.lt_u
        br_if $L40
      end
      local.get $p1
      i32.load offset=76
      local.set $p3
    end
    i32.const 0
    local.set $p2
    local.get $p1
    i32.const 0
    i32.store offset=16
    local.get $p1
    i32.const 0
    i32.store offset=24
    local.get $p1
    i32.const 0
    i32.store offset=8
    local.get $p1
    local.get $p3
    i32.const 24
    i32.mul
    i32.add
    local.tee $p6
    i32.const 40
    i32.add
    local.tee $p7
    i32.load
    local.tee $p1
    if $I42
      local.get $p6
      i32.const 36
      i32.add
      local.set $p3
      loop $L43
        local.get $p3
        i32.load
        local.get $p2
        i32.const 2
        i32.shl
        i32.add
        i32.load
        local.tee $p5
        if $I44
          call $f69753
          local.tee $p1
          local.get $p5
          local.get $p1
          i32.load
          i32.load offset=12
          call_indirect $__indirect_function_table (type $t1)
          local.get $p7
          i32.load
          local.set $p1
        end
        local.get $p2
        i32.const 1
        i32.add
        local.tee $p2
        local.get $p1
        i32.lt_u
        br_if $L43
      end
    end
    local.get $p7
    i32.const 0
    i32.store
    local.get $p6
    i32.const 0
    i32.store offset=48
    local.get $p6
    i32.const 0
    i32.store offset=32
    local.get $l9
    i32.const 247
    i32.store8 offset=8
    local.get $p0
    local.get $p4
    local.get $l9
    i32.const 8
    i32.add
    local.get $p0
    i32.load
    i32.load offset=36
    call_indirect $__indirect_function_table (type $t3)
    drop
    local.get $l9
    i32.const 480
    i32.add
    call $f71129
    drop
    local.get $l9
    i32.const 560
    i32.add
    global.set $g0
    local.get $l14)
