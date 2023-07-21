-- Project:      FLP Project 1 - simplify-bkg
-- Author:       Michal Rein (xreinm00)
-- Date:         01.04.2022
-- File:         bimplify-bkg.hs
-- Description:  Main module for simplification of BKG

module Main where

import System.IO ()
import Control.Monad (when)
import Arguments (Args(inputFile, printParsed, printFirstStep, printSecondStep), parseArgs)
import Grammar   (getGrammar, printGrammar, processGrammarFirstStep, processGrammarSecondStep)

-- program's main
main :: IO ()
main = do
    args <- parseArgs                               -- parse arguments    
    g0 <- getGrammar (inputFile args)               -- load grammar from file
    when (printParsed  args) $ printGrammar g0      -- print loaded grammar
    g1 <- processGrammarFirstStep g0                -- proccess grammar - first step
    when (printFirstStep args) $ printGrammar g1    -- print grammar after first processing step
    g2 <- processGrammarSecondStep g1               -- proccess grammar - second step
    when (printSecondStep args) $ printGrammar g2   -- print simplified grammar


