  (func $f70082 (type $t10) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (result i32)
    (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32) (local $l33 f32) (local $l34 f32) (local $l35 f32) (local $l36 f32)
    global.get $g0
    i32.const 208
    i32.sub
    local.tee $l6
    global.set $g0
    local.get $p2
    i32.load offset=32
    local.tee $l7
    i32.const 20
    i32.add
    local.tee $l10
    f32.load
    local.set $l25
    local.get $p3
    i32.load offset=32
    local.tee $l8
    i32.const 20
    i32.add
    local.tee $l11
    f32.load
    local.set $l28
    local.get $l7
    i32.const 24
    i32.add
    local.tee $l12
    f32.load
    local.set $l30
    local.get $l8
    i32.const 24
    i32.add
    local.tee $l13
    f32.load
    local.set $l31
    local.get $l7
    f32.load offset=16
    local.set $l32
    local.get $l8
    f32.load offset=16
    local.set $l33
    local.get $l8
    f32.load offset=8
    local.set $l18
    local.get $l7
    f32.load
    local.set $l16
    local.get $l8
    f32.load
    local.set $l19
    local.get $l7
    f32.load offset=8
    local.set $l17
    local.get $l8
    f32.load offset=4
    local.set $l21
    local.get $l7
    f32.load offset=12
    local.set $l14
    local.get $l8
    f32.load offset=12
    local.set $l22
    local.get $l7
    f32.load offset=4
    local.set $l20
    local.get $l6
    i32.const 0
    i32.store offset=204
    local.get $l6
    i32.const 0
    i32.store offset=188
    local.get $l6
    i32.const 0
    i32.store offset=172
    local.get $l6
    f32.const 0x1p+0 (;=1;)
    local.get $l17
    local.get $l21
    f32.mul
    local.get $l20
    local.get $l18
    f32.mul
    f32.sub
    local.get $l14
    local.get $l19
    f32.mul
    local.get $l16
    local.get $l22
    f32.mul
    f32.sub
    f32.add
    local.tee $l15
    local.get $l15
    local.get $l15
    f32.add
    local.tee $l23
    f32.mul
    f32.sub
    local.tee $l26
    local.get $l16
    local.get $l18
    f32.mul
    local.get $l17
    local.get $l19
    f32.mul
    f32.sub
    local.get $l14
    local.get $l21
    f32.mul
    local.get $l20
    local.get $l22
    f32.mul
    f32.sub
    f32.add
    local.tee $l24
    local.get $l24
    local.get $l24
    f32.add
    local.tee $l27
    f32.mul
    local.tee $l34
    f32.sub
    f32.store offset=184
    local.get $l6
    local.get $l20
    local.get $l19
    f32.mul
    local.get $l16
    local.get $l21
    f32.mul
    f32.sub
    local.get $l14
    local.get $l18
    f32.mul
    local.get $l17
    local.get $l22
    f32.mul
    f32.sub
    f32.add
    local.tee $l15
    local.get $l27
    f32.mul
    local.tee $l29
    local.get $l14
    local.get $l22
    f32.mul
    local.get $l21
    local.get $l20
    f32.neg
    local.tee $l35
    f32.mul
    local.get $l16
    local.get $l19
    f32.mul
    f32.sub
    local.get $l17
    local.get $l18
    f32.mul
    f32.sub
    f32.sub
    local.tee $l22
    local.get $l23
    f32.mul
    local.tee $l18
    f32.sub
    f32.store offset=180
    local.get $l6
    local.get $l29
    local.get $l18
    f32.add
    f32.store offset=168
    local.get $l6
    local.get $l26
    local.get $l15
    local.get $l15
    local.get $l15
    f32.add
    local.tee $l29
    f32.mul
    local.tee $l36
    f32.sub
    f32.store offset=164
    local.get $l6
    local.get $l14
    local.get $l14
    f32.mul
    f32.const -0x1p-1 (;=-0.5;)
    f32.add
    local.tee $l26
    local.get $l31
    local.get $l30
    f32.sub
    local.tee $l18
    f32.mul
    local.get $l14
    local.get $l20
    local.get $l33
    local.get $l32
    f32.sub
    local.tee $l19
    f32.mul
    local.get $l16
    local.get $l28
    local.get $l25
    f32.sub
    local.tee $l21
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l17
    local.get $l21
    local.get $l35
    f32.mul
    local.get $l16
    local.get $l19
    f32.mul
    f32.sub
    local.get $l17
    local.get $l18
    f32.mul
    f32.sub
    local.tee $l25
    f32.mul
    f32.sub
    local.tee $l28
    local.get $l28
    f32.add
    f32.store offset=200
    local.get $l6
    local.get $l26
    local.get $l21
    f32.mul
    local.get $l14
    local.get $l16
    local.get $l18
    f32.mul
    local.get $l17
    local.get $l19
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l20
    local.get $l25
    f32.mul
    f32.sub
    local.tee $l28
    local.get $l28
    f32.add
    f32.store offset=196
    local.get $l6
    i32.const 0
    i32.store offset=156
    local.get $l6
    local.get $l15
    local.get $l23
    f32.mul
    local.tee $l15
    local.get $l22
    local.get $l27
    f32.mul
    local.tee $l27
    f32.add
    f32.store offset=176
    local.get $l6
    local.get $l24
    local.get $l23
    f32.mul
    local.tee $l23
    local.get $l22
    local.get $l29
    f32.mul
    local.tee $l22
    f32.sub
    f32.store offset=160
    local.get $l6
    local.get $l15
    local.get $l27
    f32.sub
    f32.store offset=152
    local.get $l6
    local.get $l23
    local.get $l22
    f32.add
    f32.store offset=148
    local.get $l6
    f32.const 0x1p+0 (;=1;)
    local.get $l34
    f32.sub
    local.get $l36
    f32.sub
    f32.store offset=144
    local.get $l6
    local.get $l26
    local.get $l19
    f32.mul
    local.get $l14
    local.get $l17
    local.get $l21
    f32.mul
    local.get $l20
    local.get $l18
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l16
    local.get $l25
    f32.mul
    f32.sub
    local.tee $l14
    local.get $l14
    f32.add
    f32.store offset=192
    local.get $l11
    f32.load
    local.set $l15
    local.get $l10
    f32.load
    local.set $l27
    local.get $l13
    f32.load
    local.set $l23
    local.get $l12
    f32.load
    local.set $l24
    local.get $l7
    f32.load offset=8
    local.set $l18
    local.get $l7
    f32.load
    local.set $l19
    local.get $l7
    f32.load offset=4
    local.set $l21
    local.get $l7
    f32.load offset=12
    local.set $l22
    local.get $l8
    f32.load offset=12
    local.set $l14
    local.get $l8
    f32.load
    local.set $l16
    local.get $l8
    f32.load offset=16
    local.set $l26
    local.get $l7
    f32.load offset=16
    local.set $l25
    local.get $l8
    f32.load offset=4
    local.set $l20
    local.get $l8
    f32.load offset=8
    local.set $l17
    local.get $l6
    i32.const 0
    i32.store offset=140
    local.get $l6
    i32.const 0
    i32.store offset=124
    local.get $l6
    i32.const 0
    i32.store offset=108
    local.get $l6
    local.get $l14
    local.get $l14
    f32.mul
    f32.const -0x1p-1 (;=-0.5;)
    f32.add
    local.tee $l28
    local.get $l24
    local.get $l23
    f32.sub
    local.tee $l23
    f32.mul
    local.get $l14
    local.get $l20
    local.get $l25
    local.get $l26
    f32.sub
    local.tee $l24
    f32.mul
    local.get $l16
    local.get $l27
    local.get $l15
    f32.sub
    local.tee $l27
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l17
    local.get $l27
    local.get $l20
    f32.neg
    local.tee $l32
    f32.mul
    local.get $l16
    local.get $l24
    f32.mul
    f32.sub
    local.get $l17
    local.get $l23
    f32.mul
    f32.sub
    local.tee $l30
    f32.mul
    f32.sub
    local.tee $l15
    local.get $l15
    f32.add
    f32.store offset=136
    local.get $l6
    local.get $l28
    local.get $l27
    f32.mul
    local.get $l14
    local.get $l16
    local.get $l23
    f32.mul
    local.get $l17
    local.get $l24
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l20
    local.get $l30
    f32.mul
    f32.sub
    local.tee $l15
    local.get $l15
    f32.add
    f32.store offset=132
    local.get $l6
    f32.const 0x1p+0 (;=1;)
    local.get $l17
    local.get $l21
    f32.mul
    local.get $l20
    local.get $l18
    f32.mul
    f32.sub
    local.get $l14
    local.get $l19
    f32.mul
    local.get $l16
    local.get $l22
    f32.mul
    f32.sub
    f32.add
    local.tee $l15
    local.get $l15
    local.get $l15
    f32.add
    local.tee $l26
    f32.mul
    f32.sub
    local.tee $l33
    local.get $l16
    local.get $l18
    f32.mul
    local.get $l17
    local.get $l19
    f32.mul
    f32.sub
    local.get $l14
    local.get $l21
    f32.mul
    local.get $l20
    local.get $l22
    f32.mul
    f32.sub
    f32.add
    local.tee $l25
    local.get $l25
    local.get $l25
    f32.add
    local.tee $l31
    f32.mul
    local.tee $l34
    f32.sub
    f32.store offset=120
    local.get $l6
    local.get $l20
    local.get $l19
    f32.mul
    local.get $l16
    local.get $l21
    f32.mul
    f32.sub
    local.get $l14
    local.get $l18
    f32.mul
    local.get $l17
    local.get $l22
    f32.mul
    f32.sub
    f32.add
    local.tee $l15
    local.get $l31
    f32.mul
    local.tee $l29
    local.get $l14
    local.get $l22
    f32.mul
    local.get $l21
    local.get $l32
    f32.mul
    local.get $l16
    local.get $l19
    f32.mul
    f32.sub
    local.get $l17
    local.get $l18
    f32.mul
    f32.sub
    f32.sub
    local.tee $l18
    local.get $l26
    f32.mul
    local.tee $l19
    f32.sub
    f32.store offset=116
    local.get $l6
    local.get $l29
    local.get $l19
    f32.add
    f32.store offset=104
    local.get $l6
    local.get $l33
    local.get $l15
    local.get $l15
    local.get $l15
    f32.add
    local.tee $l19
    f32.mul
    local.tee $l21
    f32.sub
    f32.store offset=100
    local.get $l6
    i32.const 0
    i32.store offset=92
    local.get $l6
    local.get $l28
    local.get $l24
    f32.mul
    local.get $l14
    local.get $l17
    local.get $l27
    f32.mul
    local.get $l20
    local.get $l23
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l16
    local.get $l30
    f32.mul
    f32.sub
    local.tee $l14
    local.get $l14
    f32.add
    f32.store offset=128
    local.get $l6
    local.get $l15
    local.get $l26
    f32.mul
    local.tee $l14
    local.get $l18
    local.get $l31
    f32.mul
    local.tee $l16
    f32.add
    f32.store offset=112
    local.get $l6
    local.get $l25
    local.get $l26
    f32.mul
    local.tee $l17
    local.get $l18
    local.get $l19
    f32.mul
    local.tee $l20
    f32.sub
    f32.store offset=96
    local.get $l6
    local.get $l14
    local.get $l16
    f32.sub
    f32.store offset=88
    local.get $l6
    local.get $l17
    local.get $l20
    f32.add
    f32.store offset=84
    local.get $l6
    f32.const 0x1p+0 (;=1;)
    local.get $l34
    f32.sub
    local.get $l21
    f32.sub
    f32.store offset=80
    local.get $l6
    i32.const 0
    i32.store offset=76
    local.get $l6
    i32.const 2139095039
    i32.store offset=48
    local.get $l6
    i64.const 0
    i64.store offset=40
    local.get $l6
    i64.const 0
    i64.store offset=32
    local.get $l6
    i32.const 0
    i32.store offset=16
    block $B0
      local.get $p0
      local.get $p1
      local.get $p2
      local.get $p3
      local.get $l6
      i32.const 80
      i32.add
      local.get $l6
      i32.const 144
      i32.add
      local.get $l6
      i32.const 16
      i32.add
      local.get $l6
      i32.const 48
      i32.add
      local.get $l6
      i32.const 12
      i32.add
      local.get $l6
      i32.const 32
      i32.add
      i32.const 0
      local.get $l6
      i32.const 76
      i32.add
      call $f70078
      i32.eqz
      br_if $B0
      local.get $p1
      local.get $p0
      local.get $p3
      local.get $p2
      local.get $l6
      i32.const 144
      i32.add
      local.get $l6
      i32.const 80
      i32.add
      local.get $l6
      i32.const 16
      i32.add
      local.get $l6
      i32.const 48
      i32.add
      local.get $l6
      i32.const 8
      i32.add
      local.get $l6
      i32.const 32
      i32.add
      i32.const 1
      local.get $l6
      i32.const 76
      i32.add
      call $f70078
      i32.eqz
      br_if $B0
      local.get $p0
      local.get $p1
      local.get $p2
      local.get $p3
      local.get $l6
      i32.const 80
      i32.add
      local.get $l6
      i32.const 144
      i32.add
      local.get $l6
      i32.const 16
      i32.add
      local.get $l6
      i32.const 48
      i32.add
      local.get $l6
      i32.const 32
      i32.add
      local.get $l6
      i32.const 76
      i32.add
      call $f70079
      i32.eqz
      br_if $B0
      local.get $p4
      local.get $l6
      i64.load offset=48
      i64.store
      local.get $p4
      local.get $l6
      i64.load offset=56
      i64.store offset=8
      block $B1 (result f32)
        local.get $l6
        i32.load offset=76
        i32.const 1
        i32.eq
        if $I2
          local.get $p3
          i32.load offset=32
          local.tee $l7
          f32.load offset=8
          local.tee $l16
          local.get $l7
          f32.load
          local.tee $l17
          local.get $l6
          f32.load offset=32
          local.tee $l20
          f32.mul
          local.get $l7
          f32.load offset=4
          local.tee $l18
          local.get $l6
          f32.load offset=36
          local.tee $l19
          f32.mul
          f32.add
          local.get $l16
          local.get $l6
          f32.load offset=40
          local.tee $l21
          f32.mul
          f32.add
          local.tee $l23
          f32.mul
          local.get $l7
          f32.load offset=12
          local.tee $l14
          local.get $l14
          f32.mul
          f32.const -0x1p-1 (;=-0.5;)
          f32.add
          local.tee $l24
          local.get $l21
          f32.mul
          local.get $l14
          local.get $l17
          local.get $l19
          f32.mul
          local.get $l18
          local.get $l20
          f32.mul
          f32.sub
          f32.mul
          f32.add
          f32.add
          local.tee $l22
          local.get $l22
          f32.add
          local.set $l22
          local.get $l18
          local.get $l23
          f32.mul
          local.get $l24
          local.get $l19
          f32.mul
          local.get $l14
          local.get $l16
          local.get $l20
          f32.mul
          local.get $l17
          local.get $l21
          f32.mul
          f32.sub
          f32.mul
          f32.add
          f32.add
          local.tee $l15
          local.get $l15
          f32.add
          local.set $l15
          local.get $l17
          local.get $l23
          f32.mul
          local.get $l20
          local.get $l24
          f32.mul
          local.get $l14
          local.get $l18
          local.get $l21
          f32.mul
          local.get $l16
          local.get $l19
          f32.mul
          f32.sub
          f32.mul
          f32.add
          f32.add
          local.tee $l14
          local.get $l14
          f32.add
          br $B1
        end
        local.get $p2
        i32.load offset=32
        local.tee $l7
        f32.load offset=8
        local.tee $l16
        local.get $l7
        f32.load
        local.tee $l17
        local.get $l6
        f32.load offset=32
        local.tee $l20
        f32.mul
        local.get $l7
        f32.load offset=4
        local.tee $l18
        local.get $l6
        f32.load offset=36
        local.tee $l19
        f32.mul
        f32.add
        local.get $l16
        local.get $l6
        f32.load offset=40
        local.tee $l21
        f32.mul
        f32.add
        local.tee $l23
        f32.mul
        local.get $l7
        f32.load offset=12
        local.tee $l14
        local.get $l14
        f32.mul
        f32.const -0x1p-1 (;=-0.5;)
        f32.add
        local.tee $l24
        local.get $l21
        f32.mul
        local.get $l14
        local.get $l17
        local.get $l19
        f32.mul
        local.get $l18
        local.get $l20
        f32.mul
        f32.sub
        f32.mul
        f32.add
        f32.add
        f32.const -0x1p+1 (;=-2;)
        f32.mul
        local.set $l22
        local.get $l18
        local.get $l23
        f32.mul
        local.get $l24
        local.get $l19
        f32.mul
        local.get $l14
        local.get $l16
        local.get $l20
        f32.mul
        local.get $l17
        local.get $l21
        f32.mul
        f32.sub
        f32.mul
        f32.add
        f32.add
        f32.const -0x1p+1 (;=-2;)
        f32.mul
        local.set $l15
        local.get $l17
        local.get $l23
        f32.mul
        local.get $l20
        local.get $l24
        f32.mul
        local.get $l14
        local.get $l18
        local.get $l21
        f32.mul
        local.get $l16
        local.get $l19
        f32.mul
        f32.sub
        f32.mul
        f32.add
        f32.add
        f32.const -0x1p+1 (;=-2;)
        f32.mul
      end
      local.set $l14
      local.get $p5
      i32.const 0
      i32.store offset=12
      local.get $p5
      local.get $l22
      f32.store offset=8
      local.get $p5
      local.get $l15
      f32.store offset=4
      local.get $p5
      local.get $l14
      f32.store
      i32.const 1
      local.set $l9
    end
    local.get $l6
    i32.const 208
    i32.add
    global.set $g0
    local.get $l9)
