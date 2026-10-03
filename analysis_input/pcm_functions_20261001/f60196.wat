  (func $f60196 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 f32) (local $l6 f32) (local $l7 f32)
    global.get $g0
    i32.const 32
    i32.sub
    local.tee $p1
    global.set $g0
    i32.const 4674519
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3792572
      call $f1661
      i32.const 3753376
      call $f1661
      i32.const 3745968
      call $f1661
      i32.const 3826444
      call $f1661
      i32.const 3813948
      call $f1661
      i32.const 3836244
      call $f1661
      i32.const 3831600
      call $f1661
      i32.const 3836252
      call $f1661
      i32.const 4674519
      i32.const 1
      i32.store8
    end
    i32.const 3831600
    i32.load
    local.set $l3
    local.get $p0
    i32.load offset=212
    local.set $l2
    i32.const 3753376
    i32.load
    local.tee $l4
    i32.load offset=116
    i32.eqz
    if $I1
      local.get $l4
      call $f65192
    end
    local.get $l2
    i32.const 0
    i32.const 0
    call $f54398
    if $I2
      local.get $p0
      f32.load offset=232
      local.set $l5
      local.get $p1
      local.get $p0
      i32.load offset=212
      i32.const 0
      call $f54401
      i32.const 0
      call $f54624
      local.get $p1
      f32.load offset=8
      local.set $l6
      local.get $p0
      f32.load offset=224
      local.set $l7
      local.get $p1
      local.get $p0
      i32.load offset=212
      i32.const 0
      call $f54401
      i32.const 0
      call $f54624
      local.get $p1
      local.get $l5
      local.get $l6
      f32.sub
      f32.const 0x1.3p+1 (;=2.375;)
      f32.add
      f32.store offset=24
      local.get $p1
      local.get $l7
      local.get $p1
      f32.load
      f32.sub
      f32.const 0x1.3851ecp+2 (;=4.88;)
      f32.add
      f32.store offset=28
      local.get $p1
      local.get $p0
      i32.load offset=212
      i32.const 3792572
      i32.load
      call $f34548
      i32.const 0
      call $f32519
      local.get $p1
      f32.load offset=8
      local.set $l5
      local.get $p1
      local.get $p0
      i32.load offset=212
      i32.const 3792572
      i32.load
      call $f34548
      i32.const 0
      call $f32519
      local.get $p1
      local.get $l5
      f32.neg
      f32.store offset=16
      local.get $p1
      local.get $p1
      f32.load
      f32.neg
      f32.store offset=20
      local.get $p1
      local.get $p0
      i32.load offset=212
      i32.const 3792572
      i32.load
      call $f34548
      i32.const 0
      call $f32522
      local.get $p1
      local.get $p1
      f32.load offset=4
      f32.store offset=12
      i32.const 3745968
      i32.load
      i32.const 10
      call $f1052
      local.tee $l2
      local.get $l3
      i32.store offset=16
      local.get $l2
      local.get $p1
      i32.const 24
      i32.add
      i32.const 3826444
      i32.load
      i32.const 0
      call $f56981
      i32.store offset=20
      local.get $l2
      i32.const 3813948
      i32.load
      i32.store offset=24
      local.get $l2
      local.get $p1
      i32.const 24
      i32.add
      i32.const 4
      i32.or
      i32.const 3826444
      i32.load
      i32.const 0
      call $f56981
      i32.store offset=28
      local.get $l2
      i32.const 3813948
      i32.load
      i32.store offset=32
      local.get $l2
      local.get $p1
      i32.const 16
      i32.add
      i32.const 3826444
      i32.load
      i32.const 0
      call $f56981
      i32.store offset=36
      local.get $l2
      i32.const 3813948
      i32.load
      i32.store offset=40
      local.get $l2
      local.get $p1
      i32.const 16
      i32.add
      i32.const 4
      i32.or
      i32.const 3826444
      i32.load
      i32.const 0
      call $f56981
      i32.store offset=44
      local.get $l2
      i32.const 3813948
      i32.load
      i32.store offset=48
      local.get $l2
      local.get $p1
      i32.const 12
      i32.add
      i32.const 3826444
      i32.load
      i32.const 0
      call $f56981
      i32.store offset=52
      local.get $l2
      i32.const 0
      call $f53875
      local.set $l2
      local.get $p0
      i32.load offset=96
      local.tee $l3
      i32.const 68
      i32.const 44
      local.get $l3
      i32.load offset=24
      local.tee $l3
      select
      i32.add
      i32.load
      local.get $l2
      i32.const 0
      call $f61033
      local.get $p0
      i32.load offset=252
      i32.const 3836252
      i32.const 3836244
      local.get $l3
      select
      i32.load
      local.get $l2
      i32.const 0
      call $f53732
      i32.const 0
      call $f61055
    end
    local.get $p1
    i32.const 32
    i32.add
    global.set $g0)
