  (func $f71767 (type $t5) (param $p0 i32) (result i32)
    (local $l1 i32) (local $l2 i32) (local $l3 i32) (local $l4 i32)
    block $B0
      local.get $p0
      i32.load8_u offset=338
      i32.eqz
      br_if $B0
      i32.const 1
      local.set $l1
      local.get $p0
      i32.load offset=268
      br_if $B0
      i32.const 0
      local.set $l1
      local.get $p0
      i32.load offset=284
      local.tee $l2
      i32.eqz
      br_if $B0
      local.get $p0
      i32.load offset=32
      local.tee $l1
      if $I1
        local.get $l1
        i32.const 0
        call $f71743
        local.get $l1
        i32.load offset=52
        local.tee $l3
        if $I2
          call $f69753
          local.tee $l4
          local.get $l3
          local.get $l4
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
        local.tee $l3
        local.get $l1
        local.get $l3
        i32.load
        i32.load offset=12
        call_indirect $__indirect_function_table (type $t1)
      end
      call $f69753
      local.tee $l1
      i32.const 64
      i32.const 3177033
      i32.const 3176295
      i32.const 4700888
      i32.load
      local.tee $l3
      local.get $l3
      i32.load
      i32.load offset=20
      call_indirect $__indirect_function_table (type $t5)
      select
      i32.const 3175388
      i32.const 691
      local.get $l1
      i32.load
      i32.load offset=8
      call_indirect $__indirect_function_table (type $t9)
      local.tee $l1
      i32.const 0
      i32.store offset=8
      local.get $l1
      i64.const 0
      i64.store align=4
      local.get $l1
      i32.const 12
      i32.add
      call $f1035
      drop
      local.get $l1
      i32.const 0
      i32.store offset=60
      local.get $l1
      i64.const 0
      i64.store offset=52 align=4
      local.get $l1
      i64.const 0
      i64.store offset=44 align=4
      local.get $l1
      i64.const 0
      i64.store offset=36 align=4
      local.get $p0
      local.get $l2
      i32.store offset=40
      local.get $p0
      local.get $l1
      i32.store offset=32
      i32.const 0
      local.set $l1
      local.get $l2
      i32.const 24
      i32.mul
      local.tee $l2
      i32.const 24
      i32.add
      local.tee $l3
      if $I3
        call $f69753
        local.tee $l1
        local.get $l3
        i32.const 3176237
        i32.const 3175388
        i32.const 695
        local.get $l1
        i32.load
        i32.load offset=8
        call_indirect $__indirect_function_table (type $t9)
        local.set $l1
      end
      local.get $p0
      local.get $l1
      i32.store offset=36
      local.get $l1
      local.get $p0
      i32.load offset=292
      local.get $l2
      call $f483
      drop
      local.get $p0
      i32.const 0
      i32.store offset=16
      local.get $p0
      i64.const 0
      i64.store offset=8 align=4
      i32.const 1
      local.set $l1
      local.get $p0
      local.get $p0
      i32.load offset=48
      i32.const 1
      i32.add
      i32.store offset=48
      local.get $p0
      i32.const 60
      i32.add
      local.tee $l2
      local.get $l2
      i32.load
      i32.const -1
      i32.xor
      i32.const 1
      i32.and
      i32.store
      local.get $p0
      i32.const 56
      i32.add
      local.tee $l2
      local.get $l2
      i32.load
      i32.const -1
      i32.xor
      i32.const 1
      i32.and
      i32.store
      local.get $p0
      i32.load offset=20
      local.tee $l2
      if $I4
        call $f69753
        local.tee $l3
        local.get $l2
        local.get $l3
        i32.load
        i32.load offset=12
        call_indirect $__indirect_function_table (type $t1)
      end
      local.get $p0
      i64.const 0
      i64.store offset=20 align=4
      local.get $p0
      i32.const 4
      i32.store offset=8
      local.get $p0
      i32.const 1
      i32.store offset=268
      local.get $p0
      i32.const 0
      i32.store offset=28
      local.get $p0
      local.get $p0
      i64.load offset=36 align=4
      i64.const 32
      i64.rotl
      i64.store offset=12 align=4
    end
    local.get $l1)