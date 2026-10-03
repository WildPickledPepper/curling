  (func $f78136 (type $t5) (param $p0 i32) (result i32)
    (local $l1 i32)
    local.get $p0
    i32.load offset=112
    local.tee $l1
    if $I0 (result i32)
      local.get $l1
    else
      block $B1
        local.get $p0
        i32.load offset=32
        local.tee $l1
        if $I2
          local.get $l1
          i32.load offset=36
          i32.load
          local.set $l1
          br $B1
        end
        loop $L3
          local.get $p0
          local.tee $l1
          i32.load offset=96
          local.tee $p0
          br_if $L3
        end
      end
      local.get $l1
      i32.load offset=112
    end)
