  (func $f71751 (type $t3) (param $p0 i32) (param $p1 i32) (param $p2 i32) (result i32)
    (local $l3 f32) (local $l4 f32) (local $l5 f32) (local $l6 f32) (local $l7 f32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 i32) (local $l17 i32) (local $l18 i32) (local $l19 i32) (local $l20 i32) (local $l21 i32) (local $l22 i32) (local $l23 i32) (local $l24 i32) (local $l25 i32) (local $l26 i32) (local $l27 i32) (local $l28 i32) (local $l29 i32) (local $l30 i32) (local $l31 i32) (local $l32 i32) (local $l33 i64)
    global.get $g0
    i32.const 208
    i32.sub
    local.tee $l14
    global.set $g0
    block $B0
      block $B1
        local.get $p0
        i32.load offset=4
        local.tee $l13
        i32.eqz
        br_if $B1
        block $B2
          block $B3
            block $B4
              block $B5
                block $B6
                  local.get $p1
                  i32.load16_u offset=98
                  br_table $B4 $B1 $B5 $B6 $B3 $B1
                end
                local.get $p1
                i32.load16_u offset=96
                i32.eqz
                br_if $B2
                local.get $l14
                i32.const 16
                i32.add
                local.get $p1
                i32.const 48
                i32.add
                local.get $p1
                i32.const 12
                i32.add
                local.get $p1
                call $f71850
                local.set $l13
                local.get $p0
                i32.load offset=296
                local.get $p0
                i32.load offset=292
                local.get $p0
                i32.load offset=4
                local.get $l13
                local.get $p2
                call $f71871
                br_if $B1
                br $B0
              end
              local.get $p1
              f32.load offset=60
              local.set $l10
              local.get $p1
              f32.load offset=124
              local.set $l11
              local.get $p1
              f32.load offset=112
              local.set $l6
              local.get $p1
              f32.load offset=116
              local.set $l7
              local.get $p1
              f32.load offset=120
              local.set $l8
              local.get $l14
              i32.const 0
              i32.store offset=28
              local.get $l14
              local.get $l8
              f32.store offset=24
              local.get $l14
              local.get $l7
              f32.store offset=20
              local.get $l14
              local.get $l6
              f32.store offset=16
              local.get $p1
              f32.load offset=16
              local.set $l3
              local.get $p1
              f32.load offset=20
              local.set $l5
              local.get $p1
              f32.load offset=12
              local.set $l4
              local.get $l14
              i32.const 0
              i32.store offset=108
              local.get $l14
              i32.const 0
              i32.store offset=92
              local.get $l14
              i32.const 0
              i32.store offset=76
              local.get $l14
              local.get $l11
              f32.const 0x1.028f5cp+0 (;=1.01;)
              f32.mul
              local.tee $l11
              f32.store offset=72
              local.get $l14
              local.get $l11
              f32.store offset=68
              local.get $l14
              i32.const 0
              i32.store offset=60
              local.get $l14
              local.get $l4
              f32.store offset=56
              local.get $l14
              local.get $l5
              f32.store offset=52
              local.get $l14
              i32.const 0
              i32.store offset=44
              local.get $l14
              local.get $l5
              f32.store offset=40
              local.get $l14
              local.get $l3
              f32.store offset=36
              local.get $l14
              local.get $l4
              local.get $l4
              f32.neg
              local.tee $l12
              local.get $l4
              local.get $l12
              f32.gt
              select
              local.tee $l12
              f32.store offset=104
              local.get $l14
              local.get $l5
              local.get $l5
              f32.neg
              local.tee $l9
              local.get $l5
              local.get $l9
              f32.gt
              select
              local.tee $l9
              f32.store offset=100
              local.get $l14
              local.get $l9
              f32.store offset=88
              local.get $l14
              local.get $l3
              local.get $l3
              f32.neg
              local.tee $l9
              local.get $l3
              local.get $l9
              f32.gt
              select
              local.tee $l9
              f32.store offset=84
              local.get $l14
              local.get $l11
              f32.store offset=64
              local.get $l14
              local.get $l3
              f32.store offset=48
              local.get $l14
              local.get $l4
              f32.store offset=32
              local.get $l14
              local.get $l9
              f32.store offset=96
              local.get $l14
              local.get $l12
              f32.store offset=80
              local.get $l14
              i32.const 0
              i32.store offset=140
              local.get $l14
              i32.const 0
              i32.store offset=124
              local.get $l14
              local.get $l8
              block $B7 (result f32)
                local.get $l10
                local.get $l10
                f32.add
                local.tee $l10
                f32.const 0x1.fffffep+127 (;=3.40282e+38;)
                f32.ge
                if $I8
                  local.get $l7
                  f32.const 0x1.fffffep+127 (;=3.40282e+38;)
                  f32.const -0x1.fffffep+127 (;=-3.40282e+38;)
                  local.get $l3
                  f32.const 0x0p+0 (;=0;)
                  f32.ge
                  select
                  local.get $l3
                  f32.const 0x0p+0 (;=0;)
                  f32.eq
                  select
                  local.set $l3
                  local.get $l6
                  f32.const 0x1.fffffep+127 (;=3.40282e+38;)
                  f32.const -0x1.fffffep+127 (;=-3.40282e+38;)
                  local.get $l4
                  f32.const 0x0p+0 (;=0;)
                  f32.ge
                  select
                  local.get $l4
                  f32.const 0x0p+0 (;=0;)
                  f32.eq
                  select
                  local.set $l4
                  local.get $l8
                  local.get $l5
                  f32.const 0x0p+0 (;=0;)
                  f32.eq
                  br_if $B7
                  drop
                  f32.const 0x1.fffffep+127 (;=3.40282e+38;)
                  f32.const -0x1.fffffep+127 (;=-3.40282e+38;)
                  local.get $l5
                  f32.const 0x0p+0 (;=0;)
                  f32.ge
                  select
                  br $B7
                end
                local.get $l7
                local.get $l10
                local.get $l3
                f32.mul
                f32.add
                local.set $l3
                local.get $l6
                local.get $l10
                local.get $l4
                f32.mul
                f32.add
                local.set $l4
                local.get $l8
                local.get $l10
                local.get $l5
                f32.mul
                f32.add
              end
              local.tee $l5
              local.get $l5
              local.get $l8
              f32.lt
              select
              f32.store offset=136
              local.get $l14
              local.get $l7
              local.get $l3
              local.get $l3
              local.get $l7
              f32.lt
              select
              f32.store offset=132
              local.get $l14
              local.get $l8
              local.get $l5
              local.get $l5
              local.get $l8
              f32.gt
              select
              f32.store offset=120
              local.get $l14
              local.get $l7
              local.get $l3
              local.get $l3
              local.get $l7
              f32.gt
              select
              f32.store offset=116
              local.get $l14
              local.get $l6
              local.get $l4
              local.get $l4
              local.get $l6
              f32.lt
              select
              f32.store offset=128
              local.get $l14
              local.get $l6
              local.get $l4
              local.get $l4
              local.get $l6
              f32.gt
              select
              f32.store offset=112
              local.get $p0
              i32.load offset=296
              local.get $p0
              i32.load offset=292
              local.get $l13
              local.get $l14
              i32.const 16
              i32.add
              local.get $p2
              call $f71873
              br_if $B1
              br $B0
            end
            local.get $p1
            f32.load offset=112
            local.set $l3
            local.get $p1
            f32.load offset=108
            local.set $l4
            local.get $p1
            i64.load offset=100 align=4
            local.set $l33
            local.get $l14
            i32.const 0
            i32.store offset=28
            local.get $l14
            local.get $l4
            f32.store offset=24
            local.get $l14
            local.get $l33
            i64.store offset=16
            local.get $l14
            local.get $l3
            local.get $l3
            f32.mul
            f32.store offset=32
            local.get $p0
            i32.load offset=296
            local.get $p0
            i32.load offset=292
            local.get $l13
            local.get $l14
            i32.const 16
            i32.add
            local.get $p2
            call $f71874
            br_if $B1
            br $B0
          end
          local.get $l14
          i32.const 16
          i32.add
          local.get $p1
          i32.const 48
          i32.add
          local.get $p1
          i32.const 12
          i32.add
          local.get $p1
          call $f71850
          local.set $l13
          local.get $p0
          i32.load offset=296
          local.get $p0
          i32.load offset=292
          local.get $p0
          i32.load offset=4
          local.get $l13
          local.get $p2
          call $f71871
          br_if $B1
          br $B0
        end
        local.get $p1
        f32.load offset=84
        local.set $l3
        local.get $p1
        f32.load offset=88
        local.set $l4
        local.get $p1
        f32.load offset=76
        local.set $l5
        local.get $p1
        f32.load offset=92
        local.set $l6
        local.get $p1
        f32.load offset=80
        local.set $l7
        local.get $p1
        f32.load offset=72
        local.set $l8
        local.get $l14
        i32.const 0
        i32.store offset=44
        local.get $l14
        local.get $l6
        local.get $l7
        f32.sub
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        f32.store offset=40
        local.get $l14
        local.get $l4
        local.get $l5
        f32.sub
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        f32.store offset=36
        local.get $l14
        i32.const 0
        i32.store offset=28
        local.get $l14
        local.get $l3
        local.get $l8
        f32.sub
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        f32.store offset=32
        local.get $l14
        local.get $l7
        local.get $l6
        f32.add
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        f32.store offset=24
        local.get $l14
        local.get $l5
        local.get $l4
        f32.add
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        f32.store offset=20
        local.get $l14
        local.get $l8
        local.get $l3
        f32.add
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        f32.store offset=16
        local.get $p0
        i32.load offset=296
        local.get $p0
        i32.load offset=292
        local.get $l13
        local.get $l14
        i32.const 16
        i32.add
        local.get $p2
        call $f71872
        i32.eqz
        br_if $B0
      end
      i32.const 1
      local.set $l22
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
      local.set $l22
      global.get $g0
      i32.const 224
      i32.sub
      local.tee $l13
      global.set $g0
      block $B9
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
        if $I10
          global.get $g0
          i32.const 208
          i32.sub
          local.tee $l15
          global.set $g0
          local.get $p0
          i32.const 4
          i32.add
          local.tee $l23
          i32.const 12
          i32.add
          local.set $l16
          local.get $p1
          i32.const 12
          i32.add
          local.set $l25
          local.get $p1
          i32.const 48
          i32.add
          local.set $l26
          local.get $l23
          i32.const 60
          i32.add
          local.set $l30
          i32.const 1
          local.set $l17
          i32.const 1
          local.set $l27
          loop $L11
            block $B12
              local.get $l16
              i32.load
              local.tee $l20
              i32.eqz
              br_if $B12
              local.get $l20
              i32.load offset=588
              i32.eqz
              local.get $l17
              i32.const -1
              i32.xor
              i32.or
              i32.const 1
              i32.and
              br_if $B12
              i32.const 1
              local.set $l17
              block $B13
                block $B14
                  block $B15
                    block $B16
                      local.get $p1
                      i32.load16_u offset=98
                      br_table $B14 $B12 $B15 $B16 $B13 $B12
                    end
                    local.get $p1
                    i32.load16_u offset=96
                    if $I17
                      local.get $l15
                      i32.const 16
                      i32.add
                      local.get $l26
                      local.get $l25
                      local.get $p1
                      call $f71850
                      local.set $l20
                      local.get $l23
                      i32.load offset=104
                      local.tee $l17
                      i32.load offset=12
                      local.get $l17
                      i32.load offset=8
                      local.get $l16
                      i32.load
                      local.get $l20
                      local.get $p2
                      call $f71875
                      local.set $l17
                      br $B12
                    end
                    local.get $p1
                    f32.load offset=84
                    local.set $l3
                    local.get $p1
                    f32.load offset=72
                    local.set $l4
                    local.get $p1
                    f32.load offset=88
                    local.set $l5
                    local.get $p1
                    f32.load offset=76
                    local.set $l6
                    local.get $p1
                    f32.load offset=92
                    local.set $l7
                    local.get $p1
                    f32.load offset=80
                    local.set $l8
                    local.get $l15
                    i32.const 0
                    i32.store offset=44
                    local.get $l15
                    i32.const 0
                    i32.store offset=28
                    local.get $l15
                    local.get $l7
                    local.get $l8
                    f32.sub
                    f32.const 0x1p-1 (;=0.5;)
                    f32.mul
                    f32.store offset=40
                    local.get $l15
                    local.get $l5
                    local.get $l6
                    f32.sub
                    f32.const 0x1p-1 (;=0.5;)
                    f32.mul
                    f32.store offset=36
                    local.get $l15
                    local.get $l3
                    local.get $l4
                    f32.sub
                    f32.const 0x1p-1 (;=0.5;)
                    f32.mul
                    f32.store offset=32
                    local.get $l15
                    local.get $l8
                    local.get $l7
                    f32.add
                    f32.const 0x1p-1 (;=0.5;)
                    f32.mul
                    f32.store offset=24
                    local.get $l15
                    local.get $l6
                    local.get $l5
                    f32.add
                    f32.const 0x1p-1 (;=0.5;)
                    f32.mul
                    f32.store offset=20
                    local.get $l15
                    local.get $l4
                    local.get $l3
                    f32.add
                    f32.const 0x1p-1 (;=0.5;)
                    f32.mul
                    f32.store offset=16
                    local.get $l23
                    i32.load offset=104
                    local.tee $l16
                    i32.load offset=12
                    local.set $l31
                    local.get $l16
                    i32.load offset=8
                    local.set $l32
                    local.get $l15
                    i32.const 16
                    i32.add
                    local.set $l18
                    i32.const 0
                    local.set $l21
                    i32.const 0
                    local.set $l28
                    global.get $g0
                    i32.const 1056
                    i32.sub
                    local.tee $l19
                    global.set $g0
                    local.get $l19
                    i32.const 1
                    i32.store8 offset=1040
                    local.get $l19
                    i64.const 1099511628032
                    i64.store offset=1048
                    local.get $l19
                    local.get $l19
                    i32.const 16
                    i32.add
                    i32.store offset=1044
                    local.get $l19
                    local.get $l20
                    i32.load offset=588
                    i32.store offset=16
                    loop $L18
                      local.get $l19
                      i32.load offset=1044
                      local.get $l21
                      i32.const 2
                      i32.shl
                      i32.add
                      i32.load
                      local.tee $l16
                      f32.load offset=16
                      local.tee $l4
                      local.get $l16
                      f32.load
                      local.tee $l5
                      f32.add
                      local.set $l3
                      local.get $l4
                      local.get $l5
                      f32.sub
                      local.set $l4
                      local.get $l16
                      f32.load offset=24
                      local.tee $l6
                      local.get $l16
                      f32.load offset=8
                      local.tee $l7
                      f32.add
                      local.set $l10
                      local.get $l16
                      f32.load offset=20
                      local.tee $l8
                      local.get $l16
                      f32.load offset=4
                      local.tee $l9
                      f32.add
                      local.set $l5
                      local.get $l6
                      local.get $l7
                      f32.sub
                      local.set $l7
                      local.get $l8
                      local.get $l9
                      f32.sub
                      local.set $l6
                      loop $L19
                        block $B20
                          block $B21
                            block $B22
                              local.get $l4
                              f32.const 0x1p-1 (;=0.5;)
                              f32.mul
                              local.get $l18
                              f32.load offset=16
                              f32.add
                              local.get $l3
                              f32.const 0x1p-1 (;=0.5;)
                              f32.mul
                              local.get $l18
                              f32.load
                              f32.sub
                              local.tee $l3
                              local.get $l3
                              f32.neg
                              local.tee $l4
                              local.get $l3
                              local.get $l4
                              f32.gt
                              select
                              f32.ge
                              i32.eqz
                              br_if $B22
                              local.get $l6
                              f32.const 0x1p-1 (;=0.5;)
                              f32.mul
                              local.get $l18
                              f32.load offset=20
                              f32.add
                              local.get $l5
                              f32.const 0x1p-1 (;=0.5;)
                              f32.mul
                              local.get $l18
                              f32.load offset=4
                              f32.sub
                              local.tee $l3
                              local.get $l3
                              f32.neg
                              local.tee $l4
                              local.get $l3
                              local.get $l4
                              f32.gt
                              select
                              f32.ge
                              i32.eqz
                              br_if $B22
                              local.get $l7
                              f32.const 0x1p-1 (;=0.5;)
                              f32.mul
                              local.get $l18
                              f32.load offset=24
                              f32.add
                              local.get $l10
                              f32.const 0x1p-1 (;=0.5;)
                              f32.mul
                              local.get $l18
                              f32.load offset=8
                              f32.sub
                              local.tee $l3
                              local.get $l3
                              f32.neg
                              local.tee $l4
                              local.get $l3
                              local.get $l4
                              f32.gt
                              select
                              f32.ge
                              i32.eqz
                              br_if $B22
                              local.get $l16
                              i32.load offset=40
                              br_if $B21
                              local.get $l16
                              i32.load offset=36
                              local.tee $l16
                              i32.load
                              local.tee $l20
                              i32.eqz
                              br_if $B22
                              local.get $l16
                              i32.const 4
                              i32.add
                              local.set $l16
                              local.get $l20
                              local.set $l17
                              loop $L23
                                local.get $l16
                                i32.load
                                local.set $l29
                                block $B24
                                  local.get $l20
                                  i32.const 2
                                  i32.ge_u
                                  if $I25
                                    local.get $l32
                                    local.get $l29
                                    i32.const 24
                                    i32.mul
                                    i32.add
                                    local.tee $l24
                                    f32.load offset=12
                                    local.tee $l3
                                    local.get $l24
                                    f32.load
                                    local.tee $l4
                                    f32.sub
                                    f32.const 0x1p-1 (;=0.5;)
                                    f32.mul
                                    local.get $l18
                                    f32.load offset=16
                                    f32.add
                                    local.get $l4
                                    local.get $l3
                                    f32.add
                                    f32.const 0x1p-1 (;=0.5;)
                                    f32.mul
                                    local.get $l18
                                    f32.load
                                    f32.sub
                                    local.tee $l3
                                    local.get $l3
                                    f32.neg
                                    local.tee $l4
                                    local.get $l3
                                    local.get $l4
                                    f32.gt
                                    select
                                    f32.ge
                                    i32.eqz
                                    br_if $B24
                                    local.get $l24
                                    f32.load offset=16
                                    local.tee $l3
                                    local.get $l24
                                    f32.load offset=4
                                    local.tee $l4
                                    f32.sub
                                    f32.const 0x1p-1 (;=0.5;)
                                    f32.mul
                                    local.get $l18
                                    f32.load offset=20
                                    f32.add
                                    local.get $l4
                                    local.get $l3
                                    f32.add
                                    f32.const 0x1p-1 (;=0.5;)
                                    f32.mul
                                    local.get $l18
                                    f32.load offset=4
                                    f32.sub
                                    local.tee $l3
                                    local.get $l3
                                    f32.neg
                                    local.tee $l4
                                    local.get $l3
                                    local.get $l4
                                    f32.gt
                                    select
                                    f32.ge
                                    i32.eqz
                                    br_if $B24
                                    local.get $l24
                                    f32.load offset=20
                                    local.tee $l3
                                    local.get $l24
                                    f32.load offset=8
                                    local.tee $l4
                                    f32.sub
                                    f32.const 0x1p-1 (;=0.5;)
                                    f32.mul
                                    local.get $l18
                                    f32.load offset=24
                                    f32.add
                                    local.get $l4
                                    local.get $l3
                                    f32.add
                                    f32.const 0x1p-1 (;=0.5;)
                                    f32.mul
                                    local.get $l18
                                    f32.load offset=8
                                    f32.sub
                                    local.tee $l3
                                    local.get $l3
                                    f32.neg
                                    local.tee $l4
                                    local.get $l3
                                    local.get $l4
                                    f32.gt
                                    select
                                    f32.ge
                                    i32.eqz
                                    br_if $B24
                                  end
                                  local.get $p2
                                  local.get $l19
                                  i32.const 12
                                  i32.add
                                  local.get $l31
                                  local.get $l29
                                  i32.const 3
                                  i32.shl
                                  i32.add
                                  local.get $p2
                                  i32.load
                                  i32.load
                                  call_indirect $__indirect_function_table (type $t3)
                                  i32.eqz
                                  br_if $B20
                                end
                                local.get $l16
                                i32.const 4
                                i32.add
                                local.set $l16
                                local.get $l17
                                i32.const 1
                                i32.sub
                                local.tee $l17
                                br_if $L23
                              end
                            end
                            local.get $l21
                            i32.eqz
                            local.set $l28
                            local.get $l21
                            i32.eqz
                            br_if $B20
                            local.get $l21
                            i32.const 1
                            i32.sub
                            local.set $l21
                            br $L18
                          end
                          local.get $l19
                          i32.load offset=1044
                          local.get $l21
                          i32.const 2
                          i32.shl
                          i32.add
                          local.get $l16
                          i32.load offset=36
                          local.tee $l16
                          i32.const 48
                          i32.add
                          i32.store
                          local.get $l21
                          i32.const 1
                          i32.add
                          local.tee $l21
                          local.get $l19
                          i32.load offset=1052
                          i32.const 2147483647
                          i32.and
                          i32.eq
                          if $I26
                            local.get $l19
                            i32.const 16
                            i32.add
                            local.get $l21
                            i32.const 1
                            i32.shl
                            call $f71848
                          end
                          local.get $l16
                          f32.load offset=16
                          local.tee $l4
                          local.get $l16
                          f32.load
                          local.tee $l5
                          f32.add
                          local.set $l3
                          local.get $l4
                          local.get $l5
                          f32.sub
                          local.set $l4
                          local.get $l16
                          f32.load offset=24
                          local.tee $l6
                          local.get $l16
                          f32.load offset=8
                          local.tee $l7
                          f32.add
                          local.set $l10
                          local.get $l16
                          f32.load offset=20
                          local.tee $l8
                          local.get $l16
                          f32.load offset=4
                          local.tee $l9
                          f32.add
                          local.set $l5
                          local.get $l6
                          local.get $l7
                          f32.sub
                          local.set $l7
                          local.get $l8
                          local.get $l9
                          f32.sub
                          local.set $l6
                          br $L19
                        end
                      end
                    end
                    block $B27
                      local.get $l19
                      i32.load offset=1052
                      local.tee $l16
                      i32.const 0
                      i32.lt_s
                      br_if $B27
                      local.get $l16
                      i32.const 2147483647
                      i32.and
                      i32.eqz
                      br_if $B27
                      local.get $l19
                      i32.load offset=1044
                      local.tee $l16
                      local.get $l19
                      i32.const 16
                      i32.add
                      i32.eq
                      br_if $B27
                      local.get $l16
                      i32.eqz
                      br_if $B27
                      call $f69753
                      local.tee $l18
                      local.get $l16
                      local.get $l18
                      i32.load
                      i32.load offset=12
                      call_indirect $__indirect_function_table (type $t1)
                    end
                    local.get $l19
                    i32.const 1056
                    i32.add
                    global.set $g0
                    local.get $l28
                    local.set $l17
                    br $B12
                  end
                  local.get $p1
                  f32.load offset=60
                  local.set $l10
                  local.get $p1
                  f32.load offset=124
                  local.set $l9
                  local.get $p1
                  f32.load offset=112
                  local.set $l6
                  local.get $p1
                  f32.load offset=116
                  local.set $l7
                  local.get $p1
                  f32.load offset=120
                  local.set $l8
                  local.get $l15
                  i32.const 0
                  i32.store offset=28
                  local.get $l15
                  local.get $l8
                  f32.store offset=24
                  local.get $l15
                  local.get $l7
                  f32.store offset=20
                  local.get $l15
                  local.get $l6
                  f32.store offset=16
                  local.get $p1
                  f32.load offset=16
                  local.set $l3
                  local.get $p1
                  f32.load offset=20
                  local.set $l5
                  local.get $p1
                  f32.load offset=12
                  local.set $l4
                  local.get $l15
                  i32.const 0
                  i32.store offset=108
                  local.get $l15
                  i32.const 0
                  i32.store offset=92
                  local.get $l15
                  i32.const 0
                  i32.store offset=76
                  local.get $l15
                  local.get $l9
                  f32.const 0x1.028f5cp+0 (;=1.01;)
                  f32.mul
                  local.tee $l9
                  f32.store offset=72
                  local.get $l15
                  local.get $l9
                  f32.store offset=68
                  local.get $l15
                  local.get $l9
                  f32.store offset=64
                  local.get $l15
                  i32.const 0
                  i32.store offset=60
                  local.get $l15
                  local.get $l4
                  f32.store offset=56
                  local.get $l15
                  local.get $l5
                  f32.store offset=52
                  local.get $l15
                  local.get $l3
                  f32.store offset=48
                  local.get $l15
                  i32.const 0
                  i32.store offset=44
                  local.get $l15
                  local.get $l5
                  f32.store offset=40
                  local.get $l15
                  local.get $l3
                  f32.store offset=36
                  local.get $l15
                  local.get $l4
                  f32.store offset=32
                  local.get $l15
                  local.get $l4
                  local.get $l4
                  f32.neg
                  local.tee $l9
                  local.get $l4
                  local.get $l9
                  f32.gt
                  select
                  local.tee $l9
                  f32.store offset=104
                  local.get $l15
                  local.get $l5
                  local.get $l5
                  f32.neg
                  local.tee $l11
                  local.get $l5
                  local.get $l11
                  f32.gt
                  select
                  local.tee $l11
                  f32.store offset=100
                  local.get $l15
                  local.get $l3
                  local.get $l3
                  f32.neg
                  local.tee $l12
                  local.get $l3
                  local.get $l12
                  f32.gt
                  select
                  local.tee $l12
                  f32.store offset=96
                  local.get $l15
                  local.get $l11
                  f32.store offset=88
                  local.get $l15
                  local.get $l12
                  f32.store offset=84
                  local.get $l15
                  local.get $l9
                  f32.store offset=80
                  local.get $l15
                  i32.const 0
                  i32.store offset=140
                  local.get $l15
                  i32.const 0
                  i32.store offset=124
                  local.get $l15
                  local.get $l8
                  block $B28 (result f32)
                    local.get $l10
                    local.get $l10
                    f32.add
                    local.tee $l10
                    f32.const 0x1.fffffep+127 (;=3.40282e+38;)
                    f32.ge
                    if $I29
                      local.get $l7
                      f32.const 0x1.fffffep+127 (;=3.40282e+38;)
                      f32.const -0x1.fffffep+127 (;=-3.40282e+38;)
                      local.get $l3
                      f32.const 0x0p+0 (;=0;)
                      f32.ge
                      select
                      local.get $l3
                      f32.const 0x0p+0 (;=0;)
                      f32.eq
                      select
                      local.set $l3
                      local.get $l6
                      f32.const 0x1.fffffep+127 (;=3.40282e+38;)
                      f32.const -0x1.fffffep+127 (;=-3.40282e+38;)
                      local.get $l4
                      f32.const 0x0p+0 (;=0;)
                      f32.ge
                      select
                      local.get $l4
                      f32.const 0x0p+0 (;=0;)
                      f32.eq
                      select
                      local.set $l4
                      local.get $l8
                      local.get $l5
                      f32.const 0x0p+0 (;=0;)
                      f32.eq
                      br_if $B28
                      drop
                      f32.const 0x1.fffffep+127 (;=3.40282e+38;)
                      f32.const -0x1.fffffep+127 (;=-3.40282e+38;)
                      local.get $l5
                      f32.const 0x0p+0 (;=0;)
                      f32.ge
                      select
                      br $B28
                    end
                    local.get $l7
                    local.get $l10
                    local.get $l3
                    f32.mul
                    f32.add
                    local.set $l3
                    local.get $l6
                    local.get $l10
                    local.get $l4
                    f32.mul
                    f32.add
                    local.set $l4
                    local.get $l8
                    local.get $l10
                    local.get $l5
                    f32.mul
                    f32.add
                  end
                  local.tee $l5
                  local.get $l5
                  local.get $l8
                  f32.lt
                  select
                  f32.store offset=136
                  local.get $l15
                  local.get $l7
                  local.get $l3
                  local.get $l3
                  local.get $l7
                  f32.lt
                  select
                  f32.store offset=132
                  local.get $l15
                  local.get $l6
                  local.get $l4
                  local.get $l4
                  local.get $l6
                  f32.lt
                  select
                  f32.store offset=128
                  local.get $l15
                  local.get $l8
                  local.get $l5
                  local.get $l5
                  local.get $l8
                  f32.gt
                  select
                  f32.store offset=120
                  local.get $l15
                  local.get $l7
                  local.get $l3
                  local.get $l3
                  local.get $l7
                  f32.gt
                  select
                  f32.store offset=116
                  local.get $l15
                  local.get $l6
                  local.get $l4
                  local.get $l4
                  local.get $l6
                  f32.gt
                  select
                  f32.store offset=112
                  local.get $l23
                  i32.load offset=104
                  local.tee $l16
                  i32.load offset=12
                  local.get $l16
                  i32.load offset=8
                  local.get $l20
                  local.get $l15
                  i32.const 16
                  i32.add
                  local.get $p2
                  call $f71876
                  local.set $l17
                  br $B12
                end
                local.get $p1
                f32.load offset=112
                local.set $l3
                local.get $p1
                i64.load offset=100 align=4
                local.set $l33
                local.get $p1
                f32.load offset=108
                local.set $l4
                local.get $l15
                i32.const 0
                i32.store offset=28
                local.get $l15
                local.get $l4
                f32.store offset=24
                local.get $l15
                local.get $l33
                i64.store offset=16
                local.get $l15
                local.get $l3
                local.get $l3
                f32.mul
                f32.store offset=32
                local.get $l23
                i32.load offset=104
                local.tee $l16
                i32.load offset=12
                local.get $l16
                i32.load offset=8
                local.get $l20
                local.get $l15
                i32.const 16
                i32.add
                local.get $p2
                call $f71877
                local.set $l17
                br $B12
              end
              local.get $l15
              i32.const 16
              i32.add
              local.get $l26
              local.get $l25
              local.get $p1
              call $f71850
              local.set $l20
              local.get $l23
              i32.load offset=104
              local.tee $l17
              i32.load offset=12
              local.get $l17
              i32.load offset=8
              local.get $l16
              i32.load
              local.get $l20
              local.get $p2
              call $f71875
              local.set $l17
            end
            local.get $l27
            if $I30
              i32.const 0
              local.set $l27
              local.get $l30
              local.set $l16
              br $L11
            end
          end
          local.get $l15
          i32.const 208
          i32.add
          global.set $g0
          local.get $l17
          i32.const 1
          i32.and
          i32.eqz
          br_if $B9
        end
        i32.const 1
        local.set $l22
        local.get $p0
        i32.load offset=164
        i32.eqz
        br_if $B9
        block $B31
          block $B32
            block $B33
              block $B34
                local.get $p1
                i32.load16_u offset=98
                br_table $B32 $B9 $B33 $B34 $B31 $B9
              end
              local.get $p1
              i32.load16_u offset=96
              if $I35
                local.get $l13
                i32.const 32
                i32.add
                local.get $p1
                i32.const 48
                i32.add
                local.get $p1
                i32.const 12
                i32.add
                local.get $p1
                call $f71850
                local.set $p1
                local.get $l13
                local.get $p0
                i32.load offset=124
                i32.store offset=28
                local.get $l13
                local.get $p2
                i32.store offset=24
                local.get $l13
                local.get $p1
                i32.store offset=20
                local.get $l13
                i32.const 3179072
                i32.store offset=16
                local.get $p0
                i32.load offset=200
                local.get $p0
                i32.load offset=196
                local.get $p0
                i32.load offset=168
                local.get $p1
                local.get $l13
                i32.const 16
                i32.add
                call $f71871
                local.set $l22
                br $B9
              end
              local.get $p1
              f32.load offset=84
              local.set $l3
              local.get $p1
              f32.load offset=88
              local.set $l4
              local.get $p1
              f32.load offset=76
              local.set $l5
              local.get $p1
              f32.load offset=92
              local.set $l6
              local.get $p1
              f32.load offset=80
              local.set $l7
              local.get $p1
              f32.load offset=72
              local.set $l8
              local.get $l13
              i32.const 0
              i32.store offset=60
              local.get $l13
              local.get $l6
              local.get $l7
              f32.sub
              f32.const 0x1p-1 (;=0.5;)
              f32.mul
              f32.store offset=56
              local.get $l13
              local.get $l4
              local.get $l5
              f32.sub
              f32.const 0x1p-1 (;=0.5;)
              f32.mul
              f32.store offset=52
              local.get $l13
              i32.const 0
              i32.store offset=44
              local.get $l13
              local.get $l3
              local.get $l8
              f32.sub
              f32.const 0x1p-1 (;=0.5;)
              f32.mul
              f32.store offset=48
              local.get $l13
              local.get $l7
              local.get $l6
              f32.add
              f32.const 0x1p-1 (;=0.5;)
              f32.mul
              f32.store offset=40
              local.get $l13
              local.get $l5
              local.get $l4
              f32.add
              f32.const 0x1p-1 (;=0.5;)
              f32.mul
              f32.store offset=36
              local.get $l13
              local.get $l8
              local.get $l3
              f32.add
              f32.const 0x1p-1 (;=0.5;)
              f32.mul
              f32.store offset=32
              local.get $l13
              local.get $p0
              i32.load offset=124
              i32.store offset=28
              local.get $l13
              local.get $p2
              i32.store offset=24
              local.get $l13
              i32.const 3179092
              i32.store offset=16
              local.get $l13
              local.get $l13
              i32.const 32
              i32.add
              i32.store offset=20
              local.get $p0
              i32.load offset=200
              local.get $p0
              i32.load offset=196
              local.get $p0
              i32.load offset=168
              local.get $l13
              i32.const 32
              i32.add
              local.get $l13
              i32.const 16
              i32.add
              call $f71872
              local.set $l22
              br $B9
            end
            local.get $p1
            f32.load offset=60
            local.set $l10
            local.get $p1
            f32.load offset=124
            local.set $l11
            local.get $p1
            f32.load offset=112
            local.set $l6
            local.get $p1
            f32.load offset=116
            local.set $l7
            local.get $p1
            f32.load offset=120
            local.set $l8
            local.get $l13
            i32.const 0
            i32.store offset=44
            local.get $l13
            local.get $l8
            f32.store offset=40
            local.get $l13
            local.get $l7
            f32.store offset=36
            local.get $l13
            local.get $l6
            f32.store offset=32
            local.get $p1
            f32.load offset=16
            local.set $l3
            local.get $p1
            f32.load offset=20
            local.set $l5
            local.get $p1
            f32.load offset=12
            local.set $l4
            local.get $l13
            i32.const 0
            i32.store offset=124
            local.get $l13
            i32.const 0
            i32.store offset=108
            local.get $l13
            i32.const 0
            i32.store offset=92
            local.get $l13
            local.get $l11
            f32.const 0x1.028f5cp+0 (;=1.01;)
            f32.mul
            local.tee $l11
            f32.store offset=88
            local.get $l13
            local.get $l11
            f32.store offset=84
            local.get $l13
            i32.const 0
            i32.store offset=76
            local.get $l13
            local.get $l4
            f32.store offset=72
            local.get $l13
            local.get $l5
            f32.store offset=68
            local.get $l13
            i32.const 0
            i32.store offset=60
            local.get $l13
            local.get $l5
            f32.store offset=56
            local.get $l13
            local.get $l3
            f32.store offset=52
            local.get $l13
            local.get $l4
            local.get $l4
            f32.neg
            local.tee $l12
            local.get $l4
            local.get $l12
            f32.gt
            select
            local.tee $l12
            f32.store offset=120
            local.get $l13
            local.get $l5
            local.get $l5
            f32.neg
            local.tee $l9
            local.get $l5
            local.get $l9
            f32.gt
            select
            local.tee $l9
            f32.store offset=116
            local.get $l13
            local.get $l9
            f32.store offset=104
            local.get $l13
            local.get $l3
            local.get $l3
            f32.neg
            local.tee $l9
            local.get $l3
            local.get $l9
            f32.gt
            select
            local.tee $l9
            f32.store offset=100
            local.get $l13
            local.get $l11
            f32.store offset=80
            local.get $l13
            local.get $l3
            f32.store offset=64
            local.get $l13
            local.get $l4
            f32.store offset=48
            local.get $l13
            local.get $l9
            f32.store offset=112
            local.get $l13
            local.get $l12
            f32.store offset=96
            local.get $l13
            i32.const 0
            i32.store offset=156
            local.get $l13
            i32.const 0
            i32.store offset=140
            local.get $l13
            local.get $l8
            block $B36 (result f32)
              local.get $l10
              local.get $l10
              f32.add
              local.tee $l10
              f32.const 0x1.fffffep+127 (;=3.40282e+38;)
              f32.ge
              if $I37
                local.get $l7
                f32.const 0x1.fffffep+127 (;=3.40282e+38;)
                f32.const -0x1.fffffep+127 (;=-3.40282e+38;)
                local.get $l3
                f32.const 0x0p+0 (;=0;)
                f32.ge
                select
                local.get $l3
                f32.const 0x0p+0 (;=0;)
                f32.eq
                select
                local.set $l3
                local.get $l6
                f32.const 0x1.fffffep+127 (;=3.40282e+38;)
                f32.const -0x1.fffffep+127 (;=-3.40282e+38;)
                local.get $l4
                f32.const 0x0p+0 (;=0;)
                f32.ge
                select
                local.get $l4
                f32.const 0x0p+0 (;=0;)
                f32.eq
                select
                local.set $l4
                local.get $l8
                local.get $l5
                f32.const 0x0p+0 (;=0;)
                f32.eq
                br_if $B36
                drop
                f32.const 0x1.fffffep+127 (;=3.40282e+38;)
                f32.const -0x1.fffffep+127 (;=-3.40282e+38;)
                local.get $l5
                f32.const 0x0p+0 (;=0;)
                f32.ge
                select
                br $B36
              end
              local.get $l7
              local.get $l10
              local.get $l3
              f32.mul
              f32.add
              local.set $l3
              local.get $l6
              local.get $l10
              local.get $l4
              f32.mul
              f32.add
              local.set $l4
              local.get $l8
              local.get $l10
              local.get $l5
              f32.mul
              f32.add
            end
            local.tee $l5
            local.get $l5
            local.get $l8
            f32.lt
            select
            f32.store offset=152
            local.get $l13
            local.get $l7
            local.get $l3
            local.get $l3
            local.get $l7
            f32.lt
            select
            f32.store offset=148
            local.get $l13
            local.get $l8
            local.get $l5
            local.get $l5
            local.get $l8
            f32.gt
            select
            f32.store offset=136
            local.get $l13
            local.get $l7
            local.get $l3
            local.get $l3
            local.get $l7
            f32.gt
            select
            f32.store offset=132
            local.get $l13
            local.get $l6
            local.get $l4
            local.get $l4
            local.get $l6
            f32.lt
            select
            f32.store offset=144
            local.get $l13
            local.get $l6
            local.get $l4
            local.get $l4
            local.get $l6
            f32.gt
            select
            f32.store offset=128
            local.get $l13
            local.get $p0
            i32.load offset=124
            i32.store offset=28
            local.get $l13
            local.get $p2
            i32.store offset=24
            local.get $l13
            i32.const 3179112
            i32.store offset=16
            local.get $l13
            local.get $l13
            i32.const 32
            i32.add
            i32.store offset=20
            local.get $p0
            i32.load offset=200
            local.get $p0
            i32.load offset=196
            local.get $p0
            i32.load offset=168
            local.get $l13
            i32.const 32
            i32.add
            local.get $l13
            i32.const 16
            i32.add
            call $f71873
            local.set $l22
            br $B9
          end
          local.get $p1
          f32.load offset=112
          local.set $l3
          local.get $p1
          f32.load offset=108
          local.set $l4
          local.get $p1
          i64.load offset=100 align=4
          local.set $l33
          local.get $l13
          i32.const 0
          i32.store offset=44
          local.get $l13
          local.get $l4
          f32.store offset=40
          local.get $l13
          local.get $l33
          i64.store offset=32
          local.get $l13
          local.get $l3
          local.get $l3
          f32.mul
          f32.store offset=48
          local.get $l13
          local.get $p0
          i32.load offset=124
          i32.store offset=28
          local.get $l13
          local.get $p2
          i32.store offset=24
          local.get $l13
          i32.const 3179132
          i32.store offset=16
          local.get $l13
          local.get $l13
          i32.const 32
          i32.add
          i32.store offset=20
          local.get $p0
          i32.load offset=200
          local.get $p0
          i32.load offset=196
          local.get $p0
          i32.load offset=168
          local.get $l13
          i32.const 32
          i32.add
          local.get $l13
          i32.const 16
          i32.add
          call $f71874
          local.set $l22
          br $B9
        end
        local.get $l13
        i32.const 32
        i32.add
        local.get $p1
        i32.const 48
        i32.add
        local.get $p1
        i32.const 12
        i32.add
        local.get $p1
        call $f71850
        local.set $p1
        local.get $l13
        local.get $p0
        i32.load offset=124
        i32.store offset=28
        local.get $l13
        local.get $p2
        i32.store offset=24
        local.get $l13
        local.get $p1
        i32.store offset=20
        local.get $l13
        i32.const 3179072
        i32.store offset=16
        local.get $p0
        i32.load offset=200
        local.get $p0
        i32.load offset=196
        local.get $p0
        i32.load offset=168
        local.get $p1
        local.get $l13
        i32.const 16
        i32.add
        call $f71871
        local.set $l22
      end
      local.get $l13
      i32.const 224
      i32.add
      global.set $g0
    end
    local.get $l14
    i32.const 208
    i32.add
    global.set $g0
    local.get $l22)
