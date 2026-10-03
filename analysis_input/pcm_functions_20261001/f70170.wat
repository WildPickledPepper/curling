  (func $f70170 (type $t100) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 i32) (param $p7 i32) (param $p8 i32) (param $p9 i32) (param $p10 i32) (param $p11 i32) (result i32)
    (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 i32) (local $l17 i32) (local $l18 i32) (local $l19 i32) (local $l20 i32) (local $l21 i32) (local $l22 i32) (local $l23 i32) (local $l24 i32) (local $l25 i32) (local $l26 i32) (local $l27 i32) (local $l28 i32) (local $l29 i32) (local $l30 i32) (local $l31 i32) (local $l32 i32) (local $l33 i32) (local $l34 f32) (local $l35 f32) (local $l36 f32) (local $l37 f32) (local $l38 f32) (local $l39 f32) (local $l40 f32) (local $l41 f32) (local $l42 f32) (local $l43 f32) (local $l44 f32) (local $l45 f32) (local $l46 f32) (local $l47 f32) (local $l48 f32) (local $l49 f32) (local $l50 f32) (local $l51 f32) (local $l52 f32) (local $l53 f32) (local $l54 f32) (local $l55 f32) (local $l56 f32) (local $l57 f32) (local $l58 f32) (local $l59 f32) (local $l60 f32) (local $l61 f32) (local $l62 f32) (local $l63 f32) (local $l64 f32) (local $l65 f32) (local $l66 f32) (local $l67 f32) (local $l68 f32) (local $l69 f32) (local $l70 f32) (local $l71 f32) (local $l72 f32) (local $l73 f32) (local $l74 f32) (local $l75 f32) (local $l76 f32) (local $l77 i64)
    global.get $g0
    i32.const 544
    i32.sub
    local.tee $l21
    global.set $g0
    local.get $l21
    local.tee $l12
    local.get $p4
    f32.load offset=4
    local.tee $l40
    local.get $l40
    f32.add
    local.tee $l34
    local.get $p4
    f32.load offset=8
    local.tee $l36
    f32.mul
    local.tee $l35
    local.get $p4
    f32.load
    local.tee $l41
    local.get $l41
    f32.add
    local.tee $l37
    local.get $p4
    f32.load offset=12
    local.tee $l38
    f32.mul
    local.tee $l44
    f32.sub
    local.tee $l42
    f32.store offset=524
    local.get $l12
    local.get $l35
    local.get $l44
    f32.add
    local.tee $l35
    f32.store offset=516
    local.get $l12
    f32.const 0x1p+0 (;=1;)
    local.get $l41
    local.get $l37
    f32.mul
    f32.sub
    local.tee $l41
    local.get $l40
    local.get $l34
    f32.mul
    local.tee $l44
    f32.sub
    local.tee $l39
    f32.store offset=528
    local.get $l12
    local.get $l41
    local.get $l36
    local.get $l36
    local.get $l36
    f32.add
    local.tee $l43
    f32.mul
    local.tee $l45
    f32.sub
    local.tee $l46
    f32.store offset=512
    local.get $l12
    local.get $l37
    local.get $l36
    f32.mul
    local.tee $l36
    local.get $l34
    local.get $l38
    f32.mul
    local.tee $l34
    f32.add
    local.tee $l47
    f32.store offset=520
    local.get $l12
    f32.const 0x1p+0 (;=1;)
    local.get $l44
    f32.sub
    local.get $l45
    f32.sub
    local.tee $l44
    f32.store offset=496
    local.get $l12
    local.get $l37
    local.get $l40
    f32.mul
    local.tee $l40
    local.get $l43
    local.get $l38
    f32.mul
    local.tee $l37
    f32.sub
    local.tee $l43
    f32.store offset=508
    local.get $l12
    local.get $l40
    local.get $l37
    f32.add
    local.tee $l45
    f32.store offset=500
    local.get $l12
    local.get $l36
    local.get $l34
    f32.sub
    local.tee $l48
    f32.store offset=504
    local.get $l12
    local.get $p4
    f32.load offset=16
    local.tee $l50
    f32.store offset=532
    local.get $l12
    local.get $p4
    f32.load offset=20
    local.tee $l51
    f32.store offset=536
    local.get $l12
    local.get $p4
    f32.load offset=24
    local.tee $l49
    f32.store offset=540
    local.get $l12
    local.get $p5
    f32.load offset=4
    local.tee $l40
    local.get $l40
    f32.add
    local.tee $l34
    local.get $p5
    f32.load offset=8
    local.tee $l36
    f32.mul
    local.tee $l52
    local.get $p5
    f32.load
    local.tee $l41
    local.get $l41
    f32.add
    local.tee $l37
    local.get $p5
    f32.load offset=12
    local.tee $l38
    f32.mul
    local.tee $l53
    f32.sub
    local.tee $l55
    f32.store offset=476
    local.get $l12
    local.get $l52
    local.get $l53
    f32.add
    local.tee $l52
    f32.store offset=468
    local.get $l12
    f32.const 0x1p+0 (;=1;)
    local.get $l41
    local.get $l37
    f32.mul
    f32.sub
    local.tee $l41
    local.get $l40
    local.get $l34
    f32.mul
    local.tee $l53
    f32.sub
    local.tee $l57
    f32.store offset=480
    local.get $l12
    local.get $l41
    local.get $l36
    local.get $l36
    local.get $l36
    f32.add
    local.tee $l54
    f32.mul
    local.tee $l56
    f32.sub
    local.tee $l58
    f32.store offset=464
    local.get $l12
    local.get $l37
    local.get $l36
    f32.mul
    local.tee $l36
    local.get $l34
    local.get $l38
    f32.mul
    local.tee $l34
    f32.add
    local.tee $l59
    f32.store offset=472
    local.get $l12
    f32.const 0x1p+0 (;=1;)
    local.get $l53
    f32.sub
    local.get $l56
    f32.sub
    local.tee $l53
    f32.store offset=448
    local.get $l12
    local.get $l37
    local.get $l40
    f32.mul
    local.tee $l40
    local.get $l54
    local.get $l38
    f32.mul
    local.tee $l37
    f32.sub
    local.tee $l54
    f32.store offset=460
    local.get $l12
    local.get $l40
    local.get $l37
    f32.add
    local.tee $l56
    f32.store offset=452
    local.get $l12
    local.get $l36
    local.get $l34
    f32.sub
    local.tee $l40
    f32.store offset=456
    local.get $l12
    local.get $p5
    f32.load offset=16
    local.tee $l60
    f32.store offset=484
    local.get $l12
    local.get $p5
    f32.load offset=20
    local.tee $l61
    f32.store offset=488
    local.get $l12
    local.get $p5
    f32.load offset=24
    local.tee $l34
    f32.store offset=492
    local.get $l12
    local.get $l34
    local.get $l40
    local.get $p1
    f32.load
    local.tee $l36
    f32.mul
    local.get $l52
    local.get $p1
    f32.load offset=4
    local.tee $l40
    f32.mul
    f32.add
    local.get $l57
    local.get $p1
    f32.load offset=8
    local.tee $l37
    f32.mul
    f32.add
    f32.add
    local.get $l49
    local.get $l48
    local.get $p0
    f32.load
    local.tee $l34
    f32.mul
    local.get $l35
    local.get $p0
    f32.load offset=4
    local.tee $l41
    f32.mul
    f32.add
    local.get $l39
    local.get $p0
    f32.load offset=8
    local.tee $l38
    f32.mul
    f32.add
    f32.add
    f32.sub
    f32.store offset=440
    local.get $l12
    local.get $l61
    local.get $l56
    local.get $l36
    f32.mul
    local.get $l58
    local.get $l40
    f32.mul
    f32.add
    local.get $l55
    local.get $l37
    f32.mul
    f32.add
    f32.add
    local.get $l51
    local.get $l45
    local.get $l34
    f32.mul
    local.get $l46
    local.get $l41
    f32.mul
    f32.add
    local.get $l42
    local.get $l38
    f32.mul
    f32.add
    f32.add
    f32.sub
    f32.store offset=436
    local.get $l12
    local.get $l60
    local.get $l53
    local.get $l36
    f32.mul
    local.get $l54
    local.get $l40
    f32.mul
    f32.add
    local.get $l59
    local.get $l37
    f32.mul
    f32.add
    f32.add
    local.get $l50
    local.get $l44
    local.get $l34
    f32.mul
    local.get $l43
    local.get $l41
    f32.mul
    f32.add
    local.get $l47
    local.get $l38
    f32.mul
    f32.add
    f32.add
    f32.sub
    f32.store offset=432
    local.get $p6
    f32.load
    local.set $l36
    local.get $p0
    local.get $l12
    i32.const 432
    i32.add
    local.get $l12
    i32.const 496
    i32.add
    local.get $p8
    local.get $l12
    i32.const 192
    i32.add
    local.get $l12
    i32.const 144
    i32.add
    local.get $p0
    i32.load offset=64
    call_indirect $__indirect_function_table (type $t11)
    local.get $l12
    f32.load offset=192
    local.set $l37
    local.get $l12
    f32.load offset=144
    local.set $l40
    local.get $p1
    local.get $l12
    i32.const 432
    i32.add
    local.get $l12
    i32.const 448
    i32.add
    local.get $p9
    local.get $l12
    i32.const 368
    i32.add
    local.get $l12
    i32.const 320
    i32.add
    local.get $p1
    i32.load offset=64
    call_indirect $__indirect_function_table (type $t11)
    block $B0
      local.get $l12
      f32.load offset=368
      local.tee $l34
      local.get $l36
      local.get $l40
      f32.add
      f32.gt
      br_if $B0
      local.get $l36
      local.get $l12
      f32.load offset=320
      local.tee $l41
      f32.add
      local.get $l37
      f32.lt
      br_if $B0
      local.get $l12
      local.get $l40
      local.get $l34
      f32.sub
      local.tee $l36
      local.get $l41
      local.get $l37
      f32.sub
      local.tee $l40
      local.get $l36
      local.get $l40
      f32.lt
      select
      f32.store offset=428
      local.get $p4
      f32.load offset=8
      local.set $l40
      local.get $p4
      f32.load offset=4
      local.set $l37
      local.get $p4
      f32.load
      local.set $l34
      local.get $p4
      f32.load offset=12
      local.set $l36
      local.get $l12
      local.get $p5
      f32.load offset=12
      local.tee $l41
      local.get $l41
      f32.mul
      f32.const -0x1p-1 (;=-0.5;)
      f32.add
      local.tee $l50
      local.get $p4
      f32.load offset=24
      local.tee $l53
      local.get $p5
      f32.load offset=24
      local.tee $l55
      f32.sub
      local.tee $l38
      local.get $l38
      f32.add
      local.tee $l43
      f32.mul
      local.get $l41
      local.get $p5
      f32.load offset=4
      local.tee $l38
      local.get $p4
      f32.load offset=16
      local.tee $l57
      local.get $p5
      f32.load offset=16
      local.tee $l54
      f32.sub
      local.tee $l35
      local.get $l35
      f32.add
      local.tee $l45
      f32.mul
      local.get $p5
      f32.load
      local.tee $l35
      local.get $p4
      f32.load offset=20
      local.tee $l56
      local.get $p5
      f32.load offset=20
      local.tee $l58
      f32.sub
      local.tee $l44
      local.get $l44
      f32.add
      local.tee $l46
      f32.mul
      f32.sub
      f32.mul
      f32.add
      local.get $p5
      f32.load offset=8
      local.tee $l44
      local.get $l46
      local.get $l38
      f32.neg
      f32.mul
      local.get $l35
      local.get $l45
      f32.mul
      f32.sub
      local.get $l44
      local.get $l43
      f32.mul
      f32.sub
      local.tee $l51
      f32.mul
      f32.sub
      f32.store offset=412
      local.get $l12
      local.get $l50
      local.get $l46
      f32.mul
      local.get $l41
      local.get $l35
      local.get $l43
      f32.mul
      local.get $l44
      local.get $l45
      f32.mul
      f32.sub
      f32.mul
      f32.add
      local.get $l38
      local.get $l51
      f32.mul
      f32.sub
      f32.store offset=408
      local.get $l12
      local.get $l38
      local.get $l34
      f32.mul
      local.tee $l59
      local.get $l41
      local.get $l40
      f32.mul
      local.tee $l60
      local.get $l44
      local.get $l36
      f32.mul
      local.tee $l61
      f32.sub
      local.get $l35
      local.get $l37
      f32.mul
      local.tee $l64
      f32.sub
      f32.add
      local.tee $l39
      local.get $l35
      local.get $l40
      f32.mul
      local.tee $l65
      local.get $l41
      local.get $l37
      f32.mul
      local.tee $l66
      local.get $l38
      local.get $l36
      f32.mul
      local.tee $l67
      f32.sub
      local.get $l44
      local.get $l34
      f32.mul
      local.tee $l68
      f32.sub
      f32.add
      local.tee $l47
      local.get $l47
      f32.add
      local.tee $l49
      f32.mul
      local.tee $l62
      local.get $l41
      local.get $l34
      f32.mul
      local.tee $l69
      local.get $l35
      local.get $l36
      f32.mul
      local.tee $l70
      f32.sub
      local.get $l38
      local.get $l40
      f32.mul
      local.tee $l71
      f32.sub
      local.get $l44
      local.get $l37
      f32.mul
      local.tee $l72
      f32.add
      local.tee $l52
      local.get $l52
      f32.add
      local.tee $l48
      local.get $l44
      local.get $l40
      f32.mul
      local.get $l35
      local.get $l34
      f32.mul
      local.get $l41
      local.get $l36
      f32.mul
      f32.add
      local.get $l38
      local.get $l37
      f32.mul
      f32.add
      f32.add
      local.tee $l42
      f32.mul
      local.tee $l63
      f32.sub
      f32.store offset=396
      local.get $l12
      local.get $l63
      local.get $l62
      f32.add
      f32.store offset=388
      local.get $l12
      f32.const 0x1p+0 (;=1;)
      local.get $l52
      local.get $l48
      f32.mul
      f32.sub
      local.tee $l52
      local.get $l47
      local.get $l49
      f32.mul
      local.tee $l62
      f32.sub
      f32.store offset=400
      local.get $l12
      local.get $l52
      local.get $l39
      local.get $l39
      local.get $l39
      f32.add
      local.tee $l63
      f32.mul
      local.tee $l73
      f32.sub
      f32.store offset=384
      local.get $l12
      local.get $l50
      local.get $l45
      f32.mul
      local.get $l41
      local.get $l44
      local.get $l46
      f32.mul
      local.get $l38
      local.get $l43
      f32.mul
      f32.sub
      f32.mul
      f32.add
      local.get $l35
      local.get $l51
      f32.mul
      f32.sub
      f32.store offset=404
      local.get $l12
      local.get $l48
      local.get $l39
      f32.mul
      local.tee $l41
      local.get $l42
      local.get $l49
      f32.mul
      local.tee $l38
      f32.add
      f32.store offset=392
      local.get $l12
      local.get $l48
      local.get $l47
      f32.mul
      local.tee $l35
      local.get $l42
      local.get $l63
      f32.mul
      local.tee $l44
      f32.sub
      f32.store offset=380
      local.get $l12
      local.get $l41
      local.get $l38
      f32.sub
      f32.store offset=376
      local.get $l12
      local.get $l35
      local.get $l44
      f32.add
      f32.store offset=372
      local.get $l12
      f32.const 0x1p+0 (;=1;)
      local.get $l62
      f32.sub
      local.get $l73
      f32.sub
      f32.store offset=368
      local.get $l12
      local.get $l55
      local.get $l53
      f32.sub
      local.tee $l41
      local.get $l41
      f32.add
      local.tee $l38
      local.get $l36
      local.get $l36
      f32.mul
      f32.const -0x1p-1 (;=-0.5;)
      f32.add
      local.tee $l45
      f32.mul
      local.get $l36
      local.get $l37
      local.get $l54
      local.get $l57
      f32.sub
      local.tee $l41
      local.get $l41
      f32.add
      local.tee $l35
      f32.mul
      local.get $l34
      local.get $l58
      local.get $l56
      f32.sub
      local.tee $l41
      local.get $l41
      f32.add
      local.tee $l44
      f32.mul
      f32.sub
      f32.mul
      f32.add
      local.get $l40
      local.get $l44
      local.get $l37
      f32.neg
      f32.mul
      local.get $l35
      local.get $l34
      f32.mul
      f32.sub
      local.get $l38
      local.get $l40
      f32.mul
      f32.sub
      local.tee $l46
      f32.mul
      f32.sub
      f32.store offset=364
      local.get $l12
      local.get $l44
      local.get $l45
      f32.mul
      local.get $l36
      local.get $l34
      local.get $l38
      f32.mul
      local.get $l35
      local.get $l40
      f32.mul
      f32.sub
      f32.mul
      f32.add
      local.get $l37
      local.get $l46
      f32.mul
      f32.sub
      f32.store offset=360
      local.get $l12
      f32.const 0x1p+0 (;=1;)
      local.get $l71
      local.get $l70
      local.get $l69
      f32.sub
      local.get $l72
      f32.sub
      f32.add
      local.tee $l41
      local.get $l41
      local.get $l41
      f32.add
      local.tee $l39
      f32.mul
      f32.sub
      local.tee $l48
      local.get $l68
      local.get $l67
      local.get $l66
      f32.sub
      local.get $l65
      f32.sub
      f32.add
      local.tee $l43
      local.get $l43
      local.get $l43
      f32.add
      local.tee $l47
      f32.mul
      local.tee $l50
      f32.sub
      f32.store offset=352
      local.get $l12
      local.get $l64
      local.get $l61
      local.get $l60
      f32.sub
      local.get $l59
      f32.sub
      f32.add
      local.tee $l41
      local.get $l47
      f32.mul
      local.tee $l51
      local.get $l42
      local.get $l39
      f32.mul
      local.tee $l49
      f32.sub
      f32.store offset=348
      local.get $l12
      local.get $l49
      local.get $l51
      f32.add
      f32.store offset=340
      local.get $l12
      local.get $l48
      local.get $l41
      local.get $l41
      local.get $l41
      f32.add
      local.tee $l51
      f32.mul
      local.tee $l49
      f32.sub
      f32.store offset=336
      local.get $l12
      local.get $l35
      local.get $l45
      f32.mul
      local.get $l36
      local.get $l44
      local.get $l40
      f32.mul
      local.get $l38
      local.get $l37
      f32.mul
      f32.sub
      f32.mul
      f32.add
      local.get $l34
      local.get $l46
      f32.mul
      f32.sub
      f32.store offset=356
      local.get $l12
      local.get $l41
      local.get $l39
      f32.mul
      local.tee $l36
      local.get $l42
      local.get $l47
      f32.mul
      local.tee $l40
      f32.add
      f32.store offset=344
      local.get $l12
      local.get $l39
      local.get $l43
      f32.mul
      local.tee $l37
      local.get $l42
      local.get $l51
      f32.mul
      local.tee $l34
      f32.sub
      f32.store offset=332
      local.get $l12
      local.get $l36
      local.get $l40
      f32.sub
      f32.store offset=328
      local.get $l12
      local.get $l37
      local.get $l34
      f32.add
      f32.store offset=324
      local.get $l12
      f32.const 0x1p+0 (;=1;)
      local.get $l50
      f32.sub
      local.get $l49
      f32.sub
      f32.store offset=320
      i32.const 32767
      local.set $l26
      i32.const 32767
      local.set $l27
      i32.const 1
      local.set $l13
      loop $L1
        local.get $p6
        f32.load offset=8
        drop
        local.get $p6
        f32.load
        local.set $l40
        block $B2
          block $B3
            block $B4
              block $B5
                local.get $l13
                local.tee $l31
                if $I6
                  local.get $l12
                  i32.const 2139095039
                  i32.store
                  local.get $l12
                  i32.const 2139095039
                  i32.store offset=288
                  local.get $l12
                  local.get $l12
                  f32.load offset=432
                  local.tee $l37
                  local.get $l12
                  f32.load offset=520
                  f32.mul
                  local.get $l12
                  f32.load offset=436
                  local.tee $l34
                  local.get $l12
                  f32.load offset=524
                  f32.mul
                  f32.add
                  local.get $l12
                  f32.load offset=440
                  local.tee $l41
                  local.get $l12
                  f32.load offset=528
                  f32.mul
                  f32.add
                  f32.store offset=104
                  local.get $l12
                  local.get $l37
                  local.get $l12
                  f32.load offset=508
                  f32.mul
                  local.get $l34
                  local.get $l12
                  f32.load offset=512
                  f32.mul
                  f32.add
                  local.get $l41
                  local.get $l12
                  f32.load offset=516
                  f32.mul
                  f32.add
                  f32.store offset=100
                  local.get $l12
                  local.get $l37
                  local.get $l12
                  f32.load offset=496
                  f32.mul
                  local.get $l34
                  local.get $l12
                  f32.load offset=500
                  f32.mul
                  f32.add
                  local.get $l41
                  local.get $l12
                  f32.load offset=504
                  f32.mul
                  f32.add
                  f32.store offset=96
                  local.get $l12
                  local.get $l41
                  f32.neg
                  f32.store offset=48
                  local.get $l12
                  local.get $l34
                  f32.neg
                  f32.store offset=44
                  local.get $l12
                  local.get $l37
                  f32.neg
                  f32.store offset=40
                  local.get $p0
                  local.get $p1
                  local.get $l12
                  i32.const 496
                  i32.add
                  local.get $l12
                  i32.const 448
                  i32.add
                  local.get $p8
                  local.get $p9
                  local.get $l12
                  i32.const 320
                  i32.add
                  local.get $l12
                  i32.const 96
                  i32.add
                  local.get $l12
                  local.get $l12
                  i32.const 192
                  i32.add
                  local.get $l12
                  i32.const 304
                  i32.add
                  local.get $l40
                  local.get $l12
                  i32.const 40
                  i32.add
                  call $f70171
                  i32.eqz
                  br_if $B4
                  local.get $l12
                  f32.load offset=456
                  local.set $l38
                  local.get $l12
                  f32.load offset=448
                  local.set $l35
                  local.get $l12
                  f32.load offset=452
                  local.set $l44
                  local.get $l12
                  f32.load offset=468
                  local.set $l42
                  local.get $l12
                  f32.load offset=460
                  local.set $l39
                  local.get $l12
                  f32.load offset=464
                  local.set $l43
                  local.get $l12
                  local.get $l12
                  f32.load offset=432
                  local.tee $l37
                  local.get $l12
                  f32.load offset=472
                  f32.mul
                  local.get $l12
                  f32.load offset=436
                  local.tee $l34
                  local.get $l12
                  f32.load offset=476
                  f32.mul
                  f32.add
                  local.get $l12
                  f32.load offset=440
                  local.tee $l41
                  local.get $l12
                  f32.load offset=480
                  f32.mul
                  f32.add
                  f32.neg
                  f32.store offset=48
                  local.get $l12
                  local.get $l37
                  local.get $l39
                  f32.mul
                  local.get $l34
                  local.get $l43
                  f32.mul
                  f32.add
                  local.get $l41
                  local.get $l42
                  f32.mul
                  f32.add
                  f32.neg
                  f32.store offset=44
                  local.get $l12
                  local.get $l35
                  local.get $l37
                  f32.mul
                  local.get $l44
                  local.get $l34
                  f32.mul
                  f32.add
                  local.get $l38
                  local.get $l41
                  f32.mul
                  f32.add
                  f32.neg
                  f32.store offset=40
                  local.get $p1
                  local.get $p0
                  local.get $l12
                  i32.const 448
                  i32.add
                  local.get $l12
                  i32.const 496
                  i32.add
                  local.get $p9
                  local.get $p8
                  local.get $l12
                  i32.const 368
                  i32.add
                  local.get $l12
                  i32.const 40
                  i32.add
                  local.get $l12
                  i32.const 288
                  i32.add
                  local.get $l12
                  i32.const 144
                  i32.add
                  local.get $l12
                  i32.const 272
                  i32.add
                  local.get $l40
                  local.get $l12
                  i32.const 432
                  i32.add
                  call $f70171
                  i32.eqz
                  br_if $B4
                  local.get $l12
                  i32.const 0
                  i32.store offset=256
                  block $B7 (result f32)
                    local.get $l12
                    f32.load offset=288
                    local.tee $l34
                    local.get $l12
                    f32.load
                    local.tee $l36
                    f32.lt
                    i32.eqz
                    if $I8
                      local.get $l12
                      f32.load offset=200
                      local.set $l40
                      local.get $l12
                      f32.load offset=192
                      local.set $l37
                      local.get $l12
                      f32.load offset=196
                      br $B7
                    end
                    local.get $l12
                    i32.const 1
                    i32.store offset=256
                    local.get $l12
                    f32.load offset=152
                    local.set $l40
                    local.get $l12
                    f32.load offset=144
                    local.set $l37
                    local.get $l34
                    local.set $l36
                    local.get $l12
                    f32.load offset=148
                  end
                  local.set $l44
                  local.get $l12
                  local.get $l40
                  f32.store offset=424
                  local.get $l12
                  local.get $l44
                  f32.store offset=420
                  local.get $l12
                  local.get $l37
                  f32.store offset=416
                  local.get $l12
                  local.get $l36
                  f32.store offset=428
                  br $B5
                end
                local.get $p2
                local.set $l19
                local.get $p3
                local.set $l20
                local.get $l12
                i32.const 368
                i32.add
                local.set $l15
                local.get $l12
                i32.const 272
                i32.add
                local.set $l23
                local.get $l12
                i32.const 428
                i32.add
                local.set $l33
                local.get $l12
                i32.const 416
                i32.add
                local.set $l28
                local.get $l12
                i32.const 256
                i32.add
                local.set $l29
                global.get $g0
                i32.const 6336
                i32.sub
                local.tee $l14
                global.set $g0
                local.get $l12
                i32.const 496
                i32.add
                local.tee $l16
                f32.load offset=20
                local.set $l37
                local.get $l16
                f32.load offset=16
                local.set $l42
                local.get $l16
                f32.load offset=32
                local.set $l43
                local.get $l16
                f32.load offset=28
                local.set $l36
                local.get $l16
                f32.load offset=12
                local.set $l41
                local.get $l16
                f32.load offset=24
                local.set $l45
                local.get $l14
                local.tee $l13
                local.get $l16
                f32.load
                local.get $l12
                i32.const 432
                i32.add
                local.tee $l22
                f32.load
                local.tee $l34
                f32.mul
                local.get $l16
                f32.load offset=4
                local.get $l22
                f32.load offset=4
                local.tee $l35
                f32.mul
                f32.add
                local.get $l16
                f32.load offset=8
                local.get $l22
                f32.load offset=8
                local.tee $l38
                f32.mul
                f32.add
                f32.store offset=6304
                local.get $l13
                local.get $l34
                local.get $l45
                f32.mul
                local.get $l35
                local.get $l36
                f32.mul
                f32.add
                local.get $l38
                local.get $l43
                f32.mul
                f32.add
                f32.store offset=6312
                local.get $l13
                local.get $l34
                local.get $l41
                f32.mul
                local.get $l35
                local.get $l42
                f32.mul
                f32.add
                local.get $l38
                local.get $l37
                f32.mul
                f32.add
                f32.store offset=6308
                local.get $l13
                local.get $p0
                i32.load offset=16
                i32.const 2
                i32.shl
                i32.const 15
                i32.add
                i32.const -16
                i32.and
                i32.sub
                local.tee $l25
                local.tee $l24
                global.set $g0
                local.get $l13
                i32.const 2139095039
                i32.store offset=6296
                local.get $l13
                local.get $l38
                f32.neg
                f32.store offset=3184
                local.get $l13
                local.get $l35
                f32.neg
                f32.store offset=3180
                local.get $l13
                local.get $l34
                f32.neg
                f32.store offset=3176
                block $B9 (result i32)
                  i32.const 0
                  local.get $p0
                  local.get $p1
                  local.get $l16
                  local.get $l12
                  i32.const 448
                  i32.add
                  local.tee $l17
                  local.get $p8
                  local.get $p9
                  local.get $l12
                  i32.const 320
                  i32.add
                  local.tee $l18
                  local.get $l13
                  i32.const 6304
                  i32.add
                  local.get $l13
                  i32.const 6296
                  i32.add
                  local.get $l13
                  i32.const 6280
                  i32.add
                  local.get $l12
                  i32.const 304
                  i32.add
                  local.tee $l30
                  local.get $l25
                  local.get $l13
                  i32.const 6300
                  i32.add
                  local.get $l40
                  local.get $l13
                  i32.const 3176
                  i32.add
                  call $f70183
                  i32.eqz
                  br_if $B9
                  drop
                  local.get $l17
                  f32.load offset=20
                  local.set $l37
                  local.get $l17
                  f32.load offset=16
                  local.set $l42
                  local.get $l17
                  f32.load offset=32
                  local.set $l43
                  local.get $l17
                  f32.load offset=28
                  local.set $l36
                  local.get $l17
                  f32.load offset=8
                  local.set $l41
                  local.get $l17
                  f32.load
                  local.set $l45
                  local.get $l17
                  f32.load offset=4
                  local.set $l46
                  local.get $l17
                  f32.load offset=12
                  local.set $l47
                  local.get $l22
                  f32.load offset=8
                  local.set $l34
                  local.get $l22
                  f32.load offset=4
                  local.set $l35
                  local.get $l17
                  f32.load offset=24
                  local.set $l44
                  local.get $l22
                  f32.load
                  local.set $l38
                  local.get $l24
                  local.get $p1
                  i32.load offset=16
                  i32.const 2
                  i32.shl
                  i32.const 15
                  i32.add
                  i32.const -16
                  i32.and
                  i32.sub
                  local.tee $l32
                  global.set $g0
                  local.get $l13
                  i32.const 2139095039
                  i32.store offset=6272
                  local.get $l13
                  local.get $l38
                  local.get $l44
                  f32.mul
                  local.get $l35
                  local.get $l36
                  f32.mul
                  f32.add
                  local.get $l34
                  local.get $l43
                  f32.mul
                  f32.add
                  f32.neg
                  f32.store offset=3184
                  local.get $l13
                  local.get $l38
                  local.get $l47
                  f32.mul
                  local.get $l35
                  local.get $l42
                  f32.mul
                  f32.add
                  local.get $l34
                  local.get $l37
                  f32.mul
                  f32.add
                  f32.neg
                  f32.store offset=3180
                  local.get $l13
                  local.get $l45
                  local.get $l38
                  f32.mul
                  local.get $l46
                  local.get $l35
                  f32.mul
                  f32.add
                  local.get $l41
                  local.get $l34
                  f32.mul
                  f32.add
                  f32.neg
                  f32.store offset=3176
                  i32.const 0
                  local.get $p1
                  local.get $p0
                  local.get $l17
                  local.get $l16
                  local.get $p9
                  local.get $p8
                  local.get $l15
                  local.get $l13
                  i32.const 3176
                  i32.add
                  local.get $l13
                  i32.const 6272
                  i32.add
                  local.get $l13
                  i32.const 6256
                  i32.add
                  local.get $l23
                  local.get $l32
                  local.get $l13
                  i32.const 6276
                  i32.add
                  local.get $l40
                  local.get $l22
                  call $f70183
                  i32.eqz
                  br_if $B9
                  drop
                  local.get $l13
                  f32.load offset=6288
                  local.set $l45
                  local.get $l13
                  f32.load offset=6284
                  local.set $l46
                  local.get $l13
                  f32.load offset=6280
                  local.set $l47
                  local.get $l13
                  f32.load offset=6296
                  local.set $l36
                  i32.const 0
                  local.set $l24
                  local.get $l29
                  i32.const 0
                  i32.store
                  local.get $l36
                  local.get $l13
                  f32.load offset=6272
                  local.tee $l34
                  f32.gt
                  if $I10
                    local.get $l13
                    f32.load offset=6264
                    local.set $l45
                    local.get $l13
                    f32.load offset=6260
                    local.set $l46
                    local.get $l13
                    f32.load offset=6256
                    local.set $l47
                    local.get $l29
                    i32.const 1
                    i32.store
                    local.get $l34
                    local.set $l36
                  end
                  local.get $l13
                  i32.const 0
                  i32.store offset=3176
                  local.get $l13
                  i32.const 0
                  i32.store offset=96
                  local.get $p1
                  i32.load offset=24
                  local.get $l23
                  i32.load
                  i32.const 20
                  i32.mul
                  i32.add
                  local.tee $l14
                  f32.load offset=12
                  local.set $l41
                  local.get $p9
                  f32.load offset=68
                  local.set $l44
                  local.get $p9
                  f32.load offset=60
                  local.set $l48
                  local.get $p9
                  i32.const -64
                  i32.sub
                  f32.load
                  local.set $l49
                  local.get $p9
                  f32.load offset=40
                  local.set $l57
                  local.get $p9
                  f32.load offset=44
                  local.set $l58
                  local.get $p9
                  f32.load offset=56
                  local.set $l59
                  local.get $l14
                  f32.load offset=8
                  local.set $l34
                  local.get $p9
                  f32.load offset=48
                  local.set $l60
                  local.get $l14
                  f32.load
                  local.set $l35
                  local.get $p9
                  f32.load offset=52
                  local.set $l61
                  local.get $l14
                  f32.load offset=4
                  local.set $l38
                  local.get $p0
                  i32.load offset=24
                  local.get $l30
                  i32.load
                  i32.const 20
                  i32.mul
                  i32.add
                  local.tee $l14
                  f32.load offset=12
                  local.set $l50
                  local.get $l15
                  f32.load offset=44
                  local.set $l51
                  local.get $l15
                  f32.load offset=32
                  local.set $l52
                  local.get $l15
                  f32.load offset=20
                  local.set $l53
                  local.get $l15
                  f32.load offset=40
                  local.set $l54
                  local.get $p9
                  f32.load offset=36
                  local.set $l62
                  local.get $l15
                  f32.load offset=8
                  local.set $l55
                  local.get $l15
                  f32.load offset=36
                  local.set $l63
                  local.get $l15
                  f32.load offset=24
                  local.set $l56
                  local.get $l15
                  f32.load
                  local.set $l64
                  local.get $l15
                  f32.load offset=12
                  local.set $l65
                  local.get $l13
                  local.get $p8
                  f32.load offset=36
                  local.get $l14
                  f32.load
                  local.tee $l39
                  f32.mul
                  local.get $p8
                  f32.load offset=40
                  local.get $l14
                  f32.load offset=4
                  local.tee $l37
                  f32.mul
                  f32.add
                  local.get $p8
                  f32.load offset=44
                  local.get $l14
                  f32.load offset=8
                  local.tee $l42
                  f32.mul
                  f32.add
                  local.tee $l43
                  f32.const 0x1p+0 (;=1;)
                  local.get $l43
                  local.get $l43
                  f32.mul
                  local.get $l39
                  local.get $p8
                  f32.load offset=48
                  f32.mul
                  local.get $l37
                  local.get $p8
                  f32.load offset=52
                  f32.mul
                  f32.add
                  local.get $l42
                  local.get $p8
                  f32.load offset=56
                  f32.mul
                  f32.add
                  local.tee $l43
                  local.get $l43
                  f32.mul
                  f32.add
                  local.get $l39
                  local.get $p8
                  f32.load offset=60
                  f32.mul
                  local.get $l37
                  local.get $p8
                  i32.const -64
                  i32.sub
                  f32.load
                  f32.mul
                  f32.add
                  local.get $l42
                  local.get $p8
                  f32.load offset=68
                  f32.mul
                  f32.add
                  local.tee $l37
                  local.get $l37
                  f32.mul
                  f32.add
                  f32.sqrt
                  f32.div
                  local.tee $l39
                  f32.mul
                  local.tee $l42
                  local.get $l15
                  f32.load offset=4
                  f32.mul
                  local.get $l43
                  local.get $l39
                  f32.mul
                  local.tee $l43
                  local.get $l15
                  f32.load offset=16
                  f32.mul
                  f32.add
                  local.get $l37
                  local.get $l39
                  f32.mul
                  local.tee $l37
                  local.get $l15
                  f32.load offset=28
                  f32.mul
                  f32.add
                  local.tee $l66
                  f32.store offset=84
                  local.get $l13
                  local.get $l42
                  local.get $l64
                  f32.mul
                  local.get $l43
                  local.get $l65
                  f32.mul
                  f32.add
                  local.get $l37
                  local.get $l56
                  f32.mul
                  f32.add
                  local.tee $l56
                  f32.store offset=80
                  local.get $l13
                  local.get $l42
                  local.get $l55
                  f32.mul
                  local.get $l43
                  local.get $l53
                  f32.mul
                  f32.add
                  local.get $l37
                  local.get $l52
                  f32.mul
                  f32.add
                  local.tee $l37
                  f32.store offset=88
                  local.get $l13
                  local.get $l50
                  local.get $l39
                  f32.mul
                  local.get $l56
                  local.get $l63
                  f32.mul
                  local.get $l66
                  local.get $l54
                  f32.mul
                  f32.add
                  local.get $l37
                  local.get $l51
                  f32.mul
                  f32.add
                  f32.sub
                  f32.store offset=92
                  local.get $l18
                  f32.load offset=44
                  local.set $l37
                  local.get $l18
                  f32.load offset=32
                  local.set $l42
                  local.get $l18
                  f32.load offset=20
                  local.set $l43
                  local.get $l18
                  f32.load offset=40
                  local.set $l50
                  local.get $l18
                  f32.load offset=8
                  local.set $l51
                  local.get $l18
                  f32.load offset=36
                  local.set $l52
                  local.get $l18
                  f32.load offset=24
                  local.set $l53
                  local.get $l18
                  f32.load
                  local.set $l54
                  local.get $l18
                  f32.load offset=12
                  local.set $l55
                  local.get $l13
                  local.get $l62
                  local.get $l35
                  f32.mul
                  local.get $l57
                  local.get $l38
                  f32.mul
                  f32.add
                  local.get $l58
                  local.get $l34
                  f32.mul
                  f32.add
                  local.tee $l39
                  f32.const 0x1p+0 (;=1;)
                  local.get $l39
                  local.get $l39
                  f32.mul
                  local.get $l35
                  local.get $l60
                  f32.mul
                  local.get $l38
                  local.get $l61
                  f32.mul
                  f32.add
                  local.get $l34
                  local.get $l59
                  f32.mul
                  f32.add
                  local.tee $l39
                  local.get $l39
                  f32.mul
                  f32.add
                  local.get $l35
                  local.get $l48
                  f32.mul
                  local.get $l38
                  local.get $l49
                  f32.mul
                  f32.add
                  local.get $l34
                  local.get $l44
                  f32.mul
                  f32.add
                  local.tee $l35
                  local.get $l35
                  f32.mul
                  f32.add
                  f32.sqrt
                  f32.div
                  local.tee $l34
                  f32.mul
                  local.tee $l38
                  local.get $l18
                  f32.load offset=4
                  f32.mul
                  local.get $l39
                  local.get $l34
                  f32.mul
                  local.tee $l39
                  local.get $l18
                  f32.load offset=16
                  f32.mul
                  f32.add
                  local.get $l35
                  local.get $l34
                  f32.mul
                  local.tee $l35
                  local.get $l18
                  f32.load offset=28
                  f32.mul
                  f32.add
                  local.tee $l44
                  f32.store offset=68
                  local.get $l13
                  local.get $l38
                  local.get $l54
                  f32.mul
                  local.get $l39
                  local.get $l55
                  f32.mul
                  f32.add
                  local.get $l35
                  local.get $l53
                  f32.mul
                  f32.add
                  local.tee $l48
                  f32.store offset=64
                  local.get $l13
                  local.get $l38
                  local.get $l51
                  f32.mul
                  local.get $l39
                  local.get $l43
                  f32.mul
                  f32.add
                  local.get $l35
                  local.get $l42
                  f32.mul
                  f32.add
                  local.tee $l35
                  f32.store offset=72
                  local.get $l13
                  local.get $l41
                  local.get $l34
                  f32.mul
                  local.get $l48
                  local.get $l52
                  f32.mul
                  local.get $l44
                  local.get $l50
                  f32.mul
                  f32.add
                  local.get $l35
                  local.get $l37
                  f32.mul
                  f32.add
                  f32.sub
                  f32.store offset=76
                  local.get $l20
                  f32.load offset=16
                  local.set $l34
                  local.get $l20
                  f32.load offset=20
                  local.set $l35
                  local.get $l19
                  f32.load offset=16
                  local.set $l38
                  local.get $l20
                  f32.load offset=12
                  local.set $l39
                  local.get $l19
                  f32.load offset=12
                  local.set $l37
                  local.get $l20
                  f32.load
                  local.set $l42
                  local.get $l20
                  f32.load offset=4
                  local.set $l43
                  local.get $l20
                  f32.load offset=8
                  local.set $l41
                  local.get $l19
                  f32.load
                  local.set $l44
                  local.get $l19
                  f32.load offset=4
                  local.set $l48
                  local.get $l19
                  f32.load offset=8
                  local.set $l49
                  local.get $l13
                  local.get $l19
                  f32.load offset=20
                  local.get $l40
                  f32.add
                  f32.store offset=60
                  local.get $l13
                  local.get $l38
                  local.get $l40
                  f32.add
                  f32.store offset=56
                  local.get $l13
                  local.get $l35
                  local.get $l40
                  f32.add
                  f32.store offset=36
                  local.get $l13
                  local.get $l34
                  local.get $l40
                  f32.add
                  f32.store offset=32
                  local.get $l13
                  local.get $l49
                  local.get $l40
                  f32.sub
                  f32.store offset=48
                  local.get $l13
                  local.get $l48
                  local.get $l40
                  f32.sub
                  f32.store offset=44
                  local.get $l13
                  local.get $l44
                  local.get $l40
                  f32.sub
                  f32.store offset=40
                  local.get $l13
                  local.get $l41
                  local.get $l40
                  f32.sub
                  f32.store offset=24
                  local.get $l13
                  local.get $l43
                  local.get $l40
                  f32.sub
                  f32.store offset=20
                  local.get $l13
                  local.get $l42
                  local.get $l40
                  f32.sub
                  f32.store offset=16
                  local.get $l13
                  local.get $l37
                  local.get $l40
                  f32.add
                  f32.store offset=52
                  local.get $l13
                  local.get $l39
                  local.get $l40
                  f32.add
                  f32.store offset=28
                  local.get $l13
                  i32.const 3176
                  i32.add
                  local.get $l25
                  local.get $l13
                  i32.load offset=6300
                  local.get $p0
                  local.get $l16
                  local.get $l13
                  i32.const -64
                  i32.sub
                  local.get $l15
                  local.get $l13
                  i32.const 16
                  i32.add
                  local.get $l40
                  local.get $p8
                  call $f70184
                  local.get $l13
                  i32.const 96
                  i32.add
                  local.get $l32
                  local.get $l13
                  i32.load offset=6276
                  local.get $p1
                  local.get $l17
                  local.get $l13
                  i32.const 80
                  i32.add
                  local.get $l18
                  local.get $l13
                  i32.const 40
                  i32.add
                  local.get $l40
                  local.get $p9
                  call $f70184
                  block $B11
                    block $B12
                      local.get $l13
                      i32.load offset=3176
                      local.tee $l25
                      i32.eqz
                      if $I13
                        i32.const 0
                        local.set $l23
                        br $B12
                      end
                      i32.const 1
                      local.set $l23
                      local.get $l13
                      i32.load offset=96
                      local.set $l14
                      loop $L14
                        local.get $l14
                        if $I15
                          local.get $l13
                          i32.const 3176
                          i32.add
                          local.get $l24
                          i32.const 12
                          i32.mul
                          i32.add
                          local.tee $l18
                          i32.const 4
                          i32.add
                          local.set $l19
                          local.get $l18
                          i32.const 12
                          i32.add
                          local.set $l20
                          local.get $l18
                          i32.const 8
                          i32.add
                          local.set $l30
                          i32.const 0
                          local.set $l18
                          loop $L16
                            local.get $l13
                            i32.const 96
                            i32.add
                            local.get $l18
                            i32.const 12
                            i32.mul
                            i32.add
                            local.tee $l15
                            f32.load offset=8
                            local.tee $l34
                            local.get $l19
                            f32.load
                            local.tee $l35
                            f32.mul
                            local.get $l30
                            f32.load
                            local.tee $l38
                            local.get $l15
                            f32.load offset=4
                            local.tee $l39
                            f32.mul
                            f32.sub
                            local.set $l37
                            local.get $l20
                            f32.load
                            local.tee $l42
                            local.get $l39
                            f32.mul
                            local.get $l15
                            f32.load offset=12
                            local.tee $l43
                            local.get $l35
                            f32.mul
                            f32.sub
                            local.set $l39
                            block $B17
                              block $B18
                                local.get $l38
                                local.get $l43
                                f32.mul
                                local.get $l42
                                local.get $l34
                                f32.mul
                                f32.sub
                                local.tee $l42
                                f32.abs
                                f32.const 0x1.0c6f7ap-20 (;=1e-06;)
                                f32.gt
                                br_if $B18
                                local.get $l39
                                f32.abs
                                f32.const 0x1.0c6f7ap-20 (;=1e-06;)
                                f32.gt
                                br_if $B18
                                local.get $l37
                                f32.abs
                                f32.const 0x1.0c6f7ap-20 (;=1e-06;)
                                f32.gt
                                i32.eqz
                                br_if $B17
                              end
                              f32.const 0x0p+0 (;=0;)
                              local.set $l34
                              f32.const 0x0p+0 (;=0;)
                              local.set $l35
                              f32.const 0x0p+0 (;=0;)
                              local.set $l38
                              local.get $l37
                              local.get $l37
                              f32.mul
                              local.get $l42
                              local.get $l42
                              f32.mul
                              local.get $l39
                              local.get $l39
                              f32.mul
                              f32.add
                              f32.add
                              local.tee $l43
                              f32.const 0x0p+0 (;=0;)
                              f32.gt
                              if $I19
                                local.get $l37
                                f32.const 0x1p+0 (;=1;)
                                local.get $l43
                                f32.sqrt
                                f32.div
                                local.tee $l34
                                f32.mul
                                local.set $l38
                                local.get $l39
                                local.get $l34
                                f32.mul
                                local.set $l35
                                local.get $l42
                                local.get $l34
                                f32.mul
                                local.set $l34
                              end
                              local.get $l13
                              local.get $l38
                              f32.store offset=8
                              local.get $l13
                              local.get $l34
                              f32.store
                              local.get $l13
                              local.get $l35
                              f32.store offset=4
                              local.get $l35
                              local.get $l22
                              f32.load offset=4
                              f32.neg
                              f32.mul
                              local.get $l34
                              local.get $l22
                              f32.load
                              f32.mul
                              f32.sub
                              local.get $l38
                              local.get $l22
                              f32.load offset=8
                              f32.mul
                              f32.sub
                              local.tee $l39
                              local.get $l34
                              local.get $l16
                              f32.load
                              f32.mul
                              local.get $l35
                              local.get $l16
                              f32.load offset=4
                              f32.mul
                              f32.add
                              local.get $l38
                              local.get $l16
                              f32.load offset=8
                              f32.mul
                              f32.add
                              local.tee $l37
                              local.get $p0
                              i32.load offset=48
                              local.get $l37
                              i32.reinterpret_f32
                              i32.const -2147483648
                              i32.and
                              i32.or
                              f32.reinterpret_i32
                              f32.mul
                              local.get $l34
                              local.get $l16
                              f32.load offset=12
                              f32.mul
                              local.get $l35
                              local.get $l16
                              f32.load offset=16
                              f32.mul
                              f32.add
                              local.get $l38
                              local.get $l16
                              f32.load offset=20
                              f32.mul
                              f32.add
                              local.tee $l37
                              local.get $p0
                              i32.load offset=52
                              local.get $l37
                              i32.reinterpret_f32
                              i32.const -2147483648
                              i32.and
                              i32.or
                              f32.reinterpret_i32
                              f32.mul
                              f32.add
                              local.get $l34
                              local.get $l16
                              f32.load offset=24
                              f32.mul
                              local.get $l35
                              local.get $l16
                              f32.load offset=28
                              f32.mul
                              f32.add
                              local.get $l38
                              local.get $l16
                              f32.load offset=32
                              f32.mul
                              f32.add
                              local.tee $l37
                              local.get $p0
                              i32.load offset=56
                              local.get $l37
                              i32.reinterpret_f32
                              i32.const -2147483648
                              i32.and
                              i32.or
                              f32.reinterpret_i32
                              f32.mul
                              f32.add
                              local.tee $l37
                              local.get $p0
                              f32.load offset=44
                              local.tee $l42
                              local.get $l37
                              local.get $l42
                              f32.gt
                              select
                              local.get $l34
                              local.get $l17
                              f32.load
                              f32.mul
                              local.get $l35
                              local.get $l17
                              f32.load offset=4
                              f32.mul
                              f32.add
                              local.get $l38
                              local.get $l17
                              f32.load offset=8
                              f32.mul
                              f32.add
                              local.tee $l37
                              local.get $p1
                              i32.load offset=48
                              local.get $l37
                              i32.reinterpret_f32
                              i32.const -2147483648
                              i32.and
                              i32.or
                              f32.reinterpret_i32
                              f32.mul
                              local.get $l34
                              local.get $l17
                              f32.load offset=12
                              f32.mul
                              local.get $l35
                              local.get $l17
                              f32.load offset=16
                              f32.mul
                              f32.add
                              local.get $l38
                              local.get $l17
                              f32.load offset=20
                              f32.mul
                              f32.add
                              local.tee $l37
                              local.get $p1
                              i32.load offset=52
                              local.get $l37
                              i32.reinterpret_f32
                              i32.const -2147483648
                              i32.and
                              i32.or
                              f32.reinterpret_i32
                              f32.mul
                              f32.add
                              local.get $l34
                              local.get $l17
                              f32.load offset=24
                              f32.mul
                              local.get $l35
                              local.get $l17
                              f32.load offset=28
                              f32.mul
                              f32.add
                              local.get $l38
                              local.get $l17
                              f32.load offset=32
                              f32.mul
                              f32.add
                              local.tee $l34
                              local.get $p1
                              i32.load offset=56
                              local.get $l34
                              i32.reinterpret_f32
                              i32.const -2147483648
                              i32.and
                              i32.or
                              f32.reinterpret_i32
                              f32.mul
                              f32.add
                              local.tee $l34
                              local.get $p1
                              f32.load offset=44
                              local.tee $l35
                              local.get $l34
                              local.get $l35
                              f32.gt
                              select
                              f32.add
                              local.tee $l34
                              f32.add
                              local.tee $l35
                              local.get $l34
                              local.get $l39
                              f32.sub
                              local.tee $l34
                              local.get $l34
                              local.get $l35
                              f32.gt
                              select
                              local.get $l36
                              f32.gt
                              br_if $B17
                              local.get $p0
                              local.get $l13
                              local.get $l16
                              local.get $p8
                              local.get $l13
                              i32.const 6324
                              i32.add
                              local.get $l13
                              i32.const 6320
                              i32.add
                              local.get $p0
                              i32.load offset=64
                              call_indirect $__indirect_function_table (type $t11)
                              local.get $l13
                              f32.load offset=6324
                              local.set $l35
                              local.get $l13
                              f32.load offset=6320
                              local.set $l34
                              local.get $p1
                              local.get $l13
                              local.get $l17
                              local.get $p9
                              local.get $l13
                              i32.const 6332
                              i32.add
                              local.get $l13
                              i32.const 6328
                              i32.add
                              local.get $p1
                              i32.load offset=64
                              call_indirect $__indirect_function_table (type $t11)
                              i32.const 0
                              local.set $l15
                              block $B20
                                local.get $l13
                                f32.load offset=6332
                                local.tee $l38
                                local.get $l34
                                local.get $l40
                                f32.add
                                f32.gt
                                br_if $B20
                                local.get $l13
                                f32.load offset=6328
                                local.tee $l39
                                local.get $l40
                                f32.add
                                local.get $l35
                                f32.lt
                                br_if $B20
                                local.get $l34
                                local.get $l38
                                f32.sub
                                local.tee $l34
                                local.get $l39
                                local.get $l35
                                f32.sub
                                local.tee $l35
                                local.get $l34
                                local.get $l35
                                f32.lt
                                select
                                local.set $l41
                                i32.const 1
                                local.set $l15
                              end
                              block $B21
                                local.get $l15
                                i32.eqz
                                br_if $B21
                                local.get $l36
                                local.get $l41
                                f32.gt
                                i32.eqz
                                br_if $B21
                                local.get $l13
                                f32.load offset=8
                                local.set $l45
                                local.get $l13
                                f32.load offset=4
                                local.set $l46
                                local.get $l13
                                f32.load
                                local.set $l47
                                local.get $l29
                                i32.const 2
                                i32.store
                                local.get $l41
                                local.set $l36
                              end
                              local.get $l15
                              i32.eqz
                              br_if $B11
                            end
                            local.get $l18
                            i32.const 1
                            i32.add
                            local.tee $l18
                            local.get $l14
                            i32.ne
                            br_if $L16
                          end
                        end
                        local.get $l24
                        i32.const 1
                        i32.add
                        local.tee $l24
                        local.get $l25
                        i32.lt_u
                        local.set $l23
                        local.get $l24
                        local.get $l25
                        i32.ne
                        br_if $L14
                      end
                    end
                    local.get $l33
                    local.get $l36
                    f32.store
                    local.get $l28
                    local.get $l45
                    f32.store offset=8
                    local.get $l28
                    local.get $l46
                    f32.store offset=4
                    local.get $l28
                    local.get $l47
                    f32.store
                  end
                  local.get $l23
                  i32.const 1
                  i32.xor
                end
                local.set $l14
                local.get $l13
                i32.const 6336
                i32.add
                global.set $g0
                local.get $l14
                i32.const 1
                i32.and
                i32.eqz
                br_if $B4
                local.get $l12
                f32.load offset=424
                local.set $l40
                local.get $l12
                f32.load offset=420
                local.set $l44
                local.get $l12
                f32.load offset=416
                local.set $l37
              end
              local.get $l12
              f32.load offset=432
              local.get $l37
              f32.mul
              local.get $l12
              f32.load offset=436
              local.get $l44
              f32.mul
              f32.add
              local.get $l12
              f32.load offset=440
              local.get $l40
              f32.mul
              f32.add
              f32.const 0x0p+0 (;=0;)
              f32.lt
              if $I22
                local.get $l12
                local.get $l40
                f32.neg
                local.tee $l40
                f32.store offset=424
                local.get $l12
                local.get $l44
                f32.neg
                local.tee $l44
                f32.store offset=420
                local.get $l12
                local.get $l37
                f32.neg
                local.tee $l37
                f32.store offset=416
              end
              block $B23
                block $B24
                  local.get $l12
                  i32.load offset=256
                  br_table $B3 $B24 $B23 $B2
                end
                local.get $p0
                i32.load offset=68
                local.set $l14
                local.get $l12
                local.get $l37
                local.get $l12
                f32.load offset=520
                f32.mul
                local.get $l44
                local.get $l12
                f32.load offset=524
                f32.mul
                f32.add
                local.get $l40
                local.get $l12
                f32.load offset=528
                f32.mul
                f32.add
                f32.store offset=200
                local.get $l12
                local.get $l37
                local.get $l12
                f32.load offset=508
                f32.mul
                local.get $l44
                local.get $l12
                f32.load offset=512
                f32.mul
                f32.add
                local.get $l40
                local.get $l12
                f32.load offset=516
                f32.mul
                f32.add
                f32.store offset=196
                local.get $l12
                local.get $l12
                f32.load offset=496
                local.get $l37
                f32.mul
                local.get $l12
                f32.load offset=500
                local.get $l44
                f32.mul
                f32.add
                local.get $l12
                f32.load offset=504
                local.get $l40
                f32.mul
                f32.add
                f32.store offset=192
                local.get $p0
                local.get $p8
                local.get $l12
                i32.const 192
                i32.add
                local.get $l14
                call_indirect $__indirect_function_table (type $t3)
                local.set $l26
                local.get $l12
                i32.load offset=272
                local.set $l27
                br $B2
              end
              local.get $p0
              i32.load offset=68
              local.set $l14
              local.get $l12
              local.get $l37
              local.get $l12
              f32.load offset=520
              f32.mul
              local.get $l44
              local.get $l12
              f32.load offset=524
              f32.mul
              f32.add
              local.get $l40
              local.get $l12
              f32.load offset=528
              f32.mul
              f32.add
              f32.store offset=200
              local.get $l12
              local.get $l37
              local.get $l12
              f32.load offset=508
              f32.mul
              local.get $l44
              local.get $l12
              f32.load offset=512
              f32.mul
              f32.add
              local.get $l40
              local.get $l12
              f32.load offset=516
              f32.mul
              f32.add
              f32.store offset=196
              local.get $l12
              local.get $l12
              f32.load offset=496
              local.get $l37
              f32.mul
              local.get $l12
              f32.load offset=500
              local.get $l44
              f32.mul
              f32.add
              local.get $l12
              f32.load offset=504
              local.get $l40
              f32.mul
              f32.add
              f32.store offset=192
              local.get $p0
              local.get $p8
              local.get $l12
              i32.const 192
              i32.add
              local.get $l14
              call_indirect $__indirect_function_table (type $t3)
              local.set $l26
              local.get $p1
              i32.load offset=68
              local.set $l14
              local.get $l12
              local.get $l12
              f32.load offset=476
              local.get $l44
              f32.neg
              local.tee $l36
              f32.mul
              local.get $l37
              local.get $l12
              f32.load offset=472
              f32.mul
              f32.sub
              local.get $l40
              local.get $l12
              f32.load offset=480
              f32.mul
              f32.sub
              f32.store offset=200
              local.get $l12
              local.get $l12
              f32.load offset=464
              local.get $l36
              f32.mul
              local.get $l37
              local.get $l12
              f32.load offset=460
              f32.mul
              f32.sub
              local.get $l40
              local.get $l12
              f32.load offset=468
              f32.mul
              f32.sub
              f32.store offset=196
              local.get $l12
              local.get $l12
              f32.load offset=452
              local.get $l36
              f32.mul
              local.get $l37
              local.get $l12
              f32.load offset=448
              f32.mul
              f32.sub
              local.get $l40
              local.get $l12
              f32.load offset=456
              f32.mul
              f32.sub
              f32.store offset=192
              local.get $p1
              local.get $p9
              local.get $l12
              i32.const 192
              i32.add
              local.get $l14
              call_indirect $__indirect_function_table (type $t3)
              local.set $l27
              br $B2
            end
            i32.const 0
            local.set $l14
            br $B0
          end
          local.get $p1
          i32.load offset=68
          local.set $l14
          local.get $l12
          i32.load offset=304
          local.set $l26
          local.get $l12
          local.get $l12
          f32.load offset=476
          local.get $l44
          f32.neg
          local.tee $l36
          f32.mul
          local.get $l37
          local.get $l12
          f32.load offset=472
          f32.mul
          f32.sub
          local.get $l40
          local.get $l12
          f32.load offset=480
          f32.mul
          f32.sub
          f32.store offset=200
          local.get $l12
          local.get $l12
          f32.load offset=464
          local.get $l36
          f32.mul
          local.get $l37
          local.get $l12
          f32.load offset=460
          f32.mul
          f32.sub
          local.get $l40
          local.get $l12
          f32.load offset=468
          f32.mul
          f32.sub
          f32.store offset=196
          local.get $l12
          local.get $l12
          f32.load offset=452
          local.get $l36
          f32.mul
          local.get $l37
          local.get $l12
          f32.load offset=448
          f32.mul
          f32.sub
          local.get $l40
          local.get $l12
          f32.load offset=456
          f32.mul
          f32.sub
          f32.store offset=192
          local.get $p1
          local.get $p9
          local.get $l12
          i32.const 192
          i32.add
          local.get $l14
          call_indirect $__indirect_function_table (type $t3)
          local.set $l27
        end
        local.get $l12
        f32.load offset=428
        local.tee $l36
        f32.const 0x0p+0 (;=0;)
        f32.ge
        local.set $l13
        local.get $l36
        f32.neg
        local.set $l36
        local.get $l27
        i32.const 20
        i32.mul
        local.set $l19
        local.get $p1
        i32.load offset=24
        local.set $l16
        local.get $p0
        i32.load offset=24
        local.get $l26
        i32.const 20
        i32.mul
        i32.add
        local.set $l14
        block $B25 (result f32)
          local.get $p10
          if $I26
            local.get $l14
            i64.load align=4
            local.set $l77
            local.get $l12
            local.get $l14
            i64.load offset=8 align=4
            i64.store offset=296
            local.get $l12
            local.get $l77
            i64.store offset=288
            local.get $l14
            f32.load
            local.tee $l38
            local.get $l12
            f32.load offset=504
            local.tee $l34
            f32.mul
            local.get $l14
            f32.load offset=4
            local.tee $l35
            local.get $l12
            f32.load offset=516
            local.tee $l41
            f32.mul
            f32.add
            local.get $l14
            f32.load offset=8
            local.tee $l42
            local.get $l12
            f32.load offset=528
            local.tee $l45
            f32.mul
            f32.add
            local.set $l55
            local.get $l38
            local.get $l12
            f32.load offset=496
            local.tee $l50
            f32.mul
            local.get $l35
            local.get $l12
            f32.load offset=508
            local.tee $l51
            f32.mul
            f32.add
            local.get $l42
            local.get $l12
            f32.load offset=520
            local.tee $l49
            f32.mul
            f32.add
            local.set $l54
            local.get $l38
            local.get $l12
            f32.load offset=500
            local.tee $l46
            f32.mul
            local.get $l35
            local.get $l12
            f32.load offset=512
            local.tee $l47
            f32.mul
            f32.add
            local.get $l42
            local.get $l12
            f32.load offset=524
            local.tee $l48
            f32.mul
            f32.add
            br $B25
          end
          local.get $l12
          local.get $l14
          f32.load offset=12
          f32.const 0x1p+0 (;=1;)
          local.get $p8
          f32.load offset=36
          local.get $l14
          f32.load
          local.tee $l34
          f32.mul
          local.get $p8
          f32.load offset=40
          local.get $l14
          f32.load offset=4
          local.tee $l41
          f32.mul
          f32.add
          local.get $p8
          f32.load offset=44
          local.get $l14
          f32.load offset=8
          local.tee $l38
          f32.mul
          f32.add
          local.tee $l42
          local.get $l42
          f32.mul
          local.get $l34
          local.get $p8
          f32.load offset=48
          f32.mul
          local.get $l41
          local.get $p8
          f32.load offset=52
          f32.mul
          f32.add
          local.get $l38
          local.get $p8
          f32.load offset=56
          f32.mul
          f32.add
          local.tee $l35
          local.get $l35
          f32.mul
          f32.add
          local.get $l34
          local.get $p8
          f32.load offset=60
          f32.mul
          local.get $l41
          local.get $p8
          f32.load offset=64
          f32.mul
          f32.add
          local.get $l38
          local.get $p8
          f32.load offset=68
          f32.mul
          f32.add
          local.tee $l39
          local.get $l39
          f32.mul
          f32.add
          f32.sqrt
          f32.div
          local.tee $l38
          f32.mul
          f32.store offset=300
          local.get $l12
          local.get $l35
          local.get $l38
          f32.mul
          local.tee $l35
          f32.store offset=292
          local.get $l12
          f32.load offset=516
          local.set $l41
          local.get $l12
          local.get $l42
          local.get $l38
          f32.mul
          local.tee $l42
          f32.store offset=288
          local.get $l12
          f32.load offset=504
          local.set $l34
          local.get $l12
          local.get $l39
          local.get $l38
          f32.mul
          local.tee $l38
          f32.store offset=296
          local.get $l42
          local.get $l34
          f32.mul
          local.get $l35
          local.get $l41
          f32.mul
          f32.add
          local.get $l38
          local.get $l12
          f32.load offset=528
          local.tee $l45
          f32.mul
          f32.add
          local.set $l55
          local.get $l12
          f32.load offset=496
          local.tee $l50
          local.get $l42
          f32.mul
          local.get $l35
          local.get $l12
          f32.load offset=508
          local.tee $l51
          f32.mul
          f32.add
          local.get $l38
          local.get $l12
          f32.load offset=520
          local.tee $l49
          f32.mul
          f32.add
          local.set $l54
          local.get $l12
          f32.load offset=500
          local.tee $l46
          local.get $l42
          f32.mul
          local.get $l35
          local.get $l12
          f32.load offset=512
          local.tee $l47
          f32.mul
          f32.add
          local.get $l38
          local.get $l12
          f32.load offset=524
          local.tee $l48
          f32.mul
          f32.add
        end
        local.set $l57
        f32.const 0x0p+0 (;=0;)
        local.get $l36
        local.get $l13
        select
        local.set $l38
        local.get $l16
        local.get $l19
        i32.add
        local.set $l13
        local.get $l12
        local.get $l55
        f32.store offset=312
        local.get $l12
        local.get $l57
        f32.store offset=308
        local.get $l12
        local.get $l54
        f32.store offset=304
        block $B27
          local.get $p11
          if $I28
            local.get $l13
            i64.load align=4
            local.set $l77
            local.get $l12
            local.get $l13
            i64.load offset=8 align=4
            i64.store offset=264
            local.get $l12
            local.get $l77
            i64.store offset=256
            local.get $l13
            f32.load
            local.tee $l36
            local.get $l12
            f32.load offset=456
            f32.mul
            local.get $l13
            f32.load offset=4
            local.tee $l39
            local.get $l12
            f32.load offset=468
            f32.mul
            f32.add
            local.set $l35
            local.get $l36
            local.get $l12
            f32.load offset=452
            f32.mul
            local.get $l39
            local.get $l12
            f32.load offset=464
            f32.mul
            f32.add
            local.set $l42
            local.get $l36
            local.get $l12
            f32.load offset=448
            f32.mul
            local.get $l39
            local.get $l12
            f32.load offset=460
            f32.mul
            f32.add
            local.set $l39
            local.get $l13
            f32.load offset=8
            local.set $l36
            br $B27
          end
          local.get $l12
          local.get $l13
          f32.load offset=12
          f32.const 0x1p+0 (;=1;)
          local.get $p9
          f32.load offset=36
          local.get $l13
          f32.load
          local.tee $l36
          f32.mul
          local.get $p9
          f32.load offset=40
          local.get $l13
          f32.load offset=4
          local.tee $l35
          f32.mul
          f32.add
          local.get $p9
          f32.load offset=44
          local.get $l13
          f32.load offset=8
          local.tee $l42
          f32.mul
          f32.add
          local.tee $l43
          local.get $l43
          f32.mul
          local.get $l36
          local.get $p9
          f32.load offset=48
          f32.mul
          local.get $l35
          local.get $p9
          f32.load offset=52
          f32.mul
          f32.add
          local.get $l42
          local.get $p9
          f32.load offset=56
          f32.mul
          f32.add
          local.tee $l39
          local.get $l39
          f32.mul
          f32.add
          local.get $l36
          local.get $p9
          f32.load offset=60
          f32.mul
          local.get $l35
          local.get $p9
          f32.load offset=64
          f32.mul
          f32.add
          local.get $l42
          local.get $p9
          f32.load offset=68
          f32.mul
          f32.add
          local.tee $l36
          local.get $l36
          f32.mul
          f32.add
          f32.sqrt
          f32.div
          local.tee $l35
          f32.mul
          f32.store offset=268
          local.get $l12
          local.get $l36
          local.get $l35
          f32.mul
          local.tee $l36
          f32.store offset=264
          local.get $l12
          local.get $l39
          local.get $l35
          f32.mul
          local.tee $l39
          f32.store offset=260
          local.get $l12
          f32.load offset=468
          local.set $l42
          local.get $l12
          local.get $l43
          local.get $l35
          f32.mul
          local.tee $l43
          f32.store offset=256
          local.get $l43
          local.get $l12
          f32.load offset=456
          f32.mul
          local.get $l39
          local.get $l42
          f32.mul
          f32.add
          local.set $l35
          local.get $l12
          f32.load offset=452
          local.get $l43
          f32.mul
          local.get $l39
          local.get $l12
          f32.load offset=464
          f32.mul
          f32.add
          local.set $l42
          local.get $l12
          f32.load offset=448
          local.get $l43
          f32.mul
          local.get $l39
          local.get $l12
          f32.load offset=460
          f32.mul
          f32.add
          local.set $l39
        end
        local.get $l12
        local.get $l35
        local.get $l36
        local.get $l12
        f32.load offset=480
        f32.mul
        f32.add
        local.tee $l56
        f32.store offset=280
        local.get $l12
        local.get $l39
        local.get $l36
        local.get $l12
        f32.load offset=472
        f32.mul
        f32.add
        local.tee $l58
        f32.store offset=272
        local.get $l12
        local.get $l42
        local.get $l36
        local.get $l12
        f32.load offset=476
        f32.mul
        f32.add
        local.tee $l59
        f32.store offset=276
        local.get $l12
        local.get $l40
        local.get $l38
        local.get $p6
        f32.load offset=4
        f32.add
        local.tee $l74
        f32.neg
        local.tee $l36
        f32.mul
        local.tee $l38
        f32.store offset=248
        local.get $l12
        local.get $l44
        local.get $l36
        f32.mul
        local.tee $l35
        f32.store offset=244
        local.get $l12
        local.get $l37
        local.get $l36
        f32.mul
        local.tee $l36
        f32.store offset=240
        local.get $l12
        f32.load offset=540
        local.set $l42
        local.get $l12
        f32.load offset=536
        local.set $l39
        local.get $l12
        f32.load offset=532
        local.set $l43
        local.get $l12
        local.get $l45
        f32.store offset=224
        local.get $l12
        local.get $l48
        f32.store offset=220
        local.get $l12
        local.get $l49
        f32.store offset=216
        local.get $l12
        local.get $l41
        f32.store offset=212
        local.get $l12
        local.get $l47
        f32.store offset=208
        local.get $l12
        local.get $l51
        f32.store offset=204
        local.get $l12
        local.get $l34
        f32.store offset=200
        local.get $l12
        local.get $l46
        f32.store offset=196
        local.get $l12
        local.get $l50
        f32.store offset=192
        local.get $l12
        local.get $l43
        local.get $l36
        f32.sub
        local.tee $l48
        f32.store offset=228
        local.get $l12
        local.get $l39
        local.get $l35
        f32.sub
        local.tee $l50
        f32.store offset=232
        local.get $l12
        local.get $l42
        local.get $l38
        f32.sub
        local.tee $l51
        f32.store offset=236
        local.get $p4
        f32.load offset=8
        local.set $l34
        local.get $p4
        f32.load offset=4
        local.set $l41
        local.get $p4
        f32.load
        local.set $l38
        local.get $p4
        f32.load offset=12
        local.set $l36
        local.get $l12
        local.get $p5
        f32.load offset=12
        local.tee $l35
        local.get $l35
        f32.mul
        f32.const -0x1p-1 (;=-0.5;)
        f32.add
        local.tee $l49
        local.get $l51
        local.get $p5
        f32.load offset=24
        local.tee $l60
        f32.sub
        local.tee $l42
        local.get $l42
        f32.add
        local.tee $l45
        f32.mul
        local.get $l35
        local.get $p5
        f32.load offset=4
        local.tee $l42
        local.get $l48
        local.get $p5
        f32.load offset=16
        local.tee $l61
        f32.sub
        local.tee $l39
        local.get $l39
        f32.add
        local.tee $l46
        f32.mul
        local.get $p5
        f32.load
        local.tee $l39
        local.get $l50
        local.get $p5
        f32.load offset=20
        local.tee $l64
        f32.sub
        local.tee $l43
        local.get $l43
        f32.add
        local.tee $l47
        f32.mul
        f32.sub
        f32.mul
        f32.add
        local.get $p5
        f32.load offset=8
        local.tee $l43
        local.get $l47
        local.get $l42
        f32.neg
        f32.mul
        local.get $l39
        local.get $l46
        f32.mul
        f32.sub
        local.get $l43
        local.get $l45
        f32.mul
        f32.sub
        local.tee $l52
        f32.mul
        f32.sub
        f32.store offset=188
        local.get $l12
        local.get $l49
        local.get $l47
        f32.mul
        local.get $l35
        local.get $l39
        local.get $l45
        f32.mul
        local.get $l43
        local.get $l46
        f32.mul
        f32.sub
        f32.mul
        f32.add
        local.get $l42
        local.get $l52
        f32.mul
        f32.sub
        f32.store offset=184
        local.get $l12
        local.get $l49
        local.get $l46
        f32.mul
        local.get $l35
        local.get $l43
        local.get $l47
        f32.mul
        local.get $l42
        local.get $l45
        f32.mul
        f32.sub
        f32.mul
        f32.add
        local.get $l39
        local.get $l52
        f32.mul
        f32.sub
        f32.store offset=180
        local.get $l12
        local.get $l38
        local.get $l42
        f32.mul
        local.tee $l65
        local.get $l34
        local.get $l35
        f32.mul
        local.tee $l66
        local.get $l36
        local.get $l43
        f32.mul
        local.tee $l67
        f32.sub
        local.get $l41
        local.get $l39
        f32.mul
        local.tee $l68
        f32.sub
        f32.add
        local.tee $l46
        local.get $l34
        local.get $l39
        f32.mul
        local.tee $l62
        local.get $l41
        local.get $l35
        f32.mul
        local.tee $l69
        local.get $l36
        local.get $l42
        f32.mul
        local.tee $l70
        f32.sub
        local.get $l38
        local.get $l43
        f32.mul
        local.tee $l71
        f32.sub
        f32.add
        local.tee $l47
        local.get $l47
        f32.add
        local.tee $l49
        f32.mul
        local.tee $l53
        local.get $l34
        local.get $l43
        f32.mul
        local.get $l41
        local.get $l42
        f32.mul
        local.get $l38
        local.get $l39
        f32.mul
        local.get $l36
        local.get $l35
        f32.mul
        f32.add
        f32.add
        f32.add
        local.tee $l45
        local.get $l41
        local.get $l43
        f32.mul
        local.tee $l72
        local.get $l38
        local.get $l35
        f32.mul
        local.tee $l63
        local.get $l36
        local.get $l39
        f32.mul
        local.tee $l73
        f32.sub
        local.get $l34
        local.get $l42
        f32.mul
        local.tee $l75
        f32.sub
        f32.add
        local.tee $l52
        local.get $l52
        f32.add
        local.tee $l35
        f32.mul
        local.tee $l42
        f32.sub
        f32.store offset=172
        local.get $l12
        local.get $l46
        local.get $l35
        f32.mul
        local.tee $l39
        local.get $l45
        local.get $l49
        f32.mul
        local.tee $l43
        f32.add
        f32.store offset=168
        local.get $l12
        local.get $l53
        local.get $l42
        f32.add
        f32.store offset=164
        local.get $l12
        local.get $l47
        local.get $l35
        f32.mul
        local.tee $l42
        local.get $l45
        local.get $l46
        local.get $l46
        f32.add
        local.tee $l76
        f32.mul
        local.tee $l53
        f32.sub
        f32.store offset=156
        local.get $l12
        local.get $l39
        local.get $l43
        f32.sub
        f32.store offset=152
        local.get $l12
        local.get $l42
        local.get $l53
        f32.add
        f32.store offset=148
        local.get $l12
        local.get $l36
        local.get $l36
        f32.mul
        f32.const -0x1p-1 (;=-0.5;)
        f32.add
        local.tee $l53
        local.get $l60
        local.get $l51
        f32.sub
        local.tee $l42
        local.get $l42
        f32.add
        local.tee $l42
        f32.mul
        local.get $l36
        local.get $l41
        local.get $l61
        local.get $l48
        f32.sub
        local.tee $l39
        local.get $l39
        f32.add
        local.tee $l39
        f32.mul
        local.get $l38
        local.get $l64
        local.get $l50
        f32.sub
        local.tee $l43
        local.get $l43
        f32.add
        local.tee $l43
        f32.mul
        f32.sub
        f32.mul
        f32.add
        local.get $l34
        local.get $l43
        local.get $l41
        f32.neg
        f32.mul
        local.get $l38
        local.get $l39
        f32.mul
        f32.sub
        local.get $l34
        local.get $l42
        f32.mul
        f32.sub
        local.tee $l48
        f32.mul
        f32.sub
        f32.store offset=140
        local.get $l12
        local.get $l53
        local.get $l43
        f32.mul
        local.get $l36
        local.get $l38
        local.get $l42
        f32.mul
        local.get $l34
        local.get $l39
        f32.mul
        f32.sub
        f32.mul
        f32.add
        local.get $l41
        local.get $l48
        f32.mul
        f32.sub
        f32.store offset=136
        local.get $l12
        local.get $l53
        local.get $l39
        f32.mul
        local.get $l36
        local.get $l34
        local.get $l43
        f32.mul
        local.get $l41
        local.get $l42
        f32.mul
        f32.sub
        f32.mul
        f32.add
        local.get $l38
        local.get $l48
        f32.mul
        f32.sub
        f32.store offset=132
        local.get $l12
        local.get $l68
        local.get $l67
        local.get $l66
        f32.sub
        local.get $l65
        f32.sub
        f32.add
        local.tee $l36
        local.get $l71
        local.get $l70
        local.get $l69
        f32.sub
        local.get $l62
        f32.sub
        f32.add
        local.tee $l34
        local.get $l34
        f32.add
        local.tee $l38
        f32.mul
        local.tee $l39
        local.get $l45
        local.get $l75
        local.get $l73
        local.get $l63
        f32.sub
        local.get $l72
        f32.sub
        f32.add
        local.tee $l42
        local.get $l42
        f32.add
        local.tee $l41
        f32.mul
        local.tee $l43
        f32.sub
        f32.store offset=124
        local.get $l12
        local.get $l36
        local.get $l41
        f32.mul
        local.tee $l48
        local.get $l45
        local.get $l38
        f32.mul
        local.tee $l50
        f32.add
        f32.store offset=120
        local.get $l12
        local.get $l39
        local.get $l43
        f32.add
        f32.store offset=116
        local.get $l12
        local.get $l34
        local.get $l41
        f32.mul
        local.tee $l39
        local.get $l45
        local.get $l36
        local.get $l36
        f32.add
        local.tee $l43
        f32.mul
        local.tee $l45
        f32.sub
        f32.store offset=108
        local.get $l12
        local.get $l48
        local.get $l50
        f32.sub
        f32.store offset=104
        local.get $l12
        local.get $l39
        local.get $l45
        f32.add
        f32.store offset=100
        local.get $l12
        f32.const 0x1p+0 (;=1;)
        local.get $l52
        local.get $l35
        f32.mul
        f32.sub
        local.tee $l35
        local.get $l47
        local.get $l49
        f32.mul
        local.tee $l39
        f32.sub
        f32.store offset=176
        local.get $l12
        local.get $l35
        local.get $l46
        local.get $l76
        f32.mul
        local.tee $l45
        f32.sub
        f32.store offset=160
        local.get $l12
        f32.const 0x1p+0 (;=1;)
        local.get $l39
        f32.sub
        local.get $l45
        f32.sub
        f32.store offset=144
        local.get $l12
        f32.const 0x1p+0 (;=1;)
        local.get $l42
        local.get $l41
        f32.mul
        f32.sub
        local.tee $l41
        local.get $l34
        local.get $l38
        f32.mul
        local.tee $l34
        f32.sub
        f32.store offset=128
        local.get $l12
        local.get $l41
        local.get $l36
        local.get $l43
        f32.mul
        local.tee $l36
        f32.sub
        f32.store offset=112
        local.get $l12
        f32.const 0x1p+0 (;=1;)
        local.get $l34
        f32.sub
        local.get $l36
        f32.sub
        f32.store offset=96
        local.get $l54
        local.get $l37
        f32.mul
        local.get $l57
        local.get $l44
        f32.mul
        f32.add
        local.get $l55
        local.get $l40
        f32.mul
        f32.add
        local.set $l36
        local.get $l37
        local.get $l58
        f32.mul
        local.get $l44
        local.get $l59
        f32.mul
        f32.add
        local.get $l40
        local.get $l56
        f32.mul
        f32.add
        local.set $l40
        local.get $l14
        i32.load8_u offset=18
        local.set $l19
        i32.const 0
        local.set $l16
        i32.const 0
        local.set $l20
        i32.const 0
        local.set $l15
        local.get $p10
        i32.eqz
        if $I29
          local.get $l21
          local.get $l19
          i32.const 12
          i32.mul
          i32.const 15
          i32.add
          i32.const 8176
          i32.and
          i32.sub
          local.tee $l20
          local.tee $l21
          global.set $g0
          local.get $l21
          local.get $l19
          i32.const 15
          i32.add
          i32.const 496
          i32.and
          i32.sub
          local.tee $l15
          local.tee $l21
          global.set $g0
        end
        local.get $l36
        f32.abs
        local.set $l36
        local.get $l40
        f32.abs
        local.set $l40
        local.get $l12
        i32.const 92
        i32.add
        local.get $l12
        i32.const 88
        i32.add
        local.get $l20
        local.get $l15
        local.get $p10
        local.get $p0
        i32.load offset=28
        local.get $p0
        i32.load offset=32
        local.get $l14
        i32.load16_u offset=16
        i32.add
        local.get $l19
        local.get $p8
        call $f69921
        local.get $l13
        i32.load8_u offset=18
        local.set $l19
        i32.const 0
        local.set $l20
        local.get $p11
        i32.eqz
        if $I30
          local.get $l21
          local.get $l19
          i32.const 12
          i32.mul
          i32.const 15
          i32.add
          i32.const 8176
          i32.and
          i32.sub
          local.tee $l16
          local.tee $l21
          global.set $g0
          local.get $l21
          local.get $l19
          i32.const 15
          i32.add
          i32.const 496
          i32.and
          i32.sub
          local.tee $l20
          local.tee $l21
          global.set $g0
        end
        local.get $l14
        i32.const 18
        i32.add
        local.set $l15
        local.get $l12
        i32.const 84
        i32.add
        local.get $l12
        i32.const 80
        i32.add
        local.get $l16
        local.get $l20
        local.get $p11
        local.get $p1
        i32.load offset=28
        local.get $p1
        i32.load offset=32
        local.get $l13
        i32.load16_u offset=16
        i32.add
        local.get $l19
        local.get $p9
        call $f69921
        local.get $l13
        i32.const 18
        i32.add
        local.set $l13
        local.get $l12
        i32.const 40
        i32.add
        local.get $l12
        i32.const 288
        i32.add
        call $f70172
        local.get $l12
        local.get $l12
        i32.const 256
        i32.add
        call $f70172
        block $B31
          block $B32
            local.get $l36
            local.get $l40
            f32.gt
            if $I33
              i32.const 1
              local.set $l14
              local.get $l15
              i32.load8_u
              local.get $l12
              i32.load offset=92
              local.get $l12
              i32.load offset=88
              local.get $l12
              i32.const 192
              i32.add
              local.get $l12
              i32.const 288
              i32.add
              local.get $l12
              i32.const 40
              i32.add
              local.get $l13
              i32.load8_u
              local.get $l12
              i32.load offset=84
              local.get $l12
              i32.load offset=80
              local.get $l12
              i32.const 448
              i32.add
              local.get $l12
              i32.const 256
              i32.add
              local.get $l12
              local.get $l12
              i32.const 304
              i32.add
              local.get $l12
              i32.const 144
              i32.add
              local.get $l12
              i32.const 96
              i32.add
              i32.const -1
              local.get $p7
              i32.const 1
              local.get $l12
              i32.const 240
              i32.add
              local.get $l74
              call $f70173
              i32.eqz
              br_if $B32
              br $B31
            end
            i32.const 1
            local.set $l14
            local.get $l13
            i32.load8_u
            local.get $l12
            i32.load offset=84
            local.get $l12
            i32.load offset=80
            local.get $l12
            i32.const 448
            i32.add
            local.get $l12
            i32.const 256
            i32.add
            local.get $l12
            local.get $l15
            i32.load8_u
            local.get $l12
            i32.load offset=92
            local.get $l12
            i32.load offset=88
            local.get $l12
            i32.const 192
            i32.add
            local.get $l12
            i32.const 288
            i32.add
            local.get $l12
            i32.const 40
            i32.add
            local.get $l12
            i32.const 272
            i32.add
            local.get $l12
            i32.const 96
            i32.add
            local.get $l12
            i32.const 144
            i32.add
            i32.const -1
            local.get $p7
            i32.const 0
            local.get $l12
            i32.const 240
            i32.add
            local.get $l74
            call $f70173
            br_if $B31
          end
          i32.const 0
          local.set $l14
        end
        local.get $l14
        br_if $B0
        local.get $l31
        i32.const 1
        i32.sub
        local.set $l13
        local.get $l31
        br_if $L1
      end
    end
    local.get $l12
    i32.const 544
    i32.add
    global.set $g0
    local.get $l14)
