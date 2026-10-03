  (func $f73070 (type $t7) (param $p0 i32)
    (local $l1 i32) (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 f32) (local $l6 f32) (local $l7 f32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32) (local $l33 f32) (local $l34 f32) (local $l35 f32)
    global.get $g0
    i32.const 128
    i32.sub
    local.tee $l1
    global.set $g0
    i32.const 9
    call $f80140
    call $f73714
    local.get $p0
    i32.load offset=136
    local.set $l3
    local.get $p0
    i32.load offset=28
    i32.const 4131408
    call $f80185
    local.set $l2
    local.get $l1
    i32.const 96
    i32.add
    local.get $p0
    i32.load offset=52
    local.tee $l4
    local.get $l4
    i32.load
    i32.load offset=112
    call_indirect $__indirect_function_table (type $t1)
    local.get $l1
    local.get $l2
    call $f78093
    local.get $l1
    f32.load
    local.set $l24
    local.get $l1
    f32.load offset=4
    local.set $l26
    local.get $l1
    f32.load offset=8
    local.set $l27
    local.get $l1
    i32.const -64
    i32.sub
    local.get $l2
    call $f78150
    local.get $l1
    f32.load offset=72
    local.set $l17
    local.get $l1
    f32.load offset=76
    local.set $l16
    local.get $l1
    f32.load offset=64
    local.set $l18
    local.get $l1
    f32.load offset=68
    local.set $l19
    local.get $l1
    i32.const -64
    i32.sub
    local.get $p0
    i32.load offset=52
    local.tee $l2
    local.get $l2
    i32.load
    i32.load offset=76
    call_indirect $__indirect_function_table (type $t1)
    local.get $l1
    f32.load offset=84
    local.set $l33
    local.get $l1
    f32.load offset=88
    local.set $l34
    local.get $l1
    f32.load offset=120
    local.set $l14
    local.get $l1
    f32.load offset=116
    local.set $l13
    local.get $l1
    f32.load offset=104
    local.set $l10
    local.get $l1
    f32.load offset=100
    local.set $l11
    local.get $l1
    f32.load offset=108
    local.set $l7
    local.get $l1
    f32.load offset=96
    local.set $l15
    local.get $l1
    f32.load offset=80
    local.set $l25
    local.get $l1
    f32.load offset=72
    local.set $l12
    local.get $l1
    f32.load offset=76
    local.set $l5
    local.get $l1
    f32.load offset=64
    local.set $l8
    local.get $l1
    f32.load offset=68
    local.set $l9
    local.get $l1
    f32.load offset=112
    local.set $l6
    local.get $l1
    i32.const 48
    i32.add
    local.get $p0
    i32.load offset=52
    local.tee $l2
    local.get $l2
    i32.load
    i32.load offset=156
    call_indirect $__indirect_function_table (type $t1)
    local.get $l5
    local.get $l5
    f32.mul
    f32.const -0x1p-1 (;=-0.5;)
    f32.add
    local.set $l23
    local.get $l12
    local.get $l14
    local.get $l14
    f32.add
    local.tee $l14
    f32.mul
    local.get $l8
    local.get $l6
    local.get $l6
    f32.add
    local.tee $l6
    f32.mul
    local.get $l9
    local.get $l13
    local.get $l13
    f32.add
    local.tee $l13
    f32.mul
    f32.add
    f32.add
    local.set $l20
    local.get $l16
    local.get $l16
    f32.mul
    f32.const -0x1p-1 (;=-0.5;)
    f32.add
    local.set $l21
    local.get $l17
    local.get $l14
    f32.mul
    local.get $l18
    local.get $l6
    f32.mul
    local.get $l19
    local.get $l13
    f32.mul
    f32.add
    f32.add
    local.set $l22
    local.get $l3
    i32.const 2
    i32.and
    if $I0 (result f32)
      local.get $l1
      i32.const 0
      i32.store offset=48
      local.get $l24
      local.get $l18
      local.get $l22
      f32.mul
      local.get $l6
      local.get $l21
      f32.mul
      local.get $l16
      local.get $l19
      local.get $l14
      f32.mul
      local.get $l13
      local.get $l17
      f32.mul
      f32.sub
      f32.mul
      f32.add
      f32.add
      f32.add
    else
      local.get $l25
      local.get $l8
      local.get $l20
      f32.mul
      local.get $l6
      local.get $l23
      f32.mul
      local.get $l5
      local.get $l9
      local.get $l14
      f32.mul
      local.get $l13
      local.get $l12
      f32.mul
      f32.sub
      f32.mul
      f32.add
      f32.add
      f32.add
    end
    local.set $l35
    local.get $l15
    local.get $l8
    f32.mul
    local.set $l24
    local.get $l5
    local.get $l7
    f32.mul
    local.set $l25
    local.get $l7
    local.get $l12
    f32.mul
    local.set $l28
    local.get $l5
    local.get $l10
    f32.mul
    local.set $l29
    local.get $l7
    local.get $l9
    f32.mul
    local.set $l30
    local.get $l5
    local.get $l11
    f32.mul
    local.set $l31
    local.get $l7
    local.get $l8
    f32.mul
    local.set $l7
    local.get $l5
    local.get $l15
    f32.mul
    local.set $l32
    local.get $l3
    i32.const 4
    i32.and
    if $I1 (result f32)
      local.get $l1
      i32.const 0
      i32.store offset=52
      local.get $l26
      local.get $l19
      local.get $l22
      f32.mul
      local.get $l13
      local.get $l21
      f32.mul
      local.get $l16
      local.get $l17
      local.get $l6
      f32.mul
      local.get $l14
      local.get $l18
      f32.mul
      f32.sub
      f32.mul
      f32.add
      f32.add
      f32.add
    else
      local.get $l33
      local.get $l9
      local.get $l20
      f32.mul
      local.get $l13
      local.get $l23
      f32.mul
      local.get $l5
      local.get $l12
      local.get $l6
      f32.mul
      local.get $l14
      local.get $l8
      f32.mul
      f32.sub
      f32.mul
      f32.add
      f32.add
      f32.add
    end
    local.set $l26
    local.get $l25
    local.get $l24
    f32.sub
    local.set $l24
    local.get $l9
    local.get $l11
    f32.mul
    local.set $l25
    local.get $l29
    local.get $l28
    f32.add
    local.set $l28
    local.get $l8
    local.get $l11
    f32.mul
    local.set $l29
    local.get $l31
    local.get $l30
    f32.add
    local.set $l30
    local.get $l12
    local.get $l15
    f32.mul
    local.set $l31
    local.get $l32
    local.get $l7
    f32.add
    local.set $l7
    local.get $l9
    local.get $l10
    f32.mul
    local.set $l32
    local.get $l3
    i32.const 8
    i32.and
    if $I2 (result f32)
      local.get $l1
      i32.const 0
      i32.store offset=56
      local.get $l27
      local.get $l17
      local.get $l22
      f32.mul
      local.get $l14
      local.get $l21
      f32.mul
      local.get $l16
      local.get $l18
      local.get $l13
      f32.mul
      local.get $l6
      local.get $l19
      f32.mul
      f32.sub
      f32.mul
      f32.add
      f32.add
      f32.add
    else
      local.get $l34
      local.get $l12
      local.get $l20
      f32.mul
      local.get $l14
      local.get $l23
      f32.mul
      local.get $l5
      local.get $l8
      local.get $l13
      f32.mul
      local.get $l6
      local.get $l9
      f32.mul
      f32.sub
      f32.mul
      f32.add
      f32.add
      f32.add
    end
    local.set $l27
    local.get $l24
    local.get $l25
    f32.sub
    local.set $l5
    local.get $l12
    local.get $l10
    f32.mul
    local.set $l14
    local.get $l29
    local.get $l28
    f32.add
    local.set $l6
    local.get $l15
    local.get $l9
    f32.mul
    local.set $l9
    local.get $l31
    local.get $l30
    f32.add
    local.set $l15
    local.get $l10
    local.get $l8
    f32.mul
    local.set $l8
    local.get $l32
    local.get $l7
    f32.add
    local.set $l10
    local.get $l11
    local.get $l12
    f32.mul
    local.set $l11
    local.get $p0
    i32.load8_u offset=133
    i32.eqz
    if $I3
      local.get $p0
      i32.load offset=52
      local.tee $l2
      local.get $l1
      i32.const 48
      i32.add
      i32.const 0
      local.get $l2
      i32.load
      i32.load offset=160
      call_indirect $__indirect_function_table (type $t2)
    end
    local.get $l5
    local.get $l14
    f32.sub
    local.set $l5
    local.get $l6
    local.get $l9
    f32.sub
    local.set $l12
    local.get $l15
    local.get $l8
    f32.sub
    local.set $l8
    local.get $l10
    local.get $l11
    f32.sub
    local.set $l9
    block $B4
      local.get $l3
      i32.const 112
      i32.and
      i32.eqz
      if $I5
        local.get $l5
        local.get $l5
        f32.mul
        f32.const -0x1p-1 (;=-0.5;)
        f32.add
        local.set $l14
        local.get $l8
        f32.neg
        local.set $l20
        local.get $l9
        f32.neg
        local.set $l21
        local.get $l12
        f32.neg
        local.set $l22
        br $B4
      end
      local.get $l1
      local.get $p0
      i32.load offset=52
      local.tee $l2
      local.get $l2
      i32.load
      i32.load offset=164
      call_indirect $__indirect_function_table (type $t1)
      local.get $l1
      f32.load offset=8
      local.set $l10
      local.get $l1
      f32.load offset=4
      local.set $l11
      local.get $l1
      f32.load
      local.set $l7
      local.get $l1
      local.get $p0
      i32.load offset=52
      local.tee $l2
      local.get $l2
      i32.load
      i32.load offset=132
      call_indirect $__indirect_function_table (type $t1)
      local.get $l10
      local.get $l10
      f32.add
      local.tee $l10
      local.get $l5
      local.get $l5
      f32.mul
      f32.const -0x1p-1 (;=-0.5;)
      f32.add
      local.tee $l14
      f32.mul
      local.get $l5
      local.get $l9
      local.get $l11
      local.get $l11
      f32.add
      local.tee $l11
      f32.mul
      local.get $l7
      local.get $l7
      f32.add
      local.tee $l7
      local.get $l8
      f32.mul
      f32.sub
      f32.mul
      f32.sub
      local.set $l6
      local.get $l12
      local.get $l12
      local.get $l10
      f32.mul
      local.get $l9
      local.get $l7
      f32.mul
      local.get $l8
      local.get $l11
      f32.mul
      f32.add
      f32.add
      local.tee $l16
      f32.mul
      local.set $l13
      f32.const 0x0p+0 (;=0;)
      local.set $l15
      block $B6
        local.get $l3
        i32.const 4
        i32.shr_u
        local.get $l1
        f32.load
        f32.const 0x0p+0 (;=0;)
        f32.gt
        i32.and
        local.tee $l2
        i32.eqz
        if $I7
          local.get $l9
          local.get $l16
          f32.mul
          local.get $l7
          local.get $l14
          f32.mul
          local.get $l5
          local.get $l8
          local.get $l10
          f32.mul
          local.get $l11
          local.get $l12
          f32.mul
          f32.sub
          f32.mul
          f32.sub
          f32.add
          local.set $l15
          br $B6
        end
        local.get $l1
        i32.const 0
        i32.store
      end
      local.get $l13
      local.get $l6
      f32.add
      local.set $l6
      local.get $l8
      f32.neg
      local.set $l20
      local.get $l9
      f32.neg
      local.set $l21
      local.get $l12
      f32.neg
      local.set $l22
      block $B8
        block $B9
          block $B10
            local.get $l3
            i32.const 32
            i32.and
            if $I11
              f32.const 0x0p+0 (;=0;)
              local.set $l13
              local.get $l1
              f32.load offset=4
              f32.const 0x0p+0 (;=0;)
              f32.gt
              br_if $B10
            end
            local.get $l8
            local.get $l16
            f32.mul
            local.get $l11
            local.get $l14
            f32.mul
            local.get $l5
            local.get $l12
            local.get $l7
            f32.mul
            local.get $l10
            local.get $l9
            f32.mul
            f32.sub
            f32.mul
            f32.sub
            f32.add
            local.set $l13
            local.get $l3
            i32.const 64
            i32.and
            if $I12
              local.get $l1
              f32.load offset=8
              f32.const 0x0p+0 (;=0;)
              f32.gt
              br_if $B9
            end
            local.get $l2
            br_if $B8
            br $B4
          end
          local.get $l1
          i32.const 0
          i32.store offset=4
          local.get $l3
          i32.const 64
          i32.and
          i32.eqz
          br_if $B8
          local.get $l1
          f32.load offset=8
          f32.const 0x0p+0 (;=0;)
          f32.gt
          i32.eqz
          br_if $B8
        end
        local.get $l1
        i32.const 0
        i32.store offset=8
        f32.const 0x0p+0 (;=0;)
        local.set $l6
      end
      local.get $p0
      i32.load offset=52
      local.tee $l3
      local.get $l1
      local.get $l3
      i32.load
      i32.load offset=128
      call_indirect $__indirect_function_table (type $t1)
      local.get $p0
      i32.load8_u offset=133
      br_if $B4
      local.get $p0
      i32.load offset=52
      local.set $l3
      local.get $l1
      local.get $l12
      local.get $l12
      local.get $l6
      local.get $l6
      f32.add
      local.tee $l10
      f32.mul
      local.get $l9
      local.get $l15
      local.get $l15
      f32.add
      local.tee $l11
      f32.mul
      local.get $l8
      local.get $l13
      local.get $l13
      f32.add
      local.tee $l7
      f32.mul
      f32.add
      f32.add
      local.tee $l15
      f32.mul
      local.get $l10
      local.get $l14
      f32.mul
      local.get $l5
      local.get $l9
      local.get $l7
      f32.mul
      local.get $l11
      local.get $l20
      f32.mul
      f32.add
      f32.mul
      f32.add
      f32.add
      f32.store offset=40
      local.get $l1
      local.get $l8
      local.get $l15
      f32.mul
      local.get $l7
      local.get $l14
      f32.mul
      local.get $l5
      local.get $l12
      local.get $l11
      f32.mul
      local.get $l10
      local.get $l21
      f32.mul
      f32.add
      f32.mul
      f32.add
      f32.add
      f32.store offset=36
      local.get $l1
      local.get $l9
      local.get $l15
      f32.mul
      local.get $l11
      local.get $l14
      f32.mul
      local.get $l5
      local.get $l8
      local.get $l10
      f32.mul
      local.get $l7
      local.get $l22
      f32.mul
      f32.add
      f32.mul
      f32.add
      f32.add
      f32.store offset=32
      local.get $l3
      local.get $l1
      i32.const 32
      i32.add
      i32.const 1
      local.get $l3
      i32.load
      i32.load offset=168
      call_indirect $__indirect_function_table (type $t2)
    end
    local.get $p0
    i32.load offset=52
    local.set $p0
    local.get $l1
    local.get $l27
    local.get $l12
    local.get $l12
    local.get $l1
    f32.load offset=104
    local.tee $l11
    local.get $l11
    local.get $l1
    f32.load offset=120
    f32.const -0x1p+1 (;=-2;)
    f32.mul
    local.tee $l6
    f32.mul
    local.get $l1
    f32.load offset=96
    local.tee $l7
    local.get $l1
    f32.load offset=112
    f32.const -0x1p+1 (;=-2;)
    f32.mul
    local.tee $l13
    f32.mul
    local.get $l1
    f32.load offset=116
    f32.const -0x1p+1 (;=-2;)
    f32.mul
    local.tee $l16
    local.get $l1
    f32.load offset=100
    local.tee $l15
    f32.mul
    f32.add
    f32.add
    local.tee $l19
    f32.mul
    local.get $l6
    local.get $l1
    f32.load offset=108
    local.tee $l10
    local.get $l10
    f32.mul
    f32.const -0x1p-1 (;=-0.5;)
    f32.add
    local.tee $l23
    f32.mul
    local.get $l10
    local.get $l7
    local.get $l16
    f32.mul
    local.get $l13
    local.get $l15
    f32.mul
    f32.sub
    f32.mul
    f32.sub
    f32.add
    local.tee $l17
    local.get $l17
    f32.add
    local.tee $l17
    f32.mul
    local.get $l9
    local.get $l7
    local.get $l19
    f32.mul
    local.get $l13
    local.get $l23
    f32.mul
    local.get $l10
    local.get $l15
    local.get $l6
    f32.mul
    local.get $l16
    local.get $l11
    f32.mul
    f32.sub
    f32.mul
    f32.sub
    f32.add
    local.tee $l18
    local.get $l18
    f32.add
    local.tee $l18
    f32.mul
    local.get $l8
    local.get $l15
    local.get $l19
    f32.mul
    local.get $l16
    local.get $l23
    f32.mul
    local.get $l10
    local.get $l11
    local.get $l13
    f32.mul
    local.get $l6
    local.get $l7
    f32.mul
    f32.sub
    f32.mul
    f32.sub
    f32.add
    local.tee $l6
    local.get $l6
    f32.add
    local.tee $l6
    f32.mul
    f32.add
    f32.add
    local.tee $l13
    f32.mul
    local.get $l17
    local.get $l14
    f32.mul
    local.get $l5
    local.get $l9
    local.get $l6
    f32.mul
    local.get $l18
    local.get $l20
    f32.mul
    f32.add
    f32.mul
    f32.add
    f32.add
    f32.add
    f32.store offset=24
    local.get $l1
    local.get $l26
    local.get $l8
    local.get $l13
    f32.mul
    local.get $l6
    local.get $l14
    f32.mul
    local.get $l5
    local.get $l12
    local.get $l18
    f32.mul
    local.get $l17
    local.get $l21
    f32.mul
    f32.add
    f32.mul
    f32.add
    f32.add
    f32.add
    f32.store offset=20
    local.get $l1
    local.get $l12
    local.get $l11
    f32.mul
    local.get $l8
    local.get $l15
    f32.mul
    local.get $l5
    local.get $l10
    f32.mul
    local.get $l9
    local.get $l7
    f32.mul
    f32.add
    f32.add
    f32.add
    f32.store offset=12
    local.get $l1
    local.get $l7
    local.get $l8
    f32.mul
    local.get $l12
    local.get $l10
    f32.mul
    local.get $l5
    local.get $l11
    f32.mul
    f32.sub
    local.get $l9
    local.get $l15
    f32.mul
    f32.sub
    f32.add
    f32.store offset=8
    local.get $l1
    local.get $l11
    local.get $l9
    f32.mul
    local.get $l8
    local.get $l10
    f32.mul
    local.get $l5
    local.get $l15
    f32.mul
    f32.sub
    local.get $l12
    local.get $l7
    f32.mul
    f32.sub
    f32.add
    f32.store offset=4
    local.get $l1
    local.get $l15
    local.get $l12
    f32.mul
    local.get $l9
    local.get $l10
    f32.mul
    local.get $l5
    local.get $l7
    f32.mul
    f32.sub
    local.get $l8
    local.get $l11
    f32.mul
    f32.sub
    f32.add
    f32.store
    local.get $l1
    local.get $l35
    local.get $l9
    local.get $l13
    f32.mul
    local.get $l18
    local.get $l14
    f32.mul
    local.get $l5
    local.get $l8
    local.get $l17
    f32.mul
    local.get $l6
    local.get $l22
    f32.mul
    f32.add
    f32.mul
    f32.add
    f32.add
    f32.add
    f32.store offset=16
    local.get $p0
    local.get $l1
    i32.const 0
    local.get $p0
    i32.load
    i32.load offset=80
    call_indirect $__indirect_function_table (type $t2)
    local.get $l1
    i32.const 128
    i32.add
    global.set $g0)