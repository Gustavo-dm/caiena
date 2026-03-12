from github import Github

class GistService:

    def __init__(self, token: str):
        self.github = Github(token)

    def comment_on_gist(self, gist_id: str, message: str):

        gist = self.github.get_gist(gist_id)

        gist.create_comment(message)