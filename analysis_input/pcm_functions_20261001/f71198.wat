  (func $f71198 (type $t103) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 f32)
    (local $l5 f32) (local $l6 f32) (local $l7 f32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 i32) (local $l28 i32) (local $l29 i32)
    block $B0
      local.get $p3
      i32.load16_u offset=108
      local.tee $l27
      i32.eqz
      br_if $B0
      local.get $l27
      i32.const 1
      i32.and
      if $I1
        local.get $p0
        i32.const 0
        i32.store
        local.get $p2
        i32.const 0
        i32.store
      end
      local.get $l27
      i32.const 2
      i32.and
      if $I2
        local.get $p0
        i32.const 0
        i32.store offset=4
        local.get $p2
        i32.const 0
        i32.store offset=4
      end
      local.get $l27
      i32.const 4
      i32.and
      if $I3
        local.get $p0
        i32.const 0
        i32.store offset=8
        local.get $p2
        i32.const 0
        i32.store offset=8
      end
      local.get $l27
      i32.const 8
      i32.and
      if $I4
        local.get $p1
        i32.const 0
        i32.store
        local.get $p2
        i32.const 0
        i32.store offset=16
      end
      local.get $l27
      i32.const 16
      i32.and
      if $I5
        local.get $p1
        i32.const 0
        i32.store offset=4
        local.get $p2
        i32.const 0
        i32.store offset=20
      end
      local.get $l27
      i32.const 32
      i32.and
      i32.eqz
      br_if $B0
      local.get $p1
      i32.const 0
      i32.store offset=8
      local.get $p2
      i32.const 0
      i32.store offset=24
    end
    local.get $p3
    f32.load offset=44
    local.set $l7
    local.get $p3
    f32.load offset=56
    local.set $l8
    local.get $p3
    i32.const 20
    i32.add
    local.tee $l27
    f32.load
    local.set $l12
    local.get $p3
    f32.load offset=36
    local.set $l15
    local.get $p3
    f32.load offset=48
    local.set $l13
    local.get $p3
    f32.load offset=60
    local.set $l9
    local.get $p3
    i32.const 24
    i32.add
    local.tee $l29
    f32.load
    local.set $l11
    local.get $p3
    f32.load offset=40
    local.set $l14
    local.get $p3
    f32.load offset=52
    local.set $l16
    local.get $p3
    i32.const -64
    i32.sub
    f32.load
    local.set $l21
    local.get $p1
    f32.load offset=8
    local.set $l5
    local.get $p1
    f32.load
    local.set $l6
    local.get $p1
    f32.load offset=4
    local.set $l10
    local.get $p3
    f32.load offset=16
    local.set $l22
    local.get $p3
    f32.load offset=32
    local.set $l23
    local.get $p0
    f32.load offset=8
    local.set $l19
    local.get $p3
    f32.load offset=8
    local.set $l17
    local.get $p0
    f32.load offset=4
    local.set $l20
    local.get $p3
    f32.load offset=4
    local.set $l18
    local.get $p3
    i32.const 96
    i32.add
    local.tee $l28
    local.get $p3
    f32.load
    local.tee $l24
    local.get $p0
    f32.load
    f32.add
    local.tee $l25
    local.get $p4
    f32.mul
    local.get $l28
    f32.load
    f32.add
    f32.store
    local.get $p3
    i32.const 100
    i32.add
    local.tee $l28
    local.get $l18
    local.get $l20
    f32.add
    local.tee $l20
    local.get $p4
    f32.mul
    local.get $l28
    f32.load
    f32.add
    f32.store
    local.get $p3
    i32.const 104
    i32.add
    local.tee $l28
    local.get $l17
    local.get $l19
    f32.add
    local.tee $l26
    local.get $p4
    f32.mul
    local.get $l28
    f32.load
    f32.add
    f32.store
    local.get $p3
    local.get $l24
    local.get $p2
    f32.load
    f32.add
    f32.store
    local.get $p3
    local.get $l18
    local.get $p2
    f32.load offset=4
    f32.add
    f32.store offset=4
    local.get $p3
    local.get $l17
    local.get $p2
    f32.load offset=8
    f32.add
    f32.store offset=8
    local.get $l29
    local.get $l11
    local.get $l14
    local.get $p2
    f32.load offset=16
    local.tee $l17
    f32.mul
    local.get $l16
    local.get $p2
    f32.load offset=20
    local.tee $l18
    f32.mul
    f32.add
    local.get $l21
    local.get $p2
    f32.load offset=24
    local.tee $l19
    f32.mul
    f32.add
    f32.add
    f32.store
    local.get $l27
    local.get $l12
    local.get $l15
    local.get $l17
    f32.mul
    local.get $l13
    local.get $l18
    f32.mul
    f32.add
    local.get $l9
    local.get $l19
    f32.mul
    f32.add
    f32.add
    f32.store
    local.get $p3
    local.get $l22
    local.get $l23
    local.get $l17
    f32.mul
    local.get $l7
    local.get $l18
    f32.mul
    f32.add
    local.get $l8
    local.get $l19
    f32.mul
    f32.add
    f32.add
    f32.store offset=16
    block $B6
      local.get $l22
      local.get $l6
      local.get $l23
      f32.mul
      local.get $l10
      local.get $l7
      f32.mul
      f32.add
      local.get $l5
      local.get $l8
      f32.mul
      f32.add
      f32.add
      local.tee $l7
      local.get $l7
      f32.mul
      local.get $l12
      local.get $l6
      local.get $l15
      f32.mul
      local.get $l10
      local.get $l13
      f32.mul
      f32.add
      local.get $l5
      local.get $l9
      f32.mul
      f32.add
      f32.add
      local.tee $l8
      local.get $l8
      f32.mul
      f32.add
      local.get $l11
      local.get $l6
      local.get $l14
      f32.mul
      local.get $l10
      local.get $l16
      f32.mul
      f32.add
      local.get $l5
      local.get $l21
      f32.mul
      f32.add
      f32.add
      local.tee $l5
      local.get $l5
      f32.mul
      f32.add
      local.tee $l6
      f32.const 0x0p+0 (;=0;)
      f32.eq
      if $I7
        local.get $l7
        local.set $l12
        local.get $l8
        local.set $l15
        local.get $l5
        local.set $l13
        br $B6
      end
      f32.const 0x1.312dp+23 (;=1e+07;)
      local.set $l9
      block $B8 (result f32)
        local.get $l6
        f32.sqrt
        local.tee $l10
        f32.const 0x1.312dp+23 (;=1e+07;)
        f32.gt
        i32.eqz
        if $I9
          local.get $l7
          local.set $l12
          local.get $l5
          local.set $l13
          local.get $l10
          local.set $l9
          local.get $l8
          br $B8
        end
        f32.const 0x0p+0 (;=0;)
        local.set $l12
        f32.const 0x0p+0 (;=0;)
        local.set $l13
        f32.const 0x0p+0 (;=0;)
        local.get $l6
        f32.const 0x0p+0 (;=0;)
        f32.gt
        i32.eqz
        br_if $B8
        drop
        local.get $l5
        f32.const 0x1p+0 (;=1;)
        local.get $l10
        f32.div
        local.tee $l6
        f32.mul
        f32.const 0x1.312dp+23 (;=1e+07;)
        f32.mul
        local.set $l13
        local.get $l7
        local.get $l6
        f32.mul
        f32.const 0x1.312dp+23 (;=1e+07;)
        f32.mul
        local.set $l12
        local.get $l8
        local.get $l6
        f32.mul
        f32.const 0x1.312dp+23 (;=1e+07;)
        f32.mul
      end
      local.set $l15
      local.get $l9
      local.get $p4
      f32.mul
      f32.const 0x1p-1 (;=0.5;)
      f32.mul
      local.tee $l7
      call $f18890
      local.set $l8
      local.get $p3
      i32.const 88
      i32.add
      local.tee $p2
      f32.load
      local.set $p4
      local.get $p3
      i32.const 84
      i32.add
      local.tee $l27
      f32.load
      local.set $l5
      local.get $p3
      f32.load offset=80
      local.set $l6
      local.get $p3
      i32.const 92
      i32.add
      local.tee $l29
      local.get $l29
      f32.load
      local.tee $l10
      local.get $l7
      call $f33062
      local.tee $l7
      f32.mul
      local.get $l10
      f32.const 0x0p+0 (;=0;)
      f32.mul
      local.get $l6
      local.get $l12
      local.get $l8
      local.get $l9
      f32.div
      local.tee $l11
      f32.mul
      local.tee $l8
      f32.mul
      f32.sub
      local.get $l5
      local.get $l15
      local.get $l11
      f32.mul
      local.tee $l9
      f32.mul
      f32.sub
      local.get $p4
      local.get $l13
      local.get $l11
      f32.mul
      local.tee $l11
      f32.mul
      f32.sub
      f32.add
      local.tee $l14
      f32.const 0x1p+0 (;=1;)
      local.get $l14
      local.get $l14
      f32.mul
      local.get $p4
      local.get $l7
      f32.mul
      local.get $l5
      local.get $l8
      f32.mul
      local.get $p4
      f32.const 0x0p+0 (;=0;)
      f32.mul
      local.get $l10
      local.get $l11
      f32.mul
      f32.add
      f32.add
      local.get $l6
      local.get $l9
      f32.mul
      f32.sub
      f32.add
      local.tee $l14
      local.get $l14
      f32.mul
      local.get $l6
      local.get $l7
      f32.mul
      local.get $p4
      local.get $l9
      f32.mul
      local.get $l6
      f32.const 0x0p+0 (;=0;)
      f32.mul
      local.get $l10
      local.get $l8
      f32.mul
      f32.add
      f32.add
      local.get $l5
      local.get $l11
      f32.mul
      f32.sub
      f32.add
      local.tee $l16
      local.get $l16
      f32.mul
      local.get $l7
      local.get $l5
      f32.mul
      local.get $l6
      local.get $l11
      f32.mul
      local.get $l5
      f32.const 0x0p+0 (;=0;)
      f32.mul
      local.get $l10
      local.get $l9
      f32.mul
      f32.add
      f32.add
      local.get $p4
      local.get $l8
      f32.mul
      f32.sub
      f32.add
      local.tee $l5
      local.get $l5
      f32.mul
      f32.add
      f32.add
      f32.add
      f32.sqrt
      f32.div
      local.tee $p4
      f32.mul
      f32.store
      local.get $p2
      local.get $l14
      local.get $p4
      f32.mul
      f32.store
      local.get $l27
      local.get $l5
      local.get $p4
      f32.mul
      f32.store
      local.get $p3
      local.get $l16
      local.get $p4
      f32.mul
      f32.store offset=80
    end
    local.get $p0
    local.get $l26
    f32.store offset=8
    local.get $p0
    local.get $l20
    f32.store offset=4
    local.get $p0
    local.get $l25
    f32.store
    local.get $p1
    local.get $l13
    f32.store offset=8
    local.get $p1
    local.get $l15
    f32.store offset=4
    local.get $p1
    local.get $l12
    f32.store)
