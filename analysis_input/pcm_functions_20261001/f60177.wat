  (func $f60177 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l4
    global.set $g0
    i32.const 4674518
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3745968
      call $f1661
      i32.const 3826444
      call $f1661
      i32.const 3835808
      call $f1661
      i32.const 3813948
      call $f1661
      i32.const 3833976
      call $f1661
      i32.const 3835768
      call $f1661
      i32.const 3814080
      call $f1661
      i32.const 4674518
      i32.const 1
      i32.store8
    end
    local.get $l4
    i64.const 0
    i64.store offset=8
    local.get $l4
    i32.const 0
    i32.store offset=4
    i32.const 3833976
    i32.load
    local.set $l3
    block $B1
      block $B2
        local.get $p0
        i32.load offset=96
        local.tee $l2
        i32.load offset=8
        i32.const 16
        i32.ne
        br_if $B2
        i32.const 0
        local.set $p1
        local.get $l2
        i32.load offset=12
        i32.const 0
        i32.lt_s
        br_if $B2
        loop $L3
          local.get $p1
          i32.const 1
          i32.or
          local.set $l5
          block $B4 (result i32)
            block $B5
              local.get $l2
              i32.load offset=28
              local.tee $l2
              local.get $p1
              i32.const 2
              i32.shl
              local.tee $l6
              i32.add
              f32.load offset=16
              f32.const 0x0p+0 (;=0;)
              f32.eq
              if $I6
                local.get $l2
                local.get $l5
                i32.const 2
                i32.shl
                i32.add
                f32.load offset=16
                f32.const 0x0p+0 (;=0;)
                f32.eq
                br_if $B5
              end
              i32.const 3745968
              i32.load
              i32.const 5
              call $f1052
              local.tee $l2
              local.get $l3
              i32.store offset=16
              local.get $l2
              i32.const 3813948
              i32.load
              i32.store offset=20
              local.get $l4
              local.get $p0
              i32.load offset=96
              i32.load offset=28
              local.get $l6
              i32.add
              f32.load offset=16
              f64.promote_f32
              f64.const 0x1.3p+1 (;=2.375;)
              f64.add
              f64.store offset=8
              local.get $l2
              local.get $l4
              i32.const 8
              i32.add
              i32.const 3826444
              i32.load
              i32.const 0
              call $f50680
              i32.store offset=24
              local.get $l2
              i32.const 3813948
              i32.load
              i32.store offset=28
              local.get $l4
              local.get $p0
              i32.load offset=96
              i32.load offset=28
              local.get $l5
              i32.const 2
              i32.shl
              i32.add
              f32.load offset=16
              f64.promote_f32
              f64.const 0x1.3851eb851eb85p+2 (;=4.88;)
              f64.add
              f64.store offset=8
              local.get $l2
              local.get $l4
              i32.const 8
              i32.add
              i32.const 3826444
              i32.load
              i32.const 0
              call $f50680
              i32.store offset=32
              local.get $l2
              i32.const 0
              call $f53875
              br $B4
            end
            local.get $l3
            i32.const 3814080
            i32.load
            i32.const 0
            call $f53732
          end
          local.set $l3
          local.get $p1
          i32.const 28
          i32.le_u
          if $I7
            local.get $p1
            i32.const 2
            i32.add
            local.set $p1
            local.get $p0
            i32.load offset=96
            local.set $l2
            br $L3
          end
        end
        local.get $p0
        i32.load offset=96
        i32.load offset=44
        local.get $l3
        i32.const 0
        call $f61033
        local.get $p0
        i32.load offset=96
        i32.load offset=68
        local.get $l3
        i32.const 0
        call $f61033
        i32.const 500
        i32.const 0
        call $f52516
        local.get $p0
        i32.load offset=252
        local.get $l3
        i32.const 0
        call $f61055
        local.get $p0
        i32.load offset=96
        local.tee $p1
        i32.load offset=20
        local.get $p1
        i32.load offset=12
        i32.const 2
        i32.shl
        i32.add
        i32.const 16
        i32.add
        i32.const 0
        call $f56590
        local.set $p1
        i32.const 3835768
        i32.load
        local.get $p1
        i32.const 0
        call $f53732
        local.set $l3
        local.get $l4
        i32.const 0
        local.get $p0
        i32.load offset=96
        local.tee $p1
        i32.load offset=20
        local.get $p1
        i32.load offset=12
        i32.const 2
        i32.shl
        i32.add
        i32.load offset=16
        i32.sub
        i32.store offset=4
        local.get $l4
        i32.const 4
        i32.add
        i32.const 0
        call $f56590
        local.set $p1
        i32.const 3835768
        i32.load
        local.get $p1
        i32.const 0
        call $f53732
        local.set $p1
        local.get $p0
        i32.load offset=96
        i32.load offset=44
        local.get $l3
        i32.const 0
        call $f61033
        i32.const 500
        i32.const 0
        call $f52516
        local.get $p0
        local.get $p1
        i32.store offset=152
        local.get $p0
        i32.load offset=96
        i32.load offset=68
        local.get $p1
        i32.const 0
        call $f61033
        br $B1
      end
      i32.const 0
      local.set $p1
      loop $L8
        local.get $p1
        i32.const 1
        i32.or
        local.set $l5
        block $B9 (result i32)
          block $B10
            local.get $l2
            i32.load offset=28
            local.tee $l2
            local.get $p1
            i32.const 2
            i32.shl
            local.tee $l6
            i32.add
            f32.load offset=16
            f32.const 0x0p+0 (;=0;)
            f32.eq
            if $I11
              local.get $l2
              local.get $l5
              i32.const 2
              i32.shl
              i32.add
              f32.load offset=16
              f32.const 0x0p+0 (;=0;)
              f32.eq
              br_if $B10
            end
            i32.const 3745968
            i32.load
            i32.const 5
            call $f1052
            local.tee $l2
            local.get $l3
            i32.store offset=16
            local.get $l2
            i32.const 3813948
            i32.load
            i32.store offset=20
            local.get $l4
            local.get $p0
            i32.load offset=96
            i32.load offset=28
            local.get $l6
            i32.add
            f32.load offset=16
            f64.promote_f32
            f64.const 0x1.3p+1 (;=2.375;)
            f64.add
            f64.store offset=8
            local.get $l2
            local.get $l4
            i32.const 8
            i32.add
            i32.const 3826444
            i32.load
            i32.const 0
            call $f50680
            i32.store offset=24
            local.get $l2
            i32.const 3813948
            i32.load
            i32.store offset=28
            local.get $l4
            local.get $p0
            i32.load offset=96
            i32.load offset=28
            local.get $l5
            i32.const 2
            i32.shl
            i32.add
            f32.load offset=16
            f64.promote_f32
            f64.const 0x1.3851eb851eb85p+2 (;=4.88;)
            f64.add
            f64.store offset=8
            local.get $l2
            local.get $l4
            i32.const 8
            i32.add
            i32.const 3826444
            i32.load
            i32.const 0
            call $f50680
            i32.store offset=32
            local.get $l2
            i32.const 0
            call $f53875
            br $B9
          end
          local.get $l3
          i32.const 3814080
          i32.load
          i32.const 0
          call $f53732
        end
        local.set $l3
        local.get $p1
        i32.const 28
        i32.le_u
        if $I12
          local.get $p1
          i32.const 2
          i32.add
          local.set $p1
          local.get $p0
          i32.load offset=96
          local.set $l2
          br $L8
        end
      end
      local.get $p0
      i32.load offset=96
      i32.load offset=44
      local.get $l3
      i32.const 0
      call $f61033
      local.get $p0
      i32.load offset=96
      i32.load offset=68
      local.get $l3
      i32.const 0
      call $f61033
    end
    local.get $p0
    i32.load offset=252
    local.get $l3
    i32.const 0
    call $f61055
    i32.const 3745968
    i32.load
    i32.const 8
    call $f1052
    local.tee $p1
    i32.const 3835808
    i32.load
    i32.store offset=16
    local.get $p1
    local.get $p0
    i32.load offset=96
    i32.const 8
    i32.add
    i32.const 0
    call $f56590
    i32.store offset=20
    local.get $p1
    i32.const 3813948
    i32.load
    i32.store offset=24
    local.get $p1
    local.get $p0
    i32.load offset=96
    i32.const 12
    i32.add
    i32.const 0
    call $f56590
    i32.store offset=28
    local.get $p1
    i32.const 3813948
    i32.load
    i32.store offset=32
    local.get $p1
    local.get $p0
    i32.load offset=96
    i32.const 16
    i32.add
    i32.const 0
    call $f56590
    i32.store offset=36
    local.get $p1
    i32.const 3813948
    i32.load
    i32.store offset=40
    local.get $p1
    local.get $p0
    i32.load offset=96
    i32.const 24
    i32.add
    i32.const 0
    call $f57314
    i32.store offset=44
    local.get $p1
    i32.const 0
    call $f53875
    local.set $p1
    local.get $p0
    i32.load offset=96
    i32.load offset=44
    local.get $p1
    i32.const 0
    call $f61033
    local.get $p0
    i32.load offset=96
    i32.load offset=68
    local.get $p1
    i32.const 0
    call $f61033
    local.get $p0
    i32.load offset=252
    local.get $p1
    i32.const 0
    call $f61055
    local.get $l4
    i32.const 16
    i32.add
    global.set $g0)
