  (func $f70045 (type $t2) (param $p0 i32) (param $p1 i32) (param $p2 i32)
    (local $l3 f32) (local $l4 f32) (local $l5 f32) (local $l6 f32) (local $l7 f32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 i32) (local $l15 i32) (local $l16 i32) (local $l17 i32) (local $l18 i32)
    block $B0
      local.get $p0
      i32.load8_u offset=64
      local.tee $l15
      i32.eqz
      br_if $B0
      local.get $p2
      f32.load
      local.tee $l3
      local.get $l3
      f32.mul
      local.set $l7
      loop $L1
        local.get $l7
        local.get $p0
        i32.load offset=76
        local.tee $l14
        local.get $l15
        i32.const 1
        i32.sub
        local.tee $l15
        i32.const 48
        i32.mul
        i32.add
        local.tee $p2
        i32.const 24
        i32.add
        local.tee $l16
        f32.load
        local.tee $l5
        local.get $p1
        f32.load offset=56
        local.get $p2
        f32.load
        local.tee $l3
        local.get $p1
        f32.load offset=8
        f32.mul
        local.get $p2
        f32.load offset=4
        local.tee $l4
        local.get $p1
        f32.load offset=24
        f32.mul
        f32.add
        local.get $p2
        f32.load offset=8
        local.tee $l6
        local.get $p1
        f32.load offset=40
        f32.mul
        f32.add
        f32.add
        local.tee $l8
        local.get $p2
        i32.const 40
        i32.add
        local.tee $l17
        f32.load
        local.tee $l9
        local.get $p1
        f32.load offset=48
        local.get $l3
        local.get $p1
        f32.load
        f32.mul
        local.get $l4
        local.get $p1
        f32.load offset=16
        f32.mul
        f32.add
        local.get $l6
        local.get $p1
        f32.load offset=32
        f32.mul
        f32.add
        f32.add
        local.tee $l10
        local.get $p2
        f32.load offset=16
        local.tee $l11
        f32.sub
        local.get $p2
        f32.load offset=32
        local.tee $l12
        f32.mul
        local.get $p1
        f32.load offset=52
        local.get $l3
        local.get $p1
        f32.load offset=4
        f32.mul
        local.get $l4
        local.get $p1
        f32.load offset=20
        f32.mul
        f32.add
        local.get $l6
        local.get $p1
        f32.load offset=36
        f32.mul
        f32.add
        f32.add
        local.tee $l4
        local.get $p2
        f32.load offset=20
        local.tee $l6
        f32.sub
        local.get $p2
        f32.load offset=36
        local.tee $l13
        f32.mul
        f32.add
        local.get $l9
        local.get $l8
        local.get $l5
        f32.sub
        f32.mul
        f32.add
        local.tee $l3
        f32.mul
        f32.sub
        f32.sub
        local.tee $l5
        local.get $l5
        f32.mul
        local.get $l11
        local.get $l10
        local.get $l12
        local.get $l3
        f32.mul
        f32.sub
        f32.sub
        local.tee $l5
        local.get $l5
        f32.mul
        local.get $l6
        local.get $l4
        local.get $l13
        local.get $l3
        f32.mul
        f32.sub
        f32.sub
        local.tee $l4
        local.get $l4
        f32.mul
        f32.add
        f32.add
        f32.lt
        if $I2
          local.get $p0
          local.get $p0
          i32.load8_u offset=64
          i32.const 1
          i32.sub
          local.tee $l18
          i32.store8 offset=64
          local.get $p2
          local.get $l14
          local.get $l18
          i32.const 255
          i32.and
          i32.const 48
          i32.mul
          i32.add
          local.tee $l14
          i64.load
          i64.store
          local.get $l17
          local.get $l14
          i64.load offset=40
          i64.store
          local.get $p2
          local.get $l14
          i64.load offset=32
          i64.store offset=32
          local.get $l16
          local.get $l14
          i64.load offset=24
          i64.store
          local.get $p2
          local.get $l14
          i64.load offset=16
          i64.store offset=16
          local.get $p2
          local.get $l14
          i64.load offset=8
          i64.store offset=8
          local.get $l15
          br_if $L1
          br $B0
        end
        local.get $p2
        local.get $l3
        f32.store offset=44
        local.get $l15
        br_if $L1
      end
    end)