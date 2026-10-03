  (func $f69979 (type $t3) (param $p0 i32) (param $p1 i32) (param $p2 i32) (result i32)
    (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32)
    local.get $p0
    i32.const 0
    i32.store8 offset=63
    local.get $p0
    i32.load8_u offset=62
    local.tee $l10
    if $I0
      loop $L1 (result i32)
        local.get $p0
        local.get $l4
        local.get $p0
        local.get $p0
        local.get $l9
        i32.add
        i32.load8_u offset=56
        i32.const 400
        i32.mul
        i32.add
        local.tee $l6
        i32.load offset=448
        local.tee $l8
        i32.add
        i32.store8 offset=63
        local.get $l6
        f32.load offset=104
        local.set $l12
        local.get $l6
        f32.load offset=100
        local.set $l13
        local.get $l6
        f32.load offset=96
        local.set $l14
        block $B2
          local.get $l8
          i32.const 2
          i32.lt_u
          br_if $B2
          i32.const 1
          local.set $l4
          local.get $l8
          i32.const 1
          i32.sub
          local.tee $l3
          i32.const 1
          i32.and
          local.set $l11
          local.get $l8
          i32.const 2
          i32.ne
          if $I3
            local.get $l3
            i32.const -2
            i32.and
            local.set $l7
            loop $L4
              local.get $l12
              local.get $l6
              local.get $l4
              i32.const 6
              i32.shl
              i32.add
              local.tee $l3
              f32.load offset=104
              f32.add
              local.get $l3
              f32.load offset=168
              f32.add
              local.set $l12
              local.get $l13
              local.get $l3
              f32.load offset=100
              f32.add
              local.get $l3
              f32.load offset=164
              f32.add
              local.set $l13
              local.get $l14
              local.get $l3
              f32.load offset=96
              f32.add
              local.get $l3
              f32.load offset=160
              f32.add
              local.set $l14
              local.get $l4
              i32.const 2
              i32.add
              local.set $l4
              local.get $l7
              i32.const 2
              i32.sub
              local.tee $l7
              br_if $L4
            end
          end
          local.get $l11
          i32.eqz
          br_if $B2
          local.get $l14
          local.get $l6
          local.get $l4
          i32.const 6
          i32.shl
          i32.add
          local.tee $l3
          f32.load offset=96
          f32.add
          local.set $l14
          local.get $l13
          local.get $l3
          f32.load offset=100
          f32.add
          local.set $l13
          local.get $l12
          local.get $l3
          f32.load offset=104
          f32.add
          local.set $l12
        end
        block $B5
          local.get $l8
          i32.eqz
          if $I6
            local.get $l5
            local.set $l3
            br $B5
          end
          local.get $l5
          i32.const 64
          i32.ge_u
          if $I7
            local.get $l5
            local.set $l3
            br $B5
          end
          local.get $p2
          f32.load offset=8
          local.tee $l17
          local.get $l14
          local.get $p2
          f32.load
          local.tee $l18
          f32.mul
          local.get $l13
          local.get $p2
          f32.load offset=4
          local.tee $l19
          f32.mul
          f32.add
          local.get $l12
          local.get $l17
          f32.mul
          f32.add
          local.tee $l20
          f32.mul
          local.get $p2
          f32.load offset=12
          local.tee $l15
          local.get $l13
          local.get $l18
          f32.mul
          local.get $l14
          local.get $l19
          f32.mul
          f32.sub
          f32.mul
          local.get $l12
          local.get $l15
          local.get $l15
          f32.mul
          f32.const -0x1p-1 (;=-0.5;)
          f32.add
          local.tee $l21
          f32.mul
          f32.add
          f32.add
          local.tee $l16
          local.get $l16
          f32.add
          local.tee $l16
          f32.const 0x1p+0 (;=1;)
          local.get $l16
          local.get $l16
          f32.mul
          local.get $l18
          local.get $l20
          f32.mul
          local.get $l15
          local.get $l12
          local.get $l19
          f32.mul
          local.get $l13
          local.get $l17
          f32.mul
          f32.sub
          f32.mul
          local.get $l14
          local.get $l21
          f32.mul
          f32.add
          f32.add
          local.tee $l16
          local.get $l16
          f32.add
          local.tee $l16
          local.get $l16
          f32.mul
          local.get $l19
          local.get $l20
          f32.mul
          local.get $l15
          local.get $l14
          local.get $l17
          f32.mul
          local.get $l12
          local.get $l18
          f32.mul
          f32.sub
          f32.mul
          local.get $l13
          local.get $l21
          f32.mul
          f32.add
          f32.add
          local.tee $l12
          local.get $l12
          f32.add
          local.tee $l12
          local.get $l12
          f32.mul
          f32.add
          f32.add
          f32.sqrt
          f32.div
          local.tee $l13
          f32.mul
          local.set $l23
          local.get $l12
          local.get $l13
          f32.mul
          local.set $l24
          local.get $l16
          local.get $l13
          f32.mul
          local.set $l25
          i32.const 0
          local.set $l7
          loop $L8
            block $B9
              local.get $l6
              local.get $l7
              i32.const 6
              i32.shl
              i32.add
              local.tee $l4
              f32.load offset=88
              local.set $l12
              local.get $l4
              f32.load offset=84
              local.set $l13
              local.get $l4
              f32.load offset=80
              local.set $l14
              local.get $l4
              f32.load offset=108
              local.set $l20
              local.get $p2
              f32.load offset=16
              local.set $l16
              local.get $p2
              f32.load offset=20
              local.set $l26
              local.get $p2
              f32.load offset=24
              local.set $l22
              local.get $p1
              local.get $l5
              i32.const 6
              i32.shl
              i32.add
              local.tee $l3
              i32.const 0
              i32.store offset=28
              local.get $l3
              local.get $l23
              f32.store offset=8
              local.get $l3
              local.get $l24
              f32.store offset=4
              local.get $l3
              local.get $l25
              f32.store
              local.get $l3
              local.get $l20
              f32.store offset=12
              local.get $l3
              local.get $l22
              local.get $l17
              local.get $l18
              local.get $l14
              f32.mul
              local.get $l19
              local.get $l13
              f32.mul
              f32.add
              local.get $l17
              local.get $l12
              f32.mul
              f32.add
              local.tee $l20
              f32.mul
              local.get $l12
              local.get $l15
              local.get $l15
              f32.mul
              f32.const -0x1p-1 (;=-0.5;)
              f32.add
              local.tee $l21
              f32.mul
              local.get $l15
              local.get $l18
              local.get $l13
              f32.mul
              local.get $l19
              local.get $l14
              f32.mul
              f32.sub
              f32.mul
              f32.add
              f32.add
              local.tee $l22
              local.get $l22
              f32.add
              f32.add
              f32.store offset=24
              local.get $l3
              local.get $l26
              local.get $l19
              local.get $l20
              f32.mul
              local.get $l21
              local.get $l13
              f32.mul
              local.get $l15
              local.get $l17
              local.get $l14
              f32.mul
              local.get $l18
              local.get $l12
              f32.mul
              f32.sub
              f32.mul
              f32.add
              f32.add
              local.tee $l22
              local.get $l22
              f32.add
              f32.add
              f32.store offset=20
              local.get $l3
              local.get $l16
              local.get $l18
              local.get $l20
              f32.mul
              local.get $l21
              local.get $l14
              f32.mul
              local.get $l15
              local.get $l19
              local.get $l12
              f32.mul
              local.get $l17
              local.get $l13
              f32.mul
              f32.sub
              f32.mul
              f32.add
              f32.add
              local.tee $l15
              local.get $l15
              f32.add
              f32.add
              f32.store offset=16
              local.get $l3
              local.get $l4
              i32.load offset=112
              i32.store offset=52
              local.get $l5
              i32.const 1
              i32.add
              local.set $l3
              local.get $l7
              i32.const 1
              i32.add
              local.tee $l7
              local.get $l8
              i32.ge_u
              br_if $B9
              local.get $l5
              i32.const 62
              i32.gt_u
              br_if $B9
              local.get $p2
              f32.load offset=12
              local.set $l15
              local.get $p2
              f32.load offset=8
              local.set $l17
              local.get $p2
              f32.load offset=4
              local.set $l19
              local.get $p2
              f32.load
              local.set $l18
              local.get $l3
              local.set $l5
              br $L8
            end
          end
          local.get $p0
          i32.load8_u offset=62
          local.set $l10
        end
        local.get $l10
        local.get $l9
        i32.const 1
        i32.add
        local.tee $l9
        i32.le_u
        if $I10 (result i32)
          local.get $l3
        else
          local.get $p0
          i32.load8_u offset=63
          local.set $l4
          local.get $l3
          local.set $l5
          br $L1
        end
      end
      local.set $l4
    end
    local.get $p1
    local.get $l4
    i32.store offset=4096
    local.get $l4
    i32.const 0
    i32.ne)
