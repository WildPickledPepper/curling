  (func $f78696 (type $t12)
    (local $l0 i32) (local $l1 i32)
    i32.const 4129148
    i32.load
    i32.const 136868
    i32.const 136988
    call $f65585
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l0
    global.set $g0
    local.get $l0
    i32.const -1
    i32.store offset=8
    local.get $l0
    i32.const 8
    i32.add
    i32.const 136988
    i32.const 136994
    call $f83231
    i32.const 4686312
    local.get $l0
    i32.load offset=8
    i32.const -1
    i32.xor
    i32.store
    i32.const 4676788
    i32.load
    if $I0
      i32.const 4
      i32.const 30
      i32.const 4
      i32.const 67
      call $f83338
      local.tee $l1
      i32.const 3099768
      i32.store
      i32.const 4686316
      local.get $l1
      i32.store
      i32.const 4676788
      i32.load
      local.tee $l1
      i32.const 4129140
      i32.const 41
      i32.const 4686316
      i32.load
      local.get $l1
      i32.load
      i32.load offset=4
      call_indirect $__indirect_function_table (type $t4)
    end
    local.get $l0
    i32.const 16
    i32.add
    global.set $g0
    i32.const 4745216
    i32.load
    i32.const 4129140
    i32.const 4786524
    i32.const 125840
    i32.const 0
    call $f78025)
