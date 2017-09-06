-module(helper).

-export([reload_modules/1, reload_server/1]).

reload_modules([]) ->
    [];
reload_modules([ H | T ]) ->
    reload_modules(H) ++ reload_modules(T);
reload_modules(ModuleName) ->
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