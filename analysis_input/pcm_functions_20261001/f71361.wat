  (func $f71361 (type $t5) (param $p0 i32) (result i32)
    (local $l1 i32) (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32)
    block $B0
      block $B1
        block $B2
          block $B3
            block $B4
              block $B5
                local.get $p0
                i32.load8_u offset=20
                br_table $B5 $B4 $B0 $B0 $B3 $B2 $B0
              end
              local.get $p0
              i32.const 4
              i32.sub
              i32.const 0
              call $f71627
              return
            end
            block $B6
              local.get $p0
              i32.load8_u offset=52
              i32.const 32
              i32.and
              br_if $B6
              block $B7
                local.get $p0
                i32.load offset=24
                i32.load offset=4
                local.tee $l1
                i32.load offset=44
                i32.load8_u offset=9
                i32.const 1
                i32.sub
                i32.const 1
                i32.gt_u
                br_if $B7
                local.get $l1
                i32.eqz
                br_if $B7
                local.get $l1
                i32.load offset=156
                i32.const -2
                i32.lt_u
                br_if $B6
              end
              local.get $p0
              i32.load offset=28
              i32.load offset=4
              local.tee $l1
              i32.load offset=44
              i32.load8_u offset=9
              i32.const 1
              i32.sub
              i32.const 1
              i32.gt_u
              br_if $B0
              local.get $l1
              i32.eqz
              br_if $B0
              local.get $l1
              i32.load offset=156
              i32.const -3
              i32.gt_u
              br_if $B0
            end
            local.get $p0
            local.get $p0
            i32.load8_u offset=21
            i32.const 32
            i32.or
            i32.store8 offset=21
            br $B1
          end
          local.get $p0
          i32.load offset=24
          local.tee $l3
          i32.const -64
          i32.sub
          i32.load
          local.set $l1
          i32.const 1
          local.set $l4
          i32.const 1
          local.set $l5
          local.get $l3
          i32.load offset=60
          local.tee $l2
          if $I8
            local.get $l2
            i32.load offset=156
            i32.const -2
            i32.lt_u
            local.set $l5
          end
          local.get $l1
          if $I9
            local.get $l1
            i32.load offset=156
            i32.const -2
            i32.lt_u
            local.set $l4
          end
          local.get $l2
          if $I10 (result i32)
            local.get $l2
            i32.load offset=44
            i32.load8_u offset=44
            i32.const 1
            i32.and
          else
            i32.const 1
          end
          i32.eqz
          local.set $l2
          local.get $l1
          if $I11
            local.get $l2
            local.get $l1
            i32.load offset=44
            i32.load8_u offset=44
            i32.const 1
            i32.and
            i32.eqz
            i32.or
            local.set $l2
          end
          i32.const 0
          local.set $l1
          block $B12
            local.get $l4
            local.get $l5
            i32.or
            i32.eqz
            br_if $B12
            local.get $l2
            i32.eqz
            br_if $B12
            local.get $p0
            local.get $p0
            i32.load8_u offset=21
            i32.const 32
            i32.or
            i32.store8 offset=21
            i32.const 1
            local.set $l1
            local.get $l3
            i32.load8_u offset=68
            i32.const 6
            i32.and
            i32.const 2
            i32.ne
            br_if $B12
            local.get $p0
            i32.load
            i32.load offset=40
            local.get $l3
            call $f71410
          end
          local.get $l1
          return
        end
        local.get $p0
        i32.load
        i32.load offset=156
        i32.const -3
        i32.gt_u
        br_if $B0
        local.get $p0
        i32.load offset=4
        i32.load offset=156
        i32.const -3
        i32.gt_u
        br_if $B0
        local.get $p0
        local.get $p0
        i32.load8_u offset=21
        i32.const 32
        i32.or
        i32.store8 offset=21
      end
      i32.const 1
      local.set $l2
    end
    local.get $l2)