  (func $f70029 (type $t2) (param $p0 i32) (param $p1 i32) (param $p2 i32)
    (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32)
    local.get $p0
    i32.const -64
    i32.sub
    f32.load
    local.set $l11
    local.get $p0
    f32.load offset=80
    local.set $l12
    local.get $p0
    f32.load offset=52
    local.set $l13
    local.get $p0
    f32.load offset=68
    local.set $l14
    local.get $p0
    f32.load offset=84
    local.set $l15
    local.get $p0
    f32.load offset=48
    local.set $l16
    local.get $p2
    local.get $p0
    i32.load offset=144
    local.tee $l3
    f32.load offset=24
    local.tee $l8
    local.get $p0
    f32.load offset=56
    f32.mul
    local.get $l3
    f32.load offset=28
    local.tee $l9
    local.get $p0
    f32.load offset=72
    f32.mul
    f32.add
    local.get $l3
    f32.load offset=32
    local.tee $l10
    local.get $p0
    f32.load offset=88
    f32.mul
    f32.add
    f32.store offset=8
    local.get $p2
    local.get $l8
    local.get $l13
    f32.mul
    local.get $l9
    local.get $l14
    f32.mul
    f32.add
    local.get $l10
    local.get $l15
    f32.mul
    f32.add
    f32.store offset=4
    local.get $p2
    local.get $l8
    local.get $l16
    f32.mul
    local.get $l9
    local.get $l11
    f32.mul
    f32.add
    local.get $l10
    local.get $l12
    f32.mul
    f32.add
    f32.store
    local.get $p2
    local.get $l3
    i32.load8_u offset=38
    local.tee $p0
    i32.store offset=12
    local.get $p2
    local.get $l3
    i32.load8_u offset=39
    local.tee $l4
    i32.store offset=16
    local.get $p2
    local.get $l3
    i32.load16_s offset=36
    local.tee $l5
    i32.const 32767
    i32.and
    local.tee $l6
    i32.store offset=20
    local.get $p2
    local.get $l3
    i32.load offset=40
    local.tee $l7
    i32.store offset=24
    local.get $p2
    local.get $l7
    local.get $l4
    i32.const 20
    i32.mul
    i32.add
    local.tee $l4
    i32.store offset=28
    local.get $p2
    local.get $l4
    local.get $p0
    i32.const 12
    i32.mul
    i32.add
    local.tee $l4
    i32.store offset=36
    local.get $p2
    i32.const 0
    local.get $p0
    i32.const 3
    i32.mul
    local.tee $p0
    local.get $l4
    local.get $l5
    i32.const 1
    i32.shl
    i32.const 65534
    i32.and
    i32.add
    i32.add
    local.get $l5
    i32.const 0
    i32.ge_s
    local.tee $l5
    select
    i32.store offset=40
    local.get $p2
    local.get $l4
    local.get $l6
    i32.const 1
    i32.shl
    i32.add
    local.get $p0
    i32.add
    local.tee $p0
    local.get $p0
    local.get $l6
    i32.const 2
    i32.shl
    i32.add
    local.get $l5
    select
    i32.store offset=32
    local.get $p2
    local.get $l3
    i32.load offset=44
    i32.store offset=60
    local.get $p2
    local.get $l3
    i64.load offset=48 align=4
    i64.store offset=44 align=4
    local.get $p2
    local.get $l3
    i64.load offset=56 align=4
    i64.store offset=52 align=4
    local.get $p1
    i32.eqz
    if $I0
      local.get $p2
      i32.const 44
      i32.add
      local.tee $p2
      i64.const 0
      i64.store align=4
      local.get $p2
      i64.const 0
      i64.store offset=8 align=4
    end)