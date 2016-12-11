use std::collections::BTreeMap;

pub struct SievedPrimes {
  pub primes: Vec<u64>,
  pub biggest: u64,
  i: usize,
}

fn smallest_odd_multiple_larger_than(d:u64, n:u64) -> u64 {
  /*! Returns the smallest odd multiple of `d` greater than or equal to `n`.
   */

  let mut mul = (n / d) * d;
  if mul < n {
    mul += d;
  }
  if (mul % 2) == 0 {
    return mul + d;
  } else {
    return mul;
  }
}

impl SievedPrimes {
  pub fn expand(&mut self) {
    /*! Given an ordered vector of primes, return a vector of primes to primes * 2 + 1
     *
     *  Assumes the biggest element of the `primes` vector is >= 3.
     */
    let prev_biggest = self.biggest;

    let left_endpoint = prev_biggest + 2;
    let right_endpoint = prev_biggest * 2 + 1;

    // Number of odd numbers between left and right inclusive.
    let num_indices = (right_endpoint - left_endpoint) / 2 + 1;

    let mut hasdivisor = vec![false; num_indices as usize];

    for prime in self.primes.iter().filter(|x| **x != 2) {
      if prime * prime > right_endpoint {
        break;
      }
      let mut cur = smallest_odd_multiple_larger_than(*prime, left_endpoint);
      while cur <= right_endpoint {
        if cur < left_endpoint {
          println!("prime={} cur={} left_endpoint={}, right_endpoint={}", prime, cur, left_endpoint, right_endpoint);
        }
        let cur_idx = (cur - left_endpoint) / 2;
        hasdivisor[cur_idx as usize] = true;
        cur += 2 * prime;
      }
    }
    self.biggest = right_endpoint;
    self.primes.extend(
      (0..hasdivisor.len())
      .filter(|x| !hasdivisor[*x])
      .map(|x| left_endpoint + 2 * (x as u64)));
  }
  pub fn nth_prime(&mut self, n:usize) -> u64 {
    while self.primes.len() <= n {
      self.expand();
    }
    return self.primes[n];
  }

  pub fn factorize(&mut self, n:u64) -> BTreeMap<u64, u32> {
    let mut prime_to_degree = BTreeMap::new();
    let mut remainder = n;
    for i in 0.. {
      let prime = self.nth_prime(i);
      while remainder % prime == 0 {
        prime_to_degree.entry(prime).or_insert(0);
        let degree = prime_to_degree[&prime];
        prime_to_degree.insert(prime, degree + 1);
        remainder /= prime;
      }
      if remainder == 1 {
        break;
      }
    }
    return prime_to_degree;
  }
}

pub fn primes() -> SievedPrimes {
  SievedPrimes {primes: vec![2, 3, 5, 7, 11], biggest: 11, i: 0}
}

impl Iterator for SievedPrimes {
  type Item = u64;
  fn next(&mut self) -> Option<u64> {
    if self.i == self.primes.len() {
      self.expand();
    }
    let ret = self.primes[self.i];
    self.i += 1;
    return Some(ret);
  }
}
