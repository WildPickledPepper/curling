  (func $f72801 (type $t2) (param $p0 i32) (param $p1 i32) (param $p2 i32)
    (local $l3 f32) (local $l4 f32) (local $l5 f32) (local $l6 f32) (local $l7 f32) (local $l8 f32) (local $l9 f32) (local $l10 i32) (local $l11 i32) (local $l12 i32)
    local.get $p1
    f32.load offset=96
    local.set $l4
    local.get $p1
    f32.load offset=92
    local.set $l6
    i32.const 4748500
    f32.load
    local.set $l3
    local.get $p2
    f32.load
    local.set $l7
    i32.const 4748504
    f32.load
    local.set $l5
    local.get $p2
    f32.load offset=4
    local.set $l9
    local.get $p0
    local.get $p2
    f32.load offset=8
    i32.const 4748508
    f32.load
    f32.mul
    local.get $p1
    f32.load offset=100
    f32.mul
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    local.tee $l8
    f32.store offset=8
    local.get $p0
    local.get $l4
    local.get $l9
    local.get $l5
    f32.mul
    f32.mul
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    local.tee $l5
    f32.store offset=4
    local.get $p0
    local.get $l6
    local.get $l7
    local.get $l3
    f32.mul
    f32.mul
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    local.tee $l4
    f32.store
    local.get $l8
    f32.const 0x0p+0 (;=0;)
    f32.lt
    local.set $p2
    local.get $l8
    f32.neg
    local.set $l3
    local.get $l5
    f32.const 0x0p+0 (;=0;)
    f32.lt
    local.set $l12
    local.get $l5
    f32.neg
    local.set $l9
    local.get $l4
    f32.neg
    local.get $l4
    local.get $l4
    f32.const 0x0p+0 (;=0;)
    f32.lt
    select
    local.set $l6
    local.get $p1
    i32.load offset=104
    local.tee $l10
    if $I0
      local.get $l10
      local.get $p1
      i32.const 108
      i32.add
      local.tee $l11
      i32.load
      i32.store offset=4
      local.get $l11
      i32.load
      local.get $p1
      i32.load offset=104
      i32.store
      local.get $p1
      i64.const 0
      i64.store offset=104 align=4
    end
    local.get $l3
    local.get $l8
    local.get $p2
    select
    local.set $l7
    local.get $l9
    local.get $l5
    local.get $l12
    select
    local.set $l3
    block $B1
      block $B2
        local.get $l4
        local.get $l6
        f32.ne
        br_if $B2
        local.get $l3
        local.get $l5
        f32.ne
        br_if $B2
        local.get $l7
        local.get $l8
        f32.eq
        br_if $B1
      end
      local.get $p1
      i32.const 1
      i32.store8 offset=124
      local.get $p1
      local.get $p1
      i32.store offset=120
      local.get $p1
      i32.const 252014
      i32.store offset=116
      local.get $p1
      i32.const 104
      i32.add
      local.tee $p2
      i32.const 9
      call $f80140
      i32.const 76
      i32.add
      local.tee $l12
      i32.eq
      br_if $B1
      local.get $p2
      i32.load
      local.tee $l10
      if $I3
        local.get $l10
        local.get $p1
        i32.const 108
        i32.add
        local.tee $l11
        i32.load
        i32.store offset=4
        local.get $l11
        i32.load
        local.get $p1
        i32.load offset=104
        i32.store
        local.get $p1
        i64.const 0
        i64.store offset=104 align=4
      end
      local.get $l12
      i32.load
      local.set $l10
      local.get $p1
      i32.const 108
      i32.add
      local.tee $l11
      local.get $l12
      i32.store
      local.get $p1
      local.get $l10
      i32.store offset=104
      local.get $l10
      local.get $p2
      i32.store offset=4
      local.get $l11
      i32.load
      local.get $p2
      i32.store
    end
    local.get $p0
    local.get $l7
    f32.const 0x1p-23 (;=1.19209e-07;)
    local.get $l7
    f32.const 0x1p-23 (;=1.19209e-07;)
    f32.gt
    select
    f32.store offset=8
    local.get $p0
    local.get $l3
    f32.const 0x1p-23 (;=1.19209e-07;)
    local.get $l3
    f32.const 0x1p-23 (;=1.19209e-07;)
    f32.gt
    select
    f32.store offset=4
    local.get $p0
    local.get $l6
    f32.const 0x1p-23 (;=1.19209e-07;)
    local.get $l6
    f32.const 0x1p-23 (;=1.19209e-07;)
    f32.gt
    select
    f32.store)
