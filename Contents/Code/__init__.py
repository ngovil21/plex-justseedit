TITLE = 'justseed.it'
PREFIX = '/video/justseed'

ART = 'art-default.jpg'
ICON = 'icon-default.png'

BASE_URL = 'https://www.justseed.it/'
API_URL = "https://api.justseed.it"


def Start():
    ObjectContainer.title1 = TITLE
    ObjectContainer.art = R(ART)

    DirectoryObject.thumb = R(ICON)
    DirectoryObject.art = R(ART)
    EpisodeObject.thumb = R(ICON)
    EpisodeObject.art = R(ART)
    VideoClipObject.thumb = R(ICON)
    VideoClipObject.art = R(ART)


@handler(PREFIX, TITLE, art=ART, thumb=ICON)
def MainMenu():
    oc = ObjectContainer()

    # Below is a basic example of a list of three object containers that returns an icon to the screen with a title.
    # In this version we just hardcoded in the sections we would like to break the videos into based on the types of functions
    # that will be described below. I am using a function from below that pulls the thumb from the head of the page
    if not Prefs["api_key"]:
        oc.add(PrefsObject(title='Preferences', thumb=R(ICON), art=R(ART)))
    else:
        labels = getLabels()
        for label in labels:
            oc.add(DirectoryObject(key=Callback(ShowTorrents, label=label), title=label))

    if len(oc) == 0:
        return ObjectContainer(header=TITLE, message="Error loading menu!")

    return oc

@route(PREFIX + "/showtorrents")
def ShowTorrents(label):

    oc = ObjectContainer()
    xml = getURLXml("/torrents/list.csp")
    if not xml:
        return ObjectContainer(header=TITLE, message="Unable to load torrents!")
    rows = xml.xcode("//row")
    if label == "[Unlabeled]":
        label = ""

    for row in rows:
        if getFirstData(row, "label") == label:
            title = getFirstData(row, "name")
            info_hash = getFirstData(row, "info_hash")
            oc.add(DirectoryObject(key=Callback(ShowTorrentFiles, title=title, info_hash=info_hash), title=title))

    if len(oc) == 0:
        return ObjectContainer(header=TITLE, message="Error loading torrents!")

    return oc


@route(PREFIX + "/showtorrent")
def ShowTorrentFiles(title, info_hash):
    pass


def getFirstData(xml, tag):
    element = xml.xcode("//" + tag)
    if element and element[0].text:
        return element[0].text
    return ""


def getLabels():
    xml = getURLXml('/labels/list.csp')
    rows = xml.getElementsByTagName("row")
    labels = []
    for row in rows:
        labels.append(getFirstData(row, "label"))
    labels.append("[Unlabeled]")
    return labels


def getURLXml(url, values=None):
    if not url.startswith("http"):
        url = API_URL_URL + url

    values['api_key'] = Prefs["api_key"]

    xml = XML.ObjectFromURL(url=url, values=values)
    #status = xml.getElementsByTagName("status")[0]
    status = xml["status"]
    if status and status.firstChild.data == "SUCCESS":
        return xml
    return None
