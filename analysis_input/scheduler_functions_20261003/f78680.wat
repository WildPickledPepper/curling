  (func $f78680 (type $t7) (param $p0 i32)
    (local $l1 i32) (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32)
    global.get $g0
    i32.const 32
    i32.sub
    local.tee $l3
    global.set $g0
    local.get $l3
    block $B0 (result i32)
      local.get $p0
      i32.load offset=16
      local.tee $l1
      i32.eqz
      if $I1
        i32.const 5
        call $f80140
        local.set $l1
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
        local.tee $l2
        local.get $l1
        i32.load offset=256
        i32.ge_u
        br_if $B0
        drop
        local.get $l1
        i32.load offset=248
        local.get $l2
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
        local.get $l1
        call $f1642
      end
      i32.load
    end
    i32.store offset=24
    local.get $l3
    i32.const 24
    i32.add
    call $f78677
    i32.load8_s
    local.tee $l1
    i32.const 0
    i32.lt_s
    if $I4
      local.get $l3
      local.get $l1
      i32.store8 offset=16
      local.get $l3
      local.get $l1
      i32.store8 offset=15
      i32.const 4758716
      i32.load
      local.set $l2
      global.get $g0
      i32.const 32
      i32.sub
      local.tee $l1
      global.set $g0
      local.get $l2
      i32.load offset=88
      local.set $l2
      local.get $l3
      i32.load8_u offset=15
      local.set $l4
      local.get $l1
      local.get $p0
      i32.load offset=4
      i32.store offset=28
      local.get $l1
      i32.const 16
      i32.add
      local.get $l2
      local.get $l4
      i32.const 127
      i32.and
      local.tee $l4
      i32.const 124
      i32.mul
      i32.add
      local.tee $p0
      i32.const 8
      i32.add
      local.tee $l6
      local.get $l1
      i32.const 28
      i32.add
      call $f66830
      block $B5
        local.get $l1
        i32.load offset=16
        local.get $p0
        i32.load offset=8
        local.get $p0
        i32.load offset=12
        i32.const 3
        i32.mul
        i32.add
        i32.const 12
        i32.add
        i32.ne
        br_if $B5
        local.get $p0
        i32.load offset=68
        local.get $p0
        i32.const 80
        i32.add
        local.tee $l5
        i32.load
        local.tee $l7
        local.get $p0
        i32.load offset=76
        i32.sub
        i32.le_u
        if $I6
          local.get $l2
          local.get $l4
          i32.const 124
          i32.mul
          i32.add
          i32.const 56
          i32.add
          call $f78675
          local.get $l5
          i32.load
          local.set $l7
        end
        local.get $l2
        local.get $l4
        i32.const 124
        i32.mul
        i32.add
        local.tee $p0
        i32.load offset=60
        local.get $p0
        i32.load offset=84
        local.get $l7
        i32.and
        i32.const 2
        i32.shl
        i32.add
        local.get $l1
        i32.load offset=28
        i32.store
        local.get $l5
        local.get $l5
        i32.load
        local.tee $l7
        i32.const 1
        i32.add
        i32.store
        local.get $l6
        local.get $l1
        i32.const 28
        i32.add
        call $f67441
        local.get $l7
        i32.store
        local.get $l1
        i32.const 8
        i32.add
        local.get $p0
        i32.const 32
        i32.add
        local.get $l1
        i32.const 28
        i32.add
        call $f66830
        local.get $l1
        i32.load offset=8
        local.tee $l6
        local.get $p0
        i32.load offset=32
        local.get $p0
        i32.load offset=36
        i32.const 3
        i32.mul
        i32.add
        i32.const 12
        i32.add
        i32.eq
        br_if $B5
        block $B7
          local.get $l6
          i32.load offset=8
          local.tee $l5
          local.get $p0
          i32.load offset=108
          i32.lt_u
          br_if $B7
          local.get $p0
          i32.load offset=112
          local.get $l5
          i32.le_u
          br_if $B7
          local.get $l2
          local.get $l4
          i32.const 124
          i32.mul
          i32.add
          local.tee $p0
          i32.load offset=92
          local.get $p0
          i32.load offset=116
          local.get $l5
          i32.and
          i32.const 3
          i32.shl
          i32.add
          i64.const 0
          i64.store align=4
          local.get $l1
          i32.load offset=8
          local.set $l6
        end
        local.get $l6
        i32.const -2
        i32.store
        local.get $l2
        local.get $l4
        i32.const 124
        i32.mul
        i32.add
        i32.const 40
        i32.add
        local.tee $p0
        local.get $p0
        i32.load
        i32.const 1
        i32.sub
        i32.store
      end
      local.get $l1
      i32.const 32
      i32.add
      global.set $g0
    end
    local.get $l3
    i32.const 32
    i32.add
    global.set $g0)
