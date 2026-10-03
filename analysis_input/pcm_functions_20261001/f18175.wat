  (func $f18175 (type $t237) (param $p0 f64) (param $p1 i32) (result f32)
    (local $l2 f64) (local $l3 f64) (local $l4 f64)
    f64.const -0x1p+0 (;=-1;)
    local.get $p0
    local.get $p0
    f64.mul
    local.tee $l2
    local.get $p0
    f64.mul
    local.tee $l3
    local.get $l2
    local.get $l2
    f64.mul
    local.tee $l4
    f64.mul
    local.get $l4
    local.get $l2
    f64.const 0x1.362b9bf971bcdp-7 (;=0.00946565;)
    f64.mul
    f64.const 0x1.85dadfcecf44ep-9 (;=0.00297436;)
    f64.add
    f64.mul
    local.get $l2
    f64.const 0x1.91df3908c33cep-6 (;=0.0245283;)
    f64.mul
    f64.const 0x1.b54c91d865afep-5 (;=0.0533812;)
    f64.add
    f64.add
    f64.mul
    local.get $l3
    local.get $l2
    f64.const 0x1.112fd38999f72p-3 (;=0.133392;)
    f64.mul
    f64.const 0x1.5554d3418c99fp-2 (;=0.333331;)
    f64.add
    f64.mul
    local.get $p0
    f64.add
    f64.add
    local.tee $l2
    f64.div
    local.get $l2
    local.get $p1
    select
    f32.demote_f64)
