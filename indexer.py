# indexer.py: Index files included in Covid19CanadaArchive #
# https://github.com/ccodwg/Covid19CanadaArchive #
# Maintainer: Jean-Paul R. Soucy #

# import modules
print('Importing modules...')

## archivist.py
import archivist

# list of environmental variables used in this script (through functions in archivist.py)
## GD_KEY: environmental variable of Google Drive credentials as a simple string (used when mode = server)
## GH_TOKEN: personal access token for the GitHub API (used when mode = server)
## GH_NAME: name to use for GitHub commits (used when mode = server)
## GH_MAIL: email address to use for GitHub commits (used when mode = server)

# set mode from argv (server vs. local and prod vs. test)
archivist.set_mode()

# access Google Drive
if archivist.mode == 'serverprod' or archivist.mode == 'localprod':
    ## access Google Drive
    archivist.drive = archivist.access_gd()

# clone GitHub repo
if archivist.mode == 'serverprod' or archivist.mode == 'localprod':
    ## get GitHub access token, name, mail
    if archivist.mode == 'serverprod':
        archivist.gh_token = os.environ['GH_TOKEN']
        archivist.gh_name = os.environ['GH_NAME']
        archivist.gh_mail = os.environ['GH_MAIL']
    elif archivist.mode == 'localprod':
        archivist.gh_token = open('.gh/.gh_token.txt', 'r').readline().rstrip()
        archivist.gh_name = open('.gh/.gh_name.txt', 'r').readline().rstrip()
        archivist.gh_mail = open('.gh/.gh_mail.txt', 'r').readline().rstrip()
    ## clone repo to temporary directory
    repo_tmpdir = archivist.tempfile.TemporaryDirectory()
    archivist.repo = archivist.clone_gh(repo_tmpdir)

# create index
index = archivist.create_index()

# write index to CSV
archivist.write_index(index)

#d = index.set_index(['dir_parent', 'dir_file', 'file_name'])
#{level0: { level1: {level2: d.xs([level0, level1, level2]).to_dict('index') for level2 in d.index.levels[2]} for level1 in d.index.levels[1]} for level0 in d.index.levels[0]}

#d = {k: f.groupby('dir_file')['file_name'].apply(list).to_dict()
     #for k, f in index.groupby('dir_parent')}

#ppdict = {n: grp.loc[n].to_dict('index')
 #for n, grp in index.set_index(['dir_parent', 'dir_file']).groupby(level='dir_parent')}
#print (json.dumps(ppdict, indent=2))
#import json
#with open('data.json', 'w', encoding='utf-8') as f:
    #json.dump(d, f, ensure_ascii=False, indent=4)

#def split_dir_parent(index):
    #for (dir_parent), index_dir_parent in index.groupby(["dir_parent"]):
        #yield {
            #dir_parent: list(split_dir_file(index_dir_parent))
        #}

#def split_dir_file(index_dir_parent):
    #for (dir_file), index_dir_file in index_dir_parent.groupby(["dir_file"]):
        #yield {
            #"dir_file": dir_file,
            #"file_name": list(split_file_name(index_dir_file))
        #}

#def split_file_name(index_dir_file):
    #for (file_name), index_file_name in index_dir_file.groupby(["file_name"]):
        #yield {
            #"file_name": file_name,
            #"file_info": list(split_file_info(index_file_name))
        #}    

#def split_file_info(index_dir_file):
    #for row in index_dir_file.itertuples():
        #yield {
            #"file_md5": row.file_md5
        #}

#with open('data.json', 'w', encoding='utf-8') as f:
    #json.dump(list(split_dir_parent(index)), f, ensure_ascii=False, indent=4)

#list(split_dir_parent(index))

#def split_category(df_vendor):
    #for (category, count), df_category in df_vendor.groupby(
        #["Categories", "Category_Count"]
    #):
        #yield {
            #"name": category,
            #"count": count,
            #"subCategories": list(split_subcategory(df_category)),
        #}

#def split_subcategory(df_category):
    #for row in df.itertuples():
        #yield {"name": row.Subcategory, "count": row.Subcategory_Count}

#list(split_df(df))


#j = (index.groupby(['dir_parent', 'dir_file', 'dir_id', 'file_name'], as_index=False)
             #.apply(lambda x: x[['file_timestamp', 'file_date', 'file_date_true']].to_dict('r'))#,
                                 ##'file_id', 'file_mime_type', 'file_size',
                                 ##'file_md5', 'file_md5_duplicate', 'file_url']].to_dict('r'))
             #.reset_index()
             #.rename(columns={0:'file_info'})
             #.to_json(orient='records'))


#index2 = index.set_index(['dir_parent', 'dir_file', 'dir_id', 'file_name'])
#index2.to_json("data.json", orient = "index")