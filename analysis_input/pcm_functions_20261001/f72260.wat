  (func $f72260 (type $t3) (param $p0 i32) (param $p1 i32) (param $p2 i32) (result i32)
    (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 i32) (local $l17 i32) (local $l18 i32) (local $l19 i32) (local $l20 i32) (local $l21 i32) (local $l22 i32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32) (local $l33 f32) (local $l34 f32) (local $l35 f32) (local $l36 f32) (local $l37 f32) (local $l38 f32) (local $l39 f32)
    global.get $g0
    i32.const 224
    i32.sub
    local.tee $l4
    global.set $g0
    local.get $l4
    i64.const 0
    i64.store offset=200
    local.get $l4
    i64.const 0
    i64.store offset=208
    local.get $l4
    i64.const 0
    i64.store offset=192
    local.get $l4
    i32.const 0
    i32.store16 offset=188
    local.get $l4
    i64.const 0
    i64.store offset=176
    local.get $l4
    i32.const 2139095039
    i32.store offset=216
    local.get $l4
    i32.const -1
    i32.store offset=184
    local.get $p2
    i32.load
    local.set $l12
    local.get $p2
    i32.load offset=4
    local.tee $p2
    i32.load offset=4
    i32.const 22
    i32.shr_u
    i32.const 60
    i32.and
    i32.const 3181092
    i32.add
    i32.load
    local.get $p2
    i32.add
    call $f71725
    local.set $l21
    local.get $l12
    i32.const 16
    i32.add
    call $f71452
    local.set $l22
    i32.const 2
    i32.const 1
    local.get $p0
    i32.load8_u offset=42
    local.tee $l10
    select
    local.tee $l3
    i32.const 2
    local.get $l3
    local.get $p0
    i32.load offset=20
    local.tee $l5
    i32.load16_s offset=16
    local.tee $l7
    i32.const 0
    i32.ge_s
    select
    local.get $p0
    i32.load offset=12
    i32.load offset=60
    select
    local.set $l16
    local.get $p0
    i32.load16_u offset=16
    local.set $l3
    block $B0 (result i32)
      block $B1
        block $B2
          local.get $l10
          br_if $B2
          local.get $l7
          i32.const 4
          i32.and
          i32.eqz
          br_if $B2
          i32.const 1
          local.get $p0
          i32.load offset=24
          local.tee $l15
          local.get $p0
          i32.load offset=32
          local.tee $l10
          select
          i32.eqz
          br_if $B2
          local.get $l4
          local.get $l3
          i32.store16 offset=80
          block $B3
            local.get $l15
            if $I4
              local.get $l15
              local.get $l5
              local.get $l22
              local.get $l21
              local.get $l4
              i32.const 80
              i32.add
              local.get $l15
              i32.load
              i32.load
              call_indirect $__indirect_function_table (type $t9)
              local.set $l16
              br $B3
            end
            local.get $l10
            i32.load offset=8
            local.tee $l15
            i32.eqz
            br_if $B3
            local.get $l4
            local.get $l5
            i32.load
            i32.store offset=8
            local.get $l4
            local.get $l5
            i32.load offset=4
            i32.store offset=12
            local.get $l4
            local.get $l5
            i32.load offset=8
            i32.store offset=16
            local.get $l4
            local.get $l5
            i32.load offset=12
            i32.store offset=20
            local.get $l4
            local.get $l12
            i32.load offset=16
            i32.store offset=144
            local.get $l4
            local.get $l12
            i32.load offset=20
            i32.store offset=148
            local.get $l4
            local.get $l12
            i32.load offset=24
            i32.store offset=152
            local.get $l4
            local.get $l12
            i32.load offset=28
            i32.store offset=156
            local.get $l4
            i32.const 8
            i32.add
            local.get $l4
            i32.const 144
            i32.add
            local.get $l10
            i32.load
            local.get $l10
            i32.load offset=4
            local.get $l4
            i32.const 80
            i32.add
            local.get $l15
            call_indirect $__indirect_function_table (type $t9)
            local.set $l16
          end
          local.get $l16
          i32.eqz
          br_if $B1
          local.get $l4
          i32.load16_u offset=80
          i32.const 432
          i32.and
          local.get $l3
          i32.const -433
          i32.and
          i32.or
          local.set $l3
        end
        local.get $l4
        i32.const 144
        i32.add
        local.get $l12
        local.get $p2
        call $f71930
        local.get $p0
        i32.load offset=72
        local.set $l20
        local.get $p0
        i32.load offset=8
        local.set $l8
        local.get $p0
        i32.load offset=4
        local.set $l18
        local.get $p0
        i32.load offset=12
        local.tee $l10
        i32.load offset=56
        local.set $l11
        block $B5 (result i32)
          local.get $l12
          i32.load8_u offset=4
          i32.const 1
          i32.and
          if $I6
            local.get $l12
            i32.load offset=8
            i32.const -64
            i32.sub
            br $B5
          end
          local.get $l12
          i32.const 84
          i32.add
        end
        local.tee $l6
        i32.load
        drop
        local.get $l10
        i32.load offset=64
        local.set $p2
        local.get $l10
        i32.load offset=60
        local.set $l5
        local.get $l4
        local.get $p0
        i32.load16_u offset=36
        local.get $l3
        i32.or
        i32.store16 offset=136
        i32.const 1
        local.set $l15
        i32.const 0
        local.set $l10
        local.get $l4
        i32.const 136
        i32.add
        local.set $l19
        local.get $l11
        local.get $p2
        i32.const 48
        i32.mul
        i32.add
        local.get $l4
        i32.const 176
        i32.add
        local.get $p2
        local.get $l5
        i32.lt_u
        select
        local.set $l11
        local.get $p0
        f32.load offset=28
        local.set $l25
        local.get $p0
        i32.const 44
        i32.add
        i32.const 0
        local.get $p0
        i32.load8_u offset=68
        select
        local.set $l9
        global.get $g0
        i32.const 160
        i32.sub
        local.tee $l5
        global.set $g0
        local.get $l9
        f32.load offset=20
        local.set $l23
        local.get $l9
        f32.load offset=16
        local.set $l27
        local.get $l8
        i32.load offset=16
        local.set $l14
        local.get $l8
        i32.load offset=12
        local.set $l17
        local.get $l9
        f32.load offset=8
        local.set $l28
        local.get $l9
        f32.load offset=4
        local.set $l24
        local.get $l9
        f32.load offset=12
        local.set $l26
        local.get $l9
        f32.load
        local.set $l29
        i32.const 0
        local.set $l9
        local.get $l5
        i32.const 136
        i32.add
        local.get $l6
        local.tee $p2
        local.get $l4
        i32.const 144
        i32.add
        local.tee $l6
        f32.const 0x1p+0 (;=1;)
        call $f70384
        local.get $l5
        local.get $l26
        local.get $l29
        f32.sub
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        local.get $l5
        f32.load offset=148
        local.tee $l30
        local.get $l5
        f32.load offset=136
        local.tee $l31
        f32.sub
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        f32.add
        f32.const 0x1.028f5cp+0 (;=1.01;)
        f32.mul
        local.tee $l33
        f32.store offset=120
        local.get $l5
        local.get $l27
        local.get $l24
        f32.sub
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        local.get $l5
        f32.load offset=152
        local.tee $l34
        local.get $l5
        f32.load offset=140
        local.tee $l35
        f32.sub
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        f32.add
        f32.const 0x1.028f5cp+0 (;=1.01;)
        f32.mul
        local.tee $l36
        f32.store offset=124
        local.get $l5
        local.get $l23
        local.get $l28
        f32.sub
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        local.get $l5
        f32.load offset=156
        local.tee $l37
        local.get $l5
        f32.load offset=144
        local.tee $l38
        f32.sub
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        f32.add
        f32.const 0x1.028f5cp+0 (;=1.01;)
        f32.mul
        local.tee $l39
        f32.store offset=128
        local.get $l5
        local.get $l39
        f32.neg
        f32.store offset=88
        local.get $l5
        local.get $l36
        f32.neg
        f32.store offset=84
        local.get $l5
        local.get $l33
        f32.neg
        f32.store offset=80
        local.get $l5
        local.get $l28
        local.get $l23
        f32.add
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        local.get $l37
        local.get $l38
        f32.add
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        f32.sub
        f32.store offset=40
        local.get $l5
        local.get $l24
        local.get $l27
        f32.add
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        local.get $l34
        local.get $l35
        f32.add
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        f32.sub
        f32.store offset=36
        local.get $l5
        local.get $l29
        local.get $l26
        f32.add
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        local.get $l30
        local.get $l31
        f32.add
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        f32.sub
        f32.store offset=32
        local.get $l5
        i32.const 80
        i32.add
        local.get $l5
        i32.const 120
        i32.add
        local.get $l5
        i32.const 32
        i32.add
        local.get $l8
        i32.load offset=4
        local.get $l25
        local.get $l5
        i32.const 116
        i32.add
        local.get $l5
        i32.const 112
        i32.add
        call $f69911
        local.set $l13
        local.get $l5
        f32.load offset=116
        local.set $l23
        block $B7
          local.get $l13
          i32.eqz
          if $I8
            local.get $l23
            local.get $l5
            f32.load offset=112
            f32.gt
            br_if $B7
          end
          local.get $l23
          f32.const -0x1.4p+3 (;=-10;)
          f32.add
          f32.const 0x0p+0 (;=0;)
          local.get $l23
          f32.const 0x1.4p+3 (;=10;)
          f32.gt
          local.tee $l9
          select
          local.set $l23
          local.get $l8
          i32.load offset=4
          local.set $l13
          f32.const 0x0p+0 (;=0;)
          local.set $l27
          f32.const 0x0p+0 (;=0;)
          local.set $l28
          local.get $l9
          if $I9
            local.get $l23
            local.get $l13
            f32.load offset=8
            f32.mul
            local.set $l28
            local.get $l23
            local.get $l13
            f32.load
            f32.mul
            local.set $l32
            local.get $l23
            local.get $l13
            f32.load offset=4
            f32.mul
            local.set $l27
          end
          local.get $l6
          f32.load offset=20
          local.set $l24
          local.get $l6
          f32.load offset=24
          local.set $l26
          local.get $l6
          f32.load offset=16
          local.set $l29
          local.get $l5
          local.get $l6
          f32.load
          f32.store offset=80
          local.get $l5
          local.get $l6
          f32.load offset=4
          f32.store offset=84
          local.get $l5
          local.get $l6
          f32.load offset=8
          f32.store offset=88
          local.get $l6
          f32.load offset=12
          local.set $l30
          local.get $l5
          local.get $l26
          local.get $l28
          f32.sub
          f32.store offset=104
          local.get $l5
          local.get $l24
          local.get $l27
          f32.sub
          f32.store offset=100
          local.get $l5
          local.get $l29
          local.get $l32
          f32.sub
          f32.store offset=96
          local.get $l5
          local.get $l30
          f32.store offset=92
          local.get $l5
          f32.load offset=112
          local.tee $l24
          local.get $l25
          local.get $l24
          local.get $l25
          f32.lt
          select
          local.get $l23
          f32.sub
          local.set $l25
          local.get $l18
          i32.load offset=5732
          local.set $l6
          local.get $l8
          f32.load offset=20
          local.set $l24
          i32.const 0
          local.set $l9
          block $B10
            block $B11
              block $B12
                block $B13
                  block $B14
                    block $B15
                      local.get $l17
                      i32.load
                      i32.const 1
                      i32.add
                      br_table $B12 $B11 $B12 $B15 $B14 $B13 $B12 $B12 $B12 $B7
                    end
                    local.get $l6
                    local.get $p2
                    i32.load
                    i32.const 2
                    i32.shl
                    i32.add
                    local.tee $l6
                    i32.const 28
                    i32.add
                    local.get $l6
                    local.get $l19
                    i32.load16_u
                    local.tee $l8
                    i32.const 256
                    i32.and
                    select
                    i32.load
                    local.set $l6
                    local.get $l5
                    local.get $l8
                    i32.store16 offset=16
                    local.get $p2
                    local.get $l5
                    i32.const 80
                    i32.add
                    local.get $l17
                    local.get $l14
                    local.get $l20
                    i32.const 100
                    i32.add
                    local.get $l13
                    local.get $l25
                    local.get $l11
                    local.get $l5
                    i32.const 16
                    i32.add
                    local.get $l24
                    local.get $l6
                    call_indirect $__indirect_function_table (type $t80)
                    br_if $B10
                    br $B7
                  end
                  local.get $l6
                  local.get $p2
                  i32.load
                  i32.const 2
                  i32.shl
                  i32.add
                  local.tee $l6
                  i32.const 84
                  i32.add
                  local.get $l6
                  i32.const 56
                  i32.add
                  local.get $l19
                  i32.load16_u
                  local.tee $l6
                  i32.const 256
                  i32.and
                  select
                  i32.load
                  local.set $l8
                  local.get $l5
                  local.get $l6
                  i32.store16 offset=8
                  local.get $p2
                  local.get $l5
                  i32.const 80
                  i32.add
                  local.get $l17
                  local.get $l14
                  local.get $l20
                  i32.const 12
                  i32.add
                  local.get $l13
                  local.get $l25
                  local.get $l11
                  local.get $l5
                  i32.const 8
                  i32.add
                  local.get $l24
                  local.get $l8
                  call_indirect $__indirect_function_table (type $t80)
                  br_if $B10
                  br $B7
                end
                local.get $l6
                local.get $p2
                i32.load
                i32.const 2
                i32.shl
                i32.add
                i32.load offset=112
                local.set $l6
                local.get $l5
                local.get $l19
                i32.load16_u
                i32.store16
                local.get $p2
                local.get $l5
                i32.const 80
                i32.add
                local.get $l17
                local.get $l14
                local.get $l13
                local.get $l25
                local.get $l11
                local.get $l5
                local.get $l24
                local.get $l6
                call_indirect $__indirect_function_table (type $t130)
                br_if $B10
                br $B7
              end
              i32.const 4700888
              i32.load
              i32.const 4
              i32.const 3187986
              i32.const 298
              i32.const 3196668
              i32.const 0
              call $f69760
              br $B7
            end
            local.get $l17
            f32.load offset=4
            local.set $l26
            local.get $l5
            i32.const 0
            i32.store offset=72
            local.get $l5
            local.get $l26
            f32.store offset=68
            local.get $l5
            i32.const 2
            i32.store offset=64
            local.get $l17
            f32.load offset=4
            local.set $l26
            local.get $l5
            local.get $l14
            f32.load offset=16
            local.tee $l29
            f32.store offset=32
            local.get $l5
            local.get $l14
            f32.load offset=20
            local.tee $l30
            f32.store offset=36
            local.get $l5
            local.get $l14
            f32.load offset=24
            local.tee $l31
            f32.store offset=52
            local.get $l5
            local.get $l30
            f32.store offset=48
            local.get $l5
            local.get $l26
            f32.store offset=56
            local.get $l5
            local.get $l29
            f32.store offset=44
            local.get $l5
            local.get $l31
            f32.store offset=40
            local.get $l6
            local.get $p2
            i32.load
            i32.const 2
            i32.shl
            i32.add
            local.tee $l6
            i32.const 28
            i32.add
            local.get $l6
            local.get $l19
            i32.load16_u
            local.tee $l8
            i32.const 256
            i32.and
            select
            i32.load
            local.set $l6
            local.get $l5
            local.get $l8
            i32.store16 offset=24
            local.get $p2
            local.get $l5
            i32.const 80
            i32.add
            local.get $l5
            i32.const -64
            i32.sub
            local.get $l14
            local.get $l5
            i32.const 32
            i32.add
            local.get $l13
            local.get $l25
            local.get $l11
            local.get $l5
            i32.const 24
            i32.add
            local.get $l24
            local.get $l6
            call_indirect $__indirect_function_table (type $t80)
            i32.eqz
            br_if $B7
          end
          local.get $l11
          local.get $l23
          local.get $l11
          f32.load offset=40
          f32.add
          f32.store offset=40
          local.get $l11
          local.get $l32
          local.get $l11
          f32.load offset=16
          f32.add
          f32.store offset=16
          local.get $l11
          i32.const 20
          i32.add
          local.tee $l9
          local.get $l27
          local.get $l9
          f32.load
          f32.add
          f32.store
          local.get $l11
          i32.const 24
          i32.add
          local.tee $l9
          local.get $l28
          local.get $l9
          f32.load
          f32.add
          f32.store
          i32.const 1
          local.set $l9
        end
        local.get $l5
        i32.const 160
        i32.add
        global.set $g0
        block $B16
          local.get $l9
          local.tee $l5
          i32.eqz
          if $I17
            i32.const 0
            local.set $l15
            br $B16
          end
          local.get $l7
          i32.const 8
          i32.and
          local.set $l20
          local.get $l3
          i32.const 512
          i32.and
          local.set $l6
          local.get $l4
          i32.const 8
          i32.add
          i32.const 4
          i32.or
          local.set $l14
          local.get $l4
          i32.const 28
          i32.add
          local.tee $l9
          i32.const 16
          i32.add
          local.set $l17
          local.get $l9
          i32.const 8
          i32.add
          local.set $l19
          loop $L18
            local.get $l11
            local.get $l10
            i32.const 48
            i32.mul
            i32.add
            local.tee $p2
            local.get $l22
            i32.store offset=4
            local.get $p2
            local.get $l21
            i32.store
            block $B19
              local.get $p2
              f32.load offset=40
              f32.const 0x0p+0 (;=0;)
              f32.ne
              br_if $B19
              local.get $l6
              br_if $B19
              local.get $p0
              i32.load offset=8
              i32.load offset=4
              local.tee $l3
              f32.load
              local.set $l23
              local.get $l3
              f32.load offset=4
              local.set $l24
              local.get $p2
              local.get $l3
              f32.load offset=8
              f32.neg
              f32.store offset=36
              local.get $p2
              local.get $l24
              f32.neg
              f32.store offset=32
              local.get $p2
              local.get $l23
              f32.neg
              f32.store offset=28
            end
            block $B20
              block $B21 (result i32)
                local.get $l16
                local.get $p0
                i32.load8_u offset=42
                br_if $B21
                drop
                local.get $p0
                i32.load offset=24
                local.tee $l7
                i32.eqz
                if $I22
                  local.get $l16
                  local.get $p0
                  i32.load offset=32
                  local.tee $l7
                  i32.eqz
                  br_if $B21
                  drop
                  local.get $l16
                  local.get $l20
                  i32.eqz
                  br_if $B21
                  drop
                  local.get $l16
                  local.get $l7
                  i32.load offset=12
                  local.tee $l8
                  i32.eqz
                  br_if $B21
                  drop
                  local.get $l4
                  local.get $p0
                  i32.load offset=20
                  local.tee $l3
                  i32.load
                  i32.store offset=120
                  local.get $l4
                  local.get $l3
                  i32.load offset=4
                  i32.store offset=124
                  local.get $l4
                  local.get $l3
                  i32.load offset=8
                  i32.store offset=128
                  local.get $l4
                  local.get $l3
                  i32.load offset=12
                  i32.store offset=132
                  local.get $l4
                  local.get $l12
                  i32.load offset=16
                  i32.store offset=104
                  local.get $l4
                  local.get $l12
                  i32.load offset=20
                  i32.store offset=108
                  local.get $l4
                  local.get $l12
                  i32.load offset=24
                  i32.store offset=112
                  local.get $l4
                  local.get $l12
                  i32.load offset=28
                  i32.store offset=116
                  local.get $l4
                  i32.const 120
                  i32.add
                  local.get $l4
                  i32.const 104
                  i32.add
                  local.get $l7
                  i32.load
                  local.get $l7
                  i32.load offset=4
                  local.get $p2
                  local.get $l8
                  call_indirect $__indirect_function_table (type $t9)
                  br $B21
                end
                local.get $l16
                local.get $l20
                i32.eqz
                br_if $B21
                drop
                local.get $l7
                local.get $p0
                i32.load offset=20
                local.get $p2
                local.get $l7
                i32.load
                i32.load offset=4
                call_indirect $__indirect_function_table (type $t3)
              end
              local.tee $l3
              i32.eqz
              br_if $B20
              local.get $p0
              i32.load8_u offset=41
              i32.eqz
              br_if $B20
              local.get $p0
              i32.load offset=12
              local.tee $l3
              local.get $p2
              i64.load align=4
              i64.store offset=4 align=4
              local.get $l3
              local.get $p2
              i32.load offset=8
              i32.store offset=12
              local.get $l3
              local.get $l11
              local.get $l10
              i32.const 48
              i32.mul
              i32.add
              local.tee $p2
              i32.load16_u offset=12
              i32.store16 offset=16
              local.get $l3
              local.get $p2
              f32.load offset=16
              f32.store offset=20
              local.get $l3
              local.get $p2
              f32.load offset=20
              f32.store offset=24
              local.get $l3
              local.get $p2
              f32.load offset=24
              f32.store offset=28
              local.get $l3
              local.get $p2
              f32.load offset=28
              f32.store offset=32
              local.get $l3
              local.get $p2
              f32.load offset=32
              f32.store offset=36
              local.get $l3
              local.get $p2
              f32.load offset=36
              f32.store offset=40
              local.get $l3
              local.get $p2
              f32.load offset=40
              f32.store offset=44
              local.get $l3
              local.get $p2
              i32.load offset=44
              i32.store offset=48
              local.get $p0
              i32.load offset=12
              i32.const 1
              i32.store8 offset=52
              br $B16
            end
            block $B23
              block $B24
                block $B25
                  i32.const 1
                  local.get $l3
                  local.get $p0
                  i32.load8_u offset=40
                  select
                  i32.const 1
                  i32.sub
                  br_table $B25 $B24 $B23
                end
                local.get $p0
                i32.load offset=12
                local.tee $l3
                i32.load offset=60
                local.tee $l7
                i32.eqz
                br_if $B23
                local.get $p0
                i32.load8_u offset=38
                i32.eqz
                br_if $B23
                local.get $p2
                f32.load offset=40
                local.get $p0
                f32.load offset=28
                f32.le
                i32.eqz
                br_if $B23
                block $B26
                  local.get $l3
                  i32.load offset=64
                  local.tee $l8
                  local.get $l7
                  i32.ne
                  br_if $B26
                  local.get $l4
                  local.get $p0
                  i32.load offset=20
                  local.tee $l7
                  i32.load
                  i32.store offset=80
                  local.get $l4
                  local.get $l7
                  i32.load offset=4
                  i32.store offset=84
                  local.get $l4
                  local.get $l7
                  i32.load offset=8
                  i32.store offset=88
                  local.get $l4
                  local.get $l7
                  i32.load offset=12
                  i32.store offset=92
                  local.get $l4
                  local.get $l7
                  i32.load16_u offset=16
                  i32.const 32768
                  i32.or
                  i32.store16 offset=96
                  local.get $l4
                  i32.const 0
                  i32.store16 offset=24
                  local.get $l4
                  i32.const -1
                  i32.store offset=20
                  local.get $l4
                  i64.const 0
                  i64.store offset=12 align=4
                  local.get $l17
                  i64.const 0
                  i64.store align=4
                  local.get $l19
                  i64.const 0
                  i64.store align=4
                  local.get $l9
                  i64.const 0
                  i64.store align=4
                  local.get $l4
                  i32.const 0
                  i32.store offset=72
                  local.get $l4
                  i64.const 0
                  i64.store offset=64
                  local.get $l4
                  i32.const 0
                  i32.store8 offset=60
                  local.get $l4
                  i32.const 2139095039
                  i32.store offset=52
                  local.get $l4
                  i32.const 3211156
                  i32.store offset=8
                  block $B27
                    local.get $p0
                    i32.load8_u offset=39
                    br_if $B27
                    local.get $l3
                    i32.load offset=60
                    i32.eqz
                    br_if $B27
                    local.get $p0
                    i32.load offset=8
                    local.set $l3
                    local.get $p0
                    i32.load offset=4
                    local.set $l7
                    local.get $l4
                    local.get $p0
                    i32.load16_u offset=16
                    i32.store16
                    local.get $l7
                    local.get $l3
                    local.get $l4
                    i32.const 8
                    i32.add
                    local.get $l4
                    i32.const 0
                    local.get $l4
                    i32.const 80
                    i32.add
                    local.get $p0
                    i32.load offset=24
                    local.get $p0
                    i32.load offset=32
                    call $f72259
                    i32.eqz
                    br_if $B27
                    local.get $p0
                    i32.load offset=12
                    local.tee $l3
                    local.get $l14
                    i64.load align=4
                    i64.store offset=4 align=4
                    local.get $l3
                    local.get $l14
                    i32.load offset=8
                    i32.store offset=12
                    local.get $l3
                    local.get $l4
                    i32.load16_u offset=24
                    i32.store16 offset=16
                    local.get $l3
                    local.get $l4
                    f32.load offset=28
                    f32.store offset=20
                    local.get $l3
                    local.get $l4
                    f32.load offset=32
                    f32.store offset=24
                    local.get $l3
                    local.get $l4
                    f32.load offset=36
                    f32.store offset=28
                    local.get $l3
                    local.get $l4
                    f32.load offset=40
                    f32.store offset=32
                    local.get $l3
                    local.get $l4
                    f32.load offset=44
                    f32.store offset=36
                    local.get $l3
                    local.get $l4
                    f32.load offset=48
                    f32.store offset=40
                    local.get $l3
                    local.get $l4
                    f32.load offset=52
                    f32.store offset=44
                    local.get $l3
                    local.get $l4
                    i32.load offset=56
                    i32.store offset=48
                    local.get $p0
                    i32.load offset=12
                    i32.const 1
                    i32.store8 offset=52
                    i32.const 0
                    local.set $l8
                    local.get $l4
                    f32.load offset=52
                    local.set $l23
                    block $B28
                      local.get $p0
                      i32.load offset=12
                      local.tee $l3
                      i32.load offset=64
                      local.tee $l18
                      i32.eqz
                      if $I29
                        i32.const 0
                        local.set $l18
                        br $B28
                      end
                      local.get $l3
                      i32.load offset=56
                      local.set $l13
                      loop $L30
                        block $B31
                          local.get $l23
                          local.get $l13
                          local.get $l8
                          i32.const 48
                          i32.mul
                          i32.add
                          local.tee $l3
                          f32.load offset=40
                          f32.lt
                          if $I32
                            local.get $l3
                            local.get $l13
                            local.get $l18
                            i32.const 1
                            i32.sub
                            local.tee $l18
                            i32.const 48
                            i32.mul
                            i32.add
                            local.tee $l7
                            i64.load align=4
                            i64.store align=4
                            local.get $l3
                            local.get $l7
                            i32.load offset=8
                            i32.store offset=8
                            local.get $l3
                            local.get $l7
                            i32.load16_u offset=12
                            i32.store16 offset=12
                            local.get $l3
                            local.get $l7
                            f32.load offset=16
                            f32.store offset=16
                            local.get $l3
                            local.get $l7
                            f32.load offset=20
                            f32.store offset=20
                            local.get $l3
                            local.get $l7
                            f32.load offset=24
                            f32.store offset=24
                            local.get $l3
                            local.get $l7
                            f32.load offset=28
                            f32.store offset=28
                            local.get $l3
                            local.get $l7
                            f32.load offset=32
                            f32.store offset=32
                            local.get $l3
                            local.get $l7
                            f32.load offset=36
                            f32.store offset=36
                            local.get $l3
                            local.get $l7
                            f32.load offset=40
                            f32.store offset=40
                            local.get $l3
                            local.get $l7
                            i32.load offset=44
                            i32.store offset=44
                            br $B31
                          end
                          local.get $l8
                          i32.const 1
                          i32.add
                          local.set $l8
                        end
                        local.get $l8
                        local.get $l18
                        i32.ne
                        br_if $L30
                      end
                      local.get $p0
                      i32.load offset=12
                      local.set $l3
                      local.get $l4
                      f32.load offset=52
                      local.set $l23
                    end
                    local.get $l3
                    local.get $l18
                    i32.store offset=64
                    local.get $p0
                    local.get $l23
                    f32.store offset=28
                    local.get $p1
                    local.get $l23
                    f32.store
                  end
                  local.get $p0
                  i32.const 1
                  i32.store8 offset=39
                  local.get $p0
                  i32.load offset=12
                  local.tee $l3
                  i32.load offset=64
                  local.tee $l8
                  local.get $l3
                  i32.load offset=60
                  i32.ne
                  br_if $B26
                  local.get $p0
                  local.get $l3
                  local.get $l3
                  i32.load offset=56
                  local.get $l8
                  local.get $l3
                  i32.load
                  i32.load
                  call_indirect $__indirect_function_table (type $t3)
                  local.tee $l3
                  i32.store8 offset=38
                  local.get $l3
                  i32.eqz
                  br_if $B16
                  local.get $p0
                  i32.load offset=12
                  i32.const 0
                  i32.store offset=64
                  local.get $p0
                  i32.load offset=12
                  local.tee $l3
                  i32.load offset=64
                  local.set $l8
                end
                local.get $l3
                local.get $l8
                i32.const 1
                i32.add
                i32.store offset=64
                local.get $l3
                i32.load offset=56
                local.get $l8
                i32.const 48
                i32.mul
                i32.add
                local.tee $l3
                local.get $p2
                i32.load offset=8
                i32.store offset=8
                local.get $l3
                local.get $p2
                i64.load align=4
                i64.store align=4
                local.get $l3
                local.get $p2
                i32.load16_u offset=12
                i32.store16 offset=12
                local.get $l3
                local.get $p2
                f32.load offset=16
                f32.store offset=16
                local.get $l3
                local.get $p2
                f32.load offset=20
                f32.store offset=20
                local.get $l3
                local.get $p2
                f32.load offset=24
                f32.store offset=24
                local.get $l3
                local.get $p2
                f32.load offset=28
                f32.store offset=28
                local.get $l3
                local.get $p2
                f32.load offset=32
                f32.store offset=32
                local.get $l3
                local.get $p2
                f32.load offset=36
                f32.store offset=36
                local.get $l3
                local.get $p2
                f32.load offset=40
                f32.store offset=40
                local.get $l3
                local.get $p2
                i32.load offset=44
                i32.store offset=44
                br $B23
              end
              local.get $p2
              f32.load offset=40
              local.tee $l23
              local.get $p0
              f32.load offset=28
              f32.le
              i32.eqz
              br_if $B23
              local.get $p0
              local.get $l23
              f32.store offset=28
              local.get $p1
              local.get $l23
              f32.store
              local.get $p0
              i32.load offset=12
              local.tee $l3
              local.get $p2
              i64.load align=4
              i64.store offset=4 align=4
              local.get $l3
              local.get $p2
              i32.load offset=8
              i32.store offset=12
              local.get $l3
              local.get $p2
              i32.load16_u offset=12
              i32.store16 offset=16
              local.get $l3
              local.get $p2
              f32.load offset=16
              f32.store offset=20
              local.get $l3
              local.get $p2
              f32.load offset=20
              f32.store offset=24
              local.get $l3
              local.get $p2
              f32.load offset=24
              f32.store offset=28
              local.get $l3
              local.get $p2
              f32.load offset=28
              f32.store offset=32
              local.get $l3
              local.get $p2
              f32.load offset=32
              f32.store offset=36
              local.get $l3
              local.get $p2
              f32.load offset=36
              f32.store offset=40
              local.get $l3
              local.get $p2
              f32.load offset=40
              f32.store offset=44
              local.get $l3
              local.get $p2
              i32.load offset=44
              i32.store offset=48
              local.get $p0
              i32.load offset=12
              i32.const 1
              i32.store8 offset=52
            end
            local.get $l10
            i32.const 1
            i32.add
            local.tee $l10
            local.get $l5
            i32.lt_u
            local.set $l15
            local.get $l5
            local.get $l10
            i32.ne
            br_if $L18
          end
        end
        local.get $l15
        i32.const 1
        i32.xor
        br $B0
      end
      i32.const 1
    end
    local.set $p2
    local.get $l4
    i32.const 224
    i32.add
    global.set $g0
    local.get $p2
    i32.const 1
    i32.and)
