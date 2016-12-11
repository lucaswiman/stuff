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
  /*
   * David MacIver (https://twitter.com/DRMacIver/status/808012406714728449)
   * pointed out these are the same scoping rules as ML, but with syntactic sugar for implicit nesting:
   *
   * > It might help to view "let x = v; y; z" as syntactic sugar for "let x = v in {y; z}"
   *
   * So we can rewrite the code above as:

      let x = 1 in {
        println!("x={}", x);  // x=1
        if true {
          let x = 2 in {
            println!("x={}", x);  // x=2
          }
        }
        if true {
          let x = 3 in {};
        }
        println!("x={}", x);  // x=1
      }
      let x = 4 in {
        println!("x={}", x);  // x=4
        let x = 4 in {};   // warning: unused variable: `x`, #[warn(unused_variables)] on by default
      }
      // x = 5;  // error[E0384]: re-assignment of immutable variable `x`
      let mut x = 5 in {
        println!("x={}", x);  // x=5
        if true {
          let x = 6 in {
            println!("x={}", x);  // x=6
          }
        }
        println!("x={}", x);  // x=5
        if true {
          x = 7;  // Has the _side effect_ of updating the binding in the whole mutable binding scope.
          println!("x={}", x);  // x=7
        }
        // binding is still updated to 7 due to the side effect above.
        println!("x={}", x);  // x=7
      }

   */
}
