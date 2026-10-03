  (func $f78119 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 i64)
    global.get $g0
    i32.const 80
    i32.sub
    local.tee $l2
    global.set $g0
    local.get $p1
    i64.load offset=32 align=4
    local.tee $l18
    i32.wrap_i64
    local.tee $l3
    i64.load
    i64.eqz
    i32.eqz
    if $I0
      local.get $l3
      call $f79912
      local.get $l3
      call $f79911
      local.get $p1
      i64.load offset=32 align=4
      local.tee $l18
      i32.wrap_i64
      local.set $l3
    end
    local.get $l2
    local.get $l18
    i64.store offset=32
    local.get $l2
    local.get $l3
    i32.load offset=24
    local.tee $l7
    local.get $l18
    i64.const 32
    i64.shr_u
    i32.wrap_i64
    local.tee $p1
    i32.const 40
    i32.mul
    i32.add
    local.tee $l4
    i64.load offset=20 align=4
    i64.store offset=24
    local.get $l2
    local.get $l4
    i64.load offset=12 align=4
    i64.store offset=16
    local.get $l3
    i32.load offset=28
    local.tee $l8
    local.get $p1
    i32.const 2
    i32.shl
    i32.add
    i32.load
    local.tee $p1
    i32.const 0
    i32.ge_s
    if $I1
      local.get $l2
      f32.load offset=28
      local.set $l9
      local.get $l2
      i32.load offset=24
      local.set $l4
      local.get $l2
      i32.load offset=20
      local.set $l5
      local.get $l2
      i32.load offset=16
      local.set $l6
      loop $L2
        local.get $l7
        local.get $p1
        i32.const 40
        i32.mul
        i32.add
        local.tee $l3
        f32.load offset=16
        local.tee $l10
        local.get $l3
        i32.load offset=32
        i32.const -2147483648
        i32.and
        i32.const 1065353216
        i32.or
        f32.reinterpret_i32
        local.tee $l11
        local.get $l3
        i32.load offset=36
        i32.const -2147483648
        i32.and
        i32.const 1065353216
        i32.or
        f32.reinterpret_i32
        local.tee $l12
        f32.mul
        i32.reinterpret_f32
        i32.const -2147483648
        i32.and
        local.get $l6
        i32.xor
        f32.reinterpret_i32
        local.tee $l13
        f32.mul
        local.get $l3
        f32.load offset=24
        local.tee $l14
        local.get $l3
        i32.load offset=28
        i32.const -2147483648
        i32.and
        i32.const 1065353216
        i32.or
        f32.reinterpret_i32
        local.tee $l17
        local.get $l11
        f32.mul
        i32.reinterpret_f32
        i32.const -2147483648
        i32.and
        local.get $l4
        i32.xor
        f32.reinterpret_i32
        local.tee $l11
        f32.mul
        f32.sub
        local.get $l9
        local.get $l3
        f32.load offset=20
        local.tee $l15
        f32.mul
        f32.sub
        local.get $l3
        f32.load offset=12
        local.tee $l16
        local.get $l17
        local.get $l12
        f32.mul
        i32.reinterpret_f32
        i32.const -2147483648
        i32.and
        local.get $l5
        i32.xor
        f32.reinterpret_i32
        local.tee $l12
        f32.mul
        f32.sub
        i32.reinterpret_f32
        i32.const -2147483648
        i32.xor
        local.set $l4
        local.get $l16
        local.get $l11
        f32.mul
        local.get $l15
        local.get $l13
        f32.mul
        f32.sub
        local.get $l14
        local.get $l12
        f32.mul
        f32.sub
        local.get $l9
        local.get $l10
        f32.mul
        f32.sub
        i32.reinterpret_f32
        i32.const -2147483648
        i32.xor
        local.set $l5
        local.get $l15
        local.get $l12
        f32.mul
        local.get $l10
        local.get $l11
        f32.mul
        f32.sub
        local.get $l14
        local.get $l13
        f32.mul
        f32.sub
        local.get $l9
        local.get $l16
        f32.mul
        f32.sub
        i32.reinterpret_f32
        i32.const -2147483648
        i32.xor
        local.set $l6
        local.get $l9
        local.get $l14
        f32.mul
        local.get $l16
        local.get $l13
        f32.mul
        f32.sub
        local.get $l15
        local.get $l11
        f32.mul
        f32.sub
        local.get $l10
        local.get $l12
        f32.mul
        f32.sub
        local.tee $l10
        local.set $l9
        local.get $l8
        local.get $p1
        i32.const 2
        i32.shl
        i32.add
        i32.load
        local.tee $p1
        i32.const 0
        i32.ge_s
        br_if $L2
      end
      local.get $l2
      local.get $l10
      f32.store offset=28
      local.get $l2
      local.get $l4
      i32.store offset=24
      local.get $l2
      local.get $l5
      i32.store offset=20
      local.get $l2
      local.get $l6
      i32.store offset=16
    end
    local.get $l2
    local.get $l2
    i64.load offset=32
    i64.store offset=8
    local.get $l2
    i32.const 40
    i32.add
    local.get $l2
    i32.const 8
    i32.add
    local.get $l2
    i32.const 16
    i32.add
    call $f78120
    local.get $p0
    local.get $l2
    f32.load offset=40
    f32.store
    local.get $p0
    local.get $l2
    f32.load offset=44
    f32.store offset=4
    local.get $p0
    local.get $l2
    f32.load offset=48
    f32.store offset=8
    local.get $p0
    local.get $l2
    f32.load offset=52
    f32.store offset=12
    local.get $p0
    local.get $l2
    f32.load offset=56
    f32.store offset=16
    local.get $p0
    local.get $l2
    f32.load offset=60
    f32.store offset=20
    local.get $p0
    local.get $l2
    f32.load offset=64
    f32.store offset=24
    local.get $p0
    local.get $l2
    f32.load offset=68
    f32.store offset=28
    local.get $p0
    local.get $l2
    f32.load offset=72
    f32.store offset=32
    local.get $l2
    i32.const 80
    i32.add
    global.set $g0)
