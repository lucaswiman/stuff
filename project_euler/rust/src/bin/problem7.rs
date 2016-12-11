// By listing the first six prime numbers: 2, 3, 5, 7, 11, and 13, we can see that the 6th prime is 13.
//
// What is the 10 001st prime number?

extern crate project_euler;

fn main() {
  let mut primes = project_euler::primes::primes();

  // note that nth_prime is 0-indexed, but the problem is 1-indexed.
  assert_eq!(primes.nth_prime(6 - 1), 13);
  println!("{}", project_euler::primes::primes().nth_prime(10001 - 1));
}
