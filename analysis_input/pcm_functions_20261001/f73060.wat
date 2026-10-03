  (func $f73060 (type $t7) (param $p0 i32)
    (local $l1 i32) (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32)
    global.get $g0
    i32.const -64
    i32.add
    local.tee $l1
    local.set $l2
    local.get $l1
    global.set $g0
    i32.const 9
    call $f80140
    call $f73714
    block $B0
      local.get $p0
      i32.load offset=52
      local.tee $l3
      i32.eqz
      br_if $B0
      local.get $p0
      i32.load8_u offset=133
      if $I1
        local.get $l3
        local.get $p0
        f32.load offset=72
        local.get $l3
        i32.load
        i32.load offset=116
        call_indirect $__indirect_function_table (type $t21)
        br $B0
      end
      block $B2
        local.get $p0
        i32.load8_u offset=100
        local.get $p0
        i32.load8_u offset=85
        i32.or
        if $I3
          i32.const 9
          local.set $l6
          block $B4
            local.get $l3
            local.get $l3
            i32.load
            i32.load offset=92
            call_indirect $__indirect_function_table (type $t5)
            local.tee $l4
            i32.const 2
            i32.shl
            local.tee $l3
            i32.eqz
            if $I5
              i32.const 0
              local.set $l3
              br $B4
            end
            local.get $l3
            i32.const 3
            i32.or
            local.tee $l5
            i32.const 1999
            i32.le_u
            if $I6
              local.get $l1
              local.get $l5
              i32.const 15
              i32.add
              i32.const -16
              i32.and
              i32.sub
              local.tee $l3
              global.set $g0
              br $B4
            end
            i32.const 1
            local.set $l6
            local.get $l3
            i32.const 4
            i32.const 1
            i32.const 0
            i32.const 403047
            i32.const 866
            call $f83341
            local.tee $l8
            local.set $l3
          end
          local.get $p0
          i32.load offset=52
          local.tee $l1
          local.get $l3
          i32.const 3
          i32.add
          i32.const -4
          i32.and
          local.tee $l5
          local.get $l4
          i32.const 0
          local.get $l1
          i32.load
          i32.load offset=96
          call_indirect $__indirect_function_table (type $t8)
          drop
          i32.const 1
          local.set $l3
          block $B7
            local.get $l4
            i32.const 0
            i32.gt_s
            if $I8
              local.get $l2
              i32.const 16
              i32.add
              local.get $l5
              i32.load
              local.tee $l1
              local.get $l1
              i32.load
              i32.load offset=156
              call_indirect $__indirect_function_table (type $t1)
              block $B9
                local.get $l2
                i32.load8_u offset=16
                i32.const 4
                i32.and
                if $I10
                  loop $L11
                    local.get $l3
                    local.tee $l1
                    local.get $l4
                    i32.eq
                    br_if $B9
                    local.get $l2
                    i32.const 16
                    i32.add
                    local.get $l5
                    local.get $l1
                    i32.const 2
                    i32.shl
                    i32.add
                    i32.load
                    local.tee $l3
                    local.get $l3
                    i32.load
                    i32.load offset=156
                    call_indirect $__indirect_function_table (type $t1)
                    local.get $l1
                    i32.const 1
                    i32.add
                    local.set $l3
                    local.get $l2
                    i32.load8_u offset=16
                    i32.const 4
                    i32.and
                    br_if $L11
                  end
                  local.get $l1
                  local.get $l4
                  i32.lt_s
                  local.set $l3
                end
                local.get $l2
                i32.const 16
                i32.add
                local.get $p0
                i32.load offset=52
                local.tee $l1
                local.get $l1
                i32.load
                i32.load offset=112
                call_indirect $__indirect_function_table (type $t1)
                local.get $l2
                local.get $l2
                f32.load offset=32
                f32.store offset=48
                local.get $l2
                local.get $l2
                i64.load offset=36 align=4
                i64.store offset=52 align=4
                local.get $l2
                local.get $p0
                i32.load offset=52
                local.tee $l1
                local.get $l1
                i32.load
                i32.load offset=132
                call_indirect $__indirect_function_table (type $t1)
                local.get $l2
                i32.const 16
                i32.add
                local.get $p0
                i32.load offset=52
                local.tee $l1
                local.get $l1
                i32.load
                i32.load offset=112
                call_indirect $__indirect_function_table (type $t1)
                local.get $l2
                f32.load offset=28
                local.set $l9
                local.get $l2
                f32.load offset=24
                local.set $l10
                local.get $l2
                f32.load offset=20
                local.set $l11
                local.get $l2
                f32.load offset=16
                local.set $l12
                local.get $p0
                i32.load offset=52
                local.get $p0
                f32.load offset=72
                i32.const 0
                local.get $l2
                i32.const 48
                i32.add
                local.get $p0
                i32.load8_u offset=85
                select
                call $f72778
                local.get $p0
                i32.load8_u offset=100
                i32.eqz
                if $I12
                  local.get $l2
                  i32.const 16
                  i32.add
                  local.get $p0
                  i32.load offset=52
                  local.tee $l1
                  local.get $l1
                  i32.load
                  i32.load offset=112
                  call_indirect $__indirect_function_table (type $t1)
                  local.get $l2
                  local.get $l9
                  f32.store offset=28
                  local.get $l2
                  local.get $l10
                  f32.store offset=24
                  local.get $l2
                  local.get $l11
                  f32.store offset=20
                  local.get $l2
                  local.get $l12
                  f32.store offset=16
                  local.get $p0
                  i32.load offset=52
                  local.tee $l1
                  local.get $l2
                  i32.const 16
                  i32.add
                  local.get $l1
                  i32.load
                  i32.load offset=108
                  call_indirect $__indirect_function_table (type $t1)
                  local.get $p0
                  i32.load offset=52
                  local.tee $l1
                  local.get $l2
                  local.get $l1
                  i32.load
                  i32.load offset=128
                  call_indirect $__indirect_function_table (type $t1)
                end
                local.get $p0
                i32.load offset=56
                if $I13
                  i32.const 4682120
                  i32.load
                  local.tee $l1
                  local.get $p0
                  local.get $l1
                  i32.load
                  i32.load offset=24
                  call_indirect $__indirect_function_table (type $t1)
                end
                local.get $p0
                i32.load offset=136
                i32.eqz
                br_if $B7
                local.get $p0
                call $f73070
                br $B7
              end
              local.get $l1
              local.get $l4
              i32.lt_s
              local.set $l7
            end
            local.get $p0
            i32.load8_u offset=85
            if $I14
              local.get $l2
              i32.const 16
              i32.add
              local.get $p0
              i32.load offset=52
              local.tee $l1
              local.get $l1
              i32.load
              i32.load offset=112
              call_indirect $__indirect_function_table (type $t1)
              local.get $l2
              i32.const 4748496
              f32.load
              f32.store offset=40
              local.get $l2
              i32.const 4748488
              i64.load align=4
              i64.store offset=32
              local.get $p0
              i32.load offset=52
              local.tee $l1
              local.get $l2
              i32.const 16
              i32.add
              local.get $l1
              i32.load
              i32.load offset=108
              call_indirect $__indirect_function_table (type $t1)
            end
            block $B15
              local.get $p0
              i32.load8_u offset=100
              i32.eqz
              br_if $B15
              local.get $p0
              i32.load offset=52
              local.tee $l1
              local.get $p0
              f32.load offset=72
              local.get $l1
              i32.load
              i32.load offset=116
              call_indirect $__indirect_function_table (type $t21)
              local.get $l2
              i32.const 16
              i32.add
              local.get $p0
              i32.load offset=52
              local.tee $l1
              local.get $l1
              i32.load
              i32.load offset=112
              call_indirect $__indirect_function_table (type $t1)
              local.get $l2
              i64.const 4575657221408423936
              i64.store offset=24
              local.get $l2
              i64.const 0
              i64.store offset=16
              local.get $p0
              i32.load offset=52
              local.tee $l1
              local.get $l2
              i32.const 16
              i32.add
              local.get $l1
              i32.load
              i32.load offset=108
              call_indirect $__indirect_function_table (type $t1)
              local.get $p0
              i32.load offset=52
              local.tee $l1
              i32.const 4748500
              local.get $l1
              i32.load
              i32.load offset=128
              call_indirect $__indirect_function_table (type $t1)
              local.get $p0
              i32.load offset=136
              i32.eqz
              br_if $B15
              local.get $p0
              call $f73070
            end
            local.get $l7
            local.set $l3
          end
          local.get $l8
          local.get $l6
          i32.const 403047
          i32.const 411
          call $f83342
          local.get $l3
          br_if $B0
          local.get $p0
          i32.load offset=56
          br_if $B2
          br $B0
        end
        local.get $p0
        i32.load offset=56
        i32.eqz
        br_if $B0
      end
      i32.const 4682120
      i32.load
      local.tee $l1
      local.get $p0
      local.get $l1
      i32.load
      i32.load offset=24
      call_indirect $__indirect_function_table (type $t1)
    end
    local.get $l2
    i32.const -64
    i32.sub
    global.set $g0)