  (func $f71451 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32)
    local.get $p1
    i32.load
    local.set $l4
    i32.const 52685
    local.set $l5
    block $B0
      block $B1 (result i32)
        block $B2
          block $B3
            local.get $p0
            i32.const 68
            i32.add
            local.tee $l7
            i32.load
            i32.const 5
            i32.sub
            br_table $B3 $B2 $B0
          end
          local.get $p0
          i32.const 120
          i32.add
          local.set $l3
          local.get $p0
          i32.const 116
          i32.add
          local.set $l6
          local.get $p0
          i32.const 122
          i32.add
          br $B1
        end
        local.get $p0
        i32.const 100
        i32.add
        local.set $l3
        local.get $p0
        i32.const 96
        i32.add
        local.set $l6
        local.get $p0
        i32.const 102
        i32.add
      end
      i32.load16_u
      local.set $l5
      local.get $l3
      i32.load16_u
      local.set $l2
      local.get $l6
      i32.load
      local.set $l3
    end
    local.get $l7
    local.get $p1
    call $f70398
    local.get $l4
    i32.const 5
    i32.sub
    i32.const 1
    i32.le_u
    if $I4
      local.get $p0
      i32.const 116
      i32.add
      local.get $p0
      i32.const 96
      i32.add
      local.get $l4
      i32.const 5
      i32.eq
      select
      local.set $p1
      local.get $l2
      i32.const 65535
      i32.and
      if $I5
        local.get $p1
        local.get $l5
        i32.store16 offset=6
        local.get $p1
        local.get $l2
        i32.store16 offset=4
        local.get $p1
        local.get $l3
        i32.store
        return
      end
      call $f69753
      local.tee $l2
      i32.const 2
      i32.const 3158048
      i32.const 3160701
      i32.const 109
      local.get $l2
      i32.load
      i32.load offset=8
      call_indirect $__indirect_function_table (type $t9)
      local.set $l2
      local.get $p1
      i32.const 1
      i32.store16 offset=4
      local.get $p1
      local.get $l2
      i32.store
      local.get $l2
      local.get $p0
      i32.load16_u offset=66
      i32.store16
      local.get $p0
      i32.const 1
      i32.store8 offset=65
      return
    end
    block $B6
      local.get $l2
      i32.const 65535
      i32.and
      i32.eqz
      br_if $B6
      local.get $l3
      i32.eqz
      br_if $B6
      local.get $p0
      i32.load8_u offset=65
      i32.eqz
      br_if $B6
      call $f69753
      local.tee $p0
      local.get $l3
      local.get $p0
      i32.load
      i32.load offset=12
      call_indirect $__indirect_function_table (type $t1)
    end)
