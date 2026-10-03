  (func $f71768 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l2
    global.set $g0
    local.get $p1
    i32.load offset=4
    local.tee $l3
    if $I0
      local.get $p0
      i32.const 1
      call $f71743
      local.get $l2
      i64.const 0
      i64.store offset=8
      local.get $p0
      local.get $l3
      i32.store offset=4
      local.get $p1
      local.get $p0
      i32.const 12
      i32.add
      local.get $l2
      i32.const 8
      i32.add
      local.get $p0
      call $f70312
      local.get $p0
      local.get $p1
      local.get $l2
      i32.const 8
      i32.add
      call $f71758
    end
    local.get $l2
    i32.const 16
    i32.add
    global.set $g0)