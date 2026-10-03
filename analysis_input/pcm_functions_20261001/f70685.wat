  (func $f70685 (type $t4) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32)
    (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 i32)
    global.get $g0
    i32.const 48
    i32.sub
    local.tee $l9
    global.set $g0
    local.get $l9
    local.get $p1
    i32.store offset=44
    local.get $p1
    i32.load8_u offset=47
    local.set $l5
    local.get $p1
    i32.load8_u offset=46
    local.set $l6
    local.get $l9
    i64.const 0
    i64.store offset=8
    local.get $p0
    i32.load offset=4
    local.set $l10
    local.get $l9
    i32.const 8
    i32.add
    local.set $l12
    block $B0
      local.get $p1
      i32.eqz
      br_if $B0
      local.get $l10
      i32.load8_u offset=1812
      i32.eqz
      br_if $B0
      local.get $l6
      i32.const 7
      i32.mul
      local.get $l5
      i32.add
      i32.const 4118416
      i32.add
      i32.load8_u
      if $I1
        block $B2
          local.get $l6
          i32.const 4
          i32.gt_u
          br_if $B2
          local.get $l5
          i32.const 4
          i32.gt_u
          br_if $B2
          block $B3
            local.get $l6
            i32.const 0
            local.get $l5
            select
            i32.eqz
            if $I4
              local.get $l10
              i32.load offset=932
              local.tee $l4
              i32.eqz
              if $I5
                global.get $g0
                i32.const 16
                i32.sub
                local.tee $l14
                global.set $g0
                local.get $l14
                local.get $l10
                i32.const 644
                i32.add
                local.tee $l5
                i32.load offset=284
                local.tee $l4
                if $I6 (result i32)
                  call $f69753
                  local.tee $l6
                  local.get $l4
                  i32.const 3134579
                  i32.const 3134052
                  i32.const 4700888
                  i32.load
                  local.tee $l4
                  local.get $l4
                  i32.load
                  i32.load offset=20
                  call_indirect $__indirect_function_table (type $t5)
                  select
                  i32.const 3138161
                  i32.const 180
                  local.get $l6
                  i32.load
                  i32.load offset=8
                  call_indirect $__indirect_function_table (type $t9)
                else
                  i32.const 0
                end
                local.tee $l13
                i32.store offset=12
                block $B7
                  local.get $l5
                  i32.load offset=268
                  local.tee $l4
                  local.get $l5
                  i32.load offset=272
                  i32.const 2147483647
                  i32.and
                  i32.ge_u
                  if $I8
                    local.get $l14
                    i32.const 12
                    i32.add
                    local.set $l11
                    block $B9 (result i32)
                      i32.const 0
                      local.get $l5
                      i32.const 4
                      i32.add
                      local.tee $l7
                      i32.load offset=268
                      i32.const 2147483647
                      i32.and
                      local.tee $l8
                      i32.const 1
                      i32.shl
                      i32.const 1
                      local.get $l8
                      select
                      local.tee $l16
                      i32.eqz
                      br_if $B9
                      drop
                      block $B10
                        local.get $l16
                        i32.const 2
                        i32.shl
                        local.tee $l8
                        i32.const 256
                        i32.gt_u
                        br_if $B10
                        local.get $l7
                        i32.load8_u offset=256
                        br_if $B10
                        local.get $l7
                        i32.const 1
                        i32.store8 offset=256
                        local.get $l7
                        br $B9
                      end
                      i32.const 0
                      local.get $l8
                      i32.eqz
                      br_if $B9
                      drop
                      call $f69753
                      local.tee $l4
                      local.get $l8
                      i32.const 3134579
                      i32.const 3134052
                      i32.const 4700888
                      i32.load
                      local.tee $l15
                      local.get $l15
                      i32.load
                      i32.load offset=20
                      call_indirect $__indirect_function_table (type $t5)
                      select
                      i32.const 3134537
                      i32.const 553
                      local.get $l4
                      i32.load
                      i32.load offset=8
                      call_indirect $__indirect_function_table (type $t9)
                    end
                    local.set $l6
                    local.get $l6
                    local.get $l7
                    i32.load offset=264
                    local.tee $l8
                    i32.const 0
                    i32.gt_s
                    if $I11 (result i32)
                      local.get $l6
                      local.get $l8
                      i32.const 2
                      i32.shl
                      i32.add
                      local.set $l15
                      local.get $l7
                      i32.load offset=260
                      local.set $l8
                      local.get $l6
                      local.set $l4
                      loop $L12
                        local.get $l4
                        local.get $l8
                        i32.load
                        i32.store
                        local.get $l8
                        i32.const 4
                        i32.add
                        local.set $l8
                        local.get $l4
                        i32.const 4
                        i32.add
                        local.tee $l4
                        local.get $l15
                        i32.lt_u
                        br_if $L12
                      end
                      local.get $l7
                      i32.load offset=264
                    else
                      local.get $l8
                    end
                    i32.const 2
                    i32.shl
                    i32.add
                    local.get $l11
                    i32.load
                    i32.store
                    block $B13
                      local.get $l7
                      i32.load offset=268
                      i32.const 0
                      i32.lt_s
                      br_if $B13
                      local.get $l7
                      i32.load offset=260
                      local.tee $l8
                      local.get $l7
                      i32.eq
                      if $I14
                        local.get $l7
                        i32.const 0
                        i32.store8 offset=256
                        br $B13
                      end
                      local.get $l8
                      i32.eqz
                      br_if $B13
                      call $f69753
                      local.tee $l4
                      local.get $l8
                      local.get $l4
                      i32.load
                      i32.load offset=12
                      call_indirect $__indirect_function_table (type $t1)
                    end
                    local.get $l7
                    local.get $l16
                    i32.store offset=268
                    local.get $l7
                    local.get $l6
                    i32.store offset=260
                    local.get $l7
                    local.get $l7
                    i32.load offset=264
                    i32.const 1
                    i32.add
                    i32.store offset=264
                    br $B7
                  end
                  local.get $l5
                  i32.load offset=264
                  local.get $l4
                  i32.const 2
                  i32.shl
                  i32.add
                  local.get $l13
                  i32.store
                  local.get $l5
                  local.get $l5
                  i32.load offset=268
                  i32.const 1
                  i32.add
                  i32.store offset=268
                end
                local.get $l13
                local.get $l13
                local.get $l5
                i32.load offset=276
                i32.const 7
                i32.shl
                i32.add
                i32.const 128
                i32.sub
                local.tee $l4
                i32.le_u
                if $I15
                  local.get $l5
                  i32.load offset=288
                  local.set $l6
                  loop $L16
                    local.get $l4
                    local.get $l6
                    i32.store
                    local.get $l5
                    local.get $l4
                    i32.store offset=288
                    local.get $l4
                    local.set $l6
                    local.get $l4
                    i32.const 128
                    i32.sub
                    local.tee $l4
                    local.get $l13
                    i32.ge_u
                    br_if $L16
                  end
                end
                local.get $l14
                i32.const 16
                i32.add
                global.set $g0
                local.get $l10
                i32.load offset=932
                local.set $l4
              end
              local.get $l10
              local.get $l4
              i32.load
              i32.store offset=932
              local.get $l10
              i32.const 924
              i32.add
              local.tee $l10
              local.get $l10
              i32.load
              i32.const 1
              i32.add
              i32.store
              local.get $l4
              local.get $l4
              i32.const 80
              i32.add
              i32.store offset=76
              local.get $l4
              i32.const 0
              i32.store8 offset=66
              local.get $l4
              i32.const 256
              i32.store16 offset=64
              local.get $l4
              i64.const 2139095039
              i64.store offset=24
              local.get $l4
              i64.const 9187343237679939583
              i64.store offset=16
              local.get $l4
              i64.const 4575657221408423936
              i64.store offset=56
              local.get $l4
              i64.const 0
              i64.store offset=48
              local.get $l4
              i64.const 4575657221408423936
              i64.store offset=40
              local.get $l4
              i64.const 0
              i64.store offset=32
              local.get $l4
              i64.const 4575657221408423936
              i64.store offset=8
              local.get $l4
              i64.const 0
              i64.store
              local.get $l12
              local.get $l4
              i32.store
              local.get $l12
              local.get $l12
              i32.load8_u offset=7
              i32.const 1
              i32.or
              i32.store8 offset=7
              br $B3
            end
            local.get $l10
            i32.load offset=640
            local.tee $l4
            i32.eqz
            if $I17
              global.get $g0
              i32.const 16
              i32.sub
              local.tee $l14
              global.set $g0
              local.get $l14
              local.get $l10
              i32.const 352
              i32.add
              local.tee $l5
              i32.load offset=284
              local.tee $l4
              if $I18 (result i32)
                call $f69753
                local.tee $l6
                local.get $l4
                i32.const 3134737
                i32.const 3134052
                i32.const 4700888
                i32.load
                local.tee $l4
                local.get $l4
                i32.load
                i32.load offset=20
                call_indirect $__indirect_function_table (type $t5)
                select
                i32.const 3138161
                i32.const 180
                local.get $l6
                i32.load
                i32.load offset=8
                call_indirect $__indirect_function_table (type $t9)
              else
                i32.const 0
              end
              local.tee $l13
              i32.store offset=12
              block $B19
                local.get $l5
                i32.load offset=268
                local.tee $l4
                local.get $l5
                i32.load offset=272
                i32.const 2147483647
                i32.and
                i32.ge_u
                if $I20
                  local.get $l14
                  i32.const 12
                  i32.add
                  local.set $l11
                  block $B21 (result i32)
                    i32.const 0
                    local.get $l5
                    i32.const 4
                    i32.add
                    local.tee $l7
                    i32.load offset=268
                    i32.const 2147483647
                    i32.and
                    local.tee $l8
                    i32.const 1
                    i32.shl
                    i32.const 1
                    local.get $l8
                    select
                    local.tee $l16
                    i32.eqz
                    br_if $B21
                    drop
                    block $B22
                      local.get $l16
                      i32.const 2
                      i32.shl
                      local.tee $l8
                      i32.const 256
                      i32.gt_u
                      br_if $B22
                      local.get $l7
                      i32.load8_u offset=256
                      br_if $B22
                      local.get $l7
                      i32.const 1
                      i32.store8 offset=256
                      local.get $l7
                      br $B21
                    end
                    i32.const 0
                    local.get $l8
                    i32.eqz
                    br_if $B21
                    drop
                    call $f69753
                    local.tee $l4
                    local.get $l8
                    i32.const 3134737
                    i32.const 3134052
                    i32.const 4700888
                    i32.load
                    local.tee $l15
                    local.get $l15
                    i32.load
                    i32.load offset=20
                    call_indirect $__indirect_function_table (type $t5)
                    select
                    i32.const 3134537
                    i32.const 553
                    local.get $l4
                    i32.load
                    i32.load offset=8
                    call_indirect $__indirect_function_table (type $t9)
                  end
                  local.set $l6
                  local.get $l6
                  local.get $l7
                  i32.load offset=264
                  local.tee $l8
                  i32.const 0
                  i32.gt_s
                  if $I23 (result i32)
                    local.get $l6
                    local.get $l8
                    i32.const 2
                    i32.shl
                    i32.add
                    local.set $l15
                    local.get $l7
                    i32.load offset=260
                    local.set $l8
                    local.get $l6
                    local.set $l4
                    loop $L24
                      local.get $l4
                      local.get $l8
                      i32.load
                      i32.store
                      local.get $l8
                      i32.const 4
                      i32.add
                      local.set $l8
                      local.get $l4
                      i32.const 4
                      i32.add
                      local.tee $l4
                      local.get $l15
                      i32.lt_u
                      br_if $L24
                    end
                    local.get $l7
                    i32.load offset=264
                  else
                    local.get $l8
                  end
                  i32.const 2
                  i32.shl
                  i32.add
                  local.get $l11
                  i32.load
                  i32.store
                  block $B25
                    local.get $l7
                    i32.load offset=268
                    i32.const 0
                    i32.lt_s
                    br_if $B25
                    local.get $l7
                    i32.load offset=260
                    local.tee $l8
                    local.get $l7
                    i32.eq
                    if $I26
                      local.get $l7
                      i32.const 0
                      i32.store8 offset=256
                      br $B25
                    end
                    local.get $l8
                    i32.eqz
                    br_if $B25
                    call $f69753
                    local.tee $l4
                    local.get $l8
                    local.get $l4
                    i32.load
                    i32.load offset=12
                    call_indirect $__indirect_function_table (type $t1)
                  end
                  local.get $l7
                  local.get $l16
                  i32.store offset=268
                  local.get $l7
                  local.get $l6
                  i32.store offset=260
                  local.get $l7
                  local.get $l7
                  i32.load offset=264
                  i32.const 1
                  i32.add
                  i32.store offset=264
                  br $B19
                end
                local.get $l5
                i32.load offset=264
                local.get $l4
                i32.const 2
                i32.shl
                i32.add
                local.get $l13
                i32.store
                local.get $l5
                local.get $l5
                i32.load offset=268
                i32.const 1
                i32.add
                i32.store offset=268
              end
              local.get $l13
              local.get $l13
              local.get $l5
              i32.load offset=276
              i32.const 272
              i32.mul
              i32.add
              i32.const 272
              i32.sub
              local.tee $l4
              i32.le_u
              if $I27
                local.get $l5
                i32.load offset=288
                local.set $l6
                loop $L28
                  local.get $l4
                  local.get $l6
                  i32.store
                  local.get $l5
                  local.get $l4
                  i32.store offset=288
                  local.get $l4
                  local.set $l6
                  local.get $l4
                  i32.const 272
                  i32.sub
                  local.tee $l4
                  local.get $l13
                  i32.ge_u
                  br_if $L28
                end
              end
              local.get $l14
              i32.const 16
              i32.add
              global.set $g0
              local.get $l10
              i32.load offset=640
              local.set $l4
            end
            local.get $l10
            local.get $l4
            i32.load
            i32.store offset=640
            local.get $l10
            i32.const 632
            i32.add
            local.tee $l10
            local.get $l10
            i32.load
            i32.const 1
            i32.add
            i32.store
            local.get $l4
            local.get $l4
            i32.const 80
            i32.add
            i32.store offset=76
            local.get $l4
            i32.const 0
            i32.store8 offset=66
            local.get $l4
            i32.const 1024
            i32.store16 offset=64
            local.get $l4
            i64.const 2139095039
            i64.store offset=24
            local.get $l4
            i64.const 9187343237679939583
            i64.store offset=16
            local.get $l4
            i64.const 4575657221408423936
            i64.store offset=56
            local.get $l4
            i64.const 0
            i64.store offset=48
            local.get $l4
            i64.const 4575657221408423936
            i64.store offset=40
            local.get $l4
            i64.const 0
            i64.store offset=32
            local.get $l4
            i64.const 4575657221408423936
            i64.store offset=8
            local.get $l4
            i64.const 0
            i64.store
            local.get $l12
            local.get $l4
            i32.store
            local.get $l12
            local.get $l12
            i32.load8_u offset=7
            i32.const 1
            i32.or
            i32.store8 offset=7
          end
          local.get $l4
          i32.const 0
          i32.store8 offset=64
          local.get $l4
          i32.const 0
          i32.store8 offset=66
          local.get $l4
          i64.const 9187343237679939583
          i64.store offset=16
          local.get $l4
          i64.const 4575657221408423936
          i64.store offset=8
          local.get $l4
          i64.const 0
          i64.store
          local.get $l4
          i64.const 2139095039
          i64.store offset=24
          br $B0
        end
        local.get $l12
        i32.const 0
        i32.store
        local.get $l12
        local.get $l12
        i32.load8_u offset=7
        i32.const 3
        i32.or
        i32.store8 offset=7
        br $B0
      end
      local.get $l12
      i32.const 0
      i32.store8 offset=7
      local.get $l12
      i32.const 0
      i32.store
    end
    local.get $l9
    i64.const 0
    i64.store offset=24
    local.get $l9
    i64.const 0
    i64.store offset=16
    local.get $l9
    local.get $p3
    i32.store8 offset=29
    local.get $l9
    local.get $p1
    i32.load8_u offset=40
    i32.const 2
    i32.shl
    i32.const 8
    i32.and
    i32.const 2
    local.get $p2
    i32.const 31
    i32.shr_u
    local.get $p2
    i32.const 0
    i32.gt_s
    select
    i32.or
    i32.const 32
    i32.or
    i32.store8 offset=30
    local.get $p1
    i32.load8_u offset=43
    local.tee $p2
    i32.const 2
    i32.and
    if $I29
      local.get $p1
      local.get $p2
      i32.const 64
      i32.or
      i32.store8 offset=43
    end
    block $B30
      local.get $p0
      i32.load offset=72
      local.tee $p1
      local.get $p0
      i32.load offset=76
      i32.const 2147483647
      i32.and
      i32.ge_u
      if $I31
        local.get $l9
        i32.const 16
        i32.add
        local.set $l11
        i32.const 0
        local.set $p2
        block $B32
          local.get $p0
          i32.const 68
          i32.add
          local.tee $l5
          i32.load offset=8
          i32.const 2147483647
          i32.and
          local.tee $p3
          i32.const 1
          i32.shl
          i32.const 1
          local.get $p3
          select
          local.tee $l4
          i32.eqz
          br_if $B32
          local.get $l4
          i32.const 4
          i32.shl
          local.tee $p3
          i32.eqz
          br_if $B32
          call $f69753
          local.tee $p1
          local.get $p3
          i32.const 3139013
          i32.const 3134052
          i32.const 4700888
          i32.load
          local.tee $l6
          local.get $l6
          i32.load
          i32.load offset=20
          call_indirect $__indirect_function_table (type $t5)
          select
          i32.const 3134537
          i32.const 553
          local.get $p1
          i32.load
          i32.load offset=8
          call_indirect $__indirect_function_table (type $t9)
          local.set $p2
        end
        local.get $p2
        local.get $l5
        i32.load offset=4
        local.tee $p3
        i32.const 0
        i32.gt_s
        if $I33 (result i32)
          local.get $p2
          local.get $p3
          i32.const 4
          i32.shl
          i32.add
          local.set $l6
          local.get $l5
          i32.load
          local.set $p3
          local.get $p2
          local.set $p1
          loop $L34
            local.get $p1
            local.get $p3
            i64.load
            i64.store
            local.get $p1
            local.get $p3
            i64.load offset=8
            i64.store offset=8
            local.get $p3
            i32.const 16
            i32.add
            local.set $p3
            local.get $p1
            i32.const 16
            i32.add
            local.tee $p1
            local.get $l6
            i32.lt_u
            br_if $L34
          end
          local.get $l5
          i32.load offset=4
        else
          local.get $p3
        end
        i32.const 4
        i32.shl
        i32.add
        local.tee $p3
        local.get $l11
        i64.load
        i64.store
        local.get $p3
        local.get $l11
        i64.load offset=8
        i64.store offset=8
        block $B35
          local.get $l5
          i32.load offset=8
          i32.const 0
          i32.lt_s
          br_if $B35
          local.get $l5
          i32.load
          local.tee $p3
          i32.eqz
          br_if $B35
          call $f69753
          local.tee $p1
          local.get $p3
          local.get $p1
          i32.load
          i32.load offset=12
          call_indirect $__indirect_function_table (type $t1)
        end
        local.get $l5
        local.get $l4
        i32.store offset=8
        local.get $l5
        local.get $p2
        i32.store
        local.get $l5
        local.get $l5
        i32.load offset=4
        i32.const 1
        i32.add
        i32.store offset=4
        br $B30
      end
      local.get $p0
      i32.load offset=68
      local.get $p1
      i32.const 4
      i32.shl
      i32.add
      local.tee $p1
      local.get $l9
      i64.load offset=16
      i64.store
      local.get $p1
      local.get $l9
      i64.load offset=24
      i64.store offset=8
      local.get $p0
      local.get $p0
      i32.load offset=72
      i32.const 1
      i32.add
      i32.store offset=72
    end
    block $B36
      local.get $p0
      i32.load offset=96
      local.tee $p1
      local.get $p0
      i32.load offset=100
      i32.const 2147483647
      i32.and
      i32.ge_u
      if $I37
        local.get $l9
        i32.const 8
        i32.add
        local.set $l4
        i32.const 0
        local.set $p2
        block $B38
          local.get $p0
          i32.const 92
          i32.add
          local.tee $l5
          i32.load offset=8
          i32.const 2147483647
          i32.and
          local.tee $p3
          i32.const 1
          i32.shl
          i32.const 1
          local.get $p3
          select
          local.tee $l11
          i32.eqz
          br_if $B38
          local.get $l11
          i32.const 3
          i32.shl
          local.tee $p3
          i32.eqz
          br_if $B38
          call $f69753
          local.tee $p1
          local.get $p3
          i32.const 3139147
          i32.const 3134052
          i32.const 4700888
          i32.load
          local.tee $l6
          local.get $l6
          i32.load
          i32.load offset=20
          call_indirect $__indirect_function_table (type $t5)
          select
          i32.const 3134537
          i32.const 553
          local.get $p1
          i32.load
          i32.load offset=8
          call_indirect $__indirect_function_table (type $t9)
          local.set $p2
        end
        local.get $p2
        local.get $l5
        i32.load offset=4
        local.tee $p3
        i32.const 0
        i32.gt_s
        if $I39 (result i32)
          local.get $p2
          local.get $p3
          i32.const 3
          i32.shl
          i32.add
          local.set $l6
          local.get $l5
          i32.load
          local.set $p3
          local.get $p2
          local.set $p1
          loop $L40
            local.get $p1
            local.get $p3
            i64.load align=4
            i64.store align=4
            local.get $p3
            i32.const 8
            i32.add
            local.set $p3
            local.get $p1
            i32.const 8
            i32.add
            local.tee $p1
            local.get $l6
            i32.lt_u
            br_if $L40
          end
          local.get $l5
          i32.load offset=4
        else
          local.get $p3
        end
        i32.const 3
        i32.shl
        i32.add
        local.get $l4
        i64.load align=4
        i64.store align=4
        block $B41
          local.get $l5
          i32.load offset=8
          i32.const 0
          i32.lt_s
          br_if $B41
          local.get $l5
          i32.load
          local.tee $p3
          i32.eqz
          br_if $B41
          call $f69753
          local.tee $p1
          local.get $p3
          local.get $p1
          i32.load
          i32.load offset=12
          call_indirect $__indirect_function_table (type $t1)
        end
        local.get $l5
        local.get $l11
        i32.store offset=8
        local.get $l5
        local.get $p2
        i32.store
        local.get $l5
        local.get $l5
        i32.load offset=4
        i32.const 1
        i32.add
        i32.store offset=4
        br $B36
      end
      local.get $p0
      i32.load offset=92
      local.get $p1
      i32.const 3
      i32.shl
      i32.add
      local.get $l9
      i64.load offset=8
      i64.store align=4
      local.get $p0
      local.get $p0
      i32.load offset=96
      i32.const 1
      i32.add
      i32.store offset=96
    end
    block $B42
      local.get $p0
      i32.load offset=84
      local.tee $p1
      local.get $p0
      i32.load offset=88
      i32.const 2147483647
      i32.and
      i32.ge_u
      if $I43
        local.get $l9
        i32.const 44
        i32.add
        local.set $l4
        i32.const 0
        local.set $p2
        block $B44
          local.get $p0
          i32.const 80
          i32.add
          local.tee $l5
          i32.load offset=8
          i32.const 2147483647
          i32.and
          local.tee $p3
          i32.const 1
          i32.shl
          i32.const 1
          local.get $p3
          select
          local.tee $l11
          i32.eqz
          br_if $B44
          local.get $l11
          i32.const 2
          i32.shl
          local.tee $p3
          i32.eqz
          br_if $B44
          call $f69753
          local.tee $p1
          local.get $p3
          i32.const 3139253
          i32.const 3134052
          i32.const 4700888
          i32.load
          local.tee $l6
          local.get $l6
          i32.load
          i32.load offset=20
          call_indirect $__indirect_function_table (type $t5)
          select
          i32.const 3134537
          i32.const 553
          local.get $p1
          i32.load
          i32.load offset=8
          call_indirect $__indirect_function_table (type $t9)
          local.set $p2
        end
        local.get $p2
        local.get $l5
        i32.load offset=4
        local.tee $p3
        i32.const 0
        i32.gt_s
        if $I45 (result i32)
          local.get $p2
          local.get $p3
          i32.const 2
          i32.shl
          i32.add
          local.set $l6
          local.get $l5
          i32.load
          local.set $p3
          local.get $p2
          local.set $p1
          loop $L46
            local.get $p1
            local.get $p3
            i32.load
            i32.store
            local.get $p3
            i32.const 4
            i32.add
            local.set $p3
            local.get $p1
            i32.const 4
            i32.add
            local.tee $p1
            local.get $l6
            i32.lt_u
            br_if $L46
          end
          local.get $l5
          i32.load offset=4
        else
          local.get $p3
        end
        i32.const 2
        i32.shl
        i32.add
        local.get $l4
        i32.load
        i32.store
        block $B47
          local.get $l5
          i32.load offset=8
          i32.const 0
          i32.lt_s
          br_if $B47
          local.get $l5
          i32.load
          local.tee $p3
          i32.eqz
          br_if $B47
          call $f69753
          local.tee $p1
          local.get $p3
          local.get $p1
          i32.load
          i32.load offset=12
          call_indirect $__indirect_function_table (type $t1)
        end
        local.get $l5
        local.get $l11
        i32.store offset=8
        local.get $l5
        local.get $p2
        i32.store
        local.get $l5
        local.get $l5
        i32.load offset=4
        i32.const 1
        i32.add
        i32.store offset=4
        br $B42
      end
      local.get $p0
      i32.load offset=80
      local.get $p1
      i32.const 2
      i32.shl
      i32.add
      local.get $l9
      i32.load offset=44
      i32.store
      local.get $p0
      local.get $p0
      i32.load offset=84
      i32.const 1
      i32.add
      i32.store offset=84
    end
    local.get $l9
    i32.load offset=44
    local.get $p0
    i32.load offset=64
    local.get $p0
    i32.load offset=72
    i32.const 3
    i32.shl
    i32.const 2147483640
    i32.add
    i32.or
    i32.const -2147483648
    i32.or
    i32.store offset=68
    local.get $l9
    i32.const 48
    i32.add
    global.set $g0)