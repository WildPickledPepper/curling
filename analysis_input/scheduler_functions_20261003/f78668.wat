  (func $f78668 (type $t12)
    (local $l0 i32) (local $l1 i32) (local $l2 i32)
    i32.const 4758464
    i32.load
    local.tee $l0
    local.get $l0
    i32.load
    i32.const 2
    i32.shl
    i32.add
    i32.load offset=4
    local.set $l2
    local.get $l2
    i32.load offset=4
    i32.load
    if $I0
      loop $L1
        block $B2
          local.get $l2
          i32.load offset=4
          local.tee $l0
          i32.load
          local.tee $l1
          i32.eqz
          if $I3
            i32.const 0
            local.set $l0
            br $B2
          end
          local.get $l0
          local.get $l1
          i32.load offset=4
          i32.store offset=4
          local.get $l0
          local.get $l1
          i32.load offset=8
          i32.store offset=8
          local.get $l0
          local.get $l1
          i32.load offset=12
          i32.store offset=12
          local.get $l2
          local.get $l1
          i32.store offset=4
        end
        local.get $l0
        i32.load offset=4
        local.tee $l1
        local.get $l1
        i32.load
        i32.load
        call_indirect $__indirect_function_table (type $t7)
        local.get $l0
        i32.const 14
        i32.const 403047
        i32.const 45
        call $f83342
        local.get $l2
        i32.load offset=4
        i32.load
        br_if $L1
      end
    end
    i32.const 4758464
    i32.load
    local.tee $l0
    local.get $l0
    i32.load
    i32.const -1
    i32.xor
    i32.const 1
    i32.and
    i32.store)
