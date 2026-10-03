  (func $f72185 (type $t236) (param $p0 i32) (param $p1 f32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 i32) (param $p7 i32)
    (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32) (local $l33 f32) (local $l34 i32) (local $l35 i32) (local $l36 i32) (local $l37 i32) (local $l38 i32) (local $l39 i32) (local $l40 i32) (local $l41 i32) (local $l42 i32) (local $l43 i32) (local $l44 i32)
    local.get $p0
    i32.const 4648
    i32.add
    i32.load
    if $I0
      i32.const 4700888
      i32.load
      i32.const 8
      i32.const 3184128
      i32.const 1864
      local.get $p6
      i32.const 0
      call $f69760
      return
    end
    global.get $g0
    i32.const 176
    i32.sub
    local.tee $l34
    global.set $g0
    local.get $p0
    i32.const 5884
    i32.add
    i32.const 0
    i32.store
    local.get $p0
    i32.const 5872
    i32.add
    i32.const 0
    i32.store
    local.get $p0
    i32.const 5860
    i32.add
    i32.const 0
    i32.store
    local.get $p0
    i32.const 5848
    i32.add
    i32.const 0
    i32.store
    local.get $p0
    i32.const 5836
    i32.add
    i32.const 0
    i32.store
    block $B1
      local.get $p0
      i32.const 0
      local.get $p0
      i32.load
      i32.load offset=280
      call_indirect $__indirect_function_table (type $t13)
      f32.const 0x0p+0 (;=0;)
      f32.eq
      br_if $B1
      local.get $l34
      i64.const 0
      i64.store offset=96
      local.get $l34
      i64.const 0
      i64.store offset=88
      local.get $l34
      i64.const 0
      i64.store offset=80
      local.get $l34
      i64.const 0
      i64.store offset=112
      local.get $l34
      i64.const 4575657221408423936
      i64.store offset=104
      local.get $l34
      i64.const 0
      i64.store offset=120
      local.get $l34
      i64.const 0
      i64.store offset=132 align=4
      local.get $l34
      i32.const 1065353216
      i32.store offset=128
      local.get $l34
      i64.const 0
      i64.store offset=140 align=4
      local.get $l34
      i64.const 0
      i64.store offset=152
      local.get $l34
      i32.const 1065353216
      i32.store offset=148
      local.get $l34
      i64.const 0
      i64.store offset=160
      local.get $l34
      i32.const 1065353216
      i32.store offset=168
      local.get $l34
      i64.const 0
      i64.store offset=72
      local.get $l34
      local.get $p0
      i32.const 5828
      i32.add
      i32.store offset=172
      local.get $p0
      i32.const 1
      local.get $p0
      i32.load
      i32.load offset=280
      call_indirect $__indirect_function_table (type $t13)
      local.tee $l8
      f32.const 0x0p+0 (;=0;)
      f32.ne
      if $I2
        local.get $l34
        i32.const -16776961
        i32.store offset=52
        local.get $l34
        i64.const -71777214277943296
        i64.store offset=44 align=4
        local.get $l34
        local.get $l8
        f32.store offset=40
        local.get $l34
        local.get $l8
        f32.store offset=36
        local.get $l34
        local.get $l8
        f32.store offset=32
        local.get $l34
        i32.const 72
        i32.add
        local.get $l34
        i32.const 32
        i32.add
        call $f69808
      end
      local.get $p0
      i32.const 5980
      i32.add
      i32.load
      local.tee $l36
      if $I3
        loop $L4
          i32.const 0
          local.set $l40
          local.get $p0
          i32.load offset=5948
          local.get $l43
          i32.const 2
          i32.shl
          i32.add
          i32.load
          local.tee $l37
          i32.load offset=100
          if $I5
            loop $L6
              local.get $l37
              i32.load offset=96
              local.get $l40
              i32.const 2
              i32.shl
              i32.add
              i32.load
              local.set $l35
              global.get $g0
              i32.const 32
              i32.sub
              local.tee $l36
              global.set $g0
              local.get $l35
              local.get $l34
              i32.const 72
              i32.add
              local.tee $l39
              local.get $p0
              call $f72496
              block $B7
                local.get $l35
                i32.load offset=56
                local.get $l35
                local.get $l35
                i32.load offset=52
                local.tee $p6
                i32.const 22
                i32.shr_u
                i32.const 60
                i32.and
                i32.const 3181092
                i32.add
                i32.load
                i32.add
                i32.const 56
                i32.add
                local.get $p6
                i32.const 1
                i32.and
                select
                i32.load8_u
                i32.const 1
                i32.and
                i32.eqz
                br_if $B7
                local.get $l35
                local.get $l35
                i32.load
                i32.load offset=28
                call_indirect $__indirect_function_table (type $t5)
                local.tee $p6
                i32.const 0
                local.get $p6
                i32.load
                i32.load offset=280
                call_indirect $__indirect_function_table (type $t13)
                local.tee $l10
                local.get $l35
                local.get $l35
                i32.load
                i32.load offset=28
                call_indirect $__indirect_function_table (type $t5)
                local.tee $p6
                i32.const 3
                local.get $p6
                i32.load
                i32.load offset=280
                call_indirect $__indirect_function_table (type $t13)
                f32.mul
                f32.const 0x0p+0 (;=0;)
                f32.ne
                if $I8
                  block $B9
                    local.get $l35
                    i32.load offset=316
                    local.tee $l38
                    i32.const 2
                    i32.and
                    if $I10
                      local.get $l35
                      i32.load offset=56
                      i32.const 96
                      i32.add
                      local.set $p6
                      br $B9
                    end
                    local.get $l35
                    i32.const -64
                    i32.sub
                    call $f71608
                    local.set $p6
                    local.get $l35
                    i32.load offset=316
                    local.set $l38
                  end
                  f32.const 0x0p+0 (;=0;)
                  f32.const 0x1p+0 (;=1;)
                  local.get $p6
                  f32.load offset=8
                  local.tee $l8
                  f32.div
                  local.get $l8
                  f32.const 0x0p+0 (;=0;)
                  f32.eq
                  select
                  local.set $l12
                  f32.const 0x0p+0 (;=0;)
                  f32.const 0x1p+0 (;=1;)
                  local.get $p6
                  f32.load offset=4
                  local.tee $l8
                  f32.div
                  local.get $l8
                  f32.const 0x0p+0 (;=0;)
                  f32.eq
                  select
                  local.set $l11
                  f32.const 0x0p+0 (;=0;)
                  f32.const 0x1p+0 (;=1;)
                  local.get $p6
                  f32.load
                  local.tee $l8
                  f32.div
                  local.get $l8
                  f32.const 0x0p+0 (;=0;)
                  f32.eq
                  select
                  local.set $l9
                  block $B11 (result f32)
                    local.get $l38
                    i32.const 1
                    i32.and
                    if $I12
                      local.get $l35
                      i32.load offset=56
                      f32.load offset=92
                      br $B11
                    end
                    local.get $l35
                    i32.const -64
                    i32.sub
                    call $f71606
                  end
                  local.set $l8
                  local.get $l39
                  i32.const 16777215
                  call $f69798
                  local.get $l35
                  i32.const 256
                  i32.add
                  call $f69800
                  local.set $p6
                  local.get $l36
                  local.get $l9
                  f32.const 0x1.8p+2 (;=6;)
                  f32.const 0x1p+0 (;=1;)
                  local.get $l8
                  f32.div
                  f32.div
                  local.tee $l8
                  f32.mul
                  local.tee $l9
                  local.get $l11
                  local.get $l8
                  f32.mul
                  local.tee $l11
                  f32.add
                  local.get $l12
                  local.get $l8
                  f32.mul
                  local.tee $l8
                  f32.sub
                  f32.abs
                  f32.sqrt
                  f32.const 0x1p-1 (;=0.5;)
                  f32.mul
                  local.tee $l12
                  f32.store offset=20
                  local.get $l36
                  local.get $l8
                  local.get $l9
                  local.get $l11
                  f32.sub
                  f32.add
                  f32.abs
                  f32.sqrt
                  f32.const 0x1p-1 (;=0.5;)
                  f32.mul
                  local.tee $l13
                  f32.store offset=16
                  local.get $l36
                  i32.const 1
                  i32.store8 offset=24
                  local.get $l36
                  local.get $l12
                  f32.neg
                  f32.store offset=8
                  local.get $l36
                  local.get $l13
                  f32.neg
                  f32.store offset=4
                  local.get $l36
                  local.get $l8
                  local.get $l11
                  local.get $l9
                  f32.sub
                  f32.add
                  f32.abs
                  f32.sqrt
                  f32.const 0x1p-1 (;=0.5;)
                  f32.mul
                  local.tee $l8
                  f32.store offset=12
                  local.get $l36
                  local.get $l8
                  f32.neg
                  f32.store
                  local.get $p6
                  local.get $l36
                  call $f69806
                end
                local.get $l35
                local.get $l35
                i32.load
                i32.load offset=28
                call_indirect $__indirect_function_table (type $t5)
                local.tee $p6
                i32.const 20
                local.get $p6
                i32.load
                i32.load offset=280
                call_indirect $__indirect_function_table (type $t13)
                local.set $l9
                local.get $l10
                local.get $l35
                local.get $l35
                i32.load
                i32.load offset=28
                call_indirect $__indirect_function_table (type $t5)
                local.tee $p6
                i32.const 21
                local.get $p6
                i32.load
                i32.load offset=280
                call_indirect $__indirect_function_table (type $t13)
                f32.mul
                local.set $l8
                local.get $l10
                local.get $l9
                f32.mul
                local.tee $l10
                f32.const 0x0p+0 (;=0;)
                f32.eq
                local.get $l8
                f32.const 0x0p+0 (;=0;)
                f32.eq
                i32.and
                br_if $B7
                local.get $l36
                local.get $l39
                i32.store offset=12
                local.get $l36
                local.get $l8
                f32.store offset=8
                local.get $l36
                local.get $l10
                f32.store offset=4
                local.get $l36
                i32.const 3203932
                i32.store
                global.get $g0
                i32.const 192
                i32.sub
                local.tee $p6
                global.set $g0
                block $B13
                  local.get $l35
                  i32.load offset=328
                  local.tee $l39
                  i32.eqz
                  br_if $B13
                  local.get $p6
                  i32.const 56
                  i32.add
                  local.get $l35
                  local.get $l35
                  i32.load
                  i32.load offset=76
                  call_indirect $__indirect_function_table (type $t1)
                  local.get $p6
                  i32.const 128
                  i32.add
                  local.get $l35
                  i32.load offset=324
                  local.tee $l41
                  local.get $l41
                  i32.load
                  i32.load offset=44
                  call_indirect $__indirect_function_table (type $t1)
                  local.get $p6
                  local.get $p6
                  i32.const 80
                  i32.add
                  local.tee $l42
                  f32.load
                  local.get $p6
                  i32.const 152
                  i32.add
                  local.tee $l38
                  f32.load
                  local.tee $l8
                  local.get $l8
                  f32.add
                  local.tee $l13
                  local.get $p6
                  f32.load offset=68
                  local.tee $l8
                  local.get $l8
                  f32.mul
                  f32.const -0x1p-1 (;=-0.5;)
                  f32.add
                  local.tee $l19
                  f32.mul
                  local.get $l8
                  local.get $p6
                  i32.const 148
                  i32.add
                  local.tee $l44
                  f32.load
                  local.tee $l9
                  local.get $l9
                  f32.add
                  local.tee $l12
                  local.get $p6
                  f32.load offset=56
                  local.tee $l9
                  f32.mul
                  local.get $p6
                  f32.load offset=144
                  local.tee $l11
                  local.get $l11
                  f32.add
                  local.tee $l15
                  local.get $p6
                  f32.load offset=60
                  local.tee $l11
                  f32.mul
                  f32.sub
                  f32.mul
                  f32.add
                  local.get $p6
                  f32.load offset=64
                  local.tee $l10
                  local.get $l15
                  local.get $l9
                  f32.mul
                  local.get $l12
                  local.get $l11
                  f32.mul
                  f32.add
                  local.get $l13
                  local.get $l10
                  f32.mul
                  f32.add
                  local.tee $l20
                  f32.mul
                  f32.add
                  f32.add
                  f32.store offset=184
                  local.get $p6
                  local.get $p6
                  i32.const 76
                  i32.add
                  local.tee $l41
                  f32.load
                  local.get $l11
                  local.get $l20
                  f32.mul
                  local.get $l12
                  local.get $l19
                  f32.mul
                  local.get $l8
                  local.get $l15
                  local.get $l10
                  f32.mul
                  local.get $l13
                  local.get $l9
                  f32.mul
                  f32.sub
                  f32.mul
                  f32.add
                  f32.add
                  f32.add
                  f32.store offset=180
                  local.get $p6
                  local.get $l8
                  local.get $p6
                  f32.load offset=140
                  local.tee $l14
                  f32.mul
                  local.get $l9
                  local.get $p6
                  f32.load offset=128
                  local.tee $l16
                  f32.mul
                  f32.sub
                  local.get $l11
                  local.get $p6
                  f32.load offset=132
                  local.tee $l18
                  f32.mul
                  f32.sub
                  local.get $l10
                  local.get $p6
                  f32.load offset=136
                  local.tee $l17
                  f32.mul
                  f32.sub
                  f32.store offset=172
                  local.get $p6
                  local.get $l9
                  local.get $l18
                  f32.mul
                  local.get $l10
                  local.get $l14
                  f32.mul
                  local.get $l8
                  local.get $l17
                  f32.mul
                  f32.add
                  f32.add
                  local.get $l11
                  local.get $l16
                  f32.mul
                  f32.sub
                  f32.store offset=168
                  local.get $p6
                  local.get $l10
                  local.get $l16
                  f32.mul
                  local.get $l11
                  local.get $l14
                  f32.mul
                  local.get $l8
                  local.get $l18
                  f32.mul
                  f32.add
                  f32.add
                  local.get $l9
                  local.get $l17
                  f32.mul
                  f32.sub
                  f32.store offset=164
                  local.get $p6
                  local.get $l8
                  local.get $l16
                  f32.mul
                  local.get $l9
                  local.get $l14
                  f32.mul
                  f32.add
                  local.get $l11
                  local.get $l17
                  f32.mul
                  f32.add
                  local.get $l10
                  local.get $l18
                  f32.mul
                  f32.sub
                  f32.store offset=160
                  local.get $p6
                  local.get $p6
                  f32.load offset=72
                  local.get $l9
                  local.get $l20
                  f32.mul
                  local.get $l15
                  local.get $l19
                  f32.mul
                  local.get $l8
                  local.get $l13
                  local.get $l11
                  f32.mul
                  local.get $l12
                  local.get $l10
                  f32.mul
                  f32.sub
                  f32.mul
                  f32.add
                  f32.add
                  f32.add
                  f32.store offset=176
                  local.get $p6
                  i32.const 56
                  i32.add
                  local.get $l39
                  local.get $l39
                  i32.load
                  i32.load offset=76
                  call_indirect $__indirect_function_table (type $t1)
                  local.get $p6
                  i32.const 96
                  i32.add
                  local.get $l35
                  i32.load offset=324
                  local.tee $l39
                  local.get $l39
                  i32.load
                  i32.load offset=32
                  call_indirect $__indirect_function_table (type $t1)
                  local.get $l38
                  local.get $l42
                  f32.load
                  local.get $p6
                  f32.load offset=120
                  local.tee $l8
                  local.get $l8
                  f32.add
                  local.tee $l13
                  local.get $p6
                  f32.load offset=68
                  local.tee $l8
                  local.get $l8
                  f32.mul
                  f32.const -0x1p-1 (;=-0.5;)
                  f32.add
                  local.tee $l19
                  f32.mul
                  local.get $l8
                  local.get $p6
                  f32.load offset=116
                  local.tee $l9
                  local.get $l9
                  f32.add
                  local.tee $l12
                  local.get $p6
                  f32.load offset=56
                  local.tee $l9
                  f32.mul
                  local.get $p6
                  f32.load offset=112
                  local.tee $l11
                  local.get $l11
                  f32.add
                  local.tee $l15
                  local.get $p6
                  f32.load offset=60
                  local.tee $l11
                  f32.mul
                  f32.sub
                  f32.mul
                  f32.add
                  local.get $p6
                  f32.load offset=64
                  local.tee $l10
                  local.get $l15
                  local.get $l9
                  f32.mul
                  local.get $l12
                  local.get $l11
                  f32.mul
                  f32.add
                  local.get $l13
                  local.get $l10
                  f32.mul
                  f32.add
                  local.tee $l20
                  f32.mul
                  f32.add
                  f32.add
                  f32.store
                  local.get $l44
                  local.get $l41
                  f32.load
                  local.get $l11
                  local.get $l20
                  f32.mul
                  local.get $l12
                  local.get $l19
                  f32.mul
                  local.get $l8
                  local.get $l15
                  local.get $l10
                  f32.mul
                  local.get $l13
                  local.get $l9
                  f32.mul
                  f32.sub
                  f32.mul
                  f32.add
                  f32.add
                  f32.add
                  f32.store
                  local.get $p6
                  local.get $l8
                  local.get $p6
                  f32.load offset=108
                  local.tee $l14
                  f32.mul
                  local.get $l9
                  local.get $p6
                  f32.load offset=96
                  local.tee $l16
                  f32.mul
                  f32.sub
                  local.get $l11
                  local.get $p6
                  f32.load offset=100
                  local.tee $l18
                  f32.mul
                  f32.sub
                  local.get $l10
                  local.get $p6
                  f32.load offset=104
                  local.tee $l17
                  f32.mul
                  f32.sub
                  f32.store offset=140
                  local.get $p6
                  local.get $l9
                  local.get $l18
                  f32.mul
                  local.get $l10
                  local.get $l14
                  f32.mul
                  local.get $l8
                  local.get $l17
                  f32.mul
                  f32.add
                  f32.add
                  local.get $l11
                  local.get $l16
                  f32.mul
                  f32.sub
                  f32.store offset=136
                  local.get $p6
                  local.get $l10
                  local.get $l16
                  f32.mul
                  local.get $l11
                  local.get $l14
                  f32.mul
                  local.get $l8
                  local.get $l18
                  f32.mul
                  f32.add
                  f32.add
                  local.get $l9
                  local.get $l17
                  f32.mul
                  f32.sub
                  f32.store offset=132
                  local.get $p6
                  local.get $l8
                  local.get $l16
                  f32.mul
                  local.get $l9
                  local.get $l14
                  f32.mul
                  f32.add
                  local.get $l11
                  local.get $l17
                  f32.mul
                  f32.add
                  local.get $l10
                  local.get $l18
                  f32.mul
                  f32.sub
                  f32.store offset=128
                  local.get $p6
                  local.get $p6
                  f32.load offset=72
                  local.get $l9
                  local.get $l20
                  f32.mul
                  local.get $l15
                  local.get $l19
                  f32.mul
                  local.get $l8
                  local.get $l13
                  local.get $l11
                  f32.mul
                  local.get $l12
                  local.get $l10
                  f32.mul
                  f32.sub
                  f32.mul
                  f32.add
                  f32.add
                  f32.add
                  f32.store offset=144
                  local.get $l36
                  local.get $p6
                  i32.const 160
                  i32.add
                  local.get $p6
                  i32.const 128
                  i32.add
                  local.get $l36
                  i32.load
                  i32.load offset=8
                  call_indirect $__indirect_function_table (type $t2)
                  local.get $l35
                  i32.load offset=324
                  local.tee $l39
                  local.get $l39
                  i32.load
                  i32.load offset=48
                  call_indirect $__indirect_function_table (type $t5)
                  local.set $l38
                  local.get $l35
                  local.get $l35
                  i32.load
                  i32.load offset=268
                  call_indirect $__indirect_function_table (type $t5)
                  i32.load16_u offset=4
                  i32.const 11
                  i32.eq
                  if $I14
                    local.get $l41
                    local.get $p6
                    i64.load offset=148 align=4
                    i64.store align=4
                    local.get $p6
                    local.get $p6
                    f32.load offset=128
                    local.tee $l8
                    f32.store offset=56
                    local.get $p6
                    local.get $p6
                    f32.load offset=132
                    local.tee $l9
                    f32.store offset=60
                    local.get $p6
                    local.get $p6
                    f32.load offset=136
                    local.tee $l11
                    f32.store offset=64
                    local.get $p6
                    local.get $p6
                    f32.load offset=140
                    local.tee $l10
                    f32.store offset=68
                    local.get $p6
                    local.get $p6
                    f32.load offset=144
                    f32.store offset=72
                    f32.const 0x0p+0 (;=0;)
                    local.set $l13
                    local.get $l8
                    local.get $p6
                    f32.load offset=160
                    local.tee $l15
                    f32.mul
                    local.tee $l12
                    local.get $l9
                    local.get $p6
                    f32.load offset=164
                    local.tee $l14
                    f32.mul
                    local.tee $l20
                    f32.add
                    local.get $l11
                    local.get $p6
                    f32.load offset=168
                    local.tee $l16
                    f32.mul
                    local.tee $l21
                    f32.add
                    local.get $l10
                    local.get $p6
                    f32.load offset=172
                    local.tee $l18
                    f32.mul
                    local.tee $l22
                    f32.add
                    f32.const 0x0p+0 (;=0;)
                    f32.lt
                    if $I15
                      local.get $p6
                      local.get $l10
                      f32.neg
                      local.tee $l10
                      f32.store offset=140
                      local.get $p6
                      local.get $l11
                      f32.neg
                      local.tee $l11
                      f32.store offset=136
                      local.get $p6
                      local.get $l9
                      f32.neg
                      local.tee $l9
                      f32.store offset=132
                      local.get $p6
                      local.get $l8
                      f32.neg
                      local.tee $l8
                      f32.store offset=128
                      local.get $l16
                      local.get $l11
                      f32.mul
                      local.set $l21
                      local.get $l14
                      local.get $l9
                      f32.mul
                      local.set $l20
                      local.get $l18
                      local.get $l10
                      f32.mul
                      local.set $l22
                      local.get $l15
                      local.get $l8
                      f32.mul
                      local.set $l12
                    end
                    local.get $l14
                    local.get $l8
                    f32.mul
                    local.get $l18
                    local.get $l11
                    f32.mul
                    local.get $l16
                    local.get $l10
                    f32.mul
                    f32.sub
                    local.get $l15
                    local.get $l9
                    f32.mul
                    f32.sub
                    f32.add
                    local.set $l17
                    local.get $l15
                    local.get $l11
                    f32.mul
                    local.get $l18
                    local.get $l9
                    f32.mul
                    local.get $l14
                    local.get $l10
                    f32.mul
                    f32.sub
                    local.get $l16
                    local.get $l8
                    f32.mul
                    f32.sub
                    f32.add
                    local.set $l19
                    local.get $l21
                    local.get $l12
                    local.get $l22
                    f32.add
                    local.get $l20
                    f32.add
                    f32.add
                    local.set $l12
                    block $B16 (result f32)
                      local.get $l18
                      local.get $l8
                      f32.mul
                      local.get $l15
                      local.get $l10
                      f32.mul
                      f32.sub
                      local.get $l14
                      local.get $l11
                      f32.mul
                      f32.sub
                      local.get $l16
                      local.get $l9
                      f32.mul
                      f32.add
                      local.tee $l11
                      f32.const 0x0p+0 (;=0;)
                      f32.eq
                      if $I17
                        f32.const 0x1p+0 (;=1;)
                        local.set $l8
                        f32.const 0x0p+0 (;=0;)
                        br $B16
                      end
                      local.get $l12
                      f32.const 0x1p+0 (;=1;)
                      local.get $l11
                      local.get $l11
                      f32.mul
                      f32.const 0x0p+0 (;=0;)
                      f32.add
                      local.get $l12
                      local.get $l12
                      f32.mul
                      f32.add
                      f32.sqrt
                      f32.div
                      local.tee $l10
                      f32.mul
                      local.set $l8
                      local.get $l11
                      local.get $l10
                      f32.mul
                      local.set $l13
                      local.get $l10
                      f32.const 0x0p+0 (;=0;)
                      f32.mul
                    end
                    local.set $l9
                    local.get $l11
                    local.get $l13
                    f32.mul
                    local.get $l12
                    local.get $l8
                    f32.mul
                    f32.add
                    local.set $l15
                    local.get $l19
                    local.get $l9
                    f32.mul
                    local.set $l14
                    local.get $l12
                    local.get $l9
                    f32.mul
                    local.set $l10
                    local.get $l17
                    local.get $l8
                    f32.mul
                    local.set $l12
                    local.get $l19
                    local.get $l8
                    f32.mul
                    local.set $l16
                    local.get $l8
                    f32.const -0x1p+0 (;=-1;)
                    f32.eq
                    if $I18 (result f32)
                      f32.const -0x1.fffffep+63 (;=-1.84467e+19;)
                      f32.const 0x1.fffffep+63 (;=1.84467e+19;)
                      local.get $l13
                      f32.const 0x0p+0 (;=0;)
                      f32.lt
                      select
                    else
                      local.get $l13
                      local.get $l8
                      f32.const 0x1p+0 (;=1;)
                      f32.add
                      f32.div
                    end
                    local.set $l18
                    local.get $l12
                    local.get $l10
                    f32.sub
                    local.set $l12
                    local.get $l11
                    local.get $l9
                    f32.mul
                    local.set $l8
                    local.get $l16
                    local.get $l10
                    f32.sub
                    local.set $l11
                    local.get $l17
                    local.get $l13
                    f32.mul
                    local.set $l10
                    local.get $l14
                    local.get $l15
                    f32.add
                    local.set $l15
                    local.get $l17
                    local.get $l9
                    f32.mul
                    local.set $l9
                    block $B19 (result i32)
                      local.get $l38
                      i32.load offset=4
                      local.tee $l35
                      i32.const 262144
                      i32.and
                      if $I20
                        local.get $l38
                        i32.load offset=8
                        local.tee $l41
                        i32.const 152
                        i32.add
                        local.set $l39
                        local.get $l41
                        i32.const 148
                        i32.add
                        br $B19
                      end
                      local.get $l38
                      i32.const 76
                      i32.add
                      local.set $l39
                      local.get $l38
                      i32.const 72
                      i32.add
                    end
                    local.set $l41
                    local.get $l12
                    local.get $l8
                    f32.sub
                    local.set $l12
                    local.get $l19
                    local.get $l13
                    f32.mul
                    local.set $l13
                    local.get $l11
                    local.get $l10
                    f32.sub
                    local.set $l10
                    local.get $l9
                    local.get $l15
                    f32.add
                    local.set $l11
                    local.get $l39
                    f32.load
                    local.set $l9
                    local.get $l41
                    f32.load
                    local.set $l15
                    block $B21 (result i32)
                      local.get $l35
                      i32.const 131072
                      i32.and
                      if $I22
                        local.get $l38
                        i32.load offset=8
                        local.tee $l39
                        i32.const 144
                        i32.add
                        local.set $l41
                        local.get $l39
                        i32.const 140
                        i32.add
                        br $B21
                      end
                      local.get $l38
                      i32.const 88
                      i32.add
                      local.set $l41
                      local.get $l38
                      i32.load offset=8
                      local.set $l39
                      local.get $l38
                      i32.const 80
                      i32.add
                    end
                    local.set $l42
                    local.get $l13
                    local.get $l12
                    f32.add
                    local.set $l13
                    local.get $l8
                    local.get $l10
                    f32.add
                    local.set $l8
                    local.get $l39
                    i32.const 108
                    i32.add
                    local.get $l38
                    i32.const 332
                    i32.add
                    local.get $l35
                    i32.const 1024
                    i32.and
                    select
                    f32.load
                    local.set $l10
                    local.get $l41
                    f32.load
                    local.set $l12
                    local.get $l42
                    f32.load
                    local.set $l14
                    local.get $l36
                    local.get $p6
                    i32.const 56
                    i32.add
                    local.get $l15
                    local.get $l9
                    local.get $l9
                    local.get $l39
                    i32.const 124
                    i32.add
                    local.get $l38
                    i32.const 348
                    i32.add
                    local.get $l35
                    i32.const 16384
                    i32.and
                    select
                    f32.load
                    f32.sub
                    call $f18177
                    local.get $l18
                    f32.abs
                    f32.lt
                    local.get $l36
                    i32.load
                    i32.load offset=16
                    call_indirect $__indirect_function_table (type $t78)
                    block $B23 (result f32)
                      local.get $l11
                      f32.const -0x1p+0 (;=-1;)
                      f32.eq
                      if $I24
                        f32.const -0x1.fffffep+63 (;=-1.84467e+19;)
                        f32.const 0x1.fffffep+63 (;=1.84467e+19;)
                        local.get $l8
                        f32.const 0x0p+0 (;=0;)
                        f32.lt
                        select
                        local.set $l9
                        f32.const -0x1.fffffep+63 (;=-1.84467e+19;)
                        f32.const 0x1.fffffep+63 (;=1.84467e+19;)
                        local.get $l13
                        f32.const 0x0p+0 (;=0;)
                        f32.lt
                        select
                        br $B23
                      end
                      local.get $l8
                      local.get $l11
                      f32.const 0x1p+0 (;=1;)
                      f32.add
                      local.tee $l11
                      f32.div
                      local.set $l9
                      local.get $l13
                      local.get $l11
                      f32.div
                    end
                    local.set $l8
                    local.get $l36
                    local.get $p6
                    i32.const 56
                    i32.add
                    local.get $l14
                    f32.const 0x1p-2 (;=0.25;)
                    f32.mul
                    call $f18177
                    local.tee $l11
                    local.get $l12
                    f32.const 0x1p-2 (;=0.25;)
                    f32.mul
                    call $f18177
                    local.tee $l13
                    local.get $l8
                    f32.abs
                    local.tee $l12
                    local.get $l10
                    f32.const 0x1p-2 (;=0.25;)
                    f32.mul
                    call $f18177
                    local.tee $l8
                    f32.add
                    f32.const 0x1p+0 (;=1;)
                    local.get $l12
                    local.get $l8
                    f32.mul
                    f32.sub
                    f32.div
                    local.get $l11
                    f32.div
                    local.tee $l11
                    local.get $l11
                    f32.mul
                    local.get $l9
                    f32.abs
                    local.tee $l9
                    local.get $l8
                    f32.add
                    f32.const 0x1p+0 (;=1;)
                    local.get $l9
                    local.get $l8
                    f32.mul
                    f32.sub
                    f32.div
                    local.get $l13
                    f32.div
                    local.tee $l8
                    local.get $l8
                    f32.mul
                    f32.add
                    f32.const 0x1p+0 (;=1;)
                    f32.le
                    i32.eqz
                    local.get $l36
                    i32.load
                    i32.load offset=20
                    call_indirect $__indirect_function_table (type $t78)
                    br $B13
                  end
                  local.get $p6
                  local.get $p6
                  f32.load offset=164
                  local.tee $l12
                  local.get $l12
                  f32.add
                  local.tee $l11
                  local.get $p6
                  f32.load offset=168
                  local.tee $l9
                  f32.mul
                  local.tee $l10
                  local.get $p6
                  f32.load offset=160
                  local.tee $l16
                  local.get $l16
                  f32.add
                  local.tee $l8
                  local.get $p6
                  f32.load offset=172
                  local.tee $l18
                  f32.mul
                  local.tee $l13
                  f32.sub
                  f32.store offset=84
                  local.get $l41
                  local.get $l10
                  local.get $l13
                  f32.add
                  f32.store
                  f32.const 0x1p+0 (;=1;)
                  local.set $l15
                  local.get $p6
                  f32.const 0x1p+0 (;=1;)
                  local.get $l16
                  local.get $l8
                  f32.mul
                  f32.sub
                  local.tee $l10
                  local.get $l12
                  local.get $l11
                  f32.mul
                  local.tee $l13
                  f32.sub
                  f32.store offset=88
                  local.get $p6
                  local.get $l10
                  local.get $l9
                  local.get $l9
                  local.get $l9
                  f32.add
                  local.tee $l14
                  f32.mul
                  local.tee $l17
                  f32.sub
                  f32.store offset=72
                  local.get $p6
                  local.get $l8
                  local.get $l9
                  f32.mul
                  local.tee $l10
                  local.get $l11
                  local.get $l18
                  f32.mul
                  local.tee $l11
                  f32.add
                  f32.store offset=80
                  local.get $p6
                  local.get $l8
                  local.get $l12
                  f32.mul
                  local.tee $l8
                  local.get $l14
                  local.get $l18
                  f32.mul
                  local.tee $l14
                  f32.sub
                  f32.store offset=68
                  local.get $p6
                  local.get $l10
                  local.get $l11
                  f32.sub
                  f32.store offset=64
                  local.get $p6
                  local.get $l8
                  local.get $l14
                  f32.add
                  f32.store offset=60
                  local.get $p6
                  f32.const 0x1p+0 (;=1;)
                  local.get $l13
                  f32.sub
                  local.get $l17
                  f32.sub
                  f32.store offset=56
                  f32.const 0x0p+0 (;=0;)
                  local.set $l14
                  local.get $p6
                  f32.load offset=152
                  local.set $l28
                  local.get $p6
                  f32.load offset=148
                  local.set $l29
                  local.get $p6
                  f32.load offset=144
                  local.set $l30
                  local.get $p6
                  f32.load offset=140
                  local.tee $l19
                  local.set $l8
                  local.get $p6
                  f32.load offset=136
                  local.tee $l20
                  local.set $l11
                  local.get $p6
                  f32.load offset=132
                  local.tee $l21
                  local.set $l10
                  local.get $p6
                  f32.load offset=128
                  local.tee $l22
                  local.set $l13
                  local.get $l16
                  local.get $l22
                  f32.mul
                  local.tee $l17
                  local.get $l12
                  local.get $l21
                  f32.mul
                  local.tee $l24
                  f32.add
                  local.get $l9
                  local.get $l20
                  f32.mul
                  local.tee $l25
                  f32.add
                  local.get $l18
                  local.get $l19
                  f32.mul
                  local.tee $l31
                  f32.add
                  f32.const 0x0p+0 (;=0;)
                  f32.lt
                  if $I25
                    local.get $p6
                    local.get $l19
                    f32.neg
                    local.tee $l8
                    f32.store offset=140
                    local.get $p6
                    local.get $l20
                    f32.neg
                    local.tee $l11
                    f32.store offset=136
                    local.get $p6
                    local.get $l21
                    f32.neg
                    local.tee $l10
                    f32.store offset=132
                    local.get $p6
                    local.get $l22
                    f32.neg
                    local.tee $l13
                    f32.store offset=128
                    local.get $l9
                    local.get $l11
                    f32.mul
                    local.set $l25
                    local.get $l12
                    local.get $l10
                    f32.mul
                    local.set $l24
                    local.get $l18
                    local.get $l8
                    f32.mul
                    local.set $l31
                    local.get $l16
                    local.get $l13
                    f32.mul
                    local.set $l17
                  end
                  local.get $p6
                  local.get $l8
                  local.get $l8
                  f32.mul
                  f32.const -0x1p-1 (;=-0.5;)
                  f32.add
                  local.tee $l32
                  local.get $p6
                  f32.load offset=184
                  local.get $l28
                  f32.sub
                  local.tee $l23
                  local.get $l23
                  f32.add
                  local.tee $l23
                  f32.mul
                  local.get $l8
                  local.get $l10
                  local.get $p6
                  f32.load offset=176
                  local.get $l30
                  f32.sub
                  local.tee $l26
                  local.get $l26
                  f32.add
                  local.tee $l26
                  f32.mul
                  local.get $l13
                  local.get $p6
                  f32.load offset=180
                  local.get $l29
                  f32.sub
                  local.tee $l27
                  local.get $l27
                  f32.add
                  local.tee $l27
                  f32.mul
                  f32.sub
                  f32.mul
                  f32.add
                  local.get $l11
                  local.get $l27
                  local.get $l10
                  f32.neg
                  f32.mul
                  local.get $l13
                  local.get $l26
                  f32.mul
                  f32.sub
                  local.get $l11
                  local.get $l23
                  f32.mul
                  f32.sub
                  local.tee $l33
                  f32.mul
                  f32.sub
                  f32.store offset=120
                  local.get $p6
                  local.get $l32
                  local.get $l27
                  f32.mul
                  local.get $l8
                  local.get $l13
                  local.get $l23
                  f32.mul
                  local.get $l11
                  local.get $l26
                  f32.mul
                  f32.sub
                  f32.mul
                  f32.add
                  local.get $l10
                  local.get $l33
                  f32.mul
                  f32.sub
                  f32.store offset=116
                  local.get $p6
                  local.get $l25
                  local.get $l17
                  local.get $l31
                  f32.add
                  local.get $l24
                  f32.add
                  f32.add
                  local.tee $l17
                  f32.store offset=108
                  local.get $p6
                  local.get $l10
                  local.get $l16
                  f32.mul
                  local.get $l8
                  local.get $l9
                  f32.mul
                  local.get $l11
                  local.get $l18
                  f32.mul
                  f32.sub
                  local.get $l13
                  local.get $l12
                  f32.mul
                  f32.sub
                  f32.add
                  local.tee $l24
                  f32.store offset=104
                  local.get $p6
                  local.get $l13
                  local.get $l9
                  f32.mul
                  local.get $l8
                  local.get $l12
                  f32.mul
                  local.get $l10
                  local.get $l18
                  f32.mul
                  f32.sub
                  local.get $l11
                  local.get $l16
                  f32.mul
                  f32.sub
                  f32.add
                  local.tee $l25
                  f32.store offset=100
                  local.get $p6
                  local.get $l8
                  local.get $l16
                  f32.mul
                  local.get $l13
                  local.get $l18
                  f32.mul
                  f32.sub
                  local.get $l10
                  local.get $l9
                  f32.mul
                  f32.sub
                  local.get $l11
                  local.get $l12
                  f32.mul
                  f32.add
                  local.tee $l9
                  f32.store offset=96
                  local.get $p6
                  local.get $l32
                  local.get $l26
                  f32.mul
                  local.get $l8
                  local.get $l11
                  local.get $l27
                  f32.mul
                  local.get $l10
                  local.get $l23
                  f32.mul
                  f32.sub
                  f32.mul
                  f32.add
                  local.get $l13
                  local.get $l33
                  f32.mul
                  f32.sub
                  f32.store offset=112
                  f32.const 0x0p+0 (;=0;)
                  local.set $l8
                  local.get $l9
                  f32.const 0x0p+0 (;=0;)
                  f32.ne
                  if $I26
                    local.get $l17
                    f32.const 0x1p+0 (;=1;)
                    local.get $l9
                    local.get $l9
                    f32.mul
                    f32.const 0x0p+0 (;=0;)
                    f32.add
                    local.get $l17
                    local.get $l17
                    f32.mul
                    f32.add
                    f32.sqrt
                    f32.div
                    local.tee $l11
                    f32.mul
                    local.set $l15
                    local.get $l9
                    local.get $l11
                    f32.mul
                    local.set $l14
                    local.get $l11
                    f32.const 0x0p+0 (;=0;)
                    f32.mul
                    local.set $l8
                  end
                  local.get $l9
                  local.get $l14
                  f32.mul
                  local.get $l15
                  local.get $l17
                  f32.mul
                  f32.add
                  local.get $l8
                  local.get $l25
                  f32.mul
                  local.tee $l10
                  f32.add
                  local.get $l8
                  local.get $l24
                  f32.mul
                  local.tee $l13
                  f32.add
                  local.set $l11
                  local.get $l14
                  local.get $l25
                  f32.mul
                  local.get $l15
                  local.get $l24
                  f32.mul
                  local.get $l8
                  local.get $l17
                  f32.mul
                  local.tee $l12
                  f32.sub
                  local.get $l9
                  local.get $l8
                  f32.mul
                  local.tee $l16
                  f32.sub
                  f32.add
                  local.set $l18
                  local.get $l9
                  local.get $l15
                  f32.mul
                  local.get $l14
                  local.get $l17
                  f32.mul
                  f32.sub
                  local.get $l10
                  f32.sub
                  local.get $l13
                  f32.add
                  local.set $l17
                  f32.const 0x0p+0 (;=0;)
                  local.set $l23
                  block $B27 (result f32)
                    local.get $l16
                    local.get $l15
                    local.get $l25
                    f32.mul
                    local.get $l12
                    f32.sub
                    local.get $l14
                    local.get $l24
                    f32.mul
                    f32.sub
                    f32.add
                    local.tee $l9
                    f32.const 0x0p+0 (;=0;)
                    f32.eq
                    if $I28
                      f32.const 0x1p+0 (;=1;)
                      local.set $l13
                      f32.const 0x0p+0 (;=0;)
                      local.set $l12
                      f32.const 0x0p+0 (;=0;)
                      br $B27
                    end
                    local.get $l11
                    f32.const 0x1p+0 (;=1;)
                    local.get $l11
                    local.get $l11
                    f32.mul
                    local.get $l9
                    local.get $l9
                    f32.mul
                    f32.const 0x0p+0 (;=0;)
                    f32.add
                    f32.add
                    f32.sqrt
                    f32.div
                    local.tee $l10
                    f32.mul
                    local.set $l13
                    local.get $l9
                    local.get $l10
                    f32.mul
                    local.set $l12
                    local.get $l10
                    f32.const 0x0p+0 (;=0;)
                    f32.mul
                  end
                  local.set $l10
                  local.get $l38
                  i32.const 12
                  i32.add
                  local.set $l41
                  local.get $l9
                  local.get $l10
                  f32.mul
                  local.get $l18
                  local.get $l13
                  f32.mul
                  local.get $l11
                  local.get $l10
                  f32.mul
                  f32.sub
                  local.get $l17
                  local.get $l12
                  f32.mul
                  f32.sub
                  f32.add
                  local.tee $l16
                  f32.const 0x0p+0 (;=0;)
                  f32.eq
                  if $I29 (result f32)
                    f32.const 0x1p+1 (;=2;)
                  else
                    local.get $l16
                    f32.const 0x1p+0 (;=1;)
                    local.get $l18
                    local.get $l10
                    f32.mul
                    local.get $l9
                    local.get $l12
                    f32.mul
                    local.get $l17
                    local.get $l10
                    f32.mul
                    local.get $l11
                    local.get $l13
                    f32.mul
                    f32.add
                    f32.add
                    f32.add
                    local.tee $l9
                    local.get $l9
                    f32.mul
                    local.get $l16
                    local.get $l16
                    f32.mul
                    f32.const 0x0p+0 (;=0;)
                    f32.add
                    f32.add
                    f32.sqrt
                    f32.div
                    local.tee $l11
                    f32.mul
                    local.set $l23
                    local.get $l9
                    local.get $l11
                    f32.mul
                    f32.const 0x1p+0 (;=1;)
                    f32.add
                  end
                  local.set $l11
                  local.get $l41
                  i32.const 0
                  call $f71343
                  if $I30
                    local.get $l15
                    local.get $l15
                    f32.mul
                    local.get $l8
                    local.get $l8
                    f32.mul
                    local.tee $l8
                    local.get $l8
                    local.get $l14
                    local.get $l14
                    f32.mul
                    f32.add
                    f32.add
                    f32.add
                    f32.sqrt
                    local.tee $l8
                    f32.const 0x0p+0 (;=0;)
                    f32.ne
                    if $I31
                      local.get $l15
                      f32.const 0x1p+0 (;=1;)
                      local.get $l8
                      f32.div
                      local.tee $l8
                      f32.mul
                      local.set $l15
                      local.get $l14
                      local.get $l8
                      f32.mul
                      local.set $l14
                    end
                    local.get $l38
                    f32.load offset=72
                    local.set $l8
                    local.get $l38
                    f32.load offset=76
                    local.set $l9
                    local.get $p6
                    local.get $l28
                    f32.store offset=48
                    local.get $p6
                    local.get $l29
                    f32.store offset=44
                    local.get $p6
                    local.get $l30
                    f32.store offset=40
                    local.get $p6
                    local.get $l19
                    f32.store offset=36
                    local.get $p6
                    local.get $l20
                    f32.store offset=32
                    local.get $p6
                    local.get $l21
                    f32.store offset=28
                    local.get $p6
                    local.get $l22
                    f32.store offset=24
                    local.get $l36
                    local.get $p6
                    i32.const 24
                    i32.add
                    local.get $l8
                    local.get $l9
                    local.get $l15
                    f32.const -0x1p+0 (;=-1;)
                    f32.max
                    f32.const 0x1p+0 (;=1;)
                    f32.min
                    call $f35882
                    local.tee $l10
                    local.get $l10
                    f32.add
                    local.tee $l10
                    f32.neg
                    local.get $l10
                    local.get $l14
                    f32.const 0x0p+0 (;=0;)
                    f32.lt
                    select
                    local.tee $l10
                    f32.const -0x1.47ae14p-7 (;=-0.01;)
                    f32.add
                    local.get $l8
                    f32.lt
                    local.get $l10
                    f32.const 0x1.47ae14p-7 (;=0.01;)
                    f32.add
                    local.get $l9
                    f32.gt
                    i32.or
                    local.get $l36
                    i32.load
                    i32.load offset=16
                    call_indirect $__indirect_function_table (type $t78)
                  end
                  local.get $l41
                  i32.const 1
                  call $f71343
                  if $I32
                    local.get $l38
                    f32.load offset=80
                    local.set $l8
                    local.get $l38
                    f32.load offset=84
                    local.set $l9
                    local.get $p6
                    local.get $l28
                    f32.store offset=48
                    local.get $p6
                    local.get $l29
                    f32.store offset=44
                    local.get $p6
                    local.get $l30
                    f32.store offset=40
                    local.get $p6
                    local.get $l19
                    f32.const 0x1.6a09e6p-1 (;=0.707107;)
                    f32.mul
                    local.tee $l10
                    local.get $l22
                    f32.const -0x0p+0 (;=-0;)
                    f32.mul
                    local.tee $l15
                    f32.sub
                    local.get $l21
                    f32.const -0x0p+0 (;=-0;)
                    f32.mul
                    local.tee $l14
                    f32.sub
                    local.get $l20
                    f32.const 0x1.6a09e6p-1 (;=0.707107;)
                    f32.mul
                    local.tee $l16
                    f32.add
                    f32.store offset=36
                    local.get $p6
                    local.get $l15
                    local.get $l16
                    local.get $l10
                    f32.sub
                    f32.add
                    local.get $l14
                    f32.sub
                    f32.store offset=32
                    local.get $p6
                    local.get $l19
                    f32.const -0x0p+0 (;=-0;)
                    f32.mul
                    local.tee $l10
                    local.get $l21
                    f32.const 0x1.6a09e6p-1 (;=0.707107;)
                    f32.mul
                    local.tee $l15
                    f32.add
                    local.get $l20
                    f32.const -0x0p+0 (;=-0;)
                    f32.mul
                    local.tee $l14
                    f32.add
                    local.get $l22
                    f32.const 0x1.6a09e6p-1 (;=0.707107;)
                    f32.mul
                    local.tee $l16
                    f32.add
                    f32.store offset=28
                    local.get $p6
                    local.get $l10
                    local.get $l16
                    f32.add
                    local.get $l15
                    f32.sub
                    local.get $l14
                    f32.sub
                    f32.store offset=24
                    local.get $l36
                    local.get $p6
                    i32.const 24
                    i32.add
                    local.get $l9
                    f32.neg
                    local.get $l8
                    f32.neg
                    local.get $l12
                    local.get $l13
                    f32.const 0x1p+0 (;=1;)
                    f32.add
                    call $f35884
                    f32.const 0x1p+2 (;=4;)
                    f32.mul
                    local.tee $l10
                    f32.const -0x1.47ae14p-7 (;=-0.01;)
                    f32.add
                    local.get $l8
                    f32.lt
                    local.get $l10
                    f32.const 0x1.47ae14p-7 (;=0.01;)
                    f32.add
                    local.get $l9
                    f32.gt
                    i32.or
                    local.get $l36
                    i32.load
                    i32.load offset=16
                    call_indirect $__indirect_function_table (type $t78)
                  end
                  local.get $l41
                  i32.const 2
                  call $f71343
                  if $I33
                    local.get $l38
                    f32.load offset=88
                    local.set $l8
                    local.get $l38
                    f32.load offset=92
                    local.set $l9
                    local.get $p6
                    local.get $l28
                    f32.store offset=48
                    local.get $p6
                    local.get $l29
                    f32.store offset=44
                    local.get $p6
                    local.get $l30
                    f32.store offset=40
                    local.get $p6
                    local.get $l19
                    f32.const 0x1.6a09e6p-1 (;=0.707107;)
                    f32.mul
                    local.tee $l10
                    local.get $l22
                    f32.const 0x0p+0 (;=0;)
                    f32.mul
                    local.tee $l13
                    f32.sub
                    local.get $l21
                    f32.const 0x1.6a09e6p-1 (;=0.707107;)
                    f32.mul
                    local.tee $l12
                    f32.sub
                    local.get $l20
                    f32.const 0x0p+0 (;=0;)
                    f32.mul
                    local.tee $l15
                    f32.sub
                    f32.store offset=36
                    local.get $p6
                    local.get $l22
                    f32.const 0x1.6a09e6p-1 (;=0.707107;)
                    f32.mul
                    local.tee $l14
                    local.get $l19
                    f32.const 0x0p+0 (;=0;)
                    f32.mul
                    local.tee $l16
                    local.get $l20
                    f32.const 0x1.6a09e6p-1 (;=0.707107;)
                    f32.mul
                    local.tee $l18
                    f32.add
                    f32.add
                    local.get $l21
                    f32.const 0x0p+0 (;=0;)
                    f32.mul
                    local.tee $l17
                    f32.sub
                    f32.store offset=32
                    local.get $p6
                    local.get $l10
                    local.get $l12
                    f32.add
                    local.get $l15
                    f32.add
                    local.get $l13
                    f32.sub
                    f32.store offset=28
                    local.get $p6
                    local.get $l16
                    local.get $l14
                    f32.add
                    local.get $l17
                    f32.add
                    local.get $l18
                    f32.sub
                    f32.store offset=24
                    local.get $l36
                    local.get $p6
                    i32.const 24
                    i32.add
                    local.get $l9
                    f32.neg
                    local.get $l8
                    f32.neg
                    local.get $l23
                    local.get $l11
                    call $f35884
                    f32.const 0x1p+2 (;=4;)
                    f32.mul
                    local.tee $l11
                    f32.const -0x1.47ae14p-7 (;=-0.01;)
                    f32.add
                    local.get $l8
                    f32.lt
                    local.get $l11
                    f32.const 0x1.47ae14p-7 (;=0.01;)
                    f32.add
                    local.get $l9
                    f32.gt
                    i32.or
                    local.get $l36
                    i32.load
                    i32.load offset=16
                    call_indirect $__indirect_function_table (type $t78)
                  end
                  local.get $p6
                  i32.const 112
                  i32.add
                  local.set $l44
                  i32.const 3
                  local.set $l35
                  loop $L34
                    local.get $l41
                    local.get $l35
                    call $f71343
                    i32.const 1
                    i32.eq
                    if $I35
                      local.get $l44
                      local.get $l35
                      i32.const 3
                      i32.sub
                      local.tee $l39
                      i32.const 2
                      i32.shl
                      i32.add
                      f32.load
                      local.set $l11
                      local.get $l38
                      local.get $l35
                      i32.const 3
                      i32.shl
                      i32.add
                      local.tee $l42
                      f32.load offset=76
                      local.set $l8
                      local.get $p6
                      i32.const 56
                      i32.add
                      local.get $l39
                      i32.const 12
                      i32.mul
                      i32.add
                      local.tee $l39
                      f32.load
                      local.set $l10
                      local.get $l39
                      f32.load offset=4
                      local.set $l13
                      local.get $p6
                      f32.load offset=144
                      local.set $l12
                      local.get $p6
                      f32.load offset=148
                      local.set $l15
                      local.get $p6
                      local.get $p6
                      f32.load offset=152
                      local.tee $l14
                      local.get $l42
                      f32.load offset=72
                      local.tee $l9
                      local.get $l39
                      f32.load offset=8
                      local.tee $l16
                      f32.mul
                      f32.add
                      f32.store offset=32
                      local.get $p6
                      local.get $l15
                      local.get $l9
                      local.get $l13
                      f32.mul
                      f32.add
                      f32.store offset=28
                      local.get $p6
                      local.get $l12
                      local.get $l9
                      local.get $l10
                      f32.mul
                      f32.add
                      f32.store offset=24
                      local.get $p6
                      local.get $l14
                      local.get $l8
                      local.get $l16
                      f32.mul
                      f32.add
                      f32.store offset=16
                      local.get $p6
                      local.get $l15
                      local.get $l8
                      local.get $l13
                      f32.mul
                      f32.add
                      f32.store offset=12
                      local.get $p6
                      local.get $l12
                      local.get $l8
                      local.get $l10
                      f32.mul
                      f32.add
                      f32.store offset=8
                      local.get $l36
                      local.get $p6
                      i32.const 24
                      i32.add
                      local.get $p6
                      i32.const 8
                      i32.add
                      i32.const 16711680
                      i32.const 16711680
                      i32.const 16777215
                      local.get $l8
                      local.get $l11
                      f32.lt
                      select
                      local.get $l9
                      local.get $l11
                      f32.gt
                      select
                      local.get $l36
                      i32.load
                      i32.load offset=28
                      call_indirect $__indirect_function_table (type $t4)
                    end
                    local.get $l35
                    i32.const 1
                    i32.add
                    local.tee $l35
                    i32.const 6
                    i32.ne
                    br_if $L34
                  end
                end
                local.get $p6
                i32.const 192
                i32.add
                global.set $g0
              end
              local.get $l36
              i32.const 32
              i32.add
              global.set $g0
              local.get $l40
              i32.const 1
              i32.add
              local.tee $l40
              local.get $l37
              i32.load offset=100
              i32.lt_u
              br_if $L6
            end
            local.get $p0
            i32.load offset=5980
            local.set $l36
          end
          local.get $l43
          i32.const 1
          i32.add
          local.tee $l43
          local.get $l36
          i32.lt_u
          br_if $L4
        end
      end
      local.get $p0
      i32.const 5936
      i32.add
      i32.load
      local.tee $l43
      if $I36
        local.get $p0
        i32.load offset=5932
        local.set $l36
        i32.const 0
        local.set $l40
        loop $L37
          block $B38
            local.get $l36
            local.get $l40
            i32.const 2
            i32.shl
            i32.add
            i32.load
            local.tee $l37
            local.get $l37
            i32.load
            i32.load offset=24
            call_indirect $__indirect_function_table (type $t5)
            i32.const 1
            i32.eq
            if $I39
              global.get $g0
              i32.const 32
              i32.sub
              local.tee $l35
              global.set $g0
              local.get $l37
              local.get $l34
              i32.const 72
              i32.add
              local.tee $l41
              local.get $p0
              local.tee $p6
              call $f72496
              block $B40
                local.get $l37
                i32.load offset=56
                local.get $l37
                local.get $l37
                i32.load offset=52
                local.tee $l39
                i32.const 22
                i32.shr_u
                i32.const 60
                i32.and
                i32.const 3181092
                i32.add
                i32.load
                i32.add
                i32.const 56
                i32.add
                local.get $l39
                i32.const 1
                i32.and
                select
                i32.load8_u
                i32.const 1
                i32.and
                i32.eqz
                br_if $B40
                local.get $p6
                i32.const 0
                local.get $p6
                i32.load
                i32.load offset=280
                call_indirect $__indirect_function_table (type $t13)
                local.get $p6
                i32.const 3
                local.get $p6
                i32.load
                i32.load offset=280
                call_indirect $__indirect_function_table (type $t13)
                f32.mul
                f32.const 0x0p+0 (;=0;)
                f32.eq
                br_if $B40
                block $B41 (result i32)
                  local.get $l37
                  f32.load offset=308
                  local.get $p6
                  i32.const 5148
                  i32.add
                  f32.load
                  f32.div
                  f32.const 0x1p+0 (;=1;)
                  f32.min
                  f32.const 0x1.fep+7 (;=255;)
                  f32.mul
                  local.tee $l8
                  f32.const 0x1p+32 (;=4.29497e+09;)
                  f32.lt
                  local.get $l8
                  f32.const 0x0p+0 (;=0;)
                  f32.ge
                  i32.and
                  if $I42
                    local.get $l8
                    i32.trunc_f32_u
                    br $B41
                  end
                  i32.const 0
                end
                local.tee $p6
                local.get $p6
                i32.const 8
                i32.shl
                i32.or
                local.get $p6
                i32.const 16
                i32.shl
                i32.or
                local.set $l38
                local.get $l37
                i32.load offset=312
                local.set $l42
                block $B43
                  local.get $l37
                  i32.load offset=316
                  local.tee $l39
                  i32.const 2
                  i32.and
                  if $I44
                    local.get $l37
                    i32.load offset=56
                    i32.const 96
                    i32.add
                    local.set $p6
                    br $B43
                  end
                  local.get $l37
                  i32.const -64
                  i32.sub
                  call $f71608
                  local.set $p6
                  local.get $l37
                  i32.load offset=316
                  local.set $l39
                end
                i32.const 16711680
                local.get $l38
                local.get $l42
                select
                local.set $l38
                f32.const 0x0p+0 (;=0;)
                f32.const 0x1p+0 (;=1;)
                local.get $p6
                f32.load offset=8
                local.tee $l8
                f32.div
                local.get $l8
                f32.const 0x0p+0 (;=0;)
                f32.eq
                select
                local.set $l11
                f32.const 0x0p+0 (;=0;)
                f32.const 0x1p+0 (;=1;)
                local.get $p6
                f32.load offset=4
                local.tee $l8
                f32.div
                local.get $l8
                f32.const 0x0p+0 (;=0;)
                f32.eq
                select
                local.set $l9
                f32.const 0x0p+0 (;=0;)
                f32.const 0x1p+0 (;=1;)
                local.get $p6
                f32.load
                local.tee $l8
                f32.div
                local.get $l8
                f32.const 0x0p+0 (;=0;)
                f32.eq
                select
                local.set $l10
                block $B45 (result f32)
                  local.get $l39
                  i32.const 1
                  i32.and
                  if $I46
                    local.get $l37
                    i32.load offset=56
                    f32.load offset=92
                    br $B45
                  end
                  local.get $l37
                  i32.const -64
                  i32.sub
                  call $f71606
                end
                local.set $l8
                local.get $l41
                local.get $l38
                call $f69798
                local.get $l37
                i32.const 256
                i32.add
                call $f69800
                local.set $l37
                local.get $l35
                local.get $l10
                f32.const 0x1.8p+2 (;=6;)
                f32.const 0x1p+0 (;=1;)
                local.get $l8
                f32.div
                f32.div
                local.tee $l8
                f32.mul
                local.tee $l10
                local.get $l9
                local.get $l8
                f32.mul
                local.tee $l9
                f32.add
                local.get $l11
                local.get $l8
                f32.mul
                local.tee $l8
                f32.sub
                f32.abs
                f32.sqrt
                f32.const 0x1p-1 (;=0.5;)
                f32.mul
                local.tee $l11
                f32.store offset=20
                local.get $l35
                local.get $l8
                local.get $l10
                local.get $l9
                f32.sub
                f32.add
                f32.abs
                f32.sqrt
                f32.const 0x1p-1 (;=0.5;)
                f32.mul
                local.tee $l12
                f32.store offset=16
                local.get $l35
                i32.const 1
                i32.store8 offset=24
                local.get $l35
                local.get $l11
                f32.neg
                f32.store offset=8
                local.get $l35
                local.get $l12
                f32.neg
                f32.store offset=4
                local.get $l35
                local.get $l8
                local.get $l9
                local.get $l10
                f32.sub
                f32.add
                f32.abs
                f32.sqrt
                f32.const 0x1p-1 (;=0.5;)
                f32.mul
                local.tee $l8
                f32.store offset=12
                local.get $l35
                local.get $l8
                f32.neg
                f32.store
                local.get $l37
                local.get $l35
                call $f69806
              end
              local.get $l35
              i32.const 32
              i32.add
              global.set $g0
              br $B38
            end
            global.get $g0
            i32.const -64
            i32.add
            local.tee $p6
            global.set $g0
            local.get $l37
            i32.const 20
            i32.add
            local.get $l34
            i32.const 72
            i32.add
            local.tee $l35
            local.get $p0
            local.get $l37
            call $f72096
            block $B47
              local.get $l37
              i32.load offset=56
              local.get $l37
              local.get $l37
              i32.load offset=52
              local.tee $l38
              i32.const 22
              i32.shr_u
              i32.const 60
              i32.and
              i32.const 3181092
              i32.add
              i32.load
              i32.add
              i32.const 56
              i32.add
              local.get $l38
              i32.const 1
              i32.and
              select
              i32.load8_u
              i32.const 1
              i32.and
              i32.eqz
              br_if $B47
              block $B48 (result f32)
                block $B49
                  block $B50
                    block $B51
                      local.get $p0
                      i32.const 5580
                      i32.add
                      i32.load8_u
                      i32.const 32
                      i32.and
                      i32.eqz
                      br_if $B51
                      local.get $p0
                      i32.const 5248
                      i32.add
                      i32.load8_u
                      i32.eqz
                      br_if $B51
                      local.get $p0
                      i32.const 5152
                      i32.add
                      f32.load
                      local.set $l8
                      br $B50
                    end
                    local.get $p0
                    i32.const 32
                    i32.add
                    i32.const 0
                    call $f71389
                    local.set $l8
                    local.get $p0
                    i32.load8_u offset=5580
                    i32.const 32
                    i32.and
                    i32.eqz
                    br_if $B49
                  end
                  local.get $p0
                  i32.const 5258
                  i32.add
                  i32.load8_u
                  i32.eqz
                  br_if $B49
                  local.get $p0
                  i32.const 5192
                  i32.add
                  f32.load
                  br $B48
                end
                local.get $p0
                i32.const 32
                i32.add
                i32.const 10
                call $f71389
              end
              local.set $l9
              local.get $l8
              local.get $l9
              f32.mul
              local.tee $l8
              f32.const 0x0p+0 (;=0;)
              f32.eq
              br_if $B47
              local.get $p6
              i32.const 32
              i32.add
              local.get $l37
              local.get $l37
              i32.load
              i32.load offset=76
              call_indirect $__indirect_function_table (type $t1)
              local.get $l35
              local.get $p6
              i32.const 32
              i32.add
              call $f69800
              local.set $l37
              local.get $p6
              i32.const -16776961
              i32.store offset=28
              local.get $p6
              i64.const -71777214277943296
              i64.store offset=20 align=4
              local.get $p6
              local.get $l8
              f32.store offset=16
              local.get $p6
              local.get $l8
              f32.store offset=12
              local.get $p6
              local.get $l8
              f32.store offset=8
              local.get $l37
              local.get $p6
              i32.const 8
              i32.add
              call $f69808
            end
            local.get $p6
            i32.const -64
            i32.sub
            global.set $g0
          end
          local.get $l40
          i32.const 1
          i32.add
          local.tee $l40
          local.get $l43
          i32.ne
          br_if $L37
        end
      end
      local.get $p0
      i32.const 17
      local.get $p0
      i32.load
      i32.load offset=280
      call_indirect $__indirect_function_table (type $t13)
      local.set $l8
      local.get $p0
      i32.const 18
      local.get $p0
      i32.load
      i32.load offset=280
      call_indirect $__indirect_function_table (type $t13)
      local.set $l9
      block $B52
        local.get $l8
        f32.const 0x0p+0 (;=0;)
        f32.eq
        br_if $B52
        local.get $p0
        i32.load offset=5584
        local.tee $l40
        i32.eqz
        br_if $B52
        local.get $l40
        local.get $l34
        i32.const 72
        i32.add
        i32.const -16776961
        local.get $l40
        i32.load
        i32.load offset=60
        call_indirect $__indirect_function_table (type $t2)
      end
      block $B53
        local.get $l9
        f32.const 0x0p+0 (;=0;)
        f32.eq
        br_if $B53
        local.get $p0
        i32.const 5620
        i32.add
        i32.load
        local.tee $l40
        i32.eqz
        br_if $B53
        local.get $l40
        local.get $l34
        i32.const 72
        i32.add
        i32.const -65536
        local.get $l40
        i32.load
        i32.load offset=60
        call_indirect $__indirect_function_table (type $t2)
      end
      block $B54
        local.get $p0
        i32.const 23
        local.get $p0
        i32.load
        i32.load offset=280
        call_indirect $__indirect_function_table (type $t13)
        f32.const 0x0p+0 (;=0;)
        f32.eq
        br_if $B54
        i32.const 0
        local.set $l40
        local.get $l34
        i32.const 0
        i32.store offset=56
        local.get $l34
        i64.const 0
        i64.store offset=48
        local.get $l34
        i64.const 4575657221408423936
        i64.store offset=40
        local.get $l34
        i64.const 0
        i64.store offset=32
        local.get $l34
        i32.const 72
        i32.add
        local.get $l34
        i32.const 32
        i32.add
        call $f69800
        drop
        local.get $p0
        i32.const 16
        i32.add
        local.tee $l37
        call $f72022
        local.tee $l43
        i32.eqz
        br_if $B54
        loop $L55
          local.get $l37
          local.get $l34
          i32.const 32
          i32.add
          i32.const 1
          local.get $l40
          call $f72023
          drop
          local.get $l34
          i32.const 72
          i32.add
          i32.const -256
          i32.const -16777216
          local.get $l34
          i32.load8_u offset=68
          select
          call $f69798
          drop
          local.get $l34
          local.get $l34
          i64.load offset=32
          i64.store
          local.get $l34
          local.get $l34
          i64.load offset=40
          i64.store offset=8
          local.get $l34
          i32.const 1
          i32.store8 offset=24
          local.get $l34
          local.get $l34
          i64.load offset=48
          i64.store offset=16
          local.get $l34
          i32.const 72
          i32.add
          local.get $l34
          call $f69806
          local.get $l40
          i32.const 1
          i32.add
          local.tee $l40
          local.get $l43
          i32.ne
          br_if $L55
        end
      end
      local.get $p0
      i32.const 22
      local.get $p0
      i32.load
      i32.load offset=280
      call_indirect $__indirect_function_table (type $t13)
      f32.const 0x0p+0 (;=0;)
      f32.eq
      br_if $B1
      local.get $p0
      i32.const 5580
      i32.add
      i32.load8_u
      i32.const 64
      i32.and
      if $I56 (result i32)
        local.get $p0
        i32.const 5272
        i32.add
      else
        local.get $p0
        i32.const 32
        i32.add
        call $f71443
      end
      local.tee $l40
      f32.load
      local.get $l40
      f32.load offset=12
      f32.gt
      br_if $B1
      local.get $l34
      i32.const 72
      i32.add
      i32.const -256
      call $f69798
      drop
      local.get $l34
      local.get $l40
      f32.load
      f32.store offset=32
      local.get $l34
      local.get $l40
      f32.load offset=4
      f32.store offset=36
      local.get $l34
      local.get $l40
      f32.load offset=8
      f32.store offset=40
      local.get $l34
      local.get $l40
      f32.load offset=12
      f32.store offset=44
      local.get $l34
      local.get $l40
      f32.load offset=16
      f32.store offset=48
      local.get $l34
      local.get $l40
      f32.load offset=20
      f32.store offset=52
      local.get $l34
      i32.const 1
      i32.store8 offset=56
      local.get $l34
      i32.const 72
      i32.add
      local.get $l34
      i32.const 32
      i32.add
      call $f69806
    end
    local.get $l34
    i32.const 176
    i32.add
    global.set $g0
    local.get $p0
    i32.const 5928
    i32.add
    i32.load
    if $I57
      local.get $p0
      i32.const 5896
      i32.add
      i32.load
      local.set $l36
      i32.const 0
      local.set $p6
      loop $L58
        block $B59
          local.get $l36
          local.get $p6
          i32.const 2
          i32.shl
          i32.add
          i32.load
          local.tee $l34
          i32.load8_u offset=120
          i32.eqz
          br_if $B59
          local.get $l34
          i32.const 28
          i32.add
          local.get $l34
          i32.load offset=56
          local.tee $l35
          local.get $l35
          i32.load
          i32.load
          call_indirect $__indirect_function_table (type $t5)
          call $f71667
          i32.eqz
          br_if $B59
          local.get $l34
          i32.const 0
          i32.store8 offset=120
        end
        local.get $p6
        i32.const 1
        i32.add
        local.tee $p6
        local.get $p0
        i32.load offset=5928
        i32.lt_u
        br_if $L58
      end
    end
    local.get $p0
    i32.load offset=1008
    local.set $p6
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l35
    global.set $g0
    local.get $p6
    local.get $p4
    i32.store offset=20
    local.get $p6
    local.get $p3
    i32.store offset=16
    local.get $p6
    i32.const 8
    i32.add
    local.tee $l34
    local.get $l34
    i32.load
    i32.const 1
    i32.sub
    local.tee $l34
    i32.store
    local.get $p6
    i32.load offset=4
    local.set $l36
    local.get $l35
    local.get $p3
    local.get $p4
    i32.add
    local.tee $p3
    i32.store offset=12
    block $B60
      local.get $l34
      local.get $p6
      i32.load offset=12
      i32.const 2147483647
      i32.and
      i32.ge_u
      if $I61
        local.get $p6
        i32.const 4
        i32.add
        local.get $l35
        i32.const 12
        i32.add
        call $f72370
        br $B60
      end
      local.get $l36
      local.get $l34
      i32.const 2
      i32.shl
      i32.add
      local.get $p3
      i32.store
      local.get $p6
      local.get $p6
      i32.load offset=8
      i32.const 1
      i32.add
      i32.store offset=8
    end
    local.get $l35
    i32.const 16
    i32.add
    global.set $g0
    local.get $p0
    local.get $p1
    f32.store offset=6072
    local.get $p0
    i32.const 16
    i32.add
    local.set $p6
    local.get $p7
    i32.const 1
    i32.eq
    if $I62
      local.get $p0
      i32.const 1112
      i32.add
      local.get $p1
      f32.store
      local.get $p0
      i32.const 1116
      i32.add
      f32.const 0x1p+0 (;=1;)
      local.get $p1
      f32.div
      f32.const 0x0p+0 (;=0;)
      local.get $p1
      f32.const 0x0p+0 (;=0;)
      f32.gt
      select
      f32.store
    end
    local.get $p0
    local.get $p5
    i32.store8 offset=6320
    local.get $p0
    local.get $p0
    i32.load
    i32.load offset=28
    call_indirect $__indirect_function_table (type $t5)
    i32.load offset=40
    local.set $l41
    i32.const 0
    local.set $l42
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l43
    global.set $g0
    local.get $p6
    i32.load offset=4780
    drop
    local.get $p6
    i32.const 4768
    i32.add
    local.set $l38
    local.get $p6
    i32.const 4772
    i32.add
    i32.load
    if $I63
      local.get $p6
      i32.const 16
      i32.add
      local.set $l34
      loop $L64
        local.get $l41
        local.get $l38
        i32.load
        local.get $l42
        i32.const 3
        i32.shl
        i32.add
        local.tee $l36
        i32.load16_u
        local.tee $p3
        i32.const 2
        i32.shl
        i32.add
        i32.load
        local.set $p4
        block $B65
          block $B66
            block $B67
              block $B68
                local.get $l36
                i32.load offset=4
                br_table $B68 $B67 $B66 $B65
              end
              local.get $p4
              i32.eqz
              br_if $B65
              i32.const 0
              local.set $l40
              i32.const 0
              local.set $p3
              local.get $l34
              i32.load offset=4
              local.tee $l39
              local.get $p4
              i32.load16_u offset=52
              local.tee $l36
              i32.const 1
              i32.add
              local.tee $l35
              i32.lt_u
              if $I69
                local.get $l34
                local.get $l35
                i32.const 31
                i32.add
                i32.const -32
                i32.and
                local.tee $l35
                i32.store offset=4
                call $f69753
                local.tee $l37
                local.get $l35
                i32.const 5
                i32.shl
                i32.const 19
                i32.or
                i32.const 3181558
                i32.const 3181624
                i32.const 100
                local.get $l37
                i32.load
                i32.load offset=8
                call_indirect $__indirect_function_table (type $t9)
                local.tee $l35
                if $I70
                  local.get $l35
                  i32.const 19
                  i32.add
                  i32.const -16
                  i32.and
                  local.tee $l40
                  i32.const 4
                  i32.sub
                  local.get $l40
                  local.get $l35
                  i32.sub
                  i32.store
                end
                local.get $l39
                if $I71
                  loop $L72
                    local.get $l40
                    local.get $p3
                    i32.const 5
                    i32.shl
                    local.tee $l37
                    i32.add
                    local.tee $l35
                    local.get $l34
                    i32.load
                    local.get $l37
                    i32.add
                    local.tee $l37
                    i64.load
                    i64.store
                    local.get $l35
                    local.get $l37
                    i32.load offset=8
                    i32.store offset=8
                    local.get $l35
                    local.get $l37
                    i32.load16_u offset=12
                    i32.store16 offset=12
                    local.get $l35
                    local.get $l37
                    i32.load16_u offset=14
                    i32.store16 offset=14
                    local.get $l35
                    local.get $l37
                    i64.load offset=16
                    i64.store offset=16
                    local.get $p3
                    i32.const 1
                    i32.add
                    local.tee $p3
                    local.get $l39
                    i32.ne
                    br_if $L72
                  end
                end
                local.get $l34
                i32.load offset=4
                local.get $l39
                i32.gt_u
                if $I73
                  loop $L74
                    local.get $l40
                    local.get $l39
                    i32.const 5
                    i32.shl
                    i32.add
                    i32.const 65535
                    i32.store16 offset=20
                    local.get $l39
                    i32.const 1
                    i32.add
                    local.tee $l39
                    local.get $l34
                    i32.load offset=4
                    i32.lt_u
                    br_if $L74
                  end
                end
                local.get $l34
                i32.load
                local.tee $l35
                if $I75
                  local.get $l35
                  i32.const 4
                  i32.sub
                  i32.load
                  local.set $l37
                  call $f69753
                  local.tee $l39
                  local.get $l35
                  local.get $l37
                  i32.sub
                  local.get $l39
                  i32.load
                  i32.load offset=12
                  call_indirect $__indirect_function_table (type $t1)
                end
                local.get $l34
                local.get $l40
                i32.store
              end
              local.get $l34
              i32.load
              local.get $l36
              i32.const 5
              i32.shl
              i32.add
              local.tee $l36
              local.get $p4
              i64.load offset=32
              i64.store
              local.get $l36
              local.get $p4
              i32.load offset=40
              i32.store offset=8
              local.get $l36
              local.get $p4
              i32.load16_u offset=44
              i32.store16 offset=12
              local.get $l36
              local.get $p4
              i32.load16_u offset=46
              i32.store16 offset=14
              local.get $l36
              local.get $p4
              i64.load offset=48
              i64.store offset=16
              local.get $l34
              i32.load offset=976
              i32.load offset=1024
              local.tee $p3
              local.get $p4
              i32.const 32
              i32.add
              local.get $p3
              i32.load
              i32.load offset=52
              call_indirect $__indirect_function_table (type $t1)
              br $B65
            end
            local.get $p4
            i32.eqz
            br_if $B65
            local.get $l34
            i32.load
            local.get $p4
            i32.load16_u offset=52
            i32.const 5
            i32.shl
            i32.add
            local.tee $l36
            local.get $p4
            i64.load offset=32
            i64.store
            local.get $l36
            local.get $p4
            i32.load offset=40
            i32.store offset=8
            local.get $l36
            local.get $p4
            i32.load16_u offset=44
            i32.store16 offset=12
            local.get $l36
            local.get $p4
            i32.load16_u offset=46
            i32.store16 offset=14
            local.get $l36
            local.get $p4
            i64.load offset=48
            i64.store offset=16
            local.get $l34
            i32.load offset=976
            i32.load offset=1024
            local.tee $p3
            local.get $p4
            i32.const 32
            i32.add
            local.get $p3
            i32.load
            i32.load offset=56
            call_indirect $__indirect_function_table (type $t1)
            br $B65
          end
          local.get $p6
          i32.load offset=20
          local.get $p3
          i32.le_u
          br_if $B65
          local.get $l34
          i32.load
          local.get $p3
          i32.const 5
          i32.shl
          i32.add
          local.tee $p4
          i32.load16_u offset=20
          local.get $p3
          i32.ne
          br_if $B65
          local.get $l34
          i32.load offset=976
          i32.load offset=1024
          local.tee $p3
          local.get $p4
          local.get $p3
          i32.load
          i32.load offset=60
          call_indirect $__indirect_function_table (type $t1)
          local.get $p4
          i32.const 65535
          i32.store16 offset=20
        end
        local.get $l42
        i32.const 1
        i32.add
        local.tee $l42
        local.get $p6
        i32.load offset=4772
        i32.lt_u
        br_if $L64
      end
    end
    local.get $l43
    i32.const 8
    i32.add
    local.set $l41
    local.get $l38
    i32.load offset=8
    i32.const 2147483647
    i32.and
    i32.const 0
    i32.lt_u
    if $I76
      i32.const 0
      local.set $p4
      local.get $l38
      i32.load offset=4
      local.tee $p3
      i32.const 0
      i32.gt_s
      if $I77
        local.get $p3
        i32.const 3
        i32.shl
        local.set $l34
        local.get $l38
        i32.load
        local.set $p3
        loop $L78
          local.get $p4
          local.get $p3
          i64.load align=4
          i64.store align=4
          local.get $p3
          i32.const 8
          i32.add
          local.set $p3
          local.get $p4
          i32.const 8
          i32.add
          local.tee $p4
          local.get $l34
          i32.lt_u
          br_if $L78
        end
      end
      block $B79
        local.get $l38
        i32.load offset=8
        i32.const 0
        i32.lt_s
        br_if $B79
        local.get $l38
        i32.load
        local.tee $p3
        i32.eqz
        br_if $B79
        call $f69753
        local.tee $p4
        local.get $p3
        local.get $p4
        i32.load
        i32.load offset=12
        call_indirect $__indirect_function_table (type $t1)
      end
      local.get $l38
      i32.const 0
      i32.store offset=8
      local.get $l38
      i32.const 0
      i32.store
    end
    local.get $l38
    i32.load offset=4
    local.tee $p3
    i32.const 0
    i32.lt_s
    if $I80
      local.get $l38
      i32.load
      local.tee $l34
      local.get $p3
      i32.const 3
      i32.shl
      i32.add
      local.set $p3
      loop $L81
        local.get $p3
        local.get $l41
        i64.load align=4
        i64.store align=4
        local.get $p3
        i32.const 8
        i32.add
        local.tee $p3
        local.get $l34
        i32.lt_u
        br_if $L81
      end
    end
    local.get $l38
    i32.const 0
    i32.store offset=4
    local.get $p6
    i32.load offset=4780
    drop
    local.get $l43
    i32.const 16
    i32.add
    global.set $g0
    local.get $p0
    i32.const 1
    i32.store8 offset=6353
    local.get $p0
    i32.const 4801
    i32.add
    i32.const 1
    i32.store8
    local.get $p0
    local.get $p7
    i32.store offset=4648
    local.get $p5
    if $I82
      local.get $p0
      i32.load offset=6092
      local.tee $p6
      local.get $p6
      i32.load
      i32.load offset=8
      call_indirect $__indirect_function_table (type $t7)
      local.get $p0
      i32.load offset=6092
      local.tee $p6
      local.get $p6
      i32.load
      i32.load offset=12
      call_indirect $__indirect_function_table (type $t7)
    end
    local.get $p7
    i32.const 1
    i32.eq
    if $I83
      local.get $p0
      i32.const 6160
      i32.add
      i32.const 1
      i32.store
      local.get $p0
      i32.const 6156
      i32.add
      local.get $p2
      i32.store
      local.get $p0
      i32.const 6152
      i32.add
      local.get $p0
      i32.load offset=6092
      i32.store
      local.get $p0
      i32.const 6136
      i32.add
      local.set $p6
      local.get $p2
      if $I84
        local.get $p2
        local.get $p2
        i32.load
        i32.load offset=16
        call_indirect $__indirect_function_table (type $t7)
      end
      local.get $p0
      i32.const 6260
      i32.add
      local.tee $l34
      local.get $p6
      i32.store
      local.get $p0
      i32.const 6264
      i32.add
      i32.const 1
      i32.store
      local.get $p6
      local.get $p0
      i32.load offset=6136
      i32.load offset=16
      call_indirect $__indirect_function_table (type $t7)
      local.get $p0
      i32.const 6256
      i32.add
      local.tee $l35
      local.get $l34
      i32.load
      i32.load offset=16
      i32.store
      local.get $p0
      i32.const 6128
      i32.add
      i32.const 1
      i32.store
      local.get $p0
      i32.const 6124
      i32.add
      i32.const 0
      i32.store
      local.get $p0
      i32.const 6120
      i32.add
      local.get $p0
      i32.load offset=6092
      i32.store
      local.get $p0
      i32.load offset=6152
      local.tee $l34
      local.get $p6
      local.get $l34
      i32.load
      i32.load offset=72
      call_indirect $__indirect_function_table (type $t1)
      local.get $l35
      i32.load
      local.tee $p6
      local.get $p0
      i32.const 6240
      i32.add
      local.get $p6
      i32.load
      i32.load offset=72
      call_indirect $__indirect_function_table (type $t1)
      return
    end
    local.get $p0
    i32.const 6128
    i32.add
    i32.const 1
    i32.store
    local.get $p0
    i32.const 6124
    i32.add
    local.get $p2
    i32.store
    local.get $p0
    i32.const 6120
    i32.add
    local.get $p0
    i32.load offset=6092
    local.tee $l34
    i32.store
    local.get $p0
    i32.const 6104
    i32.add
    local.set $p6
    local.get $p2
    if $I85
      local.get $p2
      local.get $p2
      i32.load
      i32.load offset=16
      call_indirect $__indirect_function_table (type $t7)
      local.get $p0
      i32.load offset=6092
      local.set $l34
    end
    local.get $p0
    i32.const 6220
    i32.add
    local.get $p6
    i32.store
    local.get $p0
    i32.const 6224
    i32.add
    i32.const 1
    i32.store
    local.get $p0
    i32.const 6216
    i32.add
    local.tee $l35
    local.get $l34
    i32.store
    local.get $p6
    local.get $p0
    i32.load offset=6104
    i32.load offset=16
    call_indirect $__indirect_function_table (type $t7)
    local.get $p0
    i32.load offset=6120
    local.tee $l34
    local.get $p6
    local.get $l34
    i32.load
    i32.load offset=72
    call_indirect $__indirect_function_table (type $t1)
    local.get $l35
    i32.load
    local.tee $p6
    local.get $p0
    i32.const 6200
    i32.add
    local.get $p6
    i32.load
    i32.load offset=72
    call_indirect $__indirect_function_table (type $t1))
