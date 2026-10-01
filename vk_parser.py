import os
import re
import sys
import django
import requests
import unidecode
from dotenv import load_dotenv
from datetime import datetime, timezone
from django.utils.text import slugify


sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

django.setup()
from news.models import VKPost

load_dotenv()

def make_slug(text: str, post_id: int) -> str:
    first_line = next((line.strip() for line in text.splitlines() if line.strip()), "")
    if not first_line:
        return f"post-{post_id}"
    # Транслитерация в латиницу + slugify без unicode
    base = slugify(unidecode.unidecode(first_line[:60]))[:150] or "post"
    return f"{base}-{post_id}"

class Post:
    def __init__(self, vk_post_id, vk_attached_photo_links, vk_date_created, vk_text):
        self.post_id = vk_post_id
        self.attached_photos = vk_attached_photo_links
        self.published = vk_date_created
        self.text = vk_text

class VKParser:

    def __init__(self):
        self.token = os.getenv("VK_ACCESS_TOKEN")
        self.session = requests.Session()
        self.api_version = "5.131"
        self.group = "schola135"

    def _make_request(self, method, params):
        url = f"https://api.vk.com/method/{method}"
        params["access_token"] = self.token
        params["v"] = self.api_version
        response = requests.get(url, params=params)
        return response.json()

    def get_last_posts(self, count: int = 10) -> list:
        """Получает последние посты, сохраняет их в БД и возвращает список объектов."""
        params = {
            "domain": self.group,
            "count": count,
        }
        json_response = self._make_request("wall.get", params)

        posts_data = json_response.get("response", {}).get("items", [])
        parsed_posts = []

        for item in posts_data:
            post_id = item.get("id")
            date_created = item.get("date")
            vk_text = item.get("text", "").strip()

            dt_created = datetime.fromtimestamp(date_created, tz=timezone.utc)

            hashtags = re.findall(r'#([^#\s]+)', vk_text)

            photo_links = []
            attachments = item.get("attachments", [])
            for attach in attachments:
                if attach.get("type") == "photo":
                    photo = attach.get("photo", {})
                    sizes = photo.get("sizes", [])
                    if sizes:
                        max_size_photo = sizes[-1]
                        photo_links.append(max_size_photo.get("url"))

            if not vk_text and not photo_links:
                print(f"[skip] Пост {post_id}: нет ни текста, ни фото")
                continue

            if not vk_text:
                vk_text = "Пост не содержал текста."

            post, created = VKPost.objects.update_or_create(
                vk_id=post_id,
                defaults={
                    'text': vk_text,
                    'created': dt_created,
                    'photos': photo_links,
                    'slug': make_slug(vk_text, post_id),
                }
            )

            post.tags.clear()
            if hashtags:
                post.tags.add(*hashtags)

            post_object = Post(
                vk_post_id=post_id,
                vk_attached_photo_links=photo_links,
                vk_date_created=date_created,
                vk_text=vk_text,
            )
            parsed_posts.append(post_object)

        return parsed_posts


if __name__ == "__main__":
    parser = VKParser()

    posts = parser.get_last_posts(count=48)

    for post in posts:
        print(f"ID Поста: {post.post_id}")
        print(f"Дата (Unixtime): {post.published}")
        print(f"Найдено фото: {len(post.attached_photos)}")
        for link in post.attached_photos:
            print(f"  -> Ссылка на фото: {link}")
        print(f'ТЕКСТ ПОСТА: {post.text}')
        print("-" * 50)