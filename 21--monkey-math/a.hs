-- Usage:
--   runhaskell a.hs < ex | runhaskell

main =
  interact
    (\text ->
      "import Prelude hiding ((/))\n" ++
      "main = print root\n" ++
      "(/) = div\n" ++
      (map (\ch -> if ch == ':' then '=' else ch) text)
    )
