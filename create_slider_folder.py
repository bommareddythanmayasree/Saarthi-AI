#!/usr/bin/env python3
"""
Script to create the slider folder structure and download placeholder images.
Run this script to quickly set up the background slider with test images.
"""

import os
import urllib.request
from pathlib import Path

def create_slider_folder():
    """Create the slider folder if it doesn't exist."""
    slider_path = Path("static/images/slider")
    slider_path.mkdir(parents=True, exist_ok=True)
    print(f"✅ Created folder: {slider_path}")
    return slider_path

def download_placeholder_images(slider_path):
    """Download placeholder images from Unsplash."""
    # Unsplash Source API for random education-related images
    topics = [
        "students,education",
        "graduation,university",
        "campus,learning",
        "internship,career",
        "scholarship,success"
    ]
    
    print("\n📥 Downloading placeholder images...")
    print("(This may take a moment depending on your internet connection)\n")
    
    for i, topic in enumerate(topics, 1):
        image_path = slider_path / f"slide{i}.jpg"
        
        # Skip if image already exists
        if image_path.exists():
            print(f"⏭️  Slide {i} already exists, skipping...")
            continue
        
        try:
            # Unsplash Source URL for random images
            url = f"https://source.unsplash.com/1920x1080/?{topic}"
            
            print(f"⬇️  Downloading slide{i}.jpg ({topic})...")
            urllib.request.urlretrieve(url, image_path)
            print(f"✅ Downloaded: {image_path}")
            
        except Exception as e:
            print(f"❌ Error downloading slide{i}.jpg: {e}")
            print(f"   You can manually add this image later.")
    
    print("\n✨ Setup complete!")

def create_readme(slider_path):
    """Create a README in the slider folder."""
    readme_path = slider_path / "README.txt"
    
    readme_content = """Background Slider Images
========================

This folder contains the background images for the landing page slider.

Required Files:
- slide1.jpg
- slide2.jpg
- slide3.jpg
- slide4.jpg
- slide5.jpg

Image Specifications:
- Dimensions: 1920x1080px (recommended)
- Format: JPG, PNG, or WebP
- File Size: < 500KB per image
- Quality: Professional, high-resolution photos

To Replace Images:
1. Add your images to this folder
2. Name them exactly: slide1.jpg, slide2.jpg, etc.
3. Ensure they meet the specifications above
4. Refresh your browser to see changes

For more information, see:
- SLIDER_IMAGES_SETUP.md
- BACKGROUND_SLIDER_IMPLEMENTATION.md
"""
    
    with open(readme_path, 'w') as f:
        f.write(readme_content)
    
    print(f"📄 Created README: {readme_path}")

def main():
    """Main function to set up the slider."""
    print("🎨 Background Slider Setup")
    print("=" * 50)
    
    # Create folder
    slider_path = create_slider_folder()
    
    # Ask user if they want to download placeholder images
    print("\n📸 Would you like to download placeholder images from Unsplash?")
    print("   (You can replace these with your own images later)")
    response = input("   Download placeholders? (y/n): ").strip().lower()
    
    if response == 'y':
        download_placeholder_images(slider_path)
    else:
        print("\n⏭️  Skipping placeholder download.")
        print("   Add your own images to: static/images/slider/")
        print("   Name them: slide1.jpg, slide2.jpg, slide3.jpg, slide4.jpg, slide5.jpg")
    
    # Create README
    create_readme(slider_path)
    
    print("\n" + "=" * 50)
    print("🎉 Setup Complete!")
    print("\nNext Steps:")
    print("1. Start your Flask server: python app.py")
    print("2. Visit: http://127.0.0.1:5000/")
    print("3. See the slider in action!")
    print("\nTo customize:")
    print("- Replace images in: static/images/slider/")
    print("- See documentation: SLIDER_IMAGES_SETUP.md")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup cancelled by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Please check the error and try again.")
