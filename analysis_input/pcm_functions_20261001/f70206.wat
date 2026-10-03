  (func $f70206 (type $t435) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 f32) (param $p6 i32) (result i32)
    (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32) (local $l33 f32) (local $l34 f32) (local $l35 f32) (local $l36 f32) (local $l37 f32) (local $l38 f32) (local $l39 f32) (local $l40 f32) (local $l41 f32) (local $l42 f32) (local $l43 f32) (local $l44 f32) (local $l45 f32) (local $l46 f32) (local $l47 f32) (local $l48 f32) (local $l49 f32) (local $l50 f32) (local $l51 f32) (local $l52 f32) (local $l53 f32) (local $l54 f32) (local $l55 f32) (local $l56 f32) (local $l57 f32) (local $l58 f32) (local $l59 f32) (local $l60 f32) (local $l61 f32) (local $l62 f32) (local $l63 f32)
    global.get $g0
    i32.const 304
    i32.sub
    local.tee $l7
    global.set $g0
    local.get $p0
    f32.load offset=2168
    local.get $p3
    f32.load
    local.tee $l18
    local.get $p0
    i32.load offset=2188
    local.tee $l8
    f32.load
    f32.mul
    local.get $p3
    f32.load offset=4
    local.tee $l19
    local.get $l8
    f32.load offset=12
    f32.mul
    f32.add
    local.get $p3
    f32.load offset=8
    local.tee $l16
    local.get $l8
    f32.load offset=24
    f32.mul
    f32.add
    local.get $l8
    f32.load offset=36
    f32.add
    f32.sub
    local.get $p4
    f32.load
    local.tee $l17
    f32.mul
    local.get $p0
    i32.const 2172
    i32.add
    f32.load
    local.get $l18
    local.get $l8
    f32.load offset=4
    f32.mul
    local.get $l19
    local.get $l8
    f32.load offset=16
    f32.mul
    f32.add
    local.get $l16
    local.get $l8
    f32.load offset=28
    f32.mul
    f32.add
    local.get $l8
    f32.load offset=40
    f32.add
    f32.sub
    local.get $p4
    f32.load offset=4
    local.tee $l20
    f32.mul
    f32.add
    local.get $p0
    i32.const 2176
    i32.add
    f32.load
    local.get $l18
    local.get $l8
    f32.load offset=8
    f32.mul
    local.get $l19
    local.get $l8
    f32.load offset=20
    f32.mul
    f32.add
    local.get $l16
    local.get $l8
    f32.load offset=32
    f32.mul
    f32.add
    local.get $l8
    f32.load offset=44
    f32.add
    f32.sub
    local.get $p4
    f32.load offset=8
    local.tee $l18
    f32.mul
    f32.add
    f32.const 0x0p+0 (;=0;)
    f32.lt
    if $I0
      local.get $p4
      local.get $l18
      f32.neg
      local.tee $l18
      f32.store offset=8
      local.get $p4
      local.get $l20
      f32.neg
      local.tee $l20
      f32.store offset=4
      local.get $p4
      local.get $l17
      f32.neg
      local.tee $l17
      f32.store
    end
    local.get $p0
    i32.load offset=2192
    local.set $p3
    local.get $p0
    i32.load offset=2180
    local.tee $l9
    i32.load offset=68
    local.set $l10
    local.get $p0
    i32.load offset=2184
    local.tee $l8
    f32.load offset=20
    local.set $l16
    local.get $l8
    f32.load offset=16
    local.set $l21
    local.get $l8
    f32.load offset=32
    local.set $l22
    local.get $l8
    f32.load offset=28
    local.set $l24
    local.get $l8
    f32.load offset=12
    local.set $l23
    local.get $l8
    f32.load offset=24
    local.set $l33
    local.get $l7
    local.get $l8
    f32.load offset=4
    local.get $l20
    f32.neg
    local.tee $l19
    f32.mul
    local.get $l17
    local.get $l8
    f32.load
    f32.mul
    f32.sub
    local.get $l18
    local.get $l8
    f32.load offset=8
    f32.mul
    f32.sub
    f32.store offset=192
    local.get $l7
    local.get $l24
    local.get $l19
    f32.mul
    local.get $l17
    local.get $l33
    f32.mul
    f32.sub
    local.get $l18
    local.get $l22
    f32.mul
    f32.sub
    f32.store offset=200
    local.get $l7
    local.get $l21
    local.get $l19
    f32.mul
    local.get $l17
    local.get $l23
    f32.mul
    f32.sub
    local.get $l18
    local.get $l16
    f32.mul
    f32.sub
    f32.store offset=196
    local.get $l9
    local.get $p3
    local.get $l7
    i32.const 192
    i32.add
    local.get $l10
    call_indirect $__indirect_function_table (type $t3)
    local.set $l9
    local.get $p0
    i32.load offset=2180
    local.tee $l10
    i32.load offset=24
    local.tee $l12
    local.get $l9
    i32.const 20
    i32.mul
    i32.add
    local.set $l8
    block $B1 (result f32)
      local.get $p0
      i32.load8_u offset=2205
      local.tee $l13
      if $I2
        local.get $l8
        f32.load offset=12
        local.set $l16
        local.get $l8
        f32.load offset=8
        local.set $l17
        local.get $l8
        f32.load offset=4
        local.set $l18
        local.get $l8
        f32.load
        br $B1
      end
      local.get $l12
      local.get $l9
      i32.const 20
      i32.mul
      i32.add
      local.tee $l11
      f32.load offset=12
      f32.const 0x1p+0 (;=1;)
      local.get $p0
      i32.load offset=2192
      local.tee $p3
      f32.load offset=36
      local.get $l8
      f32.load
      local.tee $l17
      f32.mul
      local.get $p3
      f32.load offset=40
      local.get $l11
      f32.load offset=4
      local.tee $l18
      f32.mul
      f32.add
      local.get $p3
      f32.load offset=44
      local.get $l11
      f32.load offset=8
      local.tee $l19
      f32.mul
      f32.add
      local.tee $l20
      local.get $l20
      f32.mul
      local.get $l17
      local.get $p3
      f32.load offset=48
      f32.mul
      local.get $l18
      local.get $p3
      f32.load offset=52
      f32.mul
      f32.add
      local.get $l19
      local.get $p3
      f32.load offset=56
      f32.mul
      f32.add
      local.tee $l21
      local.get $l21
      f32.mul
      f32.add
      local.get $l17
      local.get $p3
      f32.load offset=60
      f32.mul
      local.get $l18
      local.get $p3
      i32.const -64
      i32.sub
      f32.load
      f32.mul
      f32.add
      local.get $l19
      local.get $p3
      f32.load offset=68
      f32.mul
      f32.add
      local.tee $l17
      local.get $l17
      f32.mul
      f32.add
      f32.sqrt
      f32.div
      local.tee $l19
      f32.mul
      local.set $l16
      local.get $l17
      local.get $l19
      f32.mul
      local.set $l17
      local.get $l21
      local.get $l19
      f32.mul
      local.set $l18
      local.get $l20
      local.get $l19
      f32.mul
    end
    local.set $l19
    local.get $l7
    local.get $l16
    f32.store offset=300
    local.get $l7
    local.get $l17
    f32.store offset=296
    local.get $l7
    local.get $l18
    f32.store offset=292
    local.get $l7
    local.get $l19
    f32.store offset=288
    local.get $p0
    i32.load offset=2184
    local.tee $l8
    i32.const 28
    i32.add
    local.tee $p3
    f32.load
    local.set $l16
    local.get $l8
    i32.const 16
    i32.add
    local.tee $l11
    f32.load
    local.set $l20
    local.get $l8
    f32.load offset=4
    local.set $l21
    local.get $l8
    f32.load offset=24
    local.set $l22
    local.get $l8
    f32.load
    local.set $l24
    local.get $l8
    f32.load offset=12
    local.set $l23
    local.get $l7
    local.get $l19
    local.get $l8
    f32.load offset=8
    f32.mul
    local.get $l18
    local.get $l8
    i32.const 20
    i32.add
    local.tee $l14
    f32.load
    f32.mul
    f32.add
    local.get $l17
    local.get $l8
    i32.const 32
    i32.add
    local.tee $l15
    f32.load
    f32.mul
    f32.add
    local.tee $l44
    f32.store offset=280
    local.get $l7
    local.get $l19
    local.get $l24
    f32.mul
    local.get $l18
    local.get $l23
    f32.mul
    f32.add
    local.get $l17
    local.get $l22
    f32.mul
    f32.add
    local.tee $l45
    f32.store offset=272
    local.get $l7
    local.get $l19
    local.get $l21
    f32.mul
    local.get $l18
    local.get $l20
    f32.mul
    f32.add
    local.get $l17
    local.get $l16
    f32.mul
    f32.add
    local.tee $l46
    f32.store offset=276
    local.get $p4
    f32.load offset=8
    local.set $l33
    local.get $p4
    f32.load offset=4
    local.set $l37
    local.get $p4
    f32.load
    local.set $l38
    local.get $p0
    i32.load offset=2188
    local.tee $p4
    f32.load offset=28
    local.set $l16
    local.get $p4
    f32.load offset=16
    local.set $l20
    local.get $p4
    f32.load offset=24
    local.set $l21
    local.get $p4
    f32.load
    local.set $l22
    local.get $p4
    f32.load offset=12
    local.set $l24
    local.get $p4
    f32.load offset=4
    local.set $l23
    local.get $l7
    local.get $p1
    f32.load
    local.tee $l17
    local.get $p4
    f32.load offset=8
    f32.mul
    local.get $p1
    f32.load offset=4
    local.tee $l18
    local.get $p4
    f32.load offset=20
    f32.mul
    f32.add
    local.get $p1
    f32.load offset=8
    local.tee $l19
    local.get $p4
    f32.load offset=32
    f32.mul
    f32.add
    local.tee $l47
    f32.store offset=264
    local.get $l7
    local.get $l17
    local.get $l23
    f32.mul
    local.get $l18
    local.get $l20
    f32.mul
    f32.add
    local.get $l19
    local.get $l16
    f32.mul
    f32.add
    local.tee $l48
    f32.store offset=260
    local.get $l7
    local.get $l17
    local.get $l22
    f32.mul
    local.get $l18
    local.get $l24
    f32.mul
    f32.add
    local.get $l19
    local.get $l21
    f32.mul
    f32.add
    local.tee $l49
    f32.store offset=256
    local.get $l7
    local.get $l38
    local.get $p5
    f32.neg
    f32.const 0x0p+0 (;=0;)
    local.get $p5
    f32.const 0x0p+0 (;=0;)
    f32.le
    select
    local.get $p0
    f32.load offset=2208
    f32.add
    local.tee $l34
    f32.mul
    local.tee $l16
    f32.store offset=240
    local.get $l7
    local.get $l37
    local.get $l34
    f32.mul
    local.tee $l20
    f32.store offset=244
    local.get $l7
    local.get $l33
    local.get $l34
    f32.mul
    local.tee $l21
    f32.store offset=248
    local.get $l7
    local.get $l8
    f32.load
    f32.store offset=192
    local.get $l7
    local.get $l8
    f32.load offset=4
    f32.store offset=196
    local.get $l7
    local.get $l8
    f32.load offset=8
    f32.store offset=200
    local.get $l7
    local.get $l8
    f32.load offset=12
    f32.store offset=204
    local.get $l7
    local.get $l11
    f32.load
    f32.store offset=208
    local.get $l7
    local.get $l14
    f32.load
    f32.store offset=212
    local.get $l7
    local.get $l8
    f32.load offset=24
    f32.store offset=216
    local.get $l7
    local.get $p3
    f32.load
    f32.store offset=220
    local.get $l7
    local.get $l15
    f32.load
    f32.store offset=224
    local.get $l7
    local.get $l8
    f32.load offset=36
    local.tee $l22
    f32.store offset=228
    local.get $l7
    i32.const 232
    i32.add
    local.tee $p4
    local.get $l8
    f32.load offset=40
    local.tee $l24
    f32.store
    local.get $l7
    i32.const 236
    i32.add
    local.tee $p3
    local.get $l8
    f32.load offset=44
    local.tee $l23
    f32.store
    local.get $p0
    i32.load offset=2212
    local.tee $l8
    f32.load offset=8
    local.set $l18
    local.get $l8
    f32.load offset=4
    local.set $l19
    local.get $l8
    f32.load
    local.set $p5
    local.get $l8
    f32.load offset=12
    local.set $l17
    local.get $p3
    local.get $l23
    local.get $l21
    f32.sub
    local.tee $l35
    f32.store
    local.get $p4
    local.get $l24
    local.get $l20
    f32.sub
    local.tee $l30
    f32.store
    local.get $l7
    local.get $l22
    local.get $l16
    f32.sub
    local.tee $l31
    f32.store offset=228
    local.get $p0
    i32.load offset=2216
    local.tee $l8
    f32.load offset=20
    local.set $l39
    local.get $l8
    f32.load offset=24
    local.set $l40
    local.get $l8
    f32.load offset=16
    local.set $l41
    local.get $l7
    local.get $p5
    local.get $l8
    f32.load offset=4
    local.tee $l20
    f32.mul
    local.tee $l50
    local.get $l18
    local.get $l8
    f32.load offset=12
    local.tee $l16
    f32.mul
    local.tee $l51
    local.get $l17
    local.get $l8
    f32.load offset=8
    local.tee $l21
    f32.mul
    local.tee $l52
    f32.sub
    local.get $l19
    local.get $l8
    f32.load
    local.tee $l22
    f32.mul
    local.tee $l53
    f32.sub
    f32.add
    local.tee $l23
    local.get $l18
    local.get $l22
    f32.mul
    local.tee $l54
    local.get $l19
    local.get $l16
    f32.mul
    local.tee $l55
    local.get $l17
    local.get $l20
    f32.mul
    local.tee $l56
    f32.sub
    local.get $p5
    local.get $l21
    f32.mul
    local.tee $l57
    f32.sub
    f32.add
    local.tee $l27
    local.get $l27
    f32.add
    local.tee $l36
    f32.mul
    local.tee $l25
    local.get $l18
    local.get $l21
    f32.mul
    local.get $l19
    local.get $l20
    f32.mul
    local.get $p5
    local.get $l22
    f32.mul
    local.get $l17
    local.get $l16
    f32.mul
    f32.add
    f32.add
    f32.add
    local.tee $l24
    local.get $l19
    local.get $l21
    f32.mul
    local.tee $l58
    local.get $p5
    local.get $l16
    f32.mul
    local.tee $l59
    local.get $l17
    local.get $l22
    f32.mul
    local.tee $l60
    f32.sub
    local.get $l18
    local.get $l20
    f32.mul
    local.tee $l61
    f32.sub
    f32.add
    local.tee $l32
    local.get $l32
    f32.add
    local.tee $l28
    f32.mul
    local.tee $l26
    f32.sub
    f32.store offset=172
    local.get $l7
    local.get $l25
    local.get $l26
    f32.add
    f32.store offset=164
    local.get $l7
    local.get $l16
    local.get $l16
    f32.mul
    f32.const -0x1p-1 (;=-0.5;)
    f32.add
    local.tee $l42
    local.get $l35
    local.get $l40
    f32.sub
    local.tee $l25
    local.get $l25
    f32.add
    local.tee $l25
    f32.mul
    local.get $l16
    local.get $l20
    local.get $l31
    local.get $l41
    f32.sub
    local.tee $l26
    local.get $l26
    f32.add
    local.tee $l26
    f32.mul
    local.get $l22
    local.get $l30
    local.get $l39
    f32.sub
    local.tee $l29
    local.get $l29
    f32.add
    local.tee $l29
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l21
    local.get $l29
    local.get $l20
    f32.neg
    f32.mul
    local.get $l22
    local.get $l26
    f32.mul
    f32.sub
    local.get $l21
    local.get $l25
    f32.mul
    f32.sub
    local.tee $l43
    f32.mul
    f32.sub
    f32.store offset=188
    local.get $l7
    local.get $l42
    local.get $l29
    f32.mul
    local.get $l16
    local.get $l22
    local.get $l25
    f32.mul
    local.get $l21
    local.get $l26
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l20
    local.get $l43
    f32.mul
    f32.sub
    f32.store offset=184
    local.get $l7
    f32.const 0x1p+0 (;=1;)
    local.get $l32
    local.get $l28
    f32.mul
    f32.sub
    local.tee $l32
    local.get $l27
    local.get $l36
    f32.mul
    local.tee $l62
    f32.sub
    f32.store offset=176
    local.get $l7
    local.get $l32
    local.get $l23
    local.get $l23
    local.get $l23
    f32.add
    local.tee $l32
    f32.mul
    local.tee $l63
    f32.sub
    f32.store offset=160
    local.get $l7
    local.get $l23
    local.get $l28
    f32.mul
    local.tee $l23
    local.get $l24
    local.get $l36
    f32.mul
    local.tee $l36
    f32.add
    f32.store offset=168
    local.get $l7
    local.get $l27
    local.get $l28
    f32.mul
    local.tee $l27
    local.get $l24
    local.get $l32
    f32.mul
    local.tee $l28
    f32.sub
    f32.store offset=156
    local.get $l7
    local.get $l23
    local.get $l36
    f32.sub
    f32.store offset=152
    local.get $l7
    local.get $l27
    local.get $l28
    f32.add
    f32.store offset=148
    local.get $l7
    local.get $l42
    local.get $l26
    f32.mul
    local.get $l16
    local.get $l21
    local.get $l29
    f32.mul
    local.get $l20
    local.get $l25
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l22
    local.get $l43
    f32.mul
    f32.sub
    f32.store offset=180
    local.get $l7
    f32.const 0x1p+0 (;=1;)
    local.get $l62
    f32.sub
    local.get $l63
    f32.sub
    f32.store offset=144
    local.get $l7
    local.get $l17
    local.get $l17
    f32.mul
    f32.const -0x1p-1 (;=-0.5;)
    f32.add
    local.tee $l28
    local.get $l40
    local.get $l35
    f32.sub
    local.tee $l16
    local.get $l16
    f32.add
    local.tee $l20
    f32.mul
    local.get $l17
    local.get $l19
    local.get $l41
    local.get $l31
    f32.sub
    local.tee $l16
    local.get $l16
    f32.add
    local.tee $l21
    f32.mul
    local.get $p5
    local.get $l39
    local.get $l30
    f32.sub
    local.tee $l16
    local.get $l16
    f32.add
    local.tee $l22
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l18
    local.get $l22
    local.get $l19
    f32.neg
    f32.mul
    local.get $p5
    local.get $l21
    f32.mul
    f32.sub
    local.get $l18
    local.get $l20
    f32.mul
    f32.sub
    local.tee $l25
    f32.mul
    f32.sub
    f32.store offset=140
    local.get $l7
    local.get $l28
    local.get $l22
    f32.mul
    local.get $l17
    local.get $p5
    local.get $l20
    f32.mul
    local.get $l18
    local.get $l21
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l19
    local.get $l25
    f32.mul
    f32.sub
    f32.store offset=136
    local.get $l7
    f32.const 0x1p+0 (;=1;)
    local.get $l61
    local.get $l60
    local.get $l59
    f32.sub
    local.get $l58
    f32.sub
    f32.add
    local.tee $l16
    local.get $l16
    local.get $l16
    f32.add
    local.tee $l23
    f32.mul
    f32.sub
    local.tee $l29
    local.get $l57
    local.get $l56
    local.get $l55
    f32.sub
    local.get $l54
    f32.sub
    f32.add
    local.tee $l27
    local.get $l27
    local.get $l27
    f32.add
    local.tee $l26
    f32.mul
    local.tee $l35
    f32.sub
    f32.store offset=128
    local.get $l7
    local.get $l53
    local.get $l52
    local.get $l51
    f32.sub
    local.get $l50
    f32.sub
    f32.add
    local.tee $l16
    local.get $l26
    f32.mul
    local.tee $l30
    local.get $l24
    local.get $l23
    f32.mul
    local.tee $l31
    f32.sub
    f32.store offset=124
    local.get $l7
    local.get $l30
    local.get $l31
    f32.add
    f32.store offset=116
    local.get $l7
    local.get $l29
    local.get $l16
    local.get $l16
    local.get $l16
    f32.add
    local.tee $l30
    f32.mul
    local.tee $l31
    f32.sub
    f32.store offset=112
    local.get $l7
    local.get $l28
    local.get $l21
    f32.mul
    local.get $l17
    local.get $l18
    local.get $l22
    f32.mul
    local.get $l19
    local.get $l20
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $p5
    local.get $l25
    f32.mul
    f32.sub
    f32.store offset=132
    local.get $l7
    local.get $l16
    local.get $l23
    f32.mul
    local.tee $l17
    local.get $l24
    local.get $l26
    f32.mul
    local.tee $l18
    f32.add
    f32.store offset=120
    local.get $l7
    local.get $l27
    local.get $l23
    f32.mul
    local.tee $l19
    local.get $l24
    local.get $l30
    f32.mul
    local.tee $p5
    f32.sub
    f32.store offset=108
    local.get $l7
    local.get $l17
    local.get $l18
    f32.sub
    f32.store offset=104
    local.get $l7
    local.get $l19
    local.get $p5
    f32.add
    f32.store offset=100
    local.get $l7
    f32.const 0x1p+0 (;=1;)
    local.get $l35
    f32.sub
    local.get $l31
    f32.sub
    f32.store offset=96
    local.get $l45
    local.get $l38
    f32.mul
    local.get $l46
    local.get $l37
    f32.mul
    f32.add
    local.get $l44
    local.get $l33
    f32.mul
    f32.add
    f32.abs
    local.set $l17
    local.get $l38
    local.get $l49
    f32.mul
    local.get $l37
    local.get $l48
    f32.mul
    f32.add
    local.get $l33
    local.get $l47
    f32.mul
    f32.add
    f32.abs
    local.set $l18
    local.get $l12
    local.get $l9
    i32.const 20
    i32.mul
    i32.add
    local.tee $l8
    i32.load8_u offset=18
    local.set $p4
    i32.const 0
    local.set $p3
    i32.const 0
    local.set $l9
    local.get $l13
    i32.eqz
    if $I3
      local.get $l7
      local.get $p4
      i32.const 12
      i32.mul
      i32.const 15
      i32.add
      i32.const 8176
      i32.and
      i32.sub
      local.tee $p3
      local.tee $l9
      global.set $g0
      local.get $l9
      local.get $p4
      i32.const 15
      i32.add
      i32.const 496
      i32.and
      i32.sub
      local.tee $l9
      global.set $g0
    end
    local.get $l7
    i32.const 92
    i32.add
    local.get $l7
    i32.const 88
    i32.add
    local.get $p3
    local.get $l9
    local.get $l13
    i32.const 0
    i32.ne
    local.get $l10
    i32.load offset=28
    local.get $l10
    i32.load offset=32
    local.get $l8
    i32.load16_u offset=16
    i32.add
    local.get $p4
    local.get $p0
    i32.load offset=2192
    call $f69921
    local.get $l7
    i32.const 3125790
    i32.load8_u
    i32.store8 offset=86
    local.get $l7
    i32.const 3125788
    i32.load16_u align=1
    i32.store16 offset=84
    local.get $l7
    i32.const 48
    i32.add
    local.get $l7
    i32.const 288
    i32.add
    call $f70172
    local.get $l7
    i32.const 8
    i32.add
    local.get $p1
    call $f70172
    local.get $l8
    i32.const 18
    i32.add
    local.set $p4
    block $B4
      block $B5
        local.get $l17
        local.get $l18
        f32.gt
        if $I6
          i32.const 1
          local.set $l8
          local.get $p4
          i32.load8_u
          local.get $l7
          i32.load offset=92
          local.get $l7
          i32.load offset=88
          local.get $l7
          i32.const 192
          i32.add
          local.get $l7
          i32.const 288
          i32.add
          local.get $l7
          i32.const 48
          i32.add
          i32.const 3
          local.get $p2
          local.get $l7
          i32.const 84
          i32.add
          local.get $p0
          i32.load offset=2188
          local.get $p1
          local.get $l7
          i32.const 8
          i32.add
          local.get $l7
          i32.const 272
          i32.add
          local.get $l7
          i32.const 144
          i32.add
          local.get $l7
          i32.const 96
          i32.add
          local.get $p6
          local.get $p0
          i32.load offset=2220
          i32.const 1
          local.get $l7
          i32.const 240
          i32.add
          local.get $l34
          call $f70173
          i32.eqz
          br_if $B5
          br $B4
        end
        i32.const 1
        local.set $l8
        i32.const 3
        local.get $p2
        local.get $l7
        i32.const 84
        i32.add
        local.get $p0
        i32.load offset=2188
        local.get $p1
        local.get $l7
        i32.const 8
        i32.add
        local.get $p4
        i32.load8_u
        local.get $l7
        i32.load offset=92
        local.get $l7
        i32.load offset=88
        local.get $l7
        i32.const 192
        i32.add
        local.get $l7
        i32.const 288
        i32.add
        local.get $l7
        i32.const 48
        i32.add
        local.get $l7
        i32.const 256
        i32.add
        local.get $l7
        i32.const 96
        i32.add
        local.get $l7
        i32.const 144
        i32.add
        local.get $p6
        local.get $p0
        i32.load offset=2220
        i32.const 0
        local.get $l7
        i32.const 240
        i32.add
        local.get $l34
        call $f70173
        br_if $B4
      end
      i32.const 0
      local.set $l8
    end
    local.get $l7
    i32.const 304
    i32.add
    global.set $g0
    local.get $l8)
