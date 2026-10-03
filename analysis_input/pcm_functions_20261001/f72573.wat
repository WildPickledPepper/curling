  (func $f72573 (type $t10) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (result i32)
    (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 i32) (local $l17 i32)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $p0
    global.set $g0
    local.get $p0
    local.get $p5
    i32.load8_u
    i32.store8 offset=8
    i32.const 4702092
    i32.load
    local.set $l13
    local.get $p1
    local.set $p5
    local.get $p0
    i32.const 8
    i32.add
    local.set $l10
    global.get $g0
    i32.const 32
    i32.sub
    local.tee $l6
    global.set $g0
    local.get $l6
    i64.const 17179869184
    i64.store offset=16
    local.get $l6
    local.get $l6
    i32.store offset=12
    local.get $l6
    i32.const 1
    i32.store8 offset=8
    local.get $l6
    i32.const 0
    i32.store16 offset=24
    local.get $l6
    i32.const 24
    i32.add
    local.set $l14
    local.get $p3
    local.get $l6
    i32.load offset=20
    i32.const 2147483647
    i32.and
    i32.gt_u
    if $I0
      block $B1 (result i32)
        i32.const 0
        local.get $p3
        i32.eqz
        br_if $B1
        drop
        block $B2
          local.get $p3
          i32.const 1
          i32.shl
          local.tee $l7
          i32.const 8
          i32.gt_u
          br_if $B2
          local.get $l6
          i32.load8_u offset=8
          br_if $B2
          local.get $l6
          i32.const 1
          i32.store8 offset=8
          local.get $l6
          br $B1
        end
        i32.const 0
        local.get $l7
        i32.eqz
        br_if $B1
        drop
        call $f69753
        local.tee $p1
        local.get $l7
        i32.const 3194490
        i32.const 3188706
        i32.const 4700888
        i32.load
        local.tee $l11
        local.get $l11
        i32.load
        i32.load offset=20
        call_indirect $__indirect_function_table (type $t5)
        select
        i32.const 3188664
        i32.const 553
        local.get $p1
        i32.load
        i32.load offset=8
        call_indirect $__indirect_function_table (type $t9)
      end
      local.set $l8
      local.get $l6
      i32.load offset=16
      local.tee $l7
      i32.const 0
      i32.gt_s
      if $I3
        local.get $l8
        local.get $l7
        i32.const 1
        i32.shl
        i32.add
        local.set $l11
        local.get $l6
        i32.load offset=12
        local.set $l7
        local.get $l8
        local.set $p1
        loop $L4
          local.get $p1
          local.get $l7
          i32.load16_u
          i32.store16
          local.get $l7
          i32.const 2
          i32.add
          local.set $l7
          local.get $p1
          i32.const 2
          i32.add
          local.tee $p1
          local.get $l11
          i32.lt_u
          br_if $L4
        end
      end
      block $B5
        local.get $l6
        i32.load offset=20
        i32.const 0
        i32.lt_s
        br_if $B5
        local.get $l6
        i32.load offset=12
        local.tee $l7
        local.get $l6
        i32.eq
        if $I6
          local.get $l6
          i32.const 0
          i32.store8 offset=8
          br $B5
        end
        local.get $l7
        i32.eqz
        br_if $B5
        call $f69753
        local.tee $p1
        local.get $l7
        local.get $p1
        i32.load
        i32.load offset=12
        call_indirect $__indirect_function_table (type $t1)
      end
      local.get $l6
      local.get $p3
      i32.store offset=20
      local.get $l6
      local.get $l8
      i32.store offset=12
    end
    local.get $p3
    local.get $l6
    i32.load offset=16
    local.tee $p1
    i32.gt_s
    if $I7
      local.get $l6
      i32.load offset=12
      local.tee $l8
      local.get $p3
      i32.const 1
      i32.shl
      i32.add
      local.set $l7
      local.get $l8
      local.get $p1
      i32.const 1
      i32.shl
      i32.add
      local.set $p1
      loop $L8
        local.get $p1
        local.get $l14
        i32.load16_u
        i32.store16
        local.get $p1
        i32.const 2
        i32.add
        local.tee $p1
        local.get $l7
        i32.lt_u
        br_if $L8
      end
    end
    local.get $l6
    local.get $p3
    i32.store offset=16
    block $B9
      local.get $p3
      i32.const 1
      i32.eq
      if $I10
        local.get $l6
        i32.load offset=12
        local.get $p2
        i32.load
        i32.load16_u offset=52
        i32.store16
        br $B9
      end
      local.get $p3
      i32.eqz
      br_if $B9
      local.get $l6
      i32.load offset=12
      local.set $p1
      local.get $p3
      i32.const 3
      i32.and
      local.set $l8
      local.get $p3
      i32.const 1
      i32.sub
      i32.const 3
      i32.ge_u
      if $I11
        local.get $p3
        i32.const 65532
        i32.and
        local.set $l14
        loop $L12
          local.get $p1
          local.get $l9
          i32.const 1
          i32.shl
          i32.add
          local.get $p2
          local.get $l9
          i32.const 2
          i32.shl
          i32.add
          i32.load
          i32.load16_u offset=52
          i32.store16
          local.get $p1
          local.get $l9
          i32.const 1
          i32.or
          local.tee $l7
          i32.const 1
          i32.shl
          i32.add
          local.get $p2
          local.get $l7
          i32.const 2
          i32.shl
          i32.add
          i32.load
          i32.load16_u offset=52
          i32.store16
          local.get $p1
          local.get $l9
          i32.const 2
          i32.or
          local.tee $l7
          i32.const 1
          i32.shl
          i32.add
          local.get $p2
          local.get $l7
          i32.const 2
          i32.shl
          i32.add
          i32.load
          i32.load16_u offset=52
          i32.store16
          local.get $p1
          local.get $l9
          i32.const 3
          i32.or
          local.tee $l7
          i32.const 1
          i32.shl
          i32.add
          local.get $p2
          local.get $l7
          i32.const 2
          i32.shl
          i32.add
          i32.load
          i32.load16_u offset=52
          i32.store16
          local.get $l9
          i32.const 4
          i32.add
          local.set $l9
          local.get $l14
          i32.const 4
          i32.sub
          local.tee $l14
          br_if $L12
        end
      end
      local.get $l8
      i32.eqz
      br_if $B9
      loop $L13
        local.get $p1
        local.get $l9
        i32.const 1
        i32.shl
        i32.add
        local.get $p2
        local.get $l9
        i32.const 2
        i32.shl
        i32.add
        i32.load
        i32.load16_u offset=52
        i32.store16
        local.get $l9
        i32.const 1
        i32.add
        local.set $l9
        local.get $l8
        i32.const 1
        i32.sub
        local.tee $l8
        br_if $L13
      end
    end
    local.get $l13
    i32.load offset=1564
    drop
    local.get $l6
    i32.load offset=12
    local.set $l9
    local.get $l13
    i32.const 1560
    i32.add
    i32.load
    local.tee $p2
    i32.eqz
    if $I14
      global.get $g0
      i32.const 16
      i32.sub
      local.tee $l14
      global.set $g0
      local.get $l14
      local.get $l13
      i32.const 1272
      i32.add
      local.tee $l8
      i32.load offset=284
      local.tee $p2
      if $I15 (result i32)
        call $f69753
        local.tee $p1
        local.get $p2
        i32.const 3190412
        i32.const 3188706
        i32.const 4700888
        i32.load
        local.tee $p2
        local.get $p2
        i32.load
        i32.load offset=20
        call_indirect $__indirect_function_table (type $t5)
        select
        i32.const 3189274
        i32.const 180
        local.get $p1
        i32.load
        i32.load offset=8
        call_indirect $__indirect_function_table (type $t9)
      else
        i32.const 0
      end
      local.tee $l7
      i32.store offset=12
      block $B16
        local.get $l8
        i32.load offset=268
        local.tee $p2
        local.get $l8
        i32.load offset=272
        i32.const 2147483647
        i32.and
        i32.ge_u
        if $I17
          local.get $l14
          i32.const 12
          i32.add
          local.set $l17
          block $B18 (result i32)
            i32.const 0
            local.get $l8
            i32.const 4
            i32.add
            local.tee $l11
            i32.load offset=268
            i32.const 2147483647
            i32.and
            local.tee $l12
            i32.const 1
            i32.shl
            i32.const 1
            local.get $l12
            select
            local.tee $l16
            i32.eqz
            br_if $B18
            drop
            block $B19
              local.get $l16
              i32.const 2
              i32.shl
              local.tee $l12
              i32.const 256
              i32.gt_u
              br_if $B19
              local.get $l11
              i32.load8_u offset=256
              br_if $B19
              local.get $l11
              i32.const 1
              i32.store8 offset=256
              local.get $l11
              br $B18
            end
            i32.const 0
            local.get $l12
            i32.eqz
            br_if $B18
            drop
            call $f69753
            local.tee $p2
            local.get $l12
            i32.const 3190412
            i32.const 3188706
            i32.const 4700888
            i32.load
            local.tee $l15
            local.get $l15
            i32.load
            i32.load offset=20
            call_indirect $__indirect_function_table (type $t5)
            select
            i32.const 3188664
            i32.const 553
            local.get $p2
            i32.load
            i32.load offset=8
            call_indirect $__indirect_function_table (type $t9)
          end
          local.set $p1
          local.get $p1
          local.get $l11
          i32.load offset=264
          local.tee $l12
          i32.const 0
          i32.gt_s
          if $I20 (result i32)
            local.get $p1
            local.get $l12
            i32.const 2
            i32.shl
            i32.add
            local.set $l15
            local.get $l11
            i32.load offset=260
            local.set $l12
            local.get $p1
            local.set $p2
            loop $L21
              local.get $p2
              local.get $l12
              i32.load
              i32.store
              local.get $l12
              i32.const 4
              i32.add
              local.set $l12
              local.get $p2
              i32.const 4
              i32.add
              local.tee $p2
              local.get $l15
              i32.lt_u
              br_if $L21
            end
            local.get $l11
            i32.load offset=264
          else
            local.get $l12
          end
          i32.const 2
          i32.shl
          i32.add
          local.get $l17
          i32.load
          i32.store
          block $B22
            local.get $l11
            i32.load offset=268
            i32.const 0
            i32.lt_s
            br_if $B22
            local.get $l11
            i32.load offset=260
            local.tee $l12
            local.get $l11
            i32.eq
            if $I23
              local.get $l11
              i32.const 0
              i32.store8 offset=256
              br $B22
            end
            local.get $l12
            i32.eqz
            br_if $B22
            call $f69753
            local.tee $p2
            local.get $l12
            local.get $p2
            i32.load
            i32.load offset=12
            call_indirect $__indirect_function_table (type $t1)
          end
          local.get $l11
          local.get $l16
          i32.store offset=268
          local.get $l11
          local.get $p1
          i32.store offset=260
          local.get $l11
          local.get $l11
          i32.load offset=264
          i32.const 1
          i32.add
          i32.store offset=264
          br $B16
        end
        local.get $l8
        i32.load offset=264
        local.get $p2
        i32.const 2
        i32.shl
        i32.add
        local.get $l7
        i32.store
        local.get $l8
        local.get $l8
        i32.load offset=268
        i32.const 1
        i32.add
        i32.store offset=268
      end
      local.get $l7
      local.get $l7
      local.get $l8
      i32.load offset=276
      i32.const 208
      i32.mul
      i32.add
      i32.const 208
      i32.sub
      local.tee $p2
      i32.le_u
      if $I24
        local.get $l8
        i32.load offset=288
        local.set $p1
        loop $L25
          local.get $p2
          local.get $p1
          i32.store
          local.get $l8
          local.get $p2
          i32.store offset=288
          local.get $p2
          local.set $p1
          local.get $p2
          i32.const 208
          i32.sub
          local.tee $p2
          local.get $l7
          i32.ge_u
          br_if $L25
        end
      end
      local.get $l14
      i32.const 16
      i32.add
      global.set $g0
      local.get $l13
      i32.load offset=1560
      local.set $p2
    end
    local.get $l13
    local.get $p2
    i32.load
    i32.store offset=1560
    local.get $l13
    i32.const 1552
    i32.add
    local.tee $p1
    local.get $p1
    i32.load
    i32.const 1
    i32.add
    i32.store
    local.get $l6
    local.get $l10
    i32.load8_u
    i32.store8 offset=24
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $p1
    global.set $g0
    local.get $p2
    i64.const 196615
    i64.store offset=4 align=4
    local.get $p2
    i32.const 0
    i32.store offset=20
    local.get $p2
    i32.const 3180084
    i32.store offset=12
    local.get $p2
    i32.const 3179892
    i32.store
    local.get $p2
    i32.const 1
    i32.store offset=16
    local.get $l6
    i32.load8_u offset=24
    local.set $l10
    local.get $p2
    i32.const 0
    i32.store offset=40
    local.get $p2
    i64.const 0
    i64.store offset=32 align=4
    local.get $p1
    local.get $l10
    i32.store8 offset=8
    local.get $p2
    i32.const 48
    i32.add
    local.tee $l10
    i64.const 0
    i64.store align=4
    local.get $l10
    i32.const 0
    i32.store offset=136
    local.get $l10
    i64.const 0
    i64.store offset=128
    local.get $l10
    i64.const 0
    i64.store offset=24 align=4
    local.get $l10
    i64.const 0
    i64.store offset=16 align=4
    local.get $l10
    i64.const 0
    i64.store offset=8 align=4
    local.get $l10
    i32.const 68
    i32.add
    local.tee $l8
    i32.const -1
    i32.store
    local.get $l10
    i32.const 1
    i32.store8 offset=65
    i32.const 4702088
    i32.load
    local.set $l7
    local.get $l8
    local.get $p5
    call $f70398
    local.get $l10
    i32.const 0
    i32.store offset=56
    local.get $l10
    i64.const 0
    i64.store offset=48 align=4
    local.get $l10
    i64.const 4575657221408423936
    i64.store offset=40 align=4
    local.get $l10
    i64.const 0
    i64.store offset=32 align=4
    local.get $l10
    local.get $l7
    f32.load
    f32.const 0x1.47ae14p-6 (;=0.02;)
    f32.mul
    f32.store offset=60
    local.get $l10
    i32.const -64
    i32.sub
    local.get $p1
    i32.load8_u offset=8
    i32.store8
    local.get $l10
    local.get $l9
    local.get $p3
    call $f71448
    local.get $p2
    i32.const 36
    i32.add
    local.tee $p5
    local.get $p5
    i32.load
    local.tee $p5
    i32.const -251658241
    i32.and
    i32.const 16777216
    i32.const 33554432
    local.get $p4
    select
    i32.or
    i32.store
    local.get $p2
    i32.const -2147483648
    i32.const 0
    local.get $p4
    select
    i32.store offset=196
    local.get $p2
    i32.const 0
    i32.store offset=192
    local.get $p2
    i32.const 0
    i32.store offset=8
    block $B26
      block $B27 (result i32)
        block $B28
          block $B29
            block $B30
              local.get $p2
              i32.const 116
              i32.add
              local.tee $p4
              i32.load
              i32.const 4
              i32.sub
              br_table $B30 $B28 $B29 $B26
            end
            local.get $p5
            i32.const 1
            i32.and
            if $I31 (result i32)
              local.get $p2
              i32.load offset=40
              i32.const -64
              i32.sub
            else
              local.get $p4
            end
            i32.load offset=32
            local.tee $p4
            i32.eqz
            br_if $B26
            local.get $p4
            i32.const 8
            i32.add
            br $B27
          end
          local.get $p5
          i32.const 1
          i32.and
          if $I32 (result i32)
            local.get $p2
            i32.load offset=40
            i32.const -64
            i32.sub
          else
            local.get $p4
          end
          i32.load offset=4
          local.tee $p4
          i32.eqz
          br_if $B26
          local.get $p4
          i32.const 8
          i32.add
          br $B27
        end
        local.get $p5
        i32.const 1
        i32.and
        if $I33 (result i32)
          local.get $p2
          i32.load offset=40
          i32.const -64
          i32.sub
        else
          local.get $p4
        end
        i32.load offset=36
        local.tee $p4
        i32.eqz
        br_if $B26
        local.get $p4
        i32.const 8
        i32.add
      end
      i32.const 4
      i32.add
      call $f1709
      drop
    end
    local.get $p1
    i32.const 16
    i32.add
    global.set $g0
    local.get $p2
    local.set $l7
    local.get $l13
    i32.load offset=1564
    drop
    local.get $p3
    if $I34
      local.get $p2
      i32.const 48
      i32.add
      local.set $l14
      i32.const 0
      local.set $l9
      loop $L35
        i32.const 4702108
        i32.load
        local.set $p1
        block $B36 (result i32)
          local.get $p2
          i32.load8_u offset=36
          i32.const 2
          i32.and
          if $I37
            local.get $p2
            i32.load offset=40
            local.tee $l8
            i32.const 120
            i32.add
            local.get $p2
            i32.load offset=32
            i32.load offset=4856
            local.get $l8
            i32.load offset=120
            i32.const 1
            i32.shl
            i32.add
            local.get $l8
            i32.load16_u offset=124
            i32.const 1
            i32.eq
            select
            br $B36
          end
          local.get $l14
          call $f71450
        end
        local.set $l8
        local.get $p1
        i32.load offset=40
        local.get $l8
        local.get $l9
        i32.const 1
        i32.shl
        i32.add
        i32.load16_u
        i32.const 2
        i32.shl
        i32.add
        i32.load
        i32.const 16
        i32.add
        call $f1709
        drop
        local.get $l9
        i32.const 1
        i32.add
        local.tee $l9
        local.get $p3
        i32.ne
        br_if $L35
      end
    end
    local.get $l6
    local.get $p2
    i32.store offset=24
    local.get $l13
    i32.load offset=4
    drop
    local.get $l13
    i32.const 640
    i32.add
    local.get $l6
    i32.const 24
    i32.add
    local.get $l6
    i32.const 31
    i32.add
    call $f72047
    local.set $l9
    local.get $l6
    i32.load8_u offset=31
    i32.eqz
    if $I38
      local.get $l9
      local.get $l6
      i32.load offset=24
      i32.store
    end
    local.get $l13
    i32.load offset=4
    drop
    block $B39
      local.get $l6
      i32.load offset=20
      local.tee $l9
      i32.const 0
      i32.lt_s
      br_if $B39
      local.get $l9
      i32.const 2147483647
      i32.and
      i32.eqz
      br_if $B39
      local.get $l6
      local.get $l6
      i32.load offset=12
      local.tee $l9
      i32.eq
      br_if $B39
      local.get $l9
      i32.eqz
      br_if $B39
      call $f69753
      local.tee $p2
      local.get $l9
      local.get $p2
      i32.load
      i32.load offset=12
      call_indirect $__indirect_function_table (type $t1)
    end
    local.get $l6
    i32.const 32
    i32.add
    global.set $g0
    local.get $l7
    local.set $p1
    local.get $p0
    i32.const 16
    i32.add
    global.set $g0
    local.get $p1)
