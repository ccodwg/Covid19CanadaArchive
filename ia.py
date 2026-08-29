# ia.py: Update metadata for Canadian COVID-19 Data Archive items on archive.org
# https://github.com/ccodwg/Covid19CanadaArchive
# Maintainer: Jean-Paul R. Soucy
#
# Usage:
#   python ia.py                         # update all UUIDs
#   python ia.py --dry-run               # preview all updates
#   python ia.py --uuid UUID1 UUID2      # update selected UUIDs
#   python ia.py --uuid UUID1 --dry-run  # preview selected UUIDs

import argparse
import json
import time
import internetarchive as ia  # configure credentials w/ ia configure

# load and unpack datasets.json
with open('datasets.json') as json_file:
    ds_raw = json.load(json_file)

ds = {}
for a in ds_raw:
    for d in ds_raw[a].keys():
        for i in range(len(ds_raw[a][d])):
            ds[ds_raw[a][d][i]['uuid']] = ds_raw[a][d][i]

# generate title for UUID
def gen_title(uuid):
    return f"{ds[uuid]['id_name']} [Canadian COVID-19 Data Archive]"

# generate HTML description for UUID
def gen_description(uuid):
    # get data
    d = ds[uuid]
    # define group
    meta_group = d['metadata']['meta_group_1']
    if 'meta_group_2' in d:
        meta_group += f" / {d['metadata']['meta_group_2']}"
    # add mandatory fields
    descr = f'''
    <div>
        <a href="https://github.com/ccodwg/Covid19CanadaArchive">Canadian COVID-19 Data Archive</a><br>
        ID name: {d['id_name']}<br>
        Group: {meta_group}<br>
        File group: <a href="{d['metadata']['meta_url']}">{d['metadata']['meta_url_name']}</a><br>
        File name: {d['metadata']['meta_name']}<br>
    '''
    if 'url_fun_python' in d:
        descr += f'Dynamic URL retrieved from: <a href="{d["metadata"]["meta_url"]}">{d["metadata"]["meta_url"]}</a><br>'
    else:
        descr += f'URL: <a href="{d["url"]}">{d["url"]}</a><br>'
    descr += f'''
        UUID: <a href="https://raw.githubusercontent.com/ccodwg/Covid19CanadaArchive-index/main/uuid/json/{d['uuid']}.json">{d['uuid']}</a><br>
        File path: {d['dir_parent']}/{d['dir_file']}/{d['file_name']}.{d['file_ext']}<br>
    '''
    # add optional fields
    if 'notes_data' in d.get('notes', {}):
        descr += f'<br>Data notes: {d["notes"]["notes_data"]}<br>'
    if 'notes_usage' in d.get('notes', {}):
        descr += f'<br>Usage notes: {d["notes"]["notes_usage"]}<br>'
    if 'notes_misc' in d.get('notes', {}):
        descr += f'<br>Misc notes: {d["notes"]["notes_misc"]}<br>'
    # close tag
    descr += '</div>'
    # return
    return descr

# generate subjects for UUID
def gen_subjects(uuid):
    subjects = ['covid-19', 'canada']
    # add province/territory
    all_pt = [
        'alberta', 'british columbia', 'manitoba',
        'new brunswick', 'newfoundland and labrador',
        'northwest territories', 'nova scotia', 'nunavut',
        'ontario', 'prince edward island', 'quebec',
        'saskatchewan', 'yukon']
    pt = next((i.lower() for i in all_pt if i.lower() in
               ds[uuid]['metadata'].get('meta_group_1', "").lower() or
               i.lower() in ds[uuid]['metadata'].get('meta_group_2', "").lower()),
               None)
    if pt:
        subjects.append(pt)
    # add CC19DA
    subjects.append('cc19da')
    # return
    return subjects

# generate license for UUID
def gen_license(uuid):
    if 'meta_licence_url' in ds[uuid]['metadata']:
        return ds[uuid]['metadata']['meta_licence_url']
    else:
        return None

# generate metadata for UUID
def gen_metadata(uuid):
    # generate title
    title = gen_title(uuid)
    # generate description
    descr = gen_description(uuid)
    # generate subjects
    subjects = gen_subjects(uuid)
    # generate metadata
    md = {
        'title': title,
        'mediatype': 'data',
        'collection': ['opensource_media', 'canadian-covid-19-data-archive'],
        'date': '2024-01-31',
        'description': descr,
        'subject': subjects,
        'creator': 'Canadian COVID-19 Data Archive',
        'language': ['English', 'French']
        }
    # add license, if available
    license = gen_license(uuid)
    if license:
        md['licenseurl'] = license
    # return
    return md

# generate item name
def gen_item_name(uuid):
    return 'cc19da_' + uuid

# compare generated metadata with archive.org metadata
def metadata_equal(key, generated, existing):
    if key == 'collection':
        return existing == generated[-1]

    if key == 'description':
        existing = existing.replace(' rel="ugc nofollow"', '')
        existing = existing.replace('<br />', '<br>')

    return generated == existing

# update metadata for a UUID
def update_uuid_metadata(uuid, dry_run=False):
    item = ia.get_item(gen_item_name(uuid))
    md = gen_metadata(uuid)

    changed = any(
        not metadata_equal(key, value, item.metadata.get(key))
        for key, value in md.items()
    )

    if not changed:
        print(f'Unchanged: {uuid}')
    elif dry_run:
        print(f'Would update: {uuid}')
    else:
        print(f'Updating: {uuid}')
        item.modify_metadata(md)
        time.sleep(1)

# update selected UUIDs, or all by default
def update_metadata(uuids=None, dry_run=False):
    if uuids is None:
        uuids = list(ds.keys())

    for i, uuid in enumerate(uuids, 1):
        print(f'[{i}/{len(uuids)}] ', end='')
        update_uuid_metadata(uuid, dry_run=dry_run)

# command line interface
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--uuid', nargs='+')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    update_metadata(args.uuid, dry_run=args.dry_run)
