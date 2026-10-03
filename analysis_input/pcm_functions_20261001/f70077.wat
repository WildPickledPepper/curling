  (func $f70077 (type $t491) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 i32) (param $p7 i32) (param $p8 i32) (param $p9 i32) (param $p10 f32) (param $p11 f32) (param $p12 i32) (param $p13 f32) (result i32)
    (local $l14 i32) (local $l15 i32) (local $l16 i32) (local $l17 i32) (local $l18 i32) (local $l19 i32) (local $l20 i32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32) (local $l33 f32) (local $l34 f32) (local $l35 f32) (local $l36 f32) (local $l37 f32) (local $l38 f32) (local $l39 f32) (local $l40 f32) (local $l41 f32) (local $l42 f32) (local $l43 f32) (local $l44 i64)
    global.get $g0
    i32.const 224
    i32.sub
    local.tee $l14
    global.set $g0
    local.get $p2
    i32.load offset=32
    local.tee $l15
    i32.const 20
    i32.add
    local.tee $l17
    f32.load
    local.set $l31
    local.get $p3
    i32.load offset=32
    local.tee $l16
    i32.const 20
    i32.add
    local.tee $l18
    f32.load
    local.set $l35
    local.get $l15
    i32.const 24
    i32.add
    local.tee $l19
    f32.load
    local.set $l39
    local.get $l16
    i32.const 24
    i32.add
    local.tee $l20
    f32.load
    local.set $l40
    local.get $l15
    f32.load offset=16
    local.set $l36
    local.get $l16
    f32.load offset=16
    local.set $l37
    local.get $l16
    f32.load offset=8
    local.set $l25
    local.get $l15
    f32.load
    local.set $l22
    local.get $l16
    f32.load
    local.set $l27
    local.get $l15
    f32.load offset=8
    local.set $l23
    local.get $l16
    f32.load offset=4
    local.set $l28
    local.get $l15
    f32.load offset=12
    local.set $l21
    local.get $l16
    f32.load offset=12
    local.set $l29
    local.get $l15
    f32.load offset=4
    local.set $l24
    local.get $l14
    i32.const 0
    i32.store offset=220
    local.get $l14
    i32.const 0
    i32.store offset=204
    local.get $l14
    i32.const 0
    i32.store offset=188
    local.get $l14
    f32.const 0x1p+0 (;=1;)
    local.get $l23
    local.get $l28
    f32.mul
    local.get $l24
    local.get $l25
    f32.mul
    f32.sub
    local.get $l21
    local.get $l27
    f32.mul
    local.get $l22
    local.get $l29
    f32.mul
    f32.sub
    f32.add
    local.tee $l26
    local.get $l26
    local.get $l26
    f32.add
    local.tee $l30
    f32.mul
    f32.sub
    local.tee $l32
    local.get $l22
    local.get $l25
    f32.mul
    local.get $l23
    local.get $l27
    f32.mul
    f32.sub
    local.get $l21
    local.get $l28
    f32.mul
    local.get $l24
    local.get $l29
    f32.mul
    f32.sub
    f32.add
    local.tee $l34
    local.get $l34
    local.get $l34
    f32.add
    local.tee $l33
    f32.mul
    local.tee $l41
    f32.sub
    f32.store offset=200
    local.get $l14
    local.get $l24
    local.get $l27
    f32.mul
    local.get $l22
    local.get $l28
    f32.mul
    f32.sub
    local.get $l21
    local.get $l25
    f32.mul
    local.get $l23
    local.get $l29
    f32.mul
    f32.sub
    f32.add
    local.tee $l26
    local.get $l33
    f32.mul
    local.tee $l38
    local.get $l21
    local.get $l29
    f32.mul
    local.get $l28
    local.get $l24
    f32.neg
    local.tee $l42
    f32.mul
    local.get $l22
    local.get $l27
    f32.mul
    f32.sub
    local.get $l23
    local.get $l25
    f32.mul
    f32.sub
    f32.sub
    local.tee $l29
    local.get $l30
    f32.mul
    local.tee $l25
    f32.sub
    f32.store offset=196
    local.get $l14
    local.get $l38
    local.get $l25
    f32.add
    f32.store offset=184
    local.get $l14
    local.get $l32
    local.get $l26
    local.get $l26
    local.get $l26
    f32.add
    local.tee $l38
    f32.mul
    local.tee $l43
    f32.sub
    f32.store offset=180
    local.get $l14
    local.get $l21
    local.get $l21
    f32.mul
    f32.const -0x1p-1 (;=-0.5;)
    f32.add
    local.tee $l32
    local.get $l40
    local.get $l39
    f32.sub
    local.tee $l25
    f32.mul
    local.get $l21
    local.get $l24
    local.get $l37
    local.get $l36
    f32.sub
    local.tee $l27
    f32.mul
    local.get $l22
    local.get $l35
    local.get $l31
    f32.sub
    local.tee $l28
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l23
    local.get $l28
    local.get $l42
    f32.mul
    local.get $l22
    local.get $l27
    f32.mul
    f32.sub
    local.get $l23
    local.get $l25
    f32.mul
    f32.sub
    local.tee $l31
    f32.mul
    f32.sub
    local.tee $l35
    local.get $l35
    f32.add
    f32.store offset=216
    local.get $l14
    local.get $l32
    local.get $l28
    f32.mul
    local.get $l21
    local.get $l22
    local.get $l25
    f32.mul
    local.get $l23
    local.get $l27
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l24
    local.get $l31
    f32.mul
    f32.sub
    local.tee $l35
    local.get $l35
    f32.add
    f32.store offset=212
    local.get $l14
    i32.const 0
    i32.store offset=172
    local.get $l14
    local.get $l26
    local.get $l30
    f32.mul
    local.tee $l26
    local.get $l29
    local.get $l33
    f32.mul
    local.tee $l33
    f32.add
    f32.store offset=192
    local.get $l14
    local.get $l34
    local.get $l30
    f32.mul
    local.tee $l30
    local.get $l29
    local.get $l38
    f32.mul
    local.tee $l29
    f32.sub
    f32.store offset=176
    local.get $l14
    local.get $l26
    local.get $l33
    f32.sub
    f32.store offset=168
    local.get $l14
    local.get $l30
    local.get $l29
    f32.add
    f32.store offset=164
    local.get $l14
    f32.const 0x1p+0 (;=1;)
    local.get $l41
    f32.sub
    local.get $l43
    f32.sub
    f32.store offset=160
    local.get $l14
    local.get $l32
    local.get $l27
    f32.mul
    local.get $l21
    local.get $l23
    local.get $l28
    f32.mul
    local.get $l24
    local.get $l25
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l22
    local.get $l31
    f32.mul
    f32.sub
    local.tee $l21
    local.get $l21
    f32.add
    f32.store offset=208
    local.get $l18
    f32.load
    local.set $l26
    local.get $l17
    f32.load
    local.set $l33
    local.get $l20
    f32.load
    local.set $l30
    local.get $l19
    f32.load
    local.set $l34
    local.get $l15
    f32.load offset=8
    local.set $l25
    local.get $l15
    f32.load
    local.set $l27
    local.get $l15
    f32.load offset=4
    local.set $l28
    local.get $l15
    f32.load offset=12
    local.set $l29
    local.get $l16
    f32.load offset=12
    local.set $l21
    local.get $l16
    f32.load
    local.set $l22
    local.get $l16
    f32.load offset=16
    local.set $l32
    local.get $l15
    f32.load offset=16
    local.set $l31
    local.get $l16
    f32.load offset=4
    local.set $l24
    local.get $l16
    f32.load offset=8
    local.set $l23
    local.get $l14
    i32.const 0
    i32.store offset=156
    local.get $l14
    i32.const 0
    i32.store offset=140
    local.get $l14
    i32.const 0
    i32.store offset=124
    local.get $l14
    local.get $l21
    local.get $l21
    f32.mul
    f32.const -0x1p-1 (;=-0.5;)
    f32.add
    local.tee $l35
    local.get $l34
    local.get $l30
    f32.sub
    local.tee $l30
    f32.mul
    local.get $l21
    local.get $l24
    local.get $l31
    local.get $l32
    f32.sub
    local.tee $l34
    f32.mul
    local.get $l22
    local.get $l33
    local.get $l26
    f32.sub
    local.tee $l33
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l23
    local.get $l33
    local.get $l24
    f32.neg
    local.tee $l36
    f32.mul
    local.get $l22
    local.get $l34
    f32.mul
    f32.sub
    local.get $l23
    local.get $l30
    f32.mul
    f32.sub
    local.tee $l39
    f32.mul
    f32.sub
    local.tee $l26
    local.get $l26
    f32.add
    f32.store offset=152
    local.get $l14
    local.get $l35
    local.get $l33
    f32.mul
    local.get $l21
    local.get $l22
    local.get $l30
    f32.mul
    local.get $l23
    local.get $l34
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l24
    local.get $l39
    f32.mul
    f32.sub
    local.tee $l26
    local.get $l26
    f32.add
    f32.store offset=148
    local.get $l14
    f32.const 0x1p+0 (;=1;)
    local.get $l23
    local.get $l28
    f32.mul
    local.get $l24
    local.get $l25
    f32.mul
    f32.sub
    local.get $l21
    local.get $l27
    f32.mul
    local.get $l22
    local.get $l29
    f32.mul
    f32.sub
    f32.add
    local.tee $l26
    local.get $l26
    local.get $l26
    f32.add
    local.tee $l32
    f32.mul
    f32.sub
    local.tee $l37
    local.get $l22
    local.get $l25
    f32.mul
    local.get $l23
    local.get $l27
    f32.mul
    f32.sub
    local.get $l21
    local.get $l28
    f32.mul
    local.get $l24
    local.get $l29
    f32.mul
    f32.sub
    f32.add
    local.tee $l31
    local.get $l31
    local.get $l31
    f32.add
    local.tee $l40
    f32.mul
    local.tee $l41
    f32.sub
    local.tee $l42
    f32.store offset=136
    local.get $l14
    local.get $l24
    local.get $l27
    f32.mul
    local.get $l22
    local.get $l28
    f32.mul
    f32.sub
    local.get $l21
    local.get $l25
    f32.mul
    local.get $l23
    local.get $l29
    f32.mul
    f32.sub
    f32.add
    local.tee $l26
    local.get $l40
    f32.mul
    local.tee $l38
    local.get $l21
    local.get $l29
    f32.mul
    local.get $l28
    local.get $l36
    f32.mul
    local.get $l22
    local.get $l27
    f32.mul
    f32.sub
    local.get $l23
    local.get $l25
    f32.mul
    f32.sub
    f32.sub
    local.tee $l25
    local.get $l32
    f32.mul
    local.tee $l27
    f32.sub
    local.tee $l29
    f32.store offset=132
    local.get $l14
    local.get $l38
    local.get $l27
    f32.add
    local.tee $l36
    f32.store offset=120
    local.get $l14
    local.get $l37
    local.get $l26
    local.get $l26
    local.get $l26
    f32.add
    local.tee $l27
    f32.mul
    local.tee $l28
    f32.sub
    local.tee $l37
    f32.store offset=116
    local.get $l14
    i32.const 0
    i32.store offset=108
    local.get $l14
    local.get $l35
    local.get $l34
    f32.mul
    local.get $l21
    local.get $l23
    local.get $l33
    f32.mul
    local.get $l24
    local.get $l30
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l22
    local.get $l39
    f32.mul
    f32.sub
    local.tee $l21
    local.get $l21
    f32.add
    f32.store offset=144
    local.get $l14
    local.get $l26
    local.get $l32
    f32.mul
    local.tee $l21
    local.get $l25
    local.get $l40
    f32.mul
    local.tee $l22
    f32.add
    local.tee $l26
    f32.store offset=128
    local.get $l14
    local.get $l31
    local.get $l32
    f32.mul
    local.tee $l23
    local.get $l25
    local.get $l27
    f32.mul
    local.tee $l24
    f32.sub
    local.tee $l25
    f32.store offset=112
    local.get $l14
    local.get $l21
    local.get $l22
    f32.sub
    local.tee $l27
    f32.store offset=104
    local.get $l14
    local.get $l23
    local.get $l24
    f32.add
    local.tee $l24
    f32.store offset=100
    local.get $l14
    f32.const 0x1p+0 (;=1;)
    local.get $l41
    f32.sub
    local.get $l28
    f32.sub
    local.tee $l28
    f32.store offset=96
    block $B0
      block $B1
        local.get $p12
        if $I2
          local.get $l14
          i32.const 0
          i32.store offset=92
          local.get $l14
          i32.const 2139095039
          i32.store offset=64
          local.get $l14
          i64.const 0
          i64.store offset=56
          local.get $l14
          i64.const 0
          i64.store offset=48
          local.get $p0
          local.get $p1
          local.get $p2
          local.get $p3
          local.get $l14
          i32.const 96
          i32.add
          local.get $l14
          i32.const 160
          i32.add
          local.get $p6
          local.get $l14
          i32.const -64
          i32.sub
          local.get $l14
          i32.const 44
          i32.add
          local.get $l14
          i32.const 48
          i32.add
          i32.const 0
          local.get $l14
          i32.const 92
          i32.add
          call $f70078
          i32.eqz
          if $I3
            i32.const 0
            local.set $l15
            br $B0
          end
          i32.const 0
          local.set $l15
          block $B4 (result i32)
            i32.const 1
            local.get $p1
            local.get $p0
            local.get $p3
            local.get $p2
            local.get $l14
            i32.const 160
            i32.add
            local.get $l14
            i32.const 96
            i32.add
            local.get $p6
            local.get $l14
            i32.const -64
            i32.sub
            local.get $l14
            i32.const 40
            i32.add
            local.get $l14
            i32.const 48
            i32.add
            i32.const 1
            local.get $l14
            i32.const 92
            i32.add
            call $f70078
            i32.eqz
            br_if $B4
            drop
            local.get $l14
            i32.load offset=44
            i32.const 20
            i32.mul
            local.set $l17
            local.get $l14
            i32.load offset=40
            i32.const 20
            i32.mul
            local.set $l18
            i32.const 0
            local.set $p12
            loop $L5
              block $B6
                block $B7
                  local.get $p12
                  i32.const 1
                  i32.and
                  if $I8
                    local.get $p0
                    local.get $p1
                    local.get $p2
                    local.get $p3
                    local.get $l14
                    i32.const 96
                    i32.add
                    local.get $l14
                    i32.const 160
                    i32.add
                    local.get $p6
                    local.get $l14
                    i32.const -64
                    i32.sub
                    local.get $l14
                    i32.const 48
                    i32.add
                    local.get $l14
                    i32.const 92
                    i32.add
                    call $f70079
                    i32.eqz
                    if $I9
                      i32.const 0
                      local.set $l15
                      i32.const 1
                      br $B4
                    end
                    local.get $l14
                    i32.load offset=92
                    i32.const 2
                    i32.eq
                    br_if $B7
                    i32.const 1
                    local.set $l15
                    i32.const 1
                    br $B4
                  end
                  block $B10
                    block $B11
                      local.get $l14
                      i32.load offset=92
                      br_table $B11 $B10 $B7
                    end
                    local.get $p0
                    i32.load offset=24
                    local.set $l15
                    local.get $l14
                    i32.const 0
                    i32.store offset=28
                    local.get $l14
                    local.get $l14
                    f32.load offset=48
                    local.tee $l21
                    local.get $l14
                    f32.load offset=104
                    f32.mul
                    local.get $l14
                    f32.load offset=52
                    local.tee $l22
                    local.get $l14
                    f32.load offset=120
                    f32.mul
                    f32.add
                    local.get $l14
                    f32.load offset=56
                    local.tee $l23
                    local.get $l14
                    f32.load offset=136
                    f32.mul
                    f32.add
                    f32.store offset=24
                    local.get $l14
                    local.get $l21
                    local.get $l14
                    f32.load offset=100
                    f32.mul
                    local.get $l22
                    local.get $l14
                    f32.load offset=116
                    f32.mul
                    f32.add
                    local.get $l23
                    local.get $l14
                    f32.load offset=132
                    f32.mul
                    f32.add
                    f32.store offset=20
                    local.get $l14
                    local.get $l21
                    local.get $l14
                    f32.load offset=96
                    f32.mul
                    local.get $l22
                    local.get $l14
                    f32.load offset=112
                    f32.mul
                    f32.add
                    local.get $l23
                    local.get $l14
                    f32.load offset=128
                    f32.mul
                    f32.add
                    f32.store offset=16
                    local.get $p0
                    local.get $p1
                    local.get $l15
                    local.get $l17
                    i32.add
                    local.get $p1
                    i32.load offset=24
                    local.get $p1
                    local.get $p3
                    local.get $l14
                    i32.const 16
                    i32.add
                    call $f70060
                    i32.const 20
                    i32.mul
                    i32.add
                    local.get $p2
                    local.get $p3
                    local.get $l14
                    i32.const 96
                    i32.add
                    local.get $p4
                    local.get $p5
                    local.get $p6
                    call $f70076
                    local.get $p5
                    i32.load
                    i32.eqz
                    br_if $B6
                    local.get $l14
                    f32.load offset=24
                    f32.neg
                    local.set $l21
                    local.get $l14
                    f32.load offset=20
                    f32.neg
                    local.set $l22
                    local.get $l14
                    f32.load offset=16
                    f32.neg
                    local.set $l23
                    i32.const 0
                    local.set $l16
                    loop $L12
                      local.get $l14
                      local.get $p4
                      local.get $l16
                      i32.const 48
                      i32.mul
                      i32.add
                      local.tee $l15
                      i64.load offset=16
                      i64.store
                      local.get $l15
                      local.get $l15
                      i64.load
                      i64.store offset=16
                      local.get $l14
                      local.get $l15
                      i32.const 24
                      i32.add
                      local.tee $p7
                      i64.load
                      i64.store offset=8
                      local.get $p7
                      local.get $l15
                      i32.const 8
                      i32.add
                      local.tee $p8
                      i64.load
                      i64.store
                      local.get $l15
                      local.get $l14
                      i64.load
                      i64.store
                      local.get $l14
                      i64.load offset=8
                      local.set $l44
                      local.get $l15
                      local.get $l22
                      f32.store offset=36
                      local.get $l15
                      local.get $l21
                      f32.store offset=40
                      local.get $p8
                      local.get $l44
                      i64.store
                      local.get $l15
                      local.get $l23
                      f32.store offset=32
                      local.get $l16
                      i32.const 1
                      i32.add
                      local.tee $l16
                      local.get $p5
                      i32.load
                      i32.lt_u
                      br_if $L12
                    end
                    br $B6
                  end
                  local.get $p0
                  i32.load offset=24
                  local.set $l15
                  local.get $p1
                  i32.load offset=24
                  local.set $l16
                  local.get $l14
                  i32.const 0
                  i32.store offset=28
                  local.get $l14
                  local.get $l14
                  f32.load offset=48
                  local.tee $l21
                  local.get $l14
                  f32.load offset=168
                  f32.mul
                  local.get $l14
                  f32.load offset=52
                  local.tee $l22
                  local.get $l14
                  f32.load offset=184
                  f32.mul
                  f32.add
                  local.get $l14
                  f32.load offset=56
                  local.tee $l23
                  local.get $l14
                  f32.load offset=200
                  f32.mul
                  f32.add
                  f32.store offset=24
                  local.get $l14
                  local.get $l21
                  local.get $l14
                  f32.load offset=164
                  f32.mul
                  local.get $l22
                  local.get $l14
                  f32.load offset=180
                  f32.mul
                  f32.add
                  local.get $l23
                  local.get $l14
                  f32.load offset=196
                  f32.mul
                  f32.add
                  f32.store offset=20
                  local.get $l14
                  local.get $l21
                  local.get $l14
                  f32.load offset=160
                  f32.mul
                  local.get $l22
                  local.get $l14
                  f32.load offset=176
                  f32.mul
                  f32.add
                  local.get $l23
                  local.get $l14
                  f32.load offset=192
                  f32.mul
                  f32.add
                  f32.store offset=16
                  local.get $p1
                  local.get $p0
                  local.get $l16
                  local.get $l18
                  i32.add
                  local.get $l15
                  local.get $p0
                  local.get $p2
                  local.get $l14
                  i32.const 16
                  i32.add
                  call $f70060
                  i32.const 20
                  i32.mul
                  i32.add
                  local.get $p3
                  local.get $p2
                  local.get $l14
                  i32.const 160
                  i32.add
                  local.get $p4
                  local.get $p5
                  local.get $p6
                  call $f70076
                  br $B6
                end
                local.get $p0
                i32.load offset=24
                local.set $l15
                local.get $l14
                i32.const 0
                i32.store offset=28
                local.get $l14
                local.get $l14
                f32.load offset=56
                local.tee $l21
                f32.neg
                f32.store offset=24
                local.get $l14
                local.get $l14
                f32.load offset=52
                local.tee $l22
                f32.neg
                f32.store offset=20
                local.get $l14
                local.get $l14
                f32.load offset=48
                local.tee $l23
                f32.neg
                f32.store offset=16
                local.get $p0
                local.get $p2
                local.get $l14
                i32.const 16
                i32.add
                call $f70060
                local.set $l16
                local.get $p1
                i32.load offset=24
                local.set $p7
                local.get $l14
                i32.const 0
                i32.store offset=28
                local.get $l14
                local.get $l23
                local.get $l14
                f32.load offset=104
                f32.mul
                local.get $l22
                local.get $l14
                f32.load offset=120
                f32.mul
                f32.add
                local.get $l21
                local.get $l14
                f32.load offset=136
                f32.mul
                f32.add
                f32.store offset=24
                local.get $l14
                local.get $l23
                local.get $l14
                f32.load offset=100
                f32.mul
                local.get $l22
                local.get $l14
                f32.load offset=116
                f32.mul
                f32.add
                local.get $l21
                local.get $l14
                f32.load offset=132
                f32.mul
                f32.add
                f32.store offset=20
                local.get $l14
                local.get $l23
                local.get $l14
                f32.load offset=96
                f32.mul
                local.get $l22
                local.get $l14
                f32.load offset=112
                f32.mul
                f32.add
                local.get $l21
                local.get $l14
                f32.load offset=128
                f32.mul
                f32.add
                f32.store offset=16
                local.get $p1
                local.get $p0
                local.get $p7
                local.get $p1
                local.get $p3
                local.get $l14
                i32.const 16
                i32.add
                call $f70060
                i32.const 20
                i32.mul
                i32.add
                local.get $l15
                local.get $l16
                i32.const 20
                i32.mul
                i32.add
                local.get $p3
                local.get $p2
                local.get $l14
                i32.const 160
                i32.add
                local.get $p4
                local.get $p5
                local.get $p6
                call $f70076
              end
              local.get $p12
              i32.const -1
              i32.xor
              local.set $l15
              i32.const 1
              local.set $p12
              local.get $l15
              local.get $p5
              i32.load
              i32.eqz
              i32.and
              br_if $L5
            end
            i32.const 0
          end
          i32.eqz
          br_if $B1
          br $B0
        end
        local.get $p7
        f32.load
        local.set $l21
        local.get $p7
        f32.load offset=4
        local.set $l22
        local.get $p7
        f32.load offset=8
        local.set $l23
        local.get $l14
        i32.const 0
        i32.store offset=76
        local.get $l14
        local.get $l23
        f32.neg
        f32.store offset=72
        local.get $l14
        local.get $l22
        f32.neg
        f32.store offset=68
        local.get $l14
        local.get $l21
        f32.neg
        f32.store offset=64
        local.get $l14
        i32.const 0
        i32.store offset=60
        local.get $l14
        local.get $l26
        local.get $l21
        f32.mul
        local.get $l29
        local.get $l22
        f32.mul
        f32.add
        local.get $l42
        local.get $l23
        f32.mul
        f32.add
        f32.store offset=56
        local.get $l14
        local.get $l25
        local.get $l21
        f32.mul
        local.get $l37
        local.get $l22
        f32.mul
        f32.add
        local.get $l36
        local.get $l23
        f32.mul
        f32.add
        f32.store offset=52
        local.get $l14
        local.get $l28
        local.get $l21
        f32.mul
        local.get $l24
        local.get $l22
        f32.mul
        f32.add
        local.get $l27
        local.get $l23
        f32.mul
        f32.add
        f32.store offset=48
        local.get $p1
        local.get $p3
        local.get $l14
        i32.const -64
        i32.sub
        local.get $p9
        local.get $p13
        f32.const 0x1.99999ap-5 (;=0.05;)
        f32.mul
        local.tee $l21
        local.get $p13
        f32.const 0x1.47ae14p-7 (;=0.01;)
        f32.mul
        local.tee $l22
        local.get $p11
        local.get $p11
        local.get $l22
        f32.lt
        select
        local.tee $l23
        local.get $l21
        local.get $l23
        f32.lt
        select
        call $f70080
        local.set $l15
        local.get $p8
        f32.load offset=8
        local.set $l25
        local.get $p8
        f32.load
        local.set $l23
        local.get $p8
        f32.load offset=4
        local.set $l24
        local.get $l14
        i32.const 0
        i32.store offset=28
        local.get $l14
        local.get $l23
        local.get $l14
        f32.load offset=144
        f32.sub
        local.tee $l23
        local.get $l14
        f32.load offset=128
        f32.mul
        local.get $l24
        local.get $l14
        f32.load offset=148
        f32.sub
        local.tee $l24
        local.get $l14
        f32.load offset=132
        f32.mul
        f32.add
        local.get $l25
        local.get $l14
        f32.load offset=152
        f32.sub
        local.tee $l25
        local.get $l14
        f32.load offset=136
        f32.mul
        f32.add
        f32.store offset=24
        local.get $l14
        local.get $l23
        local.get $l14
        f32.load offset=112
        f32.mul
        local.get $l24
        local.get $l14
        f32.load offset=116
        f32.mul
        f32.add
        local.get $l25
        local.get $l14
        f32.load offset=120
        f32.mul
        f32.add
        f32.store offset=20
        local.get $l14
        local.get $l23
        local.get $l14
        f32.load offset=96
        f32.mul
        local.get $l24
        local.get $l14
        f32.load offset=100
        f32.mul
        f32.add
        local.get $l25
        local.get $l14
        f32.load offset=104
        f32.mul
        f32.add
        f32.store offset=16
        local.get $p0
        local.get $p2
        local.get $l14
        i32.const 48
        i32.add
        local.get $l14
        i32.const 16
        i32.add
        local.get $l21
        local.get $l22
        local.get $p10
        local.get $p10
        local.get $l22
        f32.lt
        select
        local.tee $l22
        local.get $l21
        local.get $l22
        f32.lt
        select
        call $f70080
        local.set $p7
        local.get $p1
        i32.load offset=24
        local.get $l15
        i32.const 20
        i32.mul
        i32.add
        local.tee $l16
        f32.load
        local.tee $l21
        local.get $p3
        i32.load offset=40
        local.tee $l15
        f32.load
        f32.mul
        local.get $l16
        f32.load offset=4
        local.tee $l22
        local.get $l15
        f32.load offset=4
        f32.mul
        f32.add
        local.get $l16
        f32.load offset=8
        local.tee $l23
        local.get $l15
        f32.load offset=8
        f32.mul
        f32.add
        local.tee $l24
        f32.const 0x1p+0 (;=1;)
        local.get $l24
        local.get $l24
        f32.mul
        local.get $l21
        local.get $l15
        f32.load offset=16
        f32.mul
        local.get $l22
        local.get $l15
        f32.load offset=20
        f32.mul
        f32.add
        local.get $l23
        local.get $l15
        f32.load offset=24
        f32.mul
        f32.add
        local.tee $l24
        local.get $l24
        f32.mul
        f32.add
        local.get $l21
        local.get $l15
        f32.load offset=32
        f32.mul
        local.get $l22
        local.get $l15
        f32.load offset=36
        f32.mul
        f32.add
        local.get $l23
        local.get $l15
        f32.load offset=40
        f32.mul
        f32.add
        local.tee $l21
        local.get $l21
        f32.mul
        f32.add
        f32.sqrt
        f32.div
        local.tee $l22
        f32.mul
        local.get $l14
        f32.load offset=64
        f32.mul
        local.get $l24
        local.get $l22
        f32.mul
        local.get $l14
        f32.load offset=68
        f32.mul
        f32.add
        local.get $l21
        local.get $l22
        f32.mul
        local.get $l14
        f32.load offset=72
        f32.mul
        f32.add
        f32.abs
        local.get $l14
        f32.load offset=56
        local.get $p0
        i32.load offset=24
        local.get $p7
        i32.const 20
        i32.mul
        i32.add
        local.tee $p7
        f32.load
        local.tee $l21
        local.get $p2
        i32.load offset=40
        local.tee $l15
        f32.load offset=32
        f32.mul
        local.get $p7
        f32.load offset=4
        local.tee $l22
        local.get $l15
        f32.load offset=36
        f32.mul
        f32.add
        local.get $p7
        f32.load offset=8
        local.tee $l23
        local.get $l15
        f32.load offset=40
        f32.mul
        f32.add
        local.tee $l24
        f32.const 0x1p+0 (;=1;)
        local.get $l21
        local.get $l15
        f32.load
        f32.mul
        local.get $l22
        local.get $l15
        f32.load offset=4
        f32.mul
        f32.add
        local.get $l23
        local.get $l15
        f32.load offset=8
        f32.mul
        f32.add
        local.tee $l25
        local.get $l25
        f32.mul
        local.get $l21
        local.get $l15
        f32.load offset=16
        f32.mul
        local.get $l22
        local.get $l15
        f32.load offset=20
        f32.mul
        f32.add
        local.get $l23
        local.get $l15
        f32.load offset=24
        f32.mul
        f32.add
        local.tee $l21
        local.get $l21
        f32.mul
        f32.add
        local.get $l24
        local.get $l24
        f32.mul
        f32.add
        f32.sqrt
        f32.div
        local.tee $l22
        f32.mul
        local.tee $l23
        f32.mul
        local.get $l14
        f32.load offset=48
        local.get $l25
        local.get $l22
        f32.mul
        local.tee $l24
        f32.mul
        local.get $l14
        f32.load offset=52
        local.get $l21
        local.get $l22
        f32.mul
        local.tee $l25
        f32.mul
        f32.add
        f32.add
        f32.abs
        f32.ge
        if $I13
          local.get $p1
          local.get $p0
          local.get $l16
          local.get $p7
          local.get $p3
          local.get $p2
          local.get $l14
          i32.const 160
          i32.add
          local.get $p4
          local.get $p5
          local.get $p6
          call $f70076
          br $B1
        end
        local.get $p0
        local.get $p1
        local.get $p7
        local.get $l16
        local.get $p2
        local.get $p3
        local.get $l14
        i32.const 96
        i32.add
        local.get $p4
        local.get $p5
        local.get $p6
        call $f70076
        local.get $p5
        i32.load
        i32.eqz
        br_if $B1
        local.get $l24
        local.get $l14
        f32.load offset=104
        f32.mul
        local.get $l25
        local.get $l14
        f32.load offset=120
        f32.mul
        f32.add
        local.get $l23
        local.get $l14
        f32.load offset=136
        f32.mul
        f32.add
        f32.neg
        local.set $l21
        local.get $l24
        local.get $l14
        f32.load offset=100
        f32.mul
        local.get $l25
        local.get $l14
        f32.load offset=116
        f32.mul
        f32.add
        local.get $l23
        local.get $l14
        f32.load offset=132
        f32.mul
        f32.add
        f32.neg
        local.set $l22
        local.get $l24
        local.get $l14
        f32.load offset=96
        f32.mul
        local.get $l25
        local.get $l14
        f32.load offset=112
        f32.mul
        f32.add
        local.get $l23
        local.get $l14
        f32.load offset=128
        f32.mul
        f32.add
        f32.neg
        local.set $l23
        i32.const 0
        local.set $l16
        loop $L14
          local.get $l14
          local.get $p4
          local.get $l16
          i32.const 48
          i32.mul
          i32.add
          local.tee $l15
          i64.load offset=16
          i64.store offset=16
          local.get $l15
          local.get $l15
          i64.load
          i64.store offset=16
          local.get $l14
          local.get $l15
          i32.const 24
          i32.add
          local.tee $p7
          i64.load
          i64.store offset=24
          local.get $p7
          local.get $l15
          i32.const 8
          i32.add
          local.tee $p8
          i64.load
          i64.store
          local.get $l15
          local.get $l14
          i64.load offset=16
          i64.store
          local.get $l14
          i64.load offset=24
          local.set $l44
          local.get $l15
          local.get $l22
          f32.store offset=36
          local.get $l15
          local.get $l21
          f32.store offset=40
          local.get $p8
          local.get $l44
          i64.store
          local.get $l15
          local.get $l23
          f32.store offset=32
          local.get $l16
          i32.const 1
          i32.add
          local.tee $l16
          local.get $p5
          i32.load
          i32.lt_u
          br_if $L14
        end
      end
      i32.const 1
      local.set $l15
    end
    local.get $l14
    i32.const 224
    i32.add
    global.set $g0
    local.get $l15
    i32.const 1
    i32.and)
