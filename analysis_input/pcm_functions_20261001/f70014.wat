  (func $f70014 (type $t9) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (result i32)
    (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32) (local $l33 i64)
    global.get $g0
    i32.const 224
    i32.sub
    local.tee $l7
    global.set $g0
    local.get $p1
    i32.const 124
    i32.add
    local.set $p1
    local.get $p3
    f32.load offset=4
    local.set $l19
    block $B0 (result i32)
      block $B1
        local.get $p3
        f32.load
        local.tee $l21
        f32.const 0x1p+0 (;=1;)
        f32.ne
        br_if $B1
        local.get $l19
        f32.const 0x1p+0 (;=1;)
        f32.ne
        br_if $B1
        f32.const 0x1p+0 (;=1;)
        local.set $l19
        local.get $p3
        f32.load offset=8
        f32.const 0x1p+0 (;=1;)
        f32.ne
        br_if $B1
        local.get $l7
        i64.const 0
        i64.store offset=152
        local.get $l7
        i32.const 1065353216
        i32.store offset=148
        local.get $l7
        i64.const 0
        i64.store offset=160
        local.get $l7
        i64.const 0
        i64.store offset=172 align=4
        local.get $l7
        i32.const 1065353216
        i32.store offset=168
        local.get $l7
        i64.const 0
        i64.store offset=180 align=4
        local.get $l7
        i32.const 1065353216
        i32.store offset=188
        local.get $l7
        i64.const 0
        i64.store offset=132 align=4
        local.get $l7
        i32.const 1065353216
        i32.store offset=128
        local.get $l7
        i64.const 0
        i64.store offset=140 align=4
        block $B2 (result i32)
          block $B3
            local.get $p2
            i32.load
            local.tee $l11
            if $I4
              local.get $p2
              f32.load offset=4
              local.set $l21
              br $B3
            end
            local.get $p2
            i32.load offset=4
            local.tee $p3
            f32.reinterpret_i32
            local.set $l21
            local.get $p3
            br_if $B3
            local.get $p2
            i32.load offset=8
            br_if $B3
            i32.const 0
            local.get $p2
            i32.load offset=12
            i32.const 1065353216
            i32.eq
            br_if $B2
            drop
          end
          local.get $p2
          f32.load offset=8
          local.set $l19
          local.get $p2
          f32.load offset=12
          local.set $l22
          local.get $l7
          i32.const 0
          i32.store offset=156
          local.get $l7
          local.get $l19
          local.get $l21
          local.get $l21
          f32.add
          local.tee $l27
          f32.mul
          local.tee $l28
          local.get $l22
          local.get $l11
          f32.reinterpret_i32
          local.tee $l25
          local.get $l25
          f32.add
          local.tee $l24
          f32.mul
          local.tee $l14
          f32.sub
          f32.store offset=164
          local.get $l7
          i32.const 0
          i32.store offset=172
          local.get $l7
          i32.const 0
          i32.store offset=140
          local.get $l7
          local.get $l24
          local.get $l19
          f32.mul
          local.tee $l15
          local.get $l27
          local.get $l22
          f32.mul
          local.tee $l16
          f32.add
          f32.store offset=160
          local.get $l7
          local.get $l28
          local.get $l14
          f32.add
          f32.store offset=152
          local.get $l7
          local.get $l15
          local.get $l16
          f32.sub
          f32.store offset=136
          local.get $l7
          f32.const 0x1p+0 (;=1;)
          local.get $l24
          local.get $l25
          f32.mul
          f32.sub
          local.tee $l25
          local.get $l21
          local.get $l27
          f32.mul
          local.tee $l27
          f32.sub
          f32.store offset=168
          local.get $l7
          local.get $l25
          local.get $l19
          local.get $l19
          local.get $l19
          f32.add
          local.tee $l28
          f32.mul
          local.tee $l19
          f32.sub
          f32.store offset=148
          local.get $l7
          local.get $l24
          local.get $l21
          f32.mul
          local.tee $l21
          local.get $l28
          local.get $l22
          f32.mul
          local.tee $l22
          f32.sub
          f32.store offset=144
          local.get $l7
          local.get $l21
          local.get $l22
          f32.add
          f32.store offset=132
          local.get $l7
          f32.const 0x1p+0 (;=1;)
          local.get $l27
          f32.sub
          local.get $l19
          f32.sub
          f32.store offset=128
          local.get $l7
          i32.const 128
          i32.add
        end
        local.set $p3
        block $B5
          block $B6
            local.get $p2
            i32.load offset=16
            local.tee $l11
            if $I7
              local.get $p2
              f32.load offset=20
              local.set $l19
              br $B6
            end
            local.get $p2
            i32.load offset=20
            local.tee $l12
            f32.reinterpret_i32
            local.set $l19
            local.get $l12
            br_if $B6
            local.get $p2
            i32.load offset=24
            i32.eqz
            br_if $B5
          end
          local.get $l7
          local.get $l19
          f32.store offset=180
          local.get $l7
          local.get $l11
          i32.store offset=176
          local.get $l7
          local.get $p2
          f32.load offset=24
          f32.store offset=184
          local.get $l7
          i32.const 128
          i32.add
          local.set $p3
        end
        block $B8
          local.get $p4
          if $I9
            local.get $p4
            block $B10 (result i32)
              local.get $p4
              i32.load
              local.set $l9
              local.get $p4
              i32.load offset=8
              local.set $l8
              global.get $g0
              i32.const 1488
              i32.sub
              local.tee $l5
              global.set $g0
              local.get $p1
              local.tee $p2
              i32.load
              local.set $l6
              local.get $l5
              local.get $l9
              i32.store offset=424
              local.get $l5
              local.get $l8
              i32.store offset=420
              local.get $l5
              i32.const 0
              i32.store offset=416
              local.get $l5
              i32.const 368
              i32.add
              local.tee $l8
              local.get $p0
              local.get $p3
              call $f69990
              local.get $l5
              local.get $l5
              f32.load offset=388
              local.get $l5
              f32.load offset=376
              f32.sub
              local.tee $l15
              f32.store offset=404
              local.get $l5
              local.get $l5
              f32.load offset=384
              local.get $l5
              f32.load offset=372
              f32.sub
              local.tee $l17
              f32.store offset=400
              local.get $l5
              local.get $l5
              f32.load offset=380
              local.get $l5
              f32.load offset=368
              f32.sub
              local.tee $l18
              f32.store offset=396
              local.get $l5
              local.get $l18
              local.get $l18
              f32.mul
              local.get $l17
              local.get $l17
              f32.mul
              f32.add
              local.get $l15
              local.get $l15
              f32.mul
              f32.add
              local.tee $l15
              f32.store offset=408
              local.get $l5
              f32.const 0x1p+0 (;=1;)
              local.get $l15
              f32.div
              f32.const 0x0p+0 (;=0;)
              local.get $l15
              f32.const 0x0p+0 (;=0;)
              f32.ne
              select
              f32.store offset=412
              local.get $l8
              local.get $l5
              i32.const 432
              i32.add
              call $f70397
              local.get $l5
              local.get $l5
              f32.load offset=440
              local.tee $l15
              f32.store offset=340
              local.get $l5
              local.get $l5
              f32.load offset=436
              local.tee $l17
              f32.store offset=328
              local.get $l5
              local.get $l5
              f32.load offset=452
              local.tee $l18
              f32.store offset=344
              local.get $l5
              local.get $l5
              f32.load offset=448
              local.tee $l20
              f32.store offset=332
              local.get $l5
              local.get $l5
              f32.load offset=444
              local.tee $l16
              f32.store offset=320
              local.get $l5
              local.get $l16
              local.get $l5
              f32.load offset=468
              local.tee $l14
              f32.mul
              local.get $l20
              local.get $l5
              f32.load offset=472
              local.tee $l23
              f32.mul
              f32.add
              local.get $l18
              local.get $l5
              f32.load offset=476
              local.tee $l26
              f32.mul
              f32.add
              f32.neg
              f32.store offset=356
              local.get $l5
              local.get $l5
              f32.load offset=432
              local.tee $l29
              f32.store offset=316
              local.get $l5
              local.get $l14
              local.get $l29
              f32.mul
              local.get $l23
              local.get $l17
              f32.mul
              f32.add
              local.get $l26
              local.get $l15
              f32.mul
              f32.add
              f32.neg
              f32.store offset=352
              local.get $l5
              local.get $l14
              local.get $l5
              f32.load offset=456
              local.tee $l30
              f32.mul
              local.get $l23
              local.get $l5
              f32.load offset=460
              local.tee $l31
              f32.mul
              f32.add
              local.get $l26
              local.get $l5
              f32.load offset=464
              local.tee $l32
              f32.mul
              f32.add
              f32.neg
              f32.store offset=360
              local.get $l5
              local.get $l32
              f32.store offset=348
              local.get $l5
              local.get $l31
              f32.store offset=336
              local.get $l5
              local.get $l30
              f32.store offset=324
              local.get $l5
              local.get $l23
              f32.store offset=164
              local.get $l5
              local.get $l26
              f32.store offset=168
              local.get $l5
              local.get $l14
              f32.store offset=160
              local.get $l5
              local.get $l6
              i32.load offset=16
              i32.store offset=304
              local.get $l5
              local.get $l6
              i32.load offset=20
              i32.store offset=308
              local.get $l5
              local.get $l6
              i32.load offset=4
              i32.store offset=312
              local.get $p2
              f32.load offset=40
              local.set $l14
              local.get $p2
              i64.load offset=32 align=4
              local.set $l33
              local.get $l5
              local.get $p2
              f32.load offset=44
              local.tee $l23
              f32.store offset=140
              local.get $l5
              local.get $l14
              f32.store offset=136
              local.get $l5
              local.get $l33
              i64.store offset=128
              local.get $p2
              f32.load offset=56
              local.set $l14
              local.get $l5
              local.get $p2
              i64.load offset=48 align=4
              i64.store offset=148 align=4
              local.get $l5
              local.get $l16
              f32.abs
              f32.const 0x1.0c6f7ap-20 (;=1e-06;)
              f32.add
              local.tee $l26
              f32.store offset=292
              local.get $l5
              local.get $l31
              f32.store offset=248
              local.get $l5
              local.get $l16
              f32.store offset=244
              local.get $l5
              local.get $l30
              f32.store offset=232
              local.get $l5
              local.get $l18
              f32.store offset=228
              local.get $l5
              local.get $l32
              f32.store offset=216
              local.get $l5
              local.get $l20
              f32.store offset=212
              local.get $l5
              local.get $l14
              f32.store offset=156
              local.get $l5
              local.get $l31
              f32.abs
              f32.const 0x1.0c6f7ap-20 (;=1e-06;)
              f32.add
              local.tee $l16
              f32.store offset=296
              local.get $l5
              local.get $l30
              f32.abs
              f32.const 0x1.0c6f7ap-20 (;=1e-06;)
              f32.add
              local.tee $l14
              f32.store offset=280
              local.get $l5
              local.get $l18
              f32.abs
              f32.const 0x1.0c6f7ap-20 (;=1e-06;)
              f32.add
              local.tee $l30
              f32.store offset=276
              local.get $l5
              local.get $l20
              f32.abs
              f32.const 0x1.0c6f7ap-20 (;=1e-06;)
              f32.add
              local.tee $l20
              f32.store offset=260
              local.get $l5
              local.get $l15
              f32.store offset=240
              local.get $l5
              local.get $l17
              f32.store offset=224
              local.get $l5
              local.get $l29
              f32.store offset=208
              local.get $l5
              local.get $l23
              f32.store offset=144
              local.get $l5
              local.get $l29
              f32.abs
              f32.const 0x1.0c6f7ap-20 (;=1e-06;)
              f32.add
              local.tee $l23
              f32.store offset=256
              local.get $l5
              local.get $l15
              f32.abs
              f32.const 0x1.0c6f7ap-20 (;=1e-06;)
              f32.add
              local.tee $l29
              f32.store offset=288
              local.get $l5
              local.get $l17
              f32.abs
              f32.const 0x1.0c6f7ap-20 (;=1e-06;)
              f32.add
              local.tee $l31
              f32.store offset=272
              local.get $l5
              local.get $l32
              f32.abs
              f32.const 0x1.0c6f7ap-20 (;=1e-06;)
              f32.add
              local.tee $l32
              f32.store offset=264
              local.get $l5
              local.get $l5
              f32.load offset=484
              local.tee $l15
              f32.store offset=196
              local.get $l5
              local.get $l5
              f32.load offset=488
              local.tee $l17
              f32.store offset=200
              local.get $l5
              local.get $l31
              local.get $l5
              f32.load offset=480
              local.tee $l18
              f32.mul
              local.get $l20
              local.get $l15
              f32.mul
              f32.add
              local.get $l16
              local.get $l17
              f32.mul
              f32.add
              f32.store offset=180
              local.get $l5
              local.get $l29
              local.get $l18
              f32.mul
              local.get $l30
              local.get $l15
              f32.mul
              f32.add
              local.get $l32
              local.get $l17
              f32.mul
              f32.add
              f32.store offset=184
              local.get $l5
              local.get $l18
              f32.store offset=192
              local.get $l5
              local.get $l23
              local.get $l18
              f32.mul
              local.get $l26
              local.get $l15
              f32.mul
              f32.add
              local.get $l14
              local.get $l17
              f32.mul
              f32.add
              f32.store offset=176
              local.get $p4
              i32.const 20
              i32.add
              block $B11 (result i32)
                block $B12 (result i32)
                  block $B13
                    local.get $p2
                    i32.load offset=24
                    local.tee $l12
                    if $I14
                      local.get $l5
                      local.get $p2
                      i32.load offset=28
                      i32.store offset=432
                      i32.const 1
                      local.set $p1
                      loop $L15
                        local.get $l12
                        local.get $l5
                        i32.const 432
                        i32.add
                        local.get $p1
                        i32.const 1
                        i32.sub
                        local.tee $p0
                        i32.const 2
                        i32.shl
                        i32.add
                        local.tee $p4
                        i32.load
                        local.tee $p2
                        i32.const 11
                        i32.shr_u
                        i32.const 4
                        i32.shl
                        i32.add
                        local.set $l6
                        block $B16
                          local.get $p2
                          i32.const 1
                          i32.shr_u
                          i32.const 3
                          i32.and
                          local.tee $l13
                          i32.const 2
                          i32.lt_u
                          if $I17
                            local.get $p0
                            local.set $p1
                            br $B16
                          end
                          local.get $l6
                          i32.load16_s offset=12
                          local.set $p2
                          local.get $l6
                          i32.load16_s offset=14
                          local.set $p3
                          local.get $l6
                          i32.load16_s offset=28
                          local.set $l8
                          local.get $l6
                          i32.load16_s offset=30
                          local.set $l9
                          local.get $l6
                          i32.load16_s offset=44
                          local.set $l10
                          local.get $l6
                          i32.load16_s offset=46
                          local.set $l11
                          local.get $l5
                          local.get $l5
                          f32.load offset=140
                          f32.const 0x0p+0 (;=0;)
                          f32.mul
                          local.tee $l15
                          local.get $l5
                          f32.load offset=156
                          f32.const 0x0p+0 (;=0;)
                          f32.mul
                          local.tee $l17
                          f32.add
                          f32.const 0x1p-1 (;=0.5;)
                          f32.mul
                          f32.store offset=1484
                          local.get $l5
                          local.get $l5
                          f32.load offset=136
                          local.get $l10
                          f32.convert_i32_s
                          f32.mul
                          local.tee $l18
                          local.get $l5
                          f32.load offset=152
                          local.get $l11
                          f32.convert_i32_s
                          f32.mul
                          local.tee $l20
                          f32.add
                          f32.const 0x1p-1 (;=0.5;)
                          f32.mul
                          f32.store offset=1480
                          local.get $l5
                          local.get $l5
                          f32.load offset=132
                          local.get $l8
                          f32.convert_i32_s
                          f32.mul
                          local.tee $l16
                          local.get $l5
                          f32.load offset=148
                          local.get $l9
                          f32.convert_i32_s
                          f32.mul
                          local.tee $l14
                          f32.add
                          f32.const 0x1p-1 (;=0.5;)
                          f32.mul
                          f32.store offset=1476
                          local.get $l5
                          local.get $l14
                          local.get $l16
                          f32.sub
                          f32.const 0x1p-1 (;=0.5;)
                          f32.mul
                          f32.store offset=1460
                          local.get $l5
                          local.get $l5
                          f32.load offset=128
                          local.get $p2
                          f32.convert_i32_s
                          f32.mul
                          local.tee $l16
                          local.get $l5
                          f32.load offset=144
                          local.get $p3
                          f32.convert_i32_s
                          f32.mul
                          local.tee $l14
                          f32.add
                          f32.const 0x1p-1 (;=0.5;)
                          f32.mul
                          f32.store offset=1472
                          local.get $l5
                          local.get $l14
                          local.get $l16
                          f32.sub
                          f32.const 0x1p-1 (;=0.5;)
                          f32.mul
                          f32.store offset=1456
                          local.get $l5
                          local.get $l17
                          local.get $l15
                          f32.sub
                          f32.const 0x1p-1 (;=0.5;)
                          f32.mul
                          f32.store offset=1468
                          local.get $l5
                          local.get $l20
                          local.get $l18
                          f32.sub
                          f32.const 0x1p-1 (;=0.5;)
                          f32.mul
                          f32.store offset=1464
                          local.get $l5
                          local.get $l5
                          i64.load offset=1480
                          i64.store offset=120
                          local.get $l5
                          local.get $l5
                          i64.load offset=1472
                          i64.store offset=112
                          local.get $l5
                          local.get $l5
                          i64.load offset=1464
                          i64.store offset=104
                          local.get $l5
                          local.get $l5
                          i64.load offset=1456
                          i64.store offset=96
                          local.get $l5
                          i32.const 112
                          i32.add
                          local.get $l5
                          i32.const 96
                          i32.add
                          local.get $l5
                          i32.const 128
                          i32.add
                          call $f69988
                          i32.eqz
                          if $I18
                            local.get $p0
                            local.set $p1
                            br $B16
                          end
                          local.get $l6
                          i32.load offset=60
                          local.tee $p3
                          i32.const 1
                          i32.and
                          if $I19
                            local.get $p3
                            i32.const 5
                            i32.shr_u
                            local.set $p2
                            local.get $p3
                            i32.const 1
                            i32.shr_u
                            i32.const 15
                            i32.and
                            local.set $p3
                            loop $L20
                              block $B21 (result i32)
                                local.get $l5
                                i32.load offset=304
                                local.tee $p4
                                if $I22
                                  local.get $p4
                                  local.get $p2
                                  i32.const 12
                                  i32.mul
                                  i32.add
                                  local.tee $p4
                                  i32.load offset=8
                                  local.set $l8
                                  local.get $p4
                                  i32.load
                                  local.set $l10
                                  local.get $p4
                                  i32.load offset=4
                                  br $B21
                                end
                                local.get $l5
                                i32.load offset=308
                                local.get $p2
                                i32.const 6
                                i32.mul
                                i32.add
                                local.tee $p4
                                i32.load16_u offset=4
                                local.set $l8
                                local.get $p4
                                i32.load16_u
                                local.set $l10
                                local.get $p4
                                i32.load16_u offset=2
                              end
                              local.set $l9
                              local.get $l5
                              i32.load offset=312
                              local.tee $p4
                              local.get $l10
                              i32.const 12
                              i32.mul
                              i32.add
                              local.get $p4
                              local.get $l9
                              i32.const 12
                              i32.mul
                              i32.add
                              local.get $p4
                              local.get $l8
                              i32.const 12
                              i32.mul
                              i32.add
                              local.get $l5
                              i32.const 128
                              i32.add
                              call $f69991
                              if $I23
                                local.get $l5
                                i32.load offset=416
                                local.tee $p4
                                local.get $l5
                                i32.load offset=420
                                i32.eq
                                br_if $B13
                                local.get $l5
                                i32.load offset=424
                                local.get $p4
                                i32.const 2
                                i32.shl
                                i32.add
                                local.get $p2
                                i32.store
                                local.get $l5
                                local.get $l5
                                i32.load offset=416
                                i32.const 1
                                i32.add
                                i32.store offset=416
                              end
                              local.get $p2
                              i32.const 1
                              i32.add
                              local.set $p2
                              local.get $p3
                              i32.const 1
                              i32.sub
                              local.tee $p3
                              br_if $L20
                            end
                            local.get $p0
                            local.set $p1
                            br $B16
                          end
                          local.get $p4
                          local.get $p3
                          i32.store
                        end
                        block $B24
                          local.get $l13
                          i32.eqz
                          br_if $B24
                          local.get $l6
                          i32.load16_s offset=10
                          local.set $p2
                          local.get $l6
                          i32.load16_s offset=8
                          local.set $p4
                          local.get $l6
                          i32.load16_s offset=24
                          local.set $p3
                          local.get $l6
                          i32.load16_s offset=26
                          local.set $l8
                          local.get $l6
                          i32.load16_s offset=40
                          local.set $l9
                          local.get $l6
                          i32.load16_s offset=42
                          local.set $l10
                          local.get $l5
                          local.get $l5
                          f32.load offset=140
                          f32.const 0x0p+0 (;=0;)
                          f32.mul
                          local.tee $l15
                          local.get $l5
                          f32.load offset=156
                          f32.const 0x0p+0 (;=0;)
                          f32.mul
                          local.tee $l17
                          f32.add
                          f32.const 0x1p-1 (;=0.5;)
                          f32.mul
                          f32.store offset=1484
                          local.get $l5
                          local.get $l5
                          f32.load offset=136
                          local.get $l9
                          f32.convert_i32_s
                          f32.mul
                          local.tee $l18
                          local.get $l5
                          f32.load offset=152
                          local.get $l10
                          f32.convert_i32_s
                          f32.mul
                          local.tee $l20
                          f32.add
                          f32.const 0x1p-1 (;=0.5;)
                          f32.mul
                          f32.store offset=1480
                          local.get $l5
                          local.get $l5
                          f32.load offset=132
                          local.get $p3
                          f32.convert_i32_s
                          f32.mul
                          local.tee $l16
                          local.get $l5
                          f32.load offset=148
                          local.get $l8
                          f32.convert_i32_s
                          f32.mul
                          local.tee $l14
                          f32.add
                          f32.const 0x1p-1 (;=0.5;)
                          f32.mul
                          f32.store offset=1476
                          local.get $l5
                          local.get $l14
                          local.get $l16
                          f32.sub
                          f32.const 0x1p-1 (;=0.5;)
                          f32.mul
                          f32.store offset=1460
                          local.get $l5
                          local.get $l5
                          f32.load offset=128
                          local.get $p4
                          f32.convert_i32_s
                          f32.mul
                          local.tee $l16
                          local.get $l5
                          f32.load offset=144
                          local.get $p2
                          f32.convert_i32_s
                          f32.mul
                          local.tee $l14
                          f32.add
                          f32.const 0x1p-1 (;=0.5;)
                          f32.mul
                          f32.store offset=1472
                          local.get $l5
                          local.get $l14
                          local.get $l16
                          f32.sub
                          f32.const 0x1p-1 (;=0.5;)
                          f32.mul
                          f32.store offset=1456
                          local.get $l5
                          local.get $l17
                          local.get $l15
                          f32.sub
                          f32.const 0x1p-1 (;=0.5;)
                          f32.mul
                          f32.store offset=1468
                          local.get $l5
                          local.get $l20
                          local.get $l18
                          f32.sub
                          f32.const 0x1p-1 (;=0.5;)
                          f32.mul
                          f32.store offset=1464
                          local.get $l5
                          local.get $l5
                          i64.load offset=1480
                          i64.store offset=88
                          local.get $l5
                          local.get $l5
                          i64.load offset=1472
                          i64.store offset=80
                          local.get $l5
                          local.get $l5
                          i64.load offset=1464
                          i64.store offset=72
                          local.get $l5
                          local.get $l5
                          i64.load offset=1456
                          i64.store offset=64
                          local.get $l5
                          i32.const 80
                          i32.add
                          local.get $l5
                          i32.const -64
                          i32.sub
                          local.get $l5
                          i32.const 128
                          i32.add
                          call $f69988
                          i32.eqz
                          br_if $B24
                          local.get $l6
                          i32.load offset=56
                          local.tee $p4
                          i32.const 1
                          i32.and
                          if $I25
                            local.get $p4
                            i32.const 5
                            i32.shr_u
                            local.set $p2
                            local.get $p4
                            i32.const 1
                            i32.shr_u
                            i32.const 15
                            i32.and
                            local.set $p3
                            loop $L26
                              block $B27 (result i32)
                                local.get $l5
                                i32.load offset=304
                                local.tee $p4
                                if $I28
                                  local.get $p4
                                  local.get $p2
                                  i32.const 12
                                  i32.mul
                                  i32.add
                                  local.tee $p4
                                  i32.load offset=8
                                  local.set $l8
                                  local.get $p4
                                  i32.load
                                  local.set $l10
                                  local.get $p4
                                  i32.load offset=4
                                  br $B27
                                end
                                local.get $l5
                                i32.load offset=308
                                local.get $p2
                                i32.const 6
                                i32.mul
                                i32.add
                                local.tee $p4
                                i32.load16_u offset=4
                                local.set $l8
                                local.get $p4
                                i32.load16_u
                                local.set $l10
                                local.get $p4
                                i32.load16_u offset=2
                              end
                              local.set $l9
                              local.get $l5
                              i32.load offset=312
                              local.tee $p4
                              local.get $l10
                              i32.const 12
                              i32.mul
                              i32.add
                              local.get $p4
                              local.get $l9
                              i32.const 12
                              i32.mul
                              i32.add
                              local.get $p4
                              local.get $l8
                              i32.const 12
                              i32.mul
                              i32.add
                              local.get $l5
                              i32.const 128
                              i32.add
                              call $f69991
                              if $I29
                                local.get $l5
                                i32.load offset=416
                                local.tee $p4
                                local.get $l5
                                i32.load offset=420
                                i32.eq
                                br_if $B13
                                local.get $l5
                                i32.load offset=424
                                local.get $p4
                                i32.const 2
                                i32.shl
                                i32.add
                                local.get $p2
                                i32.store
                                local.get $l5
                                local.get $l5
                                i32.load offset=416
                                i32.const 1
                                i32.add
                                i32.store offset=416
                              end
                              local.get $p2
                              i32.const 1
                              i32.add
                              local.set $p2
                              local.get $p3
                              i32.const 1
                              i32.sub
                              local.tee $p3
                              br_if $L26
                            end
                            br $B24
                          end
                          local.get $l5
                          i32.const 432
                          i32.add
                          local.get $p1
                          i32.const 2
                          i32.shl
                          i32.add
                          local.get $p4
                          i32.store
                          local.get $p1
                          i32.const 1
                          i32.add
                          local.set $p1
                        end
                        local.get $l6
                        i32.load16_s offset=6
                        local.set $p2
                        local.get $l6
                        i32.load16_s offset=4
                        local.set $p4
                        local.get $l6
                        i32.load16_s offset=20
                        local.set $p3
                        local.get $l6
                        i32.load16_s offset=22
                        local.set $l8
                        local.get $l6
                        i32.load16_s offset=36
                        local.set $l9
                        local.get $l6
                        i32.load16_s offset=38
                        local.set $l10
                        local.get $l5
                        local.get $l5
                        f32.load offset=140
                        f32.const 0x0p+0 (;=0;)
                        f32.mul
                        local.tee $l15
                        local.get $l5
                        f32.load offset=156
                        f32.const 0x0p+0 (;=0;)
                        f32.mul
                        local.tee $l17
                        f32.add
                        f32.const 0x1p-1 (;=0.5;)
                        f32.mul
                        f32.store offset=1484
                        local.get $l5
                        local.get $l5
                        f32.load offset=136
                        local.get $l9
                        f32.convert_i32_s
                        f32.mul
                        local.tee $l18
                        local.get $l5
                        f32.load offset=152
                        local.get $l10
                        f32.convert_i32_s
                        f32.mul
                        local.tee $l20
                        f32.add
                        f32.const 0x1p-1 (;=0.5;)
                        f32.mul
                        f32.store offset=1480
                        local.get $l5
                        local.get $l5
                        f32.load offset=132
                        local.get $p3
                        f32.convert_i32_s
                        f32.mul
                        local.tee $l16
                        local.get $l5
                        f32.load offset=148
                        local.get $l8
                        f32.convert_i32_s
                        f32.mul
                        local.tee $l14
                        f32.add
                        f32.const 0x1p-1 (;=0.5;)
                        f32.mul
                        f32.store offset=1476
                        local.get $l5
                        local.get $l14
                        local.get $l16
                        f32.sub
                        f32.const 0x1p-1 (;=0.5;)
                        f32.mul
                        f32.store offset=1460
                        local.get $l5
                        local.get $l5
                        f32.load offset=128
                        local.get $p4
                        f32.convert_i32_s
                        f32.mul
                        local.tee $l16
                        local.get $l5
                        f32.load offset=144
                        local.get $p2
                        f32.convert_i32_s
                        f32.mul
                        local.tee $l14
                        f32.add
                        f32.const 0x1p-1 (;=0.5;)
                        f32.mul
                        f32.store offset=1472
                        local.get $l5
                        local.get $l14
                        local.get $l16
                        f32.sub
                        f32.const 0x1p-1 (;=0.5;)
                        f32.mul
                        f32.store offset=1456
                        local.get $l5
                        local.get $l17
                        local.get $l15
                        f32.sub
                        f32.const 0x1p-1 (;=0.5;)
                        f32.mul
                        f32.store offset=1468
                        local.get $l5
                        local.get $l20
                        local.get $l18
                        f32.sub
                        f32.const 0x1p-1 (;=0.5;)
                        f32.mul
                        f32.store offset=1464
                        local.get $l5
                        local.get $l5
                        i64.load offset=1480
                        i64.store offset=56
                        local.get $l5
                        local.get $l5
                        i64.load offset=1472
                        i64.store offset=48
                        local.get $l5
                        local.get $l5
                        i64.load offset=1464
                        i64.store offset=40
                        local.get $l5
                        local.get $l5
                        i64.load offset=1456
                        i64.store offset=32
                        block $B30
                          local.get $l5
                          i32.const 48
                          i32.add
                          local.get $l5
                          i32.const 32
                          i32.add
                          local.get $l5
                          i32.const 128
                          i32.add
                          call $f69988
                          i32.eqz
                          br_if $B30
                          local.get $l6
                          i32.load offset=52
                          local.tee $p4
                          i32.const 1
                          i32.and
                          if $I31
                            local.get $p4
                            i32.const 5
                            i32.shr_u
                            local.set $p2
                            local.get $p4
                            i32.const 1
                            i32.shr_u
                            i32.const 15
                            i32.and
                            local.set $p3
                            loop $L32
                              block $B33 (result i32)
                                local.get $l5
                                i32.load offset=304
                                local.tee $p4
                                if $I34
                                  local.get $p4
                                  local.get $p2
                                  i32.const 12
                                  i32.mul
                                  i32.add
                                  local.tee $p4
                                  i32.load offset=8
                                  local.set $l8
                                  local.get $p4
                                  i32.load
                                  local.set $l10
                                  local.get $p4
                                  i32.load offset=4
                                  br $B33
                                end
                                local.get $l5
                                i32.load offset=308
                                local.get $p2
                                i32.const 6
                                i32.mul
                                i32.add
                                local.tee $p4
                                i32.load16_u offset=4
                                local.set $l8
                                local.get $p4
                                i32.load16_u
                                local.set $l10
                                local.get $p4
                                i32.load16_u offset=2
                              end
                              local.set $l9
                              block $B35
                                local.get $l5
                                i32.load offset=312
                                local.tee $p4
                                local.get $l10
                                i32.const 12
                                i32.mul
                                i32.add
                                local.get $p4
                                local.get $l9
                                i32.const 12
                                i32.mul
                                i32.add
                                local.get $p4
                                local.get $l8
                                i32.const 12
                                i32.mul
                                i32.add
                                local.get $l5
                                i32.const 128
                                i32.add
                                call $f69991
                                if $I36
                                  local.get $l5
                                  i32.load offset=416
                                  local.tee $p4
                                  local.get $l5
                                  i32.load offset=420
                                  i32.eq
                                  br_if $B35
                                  local.get $l5
                                  i32.load offset=424
                                  local.get $p4
                                  i32.const 2
                                  i32.shl
                                  i32.add
                                  local.get $p2
                                  i32.store
                                  local.get $l5
                                  local.get $l5
                                  i32.load offset=416
                                  i32.const 1
                                  i32.add
                                  i32.store offset=416
                                end
                                local.get $p2
                                i32.const 1
                                i32.add
                                local.set $p2
                                local.get $p3
                                i32.const 1
                                i32.sub
                                local.tee $p3
                                br_if $L32
                                br $B30
                              end
                            end
                            i32.const 1
                            br $B12
                          end
                          local.get $l5
                          i32.const 432
                          i32.add
                          local.get $p1
                          i32.const 2
                          i32.shl
                          i32.add
                          local.get $p4
                          i32.store
                          local.get $p1
                          i32.const 1
                          i32.add
                          local.set $p1
                        end
                        local.get $l6
                        i32.load16_s offset=2
                        local.set $p2
                        local.get $l6
                        i32.load16_s offset=18
                        local.set $p4
                        local.get $l6
                        i32.load16_s offset=34
                        local.set $p3
                        local.get $l6
                        i32.load16_s
                        local.set $l8
                        local.get $l6
                        i32.load16_s offset=16
                        local.set $l9
                        local.get $l6
                        i32.load16_s offset=32
                        local.set $l10
                        local.get $l5
                        local.get $l5
                        f32.load offset=140
                        f32.const 0x0p+0 (;=0;)
                        f32.mul
                        local.tee $l15
                        local.get $l5
                        f32.load offset=156
                        f32.const 0x0p+0 (;=0;)
                        f32.mul
                        local.tee $l17
                        f32.add
                        f32.const 0x1p-1 (;=0.5;)
                        f32.mul
                        f32.store offset=1484
                        local.get $l5
                        local.get $l5
                        f32.load offset=136
                        local.get $l10
                        f32.convert_i32_s
                        f32.mul
                        local.tee $l18
                        local.get $l5
                        f32.load offset=152
                        local.get $p3
                        f32.convert_i32_s
                        f32.mul
                        local.tee $l20
                        f32.add
                        f32.const 0x1p-1 (;=0.5;)
                        f32.mul
                        f32.store offset=1480
                        local.get $l5
                        local.get $l5
                        f32.load offset=132
                        local.get $l9
                        f32.convert_i32_s
                        f32.mul
                        local.tee $l16
                        local.get $l5
                        f32.load offset=148
                        local.get $p4
                        f32.convert_i32_s
                        f32.mul
                        local.tee $l14
                        f32.add
                        f32.const 0x1p-1 (;=0.5;)
                        f32.mul
                        f32.store offset=1476
                        local.get $l5
                        local.get $l5
                        f32.load offset=128
                        local.get $l8
                        f32.convert_i32_s
                        f32.mul
                        local.tee $l23
                        local.get $l5
                        f32.load offset=144
                        local.get $p2
                        f32.convert_i32_s
                        f32.mul
                        local.tee $l26
                        f32.add
                        f32.const 0x1p-1 (;=0.5;)
                        f32.mul
                        f32.store offset=1472
                        local.get $l5
                        local.get $l14
                        local.get $l16
                        f32.sub
                        f32.const 0x1p-1 (;=0.5;)
                        f32.mul
                        f32.store offset=1460
                        local.get $l5
                        local.get $l26
                        local.get $l23
                        f32.sub
                        f32.const 0x1p-1 (;=0.5;)
                        f32.mul
                        f32.store offset=1456
                        local.get $l5
                        local.get $l17
                        local.get $l15
                        f32.sub
                        f32.const 0x1p-1 (;=0.5;)
                        f32.mul
                        f32.store offset=1468
                        local.get $l5
                        local.get $l20
                        local.get $l18
                        f32.sub
                        f32.const 0x1p-1 (;=0.5;)
                        f32.mul
                        f32.store offset=1464
                        local.get $l5
                        local.get $l5
                        i64.load offset=1480
                        i64.store offset=24
                        local.get $l5
                        local.get $l5
                        i64.load offset=1472
                        i64.store offset=16
                        local.get $l5
                        local.get $l5
                        i64.load offset=1464
                        i64.store offset=8
                        local.get $l5
                        local.get $l5
                        i64.load offset=1456
                        i64.store
                        block $B37
                          local.get $l5
                          i32.const 16
                          i32.add
                          local.get $l5
                          local.get $l5
                          i32.const 128
                          i32.add
                          call $f69988
                          i32.eqz
                          br_if $B37
                          local.get $l6
                          i32.load offset=48
                          local.tee $l6
                          i32.const 1
                          i32.and
                          if $I38
                            local.get $l6
                            i32.const 5
                            i32.shr_u
                            local.set $p2
                            local.get $l6
                            i32.const 1
                            i32.shr_u
                            i32.const 15
                            i32.and
                            local.set $p4
                            loop $L39
                              block $B40 (result i32)
                                local.get $l5
                                i32.load offset=304
                                local.tee $l6
                                if $I41
                                  local.get $l6
                                  local.get $p2
                                  i32.const 12
                                  i32.mul
                                  i32.add
                                  local.tee $l6
                                  i32.load offset=8
                                  local.set $p3
                                  local.get $l6
                                  i32.load offset=4
                                  local.set $l8
                                  local.get $l6
                                  i32.load
                                  br $B40
                                end
                                local.get $l5
                                i32.load offset=308
                                local.get $p2
                                i32.const 6
                                i32.mul
                                i32.add
                                local.tee $l6
                                i32.load16_u offset=4
                                local.set $p3
                                local.get $l6
                                i32.load16_u offset=2
                                local.set $l8
                                local.get $l6
                                i32.load16_u
                              end
                              local.set $l9
                              block $B42
                                local.get $l5
                                i32.load offset=312
                                local.tee $l6
                                local.get $l9
                                i32.const 12
                                i32.mul
                                i32.add
                                local.get $l6
                                local.get $l8
                                i32.const 12
                                i32.mul
                                i32.add
                                local.get $l6
                                local.get $p3
                                i32.const 12
                                i32.mul
                                i32.add
                                local.get $l5
                                i32.const 128
                                i32.add
                                call $f69991
                                if $I43
                                  local.get $l5
                                  i32.load offset=416
                                  local.tee $l6
                                  local.get $l5
                                  i32.load offset=420
                                  i32.eq
                                  br_if $B42
                                  local.get $l5
                                  i32.load offset=424
                                  local.get $l6
                                  i32.const 2
                                  i32.shl
                                  i32.add
                                  local.get $p2
                                  i32.store
                                  local.get $l5
                                  local.get $l5
                                  i32.load offset=416
                                  i32.const 1
                                  i32.add
                                  i32.store offset=416
                                end
                                local.get $p2
                                i32.const 1
                                i32.add
                                local.set $p2
                                local.get $p4
                                i32.const 1
                                i32.sub
                                local.tee $p4
                                br_if $L39
                                br $B37
                              end
                            end
                            i32.const 1
                            br $B12
                          end
                          local.get $l5
                          i32.const 432
                          i32.add
                          local.get $p1
                          i32.const 2
                          i32.shl
                          i32.add
                          local.get $l6
                          i32.store
                          local.get $p1
                          i32.const 1
                          i32.add
                          local.set $p1
                        end
                        local.get $p1
                        br_if $L15
                      end
                      i32.const 0
                      br $B12
                    end
                    local.get $l6
                    i32.load offset=12
                    local.tee $l6
                    i32.const 4
                    i32.shr_u
                    local.set $p2
                    local.get $l6
                    i32.const 15
                    i32.and
                    local.set $p4
                    loop $L44
                      block $B45 (result i32)
                        local.get $l5
                        i32.load offset=304
                        local.tee $l6
                        if $I46
                          local.get $l6
                          local.get $p2
                          i32.const 12
                          i32.mul
                          i32.add
                          local.tee $l6
                          i32.load offset=8
                          local.set $p3
                          local.get $l6
                          i32.load offset=4
                          local.set $l8
                          local.get $l6
                          i32.load
                          br $B45
                        end
                        local.get $l5
                        i32.load offset=308
                        local.get $p2
                        i32.const 6
                        i32.mul
                        i32.add
                        local.tee $l6
                        i32.load16_u offset=4
                        local.set $p3
                        local.get $l6
                        i32.load16_u offset=2
                        local.set $l8
                        local.get $l6
                        i32.load16_u
                      end
                      local.set $l9
                      local.get $l5
                      i32.load offset=312
                      local.tee $l6
                      local.get $l9
                      i32.const 12
                      i32.mul
                      i32.add
                      local.get $l6
                      local.get $l8
                      i32.const 12
                      i32.mul
                      i32.add
                      local.get $l6
                      local.get $p3
                      i32.const 12
                      i32.mul
                      i32.add
                      local.get $l5
                      i32.const 128
                      i32.add
                      call $f69991
                      if $I47
                        i32.const 1
                        local.get $l5
                        i32.load offset=416
                        local.tee $l6
                        local.get $l5
                        i32.load offset=420
                        i32.eq
                        br_if $B11
                        drop
                        local.get $l5
                        i32.load offset=424
                        local.get $l6
                        i32.const 2
                        i32.shl
                        i32.add
                        local.get $p2
                        i32.store
                        local.get $l5
                        local.get $l5
                        i32.load offset=416
                        i32.const 1
                        i32.add
                        i32.store offset=416
                      end
                      local.get $p2
                      i32.const 1
                      i32.add
                      local.set $p2
                      local.get $p4
                      i32.const 1
                      i32.sub
                      local.tee $p4
                      br_if $L44
                    end
                    i32.const 0
                    br $B11
                  end
                  i32.const 1
                end
                i32.const 0
                i32.ne
              end
              i32.store8
              local.get $l5
              i32.load offset=416
              local.set $p2
              local.get $l5
              i32.const 1488
              i32.add
              global.set $g0
              local.get $p2
            end
            i32.store offset=4
            br $B8
          end
          global.get $g0
          i32.const 1472
          i32.sub
          local.tee $l5
          global.set $g0
          local.get $p1
          local.tee $p4
          i32.load
          local.set $l6
          local.get $l5
          i32.const 368
          i32.add
          local.tee $l9
          local.get $p0
          local.get $p3
          call $f69990
          local.get $l5
          local.get $l5
          f32.load offset=388
          local.get $l5
          f32.load offset=376
          f32.sub
          local.tee $l15
          f32.store offset=404
          local.get $l5
          local.get $l5
          f32.load offset=384
          local.get $l5
          f32.load offset=372
          f32.sub
          local.tee $l17
          f32.store offset=400
          local.get $l5
          local.get $l5
          f32.load offset=380
          local.get $l5
          f32.load offset=368
          f32.sub
          local.tee $l18
          f32.store offset=396
          local.get $l5
          local.get $l18
          local.get $l18
          f32.mul
          local.get $l17
          local.get $l17
          f32.mul
          f32.add
          local.get $l15
          local.get $l15
          f32.mul
          f32.add
          local.tee $l15
          f32.store offset=408
          local.get $l5
          f32.const 0x1p+0 (;=1;)
          local.get $l15
          f32.div
          f32.const 0x0p+0 (;=0;)
          local.get $l15
          f32.const 0x0p+0 (;=0;)
          f32.ne
          select
          f32.store offset=412
          local.get $l9
          local.get $l5
          i32.const 416
          i32.add
          call $f70397
          local.get $l5
          local.get $l5
          f32.load offset=424
          local.tee $l15
          f32.store offset=340
          local.get $l5
          local.get $l5
          f32.load offset=420
          local.tee $l17
          f32.store offset=328
          local.get $l5
          local.get $l5
          f32.load offset=436
          local.tee $l18
          f32.store offset=344
          local.get $l5
          local.get $l5
          f32.load offset=432
          local.tee $l20
          f32.store offset=332
          local.get $l5
          local.get $l5
          f32.load offset=428
          local.tee $l16
          f32.store offset=320
          local.get $l5
          local.get $l16
          local.get $l5
          f32.load offset=452
          local.tee $l14
          f32.mul
          local.get $l20
          local.get $l5
          f32.load offset=456
          local.tee $l23
          f32.mul
          f32.add
          local.get $l18
          local.get $l5
          f32.load offset=460
          local.tee $l26
          f32.mul
          f32.add
          f32.neg
          f32.store offset=356
          local.get $l5
          local.get $l5
          f32.load offset=416
          local.tee $l29
          f32.store offset=316
          local.get $l5
          local.get $l14
          local.get $l29
          f32.mul
          local.get $l23
          local.get $l17
          f32.mul
          f32.add
          local.get $l26
          local.get $l15
          f32.mul
          f32.add
          f32.neg
          f32.store offset=352
          local.get $l5
          local.get $l14
          local.get $l5
          f32.load offset=440
          local.tee $l30
          f32.mul
          local.get $l23
          local.get $l5
          f32.load offset=444
          local.tee $l31
          f32.mul
          f32.add
          local.get $l26
          local.get $l5
          f32.load offset=448
          local.tee $l32
          f32.mul
          f32.add
          f32.neg
          f32.store offset=360
          local.get $l5
          local.get $l32
          f32.store offset=348
          local.get $l5
          local.get $l31
          f32.store offset=336
          local.get $l5
          local.get $l30
          f32.store offset=324
          local.get $l5
          local.get $l23
          f32.store offset=164
          local.get $l5
          local.get $l26
          f32.store offset=168
          local.get $l5
          local.get $l14
          f32.store offset=160
          local.get $l5
          local.get $l6
          i32.load offset=16
          i32.store offset=304
          local.get $l5
          local.get $l6
          i32.load offset=20
          i32.store offset=308
          local.get $l5
          local.get $l6
          i32.load offset=4
          i32.store offset=312
          local.get $p4
          f32.load offset=40
          local.set $l14
          local.get $p4
          i64.load offset=32 align=4
          local.set $l33
          local.get $l5
          local.get $p4
          f32.load offset=44
          local.tee $l23
          f32.store offset=140
          local.get $l5
          local.get $l14
          f32.store offset=136
          local.get $l5
          local.get $l33
          i64.store offset=128
          local.get $p4
          f32.load offset=56
          local.set $l14
          local.get $l5
          local.get $p4
          i64.load offset=48 align=4
          i64.store offset=148 align=4
          local.get $l5
          local.get $l16
          f32.abs
          f32.const 0x1.0c6f7ap-20 (;=1e-06;)
          f32.add
          local.tee $l26
          f32.store offset=292
          local.get $l5
          local.get $l31
          f32.store offset=248
          local.get $l5
          local.get $l16
          f32.store offset=244
          local.get $l5
          local.get $l30
          f32.store offset=232
          local.get $l5
          local.get $l18
          f32.store offset=228
          local.get $l5
          local.get $l32
          f32.store offset=216
          local.get $l5
          local.get $l20
          f32.store offset=212
          local.get $l5
          local.get $l14
          f32.store offset=156
          local.get $l5
          local.get $l31
          f32.abs
          f32.const 0x1.0c6f7ap-20 (;=1e-06;)
          f32.add
          local.tee $l16
          f32.store offset=296
          local.get $l5
          local.get $l30
          f32.abs
          f32.const 0x1.0c6f7ap-20 (;=1e-06;)
          f32.add
          local.tee $l14
          f32.store offset=280
          local.get $l5
          local.get $l18
          f32.abs
          f32.const 0x1.0c6f7ap-20 (;=1e-06;)
          f32.add
          local.tee $l30
          f32.store offset=276
          local.get $l5
          local.get $l20
          f32.abs
          f32.const 0x1.0c6f7ap-20 (;=1e-06;)
          f32.add
          local.tee $l20
          f32.store offset=260
          local.get $l5
          local.get $l15
          f32.store offset=240
          local.get $l5
          local.get $l17
          f32.store offset=224
          local.get $l5
          local.get $l29
          f32.store offset=208
          local.get $l5
          local.get $l23
          f32.store offset=144
          local.get $l5
          local.get $l29
          f32.abs
          f32.const 0x1.0c6f7ap-20 (;=1e-06;)
          f32.add
          local.tee $l23
          f32.store offset=256
          local.get $l5
          local.get $l15
          f32.abs
          f32.const 0x1.0c6f7ap-20 (;=1e-06;)
          f32.add
          local.tee $l29
          f32.store offset=288
          local.get $l5
          local.get $l17
          f32.abs
          f32.const 0x1.0c6f7ap-20 (;=1e-06;)
          f32.add
          local.tee $l31
          f32.store offset=272
          local.get $l5
          local.get $l32
          f32.abs
          f32.const 0x1.0c6f7ap-20 (;=1e-06;)
          f32.add
          local.tee $l32
          f32.store offset=264
          local.get $l5
          local.get $l5
          f32.load offset=468
          local.tee $l15
          f32.store offset=196
          local.get $l5
          local.get $l5
          f32.load offset=472
          local.tee $l17
          f32.store offset=200
          local.get $l5
          local.get $l31
          local.get $l5
          f32.load offset=464
          local.tee $l18
          f32.mul
          local.get $l20
          local.get $l15
          f32.mul
          f32.add
          local.get $l16
          local.get $l17
          f32.mul
          f32.add
          f32.store offset=180
          local.get $l5
          local.get $l29
          local.get $l18
          f32.mul
          local.get $l30
          local.get $l15
          f32.mul
          f32.add
          local.get $l32
          local.get $l17
          f32.mul
          f32.add
          f32.store offset=184
          local.get $l5
          local.get $l18
          f32.store offset=192
          local.get $l5
          local.get $l23
          local.get $l18
          f32.mul
          local.get $l26
          local.get $l15
          f32.mul
          f32.add
          local.get $l14
          local.get $l17
          f32.mul
          f32.add
          f32.store offset=176
          block $B48 (result i32)
            block $B49
              block $B50
                local.get $p4
                i32.load offset=24
                local.tee $l12
                if $I51
                  local.get $l5
                  local.get $p4
                  i32.load offset=28
                  i32.store offset=416
                  i32.const 1
                  local.set $p1
                  loop $L52
                    local.get $l12
                    local.get $l5
                    i32.const 416
                    i32.add
                    local.get $p1
                    i32.const 1
                    i32.sub
                    local.tee $p0
                    i32.const 2
                    i32.shl
                    i32.add
                    local.tee $p2
                    i32.load
                    local.tee $l6
                    i32.const 11
                    i32.shr_u
                    i32.const 4
                    i32.shl
                    i32.add
                    local.set $p4
                    block $B53
                      local.get $l6
                      i32.const 1
                      i32.shr_u
                      i32.const 3
                      i32.and
                      local.tee $l13
                      i32.const 2
                      i32.lt_u
                      if $I54
                        local.get $p0
                        local.set $p1
                        br $B53
                      end
                      local.get $p4
                      i32.load16_s offset=12
                      local.set $l6
                      local.get $p4
                      i32.load16_s offset=14
                      local.set $p3
                      local.get $p4
                      i32.load16_s offset=28
                      local.set $l9
                      local.get $p4
                      i32.load16_s offset=30
                      local.set $l8
                      local.get $p4
                      i32.load16_s offset=44
                      local.set $l10
                      local.get $p4
                      i32.load16_s offset=46
                      local.set $l11
                      local.get $l5
                      local.get $l5
                      f32.load offset=140
                      f32.const 0x0p+0 (;=0;)
                      f32.mul
                      local.tee $l15
                      local.get $l5
                      f32.load offset=156
                      f32.const 0x0p+0 (;=0;)
                      f32.mul
                      local.tee $l17
                      f32.add
                      f32.const 0x1p-1 (;=0.5;)
                      f32.mul
                      f32.store offset=1468
                      local.get $l5
                      local.get $l5
                      f32.load offset=136
                      local.get $l10
                      f32.convert_i32_s
                      f32.mul
                      local.tee $l18
                      local.get $l5
                      f32.load offset=152
                      local.get $l11
                      f32.convert_i32_s
                      f32.mul
                      local.tee $l20
                      f32.add
                      f32.const 0x1p-1 (;=0.5;)
                      f32.mul
                      f32.store offset=1464
                      local.get $l5
                      local.get $l5
                      f32.load offset=132
                      local.get $l9
                      f32.convert_i32_s
                      f32.mul
                      local.tee $l16
                      local.get $l5
                      f32.load offset=148
                      local.get $l8
                      f32.convert_i32_s
                      f32.mul
                      local.tee $l14
                      f32.add
                      f32.const 0x1p-1 (;=0.5;)
                      f32.mul
                      f32.store offset=1460
                      local.get $l5
                      local.get $l14
                      local.get $l16
                      f32.sub
                      f32.const 0x1p-1 (;=0.5;)
                      f32.mul
                      f32.store offset=1444
                      local.get $l5
                      local.get $l5
                      f32.load offset=128
                      local.get $l6
                      f32.convert_i32_s
                      f32.mul
                      local.tee $l16
                      local.get $l5
                      f32.load offset=144
                      local.get $p3
                      f32.convert_i32_s
                      f32.mul
                      local.tee $l14
                      f32.add
                      f32.const 0x1p-1 (;=0.5;)
                      f32.mul
                      f32.store offset=1456
                      local.get $l5
                      local.get $l14
                      local.get $l16
                      f32.sub
                      f32.const 0x1p-1 (;=0.5;)
                      f32.mul
                      f32.store offset=1440
                      local.get $l5
                      local.get $l17
                      local.get $l15
                      f32.sub
                      f32.const 0x1p-1 (;=0.5;)
                      f32.mul
                      f32.store offset=1452
                      local.get $l5
                      local.get $l20
                      local.get $l18
                      f32.sub
                      f32.const 0x1p-1 (;=0.5;)
                      f32.mul
                      f32.store offset=1448
                      local.get $l5
                      local.get $l5
                      i64.load offset=1464
                      i64.store offset=120
                      local.get $l5
                      local.get $l5
                      i64.load offset=1456
                      i64.store offset=112
                      local.get $l5
                      local.get $l5
                      i64.load offset=1448
                      i64.store offset=104
                      local.get $l5
                      local.get $l5
                      i64.load offset=1440
                      i64.store offset=96
                      local.get $l5
                      i32.const 112
                      i32.add
                      local.get $l5
                      i32.const 96
                      i32.add
                      local.get $l5
                      i32.const 128
                      i32.add
                      call $f69988
                      i32.eqz
                      if $I55
                        local.get $p0
                        local.set $p1
                        br $B53
                      end
                      local.get $p4
                      i32.load offset=60
                      local.tee $l6
                      i32.const 1
                      i32.and
                      if $I56
                        local.get $l6
                        i32.const 5
                        i32.shr_u
                        local.set $p2
                        local.get $l6
                        i32.const 1
                        i32.shr_u
                        i32.const 15
                        i32.and
                        local.set $l10
                        loop $L57
                          block $B58 (result i32)
                            local.get $l5
                            i32.load offset=304
                            local.tee $l6
                            if $I59
                              local.get $l6
                              local.get $p2
                              i32.const 12
                              i32.mul
                              i32.add
                              local.tee $l6
                              i32.load offset=8
                              local.set $p3
                              local.get $l6
                              i32.load
                              local.set $l8
                              local.get $l6
                              i32.load offset=4
                              br $B58
                            end
                            local.get $l5
                            i32.load offset=308
                            local.get $p2
                            i32.const 6
                            i32.mul
                            i32.add
                            local.tee $l6
                            i32.load16_u offset=4
                            local.set $p3
                            local.get $l6
                            i32.load16_u
                            local.set $l8
                            local.get $l6
                            i32.load16_u offset=2
                          end
                          local.set $l9
                          local.get $l5
                          i32.load offset=312
                          local.tee $l6
                          local.get $l8
                          i32.const 12
                          i32.mul
                          i32.add
                          local.get $l6
                          local.get $l9
                          i32.const 12
                          i32.mul
                          i32.add
                          local.get $l6
                          local.get $p3
                          i32.const 12
                          i32.mul
                          i32.add
                          local.get $l5
                          i32.const 128
                          i32.add
                          call $f69991
                          br_if $B49
                          local.get $p2
                          i32.const 1
                          i32.add
                          local.set $p2
                          local.get $l10
                          i32.const 1
                          i32.sub
                          local.tee $l10
                          br_if $L57
                        end
                        local.get $p0
                        local.set $p1
                        br $B53
                      end
                      local.get $p2
                      local.get $l6
                      i32.store
                    end
                    block $B60
                      local.get $l13
                      i32.eqz
                      br_if $B60
                      local.get $p4
                      i32.load16_s offset=10
                      local.set $l6
                      local.get $p4
                      i32.load16_s offset=8
                      local.set $p2
                      local.get $p4
                      i32.load16_s offset=24
                      local.set $p3
                      local.get $p4
                      i32.load16_s offset=26
                      local.set $l9
                      local.get $p4
                      i32.load16_s offset=40
                      local.set $l8
                      local.get $p4
                      i32.load16_s offset=42
                      local.set $l10
                      local.get $l5
                      local.get $l5
                      f32.load offset=140
                      f32.const 0x0p+0 (;=0;)
                      f32.mul
                      local.tee $l15
                      local.get $l5
                      f32.load offset=156
                      f32.const 0x0p+0 (;=0;)
                      f32.mul
                      local.tee $l17
                      f32.add
                      f32.const 0x1p-1 (;=0.5;)
                      f32.mul
                      f32.store offset=1468
                      local.get $l5
                      local.get $l5
                      f32.load offset=136
                      local.get $l8
                      f32.convert_i32_s
                      f32.mul
                      local.tee $l18
                      local.get $l5
                      f32.load offset=152
                      local.get $l10
                      f32.convert_i32_s
                      f32.mul
                      local.tee $l20
                      f32.add
                      f32.const 0x1p-1 (;=0.5;)
                      f32.mul
                      f32.store offset=1464
                      local.get $l5
                      local.get $l5
                      f32.load offset=132
                      local.get $p3
                      f32.convert_i32_s
                      f32.mul
                      local.tee $l16
                      local.get $l5
                      f32.load offset=148
                      local.get $l9
                      f32.convert_i32_s
                      f32.mul
                      local.tee $l14
                      f32.add
                      f32.const 0x1p-1 (;=0.5;)
                      f32.mul
                      f32.store offset=1460
                      local.get $l5
                      local.get $l14
                      local.get $l16
                      f32.sub
                      f32.const 0x1p-1 (;=0.5;)
                      f32.mul
                      f32.store offset=1444
                      local.get $l5
                      local.get $l5
                      f32.load offset=128
                      local.get $p2
                      f32.convert_i32_s
                      f32.mul
                      local.tee $l16
                      local.get $l5
                      f32.load offset=144
                      local.get $l6
                      f32.convert_i32_s
                      f32.mul
                      local.tee $l14
                      f32.add
                      f32.const 0x1p-1 (;=0.5;)
                      f32.mul
                      f32.store offset=1456
                      local.get $l5
                      local.get $l14
                      local.get $l16
                      f32.sub
                      f32.const 0x1p-1 (;=0.5;)
                      f32.mul
                      f32.store offset=1440
                      local.get $l5
                      local.get $l17
                      local.get $l15
                      f32.sub
                      f32.const 0x1p-1 (;=0.5;)
                      f32.mul
                      f32.store offset=1452
                      local.get $l5
                      local.get $l20
                      local.get $l18
                      f32.sub
                      f32.const 0x1p-1 (;=0.5;)
                      f32.mul
                      f32.store offset=1448
                      local.get $l5
                      local.get $l5
                      i64.load offset=1464
                      i64.store offset=88
                      local.get $l5
                      local.get $l5
                      i64.load offset=1456
                      i64.store offset=80
                      local.get $l5
                      local.get $l5
                      i64.load offset=1448
                      i64.store offset=72
                      local.get $l5
                      local.get $l5
                      i64.load offset=1440
                      i64.store offset=64
                      local.get $l5
                      i32.const 80
                      i32.add
                      local.get $l5
                      i32.const -64
                      i32.sub
                      local.get $l5
                      i32.const 128
                      i32.add
                      call $f69988
                      i32.eqz
                      br_if $B60
                      local.get $p4
                      i32.load offset=56
                      local.tee $l6
                      i32.const 1
                      i32.and
                      if $I61
                        local.get $l6
                        i32.const 5
                        i32.shr_u
                        local.set $p2
                        local.get $l6
                        i32.const 1
                        i32.shr_u
                        i32.const 15
                        i32.and
                        local.set $l10
                        loop $L62
                          block $B63 (result i32)
                            local.get $l5
                            i32.load offset=304
                            local.tee $l6
                            if $I64
                              local.get $l6
                              local.get $p2
                              i32.const 12
                              i32.mul
                              i32.add
                              local.tee $l6
                              i32.load offset=8
                              local.set $p3
                              local.get $l6
                              i32.load
                              local.set $l8
                              local.get $l6
                              i32.load offset=4
                              br $B63
                            end
                            local.get $l5
                            i32.load offset=308
                            local.get $p2
                            i32.const 6
                            i32.mul
                            i32.add
                            local.tee $l6
                            i32.load16_u offset=4
                            local.set $p3
                            local.get $l6
                            i32.load16_u
                            local.set $l8
                            local.get $l6
                            i32.load16_u offset=2
                          end
                          local.set $l9
                          local.get $l5
                          i32.load offset=312
                          local.tee $l6
                          local.get $l8
                          i32.const 12
                          i32.mul
                          i32.add
                          local.get $l6
                          local.get $l9
                          i32.const 12
                          i32.mul
                          i32.add
                          local.get $l6
                          local.get $p3
                          i32.const 12
                          i32.mul
                          i32.add
                          local.get $l5
                          i32.const 128
                          i32.add
                          call $f69991
                          br_if $B49
                          local.get $p2
                          i32.const 1
                          i32.add
                          local.set $p2
                          local.get $l10
                          i32.const 1
                          i32.sub
                          local.tee $l10
                          br_if $L62
                        end
                        br $B60
                      end
                      local.get $l5
                      i32.const 416
                      i32.add
                      local.get $p1
                      i32.const 2
                      i32.shl
                      i32.add
                      local.get $l6
                      i32.store
                      local.get $p1
                      i32.const 1
                      i32.add
                      local.set $p1
                    end
                    local.get $p4
                    i32.load16_s offset=6
                    local.set $l6
                    local.get $p4
                    i32.load16_s offset=4
                    local.set $p2
                    local.get $p4
                    i32.load16_s offset=20
                    local.set $p3
                    local.get $p4
                    i32.load16_s offset=22
                    local.set $l9
                    local.get $p4
                    i32.load16_s offset=36
                    local.set $l8
                    local.get $p4
                    i32.load16_s offset=38
                    local.set $l10
                    local.get $l5
                    local.get $l5
                    f32.load offset=140
                    f32.const 0x0p+0 (;=0;)
                    f32.mul
                    local.tee $l15
                    local.get $l5
                    f32.load offset=156
                    f32.const 0x0p+0 (;=0;)
                    f32.mul
                    local.tee $l17
                    f32.add
                    f32.const 0x1p-1 (;=0.5;)
                    f32.mul
                    f32.store offset=1468
                    local.get $l5
                    local.get $l5
                    f32.load offset=136
                    local.get $l8
                    f32.convert_i32_s
                    f32.mul
                    local.tee $l18
                    local.get $l5
                    f32.load offset=152
                    local.get $l10
                    f32.convert_i32_s
                    f32.mul
                    local.tee $l20
                    f32.add
                    f32.const 0x1p-1 (;=0.5;)
                    f32.mul
                    f32.store offset=1464
                    local.get $l5
                    local.get $l5
                    f32.load offset=132
                    local.get $p3
                    f32.convert_i32_s
                    f32.mul
                    local.tee $l16
                    local.get $l5
                    f32.load offset=148
                    local.get $l9
                    f32.convert_i32_s
                    f32.mul
                    local.tee $l14
                    f32.add
                    f32.const 0x1p-1 (;=0.5;)
                    f32.mul
                    f32.store offset=1460
                    local.get $l5
                    local.get $l14
                    local.get $l16
                    f32.sub
                    f32.const 0x1p-1 (;=0.5;)
                    f32.mul
                    f32.store offset=1444
                    local.get $l5
                    local.get $l5
                    f32.load offset=128
                    local.get $p2
                    f32.convert_i32_s
                    f32.mul
                    local.tee $l16
                    local.get $l5
                    f32.load offset=144
                    local.get $l6
                    f32.convert_i32_s
                    f32.mul
                    local.tee $l14
                    f32.add
                    f32.const 0x1p-1 (;=0.5;)
                    f32.mul
                    f32.store offset=1456
                    local.get $l5
                    local.get $l14
                    local.get $l16
                    f32.sub
                    f32.const 0x1p-1 (;=0.5;)
                    f32.mul
                    f32.store offset=1440
                    local.get $l5
                    local.get $l17
                    local.get $l15
                    f32.sub
                    f32.const 0x1p-1 (;=0.5;)
                    f32.mul
                    f32.store offset=1452
                    local.get $l5
                    local.get $l20
                    local.get $l18
                    f32.sub
                    f32.const 0x1p-1 (;=0.5;)
                    f32.mul
                    f32.store offset=1448
                    local.get $l5
                    local.get $l5
                    i64.load offset=1464
                    i64.store offset=56
                    local.get $l5
                    local.get $l5
                    i64.load offset=1456
                    i64.store offset=48
                    local.get $l5
                    local.get $l5
                    i64.load offset=1448
                    i64.store offset=40
                    local.get $l5
                    local.get $l5
                    i64.load offset=1440
                    i64.store offset=32
                    block $B65
                      local.get $l5
                      i32.const 48
                      i32.add
                      local.get $l5
                      i32.const 32
                      i32.add
                      local.get $l5
                      i32.const 128
                      i32.add
                      call $f69988
                      i32.eqz
                      br_if $B65
                      local.get $p4
                      i32.load offset=52
                      local.tee $l6
                      i32.const 1
                      i32.and
                      if $I66
                        local.get $l6
                        i32.const 5
                        i32.shr_u
                        local.set $p2
                        local.get $l6
                        i32.const 1
                        i32.shr_u
                        i32.const 15
                        i32.and
                        local.set $l10
                        loop $L67
                          block $B68 (result i32)
                            local.get $l5
                            i32.load offset=304
                            local.tee $l6
                            if $I69
                              local.get $l6
                              local.get $p2
                              i32.const 12
                              i32.mul
                              i32.add
                              local.tee $l6
                              i32.load offset=8
                              local.set $p3
                              local.get $l6
                              i32.load
                              local.set $l8
                              local.get $l6
                              i32.load offset=4
                              br $B68
                            end
                            local.get $l5
                            i32.load offset=308
                            local.get $p2
                            i32.const 6
                            i32.mul
                            i32.add
                            local.tee $l6
                            i32.load16_u offset=4
                            local.set $p3
                            local.get $l6
                            i32.load16_u
                            local.set $l8
                            local.get $l6
                            i32.load16_u offset=2
                          end
                          local.set $l9
                          local.get $l5
                          i32.load offset=312
                          local.tee $l6
                          local.get $l8
                          i32.const 12
                          i32.mul
                          i32.add
                          local.get $l6
                          local.get $l9
                          i32.const 12
                          i32.mul
                          i32.add
                          local.get $l6
                          local.get $p3
                          i32.const 12
                          i32.mul
                          i32.add
                          local.get $l5
                          i32.const 128
                          i32.add
                          call $f69991
                          i32.eqz
                          if $I70
                            local.get $p2
                            i32.const 1
                            i32.add
                            local.set $p2
                            local.get $l10
                            i32.const 1
                            i32.sub
                            local.tee $l10
                            br_if $L67
                            br $B65
                          end
                        end
                        i32.const 1
                        br $B48
                      end
                      local.get $l5
                      i32.const 416
                      i32.add
                      local.get $p1
                      i32.const 2
                      i32.shl
                      i32.add
                      local.get $l6
                      i32.store
                      local.get $p1
                      i32.const 1
                      i32.add
                      local.set $p1
                    end
                    local.get $p4
                    i32.load16_s offset=2
                    local.set $l6
                    local.get $p4
                    i32.load16_s offset=18
                    local.set $p2
                    local.get $p4
                    i32.load16_s offset=34
                    local.set $p3
                    local.get $p4
                    i32.load16_s
                    local.set $l9
                    local.get $p4
                    i32.load16_s offset=16
                    local.set $l8
                    local.get $p4
                    i32.load16_s offset=32
                    local.set $l10
                    local.get $l5
                    local.get $l5
                    f32.load offset=140
                    f32.const 0x0p+0 (;=0;)
                    f32.mul
                    local.tee $l15
                    local.get $l5
                    f32.load offset=156
                    f32.const 0x0p+0 (;=0;)
                    f32.mul
                    local.tee $l17
                    f32.add
                    f32.const 0x1p-1 (;=0.5;)
                    f32.mul
                    f32.store offset=1468
                    local.get $l5
                    local.get $l5
                    f32.load offset=136
                    local.get $l10
                    f32.convert_i32_s
                    f32.mul
                    local.tee $l18
                    local.get $l5
                    f32.load offset=152
                    local.get $p3
                    f32.convert_i32_s
                    f32.mul
                    local.tee $l20
                    f32.add
                    f32.const 0x1p-1 (;=0.5;)
                    f32.mul
                    f32.store offset=1464
                    local.get $l5
                    local.get $l5
                    f32.load offset=132
                    local.get $l8
                    f32.convert_i32_s
                    f32.mul
                    local.tee $l16
                    local.get $l5
                    f32.load offset=148
                    local.get $p2
                    f32.convert_i32_s
                    f32.mul
                    local.tee $l14
                    f32.add
                    f32.const 0x1p-1 (;=0.5;)
                    f32.mul
                    f32.store offset=1460
                    local.get $l5
                    local.get $l5
                    f32.load offset=128
                    local.get $l9
                    f32.convert_i32_s
                    f32.mul
                    local.tee $l23
                    local.get $l5
                    f32.load offset=144
                    local.get $l6
                    f32.convert_i32_s
                    f32.mul
                    local.tee $l26
                    f32.add
                    f32.const 0x1p-1 (;=0.5;)
                    f32.mul
                    f32.store offset=1456
                    local.get $l5
                    local.get $l14
                    local.get $l16
                    f32.sub
                    f32.const 0x1p-1 (;=0.5;)
                    f32.mul
                    f32.store offset=1444
                    local.get $l5
                    local.get $l26
                    local.get $l23
                    f32.sub
                    f32.const 0x1p-1 (;=0.5;)
                    f32.mul
                    f32.store offset=1440
                    local.get $l5
                    local.get $l17
                    local.get $l15
                    f32.sub
                    f32.const 0x1p-1 (;=0.5;)
                    f32.mul
                    f32.store offset=1452
                    local.get $l5
                    local.get $l20
                    local.get $l18
                    f32.sub
                    f32.const 0x1p-1 (;=0.5;)
                    f32.mul
                    f32.store offset=1448
                    local.get $l5
                    local.get $l5
                    i64.load offset=1464
                    i64.store offset=24
                    local.get $l5
                    local.get $l5
                    i64.load offset=1456
                    i64.store offset=16
                    local.get $l5
                    local.get $l5
                    i64.load offset=1448
                    i64.store offset=8
                    local.get $l5
                    local.get $l5
                    i64.load offset=1440
                    i64.store
                    block $B71
                      local.get $l5
                      i32.const 16
                      i32.add
                      local.get $l5
                      local.get $l5
                      i32.const 128
                      i32.add
                      call $f69988
                      i32.eqz
                      br_if $B71
                      local.get $p4
                      i32.load offset=48
                      local.tee $l6
                      i32.const 1
                      i32.and
                      if $I72
                        local.get $l6
                        i32.const 5
                        i32.shr_u
                        local.set $p4
                        local.get $l6
                        i32.const 1
                        i32.shr_u
                        i32.const 15
                        i32.and
                        local.set $p2
                        loop $L73
                          block $B74 (result i32)
                            local.get $l5
                            i32.load offset=304
                            local.tee $l6
                            if $I75
                              local.get $l6
                              local.get $p4
                              i32.const 12
                              i32.mul
                              i32.add
                              local.tee $l6
                              i32.load offset=8
                              local.set $p3
                              local.get $l6
                              i32.load
                              local.set $l8
                              local.get $l6
                              i32.load offset=4
                              br $B74
                            end
                            local.get $l5
                            i32.load offset=308
                            local.get $p4
                            i32.const 6
                            i32.mul
                            i32.add
                            local.tee $l6
                            i32.load16_u offset=4
                            local.set $p3
                            local.get $l6
                            i32.load16_u
                            local.set $l8
                            local.get $l6
                            i32.load16_u offset=2
                          end
                          local.set $l9
                          local.get $l5
                          i32.load offset=312
                          local.tee $l6
                          local.get $l8
                          i32.const 12
                          i32.mul
                          i32.add
                          local.get $l6
                          local.get $l9
                          i32.const 12
                          i32.mul
                          i32.add
                          local.get $l6
                          local.get $p3
                          i32.const 12
                          i32.mul
                          i32.add
                          local.get $l5
                          i32.const 128
                          i32.add
                          call $f69991
                          i32.eqz
                          if $I76
                            local.get $p4
                            i32.const 1
                            i32.add
                            local.set $p4
                            local.get $p2
                            i32.const 1
                            i32.sub
                            local.tee $p2
                            br_if $L73
                            br $B71
                          end
                        end
                        i32.const 1
                        br $B48
                      end
                      local.get $l5
                      i32.const 416
                      i32.add
                      local.get $p1
                      i32.const 2
                      i32.shl
                      i32.add
                      local.get $l6
                      i32.store
                      local.get $p1
                      i32.const 1
                      i32.add
                      local.set $p1
                    end
                    local.get $p1
                    br_if $L52
                  end
                  br $B50
                end
                local.get $l6
                i32.load offset=12
                local.tee $p4
                i32.const 4
                i32.shr_u
                local.set $l6
                local.get $p4
                i32.const 15
                i32.and
                local.set $p2
                loop $L77
                  block $B78 (result i32)
                    local.get $l5
                    i32.load offset=304
                    local.tee $p4
                    if $I79
                      local.get $p4
                      local.get $l6
                      i32.const 12
                      i32.mul
                      i32.add
                      local.tee $p4
                      i32.load offset=8
                      local.set $p3
                      local.get $p4
                      i32.load
                      local.set $l8
                      local.get $p4
                      i32.load offset=4
                      br $B78
                    end
                    local.get $l5
                    i32.load offset=308
                    local.get $l6
                    i32.const 6
                    i32.mul
                    i32.add
                    local.tee $p4
                    i32.load16_u offset=4
                    local.set $p3
                    local.get $p4
                    i32.load16_u
                    local.set $l8
                    local.get $p4
                    i32.load16_u offset=2
                  end
                  local.set $l9
                  i32.const 1
                  local.get $l5
                  i32.load offset=312
                  local.tee $p4
                  local.get $l8
                  i32.const 12
                  i32.mul
                  i32.add
                  local.get $p4
                  local.get $l9
                  i32.const 12
                  i32.mul
                  i32.add
                  local.get $p4
                  local.get $p3
                  i32.const 12
                  i32.mul
                  i32.add
                  local.get $l5
                  i32.const 128
                  i32.add
                  call $f69991
                  br_if $B48
                  drop
                  local.get $l6
                  i32.const 1
                  i32.add
                  local.set $l6
                  local.get $p2
                  i32.const 1
                  i32.sub
                  local.tee $p2
                  br_if $L77
                end
              end
              i32.const 0
              br $B48
            end
            i32.const 1
          end
          local.set $p4
          local.get $l5
          i32.const 1472
          i32.add
          global.set $g0
          local.get $p4
          local.set $p2
        end
        local.get $p2
        i32.const 0
        i32.ne
        br $B0
      end
      local.get $p3
      f32.load offset=8
      local.set $l22
      local.get $l7
      local.get $p4
      i32.store offset=128
      local.get $l7
      local.get $l22
      local.get $l21
      local.get $l19
      f32.mul
      f32.mul
      f32.const 0x0p+0 (;=0;)
      f32.lt
      i32.store8 offset=133
      local.get $l7
      i32.const 0
      i32.store8 offset=132
      local.get $l7
      f32.const 0x1p+0 (;=1;)
      local.get $p3
      f32.load offset=12
      local.tee $l24
      local.get $l24
      local.get $l24
      f32.add
      local.tee $l27
      f32.mul
      f32.sub
      local.tee $l20
      local.get $p3
      f32.load offset=16
      local.tee $l25
      local.get $l25
      local.get $l25
      f32.add
      local.tee $l15
      f32.mul
      local.tee $l30
      f32.sub
      local.tee $l28
      local.get $l28
      local.get $l22
      f32.mul
      local.tee $l17
      f32.mul
      local.get $l27
      local.get $p3
      f32.load offset=20
      local.tee $l24
      f32.mul
      local.tee $l31
      local.get $l15
      local.get $p3
      f32.load offset=24
      local.tee $l18
      f32.mul
      local.tee $l32
      f32.add
      local.tee $l14
      local.get $l21
      local.get $l14
      f32.mul
      local.tee $l23
      f32.mul
      local.get $l15
      local.get $l24
      f32.mul
      local.tee $l16
      local.get $l27
      local.get $l18
      f32.mul
      local.tee $l29
      f32.sub
      local.tee $l15
      local.get $l19
      local.get $l15
      f32.mul
      local.tee $l26
      f32.mul
      f32.add
      f32.add
      f32.store offset=168
      local.get $l7
      local.get $l16
      local.get $l29
      f32.add
      local.tee $l16
      local.get $l17
      f32.mul
      local.get $l27
      local.get $l25
      f32.mul
      local.tee $l29
      local.get $l18
      local.get $l24
      local.get $l24
      f32.add
      local.tee $l25
      f32.mul
      local.tee $l18
      f32.sub
      local.tee $l27
      local.get $l23
      f32.mul
      local.get $l20
      local.get $l24
      local.get $l25
      f32.mul
      local.tee $l20
      f32.sub
      local.tee $l24
      local.get $l26
      f32.mul
      f32.add
      f32.add
      f32.store offset=156
      local.get $l7
      local.get $l31
      local.get $l32
      f32.sub
      local.tee $l25
      local.get $l17
      f32.mul
      f32.const 0x1p+0 (;=1;)
      local.get $l30
      f32.sub
      local.get $l20
      f32.sub
      local.tee $l17
      local.get $l23
      f32.mul
      local.get $l29
      local.get $l18
      f32.add
      local.tee $l18
      local.get $l26
      f32.mul
      f32.add
      f32.add
      f32.store offset=144
      local.get $l7
      local.get $l28
      local.get $l16
      local.get $l22
      f32.mul
      local.tee $l23
      f32.mul
      local.get $l14
      local.get $l21
      local.get $l27
      f32.mul
      local.tee $l26
      f32.mul
      local.get $l15
      local.get $l19
      local.get $l24
      f32.mul
      local.tee $l20
      f32.mul
      f32.add
      f32.add
      f32.store offset=164
      local.get $l7
      local.get $l28
      local.get $l25
      local.get $l22
      f32.mul
      local.tee $l22
      f32.mul
      local.get $l14
      local.get $l21
      local.get $l17
      f32.mul
      local.tee $l21
      f32.mul
      local.get $l15
      local.get $l19
      local.get $l18
      f32.mul
      local.tee $l19
      f32.mul
      f32.add
      f32.add
      f32.store offset=160
      local.get $l7
      local.get $l16
      local.get $l23
      f32.mul
      local.get $l27
      local.get $l26
      f32.mul
      local.get $l24
      local.get $l20
      f32.mul
      f32.add
      f32.add
      f32.store offset=152
      local.get $l7
      local.get $l16
      local.get $l22
      f32.mul
      local.get $l27
      local.get $l21
      f32.mul
      local.get $l24
      local.get $l19
      f32.mul
      f32.add
      f32.add
      f32.store offset=148
      local.get $l7
      local.get $l25
      local.get $l23
      f32.mul
      local.get $l17
      local.get $l26
      f32.mul
      local.get $l18
      local.get $l20
      f32.mul
      f32.add
      f32.add
      f32.store offset=140
      local.get $l7
      local.get $l25
      local.get $l22
      f32.mul
      local.get $l17
      local.get $l21
      f32.mul
      local.get $l18
      local.get $l19
      f32.mul
      f32.add
      f32.add
      f32.store offset=136
      local.get $l7
      local.get $p0
      f32.load offset=8
      local.get $p2
      f32.load offset=24
      local.tee $l16
      f32.sub
      local.tee $l19
      local.get $l19
      f32.add
      local.tee $l25
      local.get $p2
      f32.load offset=12
      local.tee $l19
      local.get $l19
      f32.mul
      f32.const -0x1p-1 (;=-0.5;)
      f32.add
      local.tee $l27
      f32.mul
      local.get $l19
      local.get $p0
      f32.load offset=4
      local.get $p2
      f32.load offset=20
      local.tee $l17
      f32.sub
      local.tee $l21
      local.get $l21
      f32.add
      local.tee $l28
      local.get $p2
      f32.load
      local.tee $l21
      f32.mul
      local.get $p0
      f32.load
      local.get $p2
      f32.load offset=16
      local.tee $l18
      f32.sub
      local.tee $l22
      local.get $l22
      f32.add
      local.tee $l14
      local.get $p2
      f32.load offset=4
      local.tee $l22
      f32.mul
      f32.sub
      f32.mul
      f32.sub
      local.get $p2
      f32.load offset=8
      local.tee $l24
      local.get $l14
      local.get $l21
      f32.mul
      local.get $l28
      local.get $l22
      f32.mul
      f32.add
      local.get $l25
      local.get $l24
      f32.mul
      f32.add
      local.tee $l15
      f32.mul
      f32.add
      local.tee $l23
      f32.store offset=180
      local.get $l7
      local.get $l22
      local.get $l15
      f32.mul
      local.get $l28
      local.get $l27
      f32.mul
      local.get $l19
      local.get $l14
      local.get $l24
      f32.mul
      local.get $l25
      local.get $l21
      f32.mul
      f32.sub
      f32.mul
      f32.sub
      f32.add
      local.tee $l26
      f32.store offset=176
      local.get $l7
      local.get $l21
      local.get $l15
      f32.mul
      local.get $l14
      local.get $l27
      f32.mul
      local.get $l19
      local.get $l25
      local.get $l22
      f32.mul
      local.get $l28
      local.get $l24
      f32.mul
      f32.sub
      f32.mul
      f32.sub
      f32.add
      local.tee $l20
      f32.store offset=172
      local.get $l7
      local.get $l27
      local.get $p0
      f32.load offset=20
      local.get $l16
      f32.sub
      local.tee $l25
      local.get $l25
      f32.add
      local.tee $l25
      f32.mul
      local.get $l19
      local.get $l21
      local.get $p0
      f32.load offset=16
      local.get $l17
      f32.sub
      local.tee $l28
      local.get $l28
      f32.add
      local.tee $l28
      f32.mul
      local.get $l22
      local.get $p0
      f32.load offset=12
      local.get $l18
      f32.sub
      local.tee $l14
      local.get $l14
      f32.add
      local.tee $l14
      f32.mul
      f32.sub
      f32.mul
      f32.sub
      local.get $l24
      local.get $l21
      local.get $l14
      f32.mul
      local.get $l22
      local.get $l28
      f32.mul
      f32.add
      local.get $l24
      local.get $l25
      f32.mul
      f32.add
      local.tee $l15
      f32.mul
      f32.add
      local.tee $l16
      f32.store offset=192
      local.get $l7
      local.get $l22
      local.get $l15
      f32.mul
      local.get $l27
      local.get $l28
      f32.mul
      local.get $l19
      local.get $l24
      local.get $l14
      f32.mul
      local.get $l21
      local.get $l25
      f32.mul
      f32.sub
      f32.mul
      f32.sub
      f32.add
      local.tee $l17
      f32.store offset=188
      local.get $l7
      local.get $l21
      local.get $l15
      f32.mul
      local.get $l27
      local.get $l14
      f32.mul
      local.get $l19
      local.get $l22
      local.get $l25
      f32.mul
      local.get $l24
      local.get $l28
      f32.mul
      f32.sub
      f32.mul
      f32.sub
      f32.add
      local.tee $l22
      f32.store offset=184
      local.get $p0
      f32.load offset=24
      local.set $l24
      local.get $l7
      local.get $l16
      local.get $l23
      f32.sub
      local.tee $l19
      f32.store offset=208
      local.get $l7
      local.get $l17
      local.get $l26
      f32.sub
      local.tee $l21
      f32.store offset=204
      local.get $l7
      local.get $l24
      f32.store offset=196
      local.get $l7
      local.get $l22
      local.get $l20
      f32.sub
      local.tee $l22
      f32.store offset=200
      local.get $l7
      local.get $l19
      local.get $l19
      f32.mul
      local.get $l22
      local.get $l22
      f32.mul
      local.get $l21
      local.get $l21
      f32.mul
      f32.add
      f32.add
      local.tee $l19
      f32.store offset=212
      local.get $l7
      f32.const 0x1p+0 (;=1;)
      local.get $l19
      f32.div
      f32.const 0x0p+0 (;=0;)
      local.get $l19
      f32.const 0x0p+0 (;=0;)
      f32.ne
      select
      f32.store offset=216
      local.get $l7
      local.get $p0
      call $f70388
      local.get $l7
      i32.const -64
      i32.sub
      local.get $l7
      local.get $p2
      local.get $p3
      call $f69940
      local.get $l7
      i32.const -64
      i32.sub
      local.get $p1
      i32.const 119663
      local.get $l7
      i32.const 128
      i32.add
      call $f69989
      local.get $l7
      i32.load8_u offset=132
      i32.const 0
      i32.ne
    end
    local.set $p2
    local.get $l7
    i32.const 224
    i32.add
    global.set $g0
    local.get $p2)
