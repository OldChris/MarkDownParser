# MarkDownParser
A Markdown parser

This repo contains MD parsers for Python and PHP

##Key features

- The PHP parser can handle **relative image paths** so you can relocate your .md files and related image file to any location on your website without breaking image references.
- supports **text colors** (foreground, background)
- The PHP parses uses Bootstrap 5 tables  

## To Do
- Table: text align [left,center, right] to be implemented


## Current supported feautures

The following tags are supported:

# Title
## Paragraph
### Sub Paragraph

### Italic / Bold / Bold-Italic
`Italic *Italic text*, ` 
`Bold  **Bold text** and  `
`Bold-Italic ***Bold-Italic text***  `

Italic *Italic text*,  
Bold  **Bold text** en  
Bold-Italic ***Vet-Cursieve tekst***  
### Horizontale line
`  Horizontal rule  ---    `
---

### Ordered list
` 1. First item  `
` 2. Second item  `
` 3. Third item  `
1. First item  
2. Second item 
3. Third item  


### Unordered list
` - First item `
` - Second item `
` - Third item `
- First item 
- Second item 
- Third item 

### Image
` ![alt text](images/sgc2020.jpeg)  `
![alt text](images/sgc2020.jpeg) 

### Blockquote
` > this is a text `
` > in blockquote  `
> this is a text
> in blokquote

### Highlight
` Highlight  ==highlighted text==  `
Highlight  ==highlighted text== 

### Subscript
` H~2~O   `
H~2~O

### Superscript
` Trademark^TM^ ` 
Trademark^TM^ 

### Strikethrough
` The earth ~~is flat~~ `
The earth ~~is flat~~  

### Code (inline)
` Code backquote  code text backquote

### Code Block
`  3 backquotes  start code block `

```
let message = 'Hello world';
alert(message);


```
`  3 backquotes  ends code block `
### Table
` | First name | Last name |  `
` | ----------- | ----------- | `
` | John |Doe  | `
` | Peter |Smith | ` 
` | Julia | **Jones** | `
` | Jane  $$:red:blue:Miller:$$|  `

| First name | Last name | 
| ----------- | ----------- | 
| John |Doe  | 
| Peter |Smith | 
| Julia | **Jones** | 
| Jane  |Miller| 


### Link
` here is a link [dws website](https://dws.pa7rhm.nl) to the DWS website `
here is a link [dws website](https://dws.pa7rhm.nl) to the DWS website

### Color  (not yet supported by Github Flavored Markdown)
`   this is $$:red:blue:red text:$$ on a blue background  `
`   this is $$:red::red text:$$   red text  `
`   this is $$:black:red:black text:$$ on a red background   `
`   this is $$:red:red:--------------:$$  red bar `

  this is $$:red:blue:red text:$$ on a blue background
  this is $$:red::red text:$$   red text
  this is $$:black:red:black text:$$ on a red background
  this is $$:red:red:--------------:$$  red bar





More to follow soon.
