-- Usage:
--   runhaskell a.hs < ex

import Data.Function ((&))
import Numeric (showIntAtBase)

main = interact solve

solve text =
  text
  & lines
  & map readSnafu
  & sum
  & showSnafu
  & (++ "\n")

readSnafu :: String -> Int
readSnafu s =
  s
  & reverse
  & map decodeDigit
  & zip powersOfFive
  & map (\(power, digit) -> power * digit)
  & sum
  where
    decodeDigit '2' = 2
    decodeDigit '1' = 1
    decodeDigit '0' = 0
    decodeDigit '-' = -1
    decodeDigit '=' = -2

    powersOfFive = map (\n -> 5 ^ n) [0..]

showSnafu :: Int -> String
showSnafu n = showQuinaryWithDigits "=-012" (k + n)
  where
    k =
      [1..]
      & map (\i -> replicate i '2')  -- ["2", "22", "222", ...]
      & map readSnafu
      & dropWhile (< n)
      & head
    showQuinaryWithDigits digits n =
      showIntAtBase
        5
        (\d -> digits !! d)
        n
        ""

-- Explanation of showSnafu:
--
--
-- 1) Notice that counting in SNAFU e.g. from 0000 to 2222 in SNAFU is
-- isomorphic to counting in ordinary quinary from 2222 to 4444.
--
-- To illustrate, consider this table: The SNAFU values are equal to the
-- decimal values, but the quinary values are NOT equal to the SNAFU/decimal
-- values. The key is simply that both "2222-quinary" and SNAFU "roll over" to
-- the next digit (e.g. from 0002 to 001=) at the same "time" i.e. at the same
-- row.
--
-- SNAFU  Decimal  "2222-quinary"
-- 0000   0        2222
-- 0001   1        2223
-- 0002   2        2224
-- 001=   3        2230
-- 001-   4        2231
-- 0010   5        2232
-- (and so on)
--
--
-- 2) Take advantage of this isomorphism to convert a number from decimal to
-- SNAFU. For example, to convert 3 to SNAFU:
--
--   a. We'll need to use the magic number 2222. In both SNAFU and ordinary
--   quinary, this equals decimal 312.
--
--   b. Calculate 2222 (quinary) + 3 (decimal). This is 2230.
--
--   c. Map each quinary digit to to a SNAFU digit, using the following table:
--
--        Quinary  SNAFU
--           0       =
--           1       -
--           2       0
--           3       1
--           4       2
--
--   d. So in our example, 2230 becomes 001=: 3 in decimal is 001= in SNAFU.
--   This can also be written as 1= (remove leading zeros).
--
--
-- 3) In our example, we used a four-digit magic number. But if the number to
-- convert is too large, it won't fit in four digits of SNAFU -- we'll need a
-- larger magic number. In this implementation, we find the smallest magic
-- number `k` that is sufficiently large to work for the given `n`.
--
--
-- P.S.: SNAFU could be called "balanced quinary" (by analogy to balanced
-- ternary, which is well-studied). There are better ways to implement
-- showSnafu, but I liked this one. Alternatively, this problem can be solved
-- without showSnafu at all, by implementing addition directly in SNAFU (no
-- conversion to decimal/int).
