  (func $f60185 (type $t1) (param $p0 i32) (param $p1 i32)
    i32.const 4674509
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3750924
      call $f1661
      i32.const 3816820
      call $f1661
      i32.const 3854368
      call $f1661
      i32.const 3834472
      call $f1661
      i32.const 4674509
      i32.const 1
      i32.store8
    end
    local.get $p0
    i32.const 0
    call $f51726
    i32.const 3816820
    i32.load
    i32.const 0
    call $f53732
    i32.store offset=80
    i32.const 3750924
    i32.load
    call $f1446
    local.tee $p1
    i32.const 0
    call $f60952
    local.get $p1
    local.get $p0
    i32.load offset=80
    i32.const 0
    call $f60918
    local.get $p0
    local.get $p1
    i32.const 3834472
    i32.load
    i32.const 3854368
    i32.load
    i32.const 7788
    i32.const 0
    call $f60941
    i32.store offset=76
    local.get $p1
    i32.const 0
    call $f60926)
