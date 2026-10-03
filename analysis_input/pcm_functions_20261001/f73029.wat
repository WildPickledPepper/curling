  (func $f73029 (type $t4) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32)
    (local $l4 i32) (local $l5 i32) (local $l6 f32) (local $l7 f32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32)
    global.get $g0
    i32.const 48
    i32.sub
    local.tee $l4
    global.set $g0
    i32.const 9
    call $f80140
    call $f73714
    local.get $p0
    i32.load offset=28
    i32.const 4131408
    call $f80185
    local.set $l5
    local.get $l4
    local.get $p0
    f32.load offset=64
    local.tee $l6
    f32.store offset=32
    local.get $l4
    local.get $p0
    f32.load offset=68
    local.tee $l7
    f32.store offset=36
    local.get $l4
    local.get $p0
    f32.load offset=72
    local.tee $l8
    f32.store offset=40
    i32.const 3437616
    f32.load
    local.get $l8
    local.get $l8
    f32.mul
    local.get $l6
    local.get $l6
    f32.mul
    local.get $l7
    local.get $l7
    f32.mul
    f32.add
    f32.add
    f32.gt
    if $I0
      local.get $l4
      i32.const 0
      i32.store offset=40
      local.get $l4
      i64.const 1065353216
      i64.store offset=32
      f32.const 0x0p+0 (;=0;)
      local.set $l7
      f32.const 0x0p+0 (;=0;)
      local.set $l8
      f32.const 0x1p+0 (;=1;)
      local.set $l6
    end
    local.get $l4
    i32.const 16
    i32.add
    local.get $l5
    local.get $p0
    i32.const 40
    i32.add
    call $f78098
    local.get $p1
    local.get $l4
    i32.load offset=24
    i32.store offset=8
    local.get $p1
    local.get $l4
    i64.load offset=16
    i64.store align=4
    local.get $p0
    f32.load offset=48
    local.set $l9
    local.get $l4
    local.get $p0
    f32.load offset=44
    local.tee $l10
    local.get $l6
    f32.mul
    local.get $p0
    f32.load offset=40
    local.tee $l11
    local.get $l7
    f32.mul
    f32.sub
    f32.store offset=24
    local.get $l4
    local.get $l11
    local.get $l8
    f32.mul
    local.get $l9
    local.get $l6
    f32.mul
    f32.sub
    f32.store offset=20
    local.get $l4
    local.get $l9
    local.get $l7
    f32.mul
    local.get $l10
    local.get $l8
    f32.mul
    f32.sub
    f32.store offset=16
    local.get $l4
    i32.const 32
    i32.add
    local.get $l4
    i32.const 16
    i32.add
    call $f78420
    local.get $l4
    local.get $l5
    local.get $l4
    i32.const 32
    i32.add
    call $f78157
    local.get $p2
    local.get $l4
    i32.const 8
    i32.add
    local.tee $p0
    i32.load
    i32.store offset=8
    local.get $p2
    local.get $l4
    i64.load
    i64.store align=4
    local.get $l4
    local.get $l5
    local.get $l4
    i32.const 16
    i32.add
    call $f78157
    local.get $p3
    local.get $p0
    i32.load
    i32.store offset=8
    local.get $p3
    local.get $l4
    i64.load
    i64.store align=4
    local.get $l4
    i32.const 48
    i32.add
    global.set $g0)