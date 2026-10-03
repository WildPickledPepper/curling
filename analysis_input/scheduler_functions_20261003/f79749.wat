  (func $f79749 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 f64) (local $l3 f64) (local $l4 f64) (local $l5 f64) (local $l6 i64) (local $l7 i64) (local $l8 i32) (local $l9 i32) (local $l10 i32)
    block $B0
      block $B1
        block $B2
          local.get $p1
          br_table $B2 $B1 $B0
        end
        local.get $p0
        call $f80340
        local.tee $l2
        f64.store offset=248
        local.get $p0
        local.get $p0
        i64.load offset=184
        i64.const 100
        i64.rem_s
        i32.wrap_i64
        i32.const 3
        i32.shl
        i32.add
        local.get $l2
        f64.store offset=256
        i32.const 4774148
        call $f80292
        return
      end
      i32.const 0
      local.set $p1
      i32.const 4774148
      call $f80291
      local.get $p0
      f64.load offset=256
      local.set $l4
      f64.const inf (;=inf;)
      local.set $l2
      loop $L3
        local.get $p0
        local.get $l8
        i32.const 1
        i32.or
        local.tee $l9
        i32.const 3
        i32.shl
        i32.add
        f64.load offset=256
        local.tee $l5
        local.get $l4
        f64.sub
        local.tee $l3
        local.get $l2
        local.get $l2
        local.get $l3
        f64.gt
        select
        local.get $l2
        local.get $l3
        f64.const 0x0p+0 (;=0;)
        f64.gt
        local.tee $l10
        select
        local.set $l2
        local.get $p1
        local.get $l10
        i32.add
        local.set $p1
        local.get $l9
        i32.const 99
        i32.ne
        if $I4
          local.get $p0
          local.get $l8
          i32.const 2
          i32.add
          local.tee $l8
          i32.const 3
          i32.shl
          i32.add
          f64.load offset=256
          local.tee $l4
          local.get $l5
          f64.sub
          local.tee $l3
          local.get $l2
          local.get $l2
          local.get $l3
          f64.gt
          select
          local.get $l2
          local.get $l3
          f64.const 0x0p+0 (;=0;)
          f64.gt
          local.tee $l9
          select
          local.set $l2
          local.get $p1
          local.get $l9
          i32.add
          local.set $p1
          br $L3
        end
      end
      local.get $l2
      f64.const 0x0p+0 (;=0;)
      local.get $p1
      select
      local.tee $l3
      f64.const 0x0p+0 (;=0;)
      f64.gt
      if $I5
        call $f80340
        local.set $l2
        local.get $p0
        f64.load offset=248
        local.set $l4
        call $f1070
        if $I6
          block $B7 (result i64)
            local.get $l3
            local.get $l2
            local.get $l4
            f64.sub
            f64.sub
            f64.const -0x1.0624dd2f1a9fcp-10 (;=-0.001;)
            f64.add
            f64.const 0x1.0624dd2f1a9fcp-10 (;=0.001;)
            f64.max
            f64.const 0x1.dcd65p+29 (;=1e+09;)
            f64.mul
            local.tee $l2
            f64.const 0x1p+64 (;=1.84467e+19;)
            f64.lt
            local.get $l2
            f64.const 0x0p+0 (;=0;)
            f64.ge
            i32.and
            if $I8
              local.get $l2
              i64.trunc_f64_u
              br $B7
            end
            i64.const 0
          end
          local.set $l6
          call $f1070
          if $I9
            i32.const 3455088
            i64.load
            local.set $l7
            local.get $l6
            i64.const 0
            i64.le_s
            if $I10 (result i32)
              i32.const 1
            else
              loop $L11
                block $B12
                  call $f80340
                  local.set $l2
                  local.get $l6
                  call $f83050
                  i32.const 1
                  call $f83049
                  call $f1068
                  local.set $p0
                  i32.const 0
                  call $f83049
                  local.get $p0
                  i32.eqz
                  br_if $B12
                  block $B13 (result i64)
                    local.get $l6
                    f64.convert_i64_s
                    call $f80340
                    local.get $l2
                    f64.sub
                    f64.const -0x1.dcd65p+29 (;=-1e+09;)
                    f64.mul
                    f64.add
                    local.tee $l2
                    f64.abs
                    f64.const 0x1p+63 (;=9.22337e+18;)
                    f64.lt
                    if $I14
                      local.get $l2
                      i64.trunc_f64_s
                      br $B13
                    end
                    i64.const -9223372036854775808
                  end
                  local.tee $l6
                  i64.const 0
                  i64.gt_s
                  br_if $L11
                end
              end
              i32.const 0
            end
            drop
            local.get $l7
            call $f83050
          end
          call $f80340
          drop
        end
      end
    end)
