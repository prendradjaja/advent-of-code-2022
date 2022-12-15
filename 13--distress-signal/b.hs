-- Usage:
--   runhaskell b.hs < ex

import Rose (RoseInt, Rose(Rose, Leaf), parse, showRose)
import Data.Function ((&))
import Data.List (isPrefixOf, sortBy, intercalate, findIndex)
import Data.Maybe (fromJust)

main =
  interact solve

solve text =
  text
  & lines
  & (++ ["[[2]]", "[[6]]"])
  & filter (not . null)
  & map parse
  & sortBy myCompare
  & (\packets ->
      let
        p1index = 1 + (fromJust $ findIndex (\p -> EQ == myCompare p (parse "[[2]]")) packets)
        p2index = 1 + (fromJust $ findIndex (\p -> EQ == myCompare p (parse "[[6]]")) packets)
      in
        p1index * p2index
    )
  & show
  & (++ "\n")

myCompare :: RoseInt -> RoseInt -> Ordering
myCompare (Leaf x) (Leaf y) = compare x y
myCompare (Leaf x) (Rose y) = myCompare (Rose [Leaf x]) (Rose y)
myCompare (Rose x) (Leaf y) = myCompare (Rose x) (Rose [Leaf y])
myCompare (Rose xs) (Rose ys)
  | (null xs)       && (not $ null ys) = LT
  | (not $ null xs) && (null ys)       = GT
  | (null xs)       && (null ys)       = EQ
  | otherwise =
      let
        x = head xs
        y = head ys
        headsOrdering = myCompare x y
      in
        if EQ == headsOrdering
        then (
          myCompare
            (Rose (tail xs))
            (Rose (tail ys))
        )
        else headsOrdering

split sep s = split' sep s [] ""
  where
    split' sep s parts curr
      | null s =
          parts ++ [curr]
      | sep `isPrefixOf` s =
          split'
            sep
            (drop (length sep) s)
            (parts ++ [curr])
            ""
      | otherwise =
          split'
            sep
            (tail s)
            parts
            (curr ++ [(head s)])
