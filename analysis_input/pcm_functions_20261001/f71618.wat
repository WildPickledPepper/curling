  (func $f71618 (type $t17) (param $p0 i32) (param $p1 f32) (param $p2 i32)
    (local $l3 i32) (local $l4 i32) (local $l5 i32)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l3
    global.set $g0
    local.get $p0
    local.get $p1
    f32.store offset=156
    local.get $p0
    i32.load
    local.tee $p0
    if $I0
      local.get $p0
      i32.load offset=40
      i32.load offset=1012
      local.set $l4
      local.get $p0
      i32.load offset=44
      i32.load8_u offset=9
      local.set $l5
      local.get $l3
      local.get $p0
      i64.load offset=144
      i64.store offset=8
      local.get $l4
      local.get $l5
      i32.const 2
      i32.eq
      local.get $l3
      i32.const 8
      i32.add
      local.get $l4
      i32.load
      i32.load offset=44
      call_indirect $__indirect_function_table (type $t2)
      i32.const 1
      local.get $p1
      f32.const 0x0p+0 (;=0;)
      f32.gt
      local.get $p2
      select
      if $I1
        local.get $p0
        call $f71571
      end
      local.get $p0
      local.get $p1
      local.get $p2
      call $f71566
    end
    local.get $l3
    i32.const 16
    i32.add
    global.set $g0)