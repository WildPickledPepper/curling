  (func $f71760 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32)
    local.get $p0
    i32.const 284
    i32.add
    local.tee $l5
    i32.load
    if $I0
      loop $L1
        local.get $l4
        i32.const 24
        i32.mul
        local.tee $l6
        local.get $l5
        i32.load offset=8
        i32.add
        local.tee $l2
        local.get $l2
        f32.load
        local.get $p1
        f32.load
        f32.sub
        f32.store
        local.get $l2
        local.get $l2
        f32.load offset=4
        local.get $p1
        f32.load offset=4
        f32.sub
        f32.store offset=4
        local.get $l2
        local.get $l2
        f32.load offset=8
        local.get $p1
        f32.load offset=8
        f32.sub
        f32.store offset=8
        local.get $l5
        i32.load offset=8
        local.get $l6
        i32.add
        local.tee $l2
        local.get $l2
        f32.load offset=12
        local.get $p1
        f32.load
        f32.sub
        f32.store offset=12
        local.get $l2
        i32.const 16
        i32.add
        local.tee $l6
        local.get $l6
        f32.load
        local.get $p1
        f32.load offset=4
        f32.sub
        f32.store
        local.get $l2
        i32.const 20
        i32.add
        local.tee $l2
        local.get $l2
        f32.load
        local.get $p1
        f32.load offset=8
        f32.sub
        f32.store
        local.get $l4
        i32.const 1
        i32.add
        local.tee $l4
        local.get $l5
        i32.load
        i32.lt_u
        br_if $L1
      end
    end
    block $B2
      local.get $p0
      i32.load offset=4
      local.tee $l2
      i32.eqz
      br_if $B2
      local.get $l2
      i32.load offset=40
      local.tee $l6
      i32.eqz
      br_if $B2
      local.get $l2
      i32.load offset=8
      local.set $l4
      loop $L3
        local.get $l4
        local.get $l3
        i32.const 28
        i32.mul
        i32.add
        local.tee $l2
        local.get $l2
        f32.load
        local.get $p1
        f32.load
        f32.sub
        f32.store
        local.get $l2
        local.get $l2
        f32.load offset=4
        local.get $p1
        f32.load offset=4
        f32.sub
        f32.store offset=4
        local.get $l2
        local.get $l2
        f32.load offset=8
        local.get $p1
        f32.load offset=8
        f32.sub
        f32.store offset=8
        local.get $l2
        local.get $l2
        f32.load offset=12
        local.get $p1
        f32.load
        f32.sub
        f32.store offset=12
        local.get $l2
        i32.const 16
        i32.add
        local.tee $l5
        local.get $l5
        f32.load
        local.get $p1
        f32.load offset=4
        f32.sub
        f32.store
        local.get $l2
        i32.const 20
        i32.add
        local.tee $l2
        local.get $l2
        f32.load
        local.get $p1
        f32.load offset=8
        f32.sub
        f32.store
        local.get $l3
        i32.const 1
        i32.add
        local.tee $l3
        local.get $l6
        i32.ne
        br_if $L3
      end
    end
    local.get $p0
    i32.load8_u offset=336
    if $I4
      i32.const 0
      local.set $l2
      local.get $p0
      i32.const 52
      i32.add
      local.tee $l3
      i32.load offset=168
      local.get $p1
      call $f71761
      local.get $l3
      i32.load offset=204
      if $I5
        loop $L6
          local.get $l3
          i32.load offset=200
          local.get $l2
          i32.const 3
          i32.shl
          i32.add
          i32.load
          local.get $p1
          call $f71761
          local.get $l2
          i32.const 1
          i32.add
          local.tee $l2
          local.get $l3
          i32.load offset=204
          i32.lt_u
          br_if $L6
        end
      end
      local.get $l3
      i32.load offset=16
      local.tee $l2
      if $I7
        local.get $l2
        local.get $p1
        call $f71812
      end
      local.get $l3
      i32.const -64
      i32.sub
      i32.load
      local.tee $l2
      if $I8
        local.get $l2
        local.get $p1
        call $f71812
      end
    end
    block $B9
      local.get $p0
      i32.load offset=32
      local.tee $l2
      i32.eqz
      br_if $B9
      local.get $l2
      i32.load offset=40
      local.tee $l6
      i32.eqz
      br_if $B9
      local.get $l2
      i32.load offset=8
      local.set $l4
      i32.const 0
      local.set $l3
      loop $L10
        local.get $l4
        local.get $l3
        i32.const 28
        i32.mul
        i32.add
        local.tee $l2
        local.get $l2
        f32.load
        local.get $p1
        f32.load
        f32.sub
        f32.store
        local.get $l2
        local.get $l2
        f32.load offset=4
        local.get $p1
        f32.load offset=4
        f32.sub
        f32.store offset=4
        local.get $l2
        local.get $l2
        f32.load offset=8
        local.get $p1
        f32.load offset=8
        f32.sub
        f32.store offset=8
        local.get $l2
        local.get $l2
        f32.load offset=12
        local.get $p1
        f32.load
        f32.sub
        f32.store offset=12
        local.get $l2
        i32.const 16
        i32.add
        local.tee $l5
        local.get $l5
        f32.load
        local.get $p1
        f32.load offset=4
        f32.sub
        f32.store
        local.get $l2
        i32.const 20
        i32.add
        local.tee $l2
        local.get $l2
        f32.load
        local.get $p1
        f32.load offset=8
        f32.sub
        f32.store
        local.get $l3
        i32.const 1
        i32.add
        local.tee $l3
        local.get $l6
        i32.ne
        br_if $L10
      end
    end)