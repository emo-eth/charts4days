import billboard

"Utils for formatting billboard charts as tweets"
links_dont_count = False
artist_handles = {}


def format_entry_as_tweet(source, chart, entry):
    """Returns an entry formatted as a tweet <140ch
    Args:
        string source: name of the source (eg billboard)
        string chart: name of chart (eg Hot-100)"""
    if chart == 'billboard-200':
        twstr = 'US Top Albums: '
    else:
        twstr = source + ' ' + chart.title() + ': '
    # add rank and change
    twstr = twstr + '#' + str(entry.rank) + format_change(entry.change)
    # add title
    twstr = twstr + ' ' + entry.title + ','
    # add artist
    twstr = twstr + ' ' + format_artist(entry.artist)
    # add weeks
    twstr = twstr + ' ' + format_weeks(entry.weeks)
    twstr = twstr.strip()
    # special stuff
    twstr = twstr + ' ' + hotshot_suffix(entry.change)
    twstr = twstr.strip()
    twstr = twstr + ' ' + peak_suffix(entry)
    # compensate for hella featured artists
    twstr = twstr.strip()
    if len(twstr) > 140:
        temp = compensate(twstr, entry.artist)
        assert len(temp) <= 140, "Time to write that title-compensate function"
        twstr = temp
    if links_dont_count:
        twstr = twstr + ' ' + link(chart, entry.spotifyID)
    return twstr.strip()


def format_change(change):
    if change == '0':
        return '(=)'
    elif change == 'New':
        return '(new)'
    elif change == 'Re-Entry':
        return '(re-entry)'
    elif any(change.startswith(x) for x in ['+', '-']):
        return '(' + change + ')'
    return '(new)'


def format_artist(artist):
    """Returns a string of artists/featured artists, replacing with handle
    where necessary.
    Args:
        string artist: artist property of entry object"""

    artist = format_feat(artist)
    # split on featured
    featured_artists = artist.split(' feat. ')
    # if contains a featured artist, figure that out
    if len(featured_artists) > 1:
        # create a featured list
        featured_list = []
        artist = featured_artists[0]
        featured = format_ampersand(featured_artists[1]).split(', ')
        for a in featured:
            featured_list.append(artist_handles.get(artist, artist))
        main_handle = artist_handles.get(artist, artist)
        return main_handle + ' feat. ' + ', '.join(featured_list)
    return artist_handles.get(artist, artist)


def format_feat(artist):
    """Formats featuring, Featuring, feat., feat, etc to a uniform string"
    Doesn't handle ' with ', unfortunately."""
    artist = artist.replace('Featuring', 'feat.')
    artist = artist.replace('featuring', 'feat.')
    artist = artist.replace('Feat.', 'feat.')
    artist = artist.replace(' feat ', ' feat. ')
    artist = artist.replace(' Feat ', ' feat. ')
    return artist


def format_ampersand(artist_split):
    "Replace ampersand with a comma for featured artists for splitting"
    if '&' in artist_split and ',' in artist_split:
        artist_split = artist_split.replace(', & ', ' & ')
        return artist_split.replace(' & ', ', ')
    return artist_split


def format_weeks(weeks):
    if type(weeks) != int:
        try:
            int(weeks)
        except:
            return ''
    if weeks > 1:
        return '[{0} weeks]'.format(weeks)
    return ''


def hotshot_suffix(change):
    if change == 'Hot Shot Debut':
        return '*Hot Shot Debut*'
    return ''


def peak_suffix(entry):
    "Returns *new peak* if ostensibly the new peak"
    "TODO: create a dict of name artist: peak and check that way?"
    peak = entry.peakPos
    change = entry.change
    rank = entry.rank
    if change.startswith('+'):
        if rank == peak:
            return '*New Peak*'
    return ''


def compensate(twstr, artist):
    "Compensates for long artist strings, trail with ..."
    artist_format = format_artist(artist)
    over = len(twstr) - 140
    try:
        replace_str = artist_format[:-over - 3] + '...'
        return twstr.replace(artist_format, replace_str)
    except:
        return twstr


def link(chart, spid):
    if not spid or type(spid) is not str:
        return ''
    open_link = 'https://open.spotify.com/'
    if chart == 'billboard-200':
        open_link = open_link + 'album/' + spid
        return open_link
    open_link = open_link + 'track/' + spid
    return open_link


def get_tweets():
    "Returns a list of tweet-formatted hot-100 and top albums charts"
    tweets = []
    todays_chart = billboard.ChartData('hot-100')
    two_hundred = billboard.ChartData('billboard-200')
    for entry in todays_chart.entries:
        x = format_entry_as_tweet('Billboard', 'hot-100', entry)
        tweets.append(x)
        # print(entry.__dict__)

    for entry in two_hundred.entries:
        x = format_entry_as_tweet('Billboard', 'billboard-200', entry)
        tweets.append(x)
        # print(entry.__dict__)
    return tweets
