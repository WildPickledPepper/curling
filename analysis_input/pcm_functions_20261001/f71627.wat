  (func $f71627 (type $t0) (param $p0 i32) (param $p1 i32) (result i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32)
    block $B0
      local.get $p0
      i32.load offset=44
      local.tee $l3
      i32.const 476
      i32.and
      i32.eqz
      br_if $B0
      local.get $l3
      i32.const 4194304
      i32.and
      i32.eqz
      br_if $B0
      local.get $p0
      i32.load offset=4
      i32.load offset=40
      i32.load offset=2168
      local.set $l2
      global.get $g0
      i32.const 16
      i32.sub
      local.tee $l4
      global.set $g0
      local.get $l4
      local.get $p0
      local.tee $l3
      i32.store offset=12
      local.get $p0
      local.get $p0
      i32.load offset=44
      i32.const 2097152
      i32.or
      i32.store offset=44
      local.get $l2
      i32.const 16
      i32.add
      local.set $l6
      block $B1
        local.get $l2
        i32.load offset=20
        local.tee $l5
        local.get $l2
        i32.load offset=28
        local.tee $l7
        i32.eq
        if $I2
          local.get $l3
          local.get $l5
          i32.store offset=52
          local.get $l2
          i32.load offset=20
          local.tee $l5
          local.get $l2
          i32.load offset=24
          i32.const 2147483647
          i32.and
          i32.ge_u
          if $I3
            local.get $l6
            local.get $l4
            i32.const 12
            i32.add
            call $f71712
            br $B1
          end
          local.get $l2
          i32.load offset=16
          local.get $l5
          i32.const 2
          i32.shl
          i32.add
          local.get $l3
          i32.store
          local.get $l2
          local.get $l2
          i32.load offset=20
          i32.const 1
          i32.add
          i32.store offset=20
          br $B1
        end
        local.get $l4
        local.get $l2
        i32.load offset=16
        local.get $l7
        i32.const 2
        i32.shl
        i32.add
        i32.load
        local.tee $l3
        i32.store offset=8
        local.get $l3
        local.get $l5
        i32.store offset=52
        block $B4
          local.get $l2
          i32.load offset=20
          local.tee $l5
          local.get $l2
          i32.load offset=24
          i32.const 2147483647
          i32.and
          i32.ge_u
          if $I5
            local.get $l6
            local.get $l4
            i32.const 8
            i32.add
            call $f71712
            br $B4
          end
          local.get $l2
          i32.load offset=16
          local.get $l5
          i32.const 2
          i32.shl
          i32.add
          local.get $l3
          i32.store
          local.get $l2
          local.get $l2
          i32.load offset=20
          i32.const 1
          i32.add
          i32.store offset=20
        end
        local.get $l4
        i32.load offset=12
        local.tee $l3
        local.get $l2
        i32.load offset=28
        i32.store offset=52
        local.get $l2
        i32.load offset=16
        local.get $l2
        i32.load offset=28
        i32.const 2
        i32.shl
        i32.add
        local.get $l3
        i32.store
      end
      local.get $l2
      local.get $l2
      i32.load offset=28
      i32.const 1
      i32.add
      i32.store offset=28
      local.get $l4
      i32.const 16
      i32.add
      global.set $g0
      local.get $p0
      local.get $p0
      i32.load offset=44
      i32.const -4194305
      i32.and
      i32.store offset=44
    end
    local.get $p0
    i32.load offset=28
    call $f71419
    local.set $l3
    local.get $p0
    i32.load offset=32
    call $f71419
    local.set $l2
    block $B6
      local.get $p0
      i32.load offset=4
      i32.load offset=40
      i32.load offset=1000
      i32.load offset=656
      local.tee $l4
      local.get $l3
      i64.load offset=144
      i64.const 9
      i64.shr_u
      i32.wrap_i64
      i32.const 5
      i32.shl
      i32.add
      i32.load8_u offset=4
      i32.const 2
      i32.and
      i32.eqz
      if $I7
        i32.const 0
        local.set $l3
        local.get $l2
        i32.eqz
        br_if $B6
        local.get $l4
        local.get $l2
        i64.load offset=144
        i64.const 9
        i64.shr_u
        i32.wrap_i64
        i32.const 5
        i32.shl
        i32.add
        i32.load8_u offset=4
        i32.const 2
        i32.and
        i32.eqz
        br_if $B6
      end
      block $B8
        local.get $p0
        i32.load offset=56
        br_if $B8
        local.get $p0
        local.get $p1
        call $f71628
        local.get $p0
        i32.load offset=56
        br_if $B8
        i32.const 0
        return
      end
      local.get $p0
      i32.const 25
      i32.add
      local.tee $p0
      local.get $p0
      i32.load8_u
      i32.const 32
      i32.or
      i32.store8
      i32.const 1
      local.set $l3
    end
    local.get $l3)