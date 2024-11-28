# %%
import pandas as pd
import os
from github import Github
from re import match

pd.set_option('display.max_rows', None)
### Do not truncate text
pd.set_option('display.max_colwidth', None)

# %%
# pygithub object
g = Github()
repo = g.get_repo("OpenDataScotland/jkan")
branch = repo.get_branch("gh-pages")
last_commit = branch.commit
#last_commit = repo.get_commit("c7812a7d9135f73256c96ea71863f72dc5a43cc1")

### if running locally, remember to pull latest /jkan/gh-pages also!!!!

# %%
committed_files = pd.DataFrame()
for f in last_commit.raw_data['files']:
    change_type = f['status']
    changes_headers = None
    if change_type=='modified':
        ### breaks the preview into lines
        extract_lines = f['patch'].split('\n')
        ### retains only lines with changes (first char is + or -)
        changes = [line for line in extract_lines if ((line[0]=='+') | (line[0]=='-'))]
        ### retains only the headers of those lines, drop the first char
        changes_headers = [line.split(':')[0][1:] for line in changes]
        ### remove dupe headers
        changes_headers = list(set(changes_headers))

    temp = pd.DataFrame({'change_type':change_type,
            'file':[f['filename']],
            'change':[changes_headers]
    })
    committed_files = pd.concat([committed_files,temp], ignore_index= True, axis=0)

committed_files.loc[committed_files['change_type']=='renamed','change_type'] = 'modified'
print(f'total files: {len(committed_files)}')

# %%
### Load data from all files in folder
org_twitter_all = {}
folder = '../jkan/_organizations'
for dirname, _, filenames in os.walk(folder):
    for filename in filenames:
        with open(f'{dirname}/{filename}','r') as f:
            test_str = f.read()
            test_list = test_str.split('\n')
            org_name, org_handle = None, None
            org_name = list(filter(lambda v: match('title: *', v), test_list))[0].split(': ')[1]
            org_handle = list(filter(lambda v: match('twitter_handle: *', v), test_list))[0].split(': ')[1]
            if (org_handle):
               org_twitter_all[org_name] = f"@{org_handle}"
            else:
                org_twitter_all[org_name] = None

# %%
def get_org(filename):
    org = filename.split('-')[0].replace('_datasets/','')
    return org

def get_org_name(filename):
    try:
        with open(f'../jkan/{filename}','r') as f:
            file_str = f.read()
            lines_list = file_str.split('\n')
            filtered_values = list(filter(lambda v: match('organization:*', v), lines_list))
            org_name = filtered_values[0].split(': ')[1]
            filtered_values = list(filter(lambda v: match('title:*', v), lines_list))
            dataset_title = filtered_values[0].replace('title:','')
    except:
        org_name = 'Error'
        dataset_title = 'Error'
    return org_name, dataset_title

def get_org_twitter(org_name):
    try:
        org_twitter = org_twitter_all[org_name]
    except:
        org_twitter = 'Error'
    return org_twitter


committed_files['organisation'] = committed_files['file'].apply(lambda x: get_org(x))
committed_files[['org_name','title']] = committed_files.apply(lambda x: get_org_name(x['file']),axis=1, result_type='expand')
committed_files['org_twitter'] = committed_files['org_name'].apply(lambda x: get_org_twitter(x))


# %%
tweet_summary = committed_files.groupby(['change_type','organisation','org_twitter'])['file'].count().reset_index()
print(f"{tweet_summary}\n")

# %%
def make_tweet_text(change_types):
    summary_df = committed_files.groupby(['change_type','organisation','org_twitter'])['file'].count().sort_values(ascending=False).reset_index()
    summary_df.loc[summary_df['org_twitter']=='Error','org_twitter'] = 'Unknown'
    summary_df.loc[summary_df['change_type']=='modified','change_type'] = 'updated'
    for ct in change_types:
        ct_df = summary_df[summary_df['change_type']==ct]
        pub_count = len(ct_df)
        total_file_count = ct_df['file'].sum()
        tweet_string = f"{pub_count} publishers {ct} {total_file_count} datasets this week: "
        n = 0
        for row in ct_df.index:
            pub = ct_df.at[row,'org_twitter']
            file_count = ct_df.at[row,'file']
            n += 1
            if n < pub_count:
                tweet_string += f"{pub}({file_count}) "
            else:
                tweet_string += f"and {pub}({file_count}) "
        print(tweet_string)
    return

make_tweet_text(['added','updated','removed'])

if len(committed_files[committed_files['change_type']=='added'])==0:
    None
else:
    print(f"\n Newly added datasets: \n{committed_files.loc[committed_files['change_type']=='added',['org_name','title']].reset_index(drop=True)}")

