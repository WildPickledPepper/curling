  (func $f70518 (type $t15) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 i32)
    (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32)
    global.get $g0
    i32.const 144
    i32.sub
    local.tee $l7
    global.set $g0
    local.get $p6
    i32.const 3
    i32.store
    local.get $l7
    local.get $p1
    i64.load offset=8
    i64.store offset=136
    local.get $l7
    local.get $p1
    i64.load
    i64.store offset=128
    local.get $l7
    local.get $p1
    i32.const 24
    i32.add
    local.tee $l12
    i64.load
    i64.store offset=120
    local.get $l7
    local.get $p1
    i64.load offset=16
    i64.store offset=112
    local.get $l7
    local.get $p1
    i64.load offset=40
    i64.store offset=104
    local.get $l7
    local.get $p1
    i64.load offset=32
    i64.store offset=96
    block $B0
      local.get $l7
      f32.load offset=112
      local.get $l7
      f32.load offset=128
      local.tee $l15
      f32.sub
      local.tee $l20
      local.get $l7
      f32.load offset=100
      local.get $l7
      f32.load offset=132
      local.tee $l16
      f32.sub
      local.tee $l17
      f32.mul
      local.get $l7
      f32.load offset=116
      local.get $l16
      f32.sub
      local.tee $l16
      local.get $l7
      f32.load offset=96
      local.get $l15
      f32.sub
      local.tee $l15
      f32.mul
      f32.sub
      local.tee $l18
      local.get $l18
      f32.mul
      local.get $l16
      local.get $l7
      f32.load offset=104
      local.get $l7
      f32.load offset=136
      local.tee $l18
      f32.sub
      local.tee $l21
      f32.mul
      local.get $l7
      f32.load offset=120
      local.get $l18
      f32.sub
      local.tee $l16
      local.get $l17
      f32.mul
      f32.sub
      local.tee $l17
      local.get $l17
      f32.mul
      local.get $l16
      local.get $l15
      f32.mul
      local.get $l20
      local.get $l21
      f32.mul
      f32.sub
      local.tee $l15
      local.get $l15
      f32.mul
      f32.add
      f32.add
      f32.const 0x1p-23 (;=1.19209e-07;)
      f32.le
      if $I1
        local.get $p6
        i32.const 2
        i32.store
        local.get $p1
        f32.load offset=16
        local.get $p1
        f32.load
        local.tee $l17
        f32.sub
        local.tee $l15
        local.get $l15
        f32.mul
        local.get $p1
        f32.load offset=20
        local.get $p1
        f32.load offset=4
        local.tee $l18
        f32.sub
        local.tee $l20
        local.get $l20
        f32.mul
        f32.add
        local.get $l12
        f32.load
        local.get $p1
        f32.load offset=8
        local.tee $l21
        f32.sub
        local.tee $l16
        local.get $l16
        f32.mul
        f32.add
        local.tee $l19
        f32.const 0x1p-23 (;=1.19209e-07;)
        f32.le
        if $I2
          local.get $p6
          i32.const 1
          i32.store
          local.get $p0
          local.get $p1
          i64.load offset=8
          i64.store offset=8
          local.get $p0
          local.get $p1
          i64.load
          i64.store
          br $B0
        end
        local.get $p0
        i32.const 0
        i32.store offset=12
        local.get $p0
        local.get $l21
        local.get $l16
        local.get $l20
        local.get $l18
        f32.neg
        f32.mul
        local.get $l17
        local.get $l15
        f32.mul
        f32.sub
        local.get $l21
        local.get $l16
        f32.mul
        f32.sub
        local.get $l19
        f32.div
        f32.const 0x1p+0 (;=1;)
        f32.min
        local.tee $l19
        f32.const 0x0p+0 (;=0;)
        local.get $l19
        f32.const 0x0p+0 (;=0;)
        f32.gt
        select
        local.tee $l19
        f32.mul
        f32.add
        f32.store offset=8
        local.get $p0
        local.get $l18
        local.get $l20
        local.get $l19
        f32.mul
        f32.add
        f32.store offset=4
        local.get $p0
        local.get $l17
        local.get $l15
        local.get $l19
        f32.mul
        f32.add
        f32.store
        br $B0
      end
      local.get $l7
      i32.const 3132524
      i32.load
      i32.store offset=88
      local.get $l7
      i32.const 3132516
      i64.load align=4
      i64.store offset=80
      local.get $l7
      i32.const 48
      i32.add
      local.get $l7
      i32.const 128
      i32.add
      local.get $l7
      i32.const 112
      i32.add
      local.get $l7
      i32.const 96
      i32.add
      local.get $l7
      i32.const 80
      i32.add
      local.get $l7
      i32.const 92
      i32.add
      local.get $l7
      i32.const -64
      i32.sub
      call $f70519
      local.get $l7
      i32.load offset=92
      local.tee $l12
      i32.const 3
      i32.ne
      if $I3
        local.get $l7
        i32.load offset=80
        local.set $l8
        local.get $l7
        local.get $p1
        local.get $l7
        i32.load offset=84
        local.tee $l11
        i32.const 4
        i32.shl
        local.tee $l9
        i32.add
        local.tee $l10
        i64.load
        i64.store offset=48
        local.get $l7
        local.get $l10
        i64.load offset=8
        i64.store offset=56
        local.get $l7
        local.get $p2
        local.get $l9
        i32.add
        local.tee $l10
        i64.load offset=8
        i64.store offset=40
        local.get $l7
        local.get $l10
        i64.load
        i64.store offset=32
        local.get $l7
        local.get $p3
        local.get $l8
        i32.const 4
        i32.shl
        local.tee $l10
        i32.add
        local.tee $l13
        i64.load offset=8
        i64.store offset=24
        local.get $l7
        local.get $l13
        i64.load
        i64.store offset=16
        local.get $l7
        local.get $p3
        local.get $l9
        i32.add
        local.tee $l9
        i64.load offset=8
        i64.store offset=8
        local.get $l7
        local.get $l9
        i64.load
        i64.store
        local.get $p5
        local.get $l8
        i32.const 2
        i32.shl
        local.tee $l8
        i32.add
        i32.load
        local.set $l9
        local.get $p5
        local.get $l11
        i32.const 2
        i32.shl
        local.tee $l11
        i32.add
        i32.load
        local.set $l13
        local.get $p4
        local.get $l11
        i32.add
        i32.load
        local.set $l11
        local.get $p4
        local.get $l8
        i32.add
        i32.load
        local.set $l8
        local.get $p1
        local.get $p1
        local.get $l10
        i32.add
        local.tee $l14
        i64.load offset=8
        i64.store offset=8
        local.get $p1
        local.get $l14
        i64.load
        i64.store
        local.get $p1
        i32.const 16
        i32.add
        local.tee $p1
        local.get $l7
        i64.load offset=48
        i64.store
        local.get $p1
        local.get $l7
        i64.load offset=56
        i64.store offset=8
        local.get $p2
        local.get $p2
        local.get $l10
        i32.add
        local.tee $p1
        i64.load
        i64.store
        local.get $p2
        local.get $p1
        i64.load offset=8
        i64.store offset=8
        local.get $p2
        local.get $l7
        i64.load offset=32
        i64.store offset=16
        local.get $p2
        local.get $l7
        i64.load offset=40
        i64.store offset=24
        local.get $p3
        local.get $l7
        i64.load offset=16
        i64.store
        local.get $p3
        local.get $l7
        i64.load offset=24
        i64.store offset=8
        local.get $p3
        local.get $l7
        i64.load offset=8
        i64.store offset=24
        local.get $p3
        local.get $l7
        i64.load
        i64.store offset=16
        local.get $p4
        local.get $l8
        i32.store
        local.get $p4
        local.get $l11
        i32.store offset=4
        local.get $p5
        local.get $l13
        i32.store offset=4
        local.get $p5
        local.get $l9
        i32.store
        local.get $p6
        local.get $l12
        i32.store
      end
      local.get $p0
      local.get $l7
      i64.load offset=64
      i64.store
      local.get $p0
      local.get $l7
      i64.load offset=72
      i64.store offset=8
    end
    local.get $l7
    i32.const 144
    i32.add
    global.set $g0)