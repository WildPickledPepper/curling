  (func $f70128 (type $t9) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (result i32)
    (local $l5 i32) (local $l6 i32) (local $l7 f32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32)
    global.get $g0
    i32.const 256
    i32.sub
    local.tee $l5
    global.set $g0
    local.get $p3
    f32.load offset=8
    local.set $l8
    local.get $p3
    f32.load offset=4
    local.set $l7
    block $B0 (result i32)
      block $B1
        local.get $p3
        f32.load
        local.tee $l9
        f32.const 0x1p+0 (;=1;)
        f32.ne
        br_if $B1
        local.get $l7
        f32.const 0x1p+0 (;=1;)
        f32.ne
        br_if $B1
        f32.const 0x1p+0 (;=1;)
        local.set $l7
        local.get $l8
        f32.const 0x1p+0 (;=1;)
        f32.ne
        br_if $B1
        local.get $l5
        i32.const 0
        i32.store16 offset=16
        local.get $l5
        local.get $p4
        i32.store offset=12
        local.get $l5
        i32.const 2
        i32.store offset=4
        local.get $l5
        i32.const 3125312
        i32.store
        local.get $l5
        local.get $l5
        i32.const -64
        i32.sub
        i32.store offset=8
        local.get $l5
        local.get $p0
        f32.load offset=8
        local.get $p2
        f32.load offset=24
        f32.sub
        local.tee $l7
        local.get $l7
        f32.add
        local.tee $l8
        local.get $p2
        f32.load offset=12
        local.tee $l7
        local.get $l7
        f32.mul
        f32.const -0x1p-1 (;=-0.5;)
        f32.add
        local.tee $l13
        f32.mul
        local.get $l7
        local.get $p0
        f32.load offset=4
        local.get $p2
        f32.load offset=20
        f32.sub
        local.tee $l9
        local.get $l9
        f32.add
        local.tee $l9
        local.get $p2
        f32.load
        local.tee $l10
        f32.mul
        local.get $p0
        f32.load
        local.get $p2
        f32.load offset=16
        f32.sub
        local.tee $l11
        local.get $l11
        f32.add
        local.tee $l11
        local.get $p2
        f32.load offset=4
        local.tee $l12
        f32.mul
        f32.sub
        f32.mul
        f32.sub
        local.get $p2
        f32.load offset=8
        local.tee $l14
        local.get $l11
        local.get $l10
        f32.mul
        local.get $l9
        local.get $l12
        f32.mul
        f32.add
        local.get $l8
        local.get $l14
        f32.mul
        f32.add
        local.tee $l15
        f32.mul
        f32.add
        local.tee $l18
        f32.store offset=32
        local.get $l5
        local.get $l12
        local.get $l15
        f32.mul
        local.get $l9
        local.get $l13
        f32.mul
        local.get $l7
        local.get $l11
        local.get $l14
        f32.mul
        local.get $l8
        local.get $l10
        f32.mul
        f32.sub
        f32.mul
        f32.sub
        f32.add
        local.tee $l16
        f32.store offset=28
        local.get $l5
        local.get $l10
        local.get $l15
        f32.mul
        local.get $l11
        local.get $l13
        f32.mul
        local.get $l7
        local.get $l8
        local.get $l12
        f32.mul
        local.get $l9
        local.get $l14
        f32.mul
        f32.sub
        f32.mul
        f32.sub
        f32.add
        local.tee $l8
        f32.store offset=24
        local.get $l5
        local.get $p0
        f32.load offset=12
        local.tee $l7
        local.get $l7
        f32.mul
        f32.store offset=20
        local.get $l5
        local.get $l18
        f32.store offset=224
        local.get $l5
        local.get $l16
        f32.store offset=220
        local.get $l5
        local.get $l8
        f32.store offset=216
        local.get $l5
        i32.const 0
        i32.store offset=184
        local.get $l5
        i64.const 1065353216
        i64.store offset=176
        local.get $l5
        local.get $l7
        f32.const 0x1.0624dep-10 (;=0.001;)
        local.get $l7
        f32.const 0x1.0624dep-10 (;=0.001;)
        f32.gt
        select
        local.tee $l7
        f32.store offset=168
        local.get $l5
        local.get $l7
        f32.store offset=164
        local.get $l5
        local.get $l7
        f32.store offset=160
        local.get $l5
        i32.const 216
        i32.add
        local.get $l5
        i32.const 176
        i32.add
        f32.const 0x0p+0 (;=0;)
        i32.const 1
        local.get $p1
        local.get $l5
        local.get $l5
        i32.const 160
        i32.add
        call $f70125
        local.get $l5
        i32.load8_u offset=16
        br $B0
      end
      local.get $l5
      f32.const 0x1p+0 (;=1;)
      local.get $p3
      f32.load offset=12
      local.tee $l10
      local.get $l10
      local.get $l10
      f32.add
      local.tee $l11
      f32.mul
      f32.sub
      local.tee $l21
      local.get $p3
      f32.load offset=16
      local.tee $l12
      local.get $l12
      local.get $l12
      f32.add
      local.tee $l15
      f32.mul
      local.tee $l24
      f32.sub
      local.tee $l14
      local.get $l8
      local.get $l14
      f32.mul
      local.tee $l16
      f32.mul
      local.get $l11
      local.get $p3
      f32.load offset=20
      local.tee $l10
      f32.mul
      local.tee $l25
      local.get $l15
      local.get $p3
      f32.load offset=24
      local.tee $l17
      f32.mul
      local.tee $l26
      f32.add
      local.tee $l13
      local.get $l9
      local.get $l13
      f32.mul
      local.tee $l19
      f32.mul
      local.get $l15
      local.get $l10
      f32.mul
      local.tee $l18
      local.get $l11
      local.get $l17
      f32.mul
      local.tee $l20
      f32.sub
      local.tee $l15
      local.get $l7
      local.get $l15
      f32.mul
      local.tee $l22
      f32.mul
      f32.add
      f32.add
      f32.store offset=248
      local.get $l5
      local.get $l14
      local.get $l8
      local.get $l18
      local.get $l20
      f32.add
      local.tee $l18
      f32.mul
      local.tee $l20
      f32.mul
      local.get $l13
      local.get $l9
      local.get $l11
      local.get $l12
      f32.mul
      local.tee $l27
      local.get $l17
      local.get $l10
      local.get $l10
      f32.add
      local.tee $l12
      f32.mul
      local.tee $l17
      f32.sub
      local.tee $l11
      f32.mul
      local.tee $l23
      f32.mul
      local.get $l15
      local.get $l7
      local.get $l21
      local.get $l10
      local.get $l12
      f32.mul
      local.tee $l28
      f32.sub
      local.tee $l10
      f32.mul
      local.tee $l21
      f32.mul
      f32.add
      f32.add
      f32.store offset=244
      local.get $l5
      local.get $l18
      local.get $l16
      f32.mul
      local.get $l11
      local.get $l19
      f32.mul
      local.get $l10
      local.get $l22
      f32.mul
      f32.add
      f32.add
      f32.store offset=236
      local.get $l5
      local.get $l18
      local.get $l20
      f32.mul
      local.get $l11
      local.get $l23
      f32.mul
      local.get $l10
      local.get $l21
      f32.mul
      f32.add
      f32.add
      f32.store offset=232
      local.get $l5
      local.get $l25
      local.get $l26
      f32.sub
      local.tee $l12
      local.get $l16
      f32.mul
      f32.const 0x1p+0 (;=1;)
      local.get $l24
      f32.sub
      local.get $l28
      f32.sub
      local.tee $l16
      local.get $l19
      f32.mul
      local.get $l27
      local.get $l17
      f32.add
      local.tee $l17
      local.get $l22
      f32.mul
      f32.add
      f32.add
      f32.store offset=224
      local.get $l5
      local.get $l12
      local.get $l20
      f32.mul
      local.get $l16
      local.get $l23
      f32.mul
      local.get $l17
      local.get $l21
      f32.mul
      f32.add
      f32.add
      f32.store offset=220
      local.get $l5
      local.get $l14
      local.get $l8
      local.get $l12
      f32.mul
      local.tee $l19
      f32.mul
      local.get $l13
      local.get $l9
      local.get $l16
      f32.mul
      local.tee $l14
      f32.mul
      local.get $l15
      local.get $l7
      local.get $l17
      f32.mul
      local.tee $l13
      f32.mul
      f32.add
      f32.add
      f32.store offset=240
      local.get $l5
      local.get $l18
      local.get $l19
      f32.mul
      local.get $l11
      local.get $l14
      f32.mul
      local.get $l10
      local.get $l13
      f32.mul
      f32.add
      f32.add
      f32.store offset=228
      local.get $l5
      local.get $l12
      local.get $l19
      f32.mul
      local.get $l16
      local.get $l14
      f32.mul
      local.get $l17
      local.get $l13
      f32.mul
      f32.add
      f32.add
      f32.store offset=216
      local.get $l5
      local.get $l9
      local.get $l7
      f32.mul
      local.get $l8
      f32.mul
      f32.const 0x0p+0 (;=0;)
      f32.lt
      i32.store8 offset=193
      local.get $l5
      local.get $p4
      i32.store offset=188
      local.get $l5
      i32.const 3125332
      i32.store offset=176
      local.get $l5
      local.get $l5
      i32.const 216
      i32.add
      i32.store offset=184
      local.get $l5
      i32.const 0
      i32.store8 offset=192
      local.get $l5
      i32.const 2
      i32.store offset=180
      local.get $l5
      local.get $p0
      f32.load offset=8
      local.tee $l18
      local.get $p2
      f32.load offset=24
      f32.sub
      local.tee $l7
      local.get $l7
      f32.add
      local.tee $l8
      local.get $p2
      f32.load offset=12
      local.tee $l7
      local.get $l7
      f32.mul
      f32.const -0x1p-1 (;=-0.5;)
      f32.add
      local.tee $l13
      f32.mul
      local.get $l7
      local.get $p0
      f32.load offset=4
      local.tee $l16
      local.get $p2
      f32.load offset=20
      f32.sub
      local.tee $l9
      local.get $l9
      f32.add
      local.tee $l9
      local.get $p2
      f32.load
      local.tee $l10
      f32.mul
      local.get $p0
      f32.load
      local.tee $l17
      local.get $p2
      f32.load offset=16
      f32.sub
      local.tee $l11
      local.get $l11
      f32.add
      local.tee $l11
      local.get $p2
      f32.load offset=4
      local.tee $l12
      f32.mul
      f32.sub
      f32.mul
      f32.sub
      local.get $p2
      f32.load offset=8
      local.tee $l14
      local.get $l11
      local.get $l10
      f32.mul
      local.get $l9
      local.get $l12
      f32.mul
      f32.add
      local.get $l8
      local.get $l14
      f32.mul
      f32.add
      local.tee $l15
      f32.mul
      f32.add
      f32.store offset=208
      local.get $l5
      local.get $l12
      local.get $l15
      f32.mul
      local.get $l9
      local.get $l13
      f32.mul
      local.get $l7
      local.get $l11
      local.get $l14
      f32.mul
      local.get $l8
      local.get $l10
      f32.mul
      f32.sub
      f32.mul
      f32.sub
      f32.add
      f32.store offset=204
      local.get $l5
      local.get $l10
      local.get $l15
      f32.mul
      local.get $l11
      local.get $l13
      f32.mul
      local.get $l7
      local.get $l8
      local.get $l12
      f32.mul
      local.get $l9
      local.get $l14
      f32.mul
      f32.sub
      f32.mul
      f32.sub
      f32.add
      f32.store offset=200
      local.get $l5
      local.get $p0
      f32.load offset=12
      local.tee $l7
      local.get $l7
      f32.mul
      f32.store offset=196
      local.get $l5
      local.get $l7
      f32.store offset=120
      local.get $l5
      local.get $l7
      f32.store offset=116
      local.get $l5
      local.get $l18
      f32.store offset=108
      local.get $l5
      local.get $l16
      f32.store offset=104
      local.get $l5
      i32.const 1065353216
      i32.store offset=96
      local.get $l5
      i64.const 1065353216
      i64.store offset=80
      local.get $l5
      local.get $l7
      f32.store offset=112
      local.get $l5
      local.get $l17
      f32.store offset=100
      local.get $l5
      i64.const 0
      i64.store offset=88
      local.get $l5
      i64.const 0
      i64.store offset=72
      local.get $l5
      i64.const 1065353216
      i64.store offset=64
      local.get $l5
      local.get $l5
      i32.const -64
      i32.sub
      local.get $p2
      local.get $p3
      call $f69940
      local.get $l5
      i32.const 2
      i32.const 2
      i32.const 1
      local.get $l5
      f32.load offset=52
      local.tee $l7
      local.get $l5
      f32.load offset=56
      local.tee $l8
      f32.ge
      local.tee $p4
      select
      local.get $l5
      f32.load offset=48
      local.get $l7
      local.get $l8
      local.get $l7
      local.get $l8
      f32.gt
      select
      f32.ge
      local.tee $p2
      select
      local.tee $l6
      i32.const 12
      i32.mul
      i32.add
      local.tee $p3
      f32.load
      local.set $l10
      local.get $p3
      f32.load offset=4
      local.set $l11
      local.get $l5
      i32.const 48
      i32.add
      local.tee $p0
      local.get $l6
      i32.const 2
      i32.shl
      i32.add
      f32.load
      local.set $l7
      local.get $p3
      f32.load offset=8
      local.set $l12
      local.get $l5
      i32.const 0
      i32.const 1
      i32.const 2
      local.get $p4
      select
      local.get $p2
      select
      local.tee $l6
      i32.const 12
      i32.mul
      i32.add
      local.tee $p3
      f32.load
      local.set $l14
      local.get $p3
      f32.load offset=4
      local.set $l13
      local.get $l5
      local.get $p2
      i32.const 12
      i32.mul
      i32.add
      local.tee $p4
      f32.load
      local.set $l15
      local.get $p4
      f32.load offset=4
      local.set $l18
      local.get $p0
      local.get $p2
      i32.const 2
      i32.shl
      i32.or
      f32.load
      local.set $l8
      local.get $p4
      f32.load offset=8
      local.set $l16
      local.get $l5
      f32.load offset=40
      local.set $l17
      local.get $l5
      f32.load offset=44
      local.set $l19
      local.get $l5
      f32.load offset=36
      local.set $l22
      local.get $l5
      local.get $p0
      local.get $l6
      i32.const 2
      i32.shl
      i32.add
      f32.load
      local.tee $l9
      local.get $p3
      f32.load offset=8
      f32.mul
      local.tee $l20
      f32.store offset=152
      local.get $l5
      local.get $l19
      local.get $l20
      f32.sub
      f32.store offset=168
      local.get $l5
      local.get $l9
      local.get $l13
      f32.mul
      local.tee $l13
      f32.store offset=148
      local.get $l5
      local.get $l17
      local.get $l13
      f32.sub
      f32.store offset=164
      local.get $l5
      local.get $l9
      local.get $l14
      f32.mul
      local.tee $l9
      f32.store offset=144
      local.get $l5
      local.get $l22
      local.get $l9
      f32.sub
      f32.store offset=160
      local.get $l5
      local.get $l8
      local.get $l16
      f32.abs
      f32.mul
      local.get $l7
      local.get $l12
      f32.abs
      f32.mul
      f32.add
      f32.const 0x1.0624dep-10 (;=0.001;)
      f32.add
      f32.store offset=136
      local.get $l5
      local.get $l8
      local.get $l18
      f32.abs
      f32.mul
      local.get $l7
      local.get $l11
      f32.abs
      f32.mul
      f32.add
      f32.const 0x1.0624dep-10 (;=0.001;)
      f32.add
      f32.store offset=132
      local.get $l5
      local.get $l8
      local.get $l15
      f32.abs
      f32.mul
      local.get $l7
      local.get $l10
      f32.abs
      f32.mul
      f32.add
      f32.const 0x1.0624dep-10 (;=0.001;)
      f32.add
      f32.store offset=128
      local.get $l5
      i32.const 160
      i32.add
      local.get $l5
      i32.const 144
      i32.add
      f32.const 0x1p+1 (;=2;)
      i32.const 1
      local.get $p1
      local.get $l5
      i32.const 176
      i32.add
      local.get $l5
      i32.const 128
      i32.add
      call $f70125
      local.get $l5
      i32.load8_u offset=192
    end
    local.set $p2
    local.get $l5
    i32.const 256
    i32.add
    global.set $g0
    local.get $p2
    i32.const 255
    i32.and
    i32.const 0
    i32.ne)
