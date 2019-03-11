from pandas import DataFrame, read_csv
import pandas as pd
from pandas import DataFrame, read_csv
import pandas as pd
#location = r'/content/gdrive/My Drive/train.csv'
df = pd.read_csv(r'C:\Users\admin\Desktop/train.csv', encoding='latin-1')
lister=df.SentimentText.tolist()
df['SentimentText'] = df['SentimentText'].str.replace('\d+', '')
import re
import nltk
from nltk.corpus import stopwords
from gensim.utils import lemmatize
from tqdm import tqdm_notebook as tqdm
from nltk.stem.wordnet import WordNetLemmatizer

stopwords = stopwords.words('english')
extra = ['amp','im','u',]
stopwords.extend(extra)
stop_words = set(stopwords)
lmtzr = WordNetLemmatizer()

appos = {
"aren't" : "are not",
"can't" : "cannot",
"couldn't" : "could not",
"didn't" : "did not",
"doesn't" : "does not",
"don't" : "do not",
"hadn't" : "had not",
"hasn't" : "has not",
"haven't" : "have not",
"he'd" : "he would",
"he'll" : "he will",
"he's" : "he is",
"i'd" : "i would",
"i'd" : "i had",
"i'll" : "i will",
"i'm" : "i am",
"isn't" : "is not",
"it's" : "it is",
"it'll":"it will",
"i've" : "i have",
"let's" : "let us",
"mightn't" : "might not",
"mustn't" : "must not",
"shan't" : "shall not",
"she'd" : "she would",
"she'll" : "she will",
"she's" : "she is",
"shouldn't" : "should not",
"that's" : "that is",
"there's" : "there is",
"they'd" : "they would",
"they'll" : "they will",
"they're" : "they are",
"they've" : "they have",
"we'd" : "we would",
"we're" : "we are",
"weren't" : "were not",
"we've" : "we have",
"what'll" : "what will",
"what're" : "what are",
"what's" : "what is",
"what've" : "what have",
"where's" : "where is",
"who'd" : "who would",
"who'll" : "who will",
"who're" : "who are",
"who's" : "who is",
"who've" : "who have",
"won't" : "will not",
"wouldn't" : "would not",
"you'd" : "you would",
"you'll" : "you will",
"you're" : "you are",
"you've" : "you have",
"'re": " are",
"wasn't": "was not",
"we'll":" will",
"didn't": "did not"
}

