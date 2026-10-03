  (func $f61049 (type $t2) (param $p0 i32) (param $p1 i32) (param $p2 i32)
    (local $l3 i32)
    i32.const 4675115
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3745664
      call $f1661
      i32.const 3745900
      call $f1661
      i32.const 4675115
      i32.const 1
      i32.store8
    end
    local.get $p0
    local.get $p1
    i32.load offset=8
    i32.store offset=8
    local.get $p0
    local.get $p1
    i32.load offset=12
    i32.store offset=12
    local.get $p0
    local.get $p1
    i32.load offset=16
    i32.store offset=16
    local.get $p0
    i32.const 3745664
    i32.load
    local.get $p1
    i32.load offset=20
    i32.load offset=12
    call $f1052
    local.tee $p2
    i32.store offset=20
    local.get $p1
    i32.load offset=20
    local.tee $l3
    local.get $p2
    local.get $l3
    i32.load offset=12
    i32.const 0
    call $f57557
    local.get $p0
    local.get $p1
    i32.load offset=24
    i32.store offset=24
    local.get $p0
    i32.const 3745900
    i32.load
    i32.const 32
    call $f1052
    local.tee $p2
    i32.store offset=28
    local.get $p1
    i32.load offset=28
    local.get $p2
    i32.const 32
    i32.const 0
    call $f57557)