  (func $f71092 (type $t2) (param $p0 i32) (param $p1 i32) (param $p2 i32)
    (local $l3 f32) (local $l4 f32) (local $l5 f32) (local $l6 f32) (local $l7 f32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32) (local $l33 f32) (local $l34 f32) (local $l35 f32)
    local.get $p2
    f32.load offset=100
    local.set $l26
    local.get $p2
    f32.load offset=104
    local.set $l27
    local.get $p2
    f32.load offset=112
    local.set $l28
    local.get $p2
    f32.load offset=116
    local.set $l29
    local.get $p2
    f32.load offset=120
    local.set $l30
    local.get $p2
    f32.load offset=128
    local.set $l31
    local.get $p2
    f32.load offset=132
    local.set $l32
    local.get $p2
    f32.load offset=136
    local.set $l33
    local.get $p2
    f32.load offset=52
    local.set $l18
    local.get $p2
    f32.load offset=56
    local.set $l19
    local.get $p2
    f32.load offset=68
    local.set $l20
    local.get $p2
    f32.load offset=72
    local.set $l21
    local.get $p2
    f32.load offset=84
    local.set $l14
    local.get $p2
    f32.load offset=88
    local.set $l15
    local.get $p2
    i32.const -64
    i32.sub
    f32.load
    local.set $l22
    local.get $p2
    f32.load offset=80
    local.set $l23
    local.get $p2
    f32.load offset=20
    local.set $l6
    local.get $p2
    f32.load offset=24
    local.set $l7
    local.get $p2
    f32.load offset=28
    local.set $l16
    local.get $p2
    f32.load offset=36
    local.set $l8
    local.get $p2
    f32.load offset=40
    local.set $l25
    local.get $p2
    f32.load offset=44
    local.set $l17
    local.get $p2
    f32.load offset=96
    local.set $l34
    local.get $p2
    f32.load offset=48
    local.set $l24
    local.get $p1
    f32.load offset=8
    local.set $l3
    local.get $p1
    f32.load
    local.set $l4
    local.get $p1
    f32.load offset=4
    local.set $l5
    local.get $p2
    f32.load
    local.set $l9
    local.get $p2
    f32.load offset=4
    local.set $l10
    local.get $p2
    f32.load offset=8
    local.set $l11
    local.get $p2
    f32.load offset=12
    local.set $l35
    local.get $p2
    f32.load offset=16
    local.set $l12
    local.get $p2
    f32.load offset=32
    local.set $l13
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
    i32.const 0
    i32.store offset=60
    local.get $p0
    local.get $l17
    f32.store offset=44
    local.get $p0
    local.get $l25
    f32.store offset=40
    local.get $p0
    local.get $l8
    f32.store offset=36
    local.get $p0
    local.get $l13
    f32.store offset=32
    local.get $p0
    local.get $l16
    f32.store offset=28
    local.get $p0
    local.get $l7
    f32.store offset=24
    local.get $p0
    local.get $l6
    f32.store offset=20
    local.get $p0
    local.get $l12
    f32.store offset=16
    local.get $p0
    local.get $l35
    f32.store offset=12
    local.get $p0
    local.get $l11
    f32.store offset=8
    local.get $p0
    local.get $l10
    f32.store offset=4
    local.get $p0
    local.get $l9
    f32.store
    local.get $p0
    local.get $l23
    local.get $l4
    local.get $l12
    f32.mul
    local.get $l5
    local.get $l9
    f32.mul
    f32.sub
    local.tee $l16
    f32.add
    f32.store offset=80
    local.get $p0
    i32.const -64
    i32.sub
    local.get $l22
    local.get $l3
    local.get $l9
    f32.mul
    local.get $l4
    local.get $l13
    f32.mul
    f32.sub
    local.tee $l9
    f32.add
    f32.store
    local.get $p0
    local.get $l24
    local.get $l5
    local.get $l13
    f32.mul
    local.get $l3
    local.get $l12
    f32.mul
    f32.sub
    local.tee $l12
    f32.add
    f32.store offset=48
    local.get $p0
    local.get $l15
    local.get $l4
    local.get $l7
    f32.mul
    local.get $l5
    local.get $l11
    f32.mul
    f32.sub
    local.tee $l13
    f32.add
    f32.store offset=88
    local.get $p0
    local.get $l14
    local.get $l4
    local.get $l6
    f32.mul
    local.get $l5
    local.get $l10
    f32.mul
    f32.sub
    local.tee $l17
    f32.add
    f32.store offset=84
    local.get $p0
    local.get $l21
    local.get $l3
    local.get $l11
    f32.mul
    local.get $l4
    local.get $l25
    f32.mul
    f32.sub
    local.tee $l11
    f32.add
    f32.store offset=72
    local.get $p0
    local.get $l20
    local.get $l3
    local.get $l10
    f32.mul
    local.get $l4
    local.get $l8
    f32.mul
    f32.sub
    local.tee $l10
    f32.add
    f32.store offset=68
    local.get $p0
    local.get $l19
    local.get $l5
    local.get $l25
    f32.mul
    local.get $l3
    local.get $l7
    f32.mul
    f32.sub
    local.tee $l7
    f32.add
    f32.store offset=56
    local.get $p0
    local.get $l18
    local.get $l5
    local.get $l8
    f32.mul
    local.get $l3
    local.get $l6
    f32.mul
    f32.sub
    local.tee $l6
    f32.add
    f32.store offset=52
    local.get $p0
    local.get $l33
    local.get $l4
    local.get $l14
    f32.mul
    local.get $l15
    f32.const 0x0p+0 (;=0;)
    f32.mul
    f32.add
    local.get $l5
    local.get $l23
    f32.mul
    f32.sub
    local.get $l13
    f32.const 0x0p+0 (;=0;)
    f32.mul
    local.get $l4
    local.get $l17
    f32.mul
    local.get $l5
    local.get $l16
    f32.mul
    f32.sub
    f32.add
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.add
    local.tee $l8
    local.get $l8
    f32.add
    f32.add
    f32.store offset=136
    local.get $p0
    local.get $l32
    local.get $l3
    local.get $l23
    f32.mul
    local.get $l14
    f32.const 0x0p+0 (;=0;)
    f32.mul
    local.get $l4
    local.get $l15
    f32.mul
    f32.sub
    f32.add
    local.get $l3
    local.get $l16
    f32.mul
    local.get $l17
    f32.const 0x0p+0 (;=0;)
    f32.mul
    f32.add
    local.get $l4
    local.get $l13
    f32.mul
    f32.sub
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.add
    local.get $l4
    local.get $l20
    f32.mul
    local.get $l21
    f32.const 0x0p+0 (;=0;)
    f32.mul
    f32.add
    local.get $l5
    local.get $l22
    f32.mul
    f32.sub
    local.get $l11
    f32.const 0x0p+0 (;=0;)
    f32.mul
    local.get $l4
    local.get $l10
    f32.mul
    local.get $l5
    local.get $l9
    f32.mul
    f32.sub
    f32.add
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.add
    f32.add
    local.tee $l8
    f32.add
    f32.store offset=132
    local.get $p0
    local.get $l31
    local.get $l23
    f32.const 0x0p+0 (;=0;)
    f32.mul
    local.get $l5
    local.get $l15
    f32.mul
    local.get $l3
    local.get $l14
    f32.mul
    f32.sub
    f32.add
    local.get $l5
    local.get $l13
    f32.mul
    local.get $l16
    f32.const 0x0p+0 (;=0;)
    f32.mul
    local.get $l3
    local.get $l17
    f32.mul
    f32.sub
    f32.add
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.add
    local.get $l4
    local.get $l18
    f32.mul
    local.get $l19
    f32.const 0x0p+0 (;=0;)
    f32.mul
    f32.add
    local.get $l5
    local.get $l24
    f32.mul
    f32.sub
    local.get $l7
    f32.const 0x0p+0 (;=0;)
    f32.mul
    local.get $l4
    local.get $l6
    f32.mul
    local.get $l5
    local.get $l12
    f32.mul
    f32.sub
    f32.add
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.add
    f32.add
    local.tee $l14
    f32.add
    f32.store offset=128
    local.get $p0
    local.get $l30
    local.get $l8
    f32.add
    f32.store offset=120
    local.get $p0
    local.get $l29
    local.get $l3
    local.get $l22
    f32.mul
    local.get $l20
    f32.const 0x0p+0 (;=0;)
    f32.mul
    local.get $l4
    local.get $l21
    f32.mul
    f32.sub
    f32.add
    local.get $l3
    local.get $l9
    f32.mul
    local.get $l10
    f32.const 0x0p+0 (;=0;)
    f32.mul
    f32.add
    local.get $l4
    local.get $l11
    f32.mul
    f32.sub
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.add
    local.tee $l15
    local.get $l15
    f32.add
    f32.add
    f32.store offset=116
    local.get $p0
    local.get $l28
    local.get $l3
    local.get $l24
    f32.mul
    local.get $l18
    f32.const 0x0p+0 (;=0;)
    f32.mul
    local.get $l4
    local.get $l19
    f32.mul
    f32.sub
    f32.add
    local.get $l3
    local.get $l12
    f32.mul
    local.get $l6
    f32.const 0x0p+0 (;=0;)
    f32.mul
    f32.add
    local.get $l4
    local.get $l7
    f32.mul
    f32.sub
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.add
    local.get $l22
    f32.const 0x0p+0 (;=0;)
    f32.mul
    local.get $l5
    local.get $l21
    f32.mul
    local.get $l3
    local.get $l20
    f32.mul
    f32.sub
    f32.add
    local.get $l5
    local.get $l11
    f32.mul
    local.get $l9
    f32.const 0x0p+0 (;=0;)
    f32.mul
    local.get $l3
    local.get $l10
    f32.mul
    f32.sub
    f32.add
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.add
    f32.add
    local.tee $l4
    f32.add
    f32.store offset=112
    local.get $p0
    local.get $l27
    local.get $l14
    f32.add
    f32.store offset=104
    local.get $p0
    local.get $l26
    local.get $l4
    f32.add
    f32.store offset=100
    local.get $p0
    local.get $l34
    local.get $l24
    f32.const 0x0p+0 (;=0;)
    f32.mul
    local.get $l5
    local.get $l19
    f32.mul
    local.get $l3
    local.get $l18
    f32.mul
    f32.sub
    f32.add
    local.get $l5
    local.get $l7
    f32.mul
    local.get $l12
    f32.const 0x0p+0 (;=0;)
    f32.mul
    local.get $l3
    local.get $l6
    f32.mul
    f32.sub
    f32.add
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.add
    local.tee $l3
    local.get $l3
    f32.add
    f32.add
    f32.store offset=96)
