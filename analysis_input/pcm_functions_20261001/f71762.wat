  (func $f71762 (type $t2) (param $p0 i32) (param $p1 i32) (param $p2 i32)
    (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32)
    global.get $g0
    i32.const 32
    i32.sub
    local.tee $l4
    global.set $g0
    block $B0
      local.get $p0
      i32.load offset=4
      local.tee $l3
      i32.eqz
      br_if $B0
      local.get $l3
      i32.load offset=8
      i32.eqz
      br_if $B0
      local.get $l4
      i32.const 0
      i32.store offset=24
      local.get $l4
      i64.const 0
      i64.store offset=16
      local.get $l4
      i64.const 4575657221408423936
      i64.store offset=8
      local.get $l4
      i64.const 0
      i64.store
      local.get $p1
      local.get $l4
      call $f69800
      drop
      local.get $p1
      local.get $p2
      call $f69798
      drop
      local.get $l3
      i32.load offset=8
      local.tee $l3
      local.get $l3
      local.get $p1
      call $f71763
    end
    local.get $l4
    i32.const 0
    i32.store offset=24
    local.get $l4
    i64.const 0
    i64.store offset=16
    local.get $l4
    i64.const 4575657221408423936
    i64.store offset=8
    local.get $l4
    i64.const 0
    i64.store
    local.get $p1
    local.get $l4
    call $f69800
    drop
    local.get $p1
    i32.const -1
    call $f69798
    drop
    block $B1
      local.get $p0
      i32.load8_u offset=336
      i32.eqz
      br_if $B1
      local.get $p0
      i32.load offset=156
      local.get $p0
      i32.load offset=108
      i32.add
      i32.const 0
      local.get $p0
      i32.load offset=216
      i32.sub
      i32.eq
      br_if $B1
      global.get $g0
      i32.const 32
      i32.sub
      local.tee $l3
      global.set $g0
      block $B2
        local.get $p0
        i32.const 52
        i32.add
        local.tee $l5
        i32.load offset=168
        local.tee $p0
        i32.eqz
        br_if $B2
        local.get $p0
        i32.load offset=8
        i32.eqz
        br_if $B2
        local.get $l3
        i32.const 0
        i32.store offset=24
        local.get $l3
        i64.const 0
        i64.store offset=16
        local.get $l3
        i64.const 4575657221408423936
        i64.store offset=8
        local.get $l3
        i64.const 0
        i64.store
        local.get $p1
        local.get $l3
        call $f69800
        drop
        local.get $p1
        local.get $p2
        call $f69798
        drop
        local.get $p0
        i32.load offset=8
        local.tee $p0
        local.get $p0
        local.get $p1
        call $f71880
      end
      local.get $l5
      i32.load offset=204
      local.tee $l7
      if $I3
        i32.const 0
        local.set $p0
        loop $L4
          block $B5
            local.get $l5
            i32.load offset=200
            local.get $p0
            i32.const 3
            i32.shl
            i32.add
            i32.load
            local.tee $l6
            i32.eqz
            br_if $B5
            local.get $l6
            i32.load offset=8
            i32.eqz
            br_if $B5
            local.get $l3
            i32.const 0
            i32.store offset=24
            local.get $l3
            i64.const 0
            i64.store offset=16
            local.get $l3
            i64.const 4575657221408423936
            i64.store offset=8
            local.get $l3
            i64.const 0
            i64.store
            local.get $p1
            local.get $l3
            call $f69800
            drop
            local.get $p1
            local.get $p2
            call $f69798
            drop
            local.get $l6
            i32.load offset=8
            local.tee $l6
            local.get $l6
            local.get $p1
            call $f71880
            local.get $l5
            i32.load offset=204
            local.set $l7
          end
          local.get $p0
          i32.const 1
          i32.add
          local.tee $p0
          local.get $l7
          i32.lt_u
          br_if $L4
        end
      end
      global.get $g0
      i32.const 32
      i32.sub
      local.tee $p0
      global.set $g0
      block $B6
        local.get $l5
        i32.const 4
        i32.add
        local.tee $l5
        i32.load offset=12
        local.tee $l6
        i32.eqz
        br_if $B6
        local.get $l6
        i32.load offset=588
        i32.eqz
        br_if $B6
        local.get $p0
        i32.const 0
        i32.store offset=24
        local.get $p0
        i64.const 0
        i64.store offset=16
        local.get $p0
        i64.const 4575657221408423936
        i64.store offset=8
        local.get $p0
        i64.const 0
        i64.store
        local.get $p1
        local.get $p0
        call $f69800
        drop
        local.get $p1
        local.get $p2
        call $f69798
        drop
        local.get $l5
        i32.load offset=12
        i32.load offset=588
        local.tee $l6
        local.get $l6
        local.get $p1
        call $f71881
        local.get $p0
        i32.const 0
        i32.store offset=24
        local.get $p0
        i64.const 0
        i64.store offset=16
        local.get $p0
        i64.const 4575657221408423936
        i64.store offset=8
        local.get $p0
        i64.const 0
        i64.store
        local.get $p1
        local.get $p0
        call $f69800
        drop
        local.get $p1
        i32.const -1
        call $f69798
        drop
      end
      block $B7
        local.get $l5
        i32.load offset=60
        local.tee $l6
        i32.eqz
        br_if $B7
        local.get $l6
        i32.load offset=588
        i32.eqz
        br_if $B7
        local.get $p0
        i32.const 0
        i32.store offset=24
        local.get $p0
        i64.const 0
        i64.store offset=16
        local.get $p0
        i64.const 4575657221408423936
        i64.store offset=8
        local.get $p0
        i64.const 0
        i64.store
        local.get $p1
        local.get $p0
        call $f69800
        drop
        local.get $p1
        local.get $p2
        call $f69798
        drop
        local.get $l5
        i32.load offset=60
        i32.load offset=588
        local.tee $l5
        local.get $l5
        local.get $p1
        call $f71881
        local.get $p0
        i32.const 0
        i32.store offset=24
        local.get $p0
        i64.const 0
        i64.store offset=16
        local.get $p0
        i64.const 4575657221408423936
        i64.store offset=8
        local.get $p0
        i64.const 0
        i64.store
        local.get $p1
        local.get $p0
        call $f69800
        drop
        local.get $p1
        i32.const -1
        call $f69798
        drop
      end
      local.get $p0
      i32.const 32
      i32.add
      global.set $g0
      local.get $l3
      i32.const 32
      i32.add
      global.set $g0
    end
    local.get $l4
    i32.const 32
    i32.add
    global.set $g0)