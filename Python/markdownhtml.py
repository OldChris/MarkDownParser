import os
import os.path
#  
#
md_state=dict()

md_state = {
    "Bold" : True,
    "Italic"  : True,
    "BoldItalic" : True,
    "InBlockQuote" : True,
    "InOrderedList": True,
    "InUnorderedList" : True,
    "InCodeBlock" : True,
    "TableActive" : True,
    "TableColumns" :0,
    "TableRow" :0,
    "StartMarkedText" : 0,
    "EndMarkedText" : 0,
    "AfterEndMark" : 0,
    "StartMarkedText2"  : 0,
    "EndMarkedText2"  : 0,
    "MarkIsMatched"  : True,
    "MarkMatched"  : 0
        }

md_element=dict()

md_element =  {
    "header1" : 1,
    "header2" : 2,
    "header3" : 3,
    "bold" : 4,
    "italic" : 5,
    "bolditalic" : 6,
    "orderedlist" : 7,
    "unorderedlist" : 8,
    "horizontalrule" : 9,
    "table" : 10,
    "blockquote" : 11,
    "highlight" : 12,
    "subscript" : 13,
    "superscript" : 14,
    "strikethrough" : 15,
    "code" : 16,
    "link" : 17,
    "color" : 18,
    "none" : 99
    }

md_marker=dict()

md_marker = {
    "BoldItalicMarker" : "***",
    "BoldMarker" : "**",
    "ItalicMarker" : "*",
    "HighlightMarker" : "==",
    "StrikethroughMarker" : "~~",
    "SubscriptMarker" : "~",
    "SuperscriptMarker" : "^",
    "CodeMarker" : "`",
    "LinkMarker" : "[",
    "LinkMarker2" : "(",
    "ColorMarker" : "$$"
    
         }

#
HTML_text =''

def Init():
    pass
    global HTML_text
    # set initial states
    md_state["Bold"] = False
    md_state["Italic"] = False
    md_state["BoldItalic"] = False
    md_state["TableActive"] = False
    md_state["InCodeBlock"] = False
    md_state["InOrderedList"] = False
    md_state["InUnorderedList"] = False
    md_state["InCodeBlock"] = False
    md_state["InBlockQuote"] = False


    HTML_text = "<!doctype html>" + '\n'
    HTML_text += "<head><style>table, th, td {  border: 1px solid black;  border-collapse: collapse;}" + '\n'
    HTML_text += "body {background-color:#cdeaba;}" + '\n'
    # 'does not work HTML_text += "tbody tr:nth-child(odd) { background-color: #cdeaba;}" + '\n'
    # 'does not work  HTML_text += "tbody tr:nth-child(even) { background-color: #8acb51;}" + '\n'
    HTML_text += "mark { background-color: yellow; color: black;}" + '\n'
    # '  HTML_text += "font-family: sans-serif;"
    HTML_text += "h1 {  font-size: 34px;}"
    HTML_text += "h2 {  font-size: 28px;}"
    HTML_text += "p {  font-size: 24px;}"
    HTML_text += "</style></head>" + '\n'
    HTML_text += "<body style=""font-family: sans-serif"" > " + '\n'


def FinishHTML():
    global HTML_text
    
    HTML_text += "</body></html>"

