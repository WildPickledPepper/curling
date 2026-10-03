  (func $f73020 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 f32) (local $l3 f32) (local $l4 f32) (local $l5 f32) (local $l6 f32) (local $l7 f32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 i32) (local $l17 i32) (local $l18 i32)
    global.get $g0
    i32.const 160
    i32.sub
    local.tee $l13
    global.set $g0
    i32.const 9
    call $f80140
    call $f73714
    local.get $p0
    local.get $l13
    i32.const 128
    i32.add
    local.get $l13
    i32.const 112
    i32.add
    local.get $l13
    i32.const 96
    i32.add
    local.get $p0
    i32.load
    i32.load offset=132
    call_indirect $__indirect_function_table (type $t4)
    local.get $l13
    i32.const 80
    i32.add
    local.set $l17
    local.get $p0
    i32.load8_u offset=36
    local.set $l18
    global.get $g0
    i32.const 32
    i32.sub
    local.tee $l15
    global.set $g0
    i32.const 9
    call $f80140
    call $f73714
    local.get $p0
    local.tee $l14
    call $f73021
    local.set $l16
    block $B0
      local.get $l18
      i32.eqz
      br_if $B0
      local.get $l15
      i32.const 16
      i32.add
      local.get $l14
      i32.load offset=28
      i32.const 4131408
      call $f80185
      local.get $l14
      i32.const 40
      i32.add
      call $f78098
      local.get $l16
      if $I1
        local.get $l15
        local.get $l16
        local.get $l15
        i32.const 16
        i32.add
        call $f78160
        local.get $l14
        local.get $l15
        i32.load offset=8
        i32.store offset=60
        local.get $l14
        local.get $l15
        i64.load
        i64.store offset=52 align=4
        br $B0
      end
      local.get $l14
      local.get $l15
      i64.load offset=16
      i64.store offset=52 align=4
      local.get $l14
      local.get $l15
      i32.load offset=24
      i32.store offset=60
    end
    local.get $l14
    i32.const 52
    i32.add
    local.set $l14
    block $B2
      local.get $l16
      if $I3
        local.get $l17
        local.get $l16
        local.get $l14
        call $f78098
        br $B2
      end
      local.get $l17
      local.get $l14
      i64.load align=4
      i64.store align=4
      local.get $l17
      local.get $l14
      i32.load offset=8
      i32.store offset=8
    end
    local.get $l15
    i32.const 32
    i32.add
    global.set $g0
    local.get $p0
    i32.load offset=28
    i32.const 4131408
    call $f80185
    local.set $l16
    local.get $p0
    call $f73021
    local.set $l14
    local.get $l13
    i32.const 48
    i32.add
    local.get $p0
    i32.load offset=32
    local.tee $l17
    i32.const 0
    local.get $l17
    i32.load
    i32.load offset=36
    call_indirect $__indirect_function_table (type $t2)
    local.get $p1
    i32.const 2
    i32.and
    local.tee $l17
    if $I4
      local.get $l13
      i32.const 16
      i32.add
      local.get $l16
      call $f78093
      local.get $l13
      i32.const 152
      i32.add
      local.tee $l15
      local.get $l13
      f32.load offset=136
      local.get $l13
      f32.load offset=24
      f32.sub
      f32.store
      local.get $l13
      local.get $l13
      f32.load offset=132
      local.get $l13
      f32.load offset=20
      f32.sub
      f32.store offset=148
      local.get $l13
      local.get $l13
      f32.load offset=128
      local.get $l13
      f32.load offset=16
      f32.sub
      f32.store offset=144
      local.get $l13
      i32.const 16
      i32.add
      local.get $l16
      local.get $l13
      i32.const 144
      i32.add
      call $f78158
      local.get $l15
      local.get $l13
      i32.load offset=24
      i32.store
      local.get $l13
      local.get $l15
      f32.load
      f32.store offset=72
      local.get $l13
      local.get $l13
      i64.load offset=16
      i64.store offset=64
    end
    local.get $p1
    i32.const 1
    i32.and
    local.tee $l15
    if $I5
      local.get $l13
      i32.const 16
      i32.add
      local.get $l16
      local.get $l13
      i32.const 96
      i32.add
      call $f78158
      local.get $l13
      f32.load offset=20
      local.set $l2
      local.get $l13
      f32.load offset=16
      local.set $l3
      local.get $l13
      f32.load offset=24
      local.set $l5
      local.get $l13
      i32.const 16
      i32.add
      local.get $l16
      local.get $l13
      i32.const 112
      i32.add
      call $f78158
      local.get $l3
      local.get $l13
      f32.load offset=24
      local.tee $l8
      f32.mul
      local.get $l5
      local.get $l13
      f32.load offset=16
      local.tee $l4
      f32.mul
      f32.sub
      local.set $l10
      local.get $l5
      local.get $l13
      f32.load offset=20
      local.tee $l9
      f32.mul
      local.get $l2
      local.get $l8
      f32.mul
      f32.sub
      local.set $l11
      block $B6 (result f32)
        local.get $l4
        local.get $l2
        f32.mul
        local.get $l3
        local.get $l9
        f32.mul
        f32.sub
        local.tee $l6
        f32.const 0x0p+0 (;=0;)
        f32.lt
        if $I7
          local.get $l2
          local.get $l4
          f32.lt
          if $I8
            local.get $l5
            local.get $l10
            f32.sub
            f32.const 0x1p-1 (;=0.5;)
            local.get $l4
            f32.const 0x1p+0 (;=1;)
            f32.add
            local.get $l2
            f32.sub
            local.get $l6
            f32.sub
            local.tee $l5
            f32.sqrt
            f32.div
            local.tee $l2
            f32.mul
            local.set $l4
            local.get $l8
            local.get $l11
            f32.add
            local.get $l2
            f32.mul
            local.set $l6
            local.get $l3
            local.get $l9
            f32.add
            local.get $l2
            f32.mul
            local.set $l7
            local.get $l5
            local.get $l2
            f32.mul
            br $B6
          end
          local.get $l11
          local.get $l8
          f32.sub
          f32.const 0x1p-1 (;=0.5;)
          local.get $l2
          f32.const 0x1p+0 (;=1;)
          local.get $l4
          f32.sub
          f32.add
          local.get $l6
          f32.sub
          local.tee $l7
          f32.sqrt
          f32.div
          local.tee $l2
          f32.mul
          local.set $l4
          local.get $l5
          local.get $l10
          f32.add
          local.get $l2
          f32.mul
          local.set $l6
          local.get $l7
          local.get $l2
          f32.mul
          local.set $l7
          local.get $l3
          local.get $l9
          f32.add
          local.get $l2
          f32.mul
          br $B6
        end
        local.get $l2
        f32.neg
        local.get $l4
        f32.gt
        if $I9
          local.get $l9
          local.get $l3
          f32.sub
          f32.const 0x1p-1 (;=0.5;)
          f32.const 0x1p+0 (;=1;)
          local.get $l4
          f32.sub
          local.get $l2
          f32.sub
          local.get $l6
          f32.add
          local.tee $l3
          f32.sqrt
          f32.div
          local.tee $l2
          f32.mul
          local.set $l4
          local.get $l3
          local.get $l2
          f32.mul
          local.set $l6
          local.get $l5
          local.get $l10
          f32.add
          local.get $l2
          f32.mul
          local.set $l7
          local.get $l8
          local.get $l11
          f32.add
          local.get $l2
          f32.mul
          br $B6
        end
        local.get $l2
        local.get $l4
        f32.const 0x1p+0 (;=1;)
        f32.add
        f32.add
        local.get $l6
        f32.add
        local.tee $l2
        f32.const 0x1p-1 (;=0.5;)
        local.get $l2
        f32.sqrt
        f32.div
        local.tee $l2
        f32.mul
        local.set $l4
        local.get $l9
        local.get $l3
        f32.sub
        local.get $l2
        f32.mul
        local.set $l6
        local.get $l11
        local.get $l8
        f32.sub
        local.get $l2
        f32.mul
        local.set $l7
        local.get $l5
        local.get $l10
        f32.sub
        local.get $l2
        f32.mul
      end
      local.set $l3
      local.get $l13
      local.get $l4
      f32.const 0x1p+0 (;=1;)
      local.get $l4
      local.get $l4
      f32.mul
      local.get $l6
      local.get $l6
      f32.mul
      local.get $l3
      local.get $l3
      f32.mul
      local.get $l7
      local.get $l7
      f32.mul
      f32.add
      f32.add
      f32.add
      f32.sqrt
      f32.div
      local.tee $l2
      f32.mul
      f32.store offset=60
      local.get $l13
      local.get $l6
      local.get $l2
      f32.mul
      f32.store offset=56
      local.get $l13
      local.get $l7
      local.get $l2
      f32.mul
      f32.store offset=52
      local.get $l13
      local.get $l3
      local.get $l2
      f32.mul
      f32.store offset=48
    end
    local.get $p0
    i32.load offset=32
    local.tee $p1
    i32.const 0
    local.get $l13
    i32.const 48
    i32.add
    local.get $p1
    i32.load
    i32.load offset=32
    call_indirect $__indirect_function_table (type $t2)
    local.get $l13
    i32.const 16
    i32.add
    local.get $p0
    i32.load offset=32
    local.tee $p1
    i32.const 1
    local.get $p1
    i32.load
    i32.load offset=36
    call_indirect $__indirect_function_table (type $t2)
    block $B10
      block $B11 (result f32)
        local.get $l14
        if $I12
          local.get $l17
          if $I13
            local.get $l13
            i32.const 144
            i32.add
            local.get $l14
            call $f78093
            local.get $l13
            i32.const 8
            i32.add
            local.tee $p1
            local.get $l13
            f32.load offset=88
            local.get $l13
            f32.load offset=152
            f32.sub
            f32.store
            local.get $l13
            local.get $l13
            f32.load offset=84
            local.get $l13
            f32.load offset=148
            f32.sub
            f32.store offset=4
            local.get $l13
            local.get $l13
            f32.load offset=80
            local.get $l13
            f32.load offset=144
            f32.sub
            f32.store
            local.get $l13
            i32.const 144
            i32.add
            local.get $l14
            local.get $l13
            call $f78158
            local.get $p1
            local.get $l13
            i32.load offset=152
            i32.store
            local.get $l13
            local.get $p1
            f32.load
            f32.store offset=40
            local.get $l13
            local.get $l13
            i64.load offset=144
            i64.store offset=32
          end
          local.get $l15
          i32.eqz
          br_if $B10
          local.get $l13
          i32.const 144
          i32.add
          local.get $l14
          local.get $l13
          i32.const 112
          i32.add
          call $f78158
          local.get $l13
          f32.load offset=148
          local.set $l3
          local.get $l13
          f32.load offset=152
          local.set $l5
          local.get $l13
          f32.load offset=144
          local.set $l2
          local.get $l13
          i32.const 144
          i32.add
          local.get $l14
          local.get $l13
          i32.const 96
          i32.add
          call $f78158
          local.get $l5
          local.get $l13
          f32.load offset=144
          local.tee $l8
          f32.mul
          local.get $l2
          local.get $l13
          f32.load offset=152
          local.tee $l9
          f32.mul
          f32.sub
          local.set $l10
          local.get $l3
          local.get $l9
          f32.mul
          local.get $l5
          local.get $l13
          f32.load offset=148
          local.tee $l4
          f32.mul
          f32.sub
          local.set $l11
          local.get $l13
          block $B14 (result f32)
            local.get $l2
            local.get $l4
            f32.mul
            local.get $l8
            local.get $l3
            f32.mul
            f32.sub
            local.tee $l6
            f32.const 0x0p+0 (;=0;)
            f32.lt
            if $I15
              local.get $l2
              local.get $l4
              f32.gt
              if $I16
                f32.const 0x1p-1 (;=0.5;)
                local.get $l2
                f32.const 0x1p+0 (;=1;)
                f32.add
                local.get $l4
                f32.sub
                local.get $l6
                f32.sub
                local.tee $l12
                f32.sqrt
                f32.div
                local.tee $l2
                local.get $l9
                local.get $l10
                f32.sub
                f32.mul
                local.set $l4
                local.get $l5
                local.get $l11
                f32.add
                local.get $l2
                f32.mul
                local.set $l6
                local.get $l3
                local.get $l8
                f32.add
                local.get $l2
                f32.mul
                local.set $l7
                local.get $l12
                local.get $l2
                f32.mul
                br $B14
              end
              local.get $l11
              local.get $l5
              f32.sub
              f32.const 0x1p-1 (;=0.5;)
              f32.const 0x1p+0 (;=1;)
              local.get $l2
              f32.sub
              local.get $l4
              f32.add
              local.get $l6
              f32.sub
              local.tee $l5
              f32.sqrt
              f32.div
              local.tee $l2
              f32.mul
              local.set $l4
              local.get $l2
              local.get $l9
              local.get $l10
              f32.add
              f32.mul
              local.set $l6
              local.get $l5
              local.get $l2
              f32.mul
              local.set $l7
              local.get $l3
              local.get $l8
              f32.add
              local.get $l2
              f32.mul
              br $B14
            end
            local.get $l4
            f32.neg
            local.get $l2
            f32.gt
            if $I17
              local.get $l3
              local.get $l8
              f32.sub
              f32.const 0x1p-1 (;=0.5;)
              local.get $l6
              f32.const 0x1p+0 (;=1;)
              local.get $l2
              f32.sub
              local.get $l4
              f32.sub
              f32.add
              local.tee $l3
              f32.sqrt
              f32.div
              local.tee $l2
              f32.mul
              local.set $l4
              local.get $l3
              local.get $l2
              f32.mul
              local.set $l6
              local.get $l2
              local.get $l9
              local.get $l10
              f32.add
              f32.mul
              local.set $l7
              local.get $l5
              local.get $l11
              f32.add
              local.get $l2
              f32.mul
              br $B14
            end
            local.get $l6
            local.get $l2
            f32.const 0x1p+0 (;=1;)
            f32.add
            local.get $l4
            f32.add
            f32.add
            local.tee $l2
            f32.const 0x1p-1 (;=0.5;)
            local.get $l2
            f32.sqrt
            f32.div
            local.tee $l2
            f32.mul
            local.set $l4
            local.get $l3
            local.get $l8
            f32.sub
            local.get $l2
            f32.mul
            local.set $l6
            local.get $l11
            local.get $l5
            f32.sub
            local.get $l2
            f32.mul
            local.set $l7
            local.get $l2
            local.get $l9
            local.get $l10
            f32.sub
            f32.mul
          end
          local.tee $l3
          f32.const 0x1p+0 (;=1;)
          local.get $l4
          local.get $l4
          f32.mul
          local.get $l6
          local.get $l6
          f32.mul
          local.get $l3
          local.get $l3
          f32.mul
          local.get $l7
          local.get $l7
          f32.mul
          f32.add
          f32.add
          f32.add
          f32.sqrt
          f32.div
          local.tee $l2
          f32.mul
          f32.store offset=16
          local.get $l4
          local.get $l2
          f32.mul
          local.set $l3
          local.get $l6
          local.get $l2
          f32.mul
          local.set $l5
          local.get $l7
          local.get $l2
          f32.mul
          br $B11
        end
        local.get $l17
        if $I18
          local.get $l13
          local.get $l13
          f32.load offset=88
          f32.store offset=40
          local.get $l13
          local.get $l13
          i64.load offset=80
          i64.store offset=32
        end
        local.get $l15
        i32.eqz
        br_if $B10
        local.get $l13
        f32.load offset=120
        local.tee $l6
        local.get $l13
        f32.load offset=96
        local.tee $l7
        f32.mul
        local.get $l13
        f32.load offset=104
        local.tee $l8
        local.get $l13
        f32.load offset=112
        local.tee $l2
        f32.mul
        f32.sub
        local.set $l10
        local.get $l13
        f32.load offset=116
        local.tee $l9
        local.get $l8
        f32.mul
        local.get $l13
        f32.load offset=100
        local.tee $l3
        local.get $l6
        f32.mul
        f32.sub
        local.set $l11
        local.get $l13
        block $B19 (result f32)
          local.get $l2
          local.get $l3
          f32.mul
          local.get $l7
          local.get $l9
          f32.mul
          f32.sub
          local.tee $l5
          f32.const 0x0p+0 (;=0;)
          f32.lt
          if $I20
            local.get $l2
            local.get $l3
            f32.gt
            if $I21
              f32.const 0x1p-1 (;=0.5;)
              local.get $l2
              f32.const 0x1p+0 (;=1;)
              f32.add
              local.get $l3
              f32.sub
              local.get $l5
              f32.sub
              local.tee $l12
              f32.sqrt
              f32.div
              local.tee $l2
              local.get $l8
              local.get $l10
              f32.sub
              f32.mul
              local.set $l3
              local.get $l6
              local.get $l11
              f32.add
              local.get $l2
              f32.mul
              local.set $l5
              local.get $l9
              local.get $l7
              f32.add
              local.get $l2
              f32.mul
              local.set $l4
              local.get $l12
              local.get $l2
              f32.mul
              br $B19
            end
            local.get $l11
            local.get $l6
            f32.sub
            f32.const 0x1p-1 (;=0.5;)
            f32.const 0x1p+0 (;=1;)
            local.get $l2
            f32.sub
            local.get $l3
            f32.add
            local.get $l5
            f32.sub
            local.tee $l4
            f32.sqrt
            f32.div
            local.tee $l2
            f32.mul
            local.set $l3
            local.get $l2
            local.get $l8
            local.get $l10
            f32.add
            f32.mul
            local.set $l5
            local.get $l4
            local.get $l2
            f32.mul
            local.set $l4
            local.get $l9
            local.get $l7
            f32.add
            local.get $l2
            f32.mul
            br $B19
          end
          local.get $l3
          f32.neg
          local.get $l2
          f32.gt
          if $I22
            local.get $l9
            local.get $l7
            f32.sub
            f32.const 0x1p-1 (;=0.5;)
            local.get $l5
            f32.const 0x1p+0 (;=1;)
            local.get $l2
            f32.sub
            local.get $l3
            f32.sub
            f32.add
            local.tee $l5
            f32.sqrt
            f32.div
            local.tee $l2
            f32.mul
            local.set $l3
            local.get $l5
            local.get $l2
            f32.mul
            local.set $l5
            local.get $l2
            local.get $l8
            local.get $l10
            f32.add
            f32.mul
            local.set $l4
            local.get $l6
            local.get $l11
            f32.add
            local.get $l2
            f32.mul
            br $B19
          end
          local.get $l5
          local.get $l2
          f32.const 0x1p+0 (;=1;)
          f32.add
          local.get $l3
          f32.add
          f32.add
          local.tee $l2
          f32.const 0x1p-1 (;=0.5;)
          local.get $l2
          f32.sqrt
          f32.div
          local.tee $l2
          f32.mul
          local.set $l3
          local.get $l9
          local.get $l7
          f32.sub
          local.get $l2
          f32.mul
          local.set $l5
          local.get $l11
          local.get $l6
          f32.sub
          local.get $l2
          f32.mul
          local.set $l4
          local.get $l2
          local.get $l8
          local.get $l10
          f32.sub
          f32.mul
        end
        local.tee $l6
        f32.const 0x1p+0 (;=1;)
        local.get $l3
        local.get $l3
        f32.mul
        local.get $l5
        local.get $l5
        f32.mul
        local.get $l6
        local.get $l6
        f32.mul
        local.get $l4
        local.get $l4
        f32.mul
        f32.add
        f32.add
        f32.add
        f32.sqrt
        f32.div
        local.tee $l2
        f32.mul
        f32.store offset=16
        local.get $l3
        local.get $l2
        f32.mul
        local.set $l3
        local.get $l5
        local.get $l2
        f32.mul
        local.set $l5
        local.get $l4
        local.get $l2
        f32.mul
      end
      local.set $l2
      local.get $l13
      local.get $l3
      f32.store offset=28
      local.get $l13
      local.get $l5
      f32.store offset=24
      local.get $l13
      local.get $l2
      f32.store offset=20
    end
    local.get $p0
    i32.load offset=32
    local.tee $p0
    i32.const 1
    local.get $l13
    i32.const 16
    i32.add
    local.get $p0
    i32.load
    i32.load offset=32
    call_indirect $__indirect_function_table (type $t2)
    local.get $l13
    i32.const 160
    i32.add
    global.set $g0)