#!//usr/bin/python
import os, re, yaml

DOCS = '/docs/'
path = os.path.dirname(os.path.realpath(__file__))
filesList = []

def setAllFiles(dirList, extraPath = "/"):
    for item in dirList:
        if os.path.isfile(path + DOCS + extraPath + "/" + item):
            filesList.append(item)
        else:
            if os.path.isdir(path + DOCS + item):
                tmpDirList = os.listdir(path + DOCS + item)
                setAllFiles(tmpDirList, item)

def findFilePath(name, directory = path + DOCS):
    if os.path.isfile(directory + name):
        return directory + name
    else:
        for dir in os.listdir(directory):
            extraPath = directory + dir

            if os.path.isdir(extraPath):
                if os.path.isfile(extraPath + "/" + name):
                    return extraPath + "/" + name

def getRequiredReferences():
    with open(path + '/mkdocs.yml', 'r') as stream:
        try:
            streamYaml = yaml.safe_load(stream)
            return streamYaml['references']
        except yaml.YAMLError as exc:
            print(exc)

setAllFiles(os.listdir(path + DOCS))
requiredReferences = getRequiredReferences()

page = '<div class="references">'
aAllHeaders = []
H3_ITEMS_COUNT = 30
COLUMN_WIDTH = 205
columnsCount = 1
headersExists = 0
pageTag = ''

def formatH2Tag(name):
    name = name.replace('-', ' ')
    list = name.split()
    resultName = ''

    for index, item in enumerate(list):
        resultName += item.capitalize()

        if index + 1 != len(list):
            resultName += ' '

    return resultName

for file in requiredReferences:
    if filesList.index(file + '.md'):

        pageTag = '\n    <div class="block-section"><div class="page">\n        <h2>' + formatH2Tag(file) + '</h2>\n    </div>\n'

        with open(findFilePath(file + '.md'), 'r') as stream:
            fileContent = stream.read()
            aH2Headers = re.findall(r'\n## ?[a-zA-Z].*', fileContent)

            page += '    <div class="headers">\n'
            for index, header in enumerate(aH2Headers):
                headersExists = 1

                if (index + 1 < len(aH2Headers)):
                    foundBlock = fileContent[fileContent.index(header) + len(header):fileContent.index(aH2Headers[index + 1])]
                else:
                    foundBlock = re.search(r'' + header + '([\s\S]*)', fileContent, flags=0).group(1)

                aAllHeaders.append(re.findall(r'\n## ?([a-zA-Z].*)', header))

                aH3Headers = re.findall(r'\n### ?([a-zA-Z].*)', foundBlock)

                h3Length = len(aH3Headers)

                if h3Length > 15:
                    BIG_CLASS = 'big'
                else:
                    BIG_CLASS = ''

                columnsCount = round(h3Length / H3_ITEMS_COUNT) + 1
                columnsWidth = COLUMN_WIDTH * columnsCount

                page += '\n        <div class="h2-headers ' + BIG_CLASS + '" style="width:' + str(columnsWidth) + 'px">\n            <h4><a href="/creating-manifest/' + file + '/' + header[2:].lower().strip().replace('# ', '#').replace(' ', '-').replace(' ', '') + '">' + header[3:] + '</a></h4>'

                if h3Length:
                    aAllHeaders[index].append(aH3Headers)
                    page += '<div class="columns">'     #columns

                    for ind, h3 in enumerate(aH3Headers):

                        if (ind != 0 and ind % H3_ITEMS_COUNT == 0):
                            page += '</div>'

                        if (ind % H3_ITEMS_COUNT == 0):
                            page += '<div class="column">'

                        localPath = findFilePath(file + '.md').replace('.md', '')
                        localPath = localPath.replace(path + DOCS, '')

                        page += '\n            <div class="h3-headers">'
                        page += '\n	            <a href="/' + localPath + '/#' + h3.lower().strip().replace(' ', '-').replace('*', '') + '">' + h3.replace('*', '') + '</a>'
                        page += '\n            </div>'

                        if ind + 1 == h3Length:
                            page += '</div>'
                    page += '</div>'    #columns
                page += '\n        </div>'
            page += '</div>'
        page += '</div>'


print("aAllHeaders", aAllHeaders)

page += '</div>'

f = open('theme/readthedocs/reference-page.html', 'a')
f.truncate(0)
f.write(page)
f.close()