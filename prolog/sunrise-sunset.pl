#!/usr/bin/env swipl -q
% https://sunrise-sunset.org/api

:- use_module(library(http/http_open)).
:- use_module(library(http/json)).

:- initialization main.

usage :-
  writeln('./sunrise-sunset.pl latitude longitude'),
  writeln('e.g. for Oakland, CA: ./sunrise-sunset.pl 37.8044 122.2712'),
  halt(1)
.

parse_argv([X, Y], Lat, Lon) :- atom_number(X, Lat), atom_number(Y, Lon).

parse_argv(_, _, _) :-
  usage.


% https://www.swi-prolog.org/pldoc/man?predicate=setup_call_cleanup/3
% https://stackoverflow.com/a/29168051/303931

sunrise_sunset(Lat, Lon, Sunrise, Sunset):-
  format(atom(Url), 'https://api.sunrise-sunset.org/json?formatted=0&lat=~w&lng=~w', [Lat, Lon]),
  writeln(Url),
  setup_call_cleanup(
    http_open(
      Url,
      In,
      [request_header('Accept'='application/json')]),
    json_read_dict(In, Dict),
    close(In)),
  parse_time(Dict.results.sunrise, SunriseUtcStamp),
  stamp_date_time(SunriseUtcStamp, D),  % TODO: time zone hell
  date_time_value('time', D, SunriseLocal),
  writeln(SunriseLocal),
  writeln(SunriseUtc),
  writeln(Dict)  % TODO: extract out data from the Dict and print it to screen.
.

main :- 
  current_prolog_flag(argv, Argv),
  parse_argv(Argv, Lat, Lon),
  sunrise_sunset(Lat, Lon, _, _),
  format('Hello World, argv:~w\n', [Argv]),
  halt(0)
.