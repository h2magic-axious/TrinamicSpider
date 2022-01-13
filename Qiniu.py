import qiniu

from Downloader import DownloadMemory


class CONST:
    AK = 'DmTlI2aO1kvctWx1Nl93LrLsGVeJt6s5u2AzzXsO'
    SK = '6nqczhLsD_0kf6jrNYeoIf9z5euCcfNCaLsikPGG'
    BUCKET_NAME = 'tmc-item'


class QiNiu:
    def __init__(self):
        self.__session = qiniu.Auth(CONST.AK, CONST.SK)
        self.bucket = CONST.BUCKET_NAME

    def token(self, key, lifetime=3600):
        return self.__session.upload_token(self.bucket, key, lifetime)

    def upload(self, key, file_path):
        print("Upload: ", file_path)
        qiniu.put_file(self.token(key), key, file_path)


def main():
    dm = DownloadMemory()
    qu = QiNiu()

    for file in dm.download_dir.iterdir():
        qu.upload(file.name, file)


if __name__ == '__main__':
    main()
