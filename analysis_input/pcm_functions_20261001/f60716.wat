  (func $f60716 (type $t2) (param $p0 i32) (param $p1 i32) (param $p2 i32)
    (local $l3 i32) (local $l4 i64)
    global.get $g0
    i32.const -64
    i32.add
    local.tee $p2
    global.set $g0
    i32.const 4674888
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3786520
      call $f1661
      i32.const 3792572
      call $f1661
      i32.const 3843892
      call $f1661
      i32.const 3837100
      call $f1661
      i32.const 4674888
      i32.const 1
      i32.store8
    end
    local.get $p1
    i32.const 0
    call $f32444
    i32.const 0
    call $f54408
    i32.const 3837100
    i32.load
    i32.const 0
    call $f53861
    if $I1
      local.get $p0
      i32.const 1
      i32.store8 offset=32
      local.get $p0
      i32.const 3786520
      i32.load
      call $f59510
      i32.const 0
      call $f32557
      f32.const 0x1.333334p-1 (;=0.6;)
      i32.const 0
      call $f32511
      local.get $p0
      i32.const 3786520
      i32.load
      call $f59510
      i32.const 0
      call $f32557
      f32.const 0x1.333334p-1 (;=0.6;)
      i32.const 0
      call $f32512
    end
    local.get $p1
    i32.const 0
    call $f32444
    i32.const 0
    call $f54408
    i32.const 3843892
    i32.load
    i32.const 0
    call $f53861
    if $I2
      local.get $p0
      i32.const 1
      i32.store8 offset=32
      local.get $p0
      i32.const 3786520
      i32.load
      call $f59510
      i32.const 0
      call $f32557
      f32.const 0x1.333334p-1 (;=0.6;)
      i32.const 0
      call $f32511
      local.get $p0
      i32.const 3786520
      i32.load
      call $f59510
      i32.const 0
      call $f32557
      f32.const 0x1.333334p-1 (;=0.6;)
      i32.const 0
      call $f32512
      local.get $p0
      i32.const 0
      call $f54361
      i32.const 3792572
      i32.load
      call $f34548
      local.set $p1
      i32.const 4674229
      i32.load8_u
      i32.eqz
      if $I3
        i32.const 3757216
        call $f1661
        i32.const 4674229
        i32.const 1
        i32.store8
      end
      i32.const 3757216
      i32.load
      i32.load offset=92
      local.tee $l3
      i64.load align=4
      local.set $l4
      local.get $p2
      local.get $l3
      i32.load offset=8
      local.tee $l3
      i32.store offset=24
      local.get $p2
      local.get $l3
      i32.store offset=56
      local.get $p2
      local.get $l4
      i64.store offset=48
      local.get $p2
      local.get $l4
      i64.store offset=16
      local.get $p1
      local.get $p2
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
      local.set $p1
      i32.const 4674229
      i32.load8_u
      i32.eqz
      if $I4
        i32.const 3757216
        call $f1661
        i32.const 4674229
        i32.const 1
        i32.store8
      end
      i32.const 3757216
      i32.load
      i32.load offset=92
      local.tee $l3
      i64.load align=4
      local.set $l4
      local.get $p2
      local.get $l3
      i32.load offset=8
      local.tee $l3
      i32.store offset=8
      local.get $p2
      local.get $l3
      i32.store offset=40
      local.get $p2
      local.get $l4
      i64.store offset=32
      local.get $p2
      local.get $l4
      i64.store
      local.get $p1
      local.get $p2
      i32.const 0
      call $f32524
      local.get $p0
      i32.const 0
      call $f54361
      i32.const 0
      i32.const 0
      call $f54405
    end
    local.get $p2
    i32.const -64
    i32.sub
    global.set $g0)
