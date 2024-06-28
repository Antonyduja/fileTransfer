import requests
import streamlit as st
import pandas as pd
import os 
from main import read_config_file


st.title("API Response Display")
base_url = "http://localhost:8000"  # Change this to your FastAPI server URL if different

st.subheader("Get Root Files Metadata")
if st.button("Submit"):
        
        try:
            config = read_config_file()
            folder_location = config['folder_location']
            folder_name = os.path.basename(folder_location)
            # Construct the full URL with the folder parameter
            url = f"{base_url}/rootFileList"
            response = requests.get(url)
            if response.status_code == 200:
                # st.write(response.json())
                data = response.json()
                if 'files' in data and 'fileCount'in data:
                     folder_name = os.path.basename(folder_location)
                     filecount = data['fileCount']
                     folders_list = []
                     files_list = []
                     st.write(f'The number of files present in the {folder_name} folder: {filecount}')
                     for metadata in data['files']:
                          if metadata['type'] == 'folder':
                               metadata.pop('size', None)
                               metadata.pop('last_modified', None)
                               folders_list.append(metadata)
                            #    print(folders_list)
                          else:
                            #    download_url = metadata.get('downloadUrl', 'N/A')
                            #    download_url = f"{base_url}/download{download_url}"
                            #    print(download_url)
                            #    metadata['downloadUrl'] = download_url
                            #    st.markdown(f"Download link: [{metadata['filename']}]({download_url})")
                               files_list.append(metadata)                          
                     if files_list:
                        df_files= pd.DataFrame(files_list)
                        st.subheader("List of files")
                        st.write(f'Number of files present: {len(df_files)}')
                        # st.dataframe(df_files)
                        df_files['downloadUrl'] = df_files['downloadUrl'].apply(lambda x: f"{base_url}/download?filename={x}")
                        st.data_editor(
                            df_files,
                            column_config={
                                "downloadUrl": st.column_config.LinkColumn(
                                    "Download Link", 
                                    display_text="Download"
                                ),
                            },
                            hide_index=True,
                        )
                     if folders_list:
                        df_folders = pd.DataFrame(folders_list)
                        st.subheader("List of folders")
                        st.write(f'Number of folders present: {len(df_folders)}')
                        # st.dataframe(df_folders)    
                        df_folders['folder_path'] = df_folders['file_Path'].apply(lambda x: f"{base_url}/rootFileList{x}")
                        st.data_editor(
                            df_folders,
                            column_config={
                                "folder_path": st.column_config.LinkColumn(
                                    "Go to folder", 
                                    display_text="GO"
                                ),
                            },
                            hide_index=True,
                        )   
                else:
                     st.error(f"Could not convert to dataframe") 
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"An error occurred: {e}")