  (func $f78669 (type $t5) (param $p0 i32) (result i32)
    (local $l1 i32)
    global.get $g0
    i32.const 48
    i32.sub
    local.tee $l1
    global.set $g0
    block $B0
      local.get $p0
      i32.load
      i32.eqz
      if $I1
        i32.const -1
        local.set $p0
        br $B0
      end
      local.get $l1
      i32.const 8
      i32.add
      local.get $p0
      call $f79963
      local.get $l1
      i32.const -1
      i32.store offset=40
      local.get $l1
      i32.const 40
      i32.add
      local.get $l1
      i32.const 8
      i32.add
      local.get $l1
      i32.load offset=8
      local.get $l1
      i32.load8_u offset=28
      i32.const 1
      i32.eq
      select
      call $f78598
      local.get $l1
      i32.load offset=40
      local.set $p0
      local.get $l1
      i32.load8_u offset=28
      br_if $B0
      local.get $l1
      i32.load offset=8
      local.get $l1
      i32.load offset=32
      i32.const 403047
      i32.const 518
      call $f83342
    end
    local.get $l1
    i32.const 48
    i32.add
    global.set $g0
    local.get $p0)
