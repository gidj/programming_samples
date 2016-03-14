import time
import json
from requests_oauthlib import OAuth1Session

# Pulled from here: http://xpo6.com/list-of-english-stop-words/
# In a real program, stop words would be more domain-specific
STOP_WORDS = (
        "a", "about", "above", "across", "after", "afterwards", "again", "against", "all", "almost",
        "alone", "along", "already", "also", "although", "always", "am", "among", "amongst", "amoungst",
        "amount", "an", "and", "another", "any", "anyhow", "anyone", "anything", "anyway", "anywhere",
        "are", "around", "as", "at", "back", "be", "became", "because", "become", "becomes",
        "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between",
        "beyond", "bill", "both", "bottom", "but", "by", "call", "can", "cannot", "cant",
        "co", "computer", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do",
        "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven", "else",
        "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere",
        "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for",
        "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get",
        "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here",
        "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how",
        "however", "hundred", "i", "ie", "if", "in", "inc", "indeed", "interest", "into",
        "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less",
        "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more",
        "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely",
        "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor",
        "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one",
        "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out",
        "over", "own", "part", "per", "perhaps", "please", "put", "rather", "re", "same",
        "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show",
        "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something",
        "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that",
        "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore",
        "therein", "thereupon", "these", "they", "thick", "thin", "third", "this", "those", "though",
        "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward",
        "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us",
        "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence",
        "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which",
        "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with",
        "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves",)

CONSUMER_KEY = u"CONSUMER_KEY"
CONSUMER_SECRET = "CONSUMER_SECRET"
ACCESS_TOKEN = "ACCESS_TOKEN"
ACCESS_TOKEN_SECRET = "ACCESS_TOKEN_SECRET"

class TwitterStatusStream(object):
    stream_url = url = 'https://stream.twitter.com/1.1/statuses/sample.json'
    word_dictionary = {}
    twitter_data = []

    def __init__(self, consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET,
                       access_token=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret

    def get_stream_data(self, duration=5):
        session = OAuth1Session(self.consumer_key, self.consumer_secret,
                                self.access_token, self.access_token_secret)
        r = session.get(self.stream_url, stream=True)
        lines = r.iter_lines()

        end_time = time.time() + duration
        while time.time() < end_time:
            line = next(lines)
            if line:
                self.twitter_data.append(json.loads(line))

    def parse_stream_data(self):
        def _process_word(word):
            # Put all word processing here
            if word.lower() not in STOP_WORDS:
                return word.lower()
            else:
                return None

        for line in self.twitter_data:
            # Collect word count into self.word_dictionary; if a tweet doesn't have text,
            # move on.
            try:
                relevant_words = [_process_word(word) for word in line['text'].split() if _process_word(word)]
                for word in relevant_words:
                    if word in self.word_dictionary:
                        self.word_dictionary[word] += 1
                    else:
                        self.word_dictionary[word] = 1
            except KeyError:
                pass

    def get_top_words(self, number=10):
        # Return the top <number> words along with their frequency, in a list of tuples
        return sorted(self.word_dictionary.items(), key=lambda x: -x[1])[:number]

    def print_top_words(self, number=10):
        for word, frequency in self.get_top_words(number):
            print u"{}: {}".format(word, frequency)


if __name__ == "__main__":
    # Create our streaming object with default credentials
    stream = TwitterStatusStream()

    # Collect Tweets for five minutes
    stream.get_stream_data(5*60)

    # Populate the word_dictionary along with frequency
    stream.parse_stream_data()

    # Print the top 10 words:
    stream.print_top_words(10)
