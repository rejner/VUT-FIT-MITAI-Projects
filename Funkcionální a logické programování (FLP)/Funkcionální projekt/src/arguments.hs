-- Project:      FLP Project 1 - simplify-bkg
-- Author:       Michal Rein (xreinm00)
-- Date:         01.04.2022
-- File:         arguments.hs
-- Description:  Module for parsing arguments

module Arguments (
    Args(inputFile, printParsed, printFirstStep, printSecondStep),
    parseArgs,
    printArgs) where

-- import System.Directory (getArgs)
import Data.List (find)
import System.Posix (fileExist)
import Data.Maybe (fromJust)
import Control.Monad.List (unless, when)
import System.Exit (exitSuccess)
import System.Environment (getArgs)

-- data structure for storing arguments
data Args = Args {
    inputFile :: Maybe String,
    printHelp :: Bool,
    printParsed :: Bool,
    printFirstStep :: Bool,
    printSecondStep :: Bool
}

-- parse arguments
parseArgs :: IO Args
parseArgs = do
    args <- getArgs
    let arguments = Args {
        inputFile = find (\x -> (x /= "-2") && (x /= "-i") && (x /= "-1") && (x /= "-h")) args,
        printHelp       = "-h" `elem` args,
        printParsed     = "-i" `elem` args,
        printFirstStep  = "-1" `elem` args,
        printSecondStep = "-2" `elem` args
    }
    -- check if found file exists
    isFileLegit <- maybe (return True) fileExist (inputFile arguments)
    unless isFileLegit $ error ("File '" ++ fromJust (inputFile arguments) ++ "' doesn't exist or invalid argument was given!") 
    -- print help if required
    when (printHelp arguments) $ help >> exitSuccess
    return arguments

-- help message
help :: IO ()
help =  putStrLn "USAGE: ./flp21-fun [-i|-1|-2|-h] <INPUT>" >> 
        putStrLn "See doc/README.md for more info."

-- print parsed Args in a pretty way (FOR DEBUG PURPOSES)
printArgs :: Args -> IO ()
printArgs args = do
    print "Input file: "
    print (inputFile args)
    print "-i | Print parsed grammar"
    print (printParsed args)
    print "-1 | Print grammar after first step of algorithm "
    print (printFirstStep args)
    print "-2 | Print grammar after second step of algorithm"
    print (printSecondStep args)