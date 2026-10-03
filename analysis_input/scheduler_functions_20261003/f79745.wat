  (func $f79745 (type $t0) (param $p0 i32) (param $p1 i32) (result i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32)
    local.get $p0
    i32.load offset=4
    local.tee $l2
    local.get $p0
    i32.load offset=16
    local.tee $l4
    local.get $p0
    i32.load offset=20
    i32.add
    local.tee $l6
    i32.const 36
    i32.div_u
    local.tee $l3
    i32.const 2
    i32.shl
    i32.add
    local.set $l5
    local.get $p0
    i32.load offset=8
    local.get $l2
    i32.eq
    local.tee $l7
    if $I0 (result i32)
      i32.const 0
    else
      local.get $l5
      i32.load
      local.get $l6
      local.get $l3
      i32.const 36
      i32.mul
      i32.sub
      i32.const 112
      i32.mul
      i32.add
    end
    local.set $p0
    local.get $l2
    local.get $l4
    i32.const 36
    i32.div_u
    local.tee $l3
    i32.const 2
    i32.shl
    i32.add
    local.set $l6
    local.get $l4
    local.get $l3
    i32.const 36
    i32.mul
    i32.sub
    i32.const 112
    i32.mul
    local.set $l3
    loop $L1
      i32.const 0
      local.set $l4
      i32.const 0
      local.set $l2
      block $B2
        local.get $l7
        if $I3 (result i32)
          local.get $l2
        else
          local.get $l6
          i32.load
          local.get $l3
          i32.add
        end
        local.get $p0
        i32.ne
        if $I4 (result i32)
          block $B5
            local.get $p0
            local.get $l5
            i32.load
            i32.eq
            if $I6
              local.get $l5
              i32.const 4
              i32.sub
              local.tee $l5
              i32.load
              local.tee $l2
              i32.const 4032
              i32.add
              local.set $p0
              local.get $l2
              i32.const 3996
              i32.add
              i32.load
              local.get $p1
              i32.eq
              br_if $B5
              br $B2
            end
            local.get $p0
            i32.const 36
            i32.sub
            i32.load
            local.get $p1
            i32.ne
            br_if $B2
          end
          local.get $p0
          i32.const 112
          i32.sub
        else
          local.get $l4
        end
        return
      end
      local.get $p0
      i32.const 112
      i32.sub
      local.set $p0
      br $L1
    end
    unreachable)
