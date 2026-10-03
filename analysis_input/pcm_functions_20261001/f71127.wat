  (func $f71127 (type $t4) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32)
    (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 i32) (local $l17 i32) (local $l18 i32) (local $l19 i32) (local $l20 i32) (local $l21 i32) (local $l22 i32) (local $l23 i32) (local $l24 i32) (local $l25 i32) (local $l26 i32) (local $l27 f32) (local $l28 f32)
    global.get $g0
    i32.const 1328
    i32.sub
    local.tee $l4
    global.set $g0
    block $B0
      local.get $p0
      i32.load8_u offset=488
      if $I1
        i32.const 4700888
        i32.load
        i32.const 8
        i32.const 3148550
        i32.const 1211
        i32.const 3148910
        i32.const 0
        call $f69760
        br $B0
      end
      local.get $p0
      local.get $p0
      i32.const 112
      i32.add
      local.tee $l7
      call $f71203
      local.get $p0
      i32.load offset=448
      local.set $l5
      local.get $p3
      i32.load offset=44
      i32.const 0
      local.get $p2
      local.get $p0
      i32.const 468
      i32.add
      local.tee $l6
      i32.load
      local.tee $l18
      i32.mul
      i32.const 2
      i32.shl
      call $f484
      local.set $l19
      local.get $p0
      i32.load offset=476
      i32.load8_u
      local.set $l11
      local.get $p3
      i32.load offset=56
      local.set $l8
      local.get $l4
      i32.const 1320
      i32.add
      i32.const 0
      i32.store
      local.get $l4
      i32.const 1312
      i32.add
      i64.const 0
      i64.store
      local.get $l4
      i32.const 1304
      i32.add
      i64.const 0
      i64.store
      local.get $l4
      i32.const 1296
      i32.add
      i64.const 0
      i64.store
      local.get $l4
      i32.const 1288
      i32.add
      i64.const 0
      i64.store
      local.get $l4
      i64.const 0
      i64.store offset=1280
      local.get $l8
      local.get $l5
      local.get $l4
      i32.const 1280
      i32.add
      call $f71033
      local.set $l20
      local.get $l4
      i32.load offset=1292
      local.set $l14
      local.get $l8
      i32.load
      drop
      local.get $l6
      i32.load
      local.tee $l12
      i32.const 3
      i32.shl
      i32.const 15
      i32.add
      i32.const -16
      i32.and
      local.tee $l6
      local.get $l8
      i32.load offset=4
      local.tee $l9
      local.get $l8
      i32.load offset=8
      local.tee $p3
      i32.const 2
      i32.shl
      i32.add
      i32.const 4
      i32.sub
      i32.load
      local.tee $l5
      local.get $l8
      i32.load offset=16
      i32.sub
      i32.le_s
      if $I2
        local.get $l4
        local.get $l5
        local.get $l6
        i32.sub
        local.tee $l5
        i32.store offset=320
        block $B3
          local.get $p3
          local.get $l8
          i32.load offset=12
          i32.const 2147483647
          i32.and
          i32.ge_u
          if $I4
            local.get $l8
            i32.const 4
            i32.add
            local.get $l4
            i32.const 320
            i32.add
            call $f72370
            br $B3
          end
          local.get $l9
          local.get $p3
          i32.const 2
          i32.shl
          i32.add
          local.get $l5
          i32.store
          local.get $l8
          local.get $l8
          i32.load offset=8
          i32.const 1
          i32.add
          i32.store offset=8
        end
        local.get $l4
        i32.load offset=320
        local.set $l15
      end
      local.get $l8
      i32.load
      drop
      local.get $p2
      i32.eqz
      br_if $B0
      local.get $l11
      i32.const 1
      i32.and
      local.set $l13
      local.get $l15
      local.get $l12
      i32.const 2
      i32.shl
      local.tee $l21
      i32.add
      local.set $l11
      f32.const 0x1p+0 (;=1;)
      local.get $p0
      f32.load offset=464
      f32.div
      local.set $l28
      local.get $l12
      i32.const -4
      i32.and
      local.set $l22
      local.get $l12
      i32.const 3
      i32.and
      local.set $l23
      local.get $l12
      i32.const 1
      i32.sub
      i32.const 3
      i32.lt_u
      local.set $l24
      loop $L5
        local.get $p1
        local.get $l16
        i32.const 12
        i32.mul
        i32.add
        local.tee $l10
        i32.load offset=8
        local.set $p3
        local.get $l4
        i32.const 320
        i32.add
        i32.const 0
        i32.const 960
        call $f484
        drop
        local.get $l4
        i32.const 2139095039
        i32.store offset=1260
        local.get $l4
        i32.const -8388609
        i32.store offset=1244
        local.get $l4
        i32.const 2139095039
        i32.store offset=1180
        local.get $l4
        i32.const -8388609
        i32.store offset=1164
        local.get $l4
        i32.const 2139095039
        i32.store offset=1100
        local.get $l4
        i32.const -8388609
        i32.store offset=1084
        local.get $l4
        i32.const 2139095039
        i32.store offset=1020
        local.get $l4
        i32.const -8388609
        i32.store offset=1004
        local.get $l4
        i32.const 2139095039
        i32.store offset=940
        local.get $l4
        i32.const -8388609
        i32.store offset=924
        local.get $l4
        i32.const 2139095039
        i32.store offset=860
        local.get $l4
        i32.const -8388609
        i32.store offset=844
        local.get $l4
        i32.const 2139095039
        i32.store offset=780
        local.get $l4
        i32.const -8388609
        i32.store offset=764
        local.get $l4
        i32.const 2139095039
        i32.store offset=700
        local.get $l4
        i32.const -8388609
        i32.store offset=684
        local.get $l4
        i32.const 2139095039
        i32.store offset=620
        local.get $l4
        i32.const -8388609
        i32.store offset=604
        local.get $l4
        i32.const 2139095039
        i32.store offset=540
        local.get $l4
        i32.const -8388609
        i32.store offset=524
        local.get $l4
        i32.const 2139095039
        i32.store offset=460
        local.get $l4
        i32.const -8388609
        i32.store offset=444
        local.get $l4
        i32.const 2139095039
        i32.store offset=380
        local.get $l4
        i32.const -8388609
        i32.store offset=364
        local.get $l4
        block $B6 (result f32)
          local.get $p3
          i32.load offset=24
          if $I7
            local.get $l4
            local.get $p3
            i32.load offset=32
            local.tee $l5
            f32.load
            f32.store offset=288
            local.get $l4
            local.get $l5
            f32.load offset=4
            f32.store offset=292
            local.get $l4
            local.get $l5
            f32.load offset=8
            f32.store offset=296
            local.get $l4
            local.get $l5
            f32.load offset=12
            f32.store offset=300
            local.get $l4
            local.get $l5
            f32.load offset=16
            f32.store offset=304
            local.get $l4
            local.get $l5
            f32.load offset=20
            f32.store offset=308
            local.get $l5
            f32.load offset=24
            br $B6
          end
          local.get $l4
          i64.const 0
          i64.store offset=304
          local.get $l4
          i64.const 4575657221408423936
          i64.store offset=296
          local.get $l4
          i64.const 0
          i64.store offset=288
          f32.const 0x0p+0 (;=0;)
        end
        f32.store offset=312
        local.get $l4
        block $B8 (result f32)
          local.get $p3
          i32.load offset=28
          if $I9
            local.get $l4
            local.get $p3
            i32.load offset=36
            local.tee $l5
            f32.load
            f32.store offset=256
            local.get $l4
            local.get $l5
            f32.load offset=4
            f32.store offset=260
            local.get $l4
            local.get $l5
            f32.load offset=8
            f32.store offset=264
            local.get $l4
            local.get $l5
            f32.load offset=12
            f32.store offset=268
            local.get $l4
            local.get $l5
            f32.load offset=16
            f32.store offset=272
            local.get $l4
            local.get $l5
            f32.load offset=20
            f32.store offset=276
            local.get $l5
            f32.load offset=24
            br $B8
          end
          local.get $l4
          i64.const 0
          i64.store offset=272
          local.get $l4
          i64.const 4575657221408423936
          i64.store offset=264
          local.get $l4
          i64.const 0
          i64.store offset=256
          f32.const 0x0p+0 (;=0;)
        end
        f32.store offset=280
        i32.const 0
        local.set $l6
        local.get $l4
        i32.const 0
        i32.store offset=248
        local.get $l4
        i64.const 0
        i64.store offset=240
        local.get $l4
        i32.const 320
        i32.add
        local.get $l4
        i32.const 240
        i32.add
        i32.const 12
        local.get $l4
        i32.const 192
        i32.add
        local.get $p3
        i32.load offset=20
        local.get $l4
        i32.const 288
        i32.add
        local.get $l4
        i32.const 256
        i32.add
        local.get $p3
        i32.load16_u offset=10
        i32.const 512
        i32.and
        i32.const 9
        i32.shr_u
        local.get $l4
        i32.const 224
        i32.add
        local.get $l4
        i32.const 208
        i32.add
        local.get $p3
        i32.load offset=12
        call_indirect $__indirect_function_table (type $t32)
        local.set $l17
        local.get $l10
        i32.load
        local.set $l9
        local.get $l10
        i32.load offset=4
        local.set $l10
        local.get $l15
        i32.const 0
        local.get $l21
        call $f484
        local.set $l5
        local.get $l17
        if $I10
          local.get $l9
          i32.const -2147483648
          i32.ne
          local.tee $l25
          local.get $l10
          i32.const -2147483648
          i32.ne
          i32.and
          local.set $l26
          loop $L11
            local.get $l4
            i32.const 320
            i32.add
            local.get $l6
            i32.const 80
            i32.mul
            i32.add
            local.set $p3
            block $B12
              local.get $l26
              if $I13
                local.get $l4
                local.get $p3
                f32.load
                f32.store offset=160
                local.get $l4
                local.get $p3
                f32.load offset=4
                f32.store offset=164
                local.get $p3
                f32.load offset=8
                local.set $l27
                local.get $l4
                i32.const 0
                i32.store offset=172
                local.get $l4
                local.get $l27
                f32.store offset=168
                local.get $l4
                local.get $p3
                f32.load offset=16
                f32.store offset=176
                local.get $l4
                local.get $p3
                f32.load offset=20
                f32.store offset=180
                local.get $p3
                f32.load offset=24
                local.set $l27
                local.get $l4
                i32.const 0
                i32.store offset=188
                local.get $l4
                local.get $l27
                f32.store offset=184
                local.get $l4
                local.get $p3
                f32.load offset=32
                f32.store offset=128
                local.get $l4
                local.get $p3
                f32.load offset=36
                f32.store offset=132
                local.get $p3
                f32.load offset=40
                local.set $l27
                local.get $l4
                i32.const 0
                i32.store offset=140
                local.get $l4
                local.get $l27
                f32.store offset=136
                local.get $l4
                local.get $p3
                f32.load offset=48
                f32.store offset=144
                local.get $l4
                local.get $p3
                f32.load offset=52
                f32.store offset=148
                local.get $p3
                f32.load offset=56
                local.set $l27
                local.get $l4
                i32.const 0
                i32.store offset=156
                local.get $l4
                local.get $l27
                f32.store offset=152
                local.get $l9
                local.get $l10
                i32.gt_u
                if $I14
                  local.get $p0
                  local.get $l13
                  local.get $l10
                  local.get $l9
                  local.get $l14
                  local.get $l4
                  i32.const 128
                  i32.add
                  local.get $l4
                  i32.const 160
                  i32.add
                  local.get $l4
                  i32.const -64
                  i32.sub
                  local.get $l4
                  i32.const 96
                  i32.add
                  local.get $l5
                  call $f71125
                  br $B12
                end
                local.get $p0
                local.get $l13
                local.get $l9
                local.get $l10
                local.get $l14
                local.get $l4
                i32.const 160
                i32.add
                local.get $l4
                i32.const 128
                i32.add
                local.get $l4
                i32.const 96
                i32.add
                local.get $l4
                i32.const -64
                i32.sub
                local.get $l5
                call $f71125
                br $B12
              end
              local.get $l25
              i32.eqz
              if $I15
                local.get $l4
                local.get $p3
                f32.load offset=32
                f32.store offset=160
                local.get $l4
                local.get $p3
                f32.load offset=36
                f32.store offset=164
                local.get $p3
                f32.load offset=40
                local.set $l27
                local.get $l4
                i32.const 0
                i32.store offset=172
                local.get $l4
                local.get $l27
                f32.store offset=168
                local.get $l4
                local.get $p3
                f32.load offset=48
                f32.store offset=176
                local.get $l4
                local.get $p3
                f32.load offset=52
                f32.store offset=180
                local.get $p3
                f32.load offset=56
                local.set $l27
                local.get $l4
                i32.const 0
                i32.store offset=188
                local.get $l4
                local.get $l27
                f32.store offset=184
                local.get $l4
                i32.const 32
                i32.add
                local.get $p0
                local.get $l13
                local.get $l10
                local.get $l14
                local.get $l4
                i32.const 160
                i32.add
                local.get $l5
                call $f71126
                br $B12
              end
              local.get $l4
              local.get $p3
              f32.load
              f32.store offset=160
              local.get $l4
              local.get $p3
              f32.load offset=4
              f32.store offset=164
              local.get $p3
              f32.load offset=8
              local.set $l27
              local.get $l4
              i32.const 0
              i32.store offset=172
              local.get $l4
              local.get $l27
              f32.store offset=168
              local.get $l4
              local.get $p3
              f32.load offset=16
              f32.store offset=176
              local.get $l4
              local.get $p3
              f32.load offset=20
              f32.store offset=180
              local.get $p3
              f32.load offset=24
              local.set $l27
              local.get $l4
              i32.const 0
              i32.store offset=188
              local.get $l4
              local.get $l27
              f32.store offset=184
              local.get $l4
              local.get $p0
              local.get $l13
              local.get $l9
              local.get $l14
              local.get $l4
              i32.const 160
              i32.add
              local.get $l5
              call $f71126
            end
            local.get $l6
            i32.const 1
            i32.add
            local.tee $l6
            local.get $l17
            i32.ne
            br_if $L11
          end
        end
        block $B16
          local.get $l12
          i32.eqz
          br_if $B16
          i32.const 0
          local.set $p3
          local.get $l22
          local.set $l9
          local.get $l24
          i32.eqz
          if $I17
            loop $L18
              local.get $l11
              local.get $p3
              i32.const 2
              i32.shl
              local.tee $l6
              i32.add
              local.get $l28
              local.get $l5
              local.get $l6
              i32.add
              f32.load
              f32.mul
              f32.store
              local.get $l11
              local.get $l6
              i32.const 4
              i32.or
              local.tee $l10
              i32.add
              local.get $l28
              local.get $l5
              local.get $l10
              i32.add
              f32.load
              f32.mul
              f32.store
              local.get $l11
              local.get $l6
              i32.const 8
              i32.or
              local.tee $l10
              i32.add
              local.get $l28
              local.get $l5
              local.get $l10
              i32.add
              f32.load
              f32.mul
              f32.store
              local.get $l11
              local.get $l6
              i32.const 12
              i32.or
              local.tee $l6
              i32.add
              local.get $l28
              local.get $l5
              local.get $l6
              i32.add
              f32.load
              f32.mul
              f32.store
              local.get $p3
              i32.const 4
              i32.add
              local.set $p3
              local.get $l9
              i32.const 4
              i32.sub
              local.tee $l9
              br_if $L18
            end
          end
          local.get $l23
          local.tee $l6
          i32.eqz
          br_if $B16
          loop $L19
            local.get $l11
            local.get $p3
            i32.const 2
            i32.shl
            local.tee $l9
            i32.add
            local.get $l28
            local.get $l5
            local.get $l9
            i32.add
            f32.load
            f32.mul
            f32.store
            local.get $p3
            i32.const 1
            i32.add
            local.set $p3
            local.get $l6
            i32.const 1
            i32.sub
            local.tee $l6
            br_if $L19
          end
        end
        local.get $l7
        call $f71017
        local.get $l4
        local.get $l11
        i32.store offset=1308
        local.get $l4
        i32.const 0
        i32.store offset=1296
        local.get $l4
        i32.const 0
        i32.store offset=1304
        local.get $l4
        local.get $l19
        local.get $l16
        local.get $l18
        i32.mul
        i32.const 2
        i32.shl
        i32.add
        i32.store offset=1312
        block $B20
          local.get $l13
          if $I21
            local.get $l4
            i32.const 0
            i32.store offset=168
            local.get $l4
            i64.const 0
            i64.store offset=160
            local.get $l7
            local.get $l4
            i32.const 1280
            i32.add
            call $f71022
            local.get $l4
            i32.load offset=1288
            i32.const 0
            local.get $p0
            i32.load offset=448
            i32.const 5
            i32.shl
            call $f484
            drop
            local.get $l7
            local.get $l4
            i32.const 160
            i32.add
            local.get $l4
            i32.const 1280
            i32.add
            call $f71018
            local.get $l7
            local.get $l4
            i32.const 1280
            i32.add
            call $f71110
            local.get $l7
            local.get $l4
            i32.const 1280
            i32.add
            call $f71112
            local.get $l7
            local.get $l4
            i32.const 1280
            i32.add
            call $f71111
            br $B20
          end
          local.get $l4
          i32.const 0
          i32.store offset=168
          local.get $l4
          i64.const 0
          i64.store offset=160
          local.get $l7
          local.get $l4
          i32.const 1280
          i32.add
          call $f71022
          local.get $l4
          i32.load offset=1288
          i32.const 0
          local.get $p0
          i32.load offset=448
          i32.const 5
          i32.shl
          call $f484
          drop
          local.get $l7
          local.get $l4
          i32.const 160
          i32.add
          local.get $l4
          i32.const 1280
          i32.add
          call $f71018
          local.get $l7
          local.get $l4
          i32.const 1280
          i32.add
          call $f71110
          local.get $l7
          local.get $l4
          i32.const 1280
          i32.add
          call $f71112
          local.get $l7
          local.get $l4
          i32.const 1280
          i32.add
          call $f71114
          local.get $l7
          local.get $l4
          i32.const 1280
          i32.add
          call $f71115
        end
        local.get $l8
        local.get $l5
        call $f71715
        local.get $l8
        local.get $l20
        call $f71715
        local.get $l16
        i32.const 1
        i32.add
        local.tee $l16
        local.get $p2
        i32.ne
        br_if $L5
      end
    end
    local.get $l4
    i32.const 1328
    i32.add
    global.set $g0)
