  (func $f71745 (type $t10) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (result i32)
    (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32)
    local.get $p4
    i32.eqz
    if $I0
      i32.const 1
      return
    end
    block $B1
      local.get $p5
      if $I2
        local.get $p0
        i32.load offset=4
        br_if $B1
      end
      local.get $p0
      i32.const 1
      i32.store8 offset=337
    end
    local.get $p0
    i32.const 284
    i32.add
    local.get $p1
    local.get $p2
    local.get $p3
    local.get $p4
    call $f71886
    local.set $p2
    block $B3
      local.get $p0
      i32.load8_u offset=336
      i32.eqz
      br_if $B3
      local.get $p0
      i32.load offset=4
      i32.eqz
      br_if $B3
      local.get $p0
      i32.const 1
      i32.store8 offset=338
      local.get $p5
      br_if $B3
      local.get $p2
      i32.eqz
      br_if $B3
      local.get $p0
      i32.const 56
      i32.add
      local.set $p3
      i32.const 0
      local.set $p5
      loop $L4
        local.get $p0
        i32.load offset=300
        local.get $p1
        local.get $p5
        i32.const 2
        i32.shl
        i32.add
        i32.load
        i32.const 2
        i32.shl
        i32.add
        i32.load
        local.set $l8
        local.get $p0
        i32.load offset=48
        local.set $l10
        block $B5
          block $B6
            local.get $p3
            local.get $p3
            i32.load
            local.tee $l9
            i32.const 48
            i32.mul
            i32.add
            i32.const 12
            i32.add
            local.tee $l11
            i32.load
            local.tee $l6
            if $I7
              local.get $l6
              i32.load offset=588
              i32.eqz
              br_if $B6
              br $B5
            end
            call $f69753
            local.tee $l6
            i32.const 616
            i32.const 3179164
            i32.const 3178240
            i32.const 4700888
            i32.load
            local.tee $l7
            local.get $l7
            i32.load
            i32.load offset=20
            call_indirect $__indirect_function_table (type $t5)
            select
            i32.const 3177865
            i32.const 88
            local.get $l6
            i32.load
            i32.load offset=8
            call_indirect $__indirect_function_table (type $t9)
            local.tee $l7
            call $f71813
            local.set $l6
            local.get $l11
            local.get $l7
            i32.store
          end
          local.get $p3
          local.get $l9
          i32.const 48
          i32.mul
          i32.add
          local.get $l10
          i32.store offset=8
        end
        local.get $p3
        i32.const 0
        i32.store offset=112
        local.get $p3
        local.get $p3
        local.get $l9
        i32.const 48
        i32.mul
        i32.add
        i32.const 16
        i32.add
        local.get $l8
        local.get $l6
        local.get $l8
        local.get $p3
        i32.load offset=104
        i32.load offset=8
        local.get $p3
        i32.const 108
        i32.add
        call $f71796
        call $f71865
        local.get $p5
        i32.const 1
        i32.add
        local.tee $p5
        local.get $p2
        i32.ne
        br_if $L4
      end
    end
    local.get $p2
    local.get $p4
    i32.eq)