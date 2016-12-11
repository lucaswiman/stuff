// The prime factors of 13195 are 5, 7, 13 and 29.
// 
// What is the largest prime factor of the number 600851475143 ?

extern crate project_euler;

fn main() {
  let mut n = 600851475143;
  for p in project_euler::primes::primes() {
    while n % p == 0 {
      println!("{}", p);
      n /= p;
    }
    if n == 1 {
      break;
    }
  }
}
