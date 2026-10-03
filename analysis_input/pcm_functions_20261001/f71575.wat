  (func $f71575 (type $t77) (param $p0 i32) (param $p1 i32) (param $p2 f32) (param $p3 i32) (param $p4 i32)
    (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i64)
    local.get $p0
    local.get $p1
    i32.store offset=164
    block $B0
      local.get $p1
      if $I1
        local.get $p0
        local.get $p4
        i32.const 1
        i32.shl
        i32.const 1
        i32.or
        i64.extend_i32_u
        local.get $p1
        i64.load offset=48
        i64.const 2199023255040
        i64.and
        i64.or
        i64.store offset=144
        local.get $p0
        i32.load offset=44
        local.get $p2
        f32.store offset=156
        local.get $p0
        i32.load offset=44
        i32.load8_u offset=44
        i32.const 32
        i32.and
        if $I2
          block $B3
            local.get $p0
            i64.load offset=144
            local.tee $l9
            i64.const 9
            i64.shr_u
            i32.wrap_i64
            local.tee $l7
            i32.const 32
            i32.add
            i32.const 5
            i32.shr_u
            local.tee $l6
            local.get $p0
            i32.load offset=40
            local.tee $p1
            i32.const 4732
            i32.add
            i32.load
            i32.const 2147483647
            i32.and
            i32.le_u
            if $I4
              local.get $p1
              i32.load offset=4728
              local.set $p4
              br $B3
            end
            call $f69753
            local.tee $p4
            local.get $l6
            i32.const 2
            i32.shl
            i32.const 3171167
            i32.const 3171183
            i32.const 438
            local.get $p4
            i32.load
            i32.load offset=8
            call_indirect $__indirect_function_table (type $t9)
            local.set $p4
            block $B5
              local.get $p1
              i32.load offset=4728
              local.tee $l5
              i32.eqz
              br_if $B5
              local.get $p4
              local.get $l5
              local.get $p1
              i32.load offset=4732
              i32.const 2
              i32.shl
              call $f483
              drop
              local.get $p1
              i32.load offset=4732
              i32.const 0
              i32.lt_s
              br_if $B5
              local.get $p1
              i32.load offset=4728
              local.tee $l5
              i32.eqz
              br_if $B5
              call $f69753
              local.tee $l8
              local.get $l5
              local.get $l8
              i32.load
              i32.load offset=12
              call_indirect $__indirect_function_table (type $t1)
            end
            local.get $p4
            local.get $p1
            i32.load offset=4732
            local.tee $l5
            i32.const 2
            i32.shl
            i32.add
            i32.const 0
            local.get $l6
            local.get $l5
            i32.sub
            i32.const 2
            i32.shl
            call $f484
            drop
            local.get $p1
            local.get $l6
            i32.store offset=4732
            local.get $p1
            local.get $p4
            i32.store offset=4728
          end
          local.get $p4
          local.get $l9
          i64.const 14
          i64.shr_u
          i32.wrap_i64
          i32.const 134217727
          i32.and
          i32.const 2
          i32.shl
          i32.add
          local.tee $p1
          local.get $p1
          i32.load
          i32.const 1
          local.get $l7
          i32.shl
          i32.or
          i32.store
        end
        local.get $p3
        i32.eqz
        if $I6
          local.get $p0
          i32.load offset=156
          i32.const -2
          i32.ge_u
          if $I7
            local.get $p0
            i32.load offset=40
            local.get $p0
            call $f71379
            local.get $p0
            call $f71555
          end
          local.get $p0
          i32.load offset=40
          i32.load offset=1000
          local.get $p0
          i64.load offset=144
          call $f70712
          return
        end
        local.get $p0
        i32.load offset=164
        i32.eqz
        if $I8
          local.get $p0
          i32.load offset=40
          i32.load offset=1000
          local.get $p0
          i64.load offset=144
          call $f70713
        end
        local.get $p0
        i32.load offset=40
        i32.load offset=1000
        local.get $p0
        i64.load offset=144
        call $f70714
        local.get $p0
        i32.load offset=156
        i32.const -3
        i32.gt_u
        br_if $B0
        local.get $p0
        i32.load offset=40
        local.get $p0
        call $f71381
        local.get $p0
        call $f71556
        return
      end
      local.get $p0
      i64.const 2199023255043
      i64.store offset=144
    end)