  (func $f72200 (type $t0) (param $p0 i32) (param $p1 i32) (result i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l5
    global.set $g0
    local.get $p0
    i32.load offset=20
    local.tee $l2
    local.get $p1
    i32.add
    local.get $p0
    i32.load offset=4
    local.tee $l7
    local.get $p0
    i32.load offset=16
    local.tee $l9
    i32.const 2
    i32.shl
    i32.add
    i32.load
    local.tee $l6
    local.get $l2
    i32.add
    local.tee $l4
    i32.const 15
    i32.add
    i32.const -16
    i32.and
    local.get $l4
    i32.sub
    local.tee $l3
    i32.add
    local.get $p0
    i32.load offset=24
    local.tee $l4
    i32.gt_u
    if $I0
      local.get $p0
      i32.const 0
      i32.store offset=20
      local.get $p0
      local.get $l9
      i32.const 1
      i32.add
      local.tee $l2
      i32.store offset=16
      local.get $p0
      i32.load offset=8
      local.tee $l3
      local.get $l2
      i32.le_u
      if $I1
        block $B2
          local.get $l4
          i32.eqz
          if $I3
            i32.const 0
            local.set $l2
            br $B2
          end
          call $f69753
          local.tee $l2
          local.get $l4
          i32.const 3188617
          i32.const 3194348
          i32.const 88
          local.get $l2
          i32.load
          i32.load offset=8
          call_indirect $__indirect_function_table (type $t9)
          local.set $l2
          local.get $p0
          i32.load offset=8
          local.set $l3
        end
        local.get $l5
        local.get $l2
        i32.store offset=12
        block $B4
          local.get $l3
          local.get $p0
          i32.load offset=12
          i32.const 2147483647
          i32.and
          i32.ge_u
          if $I5
            local.get $p0
            i32.const 4
            i32.add
            local.get $l5
            i32.const 12
            i32.add
            call $f72370
            br $B4
          end
          local.get $p0
          i32.load offset=4
          local.get $l3
          i32.const 2
          i32.shl
          i32.add
          local.get $l2
          i32.store
          local.get $p0
          local.get $p0
          i32.load offset=8
          i32.const 1
          i32.add
          i32.store offset=8
        end
        local.get $p0
        i32.load offset=4
        local.set $l7
        local.get $p0
        i32.load offset=16
        local.set $l2
        local.get $p0
        i32.load offset=20
        local.set $l8
      end
      local.get $l7
      local.get $l2
      i32.const 2
      i32.shl
      i32.add
      i32.load
      local.tee $l6
      i32.const 15
      i32.add
      i32.const -16
      i32.and
      local.get $l6
      i32.sub
      local.set $l3
      local.get $l8
      local.set $l2
    end
    local.get $p0
    local.get $p1
    local.get $l3
    i32.add
    local.get $l2
    i32.add
    i32.store offset=20
    local.get $l5
    i32.const 16
    i32.add
    global.set $g0
    local.get $l2
    local.get $l6
    i32.add
    local.get $l3
    i32.add)
