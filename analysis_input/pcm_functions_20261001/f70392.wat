  (func $f70392 (type $t80) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 f32) (param $p7 i32) (param $p8 i32) (param $p9 f32) (result i32)
    (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32)
    global.get $g0
    i32.const 176
    i32.sub
    local.tee $p2
    global.set $g0
    local.get $p1
    f32.load offset=20
    local.set $p9
    local.get $p4
    f32.load offset=40
    local.set $l10
    local.get $p1
    f32.load offset=24
    local.set $l11
    local.get $p4
    f32.load offset=44
    local.set $l13
    local.get $p1
    f32.load offset=16
    local.set $l14
    local.get $p4
    f32.load offset=36
    local.set $l15
    local.get $p2
    local.get $p4
    f32.load
    f32.store offset=112
    local.get $p2
    local.get $p4
    f32.load offset=4
    f32.store offset=116
    local.get $p2
    local.get $p4
    f32.load offset=8
    f32.store offset=120
    local.get $p2
    local.get $p4
    f32.load offset=12
    f32.store offset=124
    local.get $p2
    local.get $p4
    f32.load offset=16
    f32.store offset=128
    local.get $p2
    local.get $p4
    f32.load offset=20
    f32.store offset=132
    local.get $p2
    local.get $p4
    f32.load offset=24
    f32.store offset=136
    local.get $p2
    local.get $p4
    f32.load offset=28
    f32.store offset=140
    local.get $p4
    f32.load offset=32
    local.set $l12
    local.get $p2
    local.get $l13
    local.get $l11
    f32.sub
    local.tee $l16
    f32.store offset=156
    local.get $p2
    local.get $l10
    local.get $p9
    f32.sub
    local.tee $l17
    f32.store offset=152
    local.get $p2
    local.get $l12
    f32.store offset=144
    local.get $p2
    local.get $l15
    local.get $l14
    f32.sub
    local.tee $l15
    f32.store offset=148
    local.get $p2
    local.get $p4
    f32.load offset=48
    f32.store offset=160
    local.get $p2
    local.get $p4
    f32.load offset=52
    f32.store offset=164
    local.get $p2
    local.get $p4
    f32.load offset=56
    f32.store offset=168
    local.get $p2
    local.get $p0
    f32.load offset=8
    local.tee $p9
    local.get $p1
    f32.load
    local.tee $l10
    local.get $l10
    f32.add
    local.tee $l11
    local.get $p1
    f32.load offset=8
    local.tee $l12
    f32.mul
    local.get $p1
    f32.load offset=12
    local.tee $l13
    local.get $l13
    f32.add
    local.tee $l14
    local.get $p1
    f32.load offset=4
    local.tee $l18
    f32.mul
    f32.sub
    f32.mul
    local.tee $l19
    f32.store offset=88
    local.get $p2
    local.get $l19
    f32.neg
    f32.store offset=100
    local.get $p2
    local.get $p9
    local.get $l12
    local.get $l14
    f32.mul
    local.get $l11
    local.get $l18
    f32.mul
    f32.add
    f32.mul
    local.tee $l12
    f32.store offset=84
    local.get $p2
    local.get $l12
    f32.neg
    f32.store offset=96
    local.get $p2
    local.get $p9
    local.get $l10
    local.get $l11
    f32.mul
    local.get $l13
    local.get $l14
    f32.mul
    f32.const -0x1p+0 (;=-1;)
    f32.add
    f32.add
    f32.mul
    local.tee $p9
    f32.store offset=80
    local.get $p2
    local.get $p9
    f32.neg
    f32.store offset=92
    local.get $p2
    local.get $p0
    f32.load offset=4
    f32.store offset=104
    local.get $p2
    local.get $p3
    f32.load
    f32.store offset=48
    local.get $p2
    local.get $p3
    f32.load offset=4
    f32.store offset=52
    local.get $p2
    local.get $p3
    f32.load offset=8
    f32.store offset=56
    local.get $p3
    f32.load offset=12
    local.set $p9
    local.get $p2
    local.get $l16
    f32.store offset=72
    local.get $p2
    local.get $l17
    f32.store offset=68
    local.get $p2
    local.get $l15
    f32.store offset=64
    local.get $p2
    local.get $p9
    f32.store offset=60
    local.get $p5
    f32.load
    local.set $p9
    local.get $p5
    f32.load offset=4
    local.set $l10
    local.get $p2
    local.get $p5
    f32.load offset=8
    f32.neg
    f32.store offset=24
    local.get $p2
    local.get $l10
    f32.neg
    f32.store offset=20
    local.get $p2
    local.get $p9
    f32.neg
    f32.store offset=16
    local.get $p2
    local.get $p8
    i32.load16_u
    i32.store16 offset=8
    block $B0
      local.get $p2
      i32.const 80
      i32.add
      local.get $p2
      i32.const 48
      i32.add
      local.get $p2
      i32.const 160
      i32.add
      local.tee $p3
      local.get $p2
      i32.const 16
      i32.add
      local.get $p6
      local.get $p7
      i32.const 16
      i32.add
      local.get $p7
      i32.const 40
      i32.add
      local.get $p2
      i32.const 32
      i32.add
      local.get $p2
      i32.const 8
      i32.add
      call $f70373
      local.tee $p4
      i32.eqz
      br_if $B0
      local.get $p2
      f32.load offset=32
      local.set $p9
      local.get $p2
      f32.load offset=36
      local.set $l10
      local.get $p2
      f32.load offset=40
      local.set $l11
      local.get $p7
      i32.const 2
      i32.store16 offset=12
      local.get $p7
      local.get $l11
      f32.neg
      f32.store offset=36
      local.get $p7
      local.get $l10
      f32.neg
      f32.store offset=32
      local.get $p7
      local.get $p9
      f32.neg
      f32.store offset=28
      local.get $p8
      i32.load8_u
      i32.const 1
      i32.and
      i32.eqz
      br_if $B0
      local.get $p7
      f32.load offset=40
      local.tee $p9
      f32.const 0x0p+0 (;=0;)
      f32.eq
      br_if $B0
      local.get $p5
      f32.load offset=8
      local.set $l10
      local.get $p5
      f32.load offset=4
      local.set $l11
      local.get $p2
      local.get $p9
      local.get $p5
      f32.load
      f32.mul
      local.get $p2
      f32.load offset=148
      f32.add
      f32.store offset=148
      local.get $p2
      local.get $p9
      local.get $l11
      f32.mul
      local.get $p2
      f32.load offset=152
      f32.add
      f32.store offset=152
      local.get $p2
      local.get $p9
      local.get $l10
      f32.mul
      local.get $p2
      f32.load offset=156
      f32.add
      f32.store offset=156
      local.get $p2
      i32.const 80
      i32.add
      local.get $p2
      i32.const 92
      i32.add
      local.get $p2
      i32.const 148
      i32.add
      local.get $p3
      local.get $p2
      i32.const 112
      i32.add
      i32.const 0
      local.get $p2
      i32.const 16
      i32.add
      call $f69889
      drop
      local.get $p1
      f32.load offset=16
      local.set $l13
      local.get $p1
      f32.load offset=20
      local.set $l14
      local.get $p1
      f32.load offset=24
      local.set $p6
      local.get $p2
      f32.load offset=148
      local.set $l15
      local.get $p2
      f32.load offset=136
      local.set $l12
      local.get $p2
      f32.load offset=112
      local.set $l16
      local.get $p2
      f32.load offset=124
      local.set $l17
      local.get $p2
      f32.load offset=152
      local.set $l18
      local.get $p2
      f32.load offset=140
      local.set $l19
      local.get $p2
      f32.load offset=116
      local.set $l20
      local.get $p2
      f32.load offset=128
      local.set $l21
      local.get $p2
      f32.load offset=156
      local.set $l22
      local.get $p2
      f32.load offset=144
      local.set $l23
      local.get $p2
      f32.load offset=24
      local.set $p9
      local.get $p2
      f32.load offset=120
      local.set $l24
      local.get $p2
      f32.load offset=16
      local.set $l10
      local.get $p2
      f32.load offset=132
      local.set $l25
      local.get $p2
      f32.load offset=20
      local.set $l11
      local.get $p7
      local.get $p7
      i32.load16_u offset=12
      i32.const 1
      i32.or
      i32.store16 offset=12
      local.get $p7
      local.get $p6
      local.get $l22
      local.get $l10
      local.get $l24
      f32.mul
      local.get $l11
      local.get $l25
      f32.mul
      f32.add
      local.get $p9
      local.get $l23
      f32.mul
      f32.add
      f32.add
      f32.add
      f32.store offset=24
      local.get $p7
      local.get $l14
      local.get $l18
      local.get $l10
      local.get $l20
      f32.mul
      local.get $l11
      local.get $l21
      f32.mul
      f32.add
      local.get $p9
      local.get $l19
      f32.mul
      f32.add
      f32.add
      f32.add
      f32.store offset=20
      local.get $p7
      local.get $l13
      local.get $l15
      local.get $l10
      local.get $l16
      f32.mul
      local.get $l11
      local.get $l17
      f32.mul
      f32.add
      local.get $p9
      local.get $l12
      f32.mul
      f32.add
      f32.add
      f32.add
      f32.store offset=16
    end
    local.get $p2
    i32.const 176
    i32.add
    global.set $g0
    local.get $p4)
