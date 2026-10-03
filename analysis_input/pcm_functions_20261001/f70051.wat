  (func $f70051 (type $t2) (param $p0 i32) (param $p1 i32) (param $p2 i32)
    (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 i32) (local $l17 i32) (local $l18 i32) (local $l19 i32) (local $l20 i32) (local $l21 i32) (local $l22 i32) (local $l23 i32) (local $l24 i32) (local $l25 i32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32) (local $l33 f32)
    block $B0
      local.get $p0
      i32.load offset=2324
      i32.eqz
      br_if $B0
      local.get $p0
      i32.load offset=2328
      local.tee $l15
      i32.const 2
      i32.ge_u
      if $I1
        i32.const 1
        local.set $l5
        loop $L2
          block $B3
            local.get $p0
            local.get $l5
            i32.const 2
            i32.shl
            i32.add
            local.tee $l10
            i32.const 2044
            i32.add
            local.tee $l11
            i32.load
            local.tee $l8
            f32.load offset=32
            local.get $l10
            i32.const 2048
            i32.add
            local.tee $l10
            i32.load
            local.tee $l3
            f32.load offset=32
            f32.gt
            i32.eqz
            br_if $B3
            local.get $l11
            local.get $l3
            i32.store
            local.get $l10
            local.get $l8
            i32.store
            local.get $l5
            i32.const 2
            i32.sub
            local.tee $l10
            i32.const 0
            i32.lt_s
            br_if $B3
            loop $L4
              local.get $l3
              f32.load offset=32
              local.get $p0
              local.get $l10
              i32.const 2
              i32.shl
              i32.add
              local.tee $l11
              i32.const 2048
              i32.add
              local.tee $l8
              i32.load
              local.tee $l17
              f32.load offset=32
              f32.ge
              br_if $B3
              local.get $l11
              i32.const 2052
              i32.add
              local.get $l17
              i32.store
              local.get $l8
              local.get $l3
              i32.store
              local.get $l10
              i32.const 0
              i32.gt_s
              local.set $l11
              local.get $l10
              i32.const 1
              i32.sub
              local.set $l10
              local.get $l11
              br_if $L4
            end
          end
          local.get $l5
          i32.const 1
          i32.add
          local.tee $l5
          local.get $p0
          i32.load offset=2328
          local.tee $l15
          i32.lt_u
          br_if $L2
        end
      end
      local.get $p0
      i32.const 2224
      i32.add
      local.set $l24
      local.get $p0
      i32.const 2048
      i32.add
      local.set $l25
      block $B5 (result i32)
        local.get $l15
        if $I6
          i32.const 0
          local.set $l17
          loop $L7
            local.get $p0
            local.get $l17
            i32.const 2
            i32.shl
            i32.add
            i32.const 2048
            i32.add
            i32.load
            local.tee $l10
            i32.const 0
            i32.store offset=16
            local.get $l10
            local.get $l10
            i32.load offset=52
            local.get $l10
            i32.load offset=48
            i32.sub
            i32.store offset=56
            local.get $l10
            local.get $l10
            i32.store offset=20
            local.get $l10
            local.get $l10
            i32.store offset=24
            local.get $p0
            f32.load offset=2224
            local.set $l32
            local.get $l17
            local.set $l3
            block $B8
              loop $L9
                local.get $l3
                i32.eqz
                br_if $B8
                local.get $l10
                f32.load
                local.get $p0
                local.get $l3
                i32.const 1
                i32.sub
                local.tee $l3
                i32.const 2
                i32.shl
                i32.add
                i32.const 2048
                i32.add
                i32.load
                local.tee $l8
                i32.load offset=24
                local.tee $l11
                f32.load
                f32.mul
                local.get $l10
                f32.load offset=4
                local.get $l11
                f32.load offset=4
                f32.mul
                f32.add
                local.get $l10
                f32.load offset=8
                local.get $l11
                f32.load offset=8
                f32.mul
                f32.add
                local.get $l32
                f32.ge
                i32.eqz
                br_if $L9
              end
              local.get $l8
              local.get $l10
              i32.store offset=16
              local.get $l11
              local.get $l10
              i32.store offset=20
              local.get $l10
              local.get $l8
              i32.load offset=24
              i32.store offset=24
              local.get $l8
              i32.load offset=24
              local.tee $l3
              local.get $l3
              i32.load offset=56
              local.get $l10
              i32.load offset=52
              local.get $l10
              i32.load offset=48
              i32.sub
              i32.add
              i32.store offset=56
            end
            local.get $l17
            i32.const 1
            i32.add
            local.tee $l17
            local.get $l15
            i32.ne
            br_if $L7
          end
          local.get $p0
          i32.const 2240
          i32.add
          local.set $l18
          local.get $p0
          i32.load offset=2320
          local.set $l8
          i32.const 0
          local.get $p0
          i32.load offset=2328
          local.tee $l19
          i32.eqz
          br_if $B5
          drop
          loop $L10
            block $B11
              local.get $p0
              local.get $l22
              i32.const 2
              i32.shl
              i32.add
              i32.const 2048
              i32.add
              i32.load
              local.tee $l5
              i32.eqz
              br_if $B11
              local.get $l5
              i32.load offset=24
              local.get $l5
              i32.ne
              br_if $B11
              loop $L12
                local.get $l5
                i32.load offset=16
                local.tee $l10
                i32.eqz
                br_if $B11
                local.get $l5
                local.set $l23
                local.get $l10
                local.set $l5
                local.get $l23
                i32.load offset=48
                local.tee $l16
                local.get $l23
                i32.load offset=52
                local.tee $l10
                i32.ge_u
                br_if $L12
                local.get $l5
                i32.load offset=52
                local.set $l11
                loop $L13
                  local.get $l11
                  local.get $l5
                  i32.load offset=48
                  local.tee $l3
                  i32.gt_u
                  if $I14
                    local.get $l8
                    local.get $l16
                    i32.const 6
                    i32.shl
                    i32.add
                    local.tee $l10
                    i32.const 24
                    i32.add
                    local.set $l15
                    local.get $l10
                    i32.const 20
                    i32.add
                    local.set $l20
                    local.get $l10
                    i32.const 16
                    i32.add
                    local.set $l21
                    loop $L15
                      local.get $l18
                      f32.load
                      local.get $l8
                      local.get $l3
                      i32.const 6
                      i32.shl
                      i32.add
                      local.tee $l10
                      f32.load offset=16
                      local.get $l21
                      f32.load
                      f32.sub
                      local.tee $l32
                      local.get $l32
                      f32.mul
                      local.get $l10
                      f32.load offset=20
                      local.get $l20
                      f32.load
                      f32.sub
                      local.tee $l32
                      local.get $l32
                      f32.mul
                      f32.add
                      local.get $l10
                      i32.const 24
                      i32.add
                      local.tee $l17
                      f32.load
                      local.get $l15
                      f32.load
                      f32.sub
                      local.tee $l32
                      local.get $l32
                      f32.mul
                      f32.add
                      f32.gt
                      if $I16
                        local.get $l10
                        local.get $l11
                        i32.const 6
                        i32.shl
                        local.get $l8
                        i32.add
                        i32.const -64
                        i32.add
                        local.tee $l11
                        i64.load
                        i64.store
                        local.get $l10
                        local.get $l11
                        i32.load offset=48
                        i32.store offset=48
                        local.get $l10
                        local.get $l11
                        i64.load offset=40
                        i64.store offset=40
                        local.get $l10
                        local.get $l11
                        i64.load offset=32
                        i64.store offset=32
                        local.get $l17
                        local.get $l11
                        i64.load offset=24
                        i64.store
                        local.get $l10
                        local.get $l11
                        i64.load offset=16
                        i64.store offset=16
                        local.get $l10
                        local.get $l11
                        i64.load offset=8
                        i64.store offset=8
                        local.get $l5
                        local.get $l5
                        i32.load offset=52
                        i32.const 1
                        i32.sub
                        local.tee $l11
                        i32.store offset=52
                        local.get $l3
                        i32.const 1
                        i32.sub
                        local.set $l3
                      end
                      local.get $l3
                      i32.const 1
                      i32.add
                      local.tee $l3
                      local.get $l11
                      i32.lt_u
                      br_if $L15
                    end
                    local.get $l23
                    i32.load offset=52
                    local.set $l10
                  end
                  local.get $l10
                  local.get $l16
                  i32.const 1
                  i32.add
                  local.tee $l16
                  i32.gt_u
                  br_if $L13
                end
                br $L12
              end
              unreachable
            end
            local.get $l22
            i32.const 1
            i32.add
            local.tee $l22
            local.get $l19
            i32.ne
            br_if $L10
          end
          local.get $p0
          i32.load offset=2320
          local.set $l8
          local.get $p0
          i32.load offset=2328
          br $B5
        end
        local.get $p0
        i32.load offset=2320
        local.set $l8
        i32.const 0
      end
      local.set $l22
      local.get $p0
      i32.load offset=2216
      local.set $l13
      local.get $p0
      i32.load offset=2324
      local.set $l17
      local.get $l25
      local.set $l23
      local.get $l24
      local.set $l25
      local.get $p1
      local.set $l24
      i32.const 0
      local.set $l3
      i32.const 0
      local.set $l15
      i32.const 0
      local.set $l16
      global.get $g0
      i32.const 80
      i32.sub
      local.tee $l9
      global.set $g0
      block $B17
        local.get $l13
        i32.load8_u offset=62
        i32.eqz
        if $I18
          block $B19
            local.get $l22
            i32.eqz
            br_if $B19
            local.get $l24
            i32.const 1
            i32.sub
            local.set $l20
            loop $L20
              local.get $l23
              local.get $l16
              i32.const 2
              i32.shl
              i32.add
              i32.load
              local.tee $p1
              i32.load offset=24
              local.get $p1
              i32.eq
              if $I21
                local.get $l3
                i32.const 255
                i32.and
                local.tee $l3
                i32.const 5
                i32.gt_u
                br_if $B19
                local.get $l13
                local.get $l3
                local.get $l13
                i32.add
                i32.load8_u offset=56
                i32.const 400
                i32.mul
                i32.add
                local.tee $l14
                i32.const -64
                i32.sub
                local.set $l15
                block $B22
                  block $B23
                    block $B24
                      block $B25
                        local.get $l20
                        br_table $B25 $B24 $B23 $B24
                      end
                      i32.const -1
                      local.set $l4
                      f32.const 0x1.fffffep+127 (;=3.40282e+38;)
                      local.set $l27
                      f32.const 0x1.fffffep+127 (;=3.40282e+38;)
                      local.set $l26
                      loop $L26
                        block $B27
                          local.get $p1
                          i32.load offset=52
                          local.tee $l11
                          local.get $p1
                          i32.load offset=48
                          local.tee $l3
                          i32.le_u
                          br_if $B27
                          local.get $l11
                          local.get $l3
                          i32.const -1
                          i32.xor
                          i32.add
                          local.set $l5
                          local.get $l11
                          local.get $l3
                          i32.sub
                          i32.const 3
                          i32.and
                          local.tee $l6
                          if $I28
                            loop $L29
                              local.get $l8
                              local.get $l3
                              i32.const 6
                              i32.shl
                              i32.add
                              f32.load offset=44
                              local.tee $l28
                              local.get $l26
                              local.get $l26
                              local.get $l28
                              f32.gt
                              local.tee $l7
                              select
                              local.set $l26
                              local.get $l28
                              local.get $l27
                              local.get $l7
                              select
                              local.set $l27
                              local.get $l3
                              local.get $l4
                              local.get $l7
                              select
                              local.set $l4
                              local.get $l3
                              i32.const 1
                              i32.add
                              local.set $l3
                              local.get $l6
                              i32.const 1
                              i32.sub
                              local.tee $l6
                              br_if $L29
                            end
                          end
                          local.get $l5
                          i32.const 2
                          i32.le_u
                          br_if $B27
                          loop $L30
                            local.get $l8
                            local.get $l3
                            i32.const 3
                            i32.add
                            local.tee $l18
                            i32.const 6
                            i32.shl
                            i32.add
                            f32.load offset=44
                            local.tee $l28
                            local.get $l8
                            local.get $l3
                            i32.const 2
                            i32.add
                            local.tee $l19
                            i32.const 6
                            i32.shl
                            i32.add
                            f32.load offset=44
                            local.tee $l29
                            local.get $l8
                            local.get $l3
                            i32.const 1
                            i32.add
                            local.tee $l21
                            i32.const 6
                            i32.shl
                            i32.add
                            f32.load offset=44
                            local.tee $l30
                            local.get $l8
                            local.get $l3
                            i32.const 6
                            i32.shl
                            i32.add
                            f32.load offset=44
                            local.tee $l31
                            local.get $l26
                            local.get $l26
                            local.get $l31
                            f32.gt
                            local.tee $l7
                            select
                            local.tee $l26
                            local.get $l26
                            local.get $l30
                            f32.gt
                            local.tee $l6
                            select
                            local.tee $l26
                            local.get $l26
                            local.get $l29
                            f32.gt
                            local.tee $l5
                            select
                            local.tee $l26
                            local.get $l26
                            local.get $l28
                            f32.gt
                            local.tee $l12
                            select
                            local.set $l26
                            local.get $l28
                            local.get $l29
                            local.get $l30
                            local.get $l31
                            local.get $l27
                            local.get $l7
                            select
                            local.get $l6
                            select
                            local.get $l5
                            select
                            local.get $l12
                            select
                            local.set $l27
                            local.get $l18
                            local.get $l19
                            local.get $l21
                            local.get $l3
                            local.get $l4
                            local.get $l7
                            select
                            local.get $l6
                            select
                            local.get $l5
                            select
                            local.get $l12
                            select
                            local.set $l4
                            local.get $l3
                            i32.const 4
                            i32.add
                            local.tee $l3
                            local.get $l11
                            i32.ne
                            br_if $L30
                          end
                        end
                        local.get $p1
                        i32.load offset=16
                        local.tee $p1
                        br_if $L26
                      end
                      local.get $l9
                      local.get $l27
                      f32.store offset=16
                      local.get $l15
                      local.get $l8
                      local.get $l4
                      i32.const 6
                      i32.shl
                      i32.add
                      local.tee $l3
                      i64.load
                      i64.store
                      local.get $l15
                      local.get $l3
                      i32.load offset=48
                      i32.store offset=48
                      local.get $l15
                      local.get $l3
                      i64.load offset=40
                      i64.store offset=40
                      local.get $l15
                      local.get $l3
                      i64.load offset=32
                      i64.store offset=32
                      local.get $l15
                      local.get $l3
                      i64.load offset=24
                      i64.store offset=24
                      local.get $l15
                      local.get $l3
                      i64.load offset=16
                      i64.store offset=16
                      local.get $l15
                      local.get $l3
                      i64.load offset=8
                      i64.store offset=8
                      local.get $l14
                      i32.const 1
                      i32.store offset=448
                      br $B22
                    end
                    i32.const 0
                    local.set $l6
                    local.get $p1
                    local.tee $l5
                    i32.load offset=56
                    i32.const 6
                    i32.le_u
                    if $I31
                      loop $L32
                        local.get $l5
                        i32.load offset=48
                        local.tee $l7
                        local.get $l5
                        i32.load offset=52
                        i32.lt_u
                        if $I33
                          loop $L34
                            local.get $l14
                            local.get $l6
                            i32.const 6
                            i32.shl
                            i32.add
                            local.tee $l3
                            local.get $l8
                            local.get $l7
                            i32.const 6
                            i32.shl
                            i32.add
                            local.tee $l4
                            i32.load offset=48
                            i32.store offset=112
                            local.get $l3
                            local.get $l4
                            i64.load offset=40
                            i64.store offset=104
                            local.get $l3
                            local.get $l4
                            i64.load offset=32
                            i64.store offset=96
                            local.get $l3
                            local.get $l4
                            i64.load offset=24
                            i64.store offset=88
                            local.get $l3
                            local.get $l4
                            i64.load offset=16
                            i64.store offset=80
                            local.get $l3
                            local.get $l4
                            i64.load offset=8
                            i64.store offset=72
                            local.get $l3
                            i32.const -64
                            i32.sub
                            local.get $l4
                            i64.load
                            i64.store
                            local.get $l6
                            i32.const 1
                            i32.add
                            local.set $l6
                            local.get $l7
                            i32.const 1
                            i32.add
                            local.tee $l7
                            local.get $l5
                            i32.load offset=52
                            i32.lt_u
                            br_if $L34
                          end
                        end
                        local.get $l5
                        i32.load offset=16
                        local.tee $l5
                        br_if $L32
                      end
                      local.get $l14
                      local.get $l6
                      i32.store offset=448
                      local.get $l9
                      local.get $p1
                      i64.load offset=40
                      i64.store offset=24
                      local.get $l9
                      local.get $p1
                      i64.load offset=32
                      i64.store offset=16
                      br $B22
                    end
                    local.get $l9
                    i32.const 16
                    i32.add
                    local.get $l15
                    local.get $l8
                    local.get $l17
                    local.get $p1
                    call $f69975
                    local.get $l14
                    i32.const 6
                    i32.store offset=448
                    br $B22
                  end
                  i32.const 0
                  local.set $l6
                  local.get $p1
                  local.tee $l5
                  i32.load offset=56
                  i32.const 3
                  i32.le_u
                  if $I35
                    loop $L36
                      local.get $l5
                      i32.load offset=48
                      local.tee $l7
                      local.get $l5
                      i32.load offset=52
                      i32.lt_u
                      if $I37
                        loop $L38
                          local.get $l14
                          local.get $l6
                          i32.const 6
                          i32.shl
                          i32.add
                          local.tee $l3
                          local.get $l8
                          local.get $l7
                          i32.const 6
                          i32.shl
                          i32.add
                          local.tee $l4
                          i32.load offset=48
                          i32.store offset=112
                          local.get $l3
                          local.get $l4
                          i64.load offset=40
                          i64.store offset=104
                          local.get $l3
                          local.get $l4
                          i64.load offset=32
                          i64.store offset=96
                          local.get $l3
                          local.get $l4
                          i64.load offset=24
                          i64.store offset=88
                          local.get $l3
                          local.get $l4
                          i64.load offset=16
                          i64.store offset=80
                          local.get $l3
                          local.get $l4
                          i64.load offset=8
                          i64.store offset=72
                          local.get $l3
                          i32.const -64
                          i32.sub
                          local.get $l4
                          i64.load
                          i64.store
                          local.get $l6
                          i32.const 1
                          i32.add
                          local.set $l6
                          local.get $l7
                          i32.const 1
                          i32.add
                          local.tee $l7
                          local.get $l5
                          i32.load offset=52
                          i32.lt_u
                          br_if $L38
                        end
                      end
                      local.get $l5
                      i32.load offset=16
                      local.tee $l5
                      br_if $L36
                    end
                    local.get $l14
                    local.get $l6
                    i32.store offset=448
                    local.get $l9
                    local.get $p1
                    i64.load offset=40
                    i64.store offset=24
                    local.get $l9
                    local.get $p1
                    i64.load offset=32
                    i64.store offset=16
                    br $B22
                  end
                  local.get $l9
                  i32.const 16
                  i32.add
                  local.get $l15
                  local.get $l8
                  local.get $l17
                  local.get $p1
                  call $f69976
                  local.get $l14
                  i32.const 3
                  i32.store offset=448
                end
                local.get $l13
                local.get $l13
                local.get $l13
                i32.load8_u offset=62
                i32.add
                i32.load8_u offset=56
                i32.const 2
                i32.shl
                i32.add
                local.get $l9
                f32.load offset=16
                f32.store offset=32
                local.get $l13
                local.get $l13
                i32.load8_u offset=62
                i32.const 1
                i32.add
                local.tee $l3
                i32.store8 offset=62
              end
              local.get $l16
              i32.const 1
              i32.add
              local.tee $l16
              local.get $l22
              i32.ne
              br_if $L20
            end
          end
          local.get $l9
          i32.const 80
          i32.add
          global.set $g0
          br $B17
        end
        local.get $l9
        i32.const 2139095039
        i32.store offset=48
        local.get $l9
        i64.const 0
        i64.store offset=32
        local.get $l9
        local.get $l9
        i32.const 16
        i32.add
        i32.store offset=40
        block $B39
          local.get $l22
          i32.eqz
          br_if $B39
          local.get $l24
          i32.const 1
          i32.sub
          local.set $l10
          loop $L40
            block $B41
              local.get $l23
              local.get $l15
              i32.const 2
              i32.shl
              i32.add
              i32.load
              local.tee $l6
              i32.load offset=24
              local.get $l6
              i32.ne
              br_if $B41
              local.get $l6
              i32.const 32
              i32.add
              local.set $l14
              block $B42
                block $B43
                  block $B44
                    block $B45
                      block $B46
                        block $B47
                          block $B48
                            block $B49
                              block $B50
                                local.get $l13
                                i32.load8_u offset=62
                                local.tee $l19
                                i32.eqz
                                br_if $B50
                                local.get $l25
                                f32.load
                                local.set $l30
                                local.get $l6
                                f32.load offset=8
                                local.set $l31
                                local.get $l6
                                f32.load offset=4
                                local.set $l33
                                local.get $l6
                                f32.load
                                local.set $l32
                                i32.const 0
                                local.set $l12
                                loop $L51
                                  local.get $l13
                                  local.get $l12
                                  local.get $l13
                                  i32.add
                                  i32.const 56
                                  i32.add
                                  local.tee $l16
                                  i32.load8_u
                                  i32.const 400
                                  i32.mul
                                  i32.add
                                  local.tee $l7
                                  f32.load offset=104
                                  local.set $l26
                                  local.get $l7
                                  f32.load offset=100
                                  local.set $l27
                                  local.get $l7
                                  f32.load offset=96
                                  local.set $l28
                                  block $B52
                                    local.get $l7
                                    i32.const 448
                                    i32.add
                                    local.tee $p1
                                    i32.load
                                    local.tee $l18
                                    i32.const 2
                                    i32.lt_u
                                    br_if $B52
                                    i32.const 1
                                    local.set $l4
                                    local.get $l18
                                    i32.const 1
                                    i32.sub
                                    local.tee $l3
                                    i32.const 1
                                    i32.and
                                    local.set $l21
                                    local.get $l18
                                    i32.const 2
                                    i32.ne
                                    if $I53
                                      local.get $l3
                                      i32.const -2
                                      i32.and
                                      local.set $l5
                                      loop $L54
                                        local.get $l26
                                        local.get $l7
                                        local.get $l4
                                        i32.const 6
                                        i32.shl
                                        i32.add
                                        local.tee $l3
                                        f32.load offset=104
                                        f32.add
                                        local.get $l3
                                        f32.load offset=168
                                        f32.add
                                        local.set $l26
                                        local.get $l27
                                        local.get $l3
                                        f32.load offset=100
                                        f32.add
                                        local.get $l3
                                        f32.load offset=164
                                        f32.add
                                        local.set $l27
                                        local.get $l28
                                        local.get $l3
                                        f32.load offset=96
                                        f32.add
                                        local.get $l3
                                        f32.load offset=160
                                        f32.add
                                        local.set $l28
                                        local.get $l4
                                        i32.const 2
                                        i32.add
                                        local.set $l4
                                        local.get $l5
                                        i32.const 2
                                        i32.sub
                                        local.tee $l5
                                        br_if $L54
                                      end
                                    end
                                    local.get $l21
                                    i32.eqz
                                    br_if $B52
                                    local.get $l28
                                    local.get $l7
                                    local.get $l4
                                    i32.const 6
                                    i32.shl
                                    i32.add
                                    local.tee $l3
                                    f32.load offset=96
                                    f32.add
                                    local.set $l28
                                    local.get $l27
                                    local.get $l3
                                    f32.load offset=100
                                    f32.add
                                    local.set $l27
                                    local.get $l26
                                    local.get $l3
                                    f32.load offset=104
                                    f32.add
                                    local.set $l26
                                  end
                                  local.get $l30
                                  local.get $l31
                                  local.get $l26
                                  f32.const 0x1p+0 (;=1;)
                                  local.get $l28
                                  local.get $l28
                                  f32.mul
                                  local.get $l27
                                  local.get $l27
                                  f32.mul
                                  f32.add
                                  local.get $l26
                                  local.get $l26
                                  f32.mul
                                  f32.add
                                  f32.sqrt
                                  f32.div
                                  local.tee $l29
                                  f32.mul
                                  local.tee $l26
                                  f32.mul
                                  local.get $l32
                                  local.get $l28
                                  local.get $l29
                                  f32.mul
                                  local.tee $l28
                                  f32.mul
                                  local.get $l33
                                  local.get $l27
                                  local.get $l29
                                  f32.mul
                                  local.tee $l27
                                  f32.mul
                                  f32.add
                                  f32.add
                                  f32.le
                                  if $I55
                                    i32.const 0
                                    local.set $l5
                                    local.get $l18
                                    i32.eqz
                                    if $I56
                                      local.get $l17
                                      local.set $l3
                                      br $B42
                                    end
                                    loop $L57
                                      local.get $l8
                                      local.get $l5
                                      local.get $l17
                                      i32.add
                                      i32.const 6
                                      i32.shl
                                      i32.add
                                      local.tee $l3
                                      local.get $l7
                                      local.get $l5
                                      i32.const 6
                                      i32.shl
                                      i32.add
                                      local.tee $l4
                                      i32.load offset=112
                                      i32.store offset=48
                                      local.get $l3
                                      local.get $l4
                                      i64.load offset=104
                                      i64.store offset=40
                                      local.get $l3
                                      local.get $l4
                                      i64.load offset=96
                                      i64.store offset=32
                                      local.get $l3
                                      local.get $l4
                                      i64.load offset=88
                                      i64.store offset=24
                                      local.get $l3
                                      local.get $l4
                                      i64.load offset=80
                                      i64.store offset=16
                                      local.get $l3
                                      local.get $l4
                                      i64.load offset=72
                                      i64.store offset=8
                                      local.get $l3
                                      local.get $l4
                                      i32.const -64
                                      i32.sub
                                      i64.load
                                      i64.store
                                      local.get $l5
                                      i32.const 1
                                      i32.add
                                      local.tee $l5
                                      local.get $p1
                                      i32.load
                                      local.tee $l3
                                      i32.lt_u
                                      br_if $L57
                                    end
                                    local.get $l3
                                    local.get $l17
                                    i32.add
                                    local.set $l3
                                    br $B42
                                  end
                                  local.get $l12
                                  i32.const 1
                                  i32.add
                                  local.tee $l12
                                  local.get $l19
                                  i32.lt_u
                                  br_if $L51
                                end
                                local.get $l19
                                i32.const 6
                                i32.lt_u
                                br_if $B50
                                local.get $l19
                                i32.const 1
                                i32.sub
                                local.tee $l3
                                i32.const -2
                                i32.and
                                local.set $l12
                                local.get $l3
                                i32.const 1
                                i32.and
                                local.set $l19
                                i32.const 0
                                local.set $l5
                                local.get $l13
                                i32.const 32
                                i32.add
                                local.set $l4
                                local.get $l13
                                i32.const 56
                                i32.add
                                local.set $l7
                                i32.const 1
                                local.set $l3
                                loop $L58
                                  local.get $l3
                                  i32.const 1
                                  i32.add
                                  local.tee $l18
                                  local.get $l3
                                  local.get $l5
                                  local.get $l4
                                  local.get $l3
                                  local.get $l7
                                  i32.add
                                  i32.load8_u
                                  i32.const 2
                                  i32.shl
                                  i32.add
                                  f32.load
                                  local.get $l4
                                  local.get $l5
                                  local.get $l7
                                  i32.add
                                  i32.load8_u
                                  i32.const 2
                                  i32.shl
                                  i32.add
                                  f32.load
                                  f32.gt
                                  select
                                  local.tee $l5
                                  local.get $l4
                                  local.get $l7
                                  local.get $l18
                                  i32.add
                                  i32.load8_u
                                  i32.const 2
                                  i32.shl
                                  i32.add
                                  f32.load
                                  local.get $l4
                                  local.get $l5
                                  local.get $l7
                                  i32.add
                                  i32.load8_u
                                  i32.const 2
                                  i32.shl
                                  i32.add
                                  f32.load
                                  f32.gt
                                  select
                                  local.set $l5
                                  local.get $l3
                                  i32.const 2
                                  i32.add
                                  local.set $l3
                                  local.get $l12
                                  i32.const 2
                                  i32.sub
                                  local.tee $l12
                                  br_if $L58
                                end
                                local.get $l13
                                local.get $l19
                                if $I59 (result i32)
                                  local.get $l3
                                  local.get $l5
                                  local.get $l13
                                  i32.const 32
                                  i32.add
                                  local.tee $l4
                                  local.get $l13
                                  i32.const 56
                                  i32.add
                                  local.tee $l7
                                  local.get $l3
                                  i32.add
                                  i32.load8_u
                                  i32.const 2
                                  i32.shl
                                  i32.add
                                  f32.load
                                  local.get $l4
                                  local.get $l5
                                  local.get $l7
                                  i32.add
                                  i32.load8_u
                                  i32.const 2
                                  i32.shl
                                  i32.add
                                  f32.load
                                  f32.gt
                                  select
                                else
                                  local.get $l5
                                end
                                local.get $l13
                                i32.add
                                i32.const 56
                                i32.add
                                local.tee $l16
                                i32.load8_u
                                local.tee $l3
                                i32.const 2
                                i32.shl
                                i32.add
                                f32.load offset=32
                                local.get $l6
                                f32.load offset=32
                                f32.gt
                                i32.eqz
                                br_if $B39
                                i32.const 0
                                local.set $l5
                                local.get $l13
                                local.get $l3
                                i32.const 400
                                i32.mul
                                i32.add
                                local.tee $l4
                                i32.const 448
                                i32.add
                                local.tee $l15
                                i32.const 0
                                i32.store
                                local.get $l4
                                i32.const -64
                                i32.sub
                                local.set $p1
                                local.get $l24
                                i32.const 1
                                i32.sub
                                br_table $B47 $B49 $B48 $B49
                              end
                              local.get $l13
                              local.get $l13
                              local.get $l19
                              i32.add
                              i32.load8_u offset=56
                              i32.const 400
                              i32.mul
                              i32.add
                              local.tee $l11
                              i32.const -64
                              i32.sub
                              local.set $l16
                              block $B60
                                local.get $l10
                                br_table $B60 $B45 $B44 $B45
                              end
                              i32.const -1
                              local.set $l4
                              f32.const 0x1.fffffep+127 (;=3.40282e+38;)
                              local.set $l27
                              f32.const 0x1.fffffep+127 (;=3.40282e+38;)
                              local.set $l26
                              loop $L61
                                block $B62
                                  local.get $l6
                                  i32.load offset=52
                                  local.tee $p1
                                  local.get $l6
                                  i32.load offset=48
                                  local.tee $l3
                                  i32.le_u
                                  br_if $B62
                                  local.get $p1
                                  local.get $l3
                                  i32.const -1
                                  i32.xor
                                  i32.add
                                  local.set $l12
                                  local.get $p1
                                  local.get $l3
                                  i32.sub
                                  i32.const 3
                                  i32.and
                                  local.tee $l5
                                  if $I63
                                    loop $L64
                                      local.get $l8
                                      local.get $l3
                                      i32.const 6
                                      i32.shl
                                      i32.add
                                      f32.load offset=44
                                      local.tee $l28
                                      local.get $l26
                                      local.get $l26
                                      local.get $l28
                                      f32.gt
                                      local.tee $l7
                                      select
                                      local.set $l26
                                      local.get $l28
                                      local.get $l27
                                      local.get $l7
                                      select
                                      local.set $l27
                                      local.get $l3
                                      local.get $l4
                                      local.get $l7
                                      select
                                      local.set $l4
                                      local.get $l3
                                      i32.const 1
                                      i32.add
                                      local.set $l3
                                      local.get $l5
                                      i32.const 1
                                      i32.sub
                                      local.tee $l5
                                      br_if $L64
                                    end
                                  end
                                  local.get $l12
                                  i32.const 2
                                  i32.le_u
                                  br_if $B62
                                  loop $L65
                                    local.get $l8
                                    local.get $l3
                                    i32.const 3
                                    i32.add
                                    local.tee $l19
                                    i32.const 6
                                    i32.shl
                                    i32.add
                                    f32.load offset=44
                                    local.tee $l28
                                    local.get $l8
                                    local.get $l3
                                    i32.const 2
                                    i32.add
                                    local.tee $l21
                                    i32.const 6
                                    i32.shl
                                    i32.add
                                    f32.load offset=44
                                    local.tee $l29
                                    local.get $l8
                                    local.get $l3
                                    i32.const 1
                                    i32.add
                                    local.tee $l14
                                    i32.const 6
                                    i32.shl
                                    i32.add
                                    f32.load offset=44
                                    local.tee $l30
                                    local.get $l8
                                    local.get $l3
                                    i32.const 6
                                    i32.shl
                                    i32.add
                                    f32.load offset=44
                                    local.tee $l31
                                    local.get $l26
                                    local.get $l26
                                    local.get $l31
                                    f32.gt
                                    local.tee $l7
                                    select
                                    local.tee $l26
                                    local.get $l26
                                    local.get $l30
                                    f32.gt
                                    local.tee $l5
                                    select
                                    local.tee $l26
                                    local.get $l26
                                    local.get $l29
                                    f32.gt
                                    local.tee $l12
                                    select
                                    local.tee $l26
                                    local.get $l26
                                    local.get $l28
                                    f32.gt
                                    local.tee $l18
                                    select
                                    local.set $l26
                                    local.get $l28
                                    local.get $l29
                                    local.get $l30
                                    local.get $l31
                                    local.get $l27
                                    local.get $l7
                                    select
                                    local.get $l5
                                    select
                                    local.get $l12
                                    select
                                    local.get $l18
                                    select
                                    local.set $l27
                                    local.get $l19
                                    local.get $l21
                                    local.get $l14
                                    local.get $l3
                                    local.get $l4
                                    local.get $l7
                                    select
                                    local.get $l5
                                    select
                                    local.get $l12
                                    select
                                    local.get $l18
                                    select
                                    local.set $l4
                                    local.get $l3
                                    i32.const 4
                                    i32.add
                                    local.tee $l3
                                    local.get $p1
                                    i32.ne
                                    br_if $L65
                                  end
                                end
                                local.get $l6
                                i32.load offset=16
                                local.tee $l6
                                br_if $L61
                              end
                              local.get $l9
                              local.get $l27
                              f32.store
                              local.get $l16
                              local.get $l8
                              local.get $l4
                              i32.const 6
                              i32.shl
                              i32.add
                              local.tee $l3
                              i64.load
                              i64.store
                              local.get $l16
                              local.get $l3
                              i32.load offset=48
                              i32.store offset=48
                              local.get $l16
                              local.get $l3
                              i64.load offset=40
                              i64.store offset=40
                              local.get $l16
                              local.get $l3
                              i64.load offset=32
                              i64.store offset=32
                              local.get $l16
                              local.get $l3
                              i64.load offset=24
                              i64.store offset=24
                              local.get $l16
                              local.get $l3
                              i64.load offset=16
                              i64.store offset=16
                              local.get $l16
                              local.get $l3
                              i64.load offset=8
                              i64.store offset=8
                              local.get $l11
                              i32.const 1
                              i32.store offset=448
                              br $B43
                            end
                            local.get $l6
                            i32.load offset=56
                            i32.const 6
                            i32.le_u
                            if $I66
                              local.get $l13
                              local.get $l3
                              i32.const 400
                              i32.mul
                              i32.add
                              local.set $l12
                              loop $L67
                                local.get $l6
                                i32.load offset=48
                                local.tee $l7
                                local.get $l6
                                i32.load offset=52
                                i32.lt_u
                                if $I68
                                  loop $L69
                                    local.get $l12
                                    local.get $l5
                                    i32.const 6
                                    i32.shl
                                    i32.add
                                    local.tee $l3
                                    local.get $l8
                                    local.get $l7
                                    i32.const 6
                                    i32.shl
                                    i32.add
                                    local.tee $l4
                                    i32.load offset=48
                                    i32.store offset=112
                                    local.get $l3
                                    local.get $l4
                                    i64.load offset=40
                                    i64.store offset=104
                                    local.get $l3
                                    local.get $l4
                                    i64.load offset=32
                                    i64.store offset=96
                                    local.get $l3
                                    local.get $l4
                                    i64.load offset=24
                                    i64.store offset=88
                                    local.get $l3
                                    local.get $l4
                                    i64.load offset=16
                                    i64.store offset=80
                                    local.get $l3
                                    local.get $l4
                                    i64.load offset=8
                                    i64.store offset=72
                                    local.get $l3
                                    i32.const -64
                                    i32.sub
                                    local.get $l4
                                    i64.load
                                    i64.store
                                    local.get $l5
                                    i32.const 1
                                    i32.add
                                    local.set $l5
                                    local.get $l7
                                    i32.const 1
                                    i32.add
                                    local.tee $l7
                                    local.get $l6
                                    i32.load offset=52
                                    i32.lt_u
                                    br_if $L69
                                  end
                                end
                                local.get $l6
                                i32.load offset=16
                                local.tee $l6
                                br_if $L67
                              end
                              local.get $l15
                              local.get $l5
                              i32.store
                              local.get $l9
                              local.get $l14
                              i64.load offset=8
                              i64.store offset=8
                              local.get $l9
                              local.get $l14
                              i64.load
                              i64.store
                              br $B46
                            end
                            local.get $l9
                            local.get $p1
                            local.get $l8
                            local.get $l17
                            local.get $l6
                            call $f69975
                            local.get $l15
                            i32.const 6
                            i32.store
                            br $B46
                          end
                          local.get $l6
                          i32.load offset=56
                          i32.const 3
                          i32.le_u
                          if $I70
                            local.get $l13
                            local.get $l3
                            i32.const 400
                            i32.mul
                            i32.add
                            local.set $l12
                            loop $L71
                              local.get $l6
                              i32.load offset=48
                              local.tee $l7
                              local.get $l6
                              i32.load offset=52
                              i32.lt_u
                              if $I72
                                loop $L73
                                  local.get $l12
                                  local.get $l5
                                  i32.const 6
                                  i32.shl
                                  i32.add
                                  local.tee $l3
                                  local.get $l8
                                  local.get $l7
                                  i32.const 6
                                  i32.shl
                                  i32.add
                                  local.tee $l4
                                  i32.load offset=48
                                  i32.store offset=112
                                  local.get $l3
                                  local.get $l4
                                  i64.load offset=40
                                  i64.store offset=104
                                  local.get $l3
                                  local.get $l4
                                  i64.load offset=32
                                  i64.store offset=96
                                  local.get $l3
                                  local.get $l4
                                  i64.load offset=24
                                  i64.store offset=88
                                  local.get $l3
                                  local.get $l4
                                  i64.load offset=16
                                  i64.store offset=80
                                  local.get $l3
                                  local.get $l4
                                  i64.load offset=8
                                  i64.store offset=72
                                  local.get $l3
                                  i32.const -64
                                  i32.sub
                                  local.get $l4
                                  i64.load
                                  i64.store
                                  local.get $l5
                                  i32.const 1
                                  i32.add
                                  local.set $l5
                                  local.get $l7
                                  i32.const 1
                                  i32.add
                                  local.tee $l7
                                  local.get $l6
                                  i32.load offset=52
                                  i32.lt_u
                                  br_if $L73
                                end
                              end
                              local.get $l6
                              i32.load offset=16
                              local.tee $l6
                              br_if $L71
                            end
                            local.get $l15
                            local.get $l5
                            i32.store
                            local.get $l9
                            local.get $l14
                            i64.load offset=8
                            i64.store offset=8
                            local.get $l9
                            local.get $l14
                            i64.load
                            i64.store
                            br $B46
                          end
                          local.get $l9
                          local.get $p1
                          local.get $l8
                          local.get $l17
                          local.get $l6
                          call $f69976
                          local.get $l15
                          i32.const 3
                          i32.store
                          br $B46
                        end
                        f32.const 0x1.fffffep+127 (;=3.40282e+38;)
                        local.set $l27
                        f32.const 0x1.fffffep+127 (;=3.40282e+38;)
                        local.set $l26
                        i32.const -1
                        local.set $l4
                        loop $L74
                          block $B75
                            local.get $l6
                            i32.load offset=52
                            local.tee $l11
                            local.get $l6
                            i32.load offset=48
                            local.tee $l3
                            i32.le_u
                            br_if $B75
                            local.get $l11
                            local.get $l3
                            i32.const -1
                            i32.xor
                            i32.add
                            local.set $l12
                            local.get $l11
                            local.get $l3
                            i32.sub
                            i32.const 3
                            i32.and
                            local.tee $l5
                            if $I76
                              loop $L77
                                local.get $l8
                                local.get $l3
                                i32.const 6
                                i32.shl
                                i32.add
                                f32.load offset=44
                                local.tee $l28
                                local.get $l26
                                local.get $l26
                                local.get $l28
                                f32.gt
                                local.tee $l7
                                select
                                local.set $l26
                                local.get $l28
                                local.get $l27
                                local.get $l7
                                select
                                local.set $l27
                                local.get $l3
                                local.get $l4
                                local.get $l7
                                select
                                local.set $l4
                                local.get $l3
                                i32.const 1
                                i32.add
                                local.set $l3
                                local.get $l5
                                i32.const 1
                                i32.sub
                                local.tee $l5
                                br_if $L77
                              end
                            end
                            local.get $l12
                            i32.const 2
                            i32.le_u
                            br_if $B75
                            loop $L78
                              local.get $l8
                              local.get $l3
                              i32.const 3
                              i32.add
                              local.tee $l19
                              i32.const 6
                              i32.shl
                              i32.add
                              f32.load offset=44
                              local.tee $l28
                              local.get $l8
                              local.get $l3
                              i32.const 2
                              i32.add
                              local.tee $l21
                              i32.const 6
                              i32.shl
                              i32.add
                              f32.load offset=44
                              local.tee $l29
                              local.get $l8
                              local.get $l3
                              i32.const 1
                              i32.add
                              local.tee $l14
                              i32.const 6
                              i32.shl
                              i32.add
                              f32.load offset=44
                              local.tee $l30
                              local.get $l8
                              local.get $l3
                              i32.const 6
                              i32.shl
                              i32.add
                              f32.load offset=44
                              local.tee $l31
                              local.get $l26
                              local.get $l26
                              local.get $l31
                              f32.gt
                              local.tee $l7
                              select
                              local.tee $l26
                              local.get $l26
                              local.get $l30
                              f32.gt
                              local.tee $l5
                              select
                              local.tee $l26
                              local.get $l26
                              local.get $l29
                              f32.gt
                              local.tee $l12
                              select
                              local.tee $l26
                              local.get $l26
                              local.get $l28
                              f32.gt
                              local.tee $l18
                              select
                              local.set $l26
                              local.get $l28
                              local.get $l29
                              local.get $l30
                              local.get $l31
                              local.get $l27
                              local.get $l7
                              select
                              local.get $l5
                              select
                              local.get $l12
                              select
                              local.get $l18
                              select
                              local.set $l27
                              local.get $l19
                              local.get $l21
                              local.get $l14
                              local.get $l3
                              local.get $l4
                              local.get $l7
                              select
                              local.get $l5
                              select
                              local.get $l12
                              select
                              local.get $l18
                              select
                              local.set $l4
                              local.get $l3
                              i32.const 4
                              i32.add
                              local.tee $l3
                              local.get $l11
                              i32.ne
                              br_if $L78
                            end
                          end
                          local.get $l6
                          i32.load offset=16
                          local.tee $l6
                          br_if $L74
                        end
                        local.get $l9
                        local.get $l27
                        f32.store
                        local.get $p1
                        local.get $l8
                        local.get $l4
                        i32.const 6
                        i32.shl
                        i32.add
                        local.tee $l8
                        i64.load
                        i64.store
                        local.get $p1
                        local.get $l8
                        i32.load offset=48
                        i32.store offset=48
                        local.get $p1
                        local.get $l8
                        i64.load offset=40
                        i64.store offset=40
                        local.get $p1
                        local.get $l8
                        i64.load offset=32
                        i64.store offset=32
                        local.get $p1
                        local.get $l8
                        i64.load offset=24
                        i64.store offset=24
                        local.get $p1
                        local.get $l8
                        i64.load offset=16
                        i64.store offset=16
                        local.get $p1
                        local.get $l8
                        i64.load offset=8
                        i64.store offset=8
                        local.get $l15
                        i32.const 1
                        i32.store
                      end
                      local.get $l13
                      local.get $l16
                      i32.load8_u
                      i32.const 2
                      i32.shl
                      i32.add
                      local.get $l9
                      f32.load
                      f32.store offset=32
                      br $B39
                    end
                    i32.const 0
                    local.set $l5
                    local.get $l6
                    i32.load offset=56
                    i32.const 6
                    i32.le_u
                    if $I79
                      loop $L80
                        local.get $l6
                        i32.load offset=48
                        local.tee $l7
                        local.get $l6
                        i32.load offset=52
                        i32.lt_u
                        if $I81
                          loop $L82
                            local.get $l11
                            local.get $l5
                            i32.const 6
                            i32.shl
                            i32.add
                            local.tee $l3
                            local.get $l8
                            local.get $l7
                            i32.const 6
                            i32.shl
                            i32.add
                            local.tee $l4
                            i32.load offset=48
                            i32.store offset=112
                            local.get $l3
                            local.get $l4
                            i64.load offset=40
                            i64.store offset=104
                            local.get $l3
                            local.get $l4
                            i64.load offset=32
                            i64.store offset=96
                            local.get $l3
                            local.get $l4
                            i64.load offset=24
                            i64.store offset=88
                            local.get $l3
                            local.get $l4
                            i64.load offset=16
                            i64.store offset=80
                            local.get $l3
                            local.get $l4
                            i64.load offset=8
                            i64.store offset=72
                            local.get $l3
                            i32.const -64
                            i32.sub
                            local.get $l4
                            i64.load
                            i64.store
                            local.get $l5
                            i32.const 1
                            i32.add
                            local.set $l5
                            local.get $l7
                            i32.const 1
                            i32.add
                            local.tee $l7
                            local.get $l6
                            i32.load offset=52
                            i32.lt_u
                            br_if $L82
                          end
                        end
                        local.get $l6
                        i32.load offset=16
                        local.tee $l6
                        br_if $L80
                      end
                      local.get $l11
                      local.get $l5
                      i32.store offset=448
                      local.get $l9
                      local.get $l14
                      i64.load offset=8
                      i64.store offset=8
                      local.get $l9
                      local.get $l14
                      i64.load
                      i64.store
                      br $B43
                    end
                    local.get $l9
                    local.get $l16
                    local.get $l8
                    local.get $l17
                    local.get $l6
                    call $f69975
                    local.get $l11
                    i32.const 6
                    i32.store offset=448
                    br $B43
                  end
                  i32.const 0
                  local.set $l5
                  local.get $l6
                  i32.load offset=56
                  i32.const 3
                  i32.le_u
                  if $I83
                    loop $L84
                      local.get $l6
                      i32.load offset=48
                      local.tee $l7
                      local.get $l6
                      i32.load offset=52
                      i32.lt_u
                      if $I85
                        loop $L86
                          local.get $l11
                          local.get $l5
                          i32.const 6
                          i32.shl
                          i32.add
                          local.tee $l3
                          local.get $l8
                          local.get $l7
                          i32.const 6
                          i32.shl
                          i32.add
                          local.tee $l4
                          i32.load offset=48
                          i32.store offset=112
                          local.get $l3
                          local.get $l4
                          i64.load offset=40
                          i64.store offset=104
                          local.get $l3
                          local.get $l4
                          i64.load offset=32
                          i64.store offset=96
                          local.get $l3
                          local.get $l4
                          i64.load offset=24
                          i64.store offset=88
                          local.get $l3
                          local.get $l4
                          i64.load offset=16
                          i64.store offset=80
                          local.get $l3
                          local.get $l4
                          i64.load offset=8
                          i64.store offset=72
                          local.get $l3
                          i32.const -64
                          i32.sub
                          local.get $l4
                          i64.load
                          i64.store
                          local.get $l5
                          i32.const 1
                          i32.add
                          local.set $l5
                          local.get $l7
                          i32.const 1
                          i32.add
                          local.tee $l7
                          local.get $l6
                          i32.load offset=52
                          i32.lt_u
                          br_if $L86
                        end
                      end
                      local.get $l6
                      i32.load offset=16
                      local.tee $l6
                      br_if $L84
                    end
                    local.get $l11
                    local.get $l5
                    i32.store offset=448
                    local.get $l9
                    local.get $l14
                    i64.load offset=8
                    i64.store offset=8
                    local.get $l9
                    local.get $l14
                    i64.load
                    i64.store
                    br $B43
                  end
                  local.get $l9
                  local.get $l16
                  local.get $l8
                  local.get $l17
                  local.get $l6
                  call $f69976
                  local.get $l11
                  i32.const 3
                  i32.store offset=448
                end
                local.get $l13
                local.get $l13
                local.get $l13
                i32.load8_u offset=62
                i32.add
                i32.load8_u offset=56
                i32.const 2
                i32.shl
                i32.add
                local.get $l9
                f32.load
                f32.store offset=32
                local.get $l13
                local.get $l13
                i32.load8_u offset=62
                i32.const 1
                i32.add
                i32.store8 offset=62
                br $B41
              end
              local.get $l7
              i32.const -64
              i32.sub
              local.set $l20
              local.get $l9
              local.get $l3
              i32.store offset=68
              local.get $l9
              local.get $l6
              i32.store offset=40
              local.get $l9
              local.get $l26
              f32.store offset=24
              local.get $l9
              local.get $l27
              f32.store offset=20
              local.get $l9
              local.get $l28
              f32.store offset=16
              local.get $l9
              i64.const 0
              i64.store offset=28 align=4
              local.get $l9
              local.get $l17
              i32.store offset=64
              local.get $l6
              i32.load offset=20
              local.get $l9
              i32.const 16
              i32.add
              i32.store offset=16
              local.get $l6
              local.get $l6
              i32.load offset=56
              local.get $p1
              i32.load
              i32.add
              local.tee $l3
              i32.store offset=56
              local.get $l6
              local.get $l13
              local.get $l16
              i32.load8_u
              i32.const 2
              i32.shl
              i32.add
              f32.load offset=32
              local.tee $l26
              local.get $l6
              f32.load offset=32
              local.tee $l27
              local.get $l26
              local.get $l27
              f32.lt
              select
              f32.store offset=32
              local.get $p1
              i32.load
              local.get $l17
              i32.add
              local.set $l4
              block $B87
                block $B88
                  block $B89
                    block $B90
                      local.get $l10
                      br_table $B90 $B89 $B88 $B89
                    end
                    i32.const -1
                    local.set $l4
                    f32.const 0x1.fffffep+127 (;=3.40282e+38;)
                    local.set $l27
                    f32.const 0x1.fffffep+127 (;=3.40282e+38;)
                    local.set $l26
                    loop $L91
                      block $B92
                        local.get $l6
                        i32.load offset=52
                        local.tee $l11
                        local.get $l6
                        i32.load offset=48
                        local.tee $l3
                        i32.le_u
                        br_if $B92
                        local.get $l11
                        local.get $l3
                        i32.const -1
                        i32.xor
                        i32.add
                        local.set $l12
                        local.get $l11
                        local.get $l3
                        i32.sub
                        i32.const 3
                        i32.and
                        local.tee $l5
                        if $I93
                          loop $L94
                            local.get $l8
                            local.get $l3
                            i32.const 6
                            i32.shl
                            i32.add
                            f32.load offset=44
                            local.tee $l28
                            local.get $l26
                            local.get $l26
                            local.get $l28
                            f32.gt
                            local.tee $l7
                            select
                            local.set $l26
                            local.get $l28
                            local.get $l27
                            local.get $l7
                            select
                            local.set $l27
                            local.get $l3
                            local.get $l4
                            local.get $l7
                            select
                            local.set $l4
                            local.get $l3
                            i32.const 1
                            i32.add
                            local.set $l3
                            local.get $l5
                            i32.const 1
                            i32.sub
                            local.tee $l5
                            br_if $L94
                          end
                        end
                        local.get $l12
                        i32.const 2
                        i32.le_u
                        br_if $B92
                        loop $L95
                          local.get $l8
                          local.get $l3
                          i32.const 3
                          i32.add
                          local.tee $l19
                          i32.const 6
                          i32.shl
                          i32.add
                          f32.load offset=44
                          local.tee $l28
                          local.get $l8
                          local.get $l3
                          i32.const 2
                          i32.add
                          local.tee $l21
                          i32.const 6
                          i32.shl
                          i32.add
                          f32.load offset=44
                          local.tee $l29
                          local.get $l8
                          local.get $l3
                          i32.const 1
                          i32.add
                          local.tee $l14
                          i32.const 6
                          i32.shl
                          i32.add
                          f32.load offset=44
                          local.tee $l30
                          local.get $l8
                          local.get $l3
                          i32.const 6
                          i32.shl
                          i32.add
                          f32.load offset=44
                          local.tee $l31
                          local.get $l26
                          local.get $l26
                          local.get $l31
                          f32.gt
                          local.tee $l7
                          select
                          local.tee $l26
                          local.get $l26
                          local.get $l30
                          f32.gt
                          local.tee $l5
                          select
                          local.tee $l26
                          local.get $l26
                          local.get $l29
                          f32.gt
                          local.tee $l12
                          select
                          local.tee $l26
                          local.get $l26
                          local.get $l28
                          f32.gt
                          local.tee $l18
                          select
                          local.set $l26
                          local.get $l28
                          local.get $l29
                          local.get $l30
                          local.get $l31
                          local.get $l27
                          local.get $l7
                          select
                          local.get $l5
                          select
                          local.get $l12
                          select
                          local.get $l18
                          select
                          local.set $l27
                          local.get $l19
                          local.get $l21
                          local.get $l14
                          local.get $l3
                          local.get $l4
                          local.get $l7
                          select
                          local.get $l5
                          select
                          local.get $l12
                          select
                          local.get $l18
                          select
                          local.set $l4
                          local.get $l3
                          i32.const 4
                          i32.add
                          local.tee $l3
                          local.get $l11
                          i32.ne
                          br_if $L95
                        end
                      end
                      local.get $l6
                      i32.load offset=16
                      local.tee $l6
                      br_if $L91
                    end
                    local.get $l9
                    local.get $l27
                    f32.store
                    local.get $l20
                    local.get $l8
                    local.get $l4
                    i32.const 6
                    i32.shl
                    i32.add
                    local.tee $l3
                    i64.load
                    i64.store
                    local.get $l20
                    local.get $l3
                    i32.load offset=48
                    i32.store offset=48
                    local.get $l20
                    local.get $l3
                    i64.load offset=40
                    i64.store offset=40
                    local.get $l20
                    local.get $l3
                    i64.load offset=32
                    i64.store offset=32
                    local.get $l20
                    local.get $l3
                    i64.load offset=24
                    i64.store offset=24
                    local.get $l20
                    local.get $l3
                    i64.load offset=16
                    i64.store offset=16
                    local.get $l20
                    local.get $l3
                    i64.load offset=8
                    i64.store offset=8
                    local.get $p1
                    i32.const 1
                    i32.store
                    br $B87
                  end
                  i32.const 0
                  local.set $l12
                  local.get $l3
                  i32.const 6
                  i32.le_u
                  if $I96
                    loop $L97
                      local.get $l6
                      i32.load offset=48
                      local.tee $l5
                      local.get $l6
                      i32.load offset=52
                      i32.lt_u
                      if $I98
                        loop $L99
                          local.get $l7
                          local.get $l12
                          i32.const 6
                          i32.shl
                          i32.add
                          local.tee $l3
                          local.get $l8
                          local.get $l5
                          i32.const 6
                          i32.shl
                          i32.add
                          local.tee $l4
                          i32.load offset=48
                          i32.store offset=112
                          local.get $l3
                          local.get $l4
                          i64.load offset=40
                          i64.store offset=104
                          local.get $l3
                          local.get $l4
                          i64.load offset=32
                          i64.store offset=96
                          local.get $l3
                          local.get $l4
                          i64.load offset=24
                          i64.store offset=88
                          local.get $l3
                          local.get $l4
                          i64.load offset=16
                          i64.store offset=80
                          local.get $l3
                          local.get $l4
                          i64.load offset=8
                          i64.store offset=72
                          local.get $l3
                          i32.const -64
                          i32.sub
                          local.get $l4
                          i64.load
                          i64.store
                          local.get $l12
                          i32.const 1
                          i32.add
                          local.set $l12
                          local.get $l5
                          i32.const 1
                          i32.add
                          local.tee $l5
                          local.get $l6
                          i32.load offset=52
                          i32.lt_u
                          br_if $L99
                        end
                      end
                      local.get $l6
                      i32.load offset=16
                      local.tee $l6
                      br_if $L97
                    end
                    local.get $p1
                    local.get $l12
                    i32.store
                    local.get $l9
                    local.get $l14
                    i64.load offset=8
                    i64.store offset=8
                    local.get $l9
                    local.get $l14
                    i64.load
                    i64.store
                    br $B87
                  end
                  local.get $l9
                  local.get $l20
                  local.get $l8
                  local.get $l4
                  local.get $l6
                  call $f69975
                  local.get $p1
                  i32.const 6
                  i32.store
                  br $B87
                end
                i32.const 0
                local.set $l12
                local.get $l3
                i32.const 3
                i32.le_u
                if $I100
                  loop $L101
                    local.get $l6
                    i32.load offset=48
                    local.tee $l5
                    local.get $l6
                    i32.load offset=52
                    i32.lt_u
                    if $I102
                      loop $L103
                        local.get $l7
                        local.get $l12
                        i32.const 6
                        i32.shl
                        i32.add
                        local.tee $l3
                        local.get $l8
                        local.get $l5
                        i32.const 6
                        i32.shl
                        i32.add
                        local.tee $l4
                        i32.load offset=48
                        i32.store offset=112
                        local.get $l3
                        local.get $l4
                        i64.load offset=40
                        i64.store offset=104
                        local.get $l3
                        local.get $l4
                        i64.load offset=32
                        i64.store offset=96
                        local.get $l3
                        local.get $l4
                        i64.load offset=24
                        i64.store offset=88
                        local.get $l3
                        local.get $l4
                        i64.load offset=16
                        i64.store offset=80
                        local.get $l3
                        local.get $l4
                        i64.load offset=8
                        i64.store offset=72
                        local.get $l3
                        i32.const -64
                        i32.sub
                        local.get $l4
                        i64.load
                        i64.store
                        local.get $l12
                        i32.const 1
                        i32.add
                        local.set $l12
                        local.get $l5
                        i32.const 1
                        i32.add
                        local.tee $l5
                        local.get $l6
                        i32.load offset=52
                        i32.lt_u
                        br_if $L103
                      end
                    end
                    local.get $l6
                    i32.load offset=16
                    local.tee $l6
                    br_if $L101
                  end
                  local.get $p1
                  local.get $l12
                  i32.store
                  local.get $l9
                  local.get $l14
                  i64.load offset=8
                  i64.store offset=8
                  local.get $l9
                  local.get $l14
                  i64.load
                  i64.store
                  br $B87
                end
                local.get $l9
                local.get $l20
                local.get $l8
                local.get $l4
                local.get $l6
                call $f69976
                local.get $p1
                i32.const 3
                i32.store
              end
              local.get $l13
              local.get $l16
              i32.load8_u
              i32.const 2
              i32.shl
              i32.add
              local.get $l9
              f32.load
              f32.store offset=32
            end
            local.get $l15
            i32.const 1
            i32.add
            local.tee $l15
            local.get $l22
            i32.ne
            br_if $L40
          end
        end
        local.get $l9
        i32.const 80
        i32.add
        global.set $g0
      end
      local.get $p0
      i64.const 0
      i64.store offset=2324 align=4
      local.get $p2
      i32.eqz
      br_if $B0
      local.get $p0
      local.get $p0
      i32.store offset=2048
      local.get $p0
      i32.const 2172
      i32.add
      local.get $p0
      i32.const 1984
      i32.add
      i32.store
      local.get $p0
      i32.const 2168
      i32.add
      local.get $p0
      i32.const 1920
      i32.add
      i32.store
      local.get $p0
      i32.const 2164
      i32.add
      local.get $p0
      i32.const 1856
      i32.add
      i32.store
      local.get $p0
      i32.const 2160
      i32.add
      local.get $p0
      i32.const 1792
      i32.add
      i32.store
      local.get $p0
      i32.const 2156
      i32.add
      local.get $p0
      i32.const 1728
      i32.add
      i32.store
      local.get $p0
      i32.const 2152
      i32.add
      local.get $p0
      i32.const 1664
      i32.add
      i32.store
      local.get $p0
      i32.const 2148
      i32.add
      local.get $p0
      i32.const 1600
      i32.add
      i32.store
      local.get $p0
      i32.const 2144
      i32.add
      local.get $p0
      i32.const 1536
      i32.add
      i32.store
      local.get $p0
      i32.const 2140
      i32.add
      local.get $p0
      i32.const 1472
      i32.add
      i32.store
      local.get $p0
      i32.const 2136
      i32.add
      local.get $p0
      i32.const 1408
      i32.add
      i32.store
      local.get $p0
      i32.const 2132
      i32.add
      local.get $p0
      i32.const 1344
      i32.add
      i32.store
      local.get $p0
      i32.const 2128
      i32.add
      local.get $p0
      i32.const 1280
      i32.add
      i32.store
      local.get $p0
      i32.const 2124
      i32.add
      local.get $p0
      i32.const 1216
      i32.add
      i32.store
      local.get $p0
      i32.const 2120
      i32.add
      local.get $p0
      i32.const 1152
      i32.add
      i32.store
      local.get $p0
      i32.const 2116
      i32.add
      local.get $p0
      i32.const 1088
      i32.add
      i32.store
      local.get $p0
      i32.const 2112
      i32.add
      local.get $p0
      i32.const 1024
      i32.add
      i32.store
      local.get $p0
      i32.const 2108
      i32.add
      local.get $p0
      i32.const 960
      i32.add
      i32.store
      local.get $p0
      i32.const 2104
      i32.add
      local.get $p0
      i32.const 896
      i32.add
      i32.store
      local.get $p0
      i32.const 2100
      i32.add
      local.get $p0
      i32.const 832
      i32.add
      i32.store
      local.get $p0
      i32.const 2096
      i32.add
      local.get $p0
      i32.const 768
      i32.add
      i32.store
      local.get $p0
      i32.const 2092
      i32.add
      local.get $p0
      i32.const 704
      i32.add
      i32.store
      local.get $p0
      i32.const 2088
      i32.add
      local.get $p0
      i32.const 640
      i32.add
      i32.store
      local.get $p0
      i32.const 2084
      i32.add
      local.get $p0
      i32.const 576
      i32.add
      i32.store
      local.get $p0
      i32.const 2080
      i32.add
      local.get $p0
      i32.const 512
      i32.add
      i32.store
      local.get $p0
      i32.const 2076
      i32.add
      local.get $p0
      i32.const 448
      i32.add
      i32.store
      local.get $p0
      i32.const 2072
      i32.add
      local.get $p0
      i32.const 384
      i32.add
      i32.store
      local.get $p0
      i32.const 2068
      i32.add
      local.get $p0
      i32.const 320
      i32.add
      i32.store
      local.get $p0
      i32.const 2064
      i32.add
      local.get $p0
      i32.const 256
      i32.add
      i32.store
      local.get $p0
      i32.const 2060
      i32.add
      local.get $p0
      i32.const 192
      i32.add
      i32.store
      local.get $p0
      i32.const 2056
      i32.add
      local.get $p0
      i32.const 128
      i32.add
      i32.store
      local.get $p0
      i32.const 2052
      i32.add
      local.get $p0
      i32.const -64
      i32.sub
      i32.store
    end)
