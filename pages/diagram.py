import streamlit as st

import pandas as pd

import altair as alt

import numpy as np
import matplotlib.pyplot as plt

import gudhi as gd
import astropy.units as u

from astropy.io import fits
import sunpy.map

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


def crop_to_square(matrix, xs, xe, ys,ye):
    min_dim = min(matrix.shape)
    normalized = matrix[ys:ye,xs:xe]
    normalized=(normalized-np.min(normalized))/np.max(normalized)
    return normalized








iloc_num = int(np.load('pages/Crop_info/S_file.npy'))
size = int(np.load('pages/Crop_info/S_file.npy'))
center_x = int(np.load('pages/Crop_info/S_file.npy'))
center_y = int(np.load('pages/Crop_info/S_file.npy'))


title = st.text_input("X, Y , Size  Cordination of Center of box ", "200, 200 , 300 ")
if title:
    center_x, center_y, size = int(title.split(',')[0]), int(title.split(',')[1]), int ( title.split(',')[2]) 


def plot_persistence_diagrams( iloc_num, how_many = 3):
    """
    Plot the persistence diagrams for both sublevel and superlevel set filtrations.
    
    Parameters:
    sublevel_cc (gd.CubicalComplex): CubicalComplex object for sublevel set filtration.
    superlevel_cc (gd.CubicalComplex): CubicalComplex object for superlevel set filtration.
    data (array-like): Image data to plot.
    """
    for i in range(how_many):
        data = get_image_matrix(iloc_num)

        data = (data - np.min(data)) /( np.max(data) - np.min(data)) 

        data = crop_to_square(data,int( center_x - size/2 ),int(center_x + size/2 ) , int(center_y - size/2 ), int(center_y +  size/2 ))

        


        # Step 6: Continue with Persistence Homology Analysis for sublevel set filtration
        sublevel_cc = gd.CubicalComplex(top_dimensional_cells=data)
        sublevel_cc.compute_persistence()

        # Step 6: Continue with Persistence Homology Analysis for superlevel set filtration
        superlevel_data = -data
        superlevel_cc = gd.CubicalComplex(top_dimensional_cells=superlevel_data)
        superlevel_cc.compute_persistence()




        sublevel_H0 = sublevel_cc.persistence_intervals_in_dimension(0)
        sublevel_H1 = sublevel_cc.persistence_intervals_in_dimension(1)
        superlevel_H0 = superlevel_cc.persistence_intervals_in_dimension(0)
        superlevel_H1 = superlevel_cc.persistence_intervals_in_dimension(1)

        # Step 3: Plotting the image and the persistence diagram
        fig, axs = plt.subplots(1, 2, figsize=(12, 6))

        # Plot the image
        axs[0].imshow(data, cmap='gray')
        axs[0].set_title("Image")
        axs[0].axis('off')

        # Plot the persistence diagrams
        axs[1].plot(sublevel_H0[:, 0], sublevel_H0[:, 1], '.k', markersize=5, alpha=0.4, label='Sublevel H0')
        axs[1].plot(sublevel_H1[:, 0], sublevel_H1[:, 1], '.r', markersize=5, alpha=0.4, label='Sublevel H1')
        axs[1].plot(-superlevel_H0[:, 0], -superlevel_H0[:, 1], 'xk', markersize=5, alpha=0.4, label='Superlevel H0')
        axs[1].plot(-superlevel_H1[:, 0], -superlevel_H1[:, 1], 'xr', markersize=5, alpha=0.4, label='Superlevel H1')

        axs[1].legend()
        max_val = max(np.max(sublevel_H1), np.max(-superlevel_H1))
        axs[1].plot(np.linspace(0, max_val, 20), np.linspace(0, max_val, 20), '--')

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True) # instead of plt.show()





        data = get_image_matrix(iloc_num+1)

        data = (data - np.min(data)) /( np.max(data) - np.min(data)) 

        data = crop_to_square(data,int( center_x - size/2 ),int(center_x + size/2 ) , int(center_y - size/2 ), int(center_y +  size/2 ))

        
        


        # Step 6: Continue with Persistence Homology Analysis for sublevel set filtration
        sublevel_cc = gd.CubicalComplex(top_dimensional_cells=data)
        sublevel_cc.compute_persistence()

        # Step 6: Continue with Persistence Homology Analysis for superlevel set filtration
        superlevel_data = -data
        superlevel_cc = gd.CubicalComplex(top_dimensional_cells=superlevel_data)
        superlevel_cc.compute_persistence()





        # Step 3: Plotting the image and the persistence diagram
        fig, axs = plt.subplots(1, 2, figsize=(12, 6))

        # Plot the image
        axs[0].imshow(data, cmap='gray')
        axs[0].set_title("Image")
        axs[0].axis('off')

        # Plot the persistence diagrams
        axs[1].plot(sublevel_H0[:, 0], sublevel_H0[:, 1], '.k', markersize=5, alpha=0.3, label='Sublevel H0')
        axs[1].plot(sublevel_H1[:, 0], sublevel_H1[:, 1], '.r', markersize=5, alpha=0.3, label='Sublevel H1')
        axs[1].plot(-superlevel_H0[:, 0], -superlevel_H0[:, 1], 'xk', markersize=5, alpha=0.3, label='Superlevel H0')
        axs[1].plot(-superlevel_H1[:, 0], -superlevel_H1[:, 1], 'xr', markersize=5, alpha=0.3, label='Superlevel H1')

        axs[1].legend()
        max_val = max(np.max(sublevel_H1), np.max(-superlevel_H1))
        axs[1].plot(np.linspace(0, max_val, 20), np.linspace(0, max_val, 20), '--')

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True) # instead of plt.show()



how_many  = st.text_input("How many points to check after iloc num ", "3")
if how_many:
    how_many = int(how_many)

    plot_persistence_diagrams(iloc_num, how_many)












