  (func $f18176 (type $t74) (param $p0 f32) (param $p1 i32) (result i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 f64) (local $l6 f64) (local $l7 f64)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l3
    global.set $g0
    block $B0
      local.get $p0
      i32.reinterpret_f32
      local.tee $l4
      i32.const 2147483647
      i32.and
      local.tee $l2
      i32.const 1305022426
      i32.le_u
      if $I1
        local.get $p1
        local.get $p0
        f64.promote_f32
        local.tee $l6
        local.get $l6
        f64.const 0x1.45f306dc9c883p-1 (;=0.63662;)
        f64.mul
        f64.const 0x1.8p+52 (;=6.7554e+15;)
        f64.add
        f64.const -0x1.8p+52 (;=-6.7554e+15;)
        f64.add
        local.tee $l5
        f64.const -0x1.921fb5p+0 (;=-1.5708;)
        f64.mul
        f64.add
        local.get $l5
        f64.const -0x1.110b4611a6263p-26 (;=-1.58933e-08;)
        f64.mul
        f64.add
        local.tee $l7
        f64.store
        local.get $l7
        f64.const -0x1.921fb6p-1 (;=-0.785398;)
        f64.lt
        local.set $l4
        block $B2 (result i32)
          local.get $l5
          f64.abs
          f64.const 0x1p+31 (;=2.14748e+09;)
          f64.lt
          if $I3
            local.get $l5
            i32.trunc_f64_s
            br $B2
          end
          i32.const -2147483648
        end
        local.set $l2
        local.get $l4
        if $I4
          local.get $p1
          local.get $l6
          local.get $l5
          f64.const -0x1p+0 (;=-1;)
          f64.add
          local.tee $l5
          f64.const -0x1.921fb5p+0 (;=-1.5708;)
          f64.mul
          f64.add
          local.get $l5
          f64.const -0x1.110b4611a6263p-26 (;=-1.58933e-08;)
          f64.mul
          f64.add
          f64.store
          local.get $l2
          i32.const 1
          i32.sub
          local.set $l2
          br $B0
        end
        local.get $l7
        f64.const 0x1.921fb6p-1 (;=0.785398;)
        f64.gt
        i32.eqz
        br_if $B0
        local.get $p1
        local.get $l6
        local.get $l5
        f64.const 0x1p+0 (;=1;)
        f64.add
        local.tee $l5
        f64.const -0x1.921fb5p+0 (;=-1.5708;)
        f64.mul
        f64.add
        local.get $l5
        f64.const -0x1.110b4611a6263p-26 (;=-1.58933e-08;)
        f64.mul
        f64.add
        f64.store
        local.get $l2
        i32.const 1
        i32.add
        local.set $l2
        br $B0
      end
      local.get $l2
      i32.const 2139095040
      i32.ge_u
      if $I5
        local.get $p1
        local.get $p0
        local.get $p0
        f32.sub
        f64.promote_f32
        f64.store
        i32.const 0
        local.set $l2
        br $B0
      end
      local.get $l3
      local.get $l2
      local.get $l2
      i32.const 23
      i32.shr_u
      i32.const 150
      i32.sub
      local.tee $l2
      i32.const 23
      i32.shl
      i32.sub
      f32.reinterpret_i32
      f64.promote_f32
      f64.store offset=8
      local.get $l3
      i32.const 8
      i32.add
      local.get $l3
      local.get $l2
      i32.const 1
      i32.const 0
      call $f5976
      local.set $l2
      local.get $l3
      f64.load
      local.set $l5
      local.get $l4
      i32.const 0
      i32.lt_s
      if $I6
        local.get $p1
        local.get $l5
        f64.neg
        f64.store
        i32.const 0
        local.get $l2
        i32.sub
        local.set $l2
        br $B0
      end
      local.get $p1
      local.get $l5
      f64.store
    end
    local.get $l3
    i32.const 16
    i32.add
    global.set $g0
    local.get $l2)
