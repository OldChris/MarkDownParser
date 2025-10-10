<?php

class MarkdownParser {
    private $md_state = [];
    private $md_element = [];
    private $md_marker = [];
    private $HTML_text = '';
    private $include_header_footer=false;

    public function __construct() {
        $this->initStates();
        $this->initElements();
        $this->initMarkers();
    }

    private function initStates() {
        $this->md_state = [
            "Bold" => false,
            "Italic" => false,
            "BoldItalic" => false,
            "InBlockQuote" => false,
            "InOrderedList" => false,
            "InUnorderedList" => false,
            "InCodeBlock" => false,
            "TableActive" => false,
            "TableColumns" => 0,
            "TableRow" => 0,
            "StartMarkedText" => 0,
            "EndMarkedText" => 0,
            "AfterEndMark" => 0,
            "StartMarkedText2" => 0,
            "EndMarkedText2" => 0,
            "MarkIsMatched" => false,
            "MarkMatched" => 0
        ];
    }

    private function initElements() {
        $this->md_element = [
            "header1" => 1,
            "header2" => 2,
            "header3" => 3,
            "bold" => 4,
            "italic" => 5,
            "bolditalic" => 6,
            "orderedlist" => 7,
            "unorderedlist" => 8,
            "horizontalrule" => 9,
            "table" => 10,
            "blockquote" => 11,
            "highlight" => 12,
            "subscript" => 13,
            "superscript" => 14,
            "strikethrough" => 15,
            "code" => 16,
            "link" => 17,
            "color" => 18,
            "none" => 99
        ];
    }

    private function initMarkers() {
        $this->md_marker = [
            "BoldItalicMarker" => "***",
            "BoldMarker" => "**",
            "ItalicMarker" => "*",
            "HighlightMarker" => "==",
            "StrikethroughMarker" => "~~",
            "SubscriptMarker" => "~",
            "SuperscriptMarker" => "^",
            "CodeMarker" => "`",
            "LinkMarker" => "[",
            "LinkMarker2" => "(",
            "ColorMarker" => "$$"
        ];
    }

    private function WriteHTML($text) {
        $this->HTML_text .= $text;
    }

    private function StartOrderedList() {
        if (!$this->md_state["InOrderedList"]) {
            $this->WriteHTML("<ol>\n");
            $this->md_state["InOrderedList"] = true;
        }
    }

    private function EndOrderedList() {
        if ($this->md_state["InOrderedList"]) {
            $this->WriteHTML("</ol>\n");
            $this->md_state["InOrderedList"] = false;
        }
    }

    private function StartUnorderedList() {
        if (!$this->md_state["InUnorderedList"]) {
            $this->WriteHTML("<ul>\n");
            $this->md_state["InUnorderedList"] = true;
        }
    }

    private function EndUnorderedList() {
        if ($this->md_state["InUnorderedList"]) {
            $this->WriteHTML("</ul>\n");
            $this->md_state["InUnorderedList"] = false;
        }
    }

    private function ResetFormatting($currentElement) {
        if ($this->md_state["InOrderedList"] && $currentElement != $this->md_element["orderedlist"]) {
            $this->EndOrderedList();
        }
        if ($this->md_state["InUnorderedList"] && $currentElement != $this->md_element["unorderedlist"]) {
            $this->EndUnorderedList();
        }
        if ($this->md_state["InBlockQuote"] && $currentElement != $this->md_element["blockquote"]) {
            $this->WriteHTML("</blockquote>\n");
            $this->md_state["InBlockQuote"] = false;
        }
        if ($this->md_state["TableActive"] && $currentElement != $this->md_element["table"]) {
            $this->WriteHTML("</tbody></table>\n");
            $this->md_state["TableActive"] = false;
        }
    }

    private function GetSubString($line, $startChar, $endChar) {
        $startPos = strpos($line, $startChar);
        if ($startPos === false) return '';
        $startPos += strlen($startChar);
        $endPos = strpos($line, $endChar, $startPos);
        if ($endPos === false) return '';
        return substr($line, $startPos, $endPos - $startPos);
    }

    private function GetNthSubString($line, $delimiter, $n) {
        $parts = explode($delimiter, $line);
        if (isset($parts[$n])) {
            return trim($parts[$n]);
        }
        return '';
    }

    private function CountCharacter($line, $char) {
        return substr_count($line, $char);
    }

