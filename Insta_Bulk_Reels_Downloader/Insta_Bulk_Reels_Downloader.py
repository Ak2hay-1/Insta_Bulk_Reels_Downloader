import instaloader
import os

# Initialize instaloader with custom settings
loader = instaloader.Instaloader(
    download_videos=True,  # Ensure video files are downloaded
    download_video_thumbnails=False,  # Disable video thumbnails
    download_comments=False,  # Disable downloading comments metadata
    post_metadata_txt_pattern='',  # Disable metadata text files
    save_metadata=False  # Do not save JSON metadata
)

# Prompt the user to input the Instagram profile username
profile_name = input("Enter the Instagram username of the account you want to download reels from: ")

# Set the base directory to the default Downloads folder
base_directory = os.path.join(os.path.expanduser("~"), "Downloads")

# Create a folder in the default Downloads directory with the username
profile_directory = os.path.join(base_directory, profile_name)

# Create the directory if it doesn't exist
os.makedirs(profile_directory, exist_ok=True)

# Download only video posts (reels) from the profile
profile = instaloader.Profile.from_username(loader.context, profile_name)

for post in profile.get_posts():
    if post.is_video:  # Ensure it's a video (including Reels)
        print(f"Downloading reel: {post.url}")

        # Download post directly to the profile directory
        loader.download_post(post, target=profile_name)  # Save directly to the username folder

# Move the downloaded files to the correct folder
for file in os.listdir(os.getcwd()):
    if file.startswith(profile_name) and file.endswith('.mp4'):
        os.rename(file, os.path.join(profile_directory, file))

# Remove any files that are not .mp4 (in case they were downloaded by mistake)
for file in os.listdir(profile_directory):
    try:
        if not file.endswith(".mp4"):
            print(f"Removing non-video file: {file}")
            os.remove(os.path.join(profile_directory, file))
    except Exception as e:
        print(f"Error while deleting file {file}: {e}")

print(f"All reels have been downloaded to {profile_directory}.")
