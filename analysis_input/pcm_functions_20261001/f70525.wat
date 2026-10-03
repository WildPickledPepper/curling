  (func $f70525 (type $t0) (param $p0 i32) (param $p1 i32) (result i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 f32) (local $l6 f32) (local $l7 f32) (local $l8 f32) (local $l9 f32)
    local.get $p0
    i32.load offset=148
    if $I0
      local.get $p0
      local.get $p1
      call $f70527
      return
    end
    local.get $p0
    i32.load8_u offset=156
    local.tee $l4
    i32.const 2
    i32.ge_u
    if $I1
      local.get $p1
      f32.load
      local.tee $l6
      local.get $p0
      i32.load offset=152
      local.tee $l3
      f32.load
      f32.mul
      local.get $p1
      f32.load offset=4
      local.tee $l7
      local.get $l3
      f32.load offset=4
      f32.mul
      f32.add
      local.get $p1
      f32.load offset=8
      local.tee $l8
      local.get $l3
      f32.load offset=8
      f32.mul
      f32.add
      local.set $l5
      i32.const 1
      local.set $p0
      loop $L2
        local.get $l6
        local.get $l3
        local.get $p0
        i32.const 12
        i32.mul
        i32.add
        local.tee $p1
        f32.load
        f32.mul
        local.get $l7
        local.get $p1
        f32.load offset=4
        f32.mul
        f32.add
        local.get $l8
        local.get $p1
        f32.load offset=8
        f32.mul
        f32.add
        local.tee $l9
        local.get $l5
        local.get $l5
        local.get $l9
        f32.lt
        local.tee $p1
        select
        local.set $l5
        local.get $p0
        local.get $l2
        local.get $p1
        select
        local.set $l2
        local.get $p0
        i32.const 1
        i32.add
        local.tee $p0
        local.get $l4
        i32.ne
        br_if $L2
      end
    end
    local.get $l2)