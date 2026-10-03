  (func $f71331 (type $t2) (param $p0 i32) (param $p1 i32) (param $p2 i32)
    block $B0
      block $B1
        block $B2
          block $B3
            block $B4
              local.get $p2
              i32.const 8
              i32.sub
              br_table $B4 $B1 $B1 $B1 $B1 $B1 $B1 $B1 $B3 $B1 $B1 $B1 $B1 $B1 $B1 $B1 $B1 $B1 $B1 $B1 $B1 $B1 $B1 $B1 $B2 $B1
            end
            local.get $p1
            i32.eqz
            br_if $B0
            local.get $p0
            i32.const 380
            i32.add
            local.tee $p2
            local.get $p2
            i32.load
            i32.const 1
            i32.sub
            i32.store
            local.get $p1
            local.get $p0
            i32.const 388
            i32.add
            local.tee $p0
            i32.load
            i32.store
            local.get $p0
            local.get $p1
            i32.store
            return
          end
          local.get $p1
          i32.eqz
          br_if $B0
          local.get $p0
          i32.const 672
          i32.add
          local.tee $p2
          local.get $p2
          i32.load
          i32.const 1
          i32.sub
          i32.store
          local.get $p1
          local.get $p0
          i32.const 680
          i32.add
          local.tee $p0
          i32.load
          i32.store
          local.get $p0
          local.get $p1
          i32.store
          return
        end
        local.get $p1
        i32.eqz
        br_if $B0
        local.get $p0
        i32.const 964
        i32.add
        local.tee $p2
        local.get $p2
        i32.load
        i32.const 1
        i32.sub
        i32.store
        local.get $p1
        local.get $p0
        i32.const 972
        i32.add
        local.tee $p0
        i32.load
        i32.store
        local.get $p0
        local.get $p1
        i32.store
        return
      end
      local.get $p1
      i32.eqz
      br_if $B0
      call $f69753
      local.tee $p0
      local.get $p1
      local.get $p0
      i32.load
      i32.load offset=12
      call_indirect $__indirect_function_table (type $t1)
    end)