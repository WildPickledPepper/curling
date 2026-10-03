  (func $f78658 (type $t3) (param $p0 i32) (param $p1 i32) (param $p2 i32) (result i32)
    (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32)
    i32.const 4758240
    i32.load
    local.set $l6
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l3
    global.set $g0
    i32.const 4787792
    i32.load
    if $I0 (result i32)
      local.get $l3
      i64.const 4294967296
      i64.store offset=8
      local.get $l3
      i64.const 4294967296
      i64.store
      local.get $l6
      i32.load offset=220
      local.set $l5
      block $B1
        local.get $p0
        i32.eqz
        if $I2
          local.get $l5
          i32.eqz
          br_if $B1
          loop $L3
            block $B4
              block $B5
                local.get $l4
                i32.const 3
                i32.shl
                local.tee $p0
                local.get $l6
                i32.load offset=212
                i32.add
                local.tee $l8
                i32.load offset=4
                local.tee $l7
                i32.load
                local.get $p1
                i32.ne
                br_if $B5
                local.get $p2
                if $I6
                  local.get $l7
                  i32.load offset=4
                  local.get $p2
                  i32.ne
                  br_if $B5
                end
                local.get $l3
                i32.load offset=8
                local.tee $l5
                i32.const 1
                i32.add
                local.tee $l7
                local.get $l3
                i32.load offset=12
                i32.const 1
                i32.shr_u
                i32.gt_u
                if $I7
                  local.get $l3
                  call $f580
                end
                local.get $l3
                local.get $l7
                i32.store offset=8
                local.get $l3
                i32.load
                local.get $l5
                i32.const 3
                i32.shl
                i32.add
                local.get $l8
                i64.load align=4
                i64.store align=4
                local.get $l6
                local.get $l6
                i32.load offset=220
                i32.const 1
                i32.sub
                local.tee $l5
                i32.store offset=220
                local.get $l6
                i32.load offset=212
                local.tee $l7
                local.get $p0
                i32.add
                local.get $l7
                local.get $l5
                i32.const 3
                i32.shl
                i32.add
                i64.load align=4
                i64.store align=4
                local.get $l6
                i32.load offset=220
                local.set $l5
                br $B4
              end
              local.get $l4
              i32.const 1
              i32.add
              local.set $l4
            end
            local.get $l4
            local.get $l5
            i32.lt_u
            br_if $L3
          end
          br $B1
        end
        local.get $l5
        i32.eqz
        br_if $B1
        local.get $l6
        i32.load offset=212
        local.set $l8
        loop $L8
          block $B9
            local.get $l8
            local.get $l4
            i32.const 3
            i32.shl
            i32.add
            local.tee $l7
            i32.load
            local.get $p0
            i32.ne
            br_if $B9
            local.get $l7
            i32.load offset=4
            local.tee $l9
            i32.load
            local.get $p1
            i32.ne
            br_if $B9
            local.get $p2
            if $I10
              local.get $l9
              i32.load offset=4
              local.get $p2
              i32.ne
              br_if $B9
            end
            local.get $l3
            call $f580
            local.get $l3
            i32.const 1
            i32.store offset=8
            local.get $l3
            i32.load
            local.get $l7
            i64.load align=4
            i64.store align=4
            local.get $l6
            local.get $l6
            i32.load offset=220
            i32.const 1
            i32.sub
            local.tee $l5
            i32.store offset=220
            local.get $l6
            i32.load offset=212
            local.tee $l7
            local.get $l4
            i32.const 3
            i32.shl
            i32.add
            local.get $l7
            local.get $l5
            i32.const 3
            i32.shl
            i32.add
            i64.load align=4
            i64.store align=4
            br $B1
          end
          local.get $l4
          i32.const 1
          i32.add
          local.tee $l4
          local.get $l5
          i32.ne
          br_if $L8
        end
      end
      local.get $l3
      i32.load offset=8
      local.tee $p2
      if $I11
        i32.const 0
        local.set $l4
        loop $L12
          local.get $l3
          i32.load
          local.get $l4
          i32.const 3
          i32.shl
          i32.add
          local.tee $l5
          i32.load offset=4
          local.get $l5
          i32.load
          call $f80337
          local.get $l4
          i32.const 1
          i32.add
          local.tee $l4
          local.get $l3
          i32.load offset=8
          i32.lt_u
          br_if $L12
        end
        local.get $l3
        i32.load offset=8
        if $I13
          i32.const 0
          local.set $l4
          loop $L14
            local.get $l3
            i32.load
            local.get $l4
            i32.const 3
            i32.shl
            i32.add
            i32.const 4
            i32.add
            local.set $l7
            local.get $l6
            local.get $l6
            i32.load offset=264
            i32.const 4
            i32.shl
            i32.add
            local.tee $l5
            i32.const 232
            i32.add
            local.set $l9
            local.get $l5
            i32.const 240
            i32.add
            local.tee $p1
            i32.load
            local.tee $p0
            i32.const 1
            i32.add
            local.tee $l8
            local.get $l5
            i32.load offset=244
            i32.const 1
            i32.shr_u
            i32.gt_u
            if $I15
              local.get $l9
              call $f552
            end
            local.get $p1
            local.get $l8
            i32.store
            local.get $l9
            i32.load
            local.get $p0
            i32.const 2
            i32.shl
            i32.add
            local.get $l7
            i32.load
            i32.store
            local.get $l4
            i32.const 1
            i32.add
            local.tee $l4
            local.get $l3
            i32.load offset=8
            i32.lt_u
            br_if $L14
          end
        end
      end
      local.get $l3
      call $f554
      drop
      local.get $p2
      i32.const 0
      i32.ne
    else
      i32.const 0
    end
    local.set $l4
    local.get $l3
    i32.const 16
    i32.add
    global.set $g0
    local.get $l4
    i32.const 1
    i32.sub)
