  (func $f69977 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 i64) (local $l33 i64)
    global.get $g0
    i32.const 256
    i32.sub
    local.tee $l2
    local.set $l3
    local.get $l2
    global.set $g0
    local.get $p0
    f32.load offset=44
    local.set $l16
    local.get $l2
    local.get $p1
    i32.const 15
    i32.add
    i32.const -16
    i32.and
    i32.sub
    local.tee $l7
    i32.const 0
    i32.store8
    i32.const 1
    local.set $l2
    block $B0
      local.get $p1
      i32.const 1
      i32.le_u
      if $I1
        local.get $l7
        local.set $l2
        br $B0
      end
      local.get $p1
      i32.const 1
      i32.sub
      local.tee $l4
      i32.const 1
      i32.and
      local.set $l10
      local.get $p1
      i32.const 2
      i32.ne
      if $I2
        local.get $l4
        i32.const -2
        i32.and
        local.set $l12
        loop $L3
          local.get $l2
          local.get $l7
          i32.add
          local.get $l2
          i32.store8
          local.get $p0
          local.get $l2
          i32.const 6
          i32.shl
          i32.add
          f32.load offset=44
          local.set $l17
          local.get $l7
          local.get $l2
          i32.const 1
          i32.add
          local.tee $l4
          i32.add
          local.get $l4
          i32.store8
          local.get $p0
          local.get $l4
          i32.const 6
          i32.shl
          i32.add
          f32.load offset=44
          local.tee $l18
          local.get $l17
          local.get $l16
          local.get $l16
          local.get $l17
          f32.gt
          local.tee $l5
          select
          local.tee $l16
          local.get $l16
          local.get $l18
          f32.gt
          local.tee $l6
          select
          local.set $l16
          local.get $l4
          local.get $l2
          local.get $l8
          local.get $l5
          select
          local.get $l6
          select
          local.set $l8
          local.get $l4
          local.get $l2
          local.get $l9
          local.get $l5
          select
          local.get $l6
          select
          local.set $l9
          local.get $l2
          i32.const 2
          i32.add
          local.set $l2
          local.get $l12
          i32.const 2
          i32.sub
          local.tee $l12
          br_if $L3
        end
      end
      local.get $l10
      if $I4 (result i32)
        local.get $l2
        local.get $l7
        i32.add
        local.get $l2
        i32.store8
        local.get $l2
        local.get $l9
        local.get $l16
        local.get $p0
        local.get $l2
        i32.const 6
        i32.shl
        i32.add
        f32.load offset=44
        f32.gt
        local.tee $l4
        select
        local.set $l9
        local.get $l2
        local.get $l8
        local.get $l4
        select
      else
        local.get $l8
      end
      local.get $l7
      i32.add
      local.set $l2
      local.get $l9
      i32.const 255
      i32.and
      local.set $l13
    end
    i32.const -1
    local.set $l12
    local.get $l2
    local.get $l7
    local.get $p1
    i32.const 1
    i32.sub
    local.tee $l10
    i32.add
    i32.load8_u
    i32.store8
    local.get $p0
    local.get $l13
    i32.const 6
    i32.shl
    i32.add
    local.tee $l2
    f32.load offset=40
    local.set $l22
    local.get $l2
    f32.load offset=36
    local.set $l23
    local.get $l2
    f32.load offset=32
    local.set $l24
    local.get $l2
    f32.load offset=28
    local.set $l31
    local.get $l2
    f32.load offset=20
    local.set $l19
    local.get $l2
    f32.load offset=24
    local.set $l20
    local.get $l2
    f32.load offset=16
    local.set $l21
    local.get $l3
    local.get $l2
    i64.load offset=44 align=4
    i64.store offset=216
    local.get $l7
    i32.load8_u
    local.set $l8
    i32.const 0
    local.set $l2
    block $B5
      local.get $l10
      i32.const 2
      i32.lt_u
      if $I6
        i32.const 0
        local.set $l4
        br $B5
      end
      local.get $p0
      local.get $l8
      i32.const 6
      i32.shl
      i32.add
      local.tee $l4
      f32.load offset=16
      local.get $l21
      f32.sub
      local.tee $l16
      local.get $l16
      f32.mul
      local.get $l4
      f32.load offset=20
      local.get $l19
      f32.sub
      local.tee $l16
      local.get $l16
      f32.mul
      f32.add
      local.get $l4
      f32.load offset=24
      local.get $l20
      f32.sub
      local.tee $l16
      local.get $l16
      f32.mul
      f32.add
      local.set $l16
      i32.const 0
      local.set $l4
      i32.const 1
      local.set $l5
      loop $L7
        local.get $p0
        local.get $l5
        local.get $l7
        i32.add
        i32.load8_u
        local.tee $l9
        i32.const 6
        i32.shl
        i32.add
        local.tee $l6
        f32.load offset=16
        local.get $l21
        f32.sub
        local.tee $l17
        local.get $l17
        f32.mul
        local.get $l6
        f32.load offset=20
        local.get $l19
        f32.sub
        local.tee $l17
        local.get $l17
        f32.mul
        f32.add
        local.get $l6
        f32.load offset=24
        local.get $l20
        f32.sub
        local.tee $l17
        local.get $l17
        f32.mul
        f32.add
        local.tee $l17
        local.get $l16
        local.get $l16
        local.get $l17
        f32.lt
        local.tee $l6
        select
        local.set $l16
        local.get $l5
        local.get $l4
        local.get $l6
        select
        local.set $l4
        local.get $l9
        local.get $l8
        local.get $l6
        select
        local.set $l8
        local.get $l5
        i32.const 1
        i32.add
        local.tee $l5
        local.get $l10
        i32.ne
        br_if $L7
      end
    end
    local.get $l4
    local.get $l7
    i32.add
    local.get $l7
    local.get $p1
    i32.const 2
    i32.sub
    local.tee $l11
    i32.add
    i32.load8_u
    i32.store8
    local.get $l3
    local.get $p0
    local.get $l8
    i32.const 255
    i32.and
    i32.const 6
    i32.shl
    i32.add
    local.tee $l5
    i64.load offset=8 align=4
    i64.store offset=244 align=4
    local.get $l3
    local.get $l5
    i64.load align=4
    i64.store offset=236 align=4
    local.get $l5
    f32.load offset=20
    local.set $l26
    local.get $l5
    f32.load offset=24
    local.set $l27
    local.get $l5
    f32.load offset=16
    local.set $l28
    local.get $l3
    local.get $l5
    i64.load offset=44 align=4
    i64.store offset=144
    local.get $l3
    local.get $l5
    i64.load offset=36 align=4
    i64.store offset=136
    local.get $l3
    local.get $l5
    i64.load offset=28 align=4
    i64.store offset=128
    local.get $l28
    local.get $l21
    f32.sub
    local.tee $l17
    local.get $l23
    f32.mul
    local.get $l26
    local.get $l19
    f32.sub
    local.tee $l18
    local.get $l24
    f32.mul
    f32.sub
    local.tee $l16
    f32.const 0x1p+0 (;=1;)
    local.get $l16
    local.get $l16
    f32.mul
    local.get $l18
    local.get $l22
    f32.mul
    local.get $l27
    local.get $l20
    f32.sub
    local.tee $l18
    local.get $l23
    f32.mul
    f32.sub
    local.tee $l16
    local.get $l16
    f32.mul
    local.get $l18
    local.get $l24
    f32.mul
    local.get $l17
    local.get $l22
    f32.mul
    f32.sub
    local.tee $l17
    local.get $l17
    f32.mul
    f32.add
    f32.add
    local.tee $l25
    f32.sqrt
    f32.div
    local.tee $l18
    f32.mul
    local.get $l22
    local.get $l25
    f32.const 0x0p+0 (;=0;)
    f32.gt
    local.tee $l5
    select
    local.set $l25
    local.get $l17
    local.get $l18
    f32.mul
    local.get $l23
    local.get $l5
    select
    local.set $l29
    local.get $l16
    local.get $l18
    f32.mul
    local.get $l24
    local.get $l5
    select
    local.set $l30
    block $B8 (result i32)
      local.get $l11
      if $I9
        f32.const 0x1.fffffep+127 (;=3.40282e+38;)
        local.set $l17
        f32.const -0x1.fffffep+127 (;=-3.40282e+38;)
        local.set $l18
        i32.const -1
        local.set $l5
        i32.const -1
        local.set $l10
        loop $L10
          local.get $l30
          local.get $p0
          local.get $l2
          local.get $l7
          i32.add
          i32.load8_u
          local.tee $l6
          i32.const 6
          i32.shl
          i32.add
          local.tee $l8
          f32.load offset=16
          local.get $l21
          f32.sub
          f32.mul
          local.get $l29
          local.get $l8
          f32.load offset=20
          local.get $l19
          f32.sub
          f32.mul
          f32.add
          local.get $l25
          local.get $l8
          f32.load offset=24
          local.get $l20
          f32.sub
          f32.mul
          f32.add
          local.tee $l16
          local.get $l17
          local.get $l16
          local.get $l17
          f32.lt
          local.tee $l8
          select
          local.set $l17
          local.get $l16
          local.get $l18
          local.get $l16
          local.get $l18
          f32.gt
          local.tee $l9
          select
          local.set $l18
          local.get $l2
          local.get $l12
          local.get $l8
          select
          local.set $l12
          local.get $l6
          local.get $l5
          local.get $l8
          select
          local.set $l5
          local.get $l2
          local.get $l4
          local.get $l9
          select
          local.set $l4
          local.get $l6
          local.get $l10
          local.get $l9
          select
          local.set $l10
          local.get $l2
          i32.const 1
          i32.add
          local.tee $l2
          local.get $l11
          i32.ne
          br_if $L10
        end
        local.get $p0
        local.get $l10
        i32.const 255
        i32.and
        i32.const 6
        i32.shl
        i32.add
        br $B8
      end
      i32.const -1
      local.set $l5
      f32.const -0x1.fffffep+127 (;=-3.40282e+38;)
      local.set $l18
      f32.const 0x1.fffffep+127 (;=3.40282e+38;)
      local.set $l17
      local.get $p0
      i32.const 16320
      i32.add
    end
    local.set $l2
    local.get $l4
    local.get $l7
    i32.add
    local.get $l7
    local.get $p1
    i32.const 3
    i32.sub
    local.tee $l9
    i32.add
    i32.load8_u
    i32.store8
    local.get $l3
    local.get $l2
    i32.load offset=48
    i32.store offset=212
    local.get $l3
    local.get $l2
    i64.load offset=40 align=4
    i64.store offset=204 align=4
    local.get $l3
    local.get $l2
    i64.load offset=32 align=4
    i64.store offset=196 align=4
    local.get $l3
    local.get $l2
    i64.load offset=24 align=4
    i64.store offset=188 align=4
    local.get $l3
    local.get $l2
    i64.load offset=16 align=4
    i64.store offset=180 align=4
    local.get $l3
    local.get $l2
    i64.load offset=8 align=4
    i64.store offset=172 align=4
    local.get $l3
    local.get $l2
    i64.load align=4
    i64.store offset=164 align=4
    local.get $l4
    local.get $l12
    local.get $l9
    local.get $l12
    i32.eq
    select
    local.set $l6
    block $B11
      local.get $l17
      local.get $l18
      f32.mul
      f32.const 0x0p+0 (;=0;)
      f32.gt
      i32.eqz
      br_if $B11
      local.get $l9
      i32.eqz
      br_if $B11
      f32.const -0x1.fffffep+127 (;=-3.40282e+38;)
      local.set $l16
      i32.const 0
      local.set $l2
      loop $L12
        local.get $l30
        local.get $p0
        local.get $l2
        local.get $l7
        i32.add
        i32.load8_u
        local.tee $l8
        i32.const 6
        i32.shl
        i32.add
        local.tee $l4
        f32.load offset=16
        local.get $l21
        f32.sub
        f32.mul
        local.get $l29
        local.get $l4
        f32.load offset=20
        local.get $l19
        f32.sub
        f32.mul
        f32.add
        local.get $l25
        local.get $l4
        f32.load offset=24
        local.get $l20
        f32.sub
        f32.mul
        f32.add
        local.tee $l17
        local.get $l16
        local.get $l16
        local.get $l17
        f32.lt
        local.tee $l4
        select
        local.set $l16
        local.get $l2
        local.get $l6
        local.get $l4
        select
        local.set $l6
        local.get $l8
        local.get $l5
        local.get $l4
        select
        local.set $l5
        local.get $l2
        i32.const 1
        i32.add
        local.tee $l2
        local.get $l9
        i32.ne
        br_if $L12
      end
    end
    local.get $l3
    i32.const 236
    i32.add
    local.set $l14
    local.get $l3
    i32.const 164
    i32.add
    local.set $l10
    local.get $l6
    local.get $l7
    i32.add
    local.get $l7
    local.get $p1
    i32.const 4
    i32.sub
    local.tee $l4
    i32.add
    i32.load8_u
    i32.store8
    local.get $l3
    local.get $p0
    local.get $l5
    i32.const 255
    i32.and
    i32.const 6
    i32.shl
    i32.add
    local.tee $l2
    i32.load offset=48
    i32.store offset=124
    local.get $l3
    local.get $l2
    i64.load offset=40 align=4
    i64.store offset=116 align=4
    local.get $l3
    local.get $l2
    i64.load offset=32 align=4
    i64.store offset=108 align=4
    local.get $l3
    local.get $l2
    i64.load offset=24 align=4
    i64.store offset=100 align=4
    local.get $l3
    local.get $l2
    i64.load offset=16 align=4
    i64.store offset=92 align=4
    local.get $l3
    local.get $l2
    i64.load offset=8 align=4
    i64.store offset=84 align=4
    local.get $l3
    local.get $l2
    i64.load align=4
    i64.store offset=76 align=4
    local.get $l3
    i32.const 76
    i32.add
    local.set $l11
    local.get $l4
    if $I13 (result i32)
      local.get $p1
      i32.const 1
      i32.and
      local.set $l15
      block $B14
        local.get $p1
        i32.const 5
        i32.eq
        if $I15
          f32.const 0x1.fffffep+127 (;=3.40282e+38;)
          local.set $l16
          i32.const -1
          local.set $l6
          i32.const 0
          local.set $l2
          br $B14
        end
        local.get $l4
        i32.const -2
        i32.and
        local.set $l8
        f32.const 0x1.fffffep+127 (;=3.40282e+38;)
        local.set $l16
        i32.const -1
        local.set $l9
        i32.const 0
        local.set $l2
        i32.const -1
        local.set $l6
        loop $L16
          local.get $l7
          local.get $l2
          i32.const 1
          i32.or
          local.tee $l12
          i32.add
          i32.load8_u
          local.tee $l5
          local.get $l2
          local.get $l7
          i32.add
          i32.load8_u
          local.tee $l4
          local.get $l6
          local.get $l16
          local.get $p0
          local.get $l4
          i32.const 6
          i32.shl
          i32.add
          f32.load offset=44
          local.tee $l17
          f32.gt
          local.tee $l4
          select
          local.get $l17
          local.get $l16
          local.get $l4
          select
          local.tee $l16
          local.get $p0
          local.get $l5
          i32.const 6
          i32.shl
          i32.add
          f32.load offset=44
          local.tee $l17
          f32.gt
          local.tee $l5
          select
          local.set $l6
          local.get $l17
          local.get $l16
          local.get $l5
          select
          local.set $l16
          local.get $l12
          local.get $l2
          local.get $l9
          local.get $l4
          select
          local.get $l5
          select
          local.set $l9
          local.get $l2
          i32.const 2
          i32.add
          local.set $l2
          local.get $l8
          i32.const 2
          i32.sub
          local.tee $l8
          br_if $L16
        end
      end
      local.get $p0
      local.get $l15
      if $I17 (result i32)
        local.get $l2
        local.get $l7
        i32.add
        i32.load8_u
        local.tee $l2
        local.get $l6
        local.get $l16
        local.get $p0
        local.get $l2
        i32.const 6
        i32.shl
        i32.add
        f32.load offset=44
        f32.gt
        select
      else
        local.get $l6
      end
      i32.const 255
      i32.and
      i32.const 6
      i32.shl
      i32.add
    else
      local.get $p0
      i32.const 16320
      i32.add
    end
    local.set $l2
    local.get $l3
    i32.const 60
    i32.add
    local.tee $l7
    local.get $l2
    i32.load offset=48
    i32.store
    local.get $l3
    i32.const 52
    i32.add
    local.tee $l4
    local.get $l2
    i64.load offset=40 align=4
    i64.store align=4
    local.get $l3
    i32.const 44
    i32.add
    local.tee $l5
    local.get $l2
    i64.load offset=32 align=4
    i64.store align=4
    local.get $l3
    i32.const 36
    i32.add
    local.tee $l6
    local.get $l2
    i64.load offset=24 align=4
    i64.store align=4
    local.get $l3
    i32.const 28
    i32.add
    local.tee $l8
    local.get $l2
    i64.load offset=16 align=4
    i64.store align=4
    local.get $l3
    i32.const 20
    i32.add
    local.tee $l9
    local.get $l2
    i64.load offset=8 align=4
    i64.store align=4
    local.get $l3
    local.get $l2
    i64.load align=4
    i64.store offset=12 align=4
    local.get $p0
    local.get $l13
    i32.const 6
    i32.shl
    i32.add
    local.tee $l2
    i64.load
    local.set $l32
    local.get $l2
    i64.load offset=8
    local.set $l33
    local.get $p0
    local.get $l22
    f32.store offset=40
    local.get $p0
    local.get $l23
    f32.store offset=36
    local.get $p0
    local.get $l24
    f32.store offset=32
    local.get $p0
    local.get $l31
    f32.store offset=28
    local.get $p0
    local.get $l20
    f32.store offset=24
    local.get $p0
    local.get $l19
    f32.store offset=20
    local.get $p0
    local.get $l21
    f32.store offset=16
    local.get $p0
    local.get $l33
    i64.store offset=8
    local.get $p0
    local.get $l32
    i64.store
    local.get $p0
    local.get $l3
    i64.load offset=216
    i64.store offset=44 align=4
    local.get $l14
    i64.load offset=8 align=4
    local.set $l32
    local.get $l14
    i64.load align=4
    local.set $l33
    local.get $p0
    local.get $l27
    f32.store offset=88
    local.get $p0
    local.get $l26
    f32.store offset=84
    local.get $p0
    local.get $l28
    f32.store offset=80
    local.get $p0
    local.get $l32
    i64.store offset=72 align=4
    local.get $p0
    local.get $l33
    i64.store offset=64 align=4
    local.get $p0
    local.get $l3
    i64.load offset=144
    i64.store offset=108 align=4
    local.get $p0
    local.get $l3
    i64.load offset=136
    i64.store offset=100 align=4
    local.get $p0
    local.get $l3
    i64.load offset=128
    i64.store offset=92 align=4
    local.get $p0
    local.get $l10
    i64.load align=4
    i64.store offset=128 align=4
    local.get $p0
    local.get $l10
    i64.load offset=8 align=4
    i64.store offset=136 align=4
    local.get $p0
    local.get $l10
    i64.load offset=16 align=4
    i64.store offset=144 align=4
    local.get $p0
    local.get $l10
    i64.load offset=24 align=4
    i64.store offset=152 align=4
    local.get $p0
    local.get $l10
    i64.load offset=32 align=4
    i64.store offset=160 align=4
    local.get $p0
    local.get $l10
    i64.load offset=40 align=4
    i64.store offset=168 align=4
    local.get $p0
    local.get $l10
    i32.load offset=48
    i32.store offset=176
    local.get $p0
    local.get $l11
    i64.load offset=8 align=4
    i64.store offset=200 align=4
    local.get $p0
    local.get $l11
    i64.load offset=16 align=4
    i64.store offset=208 align=4
    local.get $p0
    local.get $l11
    i64.load offset=24 align=4
    i64.store offset=216 align=4
    local.get $p0
    local.get $l11
    i64.load offset=32 align=4
    i64.store offset=224 align=4
    local.get $p0
    local.get $l11
    i64.load offset=40 align=4
    i64.store offset=232 align=4
    local.get $p0
    local.get $l11
    i32.load offset=48
    i32.store offset=240
    local.get $p0
    local.get $l11
    i64.load align=4
    i64.store offset=192 align=4
    local.get $p0
    local.get $l3
    i64.load offset=12 align=4
    i64.store offset=256 align=4
    local.get $p0
    local.get $l9
    i64.load align=4
    i64.store offset=264 align=4
    local.get $p0
    local.get $l8
    i64.load align=4
    i64.store offset=272 align=4
    local.get $p0
    local.get $l6
    i64.load align=4
    i64.store offset=280 align=4
    local.get $p0
    local.get $l5
    i64.load align=4
    i64.store offset=288 align=4
    local.get $p0
    local.get $l4
    i64.load align=4
    i64.store offset=296 align=4
    local.get $p0
    local.get $l7
    i32.load
    i32.store offset=304
    local.get $l3
    i32.const 256
    i32.add
    global.set $g0)
