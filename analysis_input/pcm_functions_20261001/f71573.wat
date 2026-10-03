  (func $f71573 (type $t21) (param $p0 i32) (param $p1 f32)
    (local $l2 i32)
    block $B0
      local.get $p0
      i32.load offset=44
      local.tee $l2
      i32.load8_u offset=44
      i32.const 1
      i32.and
      br_if $B0
      local.get $l2
      f32.load offset=156
      local.get $p1
      f32.lt
      i32.eqz
      br_if $B0
      local.get $l2
      local.get $p1
      f32.store offset=156
      local.get $p0
      i32.load offset=40
      i32.load offset=1012
      local.tee $l2
      local.get $p0
      i32.load offset=44
      i32.load8_u offset=9
      i32.const 2
      i32.eq
      local.get $p0
      i32.const 144
      i32.add
      local.get $l2
      i32.load
      i32.load offset=44
      call_indirect $__indirect_function_table (type $t2)
      local.get $p0
      i32.load offset=156
      i32.const -2
      i32.ge_u
      if $I1
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