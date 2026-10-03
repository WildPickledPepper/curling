  (func $f60135 (type $t2) (param $p0 i32) (param $p1 i32) (param $p2 i32)
    (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32)
    global.get $g0
    i32.const 48
    i32.sub
    local.tee $p2
    global.set $g0
    i32.const 4674469
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3749908
      call $f1661
      i32.const 3792608
      call $f1661
      i32.const 3751540
      call $f1661
      i32.const 3745776
      call $f1661
      i32.const 3850008
      call $f1661
      i32.const 3850004
      call $f1661
      i32.const 3836056
      call $f1661
      i32.const 4674469
      i32.const 1
      i32.store8
    end
    block $B1
      local.get $p0
      i32.load offset=304
      i32.const 0
      i32.gt_s
      if $I2
        i32.const 3836056
        i32.load
        i32.const 0
        call $f54416
        i32.const 3792608
        i32.load
        call $f34548
        local.set $l3
        i32.const 3850008
        i32.load
        local.set $l4
        i32.const 4674403
        i32.load8_u
        i32.eqz
        if $I3
          i32.const 3753376
          call $f1661
          i32.const 4674403
          i32.const 1
          i32.store8
        end
        local.get $p0
        i32.load offset=44
        local.set $l5
        i32.const 3753376
        i32.load
        local.tee $l6
        i32.load offset=116
        i32.eqz
        if $I4
          local.get $l6
          call $f65192
        end
        block $B5
          local.get $l5
          i32.const 0
          i32.const 0
          call $f54425
          i32.eqz
          if $I6
            local.get $p0
            i32.load offset=44
            local.set $l5
            br $B5
          end
          i32.const 4675186
          i32.load8_u
          i32.eqz
          if $I7
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
          local.tee $l5
          i32.store offset=44
        end
        local.get $p0
        local.get $l3
        local.get $l5
        local.get $l4
        i32.const 0
        call $f60665
        local.get $p2
        call $f60138
        local.get $p0
        i32.load offset=304
        local.set $l4
        i32.const 3745776
        i32.load
        i32.const 1
        call $f1052
        local.set $l3
        local.get $p2
        local.get $l4
        i32.const 2
        i32.const 1
        local.get $l4
        i32.const 5
        i32.gt_s
        select
        i32.add
        i32.store offset=44
        i32.const 3751540
        i32.load
        local.get $p2
        i32.const 44
        i32.add
        call $f1675
        local.tee $l4
        if $I8
          local.get $l4
          local.get $l3
          i32.load
          i32.load offset=32
          call $f1674
          i32.eqz
          br_if $B1
        end
        local.get $l3
        local.get $l4
        i32.store offset=16
        local.get $p0
        i32.const 3850004
        i32.load
        local.get $l3
        local.get $p2
        call $f60055
        local.set $p0
        i32.const 3749908
        i32.load
        local.tee $l3
        i32.load offset=116
        i32.eqz
        if $I9
          local.get $l3
          call $f65192
        end
        local.get $p2
        i64.const 4764808406878388224
        i64.store offset=32
        local.get $p2
        i64.const 4764808406878388224
        i64.store offset=16
        local.get $p2
        i64.const 4776067405968703488
        i64.store offset=24
        local.get $p2
        i64.const 4776067405968703488
        i64.store offset=8
        local.get $p2
        i32.const 8
        i32.add
        local.get $p0
        local.get $p1
        i32.const 0
        call $f17350
      end
      local.get $p2
      i32.const 48
      i32.add
      global.set $g0
      return
    end
    call $f1684
    i32.const 0
    call $f1671
    unreachable)