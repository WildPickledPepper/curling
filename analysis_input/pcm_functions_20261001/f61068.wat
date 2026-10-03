  (func $f61068 (type $t2) (param $p0 i32) (param $p1 i32) (param $p2 i32)
    (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 f32) (local $l10 f32) (local $l11 f32)
    global.get $g0
    i32.const 224
    i32.sub
    local.tee $p2
    global.set $g0
    i32.const 4675141
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3768704
      call $f1661
      i32.const 3768708
      call $f1661
      i32.const 3768712
      call $f1661
      i32.const 3792500
      call $f1661
      i32.const 3773120
      call $f1661
      i32.const 3773132
      call $f1661
      i32.const 4675141
      i32.const 1
      i32.store8
    end
    local.get $p2
    i32.const 192
    i32.add
    local.get $p0
    i32.load offset=212
    i32.const 3773120
    i32.load
    call $f2922
    local.get $p2
    local.get $p2
    i64.load offset=200
    i64.store offset=216
    local.get $p2
    local.get $p2
    i64.load offset=192
    i64.store offset=208
    local.get $p2
    i32.const 0
    i32.store offset=192
    local.get $p2
    local.get $p2
    i32.const 208
    i32.add
    i32.store offset=196
    block $B1
      block $B2
        block $B3
          block $B4
            block $B5
              block $B6
                block $B7
                  block $B8
                    block $B9
                      block $B10
                        block $B11 (result i32)
                          block $B12
                            block $B13
                              loop $L14
                                i32.const 4133620
                                i32.const 0
                                i32.store
                                i32.const 1681
                                local.get $p2
                                i32.const 208
                                i32.add
                                i32.const 3768708
                                i32.load
                                call $env.invoke_iii
                                local.set $l4
                                i32.const 4133620
                                i32.load
                                local.set $l3
                                i32.const 4133620
                                i32.const 0
                                i32.store
                                local.get $l3
                                i32.const 1
                                i32.eq
                                br_if $B12
                                local.get $l4
                                if $I15
                                  i32.const 4133620
                                  i32.const 0
                                  i32.store
                                  i32.const 10506
                                  local.get $p2
                                  i32.load offset=220
                                  i32.const 3792500
                                  i32.load
                                  call $env.invoke_iii
                                  local.set $l4
                                  i32.const 4133620
                                  i32.load
                                  local.set $l3
                                  i32.const 4133620
                                  i32.const 0
                                  i32.store
                                  local.get $l3
                                  i32.const 1
                                  i32.eq
                                  br_if $B13
                                  local.get $l4
                                  i32.const 0
                                  i32.store8 offset=16
                                  br $L14
                                end
                              end
                              i32.const 3768704
                              i32.load
                              drop
                              br $B10
                            end
                            i32.const 3088636
                            call $env.__cxa_find_matching_catch_3
                            br $B11
                          end
                          i32.const 3088636
                          call $env.__cxa_find_matching_catch_3
                        end
                        local.set $l3
                        call $env.getTempRet0
                        i32.const 3088636
                        call $env.llvm_eh_typeid_for
                        i32.ne
                        br_if $B8
                        local.get $l3
                        call $env.__cxa_begin_catch
                        i32.load
                        local.set $l3
                        i32.const 4133620
                        i32.const 0
                        i32.store
                        local.get $p2
                        local.get $l3
                        i32.store offset=192
                        i32.const 58
                        call $env.invoke_v
                        i32.const 4133620
                        i32.load
                        local.set $l4
                        i32.const 4133620
                        i32.const 0
                        i32.store
                        local.get $l4
                        i32.const 1
                        i32.eq
                        br_if $B9
                        i32.const 3768704
                        i32.load
                        drop
                        local.get $l3
                        br_if $B6
                      end
                      local.get $p2
                      i32.const 192
                      i32.add
                      local.get $p0
                      i32.load offset=216
                      i32.const 3773120
                      i32.load
                      call $f2922
                      local.get $p2
                      local.get $p2
                      i64.load offset=200
                      i64.store offset=216
                      local.get $p2
                      local.get $p2
                      i64.load offset=192
                      i64.store offset=208
                      local.get $p2
                      i32.const 0
                      i32.store offset=192
                      local.get $p2
                      local.get $p2
                      i32.const 208
                      i32.add
                      i32.store offset=196
                      br $B7
                    end
                    call $env.__cxa_find_matching_catch_2
                    local.set $l3
                    call $env.getTempRet0
                    drop
                  end
                  i32.const 4133620
                  i32.const 0
                  i32.store
                  i32.const 10706
                  local.get $p2
                  i32.const 192
                  i32.add
                  call $env.invoke_ii
                  drop
                  i32.const 4133620
                  i32.load
                  local.set $p2
                  i32.const 4133620
                  i32.const 0
                  i32.store
                  local.get $p2
                  i32.const 1
                  i32.eq
                  br_if $B2
                  br $B1
                end
                block $B16
                  block $B17 (result i32)
                    block $B18
                      block $B19
                        loop $L20
                          i32.const 4133620
                          i32.const 0
                          i32.store
                          i32.const 1681
                          local.get $p2
                          i32.const 208
                          i32.add
                          i32.const 3768708
                          i32.load
                          call $env.invoke_iii
                          local.set $l4
                          i32.const 4133620
                          i32.load
                          local.set $l3
                          i32.const 4133620
                          i32.const 0
                          i32.store
                          local.get $l3
                          i32.const 1
                          i32.eq
                          br_if $B18
                          local.get $l4
                          if $I21
                            i32.const 4133620
                            i32.const 0
                            i32.store
                            i32.const 10506
                            local.get $p2
                            i32.load offset=220
                            i32.const 3792500
                            i32.load
                            call $env.invoke_iii
                            local.set $l4
                            i32.const 4133620
                            i32.load
                            local.set $l3
                            i32.const 4133620
                            i32.const 0
                            i32.store
                            local.get $l3
                            i32.const 1
                            i32.eq
                            br_if $B19
                            local.get $l4
                            i32.const 0
                            i32.store8 offset=16
                            br $L20
                          end
                        end
                        i32.const 3768704
                        i32.load
                        drop
                        br $B16
                      end
                      i32.const 3088636
                      call $env.__cxa_find_matching_catch_3
                      br $B17
                    end
                    i32.const 3088636
                    call $env.__cxa_find_matching_catch_3
                  end
                  local.set $l3
                  call $env.getTempRet0
                  i32.const 3088636
                  call $env.llvm_eh_typeid_for
                  i32.ne
                  br_if $B3
                  local.get $l3
                  call $env.__cxa_begin_catch
                  i32.load
                  local.set $l3
                  i32.const 4133620
                  i32.const 0
                  i32.store
                  local.get $p2
                  local.get $l3
                  i32.store offset=192
                  i32.const 58
                  call $env.invoke_v
                  i32.const 4133620
                  i32.load
                  local.set $l4
                  i32.const 4133620
                  i32.const 0
                  i32.store
                  local.get $l4
                  i32.const 1
                  i32.eq
                  br_if $B4
                  i32.const 3768704
                  i32.load
                  drop
                  local.get $l3
                  br_if $B5
                end
                local.get $p0
                i32.const 220
                i32.add
                local.set $l7
                i32.const 0
                local.set $l3
                loop $L22
                  local.get $l3
                  i32.const 2
                  i32.shl
                  local.tee $l4
                  i32.const 1
                  i32.or
                  local.set $l5
                  local.get $p1
                  i32.load
                  local.tee $l6
                  local.get $l3
                  i32.const 4
                  i32.shl
                  i32.add
                  f32.load offset=16
                  local.set $l9
                  block $B23
                    local.get $p0
                    i32.load offset=144
                    i32.eqz
                    if $I24
                      block $B25
                        block $B26
                          local.get $l9
                          f32.const 0x0p+0 (;=0;)
                          f32.eq
                          if $I27
                            local.get $l6
                            local.get $l5
                            i32.const 2
                            i32.shl
                            i32.add
                            f32.load offset=16
                            f32.const 0x0p+0 (;=0;)
                            f32.eq
                            br_if $B26
                          end
                          local.get $p0
                          i32.load offset=212
                          local.get $l3
                          i32.const 3773132
                          i32.load
                          call $f2903
                          i32.const 1
                          i32.const 0
                          call $f54405
                          local.get $p0
                          i32.load offset=212
                          local.get $l3
                          i32.const 3773132
                          i32.load
                          call $f2903
                          i32.const 0
                          call $f54401
                          local.set $l6
                          local.get $p1
                          i32.load
                          i32.const 16
                          i32.add
                          local.tee $l8
                          local.get $l5
                          i32.const 2
                          i32.shl
                          i32.add
                          f32.load
                          local.set $l9
                          local.get $p0
                          f32.load offset=244
                          local.set $l10
                          local.get $p0
                          f32.load offset=224
                          local.set $l11
                          local.get $p2
                          i32.const 184
                          i32.add
                          local.tee $l5
                          local.get $p0
                          f32.load offset=252
                          local.get $l8
                          local.get $l4
                          i32.const 2
                          i32.shl
                          i32.add
                          f32.load
                          f32.sub
                          f32.store
                          local.get $p2
                          local.get $l5
                          i32.load
                          i32.store offset=56
                          local.get $p2
                          local.get $l11
                          f32.store offset=180
                          local.get $p2
                          local.get $l10
                          local.get $l9
                          f32.sub
                          f32.store offset=176
                          local.get $p2
                          local.get $p2
                          i64.load offset=176
                          i64.store offset=48
                          local.get $l6
                          local.get $p2
                          i32.const 48
                          i32.add
                          i32.const 0
                          call $f54626
                          br $B25
                        end
                        local.get $p0
                        i32.load offset=212
                        local.get $l3
                        i32.const 3773132
                        i32.load
                        call $f2903
                        i32.const 0
                        i32.const 0
                        call $f54405
                        local.get $p0
                        i32.load offset=212
                        local.get $l3
                        i32.const 3773132
                        i32.load
                        call $f2903
                        i32.const 0
                        call $f54401
                        local.set $l5
                        local.get $p2
                        local.get $l7
                        i32.load offset=8
                        i32.store offset=40
                        local.get $p2
                        local.get $l7
                        i64.load align=4
                        i64.store offset=32
                        local.get $l5
                        local.get $p2
                        i32.const 32
                        i32.add
                        i32.const 0
                        call $f54626
                      end
                      local.get $l4
                      i32.const 3
                      i32.or
                      local.set $l5
                      block $B28
                        local.get $p1
                        i32.load
                        local.tee $l6
                        local.get $l4
                        i32.const 2
                        i32.or
                        i32.const 2
                        i32.shl
                        local.tee $l4
                        i32.add
                        f32.load offset=16
                        f32.const 0x0p+0 (;=0;)
                        f32.eq
                        if $I29
                          local.get $l6
                          local.get $l5
                          i32.const 2
                          i32.shl
                          i32.add
                          f32.load offset=16
                          f32.const 0x0p+0 (;=0;)
                          f32.eq
                          br_if $B28
                        end
                        local.get $p0
                        i32.load offset=216
                        local.get $l3
                        i32.const 3773132
                        i32.load
                        call $f2903
                        i32.const 1
                        i32.const 0
                        call $f54405
                        local.get $p0
                        i32.load offset=216
                        local.get $l3
                        i32.const 3773132
                        i32.load
                        call $f2903
                        i32.const 0
                        call $f54401
                        local.set $l6
                        local.get $p1
                        i32.load
                        i32.const 16
                        i32.add
                        local.tee $l8
                        local.get $l5
                        i32.const 2
                        i32.shl
                        i32.add
                        f32.load
                        local.set $l9
                        local.get $p0
                        f32.load offset=244
                        local.set $l10
                        local.get $p0
                        f32.load offset=224
                        local.set $l11
                        local.get $p2
                        i32.const 168
                        i32.add
                        local.tee $l5
                        local.get $p0
                        f32.load offset=252
                        local.get $l4
                        local.get $l8
                        i32.add
                        f32.load
                        f32.sub
                        f32.store
                        local.get $p2
                        local.get $l5
                        i32.load
                        i32.store offset=24
                        local.get $p2
                        local.get $l11
                        f32.store offset=164
                        local.get $p2
                        local.get $l10
                        local.get $l9
                        f32.sub
                        f32.store offset=160
                        local.get $p2
                        local.get $p2
                        i64.load offset=160
                        i64.store offset=16
                        local.get $l6
                        local.get $p2
                        i32.const 16
                        i32.add
                        i32.const 0
                        call $f54626
                        br $B23
                      end
                      local.get $p0
                      i32.load offset=216
                      local.get $l3
                      i32.const 3773132
                      i32.load
                      call $f2903
                      i32.const 0
                      i32.const 0
                      call $f54405
                      local.get $p0
                      i32.load offset=216
                      local.get $l3
                      i32.const 3773132
                      i32.load
                      call $f2903
                      i32.const 0
                      call $f54401
                      local.set $l4
                      local.get $p2
                      local.get $l7
                      i32.load offset=8
                      i32.store offset=8
                      local.get $p2
                      local.get $l7
                      i64.load align=4
                      i64.store
                      local.get $l4
                      local.get $p2
                      i32.const 0
                      call $f54626
                      br $B23
                    end
                    block $B30
                      block $B31
                        local.get $l9
                        f32.const 0x0p+0 (;=0;)
                        f32.eq
                        if $I32
                          local.get $l6
                          local.get $l5
                          i32.const 2
                          i32.shl
                          i32.add
                          f32.load offset=16
                          f32.const 0x0p+0 (;=0;)
                          f32.eq
                          br_if $B31
                        end
                        local.get $p0
                        i32.load offset=216
                        local.get $l3
                        i32.const 3773132
                        i32.load
                        call $f2903
                        i32.const 1
                        i32.const 0
                        call $f54405
                        local.get $p0
                        i32.load offset=216
                        local.get $l3
                        i32.const 3773132
                        i32.load
                        call $f2903
                        i32.const 0
                        call $f54401
                        local.set $l6
                        local.get $p1
                        i32.load
                        i32.const 16
                        i32.add
                        local.tee $l8
                        local.get $l5
                        i32.const 2
                        i32.shl
                        i32.add
                        f32.load
                        local.set $l9
                        local.get $p0
                        f32.load offset=244
                        local.set $l10
                        local.get $p0
                        f32.load offset=224
                        local.set $l11
                        local.get $p2
                        i32.const 152
                        i32.add
                        local.tee $l5
                        local.get $p0
                        f32.load offset=252
                        local.get $l8
                        local.get $l4
                        i32.const 2
                        i32.shl
                        i32.add
                        f32.load
                        f32.sub
                        f32.store
                        local.get $p2
                        local.get $l5
                        i32.load
                        i32.store offset=120
                        local.get $p2
                        local.get $l11
                        f32.store offset=148
                        local.get $p2
                        local.get $l10
                        local.get $l9
                        f32.sub
                        f32.store offset=144
                        local.get $p2
                        local.get $p2
                        i64.load offset=144
                        i64.store offset=112
                        local.get $l6
                        local.get $p2
                        i32.const 112
                        i32.add
                        i32.const 0
                        call $f54626
                        br $B30
                      end
                      local.get $p0
                      i32.load offset=216
                      local.get $l3
                      i32.const 3773132
                      i32.load
                      call $f2903
                      i32.const 0
                      i32.const 0
                      call $f54405
                      local.get $p0
                      i32.load offset=216
                      local.get $l3
                      i32.const 3773132
                      i32.load
                      call $f2903
                      i32.const 0
                      call $f54401
                      local.set $l5
                      local.get $p2
                      local.get $l7
                      i32.load offset=8
                      i32.store offset=104
                      local.get $p2
                      local.get $l7
                      i64.load align=4
                      i64.store offset=96
                      local.get $l5
                      local.get $p2
                      i32.const 96
                      i32.add
                      i32.const 0
                      call $f54626
                    end
                    local.get $l4
                    i32.const 3
                    i32.or
                    local.set $l5
                    block $B33
                      local.get $p1
                      i32.load
                      local.tee $l6
                      local.get $l4
                      i32.const 2
                      i32.or
                      i32.const 2
                      i32.shl
                      local.tee $l4
                      i32.add
                      f32.load offset=16
                      f32.const 0x0p+0 (;=0;)
                      f32.eq
                      if $I34
                        local.get $l6
                        local.get $l5
                        i32.const 2
                        i32.shl
                        i32.add
                        f32.load offset=16
                        f32.const 0x0p+0 (;=0;)
                        f32.eq
                        br_if $B33
                      end
                      local.get $p0
                      i32.load offset=212
                      local.get $l3
                      i32.const 3773132
                      i32.load
                      call $f2903
                      i32.const 1
                      i32.const 0
                      call $f54405
                      local.get $p0
                      i32.load offset=212
                      local.get $l3
                      i32.const 3773132
                      i32.load
                      call $f2903
                      i32.const 0
                      call $f54401
                      local.set $l6
                      local.get $p1
                      i32.load
                      i32.const 16
                      i32.add
                      local.tee $l8
                      local.get $l5
                      i32.const 2
                      i32.shl
                      i32.add
                      f32.load
                      local.set $l9
                      local.get $p0
                      f32.load offset=244
                      local.set $l10
                      local.get $p0
                      f32.load offset=224
                      local.set $l11
                      local.get $p2
                      i32.const 136
                      i32.add
                      local.tee $l5
                      local.get $p0
                      f32.load offset=252
                      local.get $l4
                      local.get $l8
                      i32.add
                      f32.load
                      f32.sub
                      f32.store
                      local.get $p2
                      local.get $l5
                      i32.load
                      i32.store offset=88
                      local.get $p2
                      local.get $l11
                      f32.store offset=132
                      local.get $p2
                      local.get $l10
                      local.get $l9
                      f32.sub
                      f32.store offset=128
                      local.get $p2
                      local.get $p2
                      i64.load offset=128
                      i64.store offset=80
                      local.get $l6
                      local.get $p2
                      i32.const 80
                      i32.add
                      i32.const 0
                      call $f54626
                      br $B23
                    end
                    local.get $p0
                    i32.load offset=212
                    local.get $l3
                    i32.const 3773132
                    i32.load
                    call $f2903
                    i32.const 0
                    i32.const 0
                    call $f54405
                    local.get $p0
                    i32.load offset=212
                    local.get $l3
                    i32.const 3773132
                    i32.load
                    call $f2903
                    i32.const 0
                    call $f54401
                    local.set $l4
                    local.get $p2
                    local.get $l7
                    i32.load offset=8
                    i32.store offset=72
                    local.get $p2
                    local.get $l7
                    i64.load align=4
                    i64.store offset=64
                    local.get $l4
                    local.get $p2
                    i32.const -64
                    i32.sub
                    i32.const 0
                    call $f54626
                  end
                  local.get $l3
                  i32.const 1
                  i32.add
                  local.tee $l3
                  i32.const 8
                  i32.ne
                  br_if $L22
                end
                local.get $p2
                i32.const 224
                i32.add
                global.set $g0
                return
              end
              local.get $l3
              call $f1089
              unreachable
            end
            local.get $l3
            call $f1089
            unreachable
          end
          call $env.__cxa_find_matching_catch_2
          local.set $l3
          call $env.getTempRet0
          drop
        end
        i32.const 4133620
        i32.const 0
        i32.store
        i32.const 10707
        local.get $p2
        i32.const 192
        i32.add
        call $env.invoke_ii
        drop
        i32.const 4133620
        i32.load
        local.set $p2
        i32.const 4133620
        i32.const 0
        i32.store
        local.get $p2
        i32.const 1
        i32.ne
        br_if $B1
      end
      i32.const 0
      call $env.__cxa_find_matching_catch_3
      drop
      call $env.getTempRet0
      drop
      call $f640
      unreachable
    end
    local.get $l3
    call $env.__resumeException
    unreachable)
