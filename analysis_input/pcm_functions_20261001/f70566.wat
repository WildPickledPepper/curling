  (func $f70566 (type $t18) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 i32) (param $p7 i32) (result i32)
    (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32) (local $l33 f32) (local $l34 f32) (local $l35 f32)
    global.get $g0
    i32.const 240
    i32.sub
    local.tee $p0
    global.set $g0
    local.get $p5
    i32.load
    local.set $p5
    local.get $p3
    f32.load offset=20
    local.set $l13
    local.get $p3
    f32.load offset=24
    local.set $l17
    local.get $p3
    f32.load
    local.set $l12
    local.get $p3
    f32.load offset=4
    local.set $l10
    local.get $p3
    f32.load offset=8
    local.set $l18
    local.get $p3
    f32.load offset=12
    local.set $l20
    local.get $p3
    f32.load offset=16
    local.set $l19
    local.get $p0
    i32.const 0
    i32.store offset=236
    local.get $p0
    local.get $l17
    f32.store offset=232
    local.get $p0
    local.get $l13
    f32.store offset=228
    local.get $p0
    local.get $l19
    f32.store offset=224
    local.get $p0
    local.get $l20
    f32.store offset=220
    local.get $p0
    local.get $l18
    f32.store offset=216
    local.get $p0
    local.get $l10
    f32.store offset=212
    local.get $p0
    local.get $l12
    f32.store offset=208
    local.get $p2
    f32.load offset=20
    local.set $l25
    local.get $p2
    f32.load offset=24
    local.set $l22
    local.get $p2
    f32.load offset=16
    local.set $l23
    local.get $p2
    f32.load offset=4
    local.set $l8
    local.get $p2
    f32.load
    local.set $l14
    local.get $p2
    f32.load offset=8
    local.set $l11
    local.get $p2
    f32.load offset=12
    local.set $l9
    local.get $p0
    i32.const 0
    i32.store offset=204
    local.get $p0
    local.get $l14
    local.get $l14
    local.get $l14
    f32.add
    local.tee $l16
    f32.mul
    local.get $l9
    local.get $l9
    local.get $l9
    f32.add
    local.tee $l15
    f32.mul
    f32.add
    f32.const -0x1p+0 (;=-1;)
    f32.add
    local.tee $l21
    f32.const 0x1p+0 (;=1;)
    local.get $l16
    local.get $l11
    f32.mul
    local.get $l8
    local.get $l15
    f32.mul
    f32.sub
    local.tee $l24
    local.get $l24
    f32.mul
    local.get $l16
    local.get $l8
    f32.mul
    local.get $l11
    local.get $l15
    f32.mul
    f32.add
    local.tee $l16
    local.get $l16
    f32.mul
    local.get $l21
    local.get $l21
    f32.mul
    f32.add
    f32.add
    f32.sqrt
    f32.div
    local.tee $l15
    f32.mul
    local.tee $l21
    f32.store offset=192
    local.get $p0
    local.get $l16
    local.get $l15
    f32.mul
    local.tee $l16
    f32.store offset=196
    local.get $p0
    local.get $l24
    local.get $l15
    f32.mul
    local.tee $l15
    f32.store offset=200
    local.get $p0
    i32.const 0
    i32.store offset=188
    local.get $p0
    local.get $l15
    f32.neg
    f32.store offset=184
    local.get $p0
    local.get $l16
    f32.neg
    f32.store offset=180
    local.get $p0
    local.get $l21
    f32.neg
    f32.store offset=176
    local.get $p0
    local.get $p4
    f32.load
    local.tee $l15
    f32.store offset=160
    local.get $p0
    local.get $p1
    f32.load offset=4
    local.tee $l16
    f32.store offset=144
    local.get $p1
    f32.load offset=8
    local.set $l26
    local.get $p0
    local.get $l16
    f32.const 0x1.0624dep-10 (;=0.001;)
    f32.mul
    f32.store offset=128
    local.get $p0
    local.get $l16
    f32.const 0x1.99999ap-5 (;=0.05;)
    f32.mul
    f32.store offset=112
    local.get $p5
    i32.load8_u offset=64
    local.set $p2
    local.get $p0
    local.get $l15
    local.get $l16
    f32.add
    local.tee $l27
    f32.store offset=96
    local.get $p0
    i32.const 0
    i32.store offset=92
    local.get $p0
    local.get $l9
    local.get $l9
    f32.mul
    f32.const -0x1p-1 (;=-0.5;)
    f32.add
    local.tee $l28
    local.get $l17
    local.get $l22
    f32.sub
    local.tee $l15
    f32.mul
    local.get $l9
    local.get $l8
    local.get $l19
    local.get $l23
    f32.sub
    local.tee $l21
    f32.mul
    local.get $l14
    local.get $l13
    local.get $l25
    f32.sub
    local.tee $l24
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l11
    local.get $l24
    local.get $l8
    f32.neg
    local.tee $l31
    f32.mul
    local.get $l14
    local.get $l21
    f32.mul
    f32.sub
    local.get $l11
    local.get $l15
    f32.mul
    f32.sub
    local.tee $l29
    f32.mul
    f32.sub
    local.tee $l13
    local.get $l13
    f32.add
    local.tee $l22
    f32.store offset=88
    local.get $p0
    local.get $l28
    local.get $l24
    f32.mul
    local.get $l9
    local.get $l14
    local.get $l15
    f32.mul
    local.get $l11
    local.get $l21
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l8
    local.get $l29
    f32.mul
    f32.sub
    local.tee $l13
    local.get $l13
    f32.add
    local.tee $l23
    f32.store offset=84
    local.get $p0
    i32.const 0
    i32.store offset=76
    local.get $p0
    f32.const 0x1p+0 (;=1;)
    local.get $l10
    local.get $l11
    f32.mul
    local.get $l18
    local.get $l8
    f32.mul
    f32.sub
    local.get $l12
    local.get $l9
    f32.mul
    local.get $l20
    local.get $l14
    f32.mul
    f32.sub
    f32.add
    local.tee $l19
    local.get $l19
    local.get $l19
    f32.add
    local.tee $l25
    f32.mul
    local.tee $l32
    f32.sub
    local.tee $l33
    local.get $l18
    local.get $l14
    f32.mul
    local.get $l12
    local.get $l11
    f32.mul
    f32.sub
    local.get $l10
    local.get $l9
    f32.mul
    local.get $l20
    local.get $l8
    f32.mul
    f32.sub
    f32.add
    local.tee $l17
    local.get $l17
    local.get $l17
    f32.add
    local.tee $l30
    f32.mul
    local.tee $l34
    f32.sub
    f32.store offset=72
    local.get $p0
    local.get $l12
    local.get $l8
    f32.mul
    local.get $l10
    local.get $l14
    f32.mul
    f32.sub
    local.get $l18
    local.get $l9
    f32.mul
    local.get $l20
    local.get $l11
    f32.mul
    f32.sub
    f32.add
    local.tee $l13
    local.get $l30
    f32.mul
    local.tee $l35
    local.get $l20
    local.get $l9
    f32.mul
    local.get $l10
    local.get $l31
    f32.mul
    local.get $l12
    local.get $l14
    f32.mul
    f32.sub
    local.get $l18
    local.get $l11
    f32.mul
    f32.sub
    f32.sub
    local.tee $l12
    local.get $l25
    f32.mul
    local.tee $l10
    f32.sub
    f32.store offset=68
    local.get $p0
    i32.const 0
    i32.store offset=60
    local.get $p0
    local.get $l35
    local.get $l10
    f32.add
    f32.store offset=56
    local.get $p0
    local.get $l33
    local.get $l13
    local.get $l13
    local.get $l13
    f32.add
    local.tee $l10
    f32.mul
    local.tee $l18
    f32.sub
    f32.store offset=52
    local.get $p0
    local.get $l28
    local.get $l21
    f32.mul
    local.get $l9
    local.get $l11
    local.get $l24
    f32.mul
    local.get $l8
    local.get $l15
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l14
    local.get $l29
    f32.mul
    f32.sub
    local.tee $l9
    local.get $l9
    f32.add
    local.tee $l9
    f32.store offset=80
    local.get $p0
    local.get $l13
    local.get $l25
    f32.mul
    local.tee $l14
    local.get $l12
    local.get $l30
    f32.mul
    local.tee $l8
    f32.add
    f32.store offset=64
    local.get $p0
    local.get $l17
    local.get $l25
    f32.mul
    local.tee $l11
    local.get $l12
    local.get $l10
    f32.mul
    local.tee $l10
    f32.sub
    f32.store offset=48
    local.get $p0
    i32.const 0
    i32.store offset=44
    local.get $p0
    local.get $l14
    local.get $l8
    f32.sub
    f32.store offset=40
    local.get $p0
    local.get $l11
    local.get $l10
    f32.add
    f32.store offset=36
    local.get $p0
    f32.const 0x1p+0 (;=1;)
    local.get $l34
    f32.sub
    local.get $l18
    f32.sub
    f32.store offset=32
    local.get $p5
    local.get $p0
    i32.const 32
    i32.add
    local.get $p0
    i32.const 112
    i32.add
    call $f70045
    block $B0
      block $B1
        local.get $p2
        local.get $p5
        i32.load8_u offset=64
        i32.ne
        br_if $B1
        local.get $l19
        local.get $p5
        f32.load
        f32.mul
        local.get $l17
        local.get $p5
        f32.load offset=4
        f32.mul
        f32.add
        local.get $l13
        local.get $p5
        f32.load offset=8
        f32.mul
        f32.add
        local.get $l12
        local.get $p5
        f32.load offset=12
        f32.mul
        f32.add
        f32.const 0x1.ffe5cap-1 (;=0.9998;)
        f32.lt
        br_if $B1
        local.get $l16
        f32.const 0x1.47ae14p-6 (;=0.02;)
        f32.mul
        local.get $l9
        local.get $p5
        f32.load offset=16
        f32.sub
        local.tee $l8
        local.get $l8
        f32.neg
        local.tee $l10
        local.get $l8
        local.get $l10
        f32.gt
        select
        local.tee $l8
        local.get $l23
        local.get $p5
        f32.load offset=20
        f32.sub
        local.tee $l10
        local.get $l10
        f32.neg
        local.tee $l18
        local.get $l10
        local.get $l18
        f32.gt
        select
        local.tee $l10
        local.get $l8
        local.get $l10
        f32.ge
        select
        local.tee $l18
        local.get $l8
        f32.const 0x0p+0 (;=0;)
        local.get $l22
        local.get $p5
        f32.load offset=24
        f32.sub
        local.tee $l10
        local.get $l10
        f32.neg
        local.tee $l20
        local.get $l10
        local.get $l20
        f32.gt
        select
        f32.const 0x0p+0 (;=0;)
        f32.ge
        select
        local.tee $l8
        local.get $l8
        local.get $l18
        f32.le
        select
        f32.lt
        i32.eqz
        br_if $B0
      end
      local.get $l14
      local.get $l12
      local.get $l12
      f32.add
      local.tee $l8
      local.get $l17
      f32.mul
      f32.sub
      local.get $l26
      f32.mul
      local.set $l10
      local.get $l8
      local.get $l13
      f32.mul
      local.get $l11
      f32.add
      local.get $l26
      f32.mul
      local.set $l18
      local.get $l9
      local.get $l12
      local.get $l8
      f32.mul
      local.get $l32
      f32.add
      f32.const -0x1p+0 (;=-1;)
      f32.add
      local.get $l26
      f32.mul
      local.tee $l11
      f32.sub
      local.set $l14
      local.get $p5
      local.get $l9
      f32.store offset=16
      local.get $p5
      local.get $l12
      f32.store offset=12
      local.get $p5
      local.get $l13
      f32.store offset=8
      local.get $p5
      local.get $l17
      f32.store offset=4
      local.get $p5
      local.get $l19
      f32.store
      local.get $p5
      i32.const 0
      i32.store8 offset=64
      local.get $p5
      i32.const 0
      i32.store offset=28
      local.get $p5
      local.get $l22
      f32.store offset=24
      local.get $p5
      local.get $l23
      f32.store offset=20
      local.get $l9
      local.get $l11
      f32.add
      local.tee $l11
      local.get $l27
      f32.lt
      if $I2
        local.get $p0
        i32.const 0
        i32.store offset=44
        local.get $p0
        local.get $l13
        local.get $l13
        local.get $l22
        local.get $l10
        f32.add
        local.tee $l24
        local.get $l22
        f32.sub
        local.tee $l8
        f32.mul
        local.get $l19
        local.get $l11
        local.get $l9
        f32.sub
        local.tee $l20
        f32.mul
        local.get $l17
        local.get $l23
        local.get $l18
        f32.add
        local.tee $l25
        local.get $l23
        f32.sub
        local.tee $l16
        f32.mul
        f32.add
        f32.add
        local.tee $l15
        f32.mul
        local.get $l12
        local.get $l12
        f32.mul
        f32.const -0x1p-1 (;=-0.5;)
        f32.add
        local.tee $l21
        local.get $l8
        f32.mul
        local.get $l12
        local.get $l19
        local.get $l16
        f32.mul
        local.get $l17
        local.get $l20
        f32.mul
        f32.sub
        f32.mul
        f32.sub
        f32.add
        local.tee $l26
        local.get $l26
        f32.add
        f32.store offset=40
        local.get $p0
        local.get $l17
        local.get $l15
        f32.mul
        local.get $l21
        local.get $l16
        f32.mul
        local.get $l12
        local.get $l13
        local.get $l20
        f32.mul
        local.get $l19
        local.get $l8
        f32.mul
        f32.sub
        f32.mul
        f32.sub
        f32.add
        local.tee $l26
        local.get $l26
        f32.add
        f32.store offset=36
        local.get $p0
        local.get $l19
        local.get $l15
        f32.mul
        local.get $l21
        local.get $l20
        f32.mul
        local.get $l12
        local.get $l17
        local.get $l8
        f32.mul
        local.get $l13
        local.get $l16
        f32.mul
        f32.sub
        f32.mul
        f32.sub
        f32.add
        local.tee $l8
        local.get $l8
        f32.add
        f32.store offset=32
        local.get $p0
        i32.const 0
        i32.store offset=28
        local.get $p0
        local.get $l24
        local.get $l11
        f32.const 0x0p+0 (;=0;)
        f32.mul
        local.tee $l8
        f32.sub
        f32.store offset=24
        local.get $p0
        local.get $l25
        local.get $l8
        f32.sub
        f32.store offset=20
        local.get $p0
        local.get $l11
        local.get $l11
        f32.sub
        f32.store offset=16
        local.get $p0
        local.get $l11
        f32.store offset=12
        local.get $p0
        i32.const 0
        i32.store offset=8
        local.get $p0
        i64.const 1065353216
        i64.store
        local.get $p5
        local.get $p0
        i32.const 32
        i32.add
        local.get $p0
        i32.const 16
        i32.add
        local.get $p0
        local.get $p0
        i32.const 128
        i32.add
        call $f69967
      end
      local.get $l14
      local.get $l27
      f32.lt
      i32.eqz
      br_if $B0
      local.get $p0
      i32.const 0
      i32.store offset=44
      local.get $p0
      local.get $l13
      local.get $l13
      local.get $l22
      local.get $l10
      f32.sub
      local.tee $l20
      local.get $l22
      f32.sub
      local.tee $l11
      f32.mul
      local.get $l19
      local.get $l14
      local.get $l9
      f32.sub
      local.tee $l9
      f32.mul
      local.get $l17
      local.get $l23
      local.get $l18
      f32.sub
      local.tee $l16
      local.get $l23
      f32.sub
      local.tee $l8
      f32.mul
      f32.add
      f32.add
      local.tee $l10
      f32.mul
      local.get $l12
      local.get $l12
      f32.mul
      f32.const -0x1p-1 (;=-0.5;)
      f32.add
      local.tee $l18
      local.get $l11
      f32.mul
      local.get $l12
      local.get $l19
      local.get $l8
      f32.mul
      local.get $l17
      local.get $l9
      f32.mul
      f32.sub
      f32.mul
      f32.sub
      f32.add
      local.tee $l15
      local.get $l15
      f32.add
      f32.store offset=40
      local.get $p0
      local.get $l17
      local.get $l10
      f32.mul
      local.get $l18
      local.get $l8
      f32.mul
      local.get $l12
      local.get $l13
      local.get $l9
      f32.mul
      local.get $l19
      local.get $l11
      f32.mul
      f32.sub
      f32.mul
      f32.sub
      f32.add
      local.tee $l15
      local.get $l15
      f32.add
      f32.store offset=36
      local.get $p0
      local.get $l19
      local.get $l10
      f32.mul
      local.get $l18
      local.get $l9
      f32.mul
      local.get $l12
      local.get $l17
      local.get $l11
      f32.mul
      local.get $l13
      local.get $l8
      f32.mul
      f32.sub
      f32.mul
      f32.sub
      f32.add
      local.tee $l9
      local.get $l9
      f32.add
      f32.store offset=32
      local.get $p0
      i32.const 0
      i32.store offset=28
      local.get $p0
      local.get $l20
      local.get $l14
      f32.const 0x0p+0 (;=0;)
      f32.mul
      local.tee $l9
      f32.sub
      f32.store offset=24
      local.get $p0
      local.get $l16
      local.get $l9
      f32.sub
      f32.store offset=20
      local.get $p0
      local.get $l14
      local.get $l14
      f32.sub
      f32.store offset=16
      local.get $p0
      local.get $l14
      f32.store offset=12
      local.get $p0
      i32.const 0
      i32.store offset=8
      local.get $p0
      i64.const 1065353216
      i64.store
      local.get $p5
      local.get $p0
      i32.const 32
      i32.add
      local.get $p0
      i32.const 16
      i32.add
      local.get $p0
      local.get $p0
      i32.const 128
      i32.add
      call $f69967
    end
    local.get $p5
    local.get $p6
    local.get $p0
    i32.const 176
    i32.add
    local.get $p0
    i32.const 192
    i32.add
    local.get $p0
    i32.const 208
    i32.add
    local.get $p0
    i32.const 144
    i32.add
    local.get $p0
    i32.const 160
    i32.add
    call $f69968
    local.get $p5
    i32.load8_u offset=64
    local.set $p5
    local.get $p0
    i32.const 240
    i32.add
    global.set $g0
    local.get $p5
    i32.const 0
    i32.ne)
