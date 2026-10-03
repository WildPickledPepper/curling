  (func $f78651 (type $t0) (param $p0 i32) (param $p1 i32) (result i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32)
    i32.const 4758240
    i32.load
    local.set $l5
    i32.const -1
    local.set $l6
    block $B0
      i32.const 4787792
      i32.load
      local.tee $l3
      i32.eqz
      br_if $B0
      block $B1
        local.get $l5
        i32.load offset=64
        local.tee $l2
        i32.load
        i32.eqz
        br_if $B1
        local.get $l2
        i32.load offset=8
        i32.eqz
        if $I2
          local.get $l2
          i32.const 8
          i32.add
          local.set $l2
          i32.const 1
          local.set $l4
          br $B1
        end
        local.get $l2
        i32.load offset=16
        i32.eqz
        if $I3
          local.get $l2
          i32.const 16
          i32.add
          local.set $l2
          i32.const 2
          local.set $l4
          br $B1
        end
        local.get $l2
        i32.load offset=24
        br_if $B0
        local.get $l2
        i32.const 24
        i32.add
        local.set $l2
        i32.const 3
        local.set $l4
      end
      local.get $l2
      local.get $p0
      i32.store
      local.get $l5
      i32.load offset=64
      local.get $l4
      i32.const 3
      i32.shl
      i32.add
      local.get $p1
      i32.store offset=4
      local.get $l3
      local.set $p0
      local.get $p0
      i32.load offset=192
      local.tee $p1
      i32.const 1
      i32.add
      local.tee $l3
      local.get $p0
      i32.load offset=196
      i32.const 1
      i32.shr_u
      i32.gt_u
      if $I4
        local.get $p0
        i32.const 184
        i32.add
        call $f580
      end
      local.get $p0
      local.get $l3
      i32.store offset=192
      local.get $p0
      i32.load offset=184
      local.get $p1
      i32.const 3
      i32.shl
      i32.add
      local.tee $p1
      local.get $l2
      i32.store offset=4
      local.get $p1
      i32.const 125795
      i32.store
      block $B5
        local.get $p0
        i32.load offset=32
        local.tee $l3
        i32.eqz
        br_if $B5
        local.get $l3
        i32.const 1
        i32.and
        local.set $l4
        i32.const 0
        local.set $p1
        local.get $l3
        i32.const 1
        i32.ne
        if $I6
          local.get $l3
          i32.const -2
          i32.and
          local.set $l5
          i32.const 0
          local.set $l3
          loop $L7
            local.get $p1
            i32.const 2
            i32.shl
            i32.const 248
            i32.and
            local.tee $l6
            local.get $p1
            i32.const 4
            i32.shr_u
            i32.const 268435452
            i32.and
            local.tee $l7
            local.get $p0
            i32.load offset=40
            i32.add
            i32.load
            i32.load
            i32.add
            i32.load
            local.get $l2
            i32.const 125795
            call_indirect $__indirect_function_table (type $t1)
            local.get $p0
            i32.load offset=40
            local.get $l7
            i32.add
            i32.load
            i32.load
            local.get $l6
            i32.add
            i32.load offset=4
            local.get $l2
            i32.const 125795
            call_indirect $__indirect_function_table (type $t1)
            local.get $p1
            i32.const 2
            i32.add
            local.set $p1
            local.get $l3
            i32.const 2
            i32.add
            local.tee $l3
            local.get $l5
            i32.ne
            br_if $L7
          end
        end
        local.get $l4
        i32.eqz
        br_if $B5
        local.get $p0
        i32.load offset=40
        local.get $p1
        i32.const 4
        i32.shr_u
        i32.const 268435452
        i32.and
        i32.add
        i32.load
        i32.load
        local.get $p1
        i32.const 63
        i32.and
        i32.const 2
        i32.shl
        i32.add
        i32.load
        local.get $l2
        i32.const 125795
        call_indirect $__indirect_function_table (type $t1)
      end
      i32.const 0
      local.set $l6
    end
    local.get $l6)
