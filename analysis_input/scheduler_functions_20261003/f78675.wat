  (func $f78675 (type $t7) (param $p0 i32)
    (local $l1 i32) (local $l2 i32) (local $l3 i32) (local $l4 i32)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l2
    global.set $g0
    local.get $p0
    i32.const 4
    i32.add
    local.set $l4
    block $B0
      local.get $p0
      i32.load offset=12
      local.tee $l1
      i32.eqz
      if $I1
        local.get $p0
        i32.load offset=16
        i32.const 31
        i32.le_u
        if $I2
          local.get $l4
          i32.const 16
          i32.const 1
          call $f66024
        end
        local.get $p0
        i32.const 16
        i32.store offset=12
        local.get $p0
        i32.load offset=4
        local.tee $l1
        i64.const 0
        i64.store align=1
        local.get $l1
        i64.const 0
        i64.store offset=56 align=1
        local.get $l1
        i64.const 0
        i64.store offset=48 align=1
        local.get $l1
        i64.const 0
        i64.store offset=40 align=1
        local.get $l1
        i64.const 0
        i64.store offset=32 align=1
        local.get $l1
        i64.const 0
        i64.store offset=24 align=1
        local.get $l1
        i64.const 0
        i64.store offset=16 align=1
        local.get $l1
        i64.const 0
        i64.store offset=8 align=1
        br $B0
      end
      local.get $p0
      i32.load
      local.set $l3
      local.get $l2
      i64.const 4294967296
      i64.store offset=8
      local.get $l2
      local.get $l3
      i32.store offset=4
      local.get $l2
      i32.const 0
      i32.store
      local.get $l1
      i32.const 1
      i32.shl
      local.tee $l3
      if $I3 (result i32)
        local.get $l2
        local.get $l3
        i32.const 1
        call $f66024
        local.get $l2
        local.get $l3
        i32.store offset=8
        local.get $l2
        i32.load
        i32.const 0
        local.get $l1
        i32.const 3
        i32.shl
        call $f484
        drop
        local.get $l2
        i32.load offset=8
        i32.const 1
        i32.sub
      else
        i32.const -1
      end
      local.set $l3
      local.get $p0
      i32.load offset=20
      local.tee $l1
      local.get $p0
      i32.load offset=24
      i32.lt_u
      if $I4
        loop $L5
          local.get $l2
          i32.load
          local.get $l1
          local.get $l3
          i32.and
          i32.const 2
          i32.shl
          i32.add
          local.get $p0
          i32.load offset=4
          local.get $p0
          i32.load offset=28
          local.get $l1
          i32.and
          i32.const 2
          i32.shl
          i32.add
          i32.load
          i32.store
          local.get $l1
          i32.const 1
          i32.add
          local.tee $l1
          local.get $p0
          i32.load offset=24
          i32.lt_u
          br_if $L5
        end
      end
      local.get $l4
      local.get $l2
      call $f67186
      local.get $l2
      call $f554
      drop
    end
    local.get $p0
    local.get $p0
    i32.load offset=12
    i32.const 1
    i32.sub
    i32.store offset=28
    local.get $l2
    i32.const 16
    i32.add
    global.set $g0)
