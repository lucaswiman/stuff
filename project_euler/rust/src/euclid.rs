pub fn gcd(a:u64, b:u64) -> u64 {
  if b < a {
    return gcd(b, a);
  }
  let remainder = b % a;
  if remainder == 0 {
    return a;
  }
  return gcd(remainder, a);
}


pub fn lcm(a:u64, b:u64) -> u64 {
  return (a * b) / gcd(a, b);
}
