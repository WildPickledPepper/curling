  (func $f70232 (type $t10) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (result i32)
    (local $l6 i32)
    global.get $g0
    i32.const 4256
    i32.sub
    local.tee $l6
    global.set $g0
    local.get $l6
    i32.const -1
    i32.store offset=4200
    local.get $l6
    i32.const 4200
    i32.add
    local.get $p2
    call $f70398
    local.get $l6
    i32.const -1
    i32.store offset=4144
    local.get $l6
    i32.const 4144
    i32.add
    local.get $p4
    call $f70398
    local.get $l6
    i64.const 0
    i64.store offset=4136
    i32.const 0
    local.set $p4
    local.get $l6
    i32.const 0
    i32.store offset=4112
    local.get $l6
    i32.const 1065353216
    i32.store offset=8
    local.get $l6
    i64.const 0
    i64.store
    block $B0
      local.get $l6
      i32.const 4200
      i32.add
      local.get $l6
      i32.const 4144
      i32.add
      local.get $p3
      local.get $p5
      local.get $l6
      local.get $l6
      i32.const 16
      i32.add
      call $f70203
      i32.eqz
      br_if $B0
      local.get $p0
      local.get $p1
      local.get $l6
      i32.load offset=4112
      local.get $l6
      i32.const 16
      i32.add
      call $f70216
      i32.eqz
      br_if $B0
      local.get $l6
      i32.load offset=4112
      i32.const 0
      i32.ne
      local.set $p4
    end
    local.get $l6
    i32.const 4256
    i32.add
    global.set $g0
    local.get $p4)
