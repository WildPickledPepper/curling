  (func $f70054 (type $t7) (param $p0 i32)
    (local $l1 i32) (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 i32) (local $l17 i32) (local $l18 i32) (local $l19 i32) (local $l20 i32) (local $l21 i32) (local $l22 i32) (local $l23 i32) (local $l24 i32) (local $l25 i32) (local $l26 i32) (local $l27 i32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32) (local $l33 f32) (local $l34 f32) (local $l35 f32) (local $l36 f32) (local $l37 f32) (local $l38 f32) (local $l39 f32)
    global.get $g0
    i32.const 144
    i32.sub
    local.tee $l3
    global.set $g0
    block $B0
      local.get $p0
      i32.load offset=3620
      local.tee $l2
      i32.load offset=4360
      local.tee $l1
      i32.eqz
      br_if $B0
      local.get $l1
      i32.const 15
      i32.lt_u
      br_if $B0
      local.get $p0
      i32.const 2176
      i32.add
      local.set $l18
      local.get $p0
      i32.const 2324
      i32.add
      local.set $l17
      local.get $l3
      i32.const 112
      i32.add
      local.set $l19
      local.get $l3
      i32.const 96
      i32.add
      local.set $l20
      local.get $l3
      i32.const 80
      i32.add
      local.set $l21
      local.get $l2
      i32.load offset=4356
      local.set $l22
      local.get $l1
      i32.const 15
      i32.div_u
      local.set $l23
      local.get $p0
      i32.const 4268
      i32.add
      local.set $l15
      loop $L1
        local.get $l22
        local.get $l16
        i32.const 60
        i32.mul
        i32.add
        local.tee $l2
        i32.load offset=36
        local.set $l7
        local.get $l2
        i32.load offset=44
        local.set $l8
        local.get $l2
        i32.load offset=40
        local.set $l9
        block $B2
          block $B3
            local.get $l2
            i32.load8_u offset=56
            local.tee $l11
            i32.const 8
            i32.and
            br_if $B3
            local.get $p0
            local.get $l7
            local.get $l9
            local.get $l7
            local.get $l9
            i32.lt_u
            local.tee $l1
            select
            local.tee $l5
            i32.const 16
            i32.shl
            local.get $l9
            local.get $l7
            local.get $l1
            select
            local.tee $l6
            i32.or
            local.tee $l1
            local.get $l1
            i32.const 15
            i32.shl
            i32.const -1
            i32.xor
            i32.add
            local.tee $l1
            i32.const 10
            i32.shr_u
            local.get $l1
            i32.xor
            i32.const 9
            i32.mul
            local.tee $l1
            i32.const 6
            i32.shr_u
            local.get $l1
            i32.xor
            local.tee $l1
            local.get $l1
            i32.const 11
            i32.shl
            i32.const -1
            i32.xor
            i32.add
            local.tee $l1
            i32.const 16
            i32.shr_u
            local.get $l1
            i32.xor
            i32.const 127
            i32.and
            i32.add
            i32.const 3488
            i32.add
            i32.load8_u
            local.tee $l1
            i32.const 255
            i32.eq
            br_if $B3
            loop $L4
              local.get $l5
              local.get $p0
              local.get $l1
              i32.const 255
              i32.and
              local.tee $l1
              i32.const 3
              i32.shl
              i32.add
              local.tee $l4
              i32.const 2336
              i32.add
              i32.load
              i32.eq
              if $I5
                local.get $l4
                i32.const 2340
                i32.add
                i32.load
                local.get $l6
                i32.eq
                br_if $B2
              end
              local.get $p0
              local.get $l1
              i32.add
              i32.const 3360
              i32.add
              i32.load8_u
              local.tee $l1
              i32.const 255
              i32.ne
              br_if $L4
            end
          end
          block $B6
            local.get $l11
            i32.const 16
            i32.and
            br_if $B6
            local.get $p0
            local.get $l9
            local.get $l8
            local.get $l8
            local.get $l9
            i32.gt_u
            local.tee $l1
            select
            local.tee $l5
            i32.const 16
            i32.shl
            local.get $l8
            local.get $l9
            local.get $l1
            select
            local.tee $l6
            i32.or
            local.tee $l1
            local.get $l1
            i32.const 15
            i32.shl
            i32.const -1
            i32.xor
            i32.add
            local.tee $l1
            i32.const 10
            i32.shr_u
            local.get $l1
            i32.xor
            i32.const 9
            i32.mul
            local.tee $l1
            i32.const 6
            i32.shr_u
            local.get $l1
            i32.xor
            local.tee $l1
            local.get $l1
            i32.const 11
            i32.shl
            i32.const -1
            i32.xor
            i32.add
            local.tee $l1
            i32.const 16
            i32.shr_u
            local.get $l1
            i32.xor
            i32.const 127
            i32.and
            i32.add
            i32.const 3488
            i32.add
            i32.load8_u
            local.tee $l1
            i32.const 255
            i32.eq
            br_if $B6
            loop $L7
              local.get $l5
              local.get $p0
              local.get $l1
              i32.const 255
              i32.and
              local.tee $l1
              i32.const 3
              i32.shl
              i32.add
              local.tee $l4
              i32.const 2336
              i32.add
              i32.load
              i32.eq
              if $I8
                local.get $l4
                i32.const 2340
                i32.add
                i32.load
                local.get $l6
                i32.eq
                br_if $B2
              end
              local.get $p0
              local.get $l1
              i32.add
              i32.const 3360
              i32.add
              i32.load8_u
              local.tee $l1
              i32.const 255
              i32.ne
              br_if $L7
            end
          end
          block $B9
            local.get $l11
            i32.const 32
            i32.and
            br_if $B9
            local.get $p0
            local.get $l8
            local.get $l7
            local.get $l7
            local.get $l8
            i32.gt_u
            local.tee $l1
            select
            local.tee $l5
            i32.const 16
            i32.shl
            local.get $l7
            local.get $l8
            local.get $l1
            select
            local.tee $l6
            i32.or
            local.tee $l1
            local.get $l1
            i32.const 15
            i32.shl
            i32.const -1
            i32.xor
            i32.add
            local.tee $l1
            i32.const 10
            i32.shr_u
            local.get $l1
            i32.xor
            i32.const 9
            i32.mul
            local.tee $l1
            i32.const 6
            i32.shr_u
            local.get $l1
            i32.xor
            local.tee $l1
            local.get $l1
            i32.const 11
            i32.shl
            i32.const -1
            i32.xor
            i32.add
            local.tee $l1
            i32.const 16
            i32.shr_u
            local.get $l1
            i32.xor
            i32.const 127
            i32.and
            i32.add
            i32.const 3488
            i32.add
            i32.load8_u
            local.tee $l1
            i32.const 255
            i32.eq
            br_if $B9
            loop $L10
              local.get $l5
              local.get $p0
              local.get $l1
              i32.const 255
              i32.and
              local.tee $l1
              i32.const 3
              i32.shl
              i32.add
              local.tee $l4
              i32.const 2336
              i32.add
              i32.load
              i32.eq
              if $I11
                local.get $l4
                i32.const 2340
                i32.add
                i32.load
                local.get $l6
                i32.eq
                br_if $B2
              end
              local.get $p0
              local.get $l1
              i32.add
              i32.const 3360
              i32.add
              i32.load8_u
              local.tee $l1
              i32.const 255
              i32.ne
              br_if $L10
            end
          end
          local.get $l3
          i32.const 56
          i32.add
          local.tee $l1
          i64.const 21474836480
          i64.store
          local.get $l3
          i32.const 48
          i32.add
          local.tee $l4
          i64.const 0
          i64.store
          local.get $l3
          i32.const 0
          i32.store8 offset=64
          local.get $l3
          i64.const 0
          i64.store offset=32
          local.get $l3
          i64.const 0
          i64.store offset=40
          local.get $l2
          f32.load
          local.set $l28
          local.get $l2
          f32.load offset=4
          local.set $l29
          local.get $l2
          f32.load offset=8
          local.set $l30
          local.get $l2
          f32.load offset=12
          local.set $l31
          local.get $l2
          f32.load offset=16
          local.set $l32
          local.get $l2
          f32.load offset=20
          local.set $l33
          local.get $l2
          f32.load offset=24
          local.set $l34
          local.get $l2
          f32.load offset=28
          local.set $l35
          local.get $l2
          f32.load offset=32
          local.set $l36
          local.get $l1
          i32.const 2139095039
          i32.store
          local.get $l4
          i64.const 9187343235540844544
          i64.store
          local.get $l3
          i32.const 0
          i32.store offset=124
          local.get $l3
          local.get $l36
          f32.store offset=120
          local.get $l3
          local.get $l35
          f32.store offset=116
          local.get $l3
          local.get $l34
          f32.store offset=112
          local.get $l3
          i32.const 0
          i32.store offset=108
          local.get $l3
          local.get $l33
          f32.store offset=104
          local.get $l3
          local.get $l32
          f32.store offset=100
          local.get $l3
          local.get $l31
          f32.store offset=96
          local.get $l3
          i32.const 0
          i32.store offset=92
          local.get $l3
          local.get $l30
          f32.store offset=88
          local.get $l3
          local.get $l29
          f32.store offset=84
          local.get $l3
          local.get $l28
          f32.store offset=80
          local.get $l3
          i32.const 0
          i32.store offset=44
          local.get $l3
          local.get $l34
          local.get $l28
          local.get $l31
          f32.add
          f32.add
          f32.const 0x1.55553ep-2 (;=0.333333;)
          f32.mul
          f32.store offset=32
          local.get $l3
          local.get $l36
          local.get $l30
          local.get $l33
          f32.add
          f32.add
          f32.const 0x1.55553ep-2 (;=0.333333;)
          f32.mul
          f32.store offset=40
          local.get $l3
          local.get $l35
          local.get $l29
          local.get $l32
          f32.add
          f32.add
          f32.const 0x1.55553ep-2 (;=0.333333;)
          f32.mul
          f32.store offset=36
          local.get $l2
          i32.load offset=48
          local.set $l4
          local.get $p0
          i32.load offset=2324
          local.set $l13
          local.get $p0
          i32.load offset=2320
          local.set $l5
          local.get $p0
          i32.load offset=4420
          local.tee $l6
          i32.load offset=40
          local.tee $l1
          f32.load offset=36
          local.set $l31
          local.get $l1
          f32.load offset=40
          local.set $l32
          local.get $p0
          i32.load offset=4416
          local.tee $l12
          i32.load offset=24
          local.get $l2
          i32.load offset=52
          i32.const 20
          i32.mul
          i32.add
          local.tee $l2
          f32.load
          local.set $l28
          local.get $l2
          f32.load offset=4
          local.set $l29
          local.get $l1
          f32.load offset=20
          local.set $l33
          local.get $l2
          f32.load offset=8
          local.set $l30
          local.get $l1
          f32.load offset=24
          local.set $l34
          local.get $l1
          f32.load offset=32
          local.set $l35
          local.get $l1
          f32.load offset=8
          local.set $l36
          local.get $l1
          f32.load
          local.set $l37
          local.get $l1
          f32.load offset=4
          local.set $l38
          local.get $l1
          f32.load offset=16
          local.set $l39
          local.get $l3
          i32.const 0
          i32.store offset=140
          local.get $l3
          i32.const 0
          i32.store offset=28
          local.get $l3
          local.get $l28
          local.get $l35
          f32.mul
          local.get $l29
          local.get $l31
          f32.mul
          f32.add
          local.get $l30
          local.get $l32
          f32.mul
          f32.add
          local.tee $l31
          f32.const 0x1p+0 (;=1;)
          local.get $l28
          local.get $l37
          f32.mul
          local.get $l29
          local.get $l38
          f32.mul
          f32.add
          local.get $l30
          local.get $l36
          f32.mul
          f32.add
          local.tee $l32
          local.get $l32
          f32.mul
          local.get $l28
          local.get $l39
          f32.mul
          local.get $l29
          local.get $l33
          f32.mul
          f32.add
          local.get $l30
          local.get $l34
          f32.mul
          f32.add
          local.tee $l28
          local.get $l28
          f32.mul
          f32.add
          local.get $l31
          local.get $l31
          f32.mul
          f32.add
          f32.sqrt
          f32.div
          local.tee $l29
          f32.mul
          local.tee $l30
          f32.store offset=136
          local.get $l3
          local.get $l30
          f32.neg
          f32.store offset=24
          local.get $l3
          local.get $l28
          local.get $l29
          f32.mul
          local.tee $l28
          f32.store offset=132
          local.get $l3
          local.get $l28
          f32.neg
          f32.store offset=20
          local.get $l3
          local.get $l32
          local.get $l29
          f32.mul
          local.tee $l28
          f32.store offset=128
          local.get $l3
          local.get $l28
          f32.neg
          f32.store offset=16
          local.get $l12
          local.get $l2
          local.get $l3
          i32.const 32
          i32.add
          local.get $l4
          local.get $l6
          local.get $l5
          local.get $l17
          local.get $l18
          local.get $l3
          i32.const 128
          i32.add
          local.get $p0
          i32.load offset=3624
          call $f70055
          block $B12
            local.get $l13
            local.get $p0
            i32.load offset=2324
            local.tee $l14
            i32.ge_u
            if $I13
              local.get $l14
              local.set $l10
              br $B12
            end
            local.get $l15
            local.get $l7
            i32.const 127
            i32.and
            i32.add
            local.set $l24
            local.get $l15
            local.get $l8
            i32.const 127
            i32.and
            i32.add
            local.set $l25
            local.get $l15
            local.get $l9
            i32.const 127
            i32.and
            i32.add
            local.set $l26
            local.get $l14
            i32.const 1
            i32.add
            local.set $l27
            i32.const 0
            local.set $l12
            local.get $l14
            local.tee $l6
            local.set $l10
            loop $L14
              local.get $l6
              local.tee $l2
              i32.const 1
              i32.sub
              local.tee $l6
              i32.const 6
              i32.shl
              local.tee $l5
              local.get $p0
              i32.load offset=2320
              i32.add
              i32.const 16
              i32.add
              local.get $l21
              local.get $l20
              local.get $l19
              local.get $l3
              i32.const 128
              i32.add
              local.get $l3
              call $f69896
              block $B15
                block $B16
                  local.get $l3
                  f32.load offset=128
                  local.tee $l28
                  f32.const 0x1.f0a3d8p-1 (;=0.97;)
                  f32.gt
                  if $I17
                    local.get $l26
                    i32.load8_u
                    local.tee $l1
                    i32.const 255
                    i32.eq
                    br_if $B15
                    loop $L18
                      local.get $p0
                      local.get $l1
                      i32.const 255
                      i32.and
                      local.tee $l1
                      i32.const 2
                      i32.shl
                      i32.add
                      i32.const 3628
                      i32.add
                      i32.load
                      local.get $l9
                      i32.eq
                      br_if $B16
                      local.get $p0
                      local.get $l1
                      i32.add
                      i32.const 4140
                      i32.add
                      i32.load8_u
                      local.tee $l1
                      i32.const 255
                      i32.ne
                      br_if $L18
                    end
                    br $B15
                  end
                  local.get $l3
                  f32.load
                  local.tee $l29
                  f32.const 0x1.f0a3d8p-1 (;=0.97;)
                  f32.gt
                  if $I19
                    local.get $l25
                    i32.load8_u
                    local.tee $l1
                    i32.const 255
                    i32.eq
                    br_if $B15
                    loop $L20
                      local.get $p0
                      local.get $l1
                      i32.const 255
                      i32.and
                      local.tee $l1
                      i32.const 2
                      i32.shl
                      i32.add
                      i32.const 3628
                      i32.add
                      i32.load
                      local.get $l8
                      i32.eq
                      br_if $B16
                      local.get $p0
                      local.get $l1
                      i32.add
                      i32.const 4140
                      i32.add
                      i32.load8_u
                      local.tee $l1
                      i32.const 255
                      i32.ne
                      br_if $L20
                    end
                    br $B15
                  end
                  local.get $l28
                  local.get $l29
                  f32.add
                  f32.const 0x1.eb85p-6 (;=0.03;)
                  f32.le
                  i32.eqz
                  br_if $B15
                  local.get $l24
                  i32.load8_u
                  local.tee $l1
                  i32.const 255
                  i32.eq
                  br_if $B15
                  loop $L21
                    local.get $p0
                    local.get $l1
                    i32.const 255
                    i32.and
                    local.tee $l1
                    i32.const 2
                    i32.shl
                    i32.add
                    i32.const 3628
                    i32.add
                    i32.load
                    local.get $l7
                    i32.eq
                    br_if $B16
                    local.get $p0
                    local.get $l1
                    i32.add
                    i32.const 4140
                    i32.add
                    i32.load8_u
                    local.tee $l1
                    i32.const 255
                    i32.ne
                    br_if $L21
                  end
                  br $B15
                end
                block $B22
                  local.get $l6
                  local.get $l10
                  i32.const 1
                  i32.sub
                  local.tee $l11
                  i32.ge_u
                  br_if $B22
                  local.get $l6
                  local.set $l4
                  local.get $l10
                  local.get $l12
                  local.get $l14
                  i32.sub
                  i32.add
                  i32.const 1
                  i32.and
                  if $I23
                    local.get $p0
                    i32.load offset=2320
                    local.tee $l4
                    local.get $l5
                    i32.add
                    local.tee $l1
                    local.get $l4
                    local.get $l2
                    i32.const 6
                    i32.shl
                    i32.add
                    local.tee $l4
                    i64.load
                    i64.store
                    local.get $l1
                    local.get $l4
                    i32.load offset=48
                    i32.store offset=48
                    local.get $l1
                    local.get $l4
                    i64.load offset=40
                    i64.store offset=40
                    local.get $l1
                    local.get $l4
                    i64.load offset=32
                    i64.store offset=32
                    local.get $l1
                    local.get $l4
                    i64.load offset=24
                    i64.store offset=24
                    local.get $l1
                    local.get $l4
                    i64.load offset=16
                    i64.store offset=16
                    local.get $l1
                    local.get $l4
                    i64.load offset=8
                    i64.store offset=8
                    local.get $l2
                    local.set $l4
                  end
                  local.get $l27
                  local.get $l12
                  i32.sub
                  local.get $l10
                  i32.eq
                  br_if $B22
                  loop $L24
                    local.get $p0
                    i32.load offset=2320
                    local.tee $l2
                    local.get $l4
                    i32.const 6
                    i32.shl
                    local.tee $l5
                    i32.add
                    local.tee $l1
                    local.get $l2
                    local.get $l5
                    i32.const -64
                    i32.sub
                    local.tee $l5
                    i32.add
                    local.tee $l2
                    i64.load
                    i64.store
                    local.get $l1
                    local.get $l2
                    i32.load offset=48
                    i32.store offset=48
                    local.get $l1
                    local.get $l2
                    i64.load offset=40
                    i64.store offset=40
                    local.get $l1
                    local.get $l2
                    i64.load offset=32
                    i64.store offset=32
                    local.get $l1
                    local.get $l2
                    i64.load offset=24
                    i64.store offset=24
                    local.get $l1
                    local.get $l2
                    i64.load offset=16
                    i64.store offset=16
                    local.get $l1
                    local.get $l2
                    i64.load offset=8
                    i64.store offset=8
                    local.get $p0
                    i32.load offset=2320
                    local.tee $l2
                    local.get $l5
                    i32.add
                    local.tee $l1
                    local.get $l2
                    local.get $l4
                    i32.const 2
                    i32.add
                    local.tee $l4
                    i32.const 6
                    i32.shl
                    i32.add
                    local.tee $l2
                    i64.load
                    i64.store
                    local.get $l1
                    local.get $l2
                    i64.load offset=32
                    i64.store offset=32
                    local.get $l1
                    local.get $l2
                    i64.load offset=16
                    i64.store offset=16
                    local.get $l1
                    local.get $l2
                    i64.load offset=8
                    i64.store offset=8
                    local.get $l1
                    local.get $l2
                    i64.load offset=24
                    i64.store offset=24
                    local.get $l1
                    local.get $l2
                    i64.load offset=40
                    i64.store offset=40
                    local.get $l1
                    local.get $l2
                    i32.load offset=48
                    i32.store offset=48
                    local.get $l4
                    local.get $l11
                    i32.lt_u
                    br_if $L24
                  end
                end
                local.get $l11
                local.set $l10
              end
              local.get $l12
              i32.const 1
              i32.add
              local.set $l12
              local.get $l6
              local.get $l13
              i32.gt_u
              br_if $L14
            end
          end
          local.get $l17
          local.get $l10
          i32.store
          local.get $l10
          local.get $l13
          i32.le_u
          br_if $B2
          local.get $p0
          local.get $l3
          i32.const 16
          i32.add
          local.get $l13
          call $f70052
        end
        local.get $l16
        i32.const 1
        i32.add
        local.tee $l16
        local.get $l23
        i32.ne
        br_if $L1
      end
    end
    local.get $l3
    i32.const 144
    i32.add
    global.set $g0)
