  (func $f78677 (type $t5) (param $p0 i32) (result i32)
    (local $l1 i32) (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32)
    block $B0
      i32.const 4758664
      i32.load
      local.tee $l4
      local.get $p0
      i32.load
      local.tee $l7
      i32.const 16
      i32.shr_u
      local.get $l7
      i32.xor
      i32.const -2048144789
      i32.mul
      local.tee $l1
      i32.const 13
      i32.shr_u
      local.get $l1
      i32.xor
      i32.const -1028477387
      i32.mul
      local.tee $l1
      i32.const 16
      i32.shr_u
      local.get $l1
      i32.xor
      local.tee $l9
      i32.const 4758668
      i32.load
      local.tee $l2
      i32.and
      local.tee $l5
      i32.const 3
      i32.mul
      i32.add
      local.tee $l3
      i32.load
      local.tee $l8
      local.get $l9
      i32.const -4
      i32.and
      local.tee $l10
      i32.ne
      br_if $B0
      local.get $l7
      local.get $l3
      i32.load offset=4
      i32.ne
      br_if $B0
      local.get $l3
      i32.const 8
      i32.add
      return
    end
    block $B1
      i32.const 4758664
      block $B2 (result i32)
        block $B3
          block $B4
            local.get $l8
            i32.const -1
            i32.ne
            if $I5
              i32.const 4
              local.set $l1
              local.get $l5
              local.set $l6
              loop $L6
                local.get $l10
                local.get $l4
                local.get $l1
                local.get $l6
                i32.add
                local.get $l2
                i32.and
                local.tee $l6
                i32.const 3
                i32.mul
                i32.add
                local.tee $l11
                i32.load
                local.tee $l12
                i32.eq
                if $I7
                  local.get $l7
                  local.get $l11
                  i32.load offset=4
                  i32.eq
                  br_if $B4
                end
                local.get $l1
                i32.const 4
                i32.add
                local.set $l1
                local.get $l12
                i32.const -1
                i32.ne
                br_if $L6
              end
            end
            i32.const 4758676
            i32.load
            br_if $B1
            local.get $l2
            i32.const 1
            i32.shr_u
            i32.const 2147483646
            i32.and
            i32.const 2
            i32.add
            i32.const 3
            i32.div_u
            local.tee $l1
            i32.const 4758672
            i32.load
            i32.const 1
            i32.shl
            local.tee $l4
            i32.gt_u
            br_if $B3
            local.get $l2
            i32.const 1
            i32.shl
            i32.const 4
            i32.add
            i32.const 252
            local.get $l2
            select
            br $B2
          end
          local.get $l11
          i32.const 8
          i32.add
          return
        end
        local.get $l2
        i32.const 252
        local.get $l2
        i32.const 252
        i32.gt_u
        select
        local.get $l4
        local.get $l1
        i32.const 1
        i32.shr_u
        i32.gt_u
        br_if $B2
        drop
        local.get $l2
        i32.const 4
        i32.sub
        i32.const 1
        i32.shr_u
        local.tee $l1
        i32.const 252
        local.get $l1
        i32.const 252
        i32.gt_u
        select
      end
      call $f66250
      i32.const 4758664
      i32.load
      local.tee $l4
      i32.const 4758668
      i32.load
      local.tee $l2
      local.get $l9
      i32.and
      local.tee $l5
      i32.const 3
      i32.mul
      i32.add
      local.tee $l3
      i32.load
      local.set $l8
    end
    local.get $l8
    i32.const -2
    i32.lt_u
    if $I8
      i32.const 4
      local.set $l1
      loop $L9
        local.get $l1
        local.get $l5
        i32.add
        local.set $l6
        local.get $l1
        i32.const 4
        i32.add
        local.set $l1
        local.get $l4
        local.get $l2
        local.get $l6
        i32.and
        local.tee $l5
        i32.const 3
        i32.mul
        i32.add
        local.tee $l3
        i32.load
        i32.const -2
        i32.lt_u
        br_if $L9
      end
    end
    i32.const 4758672
    i32.const 4758672
    i32.load
    i32.const 1
    i32.add
    i32.store
    local.get $l3
    i32.load
    i32.const -1
    i32.eq
    if $I10
      i32.const 4758676
      i32.const 4758676
      i32.load
      i32.const 1
      i32.sub
      i32.store
    end
    local.get $l3
    local.get $l10
    i32.store
    local.get $p0
    i32.load
    local.set $l1
    local.get $l3
    i32.const 127
    i32.store8 offset=8
    local.get $l3
    local.get $l1
    i32.store offset=4
    local.get $l3
    i32.const 8
    i32.add)
