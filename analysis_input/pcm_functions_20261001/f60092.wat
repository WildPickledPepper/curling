  (func $f60092 (type $t72) (param $p0 i32) (param $p1 f32) (param $p2 f32) (param $p3 f32) (param $p4 i32)
    (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 f64) (local $l12 f32) (local $l13 f32) (local $l14 i64)
    global.get $g0
    i32.const 144
    i32.sub
    local.tee $p4
    global.set $g0
    i32.const 4674431
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3748808
      call $f1661
      i32.const 3792480
      call $f1661
      i32.const 3792496
      call $f1661
      i32.const 3792544
      call $f1661
      i32.const 3792572
      call $f1661
      i32.const 3751540
      call $f1661
      i32.const 3773132
      call $f1661
      i32.const 3752504
      call $f1661
      i32.const 3755140
      call $f1661
      i32.const 3833220
      call $f1661
      i32.const 3821460
      call $f1661
      i32.const 3828076
      call $f1661
      i32.const 3837344
      call $f1661
      i32.const 3821464
      call $f1661
      i32.const 3834636
      call $f1661
      i32.const 4674431
      i32.const 1
      i32.store8
    end
    block $B1
      local.get $p0
      i32.load8_u offset=208
      i32.eqz
      if $I2
        i32.const 3748808
        i32.load
        local.tee $p0
        i32.load offset=116
        i32.eqz
        if $I3
          local.get $p0
          call $f65192
        end
        i32.const 3833220
        i32.load
        i32.const 0
        call $f42984
        br $B1
      end
      local.get $p0
      i32.const 0
      i32.store8 offset=208
      local.get $p4
      local.get $p1
      f32.store offset=128
      i32.const 3755140
      i32.load
      local.get $p4
      i32.const 128
      i32.add
      call $f1675
      local.set $l6
      local.get $p4
      local.get $p2
      f32.store offset=112
      i32.const 3755140
      i32.load
      local.get $p4
      i32.const 112
      i32.add
      call $f1675
      local.set $l5
      local.get $p4
      local.get $p3
      f32.store offset=140
      i32.const 3755140
      i32.load
      local.get $p4
      i32.const 140
      i32.add
      call $f1675
      local.set $l7
      i32.const 3834636
      i32.load
      local.get $l6
      local.get $l5
      local.get $l7
      i32.const 0
      call $f53877
      local.set $l6
      i32.const 3748808
      i32.load
      local.tee $l5
      i32.load offset=116
      i32.eqz
      if $I4
        local.get $l5
        call $f65192
      end
      local.get $l6
      i32.const 0
      call $f42976
      local.get $p3
      f32.const -0x1.f66666p+3 (;=-15.7;)
      f32.lt
      local.set $l6
      local.get $p3
      f32.const 0x1.f66666p+3 (;=15.7;)
      f32.min
      local.set $p3
      local.get $p2
      f32.const -0x1.1d70a4p+1 (;=-2.23;)
      f32.lt
      local.set $l5
      local.get $p2
      f32.const 0x1.1d70a4p+1 (;=2.23;)
      f32.min
      local.set $p2
      local.get $p1
      f32.const 0x1.a36e2ep-14 (;=0.0001;)
      f32.lt
      local.set $l7
      local.get $p1
      f32.const 0x1.8p+2 (;=6;)
      f32.min
      local.set $p1
      block $B5
        block $B6
          local.get $p0
          i32.load offset=124
          local.tee $l8
          i32.load offset=24
          i32.eqz
          if $I7
            local.get $l8
            i32.load offset=8
            local.set $l8
            local.get $p0
            i32.load offset=240
            local.set $l9
            i32.const 3752504
            i32.load
            local.tee $l10
            i32.load offset=116
            i32.eqz
            br_if $B6
            br $B5
          end
          local.get $l8
          i32.load offset=8
          local.set $l8
          local.get $p0
          i32.load offset=244
          local.set $l9
          i32.const 3752504
          i32.load
          local.tee $l10
          i32.load offset=116
          br_if $B5
        end
        local.get $l10
        call $f65192
      end
      f32.const -0x1.f66666p+3 (;=-15.7;)
      local.get $p3
      local.get $l6
      select
      local.set $p3
      f32.const -0x1.1d70a4p+1 (;=-2.23;)
      local.get $p2
      local.get $l5
      select
      local.set $p2
      f32.const 0x1.a36e2ep-14 (;=0.0001;)
      local.get $p1
      local.get $l7
      select
      local.set $p1
      local.get $l9
      block $B8 (result i32)
        local.get $l8
        f64.convert_i32_s
        f64.const 0x1p-1 (;=0.5;)
        f64.mul
        f64.floor
        local.tee $l11
        f64.abs
        f64.const 0x1p+31 (;=2.14748e+09;)
        f64.lt
        if $I9
          local.get $l11
          i32.trunc_f64_s
          br $B8
        end
        i32.const -2147483648
      end
      i32.const 3773132
      i32.load
      call $f2903
      local.tee $l6
      i32.const 1
      i32.const 0
      call $f54405
      local.get $p0
      i32.load offset=212
      i32.const 0
      call $f54401
      local.set $l7
      local.get $p4
      local.get $p0
      i32.const 224
      i32.add
      local.tee $l5
      i32.load
      i32.store offset=56
      local.get $p4
      local.get $p0
      i64.load offset=216 align=4
      i64.store offset=48
      local.get $l7
      local.get $p4
      i32.const 48
      i32.add
      i32.const 0
      call $f54626
      local.get $p4
      i32.const 128
      i32.add
      local.get $p0
      i32.load offset=212
      i32.const 0
      call $f54401
      i32.const 0
      call $f54624
      local.get $l5
      local.get $p4
      i32.load offset=136
      i32.store
      local.get $p0
      local.get $p4
      i64.load offset=128
      i64.store offset=216 align=4
      local.get $p4
      i32.const 112
      i32.add
      local.get $l6
      i32.const 0
      call $f54401
      i32.const 0
      call $f54624
      local.get $p4
      f32.load offset=112
      local.set $l12
      local.get $p4
      f32.load offset=116
      local.set $l13
      local.get $p0
      local.get $p4
      f32.load offset=120
      local.get $l5
      f32.load
      f32.sub
      f32.store offset=236
      local.get $p0
      local.get $l13
      local.get $p0
      f32.load offset=220
      f32.sub
      f32.store offset=232
      local.get $p0
      local.get $l12
      local.get $p0
      f32.load offset=216
      f32.sub
      f32.store offset=228
      i32.const 3821460
      i32.load
      i32.const 0
      call $f54416
      i32.const 3792480
      i32.load
      call $f34548
      local.set $l5
      local.get $p4
      i32.const 1
      i32.store offset=140
      i32.const 3751540
      i32.load
      local.get $p4
      i32.const 140
      i32.add
      call $f1675
      local.set $l7
      local.get $l5
      i32.const 3837344
      i32.load
      local.get $l7
      i32.const 0
      call $f54371
      local.get $p4
      i32.const 112
      i32.add
      local.get $l6
      i32.const 3792572
      i32.load
      call $f34548
      local.tee $l5
      i32.const 0
      call $f32544
      local.get $p4
      i32.const 104
      i32.add
      local.tee $l7
      local.get $p4
      f32.load offset=120
      local.get $p2
      f32.sub
      f32.store
      local.get $p4
      local.get $l7
      i32.load
      i32.store offset=40
      local.get $p4
      local.get $p4
      i64.load offset=112
      local.tee $l14
      i64.store offset=96
      local.get $p4
      local.get $l14
      i64.store offset=32
      local.get $l5
      local.get $p4
      i32.const 32
      i32.add
      i32.const 0
      call $f32546
      i32.const 3821464
      i32.load
      i32.const 0
      call $f54416
      i32.const 3792544
      i32.load
      call $f34548
      local.get $l6
      i32.const 0
      call $f54401
      i32.store offset=16
      local.get $l6
      i32.const 3792496
      i32.load
      call $f34548
      i32.const 0
      call $f32557
      f32.const 0x0p+0 (;=0;)
      i32.const 0
      call $f32512
      local.get $l6
      i32.const 3792496
      i32.load
      call $f34548
      i32.const 0
      call $f32557
      f32.const 0x0p+0 (;=0;)
      i32.const 0
      call $f32511
      local.get $l6
      i32.const 3792572
      i32.load
      call $f34548
      local.set $l5
      local.get $p4
      i64.const 0
      i64.store offset=84 align=4
      local.get $p4
      local.get $p4
      i32.load offset=88
      i32.store offset=24
      local.get $p4
      local.get $p1
      f32.store offset=80
      local.get $p4
      local.get $p4
      i64.load offset=80
      i64.store offset=16
      local.get $l5
      local.get $p4
      i32.const 16
      i32.add
      i32.const 0
      call $f32521
      local.get $l6
      i32.const 3792572
      i32.load
      call $f34548
      local.set $l5
      local.get $p4
      i32.const 0
      i32.store offset=72
      local.get $p4
      i32.const 0
      i32.store offset=8
      local.get $p4
      local.get $p3
      f32.store offset=68
      local.get $p4
      i32.const 0
      i32.store offset=64
      local.get $p4
      local.get $p4
      i64.load offset=64
      i64.store
      local.get $l5
      local.get $p4
      i32.const 0
      call $f32524
      local.get $p0
      local.get $l6
      i32.store offset=260
      local.get $p0
      i32.const 1
      i32.store8 offset=264
      i32.const 3748808
      i32.load
      local.tee $p0
      i32.load offset=116
      i32.eqz
      if $I10
        local.get $p0
        call $f65192
      end
      i32.const 3828076
      i32.load
      i32.const 0
      call $f42976
    end
    local.get $p4
    i32.const 144
    i32.add
    global.set $g0)