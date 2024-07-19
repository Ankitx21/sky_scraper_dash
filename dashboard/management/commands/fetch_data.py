# import requests
# from django.core.management.base import BaseCommand
# from dashboard.models import Website

# class Command(BaseCommand):
#     help = 'Fetch data from the API and populate the database'

#     def handle(self, *args, **kwargs):
#         initial_url = "https://webscrapper.inside-ai.xyz/"
#         response = requests.get(initial_url)

#         if response.status_code == 200:
#             data = response.json()
#             articles = data.get('article', [])

#             for article in articles:
#                 url = article.get('URL')
#                 if url:
#                     website_info = self.get_website_info(url)
#                     count = website_info.get("count", 0)
#                     is_automation_running = website_info.get("is_automation_running", False)
#                     is_source_active = website_info.get("is_source_active", False)

#                     Website.objects.update_or_create(
#                         name=url,
#                         defaults={
#                             'scraped_articles_24hrs': count,
#                             'automation_running': is_automation_running,
#                             'source_active': is_source_active
#                         }
#                     )
            
#             self.stdout.write(self.style.SUCCESS('Successfully fetched and populated the database'))
#         else:
#             self.stdout.write(self.style.ERROR('Failed to fetch data from the API'))

#     def get_website_info(self, url):
#         detailed_url = "https://webscrapper.inside-ai.xyz/source/"
#         payload = {'url': url}
#         headers = {}
#         response = requests.request("GET", detailed_url, headers=headers, data=payload)
#         if response.status_code == 200:
#             return response.json()
#         return {}
