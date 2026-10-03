  (func $f60170 (type $t0) (param $p0 i32) (param $p1 i32) (result i32)
    i32.const 4674496
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3749968
      call $f1661
      i32.const 4674496
      i32.const 1
      i32.store8
    end
    local.get $p0
    i32.load offset=160
    local.set $p0
    i32.const 3749968
    i32.load
    call $f1446
    local.tee $p1
    local.get $p0
    i32.const 0
    call $f61050
    local.get $p1)
