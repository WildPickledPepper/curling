  (func $f70081 (type $t28) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 i32) (param $p7 i32) (param $p8 i32) (result i32)
    (local $l9 i32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32)
    global.get $g0
    i32.const 96
    i32.sub
    local.tee $l9
    global.set $g0
    block $B0 (result i32)
      block $B1
        block $B2
          block $B3
            block $B4
              local.get $p3
              i32.const 2
              i32.sub
              br_table $B3 $B2 $B4 $B2
            end
            i32.const 1
            local.get $p7
            f32.load offset=32
            local.tee $l13
            local.get $p7
            f32.load offset=48
            f32.mul
            local.get $p7
            f32.load offset=36
            local.tee $l14
            local.get $p7
            f32.load offset=52
            f32.mul
            f32.add
            local.get $p7
            f32.load offset=40
            local.tee $l10
            local.get $p7
            f32.load offset=56
            f32.mul
            f32.add
            f32.const 0x1.fff2e4p-1 (;=0.9999;)
            f32.gt
            i32.eqz
            br_if $B0
            drop
            local.get $l9
            i32.const 80
            i32.add
            local.get $p0
            local.get $p0
            i32.load
            i32.load offset=16
            call_indirect $__indirect_function_table (type $t1)
            local.get $l9
            i32.const -64
            i32.sub
            local.get $p1
            local.get $p1
            i32.load
            i32.load offset=16
            call_indirect $__indirect_function_table (type $t1)
            local.get $l10
            local.get $l9
            f32.load offset=88
            local.get $l9
            f32.load offset=72
            f32.sub
            local.tee $l10
            f32.const 0x1p+0 (;=1;)
            local.get $l9
            f32.load offset=80
            local.get $l9
            f32.load offset=64
            f32.sub
            local.tee $l11
            local.get $l11
            f32.mul
            local.get $l9
            f32.load offset=84
            local.get $l9
            f32.load offset=68
            f32.sub
            local.tee $l12
            local.get $l12
            f32.mul
            f32.add
            local.get $l10
            local.get $l10
            f32.mul
            f32.add
            f32.sqrt
            f32.div
            local.tee $l10
            f32.mul
            f32.mul
            local.get $l13
            local.get $l11
            local.get $l10
            f32.mul
            f32.mul
            local.get $l14
            local.get $l12
            local.get $l10
            f32.mul
            f32.mul
            f32.add
            f32.add
            f32.const 0x1.69fbe8p-1 (;=0.707;)
            f32.gt
            local.tee $p3
            if $I5
              local.get $l9
              local.get $p5
              i64.load
              i64.store offset=32
              local.get $l9
              local.get $p5
              i64.load offset=8
              i64.store offset=40
              local.get $p4
              local.get $p8
              local.get $p7
              local.get $p2
              local.get $l9
              i32.const 32
              i32.add
              call $f69981
            end
            local.get $p3
            i32.const 1
            i32.xor
            br $B0
          end
          local.get $l9
          local.get $p5
          i64.load
          i64.store offset=48
          local.get $l9
          local.get $p5
          i64.load offset=8
          i64.store offset=56
          local.get $p4
          local.get $p8
          local.get $p7
          local.get $p2
          local.get $l9
          i32.const 48
          i32.add
          call $f69981
          br $B1
        end
        local.get $p8
        i32.load8_u offset=66
        local.set $p3
        local.get $l9
        local.get $p6
        i64.load
        i64.store offset=16
        local.get $l9
        local.get $p6
        i64.load offset=8
        i64.store offset=24
        i32.const 1
        local.get $p0
        local.get $p1
        local.get $p8
        i32.const 67
        i32.add
        local.get $p8
        i32.const 71
        i32.add
        local.get $p3
        i32.const 1
        local.get $l9
        i32.const 16
        i32.add
        local.get $p7
        call $f69898
        i32.const 5
        i32.ne
        br_if $B0
        drop
        local.get $l9
        local.get $p5
        i64.load
        i64.store
        local.get $l9
        local.get $p5
        i64.load offset=8
        i64.store offset=8
        local.get $p4
        local.get $p8
        local.get $p7
        local.get $p2
        local.get $l9
        call $f69981
      end
      i32.const 0
    end
    local.set $p3
    local.get $l9
    i32.const 96
    i32.add
    global.set $g0
    local.get $p3)