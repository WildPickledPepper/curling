  (func $f69905 (type $t15) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 i32)
    (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32) (local $l33 f32) (local $l34 f32) (local $l35 f32) (local $l36 f32) (local $l37 f32) (local $l38 f32) (local $l39 f32)
    global.get $g0
    i32.const 144
    i32.sub
    local.tee $l7
    global.set $g0
    block $B0
      local.get $p1
      f32.load offset=56
      local.tee $l34
      local.get $p1
      f32.load offset=8
      local.tee $l19
      f32.sub
      local.tee $l18
      local.get $p1
      f32.load offset=16
      local.tee $l25
      local.get $p1
      f32.load
      local.tee $l20
      f32.sub
      local.tee $l22
      local.get $p1
      f32.load offset=36
      local.tee $l35
      local.get $p1
      f32.load offset=4
      local.tee $l21
      f32.sub
      local.tee $l23
      f32.mul
      local.get $p1
      f32.load offset=20
      local.tee $l26
      local.get $l21
      f32.sub
      local.tee $l24
      local.get $p1
      f32.load offset=32
      local.tee $l36
      local.get $l20
      f32.sub
      local.tee $l31
      f32.mul
      f32.sub
      local.tee $l15
      f32.const 0x1p+0 (;=1;)
      local.get $l15
      local.get $l15
      f32.mul
      local.get $l24
      local.get $p1
      f32.load offset=40
      local.tee $l37
      local.get $l19
      f32.sub
      local.tee $l32
      f32.mul
      local.get $p1
      f32.load offset=24
      local.tee $l27
      local.get $l19
      f32.sub
      local.tee $l33
      local.get $l23
      f32.mul
      f32.sub
      local.tee $l16
      local.get $l16
      f32.mul
      local.get $l33
      local.get $l31
      f32.mul
      local.get $l22
      local.get $l32
      f32.mul
      f32.sub
      local.tee $l17
      local.get $l17
      f32.mul
      f32.add
      f32.add
      f32.sqrt
      f32.div
      local.tee $l28
      f32.mul
      f32.mul
      local.get $p1
      f32.load offset=48
      local.tee $l38
      local.get $l20
      f32.sub
      local.tee $l29
      local.get $l16
      local.get $l28
      f32.mul
      f32.mul
      local.get $p1
      f32.load offset=52
      local.tee $l39
      local.get $l21
      f32.sub
      local.tee $l30
      local.get $l17
      local.get $l28
      f32.mul
      f32.mul
      f32.add
      f32.add
      f32.abs
      f32.const 0x1.a36e2ep-14 (;=0.0001;)
      f32.lt
      if $I1
        local.get $p6
        i32.const 3
        i32.store
        local.get $p0
        local.get $p1
        local.get $p2
        local.get $p3
        local.get $p4
        local.get $p5
        local.get $p6
        call $f70518
        br $B0
      end
      local.get $l7
      i32.const -1
      i32.const 0
      local.get $l19
      local.get $l15
      f32.mul
      local.get $l20
      local.get $l16
      f32.mul
      local.get $l21
      local.get $l17
      f32.mul
      f32.add
      f32.add
      local.get $l15
      local.get $l34
      f32.mul
      local.get $l38
      local.get $l16
      f32.mul
      local.get $l39
      local.get $l17
      f32.mul
      f32.add
      f32.add
      f32.mul
      local.tee $l28
      f32.const 0x0p+0 (;=0;)
      f32.ge
      select
      i32.store offset=128
      local.get $l7
      i32.const -1
      i32.const 0
      local.get $l19
      local.get $l24
      local.get $l29
      f32.mul
      local.get $l22
      local.get $l30
      f32.mul
      f32.sub
      local.tee $l15
      f32.mul
      local.get $l20
      local.get $l33
      local.get $l30
      f32.mul
      local.get $l24
      local.get $l18
      f32.mul
      f32.sub
      local.tee $l16
      f32.mul
      local.get $l21
      local.get $l22
      local.get $l18
      f32.mul
      local.get $l33
      local.get $l29
      f32.mul
      f32.sub
      local.tee $l17
      f32.mul
      f32.add
      f32.add
      local.get $l37
      local.get $l15
      f32.mul
      local.get $l36
      local.get $l16
      f32.mul
      local.get $l35
      local.get $l17
      f32.mul
      f32.add
      f32.add
      f32.mul
      f32.const 0x0p+0 (;=0;)
      f32.ge
      local.tee $l9
      select
      i32.store offset=136
      local.get $l7
      i32.const -1
      i32.const 0
      local.get $l19
      local.get $l31
      local.get $l30
      f32.mul
      local.get $l23
      local.get $l29
      f32.mul
      f32.sub
      local.tee $l15
      f32.mul
      local.get $l20
      local.get $l23
      local.get $l18
      f32.mul
      local.get $l32
      local.get $l30
      f32.mul
      f32.sub
      local.tee $l16
      f32.mul
      local.get $l21
      local.get $l32
      local.get $l29
      f32.mul
      local.get $l31
      local.get $l18
      f32.mul
      f32.sub
      local.tee $l17
      f32.mul
      f32.add
      f32.add
      local.get $l27
      local.get $l15
      f32.mul
      local.get $l25
      local.get $l16
      f32.mul
      local.get $l26
      local.get $l17
      f32.mul
      f32.add
      f32.add
      f32.mul
      local.tee $l24
      f32.const 0x0p+0 (;=0;)
      f32.ge
      select
      i32.store offset=132
      local.get $l7
      i32.const -1
      i32.const 0
      local.get $l27
      local.get $l35
      local.get $l26
      f32.sub
      local.tee $l15
      local.get $l38
      local.get $l25
      f32.sub
      local.tee $l16
      f32.mul
      local.get $l36
      local.get $l25
      f32.sub
      local.tee $l17
      local.get $l39
      local.get $l26
      f32.sub
      local.tee $l18
      f32.mul
      f32.sub
      local.tee $l22
      f32.mul
      local.get $l25
      local.get $l37
      local.get $l27
      f32.sub
      local.tee $l23
      local.get $l18
      f32.mul
      local.get $l15
      local.get $l34
      local.get $l27
      f32.sub
      local.tee $l18
      f32.mul
      f32.sub
      local.tee $l15
      f32.mul
      local.get $l26
      local.get $l17
      local.get $l18
      f32.mul
      local.get $l23
      local.get $l16
      f32.mul
      f32.sub
      local.tee $l16
      f32.mul
      f32.add
      f32.add
      local.get $l19
      local.get $l22
      f32.mul
      local.get $l20
      local.get $l15
      f32.mul
      local.get $l21
      local.get $l16
      f32.mul
      f32.add
      f32.add
      f32.mul
      f32.const 0x0p+0 (;=0;)
      f32.ge
      local.tee $l8
      select
      i32.store offset=140
      block $B2
        local.get $l8
        br_if $B2
        local.get $l9
        br_if $B2
        local.get $l28
        f32.const 0x0p+0 (;=0;)
        f32.ge
        br_if $B2
        local.get $l24
        f32.const 0x0p+0 (;=0;)
        f32.ge
        br_if $B2
        local.get $p0
        i64.const 0
        i64.store
        local.get $p0
        i64.const 0
        i64.store offset=8
        br $B0
      end
      local.get $l7
      i32.const 120
      i32.add
      local.tee $l9
      i32.const 3122820
      i32.load
      i32.store
      local.get $l7
      i32.const 3122812
      i64.load align=4
      i64.store offset=112
      local.get $l7
      i32.const 96
      i32.add
      local.get $p1
      local.get $l7
      i32.const 128
      i32.add
      local.get $l7
      i32.const 112
      i32.add
      local.get $p6
      call $f69904
      local.get $l7
      i32.load offset=112
      local.set $p6
      local.get $l7
      local.get $p1
      local.get $l7
      i32.load offset=116
      local.tee $l12
      i32.const 4
      i32.shl
      local.tee $l8
      i32.add
      local.tee $l10
      i64.load
      i64.store offset=80
      local.get $l7
      local.get $l10
      i64.load offset=8
      i64.store offset=88
      local.get $l7
      local.get $p1
      local.get $l9
      i32.load
      local.tee $l10
      i32.const 4
      i32.shl
      local.tee $l9
      i32.add
      local.tee $l11
      i64.load
      i64.store offset=64
      local.get $l7
      local.get $l11
      i64.load offset=8
      i64.store offset=72
      local.get $l7
      local.get $p2
      local.get $l8
      i32.add
      local.tee $l11
      i64.load offset=8
      i64.store offset=56
      local.get $l7
      local.get $l11
      i64.load
      i64.store offset=48
      local.get $l7
      local.get $p2
      local.get $l9
      i32.add
      local.tee $l11
      i64.load offset=8
      i64.store offset=40
      local.get $l7
      local.get $l11
      i64.load
      i64.store offset=32
      local.get $l7
      local.get $p3
      local.get $l8
      i32.add
      local.tee $l8
      i64.load offset=8
      i64.store offset=24
      local.get $l7
      local.get $l8
      i64.load
      i64.store offset=16
      local.get $l7
      local.get $p3
      local.get $l9
      i32.add
      local.tee $l8
      i64.load offset=8
      i64.store offset=8
      local.get $l7
      local.get $l8
      i64.load
      i64.store
      local.get $p5
      local.get $p6
      i32.const 2
      i32.shl
      local.tee $l8
      i32.add
      i32.load
      local.set $l9
      local.get $p5
      local.get $l12
      i32.const 2
      i32.shl
      local.tee $l12
      i32.add
      i32.load
      local.set $l11
      local.get $p5
      local.get $l10
      i32.const 2
      i32.shl
      local.tee $l10
      i32.add
      i32.load
      local.set $l14
      local.get $p4
      local.get $l8
      i32.add
      i32.load
      local.set $l8
      local.get $p4
      local.get $l12
      i32.add
      i32.load
      local.set $l12
      local.get $p4
      local.get $l10
      i32.add
      i32.load
      local.set $l10
      local.get $p1
      local.get $p1
      local.get $p6
      i32.const 4
      i32.shl
      local.tee $p6
      i32.add
      local.tee $l13
      i64.load
      i64.store
      local.get $p1
      local.get $l13
      i64.load offset=8
      i64.store offset=8
      local.get $p1
      i32.const 16
      i32.add
      local.tee $l13
      local.get $l7
      i64.load offset=88
      i64.store offset=8
      local.get $l13
      local.get $l7
      i64.load offset=80
      i64.store
      local.get $p1
      i32.const 32
      i32.add
      local.tee $p1
      local.get $l7
      i64.load offset=72
      i64.store offset=8
      local.get $p1
      local.get $l7
      i64.load offset=64
      i64.store
      local.get $p2
      local.get $p2
      local.get $p6
      i32.add
      local.tee $p1
      i64.load
      i64.store
      local.get $p2
      local.get $p1
      i64.load offset=8
      i64.store offset=8
      local.get $p2
      local.get $l7
      i64.load offset=56
      i64.store offset=24
      local.get $p2
      local.get $l7
      i64.load offset=48
      i64.store offset=16
      local.get $p2
      local.get $l7
      i64.load offset=32
      i64.store offset=32
      local.get $p2
      local.get $l7
      i64.load offset=40
      i64.store offset=40
      local.get $p3
      local.get $p3
      local.get $p6
      i32.add
      local.tee $p1
      i64.load
      i64.store
      local.get $p3
      local.get $p1
      i64.load offset=8
      i64.store offset=8
      local.get $p3
      local.get $l7
      i64.load offset=16
      i64.store offset=16
      local.get $p3
      local.get $l7
      i64.load offset=24
      i64.store offset=24
      local.get $p3
      local.get $l7
      i64.load offset=8
      i64.store offset=40
      local.get $p3
      local.get $l7
      i64.load
      i64.store offset=32
      local.get $p4
      local.get $l10
      i32.store offset=8
      local.get $p4
      local.get $l12
      i32.store offset=4
      local.get $p4
      local.get $l8
      i32.store
      local.get $p5
      local.get $l14
      i32.store offset=8
      local.get $p5
      local.get $l11
      i32.store offset=4
      local.get $p5
      local.get $l9
      i32.store
      local.get $p0
      local.get $l7
      i64.load offset=104
      i64.store offset=8
      local.get $p0
      local.get $l7
      i64.load offset=96
      i64.store
    end
    local.get $l7
    i32.const 144
    i32.add
    global.set $g0)