  (func $f70454 (type $t6) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32)
    (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 i32) (local $l17 i32) (local $l18 i32) (local $l19 i32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32) (local $l33 f32) (local $l34 f32) (local $l35 f32) (local $l36 f32) (local $l37 f32) (local $l38 f32) (local $l39 f32) (local $l40 f32) (local $l41 f32) (local $l42 f32)
    global.get $g0
    i32.const 160
    i32.sub
    local.tee $l5
    global.set $g0
    block $B0
      local.get $p4
      local.get $p4
      i32.const 12
      i32.add
      local.get $p1
      local.get $p2
      f32.const 0x1p+0 (;=1;)
      local.get $l5
      i32.const 156
      i32.add
      local.get $l5
      i32.const 152
      i32.add
      call $f69911
      i32.eqz
      br_if $B0
      local.get $p0
      i32.load offset=12
      local.tee $l11
      i32.load offset=40
      local.set $l6
      local.get $l11
      i32.load offset=44
      local.set $l9
      local.get $p0
      i32.load offset=16
      f32.load offset=8
      local.set $l37
      local.get $p2
      f32.load
      local.set $l23
      local.get $p2
      f32.load offset=4
      local.set $l26
      local.get $p2
      f32.load offset=8
      local.set $l25
      local.get $p0
      f32.load
      local.set $l20
      local.get $p1
      f32.load
      local.set $l24
      local.get $p1
      f32.load offset=4
      local.set $l27
      local.get $l5
      f32.load offset=152
      local.set $l28
      local.get $l5
      f32.load offset=156
      local.set $l29
      local.get $l5
      local.get $p1
      f32.load offset=8
      local.tee $l34
      local.get $p0
      f32.load offset=8
      local.tee $l22
      f32.mul
      f32.store offset=144
      local.get $l5
      local.get $l27
      f32.store offset=140
      local.get $l5
      local.get $l24
      local.get $l20
      f32.mul
      f32.store offset=136
      local.get $l5
      local.get $l22
      local.get $l25
      f32.const 0x1p+0 (;=1;)
      f32.mul
      f32.mul
      local.tee $l30
      f32.store offset=128
      local.get $l5
      local.get $l26
      f32.const 0x1p+0 (;=1;)
      f32.mul
      local.tee $l31
      f32.store offset=124
      local.get $l5
      local.get $l20
      local.get $l23
      f32.const 0x1p+0 (;=1;)
      f32.mul
      f32.mul
      local.tee $l32
      f32.store offset=120
      local.get $l22
      local.get $l34
      local.get $l25
      local.get $l28
      f32.mul
      f32.add
      f32.mul
      local.get $l22
      local.get $l34
      local.get $l29
      local.get $l25
      f32.mul
      f32.add
      f32.mul
      local.tee $l21
      f32.sub
      local.tee $l22
      f32.abs
      local.set $l36
      f32.const 0x1p+0 (;=1;)
      f32.const -0x1p+0 (;=-1;)
      local.get $l20
      local.get $l24
      local.get $l23
      local.get $l28
      f32.mul
      f32.add
      f32.mul
      local.get $l20
      local.get $l24
      local.get $l29
      local.get $l23
      f32.mul
      f32.add
      f32.mul
      local.tee $l25
      f32.sub
      local.tee $l23
      f32.const 0x0p+0 (;=0;)
      f32.ge
      select
      local.set $l34
      local.get $l21
      f32.const 0x1.ad7f2ap-24 (;=1e-07;)
      local.get $l21
      f32.const 0x1.ad7f2ap-24 (;=1e-07;)
      f32.gt
      select
      local.set $l24
      local.get $l9
      i32.const 1
      i32.sub
      f32.convert_i32_s
      f32.const 0x1.fffffcp-1 (;=1;)
      f32.mul
      f32.const 0x0p+0 (;=0;)
      f32.add
      local.set $l33
      local.get $l25
      f32.const 0x1.ad7f2ap-24 (;=1e-07;)
      f32.gt
      local.set $p1
      local.get $l6
      i32.const 1
      i32.sub
      f32.convert_i32_s
      f32.const 0x1.fffffcp-1 (;=1;)
      f32.mul
      local.set $l20
      local.get $l31
      local.get $l31
      f32.mul
      local.get $l32
      local.get $l32
      f32.mul
      f32.add
      local.get $l30
      local.get $l30
      f32.mul
      f32.add
      f32.sqrt
      local.set $l38
      block $B1 (result i32)
        f32.const 0x1p+0 (;=1;)
        f32.const -0x1p+0 (;=-1;)
        local.get $l22
        f32.const 0x0p+0 (;=0;)
        f32.ge
        select
        local.tee $l39
        f32.abs
        f32.const 0x1p+31 (;=2.14748e+09;)
        f32.lt
        if $I2
          local.get $l39
          i32.trunc_f32_s
          br $B1
        end
        i32.const -2147483648
      end
      local.set $p4
      local.get $l23
      f32.abs
      local.set $l41
      local.get $l25
      f32.const 0x1.ad7f2ap-24 (;=1e-07;)
      local.get $p1
      select
      local.set $l35
      local.get $l20
      f32.const 0x0p+0 (;=0;)
      f32.add
      local.set $l40
      local.get $l36
      f32.const 0x1.b7cdfep-34 (;=1e-10;)
      f32.lt
      local.set $p1
      local.get $l39
      f32.const 0x1.b7cdfep-34 (;=1e-10;)
      f32.mul
      local.set $l20
      local.get $l24
      local.get $l33
      f32.lt
      local.set $p2
      local.get $l38
      f32.const 0x1.79ca1p-67 (;=1e-20;)
      f32.gt
      local.set $p0
      block $B3 (result i32)
        local.get $l34
        f32.abs
        f32.const 0x1p+31 (;=2.14748e+09;)
        f32.lt
        if $I4
          local.get $l34
          i32.trunc_f32_s
          br $B3
        end
        i32.const -2147483648
      end
      local.set $l8
      local.get $l41
      f32.const 0x1.b7cdfep-34 (;=1e-10;)
      f32.lt
      local.set $l7
      local.get $l34
      f32.const 0x1.b7cdfep-34 (;=1e-10;)
      f32.mul
      local.set $l36
      local.get $l35
      local.get $l40
      f32.lt
      local.set $l10
      local.get $l20
      local.get $l22
      local.get $p1
      select
      local.set $l20
      local.get $l24
      local.get $l33
      local.get $p2
      select
      local.set $l24
      local.get $p0
      if $I5
        local.get $l5
        local.get $l30
        f32.const 0x1p+0 (;=1;)
        local.get $l38
        f32.div
        local.tee $l22
        f32.mul
        f32.store offset=128
        local.get $l5
        local.get $l31
        local.get $l22
        f32.mul
        f32.store offset=124
        local.get $l5
        local.get $l32
        local.get $l22
        f32.mul
        f32.store offset=120
      end
      local.get $l36
      local.get $l23
      local.get $l7
      select
      local.set $l23
      local.get $l35
      local.get $l40
      local.get $l10
      select
      local.set $l22
      block $B6 (result i32)
        local.get $l24
        f32.floor
        local.tee $l30
        local.get $l24
        f32.ceil
        local.tee $l31
        local.get $l20
        f32.const 0x0p+0 (;=0;)
        f32.gt
        select
        local.tee $l32
        f32.abs
        f32.const 0x1p+31 (;=2.14748e+09;)
        f32.lt
        if $I7
          local.get $l32
          i32.trunc_f32_s
          br $B6
        end
        i32.const -2147483648
      end
      local.set $p2
      block $B8 (result i32)
        local.get $l22
        f32.floor
        local.tee $l32
        local.get $l22
        f32.ceil
        local.tee $l33
        local.get $l23
        f32.const 0x0p+0 (;=0;)
        f32.gt
        local.tee $p1
        select
        local.tee $l35
        f32.abs
        f32.const 0x1p+31 (;=2.14748e+09;)
        f32.lt
        if $I9
          local.get $l35
          i32.trunc_f32_s
          br $B8
        end
        i32.const -2147483648
      end
      local.set $p0
      local.get $l33
      f32.const 0x1p+0 (;=1;)
      f32.add
      local.get $l33
      local.get $l22
      local.get $l33
      f32.eq
      select
      local.get $l32
      f32.const -0x1p+0 (;=-1;)
      f32.add
      local.get $l32
      local.get $l22
      local.get $l32
      f32.eq
      select
      local.get $p1
      select
      local.set $l22
      local.get $l29
      local.get $l26
      f32.mul
      local.get $l27
      f32.add
      local.set $l33
      local.get $l27
      local.get $l26
      local.get $l28
      f32.mul
      f32.add
      local.set $l26
      local.get $l31
      f32.const 0x1p+0 (;=1;)
      f32.add
      local.get $l31
      local.get $l24
      local.get $l31
      f32.eq
      select
      local.get $l30
      f32.const -0x1p+0 (;=-1;)
      f32.add
      local.get $l30
      local.get $l24
      local.get $l30
      f32.eq
      select
      local.get $l20
      f32.const 0x0p+0 (;=0;)
      f32.gt
      select
      local.get $l21
      f32.sub
      local.get $l20
      f32.div
      local.set $l29
      local.get $l22
      local.get $l25
      f32.sub
      local.get $l23
      f32.div
      local.tee $l22
      f32.const 0x0p+0 (;=0;)
      f32.lt
      if $I10
        f32.const 0x1.ad7f2ap-24 (;=1e-07;)
        local.get $l23
        f32.div
        f32.abs
        local.set $l22
      end
      f32.const 0x1.ad7f2ap-24 (;=1e-07;)
      local.get $l20
      f32.div
      f32.abs
      local.get $l29
      local.get $l29
      f32.const 0x0p+0 (;=0;)
      f32.lt
      select
      local.set $l29
      local.get $p4
      i32.const 31
      i32.shr_s
      local.get $p4
      i32.and
      local.set $l15
      local.get $l33
      local.get $l26
      local.get $l33
      f32.sub
      local.tee $l35
      f32.const 0x0p+0 (;=0;)
      f32.mul
      f32.add
      local.set $l21
      f32.const 0x1p+0 (;=1;)
      local.get $l20
      f32.abs
      f32.div
      local.set $l41
      f32.const 0x1p+0 (;=1;)
      local.get $l23
      f32.abs
      f32.div
      local.set $l42
      local.get $l8
      i32.const 1
      local.get $p4
      i32.sub
      i32.const 2
      i32.div_s
      local.tee $p1
      i32.sub
      i32.const 2
      i32.shl
      local.get $l5
      i32.add
      i32.const 104
      i32.add
      local.set $l16
      local.get $p1
      local.get $l8
      i32.add
      local.tee $l7
      i32.const 2
      i32.shl
      local.get $l5
      i32.add
      i32.const 100
      i32.add
      local.set $l17
      local.get $p1
      local.get $l8
      i32.sub
      i32.const 2
      i32.shl
      local.get $l5
      i32.add
      i32.const 100
      i32.add
      local.set $l18
      i32.const 0
      local.get $l7
      i32.sub
      i32.const 2
      i32.shl
      local.get $l5
      i32.add
      i32.const 104
      i32.add
      local.set $l19
      local.get $l6
      f32.convert_i32_s
      local.set $l40
      local.get $l9
      f32.convert_i32_s
      local.set $l36
      local.get $p2
      f32.convert_i32_s
      local.set $l27
      local.get $p0
      f32.convert_i32_s
      local.set $l28
      loop $L11
        local.get $l5
        local.get $l37
        local.get $l11
        i32.load offset=60
        local.tee $p1
        local.get $p0
        local.get $l9
        i32.mul
        local.get $p2
        i32.add
        local.tee $l6
        i32.const 2
        i32.shl
        i32.add
        i32.load16_s
        f32.convert_i32_s
        f32.mul
        local.tee $l20
        f32.store offset=96
        local.get $l5
        local.get $l37
        local.get $p1
        local.get $p4
        local.get $l6
        i32.add
        i32.const 2
        i32.shl
        i32.add
        i32.load16_s
        f32.convert_i32_s
        f32.mul
        local.tee $l23
        f32.store offset=100
        local.get $l5
        local.get $l37
        local.get $p1
        local.get $p0
        local.get $l8
        i32.add
        local.tee $l6
        local.get $l9
        i32.mul
        local.get $p2
        i32.add
        local.tee $l7
        i32.const 2
        i32.shl
        i32.add
        i32.load16_s
        f32.convert_i32_s
        f32.mul
        local.tee $l26
        f32.store offset=104
        local.get $l5
        local.get $l37
        local.get $p1
        local.get $p4
        local.get $l7
        i32.add
        i32.const 2
        i32.shl
        i32.add
        i32.load16_s
        f32.convert_i32_s
        f32.mul
        local.tee $l25
        f32.store offset=108
        block $B12
          local.get $l21
          local.get $l33
          local.get $l35
          local.get $l22
          local.get $l29
          local.get $l22
          local.get $l29
          f32.lt
          local.tee $l7
          select
          local.tee $l32
          f32.mul
          f32.add
          local.tee $l24
          local.get $l21
          local.get $l24
          f32.lt
          select
          f32.const -0x1.a36e2ep-14 (;=-0.0001;)
          f32.add
          local.get $l20
          local.get $l23
          local.get $l20
          local.get $l23
          f32.gt
          select
          local.tee $l30
          local.get $l26
          local.get $l25
          local.get $l25
          local.get $l26
          f32.lt
          select
          local.tee $l31
          local.get $l30
          local.get $l31
          f32.gt
          select
          f32.gt
          br_if $B12
          local.get $l21
          local.get $l24
          local.get $l21
          local.get $l24
          f32.gt
          select
          f32.const 0x1.a36e2ep-14 (;=0.0001;)
          f32.add
          local.get $l20
          local.get $l23
          local.get $l20
          local.get $l23
          f32.lt
          select
          local.tee $l21
          local.get $l26
          local.get $l25
          local.get $l25
          local.get $l26
          f32.gt
          select
          local.tee $l20
          local.get $l20
          local.get $l21
          f32.gt
          select
          f32.lt
          br_if $B12
          local.get $l16
          f32.load
          local.set $l23
          local.get $l17
          f32.load
          local.set $l26
          local.get $l19
          f32.load
          local.set $l25
          local.get $l5
          local.get $l18
          f32.load
          f32.store offset=84
          local.get $l5
          local.get $l27
          local.get $l39
          local.get $l27
          f32.add
          local.tee $l21
          local.get $l21
          local.get $l27
          f32.gt
          select
          local.tee $l30
          f32.store offset=88
          local.get $l5
          local.get $l28
          local.get $l34
          local.get $l28
          f32.add
          local.tee $l20
          local.get $l20
          local.get $l28
          f32.gt
          select
          local.tee $l31
          f32.store offset=80
          local.get $l5
          local.get $l27
          local.get $l21
          local.get $l21
          local.get $l27
          f32.lt
          select
          local.tee $l21
          f32.store offset=72
          local.get $l5
          local.get $l25
          f32.store offset=68
          local.get $l5
          local.get $l31
          f32.store offset=64
          local.get $l5
          local.get $l30
          f32.store offset=56
          local.get $l5
          local.get $l26
          f32.store offset=52
          local.get $l5
          local.get $l28
          local.get $l20
          local.get $l20
          local.get $l28
          f32.lt
          select
          local.tee $l20
          f32.store offset=48
          local.get $l5
          local.get $l21
          f32.store offset=40
          local.get $l5
          local.get $l23
          f32.store offset=36
          local.get $l5
          local.get $l20
          f32.store offset=32
          block $B13 (result i32)
            local.get $p1
            local.get $p2
            local.get $l15
            i32.add
            local.get $l6
            local.get $p0
            local.get $l8
            i32.const 0
            i32.lt_s
            select
            local.get $l9
            i32.mul
            i32.add
            i32.const 2
            i32.shl
            local.tee $l13
            i32.add
            i32.load8_s offset=2
            i32.const 0
            i32.lt_s
            if $I14
              local.get $l5
              i32.const 48
              i32.add
              local.set $l12
              local.get $l5
              i32.const -64
              i32.sub
              local.set $l14
              local.get $l5
              i32.const 80
              i32.add
              local.set $l10
              local.get $l5
              i32.const 32
              i32.add
              br $B13
            end
            local.get $l5
            i32.const 80
            i32.add
            local.set $l12
            local.get $l5
            i32.const 32
            i32.add
            local.set $l14
            local.get $l5
            i32.const -64
            i32.sub
            local.set $l10
            local.get $l5
            i32.const 48
            i32.add
          end
          local.set $p1
          local.get $l5
          i32.const 2139095039
          i32.store offset=28
          local.get $l5
          i32.const 2139095039
          i32.store offset=24
          block $B15 (result i32)
            block $B16
              local.get $l5
              i32.const 136
              i32.add
              local.get $l5
              i32.const 120
              i32.add
              local.get $l12
              local.get $l10
              local.get $p1
              local.get $l5
              i32.const 28
              i32.add
              local.get $l5
              i32.const 20
              i32.add
              local.get $l5
              i32.const 16
              i32.add
              i32.const 0
              f32.const 0x1.a36e2ep-14 (;=0.0001;)
              call $f70472
              i32.eqz
              br_if $B16
              local.get $l5
              f32.load offset=28
              local.tee $l21
              f32.const 0x0p+0 (;=0;)
              f32.ge
              i32.eqz
              br_if $B16
              local.get $l21
              local.get $l38
              f32.le
              i32.eqz
              br_if $B16
              i32.const 0
              local.get $l11
              i32.load offset=60
              local.get $l13
              i32.add
              i32.load8_u offset=2
              i32.const 127
              i32.and
              i32.const 127
              i32.ne
              br_if $B15
              drop
            end
            local.get $l5
            i32.const 2139095039
            i32.store offset=28
            i32.const 1
          end
          local.set $l12
          block $B17 (result i32)
            block $B18
              local.get $l5
              i32.const 136
              i32.add
              local.get $l5
              i32.const 120
              i32.add
              local.get $l14
              local.get $p1
              local.get $l10
              local.get $l5
              i32.const 24
              i32.add
              local.get $l5
              i32.const 12
              i32.add
              local.get $l5
              i32.const 8
              i32.add
              i32.const 0
              f32.const 0x1.a36e2ep-14 (;=0.0001;)
              call $f70472
              i32.eqz
              br_if $B18
              local.get $l5
              f32.load offset=24
              local.tee $l21
              f32.const 0x0p+0 (;=0;)
              f32.ge
              i32.eqz
              br_if $B18
              local.get $l21
              local.get $l38
              f32.le
              i32.eqz
              br_if $B18
              i32.const 0
              local.get $l11
              i32.load offset=60
              local.get $l13
              i32.add
              i32.load8_u offset=3
              i32.const 127
              i32.and
              i32.const 127
              i32.ne
              br_if $B17
              drop
            end
            f32.const 0x1.fffffep+127 (;=3.40282e+38;)
            local.set $l21
            i32.const 1
          end
          local.set $p1
          local.get $l12
          local.get $l5
          f32.load offset=28
          local.get $l21
          f32.le
          i32.eqz
          i32.or
          i32.eqz
          if $I19
            local.get $p3
            i32.const 1
            i32.store8
            br $B0
          end
          local.get $p1
          local.get $l21
          local.get $l5
          f32.load offset=28
          f32.le
          i32.eqz
          i32.or
          br_if $B12
          local.get $p3
          i32.const 1
          i32.store8
          br $B0
        end
        block $B20
          local.get $l7
          if $I21
            local.get $l6
            local.get $l8
            i32.add
            local.tee $p1
            i32.const 0
            i32.lt_s
            br_if $B0
            local.get $p1
            f32.convert_i32_s
            local.get $l40
            f32.ge
            br_if $B0
            local.get $l42
            local.get $l22
            f32.add
            local.set $l22
            local.get $l34
            local.get $l28
            f32.add
            local.set $l28
            local.get $l6
            local.set $p0
            br $B20
          end
          local.get $p2
          local.get $p4
          i32.add
          local.tee $p2
          local.get $p4
          i32.add
          local.tee $p1
          i32.const 0
          i32.lt_s
          br_if $B0
          local.get $p1
          f32.convert_i32_s
          local.get $l36
          f32.ge
          br_if $B0
          local.get $l41
          local.get $l29
          f32.add
          local.set $l29
          local.get $l39
          local.get $l27
          f32.add
          local.set $l27
        end
        local.get $l24
        local.set $l21
        local.get $l32
        f32.const 0x1.fff2e4p-1 (;=0.9999;)
        f32.lt
        br_if $L11
      end
    end
    local.get $l5
    i32.const 160
    i32.add
    global.set $g0)
