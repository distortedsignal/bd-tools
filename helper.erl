-module(helper).

-export([reload_modules/1, reload_server/1, refresh_beams/0]).

-export([start_application/1]).

-export([loud_logging/0, quiet_logging/0]).

-export([dump_mnesia/0, traverse_table_and_show/1]).

-export([atom_test/0]).

-export([add_logging/1, add_many_logging/1]).

% Copy of reg_level_info record found in io/base/apps/bd_logger/include/bd_logger.hrl
-record(reg_level_info, {level_string, level_id, enabled, callback_module}).

-on_load(load_helper_module/0).

load_helper_module() ->
    erlang:system_flag(backtrace_depth, 100),
    % Do something here to load record definitions eventually.
    ok.

atom_test() ->
    atom_test(50000).

atom_test(0) -> ok;
atom_test(K) ->
    A = list_to_atom("test"),
    io:fwrite(atom_to_list(A)),
    atom_test(K-1).

loud_logging() ->
    bd_logger_app:enable_console("AUDIT"),
    bd_logger_app:enable_console("MGMT").

quiet_logging() ->
    bd_logger_app:disable_console("AUDIT"),
    bd_logger_app:disable_console("MGMT").

add_many_logging([]) -> ok;
add_many_logging([LevelAtom | LevelAtomList]) ->
    add_logging(LevelAtom),
    add_many_logging(LevelAtomList).

add_logging(LevelAtom) ->
    NewLevelInfo = #reg_level_info{
        level_string=LevelAtom,
        level_id=LevelAtom,
        enabled=true,
        callback_module=syslog_nif_impl},
    bd_logger_app:register_levels([NewLevelInfo]),
    bd_logger_app:enable_levels("MGMT", [LevelAtom]),
    bd_logger_app:enable_levels("AUDIT", [LevelAtom]).

refresh_beams() ->
    BeamsString = case file:read_file("/root/beam_updates") of
        {error, _} -> "";
        {ok, BeamBinString} ->
            Tmp = binary_to_list(BeamBinString),
            lists:filter(fun(C) -> not lists:member(C, "\n") end, Tmp)
    end,
    ModuleAsStringList = string:tokens(BeamsString, " "),
    ModuleAsAtomList = modules_string_to_atom(ModuleAsStringList, []),
    ReloadedModulesLength = length(reload_modules(ModuleAsAtomList)),
    ReloadedModulesLength = length(ModuleAsAtomList),
    ok = file:delete("/root/beam_updates"),
    ModuleAsAtomList.


modules_string_to_atom([], AtomList) -> AtomList;
modules_string_to_atom([[] | T], AtomList) -> modules_string_to_atom(T, AtomList);
modules_string_to_atom([H | T], AtomList) -> modules_string_to_atom(T, [list_to_atom(H) | AtomList]).

reload_modules(ModuleList) ->
    reload_modules(ModuleList, []).

reload_modules([], ReloadedModules) ->
    ReloadedModules;
reload_modules([ H | T ], ReloadedModules) ->
    reload_modules(T, reload_module(H) ++ ReloadedModules).

reload_module(ModuleName) ->
    code:purge(ModuleName),
    code:load_file(ModuleName),
    [ModuleName].

reload_server([]) ->
    [];
reload_server([ H | T ]) ->
    reload_server(H) ++ reload_server(T);
reload_server(Server) ->
    sys:suspend(Server),
    reload_modules(Server),
    sys:change_code(Server, Server, undefined, []),
    sys:resume(Server),
    [Server].

start_application(Application) ->
    io:fwrite("Attempting to load ~s\n", [Application]),
    case application:start(Application) of
        ok ->
            io:fwrite("Loaded ~s\n", [Application]),
            ok;
        {error, {not_started, DepsApplication}} ->
            io:fwrite("Failed to load ~s, application ~s not loaded.\n", [Application, DepsApplication]),
            start_application(DepsApplication),
            start_application(Application)
    end.

dump_mnesia() ->
    traverse_table_and_show(bdm_config).

traverse_table_and_show(Table_name)->
    Iterator =  fun(Rec,_)->
        case Rec of
            {_, catalog_feeds, _} ->
                io:format("{bdm_config, catalog_feeds, [long]}~n");
            _ ->
                io:format("~p~n",[Rec])
        end,
        []
    end,
    case mnesia:is_transaction() of
        true -> mnesia:foldl(Iterator,[],Table_name);
        false ->
            Exec = fun({Fun,Tab}) -> mnesia:foldl(Fun, [],Tab) end,
            mnesia:activity(transaction,Exec,[{Iterator,Table_name}],mnesia_frag)
    end.

