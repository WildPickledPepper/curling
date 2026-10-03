  (func $f71609 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l3
    global.set $g0
    block $B0
      block $B1
        local.get $p0
        i32.load offset=176
        local.tee $l2
        i32.eqz
        br_if $B1
        local.get $l2
        i32.load8_u offset=31
        i32.const 1
        i32.ne
        br_if $B1
        local.get $l2
        local.get $p1
        f32.load
        f32.store offset=32
        local.get $l2
        local.get $p1
        f32.load offset=4
        f32.store offset=36
        local.get $l2
        local.get $p1
        f32.load offset=8
        f32.store offset=40
        br $B0
      end
      local.get $p0
      local.get $p1
      f32.load
      f32.store offset=128
      local.get $p0
      local.get $p1
      f32.load offset=4
      f32.store offset=132
      local.get $p0
      local.get $p1
      f32.load offset=8
      f32.store offset=136
      local.get $p0
      i32.load
      local.tee $p0
      i32.eqz
      br_if $B0
      local.get $p0
      i32.load offset=40
      i32.load offset=1012
      local.set $p1
      local.get $p0
      i32.load offset=44
      i32.load8_u offset=9
      local.set $l2
      local.get $l3
      local.get $p0
      i64.load offset=144
      i64.store offset=8
      local.get $p1
      local.get $l2
      i32.const 2
      i32.eq
      local.get $l3
      i32.const 8
      i32.add
      local.get $p1
      i32.load
      i32.load offset=44
      call_indirect $__indirect_function_table (type $t2)
    end
    local.get $l3
    i32.const 16
    i32.add
    global.set $g0)
