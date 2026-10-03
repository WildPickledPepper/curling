  (func $f33062 (type $t106) (param $p0 f32) (result f32)
    (local $l1 i32) (local $l2 i32) (local $l3 i32) (local $l4 f64)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l1
    global.set $g0
    block $B0 (result f32)
      local.get $p0
      i32.reinterpret_f32
      local.tee $l3
      i32.const 2147483647
      i32.and
      local.tee $l2
      i32.const 1061752794
      i32.le_u
      if $I1
        f32.const 0x1p+0 (;=1;)
        local.get $l2
        i32.const 964689920
        i32.lt_u
        br_if $B0
        drop
        local.get $p0
        f64.promote_f32
        call $f18889
        br $B0
      end
      local.get $l2
      i32.const 1081824209
      i32.le_u
      if $I2
        local.get $p0
        f64.promote_f32
        local.set $l4
        local.get $l2
        i32.const 1075235812
        i32.ge_u
        if $I3
          f64.const -0x1.921fb54442d18p+1 (;=-3.14159;)
          f64.const 0x1.921fb54442d18p+1 (;=3.14159;)
          local.get $l3
          i32.const 0
          i32.ge_s
          select
          local.get $l4
          f64.add
          call $f18889
          f32.neg
          br $B0
        end
        local.get $l3
        i32.const 0
        i32.lt_s
        if $I4
          local.get $l4
          f64.const 0x1.921fb54442d18p+0 (;=1.5708;)
          f64.add
          call $f18888
          br $B0
        end
        f64.const 0x1.921fb54442d18p+0 (;=1.5708;)
        local.get $l4
        f64.sub
        call $f18888
        br $B0
      end
      local.get $l2
      i32.const 1088565717
      i32.le_u
      if $I5
        local.get $l2
        i32.const 1085271520
        i32.ge_u
        if $I6
          f64.const -0x1.921fb54442d18p+2 (;=-6.28319;)
          f64.const 0x1.921fb54442d18p+2 (;=6.28319;)
          local.get $l3
          i32.const 0
          i32.ge_s
          select
          local.get $p0
          f64.promote_f32
          f64.add
          call $f18889
          br $B0
        end
        local.get $l3
        i32.const 0
        i32.lt_s
        if $I7
          f64.const -0x1.2d97c7f3321d2p+2 (;=-4.71239;)
          local.get $p0
          f64.promote_f32
          f64.sub
          call $f18888
          br $B0
        end
        local.get $p0
        f64.promote_f32
        f64.const -0x1.2d97c7f3321d2p+2 (;=-4.71239;)
        f64.add
        call $f18888
        br $B0
      end
      local.get $p0
      local.get $p0
      f32.sub
      local.get $l2
      i32.const 2139095040
      i32.ge_u
      br_if $B0
      drop
      block $B8
        block $B9
          block $B10
            block $B11
              local.get $p0
              local.get $l1
              i32.const 8
              i32.add
              call $f18176
              i32.const 3
              i32.and
              br_table $B11 $B10 $B9 $B8
            end
            local.get $l1
            f64.load offset=8
            call $f18889
            br $B0
          end
          local.get $l1
          f64.load offset=8
          f64.neg
          call $f18888
          br $B0
        end
        local.get $l1
        f64.load offset=8
        call $f18889
        f32.neg
        br $B0
      end
      local.get $l1
      f64.load offset=8
      call $f18888
    end
    local.set $p0
    local.get $l1
    i32.const 16
    i32.add
    global.set $g0
    local.get $p0)
