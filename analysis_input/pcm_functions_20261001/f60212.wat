  (func $f60212 (type $t8) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (result i32)
    (local $l4 i32)
    i32.const 4674531
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3773808
      call $f1661
      i32.const 3773088
      call $f1661
      i32.const 3753376
      call $f1661
      i32.const 3744496
      call $f1661
      i32.const 3744484
      call $f1661
      i32.const 3809188
      call $f1661
      i32.const 3809192
      call $f1661
      i32.const 3760068
      call $f1661
      i32.const 4674531
      i32.const 1
      i32.store8
    end
    i32.const 3760068
    i32.load
    call $f1446
    local.tee $p3
    local.get $p1
    i32.store offset=12
    local.get $p3
    local.get $p2
    i32.store offset=8
    local.get $p0
    i32.load offset=12
    local.set $p0
    i32.const 3744484
    i32.load
    call $f1446
    local.tee $p1
    local.get $p3
    i32.const 3809188
    i32.load
    i32.const 0
    call $f36112
    block $B1
      local.get $p0
      local.get $p1
      i32.const 3773088
      i32.load
      call $f2917
      local.tee $p0
      i32.eqz
      br_if $B1
      local.get $p0
      i32.load offset=20
      local.set $l4
      i32.const 3744496
      i32.load
      call $f1446
      local.tee $p1
      local.get $p3
      i32.const 3809192
      i32.load
      i32.const 0
      call $f36112
      block $B2 (result i32)
        block $B3
          local.get $l4
          local.get $p1
          i32.const 3773808
          i32.load
          call $f2917
          local.tee $p3
          i32.eqz
          br_if $B3
          local.get $p3
          i32.load offset=16
          local.set $l4
          i32.const 3753376
          i32.load
          local.tee $p1
          i32.load offset=116
          i32.eqz
          if $I4
            local.get $p1
            call $f65192
          end
          local.get $l4
          i32.const 0
          i32.const 0
          call $f54398
          i32.eqz
          br_if $B3
          local.get $p3
          i32.const 16
          i32.add
          br $B2
        end
        local.get $p0
        i32.load offset=16
        local.set $p3
        i32.const 3753376
        i32.load
        local.tee $l4
        i32.load offset=116
        i32.eqz
        if $I5
          local.get $l4
          call $f65192
        end
        i32.const 0
        local.set $l4
        local.get $p3
        i32.const 0
        i32.const 0
        call $f54398
        i32.eqz
        br_if $B1
        local.get $p0
        i32.const 16
        i32.add
      end
      i32.load
      local.set $l4
    end
    local.get $l4)