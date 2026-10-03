  (func $f71428 (type $t11) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32)
    (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32)
    local.get $p2
    if $I0
      loop $L1
        local.get $p1
        local.get $l9
        i32.const 2
        i32.shl
        i32.add
        i32.load
        local.get $p3
        i32.add
        local.set $l10
        block $B2
          local.get $p0
          i32.load offset=2384
          local.tee $l7
          i32.load offset=12
          local.get $l7
          i32.load offset=8
          i32.const 12
          i32.mul
          i32.add
          local.tee $l8
          i32.load offset=4
          local.tee $l6
          if $I3
            local.get $l8
            local.get $l6
            i32.load
            i32.store offset=4
            br $B2
          end
          block $B4
            local.get $l8
            i32.load offset=8
            local.tee $l6
            local.get $l7
            i32.load
            i32.eq
            br_if $B4
            local.get $l7
            i32.load offset=4
            local.set $l11
            local.get $l8
            local.get $l6
            i32.const 1
            i32.add
            i32.store offset=8
            local.get $l8
            i32.load
            local.tee $l8
            i32.eqz
            br_if $B4
            local.get $l8
            local.get $l6
            local.get $l11
            i32.mul
            i32.add
            local.set $l6
            br $B2
          end
          local.get $l7
          call $f71372
          local.set $l6
        end
        local.get $l6
        local.get $p4
        call $f71588
        local.get $l6
        i32.const -1
        i32.store offset=48
        local.get $l6
        local.get $l10
        i32.store offset=40
        local.get $l6
        i64.const 2199023255040
        i64.store offset=24
        block $B5
          local.get $l6
          i32.load offset=4
          i32.load offset=40
          i32.load offset=2368
          local.tee $l7
          i32.load offset=12
          local.tee $l8
          if $I6
            local.get $l7
            i32.load offset=8
            local.get $l8
            i32.const 1
            i32.sub
            local.tee $l11
            i32.const 2
            i32.shl
            i32.add
            i32.load
            local.set $l8
            local.get $l7
            local.get $l11
            i32.store offset=12
            br $B5
          end
          local.get $l7
          local.get $l7
          i32.load offset=4
          local.tee $l8
          i32.const 1
          i32.add
          i32.store offset=4
        end
        local.get $l6
        local.get $l8
        i32.store offset=44
        local.get $l6
        call $f71329
        local.get $p0
        local.get $l10
        i32.load offset=68
        i32.const 2
        i32.shl
        i32.add
        i32.const 2676
        i32.add
        local.tee $l7
        local.get $l7
        i32.load
        i32.const 1
        i32.add
        i32.store
        local.get $p0
        i32.load offset=1012
        local.tee $l7
        local.get $l6
        i32.const 16
        i32.add
        local.get $l6
        i32.load offset=44
        local.get $l7
        i32.load
        i32.load offset=16
        call_indirect $__indirect_function_table (type $t2)
        local.get $p5
        if $I7
          local.get $p5
          local.get $l9
          i32.const 24
          i32.mul
          i32.add
          local.tee $l7
          local.get $p0
          i32.load offset=1140
          i32.load offset=4
          local.get $l6
          i32.load offset=8
          i32.const 2147483647
          i32.and
          i32.const 24
          i32.mul
          i32.add
          local.tee $l6
          f32.load
          f32.store
          local.get $l7
          local.get $l6
          f32.load offset=4
          f32.store offset=4
          local.get $l7
          local.get $l6
          f32.load offset=8
          f32.store offset=8
          local.get $l7
          local.get $l6
          f32.load offset=12
          f32.store offset=12
          local.get $l7
          local.get $l6
          f32.load offset=16
          f32.store offset=16
          local.get $l7
          local.get $l6
          f32.load offset=20
          f32.store offset=20
        end
        local.get $p0
        i32.load offset=976
        i32.load offset=1024
        local.tee $l6
        local.get $l10
        i32.const 32
        i32.add
        local.get $l6
        i32.load
        i32.load offset=44
        call_indirect $__indirect_function_table (type $t1)
        local.get $l9
        i32.const 1
        i32.add
        local.tee $l9
        local.get $p2
        i32.ne
        br_if $L1
      end
    end)