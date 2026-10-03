  (func $f71765 (type $t9) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (result i32)
    (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l6
    global.set $g0
    i32.const -1
    local.set $l8
    block $B0
      block $B1
        block $B2
          local.get $p3
          br_table $B2 $B1 $B0
        end
        local.get $p1
        i32.load offset=4
        local.tee $p3
        i32.eqz
        br_if $B0
        local.get $p0
        i32.const 1
        call $f71743
        local.get $p0
        local.get $p3
        i32.store offset=4
        local.get $p1
        local.get $p0
        i32.const 12
        i32.add
        local.get $p2
        local.get $p0
        call $f70311
        i32.eqz
        br_if $B0
        call $f69753
        local.tee $p3
        i32.const 16
        i32.const 3177279
        i32.const 3176295
        i32.const 4700888
        i32.load
        local.tee $l5
        local.get $l5
        i32.load
        i32.load offset=20
        call_indirect $__indirect_function_table (type $t5)
        select
        i32.const 3175524
        i32.const 281
        local.get $p3
        i32.load
        i32.load offset=8
        call_indirect $__indirect_function_table (type $t9)
        local.tee $p3
        i64.const 0
        i64.store align=4
        local.get $p3
        i32.const 8
        i32.add
        local.tee $l5
        i64.const 0
        i64.store align=4
        local.get $p0
        local.get $p3
        i32.store offset=48
        local.get $l6
        local.get $p0
        i32.load offset=12
        local.tee $p0
        i32.store offset=4
        local.get $l5
        i32.load
        i32.const 2147483647
        i32.and
        local.get $p3
        i32.load offset=4
        local.tee $l5
        i32.le_u
        if $I3
          local.get $p3
          local.get $l6
          i32.const 4
          i32.add
          call $f71766
          i32.const 0
          local.set $l8
          br $B0
        end
        local.get $p3
        i32.load
        local.get $l5
        i32.const 2
        i32.shl
        i32.add
        local.get $p0
        i32.store
        local.get $p3
        local.get $p3
        i32.load offset=4
        i32.const 1
        i32.add
        i32.store offset=4
        i32.const 0
        local.set $l8
        br $B0
      end
      local.get $p0
      i32.load offset=48
      i32.load offset=4
      if $I4
        local.get $p4
        i32.eqz
        if $I5
          i32.const 1
          local.set $l8
          br $B0
        end
        local.get $p0
        i32.const 12
        i32.add
        local.set $l10
        i32.const 1
        local.set $l8
        loop $L6
          local.get $p0
          i32.load offset=48
          local.tee $p3
          i32.load offset=4
          local.tee $l9
          i32.eqz
          br_if $B0
          local.get $p3
          local.get $p3
          i32.load offset=12
          local.tee $l5
          i32.const 1
          i32.add
          local.tee $l7
          i32.store offset=12
          local.get $p3
          i32.load
          local.get $l5
          i32.const 2
          i32.shl
          i32.add
          i32.load
          local.set $l5
          local.get $l7
          local.get $l9
          i32.eq
          if $I7
            local.get $p3
            i32.const 0
            i32.store offset=12
            local.get $p3
            i32.const 0
            i32.store offset=4
          end
          local.get $p0
          i32.load offset=48
          local.set $p3
          local.get $l5
          local.get $p1
          local.get $p2
          local.get $l10
          local.get $p0
          i32.load
          call $f70309
          block $B8
            local.get $l5
            i32.load offset=24
            local.tee $l9
            i32.eqz
            br_if $B8
            local.get $l6
            local.get $l9
            i32.const 36
            i32.add
            local.tee $l7
            i32.store offset=8
            block $B9
              local.get $p3
              i32.load offset=4
              local.tee $l11
              local.get $p3
              i32.load offset=8
              i32.const 2147483647
              i32.and
              i32.ge_u
              if $I10
                local.get $p3
                local.get $l6
                i32.const 8
                i32.add
                call $f71766
                local.get $p3
                i32.load offset=4
                local.set $l7
                br $B9
              end
              local.get $p3
              i32.load
              local.get $l11
              i32.const 2
              i32.shl
              i32.add
              local.get $l7
              i32.store
              local.get $p3
              local.get $p3
              i32.load offset=4
              i32.const 1
              i32.add
              local.tee $l7
              i32.store offset=4
            end
            local.get $l6
            local.get $l9
            i32.store offset=12
            local.get $l7
            local.get $p3
            i32.load offset=8
            i32.const 2147483647
            i32.and
            i32.ge_u
            if $I11
              local.get $p3
              local.get $l6
              i32.const 12
              i32.add
              call $f71766
              br $B8
            end
            local.get $p3
            i32.load
            local.get $l7
            i32.const 2
            i32.shl
            i32.add
            local.get $l9
            i32.store
            local.get $p3
            local.get $p3
            i32.load offset=4
            i32.const 1
            i32.add
            i32.store offset=4
          end
          local.get $p2
          local.get $p2
          i32.load offset=4
          local.get $l5
          i32.load offset=32
          i32.add
          i32.store offset=4
          local.get $l5
          i32.load offset=32
          local.get $l12
          i32.add
          local.tee $l12
          local.get $p4
          i32.lt_u
          br_if $L6
        end
        br $B0
      end
      local.get $p0
      local.get $p1
      local.get $p2
      call $f71758
      local.get $p0
      i32.load offset=48
      local.tee $p3
      if $I12
        block $B13
          local.get $p3
          i32.load offset=8
          local.tee $l5
          i32.const 0
          i32.lt_s
          br_if $B13
          local.get $l5
          i32.const 2147483647
          i32.and
          i32.eqz
          br_if $B13
          local.get $p3
          i32.load
          local.tee $l5
          i32.eqz
          br_if $B13
          call $f69753
          local.tee $p2
          local.get $l5
          local.get $p2
          i32.load
          i32.load offset=12
          call_indirect $__indirect_function_table (type $t1)
        end
        call $f69753
        local.tee $l5
        local.get $p3
        local.get $l5
        i32.load
        i32.load offset=12
        call_indirect $__indirect_function_table (type $t1)
      end
      i32.const 0
      local.set $l8
      local.get $p0
      i32.const 0
      i32.store offset=48
    end
    local.get $l6
    i32.const 16
    i32.add
    global.set $g0
    local.get $l8)