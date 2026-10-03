  (func $f60174 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32)
    global.get $g0
    i32.const 32
    i32.sub
    local.tee $l2
    global.set $g0
    i32.const 4674500
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3749616
      call $f1661
      i32.const 3750448
      call $f1661
      i32.const 3771940
      call $f1661
      i32.const 3771944
      call $f1661
      i32.const 3771948
      call $f1661
      i32.const 4674500
      i32.const 1
      i32.store8
    end
    i32.const 3749616
    i32.load
    local.tee $l4
    i32.load offset=116
    i32.eqz
    if $I1
      local.get $l4
      call $f65192
      i32.const 3749616
      i32.load
      local.set $l4
    end
    i32.const 0
    local.set $p1
    i32.const 3750448
    i32.load
    local.set $l3
    block $B2 (result i32)
      block $B3
        local.get $l4
        i32.load offset=92
        i32.load
        local.tee $l5
        i32.load
        local.tee $l6
        i32.load16_u offset=182
        local.tee $l7
        i32.eqz
        br_if $B3
        local.get $l6
        i32.load offset=88
        local.set $l4
        loop $L4
          local.get $l3
          local.get $l4
          local.get $p1
          i32.const 3
          i32.shl
          i32.add
          i32.load
          i32.ne
          if $I5
            local.get $l7
            local.get $p1
            i32.const 1
            i32.add
            local.tee $p1
            i32.ne
            br_if $L4
            br $B3
          end
        end
        local.get $l4
        local.get $p1
        i32.const 3
        i32.shl
        i32.add
        i32.load offset=4
        i32.const 3
        i32.shl
        local.get $l6
        i32.add
        i32.const 208
        i32.add
        br $B2
      end
      local.get $l5
      local.get $l3
      i32.const 2
      call $f1150
    end
    local.set $p1
    local.get $l5
    local.get $p1
    i32.load offset=4
    local.get $p1
    i32.load
    call_indirect $__indirect_function_table (type $t0)
    local.set $p1
    local.get $l2
    i32.const 0
    i32.store8 offset=27
    local.get $l2
    local.get $p1
    i32.store offset=28
    i32.const 4133620
    i32.const 0
    i32.store
    local.get $l2
    local.get $l2
    i32.const 28
    i32.add
    i32.store offset=16
    local.get $l2
    i32.const 0
    i32.store offset=8
    local.get $l2
    local.get $l2
    i32.const 27
    i32.add
    i32.store offset=12
    i32.const 1290
    local.get $p1
    local.get $l2
    i32.const 27
    i32.add
    i32.const 0
    call $env.invoke_viii
    i32.const 4133620
    i32.load
    local.set $p1
    i32.const 4133620
    i32.const 0
    i32.store
    block $B6
      block $B7
        block $B8
          block $B9
            block $B10
              block $B11 (result i32)
                block $B12
                  block $B13
                    local.get $p1
                    i32.const 1
                    i32.eq
                    br_if $B13
                    i32.const 3749616
                    i32.load
                    local.tee $p1
                    i32.load offset=116
                    i32.eqz
                    if $I14
                      i32.const 4133620
                      i32.const 0
                      i32.store
                      i32.const 664
                      local.get $p1
                      call $env.invoke_vi
                      i32.const 4133620
                      i32.load
                      local.set $p1
                      i32.const 4133620
                      i32.const 0
                      i32.store
                      local.get $p1
                      i32.const 1
                      i32.eq
                      br_if $B13
                      i32.const 3749616
                      i32.load
                      local.set $p1
                    end
                    local.get $p1
                    i32.load offset=92
                    i32.load
                    i32.load offset=12
                    i32.const 0
                    i32.gt_s
                    br_if $B12
                    i32.const 0
                    local.set $p1
                    br $B10
                  end
                  i32.const 3088636
                  call $env.__cxa_find_matching_catch_3
                  br $B11
                end
                block $B15
                  block $B16
                    block $B17
                      local.get $p1
                      i32.load offset=116
                      if $I18 (result i32)
                        local.get $p1
                      else
                        i32.const 4133620
                        i32.const 0
                        i32.store
                        i32.const 664
                        local.get $p1
                        call $env.invoke_vi
                        i32.const 4133620
                        i32.load
                        local.set $p1
                        i32.const 4133620
                        i32.const 0
                        i32.store
                        local.get $p1
                        i32.const 1
                        i32.eq
                        br_if $B17
                        i32.const 3749616
                        i32.load
                      end
                      i32.load offset=92
                      i32.load
                      local.set $p1
                      i32.const 4133620
                      i32.const 0
                      i32.store
                      i32.const 970
                      local.get $p1
                      i32.const 0
                      i32.const 3771948
                      i32.load
                      call $env.invoke_iiii
                      local.set $l3
                      i32.const 4133620
                      i32.load
                      local.set $p1
                      i32.const 4133620
                      i32.const 0
                      i32.store
                      local.get $p1
                      i32.const 1
                      i32.eq
                      br_if $B16
                      i32.const 4133620
                      i32.const 0
                      i32.store
                      i32.const 10528
                      local.get $p0
                      local.get $l3
                      local.get $p1
                      call $env.invoke_iiii
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
                      br_if $B15
                      i32.const 0
                      local.set $p1
                      i32.const 3749616
                      i32.load
                      i32.load offset=92
                      i32.load
                      local.set $l3
                      i32.const 4133620
                      i32.const 0
                      i32.store
                      i32.const 3575
                      local.get $l3
                      i32.const 0
                      i32.const 3771940
                      i32.load
                      call $env.invoke_viii
                      i32.const 4133620
                      i32.load
                      local.set $l3
                      i32.const 4133620
                      i32.const 0
                      i32.store
                      local.get $l3
                      i32.const 1
                      i32.ne
                      br_if $B10
                      i32.const 3088636
                      call $env.__cxa_find_matching_catch_3
                      br $B11
                    end
                    i32.const 3088636
                    call $env.__cxa_find_matching_catch_3
                    br $B11
                  end
                  i32.const 3088636
                  call $env.__cxa_find_matching_catch_3
                  br $B11
                end
                i32.const 3088636
                call $env.__cxa_find_matching_catch_3
              end
              local.set $p1
              call $env.getTempRet0
              i32.const 3088636
              call $env.llvm_eh_typeid_for
              i32.ne
              br_if $B8
              local.get $p1
              call $env.__cxa_begin_catch
              i32.load
              local.set $p1
              i32.const 4133620
              i32.const 0
              i32.store
              local.get $l2
              local.get $p1
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
              i32.eq
              br_if $B9
            end
            local.get $l2
            i32.load8_u offset=27
            if $I19
              local.get $l2
              i32.load offset=28
              call $f52104
            end
            local.get $p1
            br_if $B7
            local.get $l2
            i32.const 32
            i32.add
            global.set $g0
            return
          end
          call $env.__cxa_find_matching_catch_2
          local.set $p1
          call $env.getTempRet0
          drop
        end
        i32.const 4133620
        i32.const 0
        i32.store
        i32.const 10529
        local.get $l2
        i32.const 8
        i32.add
        call $env.invoke_ii
        drop
        i32.const 4133620
        i32.load
        local.set $l2
        i32.const 4133620
        i32.const 0
        i32.store
        local.get $l2
        i32.const 1
        i32.ne
        br_if $B6
        i32.const 0
        call $env.__cxa_find_matching_catch_3
        drop
        call $env.getTempRet0
        drop
        call $f640
        unreachable
      end
      local.get $p1
      call $f1089
      unreachable
    end
    local.get $p1
    call $env.__resumeException
    unreachable)
