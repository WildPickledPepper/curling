  (func $f18174 (type $t5) (param $p0 i32) (result i32)
    (local $l1 i32)
    local.get $p0
    i32.load offset=4
    drop
    i32.const 3769556
    i32.load
    drop
    local.get $p0
    i32.load
    local.tee $l1
    if $I0
      local.get $l1
      call $f1089
      unreachable
    end
    local.get $p0)
