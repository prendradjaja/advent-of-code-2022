-- Usage:
--   runhaskell a.hs < ex

import Rose (RoseInt, Rose(Rose, Leaf), parse)
import Data.Function ((&))
import Data.List (isPrefixOf)

main =
  interact solve

solve text =
  text
  & paragraphs
  & map (\para ->
      para
      & lines
      & (\[x, y] ->
          myCompare (parse x) (parse y) == LT
        )
    )
  & zip [1..]
  & filter (\(i, isCorrect) -> isCorrect)
  & map fst
  & sum
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

paragraphs s = split "\n\n" s

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
