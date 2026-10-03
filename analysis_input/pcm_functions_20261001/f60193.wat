  (func $f60193 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32)
    i32.const 4674516
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3749616
      call $f1661
      i32.const 3772452
      call $f1661
      i32.const 3772456
      call $f1661
      i32.const 3828516
      call $f1661
      i32.const 3836248
      call $f1661
      i32.const 3836256
      call $f1661
      i32.const 4674516
      i32.const 1
      i32.store8
    end
    i32.const 3749616
    i32.load
    local.tee $p1
    i32.load offset=116
    i32.eqz
    if $I1
      local.get $p1
      call $f65192
      i32.const 3749616
      i32.load
      local.set $p1
    end
    local.get $p1
    i32.load offset=92
    local.tee $l2
    i32.load offset=4
    i32.load offset=12
    i32.const 2
    i32.ge_s
    if $I2
      local.get $p1
      i32.load offset=116
      if $I3 (result i32)
        local.get $l2
      else
        local.get $p1
        call $f65192
        i32.const 3749616
        i32.load
        i32.load offset=92
      end
      i32.load offset=4
      i32.const 0
      i32.const 3772456
      i32.load
      call $f2903
      i32.const 3828516
      i32.load
      i32.const 0
      call $f61033
      local.get $p0
      i32.load offset=252
      i32.const 3836248
      i32.load
      i32.const 0
      call $f61055
      i32.const 3749616
      i32.load
      i32.load offset=92
      i32.load offset=4
      i32.const 1
      i32.const 3772456
      i32.load
      call $f2903
      i32.const 3828516
      i32.load
      i32.const 0
      call $f61033
      local.get $p0
      i32.load offset=252
      i32.const 3836256
      i32.load
      i32.const 0
      call $f61055
    end)
