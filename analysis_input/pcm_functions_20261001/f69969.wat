  (func $f69969 (type $t65) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 f32)
    (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32)
    local.get $p1
    f32.load offset=44
    local.set $l21
    global.get $g0
    i32.const 80
    i32.sub
    local.tee $l5
    i32.const 0
    i32.store8
    f32.const -0x1.fffffep+127 (;=-3.40282e+38;)
    local.set $l19
    block $B0
      local.get $p2
      i32.const 2
      i32.lt_u
      if $I1
        br $B0
      end
      i32.const 1
      local.set $l4
      local.get $p2
      i32.const 1
      i32.sub
      local.tee $l6
      i32.const 1
      i32.and
      local.set $l12
      block $B2
        local.get $p2
        i32.const 2
        i32.eq
        if $I3
          br $B2
        end
        local.get $l6
        i32.const -2
        i32.and
        local.set $l11
        loop $L4
          local.get $l4
          local.get $l5
          i32.add
          local.get $l4
          i32.store8
          local.get $p1
          local.get $l4
          i32.const 48
          i32.mul
          i32.add
          local.tee $l8
          f32.load offset=44
          local.set $l16
          local.get $l5
          local.get $l4
          i32.const 1
          i32.add
          local.tee $l6
          i32.add
          local.get $l6
          i32.store8
          local.get $l8
          f32.load offset=92
          local.tee $l17
          local.get $l16
          local.get $l21
          local.get $l16
          local.get $l21
          f32.lt
          local.tee $l8
          select
          local.tee $l18
          local.get $l17
          local.get $l18
          f32.lt
          local.tee $l9
          select
          local.set $l21
          local.get $l19
          local.get $l16
          local.get $l16
          local.get $l19
          f32.lt
          select
          local.tee $l16
          local.get $l17
          local.get $l16
          local.get $l17
          f32.gt
          select
          local.set $l19
          local.get $l6
          local.get $l4
          local.get $l10
          local.get $l8
          select
          local.get $l9
          select
          local.set $l10
          local.get $l6
          local.get $l4
          local.get $l7
          local.get $l8
          select
          local.get $l9
          select
          local.set $l7
          local.get $l4
          i32.const 2
          i32.add
          local.set $l4
          local.get $l11
          i32.const 2
          i32.sub
          local.tee $l11
          br_if $L4
        end
      end
      local.get $l12
      i32.eqz
      br_if $B0
      local.get $l4
      local.get $l5
      i32.add
      local.get $l4
      i32.store8
      local.get $l19
      local.get $p1
      local.get $l4
      i32.const 48
      i32.mul
      i32.add
      f32.load offset=44
      local.tee $l16
      local.get $l16
      local.get $l19
      f32.lt
      select
      local.set $l19
      local.get $l16
      local.get $l21
      local.get $l16
      local.get $l21
      f32.lt
      local.tee $l6
      select
      local.set $l21
      local.get $l4
      local.get $l7
      local.get $l6
      select
      local.set $l7
      local.get $l4
      local.get $l10
      local.get $l6
      select
      local.set $l10
    end
    local.get $l5
    local.get $l7
    i32.add
    local.get $l5
    local.get $p2
    i32.const 1
    i32.sub
    local.tee $l7
    i32.add
    i32.load8_u
    i32.store8
    local.get $l5
    local.get $l10
    i32.store8 offset=76
    local.get $p1
    local.get $l10
    i32.const 255
    i32.and
    local.tee $l11
    i32.const 48
    i32.mul
    i32.add
    local.tee $l4
    f32.load offset=16
    local.set $l22
    local.get $l5
    i32.load8_u
    local.set $l13
    local.get $l4
    f32.load offset=24
    local.set $l23
    local.get $l4
    f32.load offset=20
    local.set $l26
    local.get $l7
    i32.const 1
    i32.le_u
    if $I5 (result i32)
      local.get $l5
    else
      local.get $p1
      local.get $l13
      i32.const 48
      i32.mul
      i32.add
      local.tee $l4
      f32.load offset=16
      local.get $l22
      f32.sub
      local.tee $l16
      local.get $l16
      f32.mul
      local.get $l4
      f32.load offset=20
      local.get $l26
      f32.sub
      local.tee $l16
      local.get $l16
      f32.mul
      f32.add
      local.get $l4
      f32.load offset=24
      local.get $l23
      f32.sub
      local.tee $l16
      local.get $l16
      f32.mul
      f32.add
      local.set $l16
      i32.const 0
      local.set $l8
      i32.const 1
      local.set $l4
      loop $L6
        local.get $p1
        local.get $l4
        local.get $l5
        i32.add
        i32.load8_u
        local.tee $l9
        i32.const 48
        i32.mul
        i32.add
        local.tee $l6
        f32.load offset=16
        local.get $l22
        f32.sub
        local.tee $l17
        local.get $l17
        f32.mul
        local.get $l6
        f32.load offset=20
        local.get $l26
        f32.sub
        local.tee $l17
        local.get $l17
        f32.mul
        f32.add
        local.get $l6
        f32.load offset=24
        local.get $l23
        f32.sub
        local.tee $l17
        local.get $l17
        f32.mul
        f32.add
        local.tee $l17
        local.get $l16
        local.get $l16
        local.get $l17
        f32.lt
        local.tee $l6
        select
        local.set $l16
        local.get $l9
        local.get $l13
        local.get $l6
        select
        local.set $l13
        local.get $l4
        local.get $l8
        local.get $l6
        select
        local.set $l8
        local.get $l4
        i32.const 1
        i32.add
        local.tee $l4
        local.get $l7
        i32.ne
        br_if $L6
      end
      local.get $l5
      local.get $l8
      i32.add
    end
    local.set $l6
    local.get $l5
    local.get $p2
    i32.const 2
    i32.sub
    local.tee $l14
    i32.add
    i32.load8_u
    local.set $l4
    local.get $l5
    local.get $l13
    i32.store8 offset=77
    local.get $l6
    local.get $l4
    i32.store8
    local.get $p1
    local.get $l13
    i32.const 255
    i32.and
    i32.const 48
    i32.mul
    i32.add
    local.tee $l4
    f32.load offset=16
    local.get $l22
    f32.sub
    local.tee $l24
    local.get $p1
    local.get $l11
    i32.const 48
    i32.mul
    i32.add
    local.tee $l6
    f32.load offset=36
    local.tee $l16
    f32.mul
    local.get $l4
    f32.load offset=20
    local.get $l26
    f32.sub
    local.tee $l20
    local.get $l6
    f32.load offset=32
    local.tee $l17
    f32.mul
    f32.sub
    local.tee $l18
    f32.const 0x1p+0 (;=1;)
    local.get $l18
    local.get $l18
    f32.mul
    local.get $l20
    local.get $l6
    f32.load offset=40
    local.tee $l18
    f32.mul
    local.get $l4
    f32.load offset=24
    local.get $l23
    f32.sub
    local.tee $l20
    local.get $l16
    f32.mul
    f32.sub
    local.tee $l25
    local.get $l25
    f32.mul
    local.get $l20
    local.get $l17
    f32.mul
    local.get $l24
    local.get $l18
    f32.mul
    f32.sub
    local.tee $l20
    local.get $l20
    f32.mul
    f32.add
    f32.add
    local.tee $l24
    f32.sqrt
    f32.div
    local.tee $l27
    f32.mul
    local.get $l18
    local.get $l24
    f32.const 0x0p+0 (;=0;)
    f32.gt
    local.tee $l4
    select
    local.set $l24
    local.get $l20
    local.get $l27
    f32.mul
    local.get $l16
    local.get $l4
    select
    local.set $l20
    local.get $l25
    local.get $l27
    f32.mul
    local.get $l17
    local.get $l4
    select
    local.set $l25
    i32.const -1
    local.set $l15
    f32.const -0x1.fffffep+127 (;=-3.40282e+38;)
    local.set $l17
    f32.const 0x1.fffffep+127 (;=3.40282e+38;)
    local.set $l18
    block $B7
      local.get $l14
      i32.eqz
      if $I8
        i32.const -1
        local.set $l11
        i32.const -1
        local.set $l6
        i32.const -1
        local.set $l12
        i32.const 255
        local.set $l15
        br $B7
      end
      i32.const 0
      local.set $l4
      i32.const -1
      local.set $l12
      i32.const -1
      local.set $l6
      i32.const -1
      local.set $l11
      loop $L9
        local.get $l25
        local.get $p1
        local.get $l4
        local.get $l5
        i32.add
        i32.load8_u
        local.tee $l8
        i32.const 48
        i32.mul
        i32.add
        local.tee $l9
        f32.load offset=16
        local.get $l22
        f32.sub
        f32.mul
        local.get $l20
        local.get $l9
        f32.load offset=20
        local.get $l26
        f32.sub
        f32.mul
        f32.add
        local.get $l24
        local.get $l9
        f32.load offset=24
        local.get $l23
        f32.sub
        f32.mul
        f32.add
        local.tee $l16
        local.get $l18
        local.get $l16
        local.get $l18
        f32.lt
        local.tee $l9
        select
        local.set $l18
        local.get $l16
        local.get $l17
        local.get $l16
        local.get $l17
        f32.gt
        local.tee $l7
        select
        local.set $l17
        local.get $l4
        local.get $l12
        local.get $l9
        select
        local.set $l12
        local.get $l8
        local.get $l6
        local.get $l9
        select
        local.set $l6
        local.get $l8
        local.get $l15
        local.get $l7
        select
        local.set $l15
        local.get $l4
        local.get $l11
        local.get $l7
        select
        local.set $l11
        local.get $l4
        i32.const 1
        i32.add
        local.tee $l4
        local.get $l14
        i32.ne
        br_if $L9
      end
    end
    local.get $l5
    local.get $l11
    i32.add
    local.get $l5
    local.get $p2
    i32.const 3
    i32.sub
    local.tee $l14
    i32.add
    i32.load8_u
    i32.store8
    local.get $l5
    local.get $l15
    i32.store8 offset=78
    local.get $l11
    local.get $l12
    local.get $l12
    local.get $l14
    i32.eq
    select
    local.set $l9
    block $B10
      local.get $l18
      local.get $l17
      f32.mul
      f32.const 0x0p+0 (;=0;)
      f32.gt
      i32.eqz
      br_if $B10
      local.get $l14
      i32.eqz
      br_if $B10
      local.get $p1
      local.get $l10
      i32.const 255
      i32.and
      i32.const 48
      i32.mul
      i32.add
      local.tee $l4
      f32.load offset=16
      local.set $l18
      local.get $l4
      f32.load offset=24
      local.set $l22
      local.get $l4
      f32.load offset=20
      local.set $l23
      f32.const -0x1.fffffep+127 (;=-3.40282e+38;)
      local.set $l16
      i32.const 0
      local.set $l4
      loop $L11
        local.get $l25
        local.get $p1
        local.get $l4
        local.get $l5
        i32.add
        i32.load8_u
        local.tee $l7
        i32.const 48
        i32.mul
        i32.add
        local.tee $l8
        f32.load offset=16
        local.get $l18
        f32.sub
        f32.mul
        local.get $l20
        local.get $l8
        f32.load offset=20
        local.get $l23
        f32.sub
        f32.mul
        f32.add
        local.get $l24
        local.get $l8
        f32.load offset=24
        local.get $l22
        f32.sub
        f32.mul
        f32.add
        local.tee $l17
        local.get $l16
        local.get $l16
        local.get $l17
        f32.lt
        local.tee $l8
        select
        local.set $l16
        local.get $l4
        local.get $l9
        local.get $l8
        select
        local.set $l9
        local.get $l7
        local.get $l6
        local.get $l8
        select
        local.set $l6
        local.get $l4
        i32.const 1
        i32.add
        local.tee $l4
        local.get $l14
        i32.ne
        br_if $L11
      end
    end
    local.get $l5
    local.get $l9
    i32.add
    local.get $l5
    local.get $p2
    i32.const 4
    i32.sub
    local.tee $l12
    i32.add
    i32.load8_u
    i32.store8
    local.get $l5
    local.get $l6
    i32.store8 offset=79
    block $B12
      block $B13
        local.get $l19
        local.get $p3
        f32.const 0x1.47ae14p-6 (;=0.02;)
        f32.mul
        local.tee $l18
        f32.gt
        i32.eqz
        br_if $B13
        local.get $l18
        local.get $l21
        f32.gt
        i32.eqz
        br_if $B13
        local.get $l12
        i32.const -2
        i32.and
        local.set $l15
        local.get $p2
        i32.const 1
        i32.and
        local.set $l13
        i32.const 0
        local.set $l7
        local.get $p2
        i32.const 5
        i32.ne
        local.set $l14
        loop $L14
          block $B15
            local.get $p1
            local.get $l10
            i32.const 255
            i32.and
            local.tee $l11
            i32.const 48
            i32.mul
            i32.add
            f32.load offset=44
            local.tee $l16
            local.get $l18
            f32.gt
            i32.eqz
            br_if $B15
            local.get $l12
            i32.eqz
            br_if $B15
            i32.const -1
            local.set $l6
            i32.const 0
            local.set $l4
            local.get $l15
            local.set $l8
            local.get $l14
            if $I16
              loop $L17
                local.get $l6
                local.get $l4
                local.get $l16
                local.get $p1
                local.get $l4
                local.get $l5
                i32.add
                i32.load8_u
                i32.const 48
                i32.mul
                i32.add
                f32.load offset=44
                local.tee $l17
                f32.gt
                i32.eqz
                local.get $l17
                local.get $l18
                f32.lt
                i32.eqz
                i32.or
                local.tee $l9
                select
                local.get $l4
                i32.const 1
                i32.or
                local.tee $l6
                local.get $l16
                local.get $l17
                local.get $l9
                select
                local.tee $l17
                local.get $p1
                local.get $l5
                local.get $l6
                i32.add
                i32.load8_u
                i32.const 48
                i32.mul
                i32.add
                f32.load offset=44
                local.tee $l16
                f32.gt
                i32.eqz
                local.get $l16
                local.get $l18
                f32.lt
                i32.eqz
                i32.or
                local.tee $l9
                select
                local.set $l6
                local.get $l17
                local.get $l16
                local.get $l9
                select
                local.set $l16
                local.get $l4
                i32.const 2
                i32.add
                local.set $l4
                local.get $l8
                i32.const 2
                i32.sub
                local.tee $l8
                br_if $L17
              end
            end
            local.get $l13
            if $I18
              local.get $l4
              local.get $l6
              local.get $l18
              local.get $p1
              local.get $l4
              local.get $l5
              i32.add
              i32.load8_u
              i32.const 48
              i32.mul
              i32.add
              f32.load offset=44
              local.tee $l17
              f32.gt
              select
              local.get $l6
              local.get $l16
              local.get $l17
              f32.gt
              select
              local.set $l6
            end
            local.get $l6
            local.get $l12
            i32.ge_u
            br_if $B15
            local.get $l5
            i32.const 76
            i32.add
            local.get $l7
            i32.add
            local.get $l5
            local.get $l6
            i32.add
            local.tee $l4
            i32.load8_u
            local.tee $l11
            i32.store8
            local.get $l4
            local.get $l10
            i32.store8
          end
          local.get $p0
          i32.load offset=76
          local.get $l7
          i32.const 48
          i32.mul
          i32.add
          local.tee $l4
          local.get $p1
          local.get $l11
          i32.const 48
          i32.mul
          i32.add
          local.tee $l6
          i64.load
          i64.store
          local.get $l4
          local.get $l6
          i64.load offset=40
          i64.store offset=40
          local.get $l4
          local.get $l6
          i64.load offset=32
          i64.store offset=32
          local.get $l4
          local.get $l6
          i64.load offset=24
          i64.store offset=24
          local.get $l4
          local.get $l6
          i64.load offset=16
          i64.store offset=16
          local.get $l4
          local.get $l6
          i64.load offset=8
          i64.store offset=8
          local.get $l7
          i32.const 1
          i32.add
          local.tee $l7
          i32.const 4
          i32.eq
          br_if $B12
          local.get $l5
          i32.const 76
          i32.add
          local.get $l7
          i32.add
          i32.load8_u
          local.set $l10
          br $L14
        end
        unreachable
      end
      local.get $p0
      i32.load offset=76
      local.tee $l4
      local.get $p1
      local.get $l10
      i32.const 255
      i32.and
      i32.const 48
      i32.mul
      i32.add
      local.tee $l5
      i64.load
      i64.store
      local.get $l4
      local.get $l5
      i64.load offset=32
      i64.store offset=32
      local.get $l4
      local.get $l5
      i64.load offset=16
      i64.store offset=16
      local.get $l4
      local.get $l5
      i64.load offset=40
      i64.store offset=40
      local.get $l4
      local.get $l5
      i64.load offset=24
      i64.store offset=24
      local.get $l4
      local.get $l5
      i64.load offset=8
      i64.store offset=8
      local.get $p0
      i32.load offset=76
      local.tee $l4
      local.get $p1
      local.get $l13
      i32.const 255
      i32.and
      i32.const 48
      i32.mul
      i32.add
      local.tee $l5
      i64.load
      i64.store offset=48
      local.get $l4
      i32.const -64
      i32.sub
      local.get $l5
      i64.load offset=16
      i64.store
      local.get $l4
      local.get $l5
      i64.load offset=32
      i64.store offset=80
      local.get $l4
      local.get $l5
      i64.load offset=8
      i64.store offset=56
      local.get $l4
      local.get $l5
      i64.load offset=24
      i64.store offset=72
      local.get $l4
      local.get $l5
      i64.load offset=40
      i64.store offset=88
      local.get $p0
      i32.load offset=76
      local.tee $l4
      local.get $p1
      local.get $l15
      i32.const 255
      i32.and
      i32.const 48
      i32.mul
      i32.add
      local.tee $l5
      i64.load offset=8
      i64.store offset=104
      local.get $l4
      local.get $l5
      i64.load offset=40
      i64.store offset=136
      local.get $l4
      local.get $l5
      i64.load
      i64.store offset=96
      local.get $l4
      local.get $l5
      i64.load offset=16
      i64.store offset=112
      local.get $l4
      local.get $l5
      i64.load offset=24
      i64.store offset=120
      local.get $l4
      local.get $l5
      i64.load offset=32
      i64.store offset=128
      local.get $p0
      i32.load offset=76
      local.tee $l4
      local.get $p1
      local.get $l6
      i32.const 255
      i32.and
      i32.const 48
      i32.mul
      i32.add
      local.tee $l5
      i64.load
      i64.store offset=144
      local.get $l4
      local.get $l5
      i64.load offset=8
      i64.store offset=152
      local.get $l4
      local.get $l5
      i64.load offset=16
      i64.store offset=160
      local.get $l4
      local.get $l5
      i64.load offset=24
      i64.store offset=168
      local.get $l4
      local.get $l5
      i64.load offset=32
      i64.store offset=176
      local.get $l4
      local.get $l5
      i64.load offset=40
      i64.store offset=184
    end)