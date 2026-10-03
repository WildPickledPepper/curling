  (func $f18890 (type $t106) (param $p0 f32) (result f32)
    (local $l1 f64) (local $l2 i32) (local $l3 i32) (local $l4 i32)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l2
    global.set $g0
    block $B0
      local.get $p0
      i32.reinterpret_f32
      local.tee $l4
      i32.const 2147483647
      i32.and
      local.tee $l3
      i32.const 1061752794
      i32.le_u
      if $I1
        local.get $l3
        i32.const 964689920
        i32.lt_u
        br_if $B0
        local.get $p0
        f64.promote_f32
        call $f18888
        local.set $p0
        br $B0
      end
      local.get $l3
      i32.const 1081824209
      i32.le_u
      if $I2
        local.get $p0
        f64.promote_f32
        local.set $l1
        local.get $l3
        i32.const 1075235811
        i32.le_u
        if $I3
          local.get $l4
          i32.const 0
          i32.lt_s
          if $I4
            local.get $l1
            f64.const 0x1.921fb54442d18p+0 (;=1.5708;)
            f64.add
            call $f18889
            f32.neg
            local.set $p0
            br $B0
          end
          local.get $l1
          f64.const -0x1.921fb54442d18p+0 (;=-1.5708;)
          f64.add
          call $f18889
          local.set $p0
          br $B0
        end
        f64.const -0x1.921fb54442d18p+1 (;=-3.14159;)
        f64.const 0x1.921fb54442d18p+1 (;=3.14159;)
        local.get $l4
        i32.const 0
        i32.ge_s
        select
        local.get $l1
        f64.add
        f64.neg
        call $f18888
        local.set $p0
        br $B0
      end
      local.get $l3
      i32.const 1088565717
      i32.le_u
      if $I5
        local.get $p0
        f64.promote_f32
        local.set $l1
        local.get $l3
        i32.const 1085271519
        i32.le_u
        if $I6
          local.get $l4
          i32.const 0
          i32.lt_s
          if $I7
            local.get $l1
            f64.const 0x1.2d97c7f3321d2p+2 (;=4.71239;)
            f64.add
            call $f18889
            local.set $p0
            br $B0
          end
          local.get $l1
          f64.const -0x1.2d97c7f3321d2p+2 (;=-4.71239;)
          f64.add
          call $f18889
          f32.neg
          local.set $p0
          br $B0
        end
        f64.const -0x1.921fb54442d18p+2 (;=-6.28319;)
        f64.const 0x1.921fb54442d18p+2 (;=6.28319;)
        local.get $l4
        i32.const 0
        i32.ge_s
        select
        local.get $l1
        f64.add
        call $f18888
        local.set $p0
        br $B0
      end
      local.get $l3
      i32.const 2139095040
      i32.ge_u
      if $I8
        local.get $p0
        local.get $p0
        f32.sub
        local.set $p0
        br $B0
      end
      block $B9
        block $B10
          block $B11
            block $B12
              local.get $p0
              local.get $l2
              i32.const 8
              i32.add
              call $f18176
              i32.const 3
              i32.and
              br_table $B12 $B11 $B10 $B9
            end
            local.get $l2
            f64.load offset=8
            call $f18888
            local.set $p0
            br $B0
          end
          local.get $l2
          f64.load offset=8
          call $f18889
          local.set $p0
          br $B0
        end
        local.get $l2
        f64.load offset=8
        f64.neg
        call $f18888
        local.set $p0
        br $B0
      end
      local.get $l2
      f64.load offset=8
      call $f18889
      f32.neg
      local.set $p0
    end
    local.get $l2
    i32.const 16
    i32.add
    global.set $g0
    local.get $p0)
