  (func $f78120 (type $t2) (param $p0 i32) (param $p1 i32) (param $p2 i32)
    (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 f32) (local $l7 f32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 i64)
    global.get $g0
    i32.const -64
    i32.add
    local.tee $l3
    global.set $g0
    local.get $p2
    f32.load offset=12
    local.set $l6
    local.get $p2
    i32.load offset=8
    local.set $l4
    local.get $p2
    i32.load
    local.set $l5
    local.get $p2
    i32.load offset=4
    local.set $p2
    local.get $l3
    local.get $p1
    i64.load align=4
    local.tee $l29
    i64.store offset=8
    local.get $l3
    local.get $l29
    i64.store offset=16
    local.get $l3
    i32.const 24
    i32.add
    local.get $l3
    i32.const 8
    i32.add
    call $f78121
    local.get $l3
    f32.load offset=40
    local.set $l12
    local.get $l3
    f32.load offset=44
    local.set $l13
    local.get $l3
    f32.load offset=24
    local.set $l14
    local.get $l3
    f32.load offset=28
    local.set $l15
    local.get $l3
    f32.load offset=32
    local.set $l16
    local.get $l3
    f32.load offset=36
    local.set $l17
    local.get $p0
    local.get $l6
    local.get $p2
    i32.const -2147483648
    i32.xor
    f32.reinterpret_i32
    local.tee $l7
    f32.const -0x1p+1 (;=-2;)
    f32.mul
    local.tee $l27
    f32.mul
    local.get $l4
    i32.const -2147483648
    i32.xor
    f32.reinterpret_i32
    local.tee $l9
    local.get $l9
    f32.add
    local.tee $l10
    local.get $l5
    i32.const -2147483648
    i32.xor
    f32.reinterpret_i32
    local.tee $l8
    f32.mul
    f32.add
    f32.const 0x0p+0 (;=0;)
    f32.add
    local.tee $l20
    local.get $l3
    f32.load offset=48
    local.tee $l21
    f32.mul
    local.get $l6
    local.get $l8
    local.get $l8
    f32.add
    local.tee $l18
    f32.mul
    local.get $l10
    local.get $l7
    f32.mul
    f32.add
    f32.const 0x0p+0 (;=0;)
    f32.add
    local.tee $l22
    local.get $l3
    f32.load offset=52
    local.tee $l23
    f32.mul
    local.get $l8
    f32.const -0x1p+1 (;=-2;)
    f32.mul
    local.tee $l11
    local.get $l8
    f32.mul
    local.get $l7
    local.get $l7
    f32.add
    local.tee $l19
    local.get $l7
    f32.mul
    f32.sub
    f32.const 0x1p+0 (;=1;)
    f32.add
    local.tee $l24
    local.get $l3
    f32.load offset=56
    local.tee $l25
    f32.mul
    f32.add
    f32.add
    f32.store offset=32
    local.get $p0
    local.get $l21
    local.get $l19
    local.get $l8
    f32.mul
    local.get $l6
    local.get $l10
    f32.mul
    f32.add
    f32.const 0x0p+0 (;=0;)
    f32.add
    local.tee $l26
    f32.mul
    local.get $l23
    local.get $l9
    f32.const -0x1p+1 (;=-2;)
    f32.mul
    local.tee $l28
    local.get $l9
    f32.mul
    local.get $l18
    local.get $l8
    f32.mul
    f32.sub
    f32.const 0x1p+0 (;=1;)
    f32.add
    local.tee $l8
    f32.mul
    local.get $l25
    local.get $l6
    local.get $l11
    f32.mul
    local.get $l19
    local.get $l9
    f32.mul
    f32.add
    f32.const 0x0p+0 (;=0;)
    f32.add
    local.tee $l11
    f32.mul
    f32.add
    f32.add
    f32.store offset=28
    local.get $p0
    local.get $l21
    local.get $l27
    local.get $l7
    f32.mul
    local.get $l10
    local.get $l9
    f32.mul
    f32.sub
    f32.const 0x1p+0 (;=1;)
    f32.add
    local.tee $l10
    f32.mul
    local.get $l23
    local.get $l18
    local.get $l7
    f32.mul
    local.get $l6
    local.get $l28
    f32.mul
    f32.add
    f32.const 0x0p+0 (;=0;)
    f32.add
    local.tee $l7
    f32.mul
    local.get $l25
    local.get $l18
    local.get $l9
    f32.mul
    local.get $l6
    local.get $l19
    f32.mul
    f32.add
    f32.const 0x0p+0 (;=0;)
    f32.add
    local.tee $l6
    f32.mul
    f32.add
    f32.add
    f32.store offset=24
    local.get $p0
    local.get $l20
    local.get $l17
    f32.mul
    local.get $l22
    local.get $l12
    f32.mul
    local.get $l24
    local.get $l13
    f32.mul
    f32.add
    f32.add
    f32.store offset=20
    local.get $p0
    local.get $l26
    local.get $l17
    f32.mul
    local.get $l8
    local.get $l12
    f32.mul
    local.get $l11
    local.get $l13
    f32.mul
    f32.add
    f32.add
    f32.store offset=16
    local.get $p0
    local.get $l10
    local.get $l17
    f32.mul
    local.get $l7
    local.get $l12
    f32.mul
    local.get $l6
    local.get $l13
    f32.mul
    f32.add
    f32.add
    f32.store offset=12
    local.get $p0
    local.get $l20
    local.get $l14
    f32.mul
    local.get $l22
    local.get $l15
    f32.mul
    local.get $l24
    local.get $l16
    f32.mul
    f32.add
    f32.add
    f32.store offset=8
    local.get $p0
    local.get $l26
    local.get $l14
    f32.mul
    local.get $l8
    local.get $l15
    f32.mul
    local.get $l11
    local.get $l16
    f32.mul
    f32.add
    f32.add
    f32.store offset=4
    local.get $p0
    local.get $l10
    local.get $l14
    f32.mul
    local.get $l7
    local.get $l15
    f32.mul
    local.get $l6
    local.get $l16
    f32.mul
    f32.add
    f32.add
    f32.store
    local.get $l3
    i32.const -64
    i32.sub
    global.set $g0)
