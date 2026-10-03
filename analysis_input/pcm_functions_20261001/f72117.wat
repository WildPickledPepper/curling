  (func $f72117 (type $t4) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32)
    (local $l4 i32) (local $l5 i32) (local $l6 i32)
    global.get $g0
    i32.const 224
    i32.sub
    local.tee $l4
    global.set $g0
    block $B0
      local.get $p1
      i32.load offset=56
      local.get $p1
      i32.const 48
      i32.add
      local.tee $l6
      local.get $p1
      i32.load offset=52
      local.tee $l5
      i32.const 22
      i32.shr_u
      i32.const 60
      i32.and
      i32.const 3181092
      i32.add
      i32.load
      i32.add
      i32.const 8
      i32.add
      local.get $l5
      i32.const 1
      i32.and
      select
      i32.load8_u
      i32.const 8
      i32.and
      i32.eqz
      if $I1
        local.get $p0
        i32.const 16
        i32.add
        local.get $l6
        i32.const 0
        i32.const 0
        local.get $l4
        i32.const 0
        local.get $p1
        i32.load16_u offset=24
        i32.const 9
        i32.lt_u
        select
        local.get $p0
        i32.const 4801
        i32.add
        i32.load8_u
        select
        local.tee $l5
        local.get $p2
        call $f71997
        local.get $p1
        i32.const 20
        i32.add
        local.get $p0
        local.get $p1
        local.get $p3
        local.get $l5
        local.get $p2
        call $f72118
        local.get $p1
        i32.load offset=16
        i32.eqz
        br_if $B0
        local.get $p1
        i32.const 12
        i32.add
        call $f71928
        br $B0
      end
      local.get $p0
      i32.const 16
      i32.add
      local.get $l6
      i32.const 1
      i32.const 0
      local.get $p2
      call $f71997
      local.get $p1
      i32.const 20
      i32.add
      local.get $p0
      local.get $p1
      local.get $p3
      i32.const 0
      local.get $p2
      call $f72118
    end
    local.get $p1
    local.get $p0
    i32.const 5936
    i32.add
    local.tee $p2
    i32.load
    i32.store offset=44
    local.get $l4
    local.get $p1
    i32.store offset=220
    block $B2
      local.get $p2
      i32.load
      local.tee $p2
      local.get $p0
      i32.const 5940
      i32.add
      i32.load
      i32.const 2147483647
      i32.and
      i32.ge_u
      if $I3
        local.get $p0
        i32.const 5932
        i32.add
        local.get $l4
        i32.const 220
        i32.add
        call $f72119
        br $B2
      end
      local.get $p0
      i32.load offset=5932
      local.get $p2
      i32.const 2
      i32.shl
      i32.add
      local.get $p1
      i32.store
      local.get $p0
      local.get $p0
      i32.load offset=5936
      i32.const 1
      i32.add
      i32.store offset=5936
    end
    local.get $l4
    i32.const 224
    i32.add
    global.set $g0)