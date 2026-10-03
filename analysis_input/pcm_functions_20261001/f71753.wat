  (func $f71753 (type $t9) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (result i32)
    (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32)
    global.get $g0
    i32.const 32
    i32.sub
    local.tee $l11
    global.set $g0
    block $B0
      local.get $p0
      i32.load offset=4
      local.tee $l9
      if $I1
        local.get $p0
        i32.load offset=292
        local.set $l7
        local.get $p0
        i32.load offset=296
        local.set $l12
        local.get $l11
        i32.const 0
        i32.store offset=16
        local.get $l11
        i64.const 0
        i64.store offset=8
        local.get $l12
        local.get $l7
        local.get $l9
        local.get $p1
        local.get $p2
        local.get $p3
        local.get $l11
        i32.const 8
        i32.add
        local.get $p4
        call $f71868
        i32.eqz
        br_if $B0
      end
      i32.const 1
      local.set $l5
      local.get $p0
      i32.load8_u offset=336
      i32.eqz
      br_if $B0
      local.get $p0
      i32.load offset=156
      local.get $p0
      i32.load offset=108
      i32.add
      i32.const 0
      local.get $p0
      i32.load offset=216
      i32.sub
      i32.eq
      br_if $B0
      i32.const 0
      local.set $l9
      global.get $g0
      i32.const 48
      i32.sub
      local.tee $l5
      global.set $g0
      block $B2
        local.get $p0
        i32.const 52
        i32.add
        local.tee $p0
        i32.load offset=104
        i32.const 0
        local.get $p0
        i32.load offset=56
        i32.sub
        i32.ne
        if $I3
          global.get $g0
          i32.const 32
          i32.sub
          local.tee $l10
          global.set $g0
          i32.const 1
          local.set $l6
          block $B4
            local.get $p0
            i32.const 4
            i32.add
            local.tee $l8
            i32.load offset=12
            local.tee $l7
            i32.eqz
            br_if $B4
            local.get $l7
            i32.load offset=588
            i32.eqz
            br_if $B4
            local.get $l8
            i32.load offset=104
            local.tee $l6
            i32.load offset=8
            local.set $l12
            local.get $l6
            i32.load offset=12
            local.set $l6
            local.get $l10
            i32.const 0
            i32.store offset=16
            local.get $l10
            i64.const 0
            i64.store offset=8
            local.get $l6
            local.get $l12
            local.get $l7
            local.get $p1
            local.get $p2
            local.get $p3
            local.get $p4
            call $f71869
            local.set $l6
          end
          block $B5
            local.get $l8
            i32.load offset=60
            local.tee $l7
            i32.eqz
            br_if $B5
            local.get $l7
            i32.load offset=588
            i32.eqz
            local.get $l6
            i32.const 1
            i32.xor
            i32.or
            br_if $B5
            local.get $l8
            i32.load offset=104
            local.tee $l8
            i32.load offset=8
            local.set $l6
            local.get $l8
            i32.load offset=12
            local.set $l8
            local.get $l10
            i32.const 0
            i32.store offset=16
            local.get $l10
            i64.const 0
            i64.store offset=8
            local.get $l8
            local.get $l6
            local.get $l7
            local.get $p1
            local.get $p2
            local.get $p3
            local.get $p4
            call $f71869
            local.set $l6
          end
          local.get $l10
          i32.const 32
          i32.add
          global.set $g0
          local.get $l6
          i32.eqz
          br_if $B2
        end
        local.get $p0
        i32.load offset=164
        i32.eqz
        if $I6
          i32.const 1
          local.set $l9
          br $B2
        end
        local.get $l5
        i32.const 0
        i32.store offset=40
        local.get $l5
        i64.const 0
        i64.store offset=32
        local.get $l5
        local.get $p0
        i32.load offset=124
        i32.store offset=28
        local.get $l5
        local.get $p4
        i32.store offset=24
        local.get $l5
        local.get $p2
        i32.store offset=16
        local.get $l5
        local.get $p1
        i32.store offset=12
        local.get $l5
        i32.const 3178900
        i32.store offset=8
        local.get $l5
        local.get $l5
        i32.const 32
        i32.add
        i32.store offset=20
        local.get $p0
        i32.load offset=200
        local.get $p0
        i32.load offset=196
        local.get $p0
        i32.load offset=168
        local.get $p1
        local.get $p2
        local.get $p3
        local.get $l5
        i32.const 32
        i32.add
        local.get $l5
        i32.const 8
        i32.add
        call $f71868
        local.set $l9
      end
      local.get $l5
      i32.const 48
      i32.add
      global.set $g0
      local.get $l9
      local.set $l5
    end
    local.get $l11
    i32.const 32
    i32.add
    global.set $g0
    local.get $l5)