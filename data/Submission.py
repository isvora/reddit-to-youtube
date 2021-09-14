class Submission:

    def __init__(self, author_name, is_video, short_link, title):
        self.id = author_name
        self.is_video = is_video
        self.link = short_link
        self.title = title
