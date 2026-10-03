  (func $f60064 (type $t2) (param $p0 i32) (param $p1 i32) (param $p2 i32)
    (local $l3 i32) (local $l4 i32)
    i32.const 4674414
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3748144
      call $f1661
      i32.const 4674414
      i32.const 1
      i32.store8
    end
    local.get $p1
    i32.load offset=12
    i32.const 5
    i32.eq
    if $I1
      local.get $p1
      i32.load offset=20
      local.set $p2
      local.get $p0
      i32.load offset=124
      local.set $l3
      i32.const 3748144
      i32.load
      local.tee $l4
      i32.load offset=116
      i32.eqz
      if $I2
        local.get $l4
        call $f65192
      end
      local.get $l3
      local.get $p2
      i32.const 0
      call $f58915
      i32.store offset=8
      local.get $p0
      i32.load offset=124
      local.get $p1
      i32.load offset=24
      i32.const 0
      call $f58915
      i32.store offset=12
      local.get $p0
      i32.load offset=124
      local.get $p1
      i32.load offset=32
      i32.const 0
      call $f58927
      i32.store offset=24
    end
    block $B3
      local.get $p0
      block $B4 (result i32)
        block $B5
          block $B6
            local.get $p0
            i32.load offset=124
            local.tee $p1
            i32.load offset=8
            br_table $B6 $B3 $B3 $B3 $B3 $B3 $B3 $B3 $B3 $B3 $B3 $B3 $B3 $B3 $B3 $B3 $B5 $B3
          end
          local.get $p1
          i32.load offset=24
          br $B4
        end
        local.get $p1
        i32.load offset=24
        i32.const 1
        i32.xor
      end
      i32.store offset=156
    end)