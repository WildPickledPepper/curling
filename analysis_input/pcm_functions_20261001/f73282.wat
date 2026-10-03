  (func $f73282 (type $t6) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32)
    (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32)
    global.get $g0
    i32.const 112
    i32.sub
    local.tee $l5
    global.set $g0
    block $B0
      local.get $p2
      local.get $p2
      i32.load
      i32.load offset=92
      call_indirect $__indirect_function_table (type $t5)
      i32.const 65534
      i32.ge_u
      if $I1
        local.get $p0
        i32.load offset=4
        local.set $p0
        local.get $l5
        i32.const 403047
        i32.store offset=108
        local.get $l5
        i32.const 403047
        i32.store offset=104
        local.get $l5
        i64.const 0
        i64.store offset=96
        local.get $l5
        i32.const 1
        i32.store8 offset=92
        local.get $l5
        i32.const 403047
        i32.store offset=60
        local.get $l5
        i32.const 403047
        i32.store offset=56
        local.get $l5
        i32.const 403047
        i32.store offset=52
        local.get $l5
        i64.const 0
        i64.store offset=84 align=4
        local.get $l5
        local.get $p0
        i32.store offset=80
        local.get $l5
        i32.const 1
        i32.store offset=76
        local.get $l5
        i64.const -4294966889
        i64.store offset=68 align=4
        local.get $l5
        i32.const 403047
        i32.store offset=64
        local.get $l5
        i32.const 56455
        i32.store offset=48
        local.get $l5
        i32.const 48
        i32.add
        call $f83275
        br $B0
      end
      local.get $l5
      i32.const 0
      i32.store offset=44
      block $B2
        block $B3
          local.get $p0
          i32.load offset=36
          local.tee $l6
          i32.eqz
          br_if $B3
          local.get $l5
          local.get $l6
          i32.store offset=24
          block $B4
            block $B5
              i32.const 4782060
              i32.load
              local.tee $l7
              i32.eqz
              br_if $B5
              local.get $l5
              i32.const 48
              i32.add
              local.get $l7
              local.get $l5
              i32.const 24
              i32.add
              call $f66830
              local.get $l5
              i32.load offset=48
              local.tee $l8
              i32.const 4782060
              i32.load
              local.tee $l7
              i32.load
              local.get $l7
              i32.load offset=4
              i32.const 3
              i32.mul
              i32.add
              i32.const 12
              i32.add
              i32.eq
              br_if $B5
              local.get $l8
              i32.load offset=8
              local.tee $l7
              br_if $B4
            end
            local.get $l6
            call $f80110
            local.tee $l7
            i32.eqz
            br_if $B3
          end
          local.get $l5
          local.get $l7
          i32.load offset=52
          local.tee $l6
          i32.store offset=44
          br $B2
        end
        call $f73708
        local.tee $l6
        local.get $l5
        i32.const 44
        i32.add
        i32.const 1
        i32.const 0
        local.get $l6
        i32.load
        i32.load offset=128
        call_indirect $__indirect_function_table (type $t8)
        drop
        local.get $l5
        i32.load offset=44
        local.set $l6
      end
      local.get $l5
      local.get $l6
      i32.store offset=48
      i32.const 4702108
      i32.load
      local.set $l6
      local.get $l5
      i32.const 11
      i32.store8 offset=24
      block $B6
        local.get $l6
        local.get $p1
        local.get $l5
        i32.const 48
        i32.add
        i32.const 1
        i32.const 1
        local.get $l5
        i32.const 24
        i32.add
        local.get $l6
        i32.load
        i32.load offset=96
        call_indirect $__indirect_function_table (type $t10)
        local.tee $l6
        if $I7
          local.get $p2
          local.get $l6
          local.get $p2
          i32.load
          i32.load offset=84
          call_indirect $__indirect_function_table (type $t0)
          local.set $l7
          local.get $l6
          local.get $l6
          i32.load
          i32.load
          call_indirect $__indirect_function_table (type $t7)
          local.get $l7
          br_if $B6
        end
        local.get $p0
        i32.load offset=4
        local.set $p0
        local.get $l5
        i32.const 403047
        i32.store offset=108
        local.get $l5
        i32.const 403047
        i32.store offset=104
        local.get $l5
        i64.const 0
        i64.store offset=96
        local.get $l5
        i32.const 1
        i32.store8 offset=92
        local.get $l5
        i32.const 403047
        i32.store offset=60
        local.get $l5
        i32.const 403047
        i32.store offset=56
        local.get $l5
        i32.const 403047
        i32.store offset=52
        local.get $l5
        i64.const 0
        i64.store offset=84 align=4
        local.get $l5
        local.get $p0
        i32.store offset=80
        local.get $l5
        i32.const 1
        i32.store offset=76
        local.get $l5
        i64.const -4294966869
        i64.store offset=68 align=4
        local.get $l5
        i32.const 403047
        i32.store offset=64
        local.get $l5
        i32.const 217391
        i32.store offset=48
        local.get $l5
        i32.const 48
        i32.add
        call $f83275
        br $B0
      end
      local.get $p0
      local.get $l6
      i32.store offset=40
      local.get $l6
      local.get $p0
      i32.store offset=8
      local.get $l5
      i32.const 40
      i32.add
      local.get $p0
      i32.load offset=40
      local.tee $l6
      local.get $l6
      i32.load
      i32.load offset=156
      call_indirect $__indirect_function_table (type $t1)
      local.get $l5
      i32.const 0
      i32.store offset=32
      local.get $l5
      i64.const 0
      i64.store offset=24
      local.get $l5
      i64.const 0
      i64.store offset=16
      local.get $l5
      i64.const 0
      i64.store offset=8
      local.get $p1
      i32.load
      local.set $l7
      i32.const 1
      local.set $l6
      local.get $p2
      local.get $p2
      i32.load
      i32.load offset=24
      call_indirect $__indirect_function_table (type $t5)
      i32.const 2
      i32.ne
      if $I8
        local.get $p2
        local.get $p2
        i32.load
        i32.load offset=24
        call_indirect $__indirect_function_table (type $t5)
        i32.const 1
        i32.eq
        local.set $l6
      end
      block $B9 (result i32)
        local.get $p0
        i32.load8_u offset=60
        if $I10
          local.get $l5
          i32.load8_u offset=40
          i32.const -8
          i32.and
          i32.const 6
          i32.or
          br $B9
        end
        block $B11 (result i32)
          block $B12
            block $B13
              block $B14
                local.get $p2
                i32.load16_u offset=4
                i32.const 5
                i32.eq
                if $I15
                  local.get $l5
                  i32.const 48
                  i32.add
                  local.get $p2
                  local.get $p2
                  i32.load
                  i32.load offset=216
                  call_indirect $__indirect_function_table (type $t1)
                  local.get $l7
                  i32.const 5
                  i32.sub
                  i32.const 2
                  i32.ge_u
                  br_if $B12
                  local.get $l5
                  i32.load16_u offset=48
                  i32.const 1
                  i32.and
                  i32.eqz
                  br_if $B13
                  br $B14
                end
                local.get $l7
                i32.const 5
                i32.sub
                i32.const 2
                i32.ge_u
                br_if $B12
              end
              local.get $p2
              local.get $p2
              i32.load
              i32.load offset=24
              call_indirect $__indirect_function_table (type $t5)
              i32.const 2
              i32.ne
              br_if $B12
            end
            local.get $l5
            i32.load8_u offset=40
            i32.const -2
            i32.and
            br $B11
          end
          local.get $l5
          i32.load8_u offset=40
          i32.const 1
          i32.or
        end
        i32.const -7
        i32.and
        i32.const 2
        i32.or
      end
      local.set $l8
      i32.const 0
      local.set $p1
      local.get $l5
      i32.const 0
      i32.store offset=36
      local.get $l5
      local.get $p0
      i32.store offset=28
      local.get $l5
      local.get $l8
      i32.store8 offset=40
      local.get $l7
      i32.const 5
      i32.sub
      i32.const 2
      i32.lt_u
      i32.const 5
      i32.shl
      local.set $l7
      block $B16
        local.get $l6
        i32.eqz
        if $I17
          local.get $l5
          local.get $l7
          i32.const 1
          i32.or
          i32.store offset=32
          br $B16
        end
        local.get $l5
        local.get $l7
        i32.const 2
        i32.or
        i32.store offset=32
        local.get $p2
        i32.load offset=8
        i32.load offset=28
        i32.load offset=56
        local.set $p1
      end
      i32.const 540
      local.set $p2
      block $B18
        i32.const 1
        i32.const 4678968
        i32.load
        i32.shl
        i32.const 4678964
        i32.load
        i32.const 28
        i32.shl
        i32.const 31
        i32.shr_s
        i32.and
        local.tee $l7
        local.get $p0
        i32.load offset=28
        local.tee $l6
        i32.load offset=56
        local.get $p1
        i32.or
        local.tee $p1
        i32.and
        br_if $B18
        local.get $p0
        i32.load8_u offset=64
        br_if $B18
        i32.const 532
        i32.const 0
        i32.const 1
        i32.const 4678920
        i32.load
        i32.shl
        i32.const 4678916
        i32.load
        i32.const 28
        i32.shl
        i32.const 31
        i32.shr_s
        i32.and
        i32.const 1
        i32.const 4678872
        i32.load
        i32.shl
        i32.const 4678868
        i32.load
        i32.const 28
        i32.shl
        i32.const 31
        i32.shr_s
        i32.and
        local.get $l7
        i32.or
        i32.or
        local.get $p1
        i32.and
        select
        local.set $p2
      end
      local.get $l6
      i32.load offset=44
      local.set $l6
      local.get $p0
      i32.load8_u offset=63
      local.set $p1
      local.get $l5
      i32.const 0
      i32.store offset=20
      local.get $l5
      local.get $p0
      i32.store offset=12
      local.get $l5
      local.get $l6
      local.get $p2
      i32.const 2
      i32.or
      local.get $p2
      local.get $p1
      select
      i32.const 8
      i32.shl
      i32.or
      local.tee $p2
      i32.store offset=8
      local.get $l5
      local.get $p2
      i32.store offset=24
      local.get $p0
      i32.load offset=40
      local.tee $p2
      local.get $l5
      i32.const 24
      i32.add
      local.get $p2
      i32.load
      i32.load offset=84
      call_indirect $__indirect_function_table (type $t1)
      local.get $p0
      i32.load offset=40
      local.tee $p2
      local.get $l5
      i32.const 8
      i32.add
      local.get $p2
      i32.load
      i32.load offset=92
      call_indirect $__indirect_function_table (type $t1)
      local.get $p0
      i32.load offset=40
      local.set $p2
      local.get $l5
      local.get $l5
      i32.load8_u offset=40
      i32.store8
      local.get $p2
      local.get $l5
      local.get $p2
      i32.load
      i32.load offset=152
      call_indirect $__indirect_function_table (type $t1)
      local.get $p0
      i32.load offset=40
      local.tee $p2
      f32.const 0x0p+0 (;=0;)
      local.get $p2
      i32.load
      i32.load offset=124
      call_indirect $__indirect_function_table (type $t21)
      local.get $p0
      i32.load offset=40
      local.tee $p2
      local.get $p0
      f32.load offset=56
      local.get $p2
      i32.load
      i32.load offset=116
      call_indirect $__indirect_function_table (type $t21)
      local.get $p0
      i32.load offset=40
      local.tee $p2
      i32.eqz
      br_if $B0
      local.get $l5
      i32.const 48
      i32.add
      local.get $p2
      local.get $p2
      i32.load
      i32.load offset=88
      call_indirect $__indirect_function_table (type $t1)
      local.get $l5
      local.get $l5
      i32.load offset=56
      i32.const -17
      i32.and
      i32.const 16
      i32.const 0
      local.get $p4
      select
      i32.or
      i32.store offset=56
      local.get $p0
      i32.load offset=40
      local.tee $p2
      local.get $l5
      i32.const 48
      i32.add
      local.get $p2
      i32.load
      i32.load offset=84
      call_indirect $__indirect_function_table (type $t1)
      local.get $p0
      i32.load offset=40
      local.tee $p2
      i32.eqz
      br_if $B0
      local.get $l5
      i32.const 48
      i32.add
      local.get $p2
      local.get $p2
      i32.load
      i32.load offset=88
      call_indirect $__indirect_function_table (type $t1)
      local.get $l5
      local.get $l5
      i32.load offset=56
      local.tee $p2
      i32.const -13
      i32.and
      local.tee $l6
      i32.store offset=56
      block $B19
        local.get $l5
        block $B20 (result i32)
          block $B21
            block $B22
              block $B23
                local.get $p3
                i32.const 1
                i32.sub
                br_table $B23 $B22 $B21 $B19
              end
              local.get $l6
              i32.const 4
              i32.or
              br $B20
            end
            local.get $p2
            i32.const 12
            i32.or
            br $B20
          end
          local.get $p2
          i32.const 12
          i32.or
        end
        i32.store offset=56
      end
      local.get $p0
      i32.load offset=40
      local.tee $p0
      local.get $l5
      i32.const 48
      i32.add
      local.get $p0
      i32.load
      i32.load offset=84
      call_indirect $__indirect_function_table (type $t1)
    end
    local.get $l5
    i32.const 112
    i32.add
    global.set $g0)
