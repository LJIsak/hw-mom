import PyInstaller.__main__

def build_exe():
    PyInstaller.__main__.run([
        'src/main.py',                          # Replace with your main script name
        '--onedir',                             # Creates a directory containing the executable
        '--name=HWMom',                         # Replace with your app name
        '--noconsole',                          # Remove if you want to show console
        '--add-data=src/settings/*;settings/',  # Include all files from config folder
        '--add-data=src/assets/*;assets/',      # Include all files from assets folder
        '--clean',                              # Clean cache before building
        '--noupx',                              # Disable UPX compression; may improve stability
        '--noconfirm',
        
        # Add all necessary PyQt6 modules
        '--hidden-import=PyQt6',
        '--hidden-import=PyQt6.QtWidgets',
        '--hidden-import=PyQt6.QtGui',
        '--hidden-import=PyQt6.QtCore',
        #'--hidden-import=PyQt6.sip',

        # Socket and multiprocessing dependencies
        '--hidden-import=_socket',
        '--hidden-import=socket',
        '--hidden-import=multiprocessing',
        '--hidden-import=multiprocessing.pool',
        '--hidden-import=multiprocessing.synchronize',
        '--hidden-import=multiprocessing.heap',
        
        # Add PyQt6 plugins
        '--collect-all=PyQt6',
        # '--collect-data=PyQt6',
        # '--collect-submodules=PyQt6',
        # '--collect-binaries=PyQt6',        
    ])

if __name__ == "__main__":
    build_exe()