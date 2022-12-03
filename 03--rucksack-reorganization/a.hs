-- Usage:
--   runhaskell a.hs < in

import Data.Function ((&))
import Data.List (elemIndex)
import Data.Maybe (fromJust)


main = interact solve

solve text =
  text
  & lines
  & map
    (
      \line ->
        let
          (left, right) = halves line
        in
          getOverlap left right
          & priority
    )
  & sum
  & show
  & (++ "\n")

getOverlap xs ys =
  [x | x <- xs, x `elem` ys] !! 0

priority x =
  fromJust $ elemIndex x "_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

halves s =
  let
    n = (length s) `div` 2
  in
    ((take n s), (drop n s))
