  (func $f61073 (type $t2) (param $p0 i32) (param $p1 i32) (param $p2 i32)
    (local $l3 i32)
    i32.const 4675136
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3748808
      call $f1661
      i32.const 3814476
      call $f1661
      i32.const 3834896
      call $f1661
      i32.const 4675136
      i32.const 1
      i32.store8
    end
    i32.const 3834896
    i32.load
    local.get $p1
    i32.load offset=20
    i32.const 3814476
    i32.load
    i32.const 0
    call $f53871
    local.set $p2
    i32.const 3748808
    i32.load
    local.tee $l3
    i32.load offset=116
    i32.eqz
    if $I1
      local.get $l3
      call $f65192
    end
    local.get $p2
    i32.const 0
    call $f42976
    block $B2
      block $B3
        block $B4
          local.get $p1
          i32.load
          br_table $B4 $B3 $B2
        end
        local.get $p0
        i32.const 1
        i32.store8 offset=103
        return
      end
      local.get $p0
      i32.const 1
      i32.store8 offset=104
    end)
