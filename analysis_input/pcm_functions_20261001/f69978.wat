  (func $f69978 (type $t4) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32)
    (local $l4 f32) (local $l5 f32) (local $l6 f32) (local $l7 f32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 i32) (local $l17 i32) (local $l18 i32) (local $l19 i32)
    local.get $p3
    f32.load
    local.set $l4
    local.get $p0
    i32.const 0
    i32.store
    block $B0
      local.get $p1
      i32.load offset=384
      local.tee $l17
      i32.eqz
      br_if $B0
      local.get $l4
      local.get $l4
      f32.mul
      local.set $l9
      loop $L1
        local.get $l9
        local.get $p1
        local.get $l17
        i32.const 1
        i32.sub
        local.tee $l17
        i32.const 6
        i32.shl
        i32.add
        local.tee $p3
        i32.const 24
        i32.add
        local.tee $l18
        f32.load
        local.tee $l6
        local.get $p2
        f32.load offset=56
        local.get $p3
        f32.load
        local.tee $l4
        local.get $p2
        f32.load offset=8
        f32.mul
        local.get $p3
        f32.load offset=4
        local.tee $l5
        local.get $p2
        f32.load offset=24
        f32.mul
        f32.add
        local.get $p3
        f32.load offset=8
        local.tee $l7
        local.get $p2
        f32.load offset=40
        f32.mul
        f32.add
        f32.add
        local.tee $l10
        local.get $p3
        i32.const 40
        i32.add
        local.tee $l19
        f32.load
        local.tee $l11
        local.get $p2
        f32.load offset=48
        local.get $l4
        local.get $p2
        f32.load
        f32.mul
        local.get $l5
        local.get $p2
        f32.load offset=16
        f32.mul
        f32.add
        local.get $l7
        local.get $p2
        f32.load offset=32
        f32.mul
        f32.add
        f32.add
        local.tee $l12
        local.get $p3
        f32.load offset=16
        local.tee $l13
        f32.sub
        local.get $p3
        f32.load offset=32
        local.tee $l14
        f32.mul
        local.get $p2
        f32.load offset=52
        local.get $l4
        local.get $p2
        f32.load offset=4
        f32.mul
        local.get $l5
        local.get $p2
        f32.load offset=20
        f32.mul
        f32.add
        local.get $l7
        local.get $p2
        f32.load offset=36
        f32.mul
        f32.add
        f32.add
        local.tee $l5
        local.get $p3
        f32.load offset=20
        local.tee $l7
        f32.sub
        local.get $p3
        f32.load offset=36
        local.tee $l15
        f32.mul
        f32.add
        local.get $l11
        local.get $l10
        local.get $l6
        f32.sub
        f32.mul
        f32.add
        local.tee $l4
        f32.mul
        f32.sub
        f32.sub
        local.tee $l6
        local.get $l6
        f32.mul
        local.get $l13
        local.get $l12
        local.get $l14
        local.get $l4
        f32.mul
        f32.sub
        f32.sub
        local.tee $l6
        local.get $l6
        f32.mul
        local.get $l7
        local.get $l5
        local.get $l15
        local.get $l4
        f32.mul
        f32.sub
        f32.sub
        local.tee $l5
        local.get $l5
        f32.mul
        f32.add
        f32.add
        f32.lt
        if $I2
          local.get $p1
          local.get $p1
          i32.load offset=384
          i32.const 1
          i32.sub
          local.tee $l16
          i32.store offset=384
          local.get $p3
          local.get $p1
          local.get $l16
          i32.const 6
          i32.shl
          i32.add
          local.tee $l16
          i64.load
          i64.store
          local.get $p3
          local.get $l16
          i32.load offset=48
          i32.store offset=48
          local.get $l19
          local.get $l16
          i64.load offset=40
          i64.store
          local.get $p3
          local.get $l16
          i64.load offset=32
          i64.store offset=32
          local.get $l18
          local.get $l16
          i64.load offset=24
          i64.store
          local.get $p3
          local.get $l16
          i64.load offset=16
          i64.store offset=16
          local.get $p3
          local.get $l16
          i64.load offset=8
          i64.store offset=8
          local.get $l17
          br_if $L1
          br $B0
        end
        local.get $p3
        local.get $l4
        f32.store offset=44
        local.get $p0
        local.get $l4
        local.get $l8
        local.get $l4
        local.get $l8
        f32.lt
        select
        local.tee $l8
        f32.store
        local.get $l17
        br_if $L1
      end
    end)
