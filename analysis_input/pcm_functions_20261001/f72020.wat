  (func $f72020 (type $t7) (param $p0 i32)
    (local $l1 i32) (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32)
    local.get $p0
    i32.const 4928
    i32.add
    i32.load
    if $I0
      loop $L1
        local.get $p0
        i32.load offset=4896
        local.get $l3
        i32.const 2
        i32.shl
        i32.add
        i32.load
        call $f72021
        local.get $l3
        i32.const 1
        i32.add
        local.tee $l3
        local.get $p0
        i32.load offset=4928
        i32.lt_u
        br_if $L1
      end
    end
    local.get $p0
    i32.const 4968
    i32.add
    i32.load
    if $I2
      i32.const 0
      local.set $l3
      loop $L3
        local.get $p0
        i32.load offset=4936
        local.get $l3
        i32.const 2
        i32.shl
        i32.add
        i32.load
        call $f72021
        local.get $l3
        i32.const 1
        i32.add
        local.tee $l3
        local.get $p0
        i32.load offset=4968
        i32.lt_u
        br_if $L3
      end
    end
    local.get $p0
    i32.const 16
    i32.add
    local.set $l3
    block $B4
      local.get $p0
      i32.const 5008
      i32.add
      i32.load
      i32.eqz
      br_if $B4
      loop $L5
        block $B6
          local.get $p0
          i32.load offset=4976
          local.get $l1
          i32.const 2
          i32.shl
          i32.add
          i32.load
          local.tee $l2
          i32.load offset=4
          i32.const -1073741824
          i32.lt_u
          br_if $B6
          local.get $l3
          local.get $l2
          i32.const 12
          i32.add
          call $f71405
          local.get $l2
          i32.load8_u offset=7
          i32.const 16
          i32.and
          br_if $B6
          local.get $l2
          call $f72017
        end
        local.get $l1
        i32.const 1
        i32.add
        local.tee $l1
        local.get $p0
        i32.load offset=5008
        local.tee $l2
        i32.lt_u
        br_if $L5
      end
      local.get $l2
      i32.eqz
      br_if $B4
      local.get $p0
      i32.load offset=4976
      local.set $l5
      i32.const 0
      local.set $l1
      loop $L7
        local.get $l5
        local.get $l1
        i32.const 2
        i32.shl
        i32.add
        i32.load
        local.tee $l4
        i32.load offset=4
        i32.const 268435457
        i32.and
        i32.const 268435457
        i32.eq
        if $I8
          local.get $l4
          i32.const 12
          i32.add
          call $f71670
          local.get $p0
          i32.load offset=5008
          local.set $l2
        end
        local.get $l1
        i32.const 1
        i32.add
        local.tee $l1
        local.get $l2
        i32.lt_u
        br_if $L7
      end
    end
    local.get $p0
    i32.const 5088
    i32.add
    i32.load
    local.tee $l2
    if $I9
      i32.const 0
      local.set $l1
      loop $L10
        local.get $p0
        i32.load offset=5056
        local.get $l1
        i32.const 2
        i32.shl
        i32.add
        i32.load
        local.tee $l4
        i32.load offset=4
        i32.const -1073741824
        i32.ge_u
        if $I11
          local.get $l4
          i32.const 12
          i32.add
          call $f71409
          local.get $p0
          i32.load offset=5088
          local.set $l2
        end
        local.get $l1
        i32.const 1
        i32.add
        local.tee $l1
        local.get $l2
        i32.lt_u
        br_if $L10
      end
    end
    local.get $p0
    i32.load offset=4928
    local.tee $l2
    if $I12
      i32.const 0
      local.set $l1
      loop $L13
        local.get $p0
        i32.load offset=4896
        local.get $l1
        i32.const 2
        i32.shl
        i32.add
        i32.load
        local.tee $l4
        i32.load offset=4
        local.tee $l5
        i32.const -1073741824
        i32.ge_u
        if $I14
          local.get $l3
          local.get $l4
          local.get $l5
          i32.const 16
          i32.and
          i32.const 4
          i32.shr_u
          call $f71999
          local.get $p0
          i32.load offset=4928
          local.set $l2
        end
        local.get $l1
        i32.const 1
        i32.add
        local.tee $l1
        local.get $l2
        i32.lt_u
        br_if $L13
      end
    end
    local.get $p0
    i32.load offset=4968
    if $I15
      i32.const 0
      local.set $l1
      loop $L16
        block $B17
          local.get $p0
          i32.load offset=4936
          local.get $l1
          i32.const 2
          i32.shl
          i32.add
          i32.load
          local.tee $l2
          i32.load offset=4
          local.tee $l4
          i32.const -1073741824
          i32.lt_u
          br_if $B17
          local.get $l3
          local.get $l2
          local.get $l4
          i32.const 16
          i32.and
          i32.const 4
          i32.shr_u
          call $f72002
          local.get $l2
          i32.load8_u offset=7
          i32.const 16
          i32.and
          br_if $B17
          local.get $l2
          call $f72014
        end
        local.get $l1
        i32.const 1
        i32.add
        local.tee $l1
        local.get $p0
        i32.load offset=4968
        i32.lt_u
        br_if $L16
      end
    end
    local.get $p0
    i32.const 5048
    i32.add
    i32.load
    if $I18
      i32.const 0
      local.set $l1
      loop $L19
        block $B20
          local.get $p0
          i32.load offset=5016
          local.get $l1
          i32.const 2
          i32.shl
          i32.add
          i32.load
          local.tee $l2
          i32.load offset=4
          local.tee $l4
          i32.const -1073741824
          i32.lt_u
          br_if $B20
          local.get $l2
          local.get $l4
          i32.const -769
          i32.and
          i32.store offset=4
          local.get $l3
          local.get $l2
          i32.const 12
          i32.add
          call $f71407
          local.get $l2
          i32.load8_u offset=7
          i32.const 16
          i32.and
          br_if $B20
          local.get $l2
          call $f72018
        end
        local.get $l1
        i32.const 1
        i32.add
        local.tee $l1
        local.get $p0
        i32.load offset=5048
        i32.lt_u
        br_if $L19
      end
    end
    local.get $p0
    i32.const 5128
    i32.add
    i32.load
    local.tee $l4
    if $I21
      i32.const 0
      local.set $l1
      loop $L22
        local.get $p0
        i32.load offset=5096
        local.get $l1
        i32.const 2
        i32.shl
        i32.add
        i32.load
        local.tee $l2
        i32.load offset=4
        i32.const -1073741824
        i32.ge_u
        if $I23
          local.get $l2
          local.get $p0
          call $f72012
          local.get $l3
          local.get $l2
          i32.load offset=16
          call $f71446
          local.get $p0
          i32.load offset=5128
          local.set $l4
        end
        local.get $l1
        i32.const 1
        i32.add
        local.tee $l1
        local.get $l4
        i32.lt_u
        br_if $L22
      end
    end)