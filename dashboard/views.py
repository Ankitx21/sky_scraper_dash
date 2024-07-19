import requests
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from concurrent.futures import ThreadPoolExecutor
import json
import os

# File to store previous automation statuses
STATUS_FILE = 'previous_statuses.json'

# Helper function to load previous statuses from file
def load_previous_statuses():
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, 'r') as file:
            return json.load(file)
    return {}

# Helper function to save current statuses to file
def save_current_statuses(current_statuses):
    with open(STATUS_FILE, 'w') as file:
        json.dump(current_statuses, file)

def fetch_data_from_api():
    initial_url = "https://webscrapper.inside-ai.xyz/"
    response = requests.get(initial_url)
    data = response.json()
    websites = data.get("article", [])

    total_websites = len(websites)
    total_articles_scraped = 0
    active_websites_count = 0
    highest_scraped = {"url": "", "count": 0}
    recent_added_website = ""
    automation_turned_off_website = ""
    false_automation_count = 0
    zero_articles_active_automation = 0

    website_details = []

    # Load previous statuses
    previous_statuses = load_previous_statuses()
    current_statuses = {}

    def get_website_info(url):
        detailed_url = "https://webscrapper.inside-ai.xyz/source/"
        payload = {'url': url}
        headers = {}
        response = requests.request("GET", detailed_url, headers=headers, data=payload)
        return response.json()

    def process_website(website):
        nonlocal total_articles_scraped, active_websites_count, recent_added_website, automation_turned_off_website, false_automation_count, zero_articles_active_automation, highest_scraped

        url = website.get('URL')
        website_info = get_website_info(url)
        count = website_info.get("count")
        is_automation_running = website_info.get("is_automation_running")
        is_source_active = website_info.get("is_source_active")

        # Store current status
        current_statuses[url] = is_automation_running

        # Compare with previous status
        if previous_statuses.get(url) and not is_automation_running:
            automation_turned_off_website = url

        if not recent_added_website:
            recent_added_website = url

        if count > highest_scraped["count"]:
            highest_scraped = {"url": url, "count": count}

        total_articles_scraped += count
        if is_automation_running and is_source_active and count > 0:
            active_websites_count += 1

        if website.get("previous_automation_status") and not is_automation_running:
            automation_turned_off_website = url

        if not is_automation_running:
            false_automation_count += 1

        if is_automation_running and is_source_active and count == 0:
            zero_articles_active_automation += 1

        website_details.append({
            'name': url,
            'scraped_articles_24hrs': count,
            'automation_running': is_automation_running,
            'source_active': is_source_active
        })

    with ThreadPoolExecutor() as executor:
        executor.map(process_website, websites)

    # Save current statuses to file
    save_current_statuses(current_statuses)

    return {
        'total_websites': total_websites,
        'total_articles_scraped': total_articles_scraped,
        'active_websites': active_websites_count,
        'websites': website_details,
        'recent_added_website': recent_added_website,
        'automation_turned_off_website': automation_turned_off_website,
        'top_scraper_website': highest_scraped["url"],
        'top_scraper_articles': highest_scraped["count"],
        'false_automation_count': false_automation_count,
        'zero_articles_active_automation': zero_articles_active_automation
    }

@login_required
def dashboard(request):
    data = fetch_data_from_api()
    return render(request, 'dashboard/index.html', data)

def auth_view(request):
    if request.method == 'POST':
        if 'login' in request.POST:
            login_form = AuthenticationForm(request, data=request.POST)
            signup_form = UserCreationForm()
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect('dashboard')
        elif 'signup' in request.POST:
            signup_form = UserCreationForm(request.POST)
            login_form = AuthenticationForm()
            if signup_form.is_valid():
                signup_form.save()
                return redirect('auth')
    else:
        login_form = AuthenticationForm()
        signup_form = UserCreationForm()
    
    return render(request, 'dashboard/auth.html', {
        'login_form': login_form,
        'signup_form': signup_form
    })

def logout_view(request):
    logout(request)
    return redirect('auth')
