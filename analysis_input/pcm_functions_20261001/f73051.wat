  (func $f73051 (type $t20) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 i32) (param $p7 i32)
    (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 i32) (local $l17 i32) (local $l18 i32) (local $l19 i32) (local $l20 i32) (local $l21 i32) (local $l22 i32) (local $l23 i32) (local $l24 i32) (local $l25 i32) (local $l26 i32) (local $l27 i32) (local $l28 i32) (local $l29 i32) (local $l30 i32) (local $l31 i32) (local $l32 i32) (local $l33 i32) (local $l34 i32) (local $l35 i32) (local $l36 i32) (local $l37 i32) (local $l38 i32) (local $l39 i32) (local $l40 i32) (local $l41 i32) (local $l42 i32) (local $l43 i32) (local $l44 i32) (local $l45 i32) (local $l46 f32) (local $l47 f32) (local $l48 f32) (local $l49 f32) (local $l50 f32) (local $l51 f32) (local $l52 f32) (local $l53 f32) (local $l54 f32) (local $l55 f32) (local $l56 f32) (local $l57 f32) (local $l58 f32) (local $l59 f32) (local $l60 f32) (local $l61 f32) (local $l62 f32) (local $l63 f32) (local $l64 f32) (local $l65 f32) (local $l66 f32) (local $l67 f32) (local $l68 f32) (local $l69 f32) (local $l70 f32) (local $l71 f32) (local $l72 f32) (local $l73 f32) (local $l74 f32) (local $l75 f32) (local $l76 f32) (local $l77 f32) (local $l78 f32) (local $l79 f32) (local $l80 f32) (local $l81 f32) (local $l82 f32) (local $l83 f32) (local $l84 f32) (local $l85 f32) (local $l86 f32) (local $l87 f32) (local $l88 f32) (local $l89 f32) (local $l90 f32) (local $l91 f32) (local $l92 f32) (local $l93 f32) (local $l94 f32) (local $l95 f32) (local $l96 i64) (local $l97 i64)
    global.get $g0
    i32.const 336
    i32.sub
    local.tee $p0
    global.set $g0
    i32.const 9
    call $f80140
    drop
    block $B0
      local.get $p1
      call $f73768
      local.tee $l15
      i32.eqz
      br_if $B0
      local.get $p5
      i32.load offset=4
      local.tee $l16
      i32.const 0
      i32.le_s
      br_if $B0
      local.get $p2
      f32.load
      local.set $l46
      local.get $p2
      f32.load offset=4
      local.set $l50
      local.get $p2
      f32.load offset=8
      local.set $l49
      local.get $p0
      f32.const 0x1p+0 (;=1;)
      local.get $p2
      f32.load offset=12
      f32.div
      f32.store offset=332
      local.get $p0
      f32.const 0x1p+0 (;=1;)
      local.get $l49
      f32.div
      f32.store offset=328
      local.get $p0
      f32.const 0x1p+0 (;=1;)
      local.get $l50
      f32.div
      f32.store offset=324
      local.get $p0
      f32.const 0x1p+0 (;=1;)
      local.get $l46
      f32.div
      f32.store offset=320
      block $B1
        local.get $p3
        i32.load offset=8
        local.tee $l10
        i32.eqz
        if $I2
          f32.const inf (;=inf;)
          local.set $l61
          f32.const -inf (;=-inf;)
          local.set $l67
          f32.const -inf (;=-inf;)
          local.set $l62
          f32.const -inf (;=-inf;)
          local.set $l68
          f32.const -inf (;=-inf;)
          local.set $l69
          f32.const -inf (;=-inf;)
          local.set $l74
          f32.const -inf (;=-inf;)
          local.set $l75
          f32.const -inf (;=-inf;)
          local.set $l76
          f32.const -inf (;=-inf;)
          local.set $l77
          f32.const -inf (;=-inf;)
          local.set $l78
          f32.const -inf (;=-inf;)
          local.set $l79
          f32.const -inf (;=-inf;)
          local.set $l80
          f32.const -inf (;=-inf;)
          local.set $l81
          f32.const inf (;=inf;)
          local.set $l82
          f32.const inf (;=inf;)
          local.set $l83
          f32.const inf (;=inf;)
          local.set $l84
          f32.const inf (;=inf;)
          local.set $l85
          f32.const inf (;=inf;)
          local.set $l86
          f32.const inf (;=inf;)
          local.set $l87
          f32.const inf (;=inf;)
          local.set $l88
          f32.const inf (;=inf;)
          local.set $l89
          f32.const inf (;=inf;)
          local.set $l90
          f32.const inf (;=inf;)
          local.set $l91
          f32.const inf (;=inf;)
          local.set $l92
          br $B1
        end
        local.get $p3
        i32.load
        local.set $l9
        f32.const -inf (;=-inf;)
        local.set $l81
        f32.const inf (;=inf;)
        local.set $l92
        f32.const inf (;=inf;)
        local.set $l91
        f32.const inf (;=inf;)
        local.set $l90
        f32.const inf (;=inf;)
        local.set $l89
        f32.const inf (;=inf;)
        local.set $l88
        f32.const inf (;=inf;)
        local.set $l87
        f32.const inf (;=inf;)
        local.set $l86
        f32.const inf (;=inf;)
        local.set $l85
        f32.const inf (;=inf;)
        local.set $l84
        f32.const inf (;=inf;)
        local.set $l83
        f32.const inf (;=inf;)
        local.set $l82
        f32.const inf (;=inf;)
        local.set $l61
        f32.const -inf (;=-inf;)
        local.set $l80
        f32.const -inf (;=-inf;)
        local.set $l79
        f32.const -inf (;=-inf;)
        local.set $l78
        f32.const -inf (;=-inf;)
        local.set $l77
        f32.const -inf (;=-inf;)
        local.set $l76
        f32.const -inf (;=-inf;)
        local.set $l75
        f32.const -inf (;=-inf;)
        local.set $l74
        f32.const -inf (;=-inf;)
        local.set $l69
        f32.const -inf (;=-inf;)
        local.set $l68
        f32.const -inf (;=-inf;)
        local.set $l62
        f32.const -inf (;=-inf;)
        local.set $l67
        loop $L3
          local.get $l67
          local.get $l9
          local.get $l14
          i32.const 7
          i32.shl
          i32.add
          local.tee $p1
          f32.load offset=16
          local.tee $l46
          local.get $l46
          local.get $l67
          f32.lt
          select
          local.tee $l49
          local.get $p1
          f32.load offset=64
          local.tee $l50
          local.get $l49
          local.get $l50
          f32.gt
          select
          local.set $l67
          local.get $l61
          local.get $l46
          local.get $l46
          local.get $l61
          f32.gt
          select
          local.tee $l46
          local.get $l50
          local.get $l46
          local.get $l50
          f32.lt
          select
          local.set $l61
          local.get $l81
          local.get $p1
          f32.load offset=60
          local.tee $l46
          local.get $l46
          local.get $l81
          f32.lt
          select
          local.tee $l49
          local.get $p1
          f32.load offset=108
          local.tee $l50
          local.get $l49
          local.get $l50
          f32.gt
          select
          local.set $l81
          local.get $l80
          local.get $p1
          f32.load offset=56
          local.tee $l49
          local.get $l49
          local.get $l80
          f32.lt
          select
          local.tee $l57
          local.get $p1
          f32.load offset=104
          local.tee $l47
          local.get $l47
          local.get $l57
          f32.lt
          select
          local.set $l80
          local.get $l79
          local.get $p1
          f32.load offset=52
          local.tee $l57
          local.get $l57
          local.get $l79
          f32.lt
          select
          local.tee $l54
          local.get $p1
          f32.load offset=100
          local.tee $l48
          local.get $l48
          local.get $l54
          f32.lt
          select
          local.set $l79
          local.get $l78
          local.get $p1
          f32.load offset=48
          local.tee $l54
          local.get $l54
          local.get $l78
          f32.lt
          select
          local.tee $l52
          local.get $p1
          f32.load offset=96
          local.tee $l56
          local.get $l52
          local.get $l56
          f32.gt
          select
          local.set $l78
          local.get $l77
          local.get $p1
          f32.load offset=44
          local.tee $l52
          local.get $l52
          local.get $l77
          f32.lt
          select
          local.tee $l51
          local.get $p1
          f32.load offset=92
          local.tee $l58
          local.get $l51
          local.get $l58
          f32.gt
          select
          local.set $l77
          local.get $l76
          local.get $p1
          f32.load offset=40
          local.tee $l51
          local.get $l51
          local.get $l76
          f32.lt
          select
          local.tee $l53
          local.get $p1
          f32.load offset=88
          local.tee $l55
          local.get $l53
          local.get $l55
          f32.gt
          select
          local.set $l76
          local.get $l75
          local.get $p1
          f32.load offset=36
          local.tee $l53
          local.get $l53
          local.get $l75
          f32.lt
          select
          local.tee $l59
          local.get $p1
          f32.load offset=84
          local.tee $l60
          local.get $l59
          local.get $l60
          f32.gt
          select
          local.set $l75
          local.get $l74
          local.get $p1
          f32.load offset=32
          local.tee $l59
          local.get $l59
          local.get $l74
          f32.lt
          select
          local.tee $l63
          local.get $p1
          f32.load offset=80
          local.tee $l64
          local.get $l63
          local.get $l64
          f32.gt
          select
          local.set $l74
          local.get $l69
          local.get $p1
          f32.load offset=28
          local.tee $l63
          local.get $l63
          local.get $l69
          f32.lt
          select
          local.tee $l65
          local.get $p1
          f32.load offset=76
          local.tee $l70
          local.get $l65
          local.get $l70
          f32.gt
          select
          local.set $l69
          local.get $l68
          local.get $p1
          f32.load offset=24
          local.tee $l65
          local.get $l65
          local.get $l68
          f32.lt
          select
          local.tee $l66
          local.get $p1
          f32.load offset=72
          local.tee $l71
          local.get $l66
          local.get $l71
          f32.gt
          select
          local.set $l68
          local.get $l62
          local.get $p1
          f32.load offset=20
          local.tee $l66
          local.get $l62
          local.get $l66
          f32.gt
          select
          local.tee $l62
          local.get $p1
          f32.load offset=68
          local.tee $l72
          local.get $l62
          local.get $l72
          f32.gt
          select
          local.set $l62
          local.get $l92
          local.get $l46
          local.get $l46
          local.get $l92
          f32.gt
          select
          local.tee $l46
          local.get $l50
          local.get $l46
          local.get $l50
          f32.lt
          select
          local.set $l92
          local.get $l91
          local.get $l49
          local.get $l49
          local.get $l91
          f32.gt
          select
          local.tee $l46
          local.get $l47
          local.get $l46
          local.get $l47
          f32.lt
          select
          local.set $l91
          local.get $l90
          local.get $l57
          local.get $l57
          local.get $l90
          f32.gt
          select
          local.tee $l46
          local.get $l48
          local.get $l46
          local.get $l48
          f32.lt
          select
          local.set $l90
          local.get $l89
          local.get $l54
          local.get $l54
          local.get $l89
          f32.gt
          select
          local.tee $l46
          local.get $l56
          local.get $l46
          local.get $l56
          f32.lt
          select
          local.set $l89
          local.get $l88
          local.get $l52
          local.get $l52
          local.get $l88
          f32.gt
          select
          local.tee $l46
          local.get $l58
          local.get $l46
          local.get $l58
          f32.lt
          select
          local.set $l88
          local.get $l87
          local.get $l51
          local.get $l51
          local.get $l87
          f32.gt
          select
          local.tee $l46
          local.get $l55
          local.get $l46
          local.get $l55
          f32.lt
          select
          local.set $l87
          local.get $l86
          local.get $l53
          local.get $l53
          local.get $l86
          f32.gt
          select
          local.tee $l46
          local.get $l60
          local.get $l46
          local.get $l60
          f32.lt
          select
          local.set $l86
          local.get $l85
          local.get $l59
          local.get $l59
          local.get $l85
          f32.gt
          select
          local.tee $l46
          local.get $l64
          local.get $l46
          local.get $l64
          f32.lt
          select
          local.set $l85
          local.get $l84
          local.get $l63
          local.get $l63
          local.get $l84
          f32.gt
          select
          local.tee $l46
          local.get $l70
          local.get $l46
          local.get $l70
          f32.lt
          select
          local.set $l84
          local.get $l83
          local.get $l65
          local.get $l65
          local.get $l83
          f32.gt
          select
          local.tee $l46
          local.get $l71
          local.get $l46
          local.get $l71
          f32.lt
          select
          local.set $l83
          local.get $l82
          local.get $l66
          local.get $l66
          local.get $l82
          f32.gt
          select
          local.tee $l46
          local.get $l72
          local.get $l46
          local.get $l72
          f32.lt
          select
          local.set $l82
          local.get $l73
          local.get $p1
          f32.load offset=112
          local.tee $l46
          local.get $l46
          local.get $l73
          f32.lt
          select
          local.set $l73
          local.get $l93
          local.get $p1
          f32.load offset=124
          local.tee $l46
          local.get $l46
          local.get $l93
          f32.lt
          select
          local.set $l93
          local.get $l94
          local.get $p1
          f32.load offset=120
          local.tee $l46
          local.get $l46
          local.get $l94
          f32.lt
          select
          local.set $l94
          local.get $l95
          local.get $p1
          f32.load offset=116
          local.tee $l46
          local.get $l46
          local.get $l95
          f32.lt
          select
          local.set $l95
          local.get $l14
          i32.const 1
          i32.add
          local.tee $l14
          local.get $l10
          i32.ne
          br_if $L3
        end
      end
      local.get $l89
      local.get $l90
      call $f65476
      local.get $l91
      local.get $l92
      call $f65476
      call $f65476
      local.set $l50
      local.get $l73
      local.get $l95
      call $f65475
      local.get $l94
      local.get $l93
      call $f65475
      call $f65475
      local.set $l46
      local.get $l78
      local.get $l79
      call $f65475
      local.get $l80
      local.get $l81
      call $f65475
      call $f65475
      local.set $l49
      block $B4 (result i32)
        local.get $p0
        i32.const 304
        i32.add
        local.tee $l11
        i64.const 4294967296
        i64.store offset=8 align=4
        local.get $l11
        i32.const 1
        i32.store offset=4
        local.get $l11
        i32.const 0
        i32.store
        local.get $l16
        local.tee $p1
        i32.eqz
        if $I5
          local.get $l11
          i64.const 0
          i64.store offset=8 align=4
          local.get $l11
          br $B4
        end
        local.get $p1
        i32.const 4
        i32.shl
        i32.const 4
        i32.const 1
        i32.const 0
        i32.const 403047
        i32.const 72
        call $f83341
        local.set $l16
        local.get $l11
        local.get $p1
        i32.const 1
        i32.shl
        i32.store offset=12
        local.get $l11
        local.get $p1
        i32.store offset=8
        local.get $l11
        local.get $l16
        i32.store
        local.get $p1
        i32.const 3
        i32.and
        local.set $l13
        local.get $p1
        i32.const 1
        i32.sub
        i32.const 3
        i32.ge_u
        if $I6
          local.get $p1
          i32.const -4
          i32.and
          local.set $l14
          loop $L7
            local.get $l16
            local.get $l8
            i32.const 4
            i32.shl
            local.tee $p1
            i32.add
            local.tee $l9
            i32.const 8
            i32.add
            local.tee $l10
            i64.const 0
            i64.store align=4
            local.get $l9
            i64.const 0
            i64.store align=4
            local.get $l10
            i32.const -1
            i32.store
            local.get $l16
            local.get $p1
            i32.const 16
            i32.or
            i32.add
            local.tee $l9
            i32.const 8
            i32.add
            local.tee $l10
            i64.const 0
            i64.store align=4
            local.get $l9
            i64.const 0
            i64.store align=4
            local.get $l10
            i32.const -1
            i32.store
            local.get $l16
            local.get $p1
            i32.const 32
            i32.or
            i32.add
            local.tee $l9
            i32.const 8
            i32.add
            local.tee $l10
            i64.const 0
            i64.store align=4
            local.get $l9
            i64.const 0
            i64.store align=4
            local.get $l10
            i32.const -1
            i32.store
            local.get $l16
            local.get $p1
            i32.const 48
            i32.or
            i32.add
            local.tee $p1
            i32.const 8
            i32.add
            local.tee $l9
            i64.const 0
            i64.store align=4
            local.get $p1
            i64.const 0
            i64.store align=4
            local.get $l9
            i32.const -1
            i32.store
            local.get $l8
            i32.const 4
            i32.add
            local.set $l8
            local.get $l12
            i32.const 4
            i32.add
            local.tee $l12
            local.get $l14
            i32.ne
            br_if $L7
          end
        end
        local.get $l13
        if $I8
          i32.const 0
          local.set $p1
          loop $L9
            local.get $l16
            local.get $l8
            i32.const 4
            i32.shl
            i32.add
            local.tee $l12
            i32.const 8
            i32.add
            local.tee $l9
            i64.const 0
            i64.store align=4
            local.get $l12
            i64.const 0
            i64.store align=4
            local.get $l9
            i32.const -1
            i32.store
            local.get $l8
            i32.const 1
            i32.add
            local.set $l8
            local.get $p1
            i32.const 1
            i32.add
            local.tee $p1
            local.get $l13
            i32.ne
            br_if $L9
          end
        end
        local.get $l11
      end
      local.set $l22
      local.get $p0
      i32.const 288
      i32.add
      local.get $p5
      i32.load offset=4
      call $f66799
      local.set $l16
      local.get $p0
      local.get $l49
      local.get $l46
      f32.add
      f32.const 0x1.4f8b58p-17 (;=1e-05;)
      f32.add
      local.tee $l49
      local.get $l50
      local.get $l46
      f32.sub
      f32.const -0x1.4f8b58p-17 (;=-1e-05;)
      f32.add
      local.tee $l50
      f32.sub
      f32.const 0x1p-1 (;=0.5;)
      f32.mul
      f32.store offset=68
      local.get $l85
      local.get $l86
      call $f65476
      local.get $l87
      local.get $l88
      call $f65476
      call $f65476
      local.set $l47
      local.get $p0
      i32.const -64
      i32.sub
      local.get $l46
      local.get $l74
      local.get $l75
      call $f65475
      local.get $l76
      local.get $l77
      call $f65475
      call $f65475
      f32.add
      f32.const 0x1.4f8b58p-17 (;=1e-05;)
      f32.add
      local.tee $l57
      local.get $l47
      local.get $l46
      f32.sub
      f32.const -0x1.4f8b58p-17 (;=-1e-05;)
      f32.add
      local.tee $l47
      f32.sub
      f32.const 0x1p-1 (;=0.5;)
      f32.mul
      f32.store
      local.get $l61
      local.get $l82
      call $f65476
      local.get $l83
      local.get $l84
      call $f65476
      call $f65476
      local.set $l48
      local.get $p0
      local.get $l46
      local.get $l67
      local.get $l62
      call $f65475
      local.get $l68
      local.get $l69
      call $f65475
      call $f65475
      f32.add
      f32.const 0x1.4f8b58p-17 (;=1e-05;)
      f32.add
      local.tee $l54
      local.get $l48
      local.get $l46
      f32.sub
      f32.const -0x1.4f8b58p-17 (;=-1e-05;)
      f32.add
      local.tee $l46
      f32.sub
      f32.const 0x1p-1 (;=0.5;)
      f32.mul
      f32.store offset=60
      local.get $p0
      local.get $l50
      local.get $l49
      f32.add
      f32.const 0x1p-1 (;=0.5;)
      f32.mul
      f32.store offset=56
      local.get $p0
      local.get $l47
      local.get $l57
      f32.add
      f32.const 0x1p-1 (;=0.5;)
      f32.mul
      f32.store offset=52
      local.get $p0
      local.get $l46
      local.get $l54
      f32.add
      f32.const 0x1p-1 (;=0.5;)
      f32.mul
      f32.store offset=48
      i32.const 0
      local.set $p1
      local.get $p5
      i32.load offset=4
      local.set $l10
      local.get $l22
      i32.load
      local.set $l12
      local.get $p5
      i32.load
      local.set $l8
      local.get $p5
      i32.load8_u offset=12
      local.set $l14
      global.get $g0
      i32.const 176
      i32.sub
      local.tee $l9
      global.set $g0
      local.get $p0
      i32.const 48
      i32.add
      local.tee $l11
      f32.load offset=20
      local.set $l47
      local.get $l11
      i64.load align=4
      local.set $l96
      local.get $l11
      f32.load offset=8
      local.set $l46
      local.get $l11
      i64.load offset=12 align=4
      local.set $l97
      local.get $l9
      i64.const 0
      i64.store offset=160
      local.get $l9
      i64.const 0
      i64.store offset=152
      local.get $l9
      i32.const 7
      i32.const 5
      local.get $l14
      select
      i32.store16 offset=168
      local.get $l9
      i32.const 96
      i32.add
      local.tee $l11
      local.get $l8
      i32.store offset=12
      local.get $l11
      i64.const 1
      i64.store offset=4 align=4
      local.get $l11
      i32.const 3222432
      i32.store
      local.get $l11
      i32.const 9
      call $f80140
      i32.load8_u offset=56
      i32.store8 offset=16
      local.get $l11
      i64.const 322122547200
      i64.store offset=36 align=4
      local.get $l11
      i64.const 4294967296
      i64.store offset=20 align=4
      local.get $l11
      i32.const 3222408
      i32.store
      local.get $l11
      i64.const 4294967296
      i64.store offset=44 align=4
      local.get $l11
      i64.const 4294967296
      i64.store offset=28 align=4
      block $B10
        local.get $l10
        i32.eqz
        br_if $B10
        local.get $l11
        i32.const 20
        i32.add
        local.get $l10
        i32.const 16
        i32.const 4
        call $f545
        local.get $l11
        i32.load offset=36
        local.tee $l8
        i32.eqz
        br_if $B10
        local.get $l11
        i32.load8_u offset=48
        i32.const 1
        i32.and
        br_if $B10
        local.get $l8
        local.get $l11
        i32.load offset=40
        i32.const 403047
        i32.const 774
        call $f83342
      end
      local.get $l11
      i32.const 0
      i32.store offset=44
      local.get $l11
      local.get $l12
      i32.store offset=36
      local.get $l11
      local.get $l10
      i32.const 1
      i32.shl
      i32.const 1
      i32.or
      i32.store offset=48
      local.get $l11
      local.set $l13
      local.get $l9
      i32.const -1
      i32.store offset=68
      local.get $l9
      i64.const 1
      i64.store offset=84 align=4
      local.get $l9
      local.get $l12
      i32.store offset=80
      i32.const 0
      local.set $l11
      local.get $l9
      i32.const 0
      i32.store8 offset=76
      local.get $l9
      i64.const 0
      i64.store offset=60 align=4
      local.get $l9
      i32.const 3222456
      i32.store offset=56
      local.get $l15
      i32.load offset=8
      local.set $l15
      local.get $l9
      local.get $l47
      f32.store offset=52
      local.get $l9
      local.get $l97
      i64.store offset=44 align=4
      local.get $l9
      i32.const 3
      i32.store offset=40
      local.get $l9
      local.get $l46
      f32.store offset=32
      local.get $l9
      local.get $l96
      i64.store offset=24
      local.get $l9
      i64.const 4575657221408423936
      i64.store offset=16
      local.get $l9
      i64.const 0
      i64.store offset=8
      local.get $l15
      local.get $l9
      i32.const 40
      i32.add
      local.get $l9
      i32.const 8
      i32.add
      local.get $l9
      i32.const 56
      i32.add
      local.get $l9
      i32.const 152
      i32.add
      local.get $l13
      local.get $l15
      i32.load
      i32.load offset=356
      call_indirect $__indirect_function_table (type $t10)
      drop
      local.get $l13
      i32.load offset=28
      local.tee $l8
      local.get $l13
      i32.load offset=44
      i32.add
      local.tee $l15
      local.get $l10
      local.get $l10
      local.get $l15
      i32.gt_s
      select
      local.set $l15
      local.get $l13
      i32.const 20
      i32.add
      local.set $l21
      block $B11
        local.get $l8
        local.get $l10
        local.get $l8
        local.get $l10
        i32.lt_s
        select
        local.tee $l8
        i32.const 0
        i32.le_s
        br_if $B11
        local.get $l8
        i32.const 1
        i32.and
        local.set $l18
        local.get $l21
        i32.load
        local.set $l10
        local.get $l8
        i32.const 1
        i32.ne
        if $I12
          local.get $l8
          i32.const -2
          i32.and
          local.set $l19
          i32.const 0
          local.set $l8
          loop $L13
            local.get $l12
            local.get $l15
            local.get $l11
            i32.const -1
            i32.xor
            i32.add
            i32.const 4
            i32.shl
            i32.add
            local.tee $l17
            local.get $l10
            local.get $l11
            i32.const 4
            i32.shl
            local.tee $l14
            i32.add
            local.tee $l20
            i64.load align=4
            i64.store align=4
            local.get $l17
            local.get $l20
            i64.load offset=8 align=4
            i64.store offset=8 align=4
            local.get $l15
            local.get $l11
            i32.sub
            i32.const 4
            i32.shl
            local.get $l12
            i32.add
            i32.const 32
            i32.sub
            local.tee $l17
            local.get $l10
            local.get $l14
            i32.const 16
            i32.or
            i32.add
            local.tee $l14
            i64.load offset=8 align=4
            i64.store offset=8 align=4
            local.get $l17
            local.get $l14
            i64.load align=4
            i64.store align=4
            local.get $l11
            i32.const 2
            i32.add
            local.set $l11
            local.get $l8
            i32.const 2
            i32.add
            local.tee $l8
            local.get $l19
            i32.ne
            br_if $L13
          end
        end
        local.get $l18
        i32.eqz
        br_if $B11
        local.get $l12
        local.get $l15
        local.get $l11
        i32.const -1
        i32.xor
        i32.add
        i32.const 4
        i32.shl
        i32.add
        local.tee $l12
        local.get $l10
        local.get $l11
        i32.const 4
        i32.shl
        i32.add
        local.tee $l11
        i64.load align=4
        i64.store align=4
        local.get $l12
        local.get $l11
        i64.load offset=8 align=4
        i64.store offset=8 align=4
      end
      local.get $l13
      i32.const 3222408
      i32.store
      local.get $l13
      i32.const 36
      i32.add
      call $f554
      drop
      local.get $l21
      call $f554
      drop
      local.get $l9
      i32.const 176
      i32.add
      global.set $g0
      block $B14
        local.get $l15
        i32.eqz
        br_if $B14
        loop $L15
          local.get $l16
          i32.load
          local.get $p1
          i32.const 24
          i32.mul
          i32.add
          local.get $l22
          i32.load
          local.get $p1
          i32.const 4
          i32.shl
          i32.add
          call $f73052
          local.get $p1
          i32.const 1
          i32.add
          local.tee $p1
          local.get $l15
          i32.ne
          br_if $L15
        end
        local.get $p3
        i32.load offset=8
        i32.eqz
        br_if $B14
        local.get $p0
        i32.const 160
        i32.add
        local.set $l28
        local.get $p0
        i32.const 144
        i32.add
        local.set $l29
        local.get $p0
        i32.const 224
        i32.add
        local.set $l30
        local.get $p0
        i32.const 208
        i32.add
        local.set $l31
        local.get $p0
        i32.const 272
        i32.add
        local.set $l32
        local.get $p0
        i32.const 256
        i32.add
        local.set $l33
        loop $L16
          local.get $p3
          i32.load
          local.get $l23
          i32.const 7
          i32.shl
          i32.add
          local.tee $l10
          f32.load offset=20
          local.set $l46
          local.get $l10
          f32.load offset=68
          local.set $l64
          local.get $l10
          f32.load offset=24
          local.set $l50
          local.get $l10
          f32.load offset=72
          local.set $l59
          local.get $l10
          f32.load offset=28
          local.set $l49
          local.get $l10
          f32.load offset=76
          local.set $l60
          local.get $l10
          i32.const 32
          i32.add
          local.tee $l34
          f32.load
          local.set $l47
          local.get $l10
          i32.const 80
          i32.add
          local.tee $l35
          f32.load
          local.set $l63
          local.get $l10
          f32.load offset=36
          local.set $l57
          local.get $l10
          f32.load offset=84
          local.set $l70
          local.get $l10
          f32.load offset=40
          local.set $l48
          local.get $l10
          f32.load offset=88
          local.set $l65
          local.get $l10
          f32.load offset=44
          local.set $l54
          local.get $l10
          f32.load offset=92
          local.set $l71
          local.get $l10
          i32.const 48
          i32.add
          local.tee $l36
          f32.load
          local.set $l56
          local.get $l10
          i32.const 96
          i32.add
          local.tee $l37
          f32.load
          local.set $l66
          local.get $l10
          f32.load offset=52
          local.set $l52
          local.get $l10
          f32.load offset=100
          local.set $l72
          local.get $l10
          f32.load offset=56
          local.set $l58
          local.get $l10
          f32.load offset=104
          local.set $l73
          local.get $l10
          f32.load offset=60
          local.set $l51
          local.get $l10
          f32.load offset=108
          local.set $l53
          local.get $p0
          local.get $l10
          f32.load offset=64
          local.get $l10
          f32.load offset=16
          local.tee $l61
          f32.sub
          local.tee $l55
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          local.tee $l67
          local.get $l61
          f32.add
          f32.store offset=240
          local.get $p0
          local.get $l51
          local.get $l53
          local.get $l51
          f32.sub
          local.tee $l53
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          local.tee $l61
          f32.add
          f32.store offset=284
          local.get $p0
          local.get $l58
          local.get $l73
          local.get $l58
          f32.sub
          local.tee $l51
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          local.tee $l73
          f32.add
          f32.store offset=280
          local.get $p0
          local.get $l52
          local.get $l72
          local.get $l52
          f32.sub
          local.tee $l58
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          local.tee $l72
          f32.add
          f32.store offset=276
          local.get $p0
          local.get $l56
          local.get $l66
          local.get $l56
          f32.sub
          local.tee $l52
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          local.tee $l66
          f32.add
          f32.store offset=272
          local.get $p0
          local.get $l54
          local.get $l71
          local.get $l54
          f32.sub
          local.tee $l56
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          local.tee $l71
          f32.add
          f32.store offset=268
          local.get $p0
          local.get $l48
          local.get $l65
          local.get $l48
          f32.sub
          local.tee $l54
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          local.tee $l65
          f32.add
          f32.store offset=264
          local.get $p0
          local.get $l57
          local.get $l70
          local.get $l57
          f32.sub
          local.tee $l48
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          local.tee $l70
          f32.add
          f32.store offset=260
          local.get $p0
          local.get $l47
          local.get $l63
          local.get $l47
          f32.sub
          local.tee $l57
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          local.tee $l63
          f32.add
          f32.store offset=256
          local.get $p0
          local.get $l49
          local.get $l60
          local.get $l49
          f32.sub
          local.tee $l60
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          local.tee $l62
          f32.add
          f32.store offset=252
          local.get $p0
          local.get $l50
          local.get $l59
          local.get $l50
          f32.sub
          local.tee $l59
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          local.tee $l68
          f32.add
          f32.store offset=248
          local.get $p0
          local.get $l46
          local.get $l64
          local.get $l46
          f32.sub
          local.tee $l64
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          local.tee $l69
          f32.add
          f32.store offset=244
          local.get $l10
          f32.load offset=112
          local.set $l46
          local.get $l10
          f32.load offset=116
          local.set $l50
          local.get $l10
          f32.load offset=120
          local.set $l49
          local.get $p0
          local.get $l61
          f32.abs
          local.get $l10
          f32.load offset=124
          local.tee $l47
          f32.add
          f32.store offset=236
          local.get $p0
          local.get $l49
          local.get $l73
          f32.abs
          f32.add
          f32.store offset=232
          local.get $p0
          local.get $l50
          local.get $l72
          f32.abs
          f32.add
          f32.store offset=228
          local.get $p0
          local.get $l46
          local.get $l66
          f32.abs
          f32.add
          f32.store offset=224
          local.get $p0
          local.get $l47
          local.get $l71
          f32.abs
          f32.add
          f32.store offset=220
          local.get $p0
          local.get $l49
          local.get $l65
          f32.abs
          f32.add
          f32.store offset=216
          local.get $p0
          local.get $l50
          local.get $l70
          f32.abs
          f32.add
          f32.store offset=212
          local.get $p0
          local.get $l46
          local.get $l63
          f32.abs
          f32.add
          f32.store offset=208
          local.get $p0
          local.get $l47
          local.get $l62
          f32.abs
          f32.add
          f32.store offset=204
          local.get $p0
          local.get $l49
          local.get $l68
          f32.abs
          f32.add
          f32.store offset=200
          local.get $p0
          local.get $l50
          local.get $l69
          f32.abs
          f32.add
          f32.store offset=196
          local.get $p0
          local.get $l46
          local.get $l67
          f32.abs
          f32.add
          f32.store offset=192
          local.get $p0
          i32.const 240
          i32.add
          local.get $p0
          i32.const 192
          i32.add
          local.get $l16
          i32.load
          local.get $l15
          call $f65447
          if $I17
            local.get $l10
            i32.const 112
            i32.add
            local.set $l38
            local.get $l10
            i32.const 16
            i32.add
            local.set $l39
            local.get $l10
            i32.const -64
            i32.sub
            local.set $l40
            local.get $p0
            local.get $l60
            local.get $l60
            f32.mul
            local.get $l56
            local.get $l56
            f32.mul
            local.get $l53
            local.get $l53
            f32.mul
            f32.add
            f32.add
            f32.sqrt
            local.tee $l46
            f32.store offset=188
            local.get $p0
            local.get $l55
            local.get $l55
            f32.mul
            local.get $l57
            local.get $l57
            f32.mul
            local.get $l52
            local.get $l52
            f32.mul
            f32.add
            f32.add
            f32.sqrt
            local.tee $l50
            f32.store offset=176
            local.get $p0
            local.get $l64
            local.get $l64
            f32.mul
            local.get $l48
            local.get $l48
            f32.mul
            local.get $l58
            local.get $l58
            f32.mul
            f32.add
            f32.add
            f32.sqrt
            local.tee $l49
            f32.store offset=180
            local.get $p0
            local.get $l59
            local.get $l59
            f32.mul
            local.get $l54
            local.get $l54
            f32.mul
            local.get $l51
            local.get $l51
            f32.mul
            f32.add
            f32.add
            f32.sqrt
            local.tee $l47
            f32.store offset=184
            local.get $p0
            local.get $l53
            local.get $l46
            f32.div
            f32.const 0x0p+0 (;=0;)
            local.get $l46
            f32.const 0x1.0c6f7ap-20 (;=1e-06;)
            f32.gt
            local.tee $p1
            select
            f32.store offset=172
            local.get $p0
            local.get $l51
            local.get $l47
            f32.div
            f32.const 0x0p+0 (;=0;)
            local.get $l47
            f32.const 0x1.0c6f7ap-20 (;=1e-06;)
            f32.gt
            local.tee $l14
            select
            f32.store offset=168
            local.get $p0
            local.get $l58
            local.get $l49
            f32.div
            f32.const 0x0p+0 (;=0;)
            local.get $l49
            f32.const 0x1.0c6f7ap-20 (;=1e-06;)
            f32.gt
            local.tee $l9
            select
            f32.store offset=164
            local.get $p0
            local.get $l52
            local.get $l50
            f32.div
            f32.const 0x0p+0 (;=0;)
            local.get $l50
            f32.const 0x1.0c6f7ap-20 (;=1e-06;)
            f32.gt
            local.tee $l11
            select
            f32.store offset=160
            local.get $p0
            local.get $l56
            local.get $l46
            f32.div
            f32.const 0x0p+0 (;=0;)
            local.get $p1
            select
            f32.store offset=156
            local.get $p0
            local.get $l54
            local.get $l47
            f32.div
            f32.const 0x0p+0 (;=0;)
            local.get $l14
            select
            f32.store offset=152
            local.get $p0
            local.get $l48
            local.get $l49
            f32.div
            f32.const 0x0p+0 (;=0;)
            local.get $l9
            select
            f32.store offset=148
            local.get $p0
            local.get $l57
            local.get $l50
            f32.div
            f32.const 0x0p+0 (;=0;)
            local.get $l11
            select
            f32.store offset=144
            local.get $p0
            local.get $l60
            local.get $l46
            f32.div
            f32.const 0x0p+0 (;=0;)
            local.get $p1
            select
            f32.store offset=140
            local.get $p0
            local.get $l59
            local.get $l47
            f32.div
            f32.const 0x0p+0 (;=0;)
            local.get $l14
            select
            f32.store offset=136
            local.get $p0
            local.get $l64
            local.get $l49
            f32.div
            f32.const 0x0p+0 (;=0;)
            local.get $l9
            select
            f32.store offset=132
            local.get $p0
            local.get $l55
            local.get $l50
            f32.div
            f32.const 0x0p+0 (;=0;)
            local.get $l11
            select
            f32.store offset=128
            i32.const 0
            local.set $l14
            loop $L18
              block $B19
                local.get $p2
                local.get $l14
                i32.const 2
                i32.shl
                local.tee $p1
                i32.add
                f32.load
                f32.const 0x1.0c6f7ap-20 (;=1e-06;)
                f32.lt
                br_if $B19
                local.get $p1
                local.get $l10
                i32.add
                i32.load
                local.tee $l9
                local.get $p4
                i32.ge_u
                br_if $B19
                local.get $p1
                local.get $l38
                i32.add
                f32.load
                local.set $l46
                local.get $p1
                local.get $l39
                i32.add
                f32.load
                local.set $l50
                local.get $p1
                local.get $l34
                i32.add
                f32.load
                local.set $l49
                local.get $p0
                local.get $p1
                local.get $l36
                i32.add
                f32.load
                local.tee $l54
                f32.store offset=120
                local.get $p0
                local.get $l49
                f32.store offset=116
                local.get $p0
                local.get $l50
                f32.store offset=112
                local.get $p0
                local.get $l9
                i32.store offset=48
                local.get $p1
                local.get $l29
                i32.add
                f32.load
                local.set $l47
                local.get $p0
                local.get $p1
                local.get $l28
                i32.add
                f32.load
                f32.store offset=40
                local.get $p0
                local.get $l47
                f32.store offset=36
                local.get $p0
                local.get $p0
                i32.const 128
                i32.add
                local.get $p1
                i32.add
                f32.load
                f32.store offset=32
                local.get $p1
                local.get $l33
                i32.add
                f32.load
                local.set $l47
                local.get $p1
                local.get $l32
                i32.add
                f32.load
                local.set $l57
                local.get $p1
                local.get $l31
                i32.add
                f32.load
                local.set $l48
                local.get $p0
                local.get $p1
                local.get $l30
                i32.add
                f32.load
                f32.store offset=28
                local.get $p0
                local.get $l48
                f32.store offset=24
                local.get $p0
                local.get $p0
                i32.const 192
                i32.add
                local.get $p1
                i32.add
                f32.load
                f32.store offset=20
                local.get $p0
                local.get $l57
                f32.store offset=16
                local.get $p0
                local.get $l47
                f32.store offset=12
                local.get $p0
                local.get $p0
                i32.const 240
                i32.add
                local.get $p1
                i32.add
                f32.load
                f32.store offset=8
                local.get $p0
                i32.const 32
                i32.add
                local.set $l18
                local.get $p0
                i32.const 8
                i32.add
                local.set $l41
                local.get $p0
                i32.const 176
                i32.add
                local.get $p1
                i32.add
                f32.load
                local.set $l48
                local.get $l22
                i32.load
                local.set $l42
                local.get $l16
                i32.load
                local.set $l43
                local.get $p0
                i32.const 48
                i32.add
                local.set $l12
                i32.const 0
                local.set $l17
                i32.const 0
                local.set $l11
                global.get $g0
                i32.const 240
                i32.sub
                local.tee $l8
                global.set $g0
                local.get $l8
                i32.const 0
                i32.store offset=88
                local.get $l8
                local.get $l46
                local.get $l46
                f32.const 0x1.353f7cp-3 (;=0.151;)
                f32.mul
                local.tee $l60
                f32.sub
                local.tee $l47
                f32.const 0x1.0c6f7ap-20 (;=1e-06;)
                local.get $l47
                f32.const 0x1.0c6f7ap-20 (;=1e-06;)
                f32.gt
                select
                f32.store offset=92
                local.get $l8
                i64.const 4575657221408423936
                i64.store offset=64
                local.get $l8
                i64.const 0
                i64.store offset=56
                local.get $l8
                local.get $p0
                i32.const 112
                i32.add
                local.tee $l13
                f32.load
                f32.store offset=72
                local.get $l8
                local.get $l13
                f32.load offset=4
                f32.store offset=76
                local.get $l8
                local.get $l13
                f32.load offset=8
                f32.store offset=80
                block $B20
                  local.get $l15
                  i32.eqz
                  br_if $B20
                  local.get $l60
                  local.get $l48
                  f32.add
                  local.set $l61
                  local.get $l12
                  i32.const 28
                  i32.add
                  local.set $l21
                  local.get $l12
                  i32.const 16
                  i32.add
                  local.set $l24
                  local.get $l12
                  i32.const 4
                  i32.add
                  local.set $l25
                  i32.const 3437616
                  f32.load
                  local.set $l62
                  local.get $l8
                  i32.const 36
                  i32.add
                  local.set $l26
                  f32.const inf (;=inf;)
                  local.set $l57
                  local.get $l8
                  i32.const 24
                  i32.add
                  local.tee $l27
                  i32.const 8
                  i32.add
                  local.set $l44
                  loop $L21
                    block $B22
                      block $B23
                        local.get $l41
                        local.get $l43
                        local.get $l17
                        i32.const 24
                        i32.mul
                        i32.add
                        local.tee $l19
                        call $f65651
                        i32.eqz
                        br_if $B23
                        local.get $l42
                        local.get $l17
                        i32.const 4
                        i32.shl
                        i32.add
                        local.tee $l20
                        i32.load offset=4
                        local.tee $l9
                        i32.eqz
                        br_if $B23
                        local.get $l8
                        i32.const 0
                        i32.store16 offset=20
                        local.get $l8
                        i32.const -1
                        i32.store offset=16
                        local.get $l8
                        i64.const 0
                        i64.store offset=8
                        local.get $l27
                        i64.const 0
                        i64.store offset=16 align=4
                        local.get $l44
                        i64.const 0
                        i64.store align=4
                        local.get $l27
                        i64.const 0
                        i64.store align=4
                        local.get $l8
                        i32.const 2139095039
                        i32.store offset=48
                        local.get $l20
                        i32.load
                        local.set $l20
                        local.get $l8
                        i32.const 136
                        i32.add
                        local.get $l9
                        local.get $l9
                        i32.load
                        i32.load offset=40
                        call_indirect $__indirect_function_table (type $t1)
                        local.get $l8
                        local.get $l8
                        i32.const 136
                        i32.add
                        i32.store offset=208
                        local.get $l8
                        i32.load offset=208
                        local.set $l45
                        local.get $l8
                        i32.const 208
                        i32.add
                        local.get $l20
                        local.get $l20
                        i32.load
                        i32.load offset=76
                        call_indirect $__indirect_function_table (type $t1)
                        local.get $l8
                        i32.const 176
                        i32.add
                        local.get $l9
                        local.get $l9
                        i32.load
                        i32.load offset=80
                        call_indirect $__indirect_function_table (type $t1)
                        local.get $l8
                        local.get $l8
                        f32.load offset=220
                        local.tee $l47
                        local.get $l8
                        f32.load offset=188
                        local.tee $l53
                        f32.mul
                        local.get $l8
                        f32.load offset=176
                        local.tee $l55
                        local.get $l8
                        f32.load offset=208
                        local.tee $l48
                        f32.mul
                        f32.sub
                        local.get $l8
                        f32.load offset=212
                        local.tee $l51
                        local.get $l8
                        f32.load offset=180
                        local.tee $l56
                        f32.mul
                        f32.sub
                        local.get $l8
                        f32.load offset=216
                        local.tee $l52
                        local.get $l8
                        f32.load offset=184
                        local.tee $l58
                        f32.mul
                        f32.sub
                        f32.store offset=116
                        local.get $l8
                        local.get $l48
                        local.get $l56
                        f32.mul
                        local.get $l47
                        local.get $l58
                        f32.mul
                        local.get $l52
                        local.get $l53
                        f32.mul
                        f32.add
                        f32.add
                        local.get $l55
                        local.get $l51
                        f32.mul
                        f32.sub
                        f32.store offset=112
                        local.get $l8
                        local.get $l52
                        local.get $l55
                        f32.mul
                        local.get $l47
                        local.get $l56
                        f32.mul
                        local.get $l51
                        local.get $l53
                        f32.mul
                        f32.add
                        f32.add
                        local.get $l58
                        local.get $l48
                        f32.mul
                        f32.sub
                        f32.store offset=108
                        local.get $l8
                        local.get $l51
                        local.get $l58
                        f32.mul
                        local.get $l47
                        local.get $l55
                        f32.mul
                        local.get $l48
                        local.get $l53
                        f32.mul
                        f32.add
                        f32.add
                        local.get $l56
                        local.get $l52
                        f32.mul
                        f32.sub
                        f32.store offset=104
                        local.get $l8
                        local.get $l8
                        f32.load offset=232
                        local.get $l52
                        local.get $l52
                        local.get $l8
                        f32.load offset=200
                        local.tee $l53
                        local.get $l53
                        f32.add
                        local.tee $l53
                        f32.mul
                        local.get $l48
                        local.get $l8
                        f32.load offset=192
                        local.tee $l55
                        local.get $l55
                        f32.add
                        local.tee $l55
                        f32.mul
                        local.get $l51
                        local.get $l8
                        f32.load offset=196
                        local.tee $l56
                        local.get $l56
                        f32.add
                        local.tee $l56
                        f32.mul
                        f32.add
                        f32.add
                        local.tee $l58
                        f32.mul
                        local.get $l53
                        local.get $l47
                        local.get $l47
                        f32.mul
                        f32.const -0x1p-1 (;=-0.5;)
                        f32.add
                        local.tee $l59
                        f32.mul
                        local.get $l47
                        local.get $l48
                        local.get $l56
                        f32.mul
                        local.get $l55
                        local.get $l51
                        f32.mul
                        f32.sub
                        f32.mul
                        f32.add
                        f32.add
                        f32.add
                        f32.store offset=128
                        local.get $l8
                        local.get $l8
                        f32.load offset=228
                        local.get $l51
                        local.get $l58
                        f32.mul
                        local.get $l56
                        local.get $l59
                        f32.mul
                        local.get $l47
                        local.get $l52
                        local.get $l55
                        f32.mul
                        local.get $l53
                        local.get $l48
                        f32.mul
                        f32.sub
                        f32.mul
                        f32.add
                        f32.add
                        f32.add
                        f32.store offset=124
                        local.get $l8
                        local.get $l8
                        f32.load offset=224
                        local.get $l48
                        local.get $l58
                        f32.mul
                        local.get $l55
                        local.get $l59
                        f32.mul
                        local.get $l47
                        local.get $l51
                        local.get $l53
                        f32.mul
                        local.get $l56
                        local.get $l52
                        f32.mul
                        f32.sub
                        f32.mul
                        f32.add
                        f32.add
                        f32.add
                        f32.store offset=120
                        local.get $l8
                        i32.const 514
                        i32.store16 offset=96
                        local.get $l18
                        local.get $l61
                        local.get $l8
                        i32.const 88
                        i32.add
                        local.get $l8
                        i32.const 56
                        i32.add
                        local.get $l45
                        local.get $l8
                        i32.const 104
                        i32.add
                        local.get $l8
                        i32.const 8
                        i32.add
                        local.get $l8
                        i32.const 96
                        i32.add
                        call $f70313
                        i32.eqz
                        br_if $B23
                        block $B24
                          block $B25
                            local.get $l8
                            i32.load offset=36
                            i32.const 2139095040
                            i32.and
                            i32.const 2139095040
                            i32.eq
                            br_if $B25
                            local.get $l8
                            i32.load offset=40
                            i32.const 2139095040
                            i32.and
                            i32.const 2139095040
                            i32.eq
                            br_if $B25
                            local.get $l8
                            i32.load offset=44
                            i32.const 2139095040
                            i32.and
                            i32.const 2139095040
                            i32.ne
                            br_if $B24
                          end
                          block $B26 (result f32)
                            local.get $l62
                            local.get $l8
                            f32.load offset=32
                            local.get $l19
                            f32.load offset=8
                            f32.sub
                            local.tee $l47
                            local.get $l47
                            f32.mul
                            local.get $l8
                            f32.load offset=24
                            local.get $l19
                            f32.load
                            f32.sub
                            local.tee $l48
                            local.get $l48
                            f32.mul
                            local.get $l8
                            f32.load offset=28
                            local.get $l19
                            f32.load offset=4
                            f32.sub
                            local.tee $l51
                            local.get $l51
                            f32.mul
                            f32.add
                            f32.add
                            f32.sqrt
                            local.tee $l52
                            f32.lt
                            if $I27
                              local.get $l47
                              local.get $l52
                              f32.div
                              local.set $l47
                              local.get $l51
                              local.get $l52
                              f32.div
                              local.set $l51
                              local.get $l48
                              local.get $l52
                              f32.div
                              br $B26
                            end
                            i32.const 4748544
                            f32.load
                            local.set $l47
                            i32.const 4748540
                            f32.load
                            local.set $l51
                            i32.const 4748536
                            f32.load
                          end
                          local.set $l48
                          local.get $l8
                          local.get $l47
                          f32.store offset=44
                          local.get $l8
                          local.get $l51
                          f32.store offset=40
                          local.get $l8
                          local.get $l48
                          f32.store offset=36
                        end
                        local.get $l8
                        f32.load offset=48
                        local.tee $l48
                        local.get $l60
                        f32.sub
                        local.tee $l47
                        local.get $l57
                        f32.lt
                        i32.eqz
                        br_if $B23
                        local.get $l9
                        i32.load offset=8
                        local.tee $l9
                        i32.eqz
                        br_if $B23
                        local.get $l9
                        local.get $l9
                        i32.load
                        i32.load offset=116
                        call_indirect $__indirect_function_table (type $t5)
                        if $I28
                          local.get $l9
                          local.get $l9
                          i32.load
                          i32.load offset=124
                          call_indirect $__indirect_function_table (type $t5)
                          br_if $B23
                        end
                        local.get $l12
                        local.get $l9
                        i32.load offset=4
                        i32.store offset=52
                        local.get $l12
                        local.get $l9
                        local.get $l9
                        i32.load
                        i32.load offset=128
                        call_indirect $__indirect_function_table (type $t5)
                        local.tee $l19
                        i32.const 4
                        i32.add
                        local.get $l9
                        i32.const 4
                        i32.add
                        local.get $l19
                        select
                        i32.load
                        i32.store offset=56
                        local.get $l25
                        local.get $l13
                        i32.load offset=8
                        i32.store offset=8
                        local.get $l25
                        local.get $l13
                        i64.load align=4
                        i64.store align=4
                        local.get $l24
                        local.get $l18
                        i32.load offset=8
                        i32.store offset=8
                        local.get $l24
                        local.get $l18
                        i64.load align=4
                        i64.store align=4
                        local.get $l21
                        local.get $l26
                        i32.load offset=8
                        i32.store offset=8
                        local.get $l21
                        local.get $l26
                        i64.load align=4
                        i64.store align=4
                        local.get $l48
                        f32.const 0x0p+0 (;=0;)
                        f32.gt
                        i32.eqz
                        br_if $B22
                        local.get $l13
                        f32.load
                        local.set $l48
                        local.get $l18
                        f32.load
                        local.set $l51
                        local.get $l13
                        f32.load offset=4
                        local.set $l52
                        local.get $l18
                        f32.load offset=4
                        local.set $l53
                        local.get $l12
                        local.get $l47
                        local.get $l18
                        f32.load offset=8
                        f32.mul
                        local.get $l13
                        f32.load offset=8
                        f32.add
                        f32.store offset=48
                        local.get $l12
                        local.get $l52
                        local.get $l47
                        local.get $l53
                        f32.mul
                        f32.add
                        f32.store offset=44
                        local.get $l12
                        local.get $l48
                        local.get $l47
                        local.get $l51
                        f32.mul
                        f32.add
                        f32.store offset=40
                        local.get $l9
                        local.set $l11
                        local.get $l47
                        local.set $l57
                      end
                      local.get $l17
                      i32.const 1
                      i32.add
                      local.tee $l17
                      local.get $l15
                      i32.ne
                      br_if $L21
                      br $B20
                    end
                  end
                  i32.const 0
                  local.set $l11
                  local.get $l48
                  f32.const 0x0p+0 (;=0;)
                  f32.lt
                  i32.eqz
                  br_if $B20
                  local.get $l13
                  f32.load offset=4
                  local.set $l48
                  local.get $l13
                  f32.load offset=8
                  local.set $l51
                  local.get $l13
                  f32.load
                  local.set $l52
                  local.get $l12
                  local.get $l12
                  f32.load offset=28
                  local.tee $l53
                  f32.neg
                  f32.store offset=28
                  local.get $l12
                  local.get $l52
                  local.get $l47
                  local.get $l53
                  f32.mul
                  f32.sub
                  f32.store offset=40
                  local.get $l12
                  i32.const 36
                  i32.add
                  local.tee $l17
                  local.get $l17
                  f32.load
                  local.tee $l52
                  f32.neg
                  f32.store
                  local.get $l12
                  i32.const 32
                  i32.add
                  local.tee $l17
                  local.get $l17
                  f32.load
                  local.tee $l53
                  f32.neg
                  f32.store
                  local.get $l12
                  local.get $l51
                  local.get $l47
                  local.get $l52
                  f32.mul
                  f32.sub
                  f32.store offset=48
                  local.get $l12
                  local.get $l48
                  local.get $l47
                  local.get $l53
                  f32.mul
                  f32.sub
                  f32.store offset=44
                  local.get $l9
                  local.set $l11
                end
                local.get $l8
                i32.const 240
                i32.add
                global.set $g0
                local.get $l11
                i32.eqz
                br_if $B19
                local.get $p6
                i32.load offset=8
                local.tee $l9
                i32.const 1
                i32.add
                local.tee $l8
                local.get $p6
                i32.load offset=12
                i32.const 1
                i32.shr_u
                i32.gt_u
                if $I29
                  local.get $p6
                  call $f67185
                end
                local.get $p6
                local.get $l8
                i32.store offset=8
                local.get $p6
                i32.load
                local.get $l9
                i32.const 60
                i32.mul
                i32.add
                local.tee $l9
                local.get $p0
                i32.load offset=48
                i32.store
                local.get $l9
                local.get $p0
                f32.load offset=52
                f32.store offset=4
                local.get $l9
                local.get $p0
                f32.load offset=56
                f32.store offset=8
                local.get $l9
                local.get $p0
                f32.load offset=60
                f32.store offset=12
                local.get $l9
                local.get $p0
                f32.load offset=64
                f32.store offset=16
                local.get $l9
                local.get $p0
                f32.load offset=68
                f32.store offset=20
                local.get $l9
                local.get $p0
                f32.load offset=72
                f32.store offset=24
                local.get $l9
                local.get $p0
                f32.load offset=76
                local.tee $l56
                f32.store offset=28
                local.get $l9
                local.get $p0
                f32.load offset=80
                local.tee $l52
                f32.store offset=32
                local.get $l9
                local.get $p0
                f32.load offset=84
                local.tee $l58
                f32.store offset=36
                local.get $l9
                local.get $p0
                f32.load offset=88
                local.tee $l47
                f32.store offset=40
                local.get $l9
                local.get $p0
                f32.load offset=92
                local.tee $l57
                f32.store offset=44
                local.get $l9
                local.get $p0
                f32.load offset=96
                local.tee $l48
                f32.store offset=48
                local.get $l9
                local.get $p0
                i64.load offset=100 align=4
                i64.store offset=52 align=4
                i32.const 4129880
                i32.load8_u
                i32.eqz
                br_if $B19
                local.get $l11
                local.get $l11
                i32.load
                i32.load offset=128
                call_indirect $__indirect_function_table (type $t5)
                local.tee $l9
                i32.eqz
                br_if $B19
                local.get $l9
                i32.load8_u offset=133
                br_if $B19
                local.get $p5
                f32.load offset=8
                local.tee $l51
                f32.const 0x0p+0 (;=0;)
                f32.gt
                i32.eqz
                br_if $B19
                local.get $p1
                local.get $l37
                i32.add
                f32.load
                local.get $l54
                f32.sub
                local.get $p0
                i32.const 320
                i32.add
                local.get $p1
                i32.add
                f32.load
                local.tee $l54
                f32.mul
                local.tee $l55
                f32.const 0x1p+0 (;=1;)
                local.get $l55
                local.get $l55
                f32.mul
                local.get $p1
                local.get $l40
                i32.add
                f32.load
                local.get $l50
                f32.sub
                local.get $l54
                f32.mul
                local.tee $l50
                local.get $l50
                f32.mul
                local.get $p1
                local.get $l35
                i32.add
                f32.load
                local.get $l49
                f32.sub
                local.get $l54
                f32.mul
                local.tee $l49
                local.get $l49
                f32.mul
                f32.add
                f32.add
                f32.sqrt
                local.tee $l54
                f32.div
                f32.const 0x0p+0 (;=0;)
                local.get $l54
                f32.const 0x0p+0 (;=0;)
                f32.gt
                select
                local.tee $l55
                f32.mul
                local.set $l53
                local.get $l49
                local.get $l55
                f32.mul
                local.set $l49
                local.get $l50
                local.get $l55
                f32.mul
                local.set $l50
                local.get $l53
                local.get $p5
                i32.load8_u offset=15
                if $I30 (result f32)
                  local.get $l51
                  local.get $l58
                  local.get $l53
                  f32.mul
                  local.get $l56
                  local.get $l50
                  f32.mul
                  local.get $l49
                  local.get $l52
                  f32.mul
                  f32.add
                  f32.add
                  f32.neg
                  f32.const 0x0p+0 (;=0;)
                  f32.max
                  f32.mul
                else
                  local.get $l51
                end
                local.get $l54
                f32.const 0x1p+0 (;=1;)
                local.get $p5
                i32.load8_u offset=14
                select
                f32.mul
                local.get $l46
                local.get $l46
                local.get $l46
                f32.const 0x1.0c1524p+2 (;=4.18879;)
                f32.mul
                f32.mul
                f32.mul
                f32.const 0x1p+0 (;=1;)
                local.get $p5
                i32.load8_u offset=13
                select
                f32.mul
                local.tee $l46
                f32.mul
                local.set $l54
                local.get $l49
                local.get $l46
                f32.mul
                local.set $l49
                local.get $l50
                local.get $l46
                f32.mul
                local.set $l46
                local.get $p7
                i32.load offset=8
                local.tee $p1
                i32.const 1
                i32.add
                local.tee $l11
                local.get $p7
                i32.load offset=12
                i32.const 1
                i32.shr_u
                i32.gt_u
                if $I31
                  local.get $p7
                  call $f577
                end
                local.get $p7
                local.get $l11
                i32.store offset=8
                local.get $p7
                i32.load
                local.get $p1
                i32.const 28
                i32.mul
                i32.add
                local.tee $p1
                local.get $l9
                i32.store offset=24
                local.get $p1
                local.get $l47
                f32.store offset=12
                local.get $p1
                local.get $l54
                f32.store offset=8
                local.get $p1
                local.get $l49
                f32.store offset=4
                local.get $p1
                local.get $l46
                f32.store
                local.get $p1
                local.get $l48
                f32.store offset=20
                local.get $p1
                local.get $l57
                f32.store offset=16
              end
              local.get $l14
              i32.const 1
              i32.add
              local.tee $l14
              i32.const 4
              i32.ne
              br_if $L18
            end
          end
          local.get $l23
          i32.const 1
          i32.add
          local.tee $l23
          local.get $p3
          i32.load offset=8
          i32.lt_u
          br_if $L16
        end
      end
      local.get $l16
      call $f554
      drop
      local.get $l22
      call $f554
      drop
    end
    local.get $p0
    i32.const 336
    i32.add
    global.set $g0)
