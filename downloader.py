import requests
import os

CHUNK_SIZE = 10 * 1024 # 10 MB is default
CURRENT_DIR = os.path.dirname(__file__)
backgrounds = {}

def dl_file(dl_info):
    try:
        headers = _continue_download(dl_info['filename'])
        response = requests.get(dl_info['src'], stream=True, headers=headers)
        FULL_SIZE = int(response.headers['Content-Length'])
    except:
        print('Could not get content length. File may already be downloaded.')
        return
    
    downloads_folder = os.path.join(os.getenv('USERPROFILE', os.getenv('HOME')), 'Downloads')
    try:
        os.makedirs(downloads_folder, exist_ok=True)  # Create folder, ignore if exists
    except OSError as e:
        print(f"Error creating Downloads folder: {e}")
    final_name = f'{downloads_folder}/{dl_info['filename']}'

    downloaded_bytes = 0
    with open(final_name, mode='ab+') as f:
        backgrounds[dl_info['id']] = [downloaded_bytes, FULL_SIZE] # Add the current download to background: (bytes, full size)

        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:
                downloaded_bytes += len(chunk)
                f.write(chunk)
                backgrounds[dl_info['id']] = [downloaded_bytes, FULL_SIZE] # Update background task

    print(dl_info['filename'], 'saved to', final_name)
    return

def _continue_download(filename):
    if os.path.isfile(filename):
        data = open(filename, 'rb')
        bytes = len(data.read())
        if bytes > 0:
            print('Resuming file download...')
            # Continue from remaining bytes
            return {'Range': f'bytes={bytes}-'}
    return {}