  (func $f70073 (type $t489) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 i32) (param $p7 i32) (param $p8 i32) (param $p9 i32) (param $p10 i32) (param $p11 i32) (param $p12 i32) (param $p13 i32) (param $p14 f32) (result i32)
    (local $l15 i32) (local $l16 i32) (local $l17 i32) (local $l18 i32) (local $l19 i32) (local $l20 i32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32)
    global.get $g0
    i32.const 384
    i32.sub
    local.tee $l15
    global.set $g0
    block $B0
      local.get $p5
      i32.eqz
      br_if $B0
      local.get $p7
      i32.load8_u offset=64
      local.tee $l16
      if $I1 (result f32)
        i32.const 1
        local.set $l17
        local.get $p7
        i32.load offset=76
        local.tee $l19
        f32.load offset=40
        local.set $l21
        local.get $l19
        f32.load offset=36
        local.set $l22
        local.get $l19
        f32.load offset=32
        local.set $l23
        block $B2
          local.get $l16
          i32.const 1
          i32.eq
          br_if $B2
          local.get $l16
          i32.const 1
          i32.sub
          local.tee $l18
          i32.const 1
          i32.and
          local.set $l20
          local.get $l16
          i32.const 2
          i32.ne
          if $I3
            local.get $l18
            i32.const -2
            i32.and
            local.set $l18
            loop $L4
              local.get $l23
              local.get $l19
              local.get $l17
              i32.const 48
              i32.mul
              i32.add
              local.tee $l16
              f32.load offset=32
              f32.add
              local.get $l16
              f32.load offset=80
              f32.add
              local.set $l23
              local.get $l21
              local.get $l16
              f32.load offset=40
              f32.add
              local.get $l16
              f32.load offset=88
              f32.add
              local.set $l21
              local.get $l22
              local.get $l16
              f32.load offset=36
              f32.add
              local.get $l16
              f32.load offset=84
              f32.add
              local.set $l22
              local.get $l17
              i32.const 2
              i32.add
              local.set $l17
              local.get $l18
              i32.const 2
              i32.sub
              local.tee $l18
              br_if $L4
            end
          end
          local.get $l20
          i32.eqz
          br_if $B2
          local.get $l23
          local.get $l19
          local.get $l17
          i32.const 48
          i32.mul
          i32.add
          local.tee $l16
          f32.load offset=32
          f32.add
          local.set $l23
          local.get $l22
          local.get $l16
          f32.load offset=36
          f32.add
          local.set $l22
          local.get $l21
          local.get $l16
          f32.load offset=40
          f32.add
          local.set $l21
        end
        local.get $l21
        f32.const 0x1p+0 (;=1;)
        local.get $l23
        local.get $l23
        f32.mul
        local.get $l22
        local.get $l22
        f32.mul
        f32.add
        local.get $l21
        local.get $l21
        f32.mul
        f32.add
        f32.sqrt
        f32.div
        local.tee $l25
        f32.mul
        local.set $l26
        local.get $l22
        local.get $l25
        f32.mul
        local.set $l27
        local.get $l23
        local.get $l25
        f32.mul
      else
        f32.const 0x0p+0 (;=0;)
      end
      local.set $l25
      local.get $p10
      f32.load
      local.set $l21
      local.get $l15
      local.get $p14
      f32.store offset=32
      local.get $l15
      local.get $l21
      f32.const 0x1.99999ap-5 (;=0.05;)
      f32.mul
      f32.store offset=48
      local.get $l15
      local.get $l15
      i64.load offset=56
      i64.store offset=24
      local.get $l15
      local.get $l15
      i64.load offset=40
      i64.store offset=8
      local.get $l15
      local.get $l15
      i64.load offset=32
      i64.store
      local.get $l15
      local.get $l15
      i64.load offset=48
      i64.store offset=16
      local.get $p0
      local.get $p1
      local.get $p4
      local.get $p5
      local.get $p8
      local.get $l15
      i32.const 16
      i32.add
      local.get $l15
      local.get $p6
      local.get $p7
      call $f70081
      local.set $l18
      block $B5
        block $B6
          local.get $l25
          local.get $p6
          f32.load offset=32
          local.tee $l28
          f32.mul
          local.get $l27
          local.get $p6
          f32.load offset=36
          local.tee $l29
          f32.mul
          f32.add
          local.get $l26
          local.get $p6
          f32.load offset=40
          local.tee $l24
          f32.mul
          f32.add
          f32.const 0x1.6a09e6p-1 (;=0.707107;)
          f32.lt
          br_if $B6
          local.get $p7
          i32.load8_u offset=64
          local.get $p9
          i32.lt_u
          br_if $B6
          local.get $l18
          i32.eqz
          br_if $B5
        end
        local.get $p1
        i32.load offset=4
        local.set $l16
        local.get $p0
        i32.load offset=4
        local.tee $l17
        local.get $p12
        local.get $l15
        i32.const 304
        i32.add
        call $f70029
        local.get $l16
        local.get $p13
        local.get $l15
        i32.const 232
        i32.add
        call $f70029
        local.get $l15
        local.get $p12
        i32.store8 offset=204
        local.get $l15
        local.get $l17
        i32.const 96
        i32.add
        i32.store offset=200
        local.get $l15
        local.get $l17
        i32.const 48
        i32.add
        i32.store offset=196
        local.get $l15
        local.get $p2
        i32.store offset=192
        local.get $l15
        local.get $l17
        i32.store offset=208
        local.get $l15
        i32.const 3125832
        i32.const 3125860
        local.get $p12
        select
        i32.store offset=160
        local.get $l15
        local.get $p13
        i32.store8 offset=140
        local.get $l15
        local.get $l16
        i32.const 96
        i32.add
        i32.store offset=136
        local.get $l15
        local.get $l16
        i32.const 48
        i32.add
        i32.store offset=132
        local.get $l15
        local.get $p3
        i32.store offset=128
        local.get $l15
        local.get $l16
        i32.store offset=144
        local.get $l15
        i32.const 3125832
        i32.const 3125860
        local.get $p13
        select
        i32.store offset=96
        local.get $l15
        i32.const 0
        i32.store offset=92
        local.get $l15
        i32.const 304
        i32.add
        local.get $l15
        i32.const 232
        i32.add
        local.get $l15
        i32.const 160
        i32.add
        local.get $l15
        i32.const 96
        i32.add
        local.get $p8
        local.get $l15
        i32.const 92
        i32.add
        local.get $p11
        local.get $p6
        i32.const 32
        i32.add
        local.get $p6
        local.get $p6
        i32.const 16
        i32.add
        local.get $l17
        f32.load offset=16
        local.get $l16
        f32.load offset=16
        local.get $l18
        local.get $p14
        call $f70077
        local.tee $l16
        i32.eqz
        br_if $B0
        local.get $l15
        i32.load offset=92
        local.tee $l17
        if $I7
          local.get $p7
          local.get $p8
          local.get $l17
          local.get $p14
          call $f69971
          local.get $l15
          i32.const -64
          i32.sub
          local.get $p7
          local.get $p3
          call $f70047
          local.get $p7
          local.get $p8
          local.get $l15
          i32.const -64
          i32.sub
          local.get $p3
          local.get $p11
          call $f69970
          br $B0
        end
        local.get $l18
        br_if $B0
        local.get $l15
        i32.const -64
        i32.sub
        local.get $p7
        local.get $p3
        call $f70047
        local.get $p7
        local.get $p8
        local.get $l15
        i32.const -64
        i32.sub
        local.get $p3
        local.get $p11
        call $f69970
        br $B0
      end
      local.get $p3
      f32.load offset=4
      local.set $l22
      local.get $p3
      f32.load offset=8
      local.set $l23
      local.get $p3
      f32.load
      local.set $p14
      local.get $p3
      f32.load offset=12
      local.set $l21
      local.get $l15
      i32.const 0
      i32.store offset=316
      local.get $l15
      local.get $l23
      local.get $p14
      local.get $l25
      local.get $l28
      f32.add
      local.tee $l25
      f32.mul
      local.get $l22
      local.get $l27
      local.get $l29
      f32.add
      local.tee $l27
      f32.mul
      f32.add
      local.get $l23
      local.get $l26
      local.get $l24
      f32.add
      local.tee $l26
      f32.mul
      f32.add
      local.tee $l28
      f32.mul
      local.get $l21
      local.get $l27
      local.get $p14
      f32.mul
      local.get $l25
      local.get $l22
      f32.mul
      f32.sub
      f32.mul
      local.get $l26
      local.get $l21
      local.get $l21
      f32.mul
      f32.const -0x1p-1 (;=-0.5;)
      f32.add
      local.tee $l29
      f32.mul
      f32.add
      f32.add
      local.tee $l24
      local.get $l24
      f32.add
      local.tee $l24
      f32.const 0x1p+0 (;=1;)
      local.get $l24
      local.get $l24
      f32.mul
      local.get $p14
      local.get $l28
      f32.mul
      local.get $l21
      local.get $l26
      local.get $l22
      f32.mul
      local.get $l27
      local.get $l23
      f32.mul
      f32.sub
      f32.mul
      local.get $l25
      local.get $l29
      f32.mul
      f32.add
      f32.add
      local.tee $l24
      local.get $l24
      f32.add
      local.tee $l24
      local.get $l24
      f32.mul
      local.get $l22
      local.get $l28
      f32.mul
      local.get $l21
      local.get $l25
      local.get $l23
      f32.mul
      local.get $l26
      local.get $p14
      f32.mul
      f32.sub
      f32.mul
      local.get $l27
      local.get $l29
      f32.mul
      f32.add
      f32.add
      local.tee $l21
      local.get $l21
      f32.add
      local.tee $l21
      local.get $l21
      f32.mul
      f32.add
      f32.add
      f32.sqrt
      f32.div
      local.tee $l22
      f32.mul
      f32.store offset=312
      local.get $l15
      local.get $l21
      local.get $l22
      f32.mul
      f32.store offset=308
      local.get $l15
      local.get $l24
      local.get $l22
      f32.mul
      f32.store offset=304
      local.get $p7
      local.get $p8
      local.get $l15
      i32.const 304
      i32.add
      local.get $p3
      local.get $p11
      call $f69970
      i32.const 1
      local.set $l16
    end
    local.get $l15
    i32.const 384
    i32.add
    global.set $g0
    local.get $l16)