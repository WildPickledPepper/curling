  (func $f71749 (type $t6) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32)
    (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l8
    global.set $g0
    block $B0
      local.get $p4
      i32.eqz
      br_if $B0
      local.get $p0
      i32.const 1
      i32.store8 offset=337
      loop $L1
        local.get $p3
        local.get $p2
        local.get $l7
        i32.const 2
        i32.shl
        local.tee $l6
        i32.add
        i32.load
        i32.const 24
        i32.mul
        i32.add
        local.tee $l5
        f32.load offset=4
        local.set $l15
        local.get $l5
        f32.load offset=16
        local.set $l16
        local.get $l5
        f32.load offset=8
        local.set $l17
        local.get $l5
        f32.load offset=20
        local.set $l14
        local.get $p0
        i32.load offset=292
        local.get $p0
        i32.load offset=300
        local.get $p1
        local.get $l6
        i32.add
        i32.load
        i32.const 2
        i32.shl
        i32.add
        i32.load
        i32.const 24
        i32.mul
        i32.add
        local.tee $l6
        local.get $l5
        f32.load offset=12
        local.tee $l13
        local.get $l13
        local.get $l5
        f32.load
        local.tee $l18
        f32.sub
        f32.const 0x1.47ae14p-8 (;=0.005;)
        f32.mul
        local.tee $l13
        f32.add
        f32.store offset=12
        local.get $l6
        local.get $l18
        local.get $l13
        f32.sub
        f32.store
        local.get $l6
        local.get $l14
        local.get $l14
        local.get $l17
        f32.sub
        f32.const 0x1.47ae14p-8 (;=0.005;)
        f32.mul
        local.tee $l13
        f32.add
        f32.store offset=20
        local.get $l6
        local.get $l16
        local.get $l16
        local.get $l15
        f32.sub
        f32.const 0x1.47ae14p-8 (;=0.005;)
        f32.mul
        local.tee $l14
        f32.add
        f32.store offset=16
        local.get $l6
        local.get $l17
        local.get $l13
        f32.sub
        f32.store offset=8
        local.get $l6
        local.get $l15
        local.get $l14
        f32.sub
        f32.store offset=4
        local.get $l7
        i32.const 1
        i32.add
        local.tee $l7
        local.get $p4
        i32.ne
        br_if $L1
      end
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
      local.set $l9
      local.get $p0
      i32.const 52
      i32.add
      local.set $l10
      local.get $p0
      i32.load offset=296
      local.set $l11
      i32.const 0
      local.set $l6
      loop $L2
        local.get $l8
        local.get $p0
        i32.load offset=300
        local.get $p1
        local.get $l6
        i32.const 2
        i32.shl
        local.tee $l7
        i32.add
        i32.load
        i32.const 2
        i32.shl
        i32.add
        i32.load
        local.tee $l5
        i32.store offset=12
        block $B3
          block $B4
            local.get $p0
            i32.load offset=316
            local.get $l5
            i32.le_u
            br_if $B4
            local.get $p0
            i32.load offset=312
            local.get $l5
            i32.const 2
            i32.shl
            i32.add
            i32.load
            local.tee $l12
            i32.const -1
            i32.eq
            br_if $B4
            local.get $p0
            i32.load offset=4
            local.get $l12
            call $f71747
            br $B3
          end
          local.get $l10
          local.get $p3
          local.get $p2
          local.get $l7
          i32.add
          i32.load
          i32.const 24
          i32.mul
          i32.add
          local.get $l11
          local.get $l5
          i32.const 3
          i32.shl
          i32.add
          local.get $l5
          call $f71864
        end
        block $B5
          local.get $p0
          i32.load offset=268
          i32.const 3
          i32.sub
          i32.const 2
          i32.gt_u
          br_if $B5
          local.get $p0
          i32.load offset=356
          local.tee $l5
          local.get $p0
          i32.load offset=360
          i32.const 2147483647
          i32.and
          i32.ge_u
          if $I6
            local.get $l9
            local.get $l8
            i32.const 12
            i32.add
            call $f72545
            br $B5
          end
          local.get $p0
          i32.load offset=352
          local.get $l5
          i32.const 2
          i32.shl
          i32.add
          local.get $l8
          i32.load offset=12
          i32.store
          local.get $p0
          local.get $p0
          i32.load offset=356
          i32.const 1
          i32.add
          i32.store offset=356
        end
        local.get $l6
        i32.const 1
        i32.add
        local.tee $l6
        local.get $p4
        i32.ne
        br_if $L2
      end
    end
    local.get $l8
    i32.const 16
    i32.add
    global.set $g0)