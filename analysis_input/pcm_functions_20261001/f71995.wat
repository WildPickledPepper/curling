  (func $f71995 (type $t2) (param $p0 i32) (param $p1 i32) (param $p2 i32)
    (local $l3 i32)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l3
    global.set $g0
    block $B0
      local.get $p1
      i32.load offset=4
      i32.const -1073741824
      i32.and
      i32.const -2147483648
      i32.ne
      br_if $B0
      block $B1
        local.get $p2
        if $I2
          local.get $p1
          local.get $l3
          i32.const 12
          i32.add
          local.get $l3
          i32.const 11
          i32.add
          call $f72634
          local.set $p2
          local.get $p0
          i32.const 16
          i32.add
          local.get $p1
          i32.load offset=4
          i32.const 22
          i32.shr_u
          i32.const 60
          i32.and
          i32.const 3181092
          i32.add
          i32.load
          local.get $p1
          i32.add
          local.get $l3
          i32.load offset=12
          local.get $p2
          i32.const 48
          i32.const 0
          local.get $l3
          i32.load8_u offset=11
          call $f71433
          br $B1
        end
        local.get $p1
        local.get $l3
        i32.const 12
        i32.add
        call $f72093
        local.set $p2
        local.get $p0
        i32.const 16
        i32.add
        local.get $p1
        i32.load offset=4
        i32.const 22
        i32.shr_u
        i32.const 60
        i32.and
        i32.const 3181092
        i32.add
        i32.load
        local.get $p1
        i32.add
        local.get $l3
        i32.load offset=12
        local.get $p2
        i32.const 48
        i32.const 0
        call $f71431
      end
      local.get $p2
      i32.eqz
      br_if $B0
      i32.const 0
      local.set $p1
      loop $L3
        local.get $l3
        i32.load offset=12
        local.get $p1
        i32.const 2
        i32.shl
        i32.add
        i32.load
        i32.const 32
        i32.add
        call $f71979
        local.get $p1
        i32.const 1
        i32.add
        local.tee $p1
        local.get $p2
        i32.ne
        br_if $L3
      end
    end
    local.get $l3
    i32.const 16
    i32.add
    global.set $g0)