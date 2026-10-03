  (func $f69875 (type $t32) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 i32) (param $p7 i32) (param $p8 i32) (param $p9 i32) (result i32)
    (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 i32)
    global.get $g0
    i32.const -64
    i32.add
    local.tee $p2
    global.set $g0
    local.get $p3
    local.get $p4
    i64.load offset=8
    i64.store offset=8
    local.get $p3
    local.get $p4
    i64.load
    i64.store
    local.get $p2
    i32.const 32
    i32.add
    local.get $p2
    local.get $p4
    local.get $p5
    local.get $p6
    call $f72749
    local.get $p5
    i32.const 20
    i32.add
    local.tee $p3
    f32.load
    local.set $l14
    i32.const 24
    local.set $p7
    local.get $p5
    f32.load offset=16
    local.set $l12
    local.get $p2
    f32.load offset=20
    local.set $l10
    local.get $p2
    f32.load offset=16
    local.set $l11
    local.get $p1
    local.get $p2
    f32.load offset=24
    local.tee $l13
    local.get $p5
    i32.const 24
    i32.add
    local.tee $l23
    f32.load
    f32.sub
    f32.store offset=8
    local.get $p1
    local.get $l10
    local.get $l14
    f32.sub
    f32.store offset=4
    local.get $p1
    local.get $l11
    local.get $l12
    f32.sub
    f32.store
    local.get $p3
    f32.load
    local.set $l14
    local.get $l23
    f32.load
    local.set $l12
    local.get $p6
    f32.load offset=20
    local.set $l16
    local.get $p6
    f32.load offset=24
    local.set $l15
    local.get $p5
    f32.load offset=16
    local.set $l17
    local.get $p6
    f32.load offset=16
    local.set $l18
    local.get $p8
    local.get $l13
    f32.store offset=8
    local.get $p8
    local.get $l10
    f32.store offset=4
    local.get $p8
    local.get $l11
    f32.store
    local.get $p9
    local.get $l13
    f32.store offset=8
    local.get $p9
    local.get $l10
    f32.store offset=4
    local.get $p9
    local.get $l11
    f32.store
    local.get $l13
    local.get $l15
    f32.sub
    local.set $l15
    local.get $l10
    local.get $l16
    f32.sub
    local.set $l16
    local.get $l11
    local.get $l18
    f32.sub
    local.set $l18
    local.get $l13
    local.get $l12
    f32.sub
    local.set $l19
    local.get $l10
    local.get $l14
    f32.sub
    local.set $l20
    local.get $l11
    local.get $l17
    f32.sub
    local.set $l17
    local.get $p2
    f32.load offset=48
    local.get $l11
    f32.sub
    local.tee $l14
    local.get $l14
    f32.mul
    local.get $p2
    f32.load offset=52
    local.get $l10
    f32.sub
    local.tee $l11
    local.get $l11
    f32.mul
    f32.add
    local.get $p2
    f32.load offset=56
    local.get $l13
    f32.sub
    local.tee $l10
    local.get $l10
    f32.mul
    f32.add
    f32.sqrt
    local.tee $l12
    f32.const 0x0p+0 (;=0;)
    f32.gt
    if $I0
      local.get $l10
      f32.const 0x1p+0 (;=1;)
      local.get $l12
      f32.div
      local.tee $l13
      f32.mul
      local.set $l10
      local.get $l14
      local.get $l13
      f32.mul
      local.set $l14
      local.get $l11
      local.get $l13
      f32.mul
      local.set $l11
    end
    local.get $p4
    i32.load16_u offset=100
    local.set $p6
    local.get $p0
    i32.const 16
    i32.store16 offset=76
    local.get $p0
    f32.const 0x0p+0 (;=0;)
    local.get $l10
    local.get $l12
    f32.const 0x1p-23 (;=1.19209e-07;)
    f32.lt
    local.tee $p5
    select
    local.tee $l10
    f32.store offset=40
    local.get $p0
    f32.const 0x0p+0 (;=0;)
    local.get $l11
    local.get $p5
    select
    local.tee $l11
    f32.store offset=36
    local.get $p0
    f32.const 0x1p+0 (;=1;)
    local.get $l14
    local.get $p5
    select
    local.tee $l13
    f32.store offset=32
    local.get $p0
    local.get $l10
    f32.store offset=8
    local.get $p0
    local.get $l11
    f32.store offset=4
    local.get $p0
    local.get $l13
    f32.store
    local.get $p0
    local.get $l18
    local.get $l11
    f32.mul
    local.get $l16
    local.get $l13
    f32.mul
    f32.sub
    local.tee $l21
    f32.store offset=56
    local.get $p0
    local.get $l15
    local.get $l13
    f32.mul
    local.get $l18
    local.get $l10
    f32.mul
    f32.sub
    local.tee $l18
    f32.store offset=52
    local.get $p0
    local.get $l16
    local.get $l10
    f32.mul
    local.get $l15
    local.get $l11
    f32.mul
    f32.sub
    local.tee $l16
    f32.store offset=48
    local.get $p0
    local.get $l17
    local.get $l11
    f32.mul
    local.get $l20
    local.get $l13
    f32.mul
    f32.sub
    local.tee $l22
    f32.store offset=24
    local.get $p0
    local.get $l19
    local.get $l13
    f32.mul
    local.get $l17
    local.get $l10
    f32.mul
    f32.sub
    local.tee $l17
    f32.store offset=20
    local.get $p0
    local.get $l20
    local.get $l10
    f32.mul
    local.get $l19
    local.get $l11
    f32.mul
    f32.sub
    local.tee $l19
    f32.store offset=16
    local.get $p4
    i32.load8_u offset=100
    i32.const 8
    i32.and
    if $I1
      local.get $p0
      i32.const 17
      i32.store16 offset=76
      local.get $p0
      local.get $p4
      f32.load offset=92
      f32.store offset=64
      local.get $p0
      local.get $p4
      f32.load offset=96
      f32.store offset=68
      i32.const 25
      local.set $p7
    end
    local.get $p4
    f32.load offset=84
    local.set $l14
    local.get $p4
    f32.load offset=80
    local.set $l15
    block $B2 (result i32)
      block $B3
        local.get $p6
        i32.const 6
        i32.and
        i32.const 6
        i32.ne
        br_if $B3
        local.get $l14
        local.get $l15
        f32.ne
        br_if $B3
        local.get $p0
        block $B4 (result f32)
          local.get $l12
          local.get $l14
          f32.sub
          local.tee $l10
          local.get $p4
          f32.load offset=88
          local.tee $l11
          f32.gt
          if $I5
            local.get $l10
            local.get $l11
            f32.sub
            br $B4
          end
          f32.const 0x0p+0 (;=0;)
          local.get $l10
          local.get $l11
          f32.neg
          f32.lt
          i32.eqz
          br_if $B4
          drop
          local.get $l10
          local.get $l11
          f32.add
        end
        f32.store offset=12
        i32.const 1
        br $B2
      end
      local.get $p6
      i32.const 4
      i32.and
      local.set $p9
      block $B6
        block $B7
          block $B8
            local.get $p6
            i32.const 2
            i32.and
            if $I9
              local.get $l12
              local.get $l14
              f32.gt
              if $I10
                local.get $p4
                f32.load offset=88
                local.set $l10
                local.get $p0
                i32.const 0
                i32.store offset=60
                local.get $p0
                local.get $l12
                local.get $l14
                f32.sub
                local.get $l10
                f32.sub
                f32.store offset=12
                i32.const 1
                br $B2
              end
              local.get $p9
              i32.eqz
              br_if $B7
              local.get $l12
              local.get $l15
              f32.lt
              br_if $B8
              local.get $p0
              local.get $p7
              i32.store16 offset=76
              local.get $p0
              i32.const 2139095039
              i32.store offset=60
              local.get $p0
              i32.const 0
              i32.store offset=44
              local.get $p0
              local.get $l13
              f32.store offset=80
              local.get $p0
              i32.const 16
              i32.store16 offset=156
              local.get $p0
              local.get $l12
              local.get $l15
              f32.sub
              f32.store offset=12
              local.get $p0
              local.get $l21
              f32.store offset=136
              local.get $p0
              local.get $l18
              f32.store offset=132
              local.get $p0
              local.get $l16
              f32.store offset=128
              local.get $p0
              local.get $l10
              f32.store offset=120
              local.get $p0
              local.get $l11
              f32.store offset=116
              local.get $p0
              local.get $l13
              f32.store offset=112
              local.get $p0
              local.get $l22
              f32.store offset=104
              local.get $p0
              local.get $l17
              f32.store offset=100
              local.get $p0
              local.get $l19
              f32.store offset=96
              local.get $p0
              local.get $l10
              f32.store offset=88
              local.get $p0
              local.get $l11
              f32.store offset=84
              i32.const 24
              local.set $p5
              local.get $p4
              i32.load8_u offset=100
              i32.const 8
              i32.and
              if $I11
                local.get $p0
                i32.const 17
                i32.store16 offset=156
                local.get $p0
                local.get $p4
                f32.load offset=92
                f32.store offset=144
                local.get $p0
                local.get $p4
                f32.load offset=96
                f32.store offset=148
                i32.const 25
                local.set $p5
              end
              local.get $p4
              f32.load offset=84
              local.set $l10
              local.get $p0
              local.get $p5
              i32.store16 offset=156
              local.get $p0
              i32.const 0
              i32.store offset=140
              local.get $p0
              i32.const -8388609
              i32.store offset=124
              local.get $p0
              local.get $l12
              local.get $l10
              f32.sub
              f32.store offset=92
              i32.const 2
              br $B2
            end
            i32.const 1
            local.get $p9
            i32.eqz
            br_if $B2
            drop
            local.get $l12
            local.get $l15
            f32.lt
            i32.eqz
            br_if $B6
          end
          local.get $p4
          f32.load offset=88
          local.set $l10
          local.get $p0
          i32.const 0
          i32.store offset=44
          local.get $p0
          local.get $l10
          local.get $l12
          local.get $l15
          f32.sub
          f32.add
          f32.store offset=12
          i32.const 1
          br $B2
        end
        local.get $p0
        local.get $p7
        i32.store16 offset=76
        local.get $p0
        i32.const 0
        i32.store offset=60
        local.get $p0
        i32.const -8388609
        i32.store offset=44
        local.get $p0
        local.get $l12
        local.get $l14
        f32.sub
        f32.store offset=12
        i32.const 0
        br $B2
      end
      local.get $p0
      local.get $p7
      i32.store16 offset=76
      local.get $p0
      i32.const 2139095039
      i32.store offset=60
      local.get $p0
      i32.const 0
      i32.store offset=44
      local.get $p0
      local.get $l12
      local.get $l15
      f32.sub
      f32.store offset=12
      i32.const 0
    end
    local.set $p5
    local.get $p2
    i32.const -64
    i32.sub
    global.set $g0
    local.get $p5)
