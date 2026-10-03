  (func $f78698 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l2
    global.set $g0
    local.get $p1
    i32.const 4125408
    i32.load
    i32.const 4129148
    i32.load
    local.get $p0
    i32.const 0
    call $f78369
    local.get $p0
    local.get $p1
    call $f80209
    local.get $p1
    i32.const 136988
    i32.const 220012
    local.get $p0
    i32.const 32
    i32.add
    local.tee $p0
    i32.const 0
    call $f78369
    local.get $l2
    i32.const 0
    i32.store
    local.get $l2
    i64.const 0
    i64.store offset=8
    local.get $p1
    i32.const 215898
    i32.const 3092472
    i32.load
    local.get $p0
    i32.const 8388609
    call $f78369
    local.get $p1
    i32.const 40
    i32.add
    local.tee $p0
    i32.load
    i32.load
    local.get $p1
    i32.const 44
    i32.add
    local.tee $l3
    i32.load
    i32.const 5
    i32.shl
    i32.add
    i32.const 4
    i32.store offset=12
    local.get $p1
    call $f78370
    local.get $p1
    i32.const 215826
    i32.const 3092524
    i32.load
    local.get $l2
    i32.const 8
    i32.add
    i32.const 8388609
    call $f78369
    local.get $p0
    i32.load
    i32.load
    local.get $l3
    i32.load
    i32.const 5
    i32.shl
    i32.add
    i32.const 8
    i32.store offset=12
    local.get $p1
    call $f78370
    local.get $p1
    call $f78370
    local.get $p1
    call $f78370
    local.get $l2
    i32.const 16
    i32.add
    global.set $g0)
