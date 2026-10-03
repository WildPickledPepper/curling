  (func $f78236 (type $t5) (param $p0 i32) (result i32)
    (local $l1 i32) (local $l2 i32) (local $l3 i32) (local $l4 i32)
    local.get $p0
    i32.load
    local.tee $l1
    i32.load offset=76
    local.tee $l3
    local.get $p0
    i32.load offset=4
    local.tee $l2
    i32.add
    i32.load8_u
    local.set $p0
    local.get $l1
    i32.load offset=28
    local.tee $l4
    local.get $l2
    i32.const 2
    i32.shl
    i32.add
    i32.load
    local.tee $l1
    i32.const -1
    i32.ne
    if $I0
      loop $L1
        local.get $l1
        local.get $l3
        i32.add
        i32.load8_u
        local.tee $l2
        local.get $p0
        i32.xor
        i32.const 4
        i32.and
        local.get $p0
        local.get $l2
        i32.or
        i32.const -5
        i32.and
        i32.or
        local.set $p0
        local.get $l4
        local.get $l1
        i32.const 2
        i32.shl
        i32.add
        i32.load
        local.tee $l1
        i32.const -1
        i32.ne
        br_if $L1
      end
    end
    local.get $p0
    i32.const 254
    i32.and
    local.get $p0
    local.get $p0
    i32.const 2
    i32.and
    select
    i32.const 255
    i32.and)
