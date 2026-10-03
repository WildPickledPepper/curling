  (func $f72115 (type $t2) (param $p0 i32) (param $p1 i32) (param $p2 i32)
    block $B0
      local.get $p2
      i32.eqz
      br_if $B0
      block $B1
        local.get $p1
        i32.const 3191396
        local.get $p1
        i32.load
        i32.load offset=20
        call_indirect $__indirect_function_table (type $t0)
        i32.eqz
        br_if $B1
        local.get $p2
        local.get $p2
        i32.load
        i32.load offset=40
        call_indirect $__indirect_function_table (type $t5)
        i32.eqz
        br_if $B1
        local.get $p2
        local.get $p2
        i32.load
        i32.load offset=40
        call_indirect $__indirect_function_table (type $t5)
        local.get $p1
        local.get $p1
        i32.load
        i32.load offset=92
        call_indirect $__indirect_function_table (type $t5)
        i32.le_u
        br_if $B0
      end
      i32.const 4700888
      i32.load
      i32.const 4
      i32.const 3184128
      i32.const 371
      i32.const 3184477
      i32.const 0
      call $f69760
      return
    end
    block $B2
      block $B3
        block $B4
          block $B5
            local.get $p1
            i32.load16_u offset=4
            i32.const 5
            i32.sub
            br_table $B4 $B5 $B2 $B2 $B2 $B2 $B2 $B2 $B3 $B2
          end
          local.get $p0
          local.get $p1
          local.get $p2
          i32.const 0
          call $f72116
          return
        end
        local.get $p0
        local.get $p1
        local.get $p2
        i32.const 0
        call $f72117
        return
      end
      i32.const 4700888
      i32.load
      i32.const 2
      i32.const 3184128
      i32.const 400
      i32.const 3184565
      i32.const 0
      call $f69760
    end)