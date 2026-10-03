  (func $f71438 (type $t15) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 i32)
    (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i64) (local $l16 i64) (local $l17 i64) (local $l18 i64)
    local.get $p2
    if $I0
      local.get $p3
      i32.const 144
      i32.add
      i64.extend_i32_u
      i64.const 1
      i64.sub
      local.set $l17
      loop $L1
        local.get $p2
        local.get $l8
        i32.const 1
        i32.add
        local.tee $l13
        i32.gt_u
        if $I2
          local.get $l17
          local.get $p1
          local.get $l13
          i32.const 2
          i32.shl
          i32.add
          i32.load
          local.tee $l7
          i64.extend_i32_u
          local.tee $l15
          i64.add
          i64.const 6
          i64.shr_u
          local.get $l15
          i64.const 6
          i64.shr_u
          i64.sub
          i64.const 1
          i64.add
          local.set $l15
          loop $L3
            local.get $l7
            i32.const -64
            i32.sub
            local.set $l7
            local.get $l15
            i64.const 1
            i64.sub
            local.tee $l15
            i64.const 0
            i64.ne
            br_if $L3
          end
        end
        block $B4
          local.get $p0
          i32.load offset=2384
          local.tee $l7
          i32.load offset=12
          local.get $l7
          i32.load offset=8
          i32.const 12
          i32.mul
          i32.add
          local.tee $l9
          i32.load offset=4
          local.tee $l10
          if $I5
            local.get $l9
            local.get $l10
            i32.load
            i32.store offset=4
            br $B4
          end
          block $B6
            local.get $l9
            i32.load offset=8
            local.tee $l10
            local.get $l7
            i32.load
            i32.eq
            br_if $B6
            local.get $l7
            i32.load offset=4
            local.set $l11
            local.get $l9
            local.get $l10
            i32.const 1
            i32.add
            i32.store offset=8
            local.get $l9
            i32.load
            local.tee $l9
            i32.eqz
            br_if $B6
            local.get $l9
            local.get $l10
            local.get $l11
            i32.mul
            i32.add
            local.set $l10
            br $B4
          end
          local.get $l7
          call $f71372
          local.set $l10
        end
        local.get $l10
        local.tee $l7
        i64.extend_i32_u
        local.tee $l15
        i64.const 55
        i64.add
        i64.const 6
        i64.shr_u
        local.get $l15
        i64.const 6
        i64.shr_u
        i64.sub
        local.tee $l18
        i64.const 1
        i64.add
        local.tee $l15
        i64.const 7
        i64.and
        local.tee $l16
        i64.eqz
        i32.eqz
        if $I7
          loop $L8
            local.get $l15
            i64.const 1
            i64.sub
            local.set $l15
            local.get $l7
            i32.const -64
            i32.sub
            local.set $l7
            local.get $l16
            i64.const 1
            i64.sub
            local.tee $l16
            i64.const 0
            i64.ne
            br_if $L8
          end
        end
        local.get $l18
        i64.const 7
        i64.ge_u
        if $I9
          loop $L10
            local.get $l7
            i32.const 512
            i32.add
            local.set $l7
            local.get $l15
            i64.const 8
            i64.sub
            local.tee $l15
            i64.const 0
            i64.ne
            br_if $L10
          end
        end
        local.get $p1
        local.get $l8
        i32.const 2
        i32.shl
        i32.add
        i32.load
        local.set $l9
        local.get $p5
        i32.load
        local.tee $l7
        local.get $p4
        call $f71588
        local.get $l7
        i32.const -1
        i32.store offset=48
        local.get $l7
        local.get $p3
        local.get $l9
        i32.add
        local.tee $l9
        i32.store offset=40
        local.get $l7
        i64.const 2199023255040
        i64.store offset=24
        block $B11
          local.get $l7
          i32.load offset=4
          i32.load offset=40
          i32.load offset=2368
          local.tee $l11
          i32.load offset=12
          local.tee $l12
          if $I12
            local.get $l11
            i32.load offset=8
            local.get $l12
            i32.const 1
            i32.sub
            local.tee $l14
            i32.const 2
            i32.shl
            i32.add
            i32.load
            local.set $l12
            local.get $l11
            local.get $l14
            i32.store offset=12
            br $B11
          end
          local.get $l11
          local.get $l11
          i32.load offset=4
          local.tee $l12
          i32.const 1
          i32.add
          i32.store offset=4
        end
        local.get $l7
        local.get $l12
        i32.store offset=44
        local.get $l7
        call $f71329
        local.get $p6
        local.get $l8
        i32.const 24
        i32.mul
        i32.add
        local.tee $l7
        local.get $p0
        i32.load offset=1140
        i32.load offset=4
        local.get $p5
        i32.load
        i32.load offset=8
        i32.const 2147483647
        i32.and
        i32.const 24
        i32.mul
        i32.add
        local.tee $l8
        f32.load
        f32.store
        local.get $l7
        local.get $l8
        f32.load offset=4
        f32.store offset=4
        local.get $l7
        local.get $l8
        f32.load offset=8
        f32.store offset=8
        local.get $l7
        local.get $l8
        f32.load offset=12
        f32.store offset=12
        local.get $l7
        local.get $l8
        f32.load offset=16
        f32.store offset=16
        local.get $l7
        local.get $l8
        f32.load offset=20
        f32.store offset=20
        local.get $p0
        i32.load offset=1012
        local.tee $l7
        local.get $p5
        i32.load
        local.tee $l8
        i32.const 16
        i32.add
        local.get $l8
        i32.load offset=44
        local.get $l7
        i32.load
        i32.load offset=16
        call_indirect $__indirect_function_table (type $t2)
        local.get $p5
        local.get $l10
        i32.store
        local.get $p0
        local.get $l9
        i32.load offset=68
        i32.const 2
        i32.shl
        i32.add
        i32.const 2676
        i32.add
        local.tee $l7
        local.get $l7
        i32.load
        i32.const 1
        i32.add
        i32.store
        local.get $p0
        i32.load offset=976
        i32.load offset=1024
        local.tee $l7
        local.get $l9
        i32.const 32
        i32.add
        local.get $l7
        i32.load
        i32.load offset=44
        call_indirect $__indirect_function_table (type $t1)
        local.get $l13
        local.tee $l8
        local.get $p2
        i32.ne
        br_if $L1
      end
    end)