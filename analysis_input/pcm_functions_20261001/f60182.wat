  (func $f60182 (type $t3) (param $p0 i32) (param $p1 i32) (param $p2 i32) (result i32)
    (local $l3 f32) (local $l4 f32) (local $l5 f32) (local $l6 f32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32)
    i32.const 4674507
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3752504
      call $f1661
      i32.const 4674507
      i32.const 1
      i32.store8
    end
    block $B1
      local.get $p1
      i32.load offset=8
      i32.const 0
      i32.le_s
      br_if $B1
      f32.const 0x1.01eb86p+1 (;=2.015;)
      local.set $l5
      loop $L2
        local.get $p1
        i32.load offset=28
        local.get $l7
        i32.const 3
        i32.shl
        i32.add
        f32.load offset=16
        local.set $l3
        i32.const 3752504
        i32.load
        local.tee $p2
        i32.load offset=116
        i32.eqz
        if $I3
          local.get $p2
          call $f65192
        end
        local.get $l7
        i32.const 1
        i32.shl
        local.set $p2
        block $B4
          block $B5
            local.get $l3
            f32.abs
            f32.const 0x1.0c6f7ap-20 (;=1e-06;)
            f32.gt
            if $I6
              local.get $p2
              i32.const 1
              i32.or
              local.set $l8
              br $B5
            end
            local.get $p1
            i32.load offset=28
            local.get $p2
            i32.const 1
            i32.or
            local.tee $l8
            i32.const 2
            i32.shl
            i32.add
            f32.load offset=16
            local.set $l3
            i32.const 3752504
            i32.load
            local.tee $l9
            i32.load offset=116
            i32.eqz
            if $I7
              local.get $l9
              call $f65192
            end
            local.get $l3
            f32.abs
            f32.const 0x1.0c6f7ap-20 (;=1e-06;)
            f32.gt
            i32.eqz
            br_if $B4
          end
          local.get $p1
          i32.load offset=28
          i32.const 16
          i32.add
          local.tee $l9
          local.get $l8
          i32.const 2
          i32.shl
          i32.add
          f32.load
          local.set $l3
          local.get $l9
          local.get $p2
          i32.const 2
          i32.shl
          i32.add
          f32.load
          local.set $l4
          i32.const 4671895
          i32.load8_u
          i32.eqz
          if $I8
            i32.const 3752504
            call $f1661
            i32.const 4671895
            i32.const 1
            i32.store8
          end
          i32.const 3752504
          i32.load
          local.tee $p2
          i32.load offset=116
          i32.eqz
          if $I9
            local.get $p2
            call $f65192
          end
          local.get $l4
          local.get $l4
          f32.mul
          local.get $l3
          local.get $l3
          f32.mul
          f32.add
          f32.sqrt
          local.tee $l3
          local.get $l5
          f32.le
          i32.eqz
          br_if $B4
          i32.const 4671895
          i32.load8_u
          i32.eqz
          if $I10
            i32.const 3752504
            call $f1661
            i32.const 4671895
            i32.const 1
            i32.store8
          end
          i32.const 3752504
          i32.load
          local.tee $p2
          i32.load offset=116
          i32.eqz
          if $I11
            local.get $p2
            call $f65192
          end
          local.get $l3
          local.set $l5
        end
        local.get $l7
        i32.const 2
        i32.add
        local.tee $l7
        local.get $p1
        i32.load offset=8
        local.tee $p2
        i32.lt_s
        br_if $L2
      end
      f32.const 0x1.01eb86p+1 (;=2.015;)
      local.set $l6
      local.get $p2
      i32.const 2
      i32.ge_s
      if $I12
        i32.const 1
        local.set $l7
        loop $L13
          local.get $p1
          i32.load offset=28
          local.get $l7
          i32.const 3
          i32.shl
          i32.add
          f32.load offset=16
          local.set $l3
          i32.const 3752504
          i32.load
          local.tee $p2
          i32.load offset=116
          i32.eqz
          if $I14
            local.get $p2
            call $f65192
          end
          local.get $l7
          i32.const 1
          i32.shl
          local.set $p2
          block $B15
            block $B16
              local.get $l3
              f32.abs
              f32.const 0x1.0c6f7ap-20 (;=1e-06;)
              f32.gt
              if $I17
                local.get $p2
                i32.const 1
                i32.or
                local.set $l8
                br $B16
              end
              local.get $p1
              i32.load offset=28
              local.get $p2
              i32.const 1
              i32.or
              local.tee $l8
              i32.const 2
              i32.shl
              i32.add
              f32.load offset=16
              local.set $l3
              i32.const 3752504
              i32.load
              local.tee $l9
              i32.load offset=116
              i32.eqz
              if $I18
                local.get $l9
                call $f65192
              end
              local.get $l3
              f32.abs
              f32.const 0x1.0c6f7ap-20 (;=1e-06;)
              f32.gt
              i32.eqz
              br_if $B15
            end
            local.get $p1
            i32.load offset=28
            i32.const 16
            i32.add
            local.tee $l9
            local.get $l8
            i32.const 2
            i32.shl
            i32.add
            f32.load
            local.set $l3
            local.get $l9
            local.get $p2
            i32.const 2
            i32.shl
            i32.add
            f32.load
            local.set $l4
            i32.const 4671895
            i32.load8_u
            i32.eqz
            if $I19
              i32.const 3752504
              call $f1661
              i32.const 4671895
              i32.const 1
              i32.store8
            end
            i32.const 3752504
            i32.load
            local.tee $p2
            i32.load offset=116
            i32.eqz
            if $I20
              local.get $p2
              call $f65192
            end
            local.get $l4
            local.get $l4
            f32.mul
            local.get $l3
            local.get $l3
            f32.mul
            f32.add
            f32.sqrt
            local.tee $l3
            local.get $l6
            f32.le
            i32.eqz
            br_if $B15
            i32.const 4671895
            i32.load8_u
            i32.eqz
            if $I21
              i32.const 3752504
              call $f1661
              i32.const 4671895
              i32.const 1
              i32.store8
            end
            i32.const 3752504
            i32.load
            local.tee $p2
            i32.load offset=116
            i32.eqz
            if $I22
              local.get $p2
              call $f65192
            end
            local.get $l3
            local.set $l6
          end
          local.get $l7
          i32.const 2
          i32.add
          local.tee $l7
          local.get $p1
          i32.load offset=8
          local.tee $p2
          i32.lt_s
          br_if $L13
        end
      end
      local.get $l5
      local.get $l6
      f32.lt
      if $I23
        local.get $p2
        i32.const 0
        i32.le_s
        if $I24
          i32.const 0
          local.set $l8
          br $B1
        end
        i32.const 0
        local.set $l8
        i32.const 0
        local.set $l7
        loop $L25
          local.get $p1
          i32.load offset=28
          local.get $l7
          i32.const 3
          i32.shl
          i32.add
          f32.load offset=16
          local.set $l3
          i32.const 3752504
          i32.load
          local.tee $p2
          i32.load offset=116
          i32.eqz
          if $I26
            local.get $p2
            call $f65192
          end
          local.get $l7
          i32.const 1
          i32.shl
          local.set $p2
          block $B27
            block $B28
              local.get $l3
              f32.abs
              f32.const 0x1.0c6f7ap-20 (;=1e-06;)
              f32.gt
              if $I29
                local.get $p2
                i32.const 1
                i32.or
                local.set $l9
                br $B28
              end
              local.get $p1
              i32.load offset=28
              local.get $p2
              i32.const 1
              i32.or
              local.tee $l9
              i32.const 2
              i32.shl
              i32.add
              f32.load offset=16
              local.set $l3
              i32.const 3752504
              i32.load
              local.tee $l10
              i32.load offset=116
              i32.eqz
              if $I30
                local.get $l10
                call $f65192
              end
              local.get $l3
              f32.abs
              f32.const 0x1.0c6f7ap-20 (;=1e-06;)
              f32.gt
              i32.eqz
              br_if $B27
            end
            local.get $p1
            i32.load offset=28
            i32.const 16
            i32.add
            local.tee $l10
            local.get $l9
            i32.const 2
            i32.shl
            i32.add
            f32.load
            local.set $l3
            local.get $l10
            local.get $p2
            i32.const 2
            i32.shl
            i32.add
            f32.load
            local.set $l4
            i32.const 4671895
            i32.load8_u
            i32.eqz
            if $I31
              i32.const 3752504
              call $f1661
              i32.const 4671895
              i32.const 1
              i32.store8
            end
            i32.const 3752504
            i32.load
            local.tee $p2
            i32.load offset=116
            i32.eqz
            if $I32
              local.get $p2
              call $f65192
            end
            local.get $l4
            local.get $l4
            f32.mul
            local.get $l3
            local.get $l3
            f32.mul
            f32.add
            f32.sqrt
            local.get $l6
            f32.lt
            i32.eqz
            br_if $B27
            local.get $l8
            i32.const 1
            i32.add
            local.set $l8
          end
          local.get $l7
          i32.const 2
          i32.add
          local.tee $l7
          local.get $p1
          i32.load offset=8
          i32.lt_s
          br_if $L25
        end
        br $B1
      end
      i32.const 0
      local.set $l8
      local.get $l5
      local.get $l6
      f32.gt
      i32.eqz
      br_if $B1
      local.get $p2
      i32.const 2
      i32.lt_s
      br_if $B1
      i32.const 1
      local.set $l7
      loop $L33
        local.get $p1
        i32.load offset=28
        local.get $l7
        i32.const 3
        i32.shl
        i32.add
        f32.load offset=16
        local.set $l3
        i32.const 3752504
        i32.load
        local.tee $p2
        i32.load offset=116
        i32.eqz
        if $I34
          local.get $p2
          call $f65192
        end
        local.get $l7
        i32.const 1
        i32.shl
        local.set $p2
        block $B35
          block $B36
            local.get $l3
            f32.abs
            f32.const 0x1.0c6f7ap-20 (;=1e-06;)
            f32.gt
            if $I37
              local.get $p2
              i32.const 1
              i32.or
              local.set $l9
              br $B36
            end
            local.get $p1
            i32.load offset=28
            local.get $p2
            i32.const 1
            i32.or
            local.tee $l9
            i32.const 2
            i32.shl
            i32.add
            f32.load offset=16
            local.set $l3
            i32.const 3752504
            i32.load
            local.tee $l10
            i32.load offset=116
            i32.eqz
            if $I38
              local.get $l10
              call $f65192
            end
            local.get $l3
            f32.abs
            f32.const 0x1.0c6f7ap-20 (;=1e-06;)
            f32.gt
            i32.eqz
            br_if $B35
          end
          local.get $p1
          i32.load offset=28
          i32.const 16
          i32.add
          local.tee $l10
          local.get $l9
          i32.const 2
          i32.shl
          i32.add
          f32.load
          local.set $l3
          local.get $l10
          local.get $p2
          i32.const 2
          i32.shl
          i32.add
          f32.load
          local.set $l4
          i32.const 4671895
          i32.load8_u
          i32.eqz
          if $I39
            i32.const 3752504
            call $f1661
            i32.const 4671895
            i32.const 1
            i32.store8
          end
          i32.const 3752504
          i32.load
          local.tee $p2
          i32.load offset=116
          i32.eqz
          if $I40
            local.get $p2
            call $f65192
          end
          local.get $l4
          local.get $l4
          f32.mul
          local.get $l3
          local.get $l3
          f32.mul
          f32.add
          f32.sqrt
          local.get $l5
          f32.lt
          i32.eqz
          br_if $B35
          local.get $l8
          i32.const 1
          i32.sub
          local.set $l8
        end
        local.get $l7
        i32.const 2
        i32.add
        local.tee $l7
        local.get $p1
        i32.load offset=8
        i32.lt_s
        br_if $L33
      end
    end
    i32.const 0
    local.get $l8
    i32.sub
    local.get $l8
    local.get $p0
    i32.load offset=128
    i32.const 1
    i32.eq
    select)
