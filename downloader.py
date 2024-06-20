import requests
import os.path

CHUNK_SIZE = 10 * 1024 # 10 MB is default
backgrounds = {}

def dl_file(dl_info):
    try:
        headers = _continue_download(dl_info['filename'])
        response = requests.get(dl_info['src'], stream=True, headers=headers)
        FULL_SIZE = int(response.headers['Content-Length'])
    except:
        print('Could not get content length. File may already be downloaded.')
        return
    
    downloaded_bytes = 0
    with open(dl_info['filename'], mode='ab+') as f:
        backgrounds[dl_info['id']] = [downloaded_bytes, FULL_SIZE] # Add the current download to background: (bytes, full size)

        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:
                downloaded_bytes += len(chunk)
                f.write(chunk)
                backgrounds[dl_info['id']] = [downloaded_bytes, FULL_SIZE] # Update background task

    print(dl_info['filename'], 'downloaded!')
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