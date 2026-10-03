  (func $f71114 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32)
    global.get $g0
    i32.const 160
    i32.sub
    local.tee $l2
    global.set $g0
    local.get $p1
    i32.load offset=12
    local.set $l5
    local.get $p0
    i32.load offset=332
    local.set $l7
    local.get $p0
    i32.load offset=336
    local.set $l4
    local.get $p0
    local.get $p1
    i32.load offset=20
    local.tee $l6
    call $f71113
    local.get $l4
    i32.const 1
    i32.sub
    local.tee $l4
    if $I0
      loop $L1
        local.get $l2
        local.get $l6
        local.get $l4
        i32.const 112
        i32.mul
        i32.add
        local.tee $p1
        f32.load
        f32.store offset=48
        local.get $l2
        local.get $p1
        f32.load offset=4
        f32.store offset=52
        local.get $l2
        local.get $p1
        f32.load offset=8
        f32.store offset=56
        local.get $l2
        local.get $p1
        f32.load offset=12
        f32.store offset=60
        local.get $l2
        local.get $p1
        f32.load offset=16
        f32.store offset=64
        local.get $l2
        local.get $p1
        f32.load offset=20
        f32.store offset=68
        local.get $l2
        local.get $p1
        f32.load offset=24
        f32.store offset=72
        local.get $l2
        local.get $p1
        f32.load offset=28
        f32.store offset=76
        local.get $l2
        local.get $p1
        f32.load offset=32
        f32.store offset=80
        local.get $l2
        local.get $p1
        f32.load offset=36
        f32.store offset=84
        local.get $l2
        local.get $p1
        f32.load offset=40
        f32.store offset=88
        local.get $l2
        local.get $p1
        f32.load offset=44
        f32.store offset=92
        local.get $l2
        local.get $p1
        f32.load offset=48
        f32.store offset=96
        local.get $l2
        local.get $p1
        f32.load offset=52
        f32.store offset=100
        local.get $l2
        local.get $p1
        f32.load offset=56
        f32.store offset=104
        local.get $l2
        local.get $p1
        f32.load offset=60
        f32.store offset=108
        local.get $l2
        local.get $p1
        i32.const -64
        i32.sub
        f32.load
        f32.store offset=112
        local.get $l2
        local.get $p1
        f32.load offset=68
        f32.store offset=116
        local.get $l2
        local.get $p1
        f32.load offset=72
        f32.store offset=120
        local.get $l2
        local.get $p1
        f32.load offset=76
        f32.store offset=124
        local.get $l2
        local.get $p1
        f32.load offset=80
        f32.store offset=128
        local.get $l2
        local.get $p1
        f32.load offset=84
        f32.store offset=132
        local.get $l2
        local.get $p1
        f32.load offset=88
        f32.store offset=136
        local.get $l2
        local.get $p1
        f32.load offset=92
        f32.store offset=140
        local.get $l2
        local.get $p1
        f32.load offset=96
        f32.store offset=144
        local.get $l2
        local.get $p1
        f32.load offset=100
        f32.store offset=148
        local.get $l2
        local.get $p1
        f32.load offset=104
        f32.store offset=152
        local.get $l2
        local.get $p1
        i32.load offset=108
        i32.store offset=156
        local.get $p0
        i32.load offset=340
        local.get $l4
        i32.const 160
        i32.mul
        i32.add
        local.tee $p1
        f32.load offset=128
        local.set $l9
        local.get $p1
        f32.load offset=124
        local.set $l10
        local.get $p1
        f32.load offset=120
        local.set $l11
        local.get $l2
        i32.const 0
        i32.store offset=40
        local.get $l2
        local.get $l11
        f32.neg
        f32.store offset=36
        local.get $l2
        local.get $l10
        f32.store offset=32
        local.get $l2
        local.get $l11
        f32.store offset=28
        local.get $l2
        i32.const 0
        i32.store offset=24
        local.get $l2
        local.get $l9
        f32.store offset=12
        local.get $l2
        i32.const 0
        i32.store offset=8
        local.get $l2
        local.get $l9
        f32.neg
        f32.store offset=20
        local.get $l2
        local.get $l10
        f32.neg
        f32.store offset=16
        local.get $l2
        i32.const 8
        i32.add
        local.get $l2
        i32.const 48
        i32.add
        call $f70988
        local.get $l6
        local.get $l7
        local.get $l4
        i32.const 80
        i32.mul
        i32.add
        local.tee $l8
        i32.load offset=72
        i32.const 112
        i32.mul
        i32.add
        local.tee $p1
        local.get $l2
        f32.load offset=48
        local.get $p1
        f32.load
        f32.add
        f32.store
        local.get $p1
        local.get $l2
        f32.load offset=52
        local.get $p1
        f32.load offset=4
        f32.add
        f32.store offset=4
        local.get $p1
        local.get $l2
        f32.load offset=56
        local.get $p1
        f32.load offset=8
        f32.add
        f32.store offset=8
        local.get $p1
        local.get $l2
        f32.load offset=60
        local.get $p1
        f32.load offset=12
        f32.add
        f32.store offset=12
        local.get $p1
        i32.const 16
        i32.add
        local.tee $l3
        local.get $l2
        f32.load offset=64
        local.get $l3
        f32.load
        f32.add
        f32.store
        local.get $p1
        i32.const 20
        i32.add
        local.tee $l3
        local.get $l2
        f32.load offset=68
        local.get $l3
        f32.load
        f32.add
        f32.store
        local.get $p1
        local.get $l2
        f32.load offset=72
        local.get $p1
        f32.load offset=24
        f32.add
        f32.store offset=24
        local.get $p1
        i32.const 28
        i32.add
        local.tee $l3
        local.get $l2
        f32.load offset=76
        local.get $l3
        f32.load
        f32.add
        f32.store
        local.get $p1
        i32.const 32
        i32.add
        local.tee $l3
        local.get $l2
        f32.load offset=80
        local.get $l3
        f32.load
        f32.add
        f32.store
        local.get $p1
        local.get $l2
        f32.load offset=84
        local.get $p1
        f32.load offset=36
        f32.add
        f32.store offset=36
        local.get $p1
        i32.const 40
        i32.add
        local.tee $l3
        local.get $l2
        f32.load offset=88
        local.get $l3
        f32.load
        f32.add
        f32.store
        local.get $p1
        i32.const 44
        i32.add
        local.tee $l3
        local.get $l2
        f32.load offset=92
        local.get $l3
        f32.load
        f32.add
        f32.store
        local.get $p1
        i32.const 48
        i32.add
        local.tee $l3
        local.get $l2
        f32.load offset=96
        local.get $l3
        f32.load
        f32.add
        f32.store
        local.get $p1
        i32.const 52
        i32.add
        local.tee $l3
        local.get $l2
        f32.load offset=100
        local.get $l3
        f32.load
        f32.add
        f32.store
        local.get $p1
        i32.const 56
        i32.add
        local.tee $l3
        local.get $l2
        f32.load offset=104
        local.get $l3
        f32.load
        f32.add
        f32.store
        local.get $p1
        i32.const 60
        i32.add
        local.tee $l3
        local.get $l2
        f32.load offset=108
        local.get $l3
        f32.load
        f32.add
        f32.store
        local.get $p1
        i32.const -64
        i32.sub
        local.tee $l3
        local.get $l2
        f32.load offset=112
        local.get $l3
        f32.load
        f32.add
        f32.store
        local.get $p1
        i32.const 68
        i32.add
        local.tee $l3
        local.get $l2
        f32.load offset=116
        local.get $l3
        f32.load
        f32.add
        f32.store
        local.get $p1
        local.get $l2
        f32.load offset=120
        local.get $p1
        f32.load offset=72
        f32.add
        f32.store offset=72
        local.get $p1
        i32.const 76
        i32.add
        local.tee $l3
        local.get $l2
        f32.load offset=124
        local.get $l3
        f32.load
        f32.add
        f32.store
        local.get $p1
        i32.const 80
        i32.add
        local.tee $l3
        local.get $l2
        f32.load offset=128
        local.get $l3
        f32.load
        f32.add
        f32.store
        local.get $p1
        i32.const 84
        i32.add
        local.tee $l3
        local.get $l2
        f32.load offset=132
        local.get $l3
        f32.load
        f32.add
        f32.store
        local.get $p1
        i32.const 88
        i32.add
        local.tee $l3
        local.get $l2
        f32.load offset=136
        local.get $l3
        f32.load
        f32.add
        f32.store
        local.get $p1
        i32.const 92
        i32.add
        local.tee $l3
        local.get $l2
        f32.load offset=140
        local.get $l3
        f32.load
        f32.add
        f32.store
        local.get $p1
        i32.const 96
        i32.add
        local.tee $l3
        local.get $l2
        f32.load offset=144
        local.get $l3
        f32.load
        f32.add
        f32.store
        local.get $p1
        i32.const 100
        i32.add
        local.tee $l3
        local.get $l2
        f32.load offset=148
        local.get $l3
        f32.load
        f32.add
        f32.store
        local.get $p1
        i32.const 104
        i32.add
        local.tee $p1
        local.get $l2
        f32.load offset=152
        local.get $p1
        f32.load
        f32.add
        f32.store
        local.get $p0
        local.get $l4
        call $f70976
        local.set $p1
        local.get $l5
        local.get $l4
        i32.const 5
        i32.shl
        i32.add
        local.tee $l3
        f32.load offset=24
        local.set $l15
        local.get $l3
        f32.load offset=20
        local.set $l16
        local.get $p1
        f32.load offset=120
        local.set $l11
        local.get $l3
        f32.load offset=16
        local.set $l17
        local.get $p1
        f32.load offset=124
        local.set $l12
        local.get $p1
        f32.load offset=128
        local.set $l13
        local.get $l3
        f32.load offset=8
        local.set $l9
        local.get $l3
        f32.load offset=4
        local.set $l10
        local.get $l5
        local.get $l8
        i32.load offset=72
        i32.const 5
        i32.shl
        i32.add
        local.tee $p1
        local.get $l3
        f32.load
        local.tee $l14
        local.get $p1
        f32.load
        f32.add
        f32.store
        local.get $p1
        local.get $l10
        local.get $p1
        f32.load offset=4
        f32.add
        f32.store offset=4
        local.get $p1
        local.get $l9
        local.get $p1
        f32.load offset=8
        f32.add
        f32.store offset=8
        local.get $p1
        local.get $l17
        local.get $l12
        local.get $l9
        f32.mul
        local.get $l13
        local.get $l10
        f32.mul
        f32.sub
        f32.add
        local.get $p1
        f32.load offset=16
        f32.add
        f32.store offset=16
        local.get $p1
        i32.const 20
        i32.add
        local.tee $l3
        local.get $l16
        local.get $l13
        local.get $l14
        f32.mul
        local.get $l9
        local.get $l11
        f32.mul
        f32.sub
        f32.add
        local.get $l3
        f32.load
        f32.add
        f32.store
        local.get $p1
        i32.const 24
        i32.add
        local.tee $p1
        local.get $l15
        local.get $l10
        local.get $l11
        f32.mul
        local.get $l12
        local.get $l14
        f32.mul
        f32.sub
        f32.add
        local.get $p1
        f32.load
        f32.add
        f32.store
        local.get $l4
        i32.const 1
        i32.sub
        local.tee $l4
        br_if $L1
      end
    end
    local.get $l2
    i32.const 160
    i32.add
    global.set $g0)
