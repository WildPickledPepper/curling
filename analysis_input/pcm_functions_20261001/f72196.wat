  (func $f72196 (type $t3) (param $p0 i32) (param $p1 i32) (param $p2 i32) (result i32)
    (local $l3 i32)
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
      i32.const 2164
      i32.const 3186937
      i32.const 0
      call $f69760
      i32.const 0
      return
    end
    block $B1
      local.get $p0
      i32.load offset=6060
      i32.const 0
      local.get $p1
      i32.sub
      call $f69749
      i32.eqz
      br_if $B1
      local.get $p0
      i32.const 32
      i32.add
      local.tee $p1
      call $f71427
      local.get $p0
      i32.const 16
      i32.add
      call $f72020
      local.get $p1
      call $f71392
      local.get $p0
      call $f72192
      local.get $p1
      call $f71426
      local.get $p1
      call $f71394
      local.get $p1
      i32.const 0
      call $f71393
      local.get $p0
      call $f72194
      i32.const 1
      local.set $l3
      local.get $p2
      i32.eqz
      br_if $B1
      local.get $p2
      i32.const 0
      i32.store
    end
    local.get $l3)