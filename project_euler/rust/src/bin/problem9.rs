// A Pythagorean triplet is a set of three natural numbers, $a<b<c$, for which, $a^2+b^2=c^2$
// For example, 3, 4, 5.
//
// There exists exactly one Pythagorean triplet for which $a+b+c=1000$.
// Find the product $abc$.


extern crate project_euler;

fn main() {
  let answer = project_euler::pythagorean_triples::euclid_forumla_triples_iter()
    .filter(|&(a, b, c)| a+b+c == 1000)
    .next();
  match answer {
    Some((a, b, c)) => {
      println!("{}^2+{}^2={}^2", a, b, c);
      println!("{}+{}+{}=1000", a, b, c);
      println!("{}*{}*{}={}", a, b, c, a * b * c);
    },
    _ => {}
  }
}