# -*- coding: utf-8 -*-
import logging
from argparse import ArgumentParser
from bs4 import BeautifulSoup
import requests
from jinja2 import FileSystemLoader, Environment
from datetime import datetime
import sys
import errno
import os

log = logging.getLogger(__name__)

STUDIOS = {
    'a1': {
        'name': 'A1 Pictures',
        'logo': 'images/anime/studios/a1.png'
    },
    'aic': {
        'name': 'Anime International Company',
        'logo': 'images/anime/studios/aic.png'
    },
    'bones': {
        'name': 'Bones',
        'logo': 'images/anime/studios/bones.png'
    },
    'brains': {
        'name': 'Brains Base',
        'logo': 'images/anime/studios/brains_base.png'
    },
    'jc': {
        'name': 'JC Staff',
        'logo': 'images/anime/studios/jc_staff.png'
    },
    'kyoto': {
        'name': 'Kyoto Animation',
        'logo': 'images/anime/studios/kyoto.png'
    },
    'lerche': {
        'name': 'Lerche',
        'logo': 'images/anime/studios/lerche.png'
    },
    'madouse': {
        'name': 'Madhouse',
        'logo': 'images/anime/studios/madhouse.png'
    },
    'pa': {
        'name': 'PA Works',
        'logo': 'images/anime/studios/pa_works.png'
    },
    'ig': {
        'name': 'Production IG',
        'logo': 'images/anime/studios/production_ig.png'
    },
    'shaft': {
        'name': 'Shaft',
        'logo': 'images/anime/studios/shaft.png'
    },
    'tbs': {
        'name': 'TBS',
        'logo': 'images/anime/studios/tbs.png'
    },
    'trigger': {
        'name': 'Trigger',
        'logo': 'images/anime/studios/trigger.png'
    },
    'troyca': {
        'name': 'Troyca',
        'logo': 'images/anime/studios/troyca.png'
    },
    'ufotable': {
        'name': 'Ufotable',
        'logo': 'images/anime/studios/ufotable.png'
    },
    'whitefox': {
        'name': 'WhiteFox',
        'logo': 'images/anime/studios/white_fox.png'
    },
    'wit': {
        'name': 'WIT',
        'logo': 'images/anime/studios/wit.png'
    }
}

ANILIST_API = 'https://graphql.anilist.co'

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

# def anilist_authenticate(client_id, client_secret):
#     params = {
#         'grant_type': 'client_credentials',
#         'client_id': client_id,
#         'client_secret': client_secret,
#     }
#     r = requests.post("{}/auth/access_token".format(ANILIST_API), params=params)
#     r.raise_for_status()
#     return r.json()['access_token']


def anilist_browse_season(year, season, sort='popularity-desc'):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    params = {
        'year': year,
        'season': season,
        'sort': sort,
    }
    payload = {
        'operationName': 'seasonQuery',
        'query': """
        query seasonQuery($year: Int, $season: MediaSeason) {
          Page(page: 1, perPage: 100) {
            media(seasonYear: $year, season: $season, sort: [POPULARITY_DESC]) {
              id
              description
              title {
                userPreferred
              }
              coverImage {
                large
              }
              siteUrl
              studios {
                nodes {
                  name
                }
              }
            }
          }
        }
        """,
        'variables': {
            'year': year,
            'season': season.upper()
        }
    }
    r = requests.post(ANILIST_API, json=payload, headers=headers)
    r.raise_for_status()
    return r.json()


# def anilist_anime_model_page(access_token, anime_id):
#     headers = {
#         'Authorization': 'Bearer {}'.format(access_token),
#     }
#     r = requests.get("{}/anime/{}/page".format(ANILIST_API, anime_id), headers=headers)
#     r.raise_for_status()
#     return r.json()


def anilist_save_image(anime_model, image_dir=None):
    if image_dir:
        mkdir_p(image_dir)
        filename = anime_model['coverImage']['large'].split('/')[-1]
        anime_model['__pv_filename__'] = filename
        img = requests.get(anime_model['coverImage']['large'])
        with open('%s/%s' % (image_dir, filename), 'wb') as f:
            f.write(img.content)
            f.close()

    sys.stdout.write('.')
    sys.stdout.flush()

    return anime_model
    

if __name__ == '__main__':
    """
    Examples:

        python scripts/bootstrap_anime_first.py --season spring --year 2017 -o content/2016/anime_spring_first.md --save_images

        mogrify -resize 320x *.jpg # (revert hero.jpg)

    """
    logging.getLogger().addHandler(logging.StreamHandler())

    parser = ArgumentParser('Template bootstrap')
    parser.add_argument('--template', '-t', default=None)
    parser.add_argument('--output', '-o')
    # parser.add_argument('--hummingbird', '-hb', dest='hummingbird_slug')
    # parser.add_argument('--studio', '-s', choices=STUDIOS.keys())
    parser.add_argument('--year', type=int)
    parser.add_argument('--season')
    parser.add_argument('--save_images', default=False, action='store_true')

    args = parser.parse_args()

    loader = FileSystemLoader('templates/')
    env = Environment(loader=loader)
    data = {}

    if not args.template and args.season:
        args.template = 'anime_first.md'
    # elif not args.template and args.hummingbird_slug:
    #     args.template = 'anime_review.md'

    dt = datetime.now()
    data['timestamp'] = dt.isoformat(" ")[:-7]
    data['year'] = args.year

    image_dir = None
    if args.season and args.save_images:
        image_dir = 'content/images/anime/%d/%s' % (args.year, args.season)
    # elif args.hummingbird_slug and args.save_images:
    #     image_dir = 'content/images/%d/%s' % (data['year'], args.hummingbird_slug.replace('-', '_'))

    # if args.season and args.season == 'winter':
    #    data['year'] += 1

    # if args.hummingbird_slug:
    #     data.update(parse_hummingbird(args.hummingbird_slug, image_dir))
    # if args.season:
    #     data.update(process_hummingbird_upcoming(args.season, image_dir))

    # access_token = anilist_authenticate(args.client_id, args.client_secret)
    anime_models = anilist_browse_season(args.year, args.season)

    data.update({
        'shows': [anilist_save_image(m, image_dir) for m in anime_models['data']['Page']['media']],
        'season': args.season,
    })

    # data['studio'] = STUDIOS.get(args.studio, {'name': 'Unknown', 'logo': 'Unknown'})
    template = env.get_template(args.template)

    if args.output:
        with open(args.output, 'wb') as fp:
            fp.write(template.render(data).encode('utf8'))
    else:
        print(template.render(data))
