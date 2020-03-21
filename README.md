# ofrip
ofrip - OnlyFans ripper

You supply the HTML, this grabs all the files for you and names them appropriately.  It scrapes the OnlyFans account name, title, date/time to generate the file names.

This will grab whatever is on the page.

1. Log into whomever's OnlyFan page
2. Keep hitting pagedown / end key to load all content
3. Right-click anywhere on the page, then `Inspect` to open dev console
4. In the `Elements` tab, locate the `div` with class name `user_posts`
5. Right-click on `<div class="user_posts">`, then `Copy outerHTML`

![](https://i.imgur.com/PPRQ1xA.png)

6. Save copied HTML to a text file, name it whatever and save it somewhere (probably in the same location as the python file)
7. With python3, run ofrip.py
	`python ofrip.py 'pathToHtmlFile'`
8. Both images and videos will be downloaded into the `dl` folder on the same directory as the `ofrip.py` file
