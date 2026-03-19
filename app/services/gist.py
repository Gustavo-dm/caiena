from github import Github, Auth
from typing import Optional


class GistService:
    """
    Serviço para integração com GitHub Gists.

    Permite publicar comentários em gists existentes.

    Attributes:
        github (Github): Cliente PyGithub autenticado
    """

    def __init__(self, token: str):
        """
        Inicializar serviço com token de autenticação.

        Args:
            token (str): GitHub personal access token com permissão 'gist'

        Raises:
            ValueError: Se token for inválido ou vazio
        """
        self.github = Github(auth=Auth.Token(token))

    def comment_on_gist(self, gist_id: str, comment: str) -> None:
        """
        Publicar um comentário em um gist existente.

        Args:
            gist_id (str): ID do gist (pode ser encontrado na URL)
            comment (str): Texto do comentário a ser publicado

        Returns:
            None

        Raises:
            GithubException: Se o gist não existe (404) ou acesso negado (401)

        Exemplo:
            >>> service = GistService("your_github_token")
            >>> service.comment_on_gist(
            ...     "abc123def456",
            ...     "34°C e nublado em São Paulo em 19/03..."
            ... )
        """
        gist = self.github.get_gist(gist_id)
        gist.create_comment(comment)