def MarkDownParse(filename):
    Init()

    if (not os.path.isfile(filename)):
        pass
    else:        
        TutorialFolder =os.path.dirname(filename)
        TutorialImageFolder = os.path.join(TutorialFolder, "Images")
        LineNumber=0
        with open(filename, "r") as file:
            
            content = file.readlines()
            for line in content:
                LineNumber += 1
                if ( md_state["InCodeBlock"] ):
                    if (line[0:3] == "```"):
                        md_state["InCodeBlock"] = False
                        WriteHTML("</pre>")
                    else:
                        WriteHTML(line)
                        WriteHTML("\r\n")
                elif (line[0:1] == "#"): #'header
                    if (line[0:4] == "### "): #'header 3
                        ResetFormatting(md_element["header3"])
                        WriteHTML("<H3>")
                        WriteHTML(line[4:])
                        WriteHTML("</H3>")
                    if (line[0:3] == "## "): #'header 2
                        ResetFormatting(md_element["header2"])
                        WriteHTML("<H2>")
                        WriteHTML(line[3:])
                        WriteHTML("</H2>")
                    if (line[0:2] == "# "): #'header 1
                        ResetFormatting(md_element["header1"])
                        WriteHTML("<H1>")
                        WriteHTML(line[2:])
                        WriteHTML("</H1>")

                elif ((line[1:2] == ".")): # and (IsANumber(line[0:1]))) :  # 'Ordered List # 
                    if (not md_state["InOrderedList"]):
                        StartOrderedList()
                    WriteHTML("<li>" )
                    WriteHTML(line[3:])
                    WriteHTML("</li>")
                elif ((line[2:3] == ".")): # and (IsANumber(line[0:2]))):  # 'Ordered List
                    if (not md_state["InOrderedList"]):
                        StartOrderedList()
                    WriteHTML("<li>")
                    WriteHTML(line[4:])
                    WriteHTML("</li>")
    
                elif (line[0:3] == "---"):   #' Horizontal Rule
                    ResetFormatting(md_element["horizontalrule"])
                    WriteHTML("<hr>")
    
                elif (line[0:2] == "- "):    # 'Unordered List
                    if (not md_state["InUnorderedList"]):
                        StartUnorderedList()
                    WriteHTML("<li>")
                    WriteHTML(line[2:]) 
                    WriteHTML("</li>")
 
                elif (line[0:2] == "> "):  # ' Block quote
                    ResetFormatting(md_element["blockquote"])

                    if (md_state["InBlockQuote"]):
                        Markdown_TextFormatting(line[2:len(line) - 2])
                        WriteHTML("<br>")
                    else:
                        WriteHTML("<blockquote>")
                        md_state["InBlockQuote"] = True
                        Markdown_TextFormatting(line[2:len(line) - 2])
                        WriteHTML("<br>")
                elif (line[0:2] == "```"): #  ' Block quote
                    if (md_state["InCodeBlock"]):
                        md_state["InCodeBlock"] = False
                        WriteHTML("</pre>")
                    else:
                        md_state["InCodeBlock"] = True
                        WriteHTML("<pre>")
                elif (line[0:2] == "!["):  # ' Image marker
                    ImageAltText = GetSubString(line, "[", "]")
                    
                    TutorialImageFolder = os.path.join(TutorialFolder, "Images")
                    ImageFilename = os.path.join(TutorialFolder,  GetSubString(line, "(", ")"))
                    if (os.path.exists(ImageFilename)):
                        pass
                    else:
                        ImageFilename = os.path.join(TutorialImageFolder , GetSubString(line, "(", ")"))
    
                        if (os.path.exists(ImageFilename)):
                            pass
                        else:
                            pass

                    WriteHTML("<p><img src=" + "'" +  ImageFilename + "'" + " alt=" + "'" + ImageAltText + "'" +  "></p>")
                elif (line[0:1] == "|"): # ' table data
      #                  '  | Syntax      | Description | Test Text     |
     #                   '  | :---        |    :----:   |          ---: |
     #                   '  | Header      | Title       | Here's this   |
     #                   '  | Paragraph   | Text        | And more      |
                    if (md_state["TableActive"]):
                        md_state["TableRow"] += 1
      #                  ' check if column format or cell data
                        if (md_state["TableRow"] == 2):  #'expect column format here
                            pass
                        if (md_state["TableRow"] > 2): #  'cell data
                            WriteHTML("<tr>" + "\r\n")
                            for iColumn  in range(1 , md_state["TableColumns"]+1):
                                WriteHTML("<td>" + "\r\n")
                                Markdown_TextFormatting(GetNthSubString(line, "|", iColumn))
                                WriteHTML("</td>" + "\r\n")
                            WriteHTML("</tr>" + "\r\n")
                    else:
                        md_state["TableActive"] = True
                        md_state["TableColumns"] = CountCharacter(line, "|") -1
                        md_state["TableRow"] = 1
                        WriteHTML("<table>" + "\r\n" + "<thead><tr>")
                        for iColumn in range(1, md_state["TableColumns"]+1):
                            WriteHTML("<th>" + GetNthSubString(line, "|", iColumn) + "</th>")
                        WriteHTML("</tr>" + "\r\n" + "</thead>" + "\r\n" + "<tbody>" + "\r\n")
                elif (line[0:1] == '\\'): 
                    EscapeNext = True
                else:
    #    no more elements, process text for bold, italic, italicbold etc.
                    ResetFormatting(md_element["none"])
                    if (md_state["InOrderedList"]):
                        EndOrderedList()
                    if (md_state["InUnorderedList"]):
                        EndUnorderedList()
                    Markdown_TextFormatting(line)
                    WriteHTML("<br>") 
        if (md_state["InOrderedList"]):
            EndOrderedList()
        if (md_state["InUnorderedList"]):
            EndUnorderedList()

    FinishHTML()
    return HTML_text


