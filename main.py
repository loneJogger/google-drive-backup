import file_handler
import google_drive

if __name__ == '__main__':
    config = file_handler.readConfig()
    if not config:
        file_handler.log('ERROR', 'no config file discovered.')
        print('config file created at config.ini. please add a folder to backup.')
        exit()
    if config['dir_path'] is 'NO_PATH':
        file_handler.log('ERROR', 'no dir_path value in config file. please add a folder to backup.')
        print('no dir_path value in config file. please add a directory to backup.')
        exit()
    files = file_handler.mapDirectory(config['dir_path'])
    for file in files:
        data = file_handler.getMetadata(file['path'], file['name'])
        file['Date modified'] = data['Date modified']
    changes = file_handler.checkHistory(files)
    number_uploaded = google_drive.upload(changes, config['dir_path'])
    file_handler.log('FINSHED', 'process finished with {} files uploaded.'.format(number_uploaded))
    print('process finished with {} files uploaded.'.format(number_uploaded))
