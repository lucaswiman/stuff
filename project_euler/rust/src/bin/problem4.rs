// A palindromic number reads the same both ways. The largest palindrome made from the product of two 2-digit numbers is 9009 = 91 × 99.
//
// Find the largest palindrome made from the product of two 3-digit numbers.

extern crate project_euler;

fn is_palindrome(x:u64) -> bool {
  let s = x.to_string();
  let rev:String = s.chars().rev().collect();
  return s == rev;
}

fn main() {
  let mut best = 0;
  for i in 100..1000 {
    for j in 100..1000 {
      if is_palindrome(i * j) && i * j > best {
        best = i * j;
      }
    }
  }
  println!("{}", best);
}
