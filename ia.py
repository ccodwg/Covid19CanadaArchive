# ia.py: Functions for uploading and updating files from #
# the Canadian COVID-19 Data Archive to archive.org #
# https://github.com/ccodwg/Covid19CanadaArchive #
# Maintainer: Jean-Paul R. Soucy #

# load modules
import os
import json
import zipfile
import time
import internetarchive as ia # configure credentials w/ ia configure

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
        UUID: <a href="https://raw.githubusercontent.com/ccodwg/Covid19CanadaArchive-index/main/uuid/{d['uuid']}.json">{d['uuid']}</a><br>
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
        'collection': 'opensource_media',
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

# create a zip compressed archive for a UUID
def create_uuid_archive(uuid, in_dir, out_dir):
    # print UUID
    print(uuid)
    # define input path
    in_path = os.path.join(in_dir, *ds[uuid]['dir_parent'].split('/'), ds[uuid]['dir_file'])
    # define output path
    out_path = os.path.join(out_dir, 'cc19da_' + uuid + '.zip')
    # create file list
    file_paths = []
    for root, dirs, files in os.walk(in_path):
        folder = root[len(in_path):] # remove parent directory from path
        for file in files:
            file_path = os.path.join(folder, file)
            file_paths.append((os.path.join(root, file), file_path))
    # create and save zip archive
    with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file, arcname in file_paths:
            zipf.write(file, arcname)

# create zip compressed archives for all UUIDs
def create_uuid_archives(in_dir, out_dir):
    # create output directory, if it doesn't exist
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    for uuid in ds.keys():
        create_uuid_archive(uuid, in_dir, out_dir)

# create an item and upload a zip archive for a UUID
def upload_uuid_archive(uuid, in_dir, log=False):
    # get list of completed UUIDs
    if log:
        # create log if it doesn't exist
        if not os.path.exists('completed_uuids.txt'):
            with open('completed_uuids.txt', 'w') as f:
                f.write('')
        # read log
        with open('completed_uuids.txt', 'r') as f:
            completed_uuids = f.read().splitlines()
            # skip if UUID is already completed
            if uuid in completed_uuids:
                print(f'Skipping: {uuid} already exists')
                return
    # define item name
    item_name = gen_item_name(uuid)
    # create item
    item = ia.get_item(item_name)
    # check if item already exists
    if item.exists:
        # log already uploaded UUIDs if not already logged
        if log and uuid not in completed_uuids:
            with open('completed_uuids.txt', 'a') as f:
                f.write(uuid + '\n')
        # print message
        print(f'Skipping: {uuid} already exists')
        return
    else:
        print(f'Uploading: {uuid}')
    # generate metadata
    md = gen_metadata(uuid)
    # define input path
    in_path = os.path.join(in_dir, 'cc19da_' + uuid + '.zip')
    # upload zip archive
    item.upload(in_path, metadata=md, verbose=True)
    # log UUID
    if log:
        with open('completed_uuids.txt', 'a') as f:
            f.write(uuid + '\n')
    # return True
    return True

# create items and upload zip archives for all UUIDs
def upload_uuid_archives(in_dir):
    for uuid in ds.keys():
        res = upload_uuid_archive(uuid, in_dir, log=True)
        # wait 60 seconds if item was uploaded
        # and uuid is not the last one
        if res and uuid != list(ds.keys())[-1]:
            time.sleep(60)

# update metadata for a UUID
def update_uuid_metadata(uuid):
    # define item name
    item_name = gen_item_name(uuid)
    # get item
    item = ia.get_item(item_name)
    # generate metadata
    md = gen_metadata(uuid)
    # update metadata
    print(f'Updating: {uuid}')
    item.modify_metadata(md)
