  (func $f60715 (type $t2) (param $p0 i32) (param $p1 i32) (param $p2 i32)
    (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i64)
    global.get $g0
    i32.const -64
    i32.add
    local.tee $p2
    global.set $g0
    i32.const 4674887
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3786520
      call $f1661
      i32.const 3748808
      call $f1661
      i32.const 3792480
      call $f1661
      i32.const 3792572
      call $f1661
      i32.const 3751540
      call $f1661
      i32.const 3827984
      call $f1661
      i32.const 3821460
      call $f1661
      i32.const 3843892
      call $f1661
      i32.const 3837344
      call $f1661
      i32.const 3837100
      call $f1661
      i32.const 3827988
      call $f1661
      i32.const 3825660
      call $f1661
      i32.const 4674887
      i32.const 1
      i32.store8
    end
    local.get $p1
    i32.const 0
    call $f54361
    i32.const 0
    call $f54485
    local.set $l3
    i32.const 3825660
    i32.load
    local.get $l3
    i32.const 0
    call $f53732
    local.set $l3
    i32.const 3748808
    i32.load
    local.tee $l4
    i32.load offset=116
    i32.eqz
    if $I1
      local.get $l4
      call $f65192
    end
    local.get $l3
    i32.const 0
    call $f42976
    local.get $p1
    i32.const 0
    call $f54361
    i32.const 0
    call $f54485
    local.tee $l3
    i32.const 3827984
    i32.load
    i32.const 0
    call $f53861
    if $I2
      i32.const 3821460
      i32.load
      i32.const 0
      call $f54416
      i32.const 3792480
      i32.load
      call $f34548
      local.set $l4
      local.get $p2
      i32.const 2
      i32.store offset=60
      i32.const 3751540
      i32.load
      local.get $p2
      i32.const 60
      i32.add
      call $f1675
      local.set $l5
      local.get $l4
      i32.const 3837344
      i32.load
      local.get $l5
      i32.const 0
      call $f54371
    end
    local.get $l3
    i32.const 3827988
    i32.load
    i32.const 0
    call $f53861
    if $I3
      i32.const 3821460
      i32.load
      i32.const 0
      call $f54416
      i32.const 3792480
      i32.load
      call $f34548
      local.set $l3
      local.get $p2
      i32.const 3
      i32.store offset=60
      i32.const 3751540
      i32.load
      local.get $p2
      i32.const 60
      i32.add
      call $f1675
      local.set $l4
      local.get $l3
      i32.const 3837344
      i32.load
      local.get $l4
      i32.const 0
      call $f54371
    end
    local.get $p1
    i32.const 0
    call $f54361
    i32.const 0
    call $f54408
    i32.const 3837100
    i32.load
    i32.const 0
    call $f53861
    if $I4
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
    call $f54361
    i32.const 0
    call $f54408
    i32.const 3843892
    i32.load
    i32.const 0
    call $f53861
    if $I5
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
      if $I6
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
      local.set $l6
      local.get $p2
      local.get $l3
      i32.load offset=8
      local.tee $l3
      i32.store offset=24
      local.get $p2
      local.get $l3
      i32.store offset=56
      local.get $p2
      local.get $l6
      i64.store offset=48
      local.get $p2
      local.get $l6
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
      if $I7
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
      local.set $l6
      local.get $p2
      local.get $l3
      i32.load offset=8
      local.tee $l3
      i32.store offset=8
      local.get $p2
      local.get $l3
      i32.store offset=40
      local.get $p2
      local.get $l6
      i64.store offset=32
      local.get $p2
      local.get $l6
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
