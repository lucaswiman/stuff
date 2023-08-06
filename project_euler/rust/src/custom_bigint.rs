// Struct that stores a big integer as a vector of u64s
// and provides methods for arithmetic operations

use std::ops::{Add, Mul, Sub, Div, Rem, BitAnd, BitOr, BitXor, Shl, Shr, Neg};

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BigInt {
    pub digits: Vec<u64>,
    pub sign: bool,
}

macro_rules! impl_from {
    ($($t:ty),+ $(,)?) => {
        $(
            impl From<$t> for BigInt {
                fn from(i: $t) -> BigInt {
                    BigInt::new(vec![i.abs() as u64], i >= 0)
                }
            }
        )+
    };
}

impl_from!(i64, i32, i16, i8);

macro_rules! impl_from_unsigned {
    ($($t:ty),+ $(,)?) => {
        $(
            impl From<$t> for BigInt {
                fn from(i: $t) -> BigInt {
                    BigInt::new(vec![i as u64], false)
                }
            }
        )+
    };
}

impl_from_unsigned!(u64, u32, u16, u8);

impl From<String> for BigInt {
    fn from(s: String) -> BigInt {
        BigInt::parse(&s)
    }
}

fn mul(a: u64, b: u64) -> (u64, u64) {
    const result: u128 = (a as u128) * (b as u128);
    let lower = (result & ((1 << 64) - 1)) as u64;
    let upper = (result >> 64) as u64;
    (upper, lower)
}

fn add(a: u64, b: u64) -> (u64, u64) {
    let result = (a as u128) + (b as u128);
    let lower = (result & ((1 << 64) - 1)) as u64;
    let upper = (result >> 64) as u64;
    (upper, lower)
}


impl BigInt {
    fn parse(s: &str) -> BigInt {
        return BigInt::new(Vec![0], false);
    }
}

// Implemntation of the Add trait for BigInt
impl Add for BigInt {
    type Output = BigInt;

    fn add(self, other: BigInt) -> BigInt {
        let mut result = BigInt::new(Vec![0], false);
        result
    }
}

impl Mul for BigInt {
    type Output = BigInt;

    fn mul(self, other: BigInt) -> BigInt {
        let mut result = BigInt::new(Vec![0], false);
        result
    }
}

#[cfg(test)]
mod tests {
    // Note this useful idiom: importing names from outer (for mod tests) scope.
    use super::*;

    #[test]
    fn test_add() {
        let two = BigInt::from(2);
        assert_eq!(two+two, BigInt::from(4));
    }
}

