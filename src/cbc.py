#!/usr/local/bin/python
import argparse
import codecs


# returns a DirInfo list with all subfolders of dirpath
def create_badges(svgpath, csvpath, outpath, ncolumns):
    import os

    svgTemplate = load_file(svgpath)
    csvFile = load_file(csvpath)

    # early break?
    if svgTemplate is None or csvFile is None:
        return None

    outpath = os.path.normpath(outpath)

    if not os.path.exists(outpath):
        print("Sorry, " + outpath + " is not valid...")
        return None

    aList = read_csv(csvFile)

    print(aList.keywords)
    print(aList.data)

    print("seems to be working...")


def read_csv(csvFile):
    import csv

    reader = csv.reader(csvFile, delimiter=";")
    reader = list(reader)

    return CsvData(reader[:1], reader[1:])


# loads files, returns NULL if the file could not be loaded
def load_file(filepath):

    try:
        file = open(filepath, "r", encoding='utf-8')
        return file
    except:
        print("Sorry, I could not load " + filepath)

    return None


class CsvData(object):
    def __init__(self, keywords, data):
        self.keywords = keywords
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
    create_badges(args['svg'], args['csv'], args['savepath'], args['back'])

    print("In order to succeed, we must first believe that we can.")
    print("\t - Nikos Kazantzakis")
