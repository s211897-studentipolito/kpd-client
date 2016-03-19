#!/usr/bin/python3


##SHELL
#in caso di nozip in config_file allora funzione spacchetta
#config file meglio

import musicpd
import sys
import argparse
import shell, MPDdatabase, util, config_file



##sarebbe carino se il file di configurazione decidesse l'output!




#parse args
def parse_args ():
#arguments
    parser = argparse.ArgumentParser ()
    parser.add_argument ('-p', '--play', nargs = '?', default = False,
            help='toggle play, input number to play song in playlist')
    parser.add_argument ('-n', '--next', action="store_true", default=False,
            help='play next track')
    parser.add_argument ('-ps', '--previous', '--previous', action="store_true", default=False,
            help='play previous track')
    parser.add_argument ('--stop', action="store_true", default=False,
            help='stop playback')
    parser.add_argument ('--random', nargs = '?', default = False,
            help='random [on,off]')
    parser.add_argument ('-u', '--update', action="store_true", default = False,
            help='update mpd database')
    parser.add_argument ('-s', '--search', type = str, nargs = '?', default = False,
            help='search a string in the database, casi insensitive')
    parser.add_argument ('-f', '--filter', nargs = '+', default = False,
            help='filter search result, can use \'artist\', \'album\', \'title\', grep like functionality')
    parser.add_argument ('-a', '--add', action = "store_true", default=False,
            help='add songs to playlist, useful to receive piped input from shell')
    parser.add_argument ('--clear', action = "store_true", default=False,
            help='clear playlist')
    parser.add_argument ('-pl', '--playlist', action = "store_true", default=False,
            help='show playlist')
    parser.add_argument ('--seek', nargs='?', default=False,
            help='seek current track: works by seconds or by percentage ')
    parser.add_argument ('--shuffle', action = "store_true", default=False,
            help='shuffle playlist')
    parser.add_argument ('--consume', nargs = '?', default=False,
            help='consume mode [on,off]')
    parser.add_argument ('--single', nargs = '?', default=False,
            help='single mode [on,off]')
    parser.add_argument ('--swap', nargs = 2, default=False,
            help='swap two tracks in the playlist')
    parser.add_argument ('--shell', '-sh', action='store_true', default = False,
            help='invoke shell')

    args = parser.parse_args ()

    return args
#end parse_args


if __name__ == '__main__':

#MPD connect and client init
    client = musicpd.MPDClient ()
    client.connect ('localhost', '6600')
    args = parse_args ()
    status = client.status ()

    ## config file
    DBlocation, gzipBool = config_file.parse_file ()
    DBlocation = DBlocation.split ('\'')[1]
    #print ('letto dal file:', gzipBool, dbLocation)
    ##end config_file

    #pipe from shell
    if not sys.stdin.isatty() and args.add != False:
        for line in sys.stdin:
            client.add (line[:-1])
        exit ()
    #end pipe from shell

    if not len (sys.argv) > 1:
        if  status['state'] != 'stop':
            util.current_status (client)
        else:
            util.print_playlist (client)
        exit ()

    if args.play != False:
        try:
            if args.play == None:
                if status['state'] == 'stop':
                    util.play (client, 0)
                else:
                    util.pause (client)
            else:
                util.play (client, int (args.play))
        except:
            print ('mpd error: bad song index')
            exit (1)

    if args.shell:
        shell.shell (client, DBlocation)

    if args.next:
        util.next (client)
    if args.previous:
        util.previous (client)
    if args.stop:
        util.stop (client)
    if args.random != False:
        util.mpdrandom (client, args.random)
    if args.update:
        util.update(client)

    if args.filter != False and not args.search:
        print ('Sei \'no stronzo')
        exit(1)
    #search
    if args.search:
        if args.filter:
            util.mpdsearch (args.search, sys.argv, DBlocation, args.filter)
        else:
            util.mpdsearch (args.search, sys.argv, DBlocation, False)
    ##end search
    if args.shuffle:
        util.shuffle (client)
    if args.clear:
         util.clear (client)
    if args.swap:
        util.swap (client, int (args.swap[0]) - 1, int (args.swap[1]) - 1)
    if args.consume != False:
        util.consume (client, args.consume)
    if args.single != False:
        util.single (client, args.single)
    if args.playlist:
        util.print_playlist (client)

    #seek function
    if args.seek != False:
        util.seek (client, args.seek, status)