EMOTICONS = {
    ":‑\)":"Happy face or smiley",
    "):":"Frown, sad, angry or pouting",
    ":)":"Happy face smiley",
    "(:":"Happy face smiley",
    ":\)":"Happy face  smiley",
    ":-\]":"Happy face  smiley",
    ":\]":"Happy face  smiley",
    ":-3":"Happy face smiley",
    ":3":"Happy face smiley",
    ":->":"Happy face smiley",
    ":>":"Happy face smiley",
    "8-\)":"Happy face smiley",
    ":o\)":"Happy face smiley",
    ":-\}":"Happy face smiley",
    ":\}":"Happy face smiley",
    ":-\)":"Happy face smiley",
    ":c\)":"Happy face smiley",
    ":\^\)":"Happy face smiley",
    "=\]":"Happy face smiley",
    "=\)":"Happy face smiley",
    ":‑D":"Laughing, big grin or laugh with glasses",
    ":D":"Laughing, big grin or laugh with glasses",
    "8‑D":"Laughing, big grin or laugh with glasses",
    "8D":"Laughing, big grin or laugh with glasses",
    "X‑D":"Laughing, big grin or laugh with glasses",
    "XD":"Laughing, big grin or laugh with glasses",
    "=D":"Laughing, big grin or laugh with glasses",
    "=3":"Laughing, big grin or laugh with glasses",
    "B\^D":"Laughing, big grin or laugh with glasses",
    ":-\)\)":"Very happy",
    ":‑\(":"Frown, sad, andry or pouting",
    ":-\(":"Frown, sad, andry or pouting",
    ":\(":"Frown, sad, andry or pouting",
    ":‑c":"Frown, sad, andry or pouting",
    ":c":"Frown, sad, andry or pouting",
    ":‑<":"Frown, sad, andry or pouting",
    ":<":"Frown, sad, andry or pouting",
    ":‑\[":"Frown, sad, andry or pouting",
    ":\[":"Frown, sad, andry or pouting",
    ":-\|\|":"Frown, sad, andry or pouting",
    ">:\[":"Frown, sad, andry or pouting",
    ":\{":"Frown, sad, andry or pouting",
    ":@":"Frown, sad, andry or pouting",
    ">:\(":"Frown, sad, andry or pouting",
    ":'‑\(":"Crying",
    ":'\(":"Crying",
    ":'‑\)":"Tears of happiness",
    ":'\)":"Tears of happiness",
    "D‑':":"Horror",
    "D:<":"Disgust",
    "D:":"Sadness",
    "D8":"Great dismay",
    "D;":"Great dismay",
    "D=":"Great dismay",
    "DX":"Great dismay",
    ":‑O":"Surprise",
    ":O":"Surprise",
    ":‑o":"Surprise",
    ":o":"Surprise",
    ":-0":"Shock",
    "8‑0":"Yawn",
    ">:O":"Yawn",
    ":-\*":"Kiss",
    ":\*":"Kiss",
    ":X":"Kiss",
    ";‑\)":"Wink or smirk",
    ";\)":"Wink or smirk",
    "\*-\)":"Wink or smirk",
    "\*\)":"Wink or smirk",
    ";‑\]":"Wink or smirk",
    ";\]":"Wink or smirk",
    ";\^\)":"Wink or smirk",
    ":‑,":"Wink or smirk",
    ";D":"Wink or smirk",
    ":‑P":"Tongue sticking out, cheeky, playful or blowing a raspberry",
    ":P":"Tongue sticking out, cheeky, playful or blowing a raspberry",
    "X‑P":"Tongue sticking out, cheeky, playful or blowing a raspberry",
    "XP":"Tongue sticking out, cheeky, playful or blowing a raspberry",
    ":‑Þ":"Tongue sticking out, cheeky, playful or blowing a raspberry",
    ":Þ":"Tongue sticking out, cheeky, playful or blowing a raspberry",
    ":b":"Tongue sticking out, cheeky, playful or blowing a raspberry",
    "d:":"Tongue sticking out, cheeky, playful or blowing a raspberry",
    "=p":"Tongue sticking out, cheeky, playful or blowing a raspberry",
    ">:P":"Tongue sticking out, cheeky, playful or blowing a raspberry",
    ":‑/":"Skeptical, annoyed, undecided, uneasy or hesitant",
    ":-/":"Skeptical, annoyed, undecided, uneasy or hesitant" ,
    ":/":"Skeptical, annoyed, undecided, uneasy or hesitant",
    ":-[.]":"Skeptical, annoyed, undecided, uneasy or hesitant",
    ">:[(\\\)]":"Skeptical, annoyed, undecided, uneasy or hesitant",
    ">:/":"Skeptical, annoyed, undecided, uneasy or hesitant",
    ":[(\\\)]":"Skeptical, annoyed, undecided, uneasy or hesitant",
    "=/":"Skeptical, annoyed, undecided, uneasy or hesitant",
    "=[(\\\)]":"Skeptical, annoyed, undecided, uneasy or hesitant",
    ":L":"Skeptical, annoyed, undecided, uneasy or hesitant",
    "=L":"Skeptical, annoyed, undecided, uneasy or hesitant",
    ":S":"Skeptical, annoyed, undecided, uneasy or hesitant",
    ":‑\|":"Straight face",
    ":\|":"Straight face",
    ":$":"Embarrassed or blushing",
    ":‑x":"Sealed lips or wearing braces or tongue-tied",
    ":x":"Sealed lips or wearing braces or tongue-tied",
    ":‑#":"Sealed lips or wearing braces or tongue-tied",
    ":#":"Sealed lips or wearing braces or tongue-tied",
    ":‑&":"Sealed lips or wearing braces or tongue-tied",
    ":&":"Sealed lips or wearing braces or tongue-tied",
    "O:‑\)":"Angel, saint or innocent",
    "O:\)":"Angel, saint or innocent",
    "0:‑3":"Angel, saint or innocent",
    "0:3":"Angel, saint or innocent",
    "0:‑\)":"Angel, saint or innocent",
    "0:\)":"Angel, saint or innocent",
    ":‑b":"Tongue sticking out, cheeky, playful or blowing a raspberry",
    "0;\^\)":"Angel, saint or innocent",
    ">:‑\)":"Evil or devilish",
    ">:\)":"Evil or devilish",
    "\}:‑\)":"Evil or devilish",
    "\}:\)":"Evil or devilish",
    "3:‑\)":"Evil or devilish",
    "3:\)":"Evil or devilish",
    ">;\)":"Evil or devilish",
    "\|;‑\)":"Cool",
    "\|‑O":"Bored",
    ":‑J":"Tongue-in-cheek",
    "#‑\)":"Party all night",
    "%‑\)":"Drunk or confused",
    "%\)":"Drunk or confused",
    ":-###..":"Being sick",
    ":###..":"Being sick",
    "<:‑\|":"Dump",
    "\(>_<\)":"Troubled",
    "\(>_<\)>":"Troubled",
    "\(';'\)":"Baby",
    "\(\^\^>``":"Nervous or Embarrassed or Troubled or Shy or Sweat drop",
    "\(\^_\^;\)":"Nervous or Embarrassed or Troubled or Shy or Sweat drop",
    "\(-_-;\)":"Nervous or Embarrassed or Troubled or Shy or Sweat drop",
    "\(~_~;\) \(・\.・;\)":"Nervous or Embarrassed or Troubled or Shy or Sweat drop",
    "\(-_-\)zzz":"Sleeping",
    "\(\^_-\)":"Wink",
    "\(\(\+_\+\)\)":"Confused",
    "\(\+o\+\)":"Confused",
    "\(o\|o\)":"Ultraman",
    "\^_\^":"Joyful",
    "\(\^_\^\)/":"Joyful",
    "\(\^O\^\)／":"Joyful",
    "\(\^o\^\)／":"Joyful",
    "\(__\)":"Kowtow as a sign of respect, or dogeza for apology",
    "_\(\._\.\)_":"Kowtow as a sign of respect, or dogeza for apology",
    "<\(_ _\)>":"Kowtow as a sign of respect, or dogeza for apology",
    "<m\(__\)m>":"Kowtow as a sign of respect, or dogeza for apology",
    "m\(__\)m":"Kowtow as a sign of respect, or dogeza for apology",
    "m\(_ _\)m":"Kowtow as a sign of respect, or dogeza for apology",
    "\('_'\)":"Sad or Crying",
    "\(/_;\)":"Sad or Crying",
    "\(T_T\) \(;_;\)":"Sad or Crying",
    "\(;_;":"Sad of Crying",
    "\(;_:\)":"Sad or Crying",
    "\(;O;\)":"Sad or Crying",
    "\(:_;\)":"Sad or Crying",
    "\(ToT\)":"Sad or Crying",
    ";_;":"Sad or Crying",
    ";-;":"Sad or Crying",
    ";n;":"Sad or Crying",
    ";;":"Sad or Crying",
    "Q\.Q":"Sad or Crying",
    "T\.T":"Sad or Crying",
    "QQ":"Sad or Crying",
    "Q_Q":"Sad or Crying",
    "\(-\.-\)":"Shame",
    "\(-_-\)":"Shame",
    "\(一一\)":"Shame",
    "\(；一_一\)":"Shame",
    "\(=_=\)":"Tired",
    "\(=\^\·\^=\)":"cat",
    "\(=\^\·\·\^=\)":"cat",
    "=_\^=	":"cat",
    "\(\.\.\)":"Looking down",
    "\(\._\.\)":"Looking down",
    "\^m\^":"Giggling with hand covering mouth",
    "\(\・\・?":"Confusion",
    "\(?_?\)":"Confusion",
    ">\^_\^<":"Normal Laugh",
    "<\^!\^>":"Normal Laugh",
    "\^/\^":"Normal Laugh",
    "\（\*\^_\^\*）" :"Normal Laugh",
    "\(\^<\^\) \(\^\.\^\)":"Normal Laugh",
    "\(^\^\)":"Normal Laugh",
    "\(\^\.\^\)":"Normal Laugh",
    "\(\^_\^\.\)":"Normal Laugh",
    "\(\^_\^\)":"Normal Laugh",
    "\(\^\^\)":"Normal Laugh",
    "\(\^J\^\)":"Normal Laugh",
    "\(\*\^\.\^\*\)":"Normal Laugh",
    "\(\^—\^\）":"Normal Laugh",
    "\(#\^\.\^#\)":"Normal Laugh",
    "\（\^—\^\）":"Waving",
    "\(;_;\)/~~~":"Waving",
    "\(\^\.\^\)/~~~":"Waving",
    "\(-_-\)/~~~ \($\·\·\)/~~~":"Waving",
    "\(T_T\)/~~~":"Waving",
    "\(ToT\)/~~~":"Waving",
    "\(\*\^0\^\*\)":"Excited",
    "\(\*_\*\)":"Amazed",
    "\(\*_\*;":"Amazed",
    "\(\+_\+\) \(@_@\)":"Amazed",
    "\(\*\^\^\)v":"Laughing,Cheerful",
    "\(\^_\^\)v":"Laughing,Cheerful",
    "\(\(d[-_-]b\)\)":"Headphones,Listening to music",
    '\(-"-\)':"Worried",
    "\(ーー;\)":"Worried",
    "\(\^0_0\^\)":"Eyeglasses",
    "\(\＾ｖ\＾\)":"Happy",
    "\(\＾ｕ\＾\)":"Happy",
    "\(\^\)o\(\^\)":"Happy",
    "\(\^O\^\)":"Happy",
    "\(\^o\^\)":"Happy",
    "\)\^o\^\(":"Happy",
    ":O o_O":"Surprised",
    "o_0":"Surprised",
    "o\.O":"Surpised",
    "\(o\.o\)":"Surprised",
    "oO":"Surprised",
    "\(\*￣m￣\)":"Dissatisfied",
    "\(‘A`\)":"Snubbed or Deflated"
}

