  (func $f61062 (type $t0) (param $p0 i32) (param $p1 i32) (result i32)
    i32.const 4675130
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3749968
      call $f1661
      i32.const 4675130
      i32.const 1
      i32.store8
    end
    local.get $p0
    i32.load offset=176
    local.set $p1
    i32.const 3749968
    i32.load
    call $f1446
    local.set $p0
    i32.const 4675116
    i32.load8_u
    i32.eqz
    if $I1
      i32.const 3745664
      call $f1661
      i32.const 3745900
      call $f1661
      i32.const 4675116
      i32.const 1
      i32.store8
    end
    local.get $p0
    i32.const 0
    i32.store offset=16
    local.get $p0
    i64.const 0
    i64.store offset=8 align=4
    i32.const 3745664
    i32.load
    local.get $p1
    call $f1052
    local.set $p1
    local.get $p0
    i32.const 0
    i32.store offset=24
    local.get $p0
    local.get $p1
    i32.store offset=20
    i32.const 3745900
    i32.load
    i32.const 32
    call $f1052
    local.set $p1
    local.get $p0
    i64.const 0
    i64.store offset=84 align=4
    local.get $p0
    i32.const 1
    i32.store offset=60
    local.get $p0
    i64.const 0
    i64.store offset=32 align=4
    local.get $p0
    local.get $p1
    i32.store offset=28
    local.get $p0
    i64.const 0
    i64.store offset=92 align=4
    local.get $p0
    i32.const 0
    i32.store offset=100
    local.get $p0)
