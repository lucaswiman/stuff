% A palindromic number reads the same both ways. The largest palindrome made from the product of two 2-digit numbers is 9009 = 91 × 99.
%
% Find the largest palindrome made from the product of two 3-digit numbers.

reverse_string(S, Reversed) :-
  reverse(S, ReversedList), string_to_list(Reversed, ReversedList)
.

palindrome(S) :- reverse_string(S, S).
palindrome_number(N) :- number_codes(N, S), palindrome(S).

palindrome_numbers(NumDigits, Palindromes, BiggestPalindrome) :-
  Min is 10 ** (NumDigits - 1),
  Max is 10 ** (NumDigits) - 1,
  numlist(Min, Max, Factors),
  findall(
    Z,
    (
      member(X, Factors), member(Y, Factors),
      Z is X * Y,
      palindrome_number(Z)
    ),
    Palindromes
  ),
  max_member(BiggestPalindrome, Palindromes)
.

% palindrome_numbers(3, Palindromes, BiggestPalindrome).
