  (func $f72606 (type $t2) (param $p0 i32) (param $p1 i32) (param $p2 i32)
    (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 f32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32)
    global.get $g0
    i32.const 32
    i32.sub
    local.tee $l4
    global.set $g0
    local.get $p0
    call $f71932
    local.set $l5
    local.get $p1
    f32.load offset=20
    local.set $l19
    local.get $p1
    f32.load offset=16
    local.set $l21
    local.get $p0
    i32.load offset=56
    i32.const 144
    i32.add
    local.get $p0
    i32.const 112
    i32.add
    local.get $p0
    i32.load offset=316
    local.tee $l6
    i32.const 1024
    i32.and
    select
    local.tee $l3
    f32.load offset=8
    local.set $l11
    local.get $l3
    f32.load offset=4
    local.set $l16
    local.get $l3
    f32.load offset=12
    local.set $l17
    local.get $l3
    f32.load
    local.set $l18
    local.get $l4
    local.get $p1
    f32.load offset=24
    local.get $p1
    f32.load offset=12
    local.tee $l7
    f32.const 0x1p+0 (;=1;)
    local.get $p1
    f32.load
    local.tee $l8
    local.get $l8
    f32.mul
    local.get $p1
    f32.load offset=4
    local.tee $l10
    local.get $l10
    f32.mul
    f32.add
    local.get $p1
    f32.load offset=8
    local.tee $l12
    local.get $l12
    f32.mul
    f32.add
    local.get $l7
    local.get $l7
    f32.mul
    f32.add
    f32.sqrt
    f32.div
    local.tee $l9
    f32.mul
    local.tee $l7
    local.get $l7
    f32.mul
    f32.const -0x1p-1 (;=-0.5;)
    f32.add
    local.tee $l20
    local.get $l3
    f32.load offset=24
    local.tee $l13
    local.get $l13
    f32.add
    local.tee $l13
    f32.mul
    local.get $l7
    local.get $l8
    local.get $l9
    f32.mul
    local.tee $l8
    local.get $l3
    f32.load offset=20
    local.tee $l14
    local.get $l14
    f32.add
    local.tee $l14
    f32.mul
    local.get $l10
    local.get $l9
    f32.mul
    local.tee $l10
    local.get $l3
    f32.load offset=16
    local.tee $l15
    local.get $l15
    f32.add
    local.tee $l15
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l12
    local.get $l9
    f32.mul
    local.tee $l9
    local.get $l8
    local.get $l15
    f32.mul
    local.get $l10
    local.get $l14
    f32.mul
    f32.add
    local.get $l9
    local.get $l13
    f32.mul
    f32.add
    local.tee $l12
    f32.mul
    f32.add
    f32.add
    local.tee $l22
    f32.store offset=24
    local.get $l4
    local.get $l19
    local.get $l10
    local.get $l12
    f32.mul
    local.get $l20
    local.get $l14
    f32.mul
    local.get $l7
    local.get $l9
    local.get $l15
    f32.mul
    local.get $l8
    local.get $l13
    f32.mul
    f32.sub
    f32.mul
    f32.add
    f32.add
    f32.add
    local.tee $l19
    f32.store offset=20
    local.get $l4
    local.get $l7
    local.get $l17
    f32.mul
    local.get $l8
    local.get $l18
    f32.mul
    f32.sub
    local.get $l10
    local.get $l16
    f32.mul
    f32.sub
    local.get $l9
    local.get $l11
    f32.mul
    f32.sub
    local.tee $l23
    f32.store offset=12
    local.get $l4
    local.get $l8
    local.get $l16
    f32.mul
    local.get $l9
    local.get $l17
    f32.mul
    local.get $l7
    local.get $l11
    f32.mul
    f32.add
    f32.add
    local.get $l10
    local.get $l18
    f32.mul
    f32.sub
    local.tee $l24
    f32.store offset=8
    local.get $l4
    local.get $l9
    local.get $l18
    f32.mul
    local.get $l10
    local.get $l17
    f32.mul
    local.get $l7
    local.get $l16
    f32.mul
    f32.add
    f32.add
    local.get $l8
    local.get $l11
    f32.mul
    f32.sub
    local.tee $l25
    f32.store offset=4
    local.get $l4
    local.get $l7
    local.get $l18
    f32.mul
    local.get $l8
    local.get $l17
    f32.mul
    f32.add
    local.get $l10
    local.get $l11
    f32.mul
    f32.add
    local.get $l9
    local.get $l16
    f32.mul
    f32.sub
    local.tee $l11
    f32.store
    local.get $l4
    local.get $l21
    local.get $l8
    local.get $l12
    f32.mul
    local.get $l20
    local.get $l15
    f32.mul
    local.get $l7
    local.get $l10
    local.get $l13
    f32.mul
    local.get $l9
    local.get $l14
    f32.mul
    f32.sub
    f32.mul
    f32.add
    f32.add
    f32.add
    local.tee $l7
    f32.store offset=16
    local.get $p0
    local.get $l22
    f32.store offset=280
    local.get $p0
    local.get $l19
    f32.store offset=276
    local.get $p0
    local.get $l7
    f32.store offset=272
    local.get $p0
    local.get $l23
    f32.store offset=268
    local.get $p0
    local.get $l24
    f32.store offset=264
    local.get $p0
    local.get $l25
    f32.store offset=260
    local.get $p0
    local.get $l11
    f32.store offset=256
    local.get $p0
    i32.const 48
    i32.add
    local.set $p1
    block $B0
      block $B1
        block $B2
          block $B3
            block $B4
              local.get $p0
              i32.load offset=52
              i32.const 30
              i32.shr_u
              i32.const 2
              i32.sub
              br_table $B4 $B2 $B3
            end
            local.get $p1
            i32.load
            local.tee $l3
            i32.load8_u offset=4785
            br_if $B1
          end
          local.get $p0
          i32.const -64
          i32.sub
          local.get $l4
          call $f71596
          br $B0
        end
        local.get $p1
        i32.load
        local.set $l3
      end
      local.get $p0
      local.get $l6
      i32.const -2097153
      i32.and
      i32.store offset=316
      local.get $l3
      local.get $p1
      call $f71985
      local.get $p0
      local.get $p0
      i32.load offset=316
      i32.const 1048576
      i32.or
      i32.store offset=316
    end
    local.get $l5
    if $I5
      local.get $p0
      i32.const 20
      i32.add
      local.get $l5
      i32.const 5584
      i32.add
      local.get $p0
      call $f72091
      local.get $l5
      i32.const 5652
      i32.add
      local.tee $l3
      local.get $l3
      i32.load
      i32.const 1
      i32.add
      i32.store
    end
    local.get $p0
    i32.load offset=40
    if $I6
      i32.const 4700888
      i32.load
      i32.const 8
      i32.const 3201780
      i32.const 102
      i32.const 3201824
      i32.const 0
      call $f69760
      local.get $p0
      i32.load offset=40
      local.get $p0
      call $f71821
    end
    block $B7
      local.get $l5
      i32.eqz
      br_if $B7
      local.get $p2
      i32.eqz
      br_if $B7
      local.get $p0
      i32.load offset=56
      local.tee $l5
      local.get $p0
      i32.load offset=52
      local.tee $l3
      i32.const 22
      i32.shr_u
      i32.const 60
      i32.and
      i32.const 3181092
      i32.add
      i32.load
      local.get $p1
      i32.add
      i32.const 8
      i32.add
      local.get $l3
      i32.const 1
      i32.and
      select
      i32.load8_u
      i32.const 8
      i32.and
      br_if $B7
      local.get $l5
      i32.const 268
      i32.add
      local.get $p0
      i32.const 108
      i32.add
      local.get $p0
      i32.load8_u offset=317
      i32.const 64
      i32.and
      select
      i32.load8_u
      i32.const 1
      i32.and
      br_if $B7
      local.get $p0
      call $f71931
      local.set $l3
      local.get $p0
      f32.load offset=308
      local.tee $l7
      local.get $l3
      i32.const 5148
      i32.add
      f32.load
      local.tee $l8
      f32.lt
      local.tee $l3
      i32.eqz
      if $I8
        local.get $p0
        i32.load offset=312
        i32.eqz
        br_if $B7
      end
      local.get $l8
      local.get $l7
      local.get $l3
      select
      local.set $l7
      block $B9
        block $B10
          block $B11
            block $B12
              local.get $p0
              i32.load offset=52
              i32.const 30
              i32.shr_u
              i32.const 2
              i32.sub
              br_table $B12 $B10 $B11
            end
            local.get $p1
            i32.load
            local.tee $l3
            i32.load8_u offset=4785
            br_if $B9
          end
          local.get $p0
          local.get $l7
          f32.store offset=308
          local.get $p0
          i32.const 0
          i32.store offset=312
          local.get $p0
          i32.const -64
          i32.sub
          local.get $l7
          i32.const 1
          call $f71618
          br $B7
        end
        local.get $p1
        i32.load
        local.set $l3
      end
      local.get $p0
      local.get $l7
      f32.store offset=308
      local.get $p0
      i32.const 0
      i32.store offset=312
      local.get $l3
      local.get $p1
      call $f71985
      local.get $p0
      local.get $p0
      i32.load offset=316
      i32.const -117440513
      i32.and
      i32.const 83886080
      i32.or
      i32.store offset=316
    end
    local.get $l4
    i32.const 32
    i32.add
    global.set $g0)