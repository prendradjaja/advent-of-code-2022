-- Usage:
--   runhaskell b.hs < in

import Data.Function ((&))
import Data.List (elemIndex)
import Data.Maybe (fromJust)


main = interact solve

solve text =
  text
  & lines
  & chunks3
  & map
    (
      \(sack1, sack2, sack3) ->
        getOverlap sack1 sack2 sack3
        & priority
    )
  & sum
  & show
  & (++ "\n")

getOverlap xs ys zs =
  [x | x <- xs, x `elem` ys, x `elem` zs] !! 0

priority x =
  fromJust $ elemIndex x "_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

chunks3 (x:y:z:xs) = (x,y,z) : (chunks3 xs)
chunks3 [] = []
