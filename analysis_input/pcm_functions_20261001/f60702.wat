  (func $f60702 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 f32) (local $l3 i32) (local $l4 i32) (local $l5 f64) (local $l6 f64) (local $l7 f64)
    global.get $g0
    i32.const 144
    i32.sub
    local.tee $p1
    global.set $g0
    i32.const 4674876
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3792560
      call $f1661
      i32.const 3792572
      call $f1661
      i32.const 3792592
      call $f1661
      i32.const 3820972
      call $f1661
      i32.const 4674876
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
      i32.load8_u offset=100
      i32.eqz
      br_if $B1
      local.get $p0
      i32.load offset=72
      i32.const 3792560
      i32.load
      call $f34548
      i32.load8_u offset=32
      br_if $B1
      local.get $p1
      i32.const 88
      i32.add
      local.get $p0
      i32.load offset=72
      i32.const 3792572
      i32.load
      call $f34548
      i32.const 0
      call $f32519
      local.get $p1
      f32.load offset=96
      local.set $l2
      local.get $p1
      i32.const 88
      i32.add
      local.get $p0
      i32.load offset=72
      i32.const 3792572
      i32.load
      call $f34548
      i32.const 0
      call $f32519
      local.get $p1
      i32.const 128
      i32.add
      local.get $l2
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
      i32.const 3792592
      i32.load
      call $f34548
      i32.load8_u offset=24
      local.set $l3
      f32.const -0x1.a36e2ep-13 (;=-0.0002;)
      f32.const 0x1.a36e2ep-13 (;=0.0002;)
      i32.const 0
      call $f54300
      local.set $l2
      local.get $p1
      i32.const 120
      i32.add
      local.tee $l4
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
      i32.load offset=72
      i32.const 3792572
      i32.load
      call $f34548
      i32.const 0
      call $f32522
      local.get $p1
      local.get $l4
      i64.load
      i64.store offset=48
      local.get $p1
      local.get $p1
      i64.load offset=112
      i64.store offset=40
      local.get $p1
      i32.const 88
      i32.add
      local.get $l2
      f32.const 0x1.3a92a4p-11 (;=0.0006;)
      f32.const 0x1.0624dep-10 (;=0.001;)
      local.get $l3
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
      i32.load offset=72
      i32.const 3792572
      i32.load
      call $f34548
      local.set $l3
      local.get $p1
      i32.const 80
      i32.add
      local.tee $l4
      local.get $l7
      f32.demote_f64
      f32.neg
      f32.store
      local.get $p1
      local.get $l4
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
      local.get $l3
      local.get $p1
      i32.const 24
      i32.add
      i32.const 0
      call $f32521
      local.get $p0
      i32.load offset=72
      i32.const 3792572
      i32.load
      call $f34548
      local.set $p0
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
      local.get $p0
      local.get $p1
      i32.const 8
      i32.add
      i32.const 0
      call $f32524
    end
    local.get $p1
    i32.const 144
    i32.add
    global.set $g0)