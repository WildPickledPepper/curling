  (func $f71752 (type $t9) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (result i32)
    (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32)
    global.get $g0
    i32.const 48
    i32.sub
    local.tee $l8
    global.set $g0
    block $B0
      local.get $p0
      i32.load offset=4
      local.tee $l10
      if $I1
        local.get $p1
        f32.load offset=84
        local.set $l14
        local.get $p1
        f32.load offset=76
        local.set $l15
        local.get $p1
        f32.load offset=88
        local.set $l16
        local.get $p1
        f32.load offset=72
        local.set $l17
        local.get $l8
        local.get $p1
        f32.load offset=92
        local.tee $l18
        local.get $p1
        f32.load offset=80
        local.tee $l19
        f32.sub
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        f32.store offset=40
        local.get $l8
        local.get $l16
        local.get $l15
        f32.sub
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        f32.store offset=36
        local.get $l8
        local.get $l14
        local.get $l17
        f32.sub
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        f32.store offset=32
        local.get $p0
        i32.load offset=292
        local.set $l13
        local.get $p0
        i32.load offset=296
        local.set $l6
        local.get $l8
        local.get $l18
        local.get $l19
        f32.add
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        f32.store offset=16
        local.get $l8
        local.get $l16
        local.get $l15
        f32.add
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        f32.store offset=12
        local.get $l8
        local.get $l14
        local.get $l17
        f32.add
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        f32.store offset=8
        local.get $l6
        local.get $l13
        local.get $l10
        local.get $l8
        i32.const 8
        i32.add
        local.get $p2
        local.get $p3
        local.get $l8
        i32.const 32
        i32.add
        local.get $p4
        call $f71878
        i32.eqz
        br_if $B0
      end
      i32.const 1
      local.set $l5
      local.get $p0
      i32.load8_u offset=336
      i32.eqz
      br_if $B0
      local.get $p0
      i32.load offset=156
      local.get $p0
      i32.load offset=108
      i32.add
      i32.const 0
      local.get $p0
      i32.load offset=216
      i32.sub
      i32.eq
      br_if $B0
      i32.const 0
      local.set $l10
      global.get $g0
      i32.const -64
      i32.add
      local.tee $l5
      global.set $g0
      block $B2
        local.get $p0
        i32.const 52
        i32.add
        local.tee $p0
        i32.load offset=104
        i32.const 0
        local.get $p0
        i32.load offset=56
        i32.sub
        i32.ne
        if $I3
          local.get $p1
          local.set $l6
          global.get $g0
          i32.const 48
          i32.sub
          local.tee $l7
          global.set $g0
          i32.const 1
          local.set $l9
          block $B4
            local.get $p0
            i32.const 4
            i32.add
            local.tee $l11
            i32.load offset=12
            local.tee $l12
            i32.eqz
            br_if $B4
            local.get $l12
            i32.load offset=588
            i32.eqz
            br_if $B4
            local.get $l6
            f32.load offset=72
            local.set $l14
            local.get $l6
            f32.load offset=84
            local.set $l15
            local.get $l6
            f32.load offset=76
            local.set $l16
            local.get $l6
            f32.load offset=88
            local.set $l17
            local.get $l7
            local.get $l6
            f32.load offset=92
            local.tee $l18
            local.get $l6
            f32.load offset=80
            local.tee $l19
            f32.sub
            f32.const 0x1p-1 (;=0.5;)
            f32.mul
            f32.store offset=40
            local.get $l7
            local.get $l17
            local.get $l16
            f32.sub
            f32.const 0x1p-1 (;=0.5;)
            f32.mul
            f32.store offset=36
            local.get $l7
            local.get $l15
            local.get $l14
            f32.sub
            f32.const 0x1p-1 (;=0.5;)
            f32.mul
            f32.store offset=32
            local.get $l11
            i32.load offset=104
            local.tee $l9
            i32.load offset=8
            local.set $l13
            local.get $l9
            i32.load offset=12
            local.set $l9
            local.get $l7
            local.get $l18
            local.get $l19
            f32.add
            f32.const 0x1p-1 (;=0.5;)
            f32.mul
            f32.store offset=16
            local.get $l7
            local.get $l17
            local.get $l16
            f32.add
            f32.const 0x1p-1 (;=0.5;)
            f32.mul
            f32.store offset=12
            local.get $l7
            local.get $l15
            local.get $l14
            f32.add
            f32.const 0x1p-1 (;=0.5;)
            f32.mul
            f32.store offset=8
            local.get $l9
            local.get $l13
            local.get $l12
            local.get $l7
            i32.const 8
            i32.add
            local.get $p2
            local.get $p3
            local.get $l7
            i32.const 32
            i32.add
            local.get $p4
            call $f71879
            local.set $l9
          end
          block $B5
            local.get $l11
            i32.load offset=60
            local.tee $l12
            i32.eqz
            br_if $B5
            local.get $l12
            i32.load offset=588
            i32.eqz
            local.get $l9
            i32.const 1
            i32.xor
            i32.or
            br_if $B5
            local.get $l6
            f32.load offset=72
            local.set $l14
            local.get $l6
            f32.load offset=84
            local.set $l15
            local.get $l6
            f32.load offset=76
            local.set $l16
            local.get $l6
            f32.load offset=88
            local.set $l17
            local.get $l7
            local.get $l6
            f32.load offset=92
            local.tee $l18
            local.get $l6
            f32.load offset=80
            local.tee $l19
            f32.sub
            f32.const 0x1p-1 (;=0.5;)
            f32.mul
            f32.store offset=40
            local.get $l7
            local.get $l17
            local.get $l16
            f32.sub
            f32.const 0x1p-1 (;=0.5;)
            f32.mul
            f32.store offset=36
            local.get $l7
            local.get $l15
            local.get $l14
            f32.sub
            f32.const 0x1p-1 (;=0.5;)
            f32.mul
            f32.store offset=32
            local.get $l11
            i32.load offset=104
            local.tee $l6
            i32.load offset=8
            local.set $l11
            local.get $l6
            i32.load offset=12
            local.set $l6
            local.get $l7
            local.get $l18
            local.get $l19
            f32.add
            f32.const 0x1p-1 (;=0.5;)
            f32.mul
            f32.store offset=16
            local.get $l7
            local.get $l17
            local.get $l16
            f32.add
            f32.const 0x1p-1 (;=0.5;)
            f32.mul
            f32.store offset=12
            local.get $l7
            local.get $l15
            local.get $l14
            f32.add
            f32.const 0x1p-1 (;=0.5;)
            f32.mul
            f32.store offset=8
            local.get $l6
            local.get $l11
            local.get $l12
            local.get $l7
            i32.const 8
            i32.add
            local.get $p2
            local.get $p3
            local.get $l7
            i32.const 32
            i32.add
            local.get $p4
            call $f71879
            local.set $l9
          end
          local.get $l7
          i32.const 48
          i32.add
          global.set $g0
          local.get $l9
          i32.eqz
          br_if $B2
        end
        local.get $p0
        i32.load offset=164
        i32.eqz
        if $I6
          i32.const 1
          local.set $l10
          br $B2
        end
        local.get $p1
        f32.load offset=84
        local.set $l14
        local.get $p1
        f32.load offset=76
        local.set $l15
        local.get $p1
        f32.load offset=88
        local.set $l16
        local.get $p1
        f32.load offset=72
        local.set $l17
        local.get $l5
        local.get $p1
        f32.load offset=92
        local.tee $l18
        local.get $p1
        f32.load offset=80
        local.tee $l19
        f32.sub
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        f32.store offset=56
        local.get $l5
        local.get $l16
        local.get $l15
        f32.sub
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        f32.store offset=52
        local.get $l5
        local.get $l14
        local.get $l17
        f32.sub
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        f32.store offset=48
        local.get $l5
        local.get $l18
        local.get $l19
        f32.add
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        f32.store offset=40
        local.get $l5
        local.get $l16
        local.get $l15
        f32.add
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        f32.store offset=36
        local.get $l5
        local.get $l14
        local.get $l17
        f32.add
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        f32.store offset=32
        local.get $l5
        local.get $p0
        i32.load offset=124
        i32.store offset=28
        local.get $l5
        local.get $p4
        i32.store offset=24
        local.get $l5
        local.get $p2
        i32.store offset=16
        local.get $l5
        i32.const 3179152
        i32.store offset=8
        local.get $l5
        local.get $l5
        i32.const 48
        i32.add
        i32.store offset=20
        local.get $l5
        local.get $l5
        i32.const 32
        i32.add
        i32.store offset=12
        local.get $p0
        i32.load offset=200
        local.get $p0
        i32.load offset=196
        local.get $p0
        i32.load offset=168
        local.get $l5
        i32.const 32
        i32.add
        local.get $p2
        local.get $p3
        local.get $l5
        i32.const 48
        i32.add
        local.get $l5
        i32.const 8
        i32.add
        call $f71878
        local.set $l10
      end
      local.get $l5
      i32.const -64
      i32.sub
      global.set $g0
      local.get $l10
      local.set $l5
    end
    local.get $l8
    i32.const 48
    i32.add
    global.set $g0
    local.get $l5)