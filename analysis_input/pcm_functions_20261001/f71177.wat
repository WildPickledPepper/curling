  (func $f71177 (type $t524) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 f32) (param $p4 f32) (param $p5 i32) (result i32)
    (local $l6 i32) (local $l7 i32)
    global.get $g0
    i32.const 1008
    i32.sub
    local.tee $l6
    global.set $g0
    local.get $p1
    i32.load offset=16
    i32.const 0
    i32.store16 offset=22
    local.get $p0
    i32.load offset=4
    if $I0
      local.get $l6
      i32.const 48
      i32.add
      i32.const 0
      i32.const 960
      call $f484
      drop
      local.get $l6
      i32.const 2139095039
      i32.store offset=988
      local.get $l6
      i32.const -8388609
      i32.store offset=972
      local.get $l6
      i32.const 2139095039
      i32.store offset=908
      local.get $l6
      i32.const -8388609
      i32.store offset=892
      local.get $l6
      i32.const 2139095039
      i32.store offset=828
      local.get $l6
      i32.const -8388609
      i32.store offset=812
      local.get $l6
      i32.const 2139095039
      i32.store offset=748
      local.get $l6
      i32.const -8388609
      i32.store offset=732
      local.get $l6
      i32.const 2139095039
      i32.store offset=668
      local.get $l6
      i32.const -8388609
      i32.store offset=652
      local.get $l6
      i32.const 2139095039
      i32.store offset=588
      local.get $l6
      i32.const -8388609
      i32.store offset=572
      local.get $l6
      i32.const 2139095039
      i32.store offset=508
      local.get $l6
      i32.const -8388609
      i32.store offset=492
      local.get $l6
      i32.const 2139095039
      i32.store offset=428
      local.get $l6
      i32.const -8388609
      i32.store offset=412
      local.get $l6
      i32.const 2139095039
      i32.store offset=348
      local.get $l6
      i32.const -8388609
      i32.store offset=332
      local.get $l6
      i32.const 2139095039
      i32.store offset=268
      local.get $l6
      i32.const -8388609
      i32.store offset=252
      local.get $l6
      i32.const 2139095039
      i32.store offset=188
      local.get $l6
      i32.const -8388609
      i32.store offset=172
      local.get $l6
      i32.const 2139095039
      i32.store offset=108
      local.get $l6
      i32.const -8388609
      i32.store offset=92
      local.get $p1
      i64.const 4575657222473777152
      i64.store offset=4 align=4
      local.get $p1
      i32.const 1065353216
      i32.store offset=12
      local.get $p1
      i32.const 1065353216
      i32.store
      local.get $l6
      i32.const 0
      i32.store offset=40
      local.get $l6
      i64.const 0
      i64.store offset=32
      local.get $p1
      local.get $l6
      i32.const 48
      i32.add
      local.get $l6
      i32.const 32
      i32.add
      i32.const 12
      local.get $p1
      local.get $p0
      i32.load offset=8
      local.get $p1
      i32.const 36
      i32.add
      local.get $p1
      i32.const -64
      i32.sub
      local.get $p1
      i32.load8_u offset=139
      local.get $l6
      i32.const 16
      i32.add
      local.get $l6
      local.get $p0
      i32.load offset=4
      call_indirect $__indirect_function_table (type $t32)
      i32.store offset=116
      local.get $p1
      local.get $l6
      i32.const 48
      i32.add
      i32.store offset=112
      local.get $p1
      local.get $l6
      f32.load offset=32
      f32.store offset=140
      local.get $p1
      local.get $l6
      f32.load offset=36
      f32.store offset=144
      local.get $p1
      local.get $l6
      f32.load offset=40
      f32.store offset=148
      local.get $p1
      local.get $p2
      local.get $p3
      local.get $p4
      local.get $p5
      call $f71176
      local.set $l7
    end
    local.get $l6
    i32.const 1008
    i32.add
    global.set $g0
    local.get $l7)