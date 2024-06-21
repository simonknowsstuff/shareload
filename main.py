from flask import Flask, request, jsonify
import time
import downloader
import threading

app = Flask(__name__)

@app.route('/receive_download', methods=['POST'])
def receive_download():
    if request.method == 'POST':
        dl_info = request.get_json()
        dl_link = dl_info['src']
        
        CURRENT_TIME = time.strftime('%H:%M:%S - %d-%m-%Y', time.localtime())
        if dl_link:
            print(f'Download link received: {dl_link}')
            with open('history.txt', 'a') as f:
                f.write(f'[{CURRENT_TIME}]\n')
                f.write(f'{request.remote_addr}: {str(dl_info)}\n')
            
            # Create a download thread:
            dl_thread = threading.Thread(target=downloader.dl_file, args=(dl_info,))
            dl_thread.start()
            
            return 'Link received! Starting download.', 200
        else:
            return 'Invalid link!', 400
    
@app.route('/download_status', methods=['GET'])
def download_status():
    if request.method == 'GET':
        dl_id = int(request.args['id'])
        if dl_id in downloader.backgrounds:
            info = downloader.backgrounds[dl_id]
            
            resp = {'downloaded': info[0], 'fullSize': info[1]}
            return jsonify(resp), 200
        return 'Item not found!', 400

if __name__ == '__main__':
    app.run(port=6002, debug=True)