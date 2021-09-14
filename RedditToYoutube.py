import praw, os, argparse, json

from redvid import Downloader
from constants.Credentials import API
from data import Submission as sub
from data import Video as vid
from youtube_uploader_selenium import YouTubeUploader
from typing import Optional

SUBMISSIONS = []

# Set a few rules for the submission being valid
def submission_is_valid(submission):
    # If the user deleted its post skip it
    if submission.author is None:
        return False
    return True

# Gather the submissions in a subreddit
def gather_submissions(subreddit, nr_of_submissions):
    # Parse the specified number of submissions from the subreddit in the hot category
    for submission in subreddit.hot(limit=nr_of_submissions):
        if submission_is_valid(submission):
            # Create a Submission object and add it to the SUBMISSIONS list
            SUBMISSIONS.append(sub.Submission(author_name=submission.author.name,
                                              is_video=submission.is_video,
                                              short_link=submission.url,
                                              title=submission.title))

class RedditToYoutube:

    @staticmethod
    def main(subreddit_name: str, nr_of_submissions: Optional[int] = None):
        # Obtain reddit object
        reddit = praw.Reddit(
            client_id=API["client_id"],
            client_secret=API["client_secret"],
            user_agent=API["user_agent"])

        # Create downloader object
        downloder = Downloader(max_q=True)

        # Create a subreddit object
        subreddit = reddit.subreddit(subreddit_name)

        # Start gathering submissions
        print("Gathering content")
        number = nr_of_submissions if nr_of_submissions else 25
        gather_submissions(subreddit, int(number))

        # Loop through submissions and upload them to youtube
        print("Processing content")
        for submission in SUBMISSIONS:
            if submission.is_video:
                # Download video
                downloder.url = submission.link
                downloder.download()

                # Create video object
                video_description = "Original link: " + submission.link + "\nCredit to: " + submission.id
                video = vid.Video(title=submission.title, description=video_description)

                # Create metadata json file for the video
                with open('metadata.json', 'w') as f:
                    json.dump(video.__dict__, f)

                # Upload video to reddit
                uploader = YouTubeUploader(os.path.basename(downloder.file_name), "metadata.json")
                was_video_uploaded, video_id = uploader.upload()
                assert was_video_uploaded

                # Remove video and metadata from disk
                os.remove(downloder.file_name)
                os.remove('metadata.json')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--subreddit",
                        help='Subreddit to be scraped',
                        required=True)
    parser.add_argument("-nos",
                        "--submissions",
                        help='Number of submissions to check for', )
    args = parser.parse_args()
    RedditToYoutube.main(args.subreddit, args.submissions)
