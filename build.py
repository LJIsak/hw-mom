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
        '--strip',                              # Strip debug symbols from compiled binaries
        '--noupx',                              # Disable UPX compression; may improve stability
        '--noconfirm',
        
        # Add hidden imports for PyQt6 modules:
        '--hidden-import=PyQt6.QtCore',
        '--hidden-import=PyQt6.QtWidgets',
        '--hidden-import=PyQt6.QtGui',
    ])

if __name__ == "__main__":
    build_exe()