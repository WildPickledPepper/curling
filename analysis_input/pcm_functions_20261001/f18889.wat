  (func $f18889 (type $t427) (param $p0 f64) (result f32)
    (local $l1 f64)
    local.get $p0
    local.get $p0
    f64.mul
    local.tee $p0
    local.get $p0
    local.get $p0
    f64.mul
    local.tee $l1
    f64.mul
    local.get $p0
    f64.const 0x1.99342e0ee5069p-16 (;=2.43904e-05;)
    f64.mul
    f64.const -0x1.6c087e80f1e27p-10 (;=-0.00138868;)
    f64.add
    f64.mul
    local.get $l1
    f64.const 0x1.55553e1053a42p-5 (;=0.0416666;)
    f64.mul
    local.get $p0
    f64.const -0x1.ffffffd0c5e81p-2 (;=-0.5;)
    f64.mul
    f64.const 0x1p+0 (;=1;)
    f64.add
    f64.add
    f64.add
    f32.demote_f64)
