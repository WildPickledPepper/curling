  (func $f61028 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i64)
    global.get $g0
    i32.const 48
    i32.sub
    local.tee $p1
    global.set $g0
    i32.const 4675105
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3786520
      call $f1661
      i32.const 3786600
      call $f1661
      i32.const 4675105
      i32.const 1
      i32.store8
    end
    local.get $p0
    i32.const 0
    i32.store16 offset=16
    local.get $p0
    local.get $p0
    i32.const 3786600
    i32.load
    call $f59510
    local.tee $l2
    i32.store offset=20
    local.get $p1
    i32.const 32
    i32.add
    local.get $l2
    i32.const 0
    call $f32544
    local.get $p0
    local.get $p1
    i32.load offset=40
    i32.store offset=32
    local.get $p0
    local.get $p1
    i64.load offset=32
    i64.store offset=24 align=4
    local.get $p0
    i32.load offset=20
    local.set $l2
    i32.const 4674229
    i32.load8_u
    i32.eqz
    if $I1
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
    local.get $p1
    local.get $l3
    i32.load offset=8
    local.tee $l3
    i32.store offset=8
    local.get $p1
    local.get $l3
    i32.store offset=24
    local.get $p1
    local.get $l4
    i64.store offset=16
    local.get $p1
    local.get $l4
    i64.store
    local.get $l2
    local.get $p1
    i32.const 0
    call $f32537
    local.get $p0
    i32.load offset=20
    i32.const 80
    i32.const 0
    call $f32534
    local.get $p0
    i32.const 3786520
    i32.load
    call $f59510
    i32.const 0
    call $f32557
    f32.const 0x0p+0 (;=0;)
    i32.const 0
    call $f32511
    local.get $p1
    i32.const 48
    i32.add
    global.set $g0)
