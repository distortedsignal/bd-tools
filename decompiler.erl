%% Based off utility.erl, originally from github user binarytemplate.
%% Github gist link:
%% https://gist.github.com/binarytemple/d0dd5644a473e0ba1d73790168681351
-module(decompiler).

-export([decompile/1, decompdir/1]).


decompdir(Dir) ->
    {ok, Filenames} = file:list_dir(Dir),
    F = fun(Filename) -> filename:join(Dir, Filename) end,
    G = fun(Filename) -> string:substr(Filename, length(Filename) - 5) =:= "beam" end,
    FullFilepaths = lists:map(F, lists:filter(G, Filenames)),
    io:format("decompdir: ~p~n",[FullFilepaths]),
    lists:map(fun decompile/1, FullFilepaths).


decompile(Beam) ->
    io:format("decompile: ~p~n",[Beam]),
    {ok, {_, [{abstract_code, {_, A}}]}} = beam_lib:chunks(Beam, [abstract_code]),
    io:fwrite("~s~n", [erl_prettypr:format(erl_syntax:form_list(A))]).

