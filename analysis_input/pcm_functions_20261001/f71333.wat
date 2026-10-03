  (func $f71333 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32)
    local.get $p0
    block $B0 (result i32)
      local.get $p0
      i32.load offset=28
      local.tee $l12
      local.get $p0
      i32.load offset=24
      i32.ne
      if $I1
        local.get $p0
        i32.load offset=20
        local.set $l2
        local.get $l12
        br $B0
      end
      block $B2 (result i32)
        i32.const 0
        local.get $l12
        i32.const 1
        i32.add
        local.tee $l5
        local.get $l12
        i32.lt_u
        br_if $B2
        drop
        i32.const 4
        local.set $l14
        local.get $p0
        i32.const 4
        i32.add
        local.get $l5
        i32.const 4
        i32.le_u
        br_if $B2
        drop
        block $B3 (result i32)
          local.get $p0
          i32.load offset=40
          local.set $l5
          block $B4
            block $B5
              block $B6
                block $B7
                  local.get $l12
                  i32.const 1
                  i32.shr_u
                  local.get $l12
                  i32.or
                  local.tee $l2
                  i32.const 2
                  i32.shr_u
                  local.get $l2
                  i32.or
                  local.tee $l2
                  i32.const 4
                  i32.shr_u
                  local.get $l2
                  i32.or
                  local.tee $l2
                  i32.const 8
                  i32.shr_u
                  local.get $l2
                  i32.or
                  local.tee $l2
                  i32.const 16
                  i32.shr_u
                  local.get $l2
                  i32.or
                  i32.const 1
                  i32.add
                  local.tee $l14
                  local.tee $l2
                  i32.const 8
                  i32.sub
                  br_table $B7 $B4 $B4 $B4 $B4 $B4 $B4 $B4 $B6 $B4 $B4 $B4 $B4 $B4 $B4 $B4 $B4 $B4 $B4 $B4 $B4 $B4 $B4 $B4 $B5 $B4
                end
                local.get $l5
                i32.load offset=388
                local.tee $l2
                i32.eqz
                if $I8
                  global.get $g0
                  i32.const 16
                  i32.sub
                  local.tee $l9
                  global.set $g0
                  local.get $l9
                  local.get $l5
                  i32.const 100
                  i32.add
                  local.tee $l6
                  i32.load offset=284
                  local.tee $l2
                  if $I9 (result i32)
                    call $f69753
                    local.tee $l7
                    local.get $l2
                    i32.const 3160893
                    i32.const 3158199
                    i32.const 4700888
                    i32.load
                    local.tee $l2
                    local.get $l2
                    i32.load
                    i32.load offset=20
                    call_indirect $__indirect_function_table (type $t5)
                    select
                    i32.const 3160660
                    i32.const 180
                    local.get $l7
                    i32.load
                    i32.load offset=8
                    call_indirect $__indirect_function_table (type $t9)
                  else
                    i32.const 0
                  end
                  local.tee $l8
                  i32.store offset=12
                  block $B10
                    local.get $l6
                    i32.load offset=268
                    local.tee $l2
                    local.get $l6
                    i32.load offset=272
                    i32.const 2147483647
                    i32.and
                    i32.ge_u
                    if $I11
                      local.get $l9
                      i32.const 12
                      i32.add
                      local.set $l13
                      block $B12 (result i32)
                        i32.const 0
                        local.get $l6
                        i32.const 4
                        i32.add
                        local.tee $l3
                        i32.load offset=268
                        i32.const 2147483647
                        i32.and
                        local.tee $l4
                        i32.const 1
                        i32.shl
                        i32.const 1
                        local.get $l4
                        select
                        local.tee $l11
                        i32.eqz
                        br_if $B12
                        drop
                        block $B13
                          local.get $l11
                          i32.const 2
                          i32.shl
                          local.tee $l4
                          i32.const 256
                          i32.gt_u
                          br_if $B13
                          local.get $l3
                          i32.load8_u offset=256
                          br_if $B13
                          local.get $l3
                          i32.const 1
                          i32.store8 offset=256
                          local.get $l3
                          br $B12
                        end
                        i32.const 0
                        local.get $l4
                        i32.eqz
                        br_if $B12
                        drop
                        call $f69753
                        local.tee $l2
                        local.get $l4
                        i32.const 3160893
                        i32.const 3158199
                        i32.const 4700888
                        i32.load
                        local.tee $l10
                        local.get $l10
                        i32.load
                        i32.load offset=20
                        call_indirect $__indirect_function_table (type $t5)
                        select
                        i32.const 3158349
                        i32.const 553
                        local.get $l2
                        i32.load
                        i32.load offset=8
                        call_indirect $__indirect_function_table (type $t9)
                      end
                      local.set $l7
                      local.get $l7
                      local.get $l3
                      i32.load offset=264
                      local.tee $l4
                      i32.const 0
                      i32.gt_s
                      if $I14 (result i32)
                        local.get $l7
                        local.get $l4
                        i32.const 2
                        i32.shl
                        i32.add
                        local.set $l10
                        local.get $l3
                        i32.load offset=260
                        local.set $l4
                        local.get $l7
                        local.set $l2
                        loop $L15
                          local.get $l2
                          local.get $l4
                          i32.load
                          i32.store
                          local.get $l4
                          i32.const 4
                          i32.add
                          local.set $l4
                          local.get $l2
                          i32.const 4
                          i32.add
                          local.tee $l2
                          local.get $l10
                          i32.lt_u
                          br_if $L15
                        end
                        local.get $l3
                        i32.load offset=264
                      else
                        local.get $l4
                      end
                      i32.const 2
                      i32.shl
                      i32.add
                      local.get $l13
                      i32.load
                      i32.store
                      block $B16
                        local.get $l3
                        i32.load offset=268
                        i32.const 0
                        i32.lt_s
                        br_if $B16
                        local.get $l3
                        i32.load offset=260
                        local.tee $l4
                        local.get $l3
                        i32.eq
                        if $I17
                          local.get $l3
                          i32.const 0
                          i32.store8 offset=256
                          br $B16
                        end
                        local.get $l4
                        i32.eqz
                        br_if $B16
                        call $f69753
                        local.tee $l2
                        local.get $l4
                        local.get $l2
                        i32.load
                        i32.load offset=12
                        call_indirect $__indirect_function_table (type $t1)
                      end
                      local.get $l3
                      local.get $l11
                      i32.store offset=268
                      local.get $l3
                      local.get $l7
                      i32.store offset=260
                      local.get $l3
                      local.get $l3
                      i32.load offset=264
                      i32.const 1
                      i32.add
                      i32.store offset=264
                      br $B10
                    end
                    local.get $l6
                    i32.load offset=264
                    local.get $l2
                    i32.const 2
                    i32.shl
                    i32.add
                    local.get $l8
                    i32.store
                    local.get $l6
                    local.get $l6
                    i32.load offset=268
                    i32.const 1
                    i32.add
                    i32.store offset=268
                  end
                  local.get $l8
                  local.get $l8
                  local.get $l6
                  i32.load offset=276
                  i32.const 5
                  i32.shl
                  i32.add
                  i32.const 32
                  i32.sub
                  local.tee $l2
                  i32.le_u
                  if $I18
                    local.get $l6
                    i32.load offset=288
                    local.set $l7
                    loop $L19
                      local.get $l2
                      local.get $l7
                      i32.store
                      local.get $l6
                      local.get $l2
                      i32.store offset=288
                      local.get $l2
                      local.set $l7
                      local.get $l2
                      i32.const 32
                      i32.sub
                      local.tee $l2
                      local.get $l8
                      i32.ge_u
                      br_if $L19
                    end
                  end
                  local.get $l9
                  i32.const 16
                  i32.add
                  global.set $g0
                  local.get $l5
                  i32.load offset=388
                  local.set $l2
                end
                local.get $l5
                local.get $l2
                i32.load
                i32.store offset=388
                local.get $l5
                i32.const 380
                i32.add
                local.tee $l5
                local.get $l5
                i32.load
                i32.const 1
                i32.add
                i32.store
                local.get $l2
                br $B3
              end
              local.get $l5
              i32.load offset=680
              local.tee $l2
              i32.eqz
              if $I20
                global.get $g0
                i32.const 16
                i32.sub
                local.tee $l9
                global.set $g0
                local.get $l9
                local.get $l5
                i32.const 392
                i32.add
                local.tee $l6
                i32.load offset=284
                local.tee $l2
                if $I21 (result i32)
                  call $f69753
                  local.tee $l7
                  local.get $l2
                  i32.const 3161035
                  i32.const 3158199
                  i32.const 4700888
                  i32.load
                  local.tee $l2
                  local.get $l2
                  i32.load
                  i32.load offset=20
                  call_indirect $__indirect_function_table (type $t5)
                  select
                  i32.const 3160660
                  i32.const 180
                  local.get $l7
                  i32.load
                  i32.load offset=8
                  call_indirect $__indirect_function_table (type $t9)
                else
                  i32.const 0
                end
                local.tee $l8
                i32.store offset=12
                block $B22
                  local.get $l6
                  i32.load offset=268
                  local.tee $l2
                  local.get $l6
                  i32.load offset=272
                  i32.const 2147483647
                  i32.and
                  i32.ge_u
                  if $I23
                    local.get $l9
                    i32.const 12
                    i32.add
                    local.set $l13
                    block $B24 (result i32)
                      i32.const 0
                      local.get $l6
                      i32.const 4
                      i32.add
                      local.tee $l3
                      i32.load offset=268
                      i32.const 2147483647
                      i32.and
                      local.tee $l4
                      i32.const 1
                      i32.shl
                      i32.const 1
                      local.get $l4
                      select
                      local.tee $l11
                      i32.eqz
                      br_if $B24
                      drop
                      block $B25
                        local.get $l11
                        i32.const 2
                        i32.shl
                        local.tee $l4
                        i32.const 256
                        i32.gt_u
                        br_if $B25
                        local.get $l3
                        i32.load8_u offset=256
                        br_if $B25
                        local.get $l3
                        i32.const 1
                        i32.store8 offset=256
                        local.get $l3
                        br $B24
                      end
                      i32.const 0
                      local.get $l4
                      i32.eqz
                      br_if $B24
                      drop
                      call $f69753
                      local.tee $l2
                      local.get $l4
                      i32.const 3161035
                      i32.const 3158199
                      i32.const 4700888
                      i32.load
                      local.tee $l10
                      local.get $l10
                      i32.load
                      i32.load offset=20
                      call_indirect $__indirect_function_table (type $t5)
                      select
                      i32.const 3158349
                      i32.const 553
                      local.get $l2
                      i32.load
                      i32.load offset=8
                      call_indirect $__indirect_function_table (type $t9)
                    end
                    local.set $l7
                    local.get $l7
                    local.get $l3
                    i32.load offset=264
                    local.tee $l4
                    i32.const 0
                    i32.gt_s
                    if $I26 (result i32)
                      local.get $l7
                      local.get $l4
                      i32.const 2
                      i32.shl
                      i32.add
                      local.set $l10
                      local.get $l3
                      i32.load offset=260
                      local.set $l4
                      local.get $l7
                      local.set $l2
                      loop $L27
                        local.get $l2
                        local.get $l4
                        i32.load
                        i32.store
                        local.get $l4
                        i32.const 4
                        i32.add
                        local.set $l4
                        local.get $l2
                        i32.const 4
                        i32.add
                        local.tee $l2
                        local.get $l10
                        i32.lt_u
                        br_if $L27
                      end
                      local.get $l3
                      i32.load offset=264
                    else
                      local.get $l4
                    end
                    i32.const 2
                    i32.shl
                    i32.add
                    local.get $l13
                    i32.load
                    i32.store
                    block $B28
                      local.get $l3
                      i32.load offset=268
                      i32.const 0
                      i32.lt_s
                      br_if $B28
                      local.get $l3
                      i32.load offset=260
                      local.tee $l4
                      local.get $l3
                      i32.eq
                      if $I29
                        local.get $l3
                        i32.const 0
                        i32.store8 offset=256
                        br $B28
                      end
                      local.get $l4
                      i32.eqz
                      br_if $B28
                      call $f69753
                      local.tee $l2
                      local.get $l4
                      local.get $l2
                      i32.load
                      i32.load offset=12
                      call_indirect $__indirect_function_table (type $t1)
                    end
                    local.get $l3
                    local.get $l11
                    i32.store offset=268
                    local.get $l3
                    local.get $l7
                    i32.store offset=260
                    local.get $l3
                    local.get $l3
                    i32.load offset=264
                    i32.const 1
                    i32.add
                    i32.store offset=264
                    br $B22
                  end
                  local.get $l6
                  i32.load offset=264
                  local.get $l2
                  i32.const 2
                  i32.shl
                  i32.add
                  local.get $l8
                  i32.store
                  local.get $l6
                  local.get $l6
                  i32.load offset=268
                  i32.const 1
                  i32.add
                  i32.store offset=268
                end
                local.get $l8
                local.get $l8
                local.get $l6
                i32.load offset=276
                i32.const 6
                i32.shl
                i32.add
                i32.const -64
                i32.add
                local.tee $l2
                i32.le_u
                if $I30
                  local.get $l6
                  i32.load offset=288
                  local.set $l7
                  loop $L31
                    local.get $l2
                    local.get $l7
                    i32.store
                    local.get $l6
                    local.get $l2
                    i32.store offset=288
                    local.get $l2
                    local.set $l7
                    local.get $l2
                    i32.const -64
                    i32.add
                    local.tee $l2
                    local.get $l8
                    i32.ge_u
                    br_if $L31
                  end
                end
                local.get $l9
                i32.const 16
                i32.add
                global.set $g0
                local.get $l5
                i32.load offset=680
                local.set $l2
              end
              local.get $l5
              local.get $l2
              i32.load
              i32.store offset=680
              local.get $l5
              i32.const 672
              i32.add
              local.tee $l5
              local.get $l5
              i32.load
              i32.const 1
              i32.add
              i32.store
              local.get $l2
              br $B3
            end
            local.get $l5
            i32.load offset=972
            local.tee $l2
            i32.eqz
            if $I32
              global.get $g0
              i32.const 16
              i32.sub
              local.tee $l9
              global.set $g0
              local.get $l9
              local.get $l5
              i32.const 684
              i32.add
              local.tee $l6
              i32.load offset=284
              local.tee $l2
              if $I33 (result i32)
                call $f69753
                local.tee $l7
                local.get $l2
                i32.const 3161179
                i32.const 3158199
                i32.const 4700888
                i32.load
                local.tee $l2
                local.get $l2
                i32.load
                i32.load offset=20
                call_indirect $__indirect_function_table (type $t5)
                select
                i32.const 3160660
                i32.const 180
                local.get $l7
                i32.load
                i32.load offset=8
                call_indirect $__indirect_function_table (type $t9)
              else
                i32.const 0
              end
              local.tee $l8
              i32.store offset=12
              block $B34
                local.get $l6
                i32.load offset=268
                local.tee $l2
                local.get $l6
                i32.load offset=272
                i32.const 2147483647
                i32.and
                i32.ge_u
                if $I35
                  local.get $l9
                  i32.const 12
                  i32.add
                  local.set $l13
                  block $B36 (result i32)
                    i32.const 0
                    local.get $l6
                    i32.const 4
                    i32.add
                    local.tee $l3
                    i32.load offset=268
                    i32.const 2147483647
                    i32.and
                    local.tee $l4
                    i32.const 1
                    i32.shl
                    i32.const 1
                    local.get $l4
                    select
                    local.tee $l11
                    i32.eqz
                    br_if $B36
                    drop
                    block $B37
                      local.get $l11
                      i32.const 2
                      i32.shl
                      local.tee $l4
                      i32.const 256
                      i32.gt_u
                      br_if $B37
                      local.get $l3
                      i32.load8_u offset=256
                      br_if $B37
                      local.get $l3
                      i32.const 1
                      i32.store8 offset=256
                      local.get $l3
                      br $B36
                    end
                    i32.const 0
                    local.get $l4
                    i32.eqz
                    br_if $B36
                    drop
                    call $f69753
                    local.tee $l2
                    local.get $l4
                    i32.const 3161179
                    i32.const 3158199
                    i32.const 4700888
                    i32.load
                    local.tee $l10
                    local.get $l10
                    i32.load
                    i32.load offset=20
                    call_indirect $__indirect_function_table (type $t5)
                    select
                    i32.const 3158349
                    i32.const 553
                    local.get $l2
                    i32.load
                    i32.load offset=8
                    call_indirect $__indirect_function_table (type $t9)
                  end
                  local.set $l7
                  local.get $l7
                  local.get $l3
                  i32.load offset=264
                  local.tee $l4
                  i32.const 0
                  i32.gt_s
                  if $I38 (result i32)
                    local.get $l7
                    local.get $l4
                    i32.const 2
                    i32.shl
                    i32.add
                    local.set $l10
                    local.get $l3
                    i32.load offset=260
                    local.set $l4
                    local.get $l7
                    local.set $l2
                    loop $L39
                      local.get $l2
                      local.get $l4
                      i32.load
                      i32.store
                      local.get $l4
                      i32.const 4
                      i32.add
                      local.set $l4
                      local.get $l2
                      i32.const 4
                      i32.add
                      local.tee $l2
                      local.get $l10
                      i32.lt_u
                      br_if $L39
                    end
                    local.get $l3
                    i32.load offset=264
                  else
                    local.get $l4
                  end
                  i32.const 2
                  i32.shl
                  i32.add
                  local.get $l13
                  i32.load
                  i32.store
                  block $B40
                    local.get $l3
                    i32.load offset=268
                    i32.const 0
                    i32.lt_s
                    br_if $B40
                    local.get $l3
                    i32.load offset=260
                    local.tee $l4
                    local.get $l3
                    i32.eq
                    if $I41
                      local.get $l3
                      i32.const 0
                      i32.store8 offset=256
                      br $B40
                    end
                    local.get $l4
                    i32.eqz
                    br_if $B40
                    call $f69753
                    local.tee $l2
                    local.get $l4
                    local.get $l2
                    i32.load
                    i32.load offset=12
                    call_indirect $__indirect_function_table (type $t1)
                  end
                  local.get $l3
                  local.get $l11
                  i32.store offset=268
                  local.get $l3
                  local.get $l7
                  i32.store offset=260
                  local.get $l3
                  local.get $l3
                  i32.load offset=264
                  i32.const 1
                  i32.add
                  i32.store offset=264
                  br $B34
                end
                local.get $l6
                i32.load offset=264
                local.get $l2
                i32.const 2
                i32.shl
                i32.add
                local.get $l8
                i32.store
                local.get $l6
                local.get $l6
                i32.load offset=268
                i32.const 1
                i32.add
                i32.store offset=268
              end
              local.get $l8
              local.get $l8
              local.get $l6
              i32.load offset=276
              i32.const 7
              i32.shl
              i32.add
              i32.const 128
              i32.sub
              local.tee $l2
              i32.le_u
              if $I42
                local.get $l6
                i32.load offset=288
                local.set $l7
                loop $L43
                  local.get $l2
                  local.get $l7
                  i32.store
                  local.get $l6
                  local.get $l2
                  i32.store offset=288
                  local.get $l2
                  local.set $l7
                  local.get $l2
                  i32.const 128
                  i32.sub
                  local.tee $l2
                  local.get $l8
                  i32.ge_u
                  br_if $L43
                end
              end
              local.get $l9
              i32.const 16
              i32.add
              global.set $g0
              local.get $l5
              i32.load offset=972
              local.set $l2
            end
            local.get $l5
            local.get $l2
            i32.load
            i32.store offset=972
            local.get $l5
            i32.const 964
            i32.add
            local.tee $l5
            local.get $l5
            i32.load
            i32.const 1
            i32.add
            i32.store
            local.get $l2
            br $B3
          end
          i32.const 0
          local.get $l2
          i32.const 2
          i32.shl
          local.tee $l5
          i32.eqz
          br_if $B3
          drop
          call $f69753
          local.tee $l2
          local.get $l5
          i32.const 3158048
          i32.const 3157633
          i32.const 1341
          local.get $l2
          i32.load
          i32.load offset=8
          call_indirect $__indirect_function_table (type $t9)
        end
      end
      local.set $l2
      block $B44
        local.get $p0
        i32.load offset=20
        local.tee $l5
        i32.eqz
        br_if $B44
        local.get $l2
        local.get $l5
        local.get $l12
        i32.const 2
        i32.shl
        call $f483
        drop
        local.get $p0
        i32.load offset=20
        local.tee $l5
        local.get $p0
        i32.const 4
        i32.add
        i32.eq
        br_if $B44
        local.get $p0
        i32.load offset=40
        local.get $l5
        local.get $p0
        i32.load offset=24
        call $f71331
      end
      local.get $p0
      local.get $l2
      i32.store offset=20
      local.get $p0
      local.get $l14
      i32.store offset=24
      local.get $p0
      i32.load offset=28
    end
    local.tee $l14
    i32.const 1
    i32.add
    i32.store offset=28
    local.get $l2
    local.get $l14
    i32.const 2
    i32.shl
    i32.add
    local.get $p1
    i32.store
    local.get $p1
    i32.const 12
    i32.const 16
    local.get $p1
    i32.load
    local.get $p0
    i32.eq
    select
    i32.add
    local.get $l12
    i32.store)