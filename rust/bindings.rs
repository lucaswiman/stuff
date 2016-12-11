fn main() {
  let x = 1;
  println!("x={}", x);  // x=1
  if true {
    let x = 2;
    println!("x={}", x);  // x=2
  }
  if true {
    let x = 3;  // warning: unused variable: `x`, #[warn(unused_variables)] on by default
  }
  println!("x={}", x);  // x=1
  let x = 4;
  println!("x={}", x);  // x=4
  let x = 4;  // warning: unused variable: `x`, #[warn(unused_variables)] on by default

  // x = 5;  // error[E0384]: re-assignment of immutable variable `x`
  let mut x = 5;
  println!("x={}", x);  // x=5
  if true {
    let x = 6;
    println!("x={}", x);  // x=6
  }
  println!("x={}", x);  // x=5
  if true {
    x = 7;
    println!("x={}", x);  // x=7
  }
  println!("x={}", x);  // x=7
}
