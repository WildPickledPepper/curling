  (func $f71572 (type $t7) (param $p0 i32)
    (local $l1 i32)
    local.get $p0
    i32.load offset=164
    local.tee $l1
    if $I0
      block $B1
        local.get $l1
        i32.load offset=8
        local.tee $p0
        f32.load offset=32
        f32.const 0x1.999998p-2 (;=0.4;)
        f32.lt
        i32.eqz
        br_if $B1
        local.get $p0
        f32.const 0x1.999998p-2 (;=0.4;)
        f32.store offset=32
        local.get $l1
        i32.load offset=16
        i32.eqz
        br_if $B1
        i32.const 0
        local.set $p0
        loop $L2
          local.get $l1
          i32.load offset=24
          local.get $p0
          i32.const 2
          i32.shl
          i32.add
          i32.load
          f32.const 0x1.999998p-2 (;=0.4;)
          call $f71573
          local.get $p0
          i32.const 1
          i32.add
          local.tee $p0
          local.get $l1
          i32.load offset=16
          i32.lt_u
          br_if $L2
        end
      end
      return
    end
    block $B3
      local.get $p0
      i32.load offset=44
      local.tee $l1
      i32.load8_u offset=44
      i32.const 1
      i32.and
      br_if $B3
      local.get $l1
      f32.load offset=156
      f32.const 0x1.999998p-2 (;=0.4;)
      f32.lt
      i32.eqz
      br_if $B3
      local.get $l1
      f32.const 0x1.999998p-2 (;=0.4;)
      f32.store offset=156
      local.get $p0
      i32.load offset=40
      i32.load offset=1012
      local.tee $l1
      local.get $p0
      i32.load offset=44
      i32.load8_u offset=9
      i32.const 2
      i32.eq
      local.get $p0
      i32.const 144
      i32.add
      local.get $l1
      i32.load
      i32.load offset=44
      call_indirect $__indirect_function_table (type $t2)
      local.get $p0
      i32.load offset=156
      i32.const -2
      i32.ge_u
      if $I4
        local.get $p0
        i32.load offset=40
        local.get $p0
        call $f71379
        local.get $p0
        call $f71555
      end
      local.get $p0
      i32.load offset=40
      i32.load offset=1000
      local.get $p0
      i64.load offset=144
      call $f70712
      local.get $p0
      i32.const 92
      i32.add
      local.tee $p0
      local.get $p0
      i32.load16_u
      i32.const 65534
      i32.and
      i32.store16
    end)