  (func $f70494 (type $t11) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32)
    (local $l6 f32) (local $l7 f32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32)
    block $B0 (result i32)
      local.get $p5
      if $I1
        local.get $p2
        i64.const 0
        i64.store offset=4 align=4
        local.get $p2
        i32.const 1065353216
        i32.store
        local.get $p2
        i64.const 0
        i64.store offset=12 align=4
        local.get $p2
        i64.const 0
        i64.store offset=24
        local.get $p2
        i32.const 1065353216
        i32.store offset=20
        local.get $p2
        i64.const 0
        i64.store offset=32
        local.get $p2
        i64.const 1065353216
        i64.store offset=40
        local.get $p3
        i64.const 0
        i64.store offset=32
        local.get $p3
        i64.const 0
        i64.store offset=24
        local.get $p3
        i32.const 1065353216
        i32.store offset=20
        local.get $p3
        i64.const 0
        i64.store offset=12 align=4
        local.get $p3
        i64.const 0
        i64.store offset=4 align=4
        local.get $p3
        i32.const 1065353216
        i32.store
        local.get $p3
        i32.const 1065353216
        i32.store offset=40
        local.get $p3
        i32.const 44
        i32.add
        br $B0
      end
      f32.const 0x1p+0 (;=1;)
      local.get $p0
      f32.load offset=8
      local.tee $l7
      f32.div
      local.set $l18
      f32.const 0x1p+0 (;=1;)
      local.get $p0
      f32.load offset=4
      local.tee $l9
      f32.div
      local.set $l22
      f32.const 0x1p+0 (;=1;)
      local.get $p0
      f32.load
      local.tee $l6
      f32.div
      local.set $l23
      block $B2
        block $B3
          local.get $l6
          local.get $l6
          f32.ne
          br_if $B3
          local.get $l6
          local.get $l9
          f32.ne
          br_if $B3
          local.get $l6
          local.get $l7
          f32.ne
          br_if $B3
          local.get $p2
          i32.const 0
          i32.store offset=12
          local.get $p2
          local.get $l6
          f32.store
          local.get $p2
          i32.const 0
          i32.store offset=44
          local.get $p2
          local.get $l7
          f32.store offset=40
          local.get $p2
          local.get $l9
          f32.const 0x0p+0 (;=0;)
          f32.mul
          local.tee $l8
          f32.store offset=36
          local.get $p2
          local.get $l6
          f32.const 0x0p+0 (;=0;)
          f32.mul
          local.tee $l6
          f32.store offset=32
          local.get $p2
          i32.const 0
          i32.store offset=28
          local.get $p2
          local.get $l7
          f32.const 0x0p+0 (;=0;)
          f32.mul
          local.tee $l7
          f32.store offset=24
          local.get $p2
          local.get $l9
          f32.store offset=20
          local.get $p2
          local.get $l6
          f32.store offset=16
          local.get $p2
          local.get $l7
          f32.store offset=8
          local.get $p2
          local.get $l8
          f32.store offset=4
          local.get $p3
          local.get $l18
          f32.store offset=40
          local.get $p3
          local.get $l22
          f32.const 0x0p+0 (;=0;)
          f32.mul
          local.tee $l6
          f32.store offset=36
          local.get $p3
          local.get $l23
          f32.const 0x0p+0 (;=0;)
          f32.mul
          local.tee $l9
          f32.store offset=32
          local.get $p3
          i32.const 0
          i32.store offset=28
          local.get $p3
          local.get $l18
          f32.const 0x0p+0 (;=0;)
          f32.mul
          local.tee $l7
          f32.store offset=24
          local.get $p3
          local.get $l22
          f32.store offset=20
          local.get $p3
          local.get $l9
          f32.store offset=16
          local.get $p3
          i32.const 0
          i32.store offset=12
          local.get $p3
          local.get $l7
          f32.store offset=8
          local.get $p3
          local.get $l6
          f32.store offset=4
          local.get $p3
          local.get $l23
          f32.store
          br $B2
        end
        local.get $p1
        f32.load offset=8
        local.set $l10
        local.get $p1
        f32.load offset=4
        local.set $l12
        local.get $p1
        f32.load offset=12
        local.set $l15
        local.get $p1
        f32.load
        local.set $l8
        local.get $p2
        i32.const 0
        i32.store offset=44
        local.get $p2
        i32.const 0
        i32.store offset=28
        local.get $p2
        i32.const 0
        i32.store offset=12
        local.get $p2
        f32.const 0x1p+0 (;=1;)
        local.get $l8
        local.get $l8
        local.get $l8
        f32.add
        local.tee $l11
        f32.mul
        f32.sub
        local.tee $l21
        local.get $l12
        local.get $l12
        local.get $l12
        f32.add
        local.tee $l13
        f32.mul
        local.tee $l25
        f32.sub
        local.tee $l8
        local.get $l7
        local.get $l8
        f32.mul
        local.tee $l17
        f32.mul
        local.get $l11
        local.get $l10
        f32.mul
        local.tee $l26
        local.get $l13
        local.get $l15
        f32.mul
        local.tee $l27
        f32.add
        local.tee $l14
        local.get $l6
        local.get $l14
        f32.mul
        local.tee $l19
        f32.mul
        local.get $l13
        local.get $l10
        f32.mul
        local.tee $l16
        local.get $l11
        local.get $l15
        f32.mul
        local.tee $l24
        f32.sub
        local.tee $l13
        local.get $l9
        local.get $l13
        f32.mul
        local.tee $l20
        f32.mul
        f32.add
        f32.add
        f32.store offset=40
        local.get $p2
        local.get $l17
        local.get $l16
        local.get $l24
        f32.add
        local.tee $l16
        f32.mul
        local.get $l11
        local.get $l12
        f32.mul
        local.tee $l24
        local.get $l15
        local.get $l10
        local.get $l10
        f32.add
        local.tee $l11
        f32.mul
        local.tee $l28
        f32.sub
        local.tee $l12
        local.get $l19
        f32.mul
        local.get $l21
        local.get $l10
        local.get $l11
        f32.mul
        local.tee $l11
        f32.sub
        local.tee $l10
        local.get $l20
        f32.mul
        f32.add
        f32.add
        f32.store offset=24
        local.get $p2
        local.get $l26
        local.get $l27
        f32.sub
        local.tee $l15
        local.get $l17
        f32.mul
        f32.const 0x1p+0 (;=1;)
        local.get $l25
        f32.sub
        local.get $l11
        f32.sub
        local.tee $l11
        local.get $l19
        f32.mul
        local.get $l24
        local.get $l28
        f32.add
        local.tee $l17
        local.get $l20
        f32.mul
        f32.add
        f32.add
        f32.store offset=8
        local.get $p2
        local.get $l8
        local.get $l7
        local.get $l16
        f32.mul
        local.tee $l19
        f32.mul
        local.get $l14
        local.get $l6
        local.get $l12
        f32.mul
        local.tee $l20
        f32.mul
        local.get $l13
        local.get $l9
        local.get $l10
        f32.mul
        local.tee $l21
        f32.mul
        f32.add
        f32.add
        f32.store offset=36
        local.get $p2
        local.get $l8
        local.get $l7
        local.get $l15
        f32.mul
        local.tee $l7
        f32.mul
        local.get $l14
        local.get $l6
        local.get $l11
        f32.mul
        local.tee $l6
        f32.mul
        local.get $l13
        local.get $l9
        local.get $l17
        f32.mul
        local.tee $l9
        f32.mul
        f32.add
        f32.add
        f32.store offset=32
        local.get $p2
        local.get $l16
        local.get $l19
        f32.mul
        local.get $l12
        local.get $l20
        f32.mul
        local.get $l10
        local.get $l21
        f32.mul
        f32.add
        f32.add
        f32.store offset=20
        local.get $p2
        local.get $l16
        local.get $l7
        f32.mul
        local.get $l12
        local.get $l6
        f32.mul
        local.get $l10
        local.get $l9
        f32.mul
        f32.add
        f32.add
        f32.store offset=16
        local.get $p2
        local.get $l15
        local.get $l19
        f32.mul
        local.get $l11
        local.get $l20
        f32.mul
        local.get $l17
        local.get $l21
        f32.mul
        f32.add
        f32.add
        f32.store offset=4
        local.get $p2
        local.get $l15
        local.get $l7
        f32.mul
        local.get $l11
        local.get $l6
        f32.mul
        local.get $l17
        local.get $l9
        f32.mul
        f32.add
        f32.add
        f32.store
        local.get $p3
        local.get $l8
        local.get $l18
        local.get $l8
        f32.mul
        local.tee $l6
        f32.mul
        local.get $l14
        local.get $l23
        local.get $l14
        f32.mul
        local.tee $l9
        f32.mul
        local.get $l13
        local.get $l22
        local.get $l13
        f32.mul
        local.tee $l7
        f32.mul
        f32.add
        f32.add
        f32.store offset=40
        local.get $p3
        local.get $l8
        local.get $l18
        local.get $l16
        f32.mul
        local.tee $l19
        f32.mul
        local.get $l14
        local.get $l23
        local.get $l12
        f32.mul
        local.tee $l20
        f32.mul
        local.get $l13
        local.get $l22
        local.get $l10
        f32.mul
        local.tee $l21
        f32.mul
        f32.add
        f32.add
        f32.store offset=36
        local.get $p3
        local.get $l8
        local.get $l18
        local.get $l15
        f32.mul
        local.tee $l18
        f32.mul
        local.get $l14
        local.get $l23
        local.get $l11
        f32.mul
        local.tee $l8
        f32.mul
        local.get $l13
        local.get $l22
        local.get $l17
        f32.mul
        local.tee $l14
        f32.mul
        f32.add
        f32.add
        f32.store offset=32
        local.get $p3
        i32.const 0
        i32.store offset=28
        local.get $p3
        local.get $l6
        local.get $l16
        f32.mul
        local.get $l12
        local.get $l9
        f32.mul
        local.get $l10
        local.get $l7
        f32.mul
        f32.add
        f32.add
        f32.store offset=24
        local.get $p3
        local.get $l16
        local.get $l19
        f32.mul
        local.get $l12
        local.get $l20
        f32.mul
        local.get $l10
        local.get $l21
        f32.mul
        f32.add
        f32.add
        f32.store offset=20
        local.get $p3
        local.get $l16
        local.get $l18
        f32.mul
        local.get $l12
        local.get $l8
        f32.mul
        local.get $l10
        local.get $l14
        f32.mul
        f32.add
        f32.add
        f32.store offset=16
        local.get $p3
        i32.const 0
        i32.store offset=12
        local.get $p3
        local.get $l15
        local.get $l6
        f32.mul
        local.get $l11
        local.get $l9
        f32.mul
        local.get $l17
        local.get $l7
        f32.mul
        f32.add
        f32.add
        f32.store offset=8
        local.get $p3
        local.get $l15
        local.get $l19
        f32.mul
        local.get $l11
        local.get $l20
        f32.mul
        local.get $l17
        local.get $l21
        f32.mul
        f32.add
        f32.add
        f32.store offset=4
        local.get $p3
        local.get $l15
        local.get $l18
        f32.mul
        local.get $l11
        local.get $l8
        f32.mul
        local.get $l17
        local.get $l14
        f32.mul
        f32.add
        f32.add
        f32.store
      end
      local.get $p3
      i32.const 0
      i32.store offset=44
      local.get $p2
      f32.load offset=36
      local.set $l8
      local.get $p2
      f32.load offset=20
      local.set $l14
      local.get $p2
      f32.load offset=32
      local.set $l13
      local.get $p2
      f32.load
      local.set $l16
      local.get $p2
      f32.load offset=16
      local.set $l12
      local.get $p2
      f32.load offset=4
      local.set $l10
      local.get $p4
      local.get $p4
      f32.load
      local.tee $l6
      local.get $p2
      f32.load offset=8
      f32.mul
      local.get $p4
      f32.load offset=4
      local.tee $l9
      local.get $p2
      f32.load offset=24
      f32.mul
      f32.add
      local.get $p4
      f32.load offset=8
      local.tee $l7
      local.get $p2
      f32.load offset=40
      f32.mul
      f32.add
      f32.store offset=8
      local.get $p4
      local.get $l6
      local.get $l10
      f32.mul
      local.get $l9
      local.get $l14
      f32.mul
      f32.add
      local.get $l7
      local.get $l8
      f32.mul
      f32.add
      f32.store offset=4
      local.get $p4
      local.get $l6
      local.get $l16
      f32.mul
      local.get $l9
      local.get $l12
      f32.mul
      f32.add
      local.get $l7
      local.get $l13
      f32.mul
      f32.add
      f32.store
      local.get $p4
      i32.const 12
      i32.add
    end
    i32.const 0
    i32.store)