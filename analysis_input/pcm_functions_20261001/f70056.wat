  (func $f70056 (type $t6) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32)
    (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 i32) (local $l17 i32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32) (local $l33 f32) (local $l34 f32) (local $l35 f32) (local $l36 f32) (local $l37 f32) (local $l38 f32) (local $l39 f32) (local $l40 f32) (local $l41 i64)
    global.get $g0
    i32.const 224
    i32.sub
    local.tee $l5
    global.set $g0
    local.get $l5
    i64.const 1065353216
    i64.store offset=216
    local.get $l5
    i64.const 0
    i64.store offset=208
    local.get $l5
    i64.const 0
    i64.store offset=200
    local.get $l5
    i32.const 1065353216
    i32.store offset=196
    local.get $l5
    i64.const 0
    i64.store offset=180 align=4
    local.get $l5
    i32.const 1065353216
    i32.store offset=176
    local.get $l5
    i64.const 0
    i64.store offset=188 align=4
    block $B0
      local.get $p0
      i32.const 4408
      i32.add
      f32.load
      local.get $p1
      f32.load offset=12
      local.tee $l33
      local.get $p1
      f32.load
      local.tee $l29
      f32.sub
      local.tee $l22
      local.get $p1
      f32.load offset=28
      local.tee $l34
      local.get $p1
      f32.load offset=4
      local.tee $l35
      f32.sub
      local.tee $l23
      f32.mul
      local.get $p1
      f32.load offset=16
      local.tee $l36
      local.get $l35
      f32.sub
      local.tee $l24
      local.get $p1
      f32.load offset=24
      local.tee $l37
      local.get $l29
      f32.sub
      local.tee $l30
      f32.mul
      f32.sub
      local.tee $l28
      f32.const 0x1p+0 (;=1;)
      local.get $l28
      local.get $l28
      f32.mul
      local.get $l24
      local.get $p1
      f32.load offset=32
      local.tee $l18
      local.get $p1
      f32.load offset=8
      local.tee $l28
      f32.sub
      local.tee $l19
      f32.mul
      local.get $p1
      f32.load offset=20
      local.tee $l20
      local.get $l28
      f32.sub
      local.tee $l24
      local.get $l23
      f32.mul
      f32.sub
      local.tee $l23
      local.get $l23
      f32.mul
      local.get $l24
      local.get $l30
      f32.mul
      local.get $l22
      local.get $l19
      f32.mul
      f32.sub
      local.tee $l22
      local.get $l22
      f32.mul
      f32.add
      f32.add
      f32.sqrt
      f32.div
      local.tee $l24
      f32.mul
      local.tee $l30
      f32.mul
      local.get $p0
      f32.load offset=4400
      local.get $l23
      local.get $l24
      f32.mul
      local.tee $l23
      f32.mul
      local.get $p0
      i32.const 4404
      i32.add
      f32.load
      local.get $l22
      local.get $l24
      f32.mul
      local.tee $l22
      f32.mul
      f32.add
      f32.add
      local.get $l28
      local.get $l30
      f32.mul
      local.get $l29
      local.get $l23
      f32.mul
      local.get $l35
      local.get $l22
      f32.mul
      f32.add
      f32.add
      f32.sub
      f32.const 0x0p+0 (;=0;)
      f32.lt
      br_if $B0
      local.get $p0
      i32.const 2304
      i32.add
      f32.load
      local.set $l23
      local.get $p0
      i32.const 2288
      i32.add
      f32.load
      local.set $l22
      local.get $p0
      i32.const 2272
      i32.add
      f32.load
      local.set $l24
      local.get $p0
      i32.const 2308
      i32.add
      f32.load
      local.set $l30
      local.get $p0
      i32.const 2292
      i32.add
      f32.load
      local.set $l19
      local.get $p0
      i32.const 2260
      i32.add
      f32.load
      local.set $l21
      local.get $p0
      i32.const 2276
      i32.add
      f32.load
      local.set $l25
      local.get $p0
      i32.const 2312
      i32.add
      f32.load
      local.set $l26
      local.get $p0
      i32.const 2296
      i32.add
      f32.load
      local.set $l27
      local.get $p0
      i32.const 2264
      i32.add
      f32.load
      local.set $l31
      local.get $p0
      i32.const 2280
      i32.add
      f32.load
      local.set $l32
      local.get $p0
      f32.load offset=2256
      local.set $l38
      local.get $l5
      i32.const 0
      i32.store offset=172
      local.get $l5
      i32.const 0
      i32.store offset=156
      local.get $l5
      i32.const 0
      i32.store offset=140
      local.get $l5
      local.get $l26
      local.get $l37
      local.get $l31
      f32.mul
      local.get $l34
      local.get $l32
      f32.mul
      f32.add
      local.get $l18
      local.get $l27
      f32.mul
      f32.add
      f32.add
      local.tee $l39
      f32.store offset=168
      local.get $l5
      local.get $l30
      local.get $l37
      local.get $l21
      f32.mul
      local.get $l34
      local.get $l25
      f32.mul
      f32.add
      local.get $l18
      local.get $l19
      f32.mul
      f32.add
      f32.add
      local.tee $l40
      f32.store offset=164
      local.get $l5
      local.get $l23
      local.get $l37
      local.get $l38
      f32.mul
      local.get $l34
      local.get $l24
      f32.mul
      f32.add
      local.get $l18
      local.get $l22
      f32.mul
      f32.add
      f32.add
      local.tee $l34
      f32.store offset=160
      local.get $l5
      local.get $l26
      local.get $l33
      local.get $l31
      f32.mul
      local.get $l36
      local.get $l32
      f32.mul
      f32.add
      local.get $l20
      local.get $l27
      f32.mul
      f32.add
      f32.add
      local.tee $l37
      f32.store offset=152
      local.get $l5
      local.get $l30
      local.get $l33
      local.get $l21
      f32.mul
      local.get $l36
      local.get $l25
      f32.mul
      f32.add
      local.get $l20
      local.get $l19
      f32.mul
      f32.add
      f32.add
      local.tee $l18
      f32.store offset=148
      local.get $l5
      local.get $l23
      local.get $l33
      local.get $l38
      f32.mul
      local.get $l36
      local.get $l24
      f32.mul
      f32.add
      local.get $l20
      local.get $l22
      f32.mul
      f32.add
      f32.add
      local.tee $l33
      f32.store offset=144
      local.get $l5
      local.get $l26
      local.get $l29
      local.get $l31
      f32.mul
      local.get $l35
      local.get $l32
      f32.mul
      f32.add
      local.get $l28
      local.get $l27
      f32.mul
      f32.add
      f32.add
      local.tee $l36
      f32.store offset=136
      local.get $l5
      local.get $l30
      local.get $l29
      local.get $l21
      f32.mul
      local.get $l35
      local.get $l25
      f32.mul
      f32.add
      local.get $l28
      local.get $l19
      f32.mul
      f32.add
      f32.add
      local.tee $l20
      f32.store offset=132
      local.get $l5
      i32.const 0
      i32.store8 offset=112
      local.get $l5
      i64.const 23613931519
      i64.store offset=104
      local.get $l5
      i32.const 0
      i32.store offset=92
      local.get $l5
      i64.const 9187343235540844544
      i64.store offset=96
      local.get $l5
      local.get $l39
      local.get $l36
      local.get $l37
      f32.add
      f32.add
      f32.const 0x1.55553ep-2 (;=0.333333;)
      f32.mul
      f32.store offset=88
      local.get $l5
      local.get $l40
      local.get $l20
      local.get $l18
      f32.add
      f32.add
      f32.const 0x1.55553ep-2 (;=0.333333;)
      f32.mul
      f32.store offset=84
      local.get $l5
      local.get $l23
      local.get $l29
      local.get $l38
      f32.mul
      local.get $l35
      local.get $l24
      f32.mul
      f32.add
      local.get $l28
      local.get $l22
      f32.mul
      f32.add
      f32.add
      local.tee $l29
      f32.store offset=128
      local.get $l5
      local.get $l34
      local.get $l29
      local.get $l33
      f32.add
      f32.add
      f32.const 0x1.55553ep-2 (;=0.333333;)
      f32.mul
      f32.store offset=80
      local.get $p0
      i32.load offset=2208
      local.set $p1
      local.get $l5
      i32.const 1
      i32.store8 offset=60
      local.get $l5
      local.get $p1
      i32.store offset=48
      local.get $l5
      i32.const 3124664
      i32.store offset=16
      local.get $l5
      local.get $l5
      i32.const 176
      i32.add
      i32.store offset=56
      local.get $l5
      local.get $l5
      i32.const 176
      i32.add
      i32.store offset=52
      local.get $l5
      local.get $l5
      i32.const 80
      i32.add
      i32.store offset=64
      local.get $p0
      i32.load offset=2324
      local.set $l17
      local.get $p4
      local.set $l14
      local.get $p3
      local.set $p1
      local.get $p0
      i32.load offset=4416
      local.set $l7
      local.get $l5
      i32.const 16
      i32.add
      local.set $l10
      local.get $p0
      i32.load offset=4420
      local.set $l12
      local.get $p0
      i32.load offset=2320
      local.set $l8
      local.get $p0
      i32.const 2324
      i32.add
      local.set $l13
      local.get $l5
      local.set $l11
      global.get $g0
      i32.const 96
      i32.sub
      local.tee $l6
      global.set $g0
      local.get $l6
      i32.const 0
      i32.store offset=92
      local.get $l6
      i32.const 2139095039
      i32.store offset=64
      local.get $l6
      i64.const 0
      i64.store offset=56
      local.get $l6
      i64.const 0
      i64.store offset=48
      local.get $l5
      i32.const 80
      i32.add
      local.tee $l9
      local.get $l12
      local.get $p0
      i32.const 2176
      i32.add
      local.tee $l15
      local.get $l6
      i32.const -64
      i32.sub
      local.get $l6
      i32.const 44
      i32.add
      local.get $l6
      i32.const 48
      i32.add
      local.get $l6
      i32.const 92
      i32.add
      call $f70057
      if $I1
        block $B2
          local.get $l7
          local.get $l10
          local.get $l12
          local.get $l15
          local.get $l6
          i32.const -64
          i32.sub
          local.get $l6
          i32.const 40
          i32.add
          local.get $l6
          i32.const 48
          i32.add
          local.get $l6
          i32.const 92
          i32.add
          call $f70058
          i32.eqz
          br_if $B2
          local.get $l9
          local.get $p1
          local.get $l7
          local.get $l10
          local.get $l12
          local.get $l15
          local.get $l6
          i32.const -64
          i32.sub
          local.get $l6
          i32.const 48
          i32.add
          local.get $l6
          i32.const 92
          i32.add
          call $f70059
          i32.eqz
          br_if $B2
          local.get $l9
          f32.load offset=80
          local.set $l20
          local.get $l9
          i32.const -64
          i32.sub
          f32.load
          local.set $l25
          local.get $l9
          f32.load offset=68
          local.set $l26
          local.get $l9
          f32.load offset=88
          local.set $l31
          local.get $l9
          f32.load offset=56
          local.set $l18
          local.get $l9
          f32.load offset=72
          local.set $l32
          local.get $l9
          f32.load offset=84
          local.set $l27
          local.get $l9
          f32.load offset=52
          local.set $l19
          local.get $l9
          f32.load offset=48
          local.set $l21
          local.get $l6
          i32.const 0
          i32.store offset=28
          local.get $l6
          local.get $l25
          local.get $l21
          f32.sub
          local.tee $l25
          local.get $l27
          local.get $l19
          f32.sub
          local.tee $l27
          f32.mul
          local.get $l26
          local.get $l19
          f32.sub
          local.tee $l26
          local.get $l20
          local.get $l21
          f32.sub
          local.tee $l21
          f32.mul
          f32.sub
          local.tee $l19
          f32.const 0x1p+0 (;=1;)
          local.get $l19
          local.get $l19
          f32.mul
          local.get $l26
          local.get $l31
          local.get $l18
          f32.sub
          local.tee $l19
          f32.mul
          local.get $l32
          local.get $l18
          f32.sub
          local.tee $l20
          local.get $l27
          f32.mul
          f32.sub
          local.tee $l18
          local.get $l18
          f32.mul
          local.get $l20
          local.get $l21
          f32.mul
          local.get $l25
          local.get $l19
          f32.mul
          f32.sub
          local.tee $l19
          local.get $l19
          f32.mul
          f32.add
          f32.add
          f32.sqrt
          f32.div
          local.tee $l21
          f32.mul
          local.tee $l20
          f32.store offset=24
          local.get $l6
          local.get $l19
          local.get $l21
          f32.mul
          local.tee $l19
          f32.store offset=20
          local.get $l6
          local.get $l18
          local.get $l21
          f32.mul
          local.tee $l18
          f32.store offset=16
          block $B3
            block $B4
              block $B5
                block $B6
                  local.get $l6
                  i32.load offset=92
                  br_table $B6 $B5 $B4
                end
                local.get $l7
                i32.load offset=24
                local.set $l10
                local.get $l7
                local.get $l12
                local.get $l6
                i32.const 48
                i32.add
                call $f70060
                local.set $p1
                local.get $l11
                local.get $l6
                i64.load offset=24
                i64.store offset=8
                local.get $l11
                local.get $l6
                i64.load offset=16
                i64.store
                local.get $l9
                local.get $p2
                local.get $l7
                local.get $l10
                local.get $p1
                i32.const 20
                i32.mul
                i32.add
                local.get $l12
                local.get $l8
                local.get $l13
                local.get $l15
                local.get $l6
                i32.const 16
                i32.add
                local.get $p0
                i32.load offset=3624
                call $f70061
                br $B3
              end
              local.get $l6
              i32.load offset=40
              local.set $l10
              local.get $l19
              local.get $l6
              f32.load offset=52
              f32.neg
              f32.mul
              local.get $l18
              local.get $l6
              f32.load offset=48
              f32.mul
              f32.sub
              local.get $l20
              local.get $l6
              f32.load offset=56
              f32.mul
              f32.sub
              f32.const 0x1.6a09e6p-1 (;=0.707107;)
              f32.gt
              i32.eqz
              if $I7
                local.get $p1
                i32.const 7
                i32.and
                if $I8
                  local.get $p0
                  i32.load8_u offset=4429
                  i32.eqz
                  br_if $B3
                end
                block $B9
                  local.get $p0
                  i32.load offset=3620
                  local.tee $l7
                  i32.load offset=4364
                  i32.const 2147483647
                  i32.and
                  local.tee $l11
                  local.get $l7
                  i32.load offset=4360
                  local.tee $l12
                  i32.const 15
                  i32.add
                  local.tee $l15
                  i32.ge_u
                  br_if $B9
                  local.get $l11
                  local.get $l12
                  i32.const 1
                  i32.shl
                  i32.const 32
                  i32.add
                  local.tee $l16
                  i32.ge_u
                  br_if $B9
                  local.get $l7
                  local.get $l16
                  call $f70062
                  local.get $p0
                  i32.load offset=3620
                  local.tee $l7
                  i32.load offset=4360
                  local.set $l12
                end
                local.get $l7
                local.get $l15
                i32.store offset=4360
                local.get $l7
                i32.load offset=4356
                local.get $l12
                i32.const 2
                i32.shl
                i32.add
                local.tee $l7
                local.get $p1
                i32.store8 offset=56
                local.get $l7
                local.get $l10
                i32.store offset=52
                local.get $l7
                local.get $p2
                i32.store offset=48
                local.get $l7
                local.get $l14
                i32.load
                i32.store offset=36
                local.get $l7
                local.get $l14
                i32.load offset=4
                i32.store offset=40
                local.get $l7
                local.get $l14
                i32.load offset=8
                i32.store offset=44
                local.get $l9
                i64.load offset=48
                local.set $l41
                local.get $l7
                local.get $l9
                f32.load offset=56
                f32.store offset=8
                local.get $l7
                local.get $l41
                i64.store align=4
                local.get $l9
                f32.load offset=72
                local.set $l18
                local.get $l7
                local.get $l9
                i64.load offset=64
                i64.store offset=12 align=4
                local.get $l7
                local.get $l18
                f32.store offset=20
                local.get $l9
                f32.load offset=88
                local.set $l18
                local.get $l7
                local.get $l9
                i64.load offset=80
                i64.store offset=24 align=4
                local.get $l7
                local.get $l18
                f32.store offset=32
                br $B3
              end
              local.get $l7
              i32.load offset=24
              local.set $l14
              local.get $l11
              local.get $l6
              i64.load offset=24
              i64.store offset=8
              local.get $l11
              local.get $l6
              i64.load offset=16
              i64.store
              local.get $l9
              local.get $p2
              local.get $l7
              local.get $l14
              local.get $l10
              i32.const 20
              i32.mul
              i32.add
              local.get $l12
              local.get $l8
              local.get $l13
              local.get $l15
              local.get $l6
              i32.const 16
              i32.add
              local.get $p0
              i32.load offset=3624
              call $f70061
              br $B3
            end
            local.get $l7
            local.get $l12
            local.get $l6
            i32.const 48
            i32.add
            call $f70060
            local.set $l14
            local.get $l12
            i32.load offset=40
            local.tee $l10
            f32.load offset=36
            local.set $l25
            local.get $l10
            f32.load offset=40
            local.set $l26
            local.get $l7
            i32.load offset=24
            local.get $l14
            i32.const 20
            i32.mul
            i32.add
            local.tee $l16
            f32.load
            local.set $l18
            local.get $l16
            f32.load offset=4
            local.set $l19
            local.get $l10
            f32.load offset=20
            local.set $l31
            local.get $l16
            f32.load offset=8
            local.set $l21
            local.get $l10
            f32.load offset=24
            local.set $l32
            local.get $l10
            f32.load offset=32
            local.set $l27
            local.get $l10
            f32.load offset=8
            local.set $l20
            local.get $l10
            f32.load
            local.set $l38
            local.get $l10
            f32.load offset=4
            local.set $l39
            local.get $l10
            f32.load offset=16
            local.set $l40
            local.get $l6
            i32.const 0
            i32.store offset=12
            local.get $l6
            local.get $l18
            local.get $l38
            f32.mul
            local.get $l19
            local.get $l39
            f32.mul
            f32.add
            local.get $l21
            local.get $l20
            f32.mul
            f32.add
            local.tee $l20
            f32.const 0x1p+0 (;=1;)
            local.get $l20
            local.get $l20
            f32.mul
            local.get $l18
            local.get $l40
            f32.mul
            local.get $l19
            local.get $l31
            f32.mul
            f32.add
            local.get $l21
            local.get $l32
            f32.mul
            f32.add
            local.tee $l20
            local.get $l20
            f32.mul
            f32.add
            local.get $l18
            local.get $l27
            f32.mul
            local.get $l19
            local.get $l25
            f32.mul
            f32.add
            local.get $l21
            local.get $l26
            f32.mul
            f32.add
            local.tee $l18
            local.get $l18
            f32.mul
            f32.add
            f32.sqrt
            f32.div
            local.tee $l19
            f32.mul
            local.tee $l21
            f32.store
            local.get $l6
            local.get $l20
            local.get $l19
            f32.mul
            local.tee $l20
            f32.store offset=4
            local.get $l6
            local.get $l18
            local.get $l19
            f32.mul
            local.tee $l18
            f32.store offset=8
            local.get $l11
            i32.const 0
            i32.store offset=12
            local.get $l11
            local.get $l18
            f32.neg
            f32.store offset=8
            local.get $l11
            local.get $l20
            f32.neg
            f32.store offset=4
            local.get $l11
            local.get $l21
            f32.neg
            f32.store
            local.get $l7
            local.get $l16
            local.get $l9
            local.get $p2
            local.get $l12
            local.get $l8
            local.get $l13
            local.get $l15
            local.get $l6
            local.get $p0
            i32.load offset=3624
            call $f70055
          end
        end
      end
      local.get $l6
      i32.const 96
      i32.add
      global.set $g0
      local.get $p0
      i32.load offset=2324
      local.get $l17
      i32.le_u
      br_if $B0
      local.get $p3
      i32.const 16
      i32.and
      local.set $l11
      block $B10
        local.get $p3
        i32.const 8
        i32.and
        br_if $B10
        local.get $p0
        i32.const 3616
        i32.add
        i32.load
        local.tee $l14
        i32.const 128
        i32.eq
        br_if $B10
        local.get $p0
        local.get $p4
        i32.load
        local.tee $p1
        local.get $p4
        i32.load offset=4
        local.tee $p2
        local.get $p1
        local.get $p2
        i32.lt_u
        local.tee $l13
        select
        local.tee $l8
        i32.const 16
        i32.shl
        local.get $p2
        local.get $p1
        local.get $l13
        select
        local.tee $l13
        i32.or
        local.tee $p1
        local.get $p1
        i32.const 15
        i32.shl
        i32.const -1
        i32.xor
        i32.add
        local.tee $p1
        i32.const 10
        i32.shr_u
        local.get $p1
        i32.xor
        i32.const 9
        i32.mul
        local.tee $p1
        i32.const 6
        i32.shr_u
        local.get $p1
        i32.xor
        local.tee $p1
        local.get $p1
        i32.const 11
        i32.shl
        i32.const -1
        i32.xor
        i32.add
        local.tee $p1
        i32.const 16
        i32.shr_u
        local.get $p1
        i32.xor
        i32.const 127
        i32.and
        i32.add
        i32.const 3488
        i32.add
        local.tee $p2
        i32.load8_u
        local.tee $p1
        i32.const 255
        i32.ne
        if $I11
          loop $L12
            local.get $l8
            local.get $p0
            local.get $p1
            i32.const 255
            i32.and
            local.tee $p1
            i32.const 3
            i32.shl
            i32.add
            local.tee $p2
            i32.const 2336
            i32.add
            i32.load
            i32.eq
            if $I13
              local.get $p2
              i32.const 2340
              i32.add
              i32.load
              local.get $l13
              i32.eq
              br_if $B10
            end
            local.get $p0
            local.get $p1
            i32.add
            i32.const 3360
            i32.add
            local.tee $p2
            i32.load8_u
            local.tee $p1
            i32.const 255
            i32.ne
            br_if $L12
          end
        end
        local.get $p2
        local.get $l14
        i32.store8
        local.get $p0
        i32.const 2336
        i32.add
        local.tee $p1
        local.get $p0
        i32.load offset=3616
        i32.add
        i32.const 1024
        i32.add
        i32.const 255
        i32.store8
        local.get $p0
        local.get $p0
        i32.load offset=3616
        local.tee $p2
        i32.const 1
        i32.add
        i32.store offset=3616
        local.get $p1
        local.get $p2
        i32.const 3
        i32.shl
        i32.add
        local.get $l8
        i64.extend_i32_u
        local.get $l13
        i64.extend_i32_u
        i64.const 32
        i64.shl
        i64.or
        i64.store align=4
      end
      local.get $p3
      i32.const 32
      i32.and
      local.set $l13
      block $B14
        local.get $l11
        br_if $B14
        local.get $p0
        i32.const 3616
        i32.add
        i32.load
        local.tee $l11
        i32.const 128
        i32.eq
        br_if $B14
        local.get $p0
        local.get $p4
        i32.load offset=4
        local.tee $p1
        local.get $p4
        i32.load offset=8
        local.tee $p3
        local.get $p1
        local.get $p3
        i32.lt_u
        local.tee $l8
        select
        local.tee $p2
        i32.const 16
        i32.shl
        local.get $p3
        local.get $p1
        local.get $l8
        select
        local.tee $l8
        i32.or
        local.tee $p1
        local.get $p1
        i32.const 15
        i32.shl
        i32.const -1
        i32.xor
        i32.add
        local.tee $p1
        i32.const 10
        i32.shr_u
        local.get $p1
        i32.xor
        i32.const 9
        i32.mul
        local.tee $p1
        i32.const 6
        i32.shr_u
        local.get $p1
        i32.xor
        local.tee $p1
        local.get $p1
        i32.const 11
        i32.shl
        i32.const -1
        i32.xor
        i32.add
        local.tee $p1
        i32.const 16
        i32.shr_u
        local.get $p1
        i32.xor
        i32.const 127
        i32.and
        i32.add
        i32.const 3488
        i32.add
        local.tee $p3
        i32.load8_u
        local.tee $p1
        i32.const 255
        i32.ne
        if $I15
          loop $L16
            local.get $p2
            local.get $p0
            local.get $p1
            i32.const 255
            i32.and
            local.tee $p1
            i32.const 3
            i32.shl
            i32.add
            local.tee $p3
            i32.const 2336
            i32.add
            i32.load
            i32.eq
            if $I17
              local.get $p3
              i32.const 2340
              i32.add
              i32.load
              local.get $l8
              i32.eq
              br_if $B14
            end
            local.get $p0
            local.get $p1
            i32.add
            i32.const 3360
            i32.add
            local.tee $p3
            i32.load8_u
            local.tee $p1
            i32.const 255
            i32.ne
            br_if $L16
          end
        end
        local.get $p3
        local.get $l11
        i32.store8
        local.get $p0
        i32.const 2336
        i32.add
        local.tee $p1
        local.get $p0
        i32.load offset=3616
        i32.add
        i32.const 1024
        i32.add
        i32.const 255
        i32.store8
        local.get $p0
        local.get $p0
        i32.load offset=3616
        local.tee $p3
        i32.const 1
        i32.add
        i32.store offset=3616
        local.get $p1
        local.get $p3
        i32.const 3
        i32.shl
        i32.add
        local.get $p2
        i64.extend_i32_u
        local.get $l8
        i64.extend_i32_u
        i64.const 32
        i64.shl
        i64.or
        i64.store align=4
      end
      block $B18
        local.get $l13
        br_if $B18
        local.get $p0
        i32.const 3616
        i32.add
        i32.load
        local.tee $l13
        i32.const 128
        i32.eq
        br_if $B18
        local.get $p0
        local.get $p4
        i32.load offset=8
        local.tee $p1
        local.get $p4
        i32.load
        local.tee $p3
        local.get $p1
        local.get $p3
        i32.lt_u
        local.tee $l8
        select
        local.tee $p2
        i32.const 16
        i32.shl
        local.get $p3
        local.get $p1
        local.get $l8
        select
        local.tee $l8
        i32.or
        local.tee $p1
        local.get $p1
        i32.const 15
        i32.shl
        i32.const -1
        i32.xor
        i32.add
        local.tee $p1
        i32.const 10
        i32.shr_u
        local.get $p1
        i32.xor
        i32.const 9
        i32.mul
        local.tee $p1
        i32.const 6
        i32.shr_u
        local.get $p1
        i32.xor
        local.tee $p1
        local.get $p1
        i32.const 11
        i32.shl
        i32.const -1
        i32.xor
        i32.add
        local.tee $p1
        i32.const 16
        i32.shr_u
        local.get $p1
        i32.xor
        i32.const 127
        i32.and
        i32.add
        i32.const 3488
        i32.add
        local.tee $p3
        i32.load8_u
        local.tee $p1
        i32.const 255
        i32.ne
        if $I19
          loop $L20
            local.get $p2
            local.get $p0
            local.get $p1
            i32.const 255
            i32.and
            local.tee $p1
            i32.const 3
            i32.shl
            i32.add
            local.tee $p3
            i32.const 2336
            i32.add
            i32.load
            i32.eq
            if $I21
              local.get $p3
              i32.const 2340
              i32.add
              i32.load
              local.get $l8
              i32.eq
              br_if $B18
            end
            local.get $p0
            local.get $p1
            i32.add
            i32.const 3360
            i32.add
            local.tee $p3
            i32.load8_u
            local.tee $p1
            i32.const 255
            i32.ne
            br_if $L20
          end
        end
        local.get $p3
        local.get $l13
        i32.store8
        local.get $p0
        i32.const 2336
        i32.add
        local.tee $p1
        local.get $p0
        i32.load offset=3616
        i32.add
        i32.const 1024
        i32.add
        i32.const 255
        i32.store8
        local.get $p0
        local.get $p0
        i32.load offset=3616
        local.tee $p3
        i32.const 1
        i32.add
        i32.store offset=3616
        local.get $p1
        local.get $p3
        i32.const 3
        i32.shl
        i32.add
        local.get $p2
        i64.extend_i32_u
        local.get $l8
        i64.extend_i32_u
        i64.const 32
        i64.shl
        i64.or
        i64.store align=4
      end
      block $B22
        local.get $p0
        i32.const 4396
        i32.add
        i32.load
        local.tee $l8
        i32.const 128
        i32.eq
        br_if $B22
        block $B23
          local.get $p0
          local.get $p4
          i32.load
          local.tee $p3
          i32.const 127
          i32.and
          i32.add
          i32.const 4268
          i32.add
          local.tee $p2
          i32.load8_u
          local.tee $p1
          i32.const 255
          i32.ne
          if $I24
            loop $L25
              local.get $p0
              local.get $p1
              i32.const 255
              i32.and
              local.tee $p1
              i32.const 2
              i32.shl
              i32.add
              i32.const 3628
              i32.add
              i32.load
              local.get $p3
              i32.eq
              br_if $B23
              local.get $p0
              local.get $p1
              i32.add
              i32.const 4140
              i32.add
              local.tee $p2
              i32.load8_u
              local.tee $p1
              i32.const 255
              i32.ne
              br_if $L25
            end
          end
          local.get $p2
          local.get $l8
          i32.store8
          local.get $p0
          i32.const 3628
          i32.add
          local.tee $p1
          local.get $p0
          i32.load offset=4396
          i32.add
          i32.const 255
          i32.store8 offset=512
          local.get $p0
          local.get $p0
          i32.load offset=4396
          local.tee $p2
          i32.const 1
          i32.add
          i32.store offset=4396
          local.get $p1
          local.get $p2
          i32.const 2
          i32.shl
          i32.add
          local.get $p3
          i32.store
          local.get $p0
          i32.load offset=4396
          local.set $l8
        end
        local.get $l8
        i32.const 128
        i32.eq
        br_if $B22
        block $B26
          local.get $p0
          local.get $p4
          i32.load offset=4
          local.tee $p3
          i32.const 127
          i32.and
          i32.add
          i32.const 4268
          i32.add
          local.tee $p2
          i32.load8_u
          local.tee $p1
          i32.const 255
          i32.ne
          if $I27
            loop $L28
              local.get $p0
              local.get $p1
              i32.const 255
              i32.and
              local.tee $p1
              i32.const 2
              i32.shl
              i32.add
              i32.const 3628
              i32.add
              i32.load
              local.get $p3
              i32.eq
              br_if $B26
              local.get $p0
              local.get $p1
              i32.add
              i32.const 4140
              i32.add
              local.tee $p2
              i32.load8_u
              local.tee $p1
              i32.const 255
              i32.ne
              br_if $L28
            end
          end
          local.get $p2
          local.get $l8
          i32.store8
          local.get $p0
          i32.const 3628
          i32.add
          local.tee $p1
          local.get $p0
          i32.load offset=4396
          i32.add
          i32.const 255
          i32.store8 offset=512
          local.get $p0
          local.get $p0
          i32.load offset=4396
          local.tee $p2
          i32.const 1
          i32.add
          i32.store offset=4396
          local.get $p1
          local.get $p2
          i32.const 2
          i32.shl
          i32.add
          local.get $p3
          i32.store
          local.get $p0
          i32.load offset=4396
          local.set $l8
        end
        local.get $l8
        i32.const 128
        i32.eq
        br_if $B22
        local.get $p0
        local.get $p4
        i32.load offset=8
        local.tee $p3
        i32.const 127
        i32.and
        i32.add
        i32.const 4268
        i32.add
        local.tee $p4
        i32.load8_u
        local.tee $p1
        i32.const 255
        i32.ne
        if $I29
          loop $L30
            local.get $p0
            local.get $p1
            i32.const 255
            i32.and
            local.tee $p1
            i32.const 2
            i32.shl
            i32.add
            i32.const 3628
            i32.add
            i32.load
            local.get $p3
            i32.eq
            br_if $B22
            local.get $p0
            local.get $p1
            i32.add
            i32.const 4140
            i32.add
            local.tee $p4
            i32.load8_u
            local.tee $p1
            i32.const 255
            i32.ne
            br_if $L30
          end
        end
        local.get $p4
        local.get $l8
        i32.store8
        local.get $p0
        i32.const 3628
        i32.add
        local.tee $p1
        local.get $p0
        i32.load offset=4396
        i32.add
        i32.const 255
        i32.store8 offset=512
        local.get $p0
        local.get $p0
        i32.load offset=4396
        local.tee $p4
        i32.const 1
        i32.add
        i32.store offset=4396
        local.get $p1
        local.get $p4
        i32.const 2
        i32.shl
        i32.add
        local.get $p3
        i32.store
      end
      local.get $p0
      local.get $l5
      local.get $l17
      call $f70052
    end
    local.get $l5
    i32.const 224
    i32.add
    global.set $g0)
