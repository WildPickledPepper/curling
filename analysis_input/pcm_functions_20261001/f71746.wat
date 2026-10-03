  (func $f71746 (type $t2) (param $p0 i32) (param $p1 i32) (param $p2 i32)
    (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l4
    global.set $g0
    block $B0
      local.get $p2
      i32.eqz
      br_if $B0
      local.get $p0
      i32.const 1
      i32.store8 offset=337
      local.get $p0
      i32.load8_u offset=336
      i32.eqz
      br_if $B0
      local.get $p0
      i32.load offset=4
      i32.eqz
      br_if $B0
      local.get $p0
      i32.const 1
      i32.store8 offset=338
      local.get $p0
      i32.const 352
      i32.add
      local.set $l6
      local.get $p0
      i32.const 52
      i32.add
      local.set $l7
      local.get $p0
      i32.load offset=296
      local.set $l8
      local.get $p0
      i32.load offset=292
      local.set $l9
      loop $L1
        local.get $l4
        local.get $p0
        i32.load offset=300
        local.get $p1
        local.get $l5
        i32.const 2
        i32.shl
        i32.add
        i32.load
        i32.const 2
        i32.shl
        i32.add
        i32.load
        local.tee $l3
        i32.store offset=12
        block $B2
          block $B3
            local.get $p0
            i32.load offset=316
            local.get $l3
            i32.le_u
            br_if $B3
            local.get $p0
            i32.load offset=312
            local.get $l3
            i32.const 2
            i32.shl
            i32.add
            i32.load
            local.tee $l10
            i32.const -1
            i32.eq
            br_if $B3
            local.get $p0
            i32.load offset=4
            local.get $l10
            call $f71747
            br $B2
          end
          local.get $l7
          local.get $l9
          local.get $l3
          i32.const 24
          i32.mul
          i32.add
          local.get $l8
          local.get $l3
          i32.const 3
          i32.shl
          i32.add
          local.get $l3
          call $f71864
        end
        block $B4
          local.get $p0
          i32.load offset=268
          i32.const 3
          i32.sub
          i32.const 2
          i32.gt_u
          br_if $B4
          local.get $p0
          i32.load offset=356
          local.tee $l3
          local.get $p0
          i32.load offset=360
          i32.const 2147483647
          i32.and
          i32.ge_u
          if $I5
            local.get $l6
            local.get $l4
            i32.const 12
            i32.add
            call $f72545
            br $B4
          end
          local.get $p0
          i32.load offset=352
          local.get $l3
          i32.const 2
          i32.shl
          i32.add
          local.get $l4
          i32.load offset=12
          i32.store
          local.get $p0
          local.get $p0
          i32.load offset=356
          i32.const 1
          i32.add
          i32.store offset=356
        end
        local.get $l5
        i32.const 1
        i32.add
        local.tee $l5
        local.get $p2
        i32.ne
        br_if $L1
      end
    end
    local.get $l4
    i32.const 16
    i32.add
    global.set $g0)