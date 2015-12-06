fn main() {
  let mut prev = 1u32;
  let mut cur = 1u32;
  let mut acc = prev + cur;
  let mut next = prev + cur;
  while next < 1000000 {
    acc += next;
    next = cur + prev;
    prev = cur;
    cur = next
  }
}