  (func $f78678 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32)
    global.get $g0
    i32.const 32
    i32.sub
    local.tee $l2
    global.set $g0
    local.get $p0
    i32.load offset=36
    local.tee $l3
    i32.const 0
    i32.gt_s
    if $I0
      i32.const 4758660
      i32.load8_u
      local.set $l5
      loop $L1
        local.get $l5
        i32.const 255
        i32.and
        local.set $l6
        i32.const 0
        local.set $l5
        local.get $l6
        if $I2
          local.get $p0
          i32.load offset=28
          local.get $l4
          i32.const 3
          i32.shl
          i32.add
          i32.load offset=4
          call $f78679
          i32.const 4758660
          i32.load8_u
          local.set $l5
          local.get $p0
          i32.load offset=36
          local.set $l3
        end
        local.get $l4
        i32.const 1
        i32.add
        local.tee $l4
        local.get $l3
        i32.lt_s
        br_if $L1
      end
    end
    block $B3
      local.get $p0
      i32.const 4131408
      call $f80185
      local.tee $l6
      i32.eqz
      br_if $B3
      local.get $l6
      i32.load offset=88
      local.tee $p0
      i32.const 0
      i32.le_s
      br_if $B3
      local.get $p1
      i32.load8_s
      local.tee $l3
      i32.const 0
      i32.ge_s
      local.set $p1
      i32.const 0
      local.set $l4
      loop $L4
        local.get $l6
        i32.load offset=80
        local.get $l4
        i32.const 2
        i32.shl
        i32.add
        i32.load
        i32.load offset=28
        local.tee $l5
        if $I5
          local.get $p1
          i32.eqz
          if $I6
            local.get $l2
            local.get $l3
            i32.store8 offset=24
            local.get $l2
            local.get $l3
            i32.store8 offset=15
            i32.const 4758716
            i32.load
            local.get $l5
            local.get $l2
            i32.const 15
            i32.add
            call $f78676
          end
          local.get $l2
          local.get $l3
          i32.store8 offset=14
          local.get $l2
          local.get $l3
          i32.store8 offset=16
          local.get $l5
          local.get $l2
          i32.const 14
          i32.add
          call $f78678
          local.get $l6
          i32.load offset=88
          local.set $p0
        end
        local.get $l4
        i32.const 1
        i32.add
        local.tee $l4
        local.get $p0
        i32.lt_s
        br_if $L4
      end
    end
    local.get $l2
    i32.const 32
    i32.add
    global.set $g0)
