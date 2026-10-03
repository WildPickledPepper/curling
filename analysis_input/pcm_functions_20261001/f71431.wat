  (func $f71431 (type $t11) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32)
    (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32)
    block $B0
      block $B1
        local.get $p0
        i32.load offset=2388
        local.tee $l8
        i32.load offset=12
        local.tee $l9
        local.get $l8
        i32.load offset=8
        local.tee $l10
        i32.const 12
        i32.mul
        i32.add
        local.tee $l7
        i32.load offset=4
        local.tee $l6
        if $I2
          local.get $l7
          local.get $l6
          i32.load
          i32.store offset=4
          br $B1
        end
        block $B3 (result i32)
          block $B4
            local.get $l7
            i32.load offset=8
            local.tee $l6
            local.get $l8
            i32.load
            i32.eq
            br_if $B4
            local.get $l8
            i32.load offset=4
            local.set $l11
            local.get $l7
            local.get $l6
            i32.const 1
            i32.add
            i32.store offset=8
            local.get $l9
            local.get $l10
            i32.const 12
            i32.mul
            i32.add
            i32.load
            local.tee $l7
            i32.eqz
            br_if $B4
            local.get $l7
            local.get $l6
            local.get $l11
            i32.mul
            i32.add
            br $B3
          end
          local.get $l8
          call $f71372
        end
        local.tee $l6
        br_if $B1
        i32.const 0
        local.set $l6
        br $B0
      end
      local.get $l6
      local.get $p0
      local.get $p1
      call $f71726
      drop
      local.get $l6
      i32.const 3166676
      i32.store
    end
    local.get $p0
    local.get $p0
    i32.load offset=2664
    i32.const 1
    i32.add
    i32.store offset=2664
    local.get $p0
    local.get $p2
    local.get $p3
    local.get $p4
    local.get $l6
    local.get $p5
    call $f71428)