import os
import yt_dlp
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn

console = Console(color_system="auto")

class UnableToProcess(Exception):
    pass

class CustomProgressbar:
    def __init__(self, progress, task_id):
        self.progress = progress
        self.task_id = task_id
        self.total_set = False

    def sizeconv(self, sizebytes):
        if sizebytes is None:
            return "?"

        value = float(sizebytes)
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if value < 1024:
                return f"{value:.2f} {unit}"
            value /= 1024

        return f"{value:.2f} PB"

    def __call__(self, d):
        if d["status"] == "downloading":
            downloaded = d.get("downloaded_bytes", 0)
            total = d.get("total_bytes") or d.get("total_bytes_estimate")

            ##Updating progressbar Manually as Rich can't update progress manually
            if total and not self.total_set:
                self.progress.update(self.task_id, total=total)
                self.total_set = True

            self.progress.update(
                self.task_id,
                completed=downloaded,
                description=f"{self.sizeconv(downloaded)} / {self.sizeconv(total)}"
            )
        elif d["status"] == "finished":
            self.progress.update(
                self.task_id,
                completed=self.progress.tasks[self.task_id].total,
                description="[yellow]Download complete, processing...[/]"
            )
        elif d["status"] == "postprocessor":
            self.progress.update(self.task_id, description="[green]Processing... (FFmpeg)")
class ProgressManager:
    def __init__(self):
        self.progress = Progress(
            TextColumn("[bold blue]{task.description}[/]"),
            BarColumn(),
            TextColumn("{task.percentage:>3.0f}%"),
            TimeRemainingColumn()
        )
    def create_hook(self):
        task = self.progress.add_task("Starting...", total=None)
        return self.progress, CustomProgressbar(self.progress, task)


class Downloader:
    def VideoDownload(self, link, address="Downloadstesting"):
        self.link = link
        self.address = address

        pm = ProgressManager()
        progress, hook = pm.create_hook()
        ydl_opts = {
            'outtmpl': f'{self.address}/%(title)s.%(ext)s',
            'quiet': True,
            'noplaylist': True,
            'progress': True,
            "no_warnings": True,
            "progress_hooks": [hook],
            'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
        }
        try:
            with progress:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([self.link])
        except UnableToProcess:
            console.print("Unable to process your request at this time. Please try again later.", style="red",justify="center")
        else:
            console.print("Video Downloaded Successfully.", style="green", justify="center")

    def AudioDownload(self, link, address="Downloadtesting"):
        self.link = link
        self.address = address
        pm = ProgressManager()
        progress, hook = pm.create_hook()

        ydl_opts = {
            "quiet": True,
            "noplaylist": True,
            "progress": True,
            "no_warnings": True,
            "format": "bestaudio/best",
            "outtmpl": f"{self.address}/%(title)s.%(ext)s",
            "progress_hooks": [hook],
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "320",
                },
            ],
        }
        try:
            with progress:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([self.link])
        except UnableToProcess:
            console.print("Unable to process your request at this time. Please try again later.", style="red",justify="center")
        else:
            console.print("Audio Downloaded Successfully.", style="green", justify="center")


def main():
    home = os.environ.get("USERPROFILE")
    default_path = os.path.join(home, "Downloads")
    while True:
        download = Downloader()
        console.print(Panel("[purple]Welcome to Youtube Video/Audio Downloader[/][link = https://github.com/Praneeth-Gandodi/Y2Api turquoise2 ] -> [underline]Repo[/underline] <-[/]"), justify="center")
        print("\n")
        console.print("Select your options from below :", style="steel_blue1")
        print()
        console.print("[royal_blue1]1.[/royal_blue1] Download Video.", style="grey70")
        console.print("[royal_blue1]2.[/royal_blue1] Download Audio.", style="grey70")
        console.print("[royal_blue1]3.[/royal_blue1] Download Playlist.", style="grey70")
        console.print("[royal_blue1]4.[/royal_blue1] Get information from the provided link.", style="grey70")
        print()
        value = console.input("[light_sky_blue3]Select an option from those [i]listed above[/i] [Example : 1] [light_sky_blue3]: ")

        if(value == "1"):
            console.print("[yellow]Note:[/][yellow2] For video downloads, it directly downloads the highest available quality.[/]")
            link = console.input("[red]Please enter the URL: [/]")
            path = console.input("[light_sky_blue3]Enter the path to save the file [[yellow]leave empty for default Downloads folder[/yellow]]: [/]")
            if not path.strip():
                path = default_path

            download.VideoDownload(link, path)
        elif(value == "2"):
            link = console.input("[red]Please enter the URL: [/]")
            path = console.input("[light_sky_blue3]Enter the path to save the file [[yellow]leave empty for default Downloads folder[/yellow]]: [/]")
            if not path.strip():
                path = default_path
            download.AudioDownload(link, path)
        elif(value == "3"):
            console.print("[red] The feature 'Download Playlist' is still Under Construction.[/]")
        else:
            console.print("These features coming soon")



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as e:
        print()
        console.print("Thanks for using the downloader.", style="red", justify="center")
    except Exception as e:
        console.print_exception(show_locals=True)
        console.print("An unexpected error occurred.", e, style="red", justify="center")

