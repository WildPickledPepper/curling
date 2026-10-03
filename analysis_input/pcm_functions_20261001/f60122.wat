  (func $f60122 (type $t0) (param $p0 i32) (param $p1 i32) (result i32)
    (local $l2 f32) (local $l3 f32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32)
    i32.const 4674459
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3752504
      call $f1661
      i32.const 4674459
      i32.const 1
      i32.store8
    end
    local.get $p0
    i32.load offset=328
    i32.const 0
    i32.le_s
    if $I1
      i32.const 6
      return
    end
    i32.const 8
    local.set $l6
    i32.const 0
    local.set $p1
    loop $L2
      local.get $p0
      i32.load offset=124
      i32.load offset=28
      local.get $p1
      local.tee $l4
      i32.const 3
      i32.shl
      i32.add
      f32.load offset=16
      local.set $l2
      i32.const 3752504
      i32.load
      local.tee $p1
      i32.load offset=116
      i32.eqz
      if $I3
        local.get $p1
        call $f65192
      end
      local.get $l4
      i32.const 1
      i32.shl
      local.set $p1
      block $B4
        block $B5
          local.get $l2
          f32.abs
          f32.const 0x1.0c6f7ap-20 (;=1e-06;)
          f32.gt
          if $I6
            local.get $p1
            i32.const 1
            i32.or
            local.set $l7
            br $B5
          end
          local.get $p0
          i32.load offset=124
          i32.load offset=28
          local.get $p1
          i32.const 1
          i32.or
          local.tee $l7
          i32.const 2
          i32.shl
          i32.add
          f32.load offset=16
          local.set $l2
          i32.const 3752504
          i32.load
          local.tee $l5
          i32.load offset=116
          i32.eqz
          if $I7
            local.get $l5
            call $f65192
          end
          local.get $l2
          f32.abs
          f32.const 0x1.0c6f7ap-20 (;=1e-06;)
          f32.gt
          i32.eqz
          br_if $B4
        end
        local.get $p0
        i32.load offset=124
        i32.load offset=28
        i32.const 16
        i32.add
        local.tee $l5
        local.get $l7
        i32.const 2
        i32.shl
        i32.add
        f32.load
        local.set $l2
        local.get $l5
        local.get $p1
        i32.const 2
        i32.shl
        i32.add
        f32.load
        local.set $l3
        i32.const 4671895
        i32.load8_u
        i32.eqz
        if $I8
          i32.const 3752504
          call $f1661
          i32.const 4671895
          i32.const 1
          i32.store8
        end
        i32.const 3752504
        i32.load
        local.tee $p1
        i32.load offset=116
        i32.eqz
        if $I9
          local.get $p1
          call $f65192
        end
        local.get $l3
        local.get $l3
        f32.mul
        local.get $l2
        local.get $l2
        f32.mul
        f32.add
        f32.sqrt
        f32.const 0x1.89ba5ep-1 (;=0.769;)
        f32.le
        i32.eqz
        br_if $B4
        i32.const 10
        local.set $l6
      end
      local.get $l4
      i32.const 2
      i32.add
      local.set $p1
      local.get $l4
      i32.const 14
      i32.lt_u
      br_if $L2
    end
    local.get $l6)
