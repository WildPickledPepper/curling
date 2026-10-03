  (func $f71791 (type $t3) (param $p0 i32) (param $p1 i32) (param $p2 i32) (result i32)
    (local $l3 f32) (local $l4 f32) (local $l5 f32) (local $l6 f32) (local $l7 f32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 i32) (local $l17 i32) (local $l18 i32) (local $l19 i32) (local $l20 i32) (local $l21 i32) (local $l22 i32) (local $l23 i32) (local $l24 i32) (local $l25 i32) (local $l26 i32) (local $l27 i32) (local $l28 i32) (local $l29 i64)
    local.get $p0
    i32.const 7648
    i32.add
    i32.load8_u
    if $I0 (result i32)
      i32.const 1
    else
      local.get $p0
      i32.const 16
      i32.add
      local.set $l17
      global.get $g0
      i32.const 160
      i32.sub
      local.tee $p0
      global.set $g0
      local.get $p1
      i32.const 72
      i32.add
      local.set $l20
      i32.const 1
      local.set $l16
      block $B1
        block $B2
          block $B3
            block $B4
              block $B5
                local.get $p1
                i32.load16_u offset=98
                br_table $B3 $B1 $B4 $B5 $B2 $B1
              end
              local.get $p1
              i32.load16_u offset=96
              if $I6
                local.get $p1
                i64.load offset=48 align=4
                local.set $l29
                local.get $p1
                f32.load offset=56
                local.set $l5
                local.get $p0
                i32.const 0
                i32.store offset=28
                local.get $p0
                local.get $l5
                f32.store offset=24
                local.get $p0
                local.get $l29
                i64.store offset=16
                local.get $p1
                f32.load
                local.set $l5
                local.get $p1
                f32.load offset=4
                local.set $l13
                local.get $p1
                f32.load offset=8
                local.set $l14
                local.get $p0
                i32.const 0
                i32.store offset=12
                local.get $p0
                local.get $l14
                f32.store offset=8
                local.get $p0
                local.get $l13
                f32.store offset=4
                local.get $p0
                local.get $l5
                f32.store
                local.get $p1
                f32.load offset=24
                local.set $l6
                local.get $p1
                f32.load offset=36
                local.set $l7
                local.get $p1
                f32.load offset=16
                local.set $l4
                local.get $p1
                f32.load offset=28
                local.set $l8
                local.get $p1
                f32.load offset=40
                local.set $l9
                local.get $p1
                f32.load offset=20
                local.set $l10
                local.get $p1
                f32.load offset=32
                local.set $l11
                local.get $p1
                f32.load offset=44
                local.set $l12
                local.get $p1
                f32.load offset=12
                local.set $l15
                local.get $p0
                i32.const 0
                i32.store offset=140
                local.get $p0
                i32.const 0
                i32.store offset=124
                local.get $p0
                i32.const 0
                i32.store offset=108
                local.get $p0
                i32.const 0
                i32.store offset=92
                local.get $p0
                i32.const 0
                i32.store offset=76
                local.get $p0
                local.get $l12
                f32.store offset=72
                local.get $p0
                local.get $l11
                f32.store offset=68
                local.get $p0
                i32.const -64
                i32.sub
                local.get $l10
                f32.store
                local.get $p0
                i32.const 0
                i32.store offset=60
                local.get $p0
                local.get $l9
                f32.store offset=56
                local.get $p0
                local.get $l8
                f32.store offset=52
                local.get $p0
                local.get $l4
                f32.store offset=48
                local.get $p0
                i32.const 0
                i32.store offset=44
                local.get $p0
                local.get $l7
                f32.store offset=40
                local.get $p0
                local.get $l6
                f32.store offset=36
                local.get $p0
                local.get $l12
                local.get $l12
                f32.neg
                local.tee $l3
                local.get $l3
                local.get $l12
                f32.lt
                select
                f32.const 0x1.0c6f7ap-20 (;=1e-06;)
                f32.add
                local.tee $l12
                f32.store offset=120
                local.get $p0
                local.get $l11
                local.get $l11
                f32.neg
                local.tee $l3
                local.get $l3
                local.get $l11
                f32.lt
                select
                f32.const 0x1.0c6f7ap-20 (;=1e-06;)
                f32.add
                local.tee $l11
                f32.store offset=116
                local.get $p0
                local.get $l10
                local.get $l10
                f32.neg
                local.tee $l3
                local.get $l3
                local.get $l10
                f32.lt
                select
                f32.const 0x1.0c6f7ap-20 (;=1e-06;)
                f32.add
                local.tee $l10
                f32.store offset=112
                local.get $p0
                local.get $l9
                local.get $l9
                f32.neg
                local.tee $l3
                local.get $l3
                local.get $l9
                f32.lt
                select
                f32.const 0x1.0c6f7ap-20 (;=1e-06;)
                f32.add
                local.tee $l9
                f32.store offset=104
                local.get $p0
                local.get $l8
                local.get $l8
                f32.neg
                local.tee $l3
                local.get $l3
                local.get $l8
                f32.lt
                select
                f32.const 0x1.0c6f7ap-20 (;=1e-06;)
                f32.add
                local.tee $l8
                f32.store offset=100
                local.get $p0
                local.get $l4
                local.get $l4
                f32.neg
                local.tee $l3
                local.get $l3
                local.get $l4
                f32.lt
                select
                f32.const 0x1.0c6f7ap-20 (;=1e-06;)
                f32.add
                local.tee $l4
                f32.store offset=96
                local.get $p0
                local.get $l7
                local.get $l7
                f32.neg
                local.tee $l3
                local.get $l3
                local.get $l7
                f32.lt
                select
                f32.const 0x1.0c6f7ap-20 (;=1e-06;)
                f32.add
                local.tee $l7
                f32.store offset=88
                local.get $p0
                local.get $l6
                local.get $l6
                f32.neg
                local.tee $l3
                local.get $l3
                local.get $l6
                f32.lt
                select
                f32.const 0x1.0c6f7ap-20 (;=1e-06;)
                f32.add
                local.tee $l6
                f32.store offset=84
                local.get $p0
                local.get $l5
                local.get $l10
                f32.mul
                local.get $l13
                local.get $l11
                f32.mul
                f32.add
                local.get $l14
                local.get $l12
                f32.mul
                f32.add
                f32.store offset=136
                local.get $p0
                local.get $l5
                local.get $l4
                f32.mul
                local.get $l13
                local.get $l8
                f32.mul
                f32.add
                local.get $l14
                local.get $l9
                f32.mul
                f32.add
                f32.store offset=132
                local.get $p0
                local.get $l15
                f32.store offset=32
                local.get $p0
                local.get $l15
                local.get $l15
                f32.neg
                local.tee $l4
                local.get $l4
                local.get $l15
                f32.lt
                select
                f32.const 0x1.0c6f7ap-20 (;=1e-06;)
                f32.add
                local.tee $l4
                f32.store offset=80
                local.get $p0
                local.get $l5
                local.get $l4
                f32.mul
                local.get $l13
                local.get $l6
                f32.mul
                f32.add
                local.get $l14
                local.get $l7
                f32.mul
                f32.add
                f32.store offset=128
                local.get $l17
                local.get $p0
                local.get $p2
                local.get $l20
                call $f71780
                local.set $l16
                br $B1
              end
              local.get $p0
              local.get $p1
              f32.load offset=72
              f32.store
              local.get $p0
              local.get $p1
              f32.load offset=76
              f32.store offset=4
              local.get $p0
              local.get $p1
              f32.load offset=80
              f32.store offset=8
              local.get $p0
              local.get $p1
              f32.load offset=84
              f32.store offset=12
              local.get $p0
              local.get $p1
              f32.load offset=88
              f32.store offset=16
              local.get $p0
              local.get $p1
              f32.load offset=92
              f32.store offset=20
              i32.const 0
              local.set $p1
              global.get $g0
              i32.const 16
              i32.sub
              local.tee $l21
              global.set $g0
              block $B7
                local.get $l17
                i32.load offset=28
                local.tee $l18
                if $I8
                  loop $L9
                    block $B10
                      local.get $p0
                      f32.load
                      local.get $l17
                      local.get $p1
                      i32.const 24
                      i32.mul
                      i32.add
                      local.tee $l16
                      f32.load offset=172
                      f32.gt
                      br_if $B10
                      local.get $l16
                      f32.load offset=160
                      local.get $p0
                      f32.load offset=12
                      f32.gt
                      br_if $B10
                      local.get $p0
                      f32.load offset=4
                      local.get $l16
                      f32.load offset=176
                      f32.gt
                      br_if $B10
                      local.get $l16
                      f32.load offset=164
                      local.get $p0
                      f32.load offset=16
                      f32.gt
                      br_if $B10
                      local.get $p0
                      f32.load offset=8
                      local.get $l16
                      f32.load offset=180
                      f32.gt
                      br_if $B10
                      local.get $l16
                      f32.load offset=168
                      local.get $p0
                      f32.load offset=20
                      f32.gt
                      br_if $B10
                      local.get $l21
                      i32.const -1082130432
                      i32.store offset=8
                      local.get $p2
                      local.get $l21
                      i32.const 8
                      i32.add
                      local.get $l17
                      local.get $p1
                      i32.const 3
                      i32.shl
                      i32.add
                      i32.const 32
                      i32.add
                      local.get $p2
                      i32.load
                      i32.load
                      call_indirect $__indirect_function_table (type $t3)
                      i32.eqz
                      if $I11
                        i32.const 0
                        local.set $p1
                        br $B7
                      end
                      local.get $l17
                      i32.load offset=28
                      local.set $l18
                    end
                    local.get $p1
                    i32.const 1
                    i32.add
                    local.tee $p1
                    local.get $l18
                    i32.lt_u
                    br_if $L9
                  end
                end
                i32.const 1
                local.set $p1
                local.get $l17
                i32.load offset=636
                i32.eqz
                br_if $B7
                local.get $p0
                f32.load
                local.get $l17
                f32.load offset=656
                local.tee $l3
                local.get $l17
                f32.load offset=672
                local.tee $l4
                f32.add
                f32.gt
                br_if $B7
                local.get $p0
                f32.load offset=12
                local.get $l3
                local.get $l4
                f32.sub
                f32.lt
                br_if $B7
                local.get $p0
                f32.load offset=4
                local.get $l17
                f32.load offset=660
                local.tee $l3
                local.get $l17
                f32.load offset=676
                local.tee $l4
                f32.add
                f32.gt
                br_if $B7
                local.get $p0
                f32.load offset=16
                local.get $l3
                local.get $l4
                f32.sub
                f32.lt
                br_if $B7
                local.get $p0
                f32.load offset=8
                local.get $l17
                f32.load offset=664
                local.tee $l3
                local.get $l17
                f32.load offset=680
                local.tee $l4
                f32.add
                f32.gt
                br_if $B7
                local.get $p0
                f32.load offset=20
                local.get $l3
                local.get $l4
                f32.sub
                f32.lt
                br_if $B7
                local.get $l20
                local.get $l17
                i32.load offset=644
                i32.const 2
                i32.shl
                i32.add
                local.tee $l16
                i32.load
                local.tee $p1
                i32.const -2147483648
                i32.or
                local.get $p1
                i32.const -1
                i32.xor
                local.get $p1
                i32.const 0
                i32.ge_s
                select
                local.set $l25
                local.get $l16
                i32.load offset=12
                local.tee $p1
                i32.const -2147483648
                i32.or
                local.get $p1
                i32.const -1
                i32.xor
                local.get $p1
                i32.const 0
                i32.ge_s
                select
                local.set $l26
                i32.const 1
                local.set $l23
                loop $L12
                  block $B13
                    block $B14
                      local.get $l17
                      local.get $l19
                      i32.const 2
                      i32.shl
                      i32.add
                      local.tee $l16
                      i32.load offset=688
                      i32.eqz
                      br_if $B14
                      local.get $p0
                      f32.load
                      local.get $l17
                      local.get $l19
                      i32.const 5
                      i32.shl
                      i32.add
                      local.tee $p1
                      f32.load offset=736
                      local.tee $l3
                      local.get $p1
                      f32.load offset=752
                      local.tee $l4
                      f32.add
                      f32.gt
                      br_if $B14
                      local.get $p0
                      f32.load offset=12
                      local.get $l3
                      local.get $l4
                      f32.sub
                      f32.lt
                      br_if $B14
                      local.get $p0
                      f32.load offset=4
                      local.get $p1
                      f32.load offset=740
                      local.tee $l3
                      local.get $p1
                      f32.load offset=756
                      local.tee $l4
                      f32.add
                      f32.gt
                      br_if $B14
                      local.get $p0
                      f32.load offset=16
                      local.get $l3
                      local.get $l4
                      f32.sub
                      f32.lt
                      br_if $B14
                      local.get $p0
                      f32.load offset=8
                      local.get $p1
                      f32.load offset=744
                      local.tee $l3
                      local.get $p1
                      f32.load offset=760
                      local.tee $l4
                      f32.add
                      f32.gt
                      br_if $B14
                      local.get $p0
                      f32.load offset=20
                      local.get $l3
                      local.get $l4
                      f32.sub
                      f32.lt
                      br_if $B14
                      local.get $l16
                      i32.const 708
                      i32.add
                      local.set $l27
                      i32.const 0
                      local.set $l22
                      loop $L15
                        block $B16
                          local.get $l17
                          local.get $l19
                          i32.const 224
                          i32.mul
                          i32.add
                          local.tee $p1
                          local.get $l22
                          i32.const 2
                          i32.shl
                          i32.add
                          local.tee $l16
                          i32.load offset=912
                          i32.eqz
                          br_if $B16
                          local.get $p0
                          f32.load
                          local.get $p1
                          local.get $l22
                          i32.const 5
                          i32.shl
                          i32.add
                          local.tee $p1
                          f32.load offset=960
                          local.tee $l3
                          local.get $p1
                          f32.load offset=976
                          local.tee $l4
                          f32.add
                          f32.gt
                          br_if $B16
                          local.get $p0
                          f32.load offset=12
                          local.get $l3
                          local.get $l4
                          f32.sub
                          f32.lt
                          br_if $B16
                          local.get $p0
                          f32.load offset=4
                          local.get $p1
                          f32.load offset=964
                          local.tee $l3
                          local.get $p1
                          f32.load offset=980
                          local.tee $l4
                          f32.add
                          f32.gt
                          br_if $B16
                          local.get $p0
                          f32.load offset=16
                          local.get $l3
                          local.get $l4
                          f32.sub
                          f32.lt
                          br_if $B16
                          local.get $p0
                          f32.load offset=8
                          local.get $p1
                          f32.load offset=968
                          local.tee $l3
                          local.get $p1
                          f32.load offset=984
                          local.tee $l4
                          f32.add
                          f32.gt
                          br_if $B16
                          local.get $p0
                          f32.load offset=20
                          local.get $l3
                          local.get $l4
                          f32.sub
                          f32.lt
                          br_if $B16
                          local.get $l16
                          i32.const 932
                          i32.add
                          local.set $l28
                          i32.const 0
                          local.set $l20
                          i32.const 1
                          local.set $l24
                          loop $L17
                            block $B18
                              block $B19
                                local.get $l17
                                local.get $l19
                                i32.const 1120
                                i32.mul
                                i32.add
                                local.get $l22
                                i32.const 224
                                i32.mul
                                i32.add
                                local.tee $p1
                                local.get $l20
                                i32.const 2
                                i32.shl
                                i32.add
                                local.tee $l18
                                i32.const 2032
                                i32.add
                                i32.load
                                local.tee $l16
                                i32.eqz
                                br_if $B19
                                local.get $p0
                                f32.load
                                local.get $p1
                                local.get $l20
                                i32.const 5
                                i32.shl
                                i32.add
                                local.tee $p1
                                i32.const 2080
                                i32.add
                                f32.load
                                local.tee $l3
                                local.get $p1
                                i32.const 2096
                                i32.add
                                f32.load
                                local.tee $l4
                                f32.add
                                f32.gt
                                br_if $B19
                                local.get $p0
                                f32.load offset=12
                                local.get $l3
                                local.get $l4
                                f32.sub
                                f32.lt
                                br_if $B19
                                local.get $p0
                                f32.load offset=4
                                local.get $p1
                                i32.const 2084
                                i32.add
                                f32.load
                                local.tee $l3
                                local.get $p1
                                i32.const 2100
                                i32.add
                                f32.load
                                local.tee $l4
                                f32.add
                                f32.gt
                                br_if $B19
                                local.get $p0
                                f32.load offset=16
                                local.get $l3
                                local.get $l4
                                f32.sub
                                f32.lt
                                br_if $B19
                                local.get $p0
                                f32.load offset=8
                                local.get $p1
                                i32.const 2088
                                i32.add
                                f32.load
                                local.tee $l3
                                local.get $p1
                                i32.const 2104
                                i32.add
                                f32.load
                                local.tee $l4
                                f32.add
                                f32.gt
                                br_if $B19
                                local.get $p0
                                f32.load offset=20
                                local.get $l3
                                local.get $l4
                                f32.sub
                                f32.lt
                                br_if $B19
                                local.get $l17
                                i32.load offset=20
                                local.get $l18
                                i32.const 2052
                                i32.add
                                i32.load
                                local.get $l28
                                i32.load
                                local.get $l27
                                i32.load
                                i32.add
                                i32.add
                                local.tee $l18
                                i32.const 5
                                i32.shl
                                i32.add
                                local.set $p1
                                local.get $l17
                                i32.load offset=24
                                local.get $l18
                                i32.const 3
                                i32.shl
                                i32.add
                                local.set $l18
                                loop $L20
                                  block $B21
                                    local.get $p1
                                    i32.load offset=28
                                    local.get $l25
                                    i32.lt_u
                                    br_if $B21
                                    local.get $p1
                                    i32.load offset=12
                                    local.get $l26
                                    i32.gt_u
                                    br_if $B19
                                    local.get $p0
                                    f32.load
                                    local.get $p1
                                    f32.load
                                    local.tee $l3
                                    local.get $p1
                                    f32.load offset=16
                                    local.tee $l4
                                    f32.add
                                    f32.gt
                                    br_if $B21
                                    local.get $p0
                                    f32.load offset=12
                                    local.get $l3
                                    local.get $l4
                                    f32.sub
                                    f32.lt
                                    br_if $B21
                                    local.get $p0
                                    f32.load offset=4
                                    local.get $p1
                                    f32.load offset=4
                                    local.tee $l3
                                    local.get $p1
                                    f32.load offset=20
                                    local.tee $l4
                                    f32.add
                                    f32.gt
                                    br_if $B21
                                    local.get $p0
                                    f32.load offset=16
                                    local.get $l3
                                    local.get $l4
                                    f32.sub
                                    f32.lt
                                    br_if $B21
                                    local.get $p0
                                    f32.load offset=8
                                    local.get $p1
                                    f32.load offset=8
                                    local.tee $l3
                                    local.get $p1
                                    f32.load offset=24
                                    local.tee $l4
                                    f32.add
                                    f32.gt
                                    br_if $B21
                                    local.get $p0
                                    f32.load offset=20
                                    local.get $l3
                                    local.get $l4
                                    f32.sub
                                    f32.lt
                                    br_if $B21
                                    local.get $l21
                                    i32.const -1082130432
                                    i32.store offset=12
                                    local.get $p2
                                    local.get $l21
                                    i32.const 12
                                    i32.add
                                    local.get $l18
                                    local.get $p2
                                    i32.load
                                    i32.load
                                    call_indirect $__indirect_function_table (type $t3)
                                    i32.eqz
                                    br_if $B18
                                  end
                                  local.get $l18
                                  i32.const 8
                                  i32.add
                                  local.set $l18
                                  local.get $p1
                                  i32.const 32
                                  i32.add
                                  local.set $p1
                                  local.get $l16
                                  i32.const 1
                                  i32.sub
                                  local.tee $l16
                                  br_if $L20
                                end
                              end
                              local.get $l20
                              i32.const 4
                              i32.lt_u
                              local.set $l24
                              local.get $l20
                              i32.const 1
                              i32.add
                              local.tee $l20
                              i32.const 5
                              i32.ne
                              br_if $L17
                              br $B16
                            end
                          end
                          local.get $l24
                          br_if $B13
                        end
                        local.get $l22
                        i32.const 1
                        i32.add
                        local.tee $l22
                        i32.const 5
                        i32.ne
                        br_if $L15
                      end
                    end
                    local.get $l19
                    i32.const 4
                    i32.lt_u
                    local.set $l23
                    local.get $l19
                    i32.const 1
                    i32.add
                    local.tee $l19
                    i32.const 5
                    i32.ne
                    br_if $L12
                  end
                end
                local.get $l23
                i32.eqz
                local.set $p1
              end
              local.get $l21
              i32.const 16
              i32.add
              global.set $g0
              local.get $p1
              i32.const 1
              i32.and
              local.set $l16
              br $B1
            end
            local.get $p1
            i64.load offset=48 align=4
            local.set $l29
            local.get $p1
            f32.load offset=56
            local.set $l5
            local.get $p0
            i32.const 0
            i32.store offset=28
            local.get $p0
            local.get $l5
            f32.store offset=24
            local.get $p0
            local.get $l29
            i64.store offset=16
            local.get $p1
            f32.load
            local.set $l5
            local.get $p1
            f32.load offset=4
            local.set $l13
            local.get $p1
            f32.load offset=8
            local.set $l14
            local.get $p0
            i32.const 0
            i32.store offset=12
            local.get $p0
            local.get $l14
            f32.store offset=8
            local.get $p0
            local.get $l13
            f32.store offset=4
            local.get $p0
            local.get $l5
            f32.store
            local.get $p1
            f32.load offset=24
            local.set $l6
            local.get $p1
            f32.load offset=36
            local.set $l7
            local.get $p1
            f32.load offset=16
            local.set $l4
            local.get $p1
            f32.load offset=28
            local.set $l8
            local.get $p1
            f32.load offset=40
            local.set $l9
            local.get $p1
            f32.load offset=20
            local.set $l10
            local.get $p1
            f32.load offset=32
            local.set $l11
            local.get $p1
            f32.load offset=44
            local.set $l12
            local.get $p1
            f32.load offset=12
            local.set $l15
            local.get $p0
            i32.const 0
            i32.store offset=140
            local.get $p0
            i32.const 0
            i32.store offset=124
            local.get $p0
            i32.const 0
            i32.store offset=108
            local.get $p0
            i32.const 0
            i32.store offset=92
            local.get $p0
            i32.const 0
            i32.store offset=76
            local.get $p0
            local.get $l12
            f32.store offset=72
            local.get $p0
            local.get $l11
            f32.store offset=68
            local.get $p0
            i32.const -64
            i32.sub
            local.get $l10
            f32.store
            local.get $p0
            i32.const 0
            i32.store offset=60
            local.get $p0
            local.get $l9
            f32.store offset=56
            local.get $p0
            local.get $l8
            f32.store offset=52
            local.get $p0
            local.get $l4
            f32.store offset=48
            local.get $p0
            i32.const 0
            i32.store offset=44
            local.get $p0
            local.get $l7
            f32.store offset=40
            local.get $p0
            local.get $l6
            f32.store offset=36
            local.get $p0
            local.get $l12
            local.get $l12
            f32.neg
            local.tee $l3
            local.get $l3
            local.get $l12
            f32.lt
            select
            f32.const 0x1.0c6f7ap-20 (;=1e-06;)
            f32.add
            local.tee $l12
            f32.store offset=120
            local.get $p0
            local.get $l11
            local.get $l11
            f32.neg
            local.tee $l3
            local.get $l3
            local.get $l11
            f32.lt
            select
            f32.const 0x1.0c6f7ap-20 (;=1e-06;)
            f32.add
            local.tee $l11
            f32.store offset=116
            local.get $p0
            local.get $l10
            local.get $l10
            f32.neg
            local.tee $l3
            local.get $l3
            local.get $l10
            f32.lt
            select
            f32.const 0x1.0c6f7ap-20 (;=1e-06;)
            f32.add
            local.tee $l10
            f32.store offset=112
            local.get $p0
            local.get $l9
            local.get $l9
            f32.neg
            local.tee $l3
            local.get $l3
            local.get $l9
            f32.lt
            select
            f32.const 0x1.0c6f7ap-20 (;=1e-06;)
            f32.add
            local.tee $l9
            f32.store offset=104
            local.get $p0
            local.get $l8
            local.get $l8
            f32.neg
            local.tee $l3
            local.get $l3
            local.get $l8
            f32.lt
            select
            f32.const 0x1.0c6f7ap-20 (;=1e-06;)
            f32.add
            local.tee $l8
            f32.store offset=100
            local.get $p0
            local.get $l4
            local.get $l4
            f32.neg
            local.tee $l3
            local.get $l3
            local.get $l4
            f32.lt
            select
            f32.const 0x1.0c6f7ap-20 (;=1e-06;)
            f32.add
            local.tee $l4
            f32.store offset=96
            local.get $p0
            local.get $l7
            local.get $l7
            f32.neg
            local.tee $l3
            local.get $l3
            local.get $l7
            f32.lt
            select
            f32.const 0x1.0c6f7ap-20 (;=1e-06;)
            f32.add
            local.tee $l7
            f32.store offset=88
            local.get $p0
            local.get $l6
            local.get $l6
            f32.neg
            local.tee $l3
            local.get $l3
            local.get $l6
            f32.lt
            select
            f32.const 0x1.0c6f7ap-20 (;=1e-06;)
            f32.add
            local.tee $l6
            f32.store offset=84
            local.get $p0
            local.get $l5
            local.get $l10
            f32.mul
            local.get $l13
            local.get $l11
            f32.mul
            f32.add
            local.get $l14
            local.get $l12
            f32.mul
            f32.add
            f32.store offset=136
            local.get $p0
            local.get $l5
            local.get $l4
            f32.mul
            local.get $l13
            local.get $l8
            f32.mul
            f32.add
            local.get $l14
            local.get $l9
            f32.mul
            f32.add
            f32.store offset=132
            local.get $p0
            local.get $l15
            f32.store offset=32
            local.get $p0
            local.get $l15
            local.get $l15
            f32.neg
            local.tee $l4
            local.get $l4
            local.get $l15
            f32.lt
            select
            f32.const 0x1.0c6f7ap-20 (;=1e-06;)
            f32.add
            local.tee $l4
            f32.store offset=80
            local.get $p0
            local.get $l5
            local.get $l4
            f32.mul
            local.get $l13
            local.get $l6
            f32.mul
            f32.add
            local.get $l14
            local.get $l7
            f32.mul
            f32.add
            f32.store offset=128
            local.get $l17
            local.get $p0
            local.get $p2
            local.get $l20
            call $f71780
            local.set $l16
            br $B1
          end
          local.get $p1
          f32.load offset=108
          local.set $l5
          local.get $p1
          i64.load offset=100 align=4
          local.set $l29
          local.get $p0
          i32.const 0
          i32.store offset=12
          local.get $p0
          local.get $l5
          f32.store offset=8
          local.get $p0
          local.get $l29
          i64.store
          local.get $p0
          local.get $p1
          f32.load offset=112
          local.tee $l5
          local.get $l5
          f32.mul
          f32.store offset=16
          i32.const 0
          local.set $l16
          global.get $g0
          i32.const 16
          i32.sub
          local.tee $l21
          global.set $g0
          block $B22
            local.get $l17
            i32.load offset=28
            local.tee $l23
            if $I23
              loop $L24
                local.get $p0
                f32.load offset=16
                local.get $p0
                f32.load
                local.get $l17
                local.get $l16
                i32.const 24
                i32.mul
                i32.add
                local.tee $p1
                f32.load offset=160
                local.tee $l4
                local.get $p1
                f32.load offset=172
                local.tee $l5
                f32.add
                f32.const 0x1p-1 (;=0.5;)
                f32.mul
                f32.sub
                local.tee $l3
                local.get $l3
                local.get $l5
                local.get $l4
                f32.sub
                f32.const 0x1p-1 (;=0.5;)
                f32.mul
                local.tee $l4
                local.get $l3
                local.get $l4
                f32.lt
                select
                local.tee $l3
                local.get $l4
                f32.neg
                local.tee $l4
                local.get $l3
                local.get $l4
                f32.gt
                select
                f32.sub
                local.tee $l3
                local.get $l3
                f32.mul
                local.get $p0
                f32.load offset=4
                local.get $p1
                f32.load offset=164
                local.tee $l4
                local.get $p1
                f32.load offset=176
                local.tee $l5
                f32.add
                f32.const 0x1p-1 (;=0.5;)
                f32.mul
                f32.sub
                local.tee $l3
                local.get $l3
                local.get $l5
                local.get $l4
                f32.sub
                f32.const 0x1p-1 (;=0.5;)
                f32.mul
                local.tee $l4
                local.get $l3
                local.get $l4
                f32.lt
                select
                local.tee $l3
                local.get $l4
                f32.neg
                local.tee $l4
                local.get $l3
                local.get $l4
                f32.gt
                select
                f32.sub
                local.tee $l3
                local.get $l3
                f32.mul
                f32.add
                local.get $p0
                f32.load offset=8
                local.get $p1
                f32.load offset=168
                local.tee $l4
                local.get $p1
                f32.load offset=180
                local.tee $l5
                f32.add
                f32.const 0x1p-1 (;=0.5;)
                f32.mul
                f32.sub
                local.tee $l3
                local.get $l3
                local.get $l5
                local.get $l4
                f32.sub
                f32.const 0x1p-1 (;=0.5;)
                f32.mul
                local.tee $l4
                local.get $l3
                local.get $l4
                f32.lt
                select
                local.tee $l3
                local.get $l4
                f32.neg
                local.tee $l4
                local.get $l3
                local.get $l4
                f32.gt
                select
                f32.sub
                local.tee $l3
                local.get $l3
                f32.mul
                f32.add
                f32.ge
                if $I25
                  local.get $l21
                  i32.const -1082130432
                  i32.store offset=8
                  local.get $p2
                  local.get $l21
                  i32.const 8
                  i32.add
                  local.get $l17
                  local.get $l16
                  i32.const 3
                  i32.shl
                  i32.add
                  i32.const 32
                  i32.add
                  local.get $p2
                  i32.load
                  i32.load
                  call_indirect $__indirect_function_table (type $t3)
                  i32.eqz
                  if $I26
                    i32.const 0
                    local.set $p1
                    br $B22
                  end
                  local.get $l17
                  i32.load offset=28
                  local.set $l23
                end
                local.get $l16
                i32.const 1
                i32.add
                local.tee $l16
                local.get $l23
                i32.lt_u
                br_if $L24
              end
            end
            i32.const 1
            local.set $p1
            local.get $l17
            i32.load offset=636
            i32.eqz
            br_if $B22
            local.get $p0
            f32.load offset=16
            local.get $p0
            f32.load
            local.get $l17
            f32.load offset=656
            f32.sub
            local.tee $l3
            local.get $l3
            local.get $l17
            f32.load offset=672
            local.tee $l4
            local.get $l3
            local.get $l4
            f32.lt
            select
            local.tee $l3
            local.get $l4
            f32.neg
            local.tee $l4
            local.get $l3
            local.get $l4
            f32.gt
            select
            f32.sub
            local.tee $l3
            local.get $l3
            f32.mul
            local.get $p0
            f32.load offset=4
            local.get $l17
            f32.load offset=660
            f32.sub
            local.tee $l3
            local.get $l3
            local.get $l17
            f32.load offset=676
            local.tee $l4
            local.get $l3
            local.get $l4
            f32.lt
            select
            local.tee $l3
            local.get $l4
            f32.neg
            local.tee $l4
            local.get $l3
            local.get $l4
            f32.gt
            select
            f32.sub
            local.tee $l3
            local.get $l3
            f32.mul
            f32.add
            local.get $p0
            f32.load offset=8
            local.get $l17
            f32.load offset=664
            f32.sub
            local.tee $l3
            local.get $l3
            local.get $l17
            f32.load offset=680
            local.tee $l4
            local.get $l3
            local.get $l4
            f32.lt
            select
            local.tee $l3
            local.get $l4
            f32.neg
            local.tee $l4
            local.get $l3
            local.get $l4
            f32.gt
            select
            f32.sub
            local.tee $l3
            local.get $l3
            f32.mul
            f32.add
            f32.ge
            i32.eqz
            br_if $B22
            local.get $l20
            local.get $l17
            i32.load offset=644
            i32.const 2
            i32.shl
            i32.add
            local.tee $l16
            i32.load
            local.tee $p1
            i32.const -2147483648
            i32.or
            local.get $p1
            i32.const -1
            i32.xor
            local.get $p1
            i32.const 0
            i32.ge_s
            select
            local.set $l20
            local.get $l16
            i32.load offset=12
            local.tee $p1
            i32.const -2147483648
            i32.or
            local.get $p1
            i32.const -1
            i32.xor
            local.get $p1
            i32.const 0
            i32.ge_s
            select
            local.set $l26
            i32.const 1
            local.set $l24
            loop $L27
              block $B28
                block $B29
                  local.get $l17
                  local.get $l18
                  i32.const 2
                  i32.shl
                  i32.add
                  local.tee $l16
                  i32.load offset=688
                  i32.eqz
                  br_if $B29
                  local.get $p0
                  f32.load offset=16
                  local.get $p0
                  f32.load
                  local.get $l17
                  local.get $l18
                  i32.const 5
                  i32.shl
                  i32.add
                  local.tee $p1
                  f32.load offset=736
                  f32.sub
                  local.tee $l3
                  local.get $l3
                  local.get $p1
                  f32.load offset=752
                  local.tee $l4
                  local.get $l3
                  local.get $l4
                  f32.lt
                  select
                  local.tee $l3
                  local.get $l4
                  f32.neg
                  local.tee $l4
                  local.get $l3
                  local.get $l4
                  f32.gt
                  select
                  f32.sub
                  local.tee $l3
                  local.get $l3
                  f32.mul
                  local.get $p0
                  f32.load offset=4
                  local.get $p1
                  f32.load offset=740
                  f32.sub
                  local.tee $l3
                  local.get $l3
                  local.get $p1
                  f32.load offset=756
                  local.tee $l4
                  local.get $l3
                  local.get $l4
                  f32.lt
                  select
                  local.tee $l3
                  local.get $l4
                  f32.neg
                  local.tee $l4
                  local.get $l3
                  local.get $l4
                  f32.gt
                  select
                  f32.sub
                  local.tee $l3
                  local.get $l3
                  f32.mul
                  f32.add
                  local.get $p0
                  f32.load offset=8
                  local.get $p1
                  f32.load offset=744
                  f32.sub
                  local.tee $l3
                  local.get $l3
                  local.get $p1
                  f32.load offset=760
                  local.tee $l4
                  local.get $l3
                  local.get $l4
                  f32.lt
                  select
                  local.tee $l3
                  local.get $l4
                  f32.neg
                  local.tee $l4
                  local.get $l3
                  local.get $l4
                  f32.gt
                  select
                  f32.sub
                  local.tee $l3
                  local.get $l3
                  f32.mul
                  f32.add
                  f32.ge
                  i32.eqz
                  br_if $B29
                  local.get $l16
                  i32.const 708
                  i32.add
                  local.set $l27
                  i32.const 0
                  local.set $l19
                  loop $L30
                    block $B31
                      local.get $l17
                      local.get $l18
                      i32.const 224
                      i32.mul
                      i32.add
                      local.tee $p1
                      local.get $l19
                      i32.const 2
                      i32.shl
                      i32.add
                      local.tee $l16
                      i32.load offset=912
                      i32.eqz
                      br_if $B31
                      local.get $p0
                      f32.load offset=16
                      local.get $p0
                      f32.load
                      local.get $p1
                      local.get $l19
                      i32.const 5
                      i32.shl
                      i32.add
                      local.tee $p1
                      f32.load offset=960
                      f32.sub
                      local.tee $l3
                      local.get $l3
                      local.get $p1
                      f32.load offset=976
                      local.tee $l4
                      local.get $l3
                      local.get $l4
                      f32.lt
                      select
                      local.tee $l3
                      local.get $l4
                      f32.neg
                      local.tee $l4
                      local.get $l3
                      local.get $l4
                      f32.gt
                      select
                      f32.sub
                      local.tee $l3
                      local.get $l3
                      f32.mul
                      local.get $p0
                      f32.load offset=4
                      local.get $p1
                      f32.load offset=964
                      f32.sub
                      local.tee $l3
                      local.get $l3
                      local.get $p1
                      f32.load offset=980
                      local.tee $l4
                      local.get $l3
                      local.get $l4
                      f32.lt
                      select
                      local.tee $l3
                      local.get $l4
                      f32.neg
                      local.tee $l4
                      local.get $l3
                      local.get $l4
                      f32.gt
                      select
                      f32.sub
                      local.tee $l3
                      local.get $l3
                      f32.mul
                      f32.add
                      local.get $p0
                      f32.load offset=8
                      local.get $p1
                      f32.load offset=968
                      f32.sub
                      local.tee $l3
                      local.get $l3
                      local.get $p1
                      f32.load offset=984
                      local.tee $l4
                      local.get $l3
                      local.get $l4
                      f32.lt
                      select
                      local.tee $l3
                      local.get $l4
                      f32.neg
                      local.tee $l4
                      local.get $l3
                      local.get $l4
                      f32.gt
                      select
                      f32.sub
                      local.tee $l3
                      local.get $l3
                      f32.mul
                      f32.add
                      f32.ge
                      i32.eqz
                      br_if $B31
                      local.get $l16
                      i32.const 932
                      i32.add
                      local.set $l28
                      i32.const 0
                      local.set $l22
                      i32.const 1
                      local.set $l25
                      loop $L32
                        block $B33
                          block $B34
                            local.get $l17
                            local.get $l18
                            i32.const 1120
                            i32.mul
                            i32.add
                            local.get $l19
                            i32.const 224
                            i32.mul
                            i32.add
                            local.tee $p1
                            local.get $l22
                            i32.const 2
                            i32.shl
                            i32.add
                            local.tee $l16
                            i32.const 2032
                            i32.add
                            i32.load
                            local.tee $l23
                            i32.eqz
                            br_if $B34
                            local.get $p0
                            f32.load offset=16
                            local.get $p0
                            f32.load
                            local.get $p1
                            local.get $l22
                            i32.const 5
                            i32.shl
                            i32.add
                            local.tee $p1
                            i32.const 2080
                            i32.add
                            f32.load
                            f32.sub
                            local.tee $l3
                            local.get $l3
                            local.get $p1
                            i32.const 2096
                            i32.add
                            f32.load
                            local.tee $l4
                            local.get $l3
                            local.get $l4
                            f32.lt
                            select
                            local.tee $l3
                            local.get $l4
                            f32.neg
                            local.tee $l4
                            local.get $l3
                            local.get $l4
                            f32.gt
                            select
                            f32.sub
                            local.tee $l3
                            local.get $l3
                            f32.mul
                            local.get $p0
                            f32.load offset=4
                            local.get $p1
                            i32.const 2084
                            i32.add
                            f32.load
                            f32.sub
                            local.tee $l3
                            local.get $l3
                            local.get $p1
                            i32.const 2100
                            i32.add
                            f32.load
                            local.tee $l4
                            local.get $l3
                            local.get $l4
                            f32.lt
                            select
                            local.tee $l3
                            local.get $l4
                            f32.neg
                            local.tee $l4
                            local.get $l3
                            local.get $l4
                            f32.gt
                            select
                            f32.sub
                            local.tee $l3
                            local.get $l3
                            f32.mul
                            f32.add
                            local.get $p0
                            f32.load offset=8
                            local.get $p1
                            i32.const 2088
                            i32.add
                            f32.load
                            f32.sub
                            local.tee $l3
                            local.get $l3
                            local.get $p1
                            i32.const 2104
                            i32.add
                            f32.load
                            local.tee $l4
                            local.get $l3
                            local.get $l4
                            f32.lt
                            select
                            local.tee $l3
                            local.get $l4
                            f32.neg
                            local.tee $l4
                            local.get $l3
                            local.get $l4
                            f32.gt
                            select
                            f32.sub
                            local.tee $l3
                            local.get $l3
                            f32.mul
                            f32.add
                            f32.ge
                            i32.eqz
                            br_if $B34
                            local.get $l17
                            i32.load offset=20
                            local.get $l16
                            i32.const 2052
                            i32.add
                            i32.load
                            local.get $l28
                            i32.load
                            local.get $l27
                            i32.load
                            i32.add
                            i32.add
                            local.tee $l16
                            i32.const 5
                            i32.shl
                            i32.add
                            local.set $p1
                            local.get $l17
                            i32.load offset=24
                            local.get $l16
                            i32.const 3
                            i32.shl
                            i32.add
                            local.set $l16
                            loop $L35
                              block $B36
                                local.get $p1
                                i32.load offset=28
                                local.get $l20
                                i32.lt_u
                                br_if $B36
                                local.get $p1
                                i32.load offset=12
                                local.get $l26
                                i32.gt_u
                                br_if $B34
                                local.get $p0
                                f32.load offset=16
                                local.get $p0
                                f32.load
                                local.get $p1
                                f32.load
                                f32.sub
                                local.tee $l3
                                local.get $l3
                                local.get $p1
                                f32.load offset=16
                                local.tee $l4
                                local.get $l3
                                local.get $l4
                                f32.lt
                                select
                                local.tee $l3
                                local.get $l4
                                f32.neg
                                local.tee $l4
                                local.get $l3
                                local.get $l4
                                f32.gt
                                select
                                f32.sub
                                local.tee $l3
                                local.get $l3
                                f32.mul
                                local.get $p0
                                f32.load offset=4
                                local.get $p1
                                f32.load offset=4
                                f32.sub
                                local.tee $l3
                                local.get $l3
                                local.get $p1
                                f32.load offset=20
                                local.tee $l4
                                local.get $l3
                                local.get $l4
                                f32.lt
                                select
                                local.tee $l3
                                local.get $l4
                                f32.neg
                                local.tee $l4
                                local.get $l3
                                local.get $l4
                                f32.gt
                                select
                                f32.sub
                                local.tee $l3
                                local.get $l3
                                f32.mul
                                f32.add
                                local.get $p0
                                f32.load offset=8
                                local.get $p1
                                f32.load offset=8
                                f32.sub
                                local.tee $l3
                                local.get $l3
                                local.get $p1
                                f32.load offset=24
                                local.tee $l4
                                local.get $l3
                                local.get $l4
                                f32.lt
                                select
                                local.tee $l3
                                local.get $l4
                                f32.neg
                                local.tee $l4
                                local.get $l3
                                local.get $l4
                                f32.gt
                                select
                                f32.sub
                                local.tee $l3
                                local.get $l3
                                f32.mul
                                f32.add
                                f32.ge
                                i32.eqz
                                br_if $B36
                                local.get $l21
                                i32.const -1082130432
                                i32.store offset=12
                                local.get $p2
                                local.get $l21
                                i32.const 12
                                i32.add
                                local.get $l16
                                local.get $p2
                                i32.load
                                i32.load
                                call_indirect $__indirect_function_table (type $t3)
                                i32.eqz
                                br_if $B33
                              end
                              local.get $l16
                              i32.const 8
                              i32.add
                              local.set $l16
                              local.get $p1
                              i32.const 32
                              i32.add
                              local.set $p1
                              local.get $l23
                              i32.const 1
                              i32.sub
                              local.tee $l23
                              br_if $L35
                            end
                          end
                          local.get $l22
                          i32.const 4
                          i32.lt_u
                          local.set $l25
                          local.get $l22
                          i32.const 1
                          i32.add
                          local.tee $l22
                          i32.const 5
                          i32.ne
                          br_if $L32
                          br $B31
                        end
                      end
                      local.get $l25
                      br_if $B28
                    end
                    local.get $l19
                    i32.const 1
                    i32.add
                    local.tee $l19
                    i32.const 5
                    i32.ne
                    br_if $L30
                  end
                end
                local.get $l18
                i32.const 4
                i32.lt_u
                local.set $l24
                local.get $l18
                i32.const 1
                i32.add
                local.tee $l18
                i32.const 5
                i32.ne
                br_if $L27
              end
            end
            local.get $l24
            i32.eqz
            local.set $p1
          end
          local.get $l21
          i32.const 16
          i32.add
          global.set $g0
          local.get $p1
          i32.const 1
          i32.and
          local.set $l16
          br $B1
        end
        local.get $p1
        i64.load offset=48 align=4
        local.set $l29
        local.get $p1
        f32.load offset=56
        local.set $l5
        local.get $p0
        i32.const 0
        i32.store offset=28
        local.get $p0
        local.get $l5
        f32.store offset=24
        local.get $p0
        local.get $l29
        i64.store offset=16
        local.get $p1
        f32.load
        local.set $l5
        local.get $p1
        f32.load offset=4
        local.set $l13
        local.get $p1
        f32.load offset=8
        local.set $l14
        local.get $p0
        i32.const 0
        i32.store offset=12
        local.get $p0
        local.get $l14
        f32.store offset=8
        local.get $p0
        local.get $l13
        f32.store offset=4
        local.get $p0
        local.get $l5
        f32.store
        local.get $p1
        f32.load offset=24
        local.set $l6
        local.get $p1
        f32.load offset=36
        local.set $l7
        local.get $p1
        f32.load offset=16
        local.set $l4
        local.get $p1
        f32.load offset=28
        local.set $l8
        local.get $p1
        f32.load offset=40
        local.set $l9
        local.get $p1
        f32.load offset=20
        local.set $l10
        local.get $p1
        f32.load offset=32
        local.set $l11
        local.get $p1
        f32.load offset=44
        local.set $l12
        local.get $p1
        f32.load offset=12
        local.set $l15
        local.get $p0
        i32.const 0
        i32.store offset=140
        local.get $p0
        i32.const 0
        i32.store offset=124
        local.get $p0
        i32.const 0
        i32.store offset=108
        local.get $p0
        i32.const 0
        i32.store offset=92
        local.get $p0
        i32.const 0
        i32.store offset=76
        local.get $p0
        local.get $l12
        f32.store offset=72
        local.get $p0
        local.get $l11
        f32.store offset=68
        local.get $p0
        i32.const -64
        i32.sub
        local.get $l10
        f32.store
        local.get $p0
        i32.const 0
        i32.store offset=60
        local.get $p0
        local.get $l9
        f32.store offset=56
        local.get $p0
        local.get $l8
        f32.store offset=52
        local.get $p0
        local.get $l4
        f32.store offset=48
        local.get $p0
        i32.const 0
        i32.store offset=44
        local.get $p0
        local.get $l7
        f32.store offset=40
        local.get $p0
        local.get $l6
        f32.store offset=36
        local.get $p0
        local.get $l12
        local.get $l12
        f32.neg
        local.tee $l3
        local.get $l3
        local.get $l12
        f32.lt
        select
        f32.const 0x1.0c6f7ap-20 (;=1e-06;)
        f32.add
        local.tee $l12
        f32.store offset=120
        local.get $p0
        local.get $l11
        local.get $l11
        f32.neg
        local.tee $l3
        local.get $l3
        local.get $l11
        f32.lt
        select
        f32.const 0x1.0c6f7ap-20 (;=1e-06;)
        f32.add
        local.tee $l11
        f32.store offset=116
        local.get $p0
        local.get $l10
        local.get $l10
        f32.neg
        local.tee $l3
        local.get $l3
        local.get $l10
        f32.lt
        select
        f32.const 0x1.0c6f7ap-20 (;=1e-06;)
        f32.add
        local.tee $l10
        f32.store offset=112
        local.get $p0
        local.get $l9
        local.get $l9
        f32.neg
        local.tee $l3
        local.get $l3
        local.get $l9
        f32.lt
        select
        f32.const 0x1.0c6f7ap-20 (;=1e-06;)
        f32.add
        local.tee $l9
        f32.store offset=104
        local.get $p0
        local.get $l8
        local.get $l8
        f32.neg
        local.tee $l3
        local.get $l3
        local.get $l8
        f32.lt
        select
        f32.const 0x1.0c6f7ap-20 (;=1e-06;)
        f32.add
        local.tee $l8
        f32.store offset=100
        local.get $p0
        local.get $l4
        local.get $l4
        f32.neg
        local.tee $l3
        local.get $l3
        local.get $l4
        f32.lt
        select
        f32.const 0x1.0c6f7ap-20 (;=1e-06;)
        f32.add
        local.tee $l4
        f32.store offset=96
        local.get $p0
        local.get $l7
        local.get $l7
        f32.neg
        local.tee $l3
        local.get $l3
        local.get $l7
        f32.lt
        select
        f32.const 0x1.0c6f7ap-20 (;=1e-06;)
        f32.add
        local.tee $l7
        f32.store offset=88
        local.get $p0
        local.get $l6
        local.get $l6
        f32.neg
        local.tee $l3
        local.get $l3
        local.get $l6
        f32.lt
        select
        f32.const 0x1.0c6f7ap-20 (;=1e-06;)
        f32.add
        local.tee $l6
        f32.store offset=84
        local.get $p0
        local.get $l5
        local.get $l10
        f32.mul
        local.get $l13
        local.get $l11
        f32.mul
        f32.add
        local.get $l14
        local.get $l12
        f32.mul
        f32.add
        f32.store offset=136
        local.get $p0
        local.get $l5
        local.get $l4
        f32.mul
        local.get $l13
        local.get $l8
        f32.mul
        f32.add
        local.get $l14
        local.get $l9
        f32.mul
        f32.add
        f32.store offset=132
        local.get $p0
        local.get $l15
        f32.store offset=32
        local.get $p0
        local.get $l15
        local.get $l15
        f32.neg
        local.tee $l4
        local.get $l4
        local.get $l15
        f32.lt
        select
        f32.const 0x1.0c6f7ap-20 (;=1e-06;)
        f32.add
        local.tee $l4
        f32.store offset=80
        local.get $p0
        local.get $l5
        local.get $l4
        f32.mul
        local.get $l13
        local.get $l6
        f32.mul
        f32.add
        local.get $l14
        local.get $l7
        f32.mul
        f32.add
        f32.store offset=128
        local.get $l17
        local.get $p0
        local.get $p2
        local.get $l20
        call $f71780
        local.set $l16
      end
      local.get $p0
      i32.const 160
      i32.add
      global.set $g0
      local.get $l16
    end)
