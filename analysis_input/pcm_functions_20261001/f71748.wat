  (func $f71748 (type $t6) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32)
    (local $l5 i32)
    local.get $p1
    local.get $p3
    local.get $p4
    i32.sub
    i32.const 28
    i32.div_s
    i32.const 2
    i32.shl
    i32.add
    local.get $p2
    local.get $p4
    i32.sub
    i32.const 28
    i32.div_s
    i32.store
    local.get $p3
    i32.load offset=24
    local.tee $p2
    i32.const 1
    i32.and
    i32.eqz
    if $I0
      local.get $p4
      i32.const 28
      i32.add
      local.set $l5
      loop $L1
        local.get $p0
        local.get $p1
        local.get $p3
        local.get $p4
        local.get $p2
        i32.const 1
        i32.shr_u
        i32.const 28
        i32.mul
        i32.add
        local.get $p4
        call $f71748
        local.get $p3
        local.get $p4
        i32.sub
        local.set $p2
        local.get $p1
        local.get $l5
        local.get $p3
        i32.load offset=24
        i32.const 1
        i32.shr_u
        i32.const 28
        i32.mul
        i32.add
        i32.const 0
        local.get $p4
        select
        local.tee $p3
        local.get $p4
        i32.sub
        i32.const 28
        i32.div_s
        i32.const 2
        i32.shl
        i32.add
        local.get $p2
        i32.const 28
        i32.div_s
        i32.store
        local.get $p3
        i32.load offset=24
        local.tee $p2
        i32.const 1
        i32.and
        i32.eqz
        br_if $L1
      end
    end)