  (func $f70642 (type $t13) (param $p0 i32) (param $p1 i32) (result f32)
    local.get $p0
    local.get $p1
    i32.const 2
    i32.shl
    i32.add
    i32.const 1032
    i32.add
    f32.load)