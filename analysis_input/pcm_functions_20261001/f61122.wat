  (func $f61122 (type $t2) (param $p0 i32) (param $p1 i32) (param $p2 i32)
    (local $l3 i32) (local $l4 i32) (local $l5 i32)
    global.get $g0
    i32.const -64
    i32.add
    local.tee $l3
    global.set $g0
    i32.const 4675178
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3749908
      call $f1661
      i32.const 3751540
      call $f1661
      i32.const 3745776
      call $f1661
      i32.const 3857528
      call $f1661
      i32.const 3848724
      call $f1661
      i32.const 4675178
      i32.const 1
      i32.store8
    end
    i32.const 3745776
    i32.load
    i32.const 1
    call $f1052
    local.set $p2
    local.get $l3
    local.get $p0
    local.get $l3
    call $f61102
    i32.store offset=60
    block $B1
      i32.const 3751540
      i32.load
      local.get $l3
      i32.const 60
      i32.add
      call $f1675
      local.tee $l4
      if $I2
        local.get $l4
        local.get $p2
        i32.load
        i32.load offset=32
        call $f1674
        i32.eqz
        br_if $B1
      end
      local.get $p2
      local.get $l4
      i32.store offset=16
      local.get $p0
      i32.const 3848724
      i32.load
      local.get $p2
      local.get $l3
      call $f61061
      local.set $p2
      local.get $p0
      i32.load offset=328
      local.set $l4
      i32.const 3749908
      i32.load
      local.tee $l5
      i32.load offset=116
      i32.eqz
      if $I3
        local.get $l5
        call $f65192
      end
      local.get $l3
      i64.const 4764808406878388224
      i64.store offset=48
      local.get $l3
      i64.const 4764808406878388224
      i64.store offset=32
      local.get $l3
      i64.const 4776067405970997248
      i64.store offset=40
      local.get $l3
      i64.const 4776067405970997248
      i64.store offset=24
      local.get $l3
      i32.const 24
      i32.add
      local.get $p2
      local.get $l4
      i32.const 0
      call $f17350
      i32.const 3857528
      i32.load
      local.set $p2
      i32.const 4675128
      i32.load8_u
      i32.eqz
      if $I4
        i32.const 3753376
        call $f1661
        i32.const 4675128
        i32.const 1
        i32.store8
      end
      local.get $p0
      i32.load offset=32
      local.set $l4
      i32.const 3753376
      i32.load
      local.tee $l5
      i32.load offset=116
      i32.eqz
      if $I5
        local.get $l5
        call $f65192
      end
      block $B6
        local.get $l4
        i32.const 0
        i32.const 0
        call $f54425
        i32.eqz
        if $I7
          local.get $p0
          i32.load offset=32
          local.set $l4
          br $B6
        end
        i32.const 4675186
        i32.load8_u
        i32.eqz
        if $I8
          i32.const 3752300
          call $f1661
          i32.const 4675186
          i32.const 1
          i32.store8
        end
        local.get $p0
        i32.const 3752300
        i32.load
        i32.load offset=92
        i32.load
        local.tee $l4
        i32.store offset=32
      end
      local.get $l4
      local.get $p2
      i32.const 0
      call $f60665
      local.set $p2
      local.get $l3
      local.get $p1
      i64.load offset=8 align=4
      i64.store offset=16
      local.get $l3
      local.get $p1
      i64.load align=4
      i64.store offset=8
      local.get $l3
      i32.const 8
      i32.add
      local.get $p2
      i32.const 0
      call $f17366
      if $I9
        i32.const 4675165
        i32.load8_u
        i32.eqz
        if $I10
          i32.const 3759360
          call $f1661
          i32.const 4675165
          i32.const 1
          i32.store8
        end
        i32.const 3759360
        i32.load
        call $f1446
        local.tee $p2
        i32.const 0
        i32.const 0
        call $f3079
        local.get $p2
        local.get $p0
        i32.store offset=16
        local.get $p0
        local.get $p2
        i32.const 0
        call $f54440
        drop
      end
      block $B11
        local.get $p0
        i32.load8_u offset=304
        i32.eqz
        br_if $B11
        local.get $p0
        i32.load offset=312
        local.tee $p2
        i32.eqz
        br_if $B11
        local.get $p2
        i32.load offset=32
        local.get $p0
        i32.load offset=308
        local.get $p2
        i32.load offset=20
        local.get $p2
        i32.load offset=12
        call_indirect $__indirect_function_table (type $t2)
      end
      local.get $l3
      i32.const -64
      i32.sub
      global.set $g0
      return
    end
    call $f1684
    i32.const 0
    call $f1671
    unreachable)