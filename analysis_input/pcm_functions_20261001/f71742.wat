  (func $f71742 (type $t7) (param $p0 i32)
    (local $l1 i32) (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l4
    global.set $g0
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l5
    global.set $g0
    local.get $p0
    i32.const 52
    i32.add
    local.tee $l1
    i32.const 4
    i32.add
    call $f71863
    local.get $l5
    i32.const 0
    i32.store offset=8
    local.get $l1
    i32.const 172
    i32.add
    local.tee $l2
    i32.const 0
    local.get $l5
    i32.const 8
    i32.add
    call $f70631
    local.get $l2
    local.get $l1
    i32.load offset=176
    call $f70632
    local.get $l5
    i32.const 0
    i32.store offset=12
    local.get $l1
    i32.const 184
    i32.add
    local.tee $l2
    i32.const 0
    local.get $l5
    i32.const 12
    i32.add
    call $f70631
    local.get $l2
    local.get $l1
    i32.load offset=188
    call $f70632
    block $B0
      local.get $l1
      i32.load offset=148
      local.tee $l2
      i32.eqz
      br_if $B0
      local.get $l1
      i32.load offset=164
      i32.eqz
      br_if $B0
      local.get $l1
      i32.load offset=140
      i32.const 255
      local.get $l2
      i32.const 2
      i32.shl
      call $f484
      drop
      i32.const 0
      local.set $l2
      local.get $l1
      i32.load offset=144
      local.tee $l3
      i32.const 1
      i32.sub
      local.tee $l6
      if $I1
        local.get $l6
        i32.const 3
        i32.and
        local.set $l8
        local.get $l3
        i32.const 2
        i32.sub
        i32.const 3
        i32.ge_u
        if $I2
          local.get $l6
          i32.const -4
          i32.and
          local.set $l6
          loop $L3
            local.get $l1
            i32.load offset=136
            local.get $l2
            i32.const 2
            i32.shl
            i32.add
            local.get $l2
            i32.const 1
            i32.or
            local.tee $l3
            i32.store
            local.get $l1
            i32.load offset=136
            local.get $l3
            i32.const 2
            i32.shl
            i32.add
            local.get $l2
            i32.const 2
            i32.or
            local.tee $l3
            i32.store
            local.get $l1
            i32.load offset=136
            local.get $l3
            i32.const 2
            i32.shl
            i32.add
            local.get $l2
            i32.const 3
            i32.or
            local.tee $l3
            i32.store
            local.get $l1
            i32.load offset=136
            local.get $l3
            i32.const 2
            i32.shl
            i32.add
            local.get $l2
            i32.const 4
            i32.add
            local.tee $l2
            i32.store
            local.get $l6
            i32.const 4
            i32.sub
            local.tee $l6
            br_if $L3
          end
        end
        local.get $l8
        if $I4
          loop $L5
            local.get $l1
            i32.load offset=136
            local.get $l2
            i32.const 2
            i32.shl
            i32.add
            local.get $l2
            i32.const 1
            i32.add
            local.tee $l2
            i32.store
            local.get $l8
            i32.const 1
            i32.sub
            local.tee $l8
            br_if $L5
          end
        end
        local.get $l1
        i32.load offset=144
        i32.const 1
        i32.sub
        local.set $l2
      end
      local.get $l1
      i32.load offset=136
      local.get $l2
      i32.const 2
      i32.shl
      i32.add
      i32.const -1
      i32.store
      local.get $l1
      i32.const 0
      i32.store offset=164
      local.get $l1
      i32.const 0
      i32.store offset=156
    end
    local.get $l1
    i32.load offset=208
    if $I6
      loop $L7
        local.get $l7
        i32.const 3
        i32.shl
        local.tee $l2
        local.get $l1
        i32.load offset=200
        i32.add
        i32.const 0
        i32.store offset=4
        local.get $l1
        i32.load offset=200
        local.get $l2
        i32.add
        i32.load
        i32.const 1
        call $f71743
        local.get $l7
        i32.const 1
        i32.add
        local.tee $l7
        local.get $l1
        i32.load offset=208
        i32.lt_u
        br_if $L7
      end
    end
    local.get $l1
    i32.const 0
    i32.store offset=204
    local.get $l5
    i32.const 16
    i32.add
    global.set $g0
    local.get $p0
    i32.const 0
    i32.store offset=48
    local.get $l4
    i32.const 0
    i32.store offset=8
    local.get $p0
    i32.const 312
    i32.add
    local.tee $l1
    i32.const 0
    local.get $l4
    i32.const 8
    i32.add
    call $f70631
    local.get $l1
    local.get $p0
    i32.load offset=316
    call $f70632
    local.get $l4
    i32.const 0
    i32.store offset=12
    local.get $p0
    i32.const 324
    i32.add
    local.tee $l1
    i32.const 0
    local.get $l4
    i32.const 12
    i32.add
    call $f70631
    local.get $l1
    local.get $p0
    i32.load offset=328
    call $f70632
    local.get $p0
    i32.load offset=36
    local.tee $l1
    if $I8
      call $f69753
      local.tee $l2
      local.get $l1
      local.get $l2
      i32.load
      i32.load offset=12
      call_indirect $__indirect_function_table (type $t1)
    end
    local.get $p0
    i32.const 0
    i32.store offset=36
    local.get $p0
    i64.const 0
    i64.store offset=8 align=4
    local.get $p0
    i32.const 0
    i32.store offset=16
    local.get $p0
    i32.load offset=20
    local.tee $l1
    if $I9
      call $f69753
      local.tee $l2
      local.get $l1
      local.get $l2
      i32.load
      i32.load offset=12
      call_indirect $__indirect_function_table (type $t1)
    end
    local.get $p0
    i32.const 0
    i32.store offset=20
    local.get $p0
    i32.load offset=32
    local.tee $l1
    if $I10
      local.get $l1
      i32.const 0
      call $f71743
      local.get $l1
      i32.load offset=52
      local.tee $l2
      if $I11
        call $f69753
        local.tee $l3
        local.get $l2
        local.get $l3
        i32.load
        i32.load offset=12
        call_indirect $__indirect_function_table (type $t1)
      end
      local.get $l1
      i32.const 0
      i32.store offset=52
      local.get $l1
      i32.const 12
      i32.add
      call $f70304
      call $f69753
      local.tee $l2
      local.get $l1
      local.get $l2
      i32.load
      i32.load offset=12
      call_indirect $__indirect_function_table (type $t1)
    end
    local.get $p0
    i32.const 0
    i32.store offset=32
    local.get $p0
    i32.load offset=4
    local.tee $l1
    if $I12
      local.get $l1
      i32.const 0
      call $f71743
      local.get $l1
      i32.load offset=52
      local.tee $l2
      if $I13
        call $f69753
        local.tee $l3
        local.get $l2
        local.get $l3
        i32.load
        i32.load offset=12
        call_indirect $__indirect_function_table (type $t1)
      end
      local.get $l1
      i32.const 0
      i32.store offset=52
      local.get $l1
      i32.const 12
      i32.add
      call $f70304
      call $f69753
      local.tee $l2
      local.get $l1
      local.get $l2
      i32.load
      i32.load offset=12
      call_indirect $__indirect_function_table (type $t1)
    end
    local.get $p0
    i32.const 0
    i32.store offset=268
    local.get $p0
    i32.const 0
    i32.store offset=40
    local.get $p0
    i32.const 0
    i32.store offset=4
    local.get $p0
    i32.const 0
    i32.store8 offset=337
    local.get $p0
    i32.const 0
    i32.store offset=344
    local.get $l4
    i32.const 16
    i32.add
    global.set $g0)