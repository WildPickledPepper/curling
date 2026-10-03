  (func $f32444 (type $t0) (param $p0 i32) (param $p1 i32) (result i32)
    (local $l2 i32)
    i32.const 4658904
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3753376
      call $f1661
      i32.const 4658904
      i32.const 1
      i32.store8
    end
    local.get $p0
    local.get $p0
    call $f32438
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
    block $B2 (result i32)
      local.get $p1
      i32.const 0
      i32.const 0
      call $f54398
      i32.eqz
      if $I3
        local.get $p0
        local.get $p0
        call $f32441
        br $B2
      end
      local.get $p0
      local.get $p0
      call $f32438
    end
    i32.const 0
    call $f54361)
