-module(helper).

-export([reload_modules/1, reload_server/1]).

-export([start_application/1]).

-export([loud_logging/0, quiet_logging/0]).

-export([dump_mnesia/0, traverse_table_and_show/1]).

-on_load(load_helper_module/0).

load_helper_module() ->
    erlang:system_flag(backtrace_depth, 100),
    % Do something here to load record definitions eventually.
    ok.

loud_logging() ->
    bd_logger_app:enable_console("AUDIT"),
    bd_logger_app:enable_console("MGMT").

quiet_logging() ->
    bd_logger_app:disable_console("AUDIT"),
    bd_logger_app:disable_console("MGMT").

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

