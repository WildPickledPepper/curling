  (func $f69904 (type $t6) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32)
    (local $l5 i32) (local $l6 f32) (local $l7 f32)
    global.get $g0
    i32.const -64
    i32.add
    local.tee $l5
    global.set $g0
    local.get $l5
    i32.const 3122820
    i32.load
    i32.store offset=56
    local.get $l5
    i32.const 3122812
    i64.load align=4
    i64.store offset=48
    local.get $p0
    i64.const 0
    i64.store offset=8
    local.get $p0
    i64.const 0
    i64.store
    f32.const 0x1.fffffep+127 (;=3.40282e+38;)
    local.set $l6
    local.get $p2
    i32.load
    i32.const -1
    i32.eq
    if $I0
      local.get $l5
      i32.const 32
      i32.add
      local.get $p1
      local.get $p1
      i32.const 16
      i32.add
      local.get $p1
      i32.const 32
      i32.add
      local.get $p3
      local.get $p4
      local.get $p0
      call $f70519
      local.get $l5
      f32.load offset=32
      local.set $l6
    end
    block $B1
      local.get $p2
      i32.load offset=4
      i32.const -1
      i32.ne
      br_if $B1
      local.get $l5
      i32.const 3
      i32.store offset=56
      local.get $l5
      i64.const 8589934592
      i64.store offset=48
      local.get $l5
      i32.const 3
      i32.store offset=28
      local.get $l5
      local.get $p1
      local.get $p1
      i32.const 32
      i32.add
      local.get $p1
      i32.const 48
      i32.add
      local.get $l5
      i32.const 48
      i32.add
      local.get $l5
      i32.const 28
      i32.add
      local.get $l5
      i32.const 32
      i32.add
      call $f70519
      local.get $l6
      local.get $l5
      f32.load
      local.tee $l7
      f32.gt
      i32.eqz
      br_if $B1
      local.get $p0
      local.get $l5
      i64.load offset=32
      i64.store
      local.get $p0
      local.get $l5
      i64.load offset=40
      i64.store offset=8
      local.get $p3
      local.get $l5
      i32.load offset=48
      i32.store
      local.get $p3
      local.get $l5
      i32.load offset=52
      i32.store offset=4
      local.get $p3
      local.get $l5
      i32.load offset=56
      i32.store offset=8
      local.get $p4
      local.get $l5
      i32.load offset=28
      i32.store
      local.get $l7
      local.set $l6
    end
    block $B2
      local.get $p2
      i32.load offset=8
      i32.const -1
      i32.ne
      br_if $B2
      local.get $l5
      i32.const 1
      i32.store offset=56
      local.get $l5
      i64.const 12884901888
      i64.store offset=48
      local.get $l5
      i32.const 3
      i32.store offset=28
      local.get $l5
      local.get $p1
      local.get $p1
      i32.const 48
      i32.add
      local.get $p1
      i32.const 16
      i32.add
      local.get $l5
      i32.const 48
      i32.add
      local.get $l5
      i32.const 28
      i32.add
      local.get $l5
      i32.const 32
      i32.add
      call $f70519
      local.get $l6
      local.get $l5
      f32.load
      local.tee $l7
      f32.gt
      i32.eqz
      br_if $B2
      local.get $p0
      local.get $l5
      i64.load offset=32
      i64.store
      local.get $p0
      local.get $l5
      i64.load offset=40
      i64.store offset=8
      local.get $p3
      local.get $l5
      i32.load offset=48
      i32.store
      local.get $p3
      local.get $l5
      i32.load offset=52
      i32.store offset=4
      local.get $p3
      local.get $l5
      i32.load offset=56
      i32.store offset=8
      local.get $p4
      local.get $l5
      i32.load offset=28
      i32.store
      local.get $l7
      local.set $l6
    end
    block $B3
      local.get $p2
      i32.load offset=12
      i32.const -1
      i32.ne
      br_if $B3
      local.get $l5
      i32.const 2
      i32.store offset=56
      local.get $l5
      i64.const 12884901889
      i64.store offset=48
      local.get $l5
      i32.const 3
      i32.store offset=28
      local.get $l5
      local.get $p1
      i32.const 16
      i32.add
      local.get $p1
      i32.const 48
      i32.add
      local.get $p1
      i32.const 32
      i32.add
      local.get $l5
      i32.const 48
      i32.add
      local.get $l5
      i32.const 28
      i32.add
      local.get $l5
      i32.const 32
      i32.add
      call $f70519
      local.get $l6
      local.get $l5
      f32.load
      f32.gt
      i32.eqz
      br_if $B3
      local.get $p0
      local.get $l5
      i64.load offset=32
      i64.store
      local.get $p0
      local.get $l5
      i64.load offset=40
      i64.store offset=8
      local.get $p3
      local.get $l5
      i32.load offset=48
      i32.store
      local.get $p3
      local.get $l5
      i32.load offset=52
      i32.store offset=4
      local.get $p3
      local.get $l5
      i32.load offset=56
      i32.store offset=8
      local.get $p4
      local.get $l5
      i32.load offset=28
      i32.store
    end
    local.get $l5
    i32.const -64
    i32.sub
    global.set $g0)