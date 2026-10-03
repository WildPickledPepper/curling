  (func $f78679 (type $t7) (param $p0 i32)
    (local $l1 i32) (local $l2 i32) (local $l3 i32)
    global.get $g0
    i32.const 32
    i32.sub
    local.tee $l1
    global.set $g0
    local.get $l1
    block $B0 (result i32)
      local.get $p0
      i32.load offset=16
      local.tee $l2
      i32.eqz
      if $I1
        i32.const 5
        call $f80140
        local.set $l2
        i32.const 0
        local.get $p0
        i32.load offset=8
        i32.const 19
        i32.shr_u
        i32.const 8188
        i32.and
        i32.const 4782372
        i32.add
        i32.load
        i32.load offset=28
        local.tee $l3
        local.get $l2
        i32.load offset=256
        i32.ge_u
        br_if $B0
        drop
        local.get $l2
        i32.load offset=248
        local.get $l3
        i32.const 2
        i32.shl
        i32.add
        i32.load
        br $B0
      end
      block $B2 (result i32)
        local.get $p0
        i32.load offset=20
        i32.const 2
        i32.eq
        if $I3
          local.get $p0
          i32.load offset=24
          br $B2
        end
        local.get $l2
        call $f1642
      end
      i32.load
    end
    i32.store offset=24
    local.get $l1
    i32.const 24
    i32.add
    call $f78677
    i32.load8_s
    local.tee $l2
    i32.const 0
    i32.lt_s
    if $I4
      local.get $l1
      local.get $l2
      i32.store8 offset=16
      local.get $l1
      local.get $l2
      i32.store8 offset=7
      i32.const 4758716
      i32.load
      local.get $p0
      local.get $l1
      i32.const 7
      i32.add
      call $f78676
    end
    i32.const 4130624
    i32.load
    local.get $p0
    i32.load offset=8
    i32.const 21
    i32.shr_u
    i32.const 4130620
    i32.load
    i32.sub
    i32.gt_u
    if $I5
      local.get $l1
      local.get $l2
      i32.store8 offset=6
      local.get $l1
      local.get $l2
      i32.store8 offset=8
      local.get $p0
      local.get $l1
      i32.const 6
      i32.add
      call $f78678
    end
    local.get $l1
    i32.const 32
    i32.add
    global.set $g0)
