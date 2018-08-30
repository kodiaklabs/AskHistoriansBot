"""
Module constructs an sqlite database to gather comments from AskHistorians
subreddit, and gathers them. It can then check on all the posts within the
database, to see if they have been consequently removed from the subreddit.

This data can then be used to build a classifier to classify worthy answers
to questions on the subreddit.
"""
import sqlite3
import praw
import time


class Gatherer(object):
    """docstring for Gatherer"""
    def __init__(self, db_name):
        self.db_name = db_name

    def connect(self, client_id_val, client_secret_val):
        reddit_instance = praw.Reddit(user_agent='AskHistorian bot V0.1',
                                      client_id=client_id_val,
                                      client_secret=client_secret_val)
        return reddit_instance

    def construct_db(self):
        db = sqlite3.connect(self.db_name)
        cursor = db.cursor()
        sql_command = ("""CREATE TABLE Comments(CommentID TEXT, Author TEXT,
                                                CreationTime REAL,
                                                CommentText TEXT,
                                                CommentPerma TEXT,
                                                Removed INTEGER,
                                                LastChecked REAL)""")
        cursor.execute(sql_command)
        db.commit()
        db.close()

    def gather_comments(self, reddit_instance, lim):
        comment_objs = \
            reddit_instance.subreddit('AskHistorians').comments(limit=lim)
        for ind, comment_obj in enumerate(comment_objs):
            print(ind)
            comment_details = self.get_comment_details(comment_obj)
            if comment_details is not None:
                self.store_comment_details(comment_details, reddit_instance)

    def get_comment_details(self, comment_obj):
        try:
            comment_str = comment_obj.body
            if comment_str != u'[removed]':
                author = str(comment_obj.author)
                comment_id = comment_obj.id
                creation_stamp = comment_obj.created_utc
                perma = comment_obj.permalink
                return (comment_id, author, creation_stamp, comment_str,
                        perma)
            else:
                return None
        except:
            print('Could not retrive all comment details')
            return None

    def is_top_level(self, comment_id, reddit_instance):
        """
        Checks to see if comment is a top level comment. If not, returns
        False, otherwise, True
        """
        comment_obj = reddit_instance.comment(id=comment_id)
        if comment_obj.parent_id.split('_')[0] == 't3':
        #         Parent is a post, therefore top level comment.
            return True
        else:
            return False

    def store_comment_details(self, comment_details, reddit_instance):
        comment_id, author, creation_stamp, comment_str, perma = \
            comment_details[:]
        removed = -1
        last_checked = creation_stamp
        db_entry = (comment_id, author, creation_stamp, comment_str, perma,
                    removed, last_checked)

        top_level_comment = self.is_top_level(comment_id, reddit_instance)
        # comment_in_db = self.is_in_DB(comment_id, cursor)

        if top_level_comment:
        # if top_level_comment and not comment_in_db
                self.comment_into_DB(db_entry)
        else:
            pass

    def is_in_DB(self, comment_id, db_cursor):
        """
        Checks the given comment is not already in the DB. Returns True,
        if not found, otherwise False.
        """
        db_cursor.execute("SELECT CommentID FROM Comments WHERE CommentID=?",
                          (comment_id,))
        data = db_cursor.fetchone()
        if data is None:
            return False
        else:
            return True

    def comment_into_DB(self, comment_details_tuple):
        comment_id, author, creation_stamp, comment_str, perma, removed, \
            last_checked = comment_details_tuple[:]

        db = sqlite3.connect(self.db_name)
        cursor = db.cursor()
        if not self.is_in_DB(comment_id, cursor):
            cursor.execute("INSERT INTO Comments (CommentID, Author, CreationTime,"
                   "CommentText, CommentPerma, Removed, LastChecked) VALUES (?,?,?,?,?,?,?)",
                   (comment_id, author, creation_stamp, comment_str, perma,
                    removed, last_checked))
        db.commit()
        db.close()

    def check_stale_comments(self, reddit_instance, stale_days=7):
        """
        This runs through the DB, and checks on comments that are not
        older than x days, and are not removed (Removed=0).
        """
        if stale_days < 0:
            t_limit = self.stale_time_limit(stale_days)
        else:
            t_limit = stale_days
    #     Retrive the entries in the DB that satisfy the conditions
        removed_bool = 0
        comment_id_list = self.get_comment_id_list(t_limit, removed_bool)
        print('Length of comment id list to check ', len(comment_id_list))
        self.update_db_comments(reddit_instance, comment_id_list)

    def stale_time_limit(self, stale_days):
    #     Set the stale time limit for which
    #     comments are unlikely to change
        current_time_epoch = int(time.time())
        seconds_in_day = 86400.0
        t_limit = current_time_epoch - (seconds_in_day * stale_days)
        return t_limit

    def get_comment_id_list(self, t_limit, removed_bool):
        db = sqlite3.connect(self.db_name)
        cursor = db.cursor()
    #     Retrive the entries in the DB that satisfy the conditions
        if t_limit < 0:
            cursor.execute("SELECT CommentID FROM Comments WHERE CreationTime>? AND Removed<=?",
                           (t_limit, removed_bool))
        else:
            # check all comments irrespective of time.
            cursor.execute("SELECT CommentID FROM Comments WHERE Removed<=?",
                           (removed_bool, ))
        comment_id_list = cursor.fetchall()
        comment_id_list = [c[0] for c in comment_id_list]
        db.close()
        return comment_id_list

    def update_db_comments(self, reddit_instance, comment_id_list):
        """
        Checks DB to see if any comments were removed. If removed sets Removed
        column to 1 (True), else, 0 (False), and updates the time for which it
        was checked.
        """
        db = sqlite3.connect(self.db_name)
        cursor = db.cursor()
        for ind, c_id in enumerate(comment_id_list):
            print('checking ', ind)
            comment_flag = self.comment_removed(reddit_instance, c_id)
            last_checked = int(time.time())

            if comment_flag:
                cursor.execute("UPDATE Comments SET Removed=?, LastChecked=? WHERE CommentID=?",
                               (1, last_checked, c_id))

            else:
                cursor.execute("UPDATE Comments SET Removed=?, LastChecked=? WHERE CommentID=?",
                               (0, last_checked, c_id))
        db.commit()
        db.close()

    def comment_removed(self, r, comment_id):
        """
        Given a comments permalink, check to see if it has been removed.
        """
        comment_str = r.comment(id=comment_id).body
        if comment_str != u'[removed]':
            return False
        else:
            print(comment_id, ' was removed')
            return True
