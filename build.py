import os
import subprocess
from PIL import Image

def convert_png_to_ico():
    """Convert PNG icon to ICO format"""
    if not os.path.exists('src/assets/icon.ico'):
        img = Image.open('src/assets/icon.png')
        img.save('src/assets/icon.ico', format='ICO')

def build():
    """Build the executable"""
    # Convert icon if needed
    convert_png_to_ico()
    
    # Run PyInstaller
    subprocess.run(['pyinstaller', 'hw_mom.spec', '--clean'])

if __name__ == '__main__':
    build() 