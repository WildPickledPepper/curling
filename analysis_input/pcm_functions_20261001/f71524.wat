  (func $f71524 (type $t7) (param $p0 i32)
    (local $l1 i32) (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32)
    local.get $p0
    i32.load offset=28
    local.set $l1
    local.get $p0
    i32.load offset=20
    drop
    global.get $g0
    i32.const -64
    i32.add
    local.tee $l2
    global.set $g0
    local.get $l2
    i32.const 8
    i32.add
    local.get $l1
    i32.load offset=976
    i32.load offset=1024
    local.tee $l3
    local.get $l3
    i32.load
    i32.load offset=84
    call_indirect $__indirect_function_table (type $t1)
    local.get $l1
    i32.const 2472
    i32.add
    i32.load
    if $I0
      local.get $l1
      i32.const 2420
      i32.add
      local.set $l5
      i32.const 0
      local.set $l3
      local.get $l1
      i32.load offset=2360
      i32.const 8
      i32.and
      i32.const 0
      i32.ne
      local.set $l6
      loop $L1
        block $B2
          local.get $l1
          i32.load offset=2468
          local.get $l3
          i32.const 3
          i32.shl
          i32.add
          i32.load offset=4
          local.tee $p0
          i32.const 0
          local.get $l2
          i32.const 8
          i32.add
          local.get $l6
          call $f71639
          i32.eqz
          br_if $B2
          local.get $p0
          i32.load8_u offset=46
          i32.const 4
          i32.and
          br_if $B2
          local.get $p0
          i32.load offset=28
          i32.load offset=4
          local.tee $l4
          i32.load offset=44
          i32.load8_u offset=9
          local.set $l7
          local.get $l2
          local.get $p0
          i32.load offset=32
          i32.load offset=4
          local.tee $p0
          i32.const 0
          local.get $p0
          i32.load offset=44
          i32.load8_u offset=9
          i32.const 1
          i32.sub
          i32.const 2
          i32.lt_u
          select
          local.tee $p0
          i32.store offset=52
          local.get $l2
          local.get $l4
          i32.const 0
          local.get $l7
          i32.const 1
          i32.sub
          i32.const 2
          i32.lt_u
          select
          local.tee $l4
          i32.store offset=48
          local.get $l2
          local.get $l4
          i32.load offset=48
          i32.store offset=56
          local.get $l2
          local.get $p0
          i32.load offset=48
          i32.store offset=60
          local.get $l1
          i32.load offset=2424
          local.tee $p0
          local.get $l1
          i32.load offset=2428
          i32.const 2147483647
          i32.and
          i32.ge_u
          if $I3
            local.get $l5
            local.get $l2
            i32.const 48
            i32.add
            call $f71417
            br $B2
          end
          local.get $l1
          i32.load offset=2420
          local.get $p0
          i32.const 4
          i32.shl
          i32.add
          local.tee $p0
          local.get $l2
          i64.load offset=48
          i64.store align=4
          local.get $p0
          local.get $l2
          i64.load offset=56
          i64.store offset=8 align=4
          local.get $l1
          local.get $l1
          i32.load offset=2424
          i32.const 1
          i32.add
          i32.store offset=2424
        end
        local.get $l3
        i32.const 1
        i32.add
        local.tee $l3
        local.get $l1
        i32.load offset=2472
        i32.lt_u
        br_if $L1
      end
    end
    local.get $l2
    i32.const -64
    i32.sub
    global.set $g0)