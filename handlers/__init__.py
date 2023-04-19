from . import bot_admin, chat, practice, ping

labelers = [bot_admin.admin_labeler, chat.chat_labeler, practice.labeler, ping.labeler]

__all__ = ["labelers"]