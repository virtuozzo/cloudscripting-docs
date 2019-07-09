#!//usr/bin/python
# -*- coding: utf-8 -*-
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
fileNameConfig = ''
extraPages = ''
placeholderBlock = 0
hrefValue = ''
hide2hTag = ''

def formatH2Tag(name):
    name = name.replace('-', ' ')
    list = name.split()
    resultName = ''

    for index, item in enumerate(list):
        resultName += item.capitalize()

        if index + 1 != len(list):
            resultName += ' '

    return resultName

def initConfigParams(config):
    for key in config:
        if key == 'hideh2Tag':
            global hide2hTag
            hide2hTag = True

def resetConfigParams():
    global hide2hTag
    hide2hTag = False

def addExtraPages():
    extraContent = ''

    for fileName in extraPages:

        with open(findFilePath(fileName + '.md'), 'r') as stream:
            fileContent = stream.read()
            aH2Headers = re.findall(r'\n## ?[a-zA-Z].*', fileContent)

        for index, header in enumerate(aH2Headers):

            if "What’s next" in header[3:]:
                continue

            if (index + 1 < len(aH2Headers)):
                foundBlock = fileContent[fileContent.index(header) + len(header):fileContent.index(aH2Headers[index + 1])]
            else:
                foundBlock = re.search(r'' + header + '([\s\S]*)', fileContent, flags=0).group(1)

            aAllHeaders.append(re.findall(r'\n## ?([a-zA-Z].*)', header))

            aH3Headers = re.findall(r'\n### ?([a-zA-Z].*)', foundBlock)

            if aH3Headers == '':
                aH3Headers = re.findall(r'\n###### ?([a-zA-Z].*)', foundBlock)

            if aH3Headers:
                h3Length = len(aH3Headers)

            if h3Length > 15:
                BIG_CLASS = 'big'
            else:
                BIG_CLASS = ''

            columnsCount = round(h3Length / H3_ITEMS_COUNT) + 1
            columnsWidth = COLUMN_WIDTH * columnsCount

            if h3Length == 0:
                extraContent += '\n        <div class="" >'
            if h3Length:
                extraContent += '\n        <div class="h2-headers ' + BIG_CLASS + '" style="width:' + str(columnsWidth) + 'px">\n            '

                if hide2hTag != True:
                    extraContent += '<h4><a href="/creating-manifest/' + fileName + '/' + header[2:].lower().strip().replace('# ', '#').replace(' ', '-').replace(' ', '') + '">' + header[3:] + '</a></h4>'

                # if h3Length:
                aAllHeaders[index].append(aH3Headers)
                extraContent += '<div class="columns">'     #columns

                for ind, h3 in enumerate(aH3Headers):
                    if (ind != 0 and ind % H3_ITEMS_COUNT == 0):
                        extraContent += '</div>'

                    if (ind % H3_ITEMS_COUNT == 0):
                        extraContent += '<div class="column">'

                    localPath = findFilePath(fileName + '.md').replace('.md', '')
                    localPath = localPath.replace(path + DOCS, '')


                    extraContent += addH3Tag(h3)

                    if ind + 1 == h3Length:
                        extraContent += '</div>'
                extraContent += '</div>'    #columns
            extraContent += '\n        </div>'

    return extraContent



def addH3Tag(h3):
    result = ''

    if placeholderBlock is 1:
        hrefValue = re.sub(r'[${()}.]', '', h3)
    else:
        hrefValue = h3
    result += '\n            <div class="h3-headers">'
    result += '\n	            <a href="/' + localPath + '/#' + hrefValue.lower().strip().replace(' ', '-').replace('*', '') + '">' + h3.replace('*', '') + '</a>'
    result += '\n            </div>'

    return result

for file in requiredReferences:

    if type(file) is dict:
        for key in file:
            fileName = key
            if 'params' in file[key].keys():
                fileNameConfig = file[key]['params']
            else:
                fileNameConfig = ''

            if 'extraPages' in file[key].keys():
                extraPages = file[key]['extraPages']
            else:
                extraPages = ''
    else:
        fileName = file
        fileNameConfig = ''

    if fileNameConfig:
        initConfigParams(fileNameConfig)
    else:
        resetConfigParams()

    if filesList.index(fileName + '.md'):

        pageTag = '\n    <div class="block-section"><div class="page">\n        <h2>' + formatH2Tag(fileName) + '</h2>\n    </div>\n'
        page += pageTag

        with open(findFilePath(fileName + '.md'), 'r') as stream:
            fileContent = stream.read()
            aH2Headers = re.findall(r'\n## ?[a-zA-Z].*', fileContent)

            print('fileName', fileName)

            if fileName == 'placeholders':
                placeholderBlock = 1
            else:
                placeholderBlock = 0

            page += '    <div class="headers">\n'

            for index, header in enumerate(aH2Headers):
                if "What’s next" in header[3:]:
                    continue

                headersExists = 1

                if (index + 1 < len(aH2Headers)):
                    foundBlock = fileContent[fileContent.index(header) + len(header):fileContent.index(aH2Headers[index + 1])]
                else:
                    foundBlock = re.search(r'' + header + '([\s\S]*)', fileContent, flags=0).group(1)

                aAllHeaders.append(re.findall(r'\n## ?([a-zA-Z].*)', header))

                aH3Headers = re.findall(r'\n### ?([a-zA-Z].*)', foundBlock)

                if aH3Headers == '' or fileName == 'placeholders':
                    aH3Headers = re.findall(r'###### ?`([${a-zA-Z._(\\*0-9)}]*)', foundBlock)

                h3Length = len(aH3Headers)

                if h3Length > 15:
                    BIG_CLASS = 'big'
                else:
                    BIG_CLASS = ''

                columnsCount = round(h3Length / H3_ITEMS_COUNT) + 1
                columnsWidth = COLUMN_WIDTH * columnsCount

                if h3Length == 0:
                    page += '\n        <div class="" >'
                if h3Length:
                    page += '\n        <div class="h2-headers ' + BIG_CLASS + '" style="width:' + str(columnsWidth) + 'px">\n            '

                    if hide2hTag != True:
                        page += '<h4><a href="/creating-manifest/' + fileName + '/' + header[2:].lower().strip().replace('# ', '#').replace(' ', '-').replace(' ', '') + '">' + header[3:] + '</a></h4>'

                    aAllHeaders[index].append(aH3Headers)
                    page += '<div class="columns">'     #columns

                    for ind, h3 in enumerate(aH3Headers):
                        if (ind != 0 and ind % H3_ITEMS_COUNT == 0):
                            page += '</div>'

                        if (ind % H3_ITEMS_COUNT == 0):
                            page += '<div class="column">'

                        localPath = findFilePath(fileName + '.md').replace('.md', '')
                        localPath = localPath.replace(path + DOCS, '')

                        page += addH3Tag(h3)

                        if ind + 1 == h3Length:
                            page += '</div>'
                    page += '</div>'    #columns
                page += '\n        </div>'


            if extraPages:
                page += addExtraPages()

            page += '</div>'
        page += '</div>'

page += '</div>'

f = open('theme/readthedocs/reference-page.html', 'a')
f.truncate(0)
f.write(page)
f.close()