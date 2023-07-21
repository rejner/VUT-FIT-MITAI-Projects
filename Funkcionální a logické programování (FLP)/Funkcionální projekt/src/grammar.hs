-- Project:      FLP Project 1 - simplify-bkg
-- Author:       Michal Rein (xreinm00)
-- Date:         01.04.2022
-- File:         grammar.hs
-- Description:  Module for parsing and working with grammar

module Grammar (Grammar, getGrammar, printGrammar,
                processGrammarFirstStep, processGrammarSecondStep) where

import Data.List (intercalate, nub, sort)
import Data.Maybe (isJust, fromJust)

-- Grammar data type
data Grammar = Grammar {
    nterms :: [String],             -- non-terminal symbols
    terms :: [String],              -- terminal symbols
    start :: String,                -- starting non-terminal symbol
    rules :: [(String, [String])]   -- rules for non-terminal symbols
}

-- load and parse grammar from given path
getGrammar :: Maybe String -> IO Grammar
getGrammar path = do
    -- if path to file is present, load grammar from file, else read grammar from STDIN
    contents <- if isJust path then readFile (fromJust path) else getContents
    let nterms' : terms' : start' : rules' = lines contents
    let pretty_nterms = splitByDelimeter nterms' ','
    let pretty_terms = splitByDelimeter terms' ','
    let pretty_rules = map (\(nterm:_:_:symbols) -> ([nterm],  map (:[]) symbols)) rules'

    let loaded_grammar = Grammar {nterms = pretty_nterms,
                           terms = pretty_terms,
                           start = start',
                           rules = pretty_rules}
    return loaded_grammar

-- perform first step in grammar processing
processGrammarFirstStep :: Grammar -> IO Grammar
processGrammarFirstStep grammar = do
    -- compute set of non-terminal symbols which generate terminals
    let nt = sort (computeNtSet grammar [])
    -- filter rules based on nt set only
    let rules' = filter (\(_, alpha) -> all (\c ->
            (||) (c `elem` nt) (c `elem` (terms grammar ++ ["#"]))) alpha) (rules grammar)

    let grammar' = Grammar {
        nterms = nt,
        terms = terms grammar,
        start = start grammar,
        rules = rules'
    }
    return grammar'

-- perform sencond step in grammar processing
processGrammarSecondStep :: Grammar -> IO Grammar
processGrammarSecondStep grammar = do
    -- compute accessible symbols set
    let v = nub (computeAccessibleSymbolsSet grammar [start grammar])
    -- remove inaccessible symbols from non-terminal set
    let n' = filter (`elem` v) (nterms grammar)
    -- construct new sigma (alphabet) terminal symbols without inaccessible symbols
    let sigma' = filter (`elem` v) (terms grammar)
    -- filter rules containing inaccessible symbols
    let rules' = filter (\(a, alpha) ->
            elem a n' && foldr (\x acc -> elem x v && acc) True alpha
            ) (rules grammar)

    -- construct final grammar
    let grammar' = Grammar {
        nterms = n',
        terms = sigma',
        start = start grammar,
        rules = rules'
    }
    return grammar'

-- determine if all symbols of alpha (right side of the rule) are
-- members of set ('Nt' union 'Sigma')^*
alphaInNtUSigma :: [String] -> [String] -> [String] -> Bool
alphaInNtUSigma sigma nt alpha = all (\c -> ((||) (elem c sigma) (elem c nt))) alpha

-- compute set of non-terminal symbols generating terminal symbols in =>*
computeNtSet :: Grammar -> [String] -> [String]
computeNtSet grammar nt = do
    let n = computeNtSetIteration grammar nt
    if nt /= n
        then computeNtSet grammar n
        else nt

-- iteration of computeNtSet
computeNtSetIteration :: Grammar -> [String] -> [String]
computeNtSetIteration grammar nt = foldr (\(a, alpha) acc ->
    if alphaInNtUSigma (terms grammar ++ ["#"]) acc alpha && notElem a acc
    then a : acc
    else acc) nt (rules grammar)


-- compute set of accessible symbols
computeAccessibleSymbolsSet :: Grammar -> [String] -> [String]
computeAccessibleSymbolsSet grammar v = do
    let v' = computeAccessibleSymbolsSetIteration grammar v
    if v /= v'
        then computeAccessibleSymbolsSet grammar v'
        else v

-- iteration of computeAccessibleSymbolsSet
computeAccessibleSymbolsSetIteration :: Grammar -> [String] -> [String]
computeAccessibleSymbolsSetIteration grammar v = foldr (\(a, alpha) acc ->
    if a `elem` v
    then filter (`notElem` v) alpha ++ acc
    else acc) v (rules grammar)

-- split string by delimeter
splitByDelimeter :: String -> Char -> [String]
splitByDelimeter str delim =
    let (prefix, end) = break (== delim) str
    in prefix: if null end then [] else splitByDelimeter (tail end) delim

-- print parsed grammar
printGrammar :: Grammar -> IO ()
printGrammar grammar = do
    putStrLn (intercalate "," (nterms grammar))
    putStrLn (intercalate "," (terms grammar))
    putStrLn (start grammar)
    let rls = map (\(nterm, alpha) -> nterm ++ "->" ++ concat alpha) (rules grammar)
    mapM_ putStrLn rls