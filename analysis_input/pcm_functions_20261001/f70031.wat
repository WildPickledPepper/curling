  (func $f70031 (type $t8) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (result i32)
    (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32)
    block $B0 (result i32)
      block $B1
        local.get $p0
        f32.load offset=4
        f32.const 0x1p+0 (;=1;)
        f32.ne
        br_if $B1
        local.get $p0
        f32.load offset=8
        f32.const 0x1p+0 (;=1;)
        f32.ne
        br_if $B1
        i32.const 1
        local.get $p0
        f32.load offset=12
        f32.const 0x1p+0 (;=1;)
        f32.eq
        br_if $B0
        drop
      end
      local.get $p1
      local.get $p0
      i32.const 4
      i32.add
      local.get $p0
      i32.const 16
      i32.add
      call $f70485
      i32.const 0
    end
    local.set $l7
    local.get $p1
    i32.const 16
    i32.add
    local.tee $l5
    f32.load
    local.set $l10
    local.get $p1
    i32.const 28
    i32.add
    local.tee $l4
    f32.load
    local.set $l11
    local.get $p1
    f32.load offset=24
    local.set $l12
    local.get $p1
    f32.load
    local.set $l13
    local.get $p1
    f32.load offset=12
    local.set $l14
    local.get $p1
    f32.load offset=4
    local.set $l15
    local.get $p2
    local.get $p0
    i32.const 40
    i32.add
    local.tee $l6
    i32.load
    local.tee $p0
    f32.load
    local.tee $l16
    local.get $p1
    f32.load offset=8
    local.tee $l17
    f32.mul
    local.get $p0
    f32.load offset=4
    local.tee $l18
    local.get $p1
    i32.const 20
    i32.add
    local.tee $l8
    f32.load
    local.tee $l19
    f32.mul
    f32.add
    local.get $p0
    f32.load offset=8
    local.tee $l20
    local.get $p1
    i32.const 32
    i32.add
    local.tee $l9
    f32.load
    local.tee $l21
    f32.mul
    f32.add
    local.tee $l23
    local.get $l17
    local.get $p0
    f32.load offset=12
    local.tee $l22
    f32.mul
    f32.abs
    local.get $l19
    local.get $p0
    f32.load offset=16
    local.tee $l17
    f32.mul
    f32.abs
    f32.add
    local.get $l21
    local.get $p0
    f32.load offset=20
    local.tee $l19
    f32.mul
    f32.abs
    f32.add
    local.tee $l21
    f32.add
    f32.store offset=20
    local.get $p2
    local.get $l16
    local.get $l15
    f32.mul
    local.get $l18
    local.get $l10
    f32.mul
    f32.add
    local.get $l20
    local.get $l11
    f32.mul
    f32.add
    local.tee $l24
    local.get $l15
    local.get $l22
    f32.mul
    f32.abs
    local.get $l10
    local.get $l17
    f32.mul
    f32.abs
    f32.add
    local.get $l11
    local.get $l19
    f32.mul
    f32.abs
    f32.add
    local.tee $l10
    f32.add
    f32.store offset=16
    local.get $p2
    local.get $l16
    local.get $l13
    f32.mul
    local.get $l18
    local.get $l14
    f32.mul
    f32.add
    local.get $l20
    local.get $l12
    f32.mul
    f32.add
    local.tee $l11
    local.get $l13
    local.get $l22
    f32.mul
    f32.abs
    local.get $l14
    local.get $l17
    f32.mul
    f32.abs
    f32.add
    local.get $l12
    local.get $l19
    f32.mul
    f32.abs
    f32.add
    local.tee $l12
    f32.add
    f32.store offset=12
    local.get $p2
    local.get $l23
    local.get $l21
    f32.sub
    f32.store offset=8
    local.get $p2
    local.get $l24
    local.get $l10
    f32.sub
    f32.store offset=4
    local.get $p2
    local.get $l11
    local.get $l12
    f32.sub
    f32.store
    local.get $l5
    f32.load
    local.set $l13
    local.get $l4
    f32.load
    local.set $l14
    local.get $p1
    f32.load offset=24
    local.set $l15
    local.get $p1
    f32.load offset=12
    local.set $l16
    local.get $p1
    f32.load
    local.set $l18
    local.get $p1
    f32.load offset=4
    local.set $l20
    local.get $p3
    local.get $l6
    i32.load
    local.tee $p2
    f32.load offset=24
    local.tee $l10
    local.get $p1
    f32.load offset=8
    f32.mul
    local.get $p2
    f32.load offset=28
    local.tee $l11
    local.get $l8
    f32.load
    f32.mul
    f32.add
    local.get $p2
    f32.load offset=32
    local.tee $l12
    local.get $l9
    f32.load
    f32.mul
    f32.add
    f32.store offset=8
    local.get $p3
    local.get $l10
    local.get $l20
    f32.mul
    local.get $l11
    local.get $l13
    f32.mul
    f32.add
    local.get $l12
    local.get $l14
    f32.mul
    f32.add
    f32.store offset=4
    local.get $p3
    local.get $l10
    local.get $l18
    f32.mul
    local.get $l11
    local.get $l16
    f32.mul
    f32.add
    local.get $l12
    local.get $l15
    f32.mul
    f32.add
    f32.store
    local.get $p3
    local.get $p2
    i32.load8_u offset=38
    local.tee $p1
    i32.store offset=12
    local.get $p3
    local.get $p2
    i32.load8_u offset=39
    local.tee $l4
    i32.store offset=16
    local.get $p3
    local.get $p2
    i32.load16_s offset=36
    local.tee $p0
    i32.const 32767
    i32.and
    local.tee $l5
    i32.store offset=20
    local.get $p3
    local.get $p2
    i32.load offset=40
    local.tee $l6
    i32.store offset=24
    local.get $p3
    local.get $l6
    local.get $l4
    i32.const 20
    i32.mul
    i32.add
    local.tee $l4
    i32.store offset=28
    local.get $p3
    local.get $l4
    local.get $p1
    i32.const 12
    i32.mul
    i32.add
    local.tee $l4
    i32.store offset=36
    local.get $p3
    i32.const 0
    local.get $p1
    i32.const 3
    i32.mul
    local.tee $p1
    local.get $l4
    local.get $p0
    i32.const 1
    i32.shl
    i32.const 65534
    i32.and
    i32.add
    i32.add
    local.get $p0
    i32.const 0
    i32.ge_s
    local.tee $p0
    select
    i32.store offset=40
    local.get $p3
    local.get $l4
    local.get $l5
    i32.const 1
    i32.shl
    i32.add
    local.get $p1
    i32.add
    local.tee $p1
    local.get $p1
    local.get $l5
    i32.const 2
    i32.shl
    i32.add
    local.get $p0
    select
    i32.store offset=32
    local.get $p3
    local.get $p2
    i32.load offset=44
    i32.store offset=60
    local.get $p3
    local.get $p2
    i64.load offset=48 align=4
    i64.store offset=44 align=4
    local.get $p3
    local.get $p2
    i64.load offset=56 align=4
    i64.store offset=52 align=4
    local.get $l7)
