from unittest.mock import patch, MagicMock
import pytest
from github import GithubException

from app.services.gist import GistService


class TestGistService:
    """Test suite for GistService"""

    @patch("app.services.gist.Github")
    def test_gist_service_initialization(self, mock_github):
        """Test GistService initialization with token"""
        token = "test_token_123"
        service = GistService(token)
        
        assert service.github is not None

    @patch("app.services.gist.Github")
    def test_comment_on_gist_success(self, mock_github):
        """Test successful comment on gist"""
        # Mock the GitHub gist object
        mock_gist = MagicMock()
        mock_github_instance = MagicMock()
        mock_github_instance.get_gist.return_value = mock_gist
        mock_github.return_value = mock_github_instance

        service = GistService("test_token")
        service.comment_on_gist("gist_123", "Test comment")

        # Verify get_gist was called with correct ID
        mock_github_instance.get_gist.assert_called_once_with("gist_123")
        
        # Verify create_comment was called with correct text
        mock_gist.create_comment.assert_called_once_with("Test comment")

    @patch("app.services.gist.Github")
    def test_comment_on_gist_not_found(self, mock_github):
        """Test comment on gist when gist not found"""
        mock_github_instance = MagicMock()
        mock_github_instance.get_gist.side_effect = GithubException(404, "Not Found")
        mock_github.return_value = mock_github_instance

        service = GistService("test_token")
        
        with pytest.raises(GithubException):
            service.comment_on_gist("invalid_gist", "Test comment")

    @patch("app.services.gist.Github")
    def test_comment_on_gist_authentication_error(self, mock_github):
        """Test comment on gist with authentication error"""
        mock_github_instance = MagicMock()
        mock_github_instance.get_gist.side_effect = GithubException(401, "Unauthorized")
        mock_github.return_value = mock_github_instance

        service = GistService("invalid_token")
        
        with pytest.raises(GithubException):
            service.comment_on_gist("gist_123", "Test comment")

    @patch("app.services.gist.Github")
    def test_comment_on_gist_with_special_characters(self, mock_github):
        """Test comment with special characters and formatting"""
        mock_gist = MagicMock()
        mock_github_instance = MagicMock()
        mock_github_instance.get_gist.return_value = mock_gist
        mock_github.return_value = mock_github_instance

        service = GistService("test_token")
        special_comment = "🌡️ Current: 25°C, Condition: Sunny ☀️\n**Bold text**"
        service.comment_on_gist("gist_123", special_comment)

        mock_gist.create_comment.assert_called_once_with(special_comment)
