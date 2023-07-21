% FLP Project 2 - Turing machine simulation
% Author:   Michal Rein (xreinm00)
% Date:     23.04.202


:- dynamic(rule/4).
:- dynamic(tape/1).

% Create new rule as dynamic fact rule().
create_rule([Start, ' ', Symbol, ' ', Next, ' ', Op]) :-
    % format("Creating new rule, start: ~w, symb: ~w, next: ~w, op: ~w|\n", [Start, Symbol, Next, Op]),
    asserta(rule(Start, Symbol, Next, Op)).

% Last line of input won't have rule format, insert this last line as tape() fact.
create_rule(CharList) :- 
    atom_chars(Tape, CharList),
    asserta(tape(Tape)),!.

% Process lines given as list of strings.
process_lines([]) :- !.
process_lines([Head|Tail]) :-
    % Create new dynamic rule and process next line.
    create_rule(Head),
    % If tail is the last line, just add it into rule list (special fact for tape will be created).
    length(Tail, TailLength),
    (TailLength == 1, last(Tail, LastLine), create_rule(LastLine); process_lines(Tail)).

% Search tape for state symbol and return state + tape symbols
get_state(TapeAsCodes, StateSymbol, TapeSymbol) :-
    find_state(TapeAsCodes, Code, StateSymbolIndex), % find state symbol and it's index  
    char_code(StateSymbol, Code),                    % get state symbol as char
    TapeSymbolIndex is StateSymbolIndex + 1,
    nth0(TapeSymbolIndex, TapeAsCodes, Elem),        % get element next to state symbol
    char_code(TapeSymbol, Elem).                     % get tape symbol as char
    
% Find state symbol on the tape, return found symbol with index.
% Each capital letter (state symbols) has ASCII code lesser than 90.
find_state([Head|_], Head, 0) :- Head =< 90, !.
find_state([_|Tail], Char, Index) :-
    find_state(Tail, Char, Index1),
    Index is Index1 + 1.

% Start NTS simulation.
start(Tape, Tapes) :-
    next(Tape, [], NewTapes, 'S'),  % set initial State symbol and start machine execution
    append([NewTapes], Tapes1),     % get all tapes configuration from the last reccurvise call
    nth0(0, Tapes, Tape, Tapes1).   % append initial tape config at the start of the list

% Next state is final.
next(_, Tapes, NewTapes, 'F'):- 
    append([Tapes], NewTapes),!.

% Apply next avaiable rule and make reccursive call.
next(Tape, Tapes, NewTapes, _) :-
    atom_codes(Tape, Codes), % it's easier to manipulate with tape as list of ASCII codes
    get_state(Codes, StateSymbol, TapeSymbol), % get state symbol and current tape symbol
    get_next_rule(StateSymbol, TapeSymbol, NextStateSymbol, NextOperation), % get rule matching current state and tape configuration
    perform_operation(StateSymbol, NextStateSymbol, NextOperation, Tape, NewTape), % perform operation given by rule 
    % Writing operation outputs 2 tape configurations, but sometimes they're the same (only state changed).
    % Shift operations always return only one tape.
    last(NewTape, LastNewTape), 
    % Select wheter append both configurations or just one.
    char_code(StateSymbol, S1),
    char_code(NextStateSymbol, S2),
    char_code(TapeSymbol, T1),
    char_code(NextOperation, T2),
    (S1 \= S2, T1 \= T2, append([Tapes, NewTape], NewTapes1); append([Tapes, [LastNewTape]], NewTapes1)),
    next(LastNewTape, NewTapes1, NewTapes, NextStateSymbol). % reccursive call

% Get next state symbol and operation based on current machine configuration.
get_next_rule(State, Symbol, NextStateSymbol, NextOperation) :-
    rule(State, Symbol, NextStateSymbol, NextOperation).

% Shift left operation
perform_operation(StateSymbol, NextStateSymbol, 'L', Tape, [NewTape]) :-
    % Split tape into two parts, use state symbol as delimeter
    atomic_list_concat([LeftSide|RightSide], StateSymbol, Tape),
    shift_left(LeftSide, NextStateSymbol, NewLeftSide),
    last(RightSide, RightSide1),
    atom_concat(NewLeftSide, RightSide1, NewTape).

