  (func $f78663 (type $t7) (param $p0 i32)
    (local $l1 i32) (local $l2 i32) (local $l3 i32)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $p0
    global.set $g0
    i32.const 320
    i32.const 64
    i32.const 63
    i32.const 0
    i32.const 403047
    i32.const 537
    call $f83341
    local.tee $l1
    i32.const 0
    i32.store offset=212
    local.get $l1
    i32.const 0
    i32.store offset=192
    local.get $l1
    i32.const 0
    i32.store offset=64
    local.get $l1
    i64.const 4294967296
    i64.store offset=220 align=4
    local.get $l1
    i32.const 63
    i32.store offset=216
    local.get $l1
    i64.const 4294967296
    i64.store offset=200
    local.get $l1
    i32.const 63
    i32.store offset=196
    local.get $l1
    i32.const 72
    i32.add
    local.tee $l2
    i64.const 4294967296
    i64.store
    local.get $l1
    i32.const 63
    i32.store offset=68
    local.get $l1
    i32.const 63
    i32.store offset=268
    local.get $l1
    i32.const 0
    i32.store offset=264
    local.get $l1
    i64.const 4294967296
    i64.store offset=256
    local.get $l1
    i64.const 322122547200
    i64.store offset=248
    local.get $l1
    i64.const 4294967296
    i64.store offset=240
    local.get $l1
    i64.const 322122547200
    i64.store offset=232
    local.get $l1
    i32.const -64
    i32.sub
    local.set $l3
    local.get $l2
    i32.load
    local.set $l2
    local.get $l1
    i32.load offset=76
    i32.const 7
    i32.le_u
    if $I0
      local.get $l3
      i32.const 4
      i32.const 1
      call $f65937
    end
    local.get $l1
    i32.const 4
    i32.store offset=72
    local.get $l2
    i32.const 3
    i32.le_u
    if $I1
      local.get $l2
      i32.const 3
      i32.shl
      local.tee $l2
      local.get $l3
      i32.load
      i32.add
      i32.const 0
      i32.const 32
      local.get $l2
      i32.sub
      call $f484
      drop
    end
    local.get $l1
    i32.load offset=204
    i32.const 7
    i32.le_u
    if $I2
      local.get $l1
      i32.const 192
      i32.add
      i32.const 4
      i32.const 8
      i32.const 4
      call $f545
    end
    local.get $l1
    i32.const 63
    i32.store offset=252
    local.get $l1
    i32.const 63
    i32.store offset=236
    i32.const 4787792
    i32.load
    local.tee $l2
    if $I3
      local.get $l2
      i32.const 125809
      local.get $l1
      call $f80338
    end
    i32.const 4758396
    i32.const 125797
    i32.store
    i32.const 4758392
    i32.const 125798
    i32.store
    i32.const 4758388
    i32.const 125799
    i32.store
    i32.const 4758384
    i32.const 125800
    i32.store
    i32.const 4758380
    i32.const 125801
    i32.store
    i32.const 4758376
    i32.const 125802
    i32.store
    i32.const 4758372
    i32.const 125803
    i32.store
    i32.const 4758368
    i32.const 125804
    i32.store
    i32.const 4758364
    i32.const 125805
    i32.store
    i32.const 4758360
    i32.const 125806
    i32.store
    i32.const 4758240
    local.get $l1
    i32.store
    i32.const 4681168
    i32.load
    local.set $l1
    local.get $p0
    i64.const -6483183887763680552
    i64.store offset=8
    local.get $p0
    i64.const 6282481042229840671
    i64.store
    local.get $p0
    i32.const 4758360
    local.get $l1
    call_indirect $__indirect_function_table (type $t1)
    i32.const 4758444
    i32.const 125807
    i32.store
    i32.const 4758440
    i32.const 125808
    i32.store
    i32.const 4758436
    i32.const 125797
    i32.store
    i32.const 4758432
    i32.const 125798
    i32.store
    i32.const 4758428
    i32.const 125799
    i32.store
    i32.const 4758424
    i32.const 125800
    i32.store
    i32.const 4758420
    i32.const 125801
    i32.store
    i32.const 4758416
    i32.const 125802
    i32.store
    i32.const 4758412
    i32.const 125803
    i32.store
    i32.const 4758408
    i32.const 125804
    i32.store
    i32.const 4758404
    i32.const 125805
    i32.store
    i32.const 4758400
    i32.const 125806
    i32.store
    i32.const 4681168
    i32.load
    local.set $l1
    local.get $p0
    i64.const -9085915283265821892
    i64.store offset=8
    local.get $p0
    i64.const 6767601720423695729
    i64.store
    local.get $p0
    i32.const 4758400
    local.get $l1
    call_indirect $__indirect_function_table (type $t1)
    local.get $p0
    i32.const 16
    i32.add
    global.set $g0)
