  (func $f71526 (type $t7) (param $p0 i32)
    (local $l1 i32) (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i64)
    block $B0
      local.get $p0
      i32.load offset=20
      local.set $l1
      block $B1
        local.get $p0
        i32.load offset=28
        i32.load offset=2168
        local.tee $l2
        i32.load
        local.tee $l5
        i32.load offset=92
        local.tee $p0
        i32.eqz
        br_if $B1
        local.get $l5
        i32.const -64
        i32.sub
        i32.load
        local.set $l6
        local.get $l5
        i32.load offset=976
        local.get $p0
        i32.const 2
        i32.shl
        local.tee $l4
        local.get $p0
        i32.const 6
        i32.shr_u
        i32.const 56
        i32.mul
        i32.add
        i32.const 56
        i32.add
        i32.const 1
        call $f71713
        local.tee $l7
        if $I2
          local.get $l5
          i32.load offset=4604
          local.tee $l3
          local.get $l3
          i32.load
          i32.load offset=4
          call_indirect $__indirect_function_table (type $t5)
          local.tee $l3
          local.get $l3
          i32.load
          i32.load offset=4
          call_indirect $__indirect_function_table (type $t5)
          local.set $l3
          local.get $l2
          local.get $l7
          i32.store offset=1904
          block $B3
            local.get $l3
            i32.const 1
            i32.gt_u
            local.get $p0
            i32.const 64
            i32.gt_u
            i32.and
            local.tee $l8
            i32.eqz
            br_if $B3
            local.get $l2
            i32.const 1884
            i32.add
            local.get $l1
            i32.store
            local.get $l2
            i32.const 1888
            i32.add
            i32.const 1
            i32.store
            local.get $l1
            i32.eqz
            br_if $B3
            local.get $l1
            local.get $l1
            i32.load
            i32.load offset=16
            call_indirect $__indirect_function_table (type $t7)
            local.get $l2
            i32.const 1880
            i32.add
            local.get $l2
            i32.load offset=1884
            i32.load offset=16
            i32.store
          end
          local.get $l4
          local.get $l7
          i32.add
          local.set $l1
          local.get $l2
          i32.const 1864
          i32.add
          local.set $l3
          local.get $l2
          i32.const 1912
          i32.add
          local.set $l9
          local.get $l2
          i32.const 1908
          i32.add
          local.set $l10
          loop $L4
            local.get $l5
            i64.load offset=16
            local.set $l11
            local.get $l1
            i32.const 0
            i32.store offset=24
            local.get $l1
            i64.const 0
            i64.store offset=16
            local.get $l1
            local.get $l11
            i64.store offset=8
            local.get $l1
            local.get $l5
            i32.store offset=48
            local.get $l1
            local.get $l9
            i32.store offset=44
            local.get $l1
            local.get $l7
            i32.store offset=40
            local.get $l1
            local.get $l10
            i32.store offset=36
            local.get $l1
            local.get $l6
            i32.store offset=28
            local.get $l1
            i32.const 3173588
            i32.store
            local.get $l1
            local.get $p0
            i32.const 64
            local.get $p0
            i32.const 64
            i32.lt_u
            select
            local.tee $l4
            i32.store offset=32
            local.get $p0
            local.get $l4
            i32.sub
            local.set $p0
            block $B5
              local.get $l8
              if $I6
                local.get $l1
                local.get $l3
                i32.store offset=20
                local.get $l1
                i32.const 1
                i32.store offset=24
                local.get $l3
                local.get $l3
                i32.load
                i32.load offset=16
                call_indirect $__indirect_function_table (type $t7)
                local.get $l1
                local.get $l1
                i32.load offset=20
                i32.load offset=16
                i32.store offset=16
                local.get $l1
                local.get $l1
                i32.load
                i32.load offset=20
                call_indirect $__indirect_function_table (type $t7)
                local.get $p0
                br_if $B5
                local.get $l2
                i32.const 1880
                i32.add
                i32.load
                local.tee $l1
                local.get $l3
                local.get $l1
                i32.load
                i32.load offset=72
                call_indirect $__indirect_function_table (type $t1)
                br $B0
              end
              local.get $l1
              call $f71714
              local.get $p0
              br_if $B5
              local.get $l2
              i32.const 1892
              i32.add
              i32.load
              local.tee $p0
              i32.load offset=1904
              local.tee $l4
              i32.eqz
              br_if $B1
              i32.const 0
              local.set $l1
              local.get $p0
              i32.load offset=1912
              i32.const 0
              i32.gt_s
              if $I7
                loop $L8
                  local.get $p0
                  i32.load
                  local.get $l4
                  local.get $l1
                  i32.const 2
                  i32.shl
                  i32.add
                  i32.load
                  local.tee $l6
                  i32.const 4
                  i32.add
                  i32.const 0
                  local.get $l6
                  select
                  call $f71387
                  local.get $l1
                  i32.const 1
                  i32.add
                  local.tee $l1
                  local.get $p0
                  i32.load offset=1912
                  i32.lt_s
                  br_if $L8
                end
                local.get $p0
                i32.load offset=1904
                local.set $l4
              end
              local.get $p0
              i32.const 0
              i32.store offset=1912
              local.get $p0
              i32.load
              i32.load offset=976
              local.get $l4
              call $f71715
              local.get $p0
              i32.const 0
              i32.store offset=1904
              br $B0
            end
            local.get $l1
            i32.const 56
            i32.add
            local.set $l1
            local.get $l6
            local.get $l4
            i32.const 2
            i32.shl
            i32.add
            local.set $l6
            br $L4
          end
          unreachable
        end
        i32.const 4700888
        i32.load
        local.tee $l1
        local.get $l1
        i32.load
        i32.load offset=4
        call_indirect $__indirect_function_table (type $t5)
        local.tee $l1
        i32.const 16
        i32.const 3172000
        i32.const 3171943
        i32.const 1481
        local.get $l1
        i32.load
        i32.load offset=8
        call_indirect $__indirect_function_table (type $t6)
      end
    end)