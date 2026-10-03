  (func $f71233 (type $t443) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 f32) (result i32)
    (local $l6 f32) (local $l7 f32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 i32) (local $l23 i32) (local $l24 i32) (local $l25 i32) (local $l26 i32)
    i32.const 1
    local.set $l22
    block $B0
      local.get $p1
      i32.eqz
      br_if $B0
      local.get $p2
      i32.eqz
      br_if $B0
      local.get $p0
      i32.const 7556
      i32.add
      local.set $l24
      i32.const 0
      local.set $l22
      loop $L1
        block $B2
          local.get $p1
          i32.load8_u
          br_if $B2
          local.get $p1
          i32.load16_u offset=2
          local.tee $l25
          i32.eqz
          br_if $B2
          local.get $p1
          i32.load8_u offset=1
          i32.const 2
          i32.and
          br_if $B2
          local.get $l22
          i32.const 1
          i32.and
          i32.eqz
          if $I3
            local.get $p3
            f32.load offset=12
            local.tee $l9
            local.get $l9
            f32.mul
            f32.const -0x1p-1 (;=-0.5;)
            f32.add
            local.tee $l11
            local.get $p4
            f32.load offset=24
            local.get $p3
            f32.load offset=24
            f32.sub
            local.tee $l12
            local.get $l12
            f32.add
            local.tee $l12
            f32.mul
            local.get $l9
            local.get $p3
            f32.load offset=4
            local.tee $l7
            local.get $p4
            f32.load offset=16
            local.get $p3
            f32.load offset=16
            f32.sub
            local.tee $l13
            local.get $l13
            f32.add
            local.tee $l13
            f32.mul
            local.get $p3
            f32.load
            local.tee $l8
            local.get $p4
            f32.load offset=20
            local.get $p3
            f32.load offset=20
            f32.sub
            local.tee $l6
            local.get $l6
            f32.add
            local.tee $l14
            f32.mul
            f32.sub
            f32.mul
            f32.add
            local.get $p3
            f32.load offset=8
            local.tee $l6
            local.get $l14
            local.get $l7
            f32.neg
            f32.mul
            local.get $l8
            local.get $l13
            f32.mul
            f32.sub
            local.get $l6
            local.get $l12
            f32.mul
            f32.sub
            local.tee $l10
            f32.mul
            f32.sub
            local.set $l19
            local.get $l11
            local.get $l14
            f32.mul
            local.get $l9
            local.get $l8
            local.get $l12
            f32.mul
            local.get $l6
            local.get $l13
            f32.mul
            f32.sub
            f32.mul
            f32.add
            local.get $l7
            local.get $l10
            f32.mul
            f32.sub
            local.set $l20
            local.get $l11
            local.get $l13
            f32.mul
            local.get $l9
            local.get $l6
            local.get $l14
            f32.mul
            local.get $l7
            local.get $l12
            f32.mul
            f32.sub
            f32.mul
            f32.add
            local.get $l8
            local.get $l10
            f32.mul
            f32.sub
            local.set $l21
            local.get $l6
            local.get $p4
            f32.load offset=8
            local.tee $l11
            f32.mul
            local.get $l8
            local.get $p4
            f32.load
            local.tee $l10
            f32.mul
            local.get $l9
            local.get $p4
            f32.load offset=12
            local.tee $l15
            f32.mul
            f32.add
            local.get $l7
            local.get $p4
            f32.load offset=4
            local.tee $l16
            f32.mul
            f32.add
            f32.add
            local.set $l14
            local.get $l7
            local.get $l10
            f32.mul
            local.get $l9
            local.get $l11
            f32.mul
            local.get $l6
            local.get $l15
            f32.mul
            f32.sub
            local.get $l8
            local.get $l16
            f32.mul
            f32.sub
            f32.add
            local.set $l12
            local.get $l8
            local.get $l11
            f32.mul
            local.get $l9
            local.get $l16
            f32.mul
            local.get $l7
            local.get $l15
            f32.mul
            f32.sub
            local.get $l6
            local.get $l10
            f32.mul
            f32.sub
            f32.add
            local.set $l13
            local.get $l9
            local.get $l10
            f32.mul
            local.get $l8
            local.get $l15
            f32.mul
            f32.sub
            local.get $l7
            local.get $l11
            f32.mul
            f32.sub
            local.get $l6
            local.get $l16
            f32.mul
            f32.add
            local.set $l9
          end
          i32.const 1
          local.set $l22
          local.get $p1
          f32.load offset=24
          local.tee $l15
          local.get $l14
          local.get $l14
          f32.mul
          f32.const -0x1p-1 (;=-0.5;)
          f32.add
          local.tee $l11
          local.get $p1
          f32.load offset=36
          local.tee $l7
          local.get $l7
          f32.add
          local.tee $l7
          f32.mul
          local.get $l14
          local.get $l9
          local.get $p1
          f32.load offset=32
          local.tee $l8
          local.get $l8
          f32.add
          local.tee $l8
          f32.mul
          local.get $l13
          local.get $p1
          f32.load offset=28
          local.tee $l6
          local.get $l6
          f32.add
          local.tee $l6
          f32.mul
          f32.sub
          f32.mul
          f32.add
          local.get $l12
          local.get $l9
          local.get $l6
          f32.mul
          local.get $l13
          local.get $l8
          f32.mul
          f32.add
          local.get $l12
          local.get $l7
          f32.mul
          f32.add
          local.tee $l10
          f32.mul
          f32.add
          f32.mul
          local.get $p1
          f32.load offset=16
          local.tee $l16
          local.get $l9
          local.get $l10
          f32.mul
          local.get $l11
          local.get $l6
          f32.mul
          local.get $l14
          local.get $l13
          local.get $l7
          f32.mul
          local.get $l12
          local.get $l8
          f32.mul
          f32.sub
          f32.mul
          f32.add
          f32.add
          f32.mul
          local.get $p1
          f32.load offset=20
          local.tee $l17
          local.get $l13
          local.get $l10
          f32.mul
          local.get $l11
          local.get $l8
          f32.mul
          local.get $l14
          local.get $l12
          local.get $l6
          f32.mul
          local.get $l9
          local.get $l7
          f32.mul
          f32.sub
          f32.mul
          f32.add
          f32.add
          f32.mul
          f32.add
          f32.add
          f32.const 0x1.ff7ceep-1 (;=0.999;)
          f32.gt
          i32.eqz
          br_if $B2
          i32.const 0
          local.set $l23
          i32.const 1
          local.set $l26
          loop $L4
            local.get $p5
            local.get $l15
            local.get $p1
            local.get $l23
            i32.const 12
            i32.mul
            i32.add
            local.tee $l22
            f32.load offset=48
            local.get $l19
            local.get $l11
            local.get $l22
            f32.load offset=72
            local.tee $l7
            local.get $l7
            f32.add
            local.tee $l7
            f32.mul
            local.get $l14
            local.get $l9
            local.get $l22
            f32.load offset=68
            local.tee $l8
            local.get $l8
            f32.add
            local.tee $l8
            f32.mul
            local.get $l13
            local.get $l22
            i32.const -64
            i32.sub
            f32.load
            local.tee $l6
            local.get $l6
            f32.add
            local.tee $l6
            f32.mul
            f32.sub
            f32.mul
            f32.add
            local.get $l12
            local.get $l9
            local.get $l6
            f32.mul
            local.get $l13
            local.get $l8
            f32.mul
            f32.add
            local.get $l12
            local.get $l7
            f32.mul
            f32.add
            local.tee $l10
            f32.mul
            f32.add
            f32.add
            f32.sub
            f32.mul
            local.get $l16
            local.get $l22
            f32.load offset=40
            local.get $l21
            local.get $l9
            local.get $l10
            f32.mul
            local.get $l11
            local.get $l6
            f32.mul
            local.get $l14
            local.get $l13
            local.get $l7
            f32.mul
            local.get $l12
            local.get $l8
            f32.mul
            f32.sub
            f32.mul
            f32.add
            f32.add
            f32.add
            f32.sub
            f32.mul
            local.get $l17
            local.get $l22
            f32.load offset=44
            local.get $l20
            local.get $l13
            local.get $l10
            f32.mul
            local.get $l11
            local.get $l8
            f32.mul
            local.get $l14
            local.get $l12
            local.get $l6
            f32.mul
            local.get $l9
            local.get $l7
            f32.mul
            f32.sub
            f32.mul
            f32.add
            f32.add
            f32.add
            f32.sub
            f32.mul
            f32.add
            f32.add
            f32.abs
            f32.gt
            if $I5
              local.get $l23
              i32.const 1
              i32.add
              local.tee $l23
              local.get $l25
              i32.lt_u
              local.set $l26
              local.get $l23
              local.get $l25
              i32.ne
              br_if $L4
            end
          end
          i32.const 1
          local.set $l22
          local.get $l26
          br_if $B2
          local.get $p0
          i32.load offset=7688
          local.tee $l22
          i32.const 32
          i32.eq
          if $I6
            i32.const 0
            return
          end
          local.get $l24
          local.get $l22
          i32.const 2
          i32.shl
          i32.add
          i32.const 65535
          i32.store16
          local.get $l24
          local.get $p0
          i32.load offset=7688
          i32.const 2
          i32.shl
          i32.add
          i32.const 65535
          i32.store16 offset=2
          local.get $p0
          local.get $p0
          i32.load offset=7688
          i32.const 12
          i32.mul
          i32.add
          local.tee $l22
          i32.const 6152
          i32.add
          local.get $p1
          f32.load offset=24
          local.tee $l7
          local.get $l7
          f32.add
          local.tee $l8
          local.get $p3
          f32.load offset=12
          local.tee $l7
          local.get $l7
          f32.mul
          f32.const -0x1p-1 (;=-0.5;)
          f32.add
          local.tee $l17
          f32.mul
          local.get $l7
          local.get $p1
          f32.load offset=20
          local.tee $l6
          local.get $l6
          f32.add
          local.tee $l6
          local.get $p3
          f32.load
          local.tee $l11
          f32.mul
          local.get $p1
          f32.load offset=16
          local.tee $l10
          local.get $l10
          f32.add
          local.tee $l10
          local.get $p3
          f32.load offset=4
          local.tee $l15
          f32.mul
          f32.sub
          f32.mul
          f32.add
          local.get $p3
          f32.load offset=8
          local.tee $l16
          local.get $l10
          local.get $l11
          f32.mul
          local.get $l6
          local.get $l15
          f32.mul
          f32.add
          local.get $l8
          local.get $l16
          f32.mul
          f32.add
          local.tee $l18
          f32.mul
          f32.add
          f32.store
          local.get $l22
          i32.const 6148
          i32.add
          local.get $l15
          local.get $l18
          f32.mul
          local.get $l6
          local.get $l17
          f32.mul
          local.get $l7
          local.get $l10
          local.get $l16
          f32.mul
          local.get $l8
          local.get $l11
          f32.mul
          f32.sub
          f32.mul
          f32.add
          f32.add
          f32.store
          local.get $l22
          i32.const 6144
          i32.add
          local.get $l11
          local.get $l18
          f32.mul
          local.get $l10
          local.get $l17
          f32.mul
          local.get $l7
          local.get $l8
          local.get $l15
          f32.mul
          local.get $l6
          local.get $l16
          f32.mul
          f32.sub
          f32.mul
          f32.add
          f32.add
          f32.store
          local.get $p0
          local.get $p0
          i32.load offset=7688
          i32.const 2
          i32.shl
          i32.add
          i32.const 7296
          i32.add
          i32.const 0
          i32.store
          local.get $p0
          local.get $p0
          i32.load offset=7688
          i32.const 24
          i32.mul
          i32.add
          local.tee $l22
          i32.const 6544
          i32.add
          i64.const -108086391082057729
          i64.store
          local.get $l22
          i32.const 6536
          i32.add
          i64.const -108086393229541377
          i64.store
          local.get $l22
          i32.const 6528
          i32.add
          i64.const 9115285643625234431
          i64.store
          local.get $p0
          local.get $p0
          i32.load offset=7688
          i32.const 2
          i32.shl
          i32.add
          i32.const 7424
          i32.add
          i32.const 65535
          i32.store
          i32.const 1
          local.set $l22
          local.get $p0
          local.get $p0
          i32.load offset=7688
          local.tee $l23
          i32.const 1
          i32.add
          i32.store offset=7688
          local.get $p0
          local.get $l23
          i32.const 104
          i32.mul
          i32.add
          i32.const 2816
          i32.add
          local.get $p1
          i32.const 104
          call $f483
          drop
        end
        local.get $p1
        i32.const 104
        i32.add
        local.set $p1
        local.get $p2
        i32.const 1
        i32.sub
        local.tee $p2
        br_if $L1
      end
      i32.const 1
      local.set $l22
    end
    local.get $l22)