def Markdown_TextFormatting(line ):
    currentformatting = md_element["none"]
    lenLine = len(line)
    i=-1
    while  i < lenLine:
        i+=1
        currentformatting = md_element["none"]
        linepart = line[i:]
        if (CheckForMark(linepart, md_element["code"])):
            WriteHTML("<code>" + linepart[md_state["StartMarkedText"]: (md_state["EndMarkedText"] - md_state["StartMarkedText"])] + "</code>")
            i = i + md_state["AfterEndMark"]

        elif (CheckForMark(linepart, md_element["bolditalic"])):
            WriteHTML("<em><strong>" + linepart[md_state["StartMarkedText"]: md_state["EndMarkedText"] ] + "</strong></em>")
            i = i + md_state["AfterEndMark"]
            currentformatting = md_element["bolditalic"]
        elif (CheckForMark(linepart, md_element["bold"])):
            WriteHTML("<strong>" + linepart[md_state["StartMarkedText"]: md_state["EndMarkedText"] ] + "</strong>")
            i += md_state["AfterEndMark"] 
        elif (CheckForMark(linepart, md_element["italic"])):
            WriteHTML("<em>" + linepart[ md_state["StartMarkedText"]: md_state["EndMarkedText"] ] + "</em>")
            i = i + md_state["AfterEndMark"]
        elif (CheckForMark(linepart, md_element["highlight"])):
            WriteHTML("<span style=" + "'" + "color:black;background:yellow;" + "'" + ">" + linepart[ md_state["StartMarkedText"]: md_state["EndMarkedText"] ] + "</span>")
            i = i + md_state["AfterEndMark"]
        elif (CheckForMark(linepart, md_element["strikethrough"])):
            WriteHTML("<s>" + linepart[ md_state["StartMarkedText"]: md_state["EndMarkedText"] ] + "</s>")
            i = i + md_state["AfterEndMark"]
        elif (CheckForMark(linepart, md_element["subscript"])):
            WriteHTML("<sub>" + linepart[ md_state["StartMarkedText"]: (md_state["EndMarkedText"] )] + "</sub>")
            i = i + md_state["AfterEndMark"]
        elif (CheckForMark(linepart, md_element["superscript"])):
            WriteHTML("<sup>" +linepart[md_state["StartMarkedText"]: (md_state["EndMarkedText"] )] + "</sup>")
            i += md_state["AfterEndMark"] 
            
        elif (CheckForMark(linepart, md_element["color"])):
            colorLine = linepart[ md_state["StartMarkedText"]: md_state["EndMarkedText"] ]
            ForegroundColor = GetNthSubString(colorLine, ":", 1)
            BackgroundColor = GetNthSubString(colorLine, ":", 2)
            Text = GetNthSubString(colorLine, ":", 3)
            if (BackgroundColor != ""):
                bg_colorcode= "background:" + BackgroundColor + ";"
            else:
                bg_colorcode=""
            if (ForegroundColor != ""):
                fg_colorcode= "color:" + ForegroundColor + ";"
            else:
                fg_colorcode=""
            WriteHTML("<span style='" + fg_colorcode + bg_colorcode +  "'>" + Text + "</span>")
            i += md_state["AfterEndMark"]
        elif (CheckForLink(linepart)):
            part1 = linepart[md_state["StartMarkedText"]: (md_state["EndMarkedText"] - md_state["StartMarkedText"])]
            part2 = linepart[md_state["StartMarkedText2"]: md_state["EndMarkedText2"] ]
            WriteHTML("<a href=" + "'" + part2 + "'" + ">" + part1 + "</a>")
            i = i + md_state["AfterEndMark"]
        elif (linepart[0:0] == "\\"):
                WriteHTML(linepart[1:1])
                i = i + 1
        else:
            pass
            a=md_element["italic"]
            if (currentformatting == md_element["bolditalic"]):
                pass
            elif (currentformatting == md_element["italic"]):
                    pass
            elif (currentformatting == md_element["bold"]):
                    pass
            elif (currentformatting == md_element["highlight"]):
                    pass
            elif (currentformatting == md_element["subscript"]):
                    pass
            elif (currentformatting == md_element["superscript"]):
                    pass
            elif (currentformatting == md_element["none"]):
                    pass
                    WriteHTML(linepart[0:1])
            else:
                    pass

        
    return 
   

