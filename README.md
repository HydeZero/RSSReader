# RSSReader
RSSReader is a RSS Reader made in Python. It takes feeds from URLs, checks for new posts, and outputs it into markdown-friendly formatting. It saves feed urls and feed posts in 2 files in the user's home directory.

### WORKS ON WINDOWS, MACOS, AND LINUX!

## Directions to use
First, clone this repository using git clone.

``git clone https://github.com/HydeZero/RSSReader.git``

Now, `cd` into the directory created by the repository and make a virtual environment there.

``python3 -m venv ./``

Finally, install the required dependencies using `pip install`.

``pip install -r requirements.txt``

Now, you are ready to use it! Just run `python3 ./src/main.py` and add a feed. It will automatically create 2 files to store feed posts and feed urls. They are subbedFeeds.txt and subbedFeedsContent.csv, so dont delete those.

Every time it boots up, it will check for new posts.

It is not recommended to use this on rapidly posting/changing feeds, as it will clog up the post file fast.

## List Of Commands

`add`: adds a rss feed from a url.

`remove`: removes a rss feed from the subscription list and all posts by the feed (this will take time)

`help`: displays the help menu menu

`exit`: quits

`refresh`: refreshes the post list

`read`: reads a post.

## More Notes
Some sites will be broken with the feed.