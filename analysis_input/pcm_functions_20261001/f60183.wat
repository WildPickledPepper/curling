  (func $f60183 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32)
    global.get $g0
    i32.const -64
    i32.add
    local.tee $p1
    global.set $g0
    i32.const 4674508
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
      i32.const 4674508
      i32.const 1
      i32.store8
    end
    local.get $p1
    i32.const 56
    i32.add
    local.tee $l4
    i64.const 0
    i64.store
    local.get $p1
    i64.const 0
    i64.store offset=48
    local.get $p1
    i32.const 32
    i32.add
    local.get $p0
    i32.load offset=192
    i32.const 3773120
    i32.load
    call $f2922
    local.get $l4
    local.get $p1
    i64.load offset=40
    i64.store
    local.get $p1
    local.get $p1
    i64.load offset=32
    i64.store offset=48
    local.get $p1
    i32.const 0
    i32.store offset=32
    local.get $p0
    i32.const 200
    i32.add
    local.set $l4
    local.get $p1
    local.get $p1
    i32.const 48
    i32.add
    i32.store offset=36
    block $B1
      block $B2
        block $B3
          block $B4
            block $B5
              block $B6
                block $B7
                  block $B8
                    block $B9 (result i32)
                      block $B10
                        block $B11
                          block $B12
                            block $B13
                              loop $L14
                                i32.const 4133620
                                i32.const 0
                                i32.store
                                i32.const 1681
                                local.get $p1
                                i32.const 48
                                i32.add
                                i32.const 3768708
                                i32.load
                                call $env.invoke_iii
                                local.set $l3
                                i32.const 4133620
                                i32.load
                                local.set $l2
                                i32.const 4133620
                                i32.const 0
                                i32.store
                                local.get $l2
                                i32.const 1
                                i32.eq
                                br_if $B10
                                local.get $l3
                                if $I15
                                  i32.const 4133620
                                  i32.const 0
                                  i32.store
                                  i32.const 10509
                                  local.get $p1
                                  i32.load offset=60
                                  local.tee $l2
                                  i32.const 0
                                  call $env.invoke_iii
                                  local.set $l5
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
                                  i32.const 4133620
                                  i32.const 0
                                  i32.store
                                  local.get $p1
                                  local.get $l4
                                  i32.load offset=8
                                  i32.store offset=24
                                  local.get $p1
                                  local.get $l4
                                  i64.load align=4
                                  i64.store offset=16
                                  i32.const 10510
                                  local.get $l5
                                  local.get $p1
                                  i32.const 16
                                  i32.add
                                  i32.const 0
                                  call $env.invoke_viii
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
                                  i32.const 4133620
                                  i32.const 0
                                  i32.store
                                  i32.const 10506
                                  local.get $l2
                                  i32.const 3792500
                                  i32.load
                                  call $env.invoke_iii
                                  local.set $l5
                                  i32.const 4133620
                                  i32.load
                                  local.set $l3
                                  i32.const 4133620
                                  i32.const 0
                                  i32.store
                                  local.get $l3
                                  i32.const 1
                                  i32.eq
                                  br_if $B11
                                  local.get $l5
                                  i32.const 0
                                  i32.store8 offset=16
                                  i32.const 4133620
                                  i32.const 0
                                  i32.store
                                  i32.const 10236
                                  local.get $l2
                                  i32.const 0
                                  i32.const 0
                                  call $env.invoke_viii
                                  i32.const 4133620
                                  i32.load
                                  local.set $l2
                                  i32.const 4133620
                                  i32.const 0
                                  i32.store
                                  local.get $l2
                                  i32.const 1
                                  i32.eq
                                  br_if $B11
                                  br $L14
                                end
                              end
                              i32.const 3768704
                              i32.load
                              drop
                              br $B8
                            end
                            i32.const 3088636
                            call $env.__cxa_find_matching_catch_3
                            br $B9
                          end
                          i32.const 3088636
                          call $env.__cxa_find_matching_catch_3
                          br $B9
                        end
                        i32.const 3088636
                        call $env.__cxa_find_matching_catch_3
                        br $B9
                      end
                      i32.const 3088636
                      call $env.__cxa_find_matching_catch_3
                    end
                    local.set $l2
                    call $env.getTempRet0
                    i32.const 3088636
                    call $env.llvm_eh_typeid_for
                    i32.ne
                    br_if $B6
                    local.get $l2
                    call $env.__cxa_begin_catch
                    i32.load
                    local.set $l2
                    i32.const 4133620
                    i32.const 0
                    i32.store
                    local.get $p1
                    local.get $l2
                    i32.store offset=32
                    i32.const 58
                    call $env.invoke_v
                    i32.const 4133620
                    i32.load
                    local.set $l3
                    i32.const 4133620
                    i32.const 0
                    i32.store
                    local.get $l3
                    i32.const 1
                    i32.eq
                    br_if $B7
                    i32.const 3768704
                    i32.load
                    drop
                    local.get $l2
                    br_if $B3
                  end
                  local.get $p1
                  i32.const 32
                  i32.add
                  local.get $p0
                  i32.load offset=196
                  i32.const 3773120
                  i32.load
                  call $f2922
                  local.get $p1
                  local.get $p1
                  i64.load offset=40
                  i64.store offset=56
                  local.get $p1
                  local.get $p1
                  i64.load offset=32
                  i64.store offset=48
                  local.get $p1
                  i32.const 0
                  i32.store offset=32
                  local.get $p1
                  local.get $p1
                  i32.const 48
                  i32.add
                  i32.store offset=36
                  br $B5
                end
                call $env.__cxa_find_matching_catch_2
                local.set $l2
                call $env.getTempRet0
                drop
              end
              i32.const 4133620
              i32.const 0
              i32.store
              i32.const 10530
              local.get $p1
              i32.const 32
              i32.add
              call $env.invoke_ii
              drop
              i32.const 4133620
              i32.load
              local.set $p1
              i32.const 4133620
              i32.const 0
              i32.store
              local.get $p1
              i32.const 1
              i32.eq
              br_if $B4
              br $B1
            end
            block $B16
              block $B17
                block $B18
                  block $B19 (result i32)
                    block $B20
                      block $B21
                        block $B22
                          block $B23
                            loop $L24
                              i32.const 4133620
                              i32.const 0
                              i32.store
                              i32.const 1681
                              local.get $p1
                              i32.const 48
                              i32.add
                              i32.const 3768708
                              i32.load
                              call $env.invoke_iii
                              local.set $l3
                              i32.const 4133620
                              i32.load
                              local.set $l2
                              i32.const 4133620
                              i32.const 0
                              i32.store
                              local.get $l2
                              i32.const 1
                              i32.eq
                              br_if $B20
                              local.get $l3
                              if $I25
                                i32.const 4133620
                                i32.const 0
                                i32.store
                                i32.const 10509
                                local.get $p1
                                i32.load offset=60
                                local.tee $l2
                                i32.const 0
                                call $env.invoke_iii
                                local.set $l5
                                i32.const 4133620
                                i32.load
                                local.set $l3
                                i32.const 4133620
                                i32.const 0
                                i32.store
                                local.get $l3
                                i32.const 1
                                i32.eq
                                br_if $B23
                                i32.const 4133620
                                i32.const 0
                                i32.store
                                local.get $p1
                                local.get $l4
                                i32.load offset=8
                                i32.store offset=8
                                local.get $p1
                                local.get $l4
                                i64.load align=4
                                i64.store
                                i32.const 10510
                                local.get $l5
                                local.get $p1
                                i32.const 0
                                call $env.invoke_viii
                                i32.const 4133620
                                i32.load
                                local.set $l3
                                i32.const 4133620
                                i32.const 0
                                i32.store
                                local.get $l3
                                i32.const 1
                                i32.eq
                                br_if $B22
                                i32.const 4133620
                                i32.const 0
                                i32.store
                                i32.const 10506
                                local.get $l2
                                i32.const 3792500
                                i32.load
                                call $env.invoke_iii
                                local.set $l5
                                i32.const 4133620
                                i32.load
                                local.set $l3
                                i32.const 4133620
                                i32.const 0
                                i32.store
                                local.get $l3
                                i32.const 1
                                i32.eq
                                br_if $B21
                                local.get $l5
                                i32.const 0
                                i32.store8 offset=16
                                i32.const 4133620
                                i32.const 0
                                i32.store
                                i32.const 10236
                                local.get $l2
                                i32.const 0
                                i32.const 0
                                call $env.invoke_viii
                                i32.const 4133620
                                i32.load
                                local.set $l2
                                i32.const 4133620
                                i32.const 0
                                i32.store
                                local.get $l2
                                i32.const 1
                                i32.eq
                                br_if $B21
                                br $L24
                              end
                            end
                            i32.const 3768704
                            i32.load
                            drop
                            br $B18
                          end
                          i32.const 3088636
                          call $env.__cxa_find_matching_catch_3
                          br $B19
                        end
                        i32.const 3088636
                        call $env.__cxa_find_matching_catch_3
                        br $B19
                      end
                      i32.const 3088636
                      call $env.__cxa_find_matching_catch_3
                      br $B19
                    end
                    i32.const 3088636
                    call $env.__cxa_find_matching_catch_3
                  end
                  local.set $l2
                  call $env.getTempRet0
                  i32.const 3088636
                  call $env.llvm_eh_typeid_for
                  i32.ne
                  br_if $B16
                  local.get $l2
                  call $env.__cxa_begin_catch
                  i32.load
                  local.set $l4
                  i32.const 4133620
                  i32.const 0
                  i32.store
                  local.get $p1
                  local.get $l4
                  i32.store offset=32
                  i32.const 58
                  call $env.invoke_v
                  i32.const 4133620
                  i32.load
                  local.set $l2
                  i32.const 4133620
                  i32.const 0
                  i32.store
                  local.get $l2
                  i32.const 1
                  i32.eq
                  br_if $B17
                  i32.const 3768704
                  i32.load
                  drop
                  local.get $l4
                  br_if $B2
                end
                local.get $p1
                i32.const -64
                i32.sub
                global.set $g0
                return
              end
              call $env.__cxa_find_matching_catch_2
              local.set $l2
              call $env.getTempRet0
              drop
            end
            i32.const 4133620
            i32.const 0
            i32.store
            i32.const 10531
            local.get $p1
            i32.const 32
            i32.add
            call $env.invoke_ii
            drop
            i32.const 4133620
            i32.load
            local.set $p1
            i32.const 4133620
            i32.const 0
            i32.store
            local.get $p1
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
        local.get $l2
        call $f1089
        unreachable
      end
      local.get $l4
      call $f1089
      unreachable
    end
    local.get $l2
    call $env.__resumeException
    unreachable)
