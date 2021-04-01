# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name: Lynn Zhang
# Collaborators:
# Time: 241min (4h)
# 2021-03-31 06:20 - 07:00 40min class problem 1 reading and realization
# 2021-03-31 08:00 - 09:10 70min problem 2 & 3, stuck in class concept and class method debugging
#                          some basic errors - list, variable manipulation
#                          class - subclass - what attributes to put in __init__
#            21:31 - 21:39 8min Problem 3 TitleTrigger done.
#                           issue was caused by wrong use of finding index
#                           and not considering to put phrase to lower case
#                           punctuation exceptions purple@#$%cow not considered -> need to think fully
#            22:20 - 23:00 40min Problem 4 DescriptionTrigger
#                               and Problem 5&6 TimeTrigger - how to set up timezone on datetime
# 2021-04-01 05:31 - 05:54 23min Problem 7,8,9
#            05:55 - 06:55 60min Problem 10-12
# unsolved: Polling...object has no attribute 'description'

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

# write the class - NewsStory
class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_link(self):
        return self.link

    def get_pubdate(self):
        return self.pubdate

#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
# subclass - PhraseTrigger
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase

    def is_phrase_in(self, text):
        # not case sensitive - make string into lower case
        text_lowercase = text.lower()
        phrase_lower = self.phrase.lower()
        # remove the punctuations in the text - string.punctuation
        for c in string.punctuation:
            if c in text_lowercase:
                text_lowercase = text_lowercase.replace(c,' ')
        # convert the text string into list
        text_list = text_lowercase.split()

        # check validity of the phrase?

        # if phrase is valid, continue:
        # return true if phrase is present in the string text
        # split the phrase into a list of words
        phrase_list = phrase_lower.split()
        index = 0    # keep track of the index of the word in phrase list
        # starting search from the first word in the phrase,
        # if found, then starting where the first word was found, check whether the rest matches the phrase
        if phrase_list[index] in text_list:       #if find the word,
            # search the next word starting from where the first word was found
            index_in_text = text_list.index(phrase_list[index])
            # if the rest words in text is less than phrase, then return false
            if len(text_list) - index_in_text < len(phrase_list) - index:
                return False
            # else, check whether the rest matches
            index += 1    # index in phrase list
            index_in_text += 1
            while index < len(phrase_list):
                # one mismatch return false
                if phrase_list[index] != text_list[index_in_text]:
                    return False
                index += 1
                index_in_text += 1
            return True


# Problem 3
# Subclass TitleTrigger
class TitleTrigger(PhraseTrigger):
    def __init__(self, phrase):
        PhraseTrigger.__init__(self, phrase)

    def evaluate(self, story):
        title = story.get_title()
        if self.is_phrase_in(title):
            return True
        else:
            return False


# Problem 4
# subclass: DescriptionTrigger
class DescriptionTrigger(PhraseTrigger):
    def __int__(self, phrase):
        PhraseTrigger.__init__(self, phrase)

    def evaluate(self, story):
        description = story.get_description()
        if self.is_phrase_in(description):
            return True
        else:
            return False

# TIME TRIGGERS

# Problem 5
# SUBCLASS TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.
class TimeTrigger(Trigger):
    def __init__(self, time_string):
        self.time = datetime.strptime(time_string, "%d %b %Y %H:%M:%S").replace(tzinfo=pytz.timezone("EST"))

# Problem 6
# SUBCLASS BeforeTrigger and AfterTrigger
class BeforeTrigger(TimeTrigger):
    def __init__(self, time_string):
        TimeTrigger.__init__(self, time_string)

    def evaluate(self, story):
        story_date = story.get_pubdate().replace(tzinfo=pytz.timezone("EST"))
        if story_date < self.time:
            return True
        else:
            return False

class AfterTrigger(TimeTrigger):
    def __init__(self, time_string):
        TimeTrigger.__init__(self, time_string)

    def evaluate(self, story):
        story_date = story.get_pubdate().replace(tzinfo=pytz.timezone("EST"))
        if story_date > self.time:
            return True
        else:
            return False

# COMPOSITE TRIGGERS

# Problem 7
# Subclass: NotTrigger
class NotTrigger(Trigger):
    def __init__(self, T):
        self.the_other_trigger = T

    def evaluate(self, story):
        if self.the_other_trigger.evaluate(story) == True:
            return False
        else:
            return True

# Problem 8
# SUBCLASS: AndTrigger
class AndTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2

    def evaluate(self, story):
        if self.trigger1.evaluate(story) and self.trigger2.evaluate(story):
            return True
        else:
            return False

# Problem 9
# SUBCLASS: OrTrigger
class OrTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2

    def evaluate(self, story):
        if self.trigger1.evaluate(story) or self.trigger2.evaluate(story):
            return True
        else:
            return False

#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)
    stories_filtered = []
    for trigger in triggerlist:
        for story in stories:
            if trigger.evaluate(story) == True:
                stories_filtered.append(story)

    return stories_filtered




#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers
    trigger_dict = {}
    for line in lines:
        # split each line into words
        word_list = line.split(',')
        print(word_list)
        # if the first word is not ADD, then it is the trigger -> store that trigger
        key = word_list[0]
        if key != 'ADD':
            type = word_list[1]
            if type == 'TITLE':
                trigger_dict[key] = TitleTrigger(word_list[2])
            elif type == 'DESCRIPTION':
                trigger_dict[key] = DescriptionTrigger(word_list[2])
            elif type == 'AFTER':
                trigger_dict[key] = AfterTrigger(word_list[2])
            elif type == 'BEFORE':
                trigger_dict[key] = BeforeTrigger(word_list[2])
            elif type == 'AND':
                trigger_dict[key] = AndTrigger(trigger_dict[word_list[2]], trigger_dict[word_list[3]])
            elif type == 'OR':
                trigger_dict[key] = OrTrigger(trigger_dict[word_list[2]], trigger_dict[word_list[3]])
            elif type == 'NOT':
                trigger_dict[key] = NotTrigger(trigger_dict[word_list[2]])

        # else it defines the trigger list
        else:
            trigger_list_len = len(word_list) - 1   # the length of trigger list
            trigger_list = []
            for i in range(trigger_list_len):
                trigger_list.append(trigger_dict[word_list[i+1]])

    print(trigger_list)
    print(trigger_dict)
    print(lines)
    return trigger_list


SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        # t1 = TitleTrigger("election")
        # t2 = DescriptionTrigger("Trump")
        # t3 = DescriptionTrigger("Clinton")
        # t4 = AndTrigger(t2, t3)
        # triggerlist = [t1, t4]

        # Problem 11
        triggerlist = read_trigger_config('debate_triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()