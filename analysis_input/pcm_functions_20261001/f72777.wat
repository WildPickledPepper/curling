  (func $f72777 (type $t20) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 i32) (param $p7 i32)
    (local $l8 i32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32) (local $l33 f32) (local $l34 f32) (local $l35 f32) (local $l36 f32) (local $l37 i64)
    global.get $g0
    i32.const 80
    i32.sub
    local.tee $l8
    global.set $g0
    block $B0
      local.get $p5
      if $I1
        local.get $p4
        f32.load
        local.set $l9
        local.get $p4
        f32.load offset=4
        local.set $l10
        local.get $l8
        local.get $p4
        f32.load offset=8
        f32.neg
        f32.store offset=48
        local.get $l8
        local.get $l10
        f32.neg
        f32.store offset=44
        local.get $l8
        local.get $l9
        f32.neg
        f32.store offset=40
        local.get $p0
        local.get $l8
        i32.const 40
        i32.add
        call $f72775
        br $B0
      end
      local.get $p0
      i64.load offset=36 align=4
      local.set $l37
      local.get $p4
      local.get $p0
      i32.const 44
      i32.add
      local.tee $p5
      f32.load
      f32.store offset=8
      local.get $p4
      local.get $l37
      i64.store align=4
      local.get $p0
      f32.load offset=40
      local.set $l9
      local.get $p0
      f32.load offset=36
      local.set $l10
      local.get $l8
      local.get $p5
      f32.load
      f32.neg
      f32.store offset=48
      local.get $l8
      local.get $l9
      f32.neg
      f32.store offset=44
      local.get $l8
      local.get $l10
      f32.neg
      f32.store offset=40
      local.get $p0
      local.get $l8
      i32.const 40
      i32.add
      call $f72775
    end
    local.get $p3
    local.get $p0
    f32.load offset=48
    f32.store
    local.get $l8
    local.get $p0
    f32.load
    f32.store offset=40
    local.get $l8
    local.get $p0
    f32.load offset=4
    f32.store offset=44
    local.get $l8
    local.get $p0
    f32.load offset=8
    f32.store offset=48
    local.get $l8
    local.get $p0
    f32.load offset=12
    f32.store offset=52
    local.get $l8
    local.get $p0
    f32.load offset=16
    f32.store offset=56
    local.get $l8
    i32.const 60
    i32.add
    local.tee $p4
    local.get $p0
    f32.load offset=20
    f32.store
    local.get $l8
    local.get $p0
    f32.load offset=24
    f32.store offset=64
    local.get $l8
    local.get $p0
    f32.load offset=28
    f32.store offset=68
    local.get $l8
    local.get $p0
    f32.load offset=32
    f32.store offset=72
    local.get $l8
    i32.const 16
    i32.add
    local.get $l8
    i32.const 40
    i32.add
    local.get $p2
    call $f69768
    local.get $p1
    local.get $l8
    f32.load offset=16
    local.tee $l9
    f32.store
    local.get $p1
    local.get $l8
    f32.load offset=20
    local.tee $l10
    f32.store offset=4
    local.get $p1
    local.get $l8
    f32.load offset=24
    local.tee $l11
    f32.store offset=8
    block $B2
      block $B3
        local.get $l9
        f32.const 0x0p+0 (;=0;)
        f32.gt
        i32.eqz
        br_if $B3
        local.get $l10
        f32.const 0x0p+0 (;=0;)
        f32.gt
        i32.eqz
        br_if $B3
        local.get $l11
        f32.const 0x0p+0 (;=0;)
        f32.gt
        br_if $B2
      end
      i32.const 4700888
      i32.load
      local.set $p0
      local.get $l8
      local.get $p7
      i32.store
      local.get $p0
      i32.const 2
      i32.const 3210117
      i32.const 84
      i32.const 3210546
      local.get $l8
      call $f69760
      local.get $l8
      i32.const 16
      i32.add
      local.get $p6
      f32.const 0x1.028f5cp+0 (;=1.01;)
      local.get $p6
      i32.load
      i32.load offset=40
      call_indirect $__indirect_function_table (type $t31)
      local.get $l8
      i32.const 40
      i32.add
      local.get $p6
      local.get $p6
      i32.load
      i32.load offset=76
      call_indirect $__indirect_function_table (type $t1)
      local.get $p1
      local.get $p3
      f32.load
      local.get $l8
      f32.load offset=40
      local.tee $l9
      f32.neg
      local.get $l9
      f32.sub
      local.tee $l12
      local.get $l8
      f32.load offset=48
      local.tee $l11
      f32.neg
      local.tee $l15
      f32.mul
      local.tee $l31
      local.get $l8
      f32.load offset=52
      local.tee $l10
      local.get $l8
      f32.load offset=44
      local.tee $l13
      f32.neg
      local.tee $l20
      local.get $l13
      f32.sub
      local.tee $l14
      f32.mul
      local.tee $l32
      f32.sub
      local.get $l8
      f32.load offset=28
      local.tee $l16
      local.get $l8
      f32.load offset=16
      local.tee $l17
      f32.sub
      f32.const 0x1p-1 (;=0.5;)
      f32.mul
      local.tee $l27
      f32.mul
      f32.abs
      local.get $l10
      local.get $l12
      f32.mul
      local.tee $l22
      local.get $l14
      local.get $l15
      f32.mul
      local.tee $l33
      f32.add
      local.get $l8
      f32.load offset=32
      local.tee $l18
      local.get $l8
      f32.load offset=20
      local.tee $l21
      f32.sub
      f32.const 0x1p-1 (;=0.5;)
      f32.mul
      local.tee $l28
      f32.mul
      f32.abs
      f32.add
      local.get $l9
      local.get $l12
      f32.mul
      f32.const 0x1p+0 (;=1;)
      f32.add
      local.tee $l34
      local.get $l14
      local.get $l20
      f32.mul
      local.tee $l35
      f32.sub
      local.get $l8
      f32.load offset=36
      local.tee $l19
      local.get $l8
      f32.load offset=24
      local.tee $l23
      f32.sub
      f32.const 0x1p-1 (;=0.5;)
      f32.mul
      local.tee $l29
      f32.mul
      f32.abs
      f32.add
      local.tee $l36
      local.get $l8
      i32.const -64
      i32.sub
      f32.load
      f32.const -0x1p+1 (;=-2;)
      f32.mul
      local.tee $l24
      local.get $l10
      local.get $l10
      f32.mul
      f32.const -0x1p-1 (;=-0.5;)
      f32.add
      local.tee $l14
      f32.mul
      local.get $l10
      local.get $p4
      f32.load
      f32.const -0x1p+1 (;=-2;)
      f32.mul
      local.tee $l25
      local.get $l9
      f32.mul
      local.get $l8
      f32.load offset=56
      f32.const -0x1p+1 (;=-2;)
      f32.mul
      local.tee $l26
      local.get $l13
      f32.mul
      f32.sub
      f32.mul
      f32.sub
      local.get $l11
      local.get $l26
      local.get $l9
      f32.mul
      local.get $l25
      local.get $l13
      f32.mul
      f32.add
      local.get $l24
      local.get $l11
      f32.mul
      f32.add
      local.tee $l30
      f32.mul
      f32.add
      local.get $l14
      local.get $l23
      local.get $l19
      f32.add
      f32.const 0x1p-1 (;=0.5;)
      f32.mul
      local.tee $l19
      local.get $l19
      f32.add
      local.tee $l19
      f32.mul
      local.get $l10
      local.get $l13
      local.get $l17
      local.get $l16
      f32.add
      f32.const 0x1p-1 (;=0.5;)
      f32.mul
      local.tee $l16
      local.get $l16
      f32.add
      local.tee $l16
      f32.mul
      local.get $l9
      local.get $l21
      local.get $l18
      f32.add
      f32.const 0x1p-1 (;=0.5;)
      f32.mul
      local.tee $l17
      local.get $l17
      f32.add
      local.tee $l17
      f32.mul
      f32.sub
      f32.mul
      f32.add
      local.get $l11
      local.get $l17
      local.get $l20
      f32.mul
      local.get $l9
      local.get $l16
      f32.mul
      f32.sub
      local.get $l11
      local.get $l19
      f32.mul
      f32.sub
      local.tee $l21
      f32.mul
      f32.sub
      f32.add
      local.tee $l18
      f32.add
      local.get $l18
      local.get $l36
      f32.sub
      f32.sub
      f32.const 0x1p-1 (;=0.5;)
      f32.mul
      local.tee $l18
      local.get $l12
      local.get $l20
      f32.mul
      local.tee $l20
      local.get $l10
      local.get $l15
      local.get $l11
      f32.sub
      local.tee $l12
      f32.mul
      local.tee $l23
      f32.add
      local.get $l27
      f32.mul
      f32.abs
      local.get $l34
      local.get $l12
      local.get $l15
      f32.mul
      local.tee $l15
      f32.sub
      local.get $l28
      f32.mul
      f32.abs
      f32.add
      local.get $l33
      local.get $l22
      f32.sub
      local.get $l29
      f32.mul
      f32.abs
      f32.add
      local.tee $l12
      local.get $l13
      local.get $l30
      f32.mul
      local.get $l25
      local.get $l14
      f32.mul
      local.get $l10
      local.get $l26
      local.get $l11
      f32.mul
      local.get $l24
      local.get $l9
      f32.mul
      f32.sub
      f32.mul
      f32.sub
      f32.add
      local.get $l14
      local.get $l17
      f32.mul
      local.get $l10
      local.get $l9
      local.get $l19
      f32.mul
      local.get $l11
      local.get $l16
      f32.mul
      f32.sub
      f32.mul
      f32.add
      local.get $l13
      local.get $l21
      f32.mul
      f32.sub
      f32.add
      local.tee $l22
      f32.add
      local.get $l22
      local.get $l12
      f32.sub
      f32.sub
      f32.const 0x1p-1 (;=0.5;)
      f32.mul
      local.tee $l12
      f32.const 0x1p+0 (;=1;)
      local.get $l35
      f32.sub
      local.get $l15
      f32.sub
      local.get $l27
      f32.mul
      f32.abs
      local.get $l20
      local.get $l23
      f32.sub
      local.get $l28
      f32.mul
      f32.abs
      f32.add
      local.get $l31
      local.get $l32
      f32.add
      local.get $l29
      f32.mul
      f32.abs
      f32.add
      local.tee $l15
      local.get $l9
      local.get $l30
      f32.mul
      local.get $l26
      local.get $l14
      f32.mul
      local.get $l10
      local.get $l24
      local.get $l13
      f32.mul
      local.get $l25
      local.get $l11
      f32.mul
      f32.sub
      f32.mul
      f32.sub
      f32.add
      local.get $l14
      local.get $l16
      f32.mul
      local.get $l10
      local.get $l11
      local.get $l17
      f32.mul
      local.get $l13
      local.get $l19
      f32.mul
      f32.sub
      f32.mul
      f32.add
      local.get $l9
      local.get $l21
      f32.mul
      f32.sub
      f32.add
      local.tee $l9
      f32.add
      local.get $l9
      local.get $l15
      f32.sub
      f32.sub
      f32.const 0x1p-1 (;=0.5;)
      f32.mul
      local.tee $l9
      f32.const 0x1p+0 (;=1;)
      local.get $l9
      f32.const 0x0p+0 (;=0;)
      f32.ne
      select
      local.tee $l10
      f32.mul
      local.get $l10
      local.get $l12
      f32.const 0x0p+0 (;=0;)
      f32.ne
      select
      local.tee $l10
      f32.mul
      local.get $l10
      local.get $l18
      f32.const 0x0p+0 (;=0;)
      f32.ne
      select
      f32.const 0x1p+3 (;=8;)
      f32.mul
      local.tee $l11
      f32.div
      local.tee $l10
      local.get $l9
      local.get $l9
      f32.mul
      local.tee $l13
      local.get $l12
      local.get $l12
      f32.mul
      local.tee $l14
      f32.add
      local.get $l11
      f32.const 0x1.555556p-2 (;=0.333333;)
      f32.mul
      local.tee $l9
      f32.mul
      f32.mul
      f32.store offset=8
      local.get $p1
      local.get $l10
      local.get $l18
      local.get $l18
      f32.mul
      local.tee $l11
      local.get $l13
      f32.add
      local.get $l9
      f32.mul
      f32.mul
      f32.store offset=4
      local.get $p1
      local.get $l10
      local.get $l11
      local.get $l14
      f32.add
      local.get $l9
      f32.mul
      f32.mul
      f32.store
      local.get $p2
      i64.const 4575657221408423936
      i64.store offset=8 align=4
      local.get $p2
      i64.const 0
      i64.store align=4
    end
    local.get $l8
    i32.const 80
    i32.add
    global.set $g0)