  (func $f71628 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 i32) (local $l17 i32) (local $l18 i32) (local $l19 i32) (local $l20 i32) (local $l21 i32) (local $l22 f32) (local $l23 f32)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l13
    global.set $g0
    local.get $p0
    i32.load offset=4
    i32.load offset=40
    local.tee $l14
    i32.load offset=976
    local.set $l6
    local.get $p0
    i32.load offset=44
    local.tee $l15
    i32.const 2048
    i32.and
    local.tee $l16
    i32.const 11
    i32.shr_u
    local.set $l10
    local.get $p1
    local.tee $l3
    local.set $l8
    block $B0
      local.get $l3
      i32.eqz
      if $I1
        local.get $l6
        local.get $l6
        i32.load offset=328
        local.tee $l8
        if $I2 (result i32)
          local.get $l8
        else
          i32.const 0
          local.set $l8
          block $B3
            local.get $l6
            i32.const 312
            i32.add
            local.tee $l5
            i32.load
            i32.const 80
            i32.mul
            local.tee $l7
            i32.eqz
            br_if $B3
            call $f69753
            local.tee $l4
            local.get $l7
            i32.const 3138039
            i32.const 3134052
            i32.const 4700888
            i32.load
            local.tee $l11
            local.get $l11
            i32.load
            i32.load offset=20
            call_indirect $__indirect_function_table (type $t5)
            select
            i32.const 3138006
            i32.const 236
            local.get $l4
            i32.load
            i32.load offset=8
            call_indirect $__indirect_function_table (type $t9)
            local.tee $l11
            i32.eqz
            br_if $B3
            block $B4
              local.get $l5
              i32.load offset=4
              local.tee $l4
              i32.const 1
              i32.add
              local.tee $l7
              local.get $l5
              i32.load
              i32.mul
              local.tee $l9
              local.get $l5
              i32.load offset=32
              local.tee $l2
              i32.const 5
              i32.shl
              i32.le_u
              if $I5
                local.get $l5
                i32.load offset=20
                local.set $l2
                br $B4
              end
              local.get $l9
              i32.const 1
              i32.shl
              i32.const 31
              i32.add
              i32.const 5
              i32.shr_u
              local.tee $l4
              local.get $l2
              i32.const 2147483647
              i32.and
              i32.gt_u
              if $I6
                call $f69753
                local.tee $l2
                local.get $l4
                i32.const 2
                i32.shl
                i32.const 3133968
                i32.const 3135509
                i32.const 438
                local.get $l2
                i32.load
                i32.load offset=8
                call_indirect $__indirect_function_table (type $t9)
                local.set $l2
                block $B7
                  local.get $l5
                  i32.load offset=28
                  local.tee $l9
                  i32.eqz
                  br_if $B7
                  local.get $l2
                  local.get $l9
                  local.get $l5
                  i32.load offset=32
                  i32.const 2
                  i32.shl
                  call $f483
                  drop
                  local.get $l5
                  i32.load offset=32
                  i32.const 0
                  i32.lt_s
                  br_if $B7
                  local.get $l5
                  i32.load offset=28
                  local.tee $l9
                  i32.eqz
                  br_if $B7
                  call $f69753
                  local.tee $l12
                  local.get $l9
                  local.get $l12
                  i32.load
                  i32.load offset=12
                  call_indirect $__indirect_function_table (type $t1)
                end
                local.get $l2
                local.get $l5
                i32.load offset=32
                local.tee $l9
                i32.const 2
                i32.shl
                i32.add
                i32.const 0
                local.get $l4
                local.get $l9
                i32.sub
                i32.const 2
                i32.shl
                call $f484
                drop
                local.get $l5
                local.get $l4
                i32.store offset=32
                local.get $l5
                local.get $l2
                i32.store offset=28
              end
              local.get $l5
              i32.load offset=12
              local.tee $l2
              if $I8
                call $f69753
                local.tee $l4
                local.get $l2
                local.get $l4
                i32.load
                i32.load offset=12
                call_indirect $__indirect_function_table (type $t1)
              end
              i32.const 0
              local.set $l2
              local.get $l5
              local.get $l7
              i32.const 3
              i32.shl
              local.tee $l7
              local.get $l5
              i32.load
              i32.mul
              local.tee $l9
              if $I9 (result i32)
                call $f69753
                local.tee $l4
                local.get $l9
                i32.const 3138039
                i32.const 3134052
                i32.const 4700888
                i32.load
                local.tee $l12
                local.get $l12
                i32.load
                i32.load offset=20
                call_indirect $__indirect_function_table (type $t5)
                select
                i32.const 3138006
                i32.const 248
                local.get $l4
                i32.load
                i32.load offset=8
                call_indirect $__indirect_function_table (type $t9)
              else
                i32.const 0
              end
              i32.store offset=12
              local.get $l7
              if $I10
                call $f69753
                local.tee $l2
                local.get $l7
                i32.const 3138039
                i32.const 3134052
                i32.const 4700888
                i32.load
                local.tee $l4
                local.get $l4
                i32.load
                i32.load offset=20
                call_indirect $__indirect_function_table (type $t5)
                select
                i32.const 3138006
                i32.const 250
                local.get $l2
                i32.load
                i32.load offset=8
                call_indirect $__indirect_function_table (type $t9)
                local.set $l2
              end
              block $B11
                local.get $l5
                i32.load offset=20
                local.tee $l7
                i32.eqz
                br_if $B11
                local.get $l2
                local.get $l7
                local.get $l5
                i32.load offset=4
                i32.const 2
                i32.shl
                call $f483
                drop
                local.get $l5
                i32.load offset=20
                local.tee $l7
                i32.eqz
                br_if $B11
                call $f69753
                local.tee $l4
                local.get $l7
                local.get $l4
                i32.load
                i32.load offset=12
                call_indirect $__indirect_function_table (type $t1)
              end
              local.get $l5
              local.get $l2
              i32.store offset=20
              local.get $l5
              i32.load offset=4
              local.tee $l4
              i32.const 1
              i32.add
              local.set $l7
            end
            local.get $l5
            local.get $l7
            i32.store offset=4
            local.get $l2
            local.get $l4
            i32.const 2
            i32.shl
            i32.add
            local.get $l11
            i32.store
            local.get $l5
            i32.load offset=16
            local.set $l4
            local.get $l5
            i32.load
            local.tee $l2
            i32.const 1
            i32.sub
            local.tee $l7
            i32.const 0
            i32.ge_s
            if $I12
              local.get $l5
              i32.load offset=4
              i32.const 1
              i32.sub
              local.get $l2
              i32.mul
              local.set $l9
              loop $L13
                local.get $l11
                local.get $l7
                i32.const 80
                i32.mul
                i32.add
                local.tee $l2
                i32.const 0
                i32.store offset=8
                local.get $l2
                i64.const 0
                i64.store offset=16 align=4
                local.get $l2
                local.get $l7
                local.get $l9
                i32.add
                i32.store offset=48
                local.get $l2
                i32.const 0
                i32.store offset=52
                local.get $l2
                i32.const 257
                i32.store16 offset=44
                local.get $l2
                i32.const 0
                i32.store8 offset=42
                local.get $l2
                i32.const 0
                i32.store offset=36
                local.get $l5
                i32.load offset=12
                local.get $l4
                i32.const 2
                i32.shl
                i32.add
                local.get $l2
                i32.store
                local.get $l4
                i32.const 1
                i32.add
                local.set $l4
                local.get $l7
                i32.const 0
                i32.gt_s
                local.set $l2
                local.get $l7
                i32.const 1
                i32.sub
                local.set $l7
                local.get $l2
                br_if $L13
              end
            end
            local.get $l5
            local.get $l4
            i32.store offset=16
            i32.const 1
            local.set $l2
          end
          local.get $l2
          i32.eqz
          br_if $B0
          local.get $l6
          i32.load offset=328
        end
        i32.const 1
        i32.sub
        local.tee $l8
        i32.store offset=328
        local.get $l6
        i32.load offset=340
        local.get $l6
        i32.load offset=324
        local.get $l8
        i32.const 2
        i32.shl
        i32.add
        i32.load
        local.tee $l8
        i32.load offset=48
        local.tee $l2
        i32.const 3
        i32.shr_u
        i32.const 536870908
        i32.and
        i32.add
        local.tee $l5
        local.get $l5
        i32.load
        i32.const 1
        local.get $l2
        i32.shl
        i32.or
        i32.store
      end
      local.get $l8
      i64.const 0
      i64.store offset=32 align=4
      local.get $l8
      i32.const 0
      i32.store8 offset=42
      local.get $l3
      br_if $B0
      block $B14
        local.get $l8
        i32.load offset=48
        local.tee $l3
        local.get $l6
        i32.load offset=940
        local.tee $l2
        i32.const 5
        i32.shl
        i32.lt_u
        br_if $B14
        local.get $l3
        i32.const 1
        i32.shl
        i32.const 256
        i32.add
        i32.const 5
        i32.shr_u
        i32.const 134217720
        i32.and
        local.tee $l5
        local.get $l2
        i32.const 2147483647
        i32.and
        i32.le_u
        br_if $B14
        call $f69753
        local.tee $l3
        local.get $l5
        i32.const 2
        i32.shl
        i32.const 3133968
        i32.const 3135509
        i32.const 438
        local.get $l3
        i32.load
        i32.load offset=8
        call_indirect $__indirect_function_table (type $t9)
        local.set $l3
        block $B15
          local.get $l6
          i32.load offset=936
          local.tee $l2
          i32.eqz
          br_if $B15
          local.get $l3
          local.get $l2
          local.get $l6
          i32.load offset=940
          i32.const 2
          i32.shl
          call $f483
          drop
          local.get $l6
          i32.load offset=940
          i32.const 0
          i32.lt_s
          br_if $B15
          local.get $l6
          i32.load offset=936
          local.tee $l2
          i32.eqz
          br_if $B15
          call $f69753
          local.tee $l4
          local.get $l2
          local.get $l4
          i32.load
          i32.load offset=12
          call_indirect $__indirect_function_table (type $t1)
        end
        local.get $l3
        local.get $l6
        i32.load offset=940
        local.tee $l2
        i32.const 2
        i32.shl
        i32.add
        i32.const 0
        local.get $l5
        local.get $l2
        i32.sub
        i32.const 2
        i32.shl
        call $f484
        drop
        local.get $l6
        local.get $l5
        i32.store offset=940
        local.get $l6
        local.get $l3
        i32.store offset=936
        local.get $l8
        i32.load offset=48
        local.set $l3
      end
      local.get $l6
      i32.load offset=936
      local.get $l3
      i32.const 3
      i32.shr_u
      i32.const 536870908
      i32.and
      i32.add
      local.tee $l2
      local.get $l2
      i32.load
      i32.const 1
      local.get $l3
      i32.shl
      i32.or
      i32.store
      local.get $l10
      i32.eqz
      br_if $B0
      block $B16
        local.get $l8
        i32.load offset=48
        local.tee $l3
        local.get $l6
        i32.load offset=952
        local.tee $l10
        i32.const 5
        i32.shl
        i32.lt_u
        br_if $B16
        local.get $l3
        i32.const 1
        i32.shl
        i32.const 256
        i32.add
        i32.const 5
        i32.shr_u
        i32.const 134217720
        i32.and
        local.tee $l2
        local.get $l10
        i32.const 2147483647
        i32.and
        i32.le_u
        br_if $B16
        call $f69753
        local.tee $l3
        local.get $l2
        i32.const 2
        i32.shl
        i32.const 3133968
        i32.const 3135509
        i32.const 438
        local.get $l3
        i32.load
        i32.load offset=8
        call_indirect $__indirect_function_table (type $t9)
        local.set $l3
        block $B17
          local.get $l6
          i32.load offset=948
          local.tee $l10
          i32.eqz
          br_if $B17
          local.get $l3
          local.get $l10
          local.get $l6
          i32.load offset=952
          i32.const 2
          i32.shl
          call $f483
          drop
          local.get $l6
          i32.load offset=952
          i32.const 0
          i32.lt_s
          br_if $B17
          local.get $l6
          i32.load offset=948
          local.tee $l10
          i32.eqz
          br_if $B17
          call $f69753
          local.tee $l5
          local.get $l10
          local.get $l5
          i32.load
          i32.load offset=12
          call_indirect $__indirect_function_table (type $t1)
        end
        local.get $l3
        local.get $l6
        i32.load offset=952
        local.tee $l10
        i32.const 2
        i32.shl
        i32.add
        i32.const 0
        local.get $l2
        local.get $l10
        i32.sub
        i32.const 2
        i32.shl
        call $f484
        drop
        local.get $l6
        local.get $l2
        i32.store offset=952
        local.get $l6
        local.get $l3
        i32.store offset=948
        local.get $l8
        i32.load offset=48
        local.set $l3
      end
      local.get $l6
      i32.load offset=948
      local.get $l3
      i32.const 3
      i32.shr_u
      i32.const 536870908
      i32.and
      i32.add
      local.tee $l6
      local.get $l6
      i32.load
      i32.const 1
      local.get $l3
      i32.shl
      i32.or
      i32.store
    end
    local.get $l8
    local.set $l4
    i32.const 1
    i32.const -1
    local.get $p0
    i32.load offset=44
    local.tee $l3
    i32.const 32768
    i32.and
    select
    i32.const 0
    local.get $l3
    i32.const 98304
    i32.and
    select
    local.set $l9
    local.get $l15
    i32.const 448
    i32.and
    i32.eqz
    local.get $l3
    i32.const 262144
    i32.and
    local.tee $l11
    i32.const 18
    i32.shr_u
    i32.or
    local.set $l18
    local.get $l15
    i32.const 2
    i32.and
    local.tee $l10
    i32.const 1
    i32.shr_u
    local.set $l19
    local.get $l3
    i32.const 131072
    i32.and
    local.set $l20
    local.get $p0
    i32.load offset=32
    local.tee $l3
    i32.load offset=4
    i32.load offset=44
    i32.load8_u offset=9
    local.set $l5
    local.get $p0
    i32.load offset=28
    local.tee $l7
    i32.load offset=4
    i32.load offset=44
    i32.load8_u offset=9
    local.set $l6
    local.get $l7
    call $f71419
    local.set $l12
    local.get $l3
    call $f71419
    local.set $l2
    local.get $l13
    i32.const 8
    i32.add
    local.get $l14
    local.get $l12
    i32.load offset=44
    i32.load8_u offset=10
    local.get $l2
    if $I18 (result i32)
      local.get $l2
      i32.load offset=44
      local.tee $l8
      i32.load8_u offset=44
      i32.const 1
      i32.and
      local.set $l21
      local.get $l8
      i32.load8_u offset=10
    else
      i32.const 0
    end
    i32.const 255
    i32.and
    call $f71440
    local.get $l7
    i32.load offset=40
    local.set $l17
    local.get $l3
    i32.load offset=40
    local.set $l8
    local.get $l4
    local.get $p0
    i32.store offset=12
    local.get $l4
    local.get $l2
    i32.const -64
    i32.sub
    i32.const 0
    local.get $l2
    select
    i32.store offset=4
    local.get $l4
    local.get $l12
    i32.const -64
    i32.sub
    i32.store
    local.get $l4
    local.get $l8
    i32.const 32
    i32.add
    i32.store offset=28
    local.get $l4
    local.get $l17
    i32.const 32
    i32.add
    i32.store offset=24
    local.get $l4
    local.get $l7
    call $f71457
    i32.store offset=16
    local.get $l4
    local.get $l3
    call $f71457
    i32.store offset=20
    local.get $l4
    local.get $l7
    i32.load offset=40
    f32.load offset=128
    local.get $l3
    i32.load offset=40
    f32.load offset=128
    f32.add
    f32.store offset=52
    local.get $l4
    local.get $l13
    i32.load8_u offset=8
    i32.store8 offset=44
    local.get $l4
    local.get $l13
    i32.load8_u offset=9
    i32.store8 offset=45
    local.get $l4
    local.get $l17
    i32.load offset=68
    i32.store8 offset=46
    local.get $l4
    local.get $l8
    i32.load offset=68
    i32.store8 offset=47
    local.get $l4
    local.get $l7
    i32.load offset=8
    i32.const 2147483647
    i32.and
    i32.store offset=56
    local.get $l4
    local.get $l3
    i32.load offset=8
    i32.const 2147483647
    i32.and
    i32.store offset=60
    local.get $l4
    local.get $l7
    i32.load offset=40
    f32.load offset=132
    local.tee $l22
    local.get $l3
    i32.load offset=40
    f32.load offset=132
    local.tee $l23
    local.get $l22
    local.get $l23
    f32.gt
    select
    f32.store offset=72
    local.get $l3
    i32.load offset=40
    f32.load offset=136
    local.set $l22
    local.get $l7
    i32.load offset=40
    f32.load offset=136
    local.set $l23
    local.get $l4
    local.get $l10
    i32.const 6
    i32.shl
    local.get $l10
    local.get $l20
    i32.or
    i32.const 0
    i32.ne
    local.get $l15
    i32.const 1
    i32.shr_u
    i32.const 512
    i32.and
    local.get $l6
    local.tee $l3
    i32.const 2
    i32.eq
    i32.const 3
    i32.shl
    local.tee $l7
    i32.const 16
    i32.or
    local.get $l7
    local.get $l5
    local.tee $l2
    i32.const 2
    i32.eq
    select
    local.tee $l7
    i32.const 32
    i32.or
    local.get $l7
    local.get $l3
    select
    local.tee $l3
    i32.const 64
    i32.or
    local.get $l3
    local.get $l2
    select
    local.tee $l3
    local.get $l3
    i32.const 2
    i32.or
    local.get $l10
    local.get $l11
    i32.or
    select
    i32.or
    local.tee $l3
    i32.const 1024
    i32.or
    local.get $l3
    local.get $l21
    select
    local.tee $l3
    i32.const 2048
    i32.or
    local.get $l3
    local.get $l11
    select
    local.tee $l3
    i32.const 4096
    i32.or
    local.get $l3
    local.get $l16
    select
    i32.or
    local.tee $l3
    local.get $l3
    i32.const 256
    i32.or
    local.get $l18
    select
    i32.or
    i32.store16 offset=40
    local.get $l4
    i32.const -1
    i32.store offset=68
    local.get $l4
    local.get $l19
    local.get $l16
    i32.const 10
    i32.shr_u
    i32.or
    i32.store offset=8
    local.get $l4
    local.get $l23
    local.get $l22
    local.get $l22
    local.get $l23
    f32.lt
    select
    f32.store offset=76
    local.get $p0
    local.get $l4
    i32.store offset=56
    local.get $l4
    i32.const 2
    local.get $l9
    i32.const 31
    i32.shr_u
    local.get $l9
    i32.const 0
    i32.gt_s
    select
    i32.store8 offset=43
    local.get $p1
    i32.eqz
    if $I19
      local.get $l14
      i32.load offset=1000
      local.tee $l5
      i32.load offset=128
      local.get $p0
      i32.load offset=60
      local.tee $l6
      local.get $l5
      i32.load offset=148
      local.tee $l5
      i32.div_u
      local.tee $p1
      i32.const 2
      i32.shl
      i32.add
      i32.load
      local.get $l6
      local.get $p1
      local.get $l5
      i32.mul
      i32.sub
      i32.const 2
      i32.shl
      i32.add
      local.get $p0
      i32.load offset=56
      local.tee $p1
      i32.store
      local.get $p1
      i32.const -64
      i32.sub
      local.get $l6
      i32.store
      local.get $l14
      i32.load offset=976
      i32.load offset=1024
      local.tee $l4
      local.get $p0
      i32.load offset=56
      local.get $l9
      i32.const 0
      local.get $l4
      i32.load
      i32.load offset=28
      call_indirect $__indirect_function_table (type $t4)
    end
    local.get $l13
    i32.const 16
    i32.add
    global.set $g0)