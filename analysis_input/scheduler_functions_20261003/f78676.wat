  (func $f78676 (type $t2) (param $p0 i32) (param $p1 i32) (param $p2 i32)
    (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l4
    global.set $g0
    local.get $p0
    i32.load offset=88
    local.set $p0
    local.get $p2
    i32.load8_u
    local.set $p2
    local.get $l4
    local.get $p1
    i32.load offset=4
    i32.store offset=12
    local.get $l4
    local.get $p0
    local.get $p2
    i32.const 127
    i32.and
    local.tee $l6
    i32.const 124
    i32.mul
    i32.add
    local.tee $p1
    i32.const 8
    i32.add
    local.get $l4
    i32.const 12
    i32.add
    call $f66830
    block $B0
      local.get $l4
      i32.load
      local.tee $p2
      local.get $p1
      i32.load offset=8
      local.get $p1
      i32.load offset=12
      i32.const 3
      i32.mul
      i32.add
      i32.const 12
      i32.add
      i32.eq
      br_if $B0
      local.get $p1
      i32.const 56
      i32.add
      local.set $l7
      local.get $p1
      i32.const 80
      i32.add
      local.tee $l5
      i32.load
      local.set $l3
      block $B1 (result i32)
        block $B2
          local.get $p1
          i32.const 76
          i32.add
          local.tee $l8
          i32.load
          local.tee $l9
          local.get $p2
          i32.load offset=8
          local.tee $p1
          i32.gt_u
          br_if $B2
          local.get $p1
          local.get $l3
          i32.ge_u
          br_if $B2
          local.get $p0
          local.get $l6
          i32.const 124
          i32.mul
          i32.add
          local.tee $l3
          i32.load offset=120
          local.get $p1
          i32.le_u
          br_if $B0
          local.get $l3
          i32.const 60
          i32.add
          local.tee $p0
          i32.load
          local.get $l3
          i32.const 84
          i32.add
          local.tee $l6
          i32.load
          local.get $p1
          i32.and
          i32.const 2
          i32.shl
          i32.add
          i32.const 0
          i32.store
          local.get $l3
          i32.load offset=68
          local.get $l5
          i32.load
          local.tee $p1
          local.get $l8
          i32.load
          i32.sub
          i32.le_u
          if $I3 (result i32)
            local.get $l7
            call $f78675
            local.get $l5
            i32.load
          else
            local.get $p1
          end
          local.get $l6
          i32.load
          i32.and
          br $B1
        end
        local.get $p0
        local.get $l6
        i32.const 124
        i32.mul
        i32.add
        local.tee $p1
        i32.load offset=68
        local.get $l3
        local.get $l9
        i32.sub
        i32.le_u
        if $I4
          local.get $l7
          call $f78675
          local.get $l5
          i32.load
          local.set $l3
        end
        local.get $p1
        i32.const 60
        i32.add
        local.set $p0
        local.get $p1
        i32.load offset=84
        local.get $l3
        i32.and
      end
      local.set $p1
      local.get $p0
      i32.load
      local.get $p1
      i32.const 2
      i32.shl
      i32.add
      local.get $l4
      i32.load offset=12
      i32.store
      local.get $l5
      local.get $l5
      i32.load
      local.tee $p1
      i32.const 1
      i32.add
      i32.store
      local.get $p2
      local.get $p1
      i32.store offset=8
    end
    local.get $l4
    i32.const 16
    i32.add
    global.set $g0)