EMOTICONS_EMO = {
    ":‑)":"Happy face or smiley",
    ":)":"Happy face or smiley",
    ":-]":"Happy face or smiley",
    ":]":"Happy face or smiley",
    ":-3":"Happy face smiley",
    ":3":"Happy face smiley",
    ":->":"Happy face smiley",
    ":>":"Happy face smiley",
    "8-)":"Happy face smiley",
    ":o)":"Happy face smiley",
    ":-}":"Happy face smiley",
    ":}":"Happy face smiley",
    ":-)":"Happy face smiley",
    ":c)":"Happy face smiley",
    ":^)":"Happy face smiley",
    "=]":"Happy face smiley",
    "=)":"Happy face smiley",
    ":‑D":"Laughing, big grin or laugh with glasses",
    ":D":"Laughing, big grin or laugh with glasses",
    "8‑D":"Laughing, big grin or laugh with glasses",
    "8D":"Laughing, big grin or laugh with glasses",
    "X‑D":"Laughing, big grin or laugh with glasses",
    "XD":"Laughing, big grin or laugh with glasses",
    "=D":"Laughing, big grin or laugh with glasses",
    "=3":"Laughing, big grin or laugh with glasses",
    "B^D":"Laughing, big grin or laugh with glasses",
    ":-))":"Very happy",
    ":-(":"Frown, sad, andry or pouting",
    ":‑(":"Frown, sad, andry or pouting",
    ":(":"Frown, sad, andry or pouting",
    ":‑c":"Frown, sad, andry or pouting",
    ":c":"Frown, sad, andry or pouting",
    ":‑<":"Frown, sad, andry or pouting",
    ":<":"Frown, sad, andry or pouting",
    ":‑[":"Frown, sad, andry or pouting",
    ":[":"Frown, sad, andry or pouting",
    ":-||":"Frown, sad, andry or pouting",
    ">:[":"Frown, sad, andry or pouting",
    ":{":"Frown, sad, andry or pouting",
    ":@":"Frown, sad, andry or pouting",
    ">:(":"Frown, sad, andry or pouting",
    ":'‑(":"Crying",
    ":'(":"Crying",
    ":'‑)":"Tears of happiness",
    ":')":"Tears of happiness",
    "D‑':":"Horror",
    "D:<":"Disgust",
    "D:":"Sadness",
    "D8":"Great dismay",
    "D;":"Great dismay",
    "D=":"Great dismay",
    "DX":"Great dismay",
    ":‑O":"Surprise",
    ":O":"Surprise",
    ":‑o":"Surprise",
    ":o":"Surprise",
    ":-0":"Shock",
    "8‑0":"Yawn",
    ">:O":"Yawn",
    ":-*":"Kiss",
    ":*":"Kiss",
    ":X":"Kiss",
    ";‑)":"Wink or smirk",
    ";)":"Wink or smirk",
    "*-)":"Wink or smirk",
    "*)":"Wink or smirk",
    ";‑]":"Wink or smirk",
    ";]":"Wink or smirk",
    ";^)":"Wink or smirk",
    ":‑,":"Wink or smirk",
    ";D":"Wink or smirk",
    ":‑P":"Tongue sticking out, cheeky, playful or blowing a raspberry",
    ":P":"Tongue sticking out, cheeky, playful or blowing a raspberry",
    "X‑P":"Tongue sticking out, cheeky, playful or blowing a raspberry",
    "XP":"Tongue sticking out, cheeky, playful or blowing a raspberry",
    ":‑Þ":"Tongue sticking out, cheeky, playful or blowing a raspberry",
    ":Þ":"Tongue sticking out, cheeky, playful or blowing a raspberry",
    ":b":"Tongue sticking out, cheeky, playful or blowing a raspberry",
    "d:":"Tongue sticking out, cheeky, playful or blowing a raspberry",
    "=p":"Tongue sticking out, cheeky, playful or blowing a raspberry",
    ">:P":"Tongue sticking out, cheeky, playful or blowing a raspberry",
    ":‑/":"Skeptical, annoyed, undecided, uneasy or hesitant",
    ":/":"Skeptical, annoyed, undecided, uneasy or hesitant",
    ":-[.]":"Skeptical, annoyed, undecided, uneasy or hesitant",
    ">:[(\)]":"Skeptical, annoyed, undecided, uneasy or hesitant",
    ">:/":"Skeptical, annoyed, undecided, uneasy or hesitant",
    ":[(\)]":"Skeptical, annoyed, undecided, uneasy or hesitant",
    "=/":"Skeptical, annoyed, undecided, uneasy or hesitant",
    "=[(\)]":"Skeptical, annoyed, undecided, uneasy or hesitant",
    ":L":"Skeptical, annoyed, undecided, uneasy or hesitant",
    "=L":"Skeptical, annoyed, undecided, uneasy or hesitant",
    ":S":"Skeptical, annoyed, undecided, uneasy or hesitant",
    ":-|":"Straight face",
    ":|":"Straight face",
    ":$":"Embarrassed or blushing",
    ":‑x":"Sealed lips or wearing braces or tongue-tied",
    ":x":"Sealed lips or wearing braces or tongue-tied",
    ":‑#":"Sealed lips or wearing braces or tongue-tied",
    ":#":"Sealed lips or wearing braces or tongue-tied",
    ":‑&":"Sealed lips or wearing braces or tongue-tied",
    ":&":"Sealed lips or wearing braces or tongue-tied",
    "O:‑)":"Angel, saint or innocent",
    "O:)":"Angel, saint or innocent",
    "0:‑3":"Angel, saint or innocent",
    "0:3":"Angel, saint or innocent",
    "0:‑)":"Angel, saint or innocent",
    "0:)":"Angel, saint or innocent",
    ":‑b":"Tongue sticking out, cheeky, playful or blowing a raspberry",
    "0;^)":"Angel, saint or innocent",
    ">:‑)":"Evil or devilish",
    ">:)":"Evil or devilish",
    "}:‑)":"Evil or devilish",
    "}:)":"Evil or devilish",
    "3:‑)":"Evil or devilish",
    "3:)":"Evil or devilish",
    ">;)":"Evil or devilish",
    "|;‑)":"Cool",
    "|‑O":"Bored",
    ":‑J":"Tongue-in-cheek",
    "#‑)":"Party all night",
    "%‑)":"Drunk or confused",
    "%)":"Drunk or confused",
    ":-###..":"Being sick",
    ":###..":"Being sick",
    "<:‑|":"Dump",
    "(>_<)":"Troubled",
    "(>_<)>":"Troubled",
    "(';')":"Baby",
    "(^^>``":"Nervous or Embarrassed or Troubled or Shy or Sweat drop",
    "(^_^;)":"Nervous or Embarrassed or Troubled or Shy or Sweat drop",
    "(-_-;)":"Nervous or Embarrassed or Troubled or Shy or Sweat drop",
    "(~_~;) (・.・;)":"Nervous or Embarrassed or Troubled or Shy or Sweat drop",
    "(-_-)zzz":"Sleeping",
    "(^_-)":"Wink",
    "((+_+))":"Confused",
    "(+o+)":"Confused",
    "(o|o)":"Ultraman",
    "^_^":"Joyful",
    "(^_^)/":"Joyful",
    "(^O^)／":"Joyful",
    "(^o^)／":"Joyful",
    "(__)":"Kowtow as a sign of respect, or dogeza for apology",
    "_(._.)_":"Kowtow as a sign of respect, or dogeza for apology",
    "<(_ _)>":"Kowtow as a sign of respect, or dogeza for apology",
    "<m(__)m>":"Kowtow as a sign of respect, or dogeza for apology",
    "m(__)m":"Kowtow as a sign of respect, or dogeza for apology",
    "m(_ _)m":"Kowtow as a sign of respect, or dogeza for apology",
    "('_')":"Sad or Crying",
    "(/_;)":"Sad or Crying",
    "(T_T) (;_;)":"Sad or Crying",
    "(;_;":"Sad of Crying",
    "(;_:)":"Sad or Crying",
    "(;O;)":"Sad or Crying",
    "(:_;)":"Sad or Crying",
    "(ToT)":"Sad or Crying",
    ";_;":"Sad or Crying",
    ";-;":"Sad or Crying",
    ";n;":"Sad or Crying",
    ";;":"Sad or Crying",
    "Q.Q":"Sad or Crying",
    "T.T":"Sad or Crying",
    "QQ":"Sad or Crying",
    "Q_Q":"Sad or Crying",
    "(-.-)":"Shame",
    "(-_-)":"Shame",
    "(一一)":"Shame",
    "(；一_一)":"Shame",
    "(=_=)":"Tired",
    "(=^·^=)":"cat",
    "(=^··^=)":"cat",
    "=_^= ":"cat",
    "(..)":"Looking down",
    "(._.)":"Looking down",
    "^m^":"Giggling with hand covering mouth",
    "(・・?":"Confusion",
    "(?_?)":"Confusion",
    ">^_^<":"Normal Laugh",
    "<^!^>":"Normal Laugh",
    "^/^":"Normal Laugh",
    "（*^_^*）" :"Normal Laugh",
    "(^<^) (^.^)":"Normal Laugh",
    "(^^)":"Normal Laugh",
    "(^.^)":"Normal Laugh",
    "(^_^.)":"Normal Laugh",
    "(^_^)":"Normal Laugh",
    "(^^)":"Normal Laugh",
    "(^J^)":"Normal Laugh",
    "(*^.^*)":"Normal Laugh",
    "(^—^）":"Normal Laugh",
    "(#^.^#)":"Normal Laugh",
    "（^—^）":"Waving",
    "(;_;)/~~~":"Waving",
    "(^.^)/~~~":"Waving",
    "(-_-)/~~~ ($··)/~~~":"Waving",
    "(T_T)/~~~":"Waving",
    "(ToT)/~~~":"Waving",
    "(*^0^*)":"Excited",
    "(*_*)":"Amazed",
    "(*_*;":"Amazed",
    "(+_+) (@_@)":"Amazed",
    "(*^^)v":"Laughing,Cheerful",
    "(^_^)v":"Laughing,Cheerful",
    "((d[-_-]b))":"Headphones,Listening to music",
    '(-"-)':"Worried",
    "(ーー;)":"Worried",
    "(^0_0^)":"Eyeglasses",
    "(＾ｖ＾)":"Happy",
    "(＾ｕ＾)":"Happy",
    "(^)o(^)":"Happy",
    "(^O^)":"Happy",
    "(^o^)":"Happy",
    ")^o^(":"Happy",
    ":O o_O":"Surprised",
    "o_0":"Surprised",
    "o.O":"Surpised",
    "(o.o)":"Surprised",
    "oO":"Surprised",
    "(*￣m￣)":"Dissatisfied",
    "(‘A`)":"Snubbed or Deflated",
    "T_T":"Sad or Crying"

}


