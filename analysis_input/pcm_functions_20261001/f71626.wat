  (func $f71626 (type $t65) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 f32)
    (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 f32)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l5
    global.set $g0
    block $B0
      local.get $p0
      i32.load offset=176
      local.tee $l4
      if $I1
        local.get $l4
        local.get $p2
        f32.load
        f32.store
        local.get $l4
        local.get $p2
        f32.load offset=4
        f32.store offset=4
        local.get $l4
        local.get $p2
        f32.load offset=8
        f32.store offset=8
        local.get $l4
        local.get $p2
        f32.load offset=12
        f32.store offset=12
        local.get $l4
        local.get $p2
        f32.load offset=16
        f32.store offset=16
        local.get $l4
        local.get $p2
        f32.load offset=20
        f32.store offset=20
        local.get $p2
        f32.load offset=24
        local.set $l13
        local.get $l4
        i32.const 1
        i32.store8 offset=28
        local.get $l4
        local.get $l13
        f32.store offset=24
        local.get $p0
        i32.load
        local.tee $l4
        i32.eqz
        br_if $B0
        local.get $l4
        local.get $l4
        i32.load16_u offset=152
        i32.const 63483
        i32.and
        i32.const 4
        i32.or
        i32.store16 offset=152
        br $B0
      end
      local.get $p1
      i32.load offset=288
      local.tee $l4
      i32.eqz
      if $I2
        local.get $p1
        call $f71601
        local.get $p1
        i32.load offset=288
        local.set $l4
      end
      local.get $p1
      local.get $l4
      i32.load
      i32.store offset=288
      local.get $p1
      local.get $p1
      i32.load offset=280
      i32.const 1
      i32.add
      i32.store offset=280
      local.get $l4
      i32.const 24
      i32.add
      local.tee $p1
      i64.const 0
      i64.store align=1
      local.get $l4
      i32.const 56
      i32.add
      local.tee $l9
      i64.const 0
      i64.store align=1
      local.get $l4
      i32.const 48
      i32.add
      local.tee $l6
      i64.const 0
      i64.store align=1
      local.get $l4
      i32.const 40
      i32.add
      local.tee $l7
      i64.const 0
      i64.store align=1
      local.get $l4
      i32.const 32
      i32.add
      local.tee $l8
      i64.const 0
      i64.store align=1
      local.get $l4
      i32.const 16
      i32.add
      local.tee $l10
      i64.const 0
      i64.store align=1
      local.get $l4
      i32.const 8
      i32.add
      local.tee $l11
      i64.const 0
      i64.store align=1
      local.get $l4
      i64.const 0
      i64.store align=1
      local.get $l4
      i32.const 1
      i32.store8 offset=31
      local.get $l4
      i32.const 1
      i32.store8 offset=28
      local.get $l6
      local.get $p0
      i32.const 120
      i32.add
      local.tee $l12
      f32.load
      f32.store
      local.get $l4
      local.get $p0
      f32.load offset=124
      f32.store offset=52
      local.get $l8
      local.get $p0
      i32.const 128
      i32.add
      local.tee $l6
      f32.load
      f32.store
      local.get $l4
      local.get $p0
      f32.load offset=132
      f32.store offset=36
      local.get $l7
      local.get $p0
      i32.const 136
      i32.add
      local.tee $l8
      f32.load
      f32.store
      local.get $l4
      local.get $p0
      f32.load offset=140
      f32.store offset=44
      local.get $l9
      local.get $p0
      i32.const 112
      i32.add
      local.tee $l7
      f32.load
      f32.store
      local.get $l4
      local.get $p0
      f32.load offset=116
      f32.store offset=60
      local.get $p0
      local.get $l4
      i32.store offset=176
      local.get $l7
      i64.const 9187343237679939583
      i64.store
      local.get $l8
      i64.const 0
      i64.store
      local.get $l6
      i64.const 0
      i64.store
      local.get $l12
      i64.const 0
      i64.store
      local.get $l4
      local.get $p2
      f32.load
      f32.store
      local.get $l4
      local.get $p2
      f32.load offset=4
      f32.store offset=4
      local.get $l11
      local.get $p2
      f32.load offset=8
      f32.store
      local.get $l4
      local.get $p2
      f32.load offset=12
      f32.store offset=12
      local.get $l10
      local.get $p2
      f32.load offset=16
      f32.store
      local.get $l4
      local.get $p2
      f32.load offset=20
      f32.store offset=20
      local.get $p2
      f32.load offset=24
      local.set $l13
      local.get $l4
      i32.const 1
      i32.store8 offset=28
      local.get $p1
      local.get $l13
      f32.store
    end
    local.get $p0
    local.get $p3
    f32.store offset=156
    local.get $p0
    i32.load
    local.tee $l4
    if $I3
      local.get $l4
      i32.load offset=40
      i32.load offset=1012
      local.set $p2
      local.get $l4
      i32.load offset=44
      i32.load8_u offset=9
      local.set $p0
      local.get $l5
      local.get $l4
      i64.load offset=144
      i64.store offset=8
      local.get $p2
      local.get $p0
      i32.const 2
      i32.eq
      local.get $l5
      i32.const 8
      i32.add
      local.get $p2
      i32.load
      i32.load offset=44
      call_indirect $__indirect_function_table (type $t2)
      local.get $l4
      call $f71571
      local.get $l4
      local.get $p3
      i32.const 1
      call $f71566
    end
    local.get $l5
    i32.const 16
    i32.add
    global.set $g0)
