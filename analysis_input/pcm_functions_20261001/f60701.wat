  (func $f60701 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 f32) (local $l5 f32) (local $l6 f32) (local $l7 f32) (local $l8 f32) (local $l9 f32)
    global.get $g0
    i32.const 48
    i32.sub
    local.tee $p1
    global.set $g0
    i32.const 4674875
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3748808
      call $f1661
      i32.const 3792496
      call $f1661
      i32.const 3792572
      call $f1661
      i32.const 3824044
      call $f1661
      i32.const 4674875
      i32.const 1
      i32.store8
    end
    block $B1
      local.get $p0
      i32.load8_u offset=100
      i32.eqz
      br_if $B1
      local.get $p0
      i32.load offset=16
      i32.const 0
      call $f54401
      local.set $l2
      local.get $p1
      i32.const 32
      i32.add
      local.get $p0
      i32.load offset=72
      i32.const 0
      call $f54401
      i32.const 0
      call $f54624
      local.get $p1
      f32.load offset=32
      local.set $l4
      local.get $p1
      f32.load offset=36
      local.set $l5
      local.get $p0
      f32.load offset=36
      local.set $l6
      local.get $p0
      f32.load offset=32
      local.set $l7
      local.get $p1
      i32.const 24
      i32.add
      local.tee $l3
      local.get $p1
      f32.load offset=40
      local.get $p0
      f32.load offset=40
      f32.sub
      f32.store
      local.get $p1
      local.get $l3
      i32.load
      i32.store offset=8
      local.get $p1
      local.get $l5
      local.get $l6
      f32.sub
      f32.store offset=20
      local.get $p1
      local.get $l4
      local.get $l7
      f32.sub
      f32.store offset=16
      local.get $p1
      local.get $p1
      i64.load offset=16
      i64.store
      local.get $l2
      local.get $p1
      i32.const 0
      call $f54626
      local.get $p1
      i32.const 32
      i32.add
      local.get $p0
      i32.load offset=72
      i32.const 0
      call $f54401
      i32.const 0
      call $f54624
      local.get $p1
      f32.load offset=40
      local.set $l4
      local.get $p1
      f32.load offset=36
      local.set $l5
      local.get $p1
      f32.load offset=32
      local.set $l6
      local.get $p0
      f32.load offset=52
      local.set $l7
      local.get $p0
      f32.load offset=48
      local.set $l8
      local.get $p0
      f32.load offset=44
      local.set $l9
      i32.const 4675187
      i32.load8_u
      i32.eqz
      if $I2
        i32.const 3752504
        call $f1661
        i32.const 4675187
        i32.const 1
        i32.store8
      end
      i32.const 3752504
      i32.load
      local.tee $l2
      i32.load offset=116
      i32.eqz
      if $I3
        local.get $l2
        call $f65192
      end
      local.get $p1
      i32.const 32
      i32.add
      local.get $p0
      i32.load offset=72
      i32.const 3792572
      i32.load
      call $f34548
      i32.const 0
      call $f32519
      local.get $p1
      f32.load offset=32
      f32.const 0x1.0624dep-10 (;=0.001;)
      f32.lt
      i32.eqz
      br_if $B1
      local.get $l6
      local.get $l9
      f32.sub
      local.tee $l6
      local.get $l6
      f32.mul
      local.get $l5
      local.get $l8
      f32.sub
      local.tee $l5
      local.get $l5
      f32.mul
      f32.add
      local.get $l4
      local.get $l7
      f32.sub
      local.tee $l4
      local.get $l4
      f32.mul
      f32.add
      f32.sqrt
      f32.const 0x1p+0 (;=1;)
      f32.gt
      i32.eqz
      br_if $B1
      i32.const 3748808
      i32.load
      local.tee $l2
      i32.load offset=116
      i32.eqz
      if $I4
        local.get $l2
        call $f65192
      end
      i32.const 3824044
      i32.load
      i32.const 0
      call $f42976
      local.get $p0
      i32.load offset=72
      i32.const 3792496
      i32.load
      call $f34548
      i32.const 0
      call $f32557
      f32.const 0x1.333334p-1 (;=0.6;)
      i32.const 0
      call $f32511
      local.get $p0
      i32.load offset=72
      i32.const 3792496
      i32.load
      call $f34548
      i32.const 0
      call $f32557
      f32.const 0x1.333334p-1 (;=0.6;)
      i32.const 0
      call $f32512
      local.get $p0
      i32.const 0
      i32.store8 offset=100
    end
    local.get $p1
    i32.const 48
    i32.add
    global.set $g0)
