  (func $f72015 (type $t4) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32)
    (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32)
    global.get $g0
    i32.const 288
    i32.sub
    local.tee $l5
    global.set $g0
    block $B0
      local.get $p1
      i32.load offset=8
      local.get $p1
      i32.load offset=4
      local.tee $l4
      i32.const 22
      i32.shr_u
      i32.const 60
      i32.and
      i32.const 3181092
      i32.add
      i32.load
      local.get $p1
      i32.add
      i32.const 8
      i32.add
      local.get $l4
      i32.const 1
      i32.and
      select
      i32.load8_u
      i32.const 8
      i32.and
      i32.eqz
      if $I1
        local.get $l5
        i32.const 1
        i32.store8 offset=272
        local.get $l5
        i64.const 274877906944
        i64.store offset=280
        local.get $l5
        local.get $l5
        i32.const 16
        i32.add
        i32.store offset=276
        local.get $p1
        i32.const 16
        i32.add
        local.tee $l7
        call $f71725
        drop
        i32.const 0
        local.set $l4
        local.get $p1
        local.get $l5
        i32.const 12
        i32.add
        i32.const 0
        call $f72634
        local.set $l6
        local.get $p0
        local.get $l7
        local.get $l5
        i32.load offset=12
        local.get $l6
        i32.const 48
        local.get $p2
        local.get $p3
        i32.const 0
        i32.ne
        call $f71433
        local.get $l6
        if $I2
          local.get $p1
          i32.load
          local.set $p3
          loop $L3
            local.get $l5
            i32.load offset=12
            local.get $l4
            i32.const 2
            i32.shl
            i32.add
            i32.load
            i32.const 32
            i32.add
            local.tee $p0
            i32.load offset=4
            local.tee $p1
            i32.const 251658240
            i32.and
            i32.const 16777216
            i32.eq
            if $I4
              local.get $p0
              local.get $p3
              i32.store
              local.get $p0
              local.get $p1
              i32.const 1073741823
              i32.and
              i32.const -2147483648
              i32.or
              i32.store offset=4
            end
            local.get $p0
            call $f71979
            local.get $l4
            i32.const 1
            i32.add
            local.tee $l4
            local.get $l6
            i32.ne
            br_if $L3
          end
        end
        local.get $l5
        i32.load offset=284
        local.tee $l4
        i32.const 0
        i32.lt_s
        br_if $B0
        local.get $l4
        i32.const 2147483647
        i32.and
        i32.eqz
        br_if $B0
        local.get $l5
        i32.load offset=276
        local.tee $l4
        local.get $l5
        i32.const 16
        i32.add
        i32.eq
        br_if $B0
        local.get $l4
        i32.eqz
        br_if $B0
        call $f69753
        local.tee $p0
        local.get $l4
        local.get $p0
        i32.load
        i32.load offset=12
        call_indirect $__indirect_function_table (type $t1)
        br $B0
      end
      local.get $l5
      i32.const 1
      i32.store8 offset=272
      local.get $l5
      i64.const 274877906944
      i64.store offset=280
      local.get $l5
      local.get $l5
      i32.const 16
      i32.add
      i32.store offset=276
      local.get $p1
      i32.const 16
      i32.add
      call $f71725
      drop
      i32.const 0
      local.set $l4
      block $B5
        local.get $p1
        local.get $l5
        i32.const 12
        i32.add
        i32.const 0
        call $f72634
        local.tee $l6
        i32.eqz
        br_if $B5
        local.get $p1
        i32.load
        local.set $l8
        local.get $l6
        i32.const 1
        i32.and
        local.set $l7
        local.get $l6
        i32.const 1
        i32.ne
        if $I6
          local.get $l6
          i32.const -2
          i32.and
          local.set $p1
          loop $L7
            local.get $l4
            i32.const 2
            i32.shl
            local.tee $l6
            local.get $l5
            i32.load offset=12
            i32.add
            i32.load
            i32.const 32
            i32.add
            local.tee $p2
            i32.load offset=4
            local.tee $p3
            i32.const 251658240
            i32.and
            i32.const 16777216
            i32.eq
            if $I8
              local.get $p2
              local.get $l8
              i32.store
              local.get $p2
              local.get $p3
              i32.const 1073741823
              i32.and
              i32.const -2147483648
              i32.or
              i32.store offset=4
            end
            local.get $l5
            i32.load offset=12
            local.get $l6
            i32.const 4
            i32.or
            i32.add
            i32.load
            i32.const 32
            i32.add
            local.tee $l6
            i32.load offset=4
            local.tee $p2
            i32.const 251658240
            i32.and
            i32.const 16777216
            i32.eq
            if $I9
              local.get $l6
              local.get $l8
              i32.store
              local.get $l6
              local.get $p2
              i32.const 1073741823
              i32.and
              i32.const -2147483648
              i32.or
              i32.store offset=4
            end
            local.get $l4
            i32.const 2
            i32.add
            local.set $l4
            local.get $p1
            i32.const 2
            i32.sub
            local.tee $p1
            br_if $L7
          end
        end
        local.get $l7
        i32.eqz
        br_if $B5
        local.get $l5
        i32.load offset=12
        local.get $l4
        i32.const 2
        i32.shl
        i32.add
        i32.load
        i32.const 32
        i32.add
        local.tee $l4
        i32.load offset=4
        local.tee $p0
        i32.const 251658240
        i32.and
        i32.const 16777216
        i32.ne
        br_if $B5
        local.get $l4
        local.get $l8
        i32.store
        local.get $l4
        local.get $p0
        i32.const 1073741823
        i32.and
        i32.const -2147483648
        i32.or
        i32.store offset=4
      end
      local.get $l5
      i32.load offset=284
      local.tee $l4
      i32.const 0
      i32.lt_s
      br_if $B0
      local.get $l4
      i32.const 2147483647
      i32.and
      i32.eqz
      br_if $B0
      local.get $l5
      i32.load offset=276
      local.tee $l4
      local.get $l5
      i32.const 16
      i32.add
      i32.eq
      br_if $B0
      local.get $l4
      i32.eqz
      br_if $B0
      call $f69753
      local.tee $p0
      local.get $l4
      local.get $p0
      i32.load
      i32.load offset=12
      call_indirect $__indirect_function_table (type $t1)
    end
    local.get $l5
    i32.const 288
    i32.add
    global.set $g0)