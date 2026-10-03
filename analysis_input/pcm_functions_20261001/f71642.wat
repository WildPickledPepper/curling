  (func $f71642 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32)
    block $B0
      local.get $p0
      i32.load offset=56
      br_if $B0
      local.get $p0
      i32.load offset=4
      i32.load offset=40
      local.set $l2
      local.get $p0
      i32.load offset=28
      call $f71419
      local.set $l3
      local.get $p1
      i32.eqz
      br_if $B0
      local.get $p0
      i32.load offset=44
      i32.const 98304
      i32.and
      br_if $B0
      local.get $p0
      i32.load offset=32
      call $f71419
      local.tee $p1
      i32.eqz
      br_if $B0
      local.get $p0
      i32.load8_u offset=46
      i32.const 4
      i32.and
      br_if $B0
      local.get $l2
      local.get $l3
      local.get $p1
      call $f71418
    end)
