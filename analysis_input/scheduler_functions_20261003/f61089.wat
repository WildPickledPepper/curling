  (func $f61089 (type $t0) (param $p0 i32) (param $p1 i32) (result i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 f32)
    global.get $g0
    i32.const 48
    i32.sub
    local.tee $p1
    global.set $g0
    i32.const 4675153
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3768704
      call $f1661
      i32.const 3768708
      call $f1661
      i32.const 3768712
      call $f1661
      i32.const 3792572
      call $f1661
      i32.const 3773120
      call $f1661
      i32.const 4675153
      i32.const 1
      i32.store8
    end
    local.get $p1
    i32.const 40
    i32.add
    local.tee $l2
    i64.const 0
    i64.store
    local.get $p1
    i64.const 0
    i64.store offset=32
    local.get $p1
    i32.const 16
    i32.add
    local.get $p0
    i32.load offset=212
    i32.const 3773120
    i32.load
    call $f2922
    local.get $l2
    local.get $p1
    i64.load offset=24
    i64.store
    local.get $p1
    local.get $p1
    i64.load offset=16
    i64.store offset=32
    local.get $p1
    i32.const 0
    i32.store offset=8
    local.get $p1
    local.get $p1
    i32.const 32
    i32.add
    i32.store offset=12
    block $B1
      block $B2
        block $B3
          block $B4
            block $B5 (result i32)
              block $B6
                block $B7
                  block $B8
                    block $B9
                      block $B10
                        loop $L11
                          i32.const 4133620
                          i32.const 0
                          i32.store
                          i32.const 1681
                          local.get $p1
                          i32.const 32
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
                          br_if $B7
                          local.get $l3
                          i32.eqz
                          br_if $B8
                          i32.const 4133620
                          i32.const 0
                          i32.store
                          i32.const 10513
                          local.get $p1
                          i32.load offset=44
                          local.tee $l4
                          i32.const 0
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
                          br_if $B6
                          local.get $l3
                          i32.eqz
                          br_if $L11
                          i32.const 4133620
                          i32.const 0
                          i32.store
                          i32.const 10506
                          local.get $l4
                          i32.const 3792572
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
                          i32.const 4133620
                          i32.const 0
                          i32.store
                          i32.const 10514
                          local.get $p1
                          i32.const 16
                          i32.add
                          local.get $l3
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
                          br_if $B9
                          local.get $p1
                          f32.load offset=16
                          local.tee $l5
                          local.get $l5
                          f32.mul
                          local.get $p1
                          f32.load offset=20
                          local.tee $l5
                          local.get $l5
                          f32.mul
                          f32.add
                          local.get $p1
                          f32.load offset=24
                          local.tee $l5
                          local.get $l5
                          f32.mul
                          f32.add
                          f32.const 0x1.0c6f7ap-20 (;=1e-06;)
                          f32.gt
                          i32.eqz
                          br_if $L11
                        end
                        i32.const 0
                        local.set $l2
                        i32.const 3768704
                        i32.load
                        drop
                        br $B1
                      end
                      i32.const 3088636
                      call $env.__cxa_find_matching_catch_3
                      br $B5
                    end
                    i32.const 3088636
                    call $env.__cxa_find_matching_catch_3
                    br $B5
                  end
                  i32.const 3768704
                  i32.load
                  drop
                  br $B4
                end
                i32.const 3088636
                call $env.__cxa_find_matching_catch_3
                br $B5
              end
              i32.const 3088636
              call $env.__cxa_find_matching_catch_3
            end
            local.set $l2
            call $env.getTempRet0
            i32.const 3088636
            call $env.llvm_eh_typeid_for
            i32.eq
            if $I12
              local.get $l2
              call $env.__cxa_begin_catch
              i32.load
              local.set $l2
              i32.const 4133620
              i32.const 0
              i32.store
              local.get $p1
              local.get $l2
              i32.store offset=8
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
              i32.ne
              if $I13
                i32.const 3768704
                i32.load
                drop
                local.get $l2
                i32.eqz
                br_if $B4
                local.get $l2
                call $f1089
                unreachable
              end
              call $env.__cxa_find_matching_catch_2
              local.set $l2
              call $env.getTempRet0
              drop
            end
            i32.const 4133620
            i32.const 0
            i32.store
            i32.const 10710
            local.get $p1
            i32.const 8
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
            br_if $B3
            br $B2
          end
          local.get $p1
          i32.const 16
          i32.add
          local.get $p0
          i32.load offset=216
          i32.const 3773120
          i32.load
          call $f2922
          local.get $p1
          local.get $p1
          i64.load offset=24
          i64.store offset=40
          local.get $p1
          local.get $p1
          i64.load offset=16
          i64.store offset=32
          local.get $p1
          i32.const 0
          i32.store offset=8
          local.get $p1
          local.get $p1
          i32.const 32
          i32.add
          i32.store offset=12
          block $B14 (result i32)
            block $B15
              block $B16
                block $B17
                  block $B18
                    loop $L19
                      i32.const 4133620
                      i32.const 0
                      i32.store
                      i32.const 1681
                      local.get $p1
                      i32.const 32
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
                      br_if $B16
                      local.get $l3
                      i32.eqz
                      if $I20
                        i32.const 3768704
                        i32.load
                        drop
                        i32.const 1
                        local.set $l2
                        br $B1
                      end
                      i32.const 4133620
                      i32.const 0
                      i32.store
                      i32.const 10513
                      local.get $p1
                      i32.load offset=44
                      local.tee $l4
                      i32.const 0
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
                      br_if $B15
                      local.get $l3
                      i32.eqz
                      br_if $L19
                      i32.const 4133620
                      i32.const 0
                      i32.store
                      i32.const 10506
                      local.get $l4
                      i32.const 3792572
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
                      br_if $B18
                      i32.const 4133620
                      i32.const 0
                      i32.store
                      i32.const 10514
                      local.get $p1
                      i32.const 16
                      i32.add
                      local.get $l3
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
                      br_if $B17
                      local.get $p1
                      f32.load offset=16
                      local.tee $l5
                      local.get $l5
                      f32.mul
                      local.get $p1
                      f32.load offset=20
                      local.tee $l5
                      local.get $l5
                      f32.mul
                      f32.add
                      local.get $p1
                      f32.load offset=24
                      local.tee $l5
                      local.get $l5
                      f32.mul
                      f32.add
                      f32.const 0x1.0c6f7ap-20 (;=1e-06;)
                      f32.gt
                      i32.eqz
                      br_if $L19
                    end
                    i32.const 0
                    local.set $l2
                    i32.const 3768704
                    i32.load
                    drop
                    br $B1
                  end
                  i32.const 3088636
                  call $env.__cxa_find_matching_catch_3
                  br $B14
                end
                i32.const 3088636
                call $env.__cxa_find_matching_catch_3
                br $B14
              end
              i32.const 3088636
              call $env.__cxa_find_matching_catch_3
              br $B14
            end
            i32.const 3088636
            call $env.__cxa_find_matching_catch_3
          end
          local.set $l2
          call $env.getTempRet0
          i32.const 3088636
          call $env.llvm_eh_typeid_for
          i32.eq
          if $I21
            local.get $l2
            call $env.__cxa_begin_catch
            i32.load
            local.set $l2
            i32.const 4133620
            i32.const 0
            i32.store
            local.get $p1
            local.get $l2
            i32.store offset=8
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
            i32.ne
            if $I22
              i32.const 3768704
              i32.load
              drop
              local.get $l2
              i32.eqz
              if $I23
                i32.const 1
                local.set $l2
                br $B1
              end
              local.get $l2
              call $f1089
              unreachable
            end
            call $env.__cxa_find_matching_catch_2
            local.set $l2
            call $env.getTempRet0
            drop
          end
          i32.const 4133620
          i32.const 0
          i32.store
          i32.const 10711
          local.get $p1
          i32.const 8
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
          br_if $B2
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
      call $env.__resumeException
      unreachable
    end
    local.get $p1
    i32.const 48
    i32.add
    global.set $g0
    local.get $l2)
