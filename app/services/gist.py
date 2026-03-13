from github import Github, Auth

class GistService:

    def __init__(self, token):
        self.github = Github(auth=Auth.Token(token))

    def comment_on_gist(self, gist_id, comment):
        gist = self.github.get_gist(gist_id)
        gist.create_comment(comment)