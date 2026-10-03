  (func $f60202 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 f32) (local $l5 f64) (local $l6 f64) (local $l7 f64)
    global.get $g0
    i32.const 144
    i32.sub
    local.tee $p1
    global.set $g0
    i32.const 4674525
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3792500
      call $f1661
      i32.const 3792572
      call $f1661
      i32.const 3792588
      call $f1661
      i32.const 3753376
      call $f1661
      i32.const 3745900
      call $f1661
      i32.const 3813948
      call $f1661
      i32.const 3820972
      call $f1661
      i32.const 4674525
      i32.const 1
      i32.store8
    end
    local.get $p1
    i64.const 0
    i64.store offset=136
    local.get $p1
    i64.const 0
    i64.store offset=128
    block $B1
      local.get $p0
      i32.load8_u offset=89
      i32.eqz
      br_if $B1
      local.get $p0
      i32.load8_u offset=216
      i32.eqz
      br_if $B1
      local.get $p0
      i32.load offset=212
      i32.const 3792500
      i32.load
      call $f34548
      i32.load8_u offset=16
      br_if $B1
      local.get $p0
      i32.load offset=212
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
      i32.load8_u offset=156
      br_if $B1
      local.get $p0
      i32.load8_u offset=84
      br_if $B1
      local.get $p1
      i32.const 88
      i32.add
      local.get $p0
      i32.load offset=212
      i32.const 3792572
      i32.load
      call $f34548
      i32.const 0
      call $f32519
      local.get $p1
      f32.load offset=96
      local.set $l4
      local.get $p1
      i32.const 88
      i32.add
      local.get $p0
      i32.load offset=212
      i32.const 3792572
      i32.load
      call $f34548
      i32.const 0
      call $f32519
      local.get $p1
      i32.const 128
      i32.add
      local.get $l4
      f32.neg
      f64.promote_f32
      local.get $p1
      f32.load offset=88
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
      local.set $l4
      local.get $p1
      i32.const 120
      i32.add
      local.tee $l3
      local.get $p1
      i64.load offset=136
      i64.store
      local.get $p1
      local.get $p1
      i64.load offset=128
      i64.store offset=112
      local.get $p1
      i32.const 88
      i32.add
      local.get $p0
      i32.load offset=212
      i32.const 3792572
      i32.load
      call $f34548
      i32.const 0
      call $f32522
      local.get $p1
      local.get $l3
      i64.load
      i64.store offset=48
      local.get $p1
      local.get $p1
      i64.load offset=112
      i64.store offset=40
      local.get $p1
      i32.const 88
      i32.add
      local.get $l4
      f32.const 0x1.3a92a4p-11 (;=0.0006;)
      f32.const 0x1.0624dep-10 (;=0.001;)
      local.get $l2
      select
      f32.add
      f64.promote_f32
      local.get $p1
      i32.const 40
      i32.add
      local.get $p1
      f32.load offset=92
      f64.promote_f32
      f64.const 0x1.0624dep-10 (;=0.001;)
      i32.const 0
      call $f59956
      local.get $p1
      f64.load offset=104
      local.set $l5
      local.get $p1
      f64.load offset=96
      local.set $l6
      local.get $p1
      f64.load offset=88
      local.set $l7
      local.get $p0
      i32.load offset=212
      i32.const 3792572
      i32.load
      call $f34548
      local.set $l2
      local.get $p1
      i32.const 80
      i32.add
      local.tee $l3
      local.get $l7
      f32.demote_f64
      f32.neg
      f32.store
      local.get $p1
      local.get $l3
      i32.load
      i32.store offset=32
      local.get $p1
      i32.const 0
      i32.store offset=76
      local.get $p1
      local.get $l6
      f32.demote_f64
      f32.neg
      f32.store offset=72
      local.get $p1
      local.get $p1
      i64.load offset=72
      i64.store offset=24
      local.get $l2
      local.get $p1
      i32.const 24
      i32.add
      i32.const 0
      call $f32521
      local.get $p0
      i32.load offset=212
      i32.const 3792572
      i32.load
      call $f34548
      local.set $l2
      local.get $p1
      i32.const -64
      i32.sub
      i32.const 0
      i32.store
      local.get $p1
      i32.const 0
      i32.store offset=16
      local.get $p1
      local.get $l5
      f32.demote_f64
      f32.store offset=60
      local.get $p1
      i32.const 0
      i32.store offset=56
      local.get $p1
      local.get $p1
      i64.load offset=56
      i64.store offset=8
      local.get $l2
      local.get $p1
      i32.const 8
      i32.add
      i32.const 0
      call $f32524
      local.get $p1
      i32.const 3745900
      i32.load
      i32.const 32
      call $f1052
      local.tee $l3
      i32.store offset=88
      local.get $p0
      local.get $p1
      i32.const 88
      i32.add
      local.get $p0
      call $f60180
      i32.const 0
      local.set $l2
      loop $L3
        local.get $p0
        i32.load offset=124
        local.get $l3
        local.get $l2
        i32.const 2
        i32.shl
        i32.add
        i32.const 16
        i32.add
        i32.const 0
        call $f56977
        i32.const 0
        call $f2192
        drop
        local.get $p0
        i32.load offset=124
        i32.const 3813948
        i32.load
        i32.const 0
        call $f2192
        drop
        local.get $l2
        i32.const 1
        i32.add
        local.tee $l2
        i32.const 32
        i32.ne
        br_if $L3
      end
    end
    local.get $p0
    i32.load offset=212
    local.set $l2
    i32.const 3753376
    i32.load
    local.tee $l3
    i32.load offset=116
    i32.eqz
    if $I4
      local.get $l3
      call $f65192
    end
    block $B5
      local.get $l2
      i32.const 0
      i32.const 0
      call $f54398
      i32.eqz
      br_if $B5
      local.get $p0
      i32.load8_u offset=84
      br_if $B5
      local.get $p0
      i32.load offset=212
      i32.const 3792500
      i32.load
      call $f34548
      i32.load8_u offset=16
      i32.eqz
      br_if $B5
      local.get $p0
      i32.load8_u offset=216
      i32.eqz
      br_if $B5
      local.get $p1
      i32.const 3745900
      i32.load
      i32.const 32
      call $f1052
      local.tee $l3
      i32.store offset=112
      local.get $p0
      local.get $p1
      i32.const 112
      i32.add
      local.get $p0
      call $f60180
      i32.const 0
      local.set $l2
      loop $L6
        local.get $p0
        i32.load offset=124
        local.get $l3
        local.get $l2
        i32.const 2
        i32.shl
        i32.add
        i32.const 16
        i32.add
        i32.const 0
        call $f56977
        i32.const 0
        call $f2192
        drop
        local.get $p0
        i32.load offset=124
        i32.const 3813948
        i32.load
        i32.const 0
        call $f2192
        drop
        local.get $l2
        i32.const 1
        i32.add
        local.tee $l2
        i32.const 32
        i32.ne
        br_if $L6
      end
    end
    local.get $p1
    i32.const 144
    i32.add
    global.set $g0)
