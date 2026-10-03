  (func $f60194 (type $t1) (param $p0 i32) (param $p1 i32)
    i32.const 4674517
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3836244
      call $f1661
      i32.const 3827208
      call $f1661
      i32.const 4674517
      i32.const 1
      i32.store8
    end
    local.get $p0
    i32.const 0
    i32.store offset=212
    local.get $p0
    i32.load offset=96
    local.tee $p1
    i32.const 68
    i32.const 44
    local.get $p1
    i32.load offset=24
    select
    i32.add
    i32.load
    i32.const 3827208
    i32.load
    local.tee $p1
    i32.const 0
    call $f61033
    local.get $p0
    i32.load offset=252
    i32.const 3836244
    i32.load
    local.get $p1
    i32.const 0
    call $f53732
    i32.const 0
    call $f61055
    local.get $p0
    i32.const 0
    i32.store8 offset=216
    local.get $p0
    i32.const 1
    i32.store8 offset=90
    local.get $p0
    i32.const 0
    i32.store offset=92)
