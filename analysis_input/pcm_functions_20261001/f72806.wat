  (func $f72806 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32)
    global.get $g0
    i32.const 32
    i32.sub
    local.tee $l2
    global.set $g0
    i32.const 9
    call $f80140
    call $f73714
    local.get $p0
    i32.load offset=40
    if $I0
      local.get $p0
      local.get $p0
      i32.load
      i32.load offset=152
      call_indirect $__indirect_function_table (type $t7)
    end
    local.get $l2
    local.get $p0
    i32.load offset=28
    i32.const 4131408
    call $f80185
    call $f78122
    local.get $l2
    i32.const 16
    i32.add
    local.get $p0
    local.get $l2
    call $f72801
    local.get $l2
    local.get $l2
    f32.load offset=24
    f32.store offset=12
    local.get $l2
    local.get $l2
    i64.load offset=16
    i64.store offset=4 align=4
    local.get $l2
    i32.const 3
    i32.store
    local.get $p0
    local.get $l2
    local.get $p1
    call $f73283
    local.get $l2
    i32.const 32
    i32.add
    global.set $g0)