% Shift right operation
perform_operation(StateSymbol, NextStateSymbol, 'R', Tape, [NewTape]) :-
    % Split tape into two parts, use state symbol as delimeter
    atomic_list_concat([LeftSide|RightSide], StateSymbol, Tape),
    % Extend right side of the tape with blank symbol if needed
    last(RightSide, RightSideElem),
    atom_length(RightSideElem, RightSideLength),
    % string_length(RightSideString, RightSideLength),
    (RightSideLength == 1, atom_concat(RightSideElem, ' ', ExtendedRightSide),
    shift_right([ExtendedRightSide], NextStateSymbol, NewRightSide);
    shift_right(RightSide, NextStateSymbol, NewRightSide)),
    atom_concat(LeftSide, NewRightSide, NewTape).

% Write operation
perform_operation(StateSymbol, NextStateSymbol, NextTapeSymbol, Tape, NewTape) :-
    % Split tape into two parts, use state symbol as delimeter
    atomic_list_concat([LeftSide|RightSide], StateSymbol, Tape),
    last(RightSide, RightSideElem),
    % Replace first symbol on the right side of the tape with symbol given by the rule
    replace_tape_symbol(RightSide, NextTapeSymbol, NewRightSide),
    % Construct new tape configuration
    atom_concat(LeftSide, NextStateSymbol, TmpString),
    atom_concat(TmpString, RightSideElem, NewTape1),
    atom_concat(TmpString, NewRightSide, NewTape2),
    append([[NewTape1], [NewTape2]], NewTape).

% Make insertion of the next symbol into the right side of the tape.
replace_tape_symbol([RightSide], NewSymbol, NewString) :-
    % Remove first character from string and concatenate with next symbol.
    atom_codes(RightSide, [_|TailCodes]),
    atom_codes(RightSide1, TailCodes),
    atom_concat(NewSymbol, RightSide1, NewString).

% Construct new right part of the tape after shift right opration.
shift_right([RightSide], NextStateSymbol, NewString) :-
    % Convert strings (Right side of the tape) and symbol of the next state into lists (Codes).
    atom_codes(RightSide, Codes),
    atom_codes(NextStateSymbol, NextStateCode),
    last(NextStateCode, NextStateCode1),    % get element (it's the only one).
    % Place new state symbol at it's correct place
    nth1(2, NewRightSideCodes, NextStateCode1, Codes),
    % Convert sequence of codes back to string.
    atom_codes(NewString, NewRightSideCodes).

% Construct new left part of the tape after shift left opration.
shift_left("", _, _) :- !, fail. % shift left out of tape
shift_left(LeftSide, NextStateSymbol, NewString) :-
    % Convert strings (Left side of the tape) and symbol of the next state into lists (Codes).
    atom_codes(LeftSide, Codes),
    atom_codes(NextStateSymbol, NextStateCode),
    atom_length(LeftSide, LeftSideLength),
    last(NextStateCode, NextStateCode1),    % get element (it's the only one)
    % Place new state symbol at it's correct place.
    nth1(LeftSideLength, NewLeftSideCodes, NextStateCode1, Codes),
    % convert sequence of codes back to string.
    atom_codes(NewString, NewLeftSideCodes).

% Create initial tape (add start symbol to initial tape configuration).
init_tape(NewTape) :-
    % Get inital tape config, append starting symbol
    tape(InitialTape),
    atom_concat('S', InitialTape, NewTape).


% Run turing machine simulation.
% Initialize tape configuration, start machine execution and write out all configurations.
run :-
    init_tape(Tape),!,
    start(Tape, Tapes),
    write_tapes_sequence(Tapes). 

% Write all tapes to stdout.
write_tapes_sequence([]) :- !.
write_tapes_sequence([Head|Tail]) :-
    write(Head), nl,
    write_tapes_sequence(Tail).

% ---------- MAIN ------------
main :-
    read_lines(Lines),
    process_lines(Lines),!,
    run.
 

% ------ Input functions -------
read_line(L,C) :-
	get_char(C),
	(isEOFEOL(C), L = [], !;
		read_line(LL,_),
		[C|LL] = L).

isEOFEOL(C) :-
	C == end_of_file;
	(char_code(C,Code), Code==10).

read_lines(Ls) :-
	read_line(L,C),
	( C == end_of_file, Ls = [] ;
	  read_lines(LLs), Ls = [L|LLs]
	).

