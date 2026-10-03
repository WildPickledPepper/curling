  (func $f69974 (type $t2) (param $p0 i32) (param $p1 i32) (param $p2 i32)
    (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32)
    block $B0
      local.get $p2
      i32.const 2
      i32.le_u
      if $I1
        local.get $p2
        i32.eqz
        br_if $B0
        local.get $p0
        i32.load offset=76
        local.tee $l6
        local.get $p1
        i64.load
        i64.store
        local.get $l6
        local.get $p1
        i64.load offset=8
        i64.store offset=8
        local.get $p0
        i32.load offset=76
        local.tee $l6
        local.get $p1
        i64.load offset=16
        i64.store offset=16
        local.get $l6
        local.get $p1
        i64.load offset=24
        i64.store offset=24
        local.get $p0
        i32.load offset=76
        local.tee $l6
        local.get $p1
        i64.load offset=32
        i64.store offset=32
        local.get $l6
        local.get $p1
        i64.load offset=40
        i64.store offset=40
        local.get $p2
        i32.const 1
        i32.eq
        br_if $B0
        local.get $p0
        i32.load offset=76
        local.tee $l6
        local.get $p1
        i64.load offset=48
        i64.store offset=48
        local.get $l6
        local.get $p1
        i64.load offset=56
        i64.store offset=56
        local.get $p0
        i32.load offset=76
        local.tee $l6
        i32.const -64
        i32.sub
        local.get $p1
        i32.const -64
        i32.sub
        i64.load
        i64.store
        local.get $l6
        local.get $p1
        i64.load offset=72
        i64.store offset=72
        local.get $p0
        i32.load offset=76
        local.tee $l6
        local.get $p1
        i64.load offset=80
        i64.store offset=80
        local.get $l6
        local.get $p1
        i64.load offset=88
        i64.store offset=88
        local.get $p0
        local.get $p2
        i32.store8 offset=64
        return
      end
      global.get $g0
      i32.const -64
      i32.add
      local.tee $l3
      global.set $g0
      local.get $l3
      i32.const 0
      local.get $p2
      local.tee $l7
      call $f484
      local.set $l8
      block $B2
        local.get $p2
        i32.const 2
        i32.lt_u
        local.tee $l10
        br_if $B2
        local.get $l7
        i32.const 1
        i32.sub
        local.tee $l3
        i32.const 3
        i32.and
        local.set $p2
        local.get $p1
        f32.load offset=44
        local.set $l14
        block $B3
          local.get $l7
          i32.const 2
          i32.sub
          i32.const 3
          i32.lt_u
          if $I4
            i32.const 1
            local.set $l3
            br $B3
          end
          local.get $l3
          i32.const -4
          i32.and
          local.set $l9
          i32.const 1
          local.set $l3
          loop $L5
            local.get $p1
            local.get $l3
            i32.const 48
            i32.mul
            i32.add
            local.tee $l4
            f32.load offset=188
            local.tee $l15
            local.get $l4
            f32.load offset=140
            local.tee $l16
            local.get $l4
            f32.load offset=92
            local.tee $l17
            local.get $l4
            f32.load offset=44
            local.tee $l18
            local.get $l14
            local.get $l14
            local.get $l18
            f32.gt
            local.tee $l4
            select
            local.tee $l14
            local.get $l14
            local.get $l17
            f32.gt
            local.tee $l11
            select
            local.tee $l14
            local.get $l14
            local.get $l16
            f32.gt
            local.tee $l12
            select
            local.tee $l14
            local.get $l14
            local.get $l15
            f32.gt
            local.tee $l13
            select
            local.set $l14
            local.get $l3
            i32.const 3
            i32.add
            local.get $l3
            i32.const 2
            i32.add
            local.get $l3
            i32.const 1
            i32.add
            local.get $l3
            local.get $l5
            local.get $l4
            select
            local.get $l11
            select
            local.get $l12
            select
            local.get $l13
            select
            local.set $l5
            local.get $l3
            i32.const 4
            i32.add
            local.set $l3
            local.get $l9
            i32.const 4
            i32.sub
            local.tee $l9
            br_if $L5
          end
        end
        local.get $p2
        i32.eqz
        br_if $B2
        loop $L6
          local.get $p1
          local.get $l3
          i32.const 48
          i32.mul
          i32.add
          f32.load offset=44
          local.tee $l15
          local.get $l14
          local.get $l14
          local.get $l15
          f32.gt
          local.tee $l4
          select
          local.set $l14
          local.get $l3
          local.get $l5
          local.get $l4
          select
          local.set $l5
          local.get $l3
          i32.const 1
          i32.add
          local.set $l3
          local.get $p2
          i32.const 1
          i32.sub
          local.tee $p2
          br_if $L6
        end
      end
      local.get $p0
      i32.load offset=76
      local.tee $l3
      local.get $p1
      local.get $l5
      i32.const 48
      i32.mul
      i32.add
      local.tee $l4
      i64.load
      i64.store
      local.get $l3
      local.get $l4
      i64.load offset=40
      i64.store offset=40
      local.get $l3
      local.get $l4
      i64.load offset=32
      i64.store offset=32
      local.get $l3
      local.get $l4
      i64.load offset=24
      i64.store offset=24
      local.get $l3
      local.get $l4
      i64.load offset=16
      i64.store offset=16
      local.get $l3
      local.get $l4
      i64.load offset=8
      i64.store offset=8
      local.get $l5
      local.get $l8
      i32.add
      i32.const 1
      i32.store8
      local.get $p0
      i32.load offset=76
      local.set $l4
      local.get $l10
      i32.eqz
      if $I7
        local.get $p1
        f32.load offset=16
        local.get $l4
        f32.load offset=16
        local.tee $l16
        f32.sub
        local.tee $l14
        local.get $l14
        f32.mul
        local.get $p1
        f32.load offset=20
        local.get $l4
        f32.load offset=20
        local.tee $l17
        f32.sub
        local.tee $l14
        local.get $l14
        f32.mul
        f32.add
        local.get $p1
        f32.load offset=24
        local.get $l4
        f32.load offset=24
        local.tee $l18
        f32.sub
        local.tee $l14
        local.get $l14
        f32.mul
        f32.add
        local.set $l14
        i32.const 1
        local.set $l3
        loop $L8
          local.get $p1
          local.get $l3
          i32.const 48
          i32.mul
          i32.add
          local.tee $l5
          f32.load offset=16
          local.get $l16
          f32.sub
          local.tee $l15
          local.get $l15
          f32.mul
          local.get $l5
          f32.load offset=20
          local.get $l17
          f32.sub
          local.tee $l15
          local.get $l15
          f32.mul
          f32.add
          local.get $l5
          f32.load offset=24
          local.get $l18
          f32.sub
          local.tee $l15
          local.get $l15
          f32.mul
          f32.add
          local.tee $l15
          local.get $l14
          local.get $l14
          local.get $l15
          f32.lt
          local.tee $l5
          select
          local.set $l14
          local.get $l3
          local.get $l6
          local.get $l5
          select
          local.set $l6
          local.get $l3
          i32.const 1
          i32.add
          local.tee $l3
          local.get $l7
          i32.ne
          br_if $L8
        end
      end
      local.get $l4
      local.get $p1
      local.get $l6
      i32.const 48
      i32.mul
      i32.add
      local.tee $l3
      i64.load
      i64.store offset=48
      local.get $l4
      local.get $l3
      i64.load offset=40
      i64.store offset=88
      local.get $l4
      local.get $l3
      i64.load offset=32
      i64.store offset=80
      local.get $l4
      local.get $l3
      i64.load offset=24
      i64.store offset=72
      local.get $l4
      i32.const -64
      i32.sub
      local.get $l3
      i64.load offset=16
      i64.store
      local.get $l4
      local.get $l3
      i64.load offset=8
      i64.store offset=56
      local.get $l6
      local.get $l8
      i32.add
      i32.const 1
      i32.store8
      block $B9
        local.get $l7
        i32.eqz
        br_if $B9
        local.get $l3
        f32.load offset=44
        local.set $l18
        i32.const 0
        local.set $l3
        local.get $l6
        local.set $p2
        loop $L10
          block $B11
            local.get $l3
            local.get $l8
            i32.add
            i32.load8_u
            br_if $B11
            local.get $p0
            i32.load offset=76
            local.tee $l5
            f32.load offset=16
            local.get $p1
            local.get $l3
            i32.const 48
            i32.mul
            i32.add
            local.tee $l4
            f32.load offset=16
            local.tee $l14
            f32.sub
            local.tee $l15
            local.get $l15
            f32.mul
            local.get $l5
            f32.load offset=20
            local.get $l4
            f32.load offset=20
            local.tee $l15
            f32.sub
            local.tee $l16
            local.get $l16
            f32.mul
            f32.add
            local.get $l5
            f32.load offset=24
            local.get $l4
            f32.load offset=24
            local.tee $l16
            f32.sub
            local.tee $l17
            local.get $l17
            f32.mul
            f32.add
            local.get $l5
            i32.const -64
            i32.sub
            f32.load
            local.get $l14
            f32.sub
            local.tee $l14
            local.get $l14
            f32.mul
            local.get $l5
            f32.load offset=68
            local.get $l15
            f32.sub
            local.tee $l14
            local.get $l14
            f32.mul
            f32.add
            local.get $l5
            f32.load offset=72
            local.get $l16
            f32.sub
            local.tee $l14
            local.get $l14
            f32.mul
            f32.add
            f32.gt
            i32.eqz
            br_if $B11
            local.get $l3
            local.get $p2
            local.get $l18
            local.get $l4
            f32.load offset=44
            f32.gt
            select
            local.set $p2
          end
          local.get $l3
          i32.const 1
          i32.add
          local.tee $l3
          local.get $l7
          i32.ne
          br_if $L10
        end
        local.get $p2
        local.get $l6
        i32.eq
        br_if $B9
        local.get $p0
        i32.load offset=76
        local.tee $l3
        local.get $p1
        local.get $p2
        i32.const 48
        i32.mul
        i32.add
        local.tee $l5
        i64.load
        i64.store offset=48
        local.get $l3
        local.get $l5
        i64.load offset=40
        i64.store offset=88
        local.get $l3
        local.get $l5
        i64.load offset=32
        i64.store offset=80
        local.get $l3
        local.get $l5
        i64.load offset=24
        i64.store offset=72
        local.get $l3
        i32.const -64
        i32.sub
        local.get $l5
        i64.load offset=16
        i64.store
        local.get $l3
        local.get $l5
        i64.load offset=8
        i64.store offset=56
      end
      local.get $l8
      i32.const -64
      i32.sub
      global.set $g0
      i32.const 2
      local.set $p2
    end
    local.get $p0
    local.get $p2
    i32.store8 offset=64)
