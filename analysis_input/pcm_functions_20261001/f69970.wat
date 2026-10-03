  (func $f69970 (type $t6) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32)
    (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 i64)
    block $B0
      local.get $p0
      i32.load8_u offset=64
      local.tee $l8
      i32.eqz
      br_if $B0
      loop $L1
        local.get $p0
        i32.load offset=76
        local.get $l7
        i32.const 48
        i32.mul
        i32.add
        local.tee $l5
        f32.load offset=44
        local.tee $l11
        local.get $p4
        f32.load
        f32.le
        if $I2
          local.get $l5
          f32.load offset=20
          local.set $l12
          local.get $l5
          f32.load offset=16
          local.set $l13
          local.get $l5
          f32.load offset=24
          local.set $l14
          local.get $p3
          f32.load offset=16
          local.set $l19
          local.get $p3
          f32.load offset=20
          local.set $l20
          local.get $p3
          f32.load offset=24
          local.set $l10
          local.get $p3
          f32.load offset=8
          local.set $l15
          local.get $p3
          f32.load
          local.set $l16
          local.get $p3
          f32.load offset=4
          local.set $l17
          local.get $p3
          f32.load offset=12
          local.set $l9
          local.get $p2
          i64.load
          local.set $l21
          local.get $p2
          f32.load offset=8
          local.set $l18
          local.get $p1
          local.get $l6
          i32.const 6
          i32.shl
          i32.add
          local.tee $l5
          i32.const 0
          i32.store offset=28
          local.get $l5
          local.get $l18
          f32.store offset=8
          local.get $l5
          i32.const -1
          i32.store offset=52
          local.get $l5
          local.get $l11
          f32.store offset=12
          local.get $l5
          local.get $l21
          i64.store
          local.get $l5
          local.get $l10
          local.get $l15
          local.get $l16
          local.get $l13
          f32.mul
          local.get $l17
          local.get $l12
          f32.mul
          f32.add
          local.get $l15
          local.get $l14
          f32.mul
          f32.add
          local.tee $l11
          f32.mul
          local.get $l14
          local.get $l9
          local.get $l9
          f32.mul
          f32.const -0x1p-1 (;=-0.5;)
          f32.add
          local.tee $l18
          f32.mul
          local.get $l9
          local.get $l16
          local.get $l12
          f32.mul
          local.get $l17
          local.get $l13
          f32.mul
          f32.sub
          f32.mul
          f32.add
          f32.add
          local.tee $l10
          local.get $l10
          f32.add
          f32.add
          f32.store offset=24
          local.get $l5
          local.get $l20
          local.get $l17
          local.get $l11
          f32.mul
          local.get $l18
          local.get $l12
          f32.mul
          local.get $l9
          local.get $l15
          local.get $l13
          f32.mul
          local.get $l16
          local.get $l14
          f32.mul
          f32.sub
          f32.mul
          f32.add
          f32.add
          local.tee $l10
          local.get $l10
          f32.add
          f32.add
          f32.store offset=20
          local.get $l5
          local.get $l19
          local.get $l16
          local.get $l11
          f32.mul
          local.get $l18
          local.get $l13
          f32.mul
          local.get $l9
          local.get $l17
          local.get $l14
          f32.mul
          local.get $l15
          local.get $l12
          f32.mul
          f32.sub
          f32.mul
          f32.add
          f32.add
          local.tee $l9
          local.get $l9
          f32.add
          f32.add
          f32.store offset=16
          local.get $p0
          i32.load8_u offset=64
          local.set $l8
          local.get $l6
          i32.const 1
          i32.add
          local.set $l6
        end
        local.get $l6
        i32.const 63
        i32.gt_u
        br_if $B0
        local.get $l7
        i32.const 1
        i32.add
        local.tee $l7
        local.get $l8
        i32.lt_u
        br_if $L1
      end
    end
    local.get $p1
    local.get $l6
    i32.store offset=4096)