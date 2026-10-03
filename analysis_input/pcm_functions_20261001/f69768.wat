  (func $f69768 (type $t2) (param $p0 i32) (param $p1 i32) (param $p2 i32)
    (local $l3 f32) (local $l4 f32) (local $l5 f32) (local $l6 f32) (local $l7 f32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32) (local $l33 f32) (local $l34 f32) (local $l35 f32) (local $l36 i32) (local $l37 i32) (local $l38 i32) (local $l39 i32) (local $l40 i32) (local $l41 i32) (local $l42 i32)
    local.get $p1
    f32.load offset=32
    local.set $l18
    local.get $p1
    f32.load offset=28
    local.set $l19
    local.get $p1
    f32.load offset=20
    local.set $l20
    local.get $p1
    f32.load offset=16
    local.set $l21
    local.get $p1
    f32.load offset=24
    local.set $l22
    local.get $p1
    f32.load offset=12
    local.set $l23
    local.get $p1
    f32.load offset=8
    local.set $l24
    local.get $p1
    f32.load offset=4
    local.set $l25
    local.get $p1
    f32.load
    local.set $l26
    global.get $g0
    i32.const -64
    i32.add
    local.tee $p1
    i32.const 56
    i32.add
    local.set $l37
    f32.const 0x1p+0 (;=1;)
    local.set $l12
    loop $L0
      block $B1
        local.get $p1
        local.get $l7
        local.get $l7
        f32.add
        local.tee $l8
        local.get $l10
        f32.mul
        local.tee $l13
        local.get $l6
        local.get $l6
        f32.add
        local.tee $l5
        local.get $l12
        f32.mul
        local.tee $l16
        f32.add
        local.tee $l3
        local.get $l3
        local.get $l26
        f32.mul
        local.get $l5
        local.get $l10
        f32.mul
        local.tee $l11
        local.get $l8
        local.get $l12
        f32.mul
        local.tee $l14
        f32.sub
        local.tee $l4
        local.get $l25
        f32.mul
        f32.add
        f32.const 0x1p+0 (;=1;)
        local.get $l7
        local.get $l8
        f32.mul
        f32.sub
        local.tee $l9
        local.get $l6
        local.get $l5
        f32.mul
        local.tee $l15
        f32.sub
        local.tee $l5
        local.get $l24
        f32.mul
        f32.add
        local.tee $l28
        f32.mul
        local.get $l4
        local.get $l3
        local.get $l23
        f32.mul
        local.get $l4
        local.get $l21
        f32.mul
        f32.add
        local.get $l5
        local.get $l20
        f32.mul
        f32.add
        local.tee $l29
        f32.mul
        f32.add
        local.get $l5
        local.get $l3
        local.get $l22
        f32.mul
        local.get $l4
        local.get $l19
        f32.mul
        f32.add
        local.get $l5
        local.get $l18
        f32.mul
        f32.add
        local.tee $l30
        f32.mul
        f32.add
        local.tee $l33
        f32.store offset=40
        local.get $p1
        local.get $l3
        local.get $l8
        local.get $l6
        f32.mul
        local.tee $l27
        local.get $l10
        local.get $l10
        f32.add
        local.tee $l17
        local.get $l12
        f32.mul
        local.tee $l34
        f32.sub
        local.tee $l8
        local.get $l26
        f32.mul
        local.get $l9
        local.get $l10
        local.get $l17
        f32.mul
        local.tee $l35
        f32.sub
        local.tee $l9
        local.get $l25
        f32.mul
        f32.add
        local.get $l11
        local.get $l14
        f32.add
        local.tee $l11
        local.get $l24
        f32.mul
        f32.add
        local.tee $l17
        f32.mul
        local.get $l4
        local.get $l8
        local.get $l23
        f32.mul
        local.get $l9
        local.get $l21
        f32.mul
        f32.add
        local.get $l11
        local.get $l20
        f32.mul
        f32.add
        local.tee $l31
        f32.mul
        f32.add
        local.get $l5
        local.get $l8
        local.get $l22
        f32.mul
        local.get $l9
        local.get $l19
        f32.mul
        f32.add
        local.get $l11
        local.get $l18
        f32.mul
        f32.add
        local.tee $l32
        f32.mul
        f32.add
        f32.store offset=36
        local.get $p1
        local.get $l3
        f32.const 0x1p+0 (;=1;)
        local.get $l15
        f32.sub
        local.get $l35
        f32.sub
        local.tee $l14
        local.get $l26
        f32.mul
        local.get $l27
        local.get $l34
        f32.add
        local.tee $l15
        local.get $l25
        f32.mul
        f32.add
        local.get $l13
        local.get $l16
        f32.sub
        local.tee $l13
        local.get $l24
        f32.mul
        f32.add
        local.tee $l16
        f32.mul
        local.get $l4
        local.get $l14
        local.get $l23
        f32.mul
        local.get $l15
        local.get $l21
        f32.mul
        f32.add
        local.get $l13
        local.get $l20
        f32.mul
        f32.add
        local.tee $l3
        f32.mul
        f32.add
        local.get $l5
        local.get $l14
        local.get $l22
        f32.mul
        local.get $l15
        local.get $l19
        f32.mul
        f32.add
        local.get $l13
        local.get $l18
        f32.mul
        f32.add
        local.tee $l4
        f32.mul
        f32.add
        f32.store offset=32
        local.get $p1
        local.get $l8
        local.get $l17
        f32.mul
        local.get $l9
        local.get $l31
        f32.mul
        f32.add
        local.get $l11
        local.get $l32
        f32.mul
        f32.add
        local.tee $l27
        f32.store offset=24
        local.get $p1
        local.get $l8
        local.get $l16
        f32.mul
        local.get $l9
        local.get $l3
        f32.mul
        f32.add
        local.get $l11
        local.get $l4
        f32.mul
        f32.add
        f32.store offset=20
        local.get $p1
        local.get $l14
        local.get $l16
        f32.mul
        local.get $l15
        local.get $l3
        f32.mul
        f32.add
        local.get $l13
        local.get $l4
        f32.mul
        f32.add
        local.tee $l16
        f32.store offset=8
        local.get $p1
        local.get $l14
        local.get $l28
        f32.mul
        local.get $l15
        local.get $l29
        f32.mul
        f32.add
        local.get $l13
        local.get $l30
        f32.mul
        f32.add
        local.tee $l3
        f32.store offset=16
        local.get $p1
        local.get $l14
        local.get $l17
        f32.mul
        local.get $l15
        local.get $l31
        f32.mul
        f32.add
        local.get $l13
        local.get $l32
        f32.mul
        f32.add
        local.tee $l4
        f32.store offset=12
        local.get $p1
        local.get $l8
        local.get $l28
        f32.mul
        local.get $l9
        local.get $l29
        f32.mul
        f32.add
        local.get $l11
        local.get $l30
        f32.mul
        f32.add
        local.tee $l5
        f32.store offset=28
        local.get $p1
        i32.const 8
        i32.add
        i32.const 0
        i32.const 1
        i32.const 2
        local.get $l3
        f32.abs
        local.tee $l3
        local.get $l4
        f32.abs
        local.tee $l4
        f32.gt
        select
        local.tee $l36
        local.get $l5
        f32.abs
        local.tee $l5
        local.get $l4
        f32.gt
        select
        local.get $l36
        local.get $l3
        local.get $l5
        f32.lt
        select
        local.tee $l38
        local.get $l38
        i32.const 1
        i32.shr_u
        i32.add
        i32.const 1
        i32.add
        local.tee $l39
        i32.const 3
        i32.and
        local.tee $l36
        i32.const 12
        i32.mul
        i32.add
        local.tee $l41
        local.get $l39
        local.get $l36
        i32.const 1
        i32.shr_u
        i32.add
        i32.const 1
        i32.add
        i32.const 3
        i32.and
        local.tee $l39
        i32.const 2
        i32.shl
        local.tee $l42
        i32.add
        f32.load
        local.tee $l3
        f32.const 0x0p+0 (;=0;)
        f32.eq
        br_if $B1
        local.get $l41
        local.get $l36
        i32.const 2
        i32.shl
        i32.add
        f32.load
        local.get $p1
        i32.const 8
        i32.add
        local.get $l39
        i32.const 12
        i32.mul
        i32.add
        local.get $l42
        i32.add
        f32.load
        f32.sub
        local.tee $l4
        f32.abs
        local.get $l3
        local.get $l3
        f32.add
        local.tee $l3
        f32.abs
        f32.const 0x1.e848p+20 (;=2e+06;)
        f32.mul
        f32.gt
        br_if $B1
        local.get $l12
        block $B2 (result f32)
          local.get $l4
          local.get $l3
          f32.div
          local.tee $l4
          f32.abs
          local.tee $l3
          f32.const 0x1.f4p+9 (;=1000;)
          f32.gt
          if $I3
            local.get $l37
            i32.const 0
            i32.store
            local.get $p1
            i64.const 0
            i64.store offset=48
            local.get $p1
            i32.const 48
            i32.add
            local.get $l38
            i32.const 2
            i32.shl
            i32.add
            f32.const 0x1p+0 (;=1;)
            local.get $l4
            f32.const 0x1p+2 (;=4;)
            f32.mul
            f32.div
            f32.store
            f32.const 0x1p+0 (;=1;)
            br $B2
          end
          local.get $l37
          i32.const 0
          i32.store
          local.get $p1
          i64.const 0
          i64.store offset=48
          local.get $p1
          i32.const 48
          i32.add
          local.get $l38
          i32.const 2
          i32.shl
          i32.add
          f32.const 0x1p+0 (;=1;)
          f32.const 0x1p+0 (;=1;)
          f32.const 0x1p+0 (;=1;)
          local.get $l3
          local.get $l4
          local.get $l4
          f32.mul
          f32.const 0x1p+0 (;=1;)
          f32.add
          f32.sqrt
          f32.add
          f32.div
          local.tee $l3
          local.get $l3
          f32.mul
          f32.const 0x1p+0 (;=1;)
          f32.add
          f32.sqrt
          f32.div
          local.tee $l3
          f32.sub
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          f32.sqrt
          local.tee $l5
          local.get $l5
          f32.neg
          local.get $l4
          f32.const 0x0p+0 (;=0;)
          f32.ge
          select
          f32.store
          local.get $l3
          f32.const 0x1p+0 (;=1;)
          f32.add
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          f32.sqrt
        end
        local.tee $l3
        f32.mul
        local.get $l7
        local.get $p1
        f32.load offset=48
        local.tee $l4
        f32.mul
        f32.sub
        local.get $l6
        local.get $p1
        f32.load offset=52
        local.tee $l5
        f32.mul
        f32.sub
        local.get $l10
        local.get $l37
        f32.load
        local.tee $l8
        f32.mul
        f32.sub
        local.tee $l9
        f32.const 0x1p+0 (;=1;)
        local.get $l9
        local.get $l9
        f32.mul
        local.get $l7
        local.get $l5
        f32.mul
        local.get $l12
        local.get $l8
        f32.mul
        local.get $l10
        local.get $l3
        f32.mul
        f32.add
        f32.add
        local.get $l6
        local.get $l4
        f32.mul
        f32.sub
        local.tee $l9
        local.get $l9
        f32.mul
        local.get $l6
        local.get $l8
        f32.mul
        local.get $l12
        local.get $l4
        f32.mul
        local.get $l7
        local.get $l3
        f32.mul
        f32.add
        f32.add
        local.get $l10
        local.get $l5
        f32.mul
        f32.sub
        local.tee $l11
        local.get $l11
        f32.mul
        local.get $l10
        local.get $l4
        f32.mul
        local.get $l12
        local.get $l5
        f32.mul
        local.get $l6
        local.get $l3
        f32.mul
        f32.add
        f32.add
        local.get $l7
        local.get $l8
        f32.mul
        f32.sub
        local.tee $l6
        local.get $l6
        f32.mul
        f32.add
        f32.add
        f32.add
        f32.sqrt
        f32.div
        local.tee $l7
        f32.mul
        local.set $l12
        local.get $l9
        local.get $l7
        f32.mul
        local.set $l10
        local.get $l6
        local.get $l7
        f32.mul
        local.set $l6
        local.get $l11
        local.get $l7
        f32.mul
        local.set $l7
        local.get $l40
        i32.const 1
        i32.add
        local.tee $l40
        i32.const 24
        i32.ne
        br_if $L0
      end
    end
    local.get $p2
    local.get $l12
    f32.store offset=12
    local.get $p2
    local.get $l10
    f32.store offset=8
    local.get $p2
    local.get $l6
    f32.store offset=4
    local.get $p2
    local.get $l7
    f32.store
    local.get $p0
    local.get $l33
    f32.store offset=8
    local.get $p0
    local.get $l27
    f32.store offset=4
    local.get $p0
    local.get $l16
    f32.store)