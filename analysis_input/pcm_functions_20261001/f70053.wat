  (func $f70053 (type $t4) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32)
    (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 f32) (local $l15 f32)
    block $B0
      local.get $p0
      i32.load offset=2328
      local.tee $l5
      i32.eqz
      br_if $B0
      local.get $p0
      f32.load offset=2224
      local.get $p0
      local.get $l5
      i32.const 1
      i32.sub
      local.tee $l10
      i32.const 6
      i32.shl
      i32.add
      local.tee $l4
      f32.load
      local.get $p1
      f32.load
      f32.mul
      local.get $l4
      f32.load offset=4
      local.get $p1
      f32.load offset=4
      f32.mul
      f32.add
      local.get $l4
      f32.load offset=8
      local.get $p1
      f32.load offset=8
      f32.mul
      f32.add
      f32.lt
      i32.eqz
      br_if $B0
      local.get $l4
      i32.const 52
      i32.add
      local.set $l9
      local.get $p0
      i32.load offset=2324
      local.set $l6
      local.get $l4
      i32.load offset=48
      local.tee $l8
      local.get $l4
      i32.load offset=52
      local.tee $p1
      i32.lt_u
      if $I1
        loop $L2
          local.get $l6
          local.get $p3
          local.tee $l5
          i32.gt_u
          if $I3
            loop $L4
              local.get $p0
              f32.load offset=2240
              local.get $p0
              i32.load offset=2320
              local.tee $l7
              local.get $l5
              i32.const 6
              i32.shl
              local.tee $l11
              i32.add
              local.tee $p1
              f32.load offset=16
              local.get $l7
              local.get $l8
              i32.const 6
              i32.shl
              i32.add
              local.tee $l4
              f32.load offset=16
              f32.sub
              local.tee $l14
              local.get $l14
              f32.mul
              local.get $p1
              f32.load offset=20
              local.get $l4
              f32.load offset=20
              f32.sub
              local.tee $l14
              local.get $l14
              f32.mul
              f32.add
              local.get $p1
              i32.const 24
              i32.add
              local.tee $l12
              f32.load
              local.get $l4
              i32.const 24
              i32.add
              local.tee $l13
              f32.load
              f32.sub
              local.tee $l14
              local.get $l14
              f32.mul
              f32.add
              f32.gt
              if $I5
                local.get $l4
                f32.load offset=44
                local.get $p1
                f32.load offset=44
                f32.gt
                if $I6
                  local.get $l4
                  local.get $p1
                  i64.load
                  i64.store
                  local.get $l4
                  local.get $p1
                  i32.load offset=48
                  i32.store offset=48
                  local.get $l4
                  local.get $p1
                  i64.load offset=40
                  i64.store offset=40
                  local.get $l4
                  local.get $p1
                  i64.load offset=32
                  i64.store offset=32
                  local.get $l13
                  local.get $l12
                  i64.load
                  i64.store
                  local.get $l4
                  local.get $p1
                  i64.load offset=16
                  i64.store offset=16
                  local.get $l4
                  local.get $p1
                  i64.load offset=8
                  i64.store offset=8
                  local.get $p0
                  i32.load offset=2320
                  local.set $l7
                  local.get $p0
                  i32.load offset=2324
                  local.set $l6
                end
                local.get $l7
                local.get $l11
                i32.add
                local.tee $p1
                local.get $l6
                i32.const 6
                i32.shl
                local.get $l7
                i32.add
                i32.const -64
                i32.add
                local.tee $l4
                i64.load
                i64.store
                local.get $p1
                local.get $l4
                i32.load offset=48
                i32.store offset=48
                local.get $p1
                local.get $l4
                i64.load offset=40
                i64.store offset=40
                local.get $p1
                local.get $l4
                i64.load offset=32
                i64.store offset=32
                local.get $p1
                local.get $l4
                i64.load offset=24
                i64.store offset=24
                local.get $p1
                local.get $l4
                i64.load offset=16
                i64.store offset=16
                local.get $p1
                local.get $l4
                i64.load offset=8
                i64.store offset=8
                local.get $p0
                local.get $p0
                i32.load offset=2324
                i32.const 1
                i32.sub
                local.tee $l6
                i32.store offset=2324
                local.get $l5
                i32.const 1
                i32.sub
                local.set $l5
              end
              local.get $l5
              i32.const 1
              i32.add
              local.tee $l5
              local.get $l6
              i32.lt_u
              br_if $L4
            end
            local.get $l9
            i32.load
            local.set $p1
          end
          local.get $l8
          i32.const 1
          i32.add
          local.tee $l8
          local.get $p1
          i32.lt_u
          br_if $L2
        end
      end
      local.get $l9
      local.get $l6
      i32.store
      local.get $p0
      local.get $l10
      i32.const 6
      i32.shl
      i32.add
      local.tee $p1
      local.get $p2
      f32.load
      local.tee $l14
      local.get $p1
      f32.load offset=32
      local.tee $l15
      local.get $l14
      local.get $l15
      f32.lt
      select
      f32.store offset=32
      return
    end
    local.get $p0
    local.get $l5
    i32.const 6
    i32.shl
    i32.add
    local.tee $l4
    local.get $p3
    i32.store offset=48
    local.get $l4
    local.get $p0
    i32.load offset=2324
    i32.store offset=52
    local.get $l4
    local.get $p2
    i64.load
    i64.store offset=32
    local.get $l4
    local.get $p2
    i64.load offset=8
    i64.store offset=40
    local.get $p0
    local.get $l5
    i32.const 1
    i32.add
    i32.store offset=2328
    local.get $l4
    local.get $p1
    i64.load offset=8
    i64.store offset=8
    local.get $l4
    local.get $p1
    i64.load
    i64.store)
