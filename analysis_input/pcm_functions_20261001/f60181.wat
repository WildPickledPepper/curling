  (func $f60181 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32)
    global.get $g0
    i32.const 80
    i32.sub
    local.tee $l4
    global.set $g0
    i32.const 4674506
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3748808
      call $f1661
      i32.const 3773132
      call $f1661
      i32.const 3752504
      call $f1661
      i32.const 3745900
      call $f1661
      i32.const 3821172
      call $f1661
      i32.const 3836224
      call $f1661
      i32.const 3836216
      call $f1661
      i32.const 4674506
      i32.const 1
      i32.store8
    end
    local.get $p0
    i32.const 200
    i32.add
    local.set $l7
    loop $L1
      block $B2
        local.get $p0
        i32.load offset=128
        i32.eqz
        if $I3
          local.get $p0
          i32.load offset=192
          local.get $l2
          i32.const 3773132
          i32.load
          call $f2903
          i32.const 0
          call $f54404
          local.set $p1
          local.get $p0
          i32.load offset=96
          i32.load offset=28
          local.set $l3
          block $B4
            local.get $p1
            if $I5
              local.get $p0
              f32.load offset=232
              local.set $l9
              i32.const 0
              local.set $p1
              local.get $l4
              i32.const -64
              i32.sub
              local.get $p0
              i32.load offset=192
              local.get $l2
              i32.const 3773132
              i32.load
              call $f2903
              i32.const 0
              call $f54401
              i32.const 0
              call $f54624
              local.get $l3
              local.get $l2
              i32.const 4
              i32.shl
              local.tee $l5
              i32.add
              local.get $l9
              local.get $l4
              f32.load offset=72
              f32.sub
              f32.store offset=16
              local.get $p0
              f32.load offset=224
              local.set $l9
              local.get $p0
              i32.load offset=96
              i32.load offset=28
              local.set $l3
              local.get $l4
              i32.const -64
              i32.sub
              local.get $p0
              i32.load offset=192
              local.get $l2
              i32.const 3773132
              i32.load
              call $f2903
              i32.const 0
              call $f54401
              i32.const 0
              call $f54624
              local.get $l3
              local.get $l2
              i32.const 2
              i32.shl
              local.tee $l8
              i32.const 1
              i32.or
              i32.const 2
              i32.shl
              local.tee $l6
              i32.add
              local.get $l9
              local.get $l4
              f32.load offset=64
              f32.sub
              f32.store offset=16
              local.get $p0
              i32.load offset=96
              i32.load offset=28
              i32.const 16
              i32.add
              local.tee $l3
              local.get $l5
              i32.add
              f32.load
              local.tee $l9
              f32.const -0x1.1d70a4p+1 (;=-2.23;)
              f32.gt
              if $I6
                local.get $l3
                local.get $l6
                i32.add
                f32.load
                local.tee $l10
                f32.const -0x1.01eb86p+1 (;=-2.015;)
                f32.gt
                i32.const 1
                i32.shl
                i32.const 0
                local.get $l9
                f32.const 0x1.1d70a4p+1 (;=2.23;)
                f32.lt
                select
                i32.const 0
                local.get $l10
                f32.const 0x1.6947aep+2 (;=5.645;)
                f32.lt
                select
                local.set $p1
              end
              i32.const 4671895
              i32.load8_u
              i32.eqz
              if $I7
                i32.const 3752504
                call $f1661
                i32.const 4671895
                i32.const 1
                i32.store8
              end
              i32.const 3752504
              i32.load
              local.tee $l3
              i32.load offset=116
              i32.eqz
              if $I8
                local.get $l3
                call $f65192
              end
              local.get $p1
              br_if $B4
              local.get $p0
              i32.load offset=96
              i32.load offset=28
              i32.const 16
              i32.add
              local.tee $p1
              local.get $l8
              i32.const 2
              i32.shl
              i32.add
              i32.const 0
              i32.store
              local.get $p1
              local.get $l6
              i32.add
              i32.const 0
              i32.store
              local.get $p0
              i32.load offset=192
              local.get $l2
              i32.const 3773132
              i32.load
              call $f2903
              i32.const 0
              call $f54401
              local.set $p1
              local.get $l4
              local.get $l7
              i32.load offset=8
              i32.store offset=24
              local.get $l4
              local.get $l7
              i64.load align=4
              i64.store offset=16
              local.get $p1
              local.get $l4
              i32.const 16
              i32.add
              i32.const 0
              call $f54626
              local.get $p0
              i32.load offset=192
              local.get $l2
              i32.const 3773132
              i32.load
              call $f2903
              i32.const 0
              i32.const 0
              call $f54405
              br $B4
            end
            local.get $l3
            local.get $l2
            i32.const 4
            i32.shl
            i32.add
            i64.const 0
            i64.store offset=16 align=4
          end
          local.get $p0
          i32.load offset=196
          local.get $l2
          i32.const 3773132
          i32.load
          call $f2903
          i32.const 0
          call $f54404
          local.set $p1
          local.get $p0
          i32.load offset=96
          i32.load offset=28
          local.set $l3
          local.get $p1
          if $I9
            local.get $p0
            f32.load offset=232
            local.set $l9
            i32.const 0
            local.set $p1
            local.get $l4
            i32.const -64
            i32.sub
            local.get $p0
            i32.load offset=196
            local.get $l2
            i32.const 3773132
            i32.load
            call $f2903
            i32.const 0
            call $f54401
            i32.const 0
            call $f54624
            local.get $l3
            local.get $l2
            i32.const 2
            i32.shl
            local.tee $l6
            i32.const 2
            i32.or
            i32.const 2
            i32.shl
            local.tee $l5
            i32.add
            local.get $l9
            local.get $l4
            f32.load offset=72
            f32.sub
            f32.store offset=16
            local.get $p0
            f32.load offset=224
            local.set $l9
            local.get $p0
            i32.load offset=96
            i32.load offset=28
            local.set $l3
            local.get $l4
            i32.const -64
            i32.sub
            local.get $p0
            i32.load offset=196
            local.get $l2
            i32.const 3773132
            i32.load
            call $f2903
            i32.const 0
            call $f54401
            i32.const 0
            call $f54624
            local.get $l3
            local.get $l6
            i32.const 3
            i32.or
            i32.const 2
            i32.shl
            local.tee $l6
            i32.add
            local.get $l9
            local.get $l4
            f32.load offset=64
            f32.sub
            f32.store offset=16
            local.get $p0
            i32.load offset=96
            i32.load offset=28
            i32.const 16
            i32.add
            local.tee $l3
            local.get $l5
            i32.add
            f32.load
            local.tee $l9
            f32.const -0x1.1d70a4p+1 (;=-2.23;)
            f32.gt
            if $I10
              local.get $l3
              local.get $l6
              i32.add
              f32.load
              local.tee $l10
              f32.const -0x1.01eb86p+1 (;=-2.015;)
              f32.gt
              i32.const 1
              i32.shl
              i32.const 0
              local.get $l9
              f32.const 0x1.1d70a4p+1 (;=2.23;)
              f32.lt
              select
              i32.const 0
              local.get $l10
              f32.const 0x1.6947aep+2 (;=5.645;)
              f32.lt
              select
              local.set $p1
            end
            i32.const 4671895
            i32.load8_u
            i32.eqz
            if $I11
              i32.const 3752504
              call $f1661
              i32.const 4671895
              i32.const 1
              i32.store8
            end
            i32.const 3752504
            i32.load
            local.tee $l3
            i32.load offset=116
            i32.eqz
            if $I12
              local.get $l3
              call $f65192
            end
            local.get $p1
            br_if $B2
            local.get $p0
            i32.load offset=96
            i32.load offset=28
            i32.const 16
            i32.add
            local.tee $p1
            local.get $l5
            i32.add
            i32.const 0
            i32.store
            local.get $p1
            local.get $l6
            i32.add
            i32.const 0
            i32.store
            local.get $p0
            i32.load offset=196
            local.get $l2
            i32.const 3773132
            i32.load
            call $f2903
            i32.const 0
            call $f54401
            local.set $p1
            local.get $l4
            local.get $l7
            i32.load offset=8
            i32.store offset=8
            local.get $l4
            local.get $l7
            i64.load align=4
            i64.store
            local.get $p1
            local.get $l4
            i32.const 0
            call $f54626
            local.get $p0
            i32.load offset=196
            local.get $l2
            i32.const 3773132
            i32.load
            call $f2903
            i32.const 0
            i32.const 0
            call $f54405
            br $B2
          end
          local.get $l3
          local.get $l2
          i32.const 4
          i32.shl
          i32.add
          i64.const 0
          i64.store offset=24 align=4
          br $B2
        end
        local.get $p0
        i32.load offset=196
        local.get $l2
        i32.const 3773132
        i32.load
        call $f2903
        i32.const 0
        call $f54404
        local.set $p1
        local.get $p0
        i32.load offset=96
        i32.load offset=28
        local.set $l3
        block $B13
          local.get $p1
          if $I14
            local.get $p0
            f32.load offset=232
            local.set $l9
            i32.const 0
            local.set $p1
            local.get $l4
            i32.const -64
            i32.sub
            local.get $p0
            i32.load offset=196
            local.get $l2
            i32.const 3773132
            i32.load
            call $f2903
            i32.const 0
            call $f54401
            i32.const 0
            call $f54624
            local.get $l3
            local.get $l2
            i32.const 4
            i32.shl
            local.tee $l5
            i32.add
            local.get $l9
            local.get $l4
            f32.load offset=72
            f32.sub
            f32.store offset=16
            local.get $p0
            f32.load offset=224
            local.set $l9
            local.get $p0
            i32.load offset=96
            i32.load offset=28
            local.set $l3
            local.get $l4
            i32.const -64
            i32.sub
            local.get $p0
            i32.load offset=196
            local.get $l2
            i32.const 3773132
            i32.load
            call $f2903
            i32.const 0
            call $f54401
            i32.const 0
            call $f54624
            local.get $l3
            local.get $l2
            i32.const 2
            i32.shl
            local.tee $l8
            i32.const 1
            i32.or
            i32.const 2
            i32.shl
            local.tee $l6
            i32.add
            local.get $l9
            local.get $l4
            f32.load offset=64
            f32.sub
            f32.store offset=16
            local.get $p0
            i32.load offset=96
            i32.load offset=28
            i32.const 16
            i32.add
            local.tee $l3
            local.get $l5
            i32.add
            f32.load
            local.tee $l9
            f32.const -0x1.1d70a4p+1 (;=-2.23;)
            f32.gt
            if $I15
              local.get $l3
              local.get $l6
              i32.add
              f32.load
              local.tee $l10
              f32.const -0x1.01eb86p+1 (;=-2.015;)
              f32.gt
              i32.const 1
              i32.shl
              i32.const 0
              local.get $l9
              f32.const 0x1.1d70a4p+1 (;=2.23;)
              f32.lt
              select
              i32.const 0
              local.get $l10
              f32.const 0x1.6947aep+2 (;=5.645;)
              f32.lt
              select
              local.set $p1
            end
            i32.const 4671895
            i32.load8_u
            i32.eqz
            if $I16
              i32.const 3752504
              call $f1661
              i32.const 4671895
              i32.const 1
              i32.store8
            end
            i32.const 3752504
            i32.load
            local.tee $l3
            i32.load offset=116
            i32.eqz
            if $I17
              local.get $l3
              call $f65192
            end
            local.get $p1
            br_if $B13
            local.get $p0
            i32.load offset=96
            i32.load offset=28
            i32.const 16
            i32.add
            local.tee $p1
            local.get $l8
            i32.const 2
            i32.shl
            i32.add
            i32.const 0
            i32.store
            local.get $p1
            local.get $l6
            i32.add
            i32.const 0
            i32.store
            local.get $p0
            i32.load offset=196
            local.get $l2
            i32.const 3773132
            i32.load
            call $f2903
            i32.const 0
            call $f54401
            local.set $p1
            local.get $l4
            local.get $l7
            i32.load offset=8
            i32.store offset=56
            local.get $l4
            local.get $l7
            i64.load align=4
            i64.store offset=48
            local.get $p1
            local.get $l4
            i32.const 48
            i32.add
            i32.const 0
            call $f54626
            local.get $p0
            i32.load offset=196
            local.get $l2
            i32.const 3773132
            i32.load
            call $f2903
            i32.const 0
            i32.const 0
            call $f54405
            br $B13
          end
          local.get $l3
          local.get $l2
          i32.const 4
          i32.shl
          i32.add
          i64.const 0
          i64.store offset=16 align=4
        end
        local.get $p0
        i32.load offset=192
        local.get $l2
        i32.const 3773132
        i32.load
        call $f2903
        i32.const 0
        call $f54404
        local.set $p1
        local.get $p0
        i32.load offset=96
        i32.load offset=28
        local.set $l3
        local.get $p1
        if $I18
          local.get $p0
          f32.load offset=232
          local.set $l9
          i32.const 0
          local.set $p1
          local.get $l4
          i32.const -64
          i32.sub
          local.get $p0
          i32.load offset=192
          local.get $l2
          i32.const 3773132
          i32.load
          call $f2903
          i32.const 0
          call $f54401
          i32.const 0
          call $f54624
          local.get $l3
          local.get $l2
          i32.const 2
          i32.shl
          local.tee $l6
          i32.const 2
          i32.or
          i32.const 2
          i32.shl
          local.tee $l5
          i32.add
          local.get $l9
          local.get $l4
          f32.load offset=72
          f32.sub
          f32.store offset=16
          local.get $p0
          f32.load offset=224
          local.set $l9
          local.get $p0
          i32.load offset=96
          i32.load offset=28
          local.set $l3
          local.get $l4
          i32.const -64
          i32.sub
          local.get $p0
          i32.load offset=192
          local.get $l2
          i32.const 3773132
          i32.load
          call $f2903
          i32.const 0
          call $f54401
          i32.const 0
          call $f54624
          local.get $l3
          local.get $l6
          i32.const 3
          i32.or
          i32.const 2
          i32.shl
          local.tee $l6
          i32.add
          local.get $l9
          local.get $l4
          f32.load offset=64
          f32.sub
          f32.store offset=16
          local.get $p0
          i32.load offset=96
          i32.load offset=28
          i32.const 16
          i32.add
          local.tee $l3
          local.get $l5
          i32.add
          f32.load
          local.tee $l9
          f32.const -0x1.1d70a4p+1 (;=-2.23;)
          f32.gt
          if $I19
            local.get $l3
            local.get $l6
            i32.add
            f32.load
            local.tee $l10
            f32.const -0x1.01eb86p+1 (;=-2.015;)
            f32.gt
            i32.const 1
            i32.shl
            i32.const 0
            local.get $l9
            f32.const 0x1.1d70a4p+1 (;=2.23;)
            f32.lt
            select
            i32.const 0
            local.get $l10
            f32.const 0x1.6947aep+2 (;=5.645;)
            f32.lt
            select
            local.set $p1
          end
          i32.const 4671895
          i32.load8_u
          i32.eqz
          if $I20
            i32.const 3752504
            call $f1661
            i32.const 4671895
            i32.const 1
            i32.store8
          end
          i32.const 3752504
          i32.load
          local.tee $l3
          i32.load offset=116
          i32.eqz
          if $I21
            local.get $l3
            call $f65192
          end
          local.get $p1
          br_if $B2
          local.get $p0
          i32.load offset=96
          i32.load offset=28
          i32.const 16
          i32.add
          local.tee $p1
          local.get $l5
          i32.add
          i32.const 0
          i32.store
          local.get $p1
          local.get $l6
          i32.add
          i32.const 0
          i32.store
          local.get $p0
          i32.load offset=192
          local.get $l2
          i32.const 3773132
          i32.load
          call $f2903
          i32.const 0
          call $f54401
          local.set $p1
          local.get $l4
          local.get $l7
          i32.load offset=8
          i32.store offset=40
          local.get $l4
          local.get $l7
          i64.load align=4
          i64.store offset=32
          local.get $p1
          local.get $l4
          i32.const 32
          i32.add
          i32.const 0
          call $f54626
          local.get $p0
          i32.load offset=192
          local.get $l2
          i32.const 3773132
          i32.load
          call $f2903
          i32.const 0
          i32.const 0
          call $f54405
          br $B2
        end
        local.get $l3
        local.get $l2
        i32.const 4
        i32.shl
        i32.add
        i64.const 0
        i64.store offset=24 align=4
      end
      local.get $l2
      i32.const 1
      i32.add
      local.tee $l2
      i32.const 8
      i32.ne
      br_if $L1
    end
    block $B22
      block $B23
        block $B24
          block $B25
            block $B26
              local.get $p0
              i32.load offset=96
              i32.load offset=8
              local.tee $p1
              i32.const 5
              i32.sub
              i32.const -3
              i32.lt_u
              br_if $B26
              local.get $p1
              i32.const 1
              i32.and
              local.tee $l2
              local.get $p1
              i32.const 1
              i32.sub
              i32.ge_u
              br_if $B26
              local.get $p0
              i32.const 100
              i32.add
              local.set $l7
              loop $L27
                local.get $l7
                i32.load
                i32.const 16
                i32.add
                local.tee $p1
                local.get $l2
                i32.const 3
                i32.shl
                i32.add
                f32.load
                local.set $l10
                local.get $p1
                local.get $l2
                i32.const 1
                i32.shl
                local.tee $l5
                i32.const 1
                i32.or
                i32.const 2
                i32.shl
                local.tee $l3
                i32.add
                f32.load
                local.set $l9
                i32.const 4671895
                i32.load8_u
                i32.eqz
                if $I28
                  i32.const 3752504
                  call $f1661
                  i32.const 4671895
                  i32.const 1
                  i32.store8
                end
                i32.const 3752504
                i32.load
                local.tee $p1
                i32.load offset=116
                i32.eqz
                if $I29
                  local.get $p1
                  call $f65192
                end
                block $B30
                  local.get $l9
                  f32.const 0x1.6947aep+2 (;=5.645;)
                  f32.lt
                  i32.eqz
                  br_if $B30
                  local.get $l9
                  f32.const 0x1.28f5c2p-3 (;=0.145;)
                  f32.gt
                  i32.eqz
                  br_if $B30
                  local.get $l10
                  f32.const 0x1.1d70a4p+1 (;=2.23;)
                  f32.lt
                  i32.eqz
                  br_if $B30
                  local.get $l10
                  f32.const -0x1.1d70a4p+1 (;=-2.23;)
                  f32.gt
                  i32.eqz
                  br_if $B30
                  local.get $l10
                  local.get $l10
                  f32.mul
                  local.get $l9
                  local.get $l9
                  f32.mul
                  f32.add
                  f32.sqrt
                  f32.const 0x1.01eb86p+1 (;=2.015;)
                  f32.lt
                  br_if $B30
                  local.get $l5
                  i32.const 2
                  i32.shl
                  local.tee $p1
                  local.get $p0
                  i32.load offset=96
                  i32.load offset=28
                  i32.add
                  f32.load offset=16
                  local.set $l9
                  i32.const 3752504
                  i32.load
                  local.tee $l5
                  i32.load offset=116
                  i32.eqz
                  if $I31
                    local.get $l5
                    call $f65192
                  end
                  block $B32
                    local.get $l9
                    f32.abs
                    f32.const 0x1.0c6f7ap-20 (;=1e-06;)
                    f32.lt
                    i32.eqz
                    br_if $B32
                    local.get $p0
                    i32.load offset=96
                    i32.load offset=28
                    local.get $l3
                    i32.add
                    f32.load offset=16
                    local.set $l9
                    i32.const 3752504
                    i32.load
                    local.tee $l5
                    i32.load offset=116
                    i32.eqz
                    if $I33
                      local.get $l5
                      call $f65192
                    end
                    local.get $l9
                    f32.abs
                    f32.const 0x1.0c6f7ap-20 (;=1e-06;)
                    f32.lt
                    i32.eqz
                    br_if $B32
                    local.get $p0
                    i32.const 1
                    i32.store8 offset=56
                    local.get $p0
                    i32.load offset=96
                    local.set $p1
                    local.get $p0
                    i32.load offset=100
                    call $f1448
                    local.tee $l2
                    i32.eqz
                    if $I34
                      local.get $p1
                      i32.const 0
                      i32.store offset=28
                      local.get $p0
                      local.get $l7
                      local.get $p0
                      call $f60176
                      br $B26
                    end
                    local.get $l2
                    i32.const 3745900
                    i32.load
                    local.tee $l5
                    call $f1674
                    local.tee $l3
                    i32.eqz
                    br_if $B25
                    local.get $p1
                    local.get $l3
                    i32.store offset=28
                    local.get $l2
                    i32.const 3745900
                    i32.load
                    local.tee $p1
                    call $f1674
                    i32.eqz
                    br_if $B24
                    local.get $p0
                    local.get $l7
                    local.get $p0
                    call $f60176
                    br $B26
                  end
                  local.get $l7
                  i32.load
                  local.get $p1
                  i32.add
                  f32.load offset=16
                  local.set $l9
                  i32.const 4674503
                  i32.load8_u
                  i32.eqz
                  if $I35
                    i32.const 3752504
                    call $f1661
                    i32.const 4674503
                    i32.const 1
                    i32.store8
                  end
                  i32.const 3752504
                  i32.load
                  local.tee $l5
                  i32.load offset=116
                  i32.eqz
                  if $I36
                    local.get $l5
                    call $f65192
                  end
                  local.get $l9
                  f32.abs
                  f32.const 0x1.28f5c2p-3 (;=0.145;)
                  f32.le
                  i32.eqz
                  br_if $B30
                  local.get $p0
                  i32.load offset=96
                  i32.load offset=28
                  i32.const 16
                  i32.add
                  local.tee $l5
                  local.get $l3
                  i32.add
                  f32.load
                  local.set $l9
                  local.get $p1
                  local.get $l5
                  i32.add
                  f32.load
                  local.set $l10
                  i32.const 4671895
                  i32.load8_u
                  i32.eqz
                  if $I37
                    i32.const 3752504
                    call $f1661
                    i32.const 4671895
                    i32.const 1
                    i32.store8
                  end
                  i32.const 3752504
                  i32.load
                  local.tee $l5
                  i32.load offset=116
                  i32.eqz
                  if $I38
                    local.get $l5
                    call $f65192
                  end
                  i32.const 0
                  local.set $l5
                  local.get $p0
                  i32.load offset=96
                  i32.load offset=28
                  i32.const 16
                  i32.add
                  local.tee $l6
                  local.get $p1
                  i32.add
                  f32.load
                  local.tee $l11
                  f32.const -0x1.1d70a4p+1 (;=-2.23;)
                  f32.gt
                  if $I39
                    local.get $l3
                    local.get $l6
                    i32.add
                    f32.load
                    local.tee $l12
                    f32.const -0x1.01eb86p+1 (;=-2.015;)
                    f32.gt
                    i32.const 1
                    i32.shl
                    i32.const 0
                    local.get $l11
                    f32.const 0x1.1d70a4p+1 (;=2.23;)
                    f32.lt
                    select
                    i32.const 0
                    local.get $l12
                    f32.const 0x1.6947aep+2 (;=5.645;)
                    f32.lt
                    select
                    local.set $l5
                  end
                  i32.const 4671895
                  i32.load8_u
                  i32.eqz
                  if $I40
                    i32.const 3752504
                    call $f1661
                    i32.const 4671895
                    i32.const 1
                    i32.store8
                  end
                  i32.const 3752504
                  i32.load
                  local.tee $l3
                  i32.load offset=116
                  i32.eqz
                  if $I41
                    local.get $l3
                    call $f65192
                  end
                  local.get $p0
                  i32.load offset=96
                  i32.load offset=28
                  local.get $p1
                  i32.add
                  f32.load offset=16
                  local.set $l11
                  i32.const 4674503
                  i32.load8_u
                  i32.eqz
                  if $I42
                    i32.const 3752504
                    call $f1661
                    i32.const 4674503
                    i32.const 1
                    i32.store8
                  end
                  i32.const 3752504
                  i32.load
                  local.tee $p1
                  i32.load offset=116
                  i32.eqz
                  if $I43
                    local.get $p1
                    call $f65192
                  end
                  local.get $l5
                  i32.eqz
                  br_if $B30
                  local.get $l11
                  f32.abs
                  f32.const 0x1.28f5c2p-3 (;=0.145;)
                  f32.le
                  i32.eqz
                  local.get $l9
                  f32.const 0x1.6947aep+2 (;=5.645;)
                  f32.lt
                  i32.eqz
                  local.get $l9
                  f32.const 0x1.28f5c2p-3 (;=0.145;)
                  f32.gt
                  i32.eqz
                  local.get $l10
                  f32.const -0x1.1d70a4p+1 (;=-2.23;)
                  f32.gt
                  if $I44 (result i32)
                    local.get $l10
                    local.get $l10
                    f32.mul
                    local.get $l9
                    local.get $l9
                    f32.mul
                    f32.add
                    f32.sqrt
                    f32.const 0x1.01eb86p+1 (;=2.015;)
                    f32.lt
                  else
                    i32.const 1
                  end
                  local.get $l10
                  f32.const 0x1.1d70a4p+1 (;=2.23;)
                  f32.lt
                  i32.eqz
                  i32.or
                  i32.or
                  i32.or
                  i32.or
                  i32.const 1
                  i32.ne
                  br_if $B30
                  local.get $p0
                  local.get $p0
                  i32.load offset=96
                  local.tee $l3
                  i32.load offset=24
                  local.tee $l2
                  i32.store offset=20
                  local.get $p0
                  i32.const 0
                  i32.store offset=24
                  local.get $p0
                  i32.const 1
                  i32.store8 offset=16
                  i32.const 3821172
                  i32.load
                  local.set $p1
                  block $B45
                    block $B46
                      local.get $l2
                      i32.eqz
                      if $I47
                        local.get $l3
                        i32.load offset=44
                        local.get $p1
                        i32.const 0
                        call $f61033
                        i32.const 3836216
                        local.set $l2
                        i32.const 3748808
                        i32.load
                        local.tee $p1
                        i32.load offset=116
                        i32.eqz
                        br_if $B46
                        br $B45
                      end
                      local.get $l3
                      i32.load offset=68
                      local.get $p1
                      i32.const 0
                      call $f61033
                      i32.const 3836224
                      local.set $l2
                      i32.const 3748808
                      i32.load
                      local.tee $p1
                      i32.load offset=116
                      br_if $B45
                    end
                    local.get $p1
                    call $f65192
                  end
                  local.get $l2
                  i32.load
                  i32.const 0
                  call $f42976
                  f32.const 0x0p+0 (;=0;)
                  i32.const 0
                  call $f54557
                  br $B26
                end
                local.get $l2
                i32.const 2
                i32.add
                local.tee $l2
                local.get $p0
                i32.load offset=96
                i32.load offset=8
                i32.const 1
                i32.sub
                i32.lt_s
                br_if $L27
              end
            end
            block $B48
              local.get $p0
              i32.load offset=96
              i32.load offset=28
              call $f1448
              local.tee $l2
              i32.eqz
              if $I49
                local.get $p0
                i32.const 0
                i32.store offset=100
                br $B48
              end
              local.get $l2
              i32.const 3745900
              i32.load
              local.tee $l3
              call $f1674
              local.tee $p1
              i32.eqz
              br_if $B23
              local.get $p0
              local.get $p1
              i32.store offset=100
              local.get $l2
              i32.const 3745900
              i32.load
              local.tee $p0
              call $f1674
              i32.eqz
              br_if $B22
            end
            local.get $l4
            i32.const 80
            i32.add
            global.set $g0
            return
          end
          local.get $l2
          local.get $l5
          call $f1678
          unreachable
        end
        local.get $l2
        local.get $p1
        call $f1678
        unreachable
      end
      local.get $l2
      local.get $l3
      call $f1678
      unreachable
    end
    local.get $l2
    local.get $p0
    call $f1678
    unreachable)
