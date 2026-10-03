  (func $f71729 (type $t7) (param $p0 i32)
    (local $l1 i32) (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32)
    local.get $p0
    i32.load offset=32
    local.tee $l1
    if $I0
      loop $L1
        local.get $l1
        i32.const 0
        call $f71460
        local.get $l1
        i32.load
        local.tee $l1
        br_if $L1
      end
    end
    i32.const 1
    local.set $l4
    local.get $p0
    i32.load offset=44
    i32.load8_u offset=9
    i32.const 1
    i32.sub
    local.tee $l1
    i32.const 1
    i32.le_u
    if $I2
      local.get $p0
      i32.load offset=156
      i32.const -3
      i32.gt_u
      local.set $l4
    end
    local.get $p0
    i32.load offset=28
    local.tee $l5
    if $I3
      local.get $p0
      i32.load offset=40
      local.set $l3
      local.get $p0
      i32.load offset=20
      local.set $p0
      local.get $l1
      i32.const 2
      i32.lt_u
      local.set $l9
      loop $L4
        local.get $l5
        i32.const 1
        i32.sub
        local.set $l5
        block $B5
          block $B6
            block $B7
              local.get $p0
              i32.load
              local.tee $l1
              i32.load8_u offset=20
              br_table $B7 $B6 $B5
            end
            local.get $l1
            i32.const 4
            i32.sub
            local.tee $l1
            call $f71632
            local.get $l4
            i32.eqz
            br_if $B5
            local.get $l1
            local.get $l9
            call $f71642
            br $B5
          end
          local.get $l1
          i32.const 52
          i32.add
          local.tee $l2
          local.get $l2
          i32.load16_u
          i32.const 32
          i32.or
          i32.store16
          local.get $l1
          i32.load8_u offset=21
          local.tee $l2
          i32.const 32
          i32.and
          br_if $B5
          local.get $l1
          local.get $l2
          i32.const 32
          i32.or
          i32.store8 offset=21
          local.get $l3
          local.get $l3
          i32.load offset=92
          local.tee $l2
          local.get $l3
          i32.load offset=68
          i32.lt_u
          if $I8 (result i32)
            local.get $l3
            i32.load offset=64
            local.tee $l6
            local.get $l2
            i32.const 2
            i32.shl
            i32.add
            local.tee $l7
            i32.load
            local.set $l8
            local.get $l7
            local.get $l6
            local.get $l1
            i32.load offset=8
            local.tee $l1
            i32.const 2
            i32.shl
            local.tee $l7
            i32.add
            i32.load
            local.tee $l6
            i32.store
            local.get $l3
            i32.load offset=64
            local.get $l7
            i32.add
            local.get $l8
            i32.store
            local.get $l8
            local.get $l1
            i32.store offset=8
            local.get $l6
            local.get $l2
            i32.store offset=8
            local.get $l3
            i32.load offset=92
          else
            local.get $l2
          end
          i32.const 1
          i32.add
          i32.store offset=92
        end
        local.get $p0
        i32.const 4
        i32.add
        local.set $p0
        local.get $l5
        br_if $L4
      end
    end)