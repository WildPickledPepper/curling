  (func $f78664 (type $t7) (param $p0 i32)
    (local $l1 i32) (local $l2 i32)
    i32.const 4758240
    i32.load
    local.tee $p0
    if $I0
      block $B1
        i32.const 4787792
        i32.load
        local.tee $l2
        i32.eqz
        br_if $B1
        local.get $p0
        i32.load offset=64
        local.tee $l1
        i32.load
        if $I2
          local.get $l2
          local.get $l1
          call $f80335
          local.get $p0
          i32.load offset=64
          local.set $l1
        end
        local.get $l1
        i32.load offset=8
        if $I3
          local.get $l2
          local.get $l1
          i32.const 8
          i32.add
          call $f80335
          local.get $p0
          i32.load offset=64
          local.set $l1
        end
        local.get $l1
        i32.load offset=16
        if $I4
          local.get $l2
          local.get $l1
          i32.const 16
          i32.add
          call $f80335
          local.get $p0
          i32.load offset=64
          local.set $l1
        end
        local.get $l1
        i32.load offset=24
        if $I5
          local.get $l2
          local.get $l1
          i32.const 24
          i32.add
          call $f80335
        end
        local.get $l2
        local.get $p0
        call $f80335
        local.get $p0
        i32.load offset=200
        if $I6
          local.get $l2
          local.get $p0
          call $f80336
        end
        local.get $p0
        i32.load offset=220
        i32.eqz
        br_if $B1
        i32.const 0
        local.set $l1
        loop $L7
          local.get $p0
          i32.load offset=212
          local.get $l1
          i32.const 3
          i32.shl
          i32.add
          local.tee $l2
          i32.load offset=4
          local.get $l2
          i32.load
          call $f80337
          local.get $l1
          i32.const 1
          i32.add
          local.tee $l1
          local.get $p0
          i32.load offset=220
          i32.lt_u
          br_if $L7
        end
      end
      local.get $p0
      i32.load offset=240
      if $I8
        i32.const 0
        local.set $l1
        loop $L9
          local.get $p0
          i32.load offset=232
          local.get $l1
          i32.const 2
          i32.shl
          i32.add
          i32.load
          local.get $p0
          i32.load offset=268
          i32.const 403047
          i32.const 72
          call $f83342
          local.get $l1
          i32.const 1
          i32.add
          local.tee $l1
          local.get $p0
          i32.load offset=240
          i32.lt_u
          br_if $L9
        end
      end
      local.get $p0
      i32.load offset=256
      if $I10
        i32.const 0
        local.set $l1
        loop $L11
          local.get $p0
          i32.load offset=248
          local.get $l1
          i32.const 2
          i32.shl
          i32.add
          i32.load
          local.get $p0
          i32.load offset=268
          i32.const 403047
          i32.const 72
          call $f83342
          local.get $l1
          i32.const 1
          i32.add
          local.tee $l1
          local.get $p0
          i32.load offset=256
          i32.lt_u
          br_if $L11
        end
      end
      local.get $p0
      i32.const 212
      i32.add
      local.set $l2
      local.get $p0
      i32.load offset=220
      if $I12
        i32.const 0
        local.set $l1
        loop $L13
          local.get $p0
          i32.load offset=212
          local.get $l1
          i32.const 3
          i32.shl
          i32.add
          i32.load offset=4
          local.get $p0
          i32.load offset=268
          i32.const 403047
          i32.const 78
          call $f83342
          local.get $l1
          i32.const 1
          i32.add
          local.tee $l1
          local.get $p0
          i32.load offset=220
          i32.lt_u
          br_if $L13
        end
      end
      local.get $p0
      i32.const 248
      i32.add
      call $f554
      drop
      local.get $p0
      i32.const 232
      i32.add
      call $f554
      drop
      local.get $l2
      call $f554
      drop
      local.get $p0
      i32.const 192
      i32.add
      call $f554
      drop
      local.get $p0
      i32.const -64
      i32.sub
      call $f554
      drop
      local.get $p0
      i32.const 63
      i32.const 403047
      i32.const 568
      call $f83342
    end
    i32.const 4758240
    i32.const 0
    i32.store)
