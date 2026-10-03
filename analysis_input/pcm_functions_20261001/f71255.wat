  (func $f71255 (type $t7) (param $p0 i32)
    (local $l1 i32) (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 i32) (local $l17 i32) (local $l18 i32) (local $l19 f32)
    global.get $g0
    i32.const 48
    i32.sub
    local.tee $l5
    global.set $g0
    local.get $p0
    i32.load offset=44
    local.tee $l1
    i32.load offset=336
    call $f69738
    local.tee $l4
    i32.eqz
    if $I0
      call $f69753
      local.tee $l2
      i32.const 12195
      i32.const 3152658
      i32.const 3150980
      i32.const 4700888
      i32.load
      local.tee $l3
      local.get $l3
      i32.load
      i32.load offset=20
      call_indirect $__indirect_function_table (type $t5)
      select
      i32.const 3152590
      i32.const 82
      local.get $l2
      i32.load
      i32.load offset=8
      call_indirect $__indirect_function_table (type $t9)
      local.tee $l3
      i32.const 19
      i32.add
      i32.const -16
      i32.and
      local.tee $l2
      i32.const 4
      i32.sub
      local.get $l2
      local.get $l3
      i32.sub
      i32.store
      local.get $l2
      local.get $l1
      i32.load offset=340
      call $f71150
      local.set $l4
    end
    local.get $l4
    i32.const 11856
    i32.add
    i64.const 0
    i64.store align=4
    local.get $p0
    i32.load offset=40
    if $I1
      local.get $p0
      i32.load offset=36
      local.set $l1
      i32.const 0
      local.set $l3
      loop $L2
        local.get $l1
        local.get $l3
        i32.const 56
        i32.mul
        local.tee $l7
        i32.add
        local.tee $l1
        local.get $p0
        i32.load offset=32
        local.get $l3
        i32.const 2
        i32.shl
        i32.add
        i32.load
        local.tee $l2
        i64.load offset=28 align=4
        i64.store align=4
        local.get $l1
        local.get $l2
        i64.load offset=76 align=4
        i64.store offset=48 align=4
        local.get $l1
        local.get $l2
        i64.load offset=68 align=4
        i64.store offset=40 align=4
        local.get $l1
        local.get $l2
        i64.load offset=60 align=4
        i64.store offset=32 align=4
        local.get $l1
        local.get $l2
        i64.load offset=52 align=4
        i64.store offset=24 align=4
        local.get $l1
        local.get $l2
        i64.load offset=44 align=4
        i64.store offset=16 align=4
        local.get $l1
        local.get $l2
        i64.load offset=36 align=4
        i64.store offset=8 align=4
        local.get $p0
        i32.load offset=36
        local.tee $l1
        local.get $l7
        i32.add
        i32.load16_u offset=48
        local.tee $l2
        local.get $l6
        local.get $l2
        local.get $l6
        i32.gt_u
        select
        local.set $l6
        local.get $l3
        i32.const 1
        i32.add
        local.tee $l3
        local.get $p0
        i32.load offset=40
        i32.lt_u
        br_if $L2
      end
    end
    local.get $l4
    i32.const 12052
    i32.add
    i32.const 0
    i32.store
    local.get $l4
    i32.const 12048
    i32.add
    local.set $l13
    local.get $l6
    local.get $l4
    i32.const 12056
    i32.add
    i32.load
    i32.const 2147483647
    i32.and
    i32.gt_u
    if $I3
      local.get $l13
      local.get $l6
      call $f71197
    end
    local.get $l4
    i32.const 11852
    i32.add
    local.set $l2
    local.get $l4
    local.get $l6
    i32.store offset=12052
    i32.const 0
    local.set $l7
    local.get $l4
    i32.const 12064
    i32.add
    i32.const 0
    i32.store
    local.get $l4
    i32.const 12060
    i32.add
    local.set $l14
    local.get $l6
    local.get $l4
    i32.const 12068
    i32.add
    i32.load
    i32.const 2147483647
    i32.and
    i32.gt_u
    if $I4
      local.get $l14
      local.get $l6
      call $f71197
    end
    local.get $l4
    local.get $l6
    i32.store offset=12064
    local.get $p0
    i32.load offset=48
    local.set $l9
    local.get $p0
    i32.load offset=28
    local.set $l1
    local.get $l5
    local.get $l4
    i32.const 12088
    i32.add
    i32.store offset=40
    local.get $l5
    local.get $l4
    i32.const 11824
    i32.add
    i32.store offset=36
    local.get $l5
    local.get $l2
    i32.store offset=32
    local.get $l5
    i32.const 3150688
    i32.store offset=24
    local.get $l5
    local.get $l1
    i32.const 11836
    i32.add
    i32.store offset=28
    local.get $p0
    i32.load offset=40
    if $I5 (result i32)
      local.get $p0
      i32.load offset=36
      local.set $l3
      i32.const 0
      local.set $l2
      loop $L6
        local.get $p0
        i32.load offset=32
        local.get $l2
        i32.const 2
        i32.shl
        i32.add
        i32.load
        local.set $l15
        local.get $l1
        i32.load offset=12132
        local.set $l16
        local.get $p0
        i32.load offset=44
        local.tee $l1
        f32.load offset=52
        local.set $l19
        local.get $l5
        local.get $l1
        f32.load offset=68
        f32.store offset=8
        local.get $l5
        local.get $l1
        f32.load offset=72
        f32.store offset=12
        local.get $l5
        local.get $l1
        f32.load offset=76
        f32.store offset=16
        block $B7
          local.get $l3
          local.get $l2
          i32.const 56
          i32.mul
          local.tee $l8
          i32.add
          local.tee $l17
          i32.load
          i32.load offset=24
          i32.const 2
          i32.shl
          i32.const 4701964
          i32.add
          i32.load
          local.tee $l18
          i32.eqz
          if $I8
            i32.const 0
            local.set $l1
            br $B7
          end
          local.get $l17
          local.get $l19
          local.get $l5
          i32.const 24
          i32.add
          local.get $l16
          local.get $l9
          i32.const 5
          i32.shl
          i32.add
          local.get $l5
          i32.const 20
          i32.add
          local.get $l5
          i32.const 8
          i32.add
          local.get $l1
          i64.load offset=600
          local.get $l13
          i32.load
          local.get $l14
          i32.load
          local.get $l18
          call_indirect $__indirect_function_table (type $t320)
          local.set $l1
          local.get $p0
          i32.load offset=36
          local.set $l3
        end
        local.get $l3
        local.get $l8
        i32.add
        local.get $l1
        i32.store16 offset=50
        local.get $l10
        local.get $l15
        i32.load offset=60
        i32.load16_u offset=12
        local.tee $l1
        i32.const 255
        i32.and
        local.tee $l3
        local.get $l3
        local.get $l10
        i32.lt_u
        select
        local.set $l10
        local.get $l11
        local.get $l1
        i32.const 8
        i32.shr_u
        local.tee $l1
        local.get $l1
        local.get $l11
        i32.lt_u
        select
        local.set $l11
        local.get $p0
        i32.load offset=36
        local.tee $l3
        local.get $l8
        i32.add
        local.tee $l1
        i32.load16_u offset=46
        local.tee $l8
        local.get $l7
        local.get $l7
        local.get $l8
        i32.lt_u
        select
        local.set $l7
        local.get $l1
        i32.load16_u offset=44
        local.tee $l1
        local.get $l12
        local.get $l1
        local.get $l12
        i32.gt_u
        select
        local.set $l12
        local.get $l2
        i32.const 1
        i32.add
        local.tee $l2
        local.get $p0
        i32.load offset=40
        i32.lt_u
        if $I9
          local.get $l9
          i32.const 256
          i32.add
          local.set $l9
          local.get $p0
          i32.load offset=28
          local.set $l1
          br $L6
        end
      end
      local.get $p0
      i32.load offset=28
    else
      local.get $l1
    end
    i32.const 12112
    i32.add
    local.get $l10
    call $f69733
    local.get $p0
    i32.load offset=28
    i32.const 12116
    i32.add
    local.get $l11
    call $f69733
    local.get $p0
    i32.load offset=28
    i32.const 12120
    i32.add
    local.get $l12
    call $f69733
    local.get $p0
    i32.load offset=28
    i32.const 12124
    i32.add
    local.get $l7
    call $f69733
    local.get $p0
    i32.load offset=28
    i32.const 12128
    i32.add
    local.get $l6
    call $f69733
    local.get $p0
    i32.load offset=44
    i32.load offset=336
    local.get $l4
    call $f69737
    local.get $l5
    i32.const 48
    i32.add
    global.set $g0)