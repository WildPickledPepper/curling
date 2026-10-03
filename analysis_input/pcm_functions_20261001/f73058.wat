  (func $f73058 (type $t7) (param $p0 i32)
    (local $l1 i32)
    block $B0
      local.get $p0
      i32.load offset=52
      if $I1
        local.get $p0
        f32.const 0x1p+0 (;=1;)
        call $f73037
        block $B2
          local.get $p0
          f32.load offset=80
          f32.const 0x1.99999ap-5 (;=0.05;)
          f32.eq
          br_if $B2
          i32.const 4758660
          i32.load8_u
          i32.eqz
          br_if $B2
          local.get $p0
          call $f78679
        end
        i32.const 9
        call $f80140
        call $f73714
        local.get $p0
        i32.const 1028443341
        i32.store offset=80
        local.get $p0
        i32.load offset=52
        local.tee $l1
        if $I3
          local.get $l1
          f32.const 0x1.99999ap-5 (;=0.05;)
          local.get $l1
          i32.load
          i32.load offset=148
          call_indirect $__indirect_function_table (type $t21)
        end
        block $B4
          local.get $p0
          f32.load offset=76
          f32.const 0x0p+0 (;=0;)
          f32.eq
          br_if $B4
          i32.const 4758660
          i32.load8_u
          i32.eqz
          br_if $B4
          local.get $p0
          call $f78679
        end
        i32.const 9
        call $f80140
        call $f73714
        local.get $p0
        i32.const 0
        i32.store offset=76
        local.get $p0
        i32.load offset=52
        local.tee $l1
        if $I5
          local.get $l1
          f32.const 0x0p+0 (;=0;)
          local.get $l1
          i32.load
          i32.load offset=140
          call_indirect $__indirect_function_table (type $t21)
        end
        local.get $p0
        i32.const 0
        call $f73059
        local.get $p0
        i32.const 0
        call $f73036
        local.get $p0
        i32.const 1
        call $f73038
        i32.const 9
        call $f80140
        call $f73714
        local.get $p0
        i32.load offset=144
        i32.eqz
        br_if $B0
        local.get $p0
        i64.const 0
        i64.store offset=140 align=4
        local.get $p0
        i32.load offset=52
        i32.const 0
        local.get $p0
        i32.load8_u offset=133
        call $f73701
        i32.const 4758660
        i32.load8_u
        i32.eqz
        br_if $B0
        local.get $p0
        call $f78679
        br $B0
      end
      local.get $p0
      i32.const 1028443341
      i32.store offset=80
      local.get $p0
      i64.const 1065353216
      i64.store offset=72 align=4
      local.get $p0
      i32.const 0
      i32.store offset=136
      local.get $p0
      i32.const 257
      i32.store16 offset=148
      local.get $p0
      i64.const 0
      i64.store offset=140 align=4
      local.get $p0
      i32.const 1
      i32.store16 offset=132
      local.get $p0
      i32.const 1
      i32.store8 offset=100
      local.get $p0
      i32.const 4748500
      i64.load align=4
      i64.store offset=104 align=4
      local.get $p0
      i32.const 4748508
      i32.load
      i32.store offset=112
      local.get $p0
      i64.const 4575657221408423936
      i64.store offset=124 align=4
      local.get $p0
      i64.const 0
      i64.store offset=116 align=4
      local.get $p0
      i32.const 1
      i32.store8 offset=85
      local.get $p0
      i32.const 4748496
      i32.load
      i32.store offset=96
      local.get $p0
      i32.const 4748488
      i64.load align=4
      i64.store offset=88 align=4
    end
    local.get $p0
    i64.const 0
    i64.store offset=156 align=4
    local.get $p0
    i32.const 0
    i32.store8 offset=164)