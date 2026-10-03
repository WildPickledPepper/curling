  (func $f78662 (type $t0) (param $p0 i32) (param $p1 i32) (result i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32)
    i32.const 4742356
    i32.load
    local.tee $l3
    i32.eqz
    if $I0
      i32.const -1
      return
    end
    local.get $l3
    i32.load offset=124
    local.tee $l5
    if $I1
      block $B2
        local.get $l3
        i32.load offset=116
        local.set $l6
        loop $L3
          block $B4
            local.get $l6
            local.get $l2
            i32.const 3
            i32.shl
            i32.add
            local.tee $l4
            i32.load
            local.get $p0
            i32.ne
            br_if $B4
            local.get $l4
            i32.load offset=4
            local.get $p1
            i32.ne
            br_if $B4
            local.get $l4
            local.get $l4
            i32.const 8
            i32.add
            local.tee $l2
            local.get $l6
            local.get $l5
            i32.const 3
            i32.shl
            i32.add
            local.get $l2
            i32.sub
            call $f547
            drop
            local.get $l3
            local.get $l3
            i32.load offset=124
            i32.const 1
            i32.sub
            i32.store offset=124
            br $B2
          end
          local.get $l2
          i32.const 1
          i32.add
          local.tee $l2
          local.get $l5
          i32.ne
          br_if $L3
        end
      end
    end
    i32.const 0)
