  (func $f71945 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32)
    local.get $p1
    i32.load
    local.tee $l2
    local.get $p0
    i32.const 116
    i32.add
    local.tee $l5
    i32.load
    i32.ne
    if $I0
      i32.const 4700888
      i32.load
      i32.const 4
      i32.const 3180096
      i32.const 258
      i32.const 3180133
      i32.const 0
      call $f69760
      return
    end
    block $B1
      block $B2 (result i32)
        block $B3
          block $B4
            block $B5
              local.get $l2
              i32.const 4
              i32.sub
              br_table $B5 $B3 $B4 $B1
            end
            local.get $l5
            local.set $l2
            local.get $p0
            i32.load8_u offset=36
            i32.const 1
            i32.and
            if $I6 (result i32)
              local.get $p0
              i32.load offset=40
              i32.const -64
              i32.sub
            else
              local.get $l2
            end
            i32.load offset=32
            local.tee $l2
            i32.eqz
            br_if $B1
            local.get $l2
            i32.const 8
            i32.add
            br $B2
          end
          local.get $l5
          local.set $l2
          local.get $p0
          i32.load8_u offset=36
          i32.const 1
          i32.and
          if $I7 (result i32)
            local.get $p0
            i32.load offset=40
            i32.const -64
            i32.sub
          else
            local.get $l2
          end
          i32.load offset=4
          local.tee $l2
          i32.eqz
          br_if $B1
          local.get $l2
          i32.const 8
          i32.add
          br $B2
        end
        local.get $l5
        local.set $l2
        local.get $p0
        i32.load8_u offset=36
        i32.const 1
        i32.and
        if $I8 (result i32)
          local.get $p0
          i32.load offset=40
          i32.const -64
          i32.sub
        else
          local.get $l2
        end
        i32.load offset=36
        local.tee $l2
        i32.eqz
        br_if $B1
        local.get $l2
        i32.const 8
        i32.add
      end
      local.tee $l2
      i32.const 4
      i32.add
      call $f722
      br_if $B1
      local.get $l2
      local.get $l2
      i32.load
      i32.load offset=8
      call_indirect $__indirect_function_table (type $t7)
    end
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l2
    global.set $g0
    block $B9
      block $B10
        block $B11
          block $B12
            block $B13
              block $B14
                block $B15
                  local.get $p0
                  i32.const 32
                  i32.add
                  local.tee $l3
                  i32.load offset=4
                  i32.const 30
                  i32.shr_u
                  i32.const 2
                  i32.sub
                  br_table $B14 $B11 $B15
                end
                local.get $l3
                i32.load
                local.tee $l4
                br_if $B13
                local.get $l3
                i32.const 16
                i32.add
                local.tee $l6
                local.get $p1
                call $f71451
                br $B12
              end
              local.get $l3
              i32.load
              local.tee $l4
              i32.load8_u offset=4785
              br_if $B10
            end
            local.get $l4
            i32.const 16
            i32.add
            local.tee $l4
            local.get $l3
            i32.const 16
            i32.add
            local.tee $l6
            call $f71436
            local.get $l6
            local.get $p1
            call $f71451
            local.get $l4
            local.get $l6
            call $f71435
          end
          local.get $l3
          i32.const 12
          i32.sub
          i32.load
          local.tee $l3
          i32.eqz
          br_if $B9
          local.get $l2
          i32.const 0
          i32.store8
          local.get $l2
          i32.const 1
          i32.store offset=8
          local.get $l3
          i32.const -64
          i32.sub
          local.get $l6
          local.get $l2
          i32.const 8
          i32.add
          local.get $l2
          i32.const 0
          call $f71723
          br $B9
        end
        local.get $l3
        i32.load
        local.set $l4
      end
      local.get $l4
      local.get $l3
      call $f71985
      local.get $l3
      local.get $l3
      i32.load offset=4
      local.tee $l6
      i32.const 1
      i32.or
      i32.store offset=4
      local.get $l3
      i32.load offset=8
      local.tee $l4
      i32.eqz
      if $I16
        local.get $l3
        local.get $l3
        i32.load
        local.get $l6
        i32.const 24
        i32.shr_u
        i32.const 15
        i32.and
        call $f71984
        local.tee $l4
        i32.store offset=8
      end
      local.get $l4
      i32.const -64
      i32.sub
      local.get $p1
      call $f70398
    end
    local.get $l2
    i32.const 16
    i32.add
    global.set $g0
    block $B17
      block $B18 (result i32)
        block $B19
          block $B20
            block $B21
              local.get $p0
              i32.load offset=116
              i32.const 4
              i32.sub
              br_table $B21 $B19 $B20 $B17
            end
            local.get $p0
            i32.load8_u offset=36
            i32.const 1
            i32.and
            if $I22 (result i32)
              local.get $p0
              i32.load offset=40
              i32.const -64
              i32.sub
            else
              local.get $l5
            end
            i32.load offset=32
            local.tee $p1
            i32.eqz
            br_if $B17
            local.get $p1
            i32.const 8
            i32.add
            br $B18
          end
          local.get $p0
          i32.load8_u offset=36
          i32.const 1
          i32.and
          if $I23 (result i32)
            local.get $p0
            i32.load offset=40
            i32.const -64
            i32.sub
          else
            local.get $l5
          end
          i32.load offset=4
          local.tee $p1
          i32.eqz
          br_if $B17
          local.get $p1
          i32.const 8
          i32.add
          br $B18
        end
        local.get $p0
        i32.load8_u offset=36
        i32.const 1
        i32.and
        if $I24 (result i32)
          local.get $p0
          i32.load offset=40
          i32.const -64
          i32.sub
        else
          local.get $l5
        end
        i32.load offset=36
        local.tee $p1
        i32.eqz
        br_if $B17
        local.get $p1
        i32.const 8
        i32.add
      end
      i32.const 4
      i32.add
      call $f1709
      drop
    end
    local.get $p0
    i32.const 3180229
    call $f71944)
