  (func $f71849 (type $t8) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (result i32)
    (local $l4 f32) (local $l5 f32) (local $l6 f32) (local $l7 f32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 i32) (local $l15 i32) (local $l16 i32) (local $l17 i32) (local $l18 i32) (local $l19 i32) (local $l20 i32) (local $l21 i32) (local $l22 i32) (local $l23 i64)
    global.get $g0
    i32.const 224
    i32.sub
    local.tee $l15
    global.set $g0
    i32.const 1
    local.set $l16
    block $B0
      local.get $p0
      i32.load offset=592
      i32.eqz
      br_if $B0
      local.get $p0
      i32.const 4
      i32.add
      local.set $l14
      block $B1
        block $B2
          block $B3
            block $B4
              local.get $p1
              i32.load16_u offset=98
              br_table $B2 $B0 $B3 $B4 $B1 $B0
            end
            local.get $p1
            i32.load16_u offset=96
            if $I5
              local.get $l15
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
              local.set $l16
              local.get $l15
              local.get $p3
              i32.load16_u
              i32.store16 offset=28
              local.get $l15
              local.get $p2
              i32.store offset=24
              local.get $l15
              local.get $p1
              i32.store offset=20
              local.get $l15
              i32.const 3178060
              i32.store offset=16
              local.get $p0
              i32.load offset=644
              local.get $p0
              i32.load offset=640
              local.get $l14
              local.get $l16
              local.get $l15
              i32.const 16
              i32.add
              call $f71851
              local.set $l16
              br $B0
            end
            local.get $p1
            f32.load offset=84
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
            local.get $p1
            f32.load offset=72
            local.set $l9
            local.get $l15
            i32.const 0
            i32.store offset=60
            local.get $l15
            local.get $l7
            local.get $l8
            f32.sub
            f32.const 0x1p-1 (;=0.5;)
            f32.mul
            f32.store offset=56
            local.get $l15
            local.get $l5
            local.get $l6
            f32.sub
            f32.const 0x1p-1 (;=0.5;)
            f32.mul
            f32.store offset=52
            local.get $l15
            i32.const 0
            i32.store offset=44
            local.get $l15
            local.get $l4
            local.get $l9
            f32.sub
            f32.const 0x1p-1 (;=0.5;)
            f32.mul
            f32.store offset=48
            local.get $l15
            local.get $l8
            local.get $l7
            f32.add
            f32.const 0x1p-1 (;=0.5;)
            f32.mul
            f32.store offset=40
            local.get $l15
            local.get $l6
            local.get $l5
            f32.add
            f32.const 0x1p-1 (;=0.5;)
            f32.mul
            f32.store offset=36
            local.get $l15
            local.get $l9
            local.get $l4
            f32.add
            f32.const 0x1p-1 (;=0.5;)
            f32.mul
            f32.store offset=32
            local.get $l15
            local.get $p3
            i32.load16_u
            i32.store16 offset=28
            local.get $l15
            local.get $p2
            i32.store offset=24
            local.get $l15
            local.get $p1
            i32.store offset=20
            local.get $l15
            i32.const 3178080
            i32.store offset=16
            local.get $p0
            i32.load offset=644
            local.set $l21
            local.get $p0
            i32.load offset=640
            local.set $l22
            local.get $l15
            i32.const 32
            i32.add
            local.set $p2
            local.get $l15
            i32.const 16
            i32.add
            local.set $l18
            i32.const 0
            local.set $l16
            global.get $g0
            i32.const 1056
            i32.sub
            local.tee $p3
            global.set $g0
            local.get $p3
            i32.const 1
            i32.store8 offset=1040
            local.get $p3
            i64.const 1099511628032
            i64.store offset=1048
            local.get $p3
            local.get $p3
            i32.const 16
            i32.add
            i32.store offset=1044
            local.get $p3
            local.get $l14
            i32.load offset=588
            i32.store offset=16
            loop $L6
              local.get $p3
              i32.load offset=1044
              local.get $l16
              i32.const 2
              i32.shl
              i32.add
              i32.load
              local.tee $l14
              f32.load offset=16
              local.tee $l5
              local.get $l14
              f32.load
              local.tee $l6
              f32.add
              local.set $l4
              local.get $l5
              local.get $l6
              f32.sub
              local.set $l5
              local.get $l14
              f32.load offset=24
              local.tee $l7
              local.get $l14
              f32.load offset=8
              local.tee $l8
              f32.add
              local.set $l11
              local.get $l14
              f32.load offset=20
              local.tee $l9
              local.get $l14
              f32.load offset=4
              local.tee $l10
              f32.add
              local.set $l6
              local.get $l7
              local.get $l8
              f32.sub
              local.set $l8
              local.get $l9
              local.get $l10
              f32.sub
              local.set $l7
              loop $L7
                block $B8
                  block $B9
                    block $B10
                      local.get $l5
                      f32.const 0x1p-1 (;=0.5;)
                      f32.mul
                      local.get $p2
                      f32.load offset=16
                      f32.add
                      local.get $l4
                      f32.const 0x1p-1 (;=0.5;)
                      f32.mul
                      local.get $p2
                      f32.load
                      f32.sub
                      local.tee $l4
                      local.get $l4
                      f32.neg
                      local.tee $l5
                      local.get $l4
                      local.get $l5
                      f32.gt
                      select
                      f32.ge
                      i32.eqz
                      br_if $B10
                      local.get $l7
                      f32.const 0x1p-1 (;=0.5;)
                      f32.mul
                      local.get $p2
                      f32.load offset=20
                      f32.add
                      local.get $l6
                      f32.const 0x1p-1 (;=0.5;)
                      f32.mul
                      local.get $p2
                      f32.load offset=4
                      f32.sub
                      local.tee $l4
                      local.get $l4
                      f32.neg
                      local.tee $l5
                      local.get $l4
                      local.get $l5
                      f32.gt
                      select
                      f32.ge
                      i32.eqz
                      br_if $B10
                      local.get $l8
                      f32.const 0x1p-1 (;=0.5;)
                      f32.mul
                      local.get $p2
                      f32.load offset=24
                      f32.add
                      local.get $l11
                      f32.const 0x1p-1 (;=0.5;)
                      f32.mul
                      local.get $p2
                      f32.load offset=8
                      f32.sub
                      local.tee $l4
                      local.get $l4
                      f32.neg
                      local.tee $l5
                      local.get $l4
                      local.get $l5
                      f32.gt
                      select
                      f32.ge
                      i32.eqz
                      br_if $B10
                      local.get $l14
                      i32.load offset=40
                      br_if $B9
                      local.get $l14
                      i32.load offset=36
                      local.tee $l14
                      i32.load
                      local.tee $p0
                      i32.eqz
                      br_if $B10
                      local.get $l14
                      i32.const 4
                      i32.add
                      local.set $l14
                      local.get $p0
                      local.set $p1
                      loop $L11
                        local.get $l14
                        i32.load
                        local.set $l20
                        block $B12
                          local.get $p0
                          i32.const 2
                          i32.ge_u
                          if $I13
                            local.get $l22
                            local.get $l20
                            i32.const 24
                            i32.mul
                            i32.add
                            local.tee $l17
                            f32.load offset=12
                            local.tee $l4
                            local.get $l17
                            f32.load
                            local.tee $l5
                            f32.sub
                            f32.const 0x1p-1 (;=0.5;)
                            f32.mul
                            local.get $p2
                            f32.load offset=16
                            f32.add
                            local.get $l5
                            local.get $l4
                            f32.add
                            f32.const 0x1p-1 (;=0.5;)
                            f32.mul
                            local.get $p2
                            f32.load
                            f32.sub
                            local.tee $l4
                            local.get $l4
                            f32.neg
                            local.tee $l5
                            local.get $l4
                            local.get $l5
                            f32.gt
                            select
                            f32.ge
                            i32.eqz
                            br_if $B12
                            local.get $l17
                            f32.load offset=16
                            local.tee $l4
                            local.get $l17
                            f32.load offset=4
                            local.tee $l5
                            f32.sub
                            f32.const 0x1p-1 (;=0.5;)
                            f32.mul
                            local.get $p2
                            f32.load offset=20
                            f32.add
                            local.get $l5
                            local.get $l4
                            f32.add
                            f32.const 0x1p-1 (;=0.5;)
                            f32.mul
                            local.get $p2
                            f32.load offset=4
                            f32.sub
                            local.tee $l4
                            local.get $l4
                            f32.neg
                            local.tee $l5
                            local.get $l4
                            local.get $l5
                            f32.gt
                            select
                            f32.ge
                            i32.eqz
                            br_if $B12
                            local.get $l17
                            f32.load offset=20
                            local.tee $l4
                            local.get $l17
                            f32.load offset=8
                            local.tee $l5
                            f32.sub
                            f32.const 0x1p-1 (;=0.5;)
                            f32.mul
                            local.get $p2
                            f32.load offset=24
                            f32.add
                            local.get $l5
                            local.get $l4
                            f32.add
                            f32.const 0x1p-1 (;=0.5;)
                            f32.mul
                            local.get $p2
                            f32.load offset=8
                            f32.sub
                            local.tee $l4
                            local.get $l4
                            f32.neg
                            local.tee $l5
                            local.get $l4
                            local.get $l5
                            f32.gt
                            select
                            f32.ge
                            i32.eqz
                            br_if $B12
                          end
                          local.get $l18
                          local.get $p3
                          i32.const 12
                          i32.add
                          local.get $l21
                          local.get $l20
                          i32.const 44
                          i32.mul
                          i32.add
                          local.get $l18
                          i32.load
                          i32.load offset=8
                          call_indirect $__indirect_function_table (type $t3)
                          i32.eqz
                          br_if $B8
                        end
                        local.get $l14
                        i32.const 4
                        i32.add
                        local.set $l14
                        local.get $p1
                        i32.const 1
                        i32.sub
                        local.tee $p1
                        br_if $L11
                      end
                    end
                    local.get $l16
                    i32.eqz
                    local.set $l19
                    local.get $l16
                    i32.eqz
                    br_if $B8
                    local.get $l16
                    i32.const 1
                    i32.sub
                    local.set $l16
                    br $L6
                  end
                  local.get $p3
                  i32.load offset=1044
                  local.get $l16
                  i32.const 2
                  i32.shl
                  i32.add
                  local.get $l14
                  i32.load offset=36
                  local.tee $l14
                  i32.const 48
                  i32.add
                  i32.store
                  local.get $l16
                  i32.const 1
                  i32.add
                  local.tee $l16
                  local.get $p3
                  i32.load offset=1052
                  i32.const 2147483647
                  i32.and
                  i32.eq
                  if $I14
                    local.get $p3
                    i32.const 16
                    i32.add
                    local.get $l16
                    i32.const 1
                    i32.shl
                    call $f71848
                  end
                  local.get $l14
                  f32.load offset=16
                  local.tee $l5
                  local.get $l14
                  f32.load
                  local.tee $l6
                  f32.add
                  local.set $l4
                  local.get $l5
                  local.get $l6
                  f32.sub
                  local.set $l5
                  local.get $l14
                  f32.load offset=24
                  local.tee $l7
                  local.get $l14
                  f32.load offset=8
                  local.tee $l8
                  f32.add
                  local.set $l11
                  local.get $l14
                  f32.load offset=20
                  local.tee $l9
                  local.get $l14
                  f32.load offset=4
                  local.tee $l10
                  f32.add
                  local.set $l6
                  local.get $l7
                  local.get $l8
                  f32.sub
                  local.set $l8
                  local.get $l9
                  local.get $l10
                  f32.sub
                  local.set $l7
                  br $L7
                end
              end
            end
            block $B15
              local.get $p3
              i32.load offset=1052
              local.tee $l14
              i32.const 0
              i32.lt_s
              br_if $B15
              local.get $l14
              i32.const 2147483647
              i32.and
              i32.eqz
              br_if $B15
              local.get $p3
              i32.load offset=1044
              local.tee $l14
              local.get $p3
              i32.const 16
              i32.add
              i32.eq
              br_if $B15
              local.get $l14
              i32.eqz
              br_if $B15
              call $f69753
              local.tee $p2
              local.get $l14
              local.get $p2
              i32.load
              i32.load offset=12
              call_indirect $__indirect_function_table (type $t1)
            end
            local.get $p3
            i32.const 1056
            i32.add
            global.set $g0
            local.get $l19
            local.set $l16
            br $B0
          end
          local.get $p1
          f32.load offset=60
          local.set $l11
          local.get $p1
          f32.load offset=124
          local.set $l12
          local.get $p1
          f32.load offset=112
          local.set $l7
          local.get $p1
          f32.load offset=116
          local.set $l8
          local.get $p1
          f32.load offset=120
          local.set $l9
          local.get $l15
          i32.const 0
          i32.store offset=44
          local.get $l15
          local.get $l9
          f32.store offset=40
          local.get $l15
          local.get $l8
          f32.store offset=36
          local.get $l15
          local.get $l7
          f32.store offset=32
          local.get $p1
          f32.load offset=16
          local.set $l4
          local.get $p1
          f32.load offset=20
          local.set $l6
          local.get $p1
          f32.load offset=12
          local.set $l5
          local.get $l15
          i32.const 0
          i32.store offset=124
          local.get $l15
          i32.const 0
          i32.store offset=108
          local.get $l15
          i32.const 0
          i32.store offset=92
          local.get $l15
          local.get $l12
          f32.const 0x1.028f5cp+0 (;=1.01;)
          f32.mul
          local.tee $l12
          f32.store offset=88
          local.get $l15
          local.get $l12
          f32.store offset=84
          local.get $l15
          i32.const 0
          i32.store offset=76
          local.get $l15
          local.get $l5
          f32.store offset=72
          local.get $l15
          local.get $l6
          f32.store offset=68
          local.get $l15
          i32.const 0
          i32.store offset=60
          local.get $l15
          local.get $l6
          f32.store offset=56
          local.get $l15
          local.get $l4
          f32.store offset=52
          local.get $l15
          local.get $l5
          local.get $l5
          f32.neg
          local.tee $l13
          local.get $l5
          local.get $l13
          f32.gt
          select
          local.tee $l13
          f32.store offset=120
          local.get $l15
          local.get $l6
          local.get $l6
          f32.neg
          local.tee $l10
          local.get $l6
          local.get $l10
          f32.gt
          select
          local.tee $l10
          f32.store offset=116
          local.get $l15
          local.get $l10
          f32.store offset=104
          local.get $l15
          local.get $l4
          local.get $l4
          f32.neg
          local.tee $l10
          local.get $l4
          local.get $l10
          f32.gt
          select
          local.tee $l10
          f32.store offset=100
          local.get $l15
          local.get $l12
          f32.store offset=80
          local.get $l15
          local.get $l4
          f32.store offset=64
          local.get $l15
          local.get $l5
          f32.store offset=48
          local.get $l15
          local.get $l10
          f32.store offset=112
          local.get $l15
          local.get $l13
          f32.store offset=96
          local.get $l15
          i32.const 0
          i32.store offset=156
          local.get $l15
          i32.const 0
          i32.store offset=140
          local.get $l15
          local.get $l9
          block $B16 (result f32)
            local.get $l11
            local.get $l11
            f32.add
            local.tee $l11
            f32.const 0x1.fffffep+127 (;=3.40282e+38;)
            f32.ge
            if $I17
              local.get $l8
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
              local.get $l7
              f32.const 0x1.fffffep+127 (;=3.40282e+38;)
              f32.const -0x1.fffffep+127 (;=-3.40282e+38;)
              local.get $l5
              f32.const 0x0p+0 (;=0;)
              f32.ge
              select
              local.get $l5
              f32.const 0x0p+0 (;=0;)
              f32.eq
              select
              local.set $l5
              local.get $l9
              local.get $l6
              f32.const 0x0p+0 (;=0;)
              f32.eq
              br_if $B16
              drop
              f32.const 0x1.fffffep+127 (;=3.40282e+38;)
              f32.const -0x1.fffffep+127 (;=-3.40282e+38;)
              local.get $l6
              f32.const 0x0p+0 (;=0;)
              f32.ge
              select
              br $B16
            end
            local.get $l8
            local.get $l11
            local.get $l4
            f32.mul
            f32.add
            local.set $l4
            local.get $l7
            local.get $l11
            local.get $l5
            f32.mul
            f32.add
            local.set $l5
            local.get $l9
            local.get $l11
            local.get $l6
            f32.mul
            f32.add
          end
          local.tee $l6
          local.get $l6
          local.get $l9
          f32.lt
          select
          f32.store offset=152
          local.get $l15
          local.get $l8
          local.get $l4
          local.get $l4
          local.get $l8
          f32.lt
          select
          f32.store offset=148
          local.get $l15
          local.get $l9
          local.get $l6
          local.get $l6
          local.get $l9
          f32.gt
          select
          f32.store offset=136
          local.get $l15
          local.get $l8
          local.get $l4
          local.get $l4
          local.get $l8
          f32.gt
          select
          f32.store offset=132
          local.get $l15
          local.get $l7
          local.get $l5
          local.get $l5
          local.get $l7
          f32.lt
          select
          f32.store offset=144
          local.get $l15
          local.get $l7
          local.get $l5
          local.get $l5
          local.get $l7
          f32.gt
          select
          f32.store offset=128
          local.get $l15
          local.get $p3
          i32.load16_u
          i32.store16 offset=28
          local.get $l15
          local.get $p2
          i32.store offset=24
          local.get $l15
          local.get $p1
          i32.store offset=20
          local.get $l15
          i32.const 3178100
          i32.store offset=16
          local.get $p0
          i32.load offset=644
          local.set $l21
          local.get $p0
          i32.load offset=640
          local.set $l22
          local.get $l15
          i32.const 32
          i32.add
          local.set $p2
          local.get $l15
          i32.const 16
          i32.add
          local.set $l18
          i32.const 0
          local.set $l16
          global.get $g0
          i32.const 1056
          i32.sub
          local.tee $p3
          global.set $g0
          local.get $p3
          i32.const 1
          i32.store8 offset=1040
          local.get $p3
          i64.const 1099511628032
          i64.store offset=1048
          local.get $p3
          local.get $p3
          i32.const 16
          i32.add
          i32.store offset=1044
          local.get $p3
          local.get $l14
          i32.load offset=588
          i32.store offset=16
          loop $L18
            local.get $p3
            i32.load offset=1044
            local.get $l16
            i32.const 2
            i32.shl
            i32.add
            i32.load
            local.tee $l14
            f32.load offset=16
            local.tee $l5
            local.get $l14
            f32.load
            local.tee $l4
            f32.add
            local.set $l6
            local.get $l5
            local.get $l4
            f32.sub
            local.set $l5
            local.get $l14
            f32.load offset=24
            local.tee $l4
            local.get $l14
            f32.load offset=8
            local.tee $l9
            f32.add
            local.set $l10
            local.get $l14
            f32.load offset=20
            local.tee $l8
            local.get $l14
            f32.load offset=4
            local.tee $l11
            f32.add
            local.set $l7
            local.get $l4
            local.get $l9
            f32.sub
            local.set $l12
            local.get $l8
            local.get $l11
            f32.sub
            local.set $l4
            loop $L19
              block $B20
                block $B21
                  block $B22
                    local.get $l5
                    f32.const 0x1p-1 (;=0.5;)
                    f32.mul
                    local.get $p2
                    f32.load offset=48
                    f32.add
                    local.tee $l5
                    local.get $p2
                    f32.load offset=80
                    f32.mul
                    local.get $l4
                    f32.const 0x1p-1 (;=0.5;)
                    f32.mul
                    local.get $p2
                    f32.load offset=52
                    f32.add
                    local.tee $l4
                    local.get $p2
                    f32.load offset=64
                    f32.mul
                    f32.add
                    local.get $p2
                    f32.load offset=4
                    local.get $l7
                    f32.const 0x1p-1 (;=0.5;)
                    f32.mul
                    local.tee $l9
                    f32.sub
                    local.tee $l11
                    local.get $p2
                    f32.load offset=16
                    f32.mul
                    local.get $p2
                    f32.load
                    local.get $l6
                    f32.const 0x1p-1 (;=0.5;)
                    f32.mul
                    local.tee $l7
                    f32.sub
                    local.tee $l13
                    local.get $p2
                    f32.load offset=32
                    f32.mul
                    f32.sub
                    local.tee $l6
                    local.get $l6
                    f32.neg
                    local.tee $l8
                    local.get $l6
                    local.get $l8
                    f32.gt
                    select
                    f32.ge
                    i32.eqz
                    br_if $B22
                    local.get $p2
                    f32.load offset=96
                    local.get $l7
                    local.get $l5
                    f32.add
                    f32.le
                    i32.eqz
                    br_if $B22
                    local.get $p2
                    f32.load offset=112
                    local.get $l7
                    local.get $l5
                    f32.sub
                    f32.ge
                    i32.eqz
                    br_if $B22
                    local.get $l4
                    local.get $p2
                    f32.load offset=84
                    f32.mul
                    local.get $l12
                    f32.const 0x1p-1 (;=0.5;)
                    f32.mul
                    local.get $p2
                    f32.load offset=56
                    f32.add
                    local.tee $l6
                    local.get $p2
                    f32.load offset=68
                    f32.mul
                    f32.add
                    local.get $p2
                    f32.load offset=8
                    local.get $l10
                    f32.const 0x1p-1 (;=0.5;)
                    f32.mul
                    local.tee $l8
                    f32.sub
                    local.tee $l12
                    local.get $p2
                    f32.load offset=20
                    f32.mul
                    local.get $l11
                    local.get $p2
                    f32.load offset=36
                    f32.mul
                    f32.sub
                    local.tee $l7
                    local.get $l7
                    f32.neg
                    local.tee $l10
                    local.get $l7
                    local.get $l10
                    f32.gt
                    select
                    f32.ge
                    i32.eqz
                    br_if $B22
                    local.get $p2
                    f32.load offset=100
                    local.get $l9
                    local.get $l4
                    f32.add
                    f32.le
                    i32.eqz
                    br_if $B22
                    local.get $p2
                    f32.load offset=116
                    local.get $l9
                    local.get $l4
                    f32.sub
                    f32.ge
                    i32.eqz
                    br_if $B22
                    local.get $l6
                    local.get $p2
                    f32.load offset=88
                    f32.mul
                    local.get $l5
                    local.get $p2
                    f32.load offset=72
                    f32.mul
                    f32.add
                    local.get $l13
                    local.get $p2
                    f32.load offset=24
                    f32.mul
                    local.get $l12
                    local.get $p2
                    f32.load offset=40
                    f32.mul
                    f32.sub
                    local.tee $l5
                    local.get $l5
                    f32.neg
                    local.tee $l4
                    local.get $l4
                    local.get $l5
                    f32.lt
                    select
                    f32.ge
                    i32.eqz
                    br_if $B22
                    local.get $p2
                    f32.load offset=104
                    local.get $l8
                    local.get $l6
                    f32.add
                    f32.le
                    i32.eqz
                    br_if $B22
                    local.get $p2
                    f32.load offset=120
                    local.get $l8
                    local.get $l6
                    f32.sub
                    f32.ge
                    i32.eqz
                    br_if $B22
                    local.get $l14
                    i32.load offset=40
                    br_if $B21
                    local.get $l14
                    i32.load offset=36
                    local.tee $l14
                    i32.load
                    local.tee $p0
                    i32.eqz
                    br_if $B22
                    local.get $l14
                    i32.const 4
                    i32.add
                    local.set $l14
                    local.get $p0
                    local.set $p1
                    loop $L23
                      local.get $l14
                      i32.load
                      local.set $l20
                      block $B24
                        local.get $p0
                        i32.const 2
                        i32.ge_u
                        if $I25
                          local.get $l22
                          local.get $l20
                          i32.const 24
                          i32.mul
                          i32.add
                          local.tee $l17
                          f32.load offset=12
                          local.tee $l6
                          local.get $l17
                          f32.load
                          local.tee $l7
                          f32.sub
                          f32.const 0x1p-1 (;=0.5;)
                          f32.mul
                          local.get $p2
                          f32.load offset=48
                          f32.add
                          local.tee $l5
                          local.get $p2
                          f32.load offset=80
                          f32.mul
                          local.get $l17
                          f32.load offset=16
                          local.tee $l9
                          local.get $l17
                          f32.load offset=4
                          local.tee $l8
                          f32.sub
                          f32.const 0x1p-1 (;=0.5;)
                          f32.mul
                          local.get $p2
                          f32.load offset=52
                          f32.add
                          local.tee $l4
                          local.get $p2
                          f32.load offset=64
                          f32.mul
                          f32.add
                          local.get $p2
                          f32.load offset=4
                          local.get $l8
                          local.get $l9
                          f32.add
                          f32.const 0x1p-1 (;=0.5;)
                          f32.mul
                          local.tee $l9
                          f32.sub
                          local.tee $l10
                          local.get $p2
                          f32.load offset=16
                          f32.mul
                          local.get $p2
                          f32.load
                          local.get $l7
                          local.get $l6
                          f32.add
                          f32.const 0x1p-1 (;=0.5;)
                          f32.mul
                          local.tee $l7
                          f32.sub
                          local.tee $l12
                          local.get $p2
                          f32.load offset=32
                          f32.mul
                          f32.sub
                          local.tee $l6
                          local.get $l6
                          f32.neg
                          local.tee $l8
                          local.get $l6
                          local.get $l8
                          f32.gt
                          select
                          f32.ge
                          i32.eqz
                          br_if $B24
                          local.get $p2
                          f32.load offset=96
                          local.get $l7
                          local.get $l5
                          f32.add
                          f32.le
                          i32.eqz
                          br_if $B24
                          local.get $p2
                          f32.load offset=112
                          local.get $l7
                          local.get $l5
                          f32.sub
                          f32.ge
                          i32.eqz
                          br_if $B24
                          local.get $l4
                          local.get $p2
                          f32.load offset=84
                          f32.mul
                          local.get $l17
                          f32.load offset=20
                          local.tee $l7
                          local.get $l17
                          f32.load offset=8
                          local.tee $l8
                          f32.sub
                          f32.const 0x1p-1 (;=0.5;)
                          f32.mul
                          local.get $p2
                          f32.load offset=56
                          f32.add
                          local.tee $l6
                          local.get $p2
                          f32.load offset=68
                          f32.mul
                          f32.add
                          local.get $p2
                          f32.load offset=8
                          local.get $l8
                          local.get $l7
                          f32.add
                          f32.const 0x1p-1 (;=0.5;)
                          f32.mul
                          local.tee $l8
                          f32.sub
                          local.tee $l11
                          local.get $p2
                          f32.load offset=20
                          f32.mul
                          local.get $l10
                          local.get $p2
                          f32.load offset=36
                          f32.mul
                          f32.sub
                          local.tee $l7
                          local.get $l7
                          f32.neg
                          local.tee $l10
                          local.get $l7
                          local.get $l10
                          f32.gt
                          select
                          f32.ge
                          i32.eqz
                          br_if $B24
                          local.get $p2
                          f32.load offset=100
                          local.get $l9
                          local.get $l4
                          f32.add
                          f32.le
                          i32.eqz
                          br_if $B24
                          local.get $p2
                          f32.load offset=116
                          local.get $l9
                          local.get $l4
                          f32.sub
                          f32.ge
                          i32.eqz
                          br_if $B24
                          local.get $l6
                          local.get $p2
                          f32.load offset=88
                          f32.mul
                          local.get $l5
                          local.get $p2
                          f32.load offset=72
                          f32.mul
                          f32.add
                          local.get $l12
                          local.get $p2
                          f32.load offset=24
                          f32.mul
                          local.get $l11
                          local.get $p2
                          f32.load offset=40
                          f32.mul
                          f32.sub
                          local.tee $l5
                          local.get $l5
                          f32.neg
                          local.tee $l4
                          local.get $l4
                          local.get $l5
                          f32.lt
                          select
                          f32.ge
                          i32.eqz
                          br_if $B24
                          local.get $p2
                          f32.load offset=104
                          local.get $l8
                          local.get $l6
                          f32.add
                          f32.le
                          i32.eqz
                          br_if $B24
                          local.get $p2
                          f32.load offset=120
                          local.get $l8
                          local.get $l6
                          f32.sub
                          f32.ge
                          i32.eqz
                          br_if $B24
                        end
                        local.get $l18
                        local.get $p3
                        i32.const 12
                        i32.add
                        local.get $l21
                        local.get $l20
                        i32.const 44
                        i32.mul
                        i32.add
                        local.get $l18
                        i32.load
                        i32.load offset=8
                        call_indirect $__indirect_function_table (type $t3)
                        i32.eqz
                        br_if $B20
                      end
                      local.get $l14
                      i32.const 4
                      i32.add
                      local.set $l14
                      local.get $p1
                      i32.const 1
                      i32.sub
                      local.tee $p1
                      br_if $L23
                    end
                  end
                  local.get $l16
                  i32.eqz
                  local.set $l19
                  local.get $l16
                  i32.eqz
                  br_if $B20
                  local.get $l16
                  i32.const 1
                  i32.sub
                  local.set $l16
                  br $L18
                end
                local.get $p3
                i32.load offset=1044
                local.get $l16
                i32.const 2
                i32.shl
                i32.add
                local.get $l14
                i32.load offset=36
                local.tee $l14
                i32.const 48
                i32.add
                i32.store
                local.get $l16
                i32.const 1
                i32.add
                local.tee $l16
                local.get $p3
                i32.load offset=1052
                i32.const 2147483647
                i32.and
                i32.eq
                if $I26
                  local.get $p3
                  i32.const 16
                  i32.add
                  local.get $l16
                  i32.const 1
                  i32.shl
                  call $f71848
                end
                local.get $l14
                f32.load offset=16
                local.tee $l5
                local.get $l14
                f32.load
                local.tee $l4
                f32.add
                local.set $l6
                local.get $l5
                local.get $l4
                f32.sub
                local.set $l5
                local.get $l14
                f32.load offset=24
                local.tee $l4
                local.get $l14
                f32.load offset=8
                local.tee $l9
                f32.add
                local.set $l10
                local.get $l14
                f32.load offset=20
                local.tee $l8
                local.get $l14
                f32.load offset=4
                local.tee $l11
                f32.add
                local.set $l7
                local.get $l4
                local.get $l9
                f32.sub
                local.set $l12
                local.get $l8
                local.get $l11
                f32.sub
                local.set $l4
                br $L19
              end
            end
          end
          block $B27
            local.get $p3
            i32.load offset=1052
            local.tee $p2
            i32.const 0
            i32.lt_s
            br_if $B27
            local.get $p2
            i32.const 2147483647
            i32.and
            i32.eqz
            br_if $B27
            local.get $p3
            i32.load offset=1044
            local.tee $p2
            local.get $p3
            i32.const 16
            i32.add
            i32.eq
            br_if $B27
            local.get $p2
            i32.eqz
            br_if $B27
            call $f69753
            local.tee $l14
            local.get $p2
            local.get $l14
            i32.load
            i32.load offset=12
            call_indirect $__indirect_function_table (type $t1)
          end
          local.get $p3
          i32.const 1056
          i32.add
          global.set $g0
          local.get $l19
          local.set $l16
          br $B0
        end
        local.get $p1
        f32.load offset=112
        local.set $l4
        local.get $p1
        f32.load offset=108
        local.set $l5
        local.get $p1
        i64.load offset=100 align=4
        local.set $l23
        local.get $l15
        i32.const 0
        i32.store offset=44
        local.get $l15
        local.get $l5
        f32.store offset=40
        local.get $l15
        local.get $l23
        i64.store offset=32
        local.get $l15
        local.get $l4
        local.get $l4
        f32.mul
        f32.store offset=48
        local.get $l15
        local.get $p3
        i32.load16_u
        i32.store16 offset=28
        local.get $l15
        local.get $p2
        i32.store offset=24
        local.get $l15
        local.get $p1
        i32.store offset=20
        local.get $l15
        i32.const 3178120
        i32.store offset=16
        local.get $p0
        i32.load offset=644
        local.set $l21
        local.get $p0
        i32.load offset=640
        local.set $l22
        local.get $l15
        i32.const 32
        i32.add
        local.set $p3
        local.get $l15
        i32.const 16
        i32.add
        local.set $l18
        i32.const 0
        local.set $l16
        global.get $g0
        i32.const 1056
        i32.sub
        local.tee $p2
        global.set $g0
        local.get $p2
        i32.const 1
        i32.store8 offset=1040
        local.get $p2
        i64.const 1099511628032
        i64.store offset=1048
        local.get $p2
        local.get $p2
        i32.const 16
        i32.add
        i32.store offset=1044
        local.get $p2
        local.get $l14
        i32.load offset=588
        i32.store offset=16
        loop $L28
          local.get $p2
          i32.load offset=1044
          local.get $l16
          i32.const 2
          i32.shl
          i32.add
          i32.load
          local.tee $l14
          f32.load offset=16
          local.tee $l5
          local.get $l14
          f32.load
          local.tee $l6
          f32.add
          local.set $l4
          local.get $l5
          local.get $l6
          f32.sub
          local.set $l5
          local.get $l14
          f32.load offset=24
          local.tee $l7
          local.get $l14
          f32.load offset=8
          local.tee $l8
          f32.add
          local.set $l6
          local.get $l14
          f32.load offset=20
          local.tee $l9
          local.get $l14
          f32.load offset=4
          local.tee $l10
          f32.add
          local.set $l11
          local.get $l7
          local.get $l8
          f32.sub
          local.set $l7
          local.get $l9
          local.get $l10
          f32.sub
          local.set $l8
          loop $L29
            block $B30
              block $B31
                block $B32
                  local.get $p3
                  f32.load offset=16
                  local.get $p3
                  f32.load
                  local.get $l4
                  f32.const 0x1p-1 (;=0.5;)
                  f32.mul
                  f32.sub
                  local.tee $l4
                  local.get $l4
                  local.get $l5
                  f32.const 0x1p-1 (;=0.5;)
                  f32.mul
                  local.tee $l5
                  local.get $l4
                  local.get $l5
                  f32.lt
                  select
                  local.tee $l4
                  local.get $l5
                  f32.neg
                  local.tee $l5
                  local.get $l4
                  local.get $l5
                  f32.gt
                  select
                  f32.sub
                  local.tee $l4
                  local.get $l4
                  f32.mul
                  local.get $p3
                  f32.load offset=4
                  local.get $l11
                  f32.const 0x1p-1 (;=0.5;)
                  f32.mul
                  f32.sub
                  local.tee $l4
                  local.get $l4
                  local.get $l8
                  f32.const 0x1p-1 (;=0.5;)
                  f32.mul
                  local.tee $l5
                  local.get $l4
                  local.get $l5
                  f32.lt
                  select
                  local.tee $l4
                  local.get $l5
                  f32.neg
                  local.tee $l5
                  local.get $l4
                  local.get $l5
                  f32.gt
                  select
                  f32.sub
                  local.tee $l4
                  local.get $l4
                  f32.mul
                  f32.add
                  local.get $p3
                  f32.load offset=8
                  local.get $l6
                  f32.const 0x1p-1 (;=0.5;)
                  f32.mul
                  f32.sub
                  local.tee $l4
                  local.get $l4
                  local.get $l7
                  f32.const 0x1p-1 (;=0.5;)
                  f32.mul
                  local.tee $l5
                  local.get $l4
                  local.get $l5
                  f32.lt
                  select
                  local.tee $l4
                  local.get $l5
                  f32.neg
                  local.tee $l5
                  local.get $l4
                  local.get $l5
                  f32.gt
                  select
                  f32.sub
                  local.tee $l4
                  local.get $l4
                  f32.mul
                  f32.add
                  f32.ge
                  i32.eqz
                  br_if $B32
                  local.get $l14
                  i32.load offset=40
                  br_if $B31
                  local.get $l14
                  i32.load offset=36
                  local.tee $l14
                  i32.load
                  local.tee $p0
                  i32.eqz
                  br_if $B32
                  local.get $l14
                  i32.const 4
                  i32.add
                  local.set $l14
                  local.get $p0
                  local.set $p1
                  loop $L33
                    local.get $l14
                    i32.load
                    local.set $l20
                    block $B34
                      local.get $p0
                      i32.const 2
                      i32.ge_u
                      if $I35
                        local.get $p3
                        f32.load offset=16
                        local.get $p3
                        f32.load
                        local.get $l22
                        local.get $l20
                        i32.const 24
                        i32.mul
                        i32.add
                        local.tee $l17
                        f32.load
                        local.tee $l5
                        local.get $l17
                        f32.load offset=12
                        local.tee $l6
                        f32.add
                        f32.const 0x1p-1 (;=0.5;)
                        f32.mul
                        f32.sub
                        local.tee $l4
                        local.get $l4
                        local.get $l6
                        local.get $l5
                        f32.sub
                        f32.const 0x1p-1 (;=0.5;)
                        f32.mul
                        local.tee $l5
                        local.get $l4
                        local.get $l5
                        f32.lt
                        select
                        local.tee $l4
                        local.get $l5
                        f32.neg
                        local.tee $l5
                        local.get $l4
                        local.get $l5
                        f32.gt
                        select
                        f32.sub
                        local.tee $l4
                        local.get $l4
                        f32.mul
                        local.get $p3
                        f32.load offset=4
                        local.get $l17
                        f32.load offset=4
                        local.tee $l5
                        local.get $l17
                        f32.load offset=16
                        local.tee $l6
                        f32.add
                        f32.const 0x1p-1 (;=0.5;)
                        f32.mul
                        f32.sub
                        local.tee $l4
                        local.get $l4
                        local.get $l6
                        local.get $l5
                        f32.sub
                        f32.const 0x1p-1 (;=0.5;)
                        f32.mul
                        local.tee $l5
                        local.get $l4
                        local.get $l5
                        f32.lt
                        select
                        local.tee $l4
                        local.get $l5
                        f32.neg
                        local.tee $l5
                        local.get $l4
                        local.get $l5
                        f32.gt
                        select
                        f32.sub
                        local.tee $l4
                        local.get $l4
                        f32.mul
                        f32.add
                        local.get $p3
                        f32.load offset=8
                        local.get $l17
                        f32.load offset=8
                        local.tee $l5
                        local.get $l17
                        f32.load offset=20
                        local.tee $l6
                        f32.add
                        f32.const 0x1p-1 (;=0.5;)
                        f32.mul
                        f32.sub
                        local.tee $l4
                        local.get $l4
                        local.get $l6
                        local.get $l5
                        f32.sub
                        f32.const 0x1p-1 (;=0.5;)
                        f32.mul
                        local.tee $l5
                        local.get $l4
                        local.get $l5
                        f32.lt
                        select
                        local.tee $l4
                        local.get $l5
                        f32.neg
                        local.tee $l5
                        local.get $l4
                        local.get $l5
                        f32.gt
                        select
                        f32.sub
                        local.tee $l4
                        local.get $l4
                        f32.mul
                        f32.add
                        f32.ge
                        i32.eqz
                        br_if $B34
                      end
                      local.get $l18
                      local.get $p2
                      i32.const 12
                      i32.add
                      local.get $l21
                      local.get $l20
                      i32.const 44
                      i32.mul
                      i32.add
                      local.get $l18
                      i32.load
                      i32.load offset=8
                      call_indirect $__indirect_function_table (type $t3)
                      i32.eqz
                      br_if $B30
                    end
                    local.get $l14
                    i32.const 4
                    i32.add
                    local.set $l14
                    local.get $p1
                    i32.const 1
                    i32.sub
                    local.tee $p1
                    br_if $L33
                  end
                end
                local.get $l16
                i32.eqz
                local.set $l19
                local.get $l16
                i32.eqz
                br_if $B30
                local.get $l16
                i32.const 1
                i32.sub
                local.set $l16
                br $L28
              end
              local.get $p2
              i32.load offset=1044
              local.get $l16
              i32.const 2
              i32.shl
              i32.add
              local.get $l14
              i32.load offset=36
              local.tee $l14
              i32.const 48
              i32.add
              i32.store
              local.get $l16
              i32.const 1
              i32.add
              local.tee $l16
              local.get $p2
              i32.load offset=1052
              i32.const 2147483647
              i32.and
              i32.eq
              if $I36
                local.get $p2
                i32.const 16
                i32.add
                local.get $l16
                i32.const 1
                i32.shl
                call $f71848
              end
              local.get $l14
              f32.load offset=16
              local.tee $l5
              local.get $l14
              f32.load
              local.tee $l6
              f32.add
              local.set $l4
              local.get $l5
              local.get $l6
              f32.sub
              local.set $l5
              local.get $l14
              f32.load offset=24
              local.tee $l7
              local.get $l14
              f32.load offset=8
              local.tee $l8
              f32.add
              local.set $l6
              local.get $l14
              f32.load offset=20
              local.tee $l9
              local.get $l14
              f32.load offset=4
              local.tee $l10
              f32.add
              local.set $l11
              local.get $l7
              local.get $l8
              f32.sub
              local.set $l7
              local.get $l9
              local.get $l10
              f32.sub
              local.set $l8
              br $L29
            end
          end
        end
        block $B37
          local.get $p2
          i32.load offset=1052
          local.tee $l14
          i32.const 0
          i32.lt_s
          br_if $B37
          local.get $l14
          i32.const 2147483647
          i32.and
          i32.eqz
          br_if $B37
          local.get $p2
          i32.load offset=1044
          local.tee $l14
          local.get $p2
          i32.const 16
          i32.add
          i32.eq
          br_if $B37
          local.get $l14
          i32.eqz
          br_if $B37
          call $f69753
          local.tee $p3
          local.get $l14
          local.get $p3
          i32.load
          i32.load offset=12
          call_indirect $__indirect_function_table (type $t1)
        end
        local.get $p2
        i32.const 1056
        i32.add
        global.set $g0
        local.get $l19
        local.set $l16
        br $B0
      end
      local.get $l15
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
      local.set $l16
      local.get $l15
      local.get $p3
      i32.load16_u
      i32.store16 offset=28
      local.get $l15
      local.get $p2
      i32.store offset=24
      local.get $l15
      local.get $p1
      i32.store offset=20
      local.get $l15
      i32.const 3178060
      i32.store offset=16
      local.get $p0
      i32.load offset=644
      local.get $p0
      i32.load offset=640
      local.get $l14
      local.get $l16
      local.get $l15
      i32.const 16
      i32.add
      call $f71851
      local.set $l16
    end
    local.get $l15
    i32.const 224
    i32.add
    global.set $g0
    local.get $l16)
