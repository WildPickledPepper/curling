  (func $f60191 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $p0
    global.set $g0
    i32.const 4674514
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3792480
      call $f1661
      i32.const 3751540
      call $f1661
      i32.const 3821460
      call $f1661
      i32.const 3837344
      call $f1661
      i32.const 4674514
      i32.const 1
      i32.store8
    end
    i32.const 3821460
    i32.load
    i32.const 0
    call $f54416
    i32.const 3792480
    i32.load
    call $f34548
    local.set $p1
    local.get $p0
    i32.const 1
    i32.store offset=12
    i32.const 3751540
    i32.load
    local.get $p0
    i32.const 12
    i32.add
    call $f1675
    local.set $l2
    local.get $p1
    i32.const 3837344
    i32.load
    local.get $l2
    i32.const 0
    call $f54371
    local.get $p0
    i32.const 16
    i32.add
    global.set $g0)
