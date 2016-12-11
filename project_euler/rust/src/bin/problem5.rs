// 2520 is the smallest number that can be divided by each of the numbers from 1 to 10 without any remainder.
//
// What is the smallest positive number that is evenly divisible by all of the numbers from 1 to 20?

extern crate project_euler;
use std::collections::BTreeMap;
use std::cmp;


fn lcm_via_factorization(multiplicands:Vec<u64>) -> u64 {
  let mut lcm_factors = BTreeMap::new();
  let mut primes = project_euler::primes::primes();
  for m in &multiplicands {
    for (factor, exponent) in primes.factorize(*m) {
      lcm_factors.entry(factor).or_insert(0);
      let exp = cmp::max(lcm_factors[&factor], exponent);
      lcm_factors.insert(factor, exp);
    }
  }
  return lcm_factors.iter().map(|(factor, exponent)| factor.pow(*exponent)).fold(1, |k, v| k * v);
}


fn main() {
  let mut multiplicands = Vec::new();
  multiplicands.extend(2..21);
  let multiplicands = multiplicands;

  let lcm_factors = lcm_via_factorization(multiplicands.clone());
  let lcm_euclid = multiplicands.iter().fold(1, |a, b| project_euler::euclid::lcm(a, *b));
  assert_eq!(lcm_factors, lcm_euclid);
  println!("{}", lcm_euclid);
}
