import requests
from random import randint


class Capture:
	def __init__(
			self,
			session_id: int = str(randint(1, 9999))) -> None:
		self.api = "https://capture.chat/api"
		self.headers = {
			"user-agent": "15 Android/56 ru-RU",
			"session-id": session_id
		}
		self.x_token = None
		self.user_id = None

	def login_with_google(self, google_id_token: str) -> dict:
		data = {
			"id_token": google_id_token
		}
		return requests.post(
			f"{self.api}/auth/google",
			data=data,
			headers=self.headers).json()

	def login_with_x_token(self, x_token: str) -> dict:
		self.x_token = x_token
		self.headers["X-Token"] = self.x_token
		response = self.get_account_info()
		if "user_id" in response["user"]:
			self.user_id = response["user"]["user_id"]
		return response

	def register(self, username: str) -> dict:
		data = {
			"username": username
		}
		return requests.post(
			f"{self.api}/auth/username",
			data=data,
			headers=self.headers).json()

	def register_with_google(
			self,
			google_id_token: str,
			username: str) -> dict:
		data = {
			"id_token": google_id_token,
			"username": username
		}
		return requests.post(
			f"{self.api}/auth/google/signup",
			data=data,
			headers=self.headers).json()

	def get_notifications(self) -> dict:
		return requests.get(
			f"{self.api}/notification",
			headers=self.headers).json()

	def get_chat_users(
			self,
			chat_id: int,
			count: int = 10) -> dict:
		return requests.get(
			f"{self.api}/topic/{chat_id}/member?count={count}",
			headers=self.headers).json()

	def get_user_chats(
			self,
			user_id: str,
			count: int = 10) -> dict:
		return requests.get(
			f"{self.api}/user/{user_id}/topic?count={count}",
			headers=self.headers).json()

	def get_discover_items(self, count: int = 10) -> dict:
		return requests.get(
			f"{self.api}/topic/discover?count={count}",
			headers=self.headers).json()

	def get_discover_onboarding(self) -> dict:
		return requests.get(
			f"{self.api}/discover/onboarding",
			headers=self.headers).json()

	def get_discover_communities(self) -> dict:
		return requests.get(
			f"{self.api}/community/discover",
			headers=self.headers).json()

	def get_chats(self, count: int = 10) -> dict:
		return requests.get(
			f"{self.api}/topic?count={count}",
			headers=self.headers).json()

	def get_direct_messages_requests(self) -> dict:
		return requests.get(
			f"{self.api}/dm/request",
			headers=self.headers).json()

	def get_all_chats(self) -> dict:
		return requests.get(
			f"{self.api}/topic/all",
			headers=self.headers).json()

	def get_chat(self, chat_id: int) -> dict:
		return requests.get(
			f"{self.api}/topic/{chat_id}",
			headers=self.headers).json()

	def get_chat_by_link(self, link: str) -> dict:
		return requests.get(
			f"{self.api}/link/{link}",
			headers=self.headers).json()

	def get_user(self, user_id: str) -> dict:
		return requests.get(
			f"{self.api}/user/{user_id}",
			headers=self.headers).json()

	def get_trending_gifs(self) -> dict:
		return requests.get(
			f"{self.api}/gifs/trending",
			headers=self.headers).json()

	def get_chat_photos(
			self,
			chat_id: int,
			count: str = 50,
			reverse: bool = True) -> dict:
		return requests.get(
			f"{self.api}/topic/{chat_id}/photo?count={count}&reverse={reverse}",
			headers=self.headers).json()

	def get_chat_messages(
			self,
			chat_id: int,
			count: int = 10) -> dict:
		return requests.get(
			f"{self.api}/topic/{chat_id}/message?count={count}",
			headers=self.headers).json()

	def search_mention_users(
			self,
			chat_id: int,
			prefix: str = "") -> dict:
		return requests.get(
			f"{self.api}/topic/{chat_id}/mention/suggest?prefix={prefix}",
			headers=self.headers).json()

	def send_message(
			self,
			chat_id: int,
			text: str,
			quote_message_id: str = None,
			gif_id: str = None,
			gif_provider: str = None) -> dict:
		data = {
			"text": text
		}
		if quote_message_id:
			data["quote_message_id"] = quote_message_id
		if gif_id:
			data["gif_id"] = gif_id
		if gif_provider:
			data["gif_provider"] = gif_provider
		return requests.post(
			f"{self.api}/topic/{chat_id}/message",
			data=data,
			headers=self.headers).json()

	def create_chat(
			self,
			content: str,
			name: str,
			is_channel: bool = False,
			is_private: bool = False) -> dict:
		data = {
			"channel": is_channel,
			"private": is_private,
			"name": name,
			"content": content
		}
		return requests.post(
			f"{self.api}/topic",
			data=data,
			headers=self.headers).json()

	def edit_chat(
			self,
			chat_id: int,
			description: str = None,
			name: str = None,
			category_id: int = 1) -> dict:
		data = {
			"category_id": category_id,
			"name": name,
			"discription": description
		}
		return requests.patch(
			f"{self.api}/topicId/{chat_id}",
			data=data,
			headers=self.headers).json()

	def delete_message(
			self,
			chat_id: int,
			message_id: str) -> dict:
		return requests.delete(
			f"{self.api}/topic/{chat_id}/message{message_id}",
			headers=self.headers).json()

	def join_chat(self, chat_id: int) -> dict:
		return requests.post(
			f"{self.api}/topic/{chat_id}/subscription",
			headers=self.headers).json()

	def leave_chat(self, chat_id: int) -> dict:
		return requests.delete(
			f"{self.api}/topic/{chat_id}/subscription",
			headers=self.headers).json()

	def edit_profile(
			self,
			name: str = None,
			bio: str = None,
			location: str = None,
			status: bool = True) -> dict:
		data = {
			"online": status
		}
		if name:
			data["name"] = name
		if bio:
			data["bio"] = bio
		if location:
			data["location"] = location
		return requests.patch(
			f"{self.api}/user/me",
			data=data,
			headers=self.headers).json()

	def set_chat_user_role(
			self,
			chat_id: int,
			user_id: str,
			role: str) -> dict:
		data = {
			"role": role
		}
		return requests.patch(
			f"{self.api}/topic/{chat_id}/member/{user_id}",
			data=data,
			headers=self.headers).json()

	def edit_message(
			self,
			chat_id: int,
			message_id: str,
			text: str) -> dict:
		data = {
			"text": text
		}
		return requests.patch(
			f"{self.api}/topic/{chat_id}/message/{message_id}",
			data=data,
			headers=self.headers).json()

	def ban(self, chat_id: int, user_id: str) -> dict:
		return requests.post(
			f"{self.api}/topic/{chat_id}/ban/{user_id}",
			headers=self.headers).json()

	def report_user(
			self, 
			user_id: str,
			reason: str,
			comment: str = None) -> dict:
		data = {
			"reason": reason
		}
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
			comment: str = None) -> dict:
		data = {
			"reason": reason
		}
		if comment:
			data["comment"] = comment
		return requests.post(
			f"{self.api}/topic/{chat_id}/message/{message_id}",
			data=data,
			headers=self.headers).json()

	def report_chat(
			self,
			chat_id: int,
			reason: str,
			comment: str = None) -> dict:
		data = {
			"reason": reason
		}
		if comment:
			data["comment"] = comment
		return requests.post(
			f"{self.api}/topic/{chat_id}/report",
			data=data,
			headers=self.headers).json()

	def unban(self, chat_id: int, user_id: str) -> dict:
		return requests.delete(
			f"{self.api}/topic/{chat_id}/ban/{user_id}",
			headers=self.headers).json()

	def send_direct_message_request(self, user_id: str) -> dict:
		return requests.post(
			f"{self.api}/dm/user/{user_id}",
			headers=self.headers).json()

	def follow_chat(self, chat_id: int) -> dict:
		return requests.post(
			f"{self.api}/topic/{chat_id}/follow",
			headers=self.headers).json()

	def unfollow_chat(self, chat_id: int) -> dict:
		return requests.delete(
			f"{self.api}/topic/{chat_id}/unfollow",
			headers=self.headers).json()

	def search_chats(self, query: str) -> dict:
		return requests.get(
			f"{self.api}/topic/search/{query}",
			headers=self.headers).json()

	def search_gifs(self, query: str) -> dict:
		return requests.get(
			f"{self.api}/gifs/search/{query}",
			headers=self.headers).json()

	def unread(self, chat_id: int) -> dict:
		return requests.delete(
			f"{self.api}/topic/{chat_id}/unread",
			headers=self.headers).json()

	def post_typing(
			self,
			chat_id: int,
			status: str = "text") -> dict:
		return requests.post(
			f"{self.api}/topic/{chat_id}/typing?status={status}",
			headers=self.headers).json()

	def get_config(self) -> dict:
		return requests.get(
			f"{self.api}/config", headers=self.headers).json()

	def get_account_info(self) -> dict:
		return requests.get(
			f"{self.api}/user/me", headers=self.headers).json()

	def get_ml_config(self) -> dict:
		return requests.get(
			f"{self.api}/ml/config",
			headers=self.headers).json()

	def get_joined_communities(self) -> dict:
		return requests.get(
			f"{self.api}/community",
			headers=self.headers).json()

	def get_stickers(self) -> dict:
		return requests.get(
			f"{self.api}/stickers",
			headers=self.headers).json()

	def get_trending_gifs(self) -> dict:
		return requests.get(
			f"{self.api}/gifs/trending",
			headers=self.headers).json()

	def get_user_badges(self, user_id: str) -> dict:
		return requests.get(
			f"{self.api}/user/{user_id}/badges",
			headers=self.headers).json()

	def get_user_by_username(self, username: str) -> dict:
		return requests.get(
			f"{self.api}/user/screen_name/{username}",
			headers=self.headers).json()

	def update_chat_settings(
			self,
			chat_id: int,
			sound: bool = False,
			mute: bool = False) -> dict:
		data = {
			"sound": sound,
			"mute": mute
		}
		return requests.patch(
			f"{self.api}/topic/{chat_id}/settings",
			data=data,
			headers=self.headers).json()

	def get_community(self, com_id: int) -> dict:
		return requests.get(
			f"{self.api}/community/{com_id}",
			headers=self.headers).json()

	def get_community_chats(self, com_id: int) -> dict:
		return requests.get(
			f"{self.api}/community/{com_id}/topic",
			headers=self.headers).json()

	def get_link_preview(self, url: str) -> dict:
		return requests.get(
			f"{self.api}/link/preview?url={url}",
			headers=self.headers).json()

	def get_relevant_chat_photos(
			self,
			chat_id: int,
			count: int = 10) -> dict:
		return requests.get(
			f"{self.api}/topic/{chat_id}/ml/photo?count={count}",
			headers=self.headers).json()

	def remove_chat_from_community(
			self,
			com_id: int,
			chat_id: int) -> dict:
		return requests.delete(
			f"{self.api}/community/{com_id}/topic/{chat_id}",
			headers=self.headers).json()

	def follow_community(self, com_id: int) -> dict:
		return requests.post(
			f"{self.api}/community/{com_id}/member",
			headers=self.headers).json()

	def unfollow_community(self, com_id: int) -> dict:
		return requests.delete(
			f"{self.api}/community/{com_id}/member",
			headers=self.headers).json()
