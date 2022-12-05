-- Usage:
--   runhaskell a.hs < in

import Data.Function ((&))
import Data.List (isPrefixOf, transpose)


main = interact solve

solve text =
  text

  -- Parse
  & paragraphs
  & (\[drawing, instructions] -> (parseDrawing drawing, parseInstructions instructions))

  -- Simulate
  & (
      \(stacks, instructions) ->
        foldl
          (\accStacks currInstruction@[count, src, dest] ->
            move count src dest accStacks
          )
          stacks
          instructions
    )

  -- Display
  & tail
  & map (\stack -> head stack)
  & (++ "\n")

move count src dest stacks =
  applyN count (moveOnce src dest) stacks
  where
    moveOnce src dest stacks =
      let
        oldSrcStack = stacks !! src
        oldDestStack = stacks !! dest
        newSrcStack = tail oldSrcStack
        newDestStack = (head oldSrcStack) : oldDestStack
      in
        [
          if i == src then newSrcStack else
          if i == dest then newDestStack else
          stack
          | (i, stack) <- zip [0..] stacks
        ]

parseDrawing text =
  text
  & lines
  & reverse
  & transpose -- TODO Try writing transpose yourself
  & filter (\s -> hasAnyDigit s)
  & map (
      \column ->
        column
        & tail
        & filter isAlphabetic
        & foldl (\acc curr -> curr:acc) []
    )
  & (\xs -> "":xs) -- So that we can use 1-indexing

parseInstructions text =
  text
  & lines
  & map (
      \line ->
        line
        & split " "
        & (\[_, count, _, src, _, dest] -> [count, src, dest])
        & map (read :: String -> Int)
    )

-- TODO Maybe use iterate from the Prelude instead of applyN
applyN n f x =
  foldl
    (\acc curr -> f acc)
    x
    [1..n]

hasAnyDigit :: [Char] -> Bool
hasAnyDigit s =
  any (\c -> c `elem` "123456789") s

isAlphabetic c = c `elem` "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

paragraphs = split "\n\n"

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
