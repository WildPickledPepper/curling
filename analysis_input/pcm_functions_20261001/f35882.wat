  (func $f35882 (type $t106) (param $p0 f32) (result f32)
    (local $l1 f32) (local $l2 f32) (local $l3 i32) (local $l4 i32)
    local.get $p0
    i32.reinterpret_f32
    local.tee $l4
    i32.const 2147483647
    i32.and
    local.tee $l3
    i32.const 1065353216
    i32.ge_u
    if $I0
      local.get $l3
      i32.const 1065353216
      i32.eq
      if $I1
        f32.const 0x0p+0 (;=0;)
        f32.const 0x1.921fb4p+1 (;=3.14159;)
        local.get $l4
        i32.const 0
        i32.ge_s
        select
        return
      end
      f32.const 0x0p+0 (;=0;)
      local.get $p0
      local.get $p0
      f32.sub
      f32.div
      return
    end
    block $B2 (result f32)
      local.get $l3
      i32.const 1056964607
      i32.le_u
      if $I3
        f32.const 0x1.921fb4p+0 (;=1.5708;)
        local.get $l3
        i32.const 847249409
        i32.lt_u
        br_if $B2
        drop
        f32.const 0x1.4442dp-24 (;=7.54979e-08;)
        local.get $p0
        local.get $p0
        local.get $p0
        f32.mul
        call $f35883
        f32.mul
        f32.sub
        local.get $p0
        f32.sub
        f32.const 0x1.921fb4p+0 (;=1.5708;)
        f32.add
        return
      end
      local.get $l4
      i32.const 0
      i32.lt_s
      if $I4
        f32.const 0x1.921fb4p+0 (;=1.5708;)
        local.get $p0
        f32.const 0x1p+0 (;=1;)
        f32.add
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        local.tee $p0
        f32.sqrt
        local.tee $l1
        local.get $l1
        local.get $p0
        call $f35883
        f32.mul
        f32.const -0x1.4442dp-24 (;=-7.54979e-08;)
        f32.add
        f32.add
        f32.sub
        local.tee $p0
        local.get $p0
        f32.add
        return
      end
      f32.const 0x1p+0 (;=1;)
      local.get $p0
      f32.sub
      f32.const 0x1p-1 (;=0.5;)
      f32.mul
      local.tee $l1
      f32.sqrt
      local.tee $l2
      local.get $l1
      call $f35883
      f32.mul
      local.get $l1
      local.get $l2
      i32.reinterpret_f32
      i32.const -4096
      i32.and
      f32.reinterpret_i32
      local.tee $p0
      local.get $p0
      f32.mul
      f32.sub
      local.get $l2
      local.get $p0
      f32.add
      f32.div
      f32.add
      local.get $p0
      f32.add
      local.tee $p0
      local.get $p0
      f32.add
    end)