  (func $f70517 (type $t15) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 i32)
    (local $l7 f32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 i32)
    global.get $g0
    i32.const 32
    i32.sub
    local.tee $l27
    global.set $g0
    block $B0
      block $B1
        block $B2
          block $B3
            local.get $p6
            i32.const 1
            i32.sub
            br_table $B3 $B2 $B1 $B0
          end
          local.get $p4
          local.get $p1
          i64.load
          i64.store
          local.get $p4
          local.get $p1
          i64.load offset=8
          i64.store offset=8
          local.get $p5
          local.get $p2
          i64.load
          i64.store
          local.get $p5
          local.get $p2
          i64.load offset=8
          i64.store offset=8
          br $B0
        end
        local.get $l27
        i32.const 16
        i32.add
        local.get $p0
        i32.const 16
        i32.add
        local.tee $p6
        f32.load offset=4
        local.get $p3
        f32.load offset=4
        local.tee $l7
        f32.sub
        local.get $p0
        f32.load offset=4
        local.get $l7
        f32.sub
        local.tee $l8
        f32.sub
        local.tee $l7
        local.get $l8
        f32.neg
        f32.mul
        local.get $p0
        f32.load
        local.get $p3
        f32.load
        local.tee $l8
        f32.sub
        local.tee $l9
        local.get $p6
        f32.load
        local.get $l8
        f32.sub
        local.get $l9
        f32.sub
        local.tee $l8
        f32.mul
        f32.sub
        local.get $p0
        f32.load offset=8
        local.get $p3
        f32.load offset=8
        local.tee $l9
        f32.sub
        local.tee $l10
        local.get $p6
        f32.load offset=8
        local.get $l9
        f32.sub
        local.get $l10
        f32.sub
        local.tee $l9
        f32.mul
        f32.sub
        f32.const 0x1p+0 (;=1;)
        local.get $l8
        local.get $l8
        f32.mul
        local.get $l7
        local.get $l7
        f32.mul
        f32.add
        local.get $l9
        local.get $l9
        f32.mul
        f32.add
        local.tee $l7
        f32.div
        f32.const 0x0p+0 (;=0;)
        local.get $l7
        f32.const 0x0p+0 (;=0;)
        f32.gt
        select
        f32.mul
        f32.store
        local.get $p2
        f32.load offset=20
        local.set $l14
        local.get $p2
        f32.load offset=24
        local.set $l15
        local.get $p1
        f32.load offset=20
        local.set $l16
        local.get $p1
        f32.load offset=24
        local.set $l17
        local.get $p2
        f32.load
        local.set $l8
        local.get $p2
        f32.load offset=16
        local.set $l18
        local.get $p2
        f32.load offset=4
        local.set $l9
        local.get $p2
        f32.load offset=8
        local.set $l10
        local.get $p1
        f32.load
        local.set $l11
        local.get $p1
        f32.load offset=16
        local.set $l19
        local.get $p1
        f32.load offset=4
        local.set $l12
        local.get $p1
        f32.load offset=8
        local.set $l13
        local.get $l27
        f32.load offset=16
        local.set $l7
        local.get $p4
        i32.const 0
        i32.store offset=12
        local.get $p4
        local.get $l13
        local.get $l7
        local.get $l17
        local.get $l13
        f32.sub
        f32.mul
        f32.add
        f32.store offset=8
        local.get $p4
        local.get $l12
        local.get $l7
        local.get $l16
        local.get $l12
        f32.sub
        f32.mul
        f32.add
        f32.store offset=4
        local.get $p4
        local.get $l11
        local.get $l7
        local.get $l19
        local.get $l11
        f32.sub
        f32.mul
        f32.add
        f32.store
        local.get $p5
        i32.const 0
        i32.store offset=12
        local.get $p5
        local.get $l10
        local.get $l7
        local.get $l15
        local.get $l10
        f32.sub
        f32.mul
        f32.add
        f32.store offset=8
        local.get $p5
        local.get $l9
        local.get $l7
        local.get $l14
        local.get $l9
        f32.sub
        f32.mul
        f32.add
        f32.store offset=4
        local.get $p5
        local.get $l8
        local.get $l7
        local.get $l18
        local.get $l8
        f32.sub
        f32.mul
        f32.add
        f32.store
        br $B0
      end
      local.get $p3
      local.get $p0
      local.get $p0
      i32.const 16
      i32.add
      local.get $p0
      i32.const 32
      i32.add
      local.get $l27
      i32.const 16
      i32.add
      local.get $l27
      call $f69896
      local.get $p2
      f32.load offset=20
      local.set $l15
      local.get $p2
      f32.load offset=36
      local.set $l16
      local.get $p2
      f32.load offset=24
      local.set $l17
      local.get $p2
      f32.load offset=40
      local.set $l18
      local.get $p1
      f32.load offset=20
      local.set $l19
      local.get $p1
      f32.load offset=36
      local.set $l20
      local.get $p1
      f32.load offset=24
      local.set $l21
      local.get $p1
      f32.load offset=40
      local.set $l22
      local.get $p2
      f32.load offset=16
      local.set $l23
      local.get $p2
      f32.load offset=32
      local.set $l24
      local.get $p2
      f32.load
      local.set $l9
      local.get $p2
      f32.load offset=4
      local.set $l10
      local.get $p2
      f32.load offset=8
      local.set $l11
      local.get $p1
      f32.load offset=16
      local.set $l25
      local.get $p1
      f32.load offset=32
      local.set $l26
      local.get $p1
      f32.load
      local.set $l12
      local.get $p1
      f32.load offset=4
      local.set $l13
      local.get $p1
      f32.load offset=8
      local.set $l14
      local.get $l27
      f32.load offset=16
      local.set $l7
      local.get $l27
      f32.load
      local.set $l8
      local.get $p4
      i32.const 0
      i32.store offset=12
      local.get $p4
      local.get $l14
      local.get $l7
      local.get $l21
      local.get $l14
      f32.sub
      f32.mul
      local.get $l8
      local.get $l22
      local.get $l14
      f32.sub
      f32.mul
      f32.add
      f32.add
      f32.store offset=8
      local.get $p4
      local.get $l13
      local.get $l7
      local.get $l19
      local.get $l13
      f32.sub
      f32.mul
      local.get $l8
      local.get $l20
      local.get $l13
      f32.sub
      f32.mul
      f32.add
      f32.add
      f32.store offset=4
      local.get $p4
      local.get $l12
      local.get $l7
      local.get $l25
      local.get $l12
      f32.sub
      f32.mul
      local.get $l8
      local.get $l26
      local.get $l12
      f32.sub
      f32.mul
      f32.add
      f32.add
      f32.store
      local.get $p5
      i32.const 0
      i32.store offset=12
      local.get $p5
      local.get $l11
      local.get $l7
      local.get $l17
      local.get $l11
      f32.sub
      f32.mul
      local.get $l8
      local.get $l18
      local.get $l11
      f32.sub
      f32.mul
      f32.add
      f32.add
      f32.store offset=8
      local.get $p5
      local.get $l10
      local.get $l7
      local.get $l15
      local.get $l10
      f32.sub
      f32.mul
      local.get $l8
      local.get $l16
      local.get $l10
      f32.sub
      f32.mul
      f32.add
      f32.add
      f32.store offset=4
      local.get $p5
      local.get $l9
      local.get $l7
      local.get $l23
      local.get $l9
      f32.sub
      f32.mul
      local.get $l8
      local.get $l24
      local.get $l9
      f32.sub
      f32.mul
      f32.add
      f32.add
      f32.store
    end
    local.get $l27
    i32.const 32
    i32.add
    global.set $g0)