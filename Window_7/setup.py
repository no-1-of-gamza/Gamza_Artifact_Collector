from distutils.core import setup  
import py2exe, sys, os 

sys.argv.append('py2exe') 

setup(
    options = {
        'py2exe': {
            'bundle_files': 1,
            'unbuffered': True,  # Add this line to fix input() issues
            'includes': ['Artifact'], # Include the 'Artifact' module
            'dll_excludes': ['Secur32.dll', 'SHFOLDER.dll', 'CRYPT32.dll']
        }
    },  
    console = [{'script': "Gamza_Artifact_Collector.py"}],  
    zipfile = None,  
)
