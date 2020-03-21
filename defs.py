from bs4 import BeautifulSoup
import requests
import os
import string
import datetime

prct = 1

def reset_prct():
    global prct
    prct = 1

def pr(msg):
    global prct
    print(f"{str(prct).zfill(5)} | {msg}")
    prct += 1

def getVid(downloadit, par_div, name):

    vidstr = par_div.find("video")
    vidurl = ""

    if not vidstr.has_attr("src"):
        vidurl = vidstr.find('source')["src"]
    else:
        vidurl = vidstr["src"]

    outfile = os.path.join("dl", name + '.mp4')

    pr(outfile)

    if downloadit:
        if not os.path.isfile(outfile): 
            # print(vidurl)
            myfile = requests.get(vidurl)
            open(outfile, 'wb').write(myfile.content)

def getPics(downloadit, par_div, name):

    picdivs = par_div.findAll("div", {"class": "swiper-slide"})

    if picdivs is None:
        return

    imgcoll = []
    picno = 1
    for picdiv in picdivs:
        imgurl = picdiv.img["src"]
        if imgurl not in imgcoll:
            imgcoll.append(imgurl)

    for imgurl in imgcoll:
        picfile = os.path.join("dl", name + ' - ' + str(picno).zfill(3) + '.jpg')
        picno += 1
        pr(picfile)
        if downloadit:
            if not os.path.isfile(picfile): 
                myfile = requests.get(imgurl)
                open(picfile, 'wb').write(myfile.content)


def titleFix(tit):

    tit = "" if tit is None else tit.p.text
    tit = tit.replace('\n', ' ')
    tit = tit.replace('\t', ' ').strip()

    valid_chars = "!,-_.() %s%s" % (string.ascii_letters, string.digits)
    newtit = ''.join(c for c in tit if c in valid_chars)

    if len(newtit) > 70:
        newtitarr = newtit.split(' ')
        newtit = ''

        ct = 0
        while len(newtit) < 70:
            newtit += newtitarr[ct] + ' '
            ct += 1

        newtit += '...'

    return newtit

def dtFix(dt, dtstr):

    if len(dtstr.strip()) > 0:
        dtparts = dt.strip().split(',')

        if len(dtparts) == 2:

            dt = dtparts[0].strip()
            tm = dtparts[1].strip()

            if "," in dtstr:
                dt += ", " + dtstr.split(',')[1].strip()
            else:
                dt += ", " + str(datetime.datetime.now().year)

            dttm = datetime.datetime.strptime(dt + ' ' + tm, "%b %d, %Y %I:%M %p")
    else:
        return ""

    return f"{dttm.year}-{str(dttm.month).zfill(2)}-{str(dttm.day).zfill(2)} {str(dttm.hour).zfill(2)}-{str(dttm.minute).zfill(2)}"

def getAll(downloadit, par_div):

    if not os.path.isdir('dl'):
        os.mkdir('dl')

    for div in par_div:

        # print(div.prettify())

        who = div.find("div", {"class": "g-user-name"}).text.strip()
    
        dt = div.find("a", {"class": "b-post__date"}).span
        dtstr = dt["title"]
        dtstrtxt = dt.text.strip()

        # work dtstr
        dtstr = dtFix(dtstr, dtstrtxt)
    
        tit = div.find("div", {"class": "b-post__text"})
        # work tit
        tit = titleFix(tit)

        vid = div.find("div", {"class": "video-wrapper"})

        isVid = vid is not None

        #print(who.strip())
        #print(dtstr.strip().replace(':', '_'))
        #print("     -- Video" if isVid else "     -- Pics")
        #print(tit.strip())

        #title = [(f"{who} - {dtstr}"), f" - {tit}" if len(tit.strip()) > 0 else ""]
        title = (f"{who} - {dtstr}")
        title += f" - {tit}" if len(tit.strip()) > 0 else ""

        if isVid:
            getVid(downloadit, div, title)
        else:
            getPics(downloadit, div, title)
