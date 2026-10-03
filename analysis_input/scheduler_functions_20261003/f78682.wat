  (func $f78682 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32)
    local.get $p1
    i32.eqz
    if $I0
      i32.const 4126464
      local.get $p0
      i32.store
    end
    i32.const 4922576
    local.get $p1
    call $f69606
    i32.const 4758720
    i32.load
    local.tee $l2
    i32.load offset=8
    local.tee $l3
    if $I1
      loop $L2
        local.get $l2
        i32.load
        local.get $l4
        i32.const 36
        i32.mul
        i32.add
        i32.load offset=4
        local.tee $l5
        if $I3
          i32.const 0
          local.get $p0
          local.get $p1
          local.get $l5
          call_indirect $__indirect_function_table (type $t2)
          local.get $l2
          i32.load offset=8
          local.set $l3
        end
        local.get $l4
        i32.const 1
        i32.add
        local.tee $l4
        local.get $l3
        i32.lt_u
        br_if $L2
      end
    end)
