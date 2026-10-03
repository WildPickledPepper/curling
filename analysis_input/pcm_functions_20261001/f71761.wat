  (func $f71761 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32)
    local.get $p0
    i32.load offset=40
    local.tee $l3
    if $I0
      local.get $p0
      i32.load offset=8
      local.set $l4
      loop $L1
        local.get $l4
        local.get $l2
        i32.const 28
        i32.mul
        i32.add
        local.tee $p0
        local.get $p0
        f32.load
        local.get $p1
        f32.load
        f32.sub
        f32.store
        local.get $p0
        local.get $p0
        f32.load offset=4
        local.get $p1
        f32.load offset=4
        f32.sub
        f32.store offset=4
        local.get $p0
        local.get $p0
        f32.load offset=8
        local.get $p1
        f32.load offset=8
        f32.sub
        f32.store offset=8
        local.get $p0
        local.get $p0
        f32.load offset=12
        local.get $p1
        f32.load
        f32.sub
        f32.store offset=12
        local.get $p0
        i32.const 16
        i32.add
        local.tee $l5
        local.get $l5
        f32.load
        local.get $p1
        f32.load offset=4
        f32.sub
        f32.store
        local.get $p0
        i32.const 20
        i32.add
        local.tee $p0
        local.get $p0
        f32.load
        local.get $p1
        f32.load offset=8
        f32.sub
        f32.store
        local.get $l2
        i32.const 1
        i32.add
        local.tee $l2
        local.get $l3
        i32.ne
        br_if $L1
      end
    end)