def CheckForMark(Line , element ): 
    Result = False

    md_state["MarkIsMatched"] = False
    md_state["StartMarkedText"] = 0
    md_state["EndMarkedText"] = 0
    md_state["AfterEndMark"] = 0
    md_state["MarkMatched"] = md_element["none"]

    if (element == md_element["bolditalic"]):
        Mark = md_marker["BoldItalicMarker"]
    elif (element == md_element["italic"]):
        Mark = md_marker["ItalicMarker"]
    elif (element == md_element["bold"]):
        Mark = md_marker["BoldMarker"]
    elif (element == md_element["highlight"]):
        Mark = md_marker["HighlightMarker"]
    elif (element == md_element["subscript"]):
        Mark = md_marker["SubscriptMarker"]
    elif (element == md_element["superscript"]):
        Mark = md_marker["SuperscriptMarker"]
    elif (element == md_element["strikethrough"]):
        Mark = md_marker["StrikethroughMarker"]
    elif (element == md_element["code"]):
        Mark = md_marker["CodeMarker"]
    elif (element == md_element["link"]):
        Mark = "["
    elif (element == md_element["color"]):
        Mark = md_marker["ColorMarker"]
    else:
        print("Unknown element ", element)


    lenLine = len(Line)
    lenMark = len(Mark)
    position_start = Line.find(Mark)
    
    if (position_start == 0):
        position_end = Line.find(Mark,position_start + lenMark)
        if (position_end > 1):
            md_state["MarkIsMatched"] = True
            Result = True
            md_state["StartMarkedText"] = position_start + lenMark
            md_state["EndMarkedText"] = position_end
            md_state["AfterEndMark"] = position_end + lenMark -1
            

    return Result
  
    
def CheckForLink(Line):
    Result = False

    md_state["MarkIsMatched"] = False
    md_state["StartMarkedText"] = 0
    md_state["EndMarkedText"] = 0
    md_state["AfterEndMark"] = 0
    md_state["MarkMatched"] = md_element["none"]

    Mark = "["
    lenLine = len(Line)
    lenMark = len(Mark)
    position_start = Line.find(Mark)
    if (position_start == 0):
        position_end1 = Line.find("](", position_start)
        if (position_end1 > 1):
            position_end2 = Line.find(")", position_end1+2)
            if (position_end2 > 1):
                md_state["MarkIsMatched"] = True
                Result = True
                md_state["StartMarkedText"] = position_start + lenMark
                md_state["EndMarkedText"] = position_end1+ 1
                md_state["StartMarkedText2"] = position_end1 + 2
                md_state["EndMarkedText2"] = position_end2
                md_state["AfterEndMark"] = position_end2 + lenMark - 1

    return Result



def ResetFormatting(CurrentFormat):
    if (md_state["InOrderedList"]):
        if (CurrentFormat != md_element["orderedlist"]):
            EndOrderedList()
    if (md_state["InUnorderedList"]):
        if (CurrentFormat != md_element["unorderedlist"]):
            EndUnorderedList()
    if (md_state["TableActive"] == True):
        if (CurrentFormat != md_element["table"]):
            WriteHTML("</tbody></table>")
            md_state["TableActive"] = False
    if (md_state["InBlockQuote"] ):
        if (CurrentFormat != md_element["blockquote"]):
            WriteHTML("</p>")
            WriteHTML("</blockquote>")
            md_state["InBlockQuote"] = False
 
def StartOrderedList():
    WriteHTML("<ol>")
    md_state["InOrderedList"] = True

def StartUnorderedList():
    WriteHTML("<ul>")
    md_state["InUnorderedList"] = True

def EndUnorderedList():
    WriteHTML("</ul>")
    md_state["InUnorderedList"] = False

def EndOrderedList():
    WriteHTML("</ol>")
    md_state["InOrderedList"] = False


def CountCharacter(value, ch ):
    cnt = 0
    for c in value:
        if (c == ch):
            cnt += 1
    return cnt

def GetNthSubString(text, Delimiter , Nth):
    result = ""
    cnt = 0

    iStart = -1
    for c in text:
        iStart += 1
        if (c == Delimiter):
            cnt += 1
            if (cnt == Nth):
                break
    iEnd = text.find(Delimiter, iStart+1)
    if (iEnd > iStart):
        result = text[iStart +1: iEnd]
    return result


def GetSubString(text , StartMarker, EndMarker): 
    result = ""
    iStart = text.find(StartMarker)
    iEnd = text.find(EndMarker)
    if (iStart > 0 and iEnd > iStart):
        result = text[iStart + 1 :iEnd ]
    return result


def RemoveEscape(line):
    Escape  = "\\"
    lenLine = len(line)
    Result = ""
    for i in range( 1 , lenLine - 1):
        print(" line [" + i + "]  " +line[ i: 1])
        if (line[i: 1] == Escape):
            if (line[i + 1:1] == Escape):
                pass
            else:
                Result += line[i + 1: 1]
        else:
            Result += line[ i, 1]
    return Result


def IsANumber(text):
    print("text=", text,sep="")
    if (text.isnumeric()):
        Result = True
    else:
        Result = False
    return Result

def  WriteHTML(Text):
    global HTML_text
    HTML_text += Text


def markdown2html(file_md, file_html):
    HTML=MarkDownParse(file_md)

    if os.path.exists(file_html):
        os.remove(file_html)
    with open(file_html, "w") as f:
        f.write(HTML)
    

def main():
    markdown2html('test.md', 'test.html')

if __name__ == '__main__':
    main()
