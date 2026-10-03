  (func $f61097 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 f32) (local $l7 f32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f64)
    global.get $g0
    i32.const 48
    i32.sub
    local.tee $l2
    global.set $g0
    i32.const 4675161
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3748808
      call $f1661
      i32.const 3792480
      call $f1661
      i32.const 3792496
      call $f1661
      i32.const 3792572
      call $f1661
      i32.const 3792588
      call $f1661
      i32.const 3751540
      call $f1661
      i32.const 3773132
      call $f1661
      i32.const 3752504
      call $f1661
      i32.const 3753376
      call $f1661
      i32.const 3824044
      call $f1661
      i32.const 3835540
      call $f1661
      i32.const 3820972
      call $f1661
      i32.const 3821460
      call $f1661
      i32.const 3836548
      call $f1661
      i32.const 3836264
      call $f1661
      i32.const 3837344
      call $f1661
      i32.const 3822768
      call $f1661
      i32.const 3836268
      call $f1661
      i32.const 4675161
      i32.const 1
      i32.store8
    end
    block $B1
      block $B2
        local.get $p0
        i32.load8_u offset=172
        i32.eqz
        if $I3
          i32.const 4675133
          i32.load8_u
          i32.eqz
          if $I4
            i32.const 3765356
            call $f1661
            i32.const 3748320
            call $f1661
            i32.const 4675133
            i32.const 1
            i32.store8
          end
          local.get $l2
          i32.const 0
          i32.store offset=32
          i32.const 3748320
          i32.load
          local.tee $p1
          i32.load offset=116
          if $I5 (result i32)
            local.get $p1
          else
            local.get $p1
            call $f65192
            i32.const 3748320
            i32.load
          end
          i32.load offset=92
          i32.load
          local.get $l2
          i32.const 32
          i32.add
          i32.const 3765356
          i32.load
          call $f49306
          if $I6
            local.get $p0
            local.get $l2
            i32.load offset=32
            local.get $p0
            call $f61066
            drop
          end
          block $B7
            local.get $p0
            i32.load8_u offset=16
            i32.eqz
            br_if $B7
            local.get $p0
            local.get $p0
            f32.load offset=24
            i32.const 0
            call $f54555
            f32.add
            local.tee $l6
            f32.store offset=24
            local.get $l6
            f32.const 0x1.4p+2 (;=5;)
            f32.ge
            i32.eqz
            br_if $B7
            i32.const 3748808
            i32.load
            local.tee $p1
            i32.load offset=116
            i32.eqz
            if $I8
              local.get $p1
              call $f65192
            end
            i32.const 3822768
            i32.load
            i32.const 0
            call $f42976
            local.get $p0
            i32.const 0
            i32.store offset=24
            local.get $p0
            i32.const 0
            i32.store8 offset=16
            local.get $p0
            i32.load8_u offset=100
            br_if $B7
            local.get $p0
            local.get $p0
            call $f61069
            local.get $p0
            i32.load8_u offset=100
            br_if $B7
            local.get $p0
            i32.const 3836268
            i32.load
            f32.const 0x1p+4 (;=16;)
            i32.const 0
            call $f54430
          end
          block $B9
            local.get $p0
            i32.load8_u offset=236
            i32.eqz
            br_if $B9
            block $B10
              block $B11
                local.get $p0
                i32.load offset=112
                local.tee $p1
                i32.load offset=24
                i32.eqz
                if $I12
                  local.get $p1
                  i32.load offset=8
                  local.set $p1
                  local.get $p0
                  i32.load offset=212
                  local.set $l3
                  i32.const 3752504
                  i32.load
                  local.tee $l4
                  i32.load offset=116
                  i32.eqz
                  br_if $B11
                  br $B10
                end
                local.get $p1
                i32.load offset=8
                local.set $p1
                local.get $p0
                i32.load offset=216
                local.set $l3
                i32.const 3752504
                i32.load
                local.tee $l4
                i32.load offset=116
                br_if $B10
              end
              local.get $l4
              call $f65192
            end
            local.get $l3
            block $B13 (result i32)
              local.get $p1
              f64.convert_i32_s
              f64.const 0x1p-1 (;=0.5;)
              f64.mul
              f64.floor
              local.tee $l12
              f64.abs
              f64.const 0x1p+31 (;=2.14748e+09;)
              f64.lt
              if $I14
                local.get $l12
                i32.trunc_f64_s
                br $B13
              end
              i32.const -2147483648
            end
            i32.const 3773132
            i32.load
            call $f2903
            local.set $p1
            local.get $p0
            i32.load offset=184
            i32.const 0
            call $f54401
            local.set $l3
            local.get $l2
            i32.const 32
            i32.add
            local.get $p1
            i32.const 0
            call $f54401
            i32.const 0
            call $f54624
            local.get $l2
            f32.load offset=32
            local.set $l6
            local.get $l2
            f32.load offset=36
            local.set $l7
            local.get $p0
            f32.load offset=204
            local.set $l8
            local.get $p0
            f32.load offset=200
            local.set $l9
            local.get $l2
            i32.const 24
            i32.add
            local.tee $l4
            local.get $l2
            f32.load offset=40
            local.get $p0
            f32.load offset=208
            f32.sub
            f32.store
            local.get $l2
            local.get $l4
            i32.load
            i32.store offset=8
            local.get $l2
            local.get $l7
            local.get $l8
            f32.sub
            f32.store offset=20
            local.get $l2
            local.get $l6
            local.get $l9
            f32.sub
            f32.store offset=16
            local.get $l2
            local.get $l2
            i64.load offset=16
            i64.store
            local.get $l3
            local.get $l2
            i32.const 0
            call $f54626
            local.get $l2
            i32.const 32
            i32.add
            local.get $p1
            i32.const 0
            call $f54401
            i32.const 0
            call $f54624
            local.get $l2
            f32.load offset=40
            local.set $l6
            local.get $l2
            f32.load offset=36
            local.set $l7
            local.get $l2
            f32.load offset=32
            local.set $l8
            local.get $p0
            f32.load offset=228
            local.set $l9
            local.get $p0
            f32.load offset=224
            local.set $l10
            local.get $p0
            f32.load offset=220
            local.set $l11
            i32.const 4675187
            i32.load8_u
            i32.eqz
            if $I15
              i32.const 3752504
              call $f1661
              i32.const 4675187
              i32.const 1
              i32.store8
            end
            i32.const 3752504
            i32.load
            local.tee $l3
            i32.load offset=116
            i32.eqz
            if $I16
              local.get $l3
              call $f65192
            end
            local.get $l2
            i32.const 32
            i32.add
            local.get $p1
            i32.const 3792572
            i32.load
            call $f34548
            i32.const 0
            call $f32519
            local.get $l8
            local.get $l11
            f32.sub
            local.tee $l8
            local.get $l8
            f32.mul
            local.get $l7
            local.get $l10
            f32.sub
            local.tee $l7
            local.get $l7
            f32.mul
            f32.add
            local.get $l6
            local.get $l9
            f32.sub
            local.tee $l6
            local.get $l6
            f32.mul
            f32.add
            f32.sqrt
            f32.const 0x1p+0 (;=1;)
            f32.gt
            i32.eqz
            br_if $B9
            local.get $l2
            f32.load offset=32
            local.tee $l6
            local.get $l6
            f32.mul
            local.get $l2
            f32.load offset=36
            local.tee $l6
            local.get $l6
            f32.mul
            f32.add
            local.get $l2
            f32.load offset=40
            local.tee $l6
            local.get $l6
            f32.mul
            f32.add
            f32.const 0x1.0c6f7ap-20 (;=1e-06;)
            f32.lt
            i32.eqz
            br_if $B9
            i32.const 3748808
            i32.load
            local.tee $l3
            i32.load offset=116
            i32.eqz
            if $I17
              local.get $l3
              call $f65192
            end
            i32.const 3824044
            i32.load
            i32.const 0
            call $f42976
            local.get $p1
            i32.const 3792496
            i32.load
            call $f34548
            i32.const 0
            call $f32557
            f32.const 0x1.333334p-1 (;=0.6;)
            i32.const 0
            call $f32511
            local.get $p1
            i32.const 3792496
            i32.load
            call $f34548
            i32.const 0
            call $f32557
            f32.const 0x1.333334p-1 (;=0.6;)
            i32.const 0
            call $f32512
            i32.const 3820972
            i32.load
            i32.const 0
            call $f54416
            local.set $p1
            i32.const 3753376
            i32.load
            local.tee $l3
            i32.load offset=116
            i32.eqz
            if $I18
              local.get $l3
              call $f65192
            end
            local.get $p1
            i32.const 0
            i32.const 0
            call $f54398
            if $I19
              i32.const 3820972
              i32.load
              i32.const 0
              call $f54416
              i32.const 3792588
              i32.load
              call $f34548
              i32.const 0
              i32.store8 offset=24
            end
            local.get $p0
            local.get $p0
            call $f61089
            i32.eqz
            br_if $B9
            local.get $p0
            i32.const 0
            i32.store8 offset=236
            local.get $p0
            i32.load offset=112
            local.tee $p1
            local.get $p1
            i32.load offset=8
            i32.const 1
            i32.add
            local.tee $l3
            i32.store offset=8
            local.get $p0
            i32.load8_u offset=100
            if $I20 (result i32)
              local.get $p0
              local.get $p0
              i32.const 124
              i32.add
              local.get $p0
              call $f61068
              local.get $p0
              i32.load offset=112
              local.tee $p1
              i32.load offset=8
            else
              local.get $l3
            end
            i32.const 16
            i32.eq
            if $I21
              local.get $p0
              i32.load offset=176
              local.set $l3
              local.get $p0
              local.get $p0
              call $f61076
              local.get $p0
              i32.load offset=112
              local.tee $p1
              i32.load offset=20
              local.get $p1
              i32.load offset=12
              i32.const 2
              i32.shl
              i32.add
              local.get $p0
              local.get $p1
              local.get $p0
              call $f61077
              i32.store offset=16
              local.get $p0
              i32.load8_u offset=100
              local.set $p1
              local.get $l3
              i32.const 7
              i32.eq
              if $I22
                local.get $p1
                i32.const 255
                i32.and
                i32.eqz
                if $I23
                  local.get $p0
                  local.get $p0
                  call $f61069
                end
                local.get $p0
                i32.load offset=112
                local.tee $p1
                i32.const 0
                i32.store offset=8
                local.get $p1
                local.get $p1
                i32.load offset=12
                i32.const 1
                i32.add
                i32.store offset=12
                local.get $p0
                local.get $p0
                call $f61085
                local.get $p0
                i32.load offset=112
                local.tee $p1
                local.get $p1
                i32.load offset=12
                i32.const 1
                i32.sub
                local.tee $l3
                i32.store offset=12
                local.get $p1
                i32.load offset=16
                local.get $l3
                i32.gt_s
                if $I24
                  local.get $p0
                  local.get $p0
                  call $f61078
                  local.get $p0
                  local.get $p0
                  call $f61076
                  local.get $p0
                  i32.load8_u offset=100
                  if $I25
                    local.get $p0
                    i32.const 0
                    i32.store offset=144
                    local.get $p0
                    i32.load offset=112
                    i32.const 0
                    i32.store offset=24
                    br $B9
                  end
                  local.get $p0
                  local.get $p0
                  call $f61069
                  local.get $p0
                  i32.load offset=112
                  local.set $p1
                end
                local.get $p0
                i32.const 0
                i32.store offset=144
                local.get $p0
                i32.load8_u offset=100
                local.set $l3
                local.get $p1
                i32.const 0
                i32.store offset=24
                local.get $l3
                br_if $B9
                i32.const 0
                call $f54556
                local.set $l6
                local.get $p0
                i32.const 3836268
                i32.load
                local.get $l6
                i32.const 0
                call $f54430
                br $B9
              end
              local.get $p1
              i32.const 255
              i32.and
              i32.eqz
              if $I26
                local.get $p0
                local.get $p0
                call $f61069
              end
              i32.const 0
              local.set $l4
              block $B27
                local.get $p0
                i32.load offset=112
                local.tee $p1
                i32.load offset=20
                local.get $p1
                i32.load offset=12
                local.tee $l3
                i32.const 2
                i32.shl
                i32.add
                i32.load offset=16
                local.tee $l5
                i32.const 0
                i32.le_s
                if $I28
                  local.get $l5
                  i32.const 0
                  i32.ge_s
                  br_if $B27
                  i32.const 1
                  local.set $l4
                end
                local.get $p1
                local.get $l4
                i32.store offset=24
              end
              local.get $p1
              local.get $l3
              i32.const 1
              i32.add
              i32.store offset=12
              local.get $p0
              local.get $p0
              call $f61085
              block $B29
                local.get $p0
                i32.load offset=112
                local.tee $p1
                i32.load offset=12
                local.get $p1
                i32.load offset=16
                i32.lt_s
                if $I30
                  i32.const 0
                  call $f54556
                  local.set $l6
                  local.get $p0
                  i32.const 3835540
                  i32.load
                  local.get $l6
                  f32.const 0x1.4p+2 (;=5;)
                  f32.mul
                  i32.const 0
                  call $f54430
                  local.get $p0
                  local.get $p0
                  call $f61076
                  local.get $p0
                  i32.load8_u offset=100
                  br_if $B29
                  i32.const 0
                  call $f54556
                  local.set $l6
                  local.get $p0
                  i32.const 3836264
                  i32.load
                  local.get $l6
                  f32.const 0x1.4p+2 (;=5;)
                  f32.mul
                  f32.const 0x1.99999ap-4 (;=0.1;)
                  f32.add
                  i32.const 0
                  call $f54430
                  br $B29
                end
                block $B31
                  local.get $p0
                  i32.load8_u offset=100
                  br_if $B31
                  local.get $p0
                  local.get $p0
                  call $f61069
                  local.get $p0
                  i32.load8_u offset=100
                  br_if $B31
                  local.get $p0
                  local.get $p0
                  call $f61093
                end
                local.get $p0
                i32.load offset=212
                i32.const 0
                i32.const 3773132
                i32.load
                call $f2903
                i32.const 0
                i32.const 0
                call $f54405
                local.get $p0
                i32.load offset=216
                i32.const 0
                i32.const 3773132
                i32.load
                call $f2903
                i32.const 0
                i32.const 0
                call $f54405
                local.get $p0
                i32.load offset=212
                i32.const 1
                i32.const 3773132
                i32.load
                call $f2903
                i32.const 0
                i32.const 0
                call $f54405
                local.get $p0
                i32.load offset=216
                i32.const 1
                i32.const 3773132
                i32.load
                call $f2903
                i32.const 0
                i32.const 0
                call $f54405
                local.get $p0
                i32.load offset=212
                i32.const 2
                i32.const 3773132
                i32.load
                call $f2903
                i32.const 0
                i32.const 0
                call $f54405
                local.get $p0
                i32.load offset=216
                i32.const 2
                i32.const 3773132
                i32.load
                call $f2903
                i32.const 0
                i32.const 0
                call $f54405
                local.get $p0
                i32.load offset=212
                i32.const 3
                i32.const 3773132
                i32.load
                call $f2903
                i32.const 0
                i32.const 0
                call $f54405
                local.get $p0
                i32.load offset=216
                i32.const 3
                i32.const 3773132
                i32.load
                call $f2903
                i32.const 0
                i32.const 0
                call $f54405
                local.get $p0
                i32.load offset=212
                i32.const 4
                i32.const 3773132
                i32.load
                call $f2903
                i32.const 0
                i32.const 0
                call $f54405
                local.get $p0
                i32.load offset=216
                i32.const 4
                i32.const 3773132
                i32.load
                call $f2903
                i32.const 0
                i32.const 0
                call $f54405
                local.get $p0
                i32.load offset=212
                i32.const 5
                i32.const 3773132
                i32.load
                call $f2903
                i32.const 0
                i32.const 0
                call $f54405
                local.get $p0
                i32.load offset=216
                i32.const 5
                i32.const 3773132
                i32.load
                call $f2903
                i32.const 0
                i32.const 0
                call $f54405
                local.get $p0
                i32.load offset=212
                i32.const 6
                i32.const 3773132
                i32.load
                call $f2903
                i32.const 0
                i32.const 0
                call $f54405
                local.get $p0
                i32.load offset=216
                i32.const 6
                i32.const 3773132
                i32.load
                call $f2903
                i32.const 0
                i32.const 0
                call $f54405
                local.get $p0
                i32.load offset=212
                i32.const 7
                i32.const 3773132
                i32.load
                call $f2903
                i32.const 0
                i32.const 0
                call $f54405
                local.get $p0
                i32.load offset=216
                i32.const 7
                i32.const 3773132
                i32.load
                call $f2903
                i32.const 0
                i32.const 0
                call $f54405
                local.get $p0
                i32.const 1
                i32.store8 offset=172
                local.get $p0
                local.get $p0
                local.get $p0
                call $f61083
                i64.store offset=288
              end
              i32.const 0
              call $f54556
              local.set $l6
              local.get $p0
              i32.const 3836548
              i32.load
              local.get $l6
              f32.const 0x1.4p+2 (;=5;)
              f32.mul
              i32.const 0
              call $f54430
              br $B9
            end
            local.get $p0
            i32.load8_u offset=172
            br_if $B9
            local.get $p1
            local.get $p1
            i32.load offset=24
            i32.const 1
            i32.xor
            i32.store offset=24
            local.get $p0
            local.get $p0
            call $f61076
            local.get $p0
            i32.const 0
            i32.store8 offset=236
            local.get $p0
            i32.load8_u offset=16
            br_if $B1
            local.get $p0
            i32.load8_u offset=100
            br_if $B9
            local.get $p0
            local.get $p0
            call $f61069
            local.get $p0
            i32.load8_u offset=100
            br_if $B9
            local.get $p0
            i32.const 3836268
            i32.load
            f32.const 0x1p+4 (;=16;)
            i32.const 0
            call $f54430
          end
          local.get $p0
          i32.load8_u offset=106
          i32.eqz
          br_if $B2
          local.get $p0
          local.get $p0
          f32.load offset=108
          i32.const 0
          call $f54144
          i32.const 0
          call $f54556
          f32.div
          f32.add
          f32.store offset=108
          br $B2
        end
        local.get $p0
        i32.load offset=68
        i32.const 0
        i32.const 0
        call $f54405
        i32.const 3821460
        i32.load
        i32.const 0
        call $f54416
        i32.const 3792480
        i32.load
        call $f34548
        local.set $p1
        local.get $l2
        i32.const 2
        i32.store offset=32
        i32.const 3751540
        i32.load
        local.get $l2
        i32.const 32
        i32.add
        call $f1675
        local.set $l3
        local.get $p1
        i32.const 3837344
        i32.load
        local.get $l3
        i32.const 0
        call $f54371
      end
      local.get $p0
      i32.load8_u offset=256
      i32.eqz
      br_if $B1
      i32.const 0
      call $f54530
      local.get $p0
      f32.load offset=260
      local.get $p0
      f32.load offset=264
      f32.add
      f32.gt
      i32.eqz
      br_if $B1
      local.get $p0
      i64.const 0
      i64.store offset=260 align=4
      local.get $p0
      i32.const 0
      i32.store8 offset=256
      f32.const 0x1p+0 (;=1;)
      local.get $p0
      f32.load offset=268
      local.tee $l6
      local.get $l6
      f32.const 0x0p+0 (;=0;)
      f32.eq
      select
      i32.const 0
      call $f54557
    end
    local.get $l2
    i32.const 48
    i32.add
    global.set $g0)
