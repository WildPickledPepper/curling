  (func $f60187 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l3
    global.set $g0
    i32.const 4674510
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3745328
      call $f1661
      i32.const 3748808
      call $f1661
      i32.const 3792480
      call $f1661
      i32.const 3792608
      call $f1661
      i32.const 3751540
      call $f1661
      i32.const 3773132
      call $f1661
      i32.const 3795216
      call $f1661
      i32.const 3752444
      call $f1661
      i32.const 3753376
      call $f1661
      i32.const 3753484
      call $f1661
      i32.const 3745900
      call $f1661
      i32.const 3860088
      call $f1661
      i32.const 3821460
      call $f1661
      i32.const 3816824
      call $f1661
      i32.const 3837344
      call $f1661
      i32.const 3843852
      call $f1661
      i32.const 3835136
      call $f1661
      i32.const 4674510
      i32.const 1
      i32.store8
    end
    i32.const 3753484
    i32.load
    call $f1446
    local.tee $p1
    i32.const 0
    call $f61054
    i32.const 3752444
    i32.load
    local.tee $l2
    i32.load offset=116
    i32.eqz
    if $I1
      local.get $l2
      call $f65192
    end
    local.get $p1
    local.get $p1
    i32.const 3795216
    i32.load
    call $f42653
    i32.store offset=8
    local.get $p1
    i32.const 3835136
    i32.load
    i32.store offset=20
    local.get $p1
    i32.const 0
    i32.const 3745328
    i32.load
    i32.const 256
    call $f1052
    i32.const 0
    call $f53839
    local.tee $l2
    i32.store offset=36
    local.get $p1
    local.get $l2
    i32.load offset=8
    i32.store offset=40
    local.get $p1
    i32.const 0
    i32.const 3745328
    i32.load
    i32.const 64
    call $f1052
    i32.const 0
    call $f53839
    local.tee $l2
    i32.store offset=44
    local.get $p1
    local.get $l2
    i32.load offset=8
    i32.store offset=48
    local.get $p1
    i32.const 0
    call $f51726
    i32.const 3816824
    i32.load
    i32.const 0
    call $f53732
    i32.const 47
    i32.const 92
    i32.const 0
    call $f53893
    i32.store offset=52
    i32.const 3860088
    i32.load
    local.set $l2
    local.get $p1
    i32.const 530440
    i32.store offset=60
    local.get $p1
    local.get $l2
    i32.store offset=56
    block $B2
      block $B3
        block $B4
          local.get $p1
          i32.const 0
          call $f61058
          i32.eqz
          br_if $B4
          local.get $p0
          i32.const 1
          i32.store8 offset=84
          local.get $p1
          i32.load offset=36
          local.set $p1
          i32.const 3748808
          i32.load
          local.tee $l2
          i32.load offset=116
          i32.eqz
          if $I5
            local.get $l2
            call $f65192
          end
          local.get $p1
          i32.const 0
          call $f42976
          i32.const 4674496
          i32.load8_u
          i32.eqz
          if $I6
            i32.const 3749968
            call $f1661
            i32.const 4674496
            i32.const 1
            i32.store8
          end
          local.get $p0
          i32.load offset=160
          local.set $l2
          i32.const 3749968
          i32.load
          call $f1446
          local.tee $p1
          local.get $l2
          i32.const 0
          call $f61050
          local.get $p0
          local.get $p1
          i32.store offset=96
          local.get $p0
          local.get $p1
          i32.load offset=24
          i32.store offset=128
          local.get $p0
          i32.load offset=160
          local.set $l2
          local.get $p1
          i32.const 0
          i32.store offset=108
          local.get $p1
          local.get $l2
          i32.store offset=16
          local.get $p1
          i64.const 4294967296000
          i64.store offset=48 align=4
          local.get $p1
          i64.const 4294967296000
          i64.store offset=72 align=4
          local.get $p0
          local.get $p1
          i32.load offset=56
          i32.store offset=28
          local.get $p0
          local.get $p1
          i32.load offset=80
          i32.store offset=32
          local.get $p0
          i32.load offset=136
          i32.const 0
          i32.const 3773132
          i32.load
          call $f2903
          i32.const 3792608
          i32.load
          call $f34548
          local.tee $p1
          local.get $p0
          i32.load offset=28
          local.get $p1
          i32.load
          local.tee $p1
          i32.load offset=796
          local.get $p1
          i32.load offset=792
          call_indirect $__indirect_function_table (type $t2)
          local.get $p0
          i32.load offset=136
          i32.const 1
          i32.const 3773132
          i32.load
          call $f2903
          i32.const 3792608
          i32.load
          call $f34548
          local.tee $p1
          local.get $p0
          i32.load offset=32
          local.get $p1
          i32.load
          local.tee $p1
          i32.load offset=796
          local.get $p1
          i32.load offset=792
          call_indirect $__indirect_function_table (type $t2)
          local.get $p0
          i32.load offset=96
          local.tee $p1
          i32.const -64
          i32.sub
          i32.const 1
          i32.store
          local.get $p1
          i32.const 1
          i32.store offset=40
          block $B7
            local.get $p1
            i32.load offset=28
            call $f1448
            local.tee $p1
            i32.eqz
            if $I8
              local.get $p0
              i32.const 0
              i32.store offset=100
              br $B7
            end
            local.get $p1
            i32.const 3745900
            i32.load
            local.tee $l4
            call $f1674
            local.tee $l2
            i32.eqz
            br_if $B3
            local.get $p0
            local.get $l2
            i32.store offset=100
            local.get $p1
            i32.const 3745900
            i32.load
            local.tee $l2
            call $f1674
            i32.eqz
            br_if $B2
          end
          local.get $p0
          i32.const 1
          i32.store8 offset=89
          i32.const 3821460
          i32.load
          i32.const 0
          call $f54416
          i32.const 3792480
          i32.load
          call $f34548
          local.set $p1
          local.get $l3
          i32.const 4
          i32.store offset=12
          i32.const 3751540
          i32.load
          local.get $l3
          i32.const 12
          i32.add
          call $f1675
          local.set $l2
          local.get $p1
          i32.const 3837344
          i32.load
          local.get $l2
          i32.const 0
          call $f54371
          i32.const 3843852
          i32.load
          i32.const 0
          call $f54416
          i32.const 0
          i32.const 0
          call $f54405
          local.get $p0
          i32.const 1
          i32.store8 offset=132
          local.get $p0
          i32.load offset=52
          local.set $p1
          i32.const 3753376
          i32.load
          local.tee $l2
          i32.load offset=116
          i32.eqz
          if $I9
            local.get $l2
            call $f65192
          end
          local.get $p1
          i32.const 0
          i32.const 0
          call $f54398
          i32.eqz
          br_if $B4
          local.get $p0
          i32.load offset=52
          i32.const 1
          i32.const 0
          call $f54405
        end
        local.get $l3
        i32.const 16
        i32.add
        global.set $g0
        return
      end
      local.get $p1
      local.get $l4
      call $f1678
      unreachable
    end
    local.get $p1
    local.get $l2
    call $f1678
    unreachable)
