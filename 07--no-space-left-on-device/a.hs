import Data.List (isPrefixOf)
import Data.Char (isDigit)
import Data.Function ((&))
import qualified Data.Map as Map


data LogLine = CD String | LS | Dir String | File Int String deriving Show

type DirPath = [String]


main = interact solve


solve text =
  text
  & lines
  & map parseLine
  & constructFilesystem
  & (\(fileSizes, dirs) ->
      dirs
      & map (totalSize fileSizes)
      & filter (<= 100000)
      & sum
      & show
      & (++ "\n")
    )


parseLine line
  | "$ cd" `isPrefixOf` line
    = CD $ drop 5 line
  | "dir " `isPrefixOf` line
    = Dir $ drop 4 line
  | "$ ls" == line
    = LS
  | isDigit $ head line
    =
      let
        [sizeString, name] = words line
        size = read sizeString
      in File size name
  | otherwise = error "Failed to parse line"


constructFilesystem logLines =
  foldl
    processLine
    ([], Map.empty, [])
    logLines
  & (\(_, fileSizes, dirs) ->
      (fileSizes, dirs)
    )


processLine state@(workingDir, fileSizes, dirs) (CD arg)
  = (
      changeDir workingDir arg,
      fileSizes,
      dirs
    )
processLine state@(workingDir, fileSizes, dirs) (File size name)
  = (
      workingDir,
      Map.insert (workingDir ++ [name]) size fileSizes,
      dirs
    )
processLine state@(workingDir, fileSizes, dirs) (Dir name)
  = (
      workingDir,
      fileSizes,
      (workingDir ++ [name]) : dirs
    )
processLine state@(workingDir, fileSizes, dirs) LS
  = state


changeDir dir "/"
  = []
changeDir dir ".."
  = init dir
changeDir dir other
  = dir ++ [other]


totalSize fileSizes dirPath =
  Map.toList fileSizes
  & filter
    (\(filePath, fileSize) -> dirPath `isPrefixOf` filePath)
  & map
    (\(filePath, fileSize) -> fileSize)
  & sum
