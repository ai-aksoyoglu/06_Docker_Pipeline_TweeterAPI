Course Material Edit:



1. At line 32, inside the [Tweepy script](https://krspiced.pythonanywhere.com/_downloads/024c01b1720bb4d35f1bbbdda7582e1b/get_tweets.py) (which is a file called get_tweets.py provided in the [Collect Tweets challenge](https://krspiced.pythonanywhere.com/chapters/project_pipeline/api/README.html) at Step 3), we should use 

   ```python
   'text': status.full_text,
   ```

   instead of

   ```python
   'text': status.text,
   ```

   Because "when using extended mode, the `text` attribute of Status objects returned by `tweepy.API` methods is replaced by a `full_text` attribute, which contains the entire untruncated text of the Tweet." (source: https://docs.tweepy.org/en/latest/extended_tweets.html)

   When using 

   ```python
   'text': status.text,
   ```

   the error is: AttributeError: 'Status' object has no attribute 'text'.

   
