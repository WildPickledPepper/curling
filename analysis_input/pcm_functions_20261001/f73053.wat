  (func $f73053 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 f32) (local $l3 f32) (local $l4 f32) (local $l5 f32) (local $l6 f32) (local $l7 f32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 i32) (local $l19 i32) (local $l20 i32) (local $l21 i32) (local $l22 i32) (local $l23 i64)
    local.get $p1
    i32.load offset=8
    if $I0
      local.get $p1
      i32.load
      local.set $p0
      loop $L1
        local.get $p0
        i32.load offset=24
        local.set $l18
        local.get $p0
        local.tee $l19
        i32.const 12
        i32.add
        local.set $l21
        f32.const 0x0p+0 (;=0;)
        local.set $l4
        f32.const 0x0p+0 (;=0;)
        local.set $l5
        global.get $g0
        i32.const 32
        i32.sub
        local.tee $l20
        global.set $g0
        block $B2
          local.get $l18
          i32.load8_u offset=84
          i32.eqz
          br_if $B2
          block $B3
            i32.const 4748488
            f32.load
            local.get $l19
            f32.load
            local.tee $l2
            f32.neg
            local.get $l2
            local.get $l2
            f32.const 0x0p+0 (;=0;)
            f32.lt
            select
            f32.ne
            br_if $B3
            i32.const 4748492
            f32.load
            local.get $l19
            f32.load offset=4
            local.tee $l2
            f32.neg
            local.get $l2
            local.get $l2
            f32.const 0x0p+0 (;=0;)
            f32.lt
            select
            f32.ne
            br_if $B3
            i32.const 4748496
            f32.load
            local.get $l19
            f32.load offset=8
            local.tee $l2
            f32.neg
            local.get $l2
            local.get $l2
            f32.const 0x0p+0 (;=0;)
            f32.lt
            select
            f32.eq
            br_if $B2
          end
          i32.const 9
          call $f80140
          call $f73714
          i32.const 9
          call $f80140
          call $f73775
          local.get $l18
          i32.load offset=52
          i32.eqz
          br_if $B2
          local.get $l18
          i32.load8_u offset=133
          br_if $B2
          local.get $l18
          f32.load offset=72
          local.set $l3
          block $B4
            block $B5
              block $B6
                block $B7
                  i32.const 0
                  call $f73712
                  local.tee $l22
                  br_table $B7 $B7 $B5 $B6 $B4
                end
                local.get $l19
                f32.load offset=8
                local.set $l2
                local.get $l19
                f32.load offset=4
                local.set $l4
                local.get $l19
                f32.load
                local.set $l5
                br $B4
              end
              local.get $l3
              local.get $l19
              f32.load offset=8
              f32.mul
              local.set $l2
              local.get $l3
              local.get $l19
              f32.load offset=4
              f32.mul
              local.set $l4
              local.get $l3
              local.get $l19
              f32.load
              f32.mul
              local.set $l5
              i32.const 0
              local.set $l22
              br $B4
            end
            local.get $l3
            local.get $l19
            f32.load offset=8
            f32.mul
            local.set $l2
            local.get $l3
            local.get $l19
            f32.load offset=4
            f32.mul
            local.set $l4
            local.get $l3
            local.get $l19
            f32.load
            f32.mul
            local.set $l5
            i32.const 1
            local.set $l22
          end
          local.get $l18
          i32.load offset=52
          local.set $l19
          local.get $l20
          local.get $l2
          f32.store offset=24
          local.get $l20
          local.get $l4
          f32.store offset=20
          local.get $l20
          local.get $l5
          f32.store offset=16
          local.get $l21
          i64.load align=4
          local.set $l23
          local.get $l20
          local.get $l21
          f32.load offset=8
          f32.store offset=8
          local.get $l20
          local.get $l23
          i64.store
          local.get $l20
          i32.const 16
          i32.add
          local.set $l21
          global.get $g0
          i32.const -64
          i32.add
          local.tee $l18
          global.set $g0
          block $B8
            local.get $l22
            i32.const -2
            i32.and
            i32.const 2
            i32.eq
            if $I9
              i32.const 4700888
              i32.load
              i32.const 4
              i32.const 3210117
              i32.const 397
              i32.const 3210782
              i32.const 0
              call $f69760
              br $B8
            end
            local.get $l18
            i32.const 32
            i32.add
            local.get $l19
            local.get $l19
            i32.load
            i32.load offset=76
            call_indirect $__indirect_function_table (type $t1)
            local.get $l18
            local.get $l19
            local.get $l19
            i32.load
            i32.load offset=112
            call_indirect $__indirect_function_table (type $t1)
            local.get $l18
            f32.load offset=56
            local.set $l12
            local.get $l20
            f32.load offset=8
            local.set $l13
            local.get $l21
            f32.load offset=8
            local.set $l9
            local.get $l18
            local.get $l20
            f32.load
            local.get $l18
            f32.load offset=48
            local.get $l18
            f32.load offset=32
            local.tee $l3
            local.get $l3
            local.get $l18
            f32.load offset=16
            local.tee $l2
            local.get $l2
            f32.add
            local.tee $l4
            f32.mul
            local.get $l18
            f32.load offset=20
            local.tee $l2
            local.get $l2
            f32.add
            local.tee $l5
            local.get $l18
            f32.load offset=36
            local.tee $l6
            f32.mul
            f32.add
            local.get $l18
            f32.load offset=24
            local.tee $l2
            local.get $l2
            f32.add
            local.tee $l7
            local.get $l18
            f32.load offset=40
            local.tee $l8
            f32.mul
            f32.add
            local.tee $l10
            f32.mul
            local.get $l4
            local.get $l18
            f32.load offset=44
            local.tee $l2
            local.get $l2
            f32.mul
            f32.const -0x1p-1 (;=-0.5;)
            f32.add
            local.tee $l11
            f32.mul
            local.get $l2
            local.get $l7
            local.get $l6
            f32.mul
            local.get $l5
            local.get $l8
            f32.mul
            f32.sub
            f32.mul
            f32.add
            f32.add
            f32.add
            f32.sub
            local.tee $l14
            local.get $l21
            f32.load offset=4
            local.tee $l15
            f32.mul
            local.get $l20
            f32.load offset=4
            local.get $l18
            f32.load offset=52
            local.get $l6
            local.get $l10
            f32.mul
            local.get $l5
            local.get $l11
            f32.mul
            local.get $l2
            local.get $l4
            local.get $l8
            f32.mul
            local.get $l7
            local.get $l3
            f32.mul
            f32.sub
            f32.mul
            f32.add
            f32.add
            f32.add
            f32.sub
            local.tee $l16
            local.get $l21
            f32.load
            local.tee $l17
            f32.mul
            f32.sub
            f32.store offset=8
            local.get $l18
            local.get $l17
            local.get $l13
            local.get $l12
            local.get $l7
            local.get $l11
            f32.mul
            local.get $l2
            local.get $l5
            local.get $l3
            f32.mul
            local.get $l4
            local.get $l6
            f32.mul
            f32.sub
            f32.mul
            f32.add
            local.get $l8
            local.get $l10
            f32.mul
            f32.add
            f32.add
            f32.sub
            local.tee $l2
            f32.mul
            local.get $l14
            local.get $l9
            f32.mul
            f32.sub
            f32.store offset=4
            local.get $l18
            local.get $l16
            local.get $l9
            f32.mul
            local.get $l2
            local.get $l15
            f32.mul
            f32.sub
            f32.store
            local.get $l19
            local.get $l21
            local.get $l22
            i32.const 1
            local.get $l19
            i32.load
            i32.load offset=188
            call_indirect $__indirect_function_table (type $t4)
            local.get $l19
            local.get $l18
            local.get $l22
            i32.const 1
            local.get $l19
            i32.load
            i32.load offset=192
            call_indirect $__indirect_function_table (type $t4)
          end
          local.get $l18
          i32.const -64
          i32.sub
          global.set $g0
        end
        local.get $l20
        i32.const 32
        i32.add
        global.set $g0
        local.get $p0
        i32.const 28
        i32.add
        local.tee $p0
        local.get $p1
        i32.load
        local.get $p1
        i32.load offset=8
        i32.const 28
        i32.mul
        i32.add
        i32.ne
        br_if $L1
      end
    end)