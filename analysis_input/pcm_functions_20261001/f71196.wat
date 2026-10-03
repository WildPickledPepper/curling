  (func $f71196 (type $t2) (param $p0 i32) (param $p1 i32) (param $p2 i32)
    (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 i32) (local $l17 i32) (local $l18 i32) (local $l19 i32) (local $l20 i32)
    local.get $p0
    i32.load offset=336
    call $f69738
    local.tee $l6
    i32.eqz
    if $I0
      call $f69753
      local.tee $l3
      i32.const 12195
      i32.const 3152658
      i32.const 3150980
      i32.const 4700888
      i32.load
      local.tee $l6
      local.get $l6
      i32.load
      i32.load offset=20
      call_indirect $__indirect_function_table (type $t5)
      select
      i32.const 3152590
      i32.const 82
      local.get $l3
      i32.load
      i32.load offset=8
      call_indirect $__indirect_function_table (type $t9)
      local.tee $l6
      i32.const 19
      i32.add
      i32.const -16
      i32.and
      local.tee $l3
      i32.const 4
      i32.sub
      local.get $l3
      local.get $l6
      i32.sub
      i32.store
      local.get $l3
      local.get $p0
      i32.load offset=340
      call $f71150
      local.set $l6
    end
    local.get $l6
    i32.const 12052
    i32.add
    i32.const 0
    i32.store
    local.get $l6
    local.get $p1
    i32.load offset=144
    local.tee $l3
    local.get $l6
    i32.const 12056
    i32.add
    i32.load
    i32.const 2147483647
    i32.and
    i32.gt_u
    if $I1 (result i32)
      local.get $l6
      i32.const 12048
      i32.add
      local.get $l3
      call $f71197
      local.get $p1
      i32.load offset=144
    else
      local.get $l3
    end
    i32.store offset=12052
    local.get $l6
    i32.const 12064
    i32.add
    i32.const 0
    i32.store
    local.get $l6
    local.get $p1
    i32.load offset=144
    local.tee $l3
    local.get $l6
    i32.const 12068
    i32.add
    i32.load
    i32.const 2147483647
    i32.and
    i32.gt_u
    if $I2 (result i32)
      local.get $l6
      i32.const 12060
      i32.add
      local.get $l3
      call $f71197
      local.get $p1
      i32.load offset=144
    else
      local.get $l3
    end
    i32.store offset=12064
    block $B3
      local.get $p0
      local.get $p0
      i32.load offset=112
      i32.const 2
      i32.shl
      i32.add
      i32.load offset=484
      local.tee $l3
      local.get $p1
      local.get $l6
      i32.load offset=12048
      local.get $l6
      i32.load offset=12060
      local.get $l3
      i32.load
      i32.load offset=12
      call_indirect $__indirect_function_table (type $t8)
      local.tee $l4
      local.get $p1
      i32.load offset=72
      i32.le_s
      br_if $B3
      local.get $p1
      i32.load offset=72
      local.get $l4
      i32.ge_s
      br_if $B3
      i32.const 30000
      local.set $l3
      loop $L4
        local.get $p1
        i32.load offset=72
        local.get $l4
        i32.ge_s
        br_if $B3
        local.get $l3
        i32.const 1
        i32.sub
        local.tee $l3
        br_if $L4
        i32.const 10000
        local.set $l3
        br $L4
      end
      unreachable
    end
    i32.const 128
    local.set $l8
    local.get $p1
    i32.const 92
    i32.add
    local.tee $l15
    i32.const 128
    call $f1708
    local.set $l3
    local.get $p1
    i32.load offset=64
    local.set $l16
    local.get $p1
    i32.load offset=52
    local.set $l17
    local.get $p1
    i32.load offset=16
    local.set $l14
    local.get $l3
    i32.const 128
    i32.sub
    local.tee $l3
    local.get $p1
    i32.load offset=28
    local.tee $l9
    i32.lt_s
    if $I5
      local.get $p1
      i32.load offset=24
      local.set $l10
      loop $L6
        local.get $l8
        local.get $l9
        local.get $l3
        i32.sub
        local.tee $l4
        i32.const 128
        local.get $l4
        i32.const 128
        i32.lt_s
        select
        local.tee $l5
        i32.sub
        local.set $l8
        local.get $l4
        i32.const 0
        i32.gt_s
        if $I7
          local.get $l5
          i32.const 1
          local.get $l5
          i32.const 1
          i32.gt_s
          select
          local.tee $l12
          i32.const 1
          i32.and
          local.set $l13
          local.get $l5
          i32.const 2
          i32.ge_s
          if $I8
            local.get $l12
            i32.const 2147483646
            i32.and
            local.set $l5
            loop $L9
              local.get $l10
              local.get $l3
              i32.const 56
              i32.mul
              i32.add
              local.tee $l4
              i32.load
              i32.load offset=24
              i32.const 2
              i32.shl
              i32.const 4701972
              i32.add
              i32.load
              local.tee $l7
              if $I10
                local.get $l4
                local.get $p0
                f32.load offset=52
                local.get $l7
                call_indirect $__indirect_function_table (type $t21)
              end
              local.get $l4
              i32.const 56
              i32.add
              local.tee $l4
              i32.load
              i32.load offset=24
              i32.const 2
              i32.shl
              i32.const 4701972
              i32.add
              i32.load
              local.tee $l7
              if $I11
                local.get $l4
                local.get $p0
                f32.load offset=52
                local.get $l7
                call_indirect $__indirect_function_table (type $t21)
              end
              local.get $l3
              i32.const 2
              i32.add
              local.set $l3
              local.get $l5
              i32.const 2
              i32.sub
              local.tee $l5
              br_if $L9
            end
          end
          local.get $l11
          local.get $l12
          i32.add
          local.set $l11
          local.get $l13
          if $I12 (result i32)
            local.get $l10
            local.get $l3
            i32.const 56
            i32.mul
            i32.add
            local.tee $l4
            i32.load
            i32.load offset=24
            i32.const 2
            i32.shl
            i32.const 4701972
            i32.add
            i32.load
            local.tee $l5
            if $I13
              local.get $l4
              local.get $p0
              f32.load offset=52
              local.get $l5
              call_indirect $__indirect_function_table (type $t21)
            end
            local.get $l3
            i32.const 1
            i32.add
          else
            local.get $l3
          end
          local.set $l3
        end
        local.get $l8
        i32.eqz
        if $I14
          i32.const 128
          local.set $l8
          local.get $l15
          i32.const 128
          call $f1708
          i32.const 128
          i32.sub
          local.set $l3
        end
        local.get $l3
        local.get $l9
        i32.lt_s
        br_if $L6
      end
    end
    local.get $l3
    local.get $l9
    i32.sub
    local.tee $l7
    local.get $l14
    i32.lt_s
    if $I15
      i32.const -128
      local.get $l9
      i32.sub
      local.set $l18
      local.get $p1
      i32.load offset=12
      local.get $p1
      i32.load offset=20
      i32.const 112
      i32.mul
      i32.add
      i32.const 112
      i32.add
      local.set $l19
      local.get $p1
      i32.load offset=8
      local.set $l20
      loop $L16
        i32.const 0
        local.set $l9
        local.get $l14
        local.get $l7
        i32.sub
        local.tee $l3
        local.get $l8
        local.get $l3
        local.get $l8
        i32.lt_s
        select
        local.tee $l13
        i32.const 0
        i32.gt_s
        if $I17
          loop $L18
            local.get $l17
            local.get $l7
            i32.const 5
            i32.shl
            local.tee $l3
            i32.add
            local.tee $l10
            local.get $l10
            i32.const 16
            i32.add
            local.get $l3
            local.get $l20
            i32.add
            local.get $l19
            local.get $l7
            i32.const 112
            i32.mul
            i32.add
            local.tee $l4
            local.get $p0
            f32.load offset=52
            call $f71198
            local.get $l16
            local.get $l7
            i32.const 2
            i32.shl
            i32.add
            local.tee $l8
            i32.load
            local.tee $l5
            local.get $l5
            i32.load offset=36
            local.tee $l3
            f32.load
            f32.store
            local.get $l5
            local.get $l3
            f32.load offset=4
            f32.store offset=4
            local.get $l5
            local.get $l3
            f32.load offset=8
            f32.store offset=8
            local.get $l5
            local.get $l3
            f32.load offset=12
            f32.store offset=12
            local.get $l5
            local.get $l3
            f32.load offset=16
            f32.store offset=16
            local.get $l5
            local.get $l3
            i32.const 20
            i32.add
            local.tee $l12
            f32.load
            f32.store offset=20
            local.get $l5
            local.get $l3
            i32.const 24
            i32.add
            local.tee $l5
            f32.load
            f32.store offset=24
            local.get $l3
            local.get $l4
            f32.load offset=80
            f32.store
            local.get $l3
            local.get $l4
            f32.load offset=84
            f32.store offset=4
            local.get $l3
            local.get $l4
            f32.load offset=88
            f32.store offset=8
            local.get $l3
            local.get $l4
            f32.load offset=92
            f32.store offset=12
            local.get $l3
            local.get $l4
            f32.load offset=96
            f32.store offset=16
            local.get $l12
            local.get $l4
            f32.load offset=100
            f32.store
            local.get $l5
            local.get $l4
            f32.load offset=104
            f32.store
            local.get $l3
            local.get $l4
            f32.load
            f32.store offset=64
            local.get $l3
            local.get $l4
            f32.load offset=4
            f32.store offset=68
            local.get $l3
            local.get $l4
            f32.load offset=8
            f32.store offset=72
            local.get $l3
            local.get $l4
            f32.load offset=16
            f32.store offset=80
            local.get $l3
            local.get $l4
            f32.load offset=20
            f32.store offset=84
            local.get $l3
            local.get $l4
            f32.load offset=24
            f32.store offset=88
            local.get $l8
            i32.load
            local.tee $l3
            local.get $p0
            f32.load offset=52
            local.get $p0
            f32.load offset=56
            local.get $p0
            i32.load8_u offset=64
            local.get $p0
            i32.load8_u offset=66
            local.get $l10
            local.get $p2
            i32.load offset=100
            local.get $p2
            i32.load offset=204
            local.get $l4
            i32.load offset=72
            i32.const 2
            i32.shl
            i32.add
            i32.load
            i32.const 2
            i32.shl
            i32.add
            i32.load
            i32.const 0
            i32.ne
            call $f71199
            f32.const 0x0p+0 (;=0;)
            f32.eq
            if $I19
              local.get $l3
              i64.const 0
              i64.store offset=64 align=4
              local.get $l3
              i64.const 0
              i64.store offset=48 align=4
              local.get $l3
              i32.const 0
              i32.store offset=72
              local.get $l3
              i32.const 0
              i32.store offset=56
              local.get $l3
              local.get $l3
              i32.load16_u offset=28
              i32.const 16
              i32.or
              i32.store16 offset=28
            end
            local.get $l7
            i32.const 1
            i32.add
            local.set $l7
            local.get $l9
            i32.const 1
            i32.add
            local.tee $l9
            local.get $l13
            i32.ne
            br_if $L18
          end
          local.get $l11
          local.get $l13
          i32.add
          local.set $l11
        end
        i32.const 128
        local.set $l8
        local.get $l14
        local.get $l15
        i32.const 128
        call $f1708
        local.get $l18
        i32.add
        local.tee $l7
        i32.gt_s
        br_if $L16
      end
    end
    local.get $p1
    i32.const 96
    i32.add
    local.get $l11
    call $f1708
    drop
    local.get $p0
    i32.load offset=336
    local.get $l6
    call $f69737)
