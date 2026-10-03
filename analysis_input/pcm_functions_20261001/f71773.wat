  (func $f71773 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32)
    local.get $p0
    i32.load offset=8
    local.tee $l9
    if $I0
      loop $L1
        local.get $p0
        i32.load offset=4
        local.get $l6
        i32.const 12
        i32.mul
        i32.add
        local.tee $l2
        i32.load offset=4
        if $I2
          local.get $l2
          i32.const 4
          i32.add
          local.set $l11
          local.get $l2
          i32.load
          local.set $l12
          i32.const 0
          local.set $l7
          loop $L3
            local.get $p1
            local.get $l5
            i32.const 28
            i32.mul
            i32.add
            local.tee $l3
            local.get $l12
            local.get $l7
            i32.const 36
            i32.mul
            i32.add
            local.tee $l2
            f32.load
            f32.store
            local.get $l3
            local.get $l2
            f32.load offset=4
            f32.store offset=4
            local.get $l3
            local.get $l2
            f32.load offset=8
            f32.store offset=8
            local.get $l3
            local.get $l2
            f32.load offset=12
            f32.store offset=12
            local.get $l3
            local.get $l2
            f32.load offset=16
            f32.store offset=16
            local.get $l3
            local.get $l2
            f32.load offset=20
            f32.store offset=20
            local.get $l3
            block $B4 (result i32)
              local.get $l2
              i32.load offset=24
              local.tee $l8
              if $I5
                local.get $p0
                i32.load offset=4
                local.set $l13
                i32.const 0
                local.set $l2
                i32.const 0
                local.set $l3
                block $B6 (result i32)
                  loop $L7
                    local.get $l13
                    local.get $l2
                    i32.const 12
                    i32.mul
                    i32.add
                    local.tee $l4
                    i32.load offset=4
                    local.set $l10
                    block $B8
                      local.get $l8
                      local.get $l4
                      i32.load
                      local.tee $l4
                      i32.lt_u
                      br_if $B8
                      local.get $l8
                      local.get $l4
                      local.get $l10
                      i32.const 36
                      i32.mul
                      i32.add
                      i32.ge_u
                      br_if $B8
                      local.get $l8
                      local.get $l4
                      i32.sub
                      i32.const 36
                      i32.div_s
                      local.get $l3
                      i32.add
                      br $B6
                    end
                    local.get $l3
                    local.get $l10
                    i32.add
                    local.set $l3
                    local.get $l2
                    i32.const 1
                    i32.add
                    local.tee $l2
                    local.get $l9
                    i32.ne
                    br_if $L7
                  end
                  local.get $l3
                  i32.const 1
                  i32.sub
                end
                i32.const 1
                i32.shl
                br $B4
              end
              local.get $l2
              i32.load offset=32
              i32.const 1
              i32.shl
              i32.const 30
              i32.and
              local.get $l2
              i32.load offset=28
              i32.const 5
              i32.shl
              i32.or
              i32.const 1
              i32.or
            end
            i32.store offset=24
            local.get $l5
            i32.const 1
            i32.add
            local.set $l5
            local.get $l7
            i32.const 1
            i32.add
            local.tee $l7
            local.get $l11
            i32.load
            i32.lt_u
            br_if $L3
          end
        end
        local.get $l6
        i32.const 1
        i32.add
        local.tee $l6
        local.get $l9
        i32.ne
        br_if $L1
      end
    end)