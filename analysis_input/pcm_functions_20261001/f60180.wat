  (func $f60180 (type $t2) (param $p0 i32) (param $p1 i32) (param $p2 i32)
    (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 f32)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l4
    global.set $g0
    i32.const 4674505
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3773132
      call $f1661
      i32.const 4674505
      i32.const 1
      i32.store8
    end
    i32.const 0
    local.set $p2
    loop $L1
      block $B2
        local.get $p0
        i32.load offset=128
        i32.eqz
        if $I3
          local.get $p0
          i32.load offset=192
          local.get $p2
          i32.const 3773132
          i32.load
          call $f2903
          i32.const 0
          call $f54404
          local.set $l5
          local.get $p1
          i32.load
          local.set $l3
          block $B4
            local.get $l5
            if $I5
              local.get $p0
              f32.load offset=232
              local.set $l6
              local.get $l4
              local.get $p0
              i32.load offset=192
              local.get $p2
              i32.const 3773132
              i32.load
              call $f2903
              i32.const 0
              call $f54401
              i32.const 0
              call $f54624
              local.get $l3
              local.get $p2
              i32.const 4
              i32.shl
              local.tee $l5
              i32.add
              local.get $l6
              local.get $l4
              f32.load offset=8
              f32.sub
              f32.store offset=16
              local.get $p0
              f32.load offset=224
              local.set $l6
              local.get $p1
              i32.load
              local.set $l3
              local.get $l4
              local.get $p0
              i32.load offset=192
              local.get $p2
              i32.const 3773132
              i32.load
              call $f2903
              i32.const 0
              call $f54401
              i32.const 0
              call $f54624
              local.get $l3
              local.get $l5
              i32.add
              local.get $l6
              local.get $l4
              f32.load
              f32.sub
              f32.store offset=20
              br $B4
            end
            local.get $l3
            local.get $p2
            i32.const 4
            i32.shl
            i32.add
            i64.const 0
            i64.store offset=16 align=4
          end
          local.get $p0
          i32.load offset=196
          local.get $p2
          i32.const 3773132
          i32.load
          call $f2903
          i32.const 0
          call $f54404
          local.set $l5
          local.get $p1
          i32.load
          local.set $l3
          local.get $l5
          if $I6
            local.get $p0
            f32.load offset=232
            local.set $l6
            local.get $l4
            local.get $p0
            i32.load offset=196
            local.get $p2
            i32.const 3773132
            i32.load
            call $f2903
            i32.const 0
            call $f54401
            i32.const 0
            call $f54624
            local.get $l3
            local.get $p2
            i32.const 4
            i32.shl
            local.tee $l5
            i32.add
            local.get $l6
            local.get $l4
            f32.load offset=8
            f32.sub
            f32.store offset=24
            local.get $p0
            f32.load offset=224
            local.set $l6
            local.get $p1
            i32.load
            local.set $l3
            local.get $l4
            local.get $p0
            i32.load offset=196
            local.get $p2
            i32.const 3773132
            i32.load
            call $f2903
            i32.const 0
            call $f54401
            i32.const 0
            call $f54624
            local.get $l3
            local.get $l5
            i32.add
            local.get $l6
            local.get $l4
            f32.load
            f32.sub
            f32.store offset=28
            br $B2
          end
          local.get $l3
          local.get $p2
          i32.const 4
          i32.shl
          i32.add
          i64.const 0
          i64.store offset=24 align=4
          br $B2
        end
        local.get $p0
        i32.load offset=196
        local.get $p2
        i32.const 3773132
        i32.load
        call $f2903
        i32.const 0
        call $f54404
        local.set $l5
        local.get $p1
        i32.load
        local.set $l3
        block $B7
          local.get $l5
          if $I8
            local.get $p0
            f32.load offset=232
            local.set $l6
            local.get $l4
            local.get $p0
            i32.load offset=196
            local.get $p2
            i32.const 3773132
            i32.load
            call $f2903
            i32.const 0
            call $f54401
            i32.const 0
            call $f54624
            local.get $l3
            local.get $p2
            i32.const 4
            i32.shl
            local.tee $l5
            i32.add
            local.get $l6
            local.get $l4
            f32.load offset=8
            f32.sub
            f32.store offset=16
            local.get $p0
            f32.load offset=224
            local.set $l6
            local.get $p1
            i32.load
            local.set $l3
            local.get $l4
            local.get $p0
            i32.load offset=196
            local.get $p2
            i32.const 3773132
            i32.load
            call $f2903
            i32.const 0
            call $f54401
            i32.const 0
            call $f54624
            local.get $l3
            local.get $l5
            i32.add
            local.get $l6
            local.get $l4
            f32.load
            f32.sub
            f32.store offset=20
            br $B7
          end
          local.get $l3
          local.get $p2
          i32.const 4
          i32.shl
          i32.add
          i64.const 0
          i64.store offset=16 align=4
        end
        local.get $p0
        i32.load offset=192
        local.get $p2
        i32.const 3773132
        i32.load
        call $f2903
        i32.const 0
        call $f54404
        local.set $l5
        local.get $p1
        i32.load
        local.set $l3
        local.get $l5
        if $I9
          local.get $p0
          f32.load offset=232
          local.set $l6
          local.get $l4
          local.get $p0
          i32.load offset=192
          local.get $p2
          i32.const 3773132
          i32.load
          call $f2903
          i32.const 0
          call $f54401
          i32.const 0
          call $f54624
          local.get $l3
          local.get $p2
          i32.const 4
          i32.shl
          local.tee $l5
          i32.add
          local.get $l6
          local.get $l4
          f32.load offset=8
          f32.sub
          f32.store offset=24
          local.get $p0
          f32.load offset=224
          local.set $l6
          local.get $p1
          i32.load
          local.set $l3
          local.get $l4
          local.get $p0
          i32.load offset=192
          local.get $p2
          i32.const 3773132
          i32.load
          call $f2903
          i32.const 0
          call $f54401
          i32.const 0
          call $f54624
          local.get $l3
          local.get $l5
          i32.add
          local.get $l6
          local.get $l4
          f32.load
          f32.sub
          f32.store offset=28
          br $B2
        end
        local.get $l3
        local.get $p2
        i32.const 4
        i32.shl
        i32.add
        i64.const 0
        i64.store offset=24 align=4
      end
      local.get $p2
      i32.const 1
      i32.add
      local.tee $p2
      i32.const 8
      i32.ne
      br_if $L1
    end
    local.get $l4
    i32.const 16
    i32.add
    global.set $g0)
