  (func $f70519 (type $t15) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 i32)
    (local $l7 f32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32)
    local.get $p5
    i32.const 3
    i32.store
    local.get $p2
    f32.load
    local.tee $l14
    local.get $p1
    f32.load
    local.tee $l7
    f32.sub
    local.tee $l19
    local.get $p3
    f32.load offset=4
    local.tee $l17
    local.get $p1
    f32.load offset=4
    local.tee $l8
    f32.sub
    local.tee $l20
    f32.mul
    local.get $p2
    f32.load offset=4
    local.tee $l13
    local.get $l8
    f32.sub
    local.tee $l21
    local.get $p3
    f32.load
    local.tee $l15
    local.get $l7
    f32.sub
    local.tee $l22
    f32.mul
    f32.sub
    local.tee $l10
    local.get $l10
    f32.mul
    local.get $l21
    local.get $p3
    f32.load offset=8
    local.tee $l18
    local.get $p1
    f32.load offset=8
    local.tee $l9
    f32.sub
    local.tee $l23
    f32.mul
    local.get $p2
    f32.load offset=8
    local.tee $l16
    local.get $l9
    f32.sub
    local.tee $l24
    local.get $l20
    f32.mul
    f32.sub
    local.tee $l11
    local.get $l11
    f32.mul
    local.get $l24
    local.get $l22
    f32.mul
    local.get $l19
    local.get $l23
    f32.mul
    f32.sub
    local.tee $l12
    local.get $l12
    f32.mul
    f32.add
    f32.add
    local.tee $l27
    f32.const 0x0p+0 (;=0;)
    f32.eq
    if $I0
      local.get $p0
      f32.const 0x1.fffffep+127 (;=3.40282e+38;)
      f32.store
      return
    end
    local.get $l13
    local.get $l7
    f32.mul
    local.get $l14
    local.get $l8
    f32.mul
    f32.sub
    local.get $l10
    f32.mul
    local.get $l16
    local.get $l8
    f32.mul
    local.get $l13
    local.get $l9
    f32.mul
    f32.sub
    local.get $l11
    f32.mul
    local.get $l14
    local.get $l9
    f32.mul
    local.get $l16
    local.get $l7
    f32.mul
    f32.sub
    local.get $l12
    f32.mul
    f32.add
    f32.add
    local.set $l25
    local.get $l8
    local.get $l15
    f32.mul
    local.get $l7
    local.get $l17
    f32.mul
    f32.sub
    local.get $l10
    f32.mul
    local.get $l9
    local.get $l17
    f32.mul
    local.get $l8
    local.get $l18
    f32.mul
    f32.sub
    local.get $l11
    f32.mul
    local.get $l7
    local.get $l18
    f32.mul
    local.get $l9
    local.get $l15
    f32.mul
    f32.sub
    local.get $l12
    f32.mul
    f32.add
    f32.add
    local.set $l26
    block $B1
      local.get $l14
      local.get $l17
      f32.mul
      local.get $l13
      local.get $l15
      f32.mul
      f32.sub
      local.get $l10
      f32.mul
      local.get $l13
      local.get $l18
      f32.mul
      local.get $l16
      local.get $l17
      f32.mul
      f32.sub
      local.get $l11
      f32.mul
      local.get $l16
      local.get $l15
      f32.mul
      local.get $l14
      local.get $l18
      f32.mul
      f32.sub
      local.get $l12
      f32.mul
      f32.add
      f32.add
      local.tee $l28
      f32.const 0x0p+0 (;=0;)
      f32.ge
      i32.eqz
      br_if $B1
      local.get $l26
      f32.const 0x0p+0 (;=0;)
      f32.ge
      i32.eqz
      br_if $B1
      local.get $l25
      f32.const 0x0p+0 (;=0;)
      f32.ge
      i32.eqz
      br_if $B1
      local.get $p6
      i32.const 0
      i32.store offset=12
      local.get $p6
      local.get $l10
      local.get $l9
      local.get $l10
      f32.mul
      local.get $l7
      local.get $l11
      f32.mul
      local.get $l8
      local.get $l12
      f32.mul
      f32.add
      f32.add
      local.get $l27
      f32.div
      local.tee $l7
      f32.mul
      local.tee $l9
      f32.store offset=8
      local.get $p6
      local.get $l12
      local.get $l7
      f32.mul
      local.tee $l8
      f32.store offset=4
      local.get $p6
      local.get $l11
      local.get $l7
      f32.mul
      local.tee $l7
      f32.store
      local.get $p0
      local.get $l9
      local.get $l9
      f32.mul
      local.get $l7
      local.get $l7
      f32.mul
      local.get $l8
      local.get $l8
      f32.mul
      f32.add
      f32.add
      f32.store
      return
    end
    local.get $p5
    i32.const 2
    i32.store
    local.get $l21
    local.get $l13
    f32.neg
    local.tee $l12
    f32.mul
    local.get $l14
    local.get $l19
    f32.mul
    f32.sub
    local.get $l16
    local.get $l24
    f32.mul
    f32.sub
    local.set $l10
    block $B2
      local.get $l21
      local.get $l8
      f32.neg
      local.tee $l13
      f32.mul
      local.get $l7
      local.get $l19
      f32.mul
      f32.sub
      local.get $l9
      local.get $l24
      f32.mul
      f32.sub
      local.tee $l8
      f32.const 0x0p+0 (;=0;)
      f32.ge
      i32.eqz
      br_if $B2
      local.get $l10
      f32.const 0x0p+0 (;=0;)
      f32.le
      i32.eqz
      br_if $B2
      local.get $l25
      f32.const 0x0p+0 (;=0;)
      f32.le
      i32.eqz
      br_if $B2
      local.get $p1
      f32.load
      local.set $l11
      local.get $p1
      f32.load offset=4
      local.set $l12
      local.get $p1
      f32.load offset=8
      local.set $l9
      local.get $p6
      i32.const 0
      i32.store offset=12
      local.get $p6
      local.get $l9
      local.get $l24
      local.get $l8
      f32.const 0x1p+0 (;=1;)
      local.get $l8
      local.get $l10
      f32.sub
      local.tee $l7
      f32.div
      f32.const 0x0p+0 (;=0;)
      local.get $l7
      f32.abs
      f32.const 0x1p-23 (;=1.19209e-07;)
      f32.gt
      select
      f32.mul
      local.tee $l7
      f32.mul
      f32.add
      local.tee $l9
      f32.store offset=8
      local.get $p6
      local.get $l12
      local.get $l21
      local.get $l7
      f32.mul
      f32.add
      local.tee $l8
      f32.store offset=4
      local.get $p6
      local.get $l11
      local.get $l19
      local.get $l7
      f32.mul
      f32.add
      local.tee $l7
      f32.store
      local.get $p0
      local.get $l7
      local.get $l7
      f32.mul
      local.get $l8
      local.get $l8
      f32.mul
      f32.add
      local.get $l9
      local.get $l9
      f32.mul
      f32.add
      f32.store
      return
    end
    local.get $l20
    local.get $l17
    f32.neg
    local.tee $l17
    f32.mul
    local.get $l15
    local.get $l22
    f32.mul
    f32.sub
    local.get $l18
    local.get $l23
    f32.mul
    f32.sub
    local.set $l11
    block $B3
      local.get $l20
      local.get $l12
      f32.mul
      local.get $l14
      local.get $l22
      f32.mul
      f32.sub
      local.get $l16
      local.get $l23
      f32.mul
      f32.sub
      local.tee $l12
      local.get $l10
      f32.ge
      i32.eqz
      br_if $B3
      local.get $l21
      local.get $l17
      f32.mul
      local.get $l19
      local.get $l15
      f32.mul
      f32.sub
      local.get $l24
      local.get $l18
      f32.mul
      f32.sub
      local.tee $l14
      local.get $l11
      f32.ge
      i32.eqz
      br_if $B3
      local.get $l28
      f32.const 0x0p+0 (;=0;)
      f32.le
      i32.eqz
      br_if $B3
      local.get $p2
      f32.load
      local.set $l7
      local.get $p3
      f32.load
      local.set $l16
      local.get $p2
      f32.load offset=4
      local.set $l9
      local.get $p3
      f32.load offset=4
      local.set $l13
      local.get $p2
      f32.load offset=8
      local.set $l8
      local.get $p3
      f32.load offset=8
      local.set $l15
      local.get $p4
      local.get $p4
      i64.load offset=4 align=4
      i64.store align=4
      local.get $p6
      i32.const 0
      i32.store offset=12
      local.get $p6
      local.get $l8
      local.get $l12
      local.get $l10
      f32.sub
      local.tee $l10
      f32.const 0x1p+0 (;=1;)
      local.get $l10
      local.get $l14
      local.get $l11
      f32.sub
      f32.add
      local.tee $l10
      f32.div
      f32.const 0x0p+0 (;=0;)
      local.get $l10
      f32.abs
      f32.const 0x1p-23 (;=1.19209e-07;)
      f32.gt
      select
      f32.mul
      local.tee $l10
      local.get $l15
      local.get $l8
      f32.sub
      f32.mul
      f32.add
      local.tee $l8
      f32.store offset=8
      local.get $p6
      local.get $l9
      local.get $l10
      local.get $l13
      local.get $l9
      f32.sub
      f32.mul
      f32.add
      local.tee $l9
      f32.store offset=4
      local.get $p6
      local.get $l7
      local.get $l10
      local.get $l16
      local.get $l7
      f32.sub
      f32.mul
      f32.add
      local.tee $l7
      f32.store
      local.get $p0
      local.get $l7
      local.get $l7
      f32.mul
      local.get $l9
      local.get $l9
      f32.mul
      f32.add
      local.get $l8
      local.get $l8
      f32.mul
      f32.add
      f32.store
      return
    end
    block $B4
      local.get $l20
      local.get $l13
      f32.mul
      local.get $l7
      local.get $l22
      f32.mul
      f32.sub
      local.get $l9
      local.get $l23
      f32.mul
      f32.sub
      local.tee $l7
      f32.const 0x0p+0 (;=0;)
      f32.ge
      i32.eqz
      br_if $B4
      local.get $l11
      f32.const 0x0p+0 (;=0;)
      f32.le
      i32.eqz
      br_if $B4
      local.get $l26
      f32.const 0x0p+0 (;=0;)
      f32.le
      i32.eqz
      br_if $B4
      local.get $p4
      local.get $p4
      i32.load offset=8
      i32.store offset=4
      local.get $p1
      f32.load
      local.set $l10
      local.get $p1
      f32.load offset=4
      local.set $l8
      local.get $p1
      f32.load offset=8
      local.set $l9
      local.get $p6
      i32.const 0
      i32.store offset=12
      local.get $p6
      local.get $l9
      local.get $l23
      local.get $l7
      f32.const 0x1p+0 (;=1;)
      local.get $l7
      local.get $l11
      f32.sub
      local.tee $l11
      f32.div
      f32.const 0x0p+0 (;=0;)
      local.get $l11
      f32.abs
      f32.const 0x1p-23 (;=1.19209e-07;)
      f32.gt
      select
      f32.mul
      local.tee $l7
      f32.mul
      f32.add
      local.tee $l9
      f32.store offset=8
      local.get $p6
      local.get $l8
      local.get $l20
      local.get $l7
      f32.mul
      f32.add
      local.tee $l8
      f32.store offset=4
      local.get $p6
      local.get $l10
      local.get $l22
      local.get $l7
      f32.mul
      f32.add
      local.tee $l7
      f32.store
      local.get $p0
      local.get $l7
      local.get $l7
      f32.mul
      local.get $l8
      local.get $l8
      f32.mul
      f32.add
      local.get $l9
      local.get $l9
      f32.mul
      f32.add
      f32.store
      return
    end
    local.get $p5
    i32.const 1
    i32.store
    block $B5
      local.get $l8
      f32.const 0x0p+0 (;=0;)
      f32.le
      i32.eqz
      br_if $B5
      local.get $l7
      f32.const 0x0p+0 (;=0;)
      f32.le
      i32.eqz
      br_if $B5
      local.get $p6
      local.get $p1
      i64.load
      i64.store
      local.get $p6
      local.get $p1
      i32.const 8
      i32.add
      local.tee $p2
      i64.load
      i64.store offset=8
      local.get $p0
      local.get $p1
      f32.load
      local.tee $l7
      local.get $l7
      f32.mul
      local.get $p1
      f32.load offset=4
      local.tee $l7
      local.get $l7
      f32.mul
      f32.add
      local.get $p2
      f32.load
      local.tee $l7
      local.get $l7
      f32.mul
      f32.add
      f32.store
      return
    end
    block $B6
      local.get $l10
      f32.const 0x0p+0 (;=0;)
      f32.ge
      i32.eqz
      br_if $B6
      local.get $l10
      local.get $l12
      f32.ge
      i32.eqz
      br_if $B6
      local.get $p4
      local.get $p4
      i32.load offset=4
      i32.store
      local.get $p6
      local.get $p2
      i32.const 8
      i32.add
      local.tee $p1
      i64.load
      i64.store offset=8
      local.get $p6
      local.get $p2
      i64.load
      i64.store
      local.get $p0
      local.get $p2
      f32.load
      local.tee $l7
      local.get $l7
      f32.mul
      local.get $p2
      f32.load offset=4
      local.tee $l7
      local.get $l7
      f32.mul
      f32.add
      local.get $p1
      f32.load
      local.tee $l7
      local.get $l7
      f32.mul
      f32.add
      f32.store
      return
    end
    local.get $p4
    local.get $p4
    i32.load offset=8
    i32.store
    local.get $p6
    local.get $p3
    i32.const 8
    i32.add
    local.tee $p1
    i64.load
    i64.store offset=8
    local.get $p6
    local.get $p3
    i64.load
    i64.store
    local.get $p0
    local.get $p3
    f32.load
    local.tee $l7
    local.get $l7
    f32.mul
    local.get $p3
    f32.load offset=4
    local.tee $l7
    local.get $l7
    f32.mul
    f32.add
    local.get $p1
    f32.load
    local.tee $l7
    local.get $l7
    f32.mul
    f32.add
    f32.store)