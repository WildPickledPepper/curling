  (func $f71850 (type $t8) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (result i32)
    (local $l4 f32) (local $l5 f32) (local $l6 f32) (local $l7 f32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 i64)
    local.get $p1
    i64.load align=4
    local.set $l17
    local.get $p1
    f32.load offset=8
    local.set $l5
    local.get $p0
    i32.const 0
    i32.store offset=28
    local.get $p0
    local.get $l5
    f32.store offset=24
    local.get $p0
    local.get $l17
    i64.store offset=16
    local.get $p3
    f32.load
    local.set $l5
    local.get $p3
    f32.load offset=4
    local.set $l6
    local.get $p3
    f32.load offset=8
    local.set $l7
    local.get $p0
    i32.const 0
    i32.store offset=12
    local.get $p0
    local.get $l7
    f32.store offset=8
    local.get $p0
    local.get $l6
    f32.store offset=4
    local.get $p0
    local.get $l5
    f32.store
    local.get $p2
    f32.load offset=16
    local.set $l8
    local.get $p2
    f32.load offset=28
    local.set $l9
    local.get $p2
    f32.load offset=20
    local.set $l10
    local.get $p2
    f32.load offset=32
    local.set $l11
    local.get $p2
    f32.load
    local.set $l12
    local.get $p2
    f32.load offset=12
    local.set $l13
    local.get $p2
    f32.load offset=24
    local.set $l14
    local.get $p2
    f32.load offset=4
    local.set $l15
    local.get $p2
    f32.load offset=8
    local.set $l16
    local.get $p0
    i32.const 0
    i32.store offset=188
    local.get $p0
    i32.const 0
    i32.store offset=172
    local.get $p0
    i32.const 0
    i32.store offset=156
    local.get $p0
    i32.const 0
    i32.store offset=140
    local.get $p0
    i32.const 0
    i32.store offset=124
    local.get $p0
    i32.const 0
    i32.store offset=108
    local.get $p0
    i32.const 0
    i32.store offset=92
    local.get $p0
    i32.const 0
    i32.store offset=76
    local.get $p0
    local.get $l11
    f32.store offset=72
    local.get $p0
    local.get $l10
    f32.store offset=68
    local.get $p0
    i32.const -64
    i32.sub
    local.get $l16
    f32.store
    local.get $p0
    i32.const 0
    i32.store offset=60
    local.get $p0
    local.get $l9
    f32.store offset=56
    local.get $p0
    local.get $l8
    f32.store offset=52
    local.get $p0
    local.get $l15
    f32.store offset=48
    local.get $p0
    i32.const 0
    i32.store offset=44
    local.get $p0
    local.get $l14
    f32.store offset=40
    local.get $p0
    local.get $l13
    f32.store offset=36
    local.get $p0
    local.get $l12
    f32.store offset=32
    local.get $p0
    local.get $l11
    local.get $l11
    f32.neg
    local.tee $l4
    local.get $l4
    local.get $l11
    f32.lt
    select
    f32.const 0x1.0c6f7ap-20 (;=1e-06;)
    f32.add
    local.tee $l11
    f32.store offset=120
    local.get $p0
    local.get $l10
    local.get $l10
    f32.neg
    local.tee $l4
    local.get $l4
    local.get $l10
    f32.lt
    select
    f32.const 0x1.0c6f7ap-20 (;=1e-06;)
    f32.add
    local.tee $l10
    f32.store offset=116
    local.get $p0
    local.get $l16
    local.get $l16
    f32.neg
    local.tee $l4
    local.get $l4
    local.get $l16
    f32.lt
    select
    f32.const 0x1.0c6f7ap-20 (;=1e-06;)
    f32.add
    local.tee $l16
    f32.store offset=112
    local.get $p0
    local.get $l9
    local.get $l9
    f32.neg
    local.tee $l4
    local.get $l4
    local.get $l9
    f32.lt
    select
    f32.const 0x1.0c6f7ap-20 (;=1e-06;)
    f32.add
    local.tee $l9
    f32.store offset=104
    local.get $p0
    local.get $l8
    local.get $l8
    f32.neg
    local.tee $l4
    local.get $l4
    local.get $l8
    f32.lt
    select
    f32.const 0x1.0c6f7ap-20 (;=1e-06;)
    f32.add
    local.tee $l8
    f32.store offset=100
    local.get $p0
    local.get $l15
    local.get $l15
    f32.neg
    local.tee $l4
    local.get $l4
    local.get $l15
    f32.lt
    select
    f32.const 0x1.0c6f7ap-20 (;=1e-06;)
    f32.add
    local.tee $l15
    f32.store offset=96
    local.get $p0
    local.get $l14
    local.get $l14
    f32.neg
    local.tee $l4
    local.get $l4
    local.get $l14
    f32.lt
    select
    f32.const 0x1.0c6f7ap-20 (;=1e-06;)
    f32.add
    local.tee $l14
    f32.store offset=88
    local.get $p0
    local.get $l13
    local.get $l13
    f32.neg
    local.tee $l4
    local.get $l4
    local.get $l13
    f32.lt
    select
    f32.const 0x1.0c6f7ap-20 (;=1e-06;)
    f32.add
    local.tee $l13
    f32.store offset=84
    local.get $p0
    local.get $l12
    local.get $l12
    f32.neg
    local.tee $l4
    local.get $l4
    local.get $l12
    f32.lt
    select
    f32.const 0x1.0c6f7ap-20 (;=1e-06;)
    f32.add
    local.tee $l12
    f32.store offset=80
    local.get $p0
    local.get $l6
    local.get $l16
    f32.mul
    local.get $l5
    local.get $l10
    f32.mul
    f32.add
    f32.store offset=184
    local.get $p0
    local.get $l7
    local.get $l16
    f32.mul
    local.get $l5
    local.get $l11
    f32.mul
    f32.add
    f32.store offset=180
    local.get $p0
    local.get $l7
    local.get $l10
    f32.mul
    local.get $l6
    local.get $l11
    f32.mul
    f32.add
    f32.store offset=176
    local.get $p0
    local.get $l6
    local.get $l15
    f32.mul
    local.get $l5
    local.get $l8
    f32.mul
    f32.add
    f32.store offset=168
    local.get $p0
    local.get $l7
    local.get $l15
    f32.mul
    local.get $l5
    local.get $l9
    f32.mul
    f32.add
    f32.store offset=164
    local.get $p0
    local.get $l7
    local.get $l8
    f32.mul
    local.get $l6
    local.get $l9
    f32.mul
    f32.add
    f32.store offset=160
    local.get $p0
    local.get $l6
    local.get $l12
    f32.mul
    local.get $l5
    local.get $l13
    f32.mul
    f32.add
    f32.store offset=152
    local.get $p0
    local.get $l7
    local.get $l12
    f32.mul
    local.get $l5
    local.get $l14
    f32.mul
    f32.add
    f32.store offset=148
    local.get $p0
    local.get $l7
    local.get $l13
    f32.mul
    local.get $l6
    local.get $l14
    f32.mul
    f32.add
    f32.store offset=144
    local.get $p0
    local.get $l5
    local.get $l16
    f32.mul
    local.get $l6
    local.get $l10
    f32.mul
    f32.add
    local.get $l7
    local.get $l11
    f32.mul
    f32.add
    f32.store offset=136
    local.get $p0
    local.get $l5
    local.get $l15
    f32.mul
    local.get $l6
    local.get $l8
    f32.mul
    f32.add
    local.get $l7
    local.get $l9
    f32.mul
    f32.add
    f32.store offset=132
    local.get $p0
    local.get $l5
    local.get $l12
    f32.mul
    local.get $l6
    local.get $l13
    f32.mul
    f32.add
    local.get $l7
    local.get $l14
    f32.mul
    f32.add
    f32.store offset=128
    local.get $p0)
