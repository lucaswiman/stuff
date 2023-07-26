extern crate project_euler;

fn main() {
  println!("{}", project_euler::primes::primes().take_while(|&n| n < 2000000).sum::<u64>());
}