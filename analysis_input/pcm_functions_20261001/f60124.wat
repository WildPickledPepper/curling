  (func $f60124 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 f32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f64) (local $l12 f64)
    global.get $g0
    i32.const 240
    i32.sub
    local.tee $p1
    global.set $g0
    i32.const 4674461
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3748808
      call $f1661
      i32.const 3792480
      call $f1661
      i32.const 3792500
      call $f1661
      i32.const 3792544
      call $f1661
      i32.const 3792572
      call $f1661
      i32.const 3792588
      call $f1661
      i32.const 3751540
      call $f1661
      i32.const 3772052
      call $f1661
      i32.const 3772056
      call $f1661
      i32.const 3773132
      call $f1661
      i32.const 3752504
      call $f1661
      i32.const 3753376
      call $f1661
      i32.const 3857972
      call $f1661
      i32.const 3847196
      call $f1661
      i32.const 3820972
      call $f1661
      i32.const 3816140
      call $f1661
      i32.const 3821460
      call $f1661
      i32.const 3837344
      call $f1661
      i32.const 3835896
      call $f1661
      i32.const 3857968
      call $f1661
      i32.const 3835928
      call $f1661
      i32.const 3828708
      call $f1661
      i32.const 3821464
      call $f1661
      i32.const 3816136
      call $f1661
      i32.const 3853200
      call $f1661
      i32.const 4674461
      i32.const 1
      i32.store8
    end
    local.get $p1
    i64.const 0
    i64.store offset=232
    local.get $p1
    i64.const 0
    i64.store offset=224
    local.get $p1
    i64.const 0
    i64.store offset=216
    local.get $p1
    i64.const 0
    i64.store offset=208
    local.get $p1
    i64.const 0
    i64.store offset=200
    local.get $p1
    i32.const 0
    i32.store offset=196
    local.get $p1
    i32.const 0
    i32.store offset=192
    local.get $p1
    i64.const 0
    i64.store offset=184
    local.get $p1
    i32.const 0
    i32.store offset=180
    block $B1
      local.get $p0
      i32.load8_u offset=117
      i32.eqz
      br_if $B1
      local.get $p0
      i32.load8_u offset=264
      i32.eqz
      br_if $B1
      local.get $p0
      i32.load offset=260
      i32.const 3792500
      i32.load
      call $f34548
      i32.load8_u offset=16
      br_if $B1
      local.get $p0
      i32.load offset=260
      local.set $l2
      i32.const 3753376
      i32.load
      local.tee $l3
      i32.load offset=116
      i32.eqz
      if $I2
        local.get $l3
        call $f65192
      end
      local.get $l2
      i32.const 0
      i32.const 0
      call $f54398
      i32.eqz
      br_if $B1
      local.get $p0
      i32.load8_u offset=184
      br_if $B1
      local.get $p0
      i32.load8_u offset=112
      br_if $B1
      i32.const 3748808
      i32.load
      local.tee $l2
      i32.load offset=116
      i32.eqz
      if $I3
        local.get $l2
        call $f65192
      end
      i32.const 3828708
      i32.load
      i32.const 0
      call $f42976
      local.get $p1
      i32.const 136
      i32.add
      local.get $p0
      i32.load offset=260
      i32.const 3792572
      i32.load
      call $f34548
      i32.const 0
      call $f32519
      local.get $p1
      f32.load offset=144
      local.set $l7
      local.get $p1
      i32.const 136
      i32.add
      local.get $p0
      i32.load offset=260
      i32.const 3792572
      i32.load
      call $f34548
      i32.const 0
      call $f32519
      local.get $p1
      i32.const 200
      i32.add
      local.get $l7
      f32.neg
      f64.promote_f32
      local.get $p1
      f32.load offset=136
      f32.neg
      f64.promote_f32
      i32.const 0
      call $f61037
      i32.const 3820972
      i32.load
      i32.const 0
      call $f54416
      i32.const 3792588
      i32.load
      call $f34548
      i32.load8_u offset=24
      local.set $l2
      f32.const -0x1.a36e2ep-13 (;=-0.0002;)
      f32.const 0x1.a36e2ep-13 (;=0.0002;)
      i32.const 0
      call $f54300
      local.set $l7
      local.get $p1
      i32.const 168
      i32.add
      local.tee $l3
      local.get $p1
      i32.const 208
      i32.add
      local.tee $l4
      i64.load
      i64.store
      local.get $p1
      local.get $p1
      i64.load offset=200
      i64.store offset=160
      local.get $p1
      i32.const 136
      i32.add
      local.get $p0
      i32.load offset=260
      i32.const 3792572
      i32.load
      call $f34548
      i32.const 0
      call $f32522
      local.get $p1
      local.get $l3
      i64.load
      i64.store offset=80
      local.get $p1
      local.get $p1
      i64.load offset=160
      i64.store offset=72
      local.get $p1
      i32.const 136
      i32.add
      local.get $l7
      f32.const 0x1.3a92a4p-11 (;=0.0006;)
      f32.const 0x1.0624dep-10 (;=0.001;)
      local.get $l2
      select
      f32.add
      f64.promote_f32
      local.get $p1
      i32.const 72
      i32.add
      local.get $p1
      f32.load offset=140
      f64.promote_f32
      f64.const 0x1.0624dep-10 (;=0.001;)
      i32.const 0
      call $f59956
      local.get $p1
      i32.const 224
      i32.add
      local.tee $l2
      local.get $p1
      i64.load offset=144
      i64.store
      local.get $p1
      i32.const 232
      i32.add
      local.tee $l3
      local.get $p1
      i64.load offset=152
      i64.store
      local.get $p1
      local.get $p1
      i64.load offset=136
      i64.store offset=216
      local.get $l2
      f64.load
      local.set $l11
      local.get $p1
      f64.load offset=216
      local.set $l12
      local.get $p0
      i32.load offset=260
      i32.const 3792572
      i32.load
      call $f34548
      local.set $l5
      local.get $p1
      i32.const 128
      i32.add
      local.tee $l6
      local.get $l12
      f32.demote_f64
      f32.neg
      local.tee $l7
      f32.store
      local.get $p1
      i32.const -64
      i32.sub
      local.get $l6
      i32.load
      i32.store
      local.get $p1
      i32.const 0
      i32.store offset=124
      local.get $p1
      local.get $l11
      f32.demote_f64
      f32.neg
      local.tee $l8
      f32.store offset=120
      local.get $p1
      local.get $p1
      i64.load offset=120
      i64.store offset=56
      local.get $l5
      local.get $p1
      i32.const 56
      i32.add
      i32.const 0
      call $f32521
      local.get $p0
      i32.load offset=260
      i32.const 3792572
      i32.load
      call $f34548
      local.set $l5
      local.get $p1
      i32.const 0
      i32.store offset=112
      local.get $p1
      i32.const 0
      i32.store offset=48
      local.get $p1
      i32.const 0
      i32.store offset=104
      local.get $p1
      local.get $l3
      f64.load
      f32.demote_f64
      f32.store offset=108
      local.get $p1
      local.get $p1
      i64.load offset=104
      i64.store offset=40
      local.get $l5
      local.get $p1
      i32.const 40
      i32.add
      i32.const 0
      call $f32524
      local.get $p1
      i32.const 200
      i32.add
      i32.const 0
      call $f50678
      local.set $l5
      local.get $l4
      i32.const 0
      call $f50678
      local.set $l4
      i32.const 3847196
      i32.load
      local.get $l5
      i32.const 3816140
      i32.load
      local.get $l4
      i32.const 0
      call $f53874
      local.set $l4
      i32.const 3748808
      i32.load
      local.tee $l5
      i32.load offset=116
      i32.eqz
      if $I4
        local.get $l5
        call $f65192
      end
      local.get $l4
      i32.const 0
      call $f42976
      local.get $p1
      i32.const 1065353216
      i32.store offset=196
      local.get $p1
      i32.const 196
      i32.add
      i32.const 0
      call $f56977
      local.set $l4
      i32.const 3835896
      i32.load
      local.get $l4
      i32.const 0
      call $f53732
      i32.const 0
      call $f42976
      local.get $p1
      i32.const 1053609165
      i32.store offset=196
      local.get $p1
      i32.const 196
      i32.add
      i32.const 0
      call $f56977
      local.set $l4
      i32.const 3835928
      i32.load
      local.get $l4
      i32.const 0
      call $f53732
      i32.const 0
      call $f42976
      local.get $p1
      i32.const 216
      i32.add
      i32.const 0
      call $f50678
      local.set $l4
      local.get $l2
      i32.const 0
      call $f50678
      local.set $l2
      i32.const 3857972
      i32.load
      local.get $l4
      i32.const 3816136
      i32.load
      local.get $l2
      i32.const 0
      call $f53874
      i32.const 0
      call $f42976
      local.get $l3
      i32.const 0
      call $f50678
      local.set $l2
      i32.const 3857968
      i32.load
      local.get $l2
      i32.const 0
      call $f53732
      i32.const 0
      call $f42976
      local.get $p1
      local.get $l7
      f32.store offset=192
      local.get $p1
      i32.const 0
      i32.store offset=188
      local.get $p1
      local.get $l8
      f32.store offset=184
      local.get $p1
      i32.const 184
      i32.add
      i32.const 0
      i32.const 0
      call $f54067
      local.set $l2
      i32.const 3853200
      i32.load
      local.get $l2
      i32.const 0
      call $f53732
      i32.const 0
      call $f42976
    end
    block $B5
      local.get $p0
      i32.load8_u offset=112
      i32.eqz
      br_if $B5
      local.get $p0
      i32.load8_u offset=148
      i32.eqz
      br_if $B5
      local.get $p0
      i32.load offset=144
      i32.const 1
      i32.eq
      if $I6
        block $B7
          block $B8
            local.get $p0
            i32.load offset=124
            local.tee $l2
            i32.load offset=24
            i32.eqz
            if $I9
              local.get $l2
              i32.load offset=8
              local.set $l2
              local.get $p0
              i32.load offset=240
              local.set $l3
              i32.const 3752504
              i32.load
              local.tee $l4
              i32.load offset=116
              i32.eqz
              br_if $B8
              br $B7
            end
            local.get $l2
            i32.load offset=8
            local.set $l2
            local.get $p0
            i32.load offset=244
            local.set $l3
            i32.const 3752504
            i32.load
            local.tee $l4
            i32.load offset=116
            br_if $B7
          end
          local.get $l4
          call $f65192
        end
        local.get $p0
        local.get $l3
        block $B10 (result i32)
          local.get $l2
          f64.convert_i32_s
          f64.const 0x1p-1 (;=0.5;)
          f64.mul
          f64.floor
          local.tee $l11
          f64.abs
          f64.const 0x1p+31 (;=2.14748e+09;)
          f64.lt
          if $I11
            local.get $l11
            i32.trunc_f64_s
            br $B10
          end
          i32.const -2147483648
        end
        i32.const 3773132
        i32.load
        call $f2903
        i32.store offset=260
        i32.const 3821464
        i32.load
        i32.const 0
        call $f54416
        i32.const 3792544
        i32.load
        call $f34548
        local.get $p0
        i32.load offset=260
        i32.const 0
        call $f54401
        i32.store offset=16
        local.get $p0
        i32.load offset=212
        i32.const 0
        call $f54401
        local.set $l3
        local.get $p1
        local.get $p0
        i32.const 224
        i32.add
        local.tee $l2
        i32.load
        i32.store offset=32
        local.get $p1
        local.get $p0
        i64.load offset=216 align=4
        i64.store offset=24
        local.get $l3
        local.get $p1
        i32.const 24
        i32.add
        i32.const 0
        call $f54626
        local.get $p1
        i32.const 136
        i32.add
        local.get $p0
        i32.load offset=212
        i32.const 0
        call $f54401
        i32.const 0
        call $f54624
        local.get $l2
        local.get $p1
        i32.load offset=144
        i32.store
        local.get $p0
        local.get $p1
        i64.load offset=136
        i64.store offset=216 align=4
        local.get $p1
        i32.const 160
        i32.add
        local.get $p0
        i32.load offset=260
        i32.const 0
        call $f54401
        i32.const 0
        call $f54624
        local.get $p1
        f32.load offset=160
        local.set $l7
        local.get $p1
        f32.load offset=164
        local.set $l8
        local.get $p0
        i32.const 236
        i32.add
        local.tee $l3
        local.get $p1
        f32.load offset=168
        local.get $l2
        f32.load
        f32.sub
        f32.store
        local.get $p0
        i32.const 232
        i32.add
        local.tee $l2
        local.get $l8
        local.get $p0
        f32.load offset=220
        f32.sub
        f32.store
        local.get $p0
        local.get $l7
        local.get $p0
        f32.load offset=216
        f32.sub
        f32.store offset=228
        local.get $p0
        i32.load offset=212
        i32.const 0
        call $f54401
        local.set $l4
        local.get $p1
        i32.const 160
        i32.add
        local.get $p0
        i32.load offset=260
        i32.const 0
        call $f54401
        i32.const 0
        call $f54624
        local.get $p1
        f32.load offset=160
        local.set $l7
        local.get $p1
        f32.load offset=164
        local.set $l8
        local.get $l2
        f32.load
        local.set $l9
        local.get $p0
        f32.load offset=228
        local.set $l10
        local.get $p1
        i32.const 96
        i32.add
        local.tee $l2
        local.get $p1
        f32.load offset=168
        local.get $l3
        f32.load
        f32.sub
        f32.store
        local.get $p1
        local.get $l2
        i32.load
        i32.store offset=16
        local.get $p1
        local.get $l8
        local.get $l9
        f32.sub
        f32.store offset=92
        local.get $p1
        local.get $l7
        local.get $l10
        f32.sub
        f32.store offset=88
        local.get $p1
        local.get $p1
        i64.load offset=88
        i64.store offset=8
        local.get $l4
        local.get $p1
        i32.const 8
        i32.add
        i32.const 0
        call $f54626
        i32.const 3821460
        i32.load
        i32.const 0
        call $f54416
        i32.const 3792480
        i32.load
        call $f34548
        local.set $l2
        local.get $p1
        i32.const 1
        i32.store offset=160
        i32.const 3751540
        i32.load
        local.get $p1
        i32.const 160
        i32.add
        call $f1675
        local.set $l3
        local.get $l2
        i32.const 3837344
        i32.load
        local.get $l3
        i32.const 0
        call $f54371
      end
      block $B12
        local.get $p0
        i32.load offset=140
        local.tee $l3
        i32.load offset=12
        local.tee $l2
        i32.eqz
        br_if $B12
        local.get $p0
        i32.load offset=144
        local.tee $l4
        local.get $l2
        i32.ge_s
        br_if $B12
        local.get $p1
        local.get $l3
        local.get $l4
        i32.const 3772056
        i32.load
        call $f2903
        i32.store offset=180
        local.get $p0
        local.get $p0
        i32.load offset=144
        i32.const 1
        i32.add
        i32.store offset=144
        local.get $p0
        local.get $p1
        i32.const 180
        i32.add
        local.get $p1
        call $f60062
        br $B5
      end
      i32.const 0
      local.set $l3
      local.get $p0
      i32.const 0
      i32.store offset=144
      local.get $p0
      i32.const 0
      i32.store8 offset=148
      block $B13
        local.get $p0
        i32.load offset=124
        local.tee $l2
        i32.load offset=8
        local.tee $l4
        i32.const 15
        i32.le_s
        if $I14
          local.get $l4
          i32.const 1
          i32.add
          local.set $l3
          br $B13
        end
        local.get $l2
        local.get $l2
        i32.load offset=12
        i32.const 1
        i32.add
        i32.store offset=12
      end
      local.get $l2
      local.get $l3
      i32.store offset=8
      local.get $p0
      local.get $p0
      i32.const 136
      i32.add
      local.get $p1
      call $f60062
      local.get $p0
      local.get $p1
      call $f60085
    end
    local.get $p1
    i32.const 240
    i32.add
    global.set $g0)
