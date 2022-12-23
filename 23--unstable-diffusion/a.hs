-- Usage:
--   runhaskell a.hs < in

import Data.Function ((&))
import Data.Set (Set)
import qualified Data.Set as Set
import Data.Map (Map)
import qualified Data.Map as Map


-- Constants and types
type Position = (Int, Int)
type Direction = (Int, Int)

n = (-1, 0) :: Direction
s = (1, 0)
w = (0, -1)
e = (0, 1)
nw = n +! w
ne = n +! e
sw = s +! w
se = s +! e

allDirections = [n, s, e, w, nw, ne, sw, se]

type LookList = [[Direction]]
initialLookList =
  [
    -- Each list [A, B, C] represents: "If there is no Elf in the 'A', 'B', or
    -- 'C' adjacent positions, the Elf proposes moving 'A' one step."
    [n, ne, nw],
    [s, se, sw],
    [w, nw, sw],
    [e, ne, se]
  ]


-- Solution
main = interact solve


solve text =
  text
  & parse
  & (\elves -> (initialLookList, elves))
  & nthIteration 10 step
  & snd
  & countEmptyGroundTiles
  & show
  & (++ "\n")


parse :: String -> Set Position
parse text =
  let
    grid = lines text
    height = length grid
    width = length $ head grid
  in
    Set.fromList [
      (r, c)
      |
      r <- [0..height-1],
      c <- [0..width-1],
      grid !! r !! c == '#'
    ]


step :: (LookList, Set Position) -> (LookList, Set Position)
step (lookList, elves) =
  let
    proposals =
      elves
      & Set.toList
      -- TODO: Initially I used a filter to represent "This elf doesn't need
      -- to move, so omit her from `proposals` -- omission will represent
      -- non-movement." But it turns out getProposedDest can return a
      -- non-movement, so this idea has become muddied (represented in two
      -- possible ways). It would be nice to do something like: Remove the
      -- filter, and move this check into getProposedDest
      & filter (\elf -> hasNeighbor elves elf allDirections)
      & map (\elf -> (elf, getProposedDest lookList elves elf))
      & Map.fromList

    destCounts =
      proposals
      & Map.toList
      & map snd
      & counterFromList

    lookList' = rotate lookList

    elves' =
      elves
      & Set.toList
      & map
          (
            \elf ->
            let
              proposedDest = Map.findWithDefault elf elf proposals
              count = getCount proposedDest destCounts
              isConflictFree = count <= 1
            in
              if isConflictFree
              then proposedDest
              else elf
          )
      & Set.fromList
  in
    (lookList', elves')


getProposedDest lookList@[] elves elf = elf
getProposedDest lookList@(look:rest) elves elf =
  let
    direction = head look
  in
    if not $ hasNeighbor elves elf look
    then elf +! direction
    else getProposedDest rest elves elf


hasNeighbor :: Set Position -> Position -> [Direction] -> Bool
hasNeighbor elves pos directions =
  directions
  & any
      (
        \direction ->
        let
          neighbor = (direction +! pos)
        in
          neighbor `Set.member` elves
      )


countEmptyGroundTiles elves =
  let
    (rmin, rmax, cmin, cmax) = getBoundingRect elves
    height = rmax - rmin + 1
    width = cmax - cmin + 1
    area = height * width
  in
    area - (Set.size elves)


getBoundingRect elves =
  let
    rmin = getExtremum minimum fst elves
    rmax = getExtremum maximum fst elves
    cmin = getExtremum minimum snd elves
    cmax = getExtremum maximum snd elves
  in
    (rmin, rmax, cmin, cmax)


getExtremum minOrMax fstOrSnd elves =
  elves
  & Set.toList
  & map fstOrSnd
  & minOrMax


-- Counter data structure
--   The functions in this section define a data structure similar to Python's
--   collections.defaultdict(int) aka collections.Counter: A map with default
--   value 0 for each key.
emptyCounter :: Map Position Int
emptyCounter = Map.empty


incrCount k m =
  let
    newValue = (getCount k m) + 1
  in
    Map.insert k newValue m


getCount k m =
  Map.findWithDefault 0 k m


counterFromList :: [Position] -> Map Position Int
counterFromList xs =
  foldl
    (\counter x -> incrCount x counter)
    emptyCounter
    xs


-- Generic utilities
(v0,v1) +! (w0,w1) = (v0+w0, v1+w1)  -- Vector addition


rotate xs@(y:ys) = ys ++ [y]


nthIteration n f x =
  iterate f x
  & drop n
  & head
