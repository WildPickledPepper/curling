  (func $f78659 (type $t0) (param $p0 i32) (param $p1 i32) (result i32)
    (local $l2 i32)
    i32.const 4787792
    i32.load
    local.tee $l2
    i32.eqz
    if $I0
      i32.const -1
      return
    end
    local.get $l2
    local.get $p0
    local.get $p1
    call $f80338
    i32.const 0)
