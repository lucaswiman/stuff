fn main() {
  let mut i = 0u32;
  let mut acc = 0u32;
  loop {
    i += 1;
    if i == 1000 {
      break;
    }
    if (i % 3 == 0) || (i % 5 == 0) {
      println!("{}", i);
      acc += i
    }
  }
  println!("{}", acc);
}