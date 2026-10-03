  (func $f83408 (type $t2) (param $p0 i32) (param $p1 i32) (param $p2 i32)
    (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 f64) (local $l8 f64)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l4
    global.set $g0
    i32.const 4773644
    i32.load
    local.tee $l3
    local.get $l3
    i32.load
    i32.load offset=88
    call_indirect $__indirect_function_table (type $t5)
    local.set $l5
    local.get $l3
    local.get $l3
    i32.load
    i32.load offset=92
    call_indirect $__indirect_function_table (type $t5)
    local.set $l6
    local.get $p0
    block $B0 (result i32)
      local.get $l3
      i32.load offset=28
      i32.const 1
      i32.eq
      if $I1
        local.get $l5
        i32.const 2
        i32.div_s
        local.set $l5
        local.get $l6
        local.get $l6
        i32.const -2
        i32.div_s
        i32.add
        i32.const 1
        i32.sub
        br $B0
      end
      block $B2
        block $B3
          local.get $p1
          i32.const 6
          i32.sub
          br_table $B3 $B2 $B3 $B2
        end
        local.get $l4
        i32.const 0
        i32.store offset=12
        local.get $l4
        i32.const 0
        i32.store offset=8
        local.get $p2
        i32.load offset=52
        local.get $p2
        i32.load offset=56
        local.get $l4
        i32.const 12
        i32.add
        local.get $l4
        i32.const 8
        i32.add
        call $env.JS_DOM_MapViewportCoordinateToElementLocalCoordinate
        local.get $l3
        local.get $l4
        i32.load offset=12
        f64.convert_i32_s
        call $f79885
        local.set $l5
        local.get $l6
        local.get $l3
        local.get $l4
        i32.load offset=8
        f64.convert_i32_s
        call $f79886
        i32.const -1
        i32.xor
        i32.add
        br $B0
      end
      local.get $l3
      local.get $p2
      i32.load offset=52
      f64.convert_i32_s
      call $f79885
      local.set $l5
      local.get $l6
      local.get $l3
      local.get $p2
      i32.load offset=56
      f64.convert_i32_s
      call $f79886
      i32.const -1
      i32.xor
      i32.add
    end
    f32.convert_i32_s
    f32.store offset=232
    local.get $p0
    local.get $l5
    f32.convert_i32_s
    f32.store offset=228
    local.get $p0
    local.get $l3
    local.get $p2
    i32.load offset=44
    f64.convert_i32_s
    call $f79885
    f32.convert_i32_s
    f32.store offset=236
    local.get $p0
    i32.const 0
    local.get $l3
    local.get $p2
    i32.load offset=48
    f64.convert_i32_s
    call $f79886
    i32.sub
    f32.convert_i32_s
    f32.store offset=240
    local.get $p0
    i32.const 4676796
    i32.load
    local.tee $l3
    local.get $l3
    i32.load
    i32.load offset=12
    call_indirect $__indirect_function_table (type $t101)
    local.tee $l7
    f64.store offset=212 align=4
    block $B4
      block $B5
        block $B6
          local.get $p1
          i32.const 5
          i32.sub
          br_table $B6 $B5 $B4
        end
        local.get $p0
        local.get $p2
        i32.load16_u offset=42
        local.tee $l3
        i32.store16 offset=252
        local.get $p0
        i32.load16_u offset=320
        local.set $p2
        local.get $p0
        local.get $l3
        i32.store16 offset=320
        local.get $p0
        f64.load offset=312
        local.set $l8
        local.get $p0
        local.get $l7
        f64.store offset=312
        local.get $p0
        i32.const 256
        i32.add
        local.tee $p1
        local.get $p1
        i32.load16_u
        i32.const 1
        i32.add
        i32.const 1
        local.get $l7
        local.get $l8
        f64.sub
        f64.const 0x1p-1 (;=0.5;)
        f64.le
        select
        i32.const 1
        local.get $p2
        local.get $l3
        i32.eq
        select
        i32.store16
        br $B4
      end
      local.get $p0
      local.get $p2
      i32.load16_u offset=42
      i32.store16 offset=252
    end
    i32.const 4676796
    i32.load
    local.tee $l3
    local.get $p0
    i32.const 204
    i32.add
    local.get $l3
    i32.load
    i32.load offset=20
    call_indirect $__indirect_function_table (type $t1)
    local.get $l4
    i32.const 16
    i32.add
    global.set $g0)
