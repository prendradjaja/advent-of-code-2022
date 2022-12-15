module Rose where

import Data.Function ((&))
import Data.List (intercalate)

-- https://stackoverflow.com/a/22023355
-- https://en.wikipedia.org/wiki/Rose_tree
data Rose a = Rose [Rose a] | Leaf a deriving Show
type RoseInt = Rose Int

parse :: String -> RoseInt
parse s = s & tokenize & parseTokens & fst

parseTokens :: [String] -> (RoseInt, [String])
parseTokens tokens@(x:xs)
  | (head x) `elem` digits
    = (
        Leaf (read x),
        xs
      )
  | (head x) == '['
    = parseExprList xs
  | otherwise
    = error "Oops"

parseExprList :: [String] -> (RoseInt, [String])
parseExprList tokens@(x:xs)
  | x == "]"
    = (Rose [], xs)
  | otherwise
    =
      let
        (parsedX, xs') = parseTokens tokens
        (parsedXs, xs'') = parseExprList xs'
      in
        (
          Rose (parsedX : (fromRose parsedXs)),
          xs''
        )

fromRose (Rose xs) = xs

showRose :: RoseInt -> String
showRose (Leaf n) = show n
showRose (Rose xs) =
  "["
  ++ (intercalate "," $ map showRose xs)
  ++ "]"

tokenize :: String -> [String]
tokenize [] = []
tokenize s@(x:xs)
  | x `elem` "[]"
    = [x] : tokenize xs
  | x == ','
    = tokenize xs -- Don't emit a comma token
  | otherwise
    =
      let (n, rest) = consumeInt s
      in n : tokenize rest

-- Given a nonempty string:
--   - If it does not begin with an integer, return 0.
--   - If it begins with an integer, return the length (in characters) of that integer.
getIntLength :: String -> Int
getIntLength (x:xs)
  | not $ x `elem` digits
    = 0
  | otherwise
    = 1 + getIntLength xs

consumeInt :: String -> (String, String)
consumeInt s = (take n s, drop n s)
  where n = getIntLength s

digits = "0123456789"

demo = do
  print $ tokenize "[1,23]"
  putStrLn "---"
  putStrLn $ showRose $ Leaf 1
  putStrLn $ showRose $ Rose [Leaf 1, Leaf 2]
  putStrLn $ showRose $ Rose []
  putStrLn $ showRose $ Rose [Leaf 1, Leaf 2, Rose[], Rose[Leaf 3, Leaf 4]]
  putStrLn "---"
  print $ showRose $ parse "[]"
  print $ showRose $ parse "[1]"
  print $ showRose $ parse "[1,2]"
  print $ showRose $ parse "[1,2,[]]"
  print $ showRose $ parse "[1,2,[],3]"
  print $ showRose $ parse "[1,2,[],3,[4,[5]],6]"
