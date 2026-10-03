  (func $f78152 (type $t5) (param $p0 i32) (result i32)
    (local $l1 i32) (local $l2 i32) (local $l3 i64)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l1
    global.set $g0
    local.get $p0
    i64.load offset=32 align=4
    local.tee $l3
    i32.wrap_i64
    local.tee $l2
    i64.load
    i64.eqz
    i32.eqz
    if $I0
      local.get $l2
      call $f79912
      local.get $l2
      call $f79911
      local.get $p0
      i64.load offset=32 align=4
      local.set $l3
    end
    local.get $l1
    local.get $l3
    i64.store
    local.get $l1
    local.get $l3
    i64.store offset=8
    local.get $l1
    call $f78236
    local.set $p0
    local.get $l1
    i32.const 16
    i32.add
    global.set $g0
    local.get $p0)
