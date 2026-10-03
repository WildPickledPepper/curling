  (func $f60197 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l2
    global.set $g0
    i32.const 4674520
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3792608
      call $f1661
      i32.const 3773132
      call $f1661
      i32.const 3813948
      call $f1661
      i32.const 3827120
      call $f1661
      i32.const 3834404
      call $f1661
      i32.const 3827116
      call $f1661
      i32.const 3838024
      call $f1661
      i32.const 3827112
      call $f1661
      i32.const 3834424
      call $f1661
      i32.const 3834420
      call $f1661
      i32.const 3834400
      call $f1661
      i32.const 4674520
      i32.const 1
      i32.store8
    end
    local.get $l2
    local.get $p0
    i32.load offset=148
    i32.const 0
    i32.const 3773132
    i32.load
    call $f2903
    i32.const 3792608
    i32.load
    call $f34548
    local.tee $p1
    local.get $p1
    i32.load
    local.tee $p1
    i32.load offset=788
    local.get $p1
    i32.load offset=784
    call_indirect $__indirect_function_table (type $t0)
    i32.const 0
    call $f56600
    i32.store offset=12
    local.get $l2
    local.get $p0
    i32.load offset=148
    i32.const 1
    i32.const 3773132
    i32.load
    call $f2903
    i32.const 3792608
    i32.load
    call $f34548
    local.tee $p1
    local.get $p1
    i32.load
    local.tee $p1
    i32.load offset=788
    local.get $p1
    i32.load offset=784
    call_indirect $__indirect_function_table (type $t0)
    i32.const 0
    call $f56600
    i32.store offset=8
    local.get $l2
    i32.const 12
    i32.add
    i32.const 0
    call $f56590
    local.set $p1
    local.get $l2
    i32.const 8
    i32.add
    i32.const 0
    call $f56590
    local.set $l3
    i32.const 3838024
    i32.load
    local.get $p1
    i32.const 3813948
    i32.load
    local.get $l3
    i32.const 0
    call $f53874
    local.set $p1
    local.get $p0
    i32.load offset=96
    i32.load offset=44
    local.get $p1
    i32.const 0
    call $f61033
    i32.const 500
    i32.const 0
    call $f52516
    local.get $p0
    i32.load offset=96
    i32.load offset=68
    local.get $p1
    i32.const 0
    call $f61033
    local.get $p0
    i32.load offset=252
    local.get $p1
    i32.const 0
    call $f61055
    block $B1 (result i32)
      local.get $l2
      i32.load offset=12
      local.tee $p1
      local.get $l2
      i32.load offset=8
      local.tee $l3
      i32.gt_s
      if $I2
        local.get $p0
        i32.load offset=96
        i32.load offset=44
        i32.const 3827120
        i32.load
        i32.const 0
        call $f61033
        local.get $p0
        i32.load offset=96
        i32.load offset=68
        i32.const 3827116
        i32.load
        i32.const 0
        call $f61033
        local.get $p0
        i32.load offset=252
        i32.const 3834404
        i32.load
        i32.const 0
        call $f61055
        i32.const 3834420
        br $B1
      end
      local.get $p0
      i32.load offset=96
      i32.load offset=44
      local.set $l4
      local.get $p1
      local.get $l3
      i32.eq
      if $I3
        local.get $l4
        i32.const 3827112
        i32.load
        i32.const 0
        call $f61033
        local.get $p0
        i32.load offset=96
        i32.load offset=68
        i32.const 3827112
        i32.load
        i32.const 0
        call $f61033
        i32.const 3827112
        br $B1
      end
      local.get $l4
      i32.const 3827116
      i32.load
      i32.const 0
      call $f61033
      local.get $p0
      i32.load offset=96
      i32.load offset=68
      i32.const 3827120
      i32.load
      i32.const 0
      call $f61033
      local.get $p0
      i32.load offset=252
      i32.const 3834400
      i32.load
      i32.const 0
      call $f61055
      i32.const 3834424
    end
    local.set $p1
    local.get $p0
    i32.load offset=252
    local.get $p1
    i32.load
    i32.const 0
    call $f61055
    local.get $l2
    i32.const 16
    i32.add
    global.set $g0)
