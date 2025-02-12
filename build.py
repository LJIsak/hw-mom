import PyInstaller.__main__

def build_exe():
    PyInstaller.__main__.run([
        'src/main.py',                          # Replace with your main script name
        '--name=HWMom',                         # Replace with your app name
        '--add-data=src/settings/*;settings/',  # Include all files from config folder
        '--add-data=src/assets/*;assets/',      # Include all files from assets folder
        '--onedir',                             # Creates a directory containing the executable
        '--noconsole',                          # Remove if you want to show console
        '--clean',                              # Clean cache before building
        '--noupx',                              # Disable UPX compression; may improve stability
        '--noconfirm',
        
        # Core PyQt6 requirements
        '--hidden-import=PyQt6.QtWidgets',
        '--hidden-import=PyQt6.QtGui',
        '--hidden-import=PyQt6.QtCore',
        '--collect-all=PyQt6',
        
        # Your only other core dependency
        '--hidden-import=psutil',

        # Exclude build-only dependencies
        '--exclude-module=PyInstaller',
        '--exclude-module=pip',
        '--exclude-module=setuptools',
        '--exclude-module=ipykernel',
        '--exclude-module=jupyter',
        '--exclude-module=ipython',
    ])

if __name__ == "__main__":
    build_exe()