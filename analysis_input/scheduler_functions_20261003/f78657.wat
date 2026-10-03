  (func $f78657 (type $t3) (param $p0 i32) (param $p1 i32) (param $p2 i32) (result i32)
    (local $l3 i32) (local $l4 i32) (local $l5 i32)
    i32.const 4758240
    i32.load
    local.set $l3
    i32.const 4787792
    i32.load
    local.tee $l5
    if $I0
      i32.const 12
      i32.const 16
      local.get $l3
      i32.load offset=268
      i32.const 0
      i32.const 403047
      i32.const 190
      call $f83341
      local.tee $l4
      i32.const 0
      i32.store offset=8
      local.get $l4
      local.get $p2
      i32.store offset=4
      local.get $l4
      local.get $p1
      i32.store
      local.get $l3
      i32.load offset=220
      local.tee $p1
      i32.const 1
      i32.add
      local.tee $p2
      local.get $l3
      i32.load offset=224
      i32.const 1
      i32.shr_u
      i32.gt_u
      if $I1
        local.get $l3
        i32.const 212
        i32.add
        call $f580
      end
      local.get $l3
      local.get $p2
      i32.store offset=220
      local.get $l3
      i32.load offset=212
      local.get $p1
      i32.const 3
      i32.shl
      i32.add
      local.tee $l3
      local.get $l4
      i32.store offset=4
      local.get $l3
      local.get $p0
      i32.store
      local.get $p0
      i32.load
      local.set $p1
      local.get $p0
      local.get $l4
      i32.store
      local.get $l4
      local.get $p1
      i32.store offset=8
    end
    i32.const 0
    i32.const -1
    local.get $l5
    select)
