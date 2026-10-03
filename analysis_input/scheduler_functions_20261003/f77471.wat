  (func $f77471 (type $t7) (param $p0 i32)
    (local $l1 f32) (local $l2 f32) (local $l3 f32) (local $l4 f32) (local $l5 f32) (local $l6 f32) (local $l7 f32) (local $l8 f32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 i32) (local $l17 i32) (local $l18 i32) (local $l19 f64) (local $l20 f64) (local $l21 i64)
    global.get $g0
    i32.const 272
    i32.sub
    local.tee $l9
    global.set $g0
    block $B0
      block $B1
        i32.const 4678216
        i32.load
        i32.eqz
        br_if $B1
        i32.const 4678216
        i32.load
        local.tee $l13
        local.get $l13
        i32.load
        i32.load offset=8
        call_indirect $__indirect_function_table (type $t5)
        i32.eqz
        br_if $B1
        i32.const 4718208
        i32.load
        local.tee $p0
        i32.load offset=8
        i32.const 3
        i32.eq
        br_if $B0
        local.get $p0
        i32.const 3
        i32.store offset=8
        i32.const 4823504
        i32.const 3
        call $f69606
        br $B0
      end
      call $f80340
      i32.const 4718208
      i32.load
      f64.load offset=24
      f64.sub
      f32.demote_f64
      call $f77469
      i32.const 4718208
      i32.load
      i32.load8_u offset=72
      i32.eqz
      if $I2
        call $f77905
        i32.eqz
        br_if $B0
        i32.const 4124502
        i32.load8_u
        i32.eqz
        br_if $B0
      end
      i32.const 4772760
      i32.load
      local.tee $l13
      i32.const 7584
      i32.add
      i32.load8_u
      local.set $l16
      local.get $l13
      local.get $l13
      i32.load
      i32.load offset=864
      call_indirect $__indirect_function_table (type $t5)
      i32.eqz
      if $I3
        local.get $l13
        local.get $l13
        i32.load
        i32.load offset=868
        call_indirect $__indirect_function_table (type $t5)
        drop
        br $B0
      end
      local.get $l16
      i32.eqz
      if $I4
        local.get $l13
        local.get $l13
        i32.load
        i32.load offset=832
        call_indirect $__indirect_function_table (type $t7)
      end
      local.get $l9
      i32.const 8
      i32.add
      i32.const 4772760
      i32.load
      call $f67180
      local.set $l17
      call $f67171
      local.get $p0
      if $I5
        i32.const 0
        call $f80140
        local.tee $p0
        f32.load offset=324
        local.set $l5
        local.get $p0
        f32.load offset=320
        local.set $l4
        local.get $p0
        f32.load offset=316
        local.set $l2
        local.get $p0
        f32.load offset=312
        local.set $l1
        block $B6
          call $f65635
          i32.const 1
          i32.eq
          if $I7
            block $B8
              local.get $l1
              f32.const 0x1.4b5dccp-5 (;=0.04045;)
              f32.le
              if $I9
                local.get $l1
                f32.const 0x1.9d70a4p+3 (;=12.92;)
                f32.div
                local.set $l3
                br $B8
              end
              f32.const 0x1p+0 (;=1;)
              local.set $l3
              local.get $l1
              f32.const 0x1p+0 (;=1;)
              f32.lt
              if $I10
                local.get $l1
                f32.const 0x1.c28f5cp-5 (;=0.055;)
                f32.add
                f32.const 0x1.0e147ap+0 (;=1.055;)
                f32.div
                f32.const 0x1.333334p+1 (;=2.4;)
                call $f16784
                local.set $l3
                br $B8
              end
              local.get $l1
              f32.const 0x1p+0 (;=1;)
              f32.eq
              br_if $B8
              local.get $l1
              f32.const 0x1.19999ap+1 (;=2.2;)
              call $f16784
              local.set $l3
            end
            block $B11
              local.get $l2
              f32.const 0x1.4b5dccp-5 (;=0.04045;)
              f32.le
              if $I12
                local.get $l2
                f32.const 0x1.9d70a4p+3 (;=12.92;)
                f32.div
                local.set $l1
                br $B11
              end
              f32.const 0x1p+0 (;=1;)
              local.set $l1
              local.get $l2
              f32.const 0x1p+0 (;=1;)
              f32.lt
              if $I13
                local.get $l2
                f32.const 0x1.c28f5cp-5 (;=0.055;)
                f32.add
                f32.const 0x1.0e147ap+0 (;=1.055;)
                f32.div
                f32.const 0x1.333334p+1 (;=2.4;)
                call $f16784
                local.set $l1
                br $B11
              end
              local.get $l2
              f32.const 0x1p+0 (;=1;)
              f32.eq
              br_if $B11
              local.get $l2
              f32.const 0x1.19999ap+1 (;=2.2;)
              call $f16784
              local.set $l1
            end
            local.get $l4
            f32.const 0x1.4b5dccp-5 (;=0.04045;)
            f32.le
            if $I14
              local.get $l4
              f32.const 0x1.9d70a4p+3 (;=12.92;)
              f32.div
              local.set $l2
              local.get $l9
              local.get $l3
              f32.store offset=256
              br $B6
            end
            f32.const 0x1p+0 (;=1;)
            local.set $l2
            local.get $l4
            f32.const 0x1p+0 (;=1;)
            f32.lt
            if $I15
              local.get $l4
              f32.const 0x1.c28f5cp-5 (;=0.055;)
              f32.add
              f32.const 0x1.0e147ap+0 (;=1.055;)
              f32.div
              f32.const 0x1.333334p+1 (;=2.4;)
              call $f16784
              local.set $l2
              local.get $l9
              local.get $l3
              f32.store offset=256
              br $B6
            end
            local.get $l4
            f32.const 0x1p+0 (;=1;)
            f32.ne
            if $I16
              local.get $l4
              f32.const 0x1.19999ap+1 (;=2.2;)
              call $f16784
              local.set $l2
            end
            local.get $l9
            local.get $l3
            f32.store offset=256
            br $B6
          end
          local.get $l9
          local.get $l1
          f32.store offset=256
          local.get $l2
          local.set $l1
          local.get $l4
          local.set $l2
        end
        local.get $l9
        local.get $l5
        f32.store offset=268
        local.get $l9
        local.get $l2
        f32.store offset=264
        local.get $l9
        local.get $l1
        f32.store offset=260
        i32.const 7
        local.get $l9
        i32.const 256
        i32.add
        f32.const 0x1p+0 (;=1;)
        i32.const 0
        i32.const 4753524
        i32.load
        call $f77622
      end
      block $B17
        i32.const 4718208
        i32.load
        local.tee $p0
        i32.load offset=8
        i32.const 3
        i32.eq
        br_if $B17
        local.get $p0
        f32.load
        local.set $l2
        call $f80340
        local.set $l19
        i32.const 4718208
        i32.load
        local.tee $p0
        f64.load offset=16
        local.set $l20
        local.get $p0
        f32.load offset=12
        local.set $l4
        global.get $g0
        i32.const 16
        i32.sub
        local.tee $l11
        global.set $g0
        local.get $l9
        i32.const 240
        i32.add
        local.tee $p0
        i32.const 0
        call $f80140
        local.tee $l12
        i32.load offset=320
        i32.store offset=8
        local.get $p0
        local.get $l12
        i64.load offset=312 align=4
        i64.store align=4
        local.get $p0
        i32.const 1065353216
        i32.store offset=12
        block $B18
          block $B19
            block $B20
              block $B21
                i32.const 4678204
                i32.load
                if $I22
                  i32.const 4678204
                  i32.load
                  local.tee $l10
                  local.get $l10
                  i32.load
                  i32.load offset=12
                  call_indirect $__indirect_function_table (type $t5)
                  br_if $B21
                end
                i32.const 4773644
                i32.load
                local.tee $l10
                local.get $l10
                i32.load
                i32.load offset=88
                call_indirect $__indirect_function_table (type $t5)
                local.set $l14
                local.get $l10
                local.get $l10
                i32.load
                i32.load offset=92
                call_indirect $__indirect_function_table (type $t5)
                local.set $l10
                local.get $l11
                local.get $l14
                f32.convert_i32_s
                f32.store offset=8
                local.get $l11
                i64.const 0
                i64.store
                local.get $l11
                local.get $l10
                f32.convert_i32_s
                f32.store offset=12
                local.get $l11
                call $f77470
                br_if $B20
              end
              f32.const 0x0p+0 (;=0;)
              f32.const 0x1p-1 (;=0.5;)
              i32.const 10
              call $f80140
              i32.load8_u offset=108
              select
              local.get $l12
              f32.load offset=252
              call $f65475
              local.tee $l1
              f32.const 0x0p+0 (;=0;)
              f32.gt
              i32.eqz
              br_if $B18
              local.get $p0
              f32.load offset=4
              local.set $l6
              local.get $p0
              f32.load
              local.set $l7
              local.get $l12
              i32.load offset=224
              i32.const 1
              i32.eq
              if $I23
                local.get $p0
                f32.load offset=8
                local.set $l5
                local.get $l7
                local.get $l6
                call $f65475
                local.get $l5
                call $f65475
                local.tee $l3
                f32.const 0x1p-1 (;=0.5;)
                f32.gt
                i32.eqz
                br_if $B18
                local.get $p0
                local.get $l1
                f32.const -0x1p-1 (;=-0.5;)
                local.get $l3
                f32.div
                f32.const 0x1p+0 (;=1;)
                f32.add
                f32.mul
                local.tee $l3
                f32.const 0x0p+0 (;=0;)
                f32.mul
                local.tee $l8
                local.get $l5
                f32.const 0x1p+0 (;=1;)
                local.get $l3
                f32.sub
                local.tee $l1
                f32.mul
                f32.add
                f32.store offset=8
                local.get $p0
                local.get $l8
                local.get $l6
                local.get $l1
                f32.mul
                f32.add
                f32.store offset=4
                local.get $p0
                local.get $l8
                local.get $l7
                local.get $l1
                f32.mul
                f32.add
                f32.store
                local.get $l3
                local.get $l1
                f32.add
                local.set $l1
                br $B19
              end
              local.get $p0
              f32.load offset=8
              local.set $l5
              local.get $l7
              local.get $l6
              call $f65476
              local.get $l5
              call $f65476
              local.tee $l3
              f32.const 0x1p-1 (;=0.5;)
              f32.lt
              i32.eqz
              br_if $B18
              local.get $p0
              local.get $l1
              f32.const -0x1p-1 (;=-0.5;)
              f32.const 0x1p+0 (;=1;)
              local.get $l3
              f32.sub
              f32.div
              f32.const 0x1p+0 (;=1;)
              f32.add
              f32.mul
              local.tee $l1
              local.get $l5
              f32.const 0x1p+0 (;=1;)
              local.get $l1
              f32.sub
              local.tee $l3
              f32.mul
              f32.add
              f32.store offset=8
              local.get $p0
              local.get $l1
              local.get $l6
              local.get $l3
              f32.mul
              f32.add
              f32.store offset=4
              local.get $p0
              local.get $l1
              local.get $l7
              local.get $l3
              f32.mul
              f32.add
              f32.store
              local.get $l1
              local.get $l3
              f32.add
              local.set $l1
              br $B19
            end
            i32.const 4718156
            f32.load
            local.set $l1
            i32.const 4718144
            i64.load align=4
            local.set $l21
            local.get $p0
            i32.const 4718152
            f32.load
            f32.store offset=8
            local.get $p0
            local.get $l21
            i64.store align=4
          end
          local.get $p0
          local.get $l1
          f32.store offset=12
        end
        local.get $l11
        i32.const 16
        i32.add
        global.set $g0
        block $B24
          call $f65635
          i32.const 1
          i32.eq
          if $I25
            block $B26
              local.get $l9
              f32.load offset=240
              local.tee $l1
              f32.const 0x1.4b5dccp-5 (;=0.04045;)
              f32.le
              if $I27
                local.get $l1
                f32.const 0x1.9d70a4p+3 (;=12.92;)
                f32.div
                local.set $l5
                br $B26
              end
              f32.const 0x1p+0 (;=1;)
              local.set $l5
              local.get $l1
              f32.const 0x1p+0 (;=1;)
              f32.lt
              if $I28
                local.get $l1
                f32.const 0x1.c28f5cp-5 (;=0.055;)
                f32.add
                f32.const 0x1.0e147ap+0 (;=1.055;)
                f32.div
                f32.const 0x1.333334p+1 (;=2.4;)
                call $f16784
                local.set $l5
                br $B26
              end
              local.get $l1
              f32.const 0x1p+0 (;=1;)
              f32.eq
              br_if $B26
              local.get $l1
              f32.const 0x1.19999ap+1 (;=2.2;)
              call $f16784
              local.set $l5
            end
            block $B29
              local.get $l9
              f32.load offset=244
              local.tee $l1
              f32.const 0x1.4b5dccp-5 (;=0.04045;)
              f32.le
              if $I30
                local.get $l1
                f32.const 0x1.9d70a4p+3 (;=12.92;)
                f32.div
                local.set $l3
                br $B29
              end
              f32.const 0x1p+0 (;=1;)
              local.set $l3
              local.get $l1
              f32.const 0x1p+0 (;=1;)
              f32.lt
              if $I31
                local.get $l1
                f32.const 0x1.c28f5cp-5 (;=0.055;)
                f32.add
                f32.const 0x1.0e147ap+0 (;=1.055;)
                f32.div
                f32.const 0x1.333334p+1 (;=2.4;)
                call $f16784
                local.set $l3
                br $B29
              end
              local.get $l1
              f32.const 0x1p+0 (;=1;)
              f32.eq
              br_if $B29
              local.get $l1
              f32.const 0x1.19999ap+1 (;=2.2;)
              call $f16784
              local.set $l3
            end
            block $B32
              local.get $l9
              f32.load offset=248
              local.tee $l1
              f32.const 0x1.4b5dccp-5 (;=0.04045;)
              f32.le
              if $I33
                local.get $l1
                f32.const 0x1.9d70a4p+3 (;=12.92;)
                f32.div
                local.set $l6
                br $B32
              end
              f32.const 0x1p+0 (;=1;)
              local.set $l6
              local.get $l1
              f32.const 0x1p+0 (;=1;)
              f32.lt
              if $I34
                local.get $l1
                f32.const 0x1.c28f5cp-5 (;=0.055;)
                f32.add
                f32.const 0x1.0e147ap+0 (;=1.055;)
                f32.div
                f32.const 0x1.333334p+1 (;=2.4;)
                call $f16784
                local.set $l6
                br $B32
              end
              local.get $l1
              f32.const 0x1p+0 (;=1;)
              f32.eq
              br_if $B32
              local.get $l1
              f32.const 0x1.19999ap+1 (;=2.2;)
              call $f16784
              local.set $l6
            end
            local.get $l9
            local.get $l9
            f32.load offset=252
            f32.store offset=268
            local.get $l9
            local.get $l6
            f32.store offset=264
            local.get $l9
            local.get $l3
            f32.store offset=260
            local.get $l9
            local.get $l5
            f32.store offset=256
            br $B24
          end
          local.get $l9
          local.get $l9
          i64.load offset=248
          i64.store offset=264
          local.get $l9
          local.get $l9
          i64.load offset=240
          i64.store offset=256
        end
        block $B35
          i32.const 4718208
          i32.load
          local.tee $p0
          i32.load offset=8
          i32.const 2
          i32.ne
          br_if $B35
          local.get $p0
          i32.load8_u offset=73
          br_if $B35
          local.get $l9
          f32.const 0x0p+0 (;=0;)
          call $f80340
          i32.const 4718208
          i32.load
          f64.load offset=24
          f64.sub
          f32.demote_f64
          f32.const 0x1p-1 (;=0.5;)
          f32.min
          local.tee $l1
          local.get $l1
          f32.add
          local.tee $l1
          f32.const 0x1p+0 (;=1;)
          f32.min
          local.get $l1
          f32.const 0x0p+0 (;=0;)
          f32.lt
          select
          local.tee $l1
          local.get $l1
          f32.const -0x1p+1 (;=-2;)
          f32.mul
          f32.mul
          local.get $l1
          f32.mul
          local.get $l1
          local.get $l1
          f32.const 0x1.8p+1 (;=3;)
          f32.mul
          f32.mul
          f32.add
          local.tee $l1
          f32.const 0x0p+0 (;=0;)
          f32.mul
          local.get $l9
          f32.load offset=268
          f32.const 0x1p+0 (;=1;)
          local.get $l1
          f32.sub
          f32.mul
          f32.add
          f32.store offset=268
        end
        i32.const 4773644
        i32.load
        local.tee $p0
        local.get $p0
        i32.load
        i32.load offset=88
        call_indirect $__indirect_function_table (type $t5)
        local.set $l10
        local.get $p0
        local.get $p0
        i32.load
        i32.load offset=92
        call_indirect $__indirect_function_table (type $t5)
        local.set $p0
        local.get $l9
        local.get $l10
        f32.convert_i32_s
        f32.store offset=248
        local.get $l9
        i64.const 0
        i64.store offset=240
        local.get $l9
        local.get $p0
        f32.convert_i32_s
        f32.store offset=252
        local.get $l9
        i32.const 240
        i32.add
        call $f77470
        local.set $p0
        i32.const 4718208
        i32.load
        local.get $p0
        i32.store offset=48
        block $B36
          local.get $p0
          i32.eqz
          if $I37
            i32.const 4773644
            i32.load
            local.tee $p0
            local.get $p0
            i32.load
            i32.load offset=88
            call_indirect $__indirect_function_table (type $t5)
            local.set $l10
            local.get $p0
            local.get $p0
            i32.load
            i32.load offset=92
            call_indirect $__indirect_function_table (type $t5)
            local.set $p0
            local.get $l9
            local.get $l10
            f32.convert_i32_s
            f32.store offset=232
            local.get $l9
            i64.const 0
            i64.store offset=224
            local.get $l9
            local.get $p0
            f32.convert_i32_s
            f32.store offset=236
            i32.const 4773508
            i32.load
            local.set $p0
            local.get $l9
            i64.const 0
            i64.store offset=208
            local.get $l9
            i64.const 4575657222473777152
            i64.store offset=216
            local.get $l9
            i32.const 224
            i32.add
            local.get $p0
            local.get $l9
            i32.const 256
            i32.add
            local.get $l9
            i32.const 208
            i32.add
            call $f77472
            br $B36
          end
          local.get $l9
          i32.const 224
          i32.add
          local.set $l12
          local.get $l9
          i32.const 240
          i32.add
          local.set $l14
          global.get $g0
          i32.const 32
          i32.sub
          local.tee $l10
          global.set $g0
          local.get $l10
          i32.const 8
          i32.add
          i32.const 0
          call $f80140
          i32.const 216
          i32.add
          local.tee $l11
          call $f66122
          local.get $l10
          i32.load offset=8
          local.tee $p0
          if $I38 (result i32)
            local.get $l10
            local.get $p0
            i32.store offset=28
            block $B39
              block $B40
                i32.const 4782060
                i32.load
                local.tee $p0
                i32.eqz
                br_if $B40
                local.get $l10
                i32.const 16
                i32.add
                local.get $p0
                local.get $l10
                i32.const 28
                i32.add
                call $f66830
                local.get $l10
                i32.load offset=16
                local.tee $l15
                i32.const 4782060
                i32.load
                local.tee $p0
                i32.load
                local.get $p0
                i32.load offset=4
                i32.const 3
                i32.mul
                i32.add
                i32.const 12
                i32.add
                i32.eq
                br_if $B40
                local.get $l15
                i32.load offset=8
                local.tee $p0
                br_if $B39
              end
              local.get $l10
              i32.load offset=8
              call $f80110
              local.set $p0
            end
            local.get $p0
            i32.const 0
            i32.ne
          else
            i32.const 0
          end
          local.set $l15
          i32.const 4773644
          i32.load
          local.tee $p0
          local.get $p0
          i32.load
          i32.load offset=88
          call_indirect $__indirect_function_table (type $t5)
          local.set $l18
          local.get $p0
          local.get $p0
          i32.load
          i32.load offset=92
          call_indirect $__indirect_function_table (type $t5)
          local.set $p0
          block $B41 (result f32)
            block $B42 (result f32)
              block $B43
                local.get $l15
                i32.eqz
                br_if $B43
                local.get $l18
                f32.convert_i32_s
                local.get $p0
                f32.convert_i32_s
                f32.lt
                i32.eqz
                br_if $B43
                local.get $l11
                f32.load offset=32
                br $B42
              end
              local.get $l11
              f32.load offset=28
            end
            local.tee $l1
            local.get $l14
            f32.load offset=12
            local.tee $l6
            f32.mul
            local.tee $l3
            local.get $l14
            f32.load offset=8
            local.tee $l5
            f32.lt
            if $I44
              f32.const 0x1p+0 (;=1;)
              local.set $l3
              f32.const 0x1p-1 (;=0.5;)
              f32.const 0x1p-1 (;=0.5;)
              f32.const 0x1p+0 (;=1;)
              local.get $l5
              local.get $l1
              f32.div
              local.tee $l1
              local.get $l6
              f32.sub
              local.get $l1
              f32.div
              f32.sub
              f32.const 0x1p-1 (;=0.5;)
              f32.mul
              f32.sub
              f32.sub
              local.tee $l1
              local.get $l1
              f32.add
              br $B41
            end
            f32.const 0x1p-1 (;=0.5;)
            f32.const 0x1p-1 (;=0.5;)
            f32.const 0x1p+0 (;=1;)
            local.get $l3
            local.get $l5
            f32.sub
            local.get $l3
            f32.div
            f32.sub
            f32.const 0x1p-1 (;=0.5;)
            f32.mul
            f32.sub
            f32.sub
            local.tee $l3
            local.get $l3
            f32.add
            local.set $l3
            f32.const 0x1p+0 (;=1;)
          end
          local.set $l1
          local.get $l10
          i32.const 8
          i32.add
          i32.const 0
          call $f80140
          i32.const 216
          i32.add
          local.tee $p0
          call $f66122
          block $B45 (result i32)
            block $B46
              local.get $l10
              i32.load offset=8
              local.tee $l11
              i32.eqz
              br_if $B46
              local.get $l10
              local.get $l11
              i32.store offset=28
              block $B47
                block $B48
                  i32.const 4782060
                  i32.load
                  local.tee $l11
                  i32.eqz
                  br_if $B48
                  local.get $l10
                  i32.const 16
                  i32.add
                  local.get $l11
                  local.get $l10
                  i32.const 28
                  i32.add
                  call $f66830
                  local.get $l10
                  i32.load offset=16
                  local.tee $l15
                  i32.const 4782060
                  i32.load
                  local.tee $l11
                  i32.load
                  local.get $l11
                  i32.load offset=4
                  i32.const 3
                  i32.mul
                  i32.add
                  i32.const 12
                  i32.add
                  i32.eq
                  br_if $B48
                  local.get $l15
                  i32.load offset=8
                  local.tee $l11
                  br_if $B47
                end
                local.get $l10
                i32.load offset=8
                call $f80110
                local.set $l11
              end
              local.get $l11
              i32.eqz
              br_if $B46
              local.get $l14
              f32.load offset=8
              local.get $l14
              f32.load offset=12
              f32.lt
              i32.eqz
              br_if $B46
              local.get $p0
              i32.const 56
              i32.add
              br $B45
            end
            local.get $p0
            i32.const 40
            i32.add
          end
          local.set $p0
          local.get $l12
          i32.const 8
          i32.add
          local.tee $l14
          local.get $p0
          i64.load offset=8 align=4
          i64.store align=4
          local.get $l12
          local.get $p0
          i64.load align=4
          i64.store align=4
          local.get $l14
          local.get $l3
          local.get $l14
          f32.load
          local.tee $l5
          f32.mul
          local.tee $l3
          f32.store
          local.get $l12
          local.get $l1
          local.get $l12
          f32.load offset=12
          local.tee $l6
          f32.mul
          local.tee $l1
          f32.store offset=12
          local.get $l12
          local.get $l5
          local.get $l3
          f32.sub
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          local.get $l12
          f32.load
          f32.add
          f32.store
          local.get $l12
          local.get $l6
          local.get $l1
          f32.sub
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          local.get $l12
          f32.load offset=4
          f32.add
          f32.store offset=4
          local.get $l10
          i32.const 32
          i32.add
          global.set $g0
          local.get $l9
          local.get $l4
          local.get $l19
          local.get $l20
          f64.sub
          f32.demote_f64
          f32.sub
          local.get $l2
          f32.const 0x1.99999ap-5 (;=0.05;)
          f32.mul
          local.tee $l2
          f32.mul
          f32.const 0x1p+0 (;=1;)
          f32.add
          local.get $l4
          local.get $l2
          f32.mul
          f32.const 0x1p+0 (;=1;)
          f32.add
          f32.div
          local.tee $l4
          local.get $l9
          f32.load offset=236
          local.tee $l2
          f32.mul
          local.tee $l1
          f32.store offset=236
          local.get $l9
          local.get $l9
          f32.load offset=228
          local.get $l2
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          f32.add
          local.get $l1
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          f32.sub
          f32.store offset=228
          local.get $l9
          local.get $l4
          local.get $l9
          f32.load offset=232
          local.tee $l2
          f32.mul
          local.tee $l4
          f32.store offset=232
          local.get $l9
          local.get $l9
          f32.load offset=224
          local.get $l2
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          f32.add
          local.get $l4
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          f32.sub
          f32.store offset=224
          local.get $l9
          i32.const 240
          i32.add
          i32.const 4718208
          i32.load
          i32.load offset=48
          local.get $l9
          i32.const 256
          i32.add
          local.get $l9
          i32.const 224
          i32.add
          call $f77472
        end
        i32.const 4718208
        i32.load
        i32.load offset=8
        i32.const 1
        i32.ne
        br_if $B17
        i32.const 0
        call $f80140
        local.set $l10
        i32.const 4773644
        i32.load
        local.tee $p0
        local.get $p0
        i32.load
        i32.load offset=88
        call_indirect $__indirect_function_table (type $t5)
        local.set $l11
        local.get $l9
        local.get $p0
        local.get $p0
        i32.load
        i32.load offset=92
        call_indirect $__indirect_function_table (type $t5)
        f32.convert_i32_s
        local.tee $l2
        local.get $l11
        f32.convert_i32_s
        local.tee $l1
        local.get $l1
        local.get $l2
        f32.gt
        select
        local.tee $l4
        local.get $l1
        f32.add
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        local.tee $l5
        f32.store offset=264
        local.get $l9
        local.get $l4
        local.get $l2
        f32.add
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        local.tee $l3
        f32.store offset=268
        local.get $l9
        local.get $l1
        local.get $l4
        f32.sub
        f32.const 0x1p-2 (;=0.25;)
        f32.mul
        f32.const 0x0p+0 (;=0;)
        f32.add
        local.tee $l1
        f32.store offset=256
        local.get $l9
        local.get $l2
        local.get $l4
        f32.sub
        f32.const 0x1p-2 (;=0.25;)
        f32.mul
        f32.const 0x0p+0 (;=0;)
        f32.add
        local.tee $l6
        f32.store offset=260
        local.get $l10
        i32.const 216
        i32.add
        local.tee $l12
        i32.const 4718208
        i32.load
        i32.load offset=56
        local.tee $p0
        call $f77428
        local.set $l11
        i32.const 4718208
        i32.load
        local.set $l10
        local.get $l11
        if $I49
          local.get $l10
          i32.load offset=52
          local.set $p0
        end
        local.get $l10
        i32.load8_u offset=74
        if $I50
          local.get $l9
          local.get $l5
          f32.store offset=248
          local.get $l9
          local.get $l2
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          local.tee $l2
          f32.store offset=252
          local.get $l9
          local.get $l2
          f32.store offset=244
          local.get $l9
          local.get $l1
          f32.store offset=240
          local.get $l9
          i32.const 240
          i32.add
          local.get $p0
          f32.const 0x1.99999ap-1 (;=0.8;)
          i32.const 1
          call $f80340
          f32.demote_f64
          i32.const 4718208
          i32.load
          local.tee $l10
          f64.load offset=24
          local.tee $l19
          f32.demote_f64
          local.get $l19
          local.get $l10
          f64.load offset=32
          f64.add
          f32.demote_f64
          i32.const 1
          call $f77473
          local.get $l9
          local.get $l5
          f32.store offset=232
          local.get $l9
          local.get $l1
          local.get $l5
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          local.tee $l2
          f32.add
          local.get $l2
          f32.sub
          f32.store offset=224
          local.get $l9
          local.get $l3
          f32.const 0x1p-2 (;=0.25;)
          f32.mul
          local.tee $l2
          local.get $l4
          f32.const 0x1.47ae14p-2 (;=0.32;)
          f32.mul
          local.get $l2
          f32.div
          f32.mul
          local.tee $l4
          f32.store offset=236
          local.get $l9
          local.get $l3
          f32.const 0x1.333334p-3 (;=0.15;)
          f32.mul
          local.get $l6
          f32.add
          local.get $l2
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          f32.add
          local.get $l4
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          f32.sub
          f32.store offset=228
          local.get $l9
          i32.const 224
          i32.add
          i32.const 4718208
          i32.load
          i32.load offset=52
          f32.const 0x1p+0 (;=1;)
          i32.const 0
          call $f80340
          f32.demote_f64
          i32.const 4718208
          i32.load
          local.tee $p0
          f64.load offset=16
          local.tee $l19
          f32.demote_f64
          local.get $l19
          local.get $p0
          f32.load offset=12
          f64.promote_f32
          f64.add
          f32.demote_f64
          i32.const 0
          call $f77473
          br $B17
        end
        f32.const 0x1.99999ap-1 (;=0.8;)
        local.set $l2
        block $B51
          local.get $l12
          call $f77427
          i32.eqz
          br_if $B51
          local.get $l12
          local.get $p0
          call $f77428
          i32.eqz
          br_if $B51
          local.get $l9
          local.get $l1
          local.get $l5
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          local.tee $l2
          f32.add
          local.get $l2
          f32.sub
          f32.store offset=256
          local.get $l9
          local.get $l3
          local.get $l4
          f32.const 0x1.47ae14p-2 (;=0.32;)
          f32.mul
          local.get $l3
          f32.div
          f32.mul
          local.tee $l4
          f32.store offset=268
          local.get $l9
          local.get $l6
          local.get $l3
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          f32.add
          local.get $l4
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          f32.sub
          f32.store offset=260
          f32.const 0x1p+0 (;=1;)
          local.set $l2
        end
        local.get $l9
        i32.const 256
        i32.add
        local.get $p0
        local.get $l2
        i32.const 1
        call $f80340
        f32.demote_f64
        i32.const 4718208
        i32.load
        local.tee $l10
        f64.load offset=24
        local.tee $l19
        f32.demote_f64
        local.get $l19
        local.get $l10
        f64.load offset=32
        f64.add
        f32.demote_f64
        i32.const 0
        call $f77473
      end
      local.get $l16
      i32.eqz
      if $I52
        local.get $l13
        local.get $l13
        i32.load
        i32.load offset=836
        call_indirect $__indirect_function_table (type $t7)
      end
      local.get $l13
      i32.const 0
      local.get $l13
      i32.load
      i32.load offset=56
      call_indirect $__indirect_function_table (type $t1)
      i32.const 4718208
      i32.load
      i32.load8_u offset=72
      i32.eqz
      if $I53
        local.get $l13
        i32.const -1
        local.get $l13
        i32.load
        i32.load offset=848
        call_indirect $__indirect_function_table (type $t1)
      end
      local.get $l17
      call $f67181
    end
    local.get $l9
    i32.const 272
    i32.add
    global.set $g0)
