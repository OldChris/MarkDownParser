<?php
require_once 'MarkdownParser.php';

$parser = new MarkdownParser();
$parser->noheaderfooter();
$htmlContent = $parser->MarkDownParse($file_md);
echo $htmlContent;
//
//  Or use it like this.
$parser->markdown2html('test.md', 'test.html');

echo "Markdown parsed and HTML generated to test.html\n";

// Optionally, display the generated HTML content
echo file_get_contents('test.html');
?>
