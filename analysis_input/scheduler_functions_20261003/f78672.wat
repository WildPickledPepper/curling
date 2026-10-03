  (func $f78672 (type $t7) (param $p0 i32)
    (local $l1 i32) (local $l2 i32)
    i32.const 4758716
    i32.load
    local.tee $p0
    if $I0
      local.get $p0
      i32.const 484
      i32.add
      call $f554
      drop
      local.get $p0
      i32.load offset=456
      local.tee $l1
      i32.const 403680
      i32.ne
      if $I1
        local.get $l1
        local.get $p0
        i32.load offset=476
        i32.const 403047
        i32.const 1027
        call $f83342
      end
      local.get $p0
      i32.load offset=408
      local.get $p0
      i32.const 412
      i32.add
      call $f65735
      local.get $p0
      i32.const 436
      i32.add
      call $f554
      drop
      local.get $p0
      i32.const 416
      i32.add
      call $f554
      drop
      local.get $p0
      i32.const 340
      i32.add
      call $f65729
      local.get $p0
      i32.const 84
      i32.add
      local.tee $l1
      i32.load
      local.get $l1
      i32.const 4
      i32.add
      call $f65735
      local.get $l1
      i32.const 224
      i32.add
      call $f554
      drop
      local.get $l1
      i32.const 192
      i32.add
      call $f554
      drop
      local.get $l1
      i32.load offset=164
      local.tee $l2
      i32.const 403680
      i32.ne
      if $I2
        local.get $l2
        local.get $l1
        i32.load offset=184
        i32.const 403047
        i32.const 1027
        call $f83342
      end
      local.get $l1
      i32.load offset=140
      local.tee $l2
      i32.const 403680
      i32.ne
      if $I3
        local.get $l2
        local.get $l1
        i32.load offset=160
        i32.const 403047
        i32.const 1027
        call $f83342
      end
      local.get $l1
      i32.const 100
      i32.add
      call $f554
      drop
      local.get $l1
      i32.const 68
      i32.add
      call $f554
      drop
      local.get $l1
      i32.load offset=40
      local.tee $l2
      i32.const 403680
      i32.ne
      if $I4
        local.get $l2
        local.get $l1
        i32.load offset=60
        i32.const 403047
        i32.const 1027
        call $f83342
      end
      local.get $l1
      i32.load offset=16
      local.tee $l2
      i32.const 403680
      i32.ne
      if $I5
        local.get $l2
        local.get $l1
        i32.load offset=36
        i32.const 403047
        i32.const 1027
        call $f83342
      end
      local.get $p0
      i32.const 16
      i32.add
      call $f65729
      local.get $p0
      i32.const 16
      i32.const 403047
      i32.const 488
      call $f83342
    end
    i32.const 4758716
    i32.const 0
    i32.store)
