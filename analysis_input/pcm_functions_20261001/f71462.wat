  (func $f71462 (type $t2) (param $p0 i32) (param $p1 i32) (param $p2 i32)
    (local $l3 i32)
    local.get $p0
    i32.const 4
    i32.add
    local.get $p1
    i32.load offset=4
    local.get $p2
    i32.load offset=4
    i32.const 1
    i32.const 5
    call $f71680
    local.set $l3
    local.get $p0
    i32.const -1
    i32.store offset=36
    local.get $p0
    local.get $p2
    i32.store offset=32
    local.get $p0
    local.get $p1
    i32.store offset=28
    local.get $p0
    i32.const 0
    i32.store8 offset=58
    local.get $p0
    i32.const 32
    i32.store16 offset=56
    local.get $p0
    i32.const 3158040
    i32.store
    local.get $l3
    call $f71361
    local.set $p1
    local.get $l3
    i32.load
    local.get $l3
    call $f71333
    local.get $p0
    i32.load offset=8
    local.get $l3
    call $f71333
    local.get $l3
    i32.load
    i32.load offset=40
    local.tee $p2
    local.get $l3
    local.get $p1
    call $f71383
    local.get $p2
    i32.load offset=2168
    local.get $p0
    call $f71693
    local.get $p0
    i32.const 0
    i32.store16 offset=52)