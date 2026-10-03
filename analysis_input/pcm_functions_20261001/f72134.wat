  (func $f72134 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32)
    local.get $p0
    i32.const 16
    i32.add
    local.get $p1
    i32.const 48
    i32.add
    i32.const 0
    i32.const 0
    i32.const 0
    call $f71997
    local.get $p1
    i32.load16_u offset=24
    local.tee $l3
    if $I0
      local.get $p1
      i32.const 20
      i32.add
      local.get $p1
      i32.load offset=20
      local.get $l3
      i32.const 1
      i32.eq
      select
      local.set $l4
      local.get $p1
      i32.const 28
      i32.add
      local.set $l5
      local.get $p0
      i32.const 5584
      i32.add
      local.set $l6
      local.get $p1
      i32.load16_u offset=4
      i32.const -9
      i32.and
      i32.const 5
      i32.eq
      local.set $l7
      loop $L1
        local.get $l4
        local.get $l2
        i32.const 2
        i32.shl
        local.tee $l8
        i32.add
        i32.load
        local.tee $p0
        i32.load offset=40
        i32.const 52
        i32.add
        local.get $p0
        i32.const 112
        i32.add
        local.get $p0
        i32.load8_u offset=36
        i32.const 64
        i32.and
        select
        i32.load8_u
        i32.const 2
        i32.and
        if $I2
          local.get $l6
          local.get $p0
          i32.const 32
          i32.add
          local.get $p1
          local.get $p1
          i32.load16_u offset=4
          i32.const 2
          i32.shl
          i32.const 3179804
          i32.add
          i32.load
          i32.add
          local.get $l7
          local.get $p1
          i32.load offset=36
          i32.const 0
          i32.const 0
          call $f71893
          local.set $p0
          local.get $l5
          local.get $p1
          i32.load offset=28
          local.get $p1
          i32.load16_u offset=32
          i32.const 1
          i32.eq
          select
          local.get $l8
          i32.add
          local.get $p0
          i32.store
        end
        local.get $l2
        i32.const 1
        i32.add
        local.tee $l2
        local.get $l3
        i32.ne
        br_if $L1
      end
    end)