    private function CheckForMark($line, $element) {
        $this->md_state["MarkIsMatched"] = false;
        $this->md_state["StartMarkedText"] = 0;
        $this->md_state["EndMarkedText"] = 0;
        $this->md_state["AfterEndMark"] = 0;
        $this->md_state["MarkMatched"] = $this->md_element["none"];

        $mark = '';
        switch ($element) {
            case $this->md_element["bolditalic"]:
                $mark = $this->md_marker["BoldItalicMarker"];
                break;
            case $this->md_element["italic"]:
                $mark = $this->md_marker["ItalicMarker"];
                break;
            case $this->md_element["bold"]:
                $mark = $this->md_marker["BoldMarker"];
                break;
            case $this->md_element["highlight"]:
                $mark = $this->md_marker["HighlightMarker"];
                break;
            case $this->md_element["subscript"]:
                $mark = $this->md_marker["SubscriptMarker"];
                break;
            case $this->md_element["superscript"]:
                $mark = $this->md_marker["SuperscriptMarker"];
                break;
            case $this->md_element["strikethrough"]:
                $mark = $this->md_marker["StrikethroughMarker"];
                break;
            case $this->md_element["code"]:
                $mark = $this->md_marker["CodeMarker"];
                break;
            case $this->md_element["link"]:
                $mark = "[";
                break;
            case $this->md_element["color"]:
                $mark = $this->md_marker["ColorMarker"];
                break;
            default:
                // print("Unknown element " . $element);
                return false;
        }

        $lenMark = strlen($mark);
        $position_start = strpos($line, $mark);

        if ($position_start === 0) {
            $position_end = strpos($line, $mark, $position_start + $lenMark);
            if ($position_end !== false && $position_end > 1) {
                $this->md_state["MarkIsMatched"] = true;
                $this->md_state["StartMarkedText"] = $position_start + $lenMark;
                $this->md_state["EndMarkedText"] = $position_end;
                $this->md_state["AfterEndMark"] = $position_end + $lenMark - 1;
                return true;
            }
        }
        return false;
    }

    private function CheckForLink($line) {
        $this->md_state["MarkIsMatched"] = false;
        $this->md_state["StartMarkedText"] = 0;
        $this->md_state["EndMarkedText"] = 0;
        $this->md_state["AfterEndMark"] = 0;
        $this->md_state["MarkMatched"] = $this->md_element["none"];

        $mark = "[";
        $lenMark = strlen($mark);
        $position_start = strpos($line, $mark);

        if ($position_start === 0) {
            $position_end1 = strpos($line, "](", $position_start);
            if ($position_end1 !== false && $position_end1 > 1) {
                $position_end2 = strpos($line, ")", $position_end1 + 2);
                if ($position_end2 !== false && $position_end2 > 1) {
                    $this->md_state["MarkIsMatched"] = true;
                    $this->md_state["StartMarkedText"] = $position_start + $lenMark;
                    $this->md_state["EndMarkedText"] = $position_end1 + 1;
                    $this->md_state["StartMarkedText2"] = $position_end1 + 2;
                    $this->md_state["EndMarkedText2"] = $position_end2;
                    $this->md_state["AfterEndMark"] = $position_end2 + $lenMark - 1;
                    return true;
                }
            }
        }
        return false;
    }

