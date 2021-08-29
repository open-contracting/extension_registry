#!/usr/bin/env python
import csv
import json
import os
import re
from collections import defaultdict
from datetime import timedelta
from pathlib import Path
from urllib.parse import urlsplit

import click
import requests
import requests_cache
from ocdsextensionregistry import ExtensionVersion

directory = Path(__file__).resolve().parent
requests_cache.install_cache(expire_after=timedelta(hours=1))


def do_build():
    # Collect the possible extension versions to build.
    extension_versions = defaultdict(list)
    with open(directory / 'extension_versions.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Ignore v1.1 and v1.1.1 versions, as these are superseded by versions using the new extension.json format.
            if row['Version'] not in ('v1.1', 'v1.1.1'):
                extension_versions[row['Id']].append(row)

    # Collect the extension versions to build.
    extensions = []
    with open(directory / 'extensions.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            versions = extension_versions[row['Id']]

            # Prefer frozen versions to live versions.
            frozen_versions = [version for version in versions if version['Date']]
            if frozen_versions:
                versions = frozen_versions

            # Get the most recent frozen version. We presently have no strategy for choosing between live versions.
            version = max(versions, key=lambda version: version['Date'])

            response = requests.get(version['Base URL'] + 'extension.json')
            response.raise_for_status()

            data = response.json()
            extensions.append({
                'id': row['Id'],
                'category': row['Category'],
                'core': row['Core'] == 'true',
                'url': version['Base URL'],
                'name': {
                    'en': data['name']['en'],
                },
                'description': {
                    'en': data['description']['en'],
                },
                'documentation_url': data['documentationUrl']['en'],
            })

    return json.dumps({'extensions': extensions}, ensure_ascii=False, indent=2, sort_keys=True) + '\n'


def _sort(filename):
    with open(directory / filename, 'r') as f:
        fieldnames = next(f)
        rows = f.readlines()

    with open(directory / filename, 'w') as f:
        f.write(fieldnames)
        for row in sorted(rows):
            f.write(row)


def _write(filename, row):
    with open(directory / filename, 'a') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(row)

    _sort(filename)


@click.group()
def cli():
    pass


@cli.command()
@click.argument('url')
def add(url):
    """
    Add a new extension and its live version to the registry.
    """
    parsed = urlsplit(url)
    if parsed.netloc not in ('github.com', 'gitlab.com'):
        raise click.BadParameter('URL must be of the form https://github.com/org/repo or https://gitlab.com/org/repo')

    name = url.rsplit('/', 1)[-1]

    if parsed.netloc == 'github.com':
        base_url = parsed._replace(netloc='raw.githubusercontent.com', path=parsed.path + '/master/').geturl()
        download_url = url + '/archive/master.zip'
    elif parsed.netloc == 'gitlab.com':
        base_url = url + '/-/raw/master/'
        download_url = '{}/-/archive/master/{}-master.zip'.format(url, name)

    with open(directory / 'extension_versions.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Base URL'] == base_url:
                raise click.BadParameter('Extension version with Base URL "{}" already exists.'.format(base_url))

    default = re.match(r'\Aocds_(\w+)_extension\Z', name)
    if default:
        default = default[1]

    with open(directory / 'schema' / 'extensions-schema.json') as f:
        choices = json.load(f)['properties']['Category']['enum']

    _id = click.prompt('Id', default=default)
    category = click.prompt('Category', type=click.Choice(choices), default='')
    core = click.confirm('Core')

    _write('extensions.csv', [_id, category, 'true' if core else None])
    _write('extension_versions.csv', [_id, None, 'master', base_url, download_url])


@cli.command()
def refresh():
    """
    Auto-discover and add new versions of registered extensions.
    """
    versions = []
    tags = defaultdict(list)

    with open(directory / 'extension_versions.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            version = ExtensionVersion(row)
            if version.date:
                tags[version.id].append(version.version)
            elif urlsplit(version.base_url).netloc == 'raw.githubusercontent.com':
                versions.append(version)
            else:
                click.echo('{} not supported, skipping...'.format(version.base_url))

    with open(directory / 'extension_versions.csv', 'a') as f:
        writer = csv.writer(f, lineterminator='\n')
        for version in versions:
            name = version.repository_full_name
            url = 'https://api.github.com/repos/{}/releases?per_page=100'.format(name)

            response = requests.get(url)
            response.raise_for_status()

            for release in response.json():
                tag = release['tag_name']
                if tag not in tags[version.id]:
                    base_url = 'https://raw.githubusercontent.com/{}/{}/'.format(name, tag)
                    writer.writerow([version.id, release['published_at'][:10], tag, base_url, release['zipball_url']])

    _sort('extension_versions.csv')


@cli.command()
def build():
    """
    Compile build/extensions.json.
    """
    with open(os.path.join(directory, 'build', 'extensions.json'), 'w') as f:
        f.write(do_build())


if __name__ == '__main__':
    cli()
