  (func $f71461 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l4
    global.set $g0
    local.get $p0
    i32.load offset=4
    local.tee $l2
    i32.const 0
    local.get $l2
    i32.load offset=44
    i32.load8_u offset=9
    i32.const 1
    i32.sub
    i32.const 2
    i32.lt_u
    select
    local.tee $l3
    if $I0 (result i32)
      local.get $l3
      i32.load offset=156
      i32.const -3
      i32.gt_u
    else
      i32.const 1
    end
    local.set $l9
    local.get $l2
    i32.load offset=40
    local.set $l5
    local.get $l2
    i32.load offset=28
    local.set $l6
    local.get $l2
    i32.load offset=20
    local.set $l2
    local.get $l4
    local.get $p0
    i32.store offset=8
    local.get $l4
    local.get $l2
    i32.store
    local.get $l4
    local.get $l2
    local.get $l6
    i32.const 2
    i32.shl
    i32.add
    i32.store offset=4
    local.get $l4
    call $f71586
    local.tee $l2
    if $I1
      local.get $l3
      i32.const 0
      i32.ne
      local.set $l10
      loop $L2
        local.get $l2
        i32.const 4
        i32.add
        local.set $l3
        block $B3
          block $B4
            block $B5
              local.get $l2
              i32.load8_u offset=24
              br_table $B5 $B4 $B3
            end
            local.get $l3
            i32.const 4
            i32.sub
            local.tee $l2
            call $f71632
            local.get $l9
            i32.eqz
            br_if $B3
            local.get $l2
            local.get $l10
            call $f71642
            br $B3
          end
          local.get $l3
          i32.const 52
          i32.add
          local.tee $l2
          local.get $l2
          i32.load16_u
          i32.const 32
          i32.or
          i32.store16
          local.get $l3
          i32.load8_u offset=21
          local.tee $l2
          i32.const 32
          i32.and
          br_if $B3
          local.get $l3
          local.get $l2
          i32.const 32
          i32.or
          i32.store8 offset=21
          local.get $l5
          local.get $l5
          i32.load offset=92
          local.tee $l2
          local.get $l5
          i32.load offset=68
          i32.lt_u
          if $I6 (result i32)
            local.get $l5
            i32.load offset=64
            local.tee $l7
            local.get $l2
            i32.const 2
            i32.shl
            i32.add
            local.tee $l8
            i32.load
            local.set $l6
            local.get $l8
            local.get $l7
            local.get $l3
            i32.load offset=8
            local.tee $l3
            i32.const 2
            i32.shl
            local.tee $l8
            i32.add
            i32.load
            local.tee $l7
            i32.store
            local.get $l5
            i32.load offset=64
            local.get $l8
            i32.add
            local.get $l6
            i32.store
            local.get $l6
            local.get $l3
            i32.store offset=8
            local.get $l7
            local.get $l2
            i32.store offset=8
            local.get $l5
            i32.load offset=92
          else
            local.get $l2
          end
          i32.const 1
          i32.add
          i32.store offset=92
        end
        local.get $l4
        call $f71586
        local.tee $l2
        br_if $L2
      end
    end
    local.get $p0
    local.get $p1
    call $f71460
    local.get $l4
    i32.const 16
    i32.add
    global.set $g0)