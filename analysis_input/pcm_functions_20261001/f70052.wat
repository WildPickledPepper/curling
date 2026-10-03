  (func $f70052 (type $t2) (param $p0 i32) (param $p1 i32) (param $p2 i32)
    (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32)
    global.get $g0
    i32.const 32
    i32.sub
    local.tee $l3
    global.set $g0
    local.get $p0
    i32.const 2264
    i32.add
    f32.load
    local.set $l16
    local.get $p0
    i32.const 2260
    i32.add
    f32.load
    local.set $l17
    local.get $p0
    i32.const 2280
    i32.add
    f32.load
    local.set $l14
    local.get $p0
    i32.const 2272
    i32.add
    f32.load
    local.set $l18
    local.get $p0
    i32.const 2276
    i32.add
    f32.load
    local.set $l19
    local.get $p0
    i32.const 2296
    i32.add
    f32.load
    local.set $l12
    local.get $p0
    i32.const 2288
    i32.add
    f32.load
    local.set $l20
    local.get $p0
    i32.const 2292
    i32.add
    f32.load
    local.set $l21
    local.get $p0
    f32.load offset=2256
    local.set $l22
    local.get $p1
    f32.load offset=8
    local.set $l11
    local.get $p1
    f32.load
    local.set $l13
    local.get $p1
    f32.load offset=4
    local.set $l15
    local.get $l3
    i32.const 0
    i32.store offset=28
    local.get $l3
    local.get $l13
    local.get $l20
    f32.mul
    local.get $l15
    local.get $l21
    f32.mul
    f32.add
    local.get $l11
    local.get $l12
    f32.mul
    f32.add
    local.tee $l12
    f32.store offset=24
    local.get $l3
    local.get $l13
    local.get $l18
    f32.mul
    local.get $l15
    local.get $l19
    f32.mul
    f32.add
    local.get $l11
    local.get $l14
    f32.mul
    f32.add
    local.tee $l14
    f32.store offset=20
    local.get $l3
    local.get $l13
    local.get $l22
    f32.mul
    local.get $l15
    local.get $l17
    f32.mul
    f32.add
    local.get $l11
    local.get $l16
    f32.mul
    f32.add
    local.tee $l13
    f32.store offset=16
    local.get $p0
    i32.load offset=2324
    local.tee $l6
    local.get $p2
    i32.sub
    local.tee $p1
    i32.const 6
    i32.ge_u
    if $I0
      local.get $p0
      i32.load offset=2320
      local.get $p2
      i32.const 6
      i32.shl
      i32.add
      local.get $p1
      call $f69977
      local.get $p0
      local.get $p2
      i32.const 5
      i32.add
      local.tee $l6
      i32.store offset=2324
    end
    local.get $p2
    local.get $l6
    i32.lt_u
    if $I1
      local.get $p2
      local.set $l7
      loop $L2
        local.get $l7
        local.tee $l9
        i32.const 1
        i32.add
        local.tee $l7
        local.set $l5
        local.get $l6
        local.get $l7
        i32.gt_u
        if $I3
          loop $L4
            local.get $p0
            f32.load offset=2240
            local.get $p0
            i32.load offset=2320
            local.tee $l8
            local.get $l5
            i32.const 6
            i32.shl
            i32.add
            local.tee $p1
            f32.load offset=16
            local.get $l8
            local.get $l9
            i32.const 6
            i32.shl
            i32.add
            local.tee $l4
            f32.load offset=16
            f32.sub
            local.tee $l11
            local.get $l11
            f32.mul
            local.get $p1
            f32.load offset=20
            local.get $l4
            f32.load offset=20
            f32.sub
            local.tee $l11
            local.get $l11
            f32.mul
            f32.add
            local.get $p1
            i32.const 24
            i32.add
            local.tee $l10
            f32.load
            local.get $l4
            f32.load offset=24
            f32.sub
            local.tee $l11
            local.get $l11
            f32.mul
            f32.add
            f32.gt
            if $I5
              local.get $p1
              local.get $l6
              i32.const 6
              i32.shl
              local.get $l8
              i32.add
              i32.const -64
              i32.add
              local.tee $l4
              i64.load
              i64.store
              local.get $p1
              local.get $l4
              i32.load offset=48
              i32.store offset=48
              local.get $p1
              local.get $l4
              i64.load offset=40
              i64.store offset=40
              local.get $p1
              local.get $l4
              i64.load offset=32
              i64.store offset=32
              local.get $l10
              local.get $l4
              i64.load offset=24
              i64.store
              local.get $p1
              local.get $l4
              i64.load offset=16
              i64.store offset=16
              local.get $p1
              local.get $l4
              i64.load offset=8
              i64.store offset=8
              local.get $p0
              local.get $p0
              i32.load offset=2324
              i32.const 1
              i32.sub
              local.tee $l6
              i32.store offset=2324
              local.get $l5
              i32.const 1
              i32.sub
              local.set $l5
            end
            local.get $l5
            i32.const 1
            i32.add
            local.tee $l5
            local.get $l6
            i32.lt_u
            br_if $L4
          end
        end
        local.get $l6
        local.get $l7
        i32.gt_u
        br_if $L2
      end
    end
    local.get $l3
    i32.const 2139095039
    i32.store
    block $B6
      local.get $p2
      local.get $l6
      i32.ge_u
      br_if $B6
      local.get $p2
      local.set $l5
      loop $L7
        local.get $l5
        i32.const 6
        i32.shl
        local.tee $l4
        local.get $p0
        i32.load offset=2320
        i32.add
        local.tee $p1
        local.get $l13
        f32.store offset=32
        local.get $p1
        local.get $l12
        f32.store offset=40
        local.get $p1
        local.get $l14
        f32.store offset=36
        local.get $p1
        f32.load offset=44
        local.set $l11
        local.get $p0
        f32.load offset=2296
        local.set $l15
        local.get $p0
        f32.load offset=2292
        local.set $l16
        local.get $p0
        f32.load offset=2288
        local.set $l17
        local.get $p0
        f32.load offset=2280
        local.set $l18
        local.get $p0
        f32.load offset=2276
        local.set $l19
        local.get $p0
        f32.load offset=2272
        local.set $l20
        local.get $p0
        f32.load offset=2264
        local.set $l21
        local.get $p0
        f32.load offset=2312
        local.set $l13
        local.get $p0
        f32.load offset=2260
        local.set $l22
        local.get $p0
        f32.load offset=2308
        local.set $l14
        local.get $p0
        f32.load offset=2256
        local.set $l23
        local.get $p0
        f32.load offset=2304
        local.set $l12
        local.get $p0
        i32.load offset=2320
        local.get $l4
        i32.add
        local.tee $p1
        i32.const 0
        i32.store offset=28
        local.get $p1
        local.get $l23
        local.get $p1
        f32.load offset=16
        local.get $l12
        f32.sub
        local.tee $l12
        f32.mul
        local.get $l22
        local.get $p1
        i32.const 20
        i32.add
        local.tee $l4
        f32.load
        local.get $l14
        f32.sub
        local.tee $l14
        f32.mul
        f32.add
        local.get $l21
        local.get $p1
        i32.const 24
        i32.add
        local.tee $l8
        f32.load
        local.get $l13
        f32.sub
        local.tee $l13
        f32.mul
        f32.add
        f32.store offset=16
        local.get $l4
        local.get $l12
        local.get $l20
        f32.mul
        local.get $l14
        local.get $l19
        f32.mul
        f32.add
        local.get $l13
        local.get $l18
        f32.mul
        f32.add
        f32.store
        local.get $l8
        local.get $l12
        local.get $l17
        f32.mul
        local.get $l14
        local.get $l16
        f32.mul
        f32.add
        local.get $l13
        local.get $l15
        f32.mul
        f32.add
        f32.store
        local.get $l3
        local.get $l11
        local.get $l3
        f32.load
        local.tee $l12
        local.get $l11
        local.get $l12
        f32.lt
        select
        f32.store
        local.get $l5
        i32.const 1
        i32.add
        local.tee $l5
        local.get $p0
        i32.load offset=2324
        i32.ge_u
        br_if $B6
        local.get $l3
        f32.load offset=24
        local.set $l12
        local.get $l3
        f32.load offset=20
        local.set $l14
        local.get $l3
        f32.load offset=16
        local.set $l13
        br $L7
      end
      unreachable
    end
    local.get $p0
    local.get $l3
    i32.const 16
    i32.add
    local.get $l3
    local.get $p2
    call $f70053
    local.get $p0
    i32.load offset=2324
    i32.const 15
    i32.gt_u
    if $I8
      local.get $p0
      i32.const 6
      i32.const 1
      call $f70051
    end
    local.get $l3
    i32.const 32
    i32.add
    global.set $g0)
