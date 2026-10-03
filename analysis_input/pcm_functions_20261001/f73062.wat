  (func $f73062 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 f32) (local $l4 f32)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l2
    global.set $g0
    local.get $p0
    block $B0 (result f32)
      local.get $p1
      i32.load offset=52
      local.tee $p1
      i32.eqz
      if $I1
        i32.const 4748492
        f32.load
        local.set $l3
        i32.const 4748488
        f32.load
        local.set $l4
        i32.const 4748496
        f32.load
        br $B0
      end
      local.get $l2
      local.get $p1
      local.get $p1
      i32.load
      i32.load offset=156
      call_indirect $__indirect_function_table (type $t1)
      local.get $l2
      f32.load offset=4
      local.set $l3
      local.get $l2
      f32.load
      local.set $l4
      local.get $l2
      f32.load offset=8
    end
    f32.store offset=8
    local.get $p0
    local.get $l3
    f32.store offset=4
    local.get $p0
    local.get $l4
    f32.store
    local.get $l2
    i32.const 16
    i32.add
    global.set $g0)
