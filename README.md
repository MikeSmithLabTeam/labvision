# labvision
Repository for managing images, videos and cameras. 

## Documentation 
    https://lab-vision.readthedocs.io/en/latest/

## Installation from github
    pip install git+https://github.com/MikeSmithLabTeam/labvision
    
## Manually add pyqt5 dependency from conda and ffmpeg from conda-forge

    conda install -c conda-forge pyqt
    conda install conda-forge::ffmpeg

    
    
## Updating if already installed
    pip install --upgrade git+https://github.com/MikeSmithLabTeam/labvision
    
## To add as a dependency to another pip repository
Add the following argument to setup.py setuptools.setup()

    dependency_links=['https://github.com/MikeSmithLabTeam/labvision/tarball/repo/master#egg=package-1.0'],
