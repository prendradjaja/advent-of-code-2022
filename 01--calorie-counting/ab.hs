-- Usage:
--   runhaskell Main.hs < in

import Data.List (sort)

main =
  interact (
    \text ->
      "Part 1 answer: " ++ (part1 text) ++ "\n" ++
      "Part 2 answer: " ++ (part2 text) ++ "\n"
  )

part1 text =
  let
    myParagraphs = paragraphs text
    elves = map (\text -> sum $ map (\x -> read x :: Int) (lines text)) myParagraphs
  in
    show $ maximum $ elves

part2 text =
  let
    myParagraphs = paragraphs text
    elves = map (\text -> sum $ map (\x -> read x :: Int) (lines text)) myParagraphs
    top3 = last3 $ sort $ elves
  in
    show $ sum top3

last3 xs = drop (length xs - 3) xs

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
