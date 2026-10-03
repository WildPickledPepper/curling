  (func $f70733 (type $t7) (param $p0 i32)
    (local $l1 i32) (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 i32) (local $l17 i32) (local $l18 i32) (local $l19 i32) (local $l20 i32) (local $l21 i32) (local $l22 i32) (local $l23 i32) (local $l24 i32) (local $l25 i32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32) (local $l33 f32) (local $l34 f32) (local $l35 f32) (local $l36 f32) (local $l37 f32) (local $l38 f32) (local $l39 f32) (local $l40 f32) (local $l41 f32) (local $l42 f32) (local $l43 f32) (local $l44 f32) (local $l45 i64)
    global.get $g0
    i32.const 128
    i32.sub
    local.tee $l8
    global.set $g0
    local.get $p0
    i32.load offset=36
    local.tee $l2
    i32.load offset=304
    call $f69738
    local.tee $l21
    i32.eqz
    if $I0
      call $f69753
      local.tee $l12
      i32.const 7251
      i32.const 3134080
      i32.const 3134052
      i32.const 4700888
      i32.load
      local.tee $l3
      local.get $l3
      i32.load
      i32.load offset=20
      call_indirect $__indirect_function_table (type $t5)
      select
      i32.const 3133984
      i32.const 82
      local.get $l12
      i32.load
      i32.load offset=8
      call_indirect $__indirect_function_table (type $t9)
      local.tee $l3
      i32.const 19
      i32.add
      i32.const -16
      i32.and
      local.tee $l12
      i32.const 4
      i32.sub
      local.get $l12
      local.get $l3
      i32.sub
      i32.store
      local.get $l12
      local.get $l2
      i32.load offset=308
      call $f70586
      local.set $l21
    end
    block $B1
      local.get $p0
      i32.load offset=56
      local.tee $l17
      local.get $l17
      local.get $p0
      i32.load offset=60
      i32.add
      local.tee $l2
      local.get $p0
      i32.load offset=64
      local.tee $l12
      local.get $l2
      local.get $l12
      i32.lt_u
      select
      local.tee $l23
      i32.ge_u
      br_if $B1
      local.get $l8
      i32.const 48
      i32.add
      local.set $l24
      local.get $p0
      i32.load offset=40
      f32.load offset=328
      local.set $l41
      local.get $p0
      i32.load offset=68
      local.set $l13
      loop $L2
        local.get $l13
        local.get $p0
        i32.load offset=32
        local.tee $l2
        i32.ge_u
        br_if $B1
        block $B3
          block $B4
            local.get $l2
            local.get $l13
            i32.const 1
            i32.add
            local.tee $l1
            i32.le_u
            if $I5
              local.get $l1
              local.set $l12
              br $B4
            end
            local.get $p0
            i32.load offset=28
            local.set $l3
            local.get $l1
            local.set $l12
            block $B6
              loop $L7
                local.get $l3
                local.get $l12
                i32.const 2
                i32.shl
                i32.add
                i32.load
                i32.load offset=56
                local.get $l17
                i32.ne
                br_if $B6
                local.get $l12
                i32.const 1
                i32.add
                local.tee $l12
                local.get $l2
                i32.ne
                br_if $L7
              end
              local.get $l2
              local.set $l12
            end
            local.get $l1
            local.get $l12
            i32.lt_u
            if $I8
              local.get $p0
              i32.load offset=28
              local.get $l13
              i32.const 2
              i32.shl
              i32.add
              local.set $l5
              i32.const 0
              local.set $l7
              i32.const 0
              local.set $l14
              i32.const 0
              local.set $l18
              i32.const 32
              local.set $l16
              global.get $g0
              i32.const 16
              i32.sub
              local.tee $l1
              global.set $g0
              local.get $l1
              local.tee $l15
              i32.const 0
              i32.store8 offset=12
              local.get $l1
              i32.const 128
              i32.sub
              local.tee $l6
              global.set $g0
              local.get $l1
              local.get $l6
              i32.store offset=8
              block $B9
                local.get $l12
                local.get $l13
                i32.sub
                i32.const 1
                i32.sub
                local.tee $l9
                i32.const 0
                i32.le_s
                br_if $B9
                loop $L10
                  block $B11
                    local.get $l7
                    local.get $l9
                    i32.ge_s
                    br_if $B11
                    loop $L12
                      local.get $l9
                      local.get $l7
                      i32.sub
                      i32.const 4
                      i32.le_u
                      if $I13
                        loop $L14
                          local.get $l7
                          local.tee $l4
                          i32.const 1
                          i32.add
                          local.tee $l7
                          local.set $l1
                          local.get $l4
                          local.set $l2
                          loop $L15
                            block $B16
                              local.get $l5
                              local.get $l1
                              local.tee $l3
                              i32.const 2
                              i32.shl
                              i32.add
                              i32.load
                              local.tee $l1
                              f32.load offset=28
                              local.tee $l26
                              local.get $l5
                              local.get $l2
                              i32.const 2
                              i32.shl
                              i32.add
                              i32.load
                              local.tee $l10
                              f32.load offset=28
                              local.tee $l27
                              f32.lt
                              i32.eqz
                              if $I17
                                local.get $l26
                                local.get $l27
                                f32.ne
                                br_if $B16
                                local.get $l1
                                i32.load offset=4
                                i32.eqz
                                br_if $B16
                                local.get $l10
                                i32.load offset=4
                                br_if $B16
                              end
                              local.get $l3
                              local.set $l2
                            end
                            local.get $l3
                            i32.const 1
                            i32.add
                            local.set $l1
                            local.get $l3
                            local.get $l9
                            i32.lt_s
                            br_if $L15
                          end
                          local.get $l2
                          local.get $l4
                          i32.ne
                          if $I18
                            local.get $l5
                            local.get $l2
                            i32.const 2
                            i32.shl
                            i32.add
                            local.tee $l3
                            i32.load
                            local.set $l1
                            local.get $l3
                            local.get $l5
                            local.get $l4
                            i32.const 2
                            i32.shl
                            i32.add
                            local.tee $l2
                            i32.load
                            i32.store
                            local.get $l2
                            local.get $l1
                            i32.store
                          end
                          local.get $l7
                          local.get $l9
                          i32.ne
                          br_if $L14
                          br $B11
                        end
                        unreachable
                      end
                      block $B19
                        block $B20
                          local.get $l5
                          local.get $l7
                          local.get $l9
                          i32.add
                          i32.const 2
                          i32.div_s
                          i32.const 2
                          i32.shl
                          i32.add
                          local.tee $l3
                          i32.load
                          local.tee $l4
                          f32.load offset=28
                          local.tee $l27
                          local.get $l5
                          local.get $l7
                          i32.const 2
                          i32.shl
                          i32.add
                          local.tee $l10
                          i32.load
                          local.tee $l2
                          f32.load offset=28
                          local.tee $l26
                          f32.lt
                          br_if $B20
                          local.get $l26
                          local.get $l27
                          f32.ne
                          if $I21
                            local.get $l2
                            local.set $l1
                            br $B19
                          end
                          local.get $l4
                          i32.load offset=4
                          i32.eqz
                          if $I22
                            local.get $l2
                            local.set $l1
                            br $B19
                          end
                          local.get $l2
                          i32.load offset=4
                          i32.eqz
                          br_if $B20
                          local.get $l2
                          local.set $l1
                          br $B19
                        end
                        local.get $l10
                        local.get $l4
                        i32.store
                        local.get $l3
                        local.get $l2
                        i32.store
                        local.get $l10
                        i32.load
                        local.tee $l1
                        f32.load offset=28
                        local.set $l26
                        local.get $l2
                        local.set $l4
                      end
                      block $B23
                        block $B24
                          local.get $l5
                          local.get $l9
                          i32.const 2
                          i32.shl
                          i32.add
                          local.tee $l19
                          i32.load
                          local.tee $l2
                          f32.load offset=28
                          local.tee $l27
                          local.get $l26
                          f32.lt
                          br_if $B24
                          local.get $l26
                          local.get $l27
                          f32.ne
                          if $I25
                            local.get $l2
                            local.set $l1
                            br $B23
                          end
                          local.get $l2
                          i32.load offset=4
                          i32.eqz
                          if $I26
                            local.get $l2
                            local.set $l1
                            br $B23
                          end
                          local.get $l1
                          i32.load offset=4
                          i32.eqz
                          br_if $B24
                          local.get $l2
                          local.set $l1
                          br $B23
                        end
                        local.get $l10
                        local.get $l2
                        i32.store
                        local.get $l19
                        local.get $l1
                        i32.store
                        local.get $l3
                        i32.load
                        local.set $l4
                        local.get $l1
                        f32.load offset=28
                        local.set $l27
                      end
                      block $B27
                        local.get $l27
                        local.get $l4
                        f32.load offset=28
                        local.tee $l26
                        f32.lt
                        i32.eqz
                        if $I28
                          local.get $l26
                          local.get $l27
                          f32.ne
                          br_if $B27
                          local.get $l1
                          i32.load offset=4
                          i32.eqz
                          br_if $B27
                          local.get $l4
                          i32.load offset=4
                          br_if $B27
                        end
                        local.get $l3
                        local.get $l1
                        i32.store
                        local.get $l19
                        local.get $l4
                        i32.store
                        local.get $l3
                        i32.load
                        local.set $l4
                      end
                      local.get $l3
                      local.get $l5
                      local.get $l9
                      i32.const 1
                      i32.sub
                      local.tee $l1
                      i32.const 2
                      i32.shl
                      i32.add
                      local.tee $l20
                      i32.load
                      i32.store
                      local.get $l20
                      local.get $l4
                      i32.store
                      local.get $l7
                      local.set $l3
                      loop $L29
                        local.get $l4
                        f32.load offset=28
                        local.set $l26
                        loop $L30
                          local.get $l5
                          local.get $l3
                          local.tee $l11
                          i32.const 1
                          i32.add
                          local.tee $l3
                          i32.const 2
                          i32.shl
                          i32.add
                          local.tee $l19
                          i32.load
                          local.tee $l2
                          f32.load offset=28
                          local.tee $l27
                          local.get $l26
                          f32.lt
                          br_if $L30
                          block $B31
                            local.get $l26
                            local.get $l27
                            f32.ne
                            br_if $B31
                            local.get $l2
                            i32.load offset=4
                            i32.eqz
                            br_if $B31
                            local.get $l4
                            i32.load offset=4
                            i32.eqz
                            br_if $L30
                          end
                        end
                        loop $L32
                          local.get $l26
                          local.get $l5
                          local.get $l1
                          i32.const 1
                          i32.sub
                          local.tee $l1
                          i32.const 2
                          i32.shl
                          i32.add
                          local.tee $l25
                          i32.load
                          local.tee $l10
                          f32.load offset=28
                          local.tee $l27
                          f32.lt
                          br_if $L32
                          block $B33
                            local.get $l26
                            local.get $l27
                            f32.ne
                            br_if $B33
                            local.get $l4
                            i32.load offset=4
                            i32.eqz
                            br_if $B33
                            local.get $l10
                            i32.load offset=4
                            i32.eqz
                            br_if $L32
                          end
                        end
                        local.get $l1
                        local.get $l3
                        i32.gt_s
                        if $I34
                          local.get $l19
                          local.get $l10
                          i32.store
                          local.get $l25
                          local.get $l2
                          i32.store
                          local.get $l20
                          i32.load
                          local.set $l4
                          br $L29
                        end
                      end
                      local.get $l19
                      local.get $l4
                      i32.store
                      local.get $l20
                      local.get $l2
                      i32.store
                      block $B35
                        local.get $l3
                        local.get $l7
                        i32.sub
                        local.get $l9
                        local.get $l3
                        i32.sub
                        i32.lt_s
                        if $I36
                          block $B37
                            local.get $l16
                            i32.const 1
                            i32.sub
                            local.get $l14
                            i32.gt_u
                            if $I38
                              local.get $l6
                              local.set $l3
                              br $B37
                            end
                            local.get $l16
                            i32.const 3
                            i32.shl
                            local.tee $l3
                            if $I39 (result i32)
                              call $f69753
                              local.tee $l1
                              local.get $l3
                              i32.const 3134425
                              i32.const 3134052
                              i32.const 4700888
                              i32.load
                              local.tee $l2
                              local.get $l2
                              i32.load
                              i32.load offset=20
                              call_indirect $__indirect_function_table (type $t5)
                              select
                              i32.const 3134375
                              i32.const 155
                              local.get $l1
                              i32.load
                              i32.load offset=8
                              call_indirect $__indirect_function_table (type $t9)
                            else
                              i32.const 0
                            end
                            local.tee $l3
                            local.get $l6
                            local.get $l14
                            i32.const 2
                            i32.shl
                            call $f483
                            local.set $l1
                            block $B40
                              local.get $l6
                              i32.eqz
                              br_if $B40
                              local.get $l18
                              i32.eqz
                              br_if $B40
                              call $f69753
                              local.tee $l2
                              local.get $l6
                              local.get $l2
                              i32.load
                              i32.load offset=12
                              call_indirect $__indirect_function_table (type $t1)
                            end
                            local.get $l16
                            i32.const 1
                            i32.shl
                            local.set $l16
                            i32.const 1
                            local.set $l18
                            local.get $l1
                            local.set $l6
                          end
                          local.get $l3
                          local.get $l14
                          i32.const 2
                          i32.shl
                          i32.add
                          local.tee $l3
                          local.get $l7
                          i32.store
                          local.get $l3
                          local.get $l11
                          i32.store offset=4
                          local.get $l11
                          i32.const 2
                          i32.add
                          local.set $l7
                          br $B35
                        end
                        local.get $l11
                        i32.const 2
                        i32.add
                        local.set $l1
                        block $B41
                          local.get $l16
                          i32.const 1
                          i32.sub
                          local.get $l14
                          i32.gt_u
                          if $I42
                            local.get $l6
                            local.set $l3
                            br $B41
                          end
                          local.get $l16
                          i32.const 3
                          i32.shl
                          local.tee $l3
                          if $I43 (result i32)
                            call $f69753
                            local.tee $l2
                            local.get $l3
                            i32.const 3134425
                            i32.const 3134052
                            i32.const 4700888
                            i32.load
                            local.tee $l10
                            local.get $l10
                            i32.load
                            i32.load offset=20
                            call_indirect $__indirect_function_table (type $t5)
                            select
                            i32.const 3134375
                            i32.const 155
                            local.get $l2
                            i32.load
                            i32.load offset=8
                            call_indirect $__indirect_function_table (type $t9)
                          else
                            i32.const 0
                          end
                          local.tee $l3
                          local.get $l6
                          local.get $l14
                          i32.const 2
                          i32.shl
                          call $f483
                          local.set $l2
                          block $B44
                            local.get $l6
                            i32.eqz
                            br_if $B44
                            local.get $l18
                            i32.eqz
                            br_if $B44
                            call $f69753
                            local.tee $l10
                            local.get $l6
                            local.get $l10
                            i32.load
                            i32.load offset=12
                            call_indirect $__indirect_function_table (type $t1)
                          end
                          local.get $l16
                          i32.const 1
                          i32.shl
                          local.set $l16
                          i32.const 1
                          local.set $l18
                          local.get $l2
                          local.set $l6
                        end
                        local.get $l3
                        local.get $l14
                        i32.const 2
                        i32.shl
                        i32.add
                        local.tee $l3
                        local.get $l1
                        i32.store
                        local.get $l3
                        local.get $l9
                        i32.store offset=4
                        local.get $l11
                        local.set $l9
                      end
                      local.get $l14
                      i32.const 2
                      i32.add
                      local.set $l14
                      local.get $l7
                      local.get $l9
                      i32.lt_s
                      br_if $L12
                    end
                  end
                  local.get $l14
                  if $I45
                    local.get $l6
                    local.get $l14
                    i32.const 2
                    i32.sub
                    local.tee $l3
                    i32.const 2
                    i32.shl
                    i32.add
                    i32.load
                    local.set $l7
                    local.get $l14
                    i32.const 2
                    i32.shl
                    local.get $l6
                    i32.add
                    i32.const 4
                    i32.sub
                    i32.load
                    local.set $l9
                    local.get $l3
                    local.set $l14
                    br $L10
                  end
                end
                local.get $l6
                i32.eqz
                br_if $B9
                local.get $l18
                i32.eqz
                br_if $B9
                call $f69753
                local.tee $l5
                local.get $l6
                local.get $l5
                i32.load
                i32.load offset=12
                call_indirect $__indirect_function_table (type $t1)
              end
              local.get $l15
              i32.load8_u offset=12
              if $I46
                local.get $l15
                i32.load offset=8
                call $f70044
              end
              local.get $l15
              i32.const 16
              i32.add
              global.set $g0
            end
            local.get $l12
            local.get $l13
            i32.le_u
            br_if $B3
          end
          local.get $l12
          i32.const 3
          i32.sub
          local.set $l16
          local.get $l17
          i32.const 1
          i32.sub
          local.set $l19
          local.get $p0
          f32.load offset=44
          local.set $l35
          i32.const 1
          local.set $l14
          loop $L47
            local.get $p0
            i32.load offset=28
            local.get $l13
            i32.const 2
            i32.shl
            i32.add
            i32.load
            local.tee $l2
            f32.load offset=28
            local.tee $l26
            f32.const 0x1p+0 (;=1;)
            f32.gt
            br_if $B3
            local.get $l2
            i32.load
            local.tee $l3
            if $I48 (result i32)
              local.get $l3
              i32.load offset=32
              i32.load8_u offset=34
            else
              i32.const 1
            end
            i32.eqz
            local.set $l3
            block $B49
              local.get $l2
              i32.load offset=4
              local.tee $l1
              if $I50 (result i32)
                local.get $l3
                local.get $l1
                i32.load offset=32
                i32.load8_u offset=34
                i32.eqz
                i32.or
              else
                local.get $l3
              end
              i32.eqz
              br_if $B49
              block $B51
                local.get $l2
                i32.load offset=104
                br_if $B51
                local.get $l21
                local.set $l10
                local.get $l35
                local.set $l26
                local.get $l41
                local.set $l29
                global.get $g0
                i32.const 192
                i32.sub
                local.tee $l5
                global.set $g0
                local.get $l2
                call $f70616
                local.get $l2
                i32.load offset=12
                local.set $l3
                local.get $l2
                i32.load offset=8
                local.set $l11
                local.get $l2
                i32.load offset=4
                local.set $l6
                local.get $l2
                i32.load
                local.set $l15
                block $B52
                  local.get $l2
                  i32.load offset=64
                  local.tee $l9
                  local.get $l2
                  i32.load offset=60
                  local.tee $l1
                  i32.ge_s
                  if $I53
                    local.get $l9
                    local.set $l7
                    local.get $l1
                    local.set $l9
                    local.get $l3
                    local.set $l1
                    local.get $l11
                    local.set $l3
                    local.get $l6
                    local.set $l4
                    local.get $l15
                    local.set $l6
                    br $B52
                  end
                  local.get $l1
                  local.set $l7
                  local.get $l11
                  local.set $l1
                  local.get $l15
                  local.set $l4
                end
                local.get $l5
                local.get $l3
                f32.load offset=36
                f32.store offset=160
                local.get $l5
                local.get $l3
                f32.load offset=40
                f32.store offset=164
                local.get $l5
                local.get $l3
                f32.load offset=44
                f32.store offset=168
                local.get $l5
                local.get $l3
                f32.load offset=48
                f32.store offset=172
                local.get $l5
                local.get $l3
                f32.load offset=52
                local.tee $l30
                f32.store offset=176
                local.get $l5
                local.get $l3
                f32.load offset=56
                local.tee $l32
                f32.store offset=180
                local.get $l5
                local.get $l3
                f32.load offset=60
                local.tee $l33
                f32.store offset=184
                local.get $l5
                local.get $l3
                f32.load offset=8
                f32.store offset=96
                local.get $l5
                local.get $l3
                f32.load offset=12
                f32.store offset=100
                local.get $l5
                local.get $l3
                f32.load offset=16
                f32.store offset=104
                local.get $l5
                local.get $l3
                f32.load offset=20
                f32.store offset=108
                local.get $l5
                local.get $l3
                f32.load offset=24
                local.tee $l34
                f32.store offset=112
                local.get $l5
                local.get $l3
                f32.load offset=28
                local.tee $l27
                f32.store offset=116
                local.get $l5
                local.get $l3
                f32.load offset=32
                local.tee $l31
                f32.store offset=120
                local.get $l5
                local.get $l1
                f32.load offset=36
                f32.store offset=128
                local.get $l5
                local.get $l1
                f32.load offset=40
                f32.store offset=132
                local.get $l5
                local.get $l1
                f32.load offset=44
                f32.store offset=136
                local.get $l5
                local.get $l1
                f32.load offset=48
                f32.store offset=140
                local.get $l5
                local.get $l1
                f32.load offset=52
                local.tee $l38
                f32.store offset=144
                local.get $l5
                local.get $l1
                f32.load offset=56
                local.tee $l39
                f32.store offset=148
                local.get $l5
                local.get $l1
                f32.load offset=60
                local.tee $l40
                f32.store offset=152
                local.get $l5
                local.get $l1
                f32.load offset=8
                f32.store offset=64
                local.get $l5
                local.get $l1
                f32.load offset=12
                f32.store offset=68
                local.get $l5
                local.get $l1
                f32.load offset=16
                f32.store offset=72
                local.get $l5
                local.get $l1
                f32.load offset=20
                f32.store offset=76
                local.get $l5
                local.get $l1
                f32.load offset=24
                local.tee $l42
                f32.store offset=80
                local.get $l5
                local.get $l1
                f32.load offset=28
                local.tee $l43
                f32.store offset=84
                local.get $l5
                local.get $l1
                f32.load offset=32
                local.tee $l44
                f32.store offset=88
                local.get $l5
                i32.const 0
                i32.store offset=56
                local.get $l5
                i64.const 0
                i64.store offset=48
                local.get $l5
                i32.const 0
                i32.store offset=40
                local.get $l5
                i64.const 0
                i64.store offset=32
                local.get $l2
                i32.load offset=52
                f32.load offset=52
                local.set $l28
                local.get $l10
                i32.const -1
                i32.store offset=7160
                local.get $l10
                local.get $l26
                f32.store offset=7152
                block $B54
                  local.get $l3
                  local.get $l1
                  local.get $l5
                  i32.const 160
                  i32.add
                  local.get $l5
                  i32.const 128
                  i32.add
                  local.get $l5
                  i32.const 96
                  i32.add
                  local.get $l5
                  i32.const -64
                  i32.sub
                  local.get $l28
                  f32.const 0x0p+0 (;=0;)
                  local.get $l28
                  f32.const 0x0p+0 (;=0;)
                  f32.gt
                  select
                  local.get $l5
                  i32.const 48
                  i32.add
                  local.get $l5
                  i32.const 32
                  i32.add
                  local.get $l2
                  f32.load offset=28
                  local.get $l10
                  i32.const 7160
                  i32.add
                  local.tee $l11
                  local.get $l3
                  f32.load offset=4
                  local.tee $l37
                  local.get $l1
                  f32.load offset=4
                  local.tee $l36
                  f32.add
                  local.tee $l28
                  local.get $l29
                  local.get $l28
                  local.get $l29
                  f32.lt
                  select
                  local.tee $l28
                  local.get $l3
                  i32.load
                  i32.load
                  i32.const 28
                  i32.mul
                  local.get $l1
                  i32.load
                  i32.load
                  i32.const 2
                  i32.shl
                  i32.add
                  i32.const 4117520
                  i32.add
                  i32.load
                  call_indirect $__indirect_function_table (type $t171)
                  local.tee $l29
                  f32.const 0x1p+0 (;=1;)
                  f32.ge
                  if $I55
                    local.get $l2
                    i32.const 0
                    i32.store offset=48
                    local.get $l2
                    i32.const 1
                    i32.store offset=104
                    local.get $l2
                    i64.const 2139095039
                    i64.store offset=28 align=4
                    br $B54
                  end
                  local.get $l2
                  local.get $l11
                  i32.load
                  i32.store offset=72
                  local.get $l32
                  local.get $l27
                  f32.sub
                  local.get $l39
                  local.get $l43
                  f32.sub
                  f32.sub
                  local.get $l5
                  f32.load offset=52
                  local.tee $l27
                  f32.neg
                  local.tee $l26
                  f32.mul
                  local.get $l30
                  local.get $l34
                  f32.sub
                  local.get $l38
                  local.get $l42
                  f32.sub
                  f32.sub
                  local.get $l5
                  f32.load offset=48
                  local.tee $l30
                  f32.mul
                  f32.sub
                  local.get $l33
                  local.get $l31
                  f32.sub
                  local.get $l40
                  local.get $l44
                  f32.sub
                  f32.sub
                  local.get $l5
                  f32.load offset=56
                  local.tee $l32
                  f32.mul
                  f32.sub
                  local.set $l33
                  block $B56
                    local.get $l2
                    i32.load offset=64
                    local.get $l2
                    i32.load offset=60
                    i32.lt_s
                    if $I57
                      local.get $l27
                      local.set $l26
                      br $B56
                    end
                    local.get $l5
                    local.get $l26
                    f32.store offset=52
                    local.get $l5
                    local.get $l32
                    f32.neg
                    local.tee $l32
                    f32.store offset=56
                    local.get $l5
                    local.get $l30
                    f32.neg
                    local.tee $l30
                    f32.store offset=48
                  end
                  local.get $l2
                  i32.const 1
                  i32.store offset=104
                  local.get $l28
                  local.get $l33
                  f32.gt
                  if $I58
                    local.get $l2
                    i32.const 2139095039
                    i32.store offset=28
                    br $B54
                  end
                  f32.const 0x0p+0 (;=0;)
                  local.set $l28
                  block $B59
                    local.get $l29
                    f32.const 0x0p+0 (;=0;)
                    f32.le
                    i32.eqz
                    if $I60
                      f32.const 0x0p+0 (;=0;)
                      local.set $l34
                      br $B59
                    end
                    f32.const 0x1p+0 (;=1;)
                    local.set $l28
                    f32.const 0x1p+0 (;=1;)
                    local.set $l27
                    f32.const 0x1p+0 (;=1;)
                    local.set $l31
                    local.get $l29
                    f32.neg
                    local.set $l34
                    f32.const 0x0p+0 (;=0;)
                    local.set $l29
                    local.get $l6
                    if $I61
                      local.get $l6
                      i32.load offset=32
                      f32.load offset=36
                      local.set $l27
                    end
                    local.get $l4
                    if $I62
                      local.get $l4
                      i32.load offset=32
                      f32.load offset=36
                      local.set $l28
                    end
                    local.get $l27
                    local.get $l28
                    local.get $l27
                    local.get $l28
                    f32.lt
                    select
                    f32.const 0x1p+0 (;=1;)
                    f32.ne
                    if $I63
                      f32.const 0x0p+0 (;=0;)
                      local.set $l28
                      br $B59
                    end
                    local.get $l6
                    if $I64
                      local.get $l6
                      i32.load offset=36
                      f32.load offset=60
                      local.set $l31
                    end
                    block $B65 (result f32)
                      local.get $l4
                      i32.eqz
                      if $I66
                        f32.const 0x1.fffffep+127 (;=3.40282e+38;)
                        local.set $l36
                        f32.const 0x1p+0 (;=1;)
                        br $B65
                      end
                      local.get $l4
                      i32.load offset=36
                      f32.load offset=60
                    end
                    local.set $l28
                    local.get $l37
                    local.get $l36
                    local.get $l36
                    local.get $l37
                    f32.gt
                    select
                    local.get $l31
                    local.get $l28
                    local.get $l28
                    local.get $l31
                    f32.gt
                    select
                    f32.mul
                    local.get $l33
                    f32.div
                    local.set $l28
                  end
                  local.get $l2
                  local.get $l34
                  f32.store offset=48
                  local.get $l2
                  local.get $l29
                  f32.store offset=28
                  local.get $l2
                  local.get $l28
                  f32.store offset=32
                  local.get $l2
                  local.get $l5
                  f32.load offset=32
                  f32.store offset=36
                  local.get $l2
                  local.get $l5
                  f32.load offset=36
                  f32.store offset=40
                  local.get $l5
                  f32.load offset=40
                  local.set $l28
                  local.get $l2
                  local.get $l32
                  f32.store offset=24
                  local.get $l2
                  local.get $l26
                  f32.store offset=20
                  local.get $l2
                  local.get $l30
                  f32.store offset=16
                  local.get $l2
                  local.get $l28
                  f32.store offset=44
                  local.get $l10
                  i32.const 4624
                  i32.add
                  i32.const 0
                  i32.store
                  i32.const -1
                  local.set $l6
                  local.get $l7
                  i32.const 5
                  i32.sub
                  i32.const 1
                  i32.le_u
                  if $I67
                    local.get $l2
                    i32.load offset=72
                    local.set $l6
                  end
                  local.get $l10
                  i32.const 1
                  i32.store offset=4624
                  local.get $l10
                  local.get $l2
                  f32.load offset=16
                  f32.store offset=528
                  local.get $l10
                  local.get $l2
                  f32.load offset=20
                  f32.store offset=532
                  local.get $l10
                  local.get $l2
                  f32.load offset=24
                  f32.store offset=536
                  local.get $l10
                  local.get $l2
                  f32.load offset=36
                  f32.store offset=544
                  local.get $l10
                  local.get $l2
                  f32.load offset=40
                  f32.store offset=548
                  local.get $l2
                  f32.load offset=44
                  local.set $l28
                  local.get $l10
                  local.get $l6
                  i32.store offset=580
                  local.get $l10
                  i32.const 0
                  i32.store offset=540
                  local.get $l10
                  local.get $l28
                  f32.store offset=552
                  local.get $l3
                  i32.load offset=92
                  i32.const 0
                  local.get $l10
                  local.get $l5
                  i32.const 24
                  i32.add
                  local.get $l9
                  i32.const 2
                  i32.shl
                  i32.const 4118176
                  i32.add
                  i32.load
                  call_indirect $__indirect_function_table (type $t8)
                  drop
                  local.get $l1
                  i32.load offset=92
                  i32.const 1
                  local.get $l10
                  local.get $l5
                  i32.const 24
                  i32.add
                  local.get $l7
                  i32.const 2
                  i32.shl
                  i32.const 4118176
                  i32.add
                  i32.load
                  call_indirect $__indirect_function_table (type $t8)
                  drop
                  local.get $l10
                  i32.load offset=7188
                  i32.load
                  local.tee $l1
                  local.get $l5
                  i32.load16_u offset=26
                  i32.const 5
                  i32.shl
                  i32.add
                  local.tee $l3
                  f32.load offset=8
                  local.set $l26
                  local.get $l1
                  local.get $l5
                  i32.load16_u offset=24
                  i32.const 5
                  i32.shl
                  i32.add
                  local.tee $l1
                  f32.load offset=8
                  local.set $l30
                  f32.const 0x0p+0 (;=0;)
                  local.set $l28
                  block $B68
                    block $B69
                      block $B70
                        block $B71
                          block $B72
                            local.get $l3
                            i32.load8_u offset=14
                            i32.const 15
                            i32.and
                            local.tee $l10
                            local.get $l1
                            i32.load8_u offset=14
                            i32.const 15
                            i32.and
                            local.tee $l6
                            local.get $l6
                            local.get $l10
                            i32.lt_u
                            select
                            br_table $B72 $B71 $B70 $B69 $B68
                          end
                          local.get $l30
                          local.get $l26
                          f32.add
                          f32.const 0x1p-1 (;=0.5;)
                          f32.mul
                          local.set $l28
                          br $B68
                        end
                        local.get $l30
                        local.get $l26
                        local.get $l26
                        local.get $l30
                        f32.gt
                        select
                        local.set $l28
                        br $B68
                      end
                      local.get $l30
                      local.get $l26
                      f32.mul
                      local.set $l28
                      br $B68
                    end
                    local.get $l30
                    local.get $l26
                    local.get $l26
                    local.get $l30
                    f32.lt
                    select
                    local.set $l28
                  end
                  local.get $l5
                  i64.const 4575657222473777152
                  i64.store offset=16
                  local.get $l5
                  local.get $l5
                  i32.const 16
                  i32.add
                  local.get $l1
                  local.get $l3
                  call $f70617
                  local.get $l5
                  i64.load
                  local.set $l45
                  local.get $l2
                  local.get $l5
                  i32.load16_u offset=24
                  i32.store16 offset=76
                  local.get $l5
                  i32.load16_u offset=26
                  local.set $l3
                  local.get $l2
                  local.get $l28
                  f32.store offset=88
                  local.get $l2
                  local.get $l45
                  i64.const 32
                  i64.rotl
                  i64.store offset=80 align=4
                  local.get $l2
                  local.get $l3
                  i32.store16 offset=78
                end
                local.get $l5
                i32.const 192
                i32.add
                global.set $g0
                local.get $l12
                local.get $l13
                i32.const 1
                i32.add
                local.tee $l3
                i32.le_u
                if $I73
                  local.get $l2
                  f32.load offset=28
                  local.set $l26
                  br $B51
                end
                local.get $l2
                f32.load offset=28
                local.tee $l26
                local.get $p0
                i32.load offset=28
                local.tee $l1
                local.get $l3
                i32.const 2
                i32.shl
                i32.add
                i32.load
                local.tee $l4
                f32.load offset=28
                f32.gt
                local.tee $l11
                i32.eqz
                br_if $B51
                local.get $l13
                local.tee $l7
                local.set $l6
                block $B74
                  local.get $l11
                  i32.eqz
                  br_if $B74
                  loop $L75
                    local.get $l1
                    local.get $l7
                    i32.const 2
                    i32.shl
                    i32.add
                    local.get $l4
                    i32.store
                    local.get $p0
                    i32.load offset=28
                    local.set $l1
                    local.get $l3
                    local.tee $l6
                    i32.const 1
                    i32.add
                    local.tee $l3
                    local.get $l12
                    i32.eq
                    br_if $B74
                    local.get $l6
                    local.set $l7
                    local.get $l1
                    local.get $l3
                    i32.const 2
                    i32.shl
                    i32.add
                    i32.load
                    local.tee $l4
                    f32.load offset=28
                    local.get $l2
                    f32.load offset=28
                    f32.lt
                    br_if $L75
                  end
                end
                local.get $l1
                local.get $l6
                i32.const 2
                i32.shl
                i32.add
                local.get $l2
                i32.store
                local.get $l13
                i32.const 1
                i32.sub
                local.set $l13
                br $B49
              end
              local.get $l26
              f32.const 0x1p+0 (;=1;)
              f32.gt
              br_if $B3
              block $B76
                local.get $l26
                f32.const 0x1.fffffep+127 (;=3.40282e+38;)
                f32.le
                i32.eqz
                br_if $B76
                local.get $l2
                i32.load8_u offset=69
                i32.eqz
                br_if $B76
                local.get $p0
                i32.load offset=40
                local.tee $l3
                i32.load offset=120
                i32.eqz
                br_if $B76
                local.get $l8
                i64.const 4575657222473777152
                i64.store
                local.get $l8
                i64.const 4575657222473777152
                i64.store offset=8
                local.get $l8
                local.get $l2
                f32.load offset=16
                f32.store offset=16
                local.get $l8
                local.get $l2
                i32.const 20
                i32.add
                local.tee $l1
                f32.load
                f32.store offset=20
                local.get $l8
                local.get $l2
                i32.const 24
                i32.add
                local.tee $l4
                f32.load
                f32.store offset=24
                local.get $l8
                local.get $l2
                f32.load offset=80
                f32.store offset=32
                local.get $l8
                local.get $l2
                f32.load offset=84
                f32.store offset=36
                local.get $l8
                local.get $l2
                i32.load16_u offset=76
                i32.store16 offset=44
                local.get $l2
                i32.load16_u offset=78
                local.set $l6
                local.get $l8
                i32.const 0
                i32.store8 offset=42
                local.get $l8
                i32.const 256
                i32.store16 offset=40
                local.get $l8
                local.get $l6
                i32.store16 offset=46
                local.get $l8
                local.get $l2
                i32.load offset=12
                i32.load
                i32.load
                i32.const 5
                i32.eq
                i32.store8 offset=43
                local.get $l8
                local.get $l2
                f32.load offset=36
                f32.store offset=48
                local.get $l8
                local.get $l2
                f32.load offset=40
                f32.store offset=52
                local.get $l8
                local.get $l2
                f32.load offset=44
                f32.store offset=56
                local.get $l8
                local.get $l2
                f32.load offset=16
                f32.store offset=80
                local.get $l8
                local.get $l1
                f32.load
                f32.store offset=84
                local.get $l8
                local.get $l4
                f32.load
                f32.store offset=88
                local.get $l8
                local.get $l2
                i32.load offset=72
                i32.store offset=116
                local.get $l8
                local.get $l2
                i32.load16_u offset=76
                i32.store16 offset=100
                local.get $l8
                local.get $l2
                i32.load16_u offset=78
                i32.store16 offset=102
                local.get $l8
                local.get $l2
                f32.load offset=80
                f32.store offset=108
                local.get $l8
                local.get $l2
                f32.load offset=84
                f32.store offset=104
                local.get $l2
                f32.load offset=88
                local.set $l26
                local.get $l8
                i32.const 0
                i32.store offset=96
                local.get $l8
                i32.const 0
                i32.store offset=60
                local.get $l8
                local.get $l26
                f32.store offset=92
                local.get $l8
                i64.const 9187343235540844544
                i64.store offset=72
                local.get $l8
                i64.const 0
                i64.store offset=64
                local.get $l2
                i32.load offset=8
                local.tee $l1
                i32.load offset=92
                local.set $l6
                local.get $l2
                i32.load offset=12
                local.tee $l4
                i32.load offset=92
                local.set $l7
                local.get $l1
                i32.load offset=96
                local.set $l11
                local.get $l4
                i32.load offset=96
                local.set $l9
                local.get $l2
                i32.load
                local.set $l15
                local.get $l2
                i32.load offset=4
                local.set $l10
                global.get $g0
                i32.const 112
                i32.sub
                local.tee $l1
                global.set $g0
                local.get $l3
                i32.load offset=120
                if $I77
                  local.get $l1
                  local.get $l7
                  i32.const 4701952
                  i32.load
                  local.tee $l4
                  i32.add
                  i32.store offset=44
                  local.get $l1
                  local.get $l4
                  local.get $l6
                  i32.add
                  i32.store offset=40
                  local.get $l1
                  local.get $l9
                  i32.const 4701956
                  i32.load
                  local.tee $l4
                  i32.const 4701960
                  i32.load
                  local.tee $l5
                  local.get $l10
                  select
                  i32.add
                  i32.store offset=36
                  local.get $l1
                  local.get $l11
                  local.get $l4
                  local.get $l5
                  local.get $l15
                  select
                  i32.add
                  i32.store offset=32
                  local.get $l1
                  local.get $l6
                  local.get $l11
                  local.get $l15
                  i32.const 0
                  i32.ne
                  call $f70635
                  local.get $l1
                  local.get $l1
                  i64.load offset=4 align=4
                  i64.store offset=52 align=4
                  local.get $l1
                  local.get $l1
                  i64.load offset=12 align=4
                  i64.store offset=60 align=4
                  local.get $l1
                  local.get $l1
                  i32.const 20
                  i32.add
                  local.tee $l6
                  i64.load align=4
                  i64.store offset=68 align=4
                  local.get $l1
                  local.get $l1
                  f32.load
                  f32.store offset=48
                  local.get $l1
                  local.get $l7
                  local.get $l9
                  local.get $l10
                  i32.const 0
                  i32.ne
                  call $f70635
                  local.get $l1
                  local.get $l1
                  f32.load
                  f32.store offset=76
                  local.get $l1
                  local.get $l1
                  i64.load offset=4 align=4
                  i64.store offset=80
                  local.get $l1
                  local.get $l1
                  i64.load offset=12 align=4
                  i64.store offset=88
                  local.get $l1
                  local.get $l6
                  i64.load align=4
                  i64.store offset=96
                  local.get $l1
                  local.get $l24
                  i32.store offset=108
                  local.get $l1
                  i32.const 1
                  i32.store offset=104
                  local.get $l3
                  i32.load offset=120
                  local.tee $l3
                  local.get $l1
                  i32.const 32
                  i32.add
                  i32.const 1
                  local.get $l3
                  i32.load
                  i32.load
                  call_indirect $__indirect_function_table (type $t2)
                end
                local.get $l1
                i32.const 112
                i32.add
                global.set $g0
                local.get $l8
                i32.load8_u offset=43
                i32.const 32
                i32.and
                if $I78
                  local.get $l2
                  local.get $l8
                  f32.load offset=76
                  f32.store offset=100
                end
                local.get $l2
                local.get $l8
                f32.load offset=108
                f32.store offset=80
                local.get $l2
                local.get $l8
                f32.load offset=104
                f32.store offset=84
                local.get $l2
                local.get $l8
                f32.load offset=92
                f32.store offset=88
                local.get $l2
                local.get $l8
                f32.load offset=48
                f32.store offset=36
                local.get $l2
                local.get $l8
                f32.load offset=52
                f32.store offset=40
                local.get $l2
                local.get $l8
                f32.load offset=56
                f32.store offset=44
                local.get $l2
                local.get $l8
                f32.load offset=80
                f32.store offset=16
                local.get $l2
                local.get $l8
                f32.load offset=84
                f32.store offset=20
                local.get $l2
                local.get $l8
                f32.load offset=88
                f32.store offset=24
              end
              block $B79 (result i32)
                block $B80
                  local.get $l2
                  i32.load
                  local.tee $l3
                  i32.eqz
                  br_if $B80
                  local.get $l3
                  i32.load offset=32
                  i32.load8_u offset=34
                  br_if $B80
                  i32.const 1
                  br $B79
                end
                local.get $l3
                i32.eqz
              end
              local.set $l1
              block $B81 (result i32)
                block $B82
                  local.get $l2
                  i32.load offset=4
                  local.tee $l3
                  i32.eqz
                  br_if $B82
                  local.get $l3
                  i32.load offset=32
                  i32.load8_u offset=34
                  br_if $B82
                  i32.const 0
                  br $B81
                end
                local.get $l3
                i32.const 0
                i32.ne
              end
              local.set $l3
              block $B83
                local.get $l2
                f32.load offset=28
                f32.const 0x1p+0 (;=1;)
                f32.le
                i32.eqz
                br_if $B83
                local.get $l1
                i32.const 1
                i32.xor
                br_if $B83
                local.get $l3
                br_if $B83
                local.get $l2
                i32.const 1
                i32.store8 offset=68
              end
              local.get $p0
              i32.load8_u offset=84
              local.set $l10
              f32.const 0x0p+0 (;=0;)
              local.set $l29
              f32.const 0x0p+0 (;=0;)
              local.set $l28
              f32.const 0x0p+0 (;=0;)
              local.set $l30
              f32.const 0x0p+0 (;=0;)
              local.set $l31
              f32.const 0x0p+0 (;=0;)
              local.set $l34
              i32.const 0
              local.set $l15
              i32.const 0
              local.set $l5
              global.get $g0
              i32.const 16
              i32.sub
              local.tee $l6
              global.set $g0
              local.get $l2
              local.tee $l1
              i32.load offset=4
              local.set $l7
              local.get $l2
              i32.load offset=12
              local.set $l11
              local.get $l2
              i32.load offset=8
              local.set $l9
              block $B84
                block $B85
                  block $B86
                    block $B87
                      local.get $l2
                      i32.load
                      local.tee $l4
                      if $I88
                        local.get $l4
                        i32.load offset=32
                        i32.load8_u offset=34
                        i32.eqz
                        br_if $B87
                      end
                      local.get $l7
                      i32.eqz
                      br_if $B84
                      local.get $l7
                      i32.load offset=32
                      i32.load8_u offset=34
                      br_if $B84
                      local.get $l4
                      i32.eqz
                      br_if $B86
                    end
                    local.get $l4
                    i32.load offset=36
                    f32.load offset=124
                    f32.const 0x0p+0 (;=0;)
                    f32.ne
                    br_if $B85
                    local.get $l7
                    br_if $B86
                    br $B84
                  end
                  local.get $l7
                  i32.load offset=36
                  f32.load offset=124
                  f32.const 0x0p+0 (;=0;)
                  f32.eq
                  br_if $B84
                end
                local.get $l1
                f32.load offset=28
                local.tee $l33
                f32.const 0x1p+0 (;=1;)
                f32.lt
                i32.eqz
                br_if $B84
                i32.const 1
                local.set $l5
                local.get $l1
                i32.load offset=52
                i32.load8_u offset=41
                i32.const 8
                i32.and
                br_if $B84
                local.get $l1
                f32.load offset=100
                f32.const 0x0p+0 (;=0;)
                f32.eq
                br_if $B84
                local.get $l1
                f32.load offset=48
                local.set $l26
                local.get $l6
                local.get $l1
                f32.load offset=16
                f32.store
                local.get $l6
                local.get $l1
                f32.load offset=20
                f32.store offset=4
                local.get $l6
                local.get $l1
                f32.load offset=24
                f32.store offset=8
                block $B89
                  local.get $l6
                  local.tee $l3
                  i32.load
                  local.tee $l18
                  i32.const 2139095040
                  i32.and
                  i32.const 2139095040
                  i32.eq
                  br_if $B89
                  local.get $l3
                  i32.load offset=4
                  local.tee $l20
                  i32.const 2139095040
                  i32.and
                  i32.const 2139095040
                  i32.eq
                  br_if $B89
                  local.get $l3
                  i32.load offset=8
                  local.tee $l3
                  i32.const 2139095040
                  i32.and
                  i32.const 2139095040
                  i32.eq
                  br_if $B89
                  local.get $l18
                  f32.reinterpret_i32
                  local.tee $l27
                  local.get $l27
                  f32.mul
                  local.get $l20
                  f32.reinterpret_i32
                  local.tee $l27
                  local.get $l27
                  f32.mul
                  f32.add
                  local.get $l3
                  f32.reinterpret_i32
                  local.tee $l27
                  local.get $l27
                  f32.mul
                  f32.add
                  f32.sqrt
                  f32.const -0x1p+0 (;=-1;)
                  f32.add
                  f32.abs
                  f32.const 0x1.a36e2ep-14 (;=0.0001;)
                  f32.lt
                  local.set $l15
                end
                local.get $l15
                i32.eqz
                if $I90
                  local.get $l4
                  i32.eqz
                  br_if $B84
                  local.get $l4
                  i32.load offset=32
                  i32.load8_u offset=34
                  br_if $B84
                  local.get $l4
                  local.get $l33
                  call $f70621
                  local.get $l4
                  local.get $l33
                  local.get $l35
                  i32.const 1
                  call $f70622
                  local.get $l4
                  i32.load offset=32
                  local.tee $l1
                  local.get $l1
                  i32.load offset=48
                  i32.const 1
                  i32.add
                  i32.store offset=48
                  br $B84
                end
                local.get $l1
                i32.load offset=52
                local.set $l15
                local.get $l4
                if $I91
                  local.get $l9
                  f32.load offset=56
                  local.get $l4
                  i32.load offset=36
                  local.tee $l3
                  f32.load offset=20
                  f32.sub
                  local.tee $l28
                  local.get $l3
                  f32.load offset=80
                  local.tee $l30
                  f32.mul
                  local.get $l9
                  f32.load offset=52
                  local.get $l3
                  f32.load offset=16
                  f32.sub
                  local.tee $l27
                  local.get $l3
                  f32.load offset=84
                  local.tee $l34
                  f32.mul
                  f32.sub
                  local.get $l3
                  f32.load offset=72
                  f32.add
                  local.set $l31
                  local.get $l3
                  f32.load offset=68
                  local.get $l27
                  local.get $l3
                  f32.load offset=88
                  local.tee $l32
                  f32.mul
                  local.get $l9
                  f32.load offset=60
                  local.get $l3
                  f32.load offset=24
                  f32.sub
                  local.tee $l27
                  local.get $l30
                  f32.mul
                  f32.sub
                  f32.add
                  local.set $l30
                  local.get $l3
                  f32.load offset=64
                  local.get $l34
                  local.get $l27
                  f32.mul
                  local.get $l28
                  local.get $l32
                  f32.mul
                  f32.sub
                  f32.add
                  local.set $l28
                  local.get $l3
                  f32.load offset=124
                  local.get $l15
                  i32.load8_u offset=44
                  f32.convert_i32_u
                  f32.mul
                  local.set $l34
                end
                local.get $l26
                f32.const 0x1.4p+3 (;=10;)
                f32.mul
                local.set $l36
                f32.const 0x0p+0 (;=0;)
                local.set $l26
                f32.const 0x0p+0 (;=0;)
                local.set $l27
                f32.const 0x0p+0 (;=0;)
                local.set $l32
                local.get $l7
                if $I92
                  local.get $l11
                  f32.load offset=56
                  local.get $l7
                  i32.load offset=36
                  local.tee $l9
                  f32.load offset=20
                  f32.sub
                  local.tee $l29
                  local.get $l9
                  f32.load offset=80
                  local.tee $l26
                  f32.mul
                  local.get $l11
                  f32.load offset=52
                  local.get $l9
                  f32.load offset=16
                  f32.sub
                  local.tee $l32
                  local.get $l9
                  f32.load offset=84
                  local.tee $l37
                  f32.mul
                  f32.sub
                  local.get $l9
                  f32.load offset=72
                  f32.add
                  local.set $l27
                  local.get $l9
                  f32.load offset=68
                  local.get $l32
                  local.get $l9
                  f32.load offset=88
                  local.tee $l38
                  f32.mul
                  local.get $l11
                  f32.load offset=60
                  local.get $l9
                  f32.load offset=24
                  f32.sub
                  local.tee $l32
                  local.get $l26
                  f32.mul
                  f32.sub
                  f32.add
                  local.set $l26
                  local.get $l9
                  f32.load offset=64
                  local.get $l37
                  local.get $l32
                  f32.mul
                  local.get $l29
                  local.get $l38
                  f32.mul
                  f32.sub
                  f32.add
                  local.set $l29
                  local.get $l9
                  f32.load offset=124
                  local.get $l15
                  i32.load8_u offset=45
                  f32.convert_i32_u
                  f32.mul
                  local.set $l32
                end
                block $B93
                  local.get $l29
                  local.get $l28
                  f32.sub
                  local.tee $l28
                  local.get $l6
                  f32.load
                  local.tee $l37
                  f32.mul
                  local.get $l26
                  local.get $l30
                  f32.sub
                  local.tee $l30
                  local.get $l6
                  f32.load offset=4
                  local.tee $l38
                  f32.mul
                  f32.add
                  local.get $l27
                  local.get $l31
                  f32.sub
                  local.tee $l31
                  local.get $l6
                  f32.load offset=8
                  local.tee $l27
                  f32.mul
                  f32.add
                  local.tee $l29
                  local.get $l36
                  f32.sub
                  local.tee $l26
                  f32.const -0x1.0c6f7ap-20 (;=-1e-06;)
                  f32.lt
                  i32.eqz
                  br_if $B93
                  local.get $l1
                  f32.load offset=100
                  f32.neg
                  local.tee $l36
                  local.get $l1
                  f32.load offset=88
                  f32.const 0x1p+0 (;=1;)
                  f32.add
                  local.get $l26
                  f32.mul
                  local.get $l34
                  local.get $l32
                  f32.add
                  local.tee $l39
                  f32.div
                  local.tee $l26
                  local.get $l26
                  local.get $l36
                  f32.lt
                  select
                  local.set $l26
                  block $B94 (result f32)
                    local.get $l1
                    i32.load8_u offset=108
                    if $I95
                      local.get $l1
                      f32.load offset=80
                      local.set $l36
                      local.get $l1
                      f32.load offset=84
                      local.set $l40
                      local.get $l31
                      local.get $l27
                      local.get $l29
                      f32.mul
                      f32.sub
                      local.tee $l31
                      local.get $l31
                      f32.mul
                      local.get $l28
                      local.get $l37
                      local.get $l29
                      f32.mul
                      f32.sub
                      local.tee $l28
                      local.get $l28
                      f32.mul
                      local.get $l30
                      local.get $l38
                      local.get $l29
                      f32.mul
                      f32.sub
                      local.tee $l29
                      local.get $l29
                      f32.mul
                      f32.add
                      f32.add
                      f32.sqrt
                      local.tee $l30
                      f32.const 0x0p+0 (;=0;)
                      f32.gt
                      if $I96
                        local.get $l31
                        f32.const 0x1p+0 (;=1;)
                        local.get $l30
                        f32.div
                        local.tee $l27
                        f32.mul
                        local.set $l31
                        local.get $l28
                        local.get $l27
                        f32.mul
                        local.set $l28
                        local.get $l29
                        local.get $l27
                        f32.mul
                        local.set $l29
                      end
                      local.get $l30
                      local.get $l39
                      f32.div
                      local.tee $l30
                      local.get $l36
                      local.get $l26
                      f32.neg
                      f32.mul
                      local.get $l40
                      local.get $l26
                      f32.mul
                      f32.abs
                      local.get $l30
                      f32.ge
                      select
                      local.tee $l30
                      local.get $l31
                      f32.mul
                      local.get $l26
                      local.get $l1
                      f32.load offset=24
                      f32.mul
                      f32.add
                      local.set $l31
                      local.get $l30
                      local.get $l28
                      f32.mul
                      local.get $l26
                      local.get $l1
                      f32.load offset=16
                      f32.mul
                      f32.add
                      local.set $l28
                      local.get $l30
                      local.get $l29
                      f32.mul
                      local.get $l26
                      local.get $l1
                      f32.load offset=20
                      f32.mul
                      f32.add
                      br $B94
                    end
                    local.get $l26
                    local.get $l1
                    f32.load offset=24
                    f32.mul
                    local.set $l31
                    local.get $l26
                    local.get $l1
                    f32.load offset=16
                    f32.mul
                    local.set $l28
                    local.get $l26
                    local.get $l1
                    f32.load offset=20
                    f32.mul
                  end
                  local.set $l29
                  local.get $l26
                  f32.const 0x0p+0 (;=0;)
                  f32.lt
                  i32.eqz
                  br_if $B93
                  local.get $l1
                  local.get $l26
                  f32.neg
                  f32.store offset=96
                  block $B97
                    block $B98
                      local.get $l4
                      if $I99
                        local.get $l4
                        i32.load offset=32
                        i32.load8_u offset=34
                        br_if $B98
                      end
                      local.get $l7
                      i32.eqz
                      br_if $B97
                      local.get $l7
                      i32.load offset=32
                      i32.load8_u offset=34
                      i32.eqz
                      br_if $B97
                    end
                    local.get $l1
                    i32.const 0
                    i32.store offset=32
                    br $B93
                  end
                  local.get $l4
                  if $I100
                    local.get $l4
                    i32.load offset=36
                    local.tee $l11
                    local.get $l34
                    local.get $l28
                    f32.mul
                    local.get $l11
                    f32.load offset=64
                    f32.add
                    f32.store offset=64
                    local.get $l11
                    i32.const 72
                    i32.add
                    local.tee $l9
                    local.get $l34
                    local.get $l31
                    f32.mul
                    local.get $l9
                    f32.load
                    f32.add
                    f32.store
                    local.get $l11
                    i32.const 68
                    i32.add
                    local.tee $l11
                    local.get $l34
                    local.get $l29
                    f32.mul
                    local.get $l11
                    f32.load
                    f32.add
                    f32.store
                    local.get $l4
                    call $f70623
                  end
                  local.get $l7
                  i32.eqz
                  br_if $B93
                  local.get $l7
                  i32.load offset=36
                  local.tee $l11
                  local.get $l11
                  f32.load offset=64
                  local.get $l32
                  local.get $l28
                  f32.mul
                  f32.sub
                  f32.store offset=64
                  local.get $l11
                  i32.const 72
                  i32.add
                  local.tee $l9
                  local.get $l9
                  f32.load
                  local.get $l32
                  local.get $l31
                  f32.mul
                  f32.sub
                  f32.store
                  local.get $l11
                  i32.const 68
                  i32.add
                  local.tee $l11
                  local.get $l11
                  f32.load
                  local.get $l32
                  local.get $l29
                  f32.mul
                  f32.sub
                  f32.store
                  local.get $l7
                  call $f70623
                end
                block $B101
                  local.get $l4
                  i32.eqz
                  br_if $B101
                  local.get $l4
                  i32.load offset=32
                  i32.load8_u offset=34
                  br_if $B101
                  local.get $l4
                  local.get $l33
                  call $f70621
                  local.get $l4
                  local.get $l33
                  local.get $l35
                  local.get $l10
                  if $I102 (result i32)
                    local.get $l1
                    f32.load offset=32
                    f32.const 0x0p+0 (;=0;)
                    f32.eq
                  else
                    i32.const 0
                  end
                  call $f70622
                  local.get $l4
                  i32.load offset=32
                  local.tee $l11
                  local.get $l11
                  i32.load offset=48
                  i32.const 1
                  i32.add
                  i32.store offset=48
                end
                block $B103
                  local.get $l7
                  i32.eqz
                  br_if $B103
                  local.get $l7
                  i32.load offset=32
                  i32.load8_u offset=34
                  br_if $B103
                  local.get $l7
                  local.get $l33
                  call $f70621
                  local.get $l7
                  local.get $l33
                  local.get $l35
                  local.get $l10
                  if $I104 (result i32)
                    local.get $l1
                    f32.load offset=32
                    f32.const 0x0p+0 (;=0;)
                    f32.eq
                  else
                    i32.const 0
                  end
                  call $f70622
                  local.get $l7
                  i32.load offset=32
                  local.tee $l11
                  local.get $l11
                  i32.load offset=48
                  i32.const 1
                  i32.add
                  i32.store offset=48
                end
                block $B105
                  local.get $l1
                  f32.load offset=32
                  local.tee $l33
                  f32.const 0x0p+0 (;=0;)
                  f32.gt
                  i32.eqz
                  br_if $B105
                  block $B106
                    local.get $l4
                    i32.eqz
                    br_if $B106
                    local.get $l4
                    i32.load offset=32
                    i32.load8_u offset=34
                    br_if $B106
                    local.get $l4
                    local.get $l33
                    call $f70621
                    local.get $l10
                    i32.eqz
                    br_if $B106
                    local.get $l4
                    local.get $l1
                    f32.load offset=32
                    local.get $l35
                    i32.const 1
                    call $f70622
                  end
                  local.get $l7
                  i32.eqz
                  br_if $B105
                  local.get $l7
                  i32.load offset=32
                  i32.load8_u offset=34
                  br_if $B105
                  local.get $l7
                  local.get $l1
                  f32.load offset=32
                  call $f70621
                  local.get $l10
                  i32.eqz
                  br_if $B105
                  local.get $l7
                  local.get $l1
                  f32.load offset=32
                  local.get $l35
                  i32.const 1
                  call $f70622
                end
                local.get $l4
                if $I107
                  local.get $l4
                  i32.load offset=32
                  i32.const 1
                  i32.store8 offset=34
                  local.get $l4
                  i32.load offset=32
                  i32.const 1
                  i32.store8 offset=35
                end
                local.get $l7
                i32.eqz
                br_if $B84
                local.get $l7
                i32.load offset=32
                i32.const 1
                i32.store8 offset=34
                local.get $l7
                i32.load offset=32
                i32.const 1
                i32.store8 offset=35
              end
              local.get $l6
              i32.const 16
              i32.add
              global.set $g0
              local.get $l5
              local.set $l3
              block $B108
                local.get $l2
                f32.load offset=28
                local.tee $l26
                f32.const 0x0p+0 (;=0;)
                f32.lt
                i32.eqz
                if $I109
                  local.get $l3
                  i32.eqz
                  br_if $B49
                  local.get $l26
                  f32.const 0x1p+0 (;=1;)
                  f32.le
                  br_if $B108
                  br $B49
                end
                local.get $l2
                i32.const 0
                i32.store offset=28
                f32.const 0x0p+0 (;=0;)
                local.set $l26
                local.get $l3
                i32.eqz
                br_if $B49
              end
              local.get $p0
              i32.load offset=76
              local.set $l1
              local.get $l17
              if $I110 (result i32)
                local.get $l1
                local.get $l19
                i32.const 1
                i32.shl
                i32.add
                i32.load16_u
              else
                i32.const 0
              end
              local.set $l3
              block $B111
                local.get $l26
                f32.const 0x0p+0 (;=0;)
                f32.gt
                i32.eqz
                br_if $B111
                local.get $l35
                local.get $l35
                block $B112 (result f32)
                  local.get $l1
                  local.get $l17
                  i32.const 1
                  i32.shl
                  i32.add
                  i32.load16_u
                  local.tee $l4
                  local.get $l3
                  i32.gt_u
                  if $I113
                    loop $L114
                      local.get $p0
                      i32.load offset=72
                      local.get $l3
                      i32.const 2
                      i32.shl
                      i32.add
                      i32.load
                      local.tee $l1
                      i32.load8_u offset=34
                      i32.eqz
                      if $I115
                        local.get $l2
                        f32.load offset=28
                        local.set $l26
                        local.get $l1
                        i32.load offset=40
                        local.tee $l1
                        i32.load offset=36
                        local.tee $l6
                        f32.load offset=124
                        f32.const 0x0p+0 (;=0;)
                        f32.ne
                        if $I116
                          local.get $l6
                          f32.load offset=20
                          local.set $l29
                          local.get $l6
                          f32.load offset=24
                          local.set $l35
                          local.get $l1
                          f32.const 0x1p+0 (;=1;)
                          local.get $l26
                          f32.sub
                          local.tee $l27
                          local.get $l1
                          f32.load offset=16
                          f32.mul
                          local.get $l26
                          local.get $l6
                          f32.load offset=16
                          f32.mul
                          f32.add
                          f32.store offset=16
                          local.get $l1
                          i32.const 24
                          i32.add
                          local.tee $l7
                          local.get $l27
                          local.get $l7
                          f32.load
                          f32.mul
                          local.get $l26
                          local.get $l35
                          f32.mul
                          f32.add
                          f32.store
                          local.get $l1
                          i32.const 20
                          i32.add
                          local.tee $l7
                          local.get $l27
                          local.get $l7
                          f32.load
                          f32.mul
                          local.get $l26
                          local.get $l29
                          f32.mul
                          f32.add
                          f32.store
                          local.get $l8
                          local.get $l26
                          local.get $l1
                          local.get $l6
                          call $f69770
                          local.get $l1
                          local.get $l8
                          f32.load
                          f32.store
                          local.get $l1
                          local.get $l8
                          f32.load offset=4
                          f32.store offset=4
                          local.get $l1
                          local.get $l8
                          f32.load offset=8
                          f32.store offset=8
                          local.get $l1
                          local.get $l8
                          f32.load offset=12
                          f32.store offset=12
                          local.get $l2
                          f32.load offset=28
                          local.set $l26
                        end
                        local.get $l1
                        i32.load offset=32
                        local.tee $l6
                        local.get $l6
                        f32.load offset=36
                        f32.const 0x1p+0 (;=1;)
                        local.get $l26
                        f32.sub
                        f32.mul
                        local.tee $l26
                        f32.const 0x1.47ae14p-7 (;=0.01;)
                        local.get $l26
                        f32.const 0x1.47ae14p-7 (;=0.01;)
                        f32.gt
                        select
                        f32.store offset=36
                        local.get $l1
                        i32.load offset=32
                        local.tee $l1
                        local.get $l1
                        i32.load offset=48
                        i32.const 1
                        i32.add
                        i32.store offset=48
                      end
                      local.get $l3
                      i32.const 1
                      i32.add
                      local.tee $l3
                      local.get $l4
                      i32.ne
                      br_if $L114
                    end
                    local.get $l2
                    f32.load offset=28
                    local.set $l26
                  end
                  local.get $l26
                end
                f32.mul
                f32.sub
                local.set $l35
                local.get $l13
                i32.const 1
                i32.add
                local.tee $l3
                local.get $l12
                i32.ge_u
                br_if $B111
                local.get $p0
                i32.load offset=28
                local.get $l3
                i32.const 2
                i32.shl
                i32.add
                i32.load
                local.tee $l3
                f32.const 0x1p+0 (;=1;)
                f32.const 0x1p+0 (;=1;)
                local.get $l26
                f32.sub
                f32.div
                local.tee $l27
                local.get $l3
                f32.load offset=28
                local.get $l26
                f32.sub
                f32.mul
                f32.store offset=28
                local.get $l13
                i32.const 2
                i32.add
                local.tee $l3
                local.get $l12
                i32.eq
                br_if $B111
                local.get $l12
                local.get $l13
                i32.sub
                i32.const 1
                i32.and
                if $I117
                  local.get $p0
                  i32.load offset=28
                  local.get $l3
                  i32.const 2
                  i32.shl
                  i32.add
                  i32.load
                  local.tee $l3
                  local.get $l27
                  local.get $l3
                  f32.load offset=28
                  local.get $l2
                  f32.load offset=28
                  f32.sub
                  f32.mul
                  f32.store offset=28
                  local.get $l13
                  i32.const 3
                  i32.add
                  local.set $l3
                end
                local.get $l13
                local.get $l16
                i32.eq
                br_if $B111
                loop $L118
                  local.get $l3
                  i32.const 2
                  i32.shl
                  local.tee $l1
                  local.get $p0
                  i32.load offset=28
                  i32.add
                  i32.load
                  local.tee $l4
                  local.get $l27
                  local.get $l4
                  f32.load offset=28
                  local.get $l2
                  f32.load offset=28
                  f32.sub
                  f32.mul
                  f32.store offset=28
                  local.get $l1
                  local.get $p0
                  i32.load offset=28
                  i32.add
                  i32.load offset=4
                  local.tee $l1
                  local.get $l27
                  local.get $l1
                  f32.load offset=28
                  local.get $l2
                  f32.load offset=28
                  f32.sub
                  f32.mul
                  f32.store offset=28
                  local.get $l3
                  i32.const 2
                  i32.add
                  local.tee $l3
                  local.get $l12
                  i32.ne
                  br_if $L118
                end
              end
              block $B119
                local.get $p0
                i32.load8_u offset=85
                br_if $B119
                local.get $l2
                i32.load offset=52
                i32.load8_u offset=41
                i32.const 8
                i32.and
                br_if $B119
                local.get $l2
                f32.load offset=100
                f32.const 0x0p+0 (;=0;)
                f32.eq
                br_if $B119
                local.get $l13
                i32.const 1
                i32.add
                local.tee $l3
                local.get $l12
                i32.ge_u
                br_if $B119
                local.get $l2
                i32.load offset=4
                local.set $l9
                local.get $l2
                i32.load
                local.set $l11
                local.get $l13
                local.set $l2
                loop $L120
                  block $B121 (result i32)
                    local.get $l3
                    local.get $p0
                    i32.load offset=28
                    local.get $l3
                    i32.const 2
                    i32.shl
                    i32.add
                    i32.load
                    local.tee $l1
                    i32.load
                    local.tee $l4
                    i32.eqz
                    br_if $B121
                    drop
                    local.get $l3
                    local.get $l1
                    i32.load offset=4
                    local.tee $l6
                    i32.eqz
                    br_if $B121
                    drop
                    block $B122
                      local.get $l4
                      local.get $l11
                      i32.eq
                      local.get $l6
                      local.get $l9
                      i32.ne
                      i32.and
                      br_if $B122
                      local.get $l6
                      local.get $l11
                      i32.ne
                      local.tee $l7
                      i32.eqz
                      local.get $l4
                      local.get $l9
                      i32.ne
                      i32.and
                      br_if $B122
                      local.get $l4
                      local.get $l9
                      i32.eq
                      i32.const 0
                      local.get $l7
                      select
                      br_if $B122
                      local.get $l3
                      local.get $l6
                      local.get $l9
                      i32.ne
                      br_if $B121
                      drop
                      local.get $l4
                      local.get $l11
                      i32.ne
                      br_if $B122
                      local.get $l3
                      br $B121
                    end
                    local.get $l3
                    local.get $l1
                    i32.load offset=92
                    local.get $l14
                    i32.eq
                    br_if $B121
                    drop
                    local.get $l1
                    local.get $l14
                    i32.store offset=92
                    local.get $l1
                    f32.load offset=28
                    local.set $l27
                    local.get $l27
                    local.get $l1
                    local.get $l41
                    call $f70619
                    local.tee $l26
                    f32.gt
                    if $I123
                      local.get $l3
                      local.tee $l1
                      local.get $l2
                      local.get $l13
                      i32.le_u
                      br_if $B121
                      drop
                      loop $L124
                        local.get $l3
                        local.get $p0
                        i32.load offset=28
                        local.tee $l4
                        local.get $l2
                        i32.const 2
                        i32.shl
                        i32.add
                        local.tee $l6
                        i32.load
                        local.tee $l7
                        f32.load offset=28
                        local.get $l26
                        f32.gt
                        i32.eqz
                        br_if $B121
                        drop
                        local.get $l6
                        local.get $l4
                        local.get $l1
                        i32.const 2
                        i32.shl
                        local.tee $l1
                        i32.add
                        i32.load
                        i32.store
                        local.get $p0
                        i32.load offset=28
                        local.get $l1
                        i32.add
                        local.get $l7
                        i32.store
                        local.get $l2
                        local.set $l1
                        local.get $l2
                        i32.const 1
                        i32.sub
                        local.tee $l2
                        local.get $l13
                        i32.gt_u
                        br_if $L124
                      end
                      local.get $l3
                      br $B121
                    end
                    local.get $l3
                    local.get $l26
                    local.get $l27
                    f32.gt
                    i32.eqz
                    br_if $B121
                    drop
                    local.get $l3
                    local.get $l12
                    local.get $l3
                    i32.const 1
                    i32.add
                    local.tee $l2
                    i32.le_u
                    br_if $B121
                    drop
                    local.get $l3
                    local.set $l4
                    local.get $l3
                    local.get $p0
                    i32.load offset=28
                    local.tee $l6
                    local.get $l2
                    i32.const 2
                    i32.shl
                    i32.add
                    local.tee $l1
                    i32.load
                    local.tee $l7
                    f32.load offset=28
                    local.get $l26
                    f32.lt
                    i32.eqz
                    br_if $B121
                    drop
                    loop $L125
                      block $B126
                        local.get $l1
                        local.get $l6
                        local.get $l4
                        i32.const 2
                        i32.shl
                        local.tee $l4
                        i32.add
                        i32.load
                        i32.store
                        local.get $p0
                        i32.load offset=28
                        local.get $l4
                        i32.add
                        local.get $l7
                        i32.store
                        local.get $l2
                        i32.const 1
                        i32.add
                        local.tee $l1
                        local.get $l12
                        i32.eq
                        br_if $B126
                        local.get $l2
                        local.set $l4
                        local.get $p0
                        i32.load offset=28
                        local.tee $l6
                        local.get $l1
                        local.tee $l2
                        i32.const 2
                        i32.shl
                        i32.add
                        local.tee $l1
                        i32.load
                        local.tee $l7
                        f32.load offset=28
                        local.get $l26
                        f32.lt
                        br_if $L125
                      end
                    end
                    local.get $l3
                    i32.const 1
                    i32.sub
                  end
                  local.tee $l2
                  i32.const 1
                  i32.add
                  local.tee $l3
                  local.get $l12
                  i32.lt_u
                  br_if $L120
                end
              end
              local.get $l22
              i32.const 1
              i32.add
              local.set $l22
              local.get $l14
              i32.const 1
              i32.add
              local.set $l14
            end
            local.get $l13
            i32.const 1
            i32.add
            local.tee $l13
            local.get $l12
            i32.lt_u
            br_if $L47
          end
        end
        local.get $l12
        local.set $l13
        local.get $l17
        i32.const 1
        i32.add
        local.tee $l17
        local.get $l23
        i32.ne
        br_if $L2
      end
    end
    local.get $p0
    i32.load offset=80
    local.get $l22
    call $f1708
    drop
    local.get $p0
    i32.load offset=36
    i32.load offset=304
    local.get $l21
    call $f69737
    local.get $l8
    i32.const 128
    i32.add
    global.set $g0)
