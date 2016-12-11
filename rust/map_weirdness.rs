use std::collections::BTreeMap;

fn main() {
  let mut map:BTreeMap<u64, u64> = BTreeMap::new();
  map.entry(0).or_insert(0);

  let y = map[&0] + 1;  // http://stackoverflow.com/questions/41090572/expected-reference-found-integral-variable-in-accessing-a-value-from-btreemap/41090691#41090691
  println!("{}", y);
}