def processing(df):
    df['emoticons']=df['SentimentText'].apply(lambda x: ' '.join([EMOTICONS[word] if word in EMOTICONS else word for word in x.split()]))
    
    df['emo']=df['emoticons'].apply(lambda x: ' '.join([EMOTICONS_EMO[word] if word in EMOTICONS_EMO else word for word in x.split()]))
     
#     df['st']= df['emo'].apply(lambda x: ' '.join([word for word in x.split() if word not in stop_words]))
    
    #lowercase
    df['lower_desc'] =df['emo'].str.lower()
    
    
    #change appos
    df['appos']=df['lower_desc'].apply(lambda x: ' '.join([appos[word] if word in appos else word for word in x.split()]))
     #remove#
    df['hash']=df['appos'].apply(lambda x:' '.join(re.sub('#\S+', '', x).split()))
    
    #remove @user
    df['at']=df['hash'].apply(lambda x:' '.join(re.sub('@\S+', '', x).split()))
    
    #remove http
    df['http']=df['at'].apply(lambda x:' '.join(re.sub('http\S+\s*', '', x).split()))
    
    #remove punctuations
    df['processed'] = df['http'].apply(lambda x: re.sub(r'[^\w\s]', '', x.lower()))
    
    #remove punctuations, special characters and numerical tokens 
    df['remove']=df['processed'].apply(lambda x:' '.join( [word for word in x.split() if word.isalpha()]))
    
    #Lemmatization
    df['lemma'] = df['remove'].apply(lambda x: ' '.join([lmtzr.lemmatize(word, "v") for word in x.split(' ')]))
    
    #stopwords
    df['stop']= df['remove'].apply(lambda x: ' '.join([word for word in x.split() if word not in stop_words]))
    
    #remove any duplicate letter that appears more than 2 times in a word
    df['tweet'] =df['stop'].str.replace(r'(\w)\1{%d,}'%(3-1), r'\1')
    
    
    return (df)
