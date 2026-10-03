  (func $f72142 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l2
    global.set $g0
    local.get $p1
    i32.load offset=80
    local.set $l5
    local.get $l2
    i32.const 0
    i32.store offset=8
    local.get $l2
    i64.const 0
    i64.store
    block $B0
      local.get $l5
      i32.eqz
      br_if $B0
      local.get $l2
      local.get $l5
      call $f69863
      loop $L1
        block $B2
          block $B3
            block $B4
              block $B5
                block $B6
                  block $B7
                    block $B8
                      local.get $p1
                      i32.load offset=48
                      local.get $l4
                      i32.const 4
                      i32.shl
                      i32.add
                      i32.load
                      local.tee $l3
                      i32.load16_u offset=4
                      i32.const 5
                      i32.sub
                      br_table $B8 $B7 $B2 $B2 $B2 $B4 $B6 $B5 $B2 $B2 $B2 $B3 $B2
                    end
                    local.get $l3
                    i32.load offset=40
                    br_if $B2
                    local.get $l2
                    local.get $l3
                    i32.store offset=12
                    local.get $l3
                    local.get $l3
                    i32.load
                    i32.load offset=72
                    call_indirect $__indirect_function_table (type $t5)
                    br_if $B2
                    local.get $l2
                    i32.load offset=4
                    local.tee $l6
                    local.get $l2
                    i32.load offset=8
                    i32.const 2147483647
                    i32.and
                    i32.ge_u
                    if $I9
                      local.get $l2
                      local.get $l2
                      i32.const 12
                      i32.add
                      call $f72072
                      br $B2
                    end
                    local.get $l2
                    i32.load
                    local.get $l6
                    i32.const 2
                    i32.shl
                    i32.add
                    local.get $l3
                    i32.store
                    local.get $l2
                    local.get $l2
                    i32.load offset=4
                    i32.const 1
                    i32.add
                    i32.store offset=4
                    br $B2
                  end
                  local.get $l3
                  i32.load offset=40
                  br_if $B2
                  local.get $l2
                  local.get $l3
                  i32.store offset=12
                  local.get $l3
                  local.get $l3
                  i32.load
                  i32.load offset=72
                  call_indirect $__indirect_function_table (type $t5)
                  br_if $B2
                  local.get $l2
                  i32.load offset=4
                  local.tee $l6
                  local.get $l2
                  i32.load offset=8
                  i32.const 2147483647
                  i32.and
                  i32.ge_u
                  if $I10
                    local.get $l2
                    local.get $l2
                    i32.const 12
                    i32.add
                    call $f72072
                    br $B2
                  end
                  local.get $l2
                  i32.load
                  local.get $l6
                  i32.const 2
                  i32.shl
                  i32.add
                  local.get $l3
                  i32.store
                  local.get $l2
                  local.get $l2
                  i32.load offset=4
                  i32.const 1
                  i32.add
                  i32.store offset=4
                  br $B2
                end
                local.get $l3
                local.get $l3
                i32.load
                i32.load offset=96
                call_indirect $__indirect_function_table (type $t5)
                br_if $B2
                local.get $p0
                local.get $l3
                local.get $p0
                i32.load
                i32.load offset=36
                call_indirect $__indirect_function_table (type $t1)
                br $B2
              end
              local.get $l3
              local.get $l3
              i32.load
              i32.load offset=96
              call_indirect $__indirect_function_table (type $t5)
              br_if $B2
              local.get $p0
              local.get $l3
              local.get $p0
              i32.load
              i32.load offset=36
              call_indirect $__indirect_function_table (type $t1)
              br $B2
            end
            local.get $p0
            local.get $l3
            local.get $p0
            i32.load
            i32.load offset=64
            call_indirect $__indirect_function_table (type $t1)
            br $B2
          end
          local.get $p0
          local.get $l3
          local.get $p0
          i32.load
          i32.load offset=52
          call_indirect $__indirect_function_table (type $t1)
        end
        local.get $l4
        i32.const 1
        i32.add
        local.tee $l4
        local.get $l5
        i32.ne
        br_if $L1
      end
      local.get $l2
      i32.load offset=4
      local.tee $l4
      i32.eqz
      br_if $B0
      local.get $p0
      local.get $l2
      i32.load
      local.get $l4
      i32.const 0
      call $f72122
    end
    block $B11
      local.get $l2
      i32.load offset=8
      local.tee $l4
      i32.const 0
      i32.lt_s
      br_if $B11
      local.get $l4
      i32.const 2147483647
      i32.and
      i32.eqz
      br_if $B11
      local.get $l2
      i32.load
      local.tee $l4
      i32.eqz
      br_if $B11
      call $f69753
      local.tee $l3
      local.get $l4
      local.get $l3
      i32.load
      i32.load offset=12
      call_indirect $__indirect_function_table (type $t1)
    end
    local.get $l2
    i32.const 16
    i32.add
    global.set $g0)