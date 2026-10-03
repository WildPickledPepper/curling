  (func $f77469 (type $t193) (param $p0 f32)
    (local $l1 i32) (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 f64)
    block $B0
      i32.const 4718208
      i32.load
      local.tee $l1
      i32.load8_u offset=73
      br_if $B0
      block $B1
        block $B2
          local.get $l1
          i32.load offset=8
          local.tee $l2
          br_table $B2 $B1 $B1 $B0 $B1
        end
        global.get $g0
        i32.const 128
        i32.sub
        local.tee $l1
        global.set $g0
        i32.const 4718208
        i32.load
        local.tee $l2
        i32.load offset=8
        i32.const 1
        i32.ne
        if $I3
          local.get $l2
          i32.const 1
          i32.store offset=8
          i32.const 4823504
          i32.const 1
          call $f69606
        end
        i32.const 0
        call $f80140
        local.tee $l4
        i32.const 216
        i32.add
        local.set $l5
        block $B4 (result f32)
          block $B5
            block $B6
              block $B7
                local.get $l4
                i32.load offset=228
                i32.const 1
                i32.sub
                br_table $B7 $B6 $B5
              end
              i32.const 4718208
              i32.load
              i32.const 1045220557
              i32.store
              f32.const 0x1.333334p-1 (;=0.6;)
              br $B4
            end
            i32.const 4718208
            i32.load
            local.get $l4
            f32.load offset=236
            f32.store
            local.get $l4
            f32.load offset=240
            br $B4
          end
          i32.const 4718208
          i32.load
          i32.const 0
          i32.store
          f32.const 0x0p+0 (;=0;)
        end
        local.set $p0
        i32.const 4718208
        i32.load
        local.get $p0
        f32.store offset=4
        local.get $l1
        i32.const 56
        i32.add
        local.get $l5
        call $f77015
        block $B8
          block $B9
            block $B10
              local.get $l1
              i32.load offset=56
              local.tee $l2
              i32.eqz
              if $I11
                i32.const 4718208
                i32.load
                i32.const 0
                i32.store offset=52
                br $B10
              end
              local.get $l1
              local.get $l2
              i32.store offset=24
              block $B12
                i32.const 4782060
                i32.load
                local.tee $l2
                i32.eqz
                br_if $B12
                local.get $l1
                i32.const -64
                i32.sub
                local.get $l2
                local.get $l1
                i32.const 24
                i32.add
                call $f66830
                local.get $l1
                i32.load offset=64
                local.tee $l3
                i32.const 4782060
                i32.load
                local.tee $l2
                i32.load
                local.get $l2
                i32.load offset=4
                i32.const 3
                i32.mul
                i32.add
                i32.const 12
                i32.add
                i32.eq
                br_if $B12
                local.get $l3
                i32.load offset=8
                local.tee $l2
                i32.eqz
                br_if $B12
                i32.const 4718208
                i32.load
                local.tee $l3
                local.get $l2
                i32.store offset=52
                br $B9
              end
              local.get $l1
              i32.load offset=56
              call $f80110
              local.set $l2
              i32.const 4718208
              i32.load
              local.tee $l3
              local.get $l2
              i32.store offset=52
              local.get $l2
              br_if $B9
            end
            local.get $l5
            call $f77427
            br_if $B8
            i32.const 4718208
            i32.load
            local.set $l3
          end
          local.get $l3
          i32.load offset=60
          i32.eqz
          if $I13
            i32.const 4
            call $f80140
            local.set $l2
            local.get $l1
            i32.const 157124
            call $f80271
            i32.store offset=60
            local.get $l1
            i32.const 157124
            i32.store offset=56
            local.get $l2
            local.get $l1
            i32.const 56
            i32.add
            call $f77313
            local.tee $l2
            if $I14 (result i32)
              local.get $l2
            else
              local.get $l1
              i32.const 24
              i32.add
              i32.const 369827
              i32.const 0
              call $f569
              local.get $l1
              i32.const 403047
              i32.store offset=124
              local.get $l1
              i32.const 403047
              i32.store offset=120
              local.get $l1
              i64.const 0
              i64.store offset=112
              local.get $l1
              i32.const 403047
              i32.store offset=76
              local.get $l1
              i32.const 403047
              i32.store offset=72
              local.get $l1
              i32.const 403047
              i32.store offset=68
              local.get $l1
              i64.const 0
              i64.store offset=100 align=4
              local.get $l1
              i64.const 1
              i64.store offset=92 align=4
              local.get $l1
              i64.const -4294966983
              i64.store offset=84 align=4
              local.get $l1
              i32.const 403047
              i32.store offset=80
              local.get $l1
              i32.const 1
              i32.store8 offset=108
              local.get $l1
              local.get $l1
              i32.const 24
              i32.add
              local.get $l1
              i32.load offset=24
              local.get $l1
              i32.load8_u offset=44
              i32.const 1
              i32.eq
              select
              i32.store offset=64
              local.get $l1
              i32.const -64
              i32.sub
              call $f83275
              local.get $l1
              i32.load8_u offset=44
              i32.eqz
              if $I15
                local.get $l1
                i32.load offset=24
                local.get $l1
                i32.load offset=48
                i32.const 403047
                i32.const 518
                call $f83342
              end
              i32.const 4
              call $f80140
              local.set $l2
              local.get $l1
              i32.const 94977
              call $f80271
              i32.store offset=20
              local.get $l1
              i32.const 94977
              i32.store offset=16
              local.get $l2
              local.get $l1
              i32.const 16
              i32.add
              call $f77313
            end
            i32.const 61
            call $f77311
            local.set $l2
            i32.const 4718208
            i32.load
            local.get $l2
            i32.store offset=60
            local.get $l2
            i32.const 176931
            local.get $l2
            i32.load
            i32.load offset=44
            call_indirect $__indirect_function_table (type $t1)
            i32.const 4718208
            i32.load
            local.set $l3
          end
          local.get $l3
          i32.load offset=64
          i32.eqz
          if $I16
            i32.const 4
            call $f80140
            local.set $l2
            local.get $l1
            i32.const 15
            i32.store offset=12
            local.get $l1
            i32.const 54672
            i32.store offset=8
            local.get $l2
            local.get $l1
            i32.const 8
            i32.add
            call $f77313
            local.tee $l2
            if $I17 (result i32)
              local.get $l2
            else
              local.get $l1
              i32.const 24
              i32.add
              i32.const 368873
              i32.const 0
              call $f569
              local.get $l1
              i32.const 403047
              i32.store offset=124
              local.get $l1
              i32.const 403047
              i32.store offset=120
              local.get $l1
              i64.const 0
              i64.store offset=112
              local.get $l1
              i32.const 403047
              i32.store offset=76
              local.get $l1
              i32.const 403047
              i32.store offset=72
              local.get $l1
              i32.const 403047
              i32.store offset=68
              local.get $l1
              i64.const 0
              i64.store offset=100 align=4
              local.get $l1
              i64.const 1
              i64.store offset=92 align=4
              local.get $l1
              i64.const -4294966971
              i64.store offset=84 align=4
              local.get $l1
              i32.const 403047
              i32.store offset=80
              local.get $l1
              i32.const 1
              i32.store8 offset=108
              local.get $l1
              local.get $l1
              i32.const 24
              i32.add
              local.get $l1
              i32.load offset=24
              local.get $l1
              i32.load8_u offset=44
              i32.const 1
              i32.eq
              select
              i32.store offset=64
              local.get $l1
              i32.const -64
              i32.sub
              call $f83275
              local.get $l1
              i32.load8_u offset=44
              i32.eqz
              if $I18
                local.get $l1
                i32.load offset=24
                local.get $l1
                i32.load offset=48
                i32.const 403047
                i32.const 518
                call $f83342
              end
              i32.const 4
              call $f80140
              local.set $l2
              local.get $l1
              i32.const 94977
              call $f80271
              i32.store offset=68
              local.get $l1
              i32.const 94977
              i32.store offset=64
              local.get $l2
              local.get $l1
              i32.const -64
              i32.sub
              call $f77313
            end
            i32.const 61
            call $f77311
            local.set $l2
            i32.const 4718208
            i32.load
            local.get $l2
            i32.store offset=64
            local.get $l2
            i32.const 176955
            local.get $l2
            i32.load
            i32.load offset=44
            call_indirect $__indirect_function_table (type $t1)
            i32.const 4718208
            i32.load
            local.set $l3
          end
          local.get $l3
          i32.const 0
          i32.store offset=12
          block $B19
            local.get $l4
            i32.load offset=296
            i32.eqz
            if $I20
              f32.const 0x0p+0 (;=0;)
              local.set $p0
              br $B19
            end
            local.get $l4
            i32.load offset=288
            local.set $l2
            loop $L21
              local.get $l5
              call $f77427
              if $I22
                block $B23
                  local.get $l2
                  i32.load
                  local.tee $l3
                  i32.eqz
                  if $I24
                    i32.const 0
                    local.set $l3
                    br $B23
                  end
                  local.get $l1
                  local.get $l3
                  i32.store offset=24
                  block $B25
                    i32.const 4782060
                    i32.load
                    local.tee $l3
                    i32.eqz
                    br_if $B25
                    local.get $l1
                    i32.const -64
                    i32.sub
                    local.get $l3
                    local.get $l1
                    i32.const 24
                    i32.add
                    call $f66830
                    local.get $l1
                    i32.load offset=64
                    local.tee $l7
                    i32.const 4782060
                    i32.load
                    local.tee $l3
                    i32.load
                    local.get $l3
                    i32.load offset=4
                    i32.const 3
                    i32.mul
                    i32.add
                    i32.const 12
                    i32.add
                    i32.eq
                    br_if $B25
                    local.get $l7
                    i32.load offset=8
                    local.tee $l3
                    br_if $B23
                  end
                  local.get $l2
                  i32.load
                  call $f80110
                  local.set $l3
                end
                local.get $l5
                local.get $l3
                call $f77428
                local.get $l6
                i32.or
                local.set $l6
              end
              i32.const 4718208
              i32.load
              local.tee $l3
              local.get $l3
              f32.load offset=12
              local.get $l2
              f32.load offset=4
              f32.const 0x1p+1 (;=2;)
              call $f65475
              f32.add
              local.tee $p0
              f32.store offset=12
              local.get $l2
              i32.const 8
              i32.add
              local.tee $l2
              local.get $l4
              i32.load offset=288
              local.get $l4
              i32.load offset=296
              i32.const 3
              i32.shl
              i32.add
              i32.ne
              br_if $L21
            end
          end
          local.get $l3
          local.get $p0
          f32.const 0x1p+1 (;=2;)
          f32.max
          f32.store offset=12
          block $B26
            local.get $l5
            call $f77427
            br_if $B26
            i32.const 10
            call $f80140
            i32.load8_u offset=108
            i32.eqz
            br_if $B26
            i32.const 4718208
            i32.load
            local.tee $l2
            i32.const 0
            i32.store offset=68
            local.get $l2
            i32.const 0
            i32.store8 offset=74
            i32.const 0
            call $f77468
            drop
            br $B8
          end
          i32.const 4718208
          i32.load
          local.tee $l2
          i32.const 0
          i32.store offset=68
          local.get $l2
          local.get $l6
          i32.const -1
          i32.xor
          i32.const 1
          i32.and
          i32.store8 offset=74
          i32.const 0
          call $f77468
          br_if $B8
          i32.const 4718208
          i32.load
          local.tee $l2
          i64.const 4611686018427387904
          i64.store offset=32
          local.get $l2
          i32.const 0
          i32.store8 offset=74
          local.get $l2
          local.get $l2
          i32.load offset=52
          i32.store offset=56
        end
        call $f80340
        local.set $l8
        i32.const 4718208
        i32.load
        local.tee $l2
        i32.const 0
        i32.store8 offset=72
        local.get $l2
        local.get $l8
        f64.store offset=16
        local.get $l2
        local.get $l8
        f64.store offset=24
        local.get $l1
        i32.const 128
        i32.add
        global.set $g0
        return
      end
      local.get $l1
      f64.load offset=32
      local.get $p0
      f64.promote_f32
      f64.le
      i32.eqz
      br_if $B0
      block $B27
        local.get $l2
        i32.const 1
        i32.eq
        if $I28
          local.get $l1
          local.get $l1
          i32.load offset=68
          i32.const 1
          i32.add
          local.tee $l2
          i32.store offset=68
          local.get $l2
          call $f77468
          br_if $B27
          i32.const 4718208
          i32.load
          local.tee $l1
          i32.load offset=8
          i32.const 2
          i32.ne
          if $I29 (result i32)
            local.get $l1
            i32.const 2
            i32.store offset=8
            i32.const 4823504
            i32.const 2
            call $f69606
            i32.const 4718208
            i32.load
          else
            local.get $l1
          end
          i64.const 4602678819172646912
          i64.store offset=32
          call $f80340
          local.set $l8
          i32.const 4718208
          i32.load
          local.get $l8
          f64.store offset=24
          return
        end
        local.get $l1
        i32.const 3
        i32.store offset=8
        i32.const 4823504
        i32.const 3
        call $f69606
        i32.const 4718208
        i32.load
        i32.const 0
        i32.store8 offset=72
      end
      call $f80340
      local.set $l8
      i32.const 4718208
      i32.load
      local.get $l8
      f64.store offset=24
    end)