    private function Markdown_TextFormatting($line) {
        $lenLine = strlen($line);
        $i = -1;
        while ($i < $lenLine) {
            $i++;
            $linepart = substr($line, $i);

            if ($this->CheckForMark($linepart, $this->md_element["code"])) {
                $this->WriteHTML("<code>" . substr($linepart, $this->md_state["StartMarkedText"], ($this->md_state["EndMarkedText"] - $this->md_state["StartMarkedText"])) . "</code>");
                $i += $this->md_state["AfterEndMark"];
            } elseif ($this->CheckForMark($linepart, $this->md_element["bolditalic"])) {
                $this->WriteHTML("<em><strong>" . substr($linepart, $this->md_state["StartMarkedText"], ($this->md_state["EndMarkedText"] - $this->md_state["StartMarkedText"])) . "</strong></em>");
                $i += $this->md_state["AfterEndMark"];
            } elseif ($this->CheckForMark($linepart, $this->md_element["bold"])) {
                $this->WriteHTML("<strong>" . substr($linepart, $this->md_state["StartMarkedText"], ($this->md_state["EndMarkedText"] - $this->md_state["StartMarkedText"])) . "</strong>");
                $i += $this->md_state["AfterEndMark"];
            } elseif ($this->CheckForMark($linepart, $this->md_element["italic"])) {
                $this->WriteHTML("<em>" . substr($linepart, $this->md_state["StartMarkedText"], ($this->md_state["EndMarkedText"] - $this->md_state["StartMarkedText"])) . "</em>");
                $i += $this->md_state["AfterEndMark"];
            } elseif ($this->CheckForMark($linepart, $this->md_element["highlight"])) {
                $this->WriteHTML("<span style='color:black;background:yellow;'>" . substr($linepart, $this->md_state["StartMarkedText"], ($this->md_state["EndMarkedText"] - $this->md_state["StartMarkedText"])) . "</span>");
                $i += $this->md_state["AfterEndMark"];
            } elseif ($this->CheckForMark($linepart, $this->md_element["strikethrough"])) {
                $this->WriteHTML("<s>" . substr($linepart, $this->md_state["StartMarkedText"], ($this->md_state["EndMarkedText"] - $this->md_state["StartMarkedText"])) . "</s>");
                $i += $this->md_state["AfterEndMark"];
            } elseif ($this->CheckForMark($linepart, $this->md_element["subscript"])) {
                $this->WriteHTML("<sub>" . substr($linepart, $this->md_state["StartMarkedText"], ($this->md_state["EndMarkedText"] - $this->md_state["StartMarkedText"])) . "</sub>");
                $i += $this->md_state["AfterEndMark"];
            } elseif ($this->CheckForMark($linepart, $this->md_element["superscript"])) {
                $this->WriteHTML("<sup>" . substr($linepart, $this->md_state["StartMarkedText"], ($this->md_state["EndMarkedText"] - $this->md_state["StartMarkedText"])) . "</sup>");
                $i += $this->md_state["AfterEndMark"];
            } elseif ($this->CheckForMark($linepart, $this->md_element["color"])) {
                $colorContent = substr($linepart, $this->md_state["StartMarkedText"], ($this->md_state["EndMarkedText"] - $this->md_state["StartMarkedText"]));
                $parts = explode(":", $colorContent, 5);
                $foregroundColor = isset($parts[1]) ? trim($parts[1]) : "";
                $backgroundColor = isset($parts[2]) ? trim($parts[2]) : "";
                $text = isset($parts[3]) ? trim($parts[3]) : "";
                $bgColorCode = ($backgroundColor != "") ? "background-color:" . $backgroundColor . ";" : "";
                $fgColorCode = ($foregroundColor != "") ? "color:" . $foregroundColor . ";" : "";
                
                $this->WriteHTML('<span style="' . $fgColorCode . $bgColorCode . '">' . $text . '</span>');
                $i += $this->md_state["AfterEndMark"];
            } elseif ($this->CheckForLink($linepart)) {
                $linkText = substr($linepart, $this->md_state["StartMarkedText"], ($this->md_state["EndMarkedText"] - $this->md_state["StartMarkedText"] -1)); // -1 to remove the ']' before '(' in the original string
                $linkUrl = substr($linepart, $this->md_state["StartMarkedText2"], ($this->md_state["EndMarkedText2"] - $this->md_state["StartMarkedText2"]));
                $this->WriteHTML('<a href="' . $linkUrl . '">' . $linkText . '</a>');
                $i += $this->md_state["AfterEndMark"];
            } else {
                $this->WriteHTML(substr($linepart, 0, 1));
            }
        }
    }
    private function header_footer($switch)
    {
        if ($switch)
        {
            $this->include_header_footer = false;
        }
    }