new=processing(df)  
def removetext(text):
    return ''.join([i if ord(i) < 128 else '' for i in text])

#Here I am doing the actual removing of text not in ASCII format
new['clear'] = new['tweet'].apply(removetext)
pos_sentence=new[new['Sentiment'] == 1]['clear'].tolist()
neg_sentence=new[new['Sentiment'] == 0]['clear'].tolist()
print(pos_sentence[:10])
sentence=neg_sentence + pos_sentence

num_1=len(new[new['Sentiment'] == 1])
num_0=len(new[new['Sentiment'] == 0])
new.head()
import tensorflow as tf
from tensorflow import keras
print(tf.__version__)

from keras.preprocessing.text import one_hot
from keras.preprocessing.text import text_to_word_sequence
from keras.preprocessing.text import Tokenizer
# mydict=[]
# for i in range(len (new)):
#   mydict.append(new['clear'][i])
word_list = []
for s in sentence:
  words = s.split()
  word_list.extend(words)
  
unique_words = list(set(word_list))
word2ind = {unique_words[i]: i+1 for i in range(len(unique_words))}

word2ind['<PAD>'] = 0

ind2word = dict([(value, key) for (key, value) in word2ind.items()])

vocab_size = len(ind2word)
print("Vocab size: {}".format(vocab_size))
word2ind['hate']
ind2word[20582]
def encode_text(sentence):
  words = sentence.split(' ')
  return [word2ind[word] for word in words if word != '']

