  (func $f71199 (type $t525) (param $p0 i32) (param $p1 f32) (param $p2 f32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 i32) (result f32)
    (local $l7 i32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32)
    local.get $p0
    i32.load offset=36
    local.tee $l7
    f32.load offset=140
    local.set $l14
    block $B0
      block $B1
        block $B2 (result i32)
          block $B3
            block $B4
              local.get $p3
              if $I5
                local.get $p5
                f32.load
                local.tee $l20
                local.get $l20
                f32.mul
                local.get $p5
                f32.load offset=4
                local.tee $l21
                local.get $l21
                f32.mul
                f32.add
                local.get $p5
                f32.load offset=8
                local.tee $l15
                local.get $l15
                f32.mul
                f32.add
                f32.const 0x1p+0 (;=1;)
                local.get $l7
                f32.load offset=124
                local.tee $p2
                local.get $p2
                f32.const 0x0p+0 (;=0;)
                f32.eq
                select
                local.tee $l23
                f32.const 0x1p+0 (;=1;)
                local.get $l7
                f32.load offset=120
                local.tee $p2
                f32.div
                f32.const 0x1p+0 (;=1;)
                local.get $p2
                f32.const 0x0p+0 (;=0;)
                f32.gt
                select
                local.tee $l24
                local.get $p5
                f32.load offset=24
                local.tee $p2
                local.get $p2
                f32.add
                local.tee $l11
                local.get $l7
                f32.load offset=12
                local.tee $p2
                local.get $p2
                f32.mul
                f32.const -0x1p-1 (;=-0.5;)
                f32.add
                local.tee $l16
                f32.mul
                local.get $p2
                local.get $p5
                f32.load offset=20
                local.tee $l9
                local.get $l9
                f32.add
                local.tee $l9
                local.get $l7
                f32.load
                local.tee $l10
                f32.mul
                local.get $p5
                f32.load offset=16
                local.tee $l8
                local.get $l8
                f32.add
                local.tee $l8
                local.get $l7
                f32.load offset=4
                local.tee $l12
                f32.mul
                f32.sub
                f32.mul
                f32.sub
                local.get $l7
                f32.load offset=8
                local.tee $l13
                local.get $l8
                local.get $l10
                f32.mul
                local.get $l9
                local.get $l12
                f32.mul
                f32.add
                local.get $l11
                local.get $l13
                f32.mul
                f32.add
                local.tee $l22
                f32.mul
                f32.add
                local.tee $l17
                local.get $l17
                f32.mul
                f32.mul
                f32.const 0x1p+0 (;=1;)
                local.get $l7
                f32.load offset=112
                local.tee $l18
                f32.div
                f32.const 0x1p+0 (;=1;)
                local.get $l18
                f32.const 0x0p+0 (;=0;)
                f32.gt
                select
                local.tee $l25
                local.get $l10
                local.get $l22
                f32.mul
                local.get $l8
                local.get $l16
                f32.mul
                local.get $p2
                local.get $l11
                local.get $l12
                f32.mul
                local.get $l9
                local.get $l13
                f32.mul
                f32.sub
                f32.mul
                f32.sub
                f32.add
                local.tee $l18
                local.get $l18
                f32.mul
                f32.mul
                f32.const 0x1p+0 (;=1;)
                local.get $l7
                f32.load offset=116
                local.tee $l19
                f32.div
                f32.const 0x1p+0 (;=1;)
                local.get $l19
                f32.const 0x0p+0 (;=0;)
                f32.gt
                select
                local.tee $l19
                local.get $l12
                local.get $l22
                f32.mul
                local.get $l9
                local.get $l16
                f32.mul
                local.get $p2
                local.get $l8
                local.get $l13
                f32.mul
                local.get $l11
                local.get $l10
                f32.mul
                f32.sub
                f32.mul
                f32.sub
                f32.add
                local.tee $l9
                local.get $l9
                f32.mul
                f32.mul
                f32.add
                f32.add
                f32.mul
                f32.add
                f32.const 0x1p-1 (;=0.5;)
                f32.mul
                local.set $l11
                f32.const 0x0p+0 (;=0;)
                local.set $p2
                local.get $p6
                if $I6
                  local.get $l7
                  i32.load offset=152
                  local.tee $p5
                  i32.const 10
                  local.get $p5
                  i32.const 10
                  i32.lt_u
                  select
                  f32.convert_i32_u
                  local.set $p2
                end
                local.get $l7
                f32.load offset=136
                local.set $l10
                local.get $p0
                local.get $p0
                f32.load offset=60
                local.get $p1
                f32.sub
                local.tee $l8
                f32.const 0x0p+0 (;=0;)
                local.get $l8
                f32.const 0x0p+0 (;=0;)
                f32.gt
                select
                local.tee $l12
                f32.store offset=60
                local.get $p0
                f32.load offset=76
                local.get $p1
                f32.add
                f32.const 0x1p+0 (;=1;)
                f32.min
                local.set $l8
                local.get $p2
                local.get $l10
                f32.mul
                local.get $l11
                f32.le
                if $I7
                  local.get $p0
                  i32.const 1069547520
                  i32.store offset=60
                  local.get $l8
                  f32.const 0x1p+0 (;=1;)
                  local.get $p6
                  select
                  local.set $l10
                  br $B4
                end
                f32.const 0x1p+0 (;=1;)
                local.set $l10
                local.get $p6
                i32.eqz
                br_if $B4
                local.get $p2
                f32.const 0x1p+0 (;=1;)
                f32.gt
                if $I8
                  local.get $l7
                  i32.const 72
                  i32.add
                  local.tee $p5
                  local.get $p1
                  f32.const -0x1p-1 (;=-0.5;)
                  f32.mul
                  f32.const 0x1p+0 (;=1;)
                  f32.add
                  local.tee $p2
                  local.get $p5
                  f32.load
                  f32.mul
                  f32.store
                  local.get $l7
                  i32.const 68
                  i32.add
                  local.tee $p5
                  local.get $p2
                  local.get $p5
                  f32.load
                  f32.mul
                  f32.store
                  local.get $l7
                  local.get $p2
                  local.get $l7
                  f32.load offset=64
                  f32.mul
                  f32.store offset=64
                  local.get $l7
                  local.get $p2
                  local.get $l7
                  f32.load offset=80
                  f32.mul
                  f32.store offset=80
                  local.get $l7
                  i32.const 84
                  i32.add
                  local.tee $p5
                  local.get $p2
                  local.get $p5
                  f32.load
                  f32.mul
                  f32.store
                  local.get $l7
                  i32.const 88
                  i32.add
                  local.tee $p5
                  local.get $p2
                  local.get $p5
                  f32.load
                  f32.mul
                  f32.store
                  local.get $p0
                  f32.load offset=60
                  local.set $l12
                  local.get $l8
                  f32.const 0x1.8p-1 (;=0.75;)
                  f32.mul
                  f32.const 0x1.99999ap-6 (;=0.025;)
                  f32.add
                  f32.const 0x1.8cccccp-1 (;=0.775;)
                  local.get $p6
                  select
                  local.set $l8
                end
                local.get $l7
                f32.load offset=136
                local.set $p2
                local.get $p0
                local.get $l8
                f32.store offset=76
                local.get $p0
                i32.const 28
                i32.add
                local.set $p5
                local.get $p0
                i32.load16_u offset=28
                i32.const 1
                i32.and
                local.set $p6
                local.get $l12
                f32.const 0x0p+0 (;=0;)
                f32.ne
                br_if $B3
                local.get $l11
                local.get $p2
                f32.const 0x1p-2 (;=0.25;)
                f32.mul
                f32.lt
                i32.eqz
                br_if $B3
                local.get $l7
                local.get $p0
                f32.load
                f32.store
                local.get $l7
                local.get $p0
                f32.load offset=4
                f32.store offset=4
                local.get $l7
                local.get $p0
                f32.load offset=8
                f32.store offset=8
                local.get $l7
                local.get $p0
                f32.load offset=12
                f32.store offset=12
                local.get $l7
                local.get $p0
                f32.load offset=16
                f32.store offset=16
                local.get $l7
                local.get $p0
                f32.load offset=20
                f32.store offset=20
                local.get $l7
                local.get $p0
                f32.load offset=24
                f32.store offset=24
                i32.const 1
                i32.const 3
                local.get $p6
                select
                br $B2
              end
              local.get $p4
              if $I9
                f32.const 0x1p+0 (;=1;)
                local.set $p2
                block $B10
                  local.get $p6
                  i32.eqz
                  br_if $B10
                  local.get $l7
                  i32.load offset=152
                  local.tee $p6
                  i32.const 2
                  i32.lt_u
                  br_if $B10
                  f32.const 0x1p+0 (;=1;)
                  local.get $p6
                  f32.convert_i32_u
                  f32.div
                  local.set $p2
                end
                local.get $p0
                local.get $p2
                f32.store offset=76
              end
              i32.const 1
              local.get $l14
              f32.const 0x1.999998p-3 (;=0.2;)
              f32.lt
              local.get $p1
              local.get $l14
              f32.gt
              select
              i32.eqz
              br_if $B1
              local.get $l7
              f32.load offset=120
              local.set $l16
              local.get $l7
              f32.load offset=116
              local.set $l22
              local.get $p5
              f32.load offset=24
              local.set $l13
              local.get $p5
              f32.load offset=20
              local.set $l12
              local.get $l7
              f32.load offset=112
              local.set $l20
              local.get $l7
              f32.load
              local.set $l11
              local.get $p5
              f32.load offset=16
              local.set $l8
              local.get $l7
              f32.load offset=12
              local.set $p2
              local.get $l7
              f32.load offset=4
              local.set $l9
              local.get $l7
              f32.load offset=8
              local.set $l10
              local.get $p5
              f32.load offset=8
              local.set $l17
              local.get $p5
              f32.load offset=4
              local.set $l15
              local.get $p0
              local.get $p5
              f32.load
              local.get $p0
              f32.load offset=48
              f32.add
              local.tee $l21
              f32.store offset=48
              local.get $p0
              i32.const 52
              i32.add
              local.tee $p5
              local.get $l15
              local.get $p5
              f32.load
              f32.add
              local.tee $l15
              f32.store
              local.get $p0
              i32.const 56
              i32.add
              local.tee $p5
              local.get $l17
              local.get $p5
              f32.load
              f32.add
              local.tee $l17
              f32.store
              local.get $p0
              local.get $l11
              local.get $l11
              local.get $l8
              local.get $l8
              f32.add
              local.tee $l8
              f32.mul
              local.get $l9
              local.get $l12
              local.get $l12
              f32.add
              local.tee $l12
              f32.mul
              f32.add
              local.get $l10
              local.get $l13
              local.get $l13
              f32.add
              local.tee $l13
              f32.mul
              f32.add
              local.tee $l18
              f32.mul
              local.get $l8
              local.get $p2
              local.get $p2
              f32.mul
              f32.const -0x1p-1 (;=-0.5;)
              f32.add
              local.tee $l19
              f32.mul
              local.get $p2
              local.get $l13
              local.get $l9
              f32.mul
              local.get $l12
              local.get $l10
              f32.mul
              f32.sub
              f32.mul
              f32.sub
              f32.add
              local.get $p0
              f32.load offset=64
              f32.add
              local.tee $l23
              f32.store offset=64
              local.get $p0
              i32.const 68
              i32.add
              local.tee $p5
              local.get $l9
              local.get $l18
              f32.mul
              local.get $l12
              local.get $l19
              f32.mul
              local.get $p2
              local.get $l8
              local.get $l10
              f32.mul
              local.get $l13
              local.get $l11
              f32.mul
              f32.sub
              f32.mul
              f32.sub
              f32.add
              local.get $p5
              f32.load
              f32.add
              local.tee $l24
              f32.store
              local.get $p0
              i32.const 72
              i32.add
              local.tee $p5
              local.get $l13
              local.get $l19
              f32.mul
              local.get $p2
              local.get $l12
              local.get $l11
              f32.mul
              local.get $l8
              local.get $l9
              f32.mul
              f32.sub
              f32.mul
              f32.sub
              local.get $l10
              local.get $l18
              f32.mul
              f32.add
              local.get $p5
              f32.load
              f32.add
              local.tee $p2
              f32.store
              local.get $l21
              local.get $l21
              f32.mul
              local.get $l15
              local.get $l15
              f32.mul
              f32.add
              local.get $l17
              local.get $l17
              f32.mul
              f32.add
              f32.const 0x1p+0 (;=1;)
              local.get $l20
              f32.div
              f32.const 0x1p+0 (;=1;)
              local.get $l20
              f32.const 0x0p+0 (;=0;)
              f32.gt
              select
              local.get $l23
              local.get $l23
              f32.mul
              f32.mul
              f32.const 0x1p+0 (;=1;)
              local.get $l22
              f32.div
              f32.const 0x1p+0 (;=1;)
              local.get $l22
              f32.const 0x0p+0 (;=0;)
              f32.gt
              select
              local.get $l24
              local.get $l24
              f32.mul
              f32.mul
              f32.add
              f32.const 0x1p+0 (;=1;)
              local.get $l16
              f32.div
              f32.const 0x1p+0 (;=1;)
              local.get $l16
              f32.const 0x0p+0 (;=0;)
              f32.gt
              select
              local.get $p2
              local.get $p2
              f32.mul
              f32.mul
              f32.add
              f32.const 0x1p+0 (;=1;)
              local.get $l7
              f32.load offset=124
              local.tee $p2
              local.get $p2
              f32.const 0x0p+0 (;=0;)
              f32.eq
              select
              f32.mul
              f32.add
              f32.const 0x1p-1 (;=0.5;)
              f32.mul
              local.tee $l9
              local.get $l7
              f32.load offset=132
              local.get $l7
              i32.load offset=148
              i32.const 1
              i32.add
              f32.convert_i32_u
              local.tee $l11
              f32.mul
              local.tee $p2
              f32.ge
              i32.eqz
              br_if $B1
              local.get $p0
              i32.const 0
              i32.store offset=72
              local.get $p0
              i64.const 0
              i64.store offset=64 align=4
              local.get $p0
              i32.const 0
              i32.store offset=56
              local.get $p0
              i64.const 0
              i64.store offset=48 align=4
              f32.const 0x1.999998p-2 (;=0.4;)
              local.set $l10
              local.get $l7
              local.get $l11
              f32.const -0x1p+0 (;=-1;)
              f32.add
              local.get $p1
              f32.mul
              local.get $p2
              f32.const 0x0p+0 (;=0;)
              f32.ne
              if $I11 (result f32)
                local.get $l9
                local.get $p2
                f32.div
                local.tee $p2
                f32.const 0x1p+1 (;=2;)
                local.get $p2
                f32.const 0x1p+1 (;=2;)
                f32.lt
                select
                f32.const 0x1p-1 (;=0.5;)
                f32.mul
                f32.const 0x1.999998p-2 (;=0.4;)
                f32.mul
              else
                local.get $l10
              end
              f32.add
              local.tee $p1
              f32.store offset=144
              local.get $p0
              local.get $l14
              f32.const 0x0p+0 (;=0;)
              f32.eq
              i32.const 3
              i32.shl
              i32.store16 offset=28
              local.get $p1
              return
            end
            local.get $p0
            local.get $l10
            f32.store offset=76
            local.get $p0
            i32.const 28
            i32.add
            local.set $p5
            local.get $p0
            i32.load16_u offset=28
            i32.const 1
            i32.and
            local.set $p6
          end
          local.get $p6
          i32.const 2
          i32.shl
        end
        local.set $p6
        local.get $p5
        local.get $p6
        i32.store16
        i32.const 1
        local.get $l14
        f32.const 0x1.999998p-3 (;=0.2;)
        f32.lt
        local.get $p1
        local.get $l14
        f32.gt
        select
        i32.eqz
        br_if $B1
        local.get $p0
        local.get $l20
        local.get $p0
        f32.load offset=48
        f32.add
        local.tee $p2
        f32.store offset=48
        local.get $p0
        local.get $l18
        local.get $p0
        f32.load offset=64
        f32.add
        local.tee $l10
        f32.store offset=64
        local.get $p0
        i32.const 52
        i32.add
        local.tee $p6
        local.get $l21
        local.get $p6
        f32.load
        f32.add
        local.tee $l8
        f32.store
        local.get $p0
        i32.const 56
        i32.add
        local.tee $p6
        local.get $l15
        local.get $p6
        f32.load
        f32.add
        local.tee $l12
        f32.store
        local.get $p0
        i32.const 68
        i32.add
        local.tee $p6
        local.get $l9
        local.get $p6
        f32.load
        f32.add
        local.tee $l9
        f32.store
        local.get $p0
        i32.const 72
        i32.add
        local.tee $p6
        local.get $l17
        local.get $p6
        f32.load
        f32.add
        local.tee $l13
        f32.store
        local.get $l11
        local.get $l7
        f32.load offset=132
        local.tee $l16
        f32.ge
        i32.eqz
        br_if $B1
        local.get $p2
        local.get $p2
        f32.mul
        local.get $l8
        local.get $l8
        f32.mul
        f32.add
        local.get $l12
        local.get $l12
        f32.mul
        f32.add
        local.get $l23
        local.get $l25
        local.get $l10
        local.get $l10
        f32.mul
        f32.mul
        local.get $l19
        local.get $l9
        local.get $l9
        f32.mul
        f32.mul
        f32.add
        local.get $l24
        local.get $l13
        local.get $l13
        f32.mul
        f32.mul
        f32.add
        f32.mul
        f32.add
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        local.tee $l11
        local.get $l16
        local.get $l7
        i32.load offset=148
        i32.const 1
        i32.add
        f32.convert_i32_u
        local.tee $p2
        f32.mul
        local.tee $l9
        f32.ge
        i32.eqz
        br_if $B1
        local.get $p0
        i32.const 0
        i32.store offset=72
        local.get $p0
        i64.const 0
        i64.store offset=64 align=4
        local.get $p0
        i32.const 0
        i32.store offset=56
        local.get $p0
        i64.const 0
        i64.store offset=48 align=4
        f32.const 0x1.999998p-2 (;=0.4;)
        local.set $l10
        local.get $l7
        local.get $p2
        f32.const -0x1p+0 (;=-1;)
        f32.add
        local.get $p1
        f32.mul
        local.get $l7
        f32.load offset=132
        f32.const 0x0p+0 (;=0;)
        f32.ne
        if $I12 (result f32)
          local.get $l11
          local.get $l9
          f32.div
          local.tee $l11
          f32.const 0x1p+1 (;=2;)
          local.get $l11
          f32.const 0x1p+1 (;=2;)
          f32.lt
          select
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          f32.const 0x1.999998p-2 (;=0.4;)
          f32.mul
        else
          local.get $l10
        end
        f32.add
        local.tee $p1
        f32.store offset=144
        local.get $l14
        f32.const 0x0p+0 (;=0;)
        f32.ne
        br_if $B0
        local.get $p5
        local.get $p5
        i32.load16_u
        i32.const 8
        i32.or
        i32.store16
        local.get $p1
        return
      end
      local.get $l7
      local.get $l14
      local.get $p1
      f32.sub
      local.tee $p1
      f32.const 0x0p+0 (;=0;)
      local.get $p1
      f32.const 0x0p+0 (;=0;)
      f32.gt
      select
      local.tee $p1
      f32.store offset=144
    end
    local.get $p1)
