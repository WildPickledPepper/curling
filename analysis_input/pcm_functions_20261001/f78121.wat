  (func $f78121 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 f32) (local $l3 f32) (local $l4 f32) (local $l5 f32) (local $l6 f32) (local $l7 f32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 i32) (local $l33 i32) (local $l34 i32) (local $l35 i32)
    local.get $p1
    i32.load
    local.tee $l32
    i32.load offset=24
    local.tee $l33
    local.get $p1
    i32.load offset=4
    local.tee $l34
    i32.const 40
    i32.mul
    i32.add
    local.tee $p1
    f32.load offset=28
    local.set $l8
    local.get $p1
    f32.load offset=32
    local.set $l9
    local.get $p1
    f32.load offset=20
    local.set $l2
    local.get $p1
    f32.load offset=24
    local.set $l4
    local.get $p0
    local.get $p1
    f32.load offset=12
    local.tee $l3
    local.get $l3
    f32.const -0x1p+1 (;=-2;)
    f32.mul
    local.tee $l13
    f32.mul
    local.get $p1
    f32.load offset=16
    local.tee $l5
    local.get $l5
    local.get $l5
    f32.add
    local.tee $l10
    f32.mul
    f32.sub
    f32.const 0x1p+0 (;=1;)
    f32.add
    local.get $p1
    f32.load offset=36
    local.tee $l11
    f32.mul
    local.tee $l16
    f32.store offset=32
    local.get $p0
    local.get $l11
    local.get $l4
    local.get $l13
    f32.mul
    local.get $l2
    local.get $l10
    f32.mul
    f32.add
    f32.const 0x0p+0 (;=0;)
    f32.add
    f32.mul
    local.tee $l13
    f32.store offset=28
    local.get $p0
    local.get $l11
    local.get $l2
    local.get $l3
    local.get $l3
    f32.add
    local.tee $l12
    f32.mul
    local.get $l4
    local.get $l10
    f32.mul
    f32.add
    f32.const 0x0p+0 (;=0;)
    f32.add
    f32.mul
    local.tee $l11
    f32.store offset=24
    local.get $p0
    local.get $l9
    local.get $l5
    local.get $l2
    local.get $l2
    f32.add
    local.tee $l7
    f32.mul
    local.get $l4
    local.get $l12
    f32.mul
    f32.add
    f32.const 0x0p+0 (;=0;)
    f32.add
    f32.mul
    local.tee $l17
    f32.store offset=20
    local.get $p0
    local.get $l9
    local.get $l2
    local.get $l2
    f32.const -0x1p+1 (;=-2;)
    f32.mul
    local.tee $l6
    f32.mul
    local.get $l3
    local.get $l12
    f32.mul
    f32.sub
    f32.const 0x1p+0 (;=1;)
    f32.add
    f32.mul
    local.tee $l18
    f32.store offset=16
    local.get $p0
    local.get $l9
    local.get $l4
    local.get $l6
    f32.mul
    local.get $l5
    local.get $l12
    f32.mul
    f32.add
    f32.const 0x0p+0 (;=0;)
    f32.add
    f32.mul
    local.tee $l9
    f32.store offset=12
    local.get $p0
    local.get $l8
    local.get $l4
    local.get $l5
    f32.const -0x1p+1 (;=-2;)
    f32.mul
    local.tee $l6
    f32.mul
    local.get $l3
    local.get $l7
    f32.mul
    f32.add
    f32.const 0x0p+0 (;=0;)
    f32.add
    f32.mul
    local.tee $l12
    f32.store offset=8
    local.get $p0
    local.get $l8
    local.get $l3
    local.get $l10
    f32.mul
    local.get $l4
    local.get $l7
    f32.mul
    f32.add
    f32.const 0x0p+0 (;=0;)
    f32.add
    f32.mul
    local.tee $l10
    f32.store offset=4
    local.get $p0
    local.get $l8
    local.get $l5
    local.get $l6
    f32.mul
    local.get $l2
    local.get $l7
    f32.mul
    f32.sub
    f32.const 0x1p+0 (;=1;)
    f32.add
    f32.mul
    local.tee $l8
    f32.store
    local.get $l32
    i32.load offset=28
    local.tee $l35
    local.get $l34
    i32.const 2
    i32.shl
    i32.add
    i32.load
    local.tee $l32
    i32.const 0
    i32.ge_s
    if $I0
      loop $L1
        local.get $l33
        local.get $l32
        i32.const 40
        i32.mul
        i32.add
        local.tee $p1
        f32.load offset=32
        local.tee $l23
        local.get $p1
        f32.load offset=24
        local.tee $l5
        local.get $p1
        f32.load offset=12
        local.tee $l2
        local.get $l2
        f32.add
        local.tee $l7
        f32.mul
        local.get $p1
        f32.load offset=16
        local.tee $l4
        local.get $p1
        f32.load offset=20
        local.tee $l3
        local.get $l3
        f32.add
        local.tee $l6
        f32.mul
        f32.add
        f32.const 0x0p+0 (;=0;)
        f32.add
        f32.mul
        local.tee $l19
        local.get $l13
        f32.mul
        local.set $l25
        local.get $p1
        f32.load offset=28
        local.tee $l14
        local.get $l4
        f32.const -0x1p+1 (;=-2;)
        f32.mul
        local.tee $l20
        local.get $l5
        f32.mul
        local.get $l2
        local.get $l6
        f32.mul
        f32.add
        f32.const 0x0p+0 (;=0;)
        f32.add
        f32.mul
        local.tee $l21
        local.get $l11
        f32.mul
        local.set $l26
        local.get $l14
        local.get $l2
        local.get $l4
        local.get $l4
        f32.add
        local.tee $l15
        f32.mul
        local.get $l5
        local.get $l6
        f32.mul
        f32.add
        f32.const 0x0p+0 (;=0;)
        f32.add
        f32.mul
        local.tee $l22
        local.get $l11
        f32.mul
        local.set $l27
        local.get $l14
        local.get $l4
        local.get $l20
        f32.mul
        local.get $l3
        local.get $l6
        f32.mul
        f32.sub
        f32.const 0x1p+0 (;=1;)
        f32.add
        f32.mul
        local.tee $l6
        local.get $l11
        f32.mul
        local.get $l23
        local.get $l4
        local.get $l7
        f32.mul
        local.get $l5
        local.get $l3
        f32.const -0x1p+1 (;=-2;)
        f32.mul
        local.tee $l28
        f32.mul
        f32.add
        f32.const 0x0p+0 (;=0;)
        f32.add
        f32.mul
        local.tee $l14
        local.get $l13
        f32.mul
        local.get $p1
        f32.load offset=36
        local.tee $l20
        local.get $l15
        local.get $l5
        f32.mul
        local.get $l7
        local.get $l3
        f32.mul
        f32.add
        f32.const 0x0p+0 (;=0;)
        f32.add
        f32.mul
        local.tee $l24
        local.get $l16
        f32.mul
        f32.add
        f32.add
        local.set $l11
        local.get $l19
        local.get $l18
        f32.mul
        local.set $l29
        local.get $l21
        local.get $l9
        f32.mul
        local.set $l30
        local.get $l22
        local.get $l9
        f32.mul
        local.set $l31
        local.get $l6
        local.get $l9
        f32.mul
        local.get $l14
        local.get $l18
        f32.mul
        local.get $l24
        local.get $l17
        f32.mul
        f32.add
        f32.add
        local.set $l9
        local.get $l10
        local.get $l19
        f32.mul
        local.set $l19
        local.get $l8
        local.get $l21
        f32.mul
        local.set $l21
        local.get $l8
        local.get $l22
        f32.mul
        local.set $l22
        local.get $l8
        local.get $l6
        f32.mul
        local.get $l10
        local.get $l14
        f32.mul
        local.get $l24
        local.get $l12
        f32.mul
        f32.add
        f32.add
        local.set $l8
        local.get $l22
        local.get $l10
        local.get $l23
        local.get $l3
        local.get $l28
        f32.mul
        local.get $l2
        local.get $l7
        f32.mul
        f32.sub
        f32.const 0x1p+0 (;=1;)
        f32.add
        f32.mul
        local.tee $l7
        f32.mul
        local.get $l20
        local.get $l5
        local.get $l2
        f32.const -0x1p+1 (;=-2;)
        f32.mul
        local.tee $l6
        f32.mul
        local.get $l15
        local.get $l3
        f32.mul
        f32.add
        f32.const 0x0p+0 (;=0;)
        f32.add
        f32.mul
        local.tee $l3
        local.get $l12
        f32.mul
        f32.add
        f32.add
        local.tee $l5
        local.set $l10
        local.get $l21
        local.get $l19
        local.get $l2
        local.get $l6
        f32.mul
        local.get $l4
        local.get $l15
        f32.mul
        f32.sub
        f32.const 0x1p+0 (;=1;)
        f32.add
        local.get $l20
        f32.mul
        local.tee $l2
        local.get $l12
        f32.mul
        f32.add
        f32.add
        local.tee $l4
        local.set $l12
        local.get $l31
        local.get $l7
        local.get $l18
        f32.mul
        local.get $l3
        local.get $l17
        f32.mul
        f32.add
        f32.add
        local.tee $l6
        local.set $l18
        local.get $l30
        local.get $l29
        local.get $l2
        local.get $l17
        f32.mul
        f32.add
        f32.add
        local.tee $l15
        local.set $l17
        local.get $l27
        local.get $l7
        local.get $l13
        f32.mul
        local.get $l3
        local.get $l16
        f32.mul
        f32.add
        f32.add
        local.tee $l3
        local.set $l13
        local.get $l26
        local.get $l25
        local.get $l2
        local.get $l16
        f32.mul
        f32.add
        f32.add
        local.tee $l2
        local.set $l16
        local.get $l35
        local.get $l32
        i32.const 2
        i32.shl
        i32.add
        i32.load
        local.tee $l32
        i32.const 0
        i32.ge_s
        br_if $L1
      end
      local.get $p0
      local.get $l2
      f32.store offset=32
      local.get $p0
      local.get $l3
      f32.store offset=28
      local.get $p0
      local.get $l11
      f32.store offset=24
      local.get $p0
      local.get $l15
      f32.store offset=20
      local.get $p0
      local.get $l6
      f32.store offset=16
      local.get $p0
      local.get $l9
      f32.store offset=12
      local.get $p0
      local.get $l4
      f32.store offset=8
      local.get $p0
      local.get $l5
      f32.store offset=4
      local.get $p0
      local.get $l8
      f32.store
    end)