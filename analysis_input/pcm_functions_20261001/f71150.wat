  (func $f71150 (type $t0) (param $p0 i32) (param $p1 i32) (result i32)
    (local $l2 i32)
    local.get $p0
    local.get $p1
    i32.store offset=11824
    local.get $p0
    i32.const 0
    i32.store
    local.get $p0
    i32.const 0
    i32.store offset=12132
    local.get $p0
    i32.const 0
    i32.store offset=12120
    local.get $p0
    i64.const 0
    i64.store offset=12112
    local.get $p0
    i32.const 0
    i32.store offset=12104
    local.get $p0
    i32.const 0
    i32.store offset=12096
    local.get $p0
    i64.const 0
    i64.store offset=12088
    local.get $p0
    i64.const 0
    i64.store offset=11876 align=4
    local.get $p0
    i32.const 0
    i32.store offset=11868
    local.get $p0
    local.get $p1
    i32.store offset=11852
    local.get $p0
    i64.const 0
    i64.store offset=11892 align=4
    local.get $p0
    i32.const 11828
    i32.add
    i64.const 0
    i64.store align=4
    local.get $p0
    i32.const 11836
    i32.add
    i64.const 0
    i64.store align=4
    local.get $p0
    i32.const 11844
    i32.add
    i32.const 0
    i32.store
    local.get $p0
    i32.const 11856
    i32.add
    i64.const 0
    i64.store align=4
    local.get $p0
    i32.const 11848
    i32.add
    local.get $p1
    i32.store
    local.get $p0
    i32.const 11900
    i32.add
    local.tee $p1
    i64.const 0
    i64.store align=4
    local.get $p0
    i32.const 11908
    i32.add
    i64.const 0
    i64.store align=4
    local.get $p0
    i32.const 11916
    i32.add
    local.tee $l2
    i64.const 0
    i64.store align=4
    local.get $p0
    i32.const 11924
    i32.add
    i32.const 0
    i32.store
    local.get $p0
    i32.const 11976
    i32.add
    i32.const 0
    i32.const 96
    call $f484
    drop
    local.get $p0
    i32.const 12164
    i32.add
    i64.const 0
    i64.store align=4
    local.get $p0
    i32.const 12156
    i32.add
    i64.const 0
    i64.store align=4
    local.get $p0
    i32.const 12148
    i32.add
    i64.const 0
    i64.store align=4
    local.get $p0
    i64.const 0
    i64.store offset=12140 align=4
    local.get $l2
    i32.const 512
    call $f70632
    local.get $p1
    i32.load
    i32.const 2147483520
    i32.and
    i32.eqz
    if $I0
      local.get $p0
      i32.const 11892
      i32.add
      i32.const 128
      call $f70632
    end
    local.get $p0)