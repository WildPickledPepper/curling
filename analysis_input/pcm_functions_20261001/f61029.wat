  (func $f61029 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i64) (local $l5 f32)
    global.get $g0
    i32.const -64
    i32.add
    local.tee $p1
    global.set $g0
    i32.const 4675106
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3792572
      call $f1661
      i32.const 4675106
      i32.const 1
      i32.store8
    end
    local.get $p0
    f32.load offset=28
    local.set $l5
    local.get $p1
    i32.const 48
    i32.add
    local.get $p0
    i32.load offset=20
    i32.const 0
    call $f32544
    local.get $l5
    local.get $p1
    f32.load offset=52
    f32.sub
    f32.const 0x1p-1 (;=0.5;)
    f32.gt
    if $I1
      local.get $p0
      i32.load offset=20
      local.set $l3
      i32.const 4674229
      i32.load8_u
      i32.eqz
      if $I2
        i32.const 3757216
        call $f1661
        i32.const 4674229
        i32.const 1
        i32.store8
      end
      i32.const 3757216
      i32.load
      i32.load offset=92
      local.tee $l2
      i64.load align=4
      local.set $l4
      local.get $p1
      local.get $l2
      i32.load offset=8
      local.tee $l2
      i32.store offset=24
      local.get $p1
      local.get $l2
      i32.store offset=40
      local.get $p1
      local.get $l4
      i64.store offset=32
      local.get $p1
      local.get $l4
      i64.store offset=16
      local.get $l3
      local.get $p1
      i32.const 16
      i32.add
      i32.const 0
      call $f32521
      local.get $p0
      i32.const 0
      call $f54361
      i32.const 3792572
      i32.load
      call $f34548
      local.set $l3
      local.get $p1
      local.get $p0
      i32.const 24
      i32.add
      local.tee $l2
      i32.load offset=8
      i32.store offset=8
      local.get $p1
      local.get $l2
      i64.load align=4
      i64.store
      local.get $l3
      local.get $p1
      i32.const 0
      call $f32546
      local.get $p0
      i32.const 0
      call $f54361
      i32.const 0
      i32.const 0
      call $f54405
    end
    local.get $p1
    i32.const -64
    i32.sub
    global.set $g0)
