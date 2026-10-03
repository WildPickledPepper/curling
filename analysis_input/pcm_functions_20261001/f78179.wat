  (func $f78179 (type $t2) (param $p0 i32) (param $p1 i32) (param $p2 i32)
    (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32)
    global.get $g0
    i32.const 32
    i32.sub
    local.tee $l4
    global.set $g0
    i32.const 128
    i32.const 16
    i32.const 1
    i32.const 0
    i32.const 403047
    i32.const 94
    call $f83341
    local.set $l6
    block $B0
      block $B1
        local.get $p1
        local.get $p2
        i32.eq
        if $I2
          local.get $l6
          local.set $l5
          br $B1
        end
        local.get $l6
        i32.const 128
        i32.add
        local.set $l3
        local.get $l6
        local.set $l5
        loop $L3
          block $B4
            local.get $l3
            local.get $l5
            i32.ne
            if $I5
              local.get $l5
              local.get $p1
              i32.store
              br $B4
            end
            local.get $l3
            local.get $l6
            i32.sub
            local.tee $l7
            i32.const -5
            i32.le_s
            br_if $B0
            local.get $l7
            i32.const 2
            i32.shr_s
            local.tee $l5
            i32.const 1
            i32.add
            local.tee $l8
            local.get $l7
            i32.const 1
            i32.shr_s
            local.tee $l9
            local.get $l8
            local.get $l9
            i32.gt_u
            select
            i32.const 2147483647
            local.get $l7
            i32.const 0
            i32.ge_s
            select
            local.tee $l7
            if $I6 (result i32)
              local.get $l7
              i32.const 2
              i32.shl
              i32.const 16
              i32.const 1
              i32.const 0
              i32.const 403047
              i32.const 94
              call $f83341
            else
              i32.const 0
            end
            local.set $l8
            local.get $l8
            local.get $l5
            i32.const 2
            i32.shl
            i32.add
            local.tee $l5
            local.get $p1
            i32.store
            local.get $l7
            i32.const 2
            i32.shl
            local.set $l9
            local.get $l5
            local.set $l7
            local.get $l3
            local.get $l6
            i32.ne
            if $I7
              loop $L8
                local.get $l7
                i32.const 4
                i32.sub
                local.tee $l7
                local.get $l3
                i32.const 4
                i32.sub
                local.tee $l3
                i32.load
                i32.store
                local.get $l3
                local.get $l6
                i32.ne
                br_if $L8
              end
            end
            local.get $l8
            local.get $l9
            i32.add
            local.set $l3
            local.get $l6
            if $I9
              local.get $l6
              i32.const 1
              i32.const 403047
              i32.const 99
              call $f83342
            end
            local.get $l7
            local.set $l6
          end
          local.get $l5
          i32.const 4
          i32.add
          local.set $l5
          local.get $p1
          i32.load offset=96
          local.tee $p1
          local.get $p2
          i32.eq
          br_if $B1
          local.get $p1
          br_if $L3
        end
      end
      local.get $l4
      i32.const 275
      i32.store16 offset=19 align=1
      local.get $l4
      i32.const 0
      i32.store8
      local.get $l4
      i32.const 1
      i32.store offset=24
      local.get $l4
      i32.const 512
      call $f83396
      drop
      local.get $l5
      local.get $l6
      i32.ne
      if $I10
        local.get $l4
        local.get $l6
        i32.const 4
        i32.add
        local.tee $l7
        local.get $l5
        i32.ne
        if $I11 (result i32)
          loop $L12
            local.get $l4
            local.get $l5
            i32.const 4
            i32.sub
            local.tee $l5
            i32.load
            local.tee $l3
            local.get $l3
            i32.load
            i32.load offset=40
            call_indirect $__indirect_function_table (type $t5)
            local.tee $l3
            local.get $l3
            call $strlen
            call $f83266
            local.get $l4
            i32.const 235921
            i32.const 1
            call $f83266
            local.get $l5
            local.get $l7
            i32.ne
            br_if $L12
          end
          local.get $l7
        else
          local.get $l5
        end
        i32.const 4
        i32.sub
        i32.load
        local.tee $l3
        local.get $l3
        i32.load
        i32.load offset=40
        call_indirect $__indirect_function_table (type $t5)
        local.tee $l3
        local.get $l3
        call $strlen
        call $f83266
      end
      local.get $p0
      local.get $l4
      i32.load8_u offset=20
      local.tee $l3
      i32.store8 offset=20
      local.get $p0
      local.get $l4
      i32.load offset=24
      i32.store offset=24
      block $B13
        local.get $l3
        i32.const 1
        i32.eq
        if $I14
          local.get $p0
          local.get $l4
          i64.load
          i64.store align=4
          local.get $p0
          local.get $l4
          i32.load offset=16
          i32.store offset=16
          local.get $p0
          local.get $l4
          i64.load offset=8
          i64.store offset=8 align=4
          br $B13
        end
        local.get $p0
        local.get $l4
        i64.load
        i64.store align=4
        local.get $p0
        local.get $l4
        i32.load offset=8
        i32.store offset=8
      end
      local.get $l6
      if $I15
        local.get $l6
        i32.const 1
        i32.const 403047
        i32.const 99
        call $f83342
      end
      local.get $l4
      i32.const 32
      i32.add
      global.set $g0
      return
    end
    call $env.abort
    unreachable)
