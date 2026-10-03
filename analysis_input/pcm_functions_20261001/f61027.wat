  (func $f61027 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 f32) (local $l5 f32) (local $l6 f32)
    global.get $g0
    i32.const 272
    i32.sub
    local.tee $p1
    global.set $g0
    i32.const 4675104
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3749908
      call $f1661
      i32.const 3792616
      call $f1661
      i32.const 3819508
      call $f1661
      i32.const 3819496
      call $f1661
      i32.const 3835536
      call $f1661
      i32.const 4675104
      i32.const 1
      i32.store8
    end
    i32.const 3749908
    i32.load
    local.tee $l2
    i32.load offset=116
    i32.eqz
    if $I1
      local.get $l2
      call $f65192
    end
    local.get $p1
    i64.const 4751297607996276736
    i64.store offset=264
    local.get $p1
    i64.const 4751297607996276736
    i64.store offset=136
    local.get $p1
    i64.const 0
    i64.store offset=256
    local.get $p1
    i64.const 0
    i64.store offset=128
    local.get $p1
    i32.const 128
    i32.add
    i32.const 3819496
    i32.load
    i32.const 0
    call $f17366
    if $I2
      local.get $p0
      f32.load offset=24
      local.set $l4
      i32.const 4674230
      i32.load8_u
      i32.eqz
      if $I3
        i32.const 3757216
        call $f1661
        i32.const 4674230
        i32.const 1
        i32.store8
      end
      local.get $p1
      i32.const 3757216
      i32.load
      i32.load offset=92
      local.tee $l2
      i32.load offset=32
      i32.store offset=120
      local.get $p1
      local.get $l2
      i64.load offset=24 align=4
      i64.store offset=112
      local.get $p1
      i32.const 240
      i32.add
      local.get $l4
      local.get $p1
      i32.const 112
      i32.add
      i32.const 0
      call $f54081
      local.get $p1
      i32.const 0
      i32.store offset=216
      local.get $p1
      i32.const 0
      i32.store offset=88
      local.get $p1
      local.get $p1
      i64.load offset=248
      i64.store offset=104
      local.get $p1
      i64.const 1148846080
      i64.store offset=208
      local.get $p1
      i64.const 1148846080
      i64.store offset=80
      local.get $p1
      local.get $p1
      i64.load offset=240
      i64.store offset=96
      local.get $p1
      i32.const 224
      i32.add
      local.get $p1
      i32.const 96
      i32.add
      local.get $p1
      i32.const 80
      i32.add
      i32.const 0
      call $f54088
      local.get $p1
      f32.load offset=224
      local.set $l5
      local.get $p1
      f32.load offset=228
      local.set $l6
      local.get $p0
      i32.load offset=36
      local.set $l2
      local.get $p1
      i32.const 200
      i32.add
      local.tee $l3
      local.get $p1
      f32.load offset=232
      local.get $p0
      f32.load offset=16
      local.tee $l4
      f32.mul
      f32.store
      local.get $p1
      local.get $l3
      i32.load
      i32.store offset=72
      local.get $p1
      local.get $l6
      local.get $l4
      f32.mul
      f32.store offset=196
      local.get $p1
      local.get $l5
      local.get $l4
      f32.mul
      f32.store offset=192
      local.get $p1
      local.get $p1
      i64.load offset=192
      i64.store offset=64
      local.get $l2
      local.get $p1
      i32.const -64
      i32.sub
      i32.const 0
      call $f32552
    end
    i32.const 3749908
    i32.load
    local.tee $l2
    i32.load offset=116
    i32.eqz
    if $I4
      local.get $l2
      call $f65192
    end
    local.get $p1
    i64.const 4751297607996276736
    i64.store offset=184
    local.get $p1
    i64.const 4751297607996276736
    i64.store offset=56
    local.get $p1
    i64.const 1121714176
    i64.store offset=176
    local.get $p1
    i64.const 1121714176
    i64.store offset=48
    local.get $p1
    i32.const 48
    i32.add
    i32.const 3835536
    i32.load
    i32.const 0
    call $f17366
    if $I5
      local.get $p0
      i32.load offset=32
      i32.const 3792616
      i32.load
      call $f34548
      local.set $l2
      local.get $p1
      i32.const 1113393725
      i32.store offset=168
      local.get $p1
      i32.const 1113393725
      i32.store offset=40
      local.get $p1
      i64.const 4723848169179483996
      i64.store offset=160
      local.get $p1
      i64.const 4723848169179483996
      i64.store offset=32
      local.get $l2
      local.get $p1
      i32.const 32
      i32.add
      i32.const 0
      call $f54626
    end
    i32.const 3749908
    i32.load
    local.tee $l2
    i32.load offset=116
    i32.eqz
    if $I6
      local.get $l2
      call $f65192
    end
    local.get $p1
    i64.const 4751297607996276736
    i64.store offset=152
    local.get $p1
    i64.const 4751297607996276736
    i64.store offset=24
    local.get $p1
    i64.const 1130102784
    i64.store offset=144
    local.get $p1
    i64.const 1130102784
    i64.store offset=16
    local.get $p1
    i32.const 16
    i32.add
    i32.const 3819508
    i32.load
    i32.const 0
    call $f17366
    if $I7
      local.get $p0
      i32.load offset=36
      local.set $l2
      local.get $p1
      i32.const 240
      i32.add
      local.get $p0
      i32.const 0
      call $f54360
      i32.const 0
      call $f54637
      local.get $p1
      local.get $p1
      i32.load offset=248
      i32.store offset=8
      local.get $p1
      local.get $p1
      i64.load offset=240
      i64.store
      local.get $l2
      local.get $p1
      i32.const 0
      i32.const 0
      call $f32553
    end
    local.get $p1
    i32.const 272
    i32.add
    global.set $g0)
