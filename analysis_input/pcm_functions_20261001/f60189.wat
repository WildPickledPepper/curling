  (func $f60189 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l4
    global.set $g0
    i32.const 4674512
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3792608
      call $f1661
      i32.const 3773132
      call $f1661
      i32.const 3859564
      call $f1661
      i32.const 3816928
      call $f1661
      i32.const 4674512
      i32.const 1
      i32.store8
    end
    local.get $l4
    i32.const 0
    i32.store offset=12
    local.get $l4
    i32.const 0
    i32.store offset=8
    local.get $l4
    i32.const 0
    i32.store offset=4
    block $B1
      local.get $p0
      i32.load offset=96
      local.tee $p1
      i32.load offset=12
      local.tee $l3
      i32.const 0
      i32.le_s
      if $I2
        br $B1
      end
      local.get $p0
      i32.const 144
      i32.add
      local.set $l7
      local.get $p0
      i32.const 140
      i32.add
      local.set $l9
      loop $L3
        block $B4 (result i32)
          local.get $l2
          i32.const 2
          i32.shl
          local.tee $l3
          local.get $p1
          i32.load offset=20
          i32.add
          i32.load offset=16
          i32.const 0
          i32.gt_s
          if $I5
            local.get $p0
            i32.load offset=140
            local.get $l2
            i32.const 3773132
            i32.load
            call $f2903
            i32.const 3792608
            i32.load
            call $f34548
            local.tee $p1
            local.get $p0
            i32.load offset=96
            i32.load offset=20
            local.get $l3
            i32.add
            i32.const 16
            i32.add
            i32.const 0
            call $f56590
            local.get $p1
            i32.load
            local.tee $p1
            i32.load offset=796
            local.get $p1
            i32.load offset=792
            call_indirect $__indirect_function_table (type $t2)
            local.get $l4
            local.get $p0
            i32.load offset=96
            i32.load offset=20
            local.get $l3
            i32.add
            i32.load offset=16
            local.get $l6
            i32.add
            local.tee $l6
            i32.store offset=12
            local.get $l7
            br $B4
          end
          local.get $p0
          i32.load offset=144
          local.get $l2
          i32.const 3773132
          i32.load
          call $f2903
          i32.const 3792608
          i32.load
          call $f34548
          local.set $p1
          local.get $l4
          i32.const 0
          local.get $p0
          i32.load offset=96
          i32.load offset=20
          local.get $l3
          i32.add
          i32.load offset=16
          i32.sub
          i32.store offset=4
          local.get $p1
          local.get $l4
          i32.const 4
          i32.add
          i32.const 0
          call $f56590
          local.get $p1
          i32.load
          local.tee $l8
          i32.load offset=796
          local.get $l8
          i32.load offset=792
          call_indirect $__indirect_function_table (type $t2)
          local.get $l4
          local.get $l5
          local.get $p0
          i32.load offset=96
          i32.load offset=20
          local.get $l3
          i32.add
          i32.load offset=16
          i32.sub
          local.tee $l5
          i32.store offset=8
          local.get $l9
        end
        i32.load
        local.get $l2
        i32.const 3773132
        i32.load
        call $f2903
        i32.const 3792608
        i32.load
        call $f34548
        local.tee $l3
        i32.const 3816928
        i32.load
        local.get $l3
        i32.load
        local.tee $l3
        i32.load offset=796
        local.get $l3
        i32.load offset=792
        call_indirect $__indirect_function_table (type $t2)
        local.get $l2
        i32.const 1
        i32.add
        local.tee $l2
        local.get $p0
        i32.load offset=96
        local.tee $p1
        i32.load offset=12
        local.tee $l3
        i32.lt_s
        br_if $L3
      end
    end
    local.get $p1
    i32.load offset=16
    local.get $l3
    i32.gt_s
    if $I6
      local.get $p0
      i32.const 144
      i32.add
      local.set $l8
      local.get $p0
      i32.const 140
      i32.add
      local.set $l7
      loop $L7
        local.get $p0
        i32.load offset=140
        local.get $l3
        i32.const 3773132
        i32.load
        call $f2903
        i32.const 3792608
        i32.load
        call $f34548
        local.tee $l2
        i32.const 3859564
        i32.load
        local.get $l2
        i32.load
        local.tee $l2
        i32.load offset=796
        local.get $l2
        i32.load offset=792
        call_indirect $__indirect_function_table (type $t2)
        local.get $p0
        i32.load offset=144
        local.get $l3
        i32.const 3773132
        i32.load
        call $f2903
        i32.const 3792608
        i32.load
        call $f34548
        local.tee $l2
        i32.const 3859564
        i32.load
        local.get $l2
        i32.load
        local.tee $l2
        i32.load offset=796
        local.get $l2
        i32.load offset=792
        call_indirect $__indirect_function_table (type $t2)
        block $B8
          local.get $p0
          i32.load offset=96
          local.tee $l2
          i32.load offset=12
          local.tee $p1
          local.get $l2
          i32.load offset=16
          i32.const 1
          i32.sub
          i32.ne
          br_if $B8
          local.get $l2
          i32.load offset=8
          i32.const 16
          i32.ne
          br_if $B8
          block $B9 (result i32)
            local.get $l2
            i32.load offset=20
            local.get $p1
            i32.const 2
            i32.shl
            i32.add
            i32.load offset=16
            i32.const 0
            i32.gt_s
            if $I10
              local.get $p0
              i32.load offset=140
              local.get $p1
              i32.const 3773132
              i32.load
              call $f2903
              i32.const 3792608
              i32.load
              call $f34548
              local.tee $l2
              local.get $p0
              i32.load offset=96
              local.tee $p1
              i32.load offset=20
              local.get $p1
              i32.load offset=12
              i32.const 2
              i32.shl
              i32.add
              i32.const 16
              i32.add
              i32.const 0
              call $f56590
              local.get $l2
              i32.load
              local.tee $l2
              i32.load offset=796
              local.get $l2
              i32.load offset=792
              call_indirect $__indirect_function_table (type $t2)
              local.get $l4
              local.get $p0
              i32.load offset=96
              local.tee $l2
              i32.load offset=20
              local.get $l2
              i32.load offset=12
              local.tee $l2
              i32.const 2
              i32.shl
              i32.add
              i32.load offset=16
              local.get $l6
              i32.add
              local.tee $l6
              i32.store offset=12
              local.get $l8
              br $B9
            end
            local.get $p0
            i32.load offset=144
            local.get $p1
            i32.const 3773132
            i32.load
            call $f2903
            i32.const 3792608
            i32.load
            call $f34548
            local.set $l2
            local.get $l4
            i32.const 0
            local.get $p0
            i32.load offset=96
            local.tee $p1
            i32.load offset=20
            local.get $p1
            i32.load offset=12
            i32.const 2
            i32.shl
            i32.add
            i32.load offset=16
            i32.sub
            i32.store offset=4
            local.get $l2
            local.get $l4
            i32.const 4
            i32.add
            i32.const 0
            call $f56590
            local.get $l2
            i32.load
            local.tee $p1
            i32.load offset=796
            local.get $p1
            i32.load offset=792
            call_indirect $__indirect_function_table (type $t2)
            local.get $l4
            local.get $l5
            local.get $p0
            i32.load offset=96
            local.tee $l2
            i32.load offset=20
            local.get $l2
            i32.load offset=12
            local.tee $l2
            i32.const 2
            i32.shl
            i32.add
            i32.load offset=16
            i32.sub
            local.tee $l5
            i32.store offset=8
            local.get $l7
          end
          i32.load
          local.get $l2
          i32.const 3773132
          i32.load
          call $f2903
          i32.const 3792608
          i32.load
          call $f34548
          local.tee $l2
          i32.const 3816928
          i32.load
          local.get $l2
          i32.load
          local.tee $l2
          i32.load offset=796
          local.get $l2
          i32.load offset=792
          call_indirect $__indirect_function_table (type $t2)
        end
        local.get $l3
        i32.const 1
        i32.add
        local.tee $l3
        local.get $p0
        i32.load offset=96
        i32.load offset=16
        i32.lt_s
        br_if $L7
      end
    end
    local.get $p0
    i32.load offset=148
    i32.const 0
    i32.const 3773132
    i32.load
    call $f2903
    i32.const 3792608
    i32.load
    call $f34548
    local.tee $l2
    local.get $l4
    i32.const 12
    i32.add
    i32.const 0
    call $f56590
    local.get $l2
    i32.load
    local.tee $l2
    i32.load offset=796
    local.get $l2
    i32.load offset=792
    call_indirect $__indirect_function_table (type $t2)
    local.get $p0
    i32.load offset=148
    i32.const 1
    i32.const 3773132
    i32.load
    call $f2903
    i32.const 3792608
    i32.load
    call $f34548
    local.tee $p0
    local.get $l4
    i32.const 8
    i32.add
    i32.const 0
    call $f56590
    local.get $p0
    i32.load
    local.tee $p0
    i32.load offset=796
    local.get $p0
    i32.load offset=792
    call_indirect $__indirect_function_table (type $t2)
    local.get $l4
    i32.const 16
    i32.add
    global.set $g0)
