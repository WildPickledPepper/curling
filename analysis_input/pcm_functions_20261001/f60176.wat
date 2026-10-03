  (func $f60176 (type $t2) (param $p0 i32) (param $p1 i32) (param $p2 i32)
    (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 f32) (local $l10 f32) (local $l11 f32)
    global.get $g0
    i32.const 192
    i32.sub
    local.tee $p2
    global.set $g0
    i32.const 4674504
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3773132
      call $f1661
      i32.const 4674504
      i32.const 1
      i32.store8
    end
    local.get $p0
    i32.const 200
    i32.add
    local.set $l7
    loop $L1
      local.get $l4
      i32.const 2
      i32.shl
      local.tee $l5
      i32.const 1
      i32.or
      local.set $l3
      local.get $p1
      i32.load
      local.tee $l6
      local.get $l4
      i32.const 4
      i32.shl
      i32.add
      f32.load offset=16
      local.set $l9
      block $B2
        local.get $p0
        i32.load offset=128
        i32.eqz
        if $I3
          block $B4
            block $B5
              local.get $l9
              f32.const 0x0p+0 (;=0;)
              f32.eq
              if $I6
                local.get $l6
                local.get $l3
                i32.const 2
                i32.shl
                i32.add
                f32.load offset=16
                f32.const 0x0p+0 (;=0;)
                f32.eq
                br_if $B5
              end
              local.get $p0
              i32.load offset=192
              local.get $l4
              i32.const 3773132
              i32.load
              call $f2903
              i32.const 1
              i32.const 0
              call $f54405
              local.get $p0
              i32.load offset=192
              local.get $l4
              i32.const 3773132
              i32.load
              call $f2903
              i32.const 0
              call $f54401
              local.set $l6
              local.get $p1
              i32.load
              i32.const 16
              i32.add
              local.tee $l8
              local.get $l3
              i32.const 2
              i32.shl
              i32.add
              f32.load
              local.set $l9
              local.get $p0
              f32.load offset=224
              local.set $l10
              local.get $p0
              f32.load offset=204
              local.set $l11
              local.get $p2
              i32.const 184
              i32.add
              local.tee $l3
              local.get $p0
              f32.load offset=232
              local.get $l8
              local.get $l5
              i32.const 2
              i32.shl
              i32.add
              f32.load
              f32.sub
              f32.store
              local.get $p2
              local.get $l3
              i32.load
              i32.store offset=56
              local.get $p2
              local.get $l11
              f32.store offset=180
              local.get $p2
              local.get $l10
              local.get $l9
              f32.sub
              f32.store offset=176
              local.get $p2
              local.get $p2
              i64.load offset=176
              i64.store offset=48
              local.get $l6
              local.get $p2
              i32.const 48
              i32.add
              i32.const 0
              call $f54626
              br $B4
            end
            local.get $p0
            i32.load offset=192
            local.get $l4
            i32.const 3773132
            i32.load
            call $f2903
            i32.const 0
            i32.const 0
            call $f54405
            local.get $p0
            i32.load offset=192
            local.get $l4
            i32.const 3773132
            i32.load
            call $f2903
            i32.const 0
            call $f54401
            local.set $l3
            local.get $p2
            local.get $l7
            i32.load offset=8
            i32.store offset=40
            local.get $p2
            local.get $l7
            i64.load align=4
            i64.store offset=32
            local.get $l3
            local.get $p2
            i32.const 32
            i32.add
            i32.const 0
            call $f54626
          end
          local.get $l5
          i32.const 3
          i32.or
          local.set $l3
          block $B7
            local.get $p1
            i32.load
            local.tee $l6
            local.get $l5
            i32.const 2
            i32.or
            i32.const 2
            i32.shl
            local.tee $l5
            i32.add
            f32.load offset=16
            f32.const 0x0p+0 (;=0;)
            f32.eq
            if $I8
              local.get $l6
              local.get $l3
              i32.const 2
              i32.shl
              i32.add
              f32.load offset=16
              f32.const 0x0p+0 (;=0;)
              f32.eq
              br_if $B7
            end
            local.get $p0
            i32.load offset=196
            local.get $l4
            i32.const 3773132
            i32.load
            call $f2903
            i32.const 1
            i32.const 0
            call $f54405
            local.get $p0
            i32.load offset=196
            local.get $l4
            i32.const 3773132
            i32.load
            call $f2903
            i32.const 0
            call $f54401
            local.set $l6
            local.get $p1
            i32.load
            i32.const 16
            i32.add
            local.tee $l8
            local.get $l3
            i32.const 2
            i32.shl
            i32.add
            f32.load
            local.set $l9
            local.get $p0
            f32.load offset=224
            local.set $l10
            local.get $p0
            f32.load offset=204
            local.set $l11
            local.get $p2
            i32.const 168
            i32.add
            local.tee $l3
            local.get $p0
            f32.load offset=232
            local.get $l5
            local.get $l8
            i32.add
            f32.load
            f32.sub
            f32.store
            local.get $p2
            local.get $l3
            i32.load
            i32.store offset=24
            local.get $p2
            local.get $l11
            f32.store offset=164
            local.get $p2
            local.get $l10
            local.get $l9
            f32.sub
            f32.store offset=160
            local.get $p2
            local.get $p2
            i64.load offset=160
            i64.store offset=16
            local.get $l6
            local.get $p2
            i32.const 16
            i32.add
            i32.const 0
            call $f54626
            br $B2
          end
          local.get $p0
          i32.load offset=196
          local.get $l4
          i32.const 3773132
          i32.load
          call $f2903
          i32.const 0
          i32.const 0
          call $f54405
          local.get $p0
          i32.load offset=196
          local.get $l4
          i32.const 3773132
          i32.load
          call $f2903
          i32.const 0
          call $f54401
          local.set $l5
          local.get $p2
          local.get $l7
          i32.load offset=8
          i32.store offset=8
          local.get $p2
          local.get $l7
          i64.load align=4
          i64.store
          local.get $l5
          local.get $p2
          i32.const 0
          call $f54626
          br $B2
        end
        block $B9
          block $B10
            local.get $l9
            f32.const 0x0p+0 (;=0;)
            f32.eq
            if $I11
              local.get $l6
              local.get $l3
              i32.const 2
              i32.shl
              i32.add
              f32.load offset=16
              f32.const 0x0p+0 (;=0;)
              f32.eq
              br_if $B10
            end
            local.get $p0
            i32.load offset=196
            local.get $l4
            i32.const 3773132
            i32.load
            call $f2903
            i32.const 1
            i32.const 0
            call $f54405
            local.get $p0
            i32.load offset=196
            local.get $l4
            i32.const 3773132
            i32.load
            call $f2903
            i32.const 0
            call $f54401
            local.set $l6
            local.get $p1
            i32.load
            i32.const 16
            i32.add
            local.tee $l8
            local.get $l3
            i32.const 2
            i32.shl
            i32.add
            f32.load
            local.set $l9
            local.get $p0
            f32.load offset=224
            local.set $l10
            local.get $p0
            f32.load offset=204
            local.set $l11
            local.get $p2
            i32.const 152
            i32.add
            local.tee $l3
            local.get $p0
            f32.load offset=232
            local.get $l8
            local.get $l5
            i32.const 2
            i32.shl
            i32.add
            f32.load
            f32.sub
            f32.store
            local.get $p2
            local.get $l3
            i32.load
            i32.store offset=120
            local.get $p2
            local.get $l11
            f32.store offset=148
            local.get $p2
            local.get $l10
            local.get $l9
            f32.sub
            f32.store offset=144
            local.get $p2
            local.get $p2
            i64.load offset=144
            i64.store offset=112
            local.get $l6
            local.get $p2
            i32.const 112
            i32.add
            i32.const 0
            call $f54626
            br $B9
          end
          local.get $p0
          i32.load offset=196
          local.get $l4
          i32.const 3773132
          i32.load
          call $f2903
          i32.const 0
          i32.const 0
          call $f54405
          local.get $p0
          i32.load offset=196
          local.get $l4
          i32.const 3773132
          i32.load
          call $f2903
          i32.const 0
          call $f54401
          local.set $l3
          local.get $p2
          local.get $l7
          i32.load offset=8
          i32.store offset=104
          local.get $p2
          local.get $l7
          i64.load align=4
          i64.store offset=96
          local.get $l3
          local.get $p2
          i32.const 96
          i32.add
          i32.const 0
          call $f54626
        end
        local.get $l5
        i32.const 3
        i32.or
        local.set $l3
        block $B12
          local.get $p1
          i32.load
          local.tee $l6
          local.get $l5
          i32.const 2
          i32.or
          i32.const 2
          i32.shl
          local.tee $l5
          i32.add
          f32.load offset=16
          f32.const 0x0p+0 (;=0;)
          f32.eq
          if $I13
            local.get $l6
            local.get $l3
            i32.const 2
            i32.shl
            i32.add
            f32.load offset=16
            f32.const 0x0p+0 (;=0;)
            f32.eq
            br_if $B12
          end
          local.get $p0
          i32.load offset=192
          local.get $l4
          i32.const 3773132
          i32.load
          call $f2903
          i32.const 1
          i32.const 0
          call $f54405
          local.get $p0
          i32.load offset=192
          local.get $l4
          i32.const 3773132
          i32.load
          call $f2903
          i32.const 0
          call $f54401
          local.set $l6
          local.get $p1
          i32.load
          i32.const 16
          i32.add
          local.tee $l8
          local.get $l3
          i32.const 2
          i32.shl
          i32.add
          f32.load
          local.set $l9
          local.get $p0
          f32.load offset=224
          local.set $l10
          local.get $p0
          f32.load offset=204
          local.set $l11
          local.get $p2
          i32.const 136
          i32.add
          local.tee $l3
          local.get $p0
          f32.load offset=232
          local.get $l5
          local.get $l8
          i32.add
          f32.load
          f32.sub
          f32.store
          local.get $p2
          local.get $l3
          i32.load
          i32.store offset=88
          local.get $p2
          local.get $l11
          f32.store offset=132
          local.get $p2
          local.get $l10
          local.get $l9
          f32.sub
          f32.store offset=128
          local.get $p2
          local.get $p2
          i64.load offset=128
          i64.store offset=80
          local.get $l6
          local.get $p2
          i32.const 80
          i32.add
          i32.const 0
          call $f54626
          br $B2
        end
        local.get $p0
        i32.load offset=192
        local.get $l4
        i32.const 3773132
        i32.load
        call $f2903
        i32.const 0
        i32.const 0
        call $f54405
        local.get $p0
        i32.load offset=192
        local.get $l4
        i32.const 3773132
        i32.load
        call $f2903
        i32.const 0
        call $f54401
        local.set $l5
        local.get $p2
        local.get $l7
        i32.load offset=8
        i32.store offset=72
        local.get $p2
        local.get $l7
        i64.load align=4
        i64.store offset=64
        local.get $l5
        local.get $p2
        i32.const -64
        i32.sub
        i32.const 0
        call $f54626
      end
      local.get $l4
      i32.const 1
      i32.add
      local.tee $l4
      i32.const 8
      i32.ne
      br_if $L1
    end
    local.get $p2
    i32.const 192
    i32.add
    global.set $g0)
