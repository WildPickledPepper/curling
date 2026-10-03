  (func $f71764 (type $t0) (param $p0 i32) (param $p1 i32) (result i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32)
    block $B0
      local.get $p0
      i32.load8_u offset=338
      i32.eqz
      br_if $B0
      block $B1
        block $B2
          block $B3
            block $B4
              block $B5
                block $B6
                  block $B7
                    block $B8
                      block $B9
                        local.get $p0
                        i32.load offset=268
                        br_table $B9 $B8 $B7 $B6 $B5 $B4 $B3
                      end
                      local.get $p1
                      i32.eqz
                      br_if $B0
                      local.get $p0
                      local.get $p0
                      i32.load
                      i32.load offset=76
                      call_indirect $__indirect_function_table (type $t5)
                      br_if $B2
                      br $B0
                    end
                    local.get $p0
                    i32.load offset=32
                    local.get $p0
                    i32.const 8
                    i32.add
                    local.get $p0
                    i32.const 24
                    i32.add
                    i32.const 0
                    i32.const 0
                    call $f71765
                    drop
                    local.get $p0
                    i32.const 0
                    i32.store offset=44
                    local.get $p0
                    i32.const 2
                    i32.store offset=268
                    local.get $p0
                    i32.load offset=12
                    local.tee $l5
                    local.set $l4
                    loop $L10
                      local.get $l3
                      local.tee $l2
                      i32.const 31
                      i32.le_u
                      if $I11
                        local.get $l2
                        i32.const 1
                        i32.add
                        local.set $l3
                        local.get $l4
                        i32.const 1
                        i32.shr_u
                        local.tee $l4
                        br_if $L10
                      end
                    end
                    local.get $l2
                    i32.const -1
                    local.get $l2
                    i32.const 32
                    i32.lt_u
                    select
                    local.get $l5
                    i32.mul
                    local.set $l2
                    block $B12 (result i32)
                      block $B13
                        local.get $l2
                        local.get $p0
                        i32.load offset=4
                        local.tee $l3
                        if $I14 (result i32)
                          local.get $l3
                          i32.load offset=44
                        else
                          i32.const 0
                        end
                        local.tee $l3
                        i32.const 1
                        i32.shl
                        i32.gt_u
                        br_if $B13
                        local.get $l2
                        local.get $l3
                        i32.const 1
                        i32.shr_u
                        i32.lt_u
                        br_if $B13
                        local.get $l3
                        local.set $l2
                        local.get $p0
                        i32.load offset=280
                        local.get $l5
                        i32.mul
                        br $B12
                      end
                      local.get $p0
                      i32.const 0
                      i32.store offset=280
                      i32.const 0
                    end
                    local.set $l4
                    local.get $p0
                    local.get $l2
                    local.get $l4
                    i32.add
                    local.tee $l2
                    i32.const 0
                    local.get $l2
                    i32.const 0
                    i32.gt_s
                    select
                    i32.store offset=276
                    br $B3
                  end
                  local.get $p0
                  local.get $p0
                  i32.load offset=44
                  i32.const 1
                  i32.add
                  i32.store offset=44
                  local.get $p0
                  i32.load offset=32
                  local.get $p0
                  i32.const 8
                  i32.add
                  local.get $p0
                  i32.const 24
                  i32.add
                  i32.const 1
                  local.get $p0
                  i32.load offset=276
                  local.get $p0
                  i32.load offset=272
                  i32.div_u
                  i32.const 1
                  i32.add
                  call $f71765
                  br_if $B3
                  local.get $p0
                  i32.const 3
                  i32.store offset=268
                  br $B3
                end
                local.get $p0
                i32.const 4
                i32.store offset=268
                local.get $p0
                local.get $p0
                i32.load offset=44
                i32.const 1
                i32.add
                i32.store offset=44
                local.get $p0
                i32.load offset=344
                i32.eqz
                br_if $B3
                local.get $p0
                i32.const 324
                i32.add
                local.tee $l3
                local.get $p0
                i32.load offset=40
                local.tee $l2
                local.get $p0
                i32.load offset=284
                local.tee $l4
                local.get $l2
                local.get $l4
                i32.gt_u
                select
                local.get $p0
                i32.load offset=32
                call $f71832
                local.get $p0
                i32.load offset=344
                i32.const 0
                i32.gt_s
                if $I15
                  local.get $p0
                  i32.load offset=340
                  local.set $l2
                  loop $L16
                    local.get $l3
                    local.get $l2
                    i32.load
                    local.get $l2
                    i32.load offset=4
                    local.get $p0
                    i32.load offset=32
                    call $f71833
                    local.get $l2
                    i32.const 8
                    i32.add
                    local.tee $l2
                    local.get $p0
                    i32.load offset=340
                    local.get $p0
                    i32.load offset=344
                    i32.const 3
                    i32.shl
                    i32.add
                    i32.lt_u
                    br_if $L16
                  end
                end
                local.get $p0
                i32.const 0
                i32.store offset=344
                br $B3
              end
              local.get $p0
              i32.const 5
              i32.store offset=268
              local.get $p0
              local.get $p0
              i32.load offset=44
              i32.const 1
              i32.add
              i32.store offset=44
              local.get $p0
              i32.load offset=32
              local.tee $l2
              i32.load offset=40
              local.tee $l4
              i32.eqz
              br_if $B3
              local.get $p0
              i32.load offset=292
              local.set $l5
              local.get $l2
              i32.load
              local.set $l6
              local.get $l2
              i32.load offset=8
              local.tee $l3
              local.get $l4
              i32.const 1
              i32.sub
              local.tee $l2
              i32.const 28
              i32.mul
              i32.add
              local.set $l4
              local.get $l2
              if $I17 (result i32)
                loop $L18
                  local.get $l4
                  local.get $l5
                  local.get $l6
                  local.get $l3
                  call $f71759
                  local.get $l3
                  local.get $l2
                  i32.const 1
                  i32.sub
                  local.tee $l2
                  i32.const 28
                  i32.mul
                  i32.add
                  local.set $l4
                  local.get $l2
                  br_if $L18
                end
                local.get $l3
              else
                local.get $l4
              end
              local.get $l5
              local.get $l6
              local.get $l3
              call $f71759
              br $B3
            end
            local.get $p0
            i32.const 6
            i32.store offset=268
          end
          local.get $p1
          i32.eqz
          br_if $B1
        end
        local.get $p0
        i32.const 1
        i32.store8 offset=337
      end
      local.get $p0
      i32.load offset=268
      i32.const 6
      i32.eq
      local.set $l2
    end
    local.get $l2)