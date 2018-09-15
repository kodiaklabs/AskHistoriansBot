# AskHistoriansBot
Code for data pipeline and classification of comments to build an automoderator for r/AskHistorians.
**NB: This is still very much a work in progress**

## Description
[r/AskHistorians](www.reddit.com/r/AskHistorians) is one the few treasures on reddit. The community submit historical questions (questions on events>20 years old) and historians, or those with a keen interest in history attempt to answer them. Note that only answers which are properly thought-out, and cited, will remain; and all else (e.g., speculative, and shallow responses) will be removed. To achieve a high quality subreddit means that the subreddit is heavily moderated. This is why it is a gem. This heavy moderation is a massive time sink. The question is, how can machine learning alleviate this burden?

This repo contains code that will be the full process of building an automoderator of the subreddit. One that ingests answers in real time, and classfies them as qualitative enough or not for this subreddit, and then alerts a moderator if they are not. This is decomposed into 3 sections: the data pipeline to train the classifier, the classifier itself, and then the automoderator employing the classifier.

### Data Pipeline
This involves building a database of top level comments (answers) and then periodically checking on those comments to see if they have been removed or not by the moderators. If the comments have been removed after some period, say several days, then this is used as a label for the comment as not substansive enough. Otherwise, it is a label that the answer is. Therefore, we let the moderators build our labelled dataset.

See the CommentGatherer.py code for the implementation of this aspect.

### Classifier
Using a curated set of answers, we  employ all the usual means to build a classification algorithm for the bot. The features used to classify comments are the metadata of the comments, not the contents of the answer itself.

To see how this classifier is built see 'Building an AskHistorians Comment Classifier' Jupyter notebook.

### Realtime Automoderator
(Still building out this part.)
We build a bot that will automatically ingest answers, and then evaluated them via the classifier, whether they are substansive enough or not. If not, the bot will automatically report the post to the moderators, as not substansive enough.

## Requirements
- SQLite
- [PRAW (Reddit's python api wrapper)](https://praw.readthedocs.io/en/latest/)
- [An api account from Reddit](https://github.com/reddit-archive/reddit/wiki/OAuth2)
- Python (3.7)

