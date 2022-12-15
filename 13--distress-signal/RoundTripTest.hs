-- Usage:
--   runhaskell RoundTripTest.hs < ex
--   runhaskell RoundTripTest.hs < in

import Data.Function ((&))
import Rose (parse, showRose)

main = interact check

check text =
  text
  & lines
  & filter (not . null)
  & all (\line ->
      (line & parse & showRose) == line
    )
  & show
  & (++ "\n")