    public function MarkDownParse($filename) {
        $this->initStates(); // Reset states for a new parse
        if ($this->include_header_footer)
        {
            $this->HTML_text = "<!doctype html>\n";
            $this->HTML_text .= "<head><style>\n";
            $this->HTML_text .= "body {background-color:#cdeaba;}\n";
            $this->HTML_text .= "mark { background-color: yellow; color: black;}\n";
            $this->HTML_text .= "h1 {  font-size: 34px;}\n";
            $this->HTML_text .= "h2 {  font-size: 28px;}\n";
            $this->HTML_text .= "p {  font-size: 24px;}\n";
            $this->HTML_text .= "</style></head>\n";
            $this->HTML_text .= "<body style=\"font-family: sans-serif\" > \n";
        }
        if (!file_exists($filename)) {
            return "Error: Markdown file not found.";
        }

        $lines = file($filename);  
        $tutorialFolder = dirname($filename);

        foreach ($lines as $line) {
            $line = rtrim($line); // Remove trailing whitespace

            if ($this->md_state["InCodeBlock"]) {
                if (substr($line, 0, 3) == "```") {
                    $this->md_state["InCodeBlock"] = false;
                    $this->WriteHTML("</pre>\n");
                } else {
                    $this->WriteHTML(htmlspecialchars($line) . "\n");
                }
            } elseif (substr($line, 0, 1) == "#") { // Header
                if (substr($line, 0, 4) == "### ") {
                    $this->ResetFormatting($this->md_element["header3"]);
                    $this->WriteHTML("<br><h3>" . substr($line, 4) . "</h3><br>");
                } elseif (substr($line, 0, 3) == "## ") {
                    $this->ResetFormatting($this->md_element["header2"]);
                    $this->WriteHTML("<br><h2>" . substr($line, 3) . "</h2><br>");
                } elseif (substr($line, 0, 2) == "# ") {
                    $this->ResetFormatting($this->md_element["header1"]);
                    $this->WriteHTML("<br><h1>" . substr($line, 2) . "</h1><br>");
                }
            } elseif (preg_match('/^\d+\. /', $line)) { // Ordered List
                $this->StartOrderedList();
                $this->WriteHTML("<li>" . substr($line, strpos($line, '. ') + 2) . "</li>\n");
            } elseif (substr($line, 0, 3) == "---") { // Horizontal Rule
                $this->ResetFormatting($this->md_element["horizontalrule"]);
                $this->WriteHTML("<hr>\n");
            } elseif (substr($line, 0, 2) == "- ") { // Unordered List
                $this->StartUnorderedList();
                $this->WriteHTML("<li>" . substr($line, 2) . "</li>\n");
            } elseif (substr($line, 0, 2) == "> ") { // Block quote
                $this->ResetFormatting($this->md_element["blockquote"]);
                if (!$this->md_state["InBlockQuote"]) {
                    $this->WriteHTML("<blockquote>\n");
                    $this->md_state["InBlockQuote"] = true;
                }
                $this->Markdown_TextFormatting(substr($line, 2));
                $this->WriteHTML("<br>\n");
            } elseif (substr($line, 0, 3) == "```") { // Code Block
                if ($this->md_state["InCodeBlock"]) {
                    $this->md_state["InCodeBlock"] = false;
                    $this->WriteHTML("</pre>\n");
                } else {
                    $this->md_state["InCodeBlock"] = true;
                    $this->WriteHTML("<pre>\n");
                }
            } elseif (substr($line, 0, 2) == "![") { // Image
                $imageAltText = $this->GetSubString($line, "[", "]");
                $imageFilename = $this->GetSubString($line, "(", ")");
                
                // Basic path handling, needs more robust logic for real-world scenarios
                $fullImagePath = $tutorialFolder . '/../images/' . $imageFilename;
                if (!file_exists($fullImagePath)) {
                    $fullImagePath = $tutorialFolder . '/Images/' . $imageFilename;
                }

                $this->WriteHTML("<p><img src='" . $fullImagePath . "' alt='" . $imageAltText . "'></p>\n");
            } elseif (substr($line, 0, 1) == "|") { // Table
                if (!$this->md_state["TableActive"]) {
                    $this->md_state["TableActive"] = true;
                    $this->md_state["TableColumns"] = $this->CountCharacter($line, "|") - 1;
                    $this->md_state["TableRow"] = 1;
                    $this->WriteHTML('<table class="table table-striped table-bordered"><thead class="table-dark"><tr>');
                    for ($iColumn = 1; $iColumn <= $this->md_state["TableColumns"]; $iColumn++) {
                        $this->WriteHTML("<th>" . $this->GetNthSubString($line, "|", $iColumn) . "</th>\n");
                    }
                    $this->WriteHTML("</tr>\n</thead>\n<tbody>\n");
                } else {
                    $this->md_state["TableRow"]++;
                    if ($this->md_state["TableRow"] == 2) { // Separator line, ignore for now
                        // This line typically defines column alignment, which is not parsed here.
                    } else { // Cell data
                        $this->WriteHTML("<tr>\n");
                        for ($iColumn = 1; $iColumn <= $this->md_state["TableColumns"]; $iColumn++) {
                            $this->WriteHTML("<td>");
                            $this->Markdown_TextFormatting($this->GetNthSubString($line, "|", $iColumn));
                            $this->WriteHTML("</td>\n");
                        }
                        $this->WriteHTML("</tr>\n");
                    }
                }
            } else {
                $this->ResetFormatting($this->md_element["none"]);
                $this->Markdown_TextFormatting($line);
                $this->WriteHTML("<br>");
            }
        }

        $this->ResetFormatting($this->md_element["none"]); // Ensure all open tags are closed

        if ($this->include_header_footer )
        {
            $this->HTML_text .= "</body></html>";
        }
        return $this->HTML_text;
    }
    public function noheaderfooter()
    {
        $this->header_footer(false);
    
    }
    public function markdown2html($file_md, $file_html) {
        $htmlContent = $this->MarkDownParse($file_md);
        file_put_contents($file_html, $htmlContent);
    }
}

?>
