  (func $f70177 (type $t14) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 i32) (result i32)
    (local $l7 i32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32)
    global.get $g0
    i32.const 3616
    i32.sub
    local.tee $l7
    global.set $g0
    local.get $l7
    local.get $p2
    f32.load offset=24
    local.get $p3
    f32.load offset=24
    f32.sub
    local.tee $l8
    local.get $l8
    f32.add
    local.tee $l9
    local.get $p3
    f32.load offset=12
    local.tee $l8
    local.get $l8
    f32.mul
    f32.const -0x1p-1 (;=-0.5;)
    f32.add
    local.tee $l15
    f32.mul
    local.get $l8
    local.get $p2
    f32.load offset=20
    local.get $p3
    f32.load offset=20
    f32.sub
    local.tee $l10
    local.get $l10
    f32.add
    local.tee $l10
    local.get $p3
    f32.load
    local.tee $l12
    f32.mul
    local.get $p2
    f32.load offset=16
    local.get $p3
    f32.load offset=16
    f32.sub
    local.tee $l11
    local.get $l11
    f32.add
    local.tee $l11
    local.get $p3
    f32.load offset=4
    local.tee $l13
    f32.mul
    f32.sub
    f32.mul
    f32.sub
    local.get $p3
    f32.load offset=8
    local.tee $l14
    local.get $l11
    local.get $l12
    f32.mul
    local.get $l10
    local.get $l13
    f32.mul
    f32.add
    local.get $l9
    local.get $l14
    f32.mul
    f32.add
    local.tee $l16
    f32.mul
    f32.add
    local.tee $l17
    f32.store offset=3608
    local.get $l7
    local.get $l13
    local.get $l16
    f32.mul
    local.get $l10
    local.get $l15
    f32.mul
    local.get $l8
    local.get $l11
    local.get $l14
    f32.mul
    local.get $l9
    local.get $l12
    f32.mul
    f32.sub
    f32.mul
    f32.sub
    f32.add
    local.tee $l18
    f32.store offset=3604
    local.get $l7
    local.get $l12
    local.get $l16
    f32.mul
    local.get $l11
    local.get $l15
    f32.mul
    local.get $l8
    local.get $l9
    local.get $l13
    f32.mul
    local.get $l10
    local.get $l14
    f32.mul
    f32.sub
    f32.mul
    f32.sub
    f32.add
    local.tee $l9
    f32.store offset=3600
    local.get $p0
    f32.load offset=4
    local.get $p4
    f32.load
    f32.add
    local.set $l8
    local.get $p1
    i32.load offset=40
    local.set $p4
    block $B0
      block $B1
        local.get $p1
        f32.load offset=4
        f32.const 0x1p+0 (;=1;)
        f32.ne
        br_if $B1
        local.get $p1
        f32.load offset=8
        f32.const 0x1p+0 (;=1;)
        f32.ne
        br_if $B1
        local.get $p1
        f32.load offset=12
        f32.const 0x1p+0 (;=1;)
        f32.ne
        br_if $B1
        local.get $l7
        i32.const 3504
        i32.add
        local.get $p6
        i32.store
        local.get $l7
        i32.const 2732
        i32.add
        i32.const 0
        i32.store
        local.get $l7
        i32.const 0
        i32.store offset=168
        local.get $l7
        local.get $l8
        local.get $l8
        f32.mul
        f32.store offset=164
        local.get $l7
        local.get $p5
        i32.store offset=156
        local.get $l7
        local.get $p3
        i32.store offset=152
        local.get $l7
        local.get $p2
        i32.store offset=148
        local.get $l7
        local.get $p4
        i32.store offset=3508
        local.get $l7
        local.get $p0
        i32.store offset=144
        local.get $l7
        i32.const 3125624
        i32.store offset=136
        local.get $l7
        local.get $l7
        i32.const 3600
        i32.add
        i32.store offset=160
        local.get $l7
        i32.const 2
        i32.store offset=140
        local.get $l7
        i32.const 3576
        i32.add
        local.get $l8
        f32.store
        local.get $l7
        i32.const 3572
        i32.add
        local.get $l8
        f32.store
        local.get $l7
        i32.const 3564
        i32.add
        local.get $l17
        f32.store
        local.get $l7
        i32.const 3560
        i32.add
        local.get $l18
        f32.store
        local.get $l7
        i32.const 3552
        i32.add
        i32.const 1065353216
        i32.store
        local.get $l7
        i32.const 3536
        i32.add
        i64.const 1065353216
        i64.store
        local.get $l7
        local.get $l8
        f32.store offset=3568
        local.get $l7
        local.get $l9
        f32.store offset=3556
        local.get $l7
        i64.const 0
        i64.store offset=3544
        local.get $l7
        i64.const 0
        i64.store offset=3528
        local.get $l7
        i64.const 1065353216
        i64.store offset=3520
        local.get $p4
        local.get $l7
        i32.const 3520
        i32.add
        local.get $l7
        i32.const 136
        i32.add
        i32.const 1
        i32.const 1
        local.get $p4
        i32.load16_u offset=4
        i32.const 2
        i32.shl
        i32.const 3125624
        i32.add
        i32.load
        call_indirect $__indirect_function_table (type $t6)
        local.get $l7
        i32.const 3125624
        i32.store offset=136
        local.get $l7
        i32.const 144
        i32.add
        call $f70178
        br $B0
      end
      local.get $l7
      i32.const 3520
      i32.add
      local.get $p1
      i32.const 4
      i32.add
      local.get $p1
      i32.const 16
      i32.add
      call $f70485
      local.get $l7
      i32.const 3504
      i32.add
      local.get $p6
      i32.store
      local.get $l7
      i32.const 2732
      i32.add
      i32.const 0
      i32.store
      local.get $l7
      i32.const 0
      i32.store offset=168
      local.get $l7
      local.get $l8
      local.get $l8
      f32.mul
      f32.store offset=164
      local.get $l7
      local.get $p5
      i32.store offset=156
      local.get $l7
      local.get $p3
      i32.store offset=152
      local.get $l7
      local.get $p2
      i32.store offset=148
      local.get $l7
      local.get $p4
      i32.store offset=3508
      local.get $l7
      local.get $l7
      i32.const 3600
      i32.add
      i32.store offset=160
      local.get $l7
      local.get $p0
      i32.store offset=144
      local.get $l7
      i32.const 3125652
      i32.store offset=136
      local.get $l7
      local.get $l7
      i32.const 3520
      i32.add
      i32.store offset=3512
      local.get $l7
      i32.const 2
      i32.store offset=140
      local.get $l7
      local.get $l7
      i64.load offset=3600
      i64.store offset=120
      local.get $l7
      local.get $l7
      f32.load offset=3608
      f32.store offset=128
      local.get $l7
      local.get $l8
      f32.store offset=112
      local.get $l7
      local.get $l8
      f32.store offset=108
      local.get $l7
      local.get $l8
      f32.store offset=104
      local.get $l7
      i32.const 1065353216
      i32.store offset=96
      local.get $l7
      i64.const 1065353216
      i64.store offset=80
      local.get $l7
      i64.const 0
      i64.store offset=88
      local.get $l7
      i64.const 0
      i64.store offset=72
      local.get $l7
      i64.const 1065353216
      i64.store offset=64
      local.get $l7
      i32.const 3520
      i32.add
      local.get $l7
      i32.const 120
      i32.add
      local.get $l7
      i32.const 104
      i32.add
      local.get $l7
      i32.const -64
      i32.sub
      call $f70179
      local.get $l7
      local.get $l7
      i64.load offset=84 align=4
      i64.store offset=20 align=4
      local.get $l7
      local.get $l7
      i64.load offset=92 align=4
      i64.store offset=28 align=4
      local.get $l7
      local.get $l7
      f32.load offset=128
      f32.store offset=44
      local.get $l7
      local.get $l7
      f32.load offset=112
      f32.store offset=56
      local.get $l7
      local.get $l7
      f32.load offset=64
      f32.store
      local.get $l7
      local.get $l7
      i64.load offset=68 align=4
      i64.store offset=4 align=4
      local.get $l7
      local.get $l7
      i64.load offset=76 align=4
      i64.store offset=12 align=4
      local.get $l7
      local.get $l7
      i64.load offset=120
      i64.store offset=36 align=4
      local.get $l7
      local.get $l7
      i64.load offset=104
      i64.store offset=48
      local.get $p4
      local.get $l7
      local.get $l7
      i32.const 136
      i32.add
      i32.const 1
      i32.const 1
      local.get $p4
      i32.load16_u offset=4
      i32.const 2
      i32.shl
      i32.const 3125624
      i32.add
      i32.load
      call_indirect $__indirect_function_table (type $t6)
      local.get $l7
      i32.const 3125624
      i32.store offset=136
      local.get $l7
      i32.const 144
      i32.add
      call $f70178
    end
    local.get $p5
    i32.load offset=4096
    local.set $p3
    local.get $l7
    i32.const 3616
    i32.add
    global.set $g0
    local.get $p3
    i32.const 0
    i32.ne)
