  (func $f60184 (type $t1) (param $p0 i32) (param $p1 i32)
    local.get $p0
    i32.load offset=68
    local.tee $p1
    if $I0
      local.get $p1
      i32.const 0
      call $f52643
    end
    local.get $p0
    i32.load offset=64
    local.tee $p1
    if $I1
      local.get $p1
      i32.const 0
      call $f52643
    end
    local.get $p0
    i32.load offset=60
    i32.const 0
    call $f9402)
