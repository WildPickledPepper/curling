  (func $f78661 (type $t0) (param $p0 i32) (param $p1 i32) (result i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32)
    i32.const 4742356
    i32.load
    local.tee $l2
    i32.eqz
    if $I0
      i32.const -1
      return
    end
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l5
    global.set $g0
    local.get $l2
    i32.load offset=124
    local.tee $l3
    i32.const 1
    i32.add
    local.tee $l4
    local.get $l2
    i32.load offset=128
    i32.const 1
    i32.shr_u
    i32.gt_u
    if $I1
      local.get $l2
      i32.const 116
      i32.add
      call $f580
    end
    local.get $l2
    local.get $l4
    i32.store offset=124
    local.get $l2
    i32.load offset=116
    local.get $l3
    i32.const 3
    i32.shl
    i32.add
    local.tee $l3
    local.get $p1
    i32.store offset=4
    local.get $l3
    local.get $p0
    i32.store
    local.get $l2
    i32.load offset=36
    if $I2
      local.get $l2
      i32.load offset=28
      local.set $l4
      loop $L3
        local.get $l5
        local.get $l4
        i64.load
        i64.store
        local.get $l5
        local.get $l4
        i32.load offset=8
        local.tee $l3
        i32.const 232
        i32.add
        local.get $l3
        i32.load offset=232
        local.get $l3
        i32.load8_u offset=252
        i32.const 1
        i32.eq
        select
        i32.store offset=8
        local.get $l5
        local.get $l4
        i32.load offset=8
        local.tee $l3
        i32.const 260
        i32.add
        local.get $l3
        i32.load offset=260
        local.get $l3
        i32.load8_u offset=280
        i32.const 1
        i32.eq
        select
        i32.store offset=12
        local.get $l5
        local.get $p1
        local.get $p0
        call_indirect $__indirect_function_table (type $t1)
        local.get $l4
        i32.const 24
        i32.add
        local.tee $l4
        local.get $l2
        i32.load offset=28
        local.get $l2
        i32.load offset=36
        i32.const 24
        i32.mul
        i32.add
        i32.ne
        br_if $L3
      end
    end
    local.get $l5
    i32.const 16
    i32.add
    global.set $g0
    i32.const 0)
