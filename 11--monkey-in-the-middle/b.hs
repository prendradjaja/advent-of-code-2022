-- Usage:
--   runhaskell b.hs in

import Data.Function ((&))
import Data.List (isPrefixOf, sortBy)
import Data.Ord (comparing)
import System.Environment (getArgs)


data Monkey = Monkey {
  items :: [Int],
  operation :: Int -> Int,
  test :: Int -> Bool,
  divisor :: Int,
  trueTarget :: Int,
  falseTarget :: Int,
  inspections :: Int
}

instance Show Monkey where
  show myMonkey =
    "Monkey {\n" ++
    "  items = " ++ (show $ items myMonkey) ++ ",\n" ++
    "  inspections = " ++ (show $ inspections myMonkey) ++ ",\n" ++
    "}"


main = do
  [path] <- getArgs
  text <- readFile path
  let initialMonkeys = parse text
  let commonMultiple = initialMonkeys
        & map divisor
        & product
  let monkeys = nthIteration 10000 (doRound commonMultiple) initialMonkeys
  let mostActiveMonkeys = monkeys
        & sortBy (comparing (negate . inspections))
        & take 2
  let answer = mostActiveMonkeys
        & map inspections
        & product
  print answer


nthIteration n f x =
  iterate f x
  & drop n
  & head


doRound commonMultiple monkeys =
  foldl
    (\monkeys n -> doTurn commonMultiple n monkeys)
    monkeys
    [0 .. length monkeys - 1]


doTurn commonMultiple n monkeys =
  let
    monkey = monkeys !! n
  in
    if null $ items monkey
    then monkeys
    else doTurn commonMultiple n $ doStep commonMultiple n monkeys


doStep commonMultiple n monkeys =
  let
    monkey = monkeys !! n
    oldWorryLevel = head $ items monkey
    newWorryLevel = ((operation monkey) oldWorryLevel) `rem` commonMultiple
    testResult = (test monkey) newWorryLevel
    newMonkey = monkey { items = tail $ items monkey, inspections = 1 + inspections monkey }
    target = if testResult then trueTarget monkey else falseTarget monkey
    oldTargetMonkey = monkeys !! target
    newTargetMonkey = oldTargetMonkey { items = items oldTargetMonkey ++ [newWorryLevel] }
  in
    monkeys
    & replace n newMonkey
    & replace target newTargetMonkey


-- Replace the nth element of a list
replace n x xs =
  (take n xs) ++
  [x] ++
  (drop (n + 1) xs)


parse :: String -> [Monkey]
parse text =
  text
  & paragraphs
  & map
      (\para ->
        para
        & lines
        & (\[_, startingItemsLine, operationLine, testLine, trueTargetLine, falseTargetLine] ->
            Monkey
              (startingItemsLine
                & split ": "
                & (!! 1)
                & split ", "
                & map read)
              (operationLine
                & split "= "
                & (!! 1)
                & parseOperation)
              (testLine
                & words
                & last
                & read
                & (\divisor ->
                    (\n -> n `rem` divisor == 0)))
              (testLine
                & words
                & last
                & read)
              (trueTargetLine & words & last & read)
              (falseTargetLine & words & last & read)
              0
          )
      )


parseOperation :: String -> Int -> Int
parseOperation s =
  s
  & words
  & (\[leftString, opString, rightString] ->
      (\n ->
        let
          left  = if leftString  == "old" then n else read leftString
          right = if rightString == "old" then n else read rightString
          op = if opString == "+" then (+) else (*)
        in
          op left right
      )
    )


paragraphs text = split "\n\n" text


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
