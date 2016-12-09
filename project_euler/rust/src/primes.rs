// Following http://rustbyexample.com/trait/iter.html

pub fn print_hello() {
  println!("hello");
}
pub struct Primes {
  primes_list: Vec<u64>,
}

// impl Iterator for Fibonacci {
//   type Item = u64;
//   fn next(&mut self) -> Option<u64> {
//     let next = self.prev + self.cur;
//     self.prev = self.cur;
//     self.cur = next;
//     return Some(self.cur);
//   }
// }
//
// pub fn fibonacci() -> Fibonacci {
//   Fibonacci { prev: 1, cur: 1 }
// }
