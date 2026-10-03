  (func $f73054 (type $t6) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32)
    (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 i32) (local $l17 i32) (local $l18 i32) (local $l19 i32) (local $l20 i32) (local $l21 i32) (local $l22 i32) (local $l23 i32) (local $l24 i32) (local $l25 i32) (local $l26 i32) (local $l27 i32) (local $l28 i32) (local $l29 i32) (local $l30 i32) (local $l31 f32) (local $l32 f32) (local $l33 f32) (local $l34 f32) (local $l35 f32) (local $l36 f32) (local $l37 f32) (local $l38 f32) (local $l39 f32) (local $l40 f32) (local $l41 f32) (local $l42 f32) (local $l43 f32) (local $l44 f32) (local $l45 f32) (local $l46 f32) (local $l47 f32) (local $l48 f32) (local $l49 f32) (local $l50 f32) (local $l51 f32) (local $l52 f32) (local $l53 f32) (local $l54 f32) (local $l55 f32) (local $l56 f32) (local $l57 f32) (local $l58 f32) (local $l59 f32) (local $l60 f32) (local $l61 f32) (local $l62 f32) (local $l63 f32) (local $l64 f32) (local $l65 f32) (local $l66 f32) (local $l67 f32) (local $l68 f32) (local $l69 f32) (local $l70 f32) (local $l71 f32) (local $l72 f32) (local $l73 f32) (local $l74 f32) (local $l75 f32) (local $l76 f32) (local $l77 f32) (local $l78 f32) (local $l79 f32) (local $l80 f32)
    global.get $g0
    i32.const 288
    i32.sub
    local.tee $p0
    global.set $g0
    block $B0
      local.get $p1
      i32.load offset=8
      local.tee $l8
      i32.eqz
      if $I1
        f32.const inf (;=inf;)
        local.set $l54
        f32.const -inf (;=-inf;)
        local.set $l60
        f32.const -inf (;=-inf;)
        local.set $l55
        f32.const -inf (;=-inf;)
        local.set $l61
        f32.const -inf (;=-inf;)
        local.set $l62
        f32.const -inf (;=-inf;)
        local.set $l68
        f32.const -inf (;=-inf;)
        local.set $l69
        f32.const -inf (;=-inf;)
        local.set $l70
        f32.const -inf (;=-inf;)
        local.set $l71
        f32.const -inf (;=-inf;)
        local.set $l72
        f32.const -inf (;=-inf;)
        local.set $l73
        f32.const -inf (;=-inf;)
        local.set $l74
        f32.const -inf (;=-inf;)
        local.set $l75
        f32.const inf (;=inf;)
        local.set $l76
        f32.const inf (;=inf;)
        local.set $l77
        f32.const inf (;=inf;)
        local.set $l78
        f32.const inf (;=inf;)
        local.set $l79
        f32.const inf (;=inf;)
        local.set $l80
        f32.const inf (;=inf;)
        local.set $l36
        f32.const inf (;=inf;)
        local.set $l37
        f32.const inf (;=inf;)
        local.set $l38
        f32.const inf (;=inf;)
        local.set $l39
        f32.const inf (;=inf;)
        local.set $l41
        f32.const inf (;=inf;)
        local.set $l42
        br $B0
      end
      local.get $p1
      i32.load
      local.set $l14
      f32.const -inf (;=-inf;)
      local.set $l75
      f32.const inf (;=inf;)
      local.set $l42
      f32.const inf (;=inf;)
      local.set $l41
      f32.const inf (;=inf;)
      local.set $l39
      f32.const inf (;=inf;)
      local.set $l38
      f32.const inf (;=inf;)
      local.set $l37
      f32.const inf (;=inf;)
      local.set $l36
      f32.const inf (;=inf;)
      local.set $l80
      f32.const inf (;=inf;)
      local.set $l79
      f32.const inf (;=inf;)
      local.set $l78
      f32.const inf (;=inf;)
      local.set $l77
      f32.const inf (;=inf;)
      local.set $l76
      f32.const inf (;=inf;)
      local.set $l54
      f32.const -inf (;=-inf;)
      local.set $l74
      f32.const -inf (;=-inf;)
      local.set $l73
      f32.const -inf (;=-inf;)
      local.set $l72
      f32.const -inf (;=-inf;)
      local.set $l71
      f32.const -inf (;=-inf;)
      local.set $l70
      f32.const -inf (;=-inf;)
      local.set $l69
      f32.const -inf (;=-inf;)
      local.set $l68
      f32.const -inf (;=-inf;)
      local.set $l62
      f32.const -inf (;=-inf;)
      local.set $l61
      f32.const -inf (;=-inf;)
      local.set $l55
      f32.const -inf (;=-inf;)
      local.set $l60
      loop $L2
        local.get $l60
        local.get $l14
        local.get $l7
        i32.const 160
        i32.mul
        i32.add
        local.tee $l5
        f32.load offset=16
        local.tee $l31
        local.get $l31
        local.get $l60
        f32.lt
        select
        local.tee $l33
        local.get $l5
        f32.load offset=64
        local.tee $l32
        local.get $l32
        local.get $l33
        f32.lt
        select
        local.set $l60
        local.get $l54
        local.get $l31
        local.get $l31
        local.get $l54
        f32.gt
        select
        local.tee $l31
        local.get $l32
        local.get $l31
        local.get $l32
        f32.lt
        select
        local.set $l54
        local.get $l75
        local.get $l5
        f32.load offset=60
        local.tee $l31
        local.get $l31
        local.get $l75
        f32.lt
        select
        local.tee $l33
        local.get $l5
        f32.load offset=108
        local.tee $l32
        local.get $l32
        local.get $l33
        f32.lt
        select
        local.set $l75
        local.get $l74
        local.get $l5
        f32.load offset=56
        local.tee $l33
        local.get $l33
        local.get $l74
        f32.lt
        select
        local.tee $l35
        local.get $l5
        f32.load offset=104
        local.tee $l34
        local.get $l34
        local.get $l35
        f32.lt
        select
        local.set $l74
        local.get $l73
        local.get $l5
        f32.load offset=52
        local.tee $l35
        local.get $l35
        local.get $l73
        f32.lt
        select
        local.tee $l40
        local.get $l5
        f32.load offset=100
        local.tee $l43
        local.get $l40
        local.get $l43
        f32.gt
        select
        local.set $l73
        local.get $l72
        local.get $l5
        f32.load offset=48
        local.tee $l40
        local.get $l40
        local.get $l72
        f32.lt
        select
        local.tee $l44
        local.get $l5
        f32.load offset=96
        local.tee $l51
        local.get $l44
        local.get $l51
        f32.gt
        select
        local.set $l72
        local.get $l71
        local.get $l5
        f32.load offset=44
        local.tee $l44
        local.get $l44
        local.get $l71
        f32.lt
        select
        local.tee $l45
        local.get $l5
        f32.load offset=92
        local.tee $l52
        local.get $l45
        local.get $l52
        f32.gt
        select
        local.set $l71
        local.get $l70
        local.get $l5
        f32.load offset=40
        local.tee $l45
        local.get $l45
        local.get $l70
        f32.lt
        select
        local.tee $l47
        local.get $l5
        f32.load offset=88
        local.tee $l63
        local.get $l47
        local.get $l63
        f32.gt
        select
        local.set $l70
        local.get $l69
        local.get $l5
        f32.load offset=36
        local.tee $l47
        local.get $l47
        local.get $l69
        f32.lt
        select
        local.tee $l48
        local.get $l5
        f32.load offset=84
        local.tee $l56
        local.get $l48
        local.get $l56
        f32.gt
        select
        local.set $l69
        local.get $l68
        local.get $l5
        f32.load offset=32
        local.tee $l48
        local.get $l48
        local.get $l68
        f32.lt
        select
        local.tee $l49
        local.get $l5
        f32.load offset=80
        local.tee $l57
        local.get $l49
        local.get $l57
        f32.gt
        select
        local.set $l68
        local.get $l62
        local.get $l5
        f32.load offset=28
        local.tee $l49
        local.get $l49
        local.get $l62
        f32.lt
        select
        local.tee $l58
        local.get $l5
        f32.load offset=76
        local.tee $l46
        local.get $l46
        local.get $l58
        f32.lt
        select
        local.set $l62
        local.get $l61
        local.get $l5
        f32.load offset=24
        local.tee $l58
        local.get $l58
        local.get $l61
        f32.lt
        select
        local.tee $l59
        local.get $l5
        f32.load offset=72
        local.tee $l64
        local.get $l59
        local.get $l64
        f32.gt
        select
        local.set $l61
        local.get $l55
        local.get $l5
        f32.load offset=20
        local.tee $l59
        local.get $l55
        local.get $l59
        f32.gt
        select
        local.tee $l55
        local.get $l5
        f32.load offset=68
        local.tee $l65
        local.get $l55
        local.get $l65
        f32.gt
        select
        local.set $l55
        local.get $l42
        local.get $l31
        local.get $l31
        local.get $l42
        f32.gt
        select
        local.tee $l31
        local.get $l32
        local.get $l31
        local.get $l32
        f32.lt
        select
        local.set $l42
        local.get $l41
        local.get $l33
        local.get $l33
        local.get $l41
        f32.gt
        select
        local.tee $l31
        local.get $l34
        local.get $l31
        local.get $l34
        f32.lt
        select
        local.set $l41
        local.get $l39
        local.get $l35
        local.get $l35
        local.get $l39
        f32.gt
        select
        local.tee $l31
        local.get $l43
        local.get $l31
        local.get $l43
        f32.lt
        select
        local.set $l39
        local.get $l38
        local.get $l40
        local.get $l38
        local.get $l40
        f32.lt
        select
        local.tee $l31
        local.get $l51
        local.get $l31
        local.get $l51
        f32.lt
        select
        local.set $l38
        local.get $l37
        local.get $l44
        local.get $l37
        local.get $l44
        f32.lt
        select
        local.tee $l31
        local.get $l52
        local.get $l31
        local.get $l52
        f32.lt
        select
        local.set $l37
        local.get $l36
        local.get $l45
        local.get $l36
        local.get $l45
        f32.lt
        select
        local.tee $l31
        local.get $l63
        local.get $l31
        local.get $l63
        f32.lt
        select
        local.set $l36
        local.get $l80
        local.get $l47
        local.get $l47
        local.get $l80
        f32.gt
        select
        local.tee $l31
        local.get $l56
        local.get $l31
        local.get $l56
        f32.lt
        select
        local.set $l80
        local.get $l79
        local.get $l48
        local.get $l48
        local.get $l79
        f32.gt
        select
        local.tee $l31
        local.get $l57
        local.get $l31
        local.get $l57
        f32.lt
        select
        local.set $l79
        local.get $l78
        local.get $l49
        local.get $l49
        local.get $l78
        f32.gt
        select
        local.tee $l31
        local.get $l46
        local.get $l31
        local.get $l46
        f32.lt
        select
        local.set $l78
        local.get $l77
        local.get $l58
        local.get $l58
        local.get $l77
        f32.gt
        select
        local.tee $l31
        local.get $l64
        local.get $l31
        local.get $l64
        f32.lt
        select
        local.set $l77
        local.get $l76
        local.get $l59
        local.get $l59
        local.get $l76
        f32.gt
        select
        local.tee $l31
        local.get $l65
        local.get $l31
        local.get $l65
        f32.lt
        select
        local.set $l76
        local.get $l66
        local.get $l5
        f32.load offset=112
        local.tee $l31
        local.get $l31
        local.get $l66
        f32.lt
        select
        local.set $l66
        local.get $l50
        local.get $l5
        f32.load offset=124
        local.tee $l31
        local.get $l31
        local.get $l50
        f32.lt
        select
        local.set $l50
        local.get $l53
        local.get $l5
        f32.load offset=120
        local.tee $l31
        local.get $l31
        local.get $l53
        f32.lt
        select
        local.set $l53
        local.get $l67
        local.get $l5
        f32.load offset=116
        local.tee $l31
        local.get $l31
        local.get $l67
        f32.lt
        select
        local.set $l67
        local.get $l7
        i32.const 1
        i32.add
        local.tee $l7
        local.get $l8
        i32.ne
        br_if $L2
      end
    end
    local.get $l38
    local.get $l39
    call $f65476
    local.get $l41
    local.get $l42
    call $f65476
    call $f65476
    local.set $l32
    local.get $p0
    local.get $l66
    local.get $l67
    call $f65475
    local.get $l53
    local.get $l50
    call $f65475
    call $f65475
    local.tee $l31
    local.get $l72
    local.get $l73
    call $f65475
    local.get $l74
    local.get $l75
    call $f65475
    call $f65475
    f32.add
    f32.const 0x1.4f8b58p-17 (;=1e-05;)
    f32.add
    local.tee $l33
    local.get $l32
    local.get $l31
    f32.sub
    f32.const -0x1.4f8b58p-17 (;=-1e-05;)
    f32.add
    local.tee $l32
    f32.sub
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.store offset=284
    local.get $l79
    local.get $l80
    call $f65476
    local.get $l36
    local.get $l37
    call $f65476
    call $f65476
    local.set $l34
    local.get $p0
    local.get $l31
    local.get $l68
    local.get $l69
    call $f65475
    local.get $l70
    local.get $l71
    call $f65475
    call $f65475
    f32.add
    f32.const 0x1.4f8b58p-17 (;=1e-05;)
    f32.add
    local.tee $l35
    local.get $l34
    local.get $l31
    f32.sub
    f32.const -0x1.4f8b58p-17 (;=-1e-05;)
    f32.add
    local.tee $l34
    f32.sub
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.store offset=280
    local.get $l54
    local.get $l76
    call $f65476
    local.get $l77
    local.get $l78
    call $f65476
    call $f65476
    local.set $l43
    local.get $p0
    local.get $l31
    local.get $l60
    local.get $l55
    call $f65475
    local.get $l61
    local.get $l62
    call $f65475
    call $f65475
    f32.add
    f32.const 0x1.4f8b58p-17 (;=1e-05;)
    f32.add
    local.tee $l40
    local.get $l43
    local.get $l31
    f32.sub
    f32.const -0x1.4f8b58p-17 (;=-1e-05;)
    f32.add
    local.tee $l31
    f32.sub
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.store offset=276
    local.get $p0
    local.get $l32
    local.get $l33
    f32.add
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.store offset=272
    local.get $p0
    local.get $l34
    local.get $l35
    f32.add
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.store offset=268
    local.get $p0
    local.get $l31
    local.get $l40
    f32.add
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.store offset=264
    local.get $p0
    i64.const 4294967296
    i64.store offset=256
    local.get $p0
    i64.const 4294967296
    i64.store offset=248
    local.get $p0
    i64.const 4294967296
    i64.store offset=240
    local.get $p0
    i64.const 4294967296
    i64.store offset=232
    local.get $p0
    i64.const 4294967296
    i64.store offset=224
    local.get $p0
    i64.const 4294967296
    i64.store offset=216
    local.get $p3
    if $I3
      local.get $p0
      i32.const 248
      i32.add
      local.get $p3
      i32.const 16
      i32.const 4
      call $f545
      local.get $p0
      i32.const 232
      i32.add
      local.get $p3
      i32.const 24
      i32.const 4
      call $f545
      local.get $p0
      i32.const 216
      i32.add
      local.get $p3
      i32.const 4
      i32.const 4
      call $f545
      i32.const 0
      local.set $l5
      loop $L4
        block $B5
          local.get $p2
          local.get $l5
          i32.const 2
          i32.shl
          i32.add
          local.tee $l8
          i32.load
          i32.load offset=28
          local.tee $l7
          i32.eqz
          br_if $B5
          local.get $l7
          call $f80180
          i32.eqz
          br_if $B5
          local.get $p0
          i32.const -1
          i32.store offset=128
          local.get $p0
          local.get $l8
          i32.load
          i32.load offset=40
          local.tee $l7
          i32.store offset=124
          local.get $l7
          i32.eqz
          br_if $B5
          local.get $p0
          local.get $l7
          local.get $l7
          i32.load
          i32.load offset=72
          call_indirect $__indirect_function_table (type $t5)
          i32.store offset=120
          local.get $p0
          i32.const 168
          i32.add
          local.get $p0
          i32.const 120
          i32.add
          call $f73052
          local.get $p0
          i32.const 168
          i32.add
          local.get $p0
          i32.const 264
          i32.add
          call $f65650
          i32.eqz
          br_if $B5
          local.get $p0
          i32.load offset=256
          local.tee $l7
          i32.const 1
          i32.add
          local.tee $l8
          local.get $p0
          i32.load offset=260
          i32.const 1
          i32.shr_u
          i32.gt_u
          if $I6
            local.get $p0
            i32.const 248
            i32.add
            call $f65734
          end
          local.get $p0
          local.get $l8
          i32.store offset=256
          local.get $p0
          i32.load offset=248
          local.get $l7
          i32.const 4
          i32.shl
          i32.add
          local.tee $l7
          local.get $p0
          i64.load offset=120
          i64.store align=4
          local.get $l7
          local.get $p0
          i64.load offset=128
          i64.store offset=8 align=4
          local.get $p0
          i32.load offset=240
          local.tee $l7
          i32.const 1
          i32.add
          local.tee $l8
          local.get $p0
          i32.load offset=244
          i32.const 1
          i32.shr_u
          i32.gt_u
          if $I7
            local.get $p0
            i32.const 232
            i32.add
            call $f66310
          end
          local.get $p0
          local.get $l8
          i32.store offset=240
          local.get $p0
          i32.load offset=232
          local.get $l7
          i32.const 24
          i32.mul
          i32.add
          local.tee $l7
          local.get $p0
          f32.load offset=168
          f32.store
          local.get $l7
          local.get $p0
          f32.load offset=172
          f32.store offset=4
          local.get $l7
          local.get $p0
          f32.load offset=176
          f32.store offset=8
          local.get $l7
          local.get $p0
          f32.load offset=180
          f32.store offset=12
          local.get $l7
          local.get $p0
          f32.load offset=184
          f32.store offset=16
          local.get $l7
          local.get $p0
          f32.load offset=188
          f32.store offset=20
          local.get $p0
          i32.load offset=224
          local.tee $l7
          i32.const 1
          i32.add
          local.tee $l8
          local.get $p0
          i32.load offset=228
          i32.const 1
          i32.shr_u
          i32.gt_u
          if $I8
            local.get $p0
            i32.const 216
            i32.add
            call $f552
          end
          local.get $p0
          local.get $l8
          i32.store offset=224
          local.get $p0
          i32.load offset=216
          local.get $l7
          i32.const 2
          i32.shl
          i32.add
          local.get $l5
          i32.store
        end
        local.get $l5
        i32.const 1
        i32.add
        local.tee $l5
        local.get $p3
        i32.ne
        br_if $L4
      end
    end
    block $B9
      local.get $p0
      i32.load offset=256
      local.tee $l8
      i32.eqz
      br_if $B9
      local.get $p1
      i32.load offset=8
      i32.eqz
      br_if $B9
      local.get $p0
      i32.const 88
      i32.add
      local.set $l20
      local.get $p0
      i32.const 72
      i32.add
      local.set $l21
      local.get $p0
      i32.const 152
      i32.add
      local.set $l22
      local.get $p0
      i32.const 136
      i32.add
      local.set $l23
      local.get $p0
      i32.const 200
      i32.add
      local.set $l24
      local.get $p0
      i32.const 184
      i32.add
      local.set $l25
      loop $L10
        local.get $p1
        i32.load
        local.get $l17
        i32.const 160
        i32.mul
        i32.add
        local.tee $l5
        f32.load offset=20
        local.set $l31
        local.get $l5
        f32.load offset=68
        local.set $l49
        local.get $l5
        f32.load offset=24
        local.set $l32
        local.get $l5
        f32.load offset=72
        local.set $l57
        local.get $l5
        f32.load offset=28
        local.set $l33
        local.get $l5
        f32.load offset=76
        local.set $l48
        local.get $l5
        i32.const 32
        i32.add
        local.tee $p3
        f32.load
        local.set $l34
        local.get $l5
        f32.load offset=80
        local.set $l46
        local.get $l5
        f32.load offset=36
        local.set $l35
        local.get $l5
        f32.load offset=84
        local.set $l56
        local.get $l5
        f32.load offset=40
        local.set $l43
        local.get $l5
        f32.load offset=88
        local.set $l58
        local.get $l5
        f32.load offset=44
        local.set $l40
        local.get $l5
        f32.load offset=92
        local.set $l64
        local.get $l5
        i32.const 48
        i32.add
        local.tee $p2
        f32.load
        local.set $l51
        local.get $l5
        f32.load offset=96
        local.set $l59
        local.get $l5
        f32.load offset=52
        local.set $l44
        local.get $l5
        f32.load offset=100
        local.set $l65
        local.get $l5
        f32.load offset=56
        local.set $l52
        local.get $l5
        f32.load offset=104
        local.set $l66
        local.get $l5
        f32.load offset=60
        local.set $l45
        local.get $l5
        f32.load offset=108
        local.set $l47
        local.get $p0
        local.get $l5
        f32.load offset=64
        local.get $l5
        f32.load offset=16
        local.tee $l54
        f32.sub
        local.tee $l63
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        local.tee $l60
        local.get $l54
        f32.add
        f32.store offset=168
        local.get $p0
        local.get $l45
        local.get $l47
        local.get $l45
        f32.sub
        local.tee $l47
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        local.tee $l54
        f32.add
        f32.store offset=212
        local.get $p0
        local.get $l52
        local.get $l66
        local.get $l52
        f32.sub
        local.tee $l45
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        local.tee $l66
        f32.add
        f32.store offset=208
        local.get $p0
        local.get $l44
        local.get $l65
        local.get $l44
        f32.sub
        local.tee $l52
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        local.tee $l65
        f32.add
        f32.store offset=204
        local.get $p0
        local.get $l51
        local.get $l59
        local.get $l51
        f32.sub
        local.tee $l44
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        local.tee $l59
        f32.add
        f32.store offset=200
        local.get $p0
        local.get $l40
        local.get $l64
        local.get $l40
        f32.sub
        local.tee $l51
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        local.tee $l64
        f32.add
        f32.store offset=196
        local.get $p0
        local.get $l43
        local.get $l58
        local.get $l43
        f32.sub
        local.tee $l40
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        local.tee $l58
        f32.add
        f32.store offset=192
        local.get $p0
        local.get $l35
        local.get $l56
        local.get $l35
        f32.sub
        local.tee $l56
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        local.tee $l43
        f32.add
        f32.store offset=188
        local.get $p0
        local.get $l34
        local.get $l46
        local.get $l34
        f32.sub
        local.tee $l35
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        local.tee $l46
        f32.add
        f32.store offset=184
        local.get $p0
        local.get $l33
        local.get $l48
        local.get $l33
        f32.sub
        local.tee $l48
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        local.tee $l55
        f32.add
        f32.store offset=180
        local.get $p0
        local.get $l32
        local.get $l57
        local.get $l32
        f32.sub
        local.tee $l57
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        local.tee $l61
        f32.add
        f32.store offset=176
        local.get $p0
        local.get $l31
        local.get $l49
        local.get $l31
        f32.sub
        local.tee $l49
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        local.tee $l62
        f32.add
        f32.store offset=172
        local.get $l5
        f32.load offset=112
        local.set $l31
        local.get $l5
        f32.load offset=116
        local.set $l32
        local.get $l5
        f32.load offset=120
        local.set $l33
        local.get $p0
        local.get $l54
        f32.abs
        local.get $l5
        f32.load offset=124
        local.tee $l34
        f32.add
        f32.store offset=164
        local.get $p0
        local.get $l33
        local.get $l66
        f32.abs
        f32.add
        f32.store offset=160
        local.get $p0
        local.get $l32
        local.get $l65
        f32.abs
        f32.add
        f32.store offset=156
        local.get $p0
        local.get $l31
        local.get $l59
        f32.abs
        f32.add
        f32.store offset=152
        local.get $p0
        local.get $l34
        local.get $l64
        f32.abs
        f32.add
        f32.store offset=148
        local.get $p0
        local.get $l33
        local.get $l58
        f32.abs
        f32.add
        f32.store offset=144
        local.get $p0
        local.get $l32
        local.get $l43
        f32.abs
        f32.add
        f32.store offset=140
        local.get $p0
        local.get $l31
        local.get $l46
        f32.abs
        f32.add
        f32.store offset=136
        local.get $p0
        local.get $l34
        local.get $l55
        f32.abs
        f32.add
        f32.store offset=132
        local.get $p0
        local.get $l33
        local.get $l61
        f32.abs
        f32.add
        f32.store offset=128
        local.get $p0
        local.get $l32
        local.get $l62
        f32.abs
        f32.add
        f32.store offset=124
        local.get $p0
        local.get $l31
        local.get $l60
        f32.abs
        f32.add
        f32.store offset=120
        block $B11
          local.get $p0
          i32.const 168
          i32.add
          local.get $p0
          i32.const 120
          i32.add
          local.get $p0
          i32.load offset=232
          local.get $l8
          call $f65447
          i32.eqz
          br_if $B11
          local.get $l5
          i32.const 112
          i32.add
          local.set $l14
          local.get $l5
          i32.const 16
          i32.add
          local.set $l26
          local.get $p0
          local.get $l63
          local.get $l63
          f32.mul
          local.get $l35
          local.get $l35
          f32.mul
          local.get $l44
          local.get $l44
          f32.mul
          f32.add
          f32.add
          f32.sqrt
          local.tee $l31
          f32.store offset=104
          local.get $p0
          local.get $l49
          local.get $l49
          f32.mul
          local.get $l56
          local.get $l56
          f32.mul
          local.get $l52
          local.get $l52
          f32.mul
          f32.add
          f32.add
          f32.sqrt
          local.tee $l32
          f32.store offset=108
          local.get $p0
          local.get $l57
          local.get $l57
          f32.mul
          local.get $l40
          local.get $l40
          f32.mul
          local.get $l45
          local.get $l45
          f32.mul
          f32.add
          f32.add
          f32.sqrt
          local.tee $l33
          f32.store offset=112
          local.get $p0
          local.get $l48
          local.get $l48
          f32.mul
          local.get $l51
          local.get $l51
          f32.mul
          local.get $l47
          local.get $l47
          f32.mul
          f32.add
          f32.add
          f32.sqrt
          local.tee $l46
          f32.store offset=116
          local.get $p0
          local.get $l44
          local.get $l31
          f32.div
          f32.const 0x0p+0 (;=0;)
          local.get $l31
          f32.const 0x1.203afap-50 (;=1e-15;)
          f32.gt
          local.tee $l7
          select
          local.tee $l34
          f32.store offset=88
          local.get $p0
          local.get $l35
          local.get $l31
          f32.div
          f32.const 0x1p+0 (;=1;)
          local.get $l7
          select
          local.tee $l35
          f32.store offset=72
          local.get $p0
          local.get $l63
          local.get $l31
          f32.div
          f32.const 0x0p+0 (;=0;)
          local.get $l7
          select
          local.tee $l43
          f32.store offset=56
          local.get $p0
          local.get $l47
          local.get $l46
          f32.div
          f32.const 0x0p+0 (;=0;)
          local.get $l46
          f32.const 0x1.203afap-50 (;=1e-15;)
          f32.gt
          local.tee $l7
          select
          f32.store offset=100
          local.get $p0
          local.get $l45
          local.get $l33
          f32.div
          f32.const 0x0p+0 (;=0;)
          local.get $l33
          f32.const 0x1.203afap-50 (;=1e-15;)
          f32.gt
          local.tee $l11
          select
          f32.store offset=96
          local.get $p0
          local.get $l52
          local.get $l32
          f32.div
          f32.const 0x0p+0 (;=0;)
          local.get $l32
          f32.const 0x1.203afap-50 (;=1e-15;)
          f32.gt
          local.tee $l12
          select
          f32.store offset=92
          local.get $p0
          local.get $l51
          local.get $l46
          f32.div
          f32.const 0x1p+0 (;=1;)
          local.get $l7
          select
          f32.store offset=84
          local.get $p0
          local.get $l40
          local.get $l33
          f32.div
          f32.const 0x1p+0 (;=1;)
          local.get $l11
          select
          f32.store offset=80
          local.get $p0
          local.get $l56
          local.get $l32
          f32.div
          f32.const 0x1p+0 (;=1;)
          local.get $l12
          select
          f32.store offset=76
          local.get $p0
          local.get $l48
          local.get $l46
          f32.div
          f32.const 0x0p+0 (;=0;)
          local.get $l7
          select
          f32.store offset=68
          local.get $p0
          local.get $l57
          local.get $l33
          f32.div
          f32.const 0x0p+0 (;=0;)
          local.get $l11
          select
          f32.store offset=64
          local.get $p0
          local.get $l49
          local.get $l32
          f32.div
          f32.const 0x0p+0 (;=0;)
          local.get $l12
          select
          f32.store offset=60
          local.get $l5
          i32.const 128
          i32.add
          local.set $l11
          local.get $l5
          i32.const 144
          i32.add
          local.set $l12
          i32.const 0
          local.set $l7
          loop $L12
            local.get $l26
            local.get $l7
            i32.const 2
            i32.shl
            local.tee $l5
            i32.add
            f32.load
            local.set $l32
            local.get $p3
            local.get $l5
            i32.add
            f32.load
            local.set $l33
            local.get $p0
            local.get $p2
            local.get $l5
            i32.add
            f32.load
            f32.store offset=48
            local.get $p0
            local.get $l33
            f32.store offset=44
            local.get $p0
            local.get $l32
            f32.store offset=40
            local.get $p0
            local.get $l34
            f32.store offset=32
            local.get $p0
            local.get $l35
            f32.store offset=28
            local.get $p0
            local.get $l43
            f32.store offset=24
            local.get $l5
            local.get $l25
            i32.add
            f32.load
            local.set $l32
            local.get $l5
            local.get $l24
            i32.add
            f32.load
            local.set $l33
            local.get $l5
            local.get $l23
            i32.add
            f32.load
            local.set $l34
            local.get $p0
            local.get $l5
            local.get $l22
            i32.add
            f32.load
            f32.store offset=20
            local.get $p0
            local.get $l34
            f32.store offset=16
            local.get $p0
            local.get $p0
            i32.const 120
            i32.add
            local.get $l5
            i32.add
            f32.load
            f32.store offset=12
            local.get $p0
            local.get $l33
            f32.store offset=8
            local.get $p0
            local.get $l32
            f32.store offset=4
            local.get $p0
            local.get $p0
            i32.const 168
            i32.add
            local.get $l5
            i32.add
            f32.load
            f32.store
            local.get $l5
            local.get $l11
            i32.add
            block $B13 (result i32)
              local.get $p0
              i32.const 24
              i32.add
              local.set $l27
              local.get $l5
              local.get $l14
              i32.add
              f32.load
              local.set $l36
              local.get $p0
              i32.load offset=248
              local.set $l28
              local.get $p0
              i32.load offset=232
              local.set $l29
              local.get $p0
              i32.load offset=216
              local.set $l18
              i32.const 0
              local.set $l15
              global.get $g0
              i32.const 240
              i32.sub
              local.tee $l6
              global.set $g0
              local.get $l6
              local.get $l36
              f32.store offset=92
              local.get $l6
              i32.const 0
              i32.store offset=88
              local.get $l6
              i64.const 4575657221408423936
              i64.store offset=64
              local.get $l6
              i64.const 0
              i64.store offset=56
              local.get $l6
              local.get $p0
              i32.const 40
              i32.add
              local.tee $l9
              f32.load
              f32.store offset=72
              local.get $l6
              local.get $l9
              f32.load offset=4
              f32.store offset=76
              local.get $l6
              local.get $l9
              f32.load offset=8
              f32.store offset=80
              local.get $l5
              local.get $l12
              i32.add
              local.tee $l16
              i32.const 0
              i32.store
              block $B14
                local.get $l8
                i32.eqz
                br_if $B14
                local.get $l6
                i32.const 24
                i32.add
                local.tee $l19
                i32.const 8
                i32.add
                local.set $l30
                i32.const 0
                local.set $l9
                block $B15
                  loop $L16
                    block $B17
                      block $B18
                        local.get $p0
                        local.get $l29
                        local.get $l9
                        i32.const 24
                        i32.mul
                        i32.add
                        call $f65651
                        i32.eqz
                        br_if $B18
                        local.get $l28
                        local.get $l9
                        i32.const 4
                        i32.shl
                        i32.add
                        local.tee $l13
                        i32.load offset=4
                        local.tee $l10
                        i32.eqz
                        br_if $B18
                        local.get $l6
                        i32.const 0
                        i32.store16 offset=20
                        local.get $l6
                        i32.const -1
                        i32.store offset=16
                        local.get $l6
                        i64.const 0
                        i64.store offset=8
                        local.get $l19
                        i64.const 0
                        i64.store offset=16 align=4
                        local.get $l30
                        i64.const 0
                        i64.store align=4
                        local.get $l19
                        i64.const 0
                        i64.store align=4
                        local.get $l6
                        i32.const 2139095039
                        i32.store offset=48
                        local.get $l13
                        i32.load
                        local.set $l13
                        local.get $l6
                        i32.const 136
                        i32.add
                        local.get $l10
                        local.get $l10
                        i32.load
                        i32.load offset=40
                        call_indirect $__indirect_function_table (type $t1)
                        local.get $l6
                        local.get $l6
                        i32.const 136
                        i32.add
                        i32.store offset=208
                        local.get $l6
                        i32.load offset=208
                        local.set $l5
                        local.get $l6
                        i32.const 208
                        i32.add
                        local.get $l13
                        local.get $l13
                        i32.load
                        i32.load offset=76
                        call_indirect $__indirect_function_table (type $t1)
                        local.get $l6
                        i32.const 176
                        i32.add
                        local.get $l10
                        local.get $l10
                        i32.load
                        i32.load offset=80
                        call_indirect $__indirect_function_table (type $t1)
                        local.get $l6
                        local.get $l6
                        f32.load offset=220
                        local.tee $l36
                        local.get $l6
                        f32.load offset=188
                        local.tee $l37
                        f32.mul
                        local.get $l6
                        f32.load offset=176
                        local.tee $l38
                        local.get $l6
                        f32.load offset=208
                        local.tee $l41
                        f32.mul
                        f32.sub
                        local.get $l6
                        f32.load offset=212
                        local.tee $l42
                        local.get $l6
                        f32.load offset=180
                        local.tee $l39
                        f32.mul
                        f32.sub
                        local.get $l6
                        f32.load offset=216
                        local.tee $l50
                        local.get $l6
                        f32.load offset=184
                        local.tee $l53
                        f32.mul
                        f32.sub
                        f32.store offset=116
                        local.get $l6
                        local.get $l41
                        local.get $l39
                        f32.mul
                        local.get $l36
                        local.get $l53
                        f32.mul
                        local.get $l50
                        local.get $l37
                        f32.mul
                        f32.add
                        f32.add
                        local.get $l38
                        local.get $l42
                        f32.mul
                        f32.sub
                        f32.store offset=112
                        local.get $l6
                        local.get $l50
                        local.get $l38
                        f32.mul
                        local.get $l36
                        local.get $l39
                        f32.mul
                        local.get $l42
                        local.get $l37
                        f32.mul
                        f32.add
                        f32.add
                        local.get $l53
                        local.get $l41
                        f32.mul
                        f32.sub
                        f32.store offset=108
                        local.get $l6
                        local.get $l42
                        local.get $l53
                        f32.mul
                        local.get $l36
                        local.get $l38
                        f32.mul
                        local.get $l41
                        local.get $l37
                        f32.mul
                        f32.add
                        f32.add
                        local.get $l39
                        local.get $l50
                        f32.mul
                        f32.sub
                        f32.store offset=104
                        local.get $l6
                        local.get $l6
                        f32.load offset=232
                        local.get $l50
                        local.get $l50
                        local.get $l6
                        f32.load offset=200
                        local.tee $l37
                        local.get $l37
                        f32.add
                        local.tee $l37
                        f32.mul
                        local.get $l41
                        local.get $l6
                        f32.load offset=192
                        local.tee $l38
                        local.get $l38
                        f32.add
                        local.tee $l38
                        f32.mul
                        local.get $l42
                        local.get $l6
                        f32.load offset=196
                        local.tee $l39
                        local.get $l39
                        f32.add
                        local.tee $l39
                        f32.mul
                        f32.add
                        f32.add
                        local.tee $l53
                        f32.mul
                        local.get $l37
                        local.get $l36
                        local.get $l36
                        f32.mul
                        f32.const -0x1p-1 (;=-0.5;)
                        f32.add
                        local.tee $l67
                        f32.mul
                        local.get $l36
                        local.get $l41
                        local.get $l39
                        f32.mul
                        local.get $l38
                        local.get $l42
                        f32.mul
                        f32.sub
                        f32.mul
                        f32.add
                        f32.add
                        f32.add
                        f32.store offset=128
                        local.get $l6
                        local.get $l6
                        f32.load offset=228
                        local.get $l42
                        local.get $l53
                        f32.mul
                        local.get $l39
                        local.get $l67
                        f32.mul
                        local.get $l36
                        local.get $l50
                        local.get $l38
                        f32.mul
                        local.get $l37
                        local.get $l41
                        f32.mul
                        f32.sub
                        f32.mul
                        f32.add
                        f32.add
                        f32.add
                        f32.store offset=124
                        local.get $l6
                        local.get $l6
                        f32.load offset=224
                        local.get $l41
                        local.get $l53
                        f32.mul
                        local.get $l38
                        local.get $l67
                        f32.mul
                        local.get $l36
                        local.get $l42
                        local.get $l37
                        f32.mul
                        local.get $l39
                        local.get $l50
                        f32.mul
                        f32.sub
                        f32.mul
                        f32.add
                        f32.add
                        f32.add
                        f32.store offset=120
                        local.get $l6
                        i32.const 0
                        i32.store16 offset=96
                        local.get $l27
                        local.get $l31
                        local.get $l6
                        i32.const 88
                        i32.add
                        local.get $l6
                        i32.const 56
                        i32.add
                        local.get $l5
                        local.get $l6
                        i32.const 104
                        i32.add
                        local.get $l6
                        i32.const 8
                        i32.add
                        local.get $l6
                        i32.const 96
                        i32.add
                        call $f70313
                        i32.eqz
                        br_if $B18
                        block $B19
                          local.get $p4
                          br_table $B15 $B17 $B19
                        end
                        local.get $l18
                        local.get $l9
                        i32.const 2
                        i32.shl
                        i32.add
                        i32.load
                        local.tee $l10
                        i32.const 31
                        i32.gt_s
                        br_if $B15
                        i32.const 1
                        local.set $l15
                        local.get $l16
                        local.get $l16
                        i32.load
                        i32.const 1
                        local.get $l10
                        i32.shl
                        i32.or
                        i32.store
                      end
                      local.get $l9
                      i32.const 1
                      i32.add
                      local.tee $l9
                      local.get $l8
                      i32.ne
                      br_if $L16
                      br $B14
                    end
                  end
                  local.get $l16
                  local.get $l18
                  local.get $l9
                  i32.const 2
                  i32.shl
                  i32.add
                  i32.load
                  i32.store
                end
                i32.const 1
                local.set $l15
              end
              local.get $l6
              i32.const 240
              i32.add
              global.set $g0
              local.get $l15
            end
            i32.store
            local.get $l7
            i32.const 1
            i32.add
            local.tee $l7
            i32.const 4
            i32.eq
            br_if $B11
            local.get $l7
            i32.const 2
            i32.shl
            local.tee $l5
            local.get $p0
            i32.const 104
            i32.add
            i32.add
            f32.load
            local.set $l31
            local.get $l5
            local.get $l20
            i32.add
            f32.load
            local.set $l34
            local.get $l5
            local.get $l21
            i32.add
            f32.load
            local.set $l35
            local.get $p0
            i32.const 56
            i32.add
            local.get $l5
            i32.add
            f32.load
            local.set $l43
            br $L12
          end
          unreachable
        end
        local.get $l17
        i32.const 1
        i32.add
        local.tee $l17
        local.get $p1
        i32.load offset=8
        i32.lt_u
        br_if $L10
      end
    end
    local.get $p0
    i32.const 216
    i32.add
    call $f554
    drop
    local.get $p0
    i32.const 232
    i32.add
    call $f554
    drop
    local.get $p0
    i32.const 248
    i32.add
    call $f554
    drop
    local.get $p0
    i32.const 288
    i32.add
    global.set $g0)
