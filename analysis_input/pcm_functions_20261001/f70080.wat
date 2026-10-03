  (func $f70080 (type $t439) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 f32) (result i32)
    (local $l5 f32) (local $l6 f32) (local $l7 f32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 i32) (local $l25 i32) (local $l26 i32) (local $l27 i32) (local $l28 i32)
    global.get $g0
    i32.const 1024
    i32.sub
    local.tee $l26
    global.set $g0
    local.get $l26
    local.get $p0
    i32.load offset=24
    local.tee $l25
    f32.load offset=12
    local.get $p3
    f32.load
    local.tee $l6
    local.get $p1
    i32.load offset=40
    local.tee $p1
    f32.load
    local.tee $l14
    f32.mul
    local.get $p3
    f32.load offset=4
    local.tee $l9
    local.get $p1
    f32.load offset=16
    local.tee $l15
    f32.mul
    f32.add
    local.get $p3
    f32.load offset=8
    local.tee $l5
    local.get $p1
    f32.load offset=32
    local.tee $l16
    f32.mul
    f32.add
    local.tee $l8
    local.get $l25
    f32.load
    f32.mul
    local.get $l6
    local.get $p1
    f32.load offset=4
    local.tee $l17
    f32.mul
    local.get $l9
    local.get $p1
    f32.load offset=20
    local.tee $l18
    f32.mul
    f32.add
    local.get $l5
    local.get $p1
    f32.load offset=36
    local.tee $l19
    f32.mul
    f32.add
    local.tee $l10
    local.get $l25
    f32.load offset=4
    f32.mul
    f32.add
    local.get $l6
    local.get $p1
    f32.load offset=8
    local.tee $l20
    f32.mul
    local.get $l9
    local.get $p1
    f32.load offset=24
    local.tee $l21
    f32.mul
    f32.add
    local.get $l5
    local.get $p1
    f32.load offset=40
    local.tee $l22
    f32.mul
    f32.add
    local.tee $l12
    local.get $l25
    f32.load offset=8
    f32.mul
    f32.add
    f32.add
    local.tee $l5
    f32.abs
    f32.const 0x1.fffffep+127 (;=3.40282e+38;)
    local.get $l5
    local.get $p4
    f32.neg
    local.tee $l13
    f32.ge
    select
    local.tee $l11
    f32.store
    i32.const 1
    local.set $p1
    block $B0
      local.get $p0
      i32.load offset=16
      local.tee $l27
      i32.const 1
      i32.le_u
      if $I1
        i32.const 0
        local.set $p0
        local.get $l11
        local.set $l9
        br $B0
      end
      local.get $l11
      local.set $l9
      i32.const 0
      local.set $p0
      loop $L2
        local.get $l26
        local.get $p1
        i32.const 2
        i32.shl
        i32.add
        local.get $l25
        local.get $p1
        i32.const 20
        i32.mul
        i32.add
        local.tee $p3
        f32.load offset=12
        local.get $l8
        local.get $p3
        f32.load
        f32.mul
        local.get $l10
        local.get $p3
        f32.load offset=4
        f32.mul
        f32.add
        local.get $l12
        local.get $p3
        f32.load offset=8
        f32.mul
        f32.add
        f32.add
        local.tee $l6
        f32.abs
        f32.const 0x1.fffffep+127 (;=3.40282e+38;)
        local.get $l6
        local.get $l13
        f32.ge
        select
        local.tee $l7
        f32.store
        local.get $l7
        local.get $l9
        local.get $l7
        local.get $l9
        f32.lt
        local.tee $p3
        select
        local.set $l9
        local.get $l6
        local.get $l5
        local.get $l5
        local.get $l6
        f32.lt
        local.tee $l28
        select
        local.set $l5
        local.get $p1
        local.get $p0
        local.get $p3
        select
        local.set $p0
        local.get $p1
        local.get $l24
        local.get $l28
        select
        local.set $l24
        local.get $p1
        i32.const 1
        i32.add
        local.tee $p1
        local.get $l27
        i32.ne
        br_if $L2
      end
    end
    block $B3
      local.get $l9
      f32.const 0x1.fffffep+127 (;=3.40282e+38;)
      f32.eq
      br_if $B3
      local.get $l27
      i32.eqz
      if $I4
        local.get $p0
        local.set $l24
        br $B3
      end
      local.get $p2
      f32.load offset=8
      local.tee $l12
      local.get $l16
      local.get $l25
      local.get $p0
      i32.const 20
      i32.mul
      i32.add
      local.tee $p1
      f32.load
      local.tee $l6
      f32.mul
      local.get $l19
      local.get $p1
      f32.load offset=4
      local.tee $l5
      f32.mul
      f32.add
      local.get $l22
      local.get $p1
      f32.load offset=8
      local.tee $l7
      f32.mul
      f32.add
      local.tee $l8
      f32.const 0x1p+0 (;=1;)
      local.get $l8
      local.get $l8
      f32.mul
      local.get $l14
      local.get $l6
      f32.mul
      local.get $l17
      local.get $l5
      f32.mul
      f32.add
      local.get $l20
      local.get $l7
      f32.mul
      f32.add
      local.tee $l8
      local.get $l8
      f32.mul
      local.get $l15
      local.get $l6
      f32.mul
      local.get $l18
      local.get $l5
      f32.mul
      f32.add
      local.get $l21
      local.get $l7
      f32.mul
      f32.add
      local.tee $l6
      local.get $l6
      f32.mul
      f32.add
      f32.add
      f32.sqrt
      f32.div
      local.tee $l5
      f32.mul
      f32.mul
      local.get $p2
      f32.load
      local.tee $l13
      local.get $l8
      local.get $l5
      f32.mul
      f32.mul
      local.get $p2
      f32.load offset=4
      local.tee $l23
      local.get $l6
      local.get $l5
      f32.mul
      f32.mul
      f32.add
      f32.add
      local.set $l6
      i32.const 0
      local.set $p1
      local.get $p0
      local.set $l24
      loop $L5
        block $B6
          local.get $p0
          local.get $p1
          i32.eq
          br_if $B6
          local.get $l11
          local.get $l9
          f32.sub
          local.get $p4
          f32.lt
          i32.eqz
          br_if $B6
          local.get $l12
          local.get $l16
          local.get $l25
          local.get $p1
          i32.const 20
          i32.mul
          i32.add
          local.tee $p3
          f32.load
          local.tee $l5
          f32.mul
          local.get $l19
          local.get $p3
          f32.load offset=4
          local.tee $l7
          f32.mul
          f32.add
          local.get $l22
          local.get $p3
          f32.load offset=8
          local.tee $l8
          f32.mul
          f32.add
          local.tee $l10
          f32.const 0x1p+0 (;=1;)
          local.get $l10
          local.get $l10
          f32.mul
          local.get $l14
          local.get $l5
          f32.mul
          local.get $l17
          local.get $l7
          f32.mul
          f32.add
          local.get $l20
          local.get $l8
          f32.mul
          f32.add
          local.tee $l10
          local.get $l10
          f32.mul
          local.get $l15
          local.get $l5
          f32.mul
          local.get $l18
          local.get $l7
          f32.mul
          f32.add
          local.get $l21
          local.get $l8
          f32.mul
          f32.add
          local.tee $l5
          local.get $l5
          f32.mul
          f32.add
          f32.add
          f32.sqrt
          f32.div
          local.tee $l7
          f32.mul
          f32.mul
          local.get $l13
          local.get $l10
          local.get $l7
          f32.mul
          f32.mul
          local.get $l23
          local.get $l5
          local.get $l7
          f32.mul
          f32.mul
          f32.add
          f32.add
          local.tee $l5
          local.get $l6
          local.get $l5
          local.get $l6
          f32.lt
          local.tee $p3
          select
          local.set $l6
          local.get $p1
          local.get $l24
          local.get $p3
          select
          local.set $l24
        end
        local.get $p1
        i32.const 1
        i32.add
        local.tee $p1
        local.get $l27
        i32.eq
        br_if $B3
        local.get $l26
        local.get $p1
        i32.const 2
        i32.shl
        i32.add
        f32.load
        local.set $l11
        br $L5
      end
      unreachable
    end
    local.get $l26
    i32.const 1024
    i32.add
    global.set $g0
    local.get $l24)