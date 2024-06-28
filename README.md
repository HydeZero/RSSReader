# RSSReader
RSSReader is a RSS Reader made in Python. It takes feeds from URLs, checks for new posts, and outputs it into markdown-friendly formatting. It saves feed urls and feed posts in 2 files in the user's home directory. 

This works on Windows, Mac OS, and GNU/Linux systems.

## Directions to use
First, clone this repository using git clone.

``git clone https://github.com/HydeZero/RSSReader.git``

Now, `cd` into the directory created by the repository and make a virtual environment there.

``python3 -m venv ./``

Finally, install the required dependencies using `pip install`.

``pip install -r requirements.txt``

Now, you are ready to use it! Just run `python3 ./src/main.py` and add a feed. It will automatically create 2 files in your home directory to store feed posts and feed urls. They are subbedFeeds.txt and subbedFeedsContent.csv, so dont delete those.

Every time it runs, it will check for new posts.

It is not recommended to use this on rapidly posting/changing feeds, as it will clog up the post file fast.

## List Of Commands

`add`: adds a rss feed from a url.

`remove`: removes a rss feed from the subscription list and all posts by the feed (this will take time)

`help`: displays the help menu menu

`exit`: quits

`refresh`: refreshes the post list

`read`: reads a post.

`reset`: resets the post file and refreshes the feed. Use this if the post file is broken or is getting too large. All posts saved in the file will be lost forever, unless the post is still on the feed.

## More Notes
Some sites will be broken with the parser. This is out of my control. I am beginning to fix it by manually replacing some html elements with spaces.
