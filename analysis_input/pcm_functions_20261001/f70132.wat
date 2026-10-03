  (func $f70132 (type $t130) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 f32) (param $p6 i32) (param $p7 i32) (param $p8 f32) (result i32)
    (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32)
    global.get $g0
    i32.const 192
    i32.sub
    local.tee $l9
    global.set $g0
    local.get $p3
    f32.load offset=24
    local.set $l13
    local.get $l9
    local.get $p3
    f32.load
    local.tee $l15
    f32.store offset=160
    local.get $l9
    local.get $p3
    f32.load offset=4
    local.tee $l12
    f32.store offset=164
    local.get $l9
    local.get $p3
    f32.load offset=8
    local.tee $l14
    f32.store offset=168
    local.get $l9
    local.get $p3
    f32.load offset=12
    local.tee $l21
    f32.store offset=172
    local.get $l9
    local.get $p3
    f32.load offset=16
    local.tee $l20
    f32.store offset=176
    local.get $l9
    local.get $p3
    f32.load offset=20
    local.tee $l17
    f32.store offset=180
    local.get $l9
    local.get $l13
    local.get $p8
    f32.add
    local.tee $l22
    f32.store offset=184
    block $B0
      local.get $p1
      f32.load offset=4
      f32.const 0x1p+0 (;=1;)
      f32.ne
      br_if $B0
      local.get $p1
      f32.load offset=8
      f32.const 0x1p+0 (;=1;)
      f32.ne
      br_if $B0
      local.get $p1
      f32.load offset=12
      f32.const 0x1p+0 (;=1;)
      f32.eq
      local.set $l10
    end
    local.get $p7
    i32.load16_u
    local.set $l11
    local.get $p1
    i32.load8_u offset=32
    local.set $p3
    local.get $l9
    local.get $l14
    local.get $p2
    f32.load offset=24
    local.tee $l24
    f32.sub
    local.tee $p8
    local.get $p8
    f32.add
    local.tee $l18
    local.get $p2
    f32.load offset=12
    local.tee $l14
    local.get $l14
    f32.mul
    f32.const -0x1p-1 (;=-0.5;)
    f32.add
    local.tee $l19
    f32.mul
    local.get $l14
    local.get $l12
    local.get $p2
    f32.load offset=20
    local.tee $l25
    f32.sub
    local.tee $p8
    local.get $p8
    f32.add
    local.tee $l16
    local.get $p2
    f32.load
    local.tee $l12
    f32.mul
    local.get $l15
    local.get $p2
    f32.load offset=16
    local.tee $l26
    f32.sub
    local.tee $p8
    local.get $p8
    f32.add
    local.tee $l15
    local.get $p2
    f32.load offset=4
    local.tee $l13
    f32.mul
    f32.sub
    f32.mul
    f32.sub
    local.get $p2
    f32.load offset=8
    local.tee $p8
    local.get $l15
    local.get $l12
    f32.mul
    local.get $l16
    local.get $l13
    f32.mul
    f32.add
    local.get $l18
    local.get $p8
    f32.mul
    f32.add
    local.tee $l23
    f32.mul
    f32.add
    local.tee $l28
    local.get $l19
    local.get $l17
    local.get $l24
    f32.sub
    local.tee $l17
    local.get $l17
    f32.add
    local.tee $l17
    f32.mul
    local.get $l14
    local.get $l12
    local.get $l20
    local.get $l25
    f32.sub
    local.tee $l20
    local.get $l20
    f32.add
    local.tee $l20
    f32.mul
    local.get $l13
    local.get $l21
    local.get $l26
    f32.sub
    local.tee $l21
    local.get $l21
    f32.add
    local.tee $l21
    f32.mul
    f32.sub
    f32.mul
    f32.sub
    local.get $p8
    local.get $l12
    local.get $l21
    f32.mul
    local.get $l13
    local.get $l20
    f32.mul
    f32.add
    local.get $p8
    local.get $l17
    f32.mul
    f32.add
    local.tee $l27
    f32.mul
    f32.add
    local.tee $l29
    f32.add
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.store offset=152
    local.get $l9
    local.get $l13
    local.get $l23
    f32.mul
    local.get $l16
    local.get $l19
    f32.mul
    local.get $l14
    local.get $l15
    local.get $p8
    f32.mul
    local.get $l18
    local.get $l12
    f32.mul
    f32.sub
    f32.mul
    f32.sub
    f32.add
    local.tee $l30
    local.get $l13
    local.get $l27
    f32.mul
    local.get $l19
    local.get $l20
    f32.mul
    local.get $l14
    local.get $p8
    local.get $l21
    f32.mul
    local.get $l12
    local.get $l17
    f32.mul
    f32.sub
    f32.mul
    f32.sub
    f32.add
    local.tee $l31
    f32.add
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.store offset=148
    local.get $l9
    local.get $l12
    local.get $l23
    f32.mul
    local.get $l15
    local.get $l19
    f32.mul
    local.get $l14
    local.get $l18
    local.get $l13
    f32.mul
    local.get $l16
    local.get $p8
    f32.mul
    f32.sub
    f32.mul
    f32.sub
    f32.add
    local.tee $l23
    local.get $l12
    local.get $l27
    f32.mul
    local.get $l19
    local.get $l21
    f32.mul
    local.get $l14
    local.get $l13
    local.get $l17
    f32.mul
    local.get $p8
    local.get $l20
    f32.mul
    f32.sub
    f32.mul
    f32.sub
    f32.add
    local.tee $l20
    f32.add
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.store offset=144
    local.get $l9
    local.get $l19
    local.get $p4
    f32.load offset=8
    local.tee $l18
    local.get $l18
    f32.add
    local.tee $l18
    f32.mul
    local.get $l14
    local.get $l12
    local.get $p4
    f32.load offset=4
    local.tee $l16
    local.get $l16
    f32.add
    local.tee $l16
    f32.mul
    local.get $l13
    local.get $p4
    f32.load
    local.tee $l15
    local.get $l15
    f32.add
    local.tee $l15
    f32.mul
    f32.sub
    f32.mul
    f32.sub
    local.get $p8
    local.get $l12
    local.get $l15
    f32.mul
    local.get $l13
    local.get $l16
    f32.mul
    f32.add
    local.get $p8
    local.get $l18
    f32.mul
    f32.add
    local.tee $l17
    f32.mul
    f32.add
    f32.store offset=136
    local.get $l9
    local.get $l13
    local.get $l17
    f32.mul
    local.get $l19
    local.get $l16
    f32.mul
    local.get $l14
    local.get $p8
    local.get $l15
    f32.mul
    local.get $l12
    local.get $l18
    f32.mul
    f32.sub
    f32.mul
    f32.sub
    f32.add
    f32.store offset=132
    local.get $l9
    local.get $l12
    local.get $l17
    f32.mul
    local.get $l19
    local.get $l15
    f32.mul
    local.get $l14
    local.get $l13
    local.get $l18
    f32.mul
    local.get $p8
    local.get $l16
    f32.mul
    f32.sub
    f32.mul
    f32.sub
    f32.add
    f32.store offset=128
    local.get $l9
    local.get $l22
    local.get $l28
    local.get $l29
    f32.sub
    f32.abs
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.add
    f32.store offset=120
    local.get $l9
    local.get $l22
    local.get $l30
    local.get $l31
    f32.sub
    f32.abs
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.add
    f32.store offset=116
    local.get $l9
    local.get $l22
    local.get $l23
    local.get $l20
    f32.sub
    f32.abs
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.add
    f32.store offset=112
    local.get $p3
    i32.const 2
    i32.and
    local.set $p3
    block $B1 (result f32)
      local.get $l10
      i32.eqz
      if $I2
        local.get $l9
        i32.const 8
        i32.add
        local.get $p2
        local.get $p1
        i32.const 4
        i32.add
        call $f70133
        local.get $l9
        local.get $l9
        i64.load offset=28 align=4
        i64.store offset=84 align=4
        local.get $l9
        local.get $l9
        i64.load offset=36 align=4
        i64.store offset=92 align=4
        local.get $l9
        local.get $l9
        f32.load offset=52
        f32.store offset=108
        local.get $l9
        local.get $l9
        f32.load offset=8
        f32.store offset=64
        local.get $l9
        local.get $l9
        i64.load offset=12 align=4
        i64.store offset=68 align=4
        local.get $l9
        local.get $l9
        i64.load offset=20 align=4
        i64.store offset=76 align=4
        local.get $l9
        local.get $l9
        i64.load offset=44 align=4
        i64.store offset=100 align=4
        local.get $p1
        local.get $l9
        i32.const 144
        i32.add
        local.get $l9
        i32.const 112
        i32.add
        local.get $l9
        i32.const 128
        i32.add
        local.get $p5
        call $f70134
        local.tee $p8
        local.get $p5
        f32.div
        br $B1
      end
      local.get $l9
      local.get $l24
      f32.store offset=108
      local.get $l9
      local.get $l25
      f32.store offset=104
      local.get $l9
      local.get $l13
      local.get $l13
      f32.add
      local.tee $l18
      local.get $p8
      f32.mul
      local.tee $l19
      local.get $l14
      local.get $l12
      local.get $l12
      f32.add
      local.tee $l22
      f32.mul
      local.tee $l16
      f32.sub
      f32.store offset=92
      local.get $l9
      local.get $l16
      local.get $l19
      f32.add
      f32.store offset=84
      local.get $l9
      f32.const 0x1p+0 (;=1;)
      local.get $l12
      local.get $l22
      f32.mul
      f32.sub
      local.tee $l12
      local.get $l13
      local.get $l18
      f32.mul
      local.tee $l16
      f32.sub
      f32.store offset=96
      local.get $l9
      local.get $l12
      local.get $p8
      local.get $p8
      local.get $p8
      f32.add
      local.tee $l15
      f32.mul
      local.tee $l17
      f32.sub
      f32.store offset=80
      local.get $l9
      local.get $l26
      f32.store offset=100
      local.get $l9
      local.get $l22
      local.get $p8
      f32.mul
      local.tee $p8
      local.get $l14
      local.get $l18
      f32.mul
      local.tee $l12
      f32.add
      f32.store offset=88
      local.get $l9
      local.get $l22
      local.get $l13
      f32.mul
      local.tee $l13
      local.get $l14
      local.get $l15
      f32.mul
      local.tee $l14
      f32.sub
      f32.store offset=76
      local.get $l9
      local.get $p8
      local.get $l12
      f32.sub
      f32.store offset=72
      local.get $l9
      local.get $l13
      local.get $l14
      f32.add
      f32.store offset=68
      local.get $l9
      f32.const 0x1p+0 (;=1;)
      local.get $l16
      f32.sub
      local.get $l17
      f32.sub
      f32.store offset=64
      local.get $p5
      local.set $p8
      f32.const 0x1p+0 (;=1;)
    end
    local.set $l19
    local.get $l9
    i32.const 144
    i32.add
    local.get $l9
    i32.const 128
    i32.add
    local.get $p8
    i32.const 1
    local.get $p0
    local.get $l9
    i32.const 8
    i32.add
    local.get $p6
    local.get $l9
    i32.const -64
    i32.sub
    local.get $p5
    local.get $p3
    i32.const 0
    i32.ne
    local.get $l9
    i32.const 160
    i32.add
    local.get $p4
    local.get $p7
    local.get $p1
    f32.load offset=4
    local.get $p1
    f32.load offset=8
    f32.mul
    local.get $p1
    f32.load offset=12
    f32.mul
    f32.const 0x0p+0 (;=0;)
    f32.lt
    local.get $l19
    call $f70110
    local.tee $p4
    local.get $l9
    i32.const 112
    i32.add
    call $f70125
    local.get $p4
    local.get $p6
    local.get $l9
    i32.const 160
    i32.add
    local.get $p1
    local.get $p2
    local.get $p3
    local.get $l11
    i32.const 128
    i32.and
    i32.or
    i32.const 0
    i32.ne
    call $f70112
    local.set $p2
    local.get $l9
    i32.const 192
    i32.add
    global.set $g0
    local.get $p2)
