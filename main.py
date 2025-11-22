import yt_dlp
#class key
class ytd:
    def __init__(self, link):
        self.link = link

    def values(self):
        ydl_opts = {
            'quiet': True,
            'download': False
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(self.link, download = False)
            self.title = info['title']
            self.formats = info['formats']
            self.duration = info['duration']


    def getinfo(self):
        ydl_opts = {
            'quiet': True,
            'download': False
            }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(self.link)
            print(info['title'])
            print(info['resolution'])


    def VidDown(self):
        ydl_opts = {
            'noplaylist': True,
            'format': 'bestvideo/best',
            'outtmpl': r'C:\Users\prane\Projects\yt-dlp api\Downloads\%(title)s - DOWNLOADED.%(ext)s',
            'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
            'merge_output_format': 'mp4'
            }],
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.link])
        except Exception as e:
            print("Error")


    def audiodownload(self):
        ydl_opts = {
            'noplaylist': True,
            'format': 'bestaudio/best',
            'outtmpl': r'C:\Users\prane\Projects\yt-dlp api\Downloads/%(title)s - DOWNLOADED.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydll:
                ydll.download([self.link])
        except Exception as e:
            print("Error Occured",e )


def main():
    while True:
        print("Select download type:")
        print(" 1. Video")
        print(" 2. Audio")
        print(" 3. Info")

        try:
            option = int(input("\nEnter choice (1 or 2 or 3): "))
        except ValueError:
            print("Invalid input! Please enter a number.")
            return

        link = input("Enter URL: ").strip()

        downloader = ytd(link)
        downloader.values()

        for f in downloader.formats:
            if f.get("resolution"):
                print(f["resolution"])

        if option == 1:
            downloader.VidDown()
        elif option == 2:
            downloader.audiodownload()
        elif option == 3:
            downloader.getinfo()
        else:
            print("Invalid option! Please enter 1 or 2.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Error occurred in the main function")