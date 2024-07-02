import streamlit as st
import pandas as pd
import altair as alt


import os
import numpy as np
import matplotlib.pyplot as plt
import gudhi as gd
import astropy.units as u
from astropy.io import fits
from sunpy.net import Fido, attrs as a
import sunpy.map
from astropy.time import Time, TimeDelta

from PIL import Image

import os
import sunpy.map
import numpy as np

import streamlit as st
from PIL import Image

import os
from sunpy.net import Fido, attrs as a
import sunpy.map



st.set_page_config(
    page_title="Sun MagnetoGeram Persistanse Homology",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")



iloc_number = st.number_input("Insert a number", value=None, placeholder="Type a number...")
#st.write("The current iloc number is ", iloc_number)



if st.button("GIF"):


        st.switch_page("Pages/gif.py")


# Define the time range
time_range = a.Time('2015-03-11T16:00:00', '2015-03-11T17:00:00')

# Directory to save the downloaded files
download_dir = 'solar_data'

# Check if the directory exists, create if not
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# Search for SOT data within the defined time range
try:
    search_result = Fido.search(a.Instrument.sot, time_range)
    print("Search completed successfully.")
except Exception as e:
    print(f"Error occurred during search: {e}")

# Check if files already exist in the download directory
existing_files = [f for f in os.listdir(download_dir) if os.path.isfile(os.path.join(download_dir, f))]
download_needed = len(existing_files) == 0

# Download the data only if not already downloaded
if download_needed:
    try:
        downloaded_files = Fido.fetch(search_result, path=os.path.join(download_dir, '{file}'))
        print("Data downloaded successfully.")
    except Exception as e:
        print(f"Error occurred during download: {e}")
else:
    downloaded_files = [os.path.join(download_dir, f) for f in existing_files]
    print("Files already exist, skipping download.")



from PIL import Image, ImageOps 

def get_image_matrix(iloc, download_dir='solar_data'):
    import os
    import sunpy.map

    # List all files in the download directory
    files = [os.path.join(download_dir, f) for f in os.listdir(download_dir) if os.path.isfile(os.path.join(download_dir, f))]
    
    # Ensure the index is within the range of available files
    if iloc < 0 or iloc >= len(files):
        raise IndexError("Index out of range. Please provide a valid index.")
    
    # Load the specified file using SunPy
    file_path = files[iloc]
    sun_map = sunpy.map.Map(file_path)
    
    # Return the data matrix of the image
    return sun_map.data




title = st.text_input("X, Y , Size  Cordination of Center of box ", "200, 200 , 300 ")
X, Y, size = int(title.split(',')[0]), int(title.split(',')[1]), int ( title.split(',')[2]) 






matrix_init = get_image_matrix(int(iloc_number))
normalized= (matrix_init - np.min(matrix_init)) /( np.max(matrix_init) - np.min(matrix_init)) 

fig = plt.figure(figsize=[10,16 ], dpi = 100)
plt.imshow(normalized)
plt.yticks(fontsize=18)

plt.xticks(fontsize=18)

import streamlit as st

col1, col2, col3 = st.columns(3)

with col1:
    
    if st.button("Crop And Analyse"):
        np.save('Pages/Crop_info/iloc_num', iloc_number)
        np.save('Pages/Crop_info/X_file', X)
        np.save('Pages/Crop_info/Y_file', Y)
        np.save('Pages/Crop_info/S_file', size)


        st.switch_page("Pages/diagram.py")



    st.write(' ')

with col2:
    st.pyplot(fig,use_container_width = True ) # instead of plt.show()

with col3:
    st.write("Center Cordination",X , Y)    