print(encode_text('we have two choices'))

def decode_text(text):
  return ' '.join([ind2word.get(i, '?') for i in text])

print(decode_text(encode_text('we have two choices')))
import re
import numpy as np
sentence_data = []

for s in sentence:
  sentence_data.append(encode_text(s))
print(sentence_data[:10])

sentence_data = np.array(sentence_data)
print(sentence_data[:10])

num_pres = 2
pres_names = [0,1]
sentence_labels = np.zeros((len(sentence_data), num_pres))
# pres_names = [0 for negative, 1 for positive]
print(sentence_labels)

print(sentence_labels.shape)

sentence_labels[0:num_0, 0] = 1 # sad
sentence_labels[num_0: num_0+num_1, 1] = 1 # happy

print(sentence_labels[num_0-1]) # negative
print(sentence[num_0-1])
print(sentence_labels[num_0]) # positive
print(sentence[num_0])

print(sentence_labels[num_0+num_1-1]) # positive
print(sentence[num_0+num_1-1])


print(sentence_data.shape)
print(sentence_labels.shape)

rand_ind = np.random.choice(sentence_data.size, sentence_data.size)
X = sentence_data[rand_ind]
y = sentence_labels[rand_ind]


print(y[:10]) #Che
X_train = X[:70000]
y_train = y[:70000]

