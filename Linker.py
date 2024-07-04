#============================================================================================================================================
# linker.py : Take a link as a commandline argument and update the clipboard to hold the formatted links for posting to Discord.
#============================================================================================================================================
# Imports

# Local imports.
import http
import urllib.request
import re
import sys
import time

# Installed imports.
import pyperclip

#============================================================================================================================================
# Constants

# Find the title in the HTML source.
MATCH_TITLE_START = "<meta property=\"og:title\" content=\""
MATCH_TITLE_END = "\">"
# Find the data link in the HTML source.
MATCH_LINK_START = " data-url=\""
MATCH_LINK_END = "\" "

#============================================================================================================================================
# Main

def main(input_link):
	# Pull the HTML source code from the link, retry on failure.
	page_got = False
	page_handle = None
	while not page_got:
		try:
			page_handle = urllib.request.Request(input_link)
			page_handle.add_header("Cookie", "over18=1")
			page_got = True
		except:
			time.sleep(0.1)
	page_content = urllib.request.urlopen(page_handle).read().decode()
	# Find the relevant information we want.
	page_link = re.search(f"{MATCH_LINK_START}(.*?){MATCH_LINK_END}", page_content).group(1)
	page_title = re.search(f"{MATCH_TITLE_START}(.*?){MATCH_TITLE_END}", page_content).group(1)
	# Minor fixes to formatting issues.
	page_title = page_title.replace("&quot;", "\"")
	page_title = page_title.replace("&amd;", "&")
	page_title = page_title.replace("&amp;", "&")
	# Build out the clipboard string.
	clipboard_text = ""
	clipboard_text += "<" + input_link + ">\n"
	if not page_link.startswith("/r/"):
		clipboard_text += "<" + page_link + ">\n"
	clipboard_text += "```" + page_title + "```"
	# Debug print message to see progress.
	print()
	print(clipboard_text)
	# Update the clipboard with the formatted text.
	pyperclip.copy(clipboard_text)
	return

#============================================================================================================================================
# Run

if __name__ == "__main__":
	main(sys.argv[1])
	sys.exit(0)

#============================================================================================================================================