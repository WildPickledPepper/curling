  (func $f71769 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32)
    local.get $p0
    i32.load offset=52
    local.tee $l8
    if $I0
      local.get $p0
      i32.load offset=60
      local.tee $l2
      i32.const 1
      i32.add
      local.tee $l3
      local.get $l2
      i32.ge_u
      if $I1
        local.get $p0
        i32.load offset=8
        local.set $l5
        local.get $p0
        i32.load
        local.set $l9
        loop $L2
          local.get $l8
          local.get $l2
          local.tee $l6
          i32.const 2
          i32.shl
          i32.add
          local.tee $l10
          i32.load
          local.tee $l11
          if $I3
            local.get $l3
            i32.const 5
            i32.shl
            local.set $l4
            i32.const -2147483648
            local.set $l2
            i32.const 31
            local.set $l7
            loop $L4
              local.get $l7
              local.set $l3
              local.get $l4
              i32.const 1
              i32.sub
              local.set $l4
              local.get $l2
              local.get $l11
              i32.and
              if $I5
                local.get $l5
                local.get $l4
                i32.const 28
                i32.mul
                i32.add
                local.get $p1
                local.get $l9
                local.get $l5
                call $f71759
              end
              local.get $l3
              i32.const 1
              i32.sub
              local.set $l7
              local.get $l2
              i32.const 1
              i32.shr_u
              local.set $l2
              local.get $l3
              br_if $L4
            end
            local.get $l10
            i32.const 0
            i32.store
          end
          local.get $l6
          i32.const 1
          i32.sub
          local.set $l2
          local.get $l6
          local.tee $l3
          br_if $L2
        end
      end
      local.get $p0
      i32.const 0
      i32.store offset=60
    end)