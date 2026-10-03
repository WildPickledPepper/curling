  (func $f72436 (type $t118) (param $p0 i32) (param $p1 i32) (param $p2 f32) (param $p3 f32)
    (local $l4 i32) (local $l5 i32)
    block $B0
      block $B1
        block $B2
          block $B3
            local.get $p0
            i32.const 8
            i32.add
            local.tee $p0
            i32.load offset=4
            local.tee $l5
            i32.const 30
            i32.shr_u
            i32.const 2
            i32.sub
            br_table $B3 $B1 $B2
          end
          local.get $p0
          i32.load
          i32.load8_u offset=4785
          br_if $B1
        end
        local.get $p0
        i32.const 12
        i32.add
        local.get $p1
        local.get $p2
        local.get $p3
        call $f71359
        br $B0
      end
      local.get $l5
      i32.const 1048576
      i32.and
      i32.eqz
      if $I4
        local.get $p0
        i32.load offset=8
        local.tee $l4
        i32.eqz
        if $I5
          local.get $p0
          local.get $p0
          i32.load
          local.get $l5
          i32.const 24
          i32.shr_u
          i32.const 15
          i32.and
          call $f71984
          local.tee $l4
          i32.store offset=8
        end
        local.get $l4
        local.get $p0
        f32.load offset=72
        f32.store offset=156
        local.get $l4
        local.get $p0
        f32.load offset=76
        f32.store offset=160
        local.get $l4
        local.get $p0
        f32.load offset=80
        f32.store offset=164
        local.get $l4
        local.get $p0
        f32.load offset=84
        f32.store offset=168
        local.get $l4
        local.get $p0
        f32.load offset=88
        f32.store offset=172
        local.get $l4
        local.get $p0
        f32.load offset=92
        f32.store offset=176
        local.get $l4
        local.get $p0
        f32.load offset=96
        f32.store offset=180
        local.get $l4
        local.get $p0
        f32.load offset=100
        f32.store offset=184
        local.get $l4
        local.get $p0
        f32.load offset=104
        f32.store offset=188
        local.get $l4
        local.get $p0
        f32.load offset=108
        f32.store offset=192
        local.get $l4
        local.get $p0
        f32.load offset=112
        f32.store offset=196
        local.get $l4
        local.get $p0
        f32.load offset=116
        f32.store offset=200
      end
      local.get $p0
      i32.load offset=8
      local.tee $l4
      i32.eqz
      if $I6
        local.get $p0
        local.get $p0
        i32.load
        local.get $p0
        i32.load8_u offset=7
        i32.const 15
        i32.and
        call $f71984
        local.tee $l4
        i32.store offset=8
      end
      local.get $l4
      local.get $p1
      i32.const 3
      i32.shl
      local.tee $p1
      i32.add
      local.get $p2
      f32.store offset=156
      local.get $p0
      i32.load offset=8
      local.tee $l4
      i32.eqz
      if $I7
        local.get $p0
        local.get $p0
        i32.load
        local.get $p0
        i32.load8_u offset=7
        i32.const 15
        i32.and
        call $f71984
        local.tee $l4
        i32.store offset=8
      end
      local.get $p1
      local.get $l4
      i32.add
      local.get $p3
      f32.store offset=160
      local.get $p0
      i32.load
      local.get $p0
      call $f71985
      local.get $p0
      local.get $p0
      i32.load offset=4
      i32.const 1048576
      i32.or
      i32.store offset=4
    end)
