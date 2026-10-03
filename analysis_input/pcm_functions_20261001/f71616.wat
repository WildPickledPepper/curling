  (func $f71616 (type $t2) (param $p0 i32) (param $p1 i32) (param $p2 i32)
    (local $l3 i32)
    local.get $p0
    i32.load offset=176
    local.tee $l3
    if $I0
      local.get $p2
      if $I1
        local.get $p0
        local.get $l3
        f32.load offset=44
        f32.store offset=140
        local.get $p0
        local.get $l3
        f32.load offset=32
        f32.store offset=128
        local.get $p0
        local.get $l3
        f32.load offset=36
        f32.store offset=132
        local.get $p0
        local.get $l3
        f32.load offset=40
        f32.store offset=136
        local.get $p0
        local.get $l3
        f32.load offset=48
        f32.store offset=120
        local.get $p0
        local.get $l3
        f32.load offset=52
        f32.store offset=124
        local.get $p0
        local.get $l3
        f32.load offset=56
        f32.store offset=112
        local.get $p0
        local.get $l3
        f32.load offset=60
        f32.store offset=116
      end
      local.get $p1
      local.get $p1
      i32.load offset=280
      i32.const 1
      i32.sub
      i32.store offset=280
      local.get $l3
      local.get $p1
      i32.load offset=288
      i32.store
      local.get $p1
      local.get $l3
      i32.store offset=288
      local.get $p0
      i32.const 0
      i32.store offset=176
    end)
