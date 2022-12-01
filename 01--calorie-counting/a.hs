-- Usage:
--   runhaskell a.hs < in

import Data.List (sort)
import Data.Function ((&))

main = interact solve

solve text =
  text
  & paragraphs
  & map
    (
      \paragraph ->
        paragraph
        & lines
        & map
          (
            \line ->
              line
              & (read :: (String -> Int))
          )
        & sum
    )
  & maximum
  & show

paragraphs text = splitWithStr "\n\n" text

-- https://stackoverflow.com/a/10967044
splitWithStr :: Eq a => [a] -> [a] -> [[a]]
splitWithStr x y = func x y [[]]
  where
    func x [] z = reverse $ map (reverse) z
    func x (y:ys) (z:zs) = if (take (length x) (y:ys)) == x then
      func x (drop (length x) (y:ys)) ([]:(z:zs))
    else
      func x ys ((y:z):zs)
