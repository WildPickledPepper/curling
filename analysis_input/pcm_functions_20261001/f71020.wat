  (func $f71020 (type $t7) (param $p0 i32)
    (local $l1 f32) (local $l2 f32) (local $l3 f32) (local $l4 f32) (local $l5 f32) (local $l6 f32) (local $l7 f32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 i32) (local $l17 i32) (local $l18 i32) (local $l19 i32) (local $l20 i32) (local $l21 i32) (local $l22 i32) (local $l23 i32) (local $l24 i32) (local $l25 i32)
    i32.const 1
    local.set $l16
    local.get $p0
    i32.load offset=336
    local.tee $l22
    i32.const 1
    i32.gt_u
    if $I0
      local.get $p0
      i32.load offset=340
      local.set $l23
      local.get $p0
      i32.load offset=332
      local.set $l21
      loop $L1
        local.get $l23
        local.get $l16
        i32.const 160
        i32.mul
        i32.add
        local.tee $l13
        local.get $l21
        local.get $l16
        i32.const 80
        i32.mul
        local.tee $l24
        i32.add
        local.tee $l14
        i32.load offset=64
        local.tee $l15
        i32.const 24
        i32.add
        local.tee $l17
        f32.load
        local.get $l21
        local.get $l14
        i32.load offset=72
        i32.const 80
        i32.mul
        i32.add
        i32.load offset=64
        local.tee $l14
        i32.const 24
        i32.add
        local.tee $l18
        f32.load
        f32.sub
        local.tee $l1
        local.get $l1
        f32.add
        local.tee $l3
        local.get $l15
        f32.load offset=12
        local.tee $l1
        local.get $l1
        f32.mul
        f32.const -0x1p-1 (;=-0.5;)
        f32.add
        local.tee $l7
        f32.mul
        local.get $l1
        local.get $l15
        i32.const 20
        i32.add
        local.tee $l19
        f32.load
        local.get $l14
        i32.const 20
        i32.add
        local.tee $l20
        f32.load
        f32.sub
        local.tee $l2
        local.get $l2
        f32.add
        local.tee $l2
        local.get $l15
        f32.load
        local.tee $l4
        f32.mul
        local.get $l15
        f32.load offset=16
        local.get $l14
        f32.load offset=16
        f32.sub
        local.tee $l8
        local.get $l8
        f32.add
        local.tee $l8
        local.get $l15
        f32.load offset=4
        local.tee $l5
        f32.mul
        f32.sub
        f32.mul
        f32.sub
        local.get $l15
        f32.load offset=8
        local.tee $l6
        local.get $l8
        local.get $l4
        f32.mul
        local.get $l2
        local.get $l5
        f32.mul
        f32.add
        local.get $l3
        local.get $l6
        f32.mul
        f32.add
        local.tee $l9
        f32.mul
        f32.add
        f32.store offset=116
        local.get $l13
        local.get $l5
        local.get $l9
        f32.mul
        local.get $l2
        local.get $l7
        f32.mul
        local.get $l1
        local.get $l8
        local.get $l6
        f32.mul
        local.get $l3
        local.get $l4
        f32.mul
        f32.sub
        f32.mul
        f32.sub
        f32.add
        f32.store offset=112
        local.get $l13
        local.get $l4
        local.get $l9
        f32.mul
        local.get $l8
        local.get $l7
        f32.mul
        local.get $l1
        local.get $l3
        local.get $l5
        f32.mul
        local.get $l2
        local.get $l6
        f32.mul
        f32.sub
        f32.mul
        f32.sub
        f32.add
        f32.store offset=108
        local.get $l14
        f32.load offset=16
        local.set $l1
        local.get $l15
        f32.load offset=16
        local.set $l3
        local.get $l20
        f32.load
        local.set $l2
        local.get $l19
        f32.load
        local.set $l4
        local.get $l13
        local.get $l17
        f32.load
        local.get $l18
        f32.load
        f32.sub
        f32.store offset=128
        local.get $l13
        local.get $l4
        local.get $l2
        f32.sub
        f32.store offset=124
        local.get $l13
        local.get $l3
        local.get $l1
        f32.sub
        f32.store offset=120
        local.get $l16
        i32.const 76
        i32.mul
        local.tee $l13
        local.get $p0
        i32.load offset=272
        i32.add
        local.tee $l20
        local.get $p0
        i32.load offset=260
        local.get $l13
        i32.add
        local.tee $l25
        i32.load offset=72
        local.tee $l19
        i32.store offset=72
        i32.const 0
        local.set $l18
        local.get $l19
        if $I2
          loop $L3
            local.get $l25
            local.get $l18
            i32.const 24
            i32.mul
            local.tee $l17
            i32.add
            local.tee $l13
            f32.load offset=20
            local.set $l9
            local.get $l13
            f32.load offset=16
            local.set $l10
            local.get $l13
            f32.load offset=12
            local.set $l11
            local.get $l17
            local.get $l20
            i32.add
            local.tee $l14
            local.get $l13
            f32.load offset=8
            local.tee $l1
            local.get $l1
            f32.add
            local.tee $l5
            local.get $l15
            f32.load offset=12
            local.tee $l1
            local.get $l1
            f32.mul
            f32.const -0x1p-1 (;=-0.5;)
            f32.add
            local.tee $l8
            f32.mul
            local.get $l1
            local.get $l13
            f32.load offset=4
            local.tee $l3
            local.get $l3
            f32.add
            local.tee $l6
            local.get $l15
            f32.load
            local.tee $l3
            f32.mul
            local.get $l13
            f32.load
            local.tee $l2
            local.get $l2
            f32.add
            local.tee $l7
            local.get $l15
            f32.load offset=4
            local.tee $l2
            f32.mul
            f32.sub
            f32.mul
            f32.add
            local.get $l15
            f32.load offset=8
            local.tee $l4
            local.get $l7
            local.get $l3
            f32.mul
            local.get $l6
            local.get $l2
            f32.mul
            f32.add
            local.get $l5
            local.get $l4
            f32.mul
            f32.add
            local.tee $l12
            f32.mul
            f32.add
            f32.store offset=8
            local.get $l14
            local.get $l2
            local.get $l12
            f32.mul
            local.get $l6
            local.get $l8
            f32.mul
            local.get $l1
            local.get $l7
            local.get $l4
            f32.mul
            local.get $l5
            local.get $l3
            f32.mul
            f32.sub
            f32.mul
            f32.add
            f32.add
            f32.store offset=4
            local.get $l14
            local.get $l3
            local.get $l12
            f32.mul
            local.get $l7
            local.get $l8
            f32.mul
            local.get $l1
            local.get $l5
            local.get $l2
            f32.mul
            local.get $l6
            local.get $l4
            f32.mul
            f32.sub
            f32.mul
            f32.add
            f32.add
            f32.store
            local.get $l14
            local.get $l8
            local.get $l9
            local.get $l9
            f32.add
            local.tee $l5
            f32.mul
            local.get $l1
            local.get $l3
            local.get $l10
            local.get $l10
            f32.add
            local.tee $l6
            f32.mul
            local.get $l2
            local.get $l11
            local.get $l11
            f32.add
            local.tee $l7
            f32.mul
            f32.sub
            f32.mul
            f32.add
            local.get $l4
            local.get $l3
            local.get $l7
            f32.mul
            local.get $l2
            local.get $l6
            f32.mul
            f32.add
            local.get $l4
            local.get $l5
            f32.mul
            f32.add
            local.tee $l9
            f32.mul
            f32.add
            f32.store offset=20
            local.get $l14
            local.get $l2
            local.get $l9
            f32.mul
            local.get $l8
            local.get $l6
            f32.mul
            local.get $l1
            local.get $l4
            local.get $l7
            f32.mul
            local.get $l3
            local.get $l5
            f32.mul
            f32.sub
            f32.mul
            f32.add
            f32.add
            f32.store offset=16
            local.get $l14
            local.get $l3
            local.get $l9
            f32.mul
            local.get $l8
            local.get $l7
            f32.mul
            local.get $l1
            local.get $l2
            local.get $l5
            f32.mul
            local.get $l4
            local.get $l6
            f32.mul
            f32.sub
            f32.mul
            f32.add
            f32.add
            f32.store offset=12
            local.get $p0
            i32.load offset=344
            local.get $l24
            i32.add
            local.get $l17
            i32.add
            local.tee $l13
            f32.load offset=20
            local.set $l9
            local.get $l13
            f32.load offset=16
            local.set $l10
            local.get $l13
            f32.load offset=12
            local.set $l11
            local.get $p0
            i32.load offset=348
            local.get $l16
            i32.const 96
            i32.mul
            i32.add
            local.get $l17
            i32.add
            local.tee $l14
            local.get $l13
            f32.load offset=8
            local.tee $l1
            local.get $l1
            f32.add
            local.tee $l5
            local.get $l15
            f32.load offset=12
            local.tee $l1
            local.get $l1
            f32.mul
            f32.const -0x1p-1 (;=-0.5;)
            f32.add
            local.tee $l8
            f32.mul
            local.get $l1
            local.get $l13
            f32.load offset=4
            local.tee $l3
            local.get $l3
            f32.add
            local.tee $l6
            local.get $l15
            f32.load
            local.tee $l3
            f32.mul
            local.get $l13
            f32.load
            local.tee $l2
            local.get $l2
            f32.add
            local.tee $l7
            local.get $l15
            f32.load offset=4
            local.tee $l2
            f32.mul
            f32.sub
            f32.mul
            f32.add
            local.get $l15
            f32.load offset=8
            local.tee $l4
            local.get $l7
            local.get $l3
            f32.mul
            local.get $l6
            local.get $l2
            f32.mul
            f32.add
            local.get $l5
            local.get $l4
            f32.mul
            f32.add
            local.tee $l12
            f32.mul
            f32.add
            f32.store offset=32
            local.get $l14
            local.get $l2
            local.get $l12
            f32.mul
            local.get $l6
            local.get $l8
            f32.mul
            local.get $l1
            local.get $l7
            local.get $l4
            f32.mul
            local.get $l5
            local.get $l3
            f32.mul
            f32.sub
            f32.mul
            f32.add
            f32.add
            f32.store offset=28
            local.get $l14
            local.get $l3
            local.get $l12
            f32.mul
            local.get $l7
            local.get $l8
            f32.mul
            local.get $l1
            local.get $l5
            local.get $l2
            f32.mul
            local.get $l6
            local.get $l4
            f32.mul
            f32.sub
            f32.mul
            f32.add
            f32.add
            f32.store offset=24
            local.get $l14
            local.get $l8
            local.get $l9
            local.get $l9
            f32.add
            local.tee $l5
            f32.mul
            local.get $l1
            local.get $l3
            local.get $l10
            local.get $l10
            f32.add
            local.tee $l6
            f32.mul
            local.get $l2
            local.get $l11
            local.get $l11
            f32.add
            local.tee $l7
            f32.mul
            f32.sub
            f32.mul
            f32.add
            local.get $l4
            local.get $l3
            local.get $l7
            f32.mul
            local.get $l2
            local.get $l6
            f32.mul
            f32.add
            local.get $l4
            local.get $l5
            f32.mul
            f32.add
            local.tee $l9
            f32.mul
            f32.add
            f32.store offset=44
            local.get $l14
            local.get $l2
            local.get $l9
            f32.mul
            local.get $l8
            local.get $l6
            f32.mul
            local.get $l1
            local.get $l4
            local.get $l7
            f32.mul
            local.get $l3
            local.get $l5
            f32.mul
            f32.sub
            f32.mul
            f32.add
            f32.add
            f32.store offset=40
            local.get $l14
            local.get $l3
            local.get $l9
            f32.mul
            local.get $l8
            local.get $l7
            f32.mul
            local.get $l1
            local.get $l2
            local.get $l5
            f32.mul
            local.get $l4
            local.get $l6
            f32.mul
            f32.sub
            f32.mul
            f32.add
            f32.add
            f32.store offset=36
            local.get $l18
            i32.const 1
            i32.add
            local.tee $l18
            local.get $l19
            i32.ne
            br_if $L3
          end
        end
        local.get $l16
        i32.const 1
        i32.add
        local.tee $l16
        local.get $l22
        i32.ne
        br_if $L1
      end
    end)
