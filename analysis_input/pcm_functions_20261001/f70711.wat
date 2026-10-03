  (func $f70711 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l5
    global.set $g0
    block $B0
      local.get $p0
      i32.load offset=16
      local.tee $l4
      local.get $p1
      i32.ge_u
      br_if $B0
      local.get $p0
      local.get $p1
      local.get $p0
      i32.load offset=20
      local.tee $l2
      i32.add
      i32.const 1
      i32.sub
      local.get $l2
      i32.div_u
      local.get $p0
      i32.load offset=4
      i32.sub
      local.tee $l7
      local.get $l2
      i32.mul
      local.get $l4
      i32.add
      i32.store offset=16
      local.get $l7
      i32.eqz
      br_if $B0
      i32.const 0
      local.set $p1
      loop $L1
        local.get $l5
        local.get $l2
        i32.const 2
        i32.shl
        local.tee $l2
        if $I2 (result i32)
          call $f69753
          local.tee $l4
          local.get $l2
          i32.const 3133968
          i32.const 3138624
          i32.const 84
          local.get $l4
          i32.load
          i32.load offset=8
          call_indirect $__indirect_function_table (type $t9)
        else
          i32.const 0
        end
        local.tee $l2
        i32.store offset=12
        block $B3
          local.get $p0
          i32.load offset=4
          local.tee $l4
          local.get $p0
          i32.load offset=8
          i32.const 2147483647
          i32.and
          i32.ge_u
          if $I4
            local.get $l5
            i32.const 12
            i32.add
            local.set $l9
            i32.const 0
            local.set $l4
            block $B5
              local.get $p0
              i32.load offset=8
              i32.const 2147483647
              i32.and
              local.tee $l3
              i32.const 1
              i32.shl
              i32.const 1
              local.get $l3
              select
              local.tee $l8
              i32.eqz
              br_if $B5
              local.get $l8
              i32.const 2
              i32.shl
              local.tee $l3
              i32.eqz
              br_if $B5
              call $f69753
              local.tee $l2
              local.get $l3
              i32.const 3139379
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
              local.get $l2
              i32.load
              i32.load offset=8
              call_indirect $__indirect_function_table (type $t9)
              local.set $l4
            end
            local.get $l4
            local.get $p0
            i32.load offset=4
            local.tee $l3
            i32.const 0
            i32.gt_s
            if $I6 (result i32)
              local.get $l4
              local.get $l3
              i32.const 2
              i32.shl
              i32.add
              local.set $l6
              local.get $p0
              i32.load
              local.set $l3
              local.get $l4
              local.set $l2
              loop $L7
                local.get $l2
                local.get $l3
                i32.load
                i32.store
                local.get $l3
                i32.const 4
                i32.add
                local.set $l3
                local.get $l2
                i32.const 4
                i32.add
                local.tee $l2
                local.get $l6
                i32.lt_u
                br_if $L7
              end
              local.get $p0
              i32.load offset=4
            else
              local.get $l3
            end
            i32.const 2
            i32.shl
            i32.add
            local.get $l9
            i32.load
            i32.store
            block $B8
              local.get $p0
              i32.load offset=8
              i32.const 0
              i32.lt_s
              br_if $B8
              local.get $p0
              i32.load
              local.tee $l3
              i32.eqz
              br_if $B8
              call $f69753
              local.tee $l2
              local.get $l3
              local.get $l2
              i32.load
              i32.load offset=12
              call_indirect $__indirect_function_table (type $t1)
            end
            local.get $p0
            local.get $l8
            i32.store offset=8
            local.get $p0
            local.get $l4
            i32.store
            local.get $p0
            local.get $p0
            i32.load offset=4
            i32.const 1
            i32.add
            i32.store offset=4
            br $B3
          end
          local.get $p0
          i32.load
          local.get $l4
          i32.const 2
          i32.shl
          i32.add
          local.get $l2
          i32.store
          local.get $p0
          local.get $p0
          i32.load offset=4
          i32.const 1
          i32.add
          i32.store offset=4
        end
        local.get $p1
        i32.const 1
        i32.add
        local.tee $p1
        local.get $l7
        i32.eq
        br_if $B0
        local.get $p0
        i32.load offset=20
        local.set $l2
        br $L1
      end
      unreachable
    end
    local.get $l5
    i32.const 16
    i32.add
    global.set $g0)