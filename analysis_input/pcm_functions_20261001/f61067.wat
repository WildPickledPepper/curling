  (func $f61067 (type $t4) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32)
    i32.const 4675137
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3748808
      call $f1661
      i32.const 3792608
      call $f1661
      i32.const 3773132
      call $f1661
      i32.const 3827820
      call $f1661
      i32.const 3843868
      call $f1661
      i32.const 3834396
      call $f1661
      i32.const 3817856
      call $f1661
      i32.const 3843860
      call $f1661
      i32.const 4675137
      i32.const 1
      i32.store8
    end
    block $B1 (result i32)
      local.get $p1
      i32.load offset=20
      i32.const 3834396
      i32.load
      i32.const 0
      call $f53861
      if $I2
        local.get $p0
        local.get $p2
        i32.store offset=36
        local.get $p0
        local.get $p2
        i32.store offset=44
        i32.const 3827820
        i32.load
        local.get $p2
        i32.const 0
        call $f53732
        local.set $p1
        i32.const 3748808
        i32.load
        local.tee $p2
        i32.load offset=116
        i32.eqz
        if $I3
          local.get $p2
          call $f65192
        end
        local.get $p0
        i32.const 44
        i32.add
        local.set $p2
        local.get $p1
        i32.const 0
        call $f42976
        i32.const 3843860
        local.set $p1
        local.get $p0
        i32.load offset=152
        i32.const 0
        i32.const 3773132
        i32.load
        call $f2903
        i32.const 3792608
        i32.load
        call $f34548
        br $B1
      end
      local.get $p0
      local.get $p2
      i32.store offset=40
      local.get $p0
      local.get $p2
      i32.store offset=48
      local.get $p0
      i32.const 48
      i32.add
      local.set $p2
      i32.const 3843868
      local.set $p1
      local.get $p0
      i32.load offset=152
      i32.const 1
      i32.const 3773132
      i32.load
      call $f2903
      i32.const 3792608
      i32.load
      call $f34548
    end
    local.tee $p0
    local.get $p2
    i32.load
    local.get $p0
    i32.load
    local.tee $p0
    i32.load offset=796
    local.get $p0
    i32.load offset=792
    call_indirect $__indirect_function_table (type $t2)
    local.get $p1
    i32.load
    i32.const 0
    call $f54416
    i32.const 3792608
    i32.load
    call $f34548
    local.tee $p0
    local.get $p2
    i32.load
    i32.const 3817856
    i32.load
    i32.const 0
    call $f53732
    local.get $p0
    i32.load
    local.tee $p0
    i32.load offset=796
    local.get $p0
    i32.load offset=792
    call_indirect $__indirect_function_table (type $t2))
