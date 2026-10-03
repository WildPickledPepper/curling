  (func $f69975 (type $t6) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32)
    (local $l5 f32) (local $l6 f32) (local $l7 f32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 i32) (local $l17 i32) (local $l18 i32) (local $l19 i32) (local $l20 i32) (local $l21 i32) (local $l22 i32) (local $l23 i32)
    global.get $g0
    i32.const 48
    i32.sub
    local.tee $l16
    local.set $l19
    local.get $l16
    global.set $g0
    local.get $l16
    local.get $p3
    i32.const 15
    i32.add
    i32.const -16
    i32.and
    i32.sub
    local.tee $l16
    global.set $g0
    local.get $l16
    i32.const 0
    local.get $p3
    call $f484
    local.set $l21
    f32.const -0x1.fffffep+127 (;=-3.40282e+38;)
    local.set $l5
    i32.const -1
    local.set $l17
    local.get $p4
    local.set $l18
    loop $L0
      local.get $l18
      i32.load offset=48
      local.tee $p3
      local.get $l18
      i32.load offset=52
      local.tee $l20
      i32.lt_u
      if $I1
        loop $L2
          local.get $p2
          local.get $p3
          i32.const 6
          i32.shl
          i32.add
          local.tee $l16
          f32.load offset=16
          local.tee $l6
          local.get $l6
          f32.mul
          local.get $l16
          f32.load offset=20
          local.tee $l6
          local.get $l6
          f32.mul
          f32.add
          local.get $l16
          f32.load offset=24
          local.tee $l6
          local.get $l6
          f32.mul
          f32.add
          local.tee $l6
          local.get $l5
          local.get $l5
          local.get $l6
          f32.lt
          local.tee $l16
          select
          local.set $l5
          local.get $p3
          local.get $l17
          local.get $l16
          select
          local.set $l17
          local.get $p3
          i32.const 1
          i32.add
          local.tee $p3
          local.get $l20
          i32.ne
          br_if $L2
        end
      end
      local.get $l18
      i32.load offset=16
      local.tee $l18
      br_if $L0
    end
    local.get $l17
    local.get $l21
    i32.add
    i32.const 1
    i32.store8
    local.get $p2
    local.get $l17
    i32.const 6
    i32.shl
    i32.add
    local.tee $l16
    i32.const 24
    i32.add
    local.tee $p3
    f32.load
    local.set $l10
    local.get $l16
    f32.load offset=20
    local.set $l13
    local.get $l16
    i32.const 16
    i32.add
    local.tee $l17
    f32.load
    local.set $l14
    local.get $p1
    local.get $l16
    i32.load offset=48
    i32.store offset=48
    local.get $p1
    local.get $l16
    i64.load offset=40
    i64.store offset=40
    local.get $p1
    local.get $l16
    i64.load offset=32
    i64.store offset=32
    local.get $p1
    local.get $p3
    i64.load
    i64.store offset=24
    local.get $p1
    local.get $l17
    i64.load
    i64.store offset=16
    local.get $p1
    local.get $l16
    i64.load offset=8
    i64.store offset=8
    local.get $p1
    local.get $l16
    i64.load
    i64.store
    local.get $p2
    local.get $p4
    i32.load offset=48
    local.tee $p3
    i32.const 6
    i32.shl
    i32.add
    local.tee $l17
    f32.load offset=16
    local.get $l14
    f32.sub
    local.tee $l5
    local.get $l5
    f32.mul
    local.get $l17
    f32.load offset=20
    local.get $l13
    f32.sub
    local.tee $l5
    local.get $l5
    f32.mul
    f32.add
    local.get $l17
    f32.load offset=24
    local.get $l10
    f32.sub
    local.tee $l5
    local.get $l5
    f32.mul
    f32.add
    local.set $l5
    local.get $l16
    f32.load offset=44
    local.set $l11
    local.get $p3
    local.set $l17
    local.get $p4
    local.set $l18
    loop $L3
      local.get $l18
      i32.load offset=52
      local.tee $l20
      local.get $p3
      i32.gt_u
      if $I4
        loop $L5
          local.get $p2
          local.get $p3
          i32.const 6
          i32.shl
          i32.add
          local.tee $l16
          f32.load offset=16
          local.get $l14
          f32.sub
          local.tee $l6
          local.get $l6
          f32.mul
          local.get $l16
          f32.load offset=20
          local.get $l13
          f32.sub
          local.tee $l6
          local.get $l6
          f32.mul
          f32.add
          local.get $l16
          f32.load offset=24
          local.get $l10
          f32.sub
          local.tee $l6
          local.get $l6
          f32.mul
          f32.add
          local.tee $l6
          local.get $l5
          local.get $l5
          local.get $l6
          f32.lt
          local.tee $l16
          select
          local.set $l5
          local.get $p3
          local.get $l17
          local.get $l16
          select
          local.set $l17
          local.get $p3
          i32.const 1
          i32.add
          local.tee $p3
          local.get $l20
          i32.ne
          br_if $L5
        end
      end
      local.get $l18
      i32.load offset=16
      local.tee $l18
      if $I6
        local.get $l18
        i32.load offset=48
        local.set $p3
        br $L3
      end
    end
    local.get $l17
    local.get $l21
    i32.add
    i32.const 1
    i32.store8
    local.get $p2
    local.get $l17
    i32.const 6
    i32.shl
    i32.add
    local.tee $p3
    i32.const 16
    i32.add
    local.tee $l16
    f32.load
    local.set $l5
    local.get $p3
    f32.load offset=20
    local.set $l6
    local.get $p3
    i32.const 24
    i32.add
    local.tee $l17
    f32.load
    local.set $l8
    local.get $p1
    local.get $p3
    i32.load offset=48
    i32.store offset=112
    local.get $p1
    local.get $p3
    i64.load offset=40
    i64.store offset=104
    local.get $p1
    local.get $p3
    i64.load offset=32
    i64.store offset=96
    local.get $p1
    local.get $l17
    i64.load
    i64.store offset=88
    local.get $p1
    local.get $l16
    i64.load
    i64.store offset=80
    local.get $p1
    local.get $p3
    i64.load offset=8
    i64.store offset=72
    local.get $p1
    local.get $p3
    i64.load
    i64.store offset=64
    local.get $l5
    local.get $l14
    f32.sub
    local.tee $l7
    local.get $p1
    f32.load offset=36
    local.tee $l5
    f32.mul
    local.get $l6
    local.get $l13
    f32.sub
    local.tee $l12
    local.get $p1
    f32.load offset=32
    local.tee $l6
    f32.mul
    f32.sub
    local.tee $l9
    f32.const 0x1p+0 (;=1;)
    local.get $l9
    local.get $l9
    f32.mul
    local.get $l12
    local.get $p1
    f32.load offset=40
    local.tee $l9
    f32.mul
    local.get $l8
    local.get $l10
    f32.sub
    local.tee $l8
    local.get $l5
    f32.mul
    f32.sub
    local.tee $l12
    local.get $l12
    f32.mul
    local.get $l8
    local.get $l6
    f32.mul
    local.get $l7
    local.get $l9
    f32.mul
    f32.sub
    local.tee $l8
    local.get $l8
    f32.mul
    f32.add
    f32.add
    local.tee $l15
    f32.sqrt
    f32.div
    local.tee $l7
    f32.mul
    local.get $l9
    local.get $l15
    f32.const 0x0p+0 (;=0;)
    f32.gt
    local.tee $l16
    select
    local.set $l9
    local.get $l8
    local.get $l7
    f32.mul
    local.get $l5
    local.get $l16
    select
    local.set $l8
    local.get $l12
    local.get $l7
    f32.mul
    local.get $l6
    local.get $l16
    select
    local.set $l12
    local.get $p3
    f32.load offset=44
    local.tee $l5
    local.get $l11
    local.get $l5
    local.get $l11
    f32.lt
    select
    local.set $l7
    f32.const 0x1.fffffep+127 (;=3.40282e+38;)
    local.set $l6
    f32.const -0x1.fffffep+127 (;=-3.40282e+38;)
    local.set $l11
    i32.const -1
    local.set $l18
    i32.const -1
    local.set $l16
    local.get $p4
    local.set $l22
    loop $L7
      local.get $l22
      i32.load offset=48
      local.tee $p3
      local.get $l22
      i32.load offset=52
      local.tee $l20
      i32.lt_u
      if $I8
        loop $L9
          local.get $p3
          local.get $l21
          i32.add
          i32.load8_u
          i32.eqz
          if $I10
            local.get $l12
            local.get $p2
            local.get $p3
            i32.const 6
            i32.shl
            i32.add
            local.tee $l17
            f32.load offset=16
            local.get $l14
            f32.sub
            f32.mul
            local.get $l8
            local.get $l17
            f32.load offset=20
            local.get $l13
            f32.sub
            f32.mul
            f32.add
            local.get $l9
            local.get $l17
            f32.load offset=24
            local.get $l10
            f32.sub
            f32.mul
            f32.add
            local.tee $l5
            local.get $l6
            local.get $l5
            local.get $l6
            f32.lt
            local.tee $l17
            select
            local.set $l6
            local.get $l5
            local.get $l11
            local.get $l5
            local.get $l11
            f32.gt
            local.tee $l23
            select
            local.set $l11
            local.get $p3
            local.get $l16
            local.get $l17
            select
            local.set $l16
            local.get $p3
            local.get $l18
            local.get $l23
            select
            local.set $l18
          end
          local.get $p3
          i32.const 1
          i32.add
          local.tee $p3
          local.get $l20
          i32.ne
          br_if $L9
        end
      end
      local.get $l22
      i32.load offset=16
      local.tee $l22
      br_if $L7
    end
    local.get $l18
    local.get $l21
    i32.add
    i32.const 1
    i32.store8
    local.get $p1
    local.get $p2
    local.get $l18
    i32.const 6
    i32.shl
    i32.add
    local.tee $p3
    i64.load
    i64.store offset=128
    local.get $p1
    local.get $p3
    i32.load offset=48
    i32.store offset=176
    local.get $p1
    local.get $p3
    i64.load offset=40
    i64.store offset=168
    local.get $p1
    local.get $p3
    i64.load offset=32
    i64.store offset=160
    local.get $p1
    local.get $p3
    i64.load offset=24
    i64.store offset=152
    local.get $p1
    local.get $p3
    i64.load offset=16
    i64.store offset=144
    local.get $p1
    local.get $p3
    i64.load offset=8
    i64.store offset=136
    local.get $p0
    local.get $p3
    f32.load offset=44
    local.tee $l5
    local.get $l7
    local.get $l5
    local.get $l7
    f32.lt
    select
    local.tee $l7
    f32.store
    local.get $l6
    local.get $l11
    f32.mul
    f32.const 0x0p+0 (;=0;)
    f32.gt
    if $I11
      f32.const -0x1.fffffep+127 (;=-3.40282e+38;)
      local.set $l5
      local.get $p4
      local.set $l18
      loop $L12
        local.get $l18
        i32.load offset=48
        local.tee $p3
        local.get $l18
        i32.load offset=52
        local.tee $l20
        i32.lt_u
        if $I13
          loop $L14
            local.get $p3
            local.get $l21
            i32.add
            i32.load8_u
            i32.eqz
            if $I15
              local.get $l12
              local.get $p2
              local.get $p3
              i32.const 6
              i32.shl
              i32.add
              local.tee $l17
              f32.load offset=16
              local.get $l14
              f32.sub
              f32.mul
              local.get $l8
              local.get $l17
              f32.load offset=20
              local.get $l13
              f32.sub
              f32.mul
              f32.add
              local.get $l9
              local.get $l17
              f32.load offset=24
              local.get $l10
              f32.sub
              f32.mul
              f32.add
              local.tee $l6
              local.get $l5
              local.get $l5
              local.get $l6
              f32.lt
              local.tee $l17
              select
              local.set $l5
              local.get $p3
              local.get $l16
              local.get $l17
              select
              local.set $l16
            end
            local.get $p3
            i32.const 1
            i32.add
            local.tee $p3
            local.get $l20
            i32.ne
            br_if $L14
          end
        end
        local.get $l18
        i32.load offset=16
        local.tee $l18
        br_if $L12
      end
    end
    local.get $l16
    local.get $l21
    i32.add
    i32.const 1
    i32.store8
    local.get $p1
    local.get $p2
    local.get $l16
    i32.const 6
    i32.shl
    i32.add
    local.tee $p3
    i64.load
    i64.store offset=192
    local.get $p1
    local.get $p3
    i32.load offset=48
    i32.store offset=240
    local.get $p1
    local.get $p3
    i64.load offset=40
    i64.store offset=232
    local.get $p1
    local.get $p3
    i64.load offset=32
    i64.store offset=224
    local.get $p1
    local.get $p3
    i64.load offset=24
    i64.store offset=216
    local.get $p1
    local.get $p3
    i64.load offset=16
    i64.store offset=208
    local.get $p1
    local.get $p3
    i64.load offset=8
    i64.store offset=200
    local.get $p3
    f32.load offset=44
    local.set $l5
    local.get $l19
    i32.const 2139095039
    i32.store offset=32
    local.get $l19
    i32.const 2139095039
    i32.store offset=16
    local.get $l19
    i64.const 0
    i64.store offset=8
    local.get $l5
    local.get $l7
    local.get $l5
    local.get $l7
    f32.lt
    select
    local.set $l6
    local.get $l19
    i32.const 32
    i32.add
    local.set $l23
    local.get $l19
    i32.const 8
    i32.add
    i32.const 4
    i32.or
    local.set $l22
    loop $L16
      local.get $p4
      i32.load offset=48
      local.tee $p3
      local.get $p4
      i32.load offset=52
      local.tee $l16
      i32.lt_u
      if $I17
        loop $L18
          block $B19
            local.get $p3
            local.get $l21
            i32.add
            i32.load8_u
            br_if $B19
            block $B20 (result i32)
              local.get $p2
              local.get $p3
              i32.const 6
              i32.shl
              i32.add
              f32.load offset=44
              local.tee $l5
              local.get $l19
              f32.load offset=16
              f32.lt
              if $I21
                local.get $l19
                i32.load offset=8
                local.set $l17
                local.get $l23
                local.get $l19
                i64.load offset=16
                i64.store
                local.get $l23
                local.get $l19
                i64.load offset=24
                i64.store offset=8
                local.get $l19
                i32.const 8
                i32.add
                local.set $l20
                local.get $l19
                i32.const 16
                i32.add
                br $B20
              end
              local.get $l19
              f32.load offset=32
              local.get $l5
              f32.gt
              i32.eqz
              br_if $B19
              local.get $l19
              i32.load offset=12
              local.set $l17
              local.get $l22
              local.set $l20
              local.get $l23
            end
            local.set $l18
            local.get $l19
            local.get $l17
            i32.store offset=12
            local.get $l18
            local.get $l5
            f32.store
            local.get $l20
            local.get $p3
            i32.store
          end
          local.get $p3
          i32.const 1
          i32.add
          local.tee $p3
          local.get $l16
          i32.lt_u
          br_if $L18
        end
      end
      local.get $p4
      i32.load offset=16
      local.tee $p4
      br_if $L16
    end
    local.get $p1
    local.get $p2
    local.get $l19
    i32.load offset=8
    i32.const 6
    i32.shl
    i32.add
    local.tee $p3
    i64.load
    i64.store offset=256
    local.get $p1
    local.get $p3
    i32.load offset=48
    i32.store offset=304
    local.get $p1
    local.get $p3
    i64.load offset=40
    i64.store offset=296
    local.get $p1
    local.get $p3
    i64.load offset=32
    i64.store offset=288
    local.get $p1
    local.get $p3
    i64.load offset=24
    i64.store offset=280
    local.get $p1
    local.get $p3
    i64.load offset=16
    i64.store offset=272
    local.get $p1
    local.get $p3
    i64.load offset=8
    i64.store offset=264
    local.get $l19
    f32.load offset=16
    local.set $l5
    local.get $p1
    local.get $p2
    local.get $l19
    i32.load offset=12
    i32.const 6
    i32.shl
    i32.add
    local.tee $p3
    i64.load
    i64.store offset=320
    local.get $p1
    local.get $p3
    i64.load offset=16
    i64.store offset=336
    local.get $p1
    local.get $p3
    i64.load offset=32
    i64.store offset=352
    local.get $p1
    local.get $p3
    i32.load offset=48
    i32.store offset=368
    local.get $p1
    local.get $p3
    i64.load offset=40
    i64.store offset=360
    local.get $p1
    local.get $p3
    i64.load offset=24
    i64.store offset=344
    local.get $p1
    local.get $p3
    i64.load offset=8
    i64.store offset=328
    local.get $p0
    local.get $l19
    f32.load offset=32
    local.tee $l10
    local.get $l5
    local.get $l6
    local.get $l5
    local.get $l6
    f32.lt
    select
    local.tee $l5
    local.get $l5
    local.get $l10
    f32.gt
    select
    f32.store
    local.get $l19
    i32.const 48
    i32.add
    global.set $g0)
