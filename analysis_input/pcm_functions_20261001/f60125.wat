  (func $f60125 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32)
    i32.const 4674462
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3739640
      call $f1661
      i32.const 3739664
      call $f1661
      i32.const 3787852
      call $f1661
      i32.const 3748324
      call $f1661
      i32.const 3748808
      call $f1661
      i32.const 3775976
      call $f1661
      i32.const 3753376
      call $f1661
      i32.const 3808584
      call $f1661
      i32.const 3759364
      call $f1661
      i32.const 3824112
      call $f1661
      i32.const 4674462
      i32.const 1
      i32.store8
    end
    local.get $p0
    i32.load offset=44
    local.set $p1
    i32.const 3753376
    i32.load
    local.tee $l2
    i32.load offset=116
    i32.eqz
    if $I1
      local.get $l2
      call $f65192
    end
    local.get $p1
    i32.const 0
    i32.const 0
    call $f54398
    if $I2
      local.get $p0
      i32.load offset=44
      local.set $p1
      i32.const 3739640
      i32.load
      call $f1446
      local.tee $l2
      local.get $p0
      i32.const 3787852
      i32.load
      i32.const 0
      call $f30341
      local.get $p1
      local.get $l2
      i32.const 0
      call $f60649
    end
    i32.const 3748808
    i32.load
    local.tee $p0
    i32.load offset=116
    i32.eqz
    if $I3
      local.get $p0
      call $f65192
    end
    i32.const 3824112
    i32.load
    i32.const 0
    call $f42976
    i32.const 3748324
    i32.load
    local.tee $p0
    i32.load offset=116
    if $I4 (result i32)
      local.get $p0
    else
      local.get $p0
      call $f65192
      i32.const 3748324
      i32.load
    end
    i32.load offset=92
    i32.load offset=8
    local.set $l2
    i32.const 3759364
    i32.load
    local.tee $p0
    i32.load offset=116
    i32.eqz
    if $I5
      local.get $p0
      call $f65192
      i32.const 3759364
      i32.load
      local.set $p0
    end
    local.get $p0
    i32.load offset=92
    i32.load offset=12
    local.tee $p1
    i32.eqz
    if $I6
      local.get $p0
      i32.load offset=116
      if $I7 (result i32)
        local.get $p0
      else
        local.get $p0
        call $f65192
        i32.const 3759364
        i32.load
      end
      i32.load offset=92
      i32.load
      local.set $p0
      i32.const 3739664
      i32.load
      call $f1446
      local.tee $p1
      local.get $p0
      i32.const 3808584
      i32.load
      i32.const 0
      call $f30369
      i32.const 3759364
      i32.load
      i32.load offset=92
      local.get $p1
      i32.store offset=12
    end
    local.get $l2
    local.get $p1
    i32.const 3775976
    i32.load
    call $f2921)
