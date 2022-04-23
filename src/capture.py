import requests
from json import dumps
from random import randint


class Client:
    def __init__(
        self,
        token: str = None,
        session_id: int = str(
            randint(
            1,
            9999))):
        self.api = "https://capture.chat/api"
        self.headers = {
            "user-agent": "15 Android/56 ru-RU",
            "session-id": session_id
        }
        self.user_id = None
        if token:
            self.login_with_token(token)

    def login_with_google(self, google_id_token: str):
        data = {"id_token": google_id_token}
        return requests.post(
            f"{self.api}/auth/google",
            data=data,
            headers=self.headers).json()

    def login_with_token(self, token: str):
        self.token = token
        self.headers["X-Token"] = self.token
        profile = self.get_account_info()["user"]
        self.user_id = profile["user_id"]
        return profile

    def register(self, username: str):
        data = {"username": username}
        return requests.post(
            f"{self.api}/auth/username",
            data=data,
            headers=self.headers).json()

    def register_with_google(self, google_id_token: str, username: str):
        data = {"id_token": google_id_token, "username": username}
        return requests.post(
            f"{self.api}/auth/google/signup",
            data=data,
            headers=self.headers).json()

    def get_notifications(self):
        return requests.get(
            f"{self.api}/notification",
            headers=self.headers).json()

    def get_chat_users(self, chat_id: int, count: int = 10):
        return requests.get(
            f"{self.api}/topic/{chat_id}/member?count={count}",
            headers=self.headers).json()

    def get_user_chats(self, user_id: str, count: int = 10):
        return requests.get(
            f"{self.api}/user/{user_id}/topic?count={count}",
            headers=self.headers).json()

    def get_discover_items(self, count: int = 10):
        return requests.get(
            f"{self.api}/topic/discover?count={count}",
            headers=self.headers).json()

    def get_discover_onboarding(self):
        return requests.get(
            f"{self.api}/discover/onboarding",
            headers=self.headers).json()

    def get_discover_communities(self):
        return requests.get(
            f"{self.api}/community/discover",
            headers=self.headers).json()

    def get_chats(self, count: int = 10):
        return requests.get(
            f"{self.api}/topic?count={count}",
            headers=self.headers).json()

    def get_direct_messages_requests(self):
        return requests.get(
            f"{self.api}/dm/request",
            headers=self.headers).json()

    def get_all_chats(self):
        return requests.get(
            f"{self.api}/topic/all",
            headers=self.headers).json()

    def get_chat(self, chat_id: int):
        return requests.get(
            f"{self.api}/topic/{chat_id}",
            headers=self.headers).json()

    def get_chat_by_link(self, chat_link: str):
        return requests.get(
            f"{self.api}/link/{chat_link}",
            headers=self.headers).json()

    def get_user(self, user_id: str):
        return requests.get(
            f"{self.api}/user/{user_id}",
            headers=self.headers).json()

    def get_trending_gifs(self):
        return requests.get(
            f"{self.api}/gifs/trending",
            headers=self.headers).json()

    def get_chat_photos(
            self,
            chat_id: int,
            count: str = 50,
            reverse: bool = True):
        return requests.get(
            f"{self.api}/topic/{chat_id}/photo?count={count}&reverse={reverse}",
            headers=self.headers).json()

    def get_chat_messages(self, chat_id: int, count: int = 10):
        return requests.get(
            f"{self.api}/topic/{chat_id}/message?count={count}",
            headers=self.headers).json()

    def search_mention_users(self, chat_id: int, prefix: str = ""):
        return requests.get(
            f"{self.api}/topic/{chat_id}/mention/suggest?prefix={prefix}",
            headers=self.headers).json()

    def send_message(
            self,
            chat_id: int,
            text: str,
            quote_message_id: str = None,
            gif_id: str = None,
            gif_provider: str = None):
        data = {"text": text}
        if quote_message_id:
            data["quote_message_id"] = quote_message_id
        elif gif_id:
            data["gif_id"] = gif_id
        elif gif_provider:
            data["gif_provider"] = gif_provider
        data = dumps(data)
        return requests.post(
            f"{self.api}/topic/{chat_id}/message",
            data=data,
            headers=self.headers).json()

    def create_chat(
            self,
            content: str,
            name: str,
            is_channel: bool = False,
            is_private: bool = False):
        data = dumps({
            "channel": is_channel,
            "private": is_private,
            "name": name,
            "content": content
        })
        return requests.post(
            f"{self.api}/topic",
            data=data,
            headers=self.headers).json()

    def edit_chat(
            self,
            chat_id: int,
            description: str = None,
            name: str = None,
            category_id: int = 1):
        data = {
            "category_id": category_id,
            "name": name,
            "discription": description
        }
        data = dumps(data)
        return requests.patch(
            f"{self.api}/topicId/{chat_id}",
            data=data,
            headers=self.headers).json()

    def delete_message(self, chat_id: int, message_id: str):
        return requests.delete(
            f"{self.api}/topic/{chat_id}/message{message_id}",
            headers=self.headers).json()

    def join_chat(self, chat_id: int):
        return requests.post(
            f"{self.api}/topic/{chat_id}/subscription",
            headers=self.headers).json()

    def leave_chat(self, chat_id: int):
        return requests.delete(
            f"{self.api}/topic/{chat_id}/subscription",
            headers=self.headers).json()

    def edit_profile(
            self,
            name: str = None,
            bio: str = None,
            location: str = None,
            status: bool = True):
        data = dumps({
            "bio": bio,
            "location": location,
            "name": name,
            "online": status
        })
        return requests.patch(
            f"{self.api}/user/me",
            data=data,
            headers=self.headers).json()

    def set_chat_user_role(self, chat_id: int, user_id: str, role: str):
        data = {"role": role}
        return requests.patch(
            f"{self.api}/topic/{chat_id}/member/{user_id}",
            data=data,
            headers=self.headers).json()

    def edit_message(self, chat_id: int, message_id: str, text: str):
        data = {"text": text}
        return requests.patch(
            f"{self.api}/topic/{chat_id}/message/{message_id}",
            data=data,
            headers=self.headers).json()

    def ban(self, chat_id: int, user_id: str):
        return requests.post(
            f"{self.api}/topic/{chat_id}/ban{user_id}",
            headers=self.headers).json()

    def report_user(self, user_id: str, reason: str, comment: str = None):
        data = {"reason": reason}
        if comment:
            data["comment"] = comment
        return requests.post(
            f"{self.api}/user/{user_id}/report",
            data=data,
            headers=self.headers).json()

    def report_message(
            self,
            chat_id: int,
            message_id: str,
            reason: str,
            comment: str = None):
        data = {"reason": reason}
        if comment:
            data["comment"] = comment
        return requests.post(
            f"{self.api}/topic/{chat_id}/message/{message_id}",
            data=data,
            headers=self.headers).json()

    def report_chat(self, chat_id: int, reason: str, comment: str = None):
        data = {"reason": reason}
        if comment:
            data["comment"] = comment
        return requests.post(
            f"{self.api}/topic/{chat_id}/report",
            data=data,
            headers=self.headers).json()

    def unban(self, chat_id: int, user_id: str):
        return requests.delete(
            f"{self.api}/topic/{chat_id}/ban/{user_id}",
            headers=self.headers).json()

    def send_direct_message_request(self, user_id: str):
        return requests.post(
            f"{self.api}/dm/user/{user_id}",
            headers=self.headers).json()

    def follow_chat(self, chat_id: int):
        return requests.post(
            f"{self.api}/topic/{chat_id}/follow",
            headers=self.headers).json()

    def unfollow_chat(self, chat_id: int):
        return requests.delete(
            f"{self.api}/topic/{chat_id}/unfollow",
            headers=self.headers).json()

    def search_chats(self, query: str):
        return requests.get(
            f"{self.api}/topic/search/{query}",
            headers=self.headers).json()

    def search_gifs(self, query: str):
        return requests.get(
            f"{self.api}/gifs/search/{query}",
            headers=self.headers).json()

    def unread(self, chat_id: int):
        return requests.delete(
            f"{self.api}/topic/{chat_id}/unread",
            headers=self.headers).json()

    def post_typing(self, chat_id: int, status: str = "text"):
        return requests.post(
            f"{self.api}/topic/{chat_id}/typing?status={status}",
            headers=self.headers).json()

    def get_config(self):
        return requests.get(f"{self.api}/config", headers=self.headers).json()

    def get_account_info(self):
        return requests.get(f"{self.api}/user/me", headers=self.headers).json()

    def get_ml_config(self):
        return requests.get(
            f"{self.api}/ml/config",
            headers=self.headers).json()

    def get_joined_communities(self):
        return requests.get(
            f"{self.api}/community",
            headers=self.headers).json()

    def get_stickers(self):
        return requests.get(
            f"{self.api}/stickers",
            headers=self.headers).json()

    def get_trending_gifs(self):
        return requests.get(
            f"{self.api}/gifs/trending",
            headers=self.headers).json()

    def get_user_badges(self, user_id: str):
        return requests.get(
            f"{self.api}/user/{user_id}/badges",
            headers=self.headers).json()

    def get_user_by_username(self, username: str):
        return requests.get(
            f"{self.api}/user/screen_name/{username}",
            headers=self.headers).json()

    def update_chat_settings(
            self,
            chat_id: int,
            sound: bool = False,
            mute: bool = False):
        data = {"sound": sound, "mute": mute}
        return requests.patch(
            f"{self.api}/topic/{chat_id}/settings",
            data=data,
            headers=self.headers).json()

    def get_community(self, com_id: int):
        return requests.get(
            f"{self.api}/community/{com_id}",
            headers=self.headers).json()

    def get_community_chats(self, com_id: int):
        return requests.get(
            f"{self.api}/community/{com_id}/topic",
            headers=self.headers).json()

    def get_link_preview(self, url: str):
        return requests.get(
            f"{self.api}/link/preview?url={url}",
            headers=self.headers).json()

    def get_relevant_chat_photos(self, chat_id: int, count: int = 10):
        return requests.get(
            f"{self.api}/topic/{chat_id}/ml/photo?count={count}",
            headers=self.headers).json()

    def remove_chat_from_community(self, com_id: int, chat_id: int):
        return requests.delete(
            f"{self.api}/community/{com_id}/topic/{chat_id}",
            headers=self.headers).json()

    def follow_community(self, com_id: int):
        return requests.post(
            f"{self.api}/community/{com_id}/member",
            headers=self.headers).json()

    def unfollow_community(self, com_id: int):
        return requests.delete(
            f"{self.api}/community/{com_id}/member",
            headers=self.headers).json()
