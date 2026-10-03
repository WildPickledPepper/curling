  (func $f72197 (type $t8) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (result i32)
    local.get $p0
    i32.const 4648
    i32.add
    i32.load
    i32.const 3
    i32.ne
    if $I0
      i32.const 4700888
      i32.load
      i32.const 8
      i32.const 3184128
      i32.const 2215
      i32.const 3187041
      i32.const 0
      call $f69760
      i32.const 0
      return
    end
    local.get $p0
    i32.load offset=6060
    i32.const 0
    local.get $p3
    i32.sub
    call $f69749
    if $I1 (result i32)
      local.get $p0
      i32.const 32
      i32.add
      local.tee $p3
      call $f71427
      local.get $p0
      i32.const 16
      i32.add
      call $f72020
      local.get $p3
      call $f71392
      local.get $p0
      call $f72192
      local.get $p3
      call $f71426
      local.get $p3
      call $f71394
      local.get $p2
      local.get $p3
      call $f71424
      local.tee $p3
      i32.load offset=4
      i32.store
      local.get $p1
      local.get $p3
      i32.load
      i32.store
      local.get $p0
      i32.const 1
      i32.store8 offset=6354
      i32.const 1
    else
      i32.const 0
    end)