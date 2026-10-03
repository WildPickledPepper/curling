  (func $f73733 (type $t7) (param $p0 i32)
    (local $l1 i32) (local $l2 i32) (local $l3 i32)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l1
    global.set $g0
    block $B0
      block $B1
        local.get $p0
        i32.load offset=60
        local.tee $l2
        i32.eqz
        if $I2
          local.get $p0
          i32.const 0
          i32.store offset=64
          br $B1
        end
        local.get $l1
        local.get $l2
        i32.store offset=12
        block $B3
          block $B4
            i32.const 4782060
            i32.load
            local.tee $l2
            i32.eqz
            br_if $B4
            local.get $l1
            local.get $l2
            local.get $l1
            i32.const 12
            i32.add
            call $f66830
            local.get $l1
            i32.load
            local.tee $l3
            i32.const 4782060
            i32.load
            local.tee $l2
            i32.load
            local.get $l2
            i32.load offset=4
            i32.const 3
            i32.mul
            i32.add
            i32.const 12
            i32.add
            i32.eq
            br_if $B4
            local.get $l3
            i32.load offset=8
            local.tee $l2
            i32.eqz
            br_if $B4
            local.get $p0
            local.get $l2
            i32.store offset=64
            br $B3
          end
          local.get $p0
          local.get $p0
          i32.load offset=60
          call $f80110
          local.tee $l2
          i32.store offset=64
          local.get $l2
          i32.eqz
          br_if $B1
        end
        i32.const 4702528
        i32.load
        i32.load offset=12
        local.tee $p0
        local.get $l1
        i32.const 1
        i32.const 0
        local.get $p0
        i32.load
        i32.load offset=128
        call_indirect $__indirect_function_table (type $t8)
        drop
        local.get $l2
        local.get $l1
        i32.load
        call $f73734
        br $B0
      end
      i32.const 4702528
      i32.load
      i32.load offset=12
      local.tee $p0
      local.get $l1
      i32.const 1
      i32.const 0
      local.get $p0
      i32.load
      i32.load offset=128
      call_indirect $__indirect_function_table (type $t8)
      drop
      local.get $l1
      i32.load
      local.tee $p0
      f32.const 0x1.333334p-1 (;=0.6;)
      local.get $p0
      i32.load
      i32.load offset=32
      call_indirect $__indirect_function_table (type $t21)
      local.get $l1
      i32.load
      local.tee $p0
      f32.const 0x1.333334p-1 (;=0.6;)
      local.get $p0
      i32.load
      i32.load offset=40
      call_indirect $__indirect_function_table (type $t21)
      local.get $l1
      i32.load
      local.tee $p0
      f32.const 0x0p+0 (;=0;)
      local.get $p0
      i32.load
      i32.load offset=48
      call_indirect $__indirect_function_table (type $t21)
    end
    local.get $l1
    i32.const 16
    i32.add
    global.set $g0)
