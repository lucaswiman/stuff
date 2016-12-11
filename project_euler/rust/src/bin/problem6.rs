// The sum of the squares of the first ten natural numbers is,
// 1² + 2² + ... + 10² = 385
//
// The square of the sum of the first ten natural numbers is,
// (1 + 2 + ... + 10)² = 552 = 3025
//
// Hence the difference between the sum of the squares of the first ten natural numbers and the square of the sum is 3025 − 385 = 2640.
//
// Find the difference between the sum of the squares of the first one hundred natural numbers and the square of the sum.

fn main() {
  let sum_of_squares = (1u64..101u64).map(|x| x.pow(2)).fold(0, |x, y| x + y);
  let square_of_sum = (1u64..101u64).fold(0, |x, y| x + y).pow(2);
  println!("{}", square_of_sum - sum_of_squares);
}
