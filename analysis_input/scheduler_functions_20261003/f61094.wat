  (func $f61094 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $p1
    global.set $g0
    i32.const 4675159
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3754772
      call $f1661
      i32.const 3827264
      call $f1661
      i32.const 3827272
      call $f1661
      i32.const 3827268
      call $f1661
      i32.const 3827276
      call $f1661
      i32.const 4675159
      i32.const 1
      i32.store8
    end
    f32.const 0x1p+2 (;=4;)
    i32.const 0
    call $f54557
    i32.const 3754772
    i32.load
    local.tee $l2
    i32.load offset=116
    i32.eqz
    if $I1
      local.get $l2
      call $f65192
    end
    local.get $p1
    i32.const 0
    call $f18204
    i32.store offset=8
    local.get $p1
    i32.const 8
    i32.add
    i32.const 0
    call $f18194
    i32.const 3827264
    i32.load
    i32.const 0
    call $f53861
    if $I2
      local.get $p0
      i32.const 8
      i32.store offset=176
    end
    i32.const 3754772
    i32.load
    local.tee $l2
    i32.load offset=116
    i32.eqz
    if $I3
      local.get $l2
      call $f65192
    end
    local.get $p1
    i32.const 0
    call $f18204
    i32.store offset=8
    local.get $p1
    i32.const 8
    i32.add
    i32.const 0
    call $f18194
    i32.const 3827268
    i32.load
    i32.const 0
    call $f53861
    if $I4
      local.get $p0
      i32.const 4
      i32.store offset=176
    end
    i32.const 3754772
    i32.load
    local.tee $l2
    i32.load offset=116
    i32.eqz
    if $I5
      local.get $l2
      call $f65192
    end
    local.get $p1
    i32.const 0
    call $f18204
    i32.store offset=8
    local.get $p1
    i32.const 8
    i32.add
    i32.const 0
    call $f18194
    i32.const 3827276
    i32.load
    i32.const 0
    call $f53861
    if $I6
      local.get $p0
      i32.const 7
      i32.store offset=176
      f32.const 0x1.8p+6 (;=96;)
      i32.const 0
      call $f54557
    end
    i32.const 3754772
    i32.load
    local.tee $l2
    i32.load offset=116
    i32.eqz
    if $I7
      local.get $l2
      call $f65192
    end
    local.get $p1
    i32.const 0
    call $f18204
    i32.store offset=8
    local.get $p1
    i32.const 8
    i32.add
    i32.const 0
    call $f18194
    i32.const 3827272
    i32.load
    i32.const 0
    call $f53861
    if $I8
      local.get $p0
      i32.const 1
      i32.store8 offset=180
      local.get $p0
      i32.const 4
      i32.store offset=176
    end
    local.get $p1
    i32.const 16
    i32.add
    global.set $g0)
