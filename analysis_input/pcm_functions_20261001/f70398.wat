  (func $f70398 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i64)
    block $B0
      block $B1
        block $B2
          block $B3
            block $B4
              block $B5
                block $B6
                  block $B7
                    local.get $p1
                    i32.load
                    br_table $B5 $B4 $B6 $B7 $B3 $B2 $B1 $B0
                  end
                  local.get $p0
                  i32.const 3
                  i32.store
                  local.get $p0
                  local.get $p1
                  f32.load offset=4
                  f32.store offset=4
                  local.get $p0
                  local.get $p1
                  f32.load offset=8
                  f32.store offset=8
                  local.get $p0
                  local.get $p1
                  f32.load offset=12
                  f32.store offset=12
                  return
                end
                local.get $p0
                local.get $p1
                i64.load align=4
                i64.store align=4
                local.get $p0
                local.get $p1
                i32.load offset=8
                i32.store offset=8
                return
              end
              local.get $p1
              i64.load align=4
              local.set $l3
              local.get $p0
              i32.const 0
              i32.store offset=8
              local.get $p0
              local.get $l3
              i64.store align=4
              return
            end
            local.get $p0
            i32.const 1
            i32.store
            return
          end
          local.get $p0
          i32.const 4
          i32.store
          local.get $p0
          local.get $p1
          f32.load offset=4
          f32.store offset=4
          local.get $p0
          local.get $p1
          f32.load offset=8
          f32.store offset=8
          local.get $p0
          local.get $p1
          f32.load offset=12
          f32.store offset=12
          local.get $p0
          local.get $p1
          f32.load offset=16
          f32.store offset=16
          local.get $p0
          local.get $p1
          f32.load offset=20
          f32.store offset=20
          local.get $p0
          local.get $p1
          f32.load offset=24
          f32.store offset=24
          local.get $p0
          local.get $p1
          f32.load offset=28
          f32.store offset=28
          local.get $p0
          local.get $p1
          i32.load offset=32
          local.tee $l2
          i32.store offset=32
          local.get $p0
          local.get $p1
          i32.load8_u offset=36
          i32.store8 offset=36
          local.get $p0
          local.get $p1
          i32.load16_u offset=37 align=1
          i32.store16 offset=37 align=1
          local.get $p0
          local.get $p1
          i32.load8_u offset=39
          i32.store8 offset=39
          local.get $p0
          local.get $l2
          i32.const 16
          i32.add
          i32.store offset=40
          local.get $p0
          local.get $l2
          local.get $l2
          i32.load
          i32.load offset=60
          call_indirect $__indirect_function_table (type $t5)
          i32.store8 offset=44
          return
        end
        local.get $p0
        i32.const 5
        i32.store
        local.get $p0
        local.get $p1
        f32.load offset=4
        f32.store offset=4
        local.get $p0
        local.get $p1
        f32.load offset=8
        f32.store offset=8
        local.get $p0
        local.get $p1
        f32.load offset=12
        f32.store offset=12
        local.get $p0
        local.get $p1
        f32.load offset=16
        f32.store offset=16
        local.get $p0
        local.get $p1
        f32.load offset=20
        f32.store offset=20
        local.get $p0
        local.get $p1
        f32.load offset=24
        f32.store offset=24
        local.get $p0
        local.get $p1
        f32.load offset=28
        f32.store offset=28
        local.get $p0
        local.get $p1
        i32.load8_u offset=32
        i32.store8 offset=32
        local.get $p0
        local.get $p1
        i32.load offset=33 align=1
        i32.store offset=33 align=1
        local.get $p0
        i32.const 36
        i32.add
        local.tee $l2
        local.get $p1
        i32.load offset=36 align=1
        i32.store align=1
        local.get $p0
        local.get $l2
        i32.load
        local.tee $p1
        i32.store offset=40
        local.get $p0
        local.get $p1
        i32.load offset=68
        i32.store offset=44
        local.get $p0
        i64.const -3617234925708640256
        i64.store offset=48 align=4
        return
      end
      local.get $p0
      i32.const 6
      i32.store
      local.get $p0
      local.get $p1
      i64.load offset=4 align=4
      local.tee $l3
      i64.store offset=4 align=4
      local.get $p0
      local.get $p1
      i64.load offset=12 align=4
      i64.store offset=12 align=4
      local.get $p0
      local.get $p1
      i32.load8_u offset=20
      i32.store8 offset=20
      local.get $p0
      local.get $p1
      i32.load8_u offset=23
      i32.store8 offset=23
      local.get $p0
      local.get $p1
      i32.load16_u offset=21 align=1
      i32.store16 offset=21 align=1
      local.get $p0
      i64.const -3617234925708640256
      i64.store offset=28 align=4
      local.get $p0
      local.get $l3
      i32.wrap_i64
      i32.const 16
      i32.add
      i32.store offset=24
    end)
