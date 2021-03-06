#!/usr/local/bin/python
import argparse
import os
import math


# returns a DirInfo list with all subfolders of dirpath
def create_badges(svgpath, csvpath, outpath, ncolumns=0, pdf=False):

    svgTemplate = load_file(svgpath)
    csvFile = load_file(csvpath)

    # early break?
    if svgTemplate is None or csvFile is None:
        return None

    outpath = os.path.normpath(outpath)

    if not os.path.exists(outpath):
        print("Sorry, " + outpath + " is not a valid output folder...")
        return None

    aList = read_csv(csvFile)

    if len(aList.data) == 0:
        print("empty attendee list...")
        return

    # read svg
    svgData = svgTemplate.read()

    if not check_keywords(svgData, aList.keywords):
        return

    # create the badge svg pages
    replace_svg(aList, svgData, outpath, 'badges', pdf)

    # create reverse side
    if ncolumns > 0:

        # fill up the last row
        lr = len(aList.data) % ncolumns + 1
        for cIdx in range(0, lr):
            aList.data.append(aList.data[0])

        # shuffle the attendee list to match recto/verso
        rd = list(aList.data)
        for cIdx in range(0, len(aList.data)):

            cRow = math.floor(cIdx/ncolumns)
            nIdx = cRow*ncolumns + (ncolumns-1) - cIdx % ncolumns

            if nIdx >= len(rd):
                continue

            # permutate for short-side reverse printing
            rd[nIdx] = aList.data[cIdx]

        rList = aList
        rList.data = rd

        replace_svg(rList, svgData, outpath, 'badges-rv')


def replace_svg(aList, svgData, outpath, filename, pdf):

    pageIdx = 0
    cPage = svgData

    for aIdx in range(0, len(aList.data)):
        attendee = aList.data[aIdx]

        for idx in range(0, len(aList.keywords)):
            kw = aList.keywords[idx]

            # ignore empty keywords
            if kw == '':
                continue
            if idx >= len(attendee):
                print("could not find entry for " + kw +
                      " in line " + str(aIdx) + ": " + str(attendee))
                continue

            val = attendee[idx]

            # normalize names
            names = val.split(',')
            if kw == '#name' and len(names) == 2:
                val = names[1].strip() + " " + names[0].strip()

            val = normalize(val)

            # now replace the keyword with the current field value
            nPage = cPage.replace(kw, val, 1)

            # is the page full already?
            if nPage == cPage:
                op = os.path.join(outpath, filename + "-" +
                                  str(pageIdx))
                pageIdx += 1

                save(cPage, op, pdf)

                # get fresh svg & replace current string again
                cPage = svgData
                nPage = cPage.replace(kw, val, 1)

            cPage = nPage

    # save last page if it's still open
    if cPage != svgData:
        op = os.path.join(outpath, filename + "-" +
                          str(pageIdx))

        save(cPage, op, pdf)


def check_keywords(svgData, keywords):

    if len(keywords) == 0:
        print('ERROR: keywords are empty...')
        print("""they should be in the first line of the csv file
              (e.g. #name; #company)""")
        return False

    # check keyword format
    for idx in range(0, len(keywords)):
        kw = keywords[idx]
        if not kw == '' and not kw.startswith('#'):
            print("illegal keyword: " + kw)
            print("NOTE: all keywords must start with # (e.g. #name)")
            return False
        if not kw == '' and kw not in svgData:
            print("could not find " + kw + " in the svg template...")
            print("\t...ignoring (NOTE: it's case sensitive)")
            # remove illegal keywords
            keywords[idx] = ''

    return True


def read_csv(csvFile):
    import csv

    reader = csv.reader(csvFile, delimiter=";")
    reader = list(reader)

    return CsvData(reader[:1], reader[1:])


def normalize(str):

    # replace illegal characters (XML)
    str = str.replace('&', '&amp;');

    return str


# loads files, returns NULL if the file could not be loaded
def load_file(filepath):

    try:
        file = open(filepath, "r", encoding='utf-8')
        return file
    except:
        print("Sorry, I could not load " + filepath)

    return None


def save(content, dstpath: str, pdf: bool = False):

    svgpath = dstpath + ".svg"

    if save_svg(svgpath, content) and not pdf:
        print(svgpath + " saved...")

    if pdf:
        pdfpath = dstpath + ".pdf"
        if save_pdf(svgpath, pdfpath):
            print(pdfpath + " saved...")

def save_svg(filepath, svgData):
    import sys

    try:
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(svgData)
    except:
        print("Sorry, I could not save " + filepath)
        print(sys.exc_info()[0])
        return False

    return True

def save_pdf(src: str, dst: str):
    import sys
    from svglib.svglib import svg2rlg
    from reportlab.graphics import renderPDF

    try:
        graphics = svg2rlg(src)
        renderPDF.drawToFile(graphics, dst)
    except:
        print("Sorry, I could not save " + dst)
        print(sys.exc_info()[0])
        return False

    return True

class CsvData(object):
    def __init__(self, keywords, data):

        # get keywords (flat)
        self.keywords = [val for sublist in keywords for val in sublist]
        self.data = data

if __name__ == "__main__":

    # argument parser
    parser = argparse.ArgumentParser(description="""Creates conference
                        badges from a svg template.""")

    parser.add_argument('svg', metavar='svg-path', type=str,
                        help='path to svg template')
    parser.add_argument('csv', metavar='csv-path', type=str,
                        help="""path to the csv attendee list""")
    parser.add_argument('savepath', metavar='save-path', type=str,
                        help="""path to the output directory""")

    # options:
    parser.add_argument('--back', default="0", type=int,
                        metavar="number-of-columns",
                        help="""specifies the number of columns,
                        if > 0, an svg for the reverse page is created too""")

    parser.add_argument('--pdf', action="store_true",
                        help="""if set, pdfs are created.""")

    # get args and make a dict from the namespace
    args = vars(parser.parse_args())

    # write print to log file
    # NOTE: the crawling is still reported to the cmd since these are processes
    # this is (at least for now) ok
    # oldSysOut = sys.stdout
    # if args['log']:
    #     dstr = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    #     logName = "".join(("create-database-", dstr, ".log"))
    #     logFile = open(logName, "w")
    #     sys.stdout = logFile

    # do the job
    create_badges(args['svg'], args['csv'], args['savepath'], args['back'], args['pdf'])

    print("In order to succeed, we must first believe that we can.")
    print("\t - Nikos Kazantzakis")
