  (func $f70485 (type $t2) (param $p0 i32) (param $p1 i32) (param $p2 i32)
    (local $l3 f32) (local $l4 f32) (local $l5 f32) (local $l6 f32) (local $l7 f32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 i32) (local $l28 i32) (local $l29 i32)
    local.get $p0
    i32.const 28
    i32.add
    local.tee $l27
    local.get $p2
    f32.load offset=4
    local.tee $l3
    local.get $l3
    f32.add
    local.tee $l11
    local.get $p2
    f32.load offset=8
    local.tee $l6
    f32.mul
    local.tee $l7
    local.get $p2
    f32.load
    local.tee $l8
    local.get $l8
    f32.add
    local.tee $l5
    local.get $p2
    f32.load offset=12
    local.tee $l12
    f32.mul
    local.tee $l9
    f32.add
    local.tee $l4
    f32.store
    local.get $p0
    local.get $l5
    local.get $l6
    f32.mul
    local.tee $l10
    local.get $l11
    local.get $l12
    f32.mul
    local.tee $l14
    f32.sub
    local.tee $l13
    f32.store offset=24
    local.get $p0
    i32.const 20
    i32.add
    local.tee $p2
    local.get $l7
    local.get $l9
    f32.sub
    local.tee $l7
    f32.store
    local.get $p0
    local.get $l5
    local.get $l3
    f32.mul
    local.tee $l15
    local.get $l12
    local.get $l6
    local.get $l6
    f32.add
    local.tee $l17
    f32.mul
    local.tee $l18
    f32.add
    local.tee $l12
    f32.store offset=12
    local.get $p0
    local.get $l10
    local.get $l14
    f32.add
    local.tee $l9
    f32.store offset=8
    local.get $p0
    local.get $l15
    local.get $l18
    f32.sub
    local.tee $l10
    f32.store offset=4
    f32.const 0x1p+0 (;=1;)
    local.set $l25
    local.get $p0
    i32.const 32
    i32.add
    local.tee $l28
    f32.const 0x1p+0 (;=1;)
    local.get $l8
    local.get $l5
    f32.mul
    f32.sub
    local.tee $l5
    local.get $l3
    local.get $l11
    f32.mul
    local.tee $l11
    f32.sub
    local.tee $l3
    f32.store
    local.get $p0
    i32.const 16
    i32.add
    local.tee $l29
    local.get $l5
    local.get $l6
    local.get $l17
    f32.mul
    local.tee $l8
    f32.sub
    local.tee $l6
    f32.store
    local.get $p0
    f32.const 0x1p+0 (;=1;)
    local.get $l11
    f32.sub
    local.get $l8
    f32.sub
    local.tee $l5
    f32.store
    local.get $l28
    local.get $l3
    local.get $l9
    f32.const 0x0p+0 (;=0;)
    f32.mul
    local.tee $l11
    local.get $l7
    f32.const 0x0p+0 (;=0;)
    f32.mul
    local.tee $l8
    f32.add
    local.get $l3
    local.get $p1
    f32.load offset=8
    local.tee $l14
    f32.mul
    f32.add
    local.tee $l17
    f32.mul
    local.get $l9
    local.get $l3
    f32.const 0x0p+0 (;=0;)
    f32.mul
    local.tee $l19
    local.get $l8
    local.get $l9
    local.get $p1
    f32.load
    local.tee $l15
    f32.mul
    f32.add
    f32.add
    local.tee $l18
    f32.mul
    local.get $l7
    local.get $l19
    local.get $l11
    local.get $l7
    local.get $p1
    f32.load offset=4
    local.tee $l16
    f32.mul
    f32.add
    f32.add
    local.tee $l19
    f32.mul
    f32.add
    f32.add
    local.tee $l11
    f32.store
    local.get $l27
    local.get $l3
    local.get $l10
    f32.const 0x0p+0 (;=0;)
    f32.mul
    local.tee $l8
    local.get $l6
    f32.const 0x0p+0 (;=0;)
    f32.mul
    local.tee $l20
    f32.add
    local.get $l4
    local.get $l14
    f32.mul
    f32.add
    local.tee $l23
    f32.mul
    local.get $l9
    local.get $l4
    f32.const 0x0p+0 (;=0;)
    f32.mul
    local.tee $l21
    local.get $l20
    local.get $l10
    local.get $l15
    f32.mul
    f32.add
    f32.add
    local.tee $l20
    f32.mul
    local.get $l7
    local.get $l21
    local.get $l8
    local.get $l6
    local.get $l16
    f32.mul
    f32.add
    f32.add
    local.tee $l21
    f32.mul
    f32.add
    f32.add
    local.tee $l8
    f32.store
    local.get $p0
    local.get $l3
    local.get $l5
    f32.const 0x0p+0 (;=0;)
    f32.mul
    local.tee $l26
    local.get $l12
    f32.const 0x0p+0 (;=0;)
    f32.mul
    local.tee $l22
    f32.add
    local.get $l13
    local.get $l14
    f32.mul
    f32.add
    local.tee $l24
    f32.mul
    local.get $l9
    local.get $l13
    f32.const 0x0p+0 (;=0;)
    f32.mul
    local.tee $l3
    local.get $l22
    local.get $l5
    local.get $l15
    f32.mul
    f32.add
    f32.add
    local.tee $l22
    f32.mul
    local.get $l7
    local.get $l3
    local.get $l26
    local.get $l12
    local.get $l16
    f32.mul
    f32.add
    f32.add
    local.tee $l16
    f32.mul
    f32.add
    f32.add
    local.tee $l3
    f32.store offset=24
    local.get $p2
    local.get $l4
    local.get $l17
    f32.mul
    local.get $l10
    local.get $l18
    f32.mul
    local.get $l6
    local.get $l19
    f32.mul
    f32.add
    f32.add
    local.tee $l14
    f32.store
    local.get $l29
    local.get $l4
    local.get $l23
    f32.mul
    local.get $l10
    local.get $l20
    f32.mul
    local.get $l6
    local.get $l21
    f32.mul
    f32.add
    f32.add
    local.tee $l15
    f32.store
    local.get $p0
    local.get $l4
    local.get $l24
    f32.mul
    local.get $l10
    local.get $l22
    f32.mul
    local.get $l6
    local.get $l16
    f32.mul
    f32.add
    f32.add
    local.tee $l10
    f32.store offset=12
    local.get $p0
    local.get $l13
    local.get $l17
    f32.mul
    local.get $l5
    local.get $l18
    f32.mul
    local.get $l12
    local.get $l19
    f32.mul
    f32.add
    f32.add
    local.tee $l7
    f32.store offset=8
    local.get $p0
    local.get $l13
    local.get $l23
    f32.mul
    local.get $l5
    local.get $l20
    f32.mul
    local.get $l12
    local.get $l21
    f32.mul
    f32.add
    f32.add
    local.tee $l9
    f32.store offset=4
    local.get $p0
    local.get $l13
    local.get $l24
    f32.mul
    local.get $l5
    local.get $l22
    f32.mul
    local.get $l12
    local.get $l16
    f32.mul
    f32.add
    f32.add
    local.tee $l13
    f32.store
    f32.const 0x0p+0 (;=0;)
    local.set $l12
    f32.const 0x0p+0 (;=0;)
    local.set $l6
    f32.const 0x0p+0 (;=0;)
    local.set $l5
    f32.const 0x1p+0 (;=1;)
    local.set $l17
    f32.const 0x0p+0 (;=0;)
    local.set $l18
    f32.const 0x0p+0 (;=0;)
    local.set $l16
    f32.const 0x0p+0 (;=0;)
    local.set $l19
    f32.const 0x1p+0 (;=1;)
    local.set $l23
    local.get $l7
    local.get $l8
    local.get $l10
    f32.mul
    local.get $l15
    local.get $l3
    f32.mul
    f32.sub
    local.tee $l20
    f32.mul
    local.get $l13
    local.get $l15
    local.get $l11
    f32.mul
    local.get $l14
    local.get $l8
    f32.mul
    f32.sub
    local.tee $l21
    f32.mul
    local.get $l9
    local.get $l14
    local.get $l3
    f32.mul
    local.tee $l24
    local.get $l11
    local.get $l10
    f32.mul
    local.tee $l22
    f32.sub
    f32.mul
    f32.add
    f32.add
    local.tee $l4
    f32.const 0x0p+0 (;=0;)
    f32.ne
    if $I0
      local.get $l15
      local.get $l13
      f32.mul
      local.get $l10
      local.get $l9
      f32.mul
      f32.sub
      f32.const 0x1p+0 (;=1;)
      local.get $l4
      f32.div
      local.tee $l4
      f32.mul
      local.set $l23
      local.get $l11
      local.get $l13
      f32.mul
      local.get $l3
      local.get $l7
      f32.mul
      f32.sub
      local.get $l4
      f32.mul
      local.set $l17
      local.get $l14
      local.get $l9
      f32.mul
      local.get $l15
      local.get $l7
      f32.mul
      f32.sub
      local.get $l4
      f32.mul
      local.set $l6
      local.get $l4
      local.get $l8
      local.get $l13
      f32.mul
      local.get $l3
      local.get $l9
      f32.mul
      f32.sub
      f32.neg
      f32.mul
      local.set $l19
      local.get $l4
      local.get $l14
      local.get $l13
      f32.mul
      local.get $l10
      local.get $l7
      f32.mul
      f32.sub
      f32.neg
      f32.mul
      local.set $l18
      local.get $l4
      local.get $l11
      local.get $l9
      f32.mul
      local.get $l8
      local.get $l7
      f32.mul
      f32.sub
      f32.neg
      f32.mul
      local.set $l12
      local.get $l20
      local.get $l4
      f32.mul
      local.set $l16
      local.get $l21
      local.get $l4
      f32.mul
      local.set $l25
      local.get $l4
      local.get $l22
      local.get $l24
      f32.sub
      f32.neg
      f32.mul
      local.set $l5
    end
    local.get $p0
    local.get $l25
    f32.store offset=36
    local.get $p0
    local.get $l23
    f32.store offset=68
    local.get $p0
    i32.const -64
    i32.sub
    local.get $l19
    f32.store
    local.get $p0
    local.get $l16
    f32.store offset=60
    local.get $p0
    local.get $l18
    f32.store offset=56
    local.get $p0
    local.get $l17
    f32.store offset=52
    local.get $p0
    local.get $l5
    f32.store offset=48
    local.get $p0
    local.get $l6
    f32.store offset=44
    local.get $p0
    local.get $l12
    f32.store offset=40
    local.get $p0
    local.get $p1
    f32.load
    local.get $p1
    f32.load offset=4
    f32.mul
    local.get $p1
    f32.load offset=8
    f32.mul
    f32.const 0x0p+0 (;=0;)
    f32.lt
    i32.store8 offset=72)
