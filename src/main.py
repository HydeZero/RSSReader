import feedparser # to parse the feeds (what did you expect this to do)
import os # to get the user's home directory
import platform # to get the os to get the correct variable
import csv # to check for new posts
import webbrowser # to open the links in the feed
import html2markdown

os_type = platform.system()
subbed_feed_file = ""
subbed_feed_monitor = ""

def cleanse_summary(summary, for_reading=False):
    if not for_reading:
        summary = html2markdown.convert(summary)
        summary = summary.replace("\n", "\\n")
    else:
        summary = str(summary).replace("\\n", "\n")
    return summary

def parseRss(url):

    try:
        feed = feedparser.parse(url)
        print("Checking feed '" + feed.feed.title + "'")
    except:
        print(f"ERROR. THE FEED AT {url} MAY BE INVALID. BREAKING...")
        return
    for entry in feed.entries:
        entry.summary = cleanse_summary(entry.summary)

    # Open CSV file for existing entries
    with open(subbed_feed_monitor, mode='r', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['feed', 'title', 'link', 'published', 'summary']
        reader = csv.DictReader(csv_file, fieldnames=fieldnames)
        existing_titles = []
        for row in reader:
            if row['feed'] == feed.feed.title:
                existing_titles.append(row['title'])
                

    # Check for new posts
    has_new_posts = False
    for entry in feed.entries:
        if entry.title not in existing_titles:
            has_new_posts = True
            new_posts.append(entry)
            # Optionally, update monitored CSV (consider efficiency for large feeds)
            with open(subbed_feed_monitor, mode='a', newline='', encoding='utf-8') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writerow({'feed': feed.feed.title, 'title': entry.title, 'link': entry.link, 'published': entry.published, 'summary': entry.summary})

    # Print message if no new posts found
    if not has_new_posts:
        print("No new posts found in this feed.")
    
    if feed.feed.title not in feed_titles:
        feed_titles.append(feed.feed.title)
new_posts = []

feed_titles = []

def parseAndCheckRss(url):
    skip_all = False
    try:
        feed = feedparser.parse(url)
        print("Checking feed '" + feed.feed.title + "'")
    except:
        print(f"ERROR. THE FEED AT {url} MAY BE INVALID. BREAKING...")
        return
    for entry in feed.entries:
        entry.summary = cleanse_summary(entry.summary)


    # Open CSV file for existing entries
    with open(subbed_feed_monitor, mode='r', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['feed', 'title', 'link', 'published', 'summary']
        reader = csv.DictReader(csv_file, fieldnames=fieldnames)
        existing_titles = []
        for row in reader:
            if row['feed'] == feed.feed.title:
                existing_titles.append(row['title'])
                

    # Check for new posts
    has_new_posts = False
    for entry in feed.entries:
        if entry.title not in existing_titles:
            has_new_posts = True
            new_posts.append(entry)
            print(f"""New post found: {entry.title}
Link:
    {entry.link}
Published:
    {entry.published}
Summary:
    {entry.summary}""")
            if not skip_all:
                print(f"Do you want to open the link in {entry.title}? [y/N/skip_all]")
                ans = input()
                if ans.lower() == "y":
                    webbrowser.open(entry.link)
                if ans.lower() == "skip_all" or ans.lower() == "skip all":
                    skip_all = True
            # Optionally, update monitored CSV (consider efficiency for large feeds)
            with open(subbed_feed_monitor, mode='a', newline='', encoding='utf-8') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writerow({'feed': feed.feed.title, 'title': entry.title, 'link': entry.link, 'published': entry.published, 'summary': entry.summary})

    # Print message if no new posts found
    if not has_new_posts:
        print("No new posts found in this feed.")
    
    if feed.feed.title not in feed_titles:
        feed_titles.append(feed.feed.title)

if os_type == "Windows":
    subbed_feed_file = os.environ.get("UserProfile") + "\\subbedFeeds.txt"
    subbed_feed_monitor = os.environ.get("UserProfile") + "\\subbedFeedsContent.csv"
elif os_type == "Darwin" or os_type == "Linux":
    subbed_feed_file = os.environ.get("HOME") + "/subbedFeeds.txt"
    subbed_feed_monitor = os.environ.get("HOME") + "/subbedFeedsContent.csv"

is_new_file = False

try:
    with open(subbed_feed_file, "r") as file:
        print("File Found")
except:
    print("Making feed file now...")
    is_new_file = True
    with open(subbed_feed_file, "w") as file:
        print("Made File.")
        file.close()

feed_file = open(subbed_feed_file, "r")

if is_new_file:
    with open(subbed_feed_monitor, "w") as file:
        file.write("feed,title,link,published,summary")
        file.close()
        print("Cleared monitored feeds since this is a new feed file")
else:
    print("Beginning check...")

feed_file.close()

def refresh_feed():
    feed_file = open(subbed_feed_file, "r")
    for line in feed_file:
        parseAndCheckRss(line)

refresh_feed()

def add_feed():
    feed_file = open(subbed_feed_file, "a")
    print("What is the url to the feed to add?")
    urlToTry = input()
    parseRss(urlToTry)
    feed_file.write("\n" + urlToTry)
    feed_file.close()
    print("written new feed to feed subscription file")

def remove_feed():
    print("Input the URL to remove. The current URLs are as followed:")
    feed_file_read = open(subbed_feed_file, "r")
    print(feed_file_read.read())
    feed_file_read.close()
    urlToRemove = input()
    keep_list = []
    with open(subbed_feed_file, "r") as file:
        for item_to_check in file:
            if item_to_check.strip() != urlToRemove.strip():
                keep_list.append(item_to_check)
        file.close()
    with open(subbed_feed_file, "w") as file:
        for url in keep_list:
            file.write(url)
    feed = feedparser.parse(urlToRemove)
    rows_to_keep=[]
    with open(subbed_feed_monitor, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file, fieldnames=['feed','title','link','published','summary'])
        for row in reader:
            if row['feed'] != feed.feed.title:
                rows_to_keep.append(f'{row["feed"]},{row["title"]},{row["link"]},"{row["published"]}","{row["summary"]}"')
        file.close()
    with open(subbed_feed_monitor, mode='w', newline='',encoding='utf-8') as file:
        for item in rows_to_keep:
            file.write(item + '\n')
        file.close()

def read_feed():
    feed_file = open(subbed_feed_file, "r")
    item_num = 1
    
    print("What feed to read from? Type the number thats next to the feed title.")
    for feed in feed_titles:
        print(f"{item_num}: {feed}")
        item_num += 1
    try:
        num_to_read = int(input())-1
    except ValueError:
        print("Please try again with a number.")
    try:
        feed_to_read_from = feed_titles[num_to_read]
        print(f"Reading from {feed_to_read_from}")
    except IndexError:
        print(f"Can't find the feed you specified (feed {num_to_read+1}). Try again.")
    reading_parser(feed_to_read_from)

def reading_parser(title_of_feed):
    titles_to_display = []
    with open(subbed_feed_monitor, mode='r', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['feed', 'title', 'link', 'published', 'summary']
        reader = csv.DictReader(csv_file, fieldnames=fieldnames)
        existing_titles = []
        for row in reader:
            if row['feed'] == title_of_feed:
                titles_to_display.append(row)
    item_num = 1
    print("Type the number beside the post you want to read.")
    for post in titles_to_display:
        print(f"{item_num}: {post['title']}")
        item_num += 1
    try:
        num_to_read = int(input())-1
    except ValueError:
        print("Please try again with a number.")
    try:
        post_to_read = titles_to_display[num_to_read]
        print(f"Reading {post_to_read['title']}")
        print(cleanse_summary(post_to_read['summary'], True))
        print("Open the post link in the browser? [Y/n]")
        if input().lower() != "n":
            webbrowser.open(post_to_read['link'])
    except IndexError:
        print(f"Can't find the post you specified (feed {num_to_read+1}). Try again.")

        

while True:
    print("Command (help for commands):")
    match input():
        case "add":
            add_feed()
        case "remove":
            remove_feed()
        case "exit":
            break
        case "help":
            print("add: adds a rss url feed to the subscription list")
            print("remove: removes a rss url feed from the subscription list and removes all posts associated with the feed (takes time)")
            print("help: displays this menu")
            print("exit: quits")
            print("refresh: refreshes the post list")
            print("read: reads a post.")
        case "refresh":
            refresh_feed()
        case "read":
            read_feed()