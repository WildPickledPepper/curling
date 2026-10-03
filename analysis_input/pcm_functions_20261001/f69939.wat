  (func $f69939 (type $t168) (param $p0 i32) (param $p1 i32) (param $p2 f32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 i32)
    (local $l7 f32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32) (local $l33 f32) (local $l34 f32) (local $l35 f32) (local $l36 f32) (local $l37 f32) (local $l38 f32) (local $l39 f32) (local $l40 i32) (local $l41 i32)
    local.get $p4
    f32.load offset=40
    local.set $l29
    local.get $p3
    f32.load offset=40
    local.set $l30
    local.get $p4
    f32.load offset=44
    local.set $l31
    local.get $p3
    f32.load offset=44
    local.set $l32
    local.get $p3
    f32.load offset=16
    local.set $l7
    local.get $p3
    f32.load offset=20
    local.set $l11
    local.get $p4
    f32.load offset=16
    local.set $l17
    local.get $p4
    f32.load offset=20
    local.set $l18
    local.get $p3
    f32.load offset=28
    local.set $l12
    local.get $p4
    f32.load offset=28
    local.set $l8
    local.get $p3
    f32.load offset=32
    local.set $l13
    local.get $p4
    f32.load offset=32
    local.set $l9
    local.get $p1
    i32.const 16
    i32.add
    local.tee $l40
    f32.load
    local.set $l23
    local.get $p1
    i32.const 20
    i32.add
    local.tee $l41
    f32.load
    local.set $l24
    local.get $p4
    f32.load offset=36
    local.set $l33
    local.get $p3
    f32.load offset=36
    local.set $l34
    local.get $p3
    f32.load offset=8
    local.set $l14
    local.get $p3
    f32.load offset=4
    local.set $l25
    local.get $p3
    f32.load
    local.set $l26
    local.get $p3
    f32.load offset=12
    local.set $l15
    local.get $p4
    f32.load offset=8
    local.set $l19
    local.get $p4
    f32.load offset=4
    local.set $l20
    local.get $p4
    f32.load
    local.set $l21
    local.get $p4
    f32.load offset=12
    local.set $l22
    local.get $p3
    f32.load offset=24
    local.set $l16
    local.get $p4
    f32.load offset=24
    local.set $l10
    local.get $p1
    f32.load offset=4
    local.set $l27
    local.get $p1
    f32.load offset=8
    local.set $l28
    local.get $p0
    local.get $p1
    f32.load offset=12
    local.get $p1
    f32.load
    f32.sub
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    local.get $p2
    f32.add
    f32.store offset=48
    local.get $p0
    local.get $l24
    local.get $l28
    f32.sub
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    local.get $p2
    f32.add
    f32.store offset=56
    local.get $p0
    local.get $l23
    local.get $l27
    f32.sub
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    local.get $p2
    f32.add
    f32.store offset=52
    local.get $l40
    f32.load
    local.set $l23
    local.get $l41
    f32.load
    local.set $l24
    local.get $p1
    f32.load offset=12
    local.set $l27
    local.get $p1
    f32.load
    local.set $l28
    local.get $p1
    f32.load offset=4
    local.set $l35
    local.get $p1
    f32.load offset=8
    local.set $l36
    local.get $p0
    local.get $l10
    local.get $l16
    f32.mul
    local.get $l8
    local.get $l12
    f32.mul
    f32.add
    local.get $l9
    local.get $l13
    f32.mul
    f32.add
    local.tee $l37
    f32.store offset=32
    local.get $p0
    local.get $l22
    local.get $l16
    f32.mul
    local.get $l17
    local.get $l12
    f32.mul
    f32.add
    local.get $l18
    local.get $l13
    f32.mul
    f32.add
    local.tee $l38
    f32.store offset=28
    local.get $p0
    local.get $l21
    local.get $l16
    f32.mul
    local.get $l20
    local.get $l12
    f32.mul
    f32.add
    local.get $l19
    local.get $l13
    f32.mul
    f32.add
    local.tee $l12
    f32.store offset=24
    local.get $p0
    local.get $l10
    local.get $l15
    f32.mul
    local.get $l8
    local.get $l7
    f32.mul
    f32.add
    local.get $l9
    local.get $l11
    f32.mul
    f32.add
    local.tee $l13
    f32.store offset=20
    local.get $p0
    local.get $l22
    local.get $l15
    f32.mul
    local.get $l17
    local.get $l7
    f32.mul
    f32.add
    local.get $l18
    local.get $l11
    f32.mul
    f32.add
    local.tee $l16
    f32.store offset=16
    local.get $p0
    local.get $l21
    local.get $l15
    f32.mul
    local.get $l20
    local.get $l7
    f32.mul
    f32.add
    local.get $l19
    local.get $l11
    f32.mul
    f32.add
    local.tee $l15
    f32.store offset=12
    local.get $p0
    local.get $l26
    local.get $l10
    f32.mul
    local.get $l25
    local.get $l8
    f32.mul
    f32.add
    local.get $l14
    local.get $l9
    f32.mul
    f32.add
    local.tee $l7
    f32.store offset=8
    local.get $p0
    local.get $l26
    local.get $l22
    f32.mul
    local.get $l25
    local.get $l17
    f32.mul
    f32.add
    local.get $l14
    local.get $l18
    f32.mul
    f32.add
    local.tee $l39
    f32.store offset=4
    local.get $p0
    local.get $l21
    local.get $l26
    f32.mul
    local.get $l20
    local.get $l25
    f32.mul
    f32.add
    local.get $l19
    local.get $l14
    f32.mul
    f32.add
    local.tee $l14
    f32.store
    local.get $p0
    local.get $l10
    local.get $l34
    local.get $l33
    f32.sub
    local.tee $p2
    f32.mul
    local.get $l8
    local.get $l30
    local.get $l29
    f32.sub
    local.tee $l10
    f32.mul
    f32.add
    local.get $l9
    local.get $l32
    local.get $l31
    f32.sub
    local.tee $l8
    f32.mul
    f32.add
    local.get $l7
    local.get $l28
    local.get $l27
    f32.add
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    local.tee $l9
    f32.mul
    local.get $l13
    local.get $l35
    local.get $l23
    f32.add
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    local.tee $l7
    f32.mul
    f32.add
    local.get $l37
    local.get $l36
    local.get $l24
    f32.add
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    local.tee $l11
    f32.mul
    f32.add
    f32.add
    f32.store offset=44
    local.get $p0
    local.get $l22
    local.get $p2
    f32.mul
    local.get $l17
    local.get $l10
    f32.mul
    f32.add
    local.get $l18
    local.get $l8
    f32.mul
    f32.add
    local.get $l39
    local.get $l9
    f32.mul
    local.get $l16
    local.get $l7
    f32.mul
    f32.add
    local.get $l38
    local.get $l11
    f32.mul
    f32.add
    f32.add
    f32.store offset=40
    local.get $p0
    local.get $l21
    local.get $p2
    f32.mul
    local.get $l20
    local.get $l10
    f32.mul
    f32.add
    local.get $l19
    local.get $l8
    f32.mul
    f32.add
    local.get $l14
    local.get $l9
    f32.mul
    local.get $l15
    local.get $l7
    f32.mul
    f32.add
    local.get $l12
    local.get $l11
    f32.mul
    f32.add
    f32.add
    f32.store offset=36
    local.get $p6
    i32.eqz
    if $I0
      local.get $p5
      local.get $p0
      i32.const 36
      i32.add
      local.get $p0
      i32.const 48
      i32.add
      local.get $p0
      call $f70179
    end)
