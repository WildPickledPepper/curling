  (func $f78689 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32)
    local.get $p0
    local.get $p1
    i32.ne
    if $I0
      i32.const 403680
      local.set $l3
      local.get $p0
      i32.load
      local.tee $l2
      i32.const 403680
      i32.ne
      if $I1
        local.get $l2
        local.get $p0
        i32.load offset=20
        i32.const 403047
        i32.const 1027
        call $f83342
      end
      local.get $p0
      i32.const 0
      i32.store offset=12
      local.get $p0
      i64.const 0
      i64.store offset=4 align=4
      local.get $p0
      i32.const 403680
      i32.store
      local.get $p1
      i32.load offset=8
      local.tee $l2
      if $I2
        local.get $l2
        i32.const 3
        i32.mul
        i32.const 1
        i32.add
        i32.const 1
        i32.shr_u
        i32.const 1
        i32.sub
        local.tee $l2
        i32.const 16
        i32.shr_u
        local.get $l2
        i32.or
        local.tee $l2
        i32.const 8
        i32.shr_u
        local.get $l2
        i32.or
        local.tee $l2
        i32.const 4
        i32.shr_u
        local.get $l2
        i32.or
        local.tee $l2
        i32.const 2
        i32.shr_u
        local.get $l2
        i32.or
        local.tee $l2
        i32.const 1
        i32.shr_u
        local.get $l2
        i32.or
        local.tee $l2
        i32.const 1
        i32.add
        local.tee $l4
        i32.const 12
        i32.mul
        local.tee $l7
        i32.const 4
        local.get $p0
        i32.load offset=20
        i32.const 0
        i32.const 403047
        i32.const 1008
        call $f83341
        local.set $l3
        block $B3
          local.get $l7
          i32.eqz
          br_if $B3
          block $B4
            local.get $l2
            i32.const 12
            i32.mul
            local.tee $l5
            i32.const 12
            i32.div_u
            i32.const 1
            i32.add
            i32.const 7
            i32.and
            local.tee $l8
            i32.eqz
            if $I5
              local.get $l3
              local.set $l2
              br $B4
            end
            local.get $l3
            local.set $l2
            loop $L6
              local.get $l2
              i32.const -1
              i32.store
              local.get $l2
              i32.const 12
              i32.add
              local.set $l2
              local.get $l6
              i32.const 1
              i32.add
              local.tee $l6
              local.get $l8
              i32.ne
              br_if $L6
            end
          end
          local.get $l5
          i32.const 84
          i32.lt_u
          br_if $B3
          local.get $l3
          local.get $l7
          i32.add
          local.set $l6
          loop $L7
            local.get $l2
            i32.const -1
            i32.store offset=84
            local.get $l2
            i32.const -1
            i32.store offset=72
            local.get $l2
            i32.const -1
            i32.store offset=60
            local.get $l2
            i32.const -1
            i32.store offset=48
            local.get $l2
            i32.const -1
            i32.store offset=36
            local.get $l2
            i32.const -1
            i32.store offset=24
            local.get $l2
            i32.const -1
            i32.store offset=12
            local.get $l2
            i32.const -1
            i32.store
            local.get $l2
            i32.const 96
            i32.add
            local.tee $l2
            local.get $l6
            i32.ne
            br_if $L7
          end
        end
        local.get $p0
        local.get $l3
        i32.store
        local.get $p0
        local.get $l4
        i32.const 2
        i32.shl
        i32.const 4
        i32.sub
        local.tee $l4
        i32.store offset=4
      end
      local.get $p1
      i32.load
      local.tee $l5
      local.get $l5
      local.get $p1
      i32.load offset=4
      i32.const 3
      i32.mul
      i32.add
      i32.const 12
      i32.add
      local.tee $l10
      i32.ne
      if $I8
        local.get $l3
        i32.const 4
        i32.add
        local.set $l11
        loop $L9
          local.get $l5
          i32.load
          local.tee $l9
          i32.const -3
          i32.le_u
          if $I10
            i32.const 0
            local.set $l2
            local.get $l3
            local.get $l4
            local.get $l9
            i32.and
            local.tee $l6
            i32.const 3
            i32.mul
            local.tee $l8
            i32.add
            local.tee $l7
            i32.load
            i32.const -1
            i32.ne
            if $I11
              loop $L12
                local.get $l3
                local.get $l2
                i32.const 4
                i32.add
                local.tee $l2
                local.get $l6
                i32.add
                local.get $l4
                i32.and
                local.tee $l6
                i32.const 3
                i32.mul
                local.tee $l8
                i32.add
                local.tee $l7
                i32.load
                i32.const -1
                i32.ne
                br_if $L12
              end
            end
            local.get $l7
            local.get $l9
            i32.store
            local.get $l8
            local.get $l11
            i32.add
            local.get $l5
            i64.load offset=4 align=4
            i64.store align=4
          end
          local.get $l5
          i32.const 12
          i32.add
          local.tee $l5
          local.get $l10
          i32.ne
          br_if $L9
        end
        local.get $p0
        i32.load offset=4
        local.set $l4
      end
      local.get $p0
      local.get $p1
      i32.load offset=8
      local.tee $l2
      i32.store offset=8
      local.get $p0
      local.get $l4
      i32.const 1
      i32.shr_u
      i32.const 2147483646
      i32.and
      i32.const 2
      i32.add
      i32.const 3
      i32.div_u
      local.get $l2
      i32.sub
      i32.store offset=12
    end)
