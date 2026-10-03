  (func $f70063 (type $t34) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 i32) (param $p7 i32) (param $p8 i32) (param $p9 i32) (param $p10 i32)
    (local $l11 i32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32)
    global.get $g0
    i32.const 224
    i32.sub
    local.tee $l11
    global.set $g0
    local.get $l11
    i64.const 1065353216
    i64.store offset=216
    local.get $l11
    i64.const 0
    i64.store offset=208
    local.get $l11
    i64.const 0
    i64.store offset=200
    local.get $l11
    i32.const 1065353216
    i32.store offset=196
    local.get $l11
    i64.const 0
    i64.store offset=180 align=4
    local.get $l11
    i32.const 1065353216
    i32.store offset=176
    local.get $l11
    i64.const 0
    i64.store offset=188 align=4
    local.get $p8
    f32.load offset=56
    local.tee $l15
    local.get $p2
    f32.load offset=24
    local.tee $l14
    local.get $p8
    f32.load offset=8
    local.tee $l19
    f32.mul
    local.get $p2
    f32.load offset=28
    local.tee $l12
    local.get $p8
    f32.load offset=24
    local.tee $l20
    f32.mul
    f32.add
    local.get $p2
    f32.load offset=32
    local.tee $l21
    local.get $p8
    f32.load offset=40
    local.tee $l13
    f32.mul
    f32.add
    f32.add
    local.set $l25
    local.get $l15
    local.get $p2
    f32.load
    local.tee $l17
    local.get $l19
    f32.mul
    local.get $p2
    f32.load offset=4
    local.tee $l16
    local.get $l20
    f32.mul
    f32.add
    local.get $p2
    f32.load offset=8
    local.tee $l24
    local.get $l13
    f32.mul
    f32.add
    f32.add
    local.set $l22
    local.get $p8
    f32.load offset=48
    local.tee $l18
    local.get $l17
    local.get $p8
    f32.load
    local.tee $l27
    f32.mul
    local.get $l16
    local.get $p8
    f32.load offset=16
    local.tee $l28
    f32.mul
    f32.add
    local.get $l24
    local.get $p8
    f32.load offset=32
    local.tee $l29
    f32.mul
    f32.add
    f32.add
    local.set $l23
    local.get $l18
    local.get $p2
    f32.load offset=12
    local.tee $l30
    local.get $l27
    f32.mul
    local.get $p2
    f32.load offset=16
    local.tee $l31
    local.get $l28
    f32.mul
    f32.add
    local.get $p2
    f32.load offset=20
    local.tee $l32
    local.get $l29
    f32.mul
    f32.add
    f32.add
    local.set $l26
    local.get $l15
    local.get $l30
    local.get $l19
    f32.mul
    local.get $l31
    local.get $l20
    f32.mul
    f32.add
    local.get $l32
    local.get $l13
    f32.mul
    f32.add
    f32.add
    local.set $l19
    local.get $l18
    local.get $l14
    local.get $l27
    f32.mul
    local.get $l12
    local.get $l28
    f32.mul
    f32.add
    local.get $l21
    local.get $l29
    f32.mul
    f32.add
    f32.add
    local.set $l20
    local.get $p8
    f32.load offset=52
    local.tee $l13
    local.get $l14
    local.get $p8
    f32.load offset=4
    local.tee $l18
    f32.mul
    local.get $l12
    local.get $p8
    f32.load offset=20
    local.tee $l14
    f32.mul
    f32.add
    local.get $l21
    local.get $p8
    f32.load offset=36
    local.tee $l12
    f32.mul
    f32.add
    f32.add
    local.set $l21
    local.get $l13
    local.get $l17
    local.get $l18
    f32.mul
    local.get $l16
    local.get $l14
    f32.mul
    f32.add
    local.get $l24
    local.get $l12
    f32.mul
    f32.add
    f32.add
    local.set $l15
    local.get $l13
    local.get $l30
    local.get $l18
    f32.mul
    local.get $l31
    local.get $l14
    f32.mul
    f32.add
    local.get $l32
    local.get $l12
    f32.mul
    f32.add
    f32.add
    local.set $l14
    block $B0
      local.get $p6
      i32.eqz
      if $I1
        local.get $l14
        local.get $l15
        f32.sub
        local.tee $l13
        local.get $l25
        local.get $l22
        f32.sub
        local.tee $l17
        f32.mul
        local.get $l21
        local.get $l15
        f32.sub
        local.tee $l16
        local.get $l19
        local.get $l22
        f32.sub
        local.tee $l24
        f32.mul
        f32.sub
        local.tee $l12
        f32.const 0x1p+0 (;=1;)
        local.get $l26
        local.get $l23
        f32.sub
        local.tee $l18
        local.get $l16
        f32.mul
        local.get $l20
        local.get $l23
        f32.sub
        local.tee $l16
        local.get $l13
        f32.mul
        f32.sub
        local.tee $l13
        local.get $l13
        f32.mul
        local.get $l12
        local.get $l12
        f32.mul
        local.get $l16
        local.get $l24
        f32.mul
        local.get $l18
        local.get $l17
        f32.mul
        f32.sub
        local.tee $l12
        local.get $l12
        f32.mul
        f32.add
        f32.add
        f32.sqrt
        f32.div
        local.tee $l17
        f32.mul
        local.tee $l16
        local.get $p1
        f32.load offset=16
        f32.mul
        local.get $l12
        local.get $l17
        f32.mul
        local.tee $l12
        local.get $p1
        f32.load offset=20
        f32.mul
        f32.add
        local.get $l13
        local.get $l17
        f32.mul
        local.tee $l13
        local.get $p1
        f32.load offset=24
        f32.mul
        f32.add
        local.get $l22
        local.get $l13
        f32.mul
        local.get $l23
        local.get $l16
        f32.mul
        local.get $l15
        local.get $l12
        f32.mul
        f32.add
        f32.add
        f32.sub
        f32.const 0x0p+0 (;=0;)
        f32.lt
        br_if $B0
      end
      local.get $l11
      i32.const 0
      i32.store offset=172
      local.get $l11
      local.get $l25
      f32.store offset=168
      local.get $l11
      local.get $l21
      f32.store offset=164
      local.get $l11
      local.get $l20
      f32.store offset=160
      local.get $l11
      i32.const 0
      i32.store offset=156
      local.get $l11
      local.get $l19
      f32.store offset=152
      local.get $l11
      local.get $l14
      f32.store offset=148
      local.get $l11
      local.get $l26
      f32.store offset=144
      local.get $l11
      i32.const 0
      i32.store offset=140
      local.get $l11
      local.get $l22
      f32.store offset=136
      local.get $l11
      local.get $l15
      f32.store offset=132
      local.get $l11
      i32.const 0
      i32.store8 offset=112
      local.get $l11
      i64.const 23613931519
      i64.store offset=104
      local.get $l11
      i32.const 0
      i32.store offset=92
      local.get $l11
      i64.const 9187343235540844544
      i64.store offset=96
      local.get $l11
      local.get $l25
      local.get $l22
      local.get $l19
      f32.add
      f32.add
      f32.const 0x1.55553ep-2 (;=0.333333;)
      f32.mul
      f32.store offset=88
      local.get $l11
      local.get $l21
      local.get $l15
      local.get $l14
      f32.add
      f32.add
      f32.const 0x1.55553ep-2 (;=0.333333;)
      f32.mul
      f32.store offset=84
      local.get $l11
      local.get $l23
      f32.store offset=128
      local.get $l11
      local.get $l20
      local.get $l23
      local.get $l26
      f32.add
      f32.add
      f32.const 0x1.55553ep-2 (;=0.333333;)
      f32.mul
      f32.store offset=80
      local.get $l11
      i32.const 1
      i32.store8 offset=60
      local.get $l11
      local.get $p7
      i32.store offset=48
      local.get $l11
      i32.const 3124664
      i32.store offset=16
      local.get $l11
      local.get $l11
      i32.const 176
      i32.add
      i32.store offset=56
      local.get $l11
      local.get $l11
      i32.const 176
      i32.add
      i32.store offset=52
      local.get $l11
      local.get $l11
      i32.const 80
      i32.add
      i32.store offset=64
      local.get $l11
      i32.const 16
      i32.add
      local.set $p7
      global.get $g0
      i32.const 80
      i32.sub
      local.tee $p2
      global.set $g0
      local.get $p2
      i32.const 0
      i32.store offset=76
      local.get $p2
      i32.const 2139095039
      i32.store offset=48
      local.get $p2
      i64.const 0
      i64.store offset=40
      local.get $p2
      i64.const 0
      i64.store offset=32
      local.get $l11
      i32.const 80
      i32.add
      local.tee $p6
      local.get $p1
      local.get $p5
      local.get $p2
      i32.const 48
      i32.add
      local.get $p2
      i32.const 28
      i32.add
      local.get $p2
      i32.const 32
      i32.add
      local.get $p2
      i32.const 76
      i32.add
      call $f70057
      if $I2
        block $B3
          local.get $p0
          local.get $p7
          local.get $p1
          local.get $p5
          local.get $p2
          i32.const 48
          i32.add
          local.get $p2
          i32.const 24
          i32.add
          local.get $p2
          i32.const 32
          i32.add
          local.get $p2
          i32.const 76
          i32.add
          call $f70058
          i32.eqz
          br_if $B3
          local.get $p6
          local.get $p4
          local.get $p0
          local.get $p7
          local.get $p1
          local.get $p5
          local.get $p2
          i32.const 48
          i32.add
          local.get $p2
          i32.const 32
          i32.add
          local.get $p2
          i32.const 76
          i32.add
          call $f70059
          i32.eqz
          br_if $B3
          local.get $p2
          local.get $p6
          f32.load offset=72
          local.get $p6
          f32.load offset=56
          local.tee $l12
          f32.sub
          local.tee $l14
          local.get $p6
          f32.load offset=80
          local.get $p6
          f32.load offset=48
          local.tee $l13
          f32.sub
          local.tee $l16
          f32.mul
          local.get $p6
          i32.const -64
          i32.sub
          f32.load
          local.get $l13
          f32.sub
          local.tee $l13
          local.get $p6
          f32.load offset=88
          local.get $l12
          f32.sub
          local.tee $l17
          f32.mul
          f32.sub
          local.tee $l12
          f32.const 0x1p+0 (;=1;)
          local.get $l13
          local.get $p6
          f32.load offset=84
          local.get $p6
          f32.load offset=52
          local.tee $l15
          f32.sub
          local.tee $l18
          f32.mul
          local.get $p6
          f32.load offset=68
          local.get $l15
          f32.sub
          local.tee $l15
          local.get $l16
          f32.mul
          f32.sub
          local.tee $l13
          local.get $l13
          f32.mul
          local.get $l15
          local.get $l17
          f32.mul
          local.get $l14
          local.get $l18
          f32.mul
          f32.sub
          local.tee $l14
          local.get $l14
          f32.mul
          local.get $l12
          local.get $l12
          f32.mul
          f32.add
          f32.add
          f32.sqrt
          f32.div
          local.tee $l12
          f32.mul
          f32.store offset=4
          local.get $p2
          local.get $l14
          local.get $l12
          f32.mul
          f32.store
          local.get $p2
          i32.const 0
          i32.store offset=12
          local.get $p2
          local.get $l13
          local.get $l12
          f32.mul
          f32.store offset=8
          local.get $l11
          local.get $p2
          i64.load
          i64.store
          local.get $l11
          local.get $p2
          i64.load offset=8
          i64.store offset=8
          local.get $p6
          local.get $p3
          local.get $p0
          local.get $p0
          i32.load offset=24
          local.get $p0
          local.get $p1
          local.get $p2
          call $f70060
          i32.const 20
          i32.mul
          i32.add
          local.get $p1
          local.get $p9
          local.get $p10
          local.get $p5
          local.get $p2
          i32.const 0
          call $f70061
        end
      end
      local.get $p2
      i32.const 80
      i32.add
      global.set $g0
    end
    local.get $l11
    i32.const 224
    i32.add
    global.set $g0)