X_test = X[70000:]
y_test = y[70000:]

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)
X_train = keras.preprocessing.sequence.pad_sequences(X_train, 
                                                     value=word2ind['<PAD>'],
                                                     padding='post',
                                                     maxlen=128)

X_test = keras.preprocessing.sequence.pad_sequences(X_test, 
                                                    value=word2ind['<PAD>'],
                                                    padding='post',
                                                    maxlen=128)
model = keras.Sequential()
model.add(keras.layers.Embedding(vocab_size, 16))
model.add(keras.layers.GlobalAveragePooling1D())
model.add(keras.layers.Dense(16, activation=tf.nn.relu))
model.add(keras.layers.Dense(num_pres, activation=tf.nn.sigmoid))

model.summary()

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])
X_val = X_train[:14000]
y_val = y_train[:14000]

partial_X_train = X_train[14000:]
partial_y_train = y_train[14000:]

checkpoint = keras.callbacks.ModelCheckpoint('model.h5', monitor='val_loss', verbose=0, save_best_only=True, save_weights_only=False, mode='auto', period=5)

history = model.fit(partial_X_train, partial_y_train, batch_size=512, validation_data=(X_val, y_val), callbacks=[checkpoint], epochs=200)

history_dict = history.history
history_dict.keys()

acc = history_dict['acc']
val_acc = history_dict['val_acc']
loss = history_dict['loss']
val_loss = history_dict['val_loss']

epochs = range(1, len(acc) + 1)
import matplotlib.pyplot as plt
# r is for "solid red line"
plt.plot(epochs, loss, 'r', label='Training loss')
# b is for "solid blue line"
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

plt.show()