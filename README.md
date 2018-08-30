# AskHistoriansBot

**NB: This is still very much a work in progress**

## Description
[r/AskHistorians](www.reddit.com/r/AskHistorians) is one the few treasures on reddit. The community submit historical questions (questions on events (> 20 years old) and historians, and those with a keen interest in history attempt to answer them. Note that only answers which are properly cited, will remain, and all else (e.g., speculative, and shallow responses) will be removed. This means that the subreddit is heavily moderated. This is why it is a gem. This heavy moderation is a massive time sink. The question is, how can machine learning alleviate this burden?

This repo contains code that (will be) the full process of building an automoderator of the subreddit. One that ingests answers in real time, and classfies them as qualitative enough or not for this subreddit. This is decomposed into 3 sections: the data pipeline to train the classifier, the classifier itself, and then the automoderator employing the classifier.

### Data Pipeline
Status: 90% complete

This involves building a database of top level comments (answers) and then periodically checking on those comments to see if they have been removed or not by the moderators. If the comments have been removed after some period, say several days, this is a label for the comment as not substansive enough. Otherwise, it is a label that the answer is.

### Classifier
Status: 50% complete

Using a curated set of answers, we can employ all the usual means to build a classification algorithm for the bot.

### Realtime Automoderator
Status: 0% Complete

We build a bot that will automatically ingest answers, and then evaluated them via the classifier, whether they are substansive enough or not.

## Requirements
- SQLite
- PRAW (Reddit's python api wrapper)
- An api account from Reddit
- Python

