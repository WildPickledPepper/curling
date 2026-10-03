  (func $f70115 (type $t14) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 i32) (result i32)
    (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32)
    global.get $g0
    i32.const 288
    i32.sub
    local.tee $p6
    global.set $g0
    block $B0
      block $B1
        local.get $p0
        i32.load8_u offset=9
        i32.const 1
        i32.and
        if $I2
          local.get $p4
          local.get $p3
          local.get $p0
          i32.load8_u offset=12
          local.tee $l8
          select
          local.tee $l7
          f32.load offset=8
          local.set $l13
          local.get $l7
          f32.load
          local.set $l14
          local.get $l7
          f32.load offset=4
          local.set $l11
          local.get $p0
          i32.load offset=20
          local.tee $l7
          f32.load offset=40
          local.set $l10
          local.get $l7
          f32.load offset=28
          local.set $l12
          local.get $l7
          f32.load offset=16
          local.set $l15
          local.get $l7
          f32.load offset=36
          local.set $l19
          local.get $p2
          f32.load offset=8
          local.set $l21
          local.get $l7
          f32.load offset=24
          local.set $l22
          local.get $p2
          f32.load
          local.set $l16
          local.get $l7
          f32.load
          local.set $l17
          local.get $p2
          f32.load offset=4
          local.set $l18
          local.get $l7
          f32.load offset=12
          local.set $l20
          local.get $l7
          f32.load offset=4
          local.set $l23
          local.get $p6
          local.get $l7
          f32.load offset=44
          local.tee $l27
          local.get $l7
          f32.load offset=8
          local.tee $l24
          local.get $p3
          local.get $p4
          local.get $l8
          select
          local.tee $p2
          f32.load
          local.tee $l25
          f32.mul
          local.get $l7
          f32.load offset=20
          local.tee $l28
          local.get $p2
          f32.load offset=4
          local.tee $l26
          f32.mul
          f32.add
          local.get $l7
          f32.load offset=32
          local.tee $l29
          local.get $p2
          f32.load offset=8
          local.tee $l30
          f32.mul
          f32.add
          f32.add
          f32.store offset=80
          local.get $p6
          local.get $l10
          local.get $l23
          local.get $l25
          f32.mul
          local.get $l15
          local.get $l26
          f32.mul
          f32.add
          local.get $l12
          local.get $l30
          f32.mul
          f32.add
          f32.add
          f32.store offset=76
          local.get $p6
          local.get $l27
          local.get $l24
          local.get $l14
          f32.mul
          local.get $l28
          local.get $l11
          f32.mul
          f32.add
          local.get $l29
          local.get $l13
          f32.mul
          f32.add
          f32.add
          f32.store offset=68
          local.get $p6
          i32.const -64
          i32.sub
          local.get $l10
          local.get $l23
          local.get $l14
          f32.mul
          local.get $l15
          local.get $l11
          f32.mul
          f32.add
          local.get $l12
          local.get $l13
          f32.mul
          f32.add
          f32.add
          f32.store
          local.get $p6
          local.get $l19
          local.get $l16
          local.get $l17
          f32.mul
          local.get $l18
          local.get $l20
          f32.mul
          f32.add
          local.get $l21
          local.get $l22
          f32.mul
          f32.add
          f32.add
          f32.store offset=48
          local.get $p6
          local.get $l19
          local.get $l17
          local.get $l25
          f32.mul
          local.get $l20
          local.get $l26
          f32.mul
          f32.add
          local.get $l22
          local.get $l30
          f32.mul
          f32.add
          f32.add
          f32.store offset=72
          local.get $p6
          local.get $l19
          local.get $l17
          local.get $l14
          f32.mul
          local.get $l20
          local.get $l11
          f32.mul
          f32.add
          local.get $l22
          local.get $l13
          f32.mul
          f32.add
          f32.add
          f32.store offset=60
          local.get $p6
          local.get $l27
          local.get $l16
          local.get $l24
          f32.mul
          local.get $l18
          local.get $l28
          f32.mul
          f32.add
          local.get $l21
          local.get $l29
          f32.mul
          f32.add
          f32.add
          f32.store offset=56
          local.get $p6
          local.get $l10
          local.get $l16
          local.get $l23
          f32.mul
          local.get $l18
          local.get $l15
          f32.mul
          f32.add
          local.get $l21
          local.get $l12
          f32.mul
          f32.add
          f32.add
          f32.store offset=52
          local.get $p6
          i32.const 2139095039
          i32.store offset=144
          local.get $p6
          i32.const 48
          i32.add
          local.get $p0
          i32.load offset=48
          i32.const 48
          i32.add
          local.get $p0
          i32.load offset=52
          local.get $p0
          i32.const 164
          i32.add
          local.get $p0
          f32.load offset=24
          local.get $p6
          i32.const 144
          i32.add
          local.get $p0
          i32.load8_u offset=176
          i32.eqz
          call $f69954
          local.tee $l7
          if $I3
            local.get $p6
            f32.load offset=144
            local.tee $l13
            local.get $p0
            f32.load offset=24
            f32.le
            i32.eqz
            br_if $B1
            local.get $p0
            local.get $l13
            f32.store offset=24
            local.get $p5
            local.get $l13
            local.get $p0
            f32.load offset=16
            f32.mul
            f32.store
            local.get $p6
            f32.load offset=48
            local.set $l14
            local.get $p6
            f32.load offset=52
            local.set $l11
            local.get $p6
            f32.load offset=56
            local.set $l10
            local.get $p0
            i32.const 0
            i32.store offset=124
            local.get $p0
            local.get $l10
            f32.store offset=120
            local.get $p0
            local.get $l11
            f32.store offset=116
            local.get $p0
            local.get $l14
            f32.store offset=112
            local.get $p0
            i32.load offset=56
            local.tee $p2
            f32.load
            local.set $l12
            local.get $p2
            f32.load offset=4
            local.set $l15
            local.get $p2
            f32.load offset=8
            local.set $l19
            local.get $p0
            i32.const 0
            i32.store offset=140
            local.get $p0
            i32.const 1
            i32.store8 offset=10
            local.get $p0
            local.get $l19
            f32.neg
            f32.store offset=136
            local.get $p0
            local.get $l15
            f32.neg
            f32.store offset=132
            local.get $p0
            local.get $l12
            f32.neg
            f32.store offset=128
            local.get $p0
            local.get $p1
            i32.load offset=8
            i32.store offset=160
            local.get $p0
            local.get $l14
            f32.store offset=64
            local.get $p0
            local.get $l11
            f32.store offset=68
            local.get $p0
            local.get $l10
            f32.store offset=72
            local.get $p0
            local.get $p6
            f32.load offset=60
            f32.store offset=76
            local.get $p0
            local.get $p6
            f32.load offset=64
            f32.store offset=80
            local.get $p0
            local.get $p6
            f32.load offset=68
            f32.store offset=84
            local.get $p0
            local.get $p6
            f32.load offset=72
            f32.store offset=88
            local.get $p0
            local.get $p6
            f32.load offset=76
            f32.store offset=92
            local.get $p0
            local.get $p6
            f32.load offset=80
            f32.store offset=96
            local.get $l13
            f32.const 0x0p+0 (;=0;)
            f32.ne
            br_if $B1
            local.get $p0
            i32.const 1
            i32.store8 offset=11
          end
          local.get $l7
          i32.eqz
          local.set $l7
          br $B0
        end
        local.get $p6
        i32.const 0
        i32.store offset=224
        local.get $p0
        i32.load offset=20
        local.tee $l7
        f32.load offset=44
        local.tee $l10
        local.get $l7
        f32.load offset=8
        local.tee $l12
        local.get $p3
        local.get $p4
        local.get $p0
        i32.load8_u offset=12
        local.tee $l9
        select
        local.tee $l8
        f32.load
        local.tee $l13
        f32.mul
        local.get $l7
        f32.load offset=20
        local.tee $l15
        local.get $l8
        f32.load offset=4
        local.tee $l14
        f32.mul
        f32.add
        local.get $l7
        f32.load offset=32
        local.tee $l17
        local.get $l8
        f32.load offset=8
        local.tee $l11
        f32.mul
        f32.add
        f32.add
        local.set $l19
        local.get $l7
        f32.load offset=40
        local.tee $l18
        local.get $l7
        f32.load offset=4
        local.tee $l20
        local.get $l13
        f32.mul
        local.get $l7
        f32.load offset=16
        local.tee $l23
        local.get $l14
        f32.mul
        f32.add
        local.get $l7
        f32.load offset=28
        local.tee $l27
        local.get $l11
        f32.mul
        f32.add
        f32.add
        local.set $l21
        local.get $l7
        f32.load offset=36
        local.tee $l16
        local.get $l7
        f32.load
        local.tee $l24
        local.get $l13
        f32.mul
        local.get $l7
        f32.load offset=12
        local.tee $l25
        local.get $l14
        f32.mul
        f32.add
        local.get $l7
        f32.load offset=24
        local.tee $l28
        local.get $l11
        f32.mul
        f32.add
        f32.add
        local.set $l22
        local.get $l10
        local.get $l12
        local.get $p4
        local.get $p3
        local.get $l9
        select
        local.tee $l7
        f32.load
        local.tee $l11
        f32.mul
        local.get $l15
        local.get $l7
        f32.load offset=4
        local.tee $l26
        f32.mul
        f32.add
        local.get $l17
        local.get $l7
        f32.load offset=8
        local.tee $l29
        f32.mul
        f32.add
        f32.add
        local.set $l13
        local.get $l18
        local.get $l20
        local.get $l11
        f32.mul
        local.get $l23
        local.get $l26
        f32.mul
        f32.add
        local.get $l27
        local.get $l29
        f32.mul
        f32.add
        f32.add
        local.set $l14
        local.get $l16
        local.get $l24
        local.get $l11
        f32.mul
        local.get $l25
        local.get $l26
        f32.mul
        f32.add
        local.get $l28
        local.get $l29
        f32.mul
        f32.add
        f32.add
        local.set $l11
        local.get $p2
        f32.load
        local.tee $l26
        local.get $l24
        f32.mul
        local.get $p2
        f32.load offset=4
        local.tee $l24
        local.get $l25
        f32.mul
        f32.add
        local.get $p2
        f32.load offset=8
        local.tee $l25
        local.get $l28
        f32.mul
        f32.add
        local.get $l16
        f32.add
        local.set $l16
        local.get $l26
        local.get $l12
        f32.mul
        local.get $l24
        local.get $l15
        f32.mul
        f32.add
        local.get $l25
        local.get $l17
        f32.mul
        f32.add
        local.get $l10
        f32.add
        local.set $l17
        local.get $l26
        local.get $l20
        f32.mul
        local.get $l24
        local.get $l23
        f32.mul
        f32.add
        local.get $l25
        local.get $l27
        f32.mul
        f32.add
        local.get $l18
        f32.add
        local.set $l18
        local.get $p0
        i32.load8_u offset=176
        i32.eqz
        if $I4
          local.get $l17
          local.get $l13
          f32.sub
          local.tee $l10
          local.get $l21
          local.get $l14
          f32.sub
          local.tee $l12
          f32.mul
          local.get $l18
          local.get $l14
          f32.sub
          local.tee $l15
          local.get $l19
          local.get $l13
          f32.sub
          local.tee $l20
          f32.mul
          f32.sub
          local.get $p0
          f32.load offset=144
          f32.mul
          local.get $l16
          local.get $l11
          f32.sub
          local.tee $l23
          local.get $l20
          f32.mul
          local.get $l10
          local.get $l22
          local.get $l11
          f32.sub
          local.tee $l20
          f32.mul
          f32.sub
          local.get $p0
          f32.load offset=148
          f32.mul
          f32.add
          local.get $l15
          local.get $l20
          f32.mul
          local.get $l23
          local.get $l12
          f32.mul
          f32.sub
          local.get $p0
          f32.load offset=152
          f32.mul
          f32.add
          f32.const 0x0p+0 (;=0;)
          f32.ge
          br_if $B1
        end
        local.get $p6
        i64.const 0
        i64.store offset=216
        local.get $p6
        i64.const 0
        i64.store offset=208
        local.get $p0
        i32.load offset=48
        local.tee $l7
        f32.load offset=52
        local.set $l10
        local.get $l7
        f32.load offset=56
        local.set $l12
        local.get $l7
        f32.load offset=48
        local.set $l15
        local.get $p6
        i32.const 0
        i32.store offset=204
        local.get $p6
        local.get $l12
        f32.store offset=200
        local.get $p6
        local.get $l10
        f32.store offset=196
        local.get $p6
        i32.const 0
        i32.store8 offset=176
        local.get $p6
        i32.const 3
        i32.store offset=172
        local.get $p6
        i64.const 0
        i64.store offset=144
        local.get $p6
        i64.const 0
        i64.store offset=152
        local.get $p6
        local.get $l15
        f32.store offset=192
        local.get $p6
        local.get $l15
        local.get $l10
        local.get $l10
        local.get $l15
        f32.ge
        select
        local.tee $l10
        local.get $l12
        local.get $l10
        local.get $l12
        f32.le
        select
        local.tee $l10
        f32.const 0x1.99999ap-5 (;=0.05;)
        f32.mul
        local.tee $l12
        f32.store offset=168
        local.get $p6
        local.get $l12
        f32.store offset=164
        local.get $p6
        local.get $l10
        f32.const 0x1.333334p-3 (;=0.15;)
        f32.mul
        f32.store offset=160
        local.get $p6
        i32.const 0
        i32.store offset=140
        local.get $p6
        local.get $l19
        f32.store offset=136
        local.get $p6
        local.get $l21
        f32.store offset=132
        local.get $p6
        local.get $l22
        f32.store offset=128
        local.get $p6
        i32.const 0
        i32.store offset=124
        local.get $p6
        local.get $l13
        f32.store offset=120
        local.get $p6
        local.get $l14
        f32.store offset=116
        local.get $p6
        local.get $l11
        f32.store offset=112
        local.get $p6
        i32.const 0
        i32.store offset=108
        local.get $p6
        local.get $l17
        f32.store offset=104
        local.get $p6
        local.get $l18
        f32.store offset=100
        local.get $p6
        i32.const 0
        i32.store8 offset=80
        local.get $p6
        i64.const 23613931519
        i64.store offset=72
        local.get $p6
        i32.const 0
        i32.store offset=60
        local.get $p6
        i64.const 9187343235540844544
        i64.store offset=64
        local.get $p6
        local.get $l16
        f32.store offset=96
        local.get $p6
        local.get $l16
        local.get $l11
        f32.add
        local.get $l22
        f32.add
        f32.const 0x1.55553ep-2 (;=0.333333;)
        f32.mul
        local.tee $l10
        f32.store offset=48
        local.get $p6
        local.get $l18
        local.get $l14
        f32.add
        local.get $l21
        f32.add
        f32.const 0x1.55553ep-2 (;=0.333333;)
        f32.mul
        local.tee $l12
        f32.store offset=52
        local.get $p6
        local.get $l17
        local.get $l13
        f32.add
        local.get $l19
        f32.add
        f32.const 0x1.55553ep-2 (;=0.333333;)
        f32.mul
        local.tee $l15
        f32.store offset=56
        local.get $p6
        i32.const 3132108
        i32.store offset=24
        local.get $p6
        local.get $p6
        i32.const 48
        i32.add
        i32.store offset=28
        local.get $p6
        i32.const 3132536
        i32.store offset=16
        local.get $p6
        local.get $p6
        i32.const 144
        i32.add
        i32.store offset=20
        local.get $p6
        i32.const 0
        i32.store offset=12
        local.get $p6
        local.get $l15
        local.get $p6
        f32.load offset=152
        f32.sub
        f32.store offset=8
        local.get $p6
        local.get $l12
        local.get $p6
        f32.load offset=148
        f32.sub
        f32.store offset=4
        local.get $p6
        local.get $l10
        local.get $p6
        f32.load offset=144
        f32.sub
        f32.store
        block $B5 (result i32)
          local.get $p6
          i32.const 24
          i32.add
          local.get $p6
          i32.const 16
          i32.add
          local.get $p6
          local.get $p6
          i32.const 208
          i32.add
          local.get $p0
          i32.const 144
          i32.add
          local.get $p6
          i32.const 240
          i32.add
          local.get $p6
          i32.const 256
          i32.add
          local.get $p6
          i32.const 272
          i32.add
          local.get $p0
          f32.load offset=60
          call $f70481
          i32.eqz
          if $I6
            i32.const 1
            local.set $l7
            i32.const 0
            br $B5
          end
          local.get $p6
          f32.load offset=240
          local.set $l10
          local.get $p0
          local.get $p6
          i64.load offset=272
          i64.store offset=112
          local.get $p0
          local.get $p6
          i64.load offset=280
          i64.store offset=120
          local.get $p6
          local.get $p6
          i64.load offset=256
          i64.store offset=32
          local.get $p6
          local.get $p6
          i64.load offset=264
          i64.store offset=40
          local.get $p0
          i32.const 1
          i32.store8 offset=10
          local.get $p0
          local.get $p1
          i32.load offset=8
          i32.store offset=160
          local.get $l10
          local.get $p6
          f32.load offset=224
          f32.le
          if $I7
            local.get $p0
            i32.const 1
            i32.store8 offset=11
            i32.const 0
            local.set $l7
            local.get $p5
            i32.const 0
            i32.store
            local.get $p0
            local.get $p6
            i64.load offset=232
            i64.store offset=40
            local.get $p0
            local.get $p6
            i64.load offset=224
            i64.store offset=32
            local.get $p0
            i32.const 0
            i32.store offset=24
            local.get $p0
            i32.load offset=56
            local.tee $p2
            f32.load
            local.set $l13
            local.get $p2
            f32.load offset=4
            local.set $l14
            local.get $p2
            f32.load offset=8
            local.set $l11
            local.get $p0
            i32.const 0
            i32.store offset=140
            local.get $p0
            local.get $l11
            f32.neg
            f32.store offset=136
            local.get $p0
            local.get $l14
            f32.neg
            f32.store offset=132
            local.get $p0
            local.get $l13
            f32.neg
            f32.store offset=128
            i32.const 0
            br $B5
          end
          local.get $p0
          i32.const 0
          i32.store offset=156
          local.get $p0
          local.get $l10
          local.get $p0
          f32.load offset=24
          f32.mul
          local.tee $l12
          f32.store offset=24
          local.get $p0
          local.get $l10
          local.get $p0
          f32.load offset=144
          f32.mul
          f32.store offset=144
          local.get $p0
          local.get $l10
          local.get $p0
          f32.load offset=32
          f32.mul
          f32.store offset=32
          local.get $p0
          i32.const 148
          i32.add
          local.tee $l7
          local.get $l10
          local.get $l7
          f32.load
          f32.mul
          f32.store
          local.get $p0
          i32.const 152
          i32.add
          local.tee $l7
          local.get $l10
          local.get $l7
          f32.load
          f32.mul
          f32.store
          local.get $p0
          local.get $p6
          i64.load offset=40
          i64.store offset=136
          local.get $p0
          local.get $p6
          i64.load offset=32
          i64.store offset=128
          local.get $l12
          local.get $p0
          f32.load offset=16
          f32.mul
          local.tee $l10
          local.get $p5
          f32.load
          f32.lt
          if $I8
            local.get $p5
            local.get $l10
            f32.store
          end
          local.get $p0
          local.get $l16
          f32.store offset=64
          local.get $p0
          local.get $l19
          f32.store offset=96
          local.get $p0
          local.get $l21
          f32.store offset=92
          local.get $p0
          local.get $l22
          f32.store offset=88
          local.get $p0
          local.get $l13
          f32.store offset=84
          local.get $p0
          local.get $l14
          f32.store offset=80
          local.get $p0
          local.get $l11
          f32.store offset=76
          local.get $p0
          local.get $l17
          f32.store offset=72
          local.get $p0
          local.get $l18
          f32.store offset=68
          i32.const 1
          local.set $l7
          i32.const 1
        end
        i32.eqz
        br_if $B0
      end
      i32.const 1
      local.set $l7
    end
    local.get $p6
    i32.const 288
    i32.add
    global.set $g0
    local.get $l7)
