// A Pythagorean triplet is a set of three natural numbers, $a<b<c$, for which, $a^2+b^2=c^2$
// For example, 3, 4, 5.
//
// There exists exactly one Pythagorean triplet for which $a+b+c=1000$.
// Find the product $abc$.

use std::collections::HashMap;

fn main() {
  let square_to_root = (2..1000)
      .map(|x| (x * x, x))
      .collect::<HashMap<u64, u64>>();
  for (c_squared, c) in square_to_root.iter() {
    for (b_squared, b) in square_to_root.iter().filter(|&(square, _)| (square < c_squared) && square_to_root.contains_key(&(c_squared - square))) {
      let a_squared = c_squared - b_squared;
      match square_to_root.get(&a_squared) {
        Some(&a) => {
          if a+b+c == 1000 {
            println!("{}^2+{}^2={}^2", a, b, c);
            println!("{}+{}+{}=1000", a, b, c);
            println!("{}*{}*{}={}", a, b, c, a*b*c);
          }
        },
        _ => {}
      }
    }
  }
}