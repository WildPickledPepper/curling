  (func $f73030 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i32)
    global.get $g0
    i32.const 80
    i32.sub
    local.tee $l2
    local.set $l4
    local.get $l2
    global.set $g0
    i32.const 9
    call $f80140
    call $f73714
    local.get $p0
    i32.load offset=52
    local.tee $l5
    if $I0
      i32.const 9
      local.set $l12
      block $B1 (result i32)
        i32.const 9
        local.get $l5
        local.get $l5
        i32.load
        i32.load offset=92
        call_indirect $__indirect_function_table (type $t5)
        local.tee $l8
        i32.const 2
        i32.shl
        local.tee $l5
        i32.eqz
        br_if $B1
        drop
        local.get $l5
        i32.const 3
        i32.or
        local.tee $l3
        i32.const 1999
        i32.le_u
        if $I2
          local.get $l2
          local.get $l3
          i32.const 15
          i32.add
          i32.const -16
          i32.and
          i32.sub
          local.tee $l3
          local.tee $l2
          global.set $g0
          i32.const 9
          br $B1
        end
        local.get $l5
        i32.const 4
        i32.const 1
        i32.const 0
        i32.const 403047
        i32.const 255
        call $f83341
        local.tee $l13
        local.set $l3
        i32.const 1
      end
      local.set $l14
      local.get $p0
      i32.load offset=52
      local.tee $l6
      local.get $l3
      i32.const 3
      i32.add
      i32.const -4
      i32.and
      local.tee $l7
      local.get $l8
      i32.const 0
      local.get $l6
      i32.load
      i32.load offset=96
      call_indirect $__indirect_function_table (type $t8)
      drop
      block $B3
        local.get $l5
        i32.eqz
        if $I4
          i32.const 0
          local.set $l2
          br $B3
        end
        local.get $l5
        i32.const 3
        i32.or
        local.tee $l3
        i32.const 1999
        i32.le_u
        if $I5
          local.get $l2
          local.get $l3
          i32.const 15
          i32.add
          i32.const -16
          i32.and
          i32.sub
          local.tee $l2
          global.set $g0
          br $B3
        end
        i32.const 1
        local.set $l12
        local.get $l5
        i32.const 4
        i32.const 1
        i32.const 0
        i32.const 403047
        i32.const 259
        call $f83341
        local.tee $l15
        local.set $l2
      end
      local.get $l2
      i32.const 3
      i32.add
      i32.const -4
      i32.and
      local.set $l5
      block $B6
        local.get $l8
        i32.const 0
        i32.le_s
        br_if $B6
        local.get $l8
        i32.const 1
        i32.and
        local.set $l9
        i32.const 0
        local.set $l2
        local.get $l8
        i32.const 1
        i32.ne
        if $I7
          local.get $l8
          i32.const -2
          i32.and
          local.set $l10
          loop $L8
            local.get $l5
            local.get $l2
            i32.const 2
            i32.shl
            local.tee $l3
            i32.add
            local.get $l3
            local.get $l7
            i32.add
            i32.load
            i32.load offset=8
            local.tee $l6
            i32.store
            local.get $l6
            local.get $l6
            i32.load
            i32.load offset=152
            call_indirect $__indirect_function_table (type $t7)
            local.get $l5
            local.get $l3
            i32.const 4
            i32.or
            local.tee $l3
            i32.add
            local.get $l3
            local.get $l7
            i32.add
            i32.load
            i32.load offset=8
            local.tee $l3
            i32.store
            local.get $l3
            local.get $l3
            i32.load
            i32.load offset=152
            call_indirect $__indirect_function_table (type $t7)
            local.get $l2
            i32.const 2
            i32.add
            local.set $l2
            local.get $l11
            i32.const 2
            i32.add
            local.tee $l11
            local.get $l10
            i32.ne
            br_if $L8
          end
        end
        local.get $l9
        i32.eqz
        br_if $B6
        local.get $l5
        local.get $l2
        i32.const 2
        i32.shl
        local.tee $l2
        i32.add
        local.get $l2
        local.get $l7
        i32.add
        i32.load
        i32.load offset=8
        local.tee $l2
        i32.store
        local.get $l2
        local.get $l2
        i32.load
        i32.load offset=152
        call_indirect $__indirect_function_table (type $t7)
      end
      block $B9
        local.get $p0
        i32.load offset=48
        local.tee $l2
        local.get $p0
        i32.const 44
        i32.add
        local.tee $l6
        i32.eq
        br_if $B9
        loop $L10
          local.get $l2
          i32.eqz
          if $I11
            local.get $p0
            i32.load offset=4
            local.set $l2
            local.get $l4
            i32.const 403047
            i32.store offset=60
            local.get $l4
            i32.const 403047
            i32.store offset=56
            local.get $l4
            i64.const 0
            i64.store offset=48
            local.get $l4
            i32.const 1
            i32.store8 offset=44
            local.get $l4
            i32.const 403047
            i32.store offset=12
            local.get $l4
            i32.const 403047
            i32.store offset=8
            local.get $l4
            i32.const 403047
            i32.store offset=4
            local.get $l4
            i64.const 0
            i64.store offset=36 align=4
            local.get $l4
            local.get $l2
            i32.store offset=32
            local.get $l4
            i32.const 1
            i32.store offset=28
            local.get $l4
            i64.const -4294967023
            i64.store offset=20 align=4
            local.get $l4
            i32.const 403047
            i32.store offset=16
            local.get $l4
            i32.const 376431
            i32.store
            local.get $l4
            call $f83275
            br $B9
          end
          block $B12
            local.get $l2
            i32.load offset=8
            local.tee $l3
            i32.eqz
            br_if $B12
            local.get $l3
            i32.load offset=28
            local.tee $l7
            i32.eqz
            br_if $B12
            local.get $l7
            call $f80180
            i32.eqz
            br_if $B12
            local.get $l3
            local.get $l3
            i32.load
            i32.load offset=104
            call_indirect $__indirect_function_table (type $t5)
            i32.eqz
            br_if $B12
            local.get $l2
            i32.load
            local.set $l2
            local.get $l3
            local.get $l3
            i32.load
            i32.load offset=152
            call_indirect $__indirect_function_table (type $t7)
            local.get $l3
            local.get $p0
            local.get $l3
            i32.load
            i32.load offset=148
            call_indirect $__indirect_function_table (type $t1)
          end
          local.get $l2
          i32.load offset=4
          local.tee $l2
          local.get $l6
          i32.ne
          br_if $L10
        end
      end
      block $B13
        local.get $p0
        i32.load offset=56
        local.tee $l2
        i32.eqz
        if $I14
          i32.const 0
          local.set $l7
          br $B13
        end
        i32.const 0
        local.set $l7
        local.get $l2
        i32.load offset=48
        local.tee $l6
        i32.eqz
        br_if $B13
        i32.const 0
        local.set $l2
        loop $L15
          local.get $l4
          local.get $l2
          i32.const 2
          i32.shl
          i32.add
          i32.const 4682120
          i32.load
          local.tee $l3
          local.get $p0
          i32.load offset=56
          local.get $l2
          local.get $l3
          i32.load
          i32.load offset=28
          call_indirect $__indirect_function_table (type $t3)
          i32.store
          local.get $l2
          i32.const 1
          i32.add
          local.tee $l2
          local.get $l6
          i32.ne
          br_if $L15
        end
        local.get $l6
        i32.eqz
        br_if $B13
        local.get $l6
        i32.const 1
        i32.and
        local.set $l9
        i32.const 0
        local.set $l2
        local.get $l6
        i32.const 1
        i32.ne
        if $I16
          local.get $l6
          i32.const -2
          i32.and
          local.set $l10
          loop $L17
            local.get $l4
            local.get $l2
            i32.const 2
            i32.shl
            local.tee $l11
            i32.add
            i32.load
            local.tee $l3
            if $I18
              local.get $l3
              local.get $l3
              i32.load
              i32.load offset=152
              call_indirect $__indirect_function_table (type $t7)
            end
            local.get $l4
            local.get $l11
            i32.const 4
            i32.or
            i32.add
            i32.load
            local.tee $l3
            if $I19
              local.get $l3
              local.get $l3
              i32.load
              i32.load offset=152
              call_indirect $__indirect_function_table (type $t7)
            end
            local.get $l2
            i32.const 2
            i32.add
            local.set $l2
            local.get $l7
            i32.const 2
            i32.add
            local.tee $l7
            local.get $l10
            i32.ne
            br_if $L17
          end
        end
        block $B20
          local.get $l9
          i32.eqz
          br_if $B20
          local.get $l4
          local.get $l2
          i32.const 2
          i32.shl
          i32.add
          i32.load
          local.tee $l2
          i32.eqz
          br_if $B20
          local.get $l2
          local.get $l2
          i32.load
          i32.load offset=152
          call_indirect $__indirect_function_table (type $t7)
        end
        local.get $l6
        local.set $l7
      end
      local.get $p0
      i32.load8_u offset=84
      if $I21
        local.get $p0
        i32.load offset=68
        i32.load offset=8
        local.tee $l2
        local.get $p0
        i32.load offset=52
        i32.const 1
        local.get $l2
        i32.load
        i32.load offset=56
        call_indirect $__indirect_function_table (type $t2)
      end
      local.get $p0
      i32.load offset=52
      local.tee $l2
      local.get $l2
      i32.load
      i32.load
      call_indirect $__indirect_function_table (type $t7)
      i32.const 0
      local.set $l2
      local.get $p0
      i32.const 0
      i32.store offset=52
      block $B22
        local.get $p1
        i32.eqz
        br_if $B22
        local.get $l8
        i32.const 0
        i32.gt_s
        if $I23
          loop $L24
            local.get $l5
            local.get $l2
            i32.const 2
            i32.shl
            i32.add
            i32.load
            local.get $p0
            call $f73271
            local.get $l2
            i32.const 1
            i32.add
            local.tee $l2
            local.get $l8
            i32.ne
            br_if $L24
          end
        end
        local.get $l7
        i32.eqz
        br_if $B22
        i32.const 0
        local.set $l2
        loop $L25
          local.get $l4
          local.get $l2
          i32.const 2
          i32.shl
          i32.add
          i32.load
          local.tee $l5
          if $I26
            local.get $l5
            local.get $p0
            call $f73271
          end
          local.get $l2
          i32.const 1
          i32.add
          local.tee $l2
          local.get $l7
          i32.ne
          br_if $L25
        end
      end
      local.get $p0
      i32.load offset=168
      local.tee $l2
      if $I27
        local.get $l2
        i32.load
        local.tee $l5
        if $I28
          local.get $l5
          local.get $l2
          i32.load offset=4
          i32.store offset=4
          local.get $l2
          i32.load offset=4
          local.get $l2
          i32.load
          i32.store
          local.get $l2
          i64.const 0
          i64.store align=4
        end
        local.get $l2
        i32.const 41
        i32.const 403047
        i32.const 344
        call $f83342
        local.get $p0
        i32.const 0
        i32.store offset=168
      end
      local.get $p0
      local.get $p0
      i32.load offset=140
      i32.store offset=144
      local.get $p0
      local.get $p0
      i32.load8_u offset=148
      i32.store8 offset=149
      local.get $l15
      local.get $l12
      i32.const 403047
      i32.const 411
      call $f83342
      local.get $l13
      local.get $l14
      i32.const 403047
      i32.const 411
      call $f83342
    end
    local.get $p0
    i32.load offset=32
    local.tee $l2
    if $I29
      local.get $l2
      local.get $p0
      i32.const 36
      i32.add
      local.tee $l5
      i32.load
      i32.store offset=4
      local.get $l5
      i32.load
      local.get $p0
      i32.load offset=32
      i32.store
      local.get $p0
      i64.const 0
      i64.store offset=32 align=4
    end
    local.get $p0
    i32.const 0
    i32.store offset=68
    local.get $l4
    i32.const 80
    i32.add
    global.set $g0)