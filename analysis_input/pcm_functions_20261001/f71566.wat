  (func $f71566 (type $t17) (param $p0 i32) (param $p1 f32) (param $p2 i32)
    i32.const 1
    local.get $p1
    f32.const 0x0p+0 (;=0;)
    f32.gt
    local.get $p2
    select
    if $I0
      local.get $p0
      i32.load offset=40
      i32.load offset=1000
      local.get $p0
      i64.load offset=144
      call $f70712
      return
    end
    block $B1
      local.get $p0
      call $f71654
      i32.eqz
      br_if $B1
      local.get $p0
      i32.load offset=164
      br_if $B1
      local.get $p0
      i32.load offset=40
      i32.load offset=1000
      local.get $p0
      i64.load offset=144
      call $f70713
    end)