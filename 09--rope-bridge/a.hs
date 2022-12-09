import qualified Data.Set as Set
import Data.Function ((&))
import System.Environment (getArgs)
import System.IO (readFile)

data Motion = Motion {
  direction :: Char,
  count :: Int
} deriving (Show)

main = do
  args <- getArgs
  let [path] = args
  text <- readFile path

  let headPath = getHeadPath $ parse text
  putStrLn "Computing head path"
  print (length headPath, head headPath, last headPath)

  let tailPath = getTailPath headPath
  putStrLn "Computing tail path"
  print (length tailPath, head tailPath, last tailPath)

  let answer = Set.size $ Set.fromList tailPath
  putStrLn "\nAnswer:"
  print answer

parse text =
  text
  & lines
  & map parseLine

getHeadPath motions =
  motions
  & foldl
      (\path motion ->
        let
          lastPosition = last path
          moveOnce = moveHead (direction motion)
          newPositions = (iterate moveOnce lastPosition) & drop 1 & take (count motion)
        in
          path ++ newPositions
      )
      [(0, 0)]

-- getTailPath headPath =
--   (0, 0)
--   : map
--       (\(prevTailPosition, currHeadPosition) -> approach prevTailPosition currHeadPosition)
--       (zip (getTailPath headPath) (tail headPath))

-- getTailPath headPath =
--   foldl
--     (\tailPath headPosition ->
--       let
--         lastTailPosition = last tailPath
--         newTailPosition = approach lastTailPosition headPosition
--       in
--         tailPath ++ [newTailPosition]
--     )
--     [(0, 0)]
--     (tail headPath)

getTailPath headPath =
  foldl
    (\(lastTailPosition, tailPath) headPosition ->
      let
        newTailPosition = approach lastTailPosition headPosition
      in
        (newTailPosition, tailPath ++ [newTailPosition])
    )
    ((0, 0), [(0, 0)])
    (tail headPath)
  & snd

approach prevTail@(tr, tc) currHead@(hr, hc)
  | isTouching
    = prevTail
  | dr == 0
    = (tr, tc + signum dc)
  | dc == 0
    = (tr + signum dr, tc)
  | otherwise
    = (tr + signum dr, tc + signum dc)
  where
    dr = hr - tr
    dc = hc - tc
    isTouching = (abs dr) <= 1 && (abs dc) <= 1

moveHead direction position = addvec position (offset direction)

parseLine (direction : ' ' : numStr) = Motion direction (read numStr)

offset 'R' = (0, 1)
offset 'L' = (0, -1)
offset 'U' = (-1, 0)
offset 'D' = (1, 0)

addvec (r1, c1) (r2, c2) = (r1+r2, c1+c2)
