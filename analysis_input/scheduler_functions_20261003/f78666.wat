  (func $f78666 (type $t7) (param $p0 i32)
    (local $l1 i32) (local $l2 i32) (local $l3 i32) (local $l4 i32)
    block $B0
      local.get $p0
      i32.load offset=240
      i32.eqz
      if $I1
        local.get $p0
        i32.load offset=256
        i32.eqz
        br_if $B0
      end
      local.get $p0
      i32.const 232
      i32.add
      local.get $p0
      i32.load offset=264
      i32.const -1
      i32.xor
      i32.const 1
      i32.and
      local.tee $l4
      i32.const 4
      i32.shl
      i32.add
      local.tee $l1
      i32.const 8
      i32.add
      local.set $l2
      local.get $l1
      i32.load offset=8
      if $I2
        loop $L3
          local.get $l1
          i32.load
          local.get $l3
          i32.const 2
          i32.shl
          i32.add
          i32.load
          local.get $p0
          i32.load offset=268
          i32.const 403047
          i32.const 394
          call $f83342
          local.get $l3
          i32.const 1
          i32.add
          local.tee $l3
          local.get $l2
          i32.load
          i32.lt_u
          br_if $L3
        end
      end
      local.get $l2
      i32.const 0
      i32.store
      local.get $p0
      local.get $l4
      i32.store offset=264
    end)
