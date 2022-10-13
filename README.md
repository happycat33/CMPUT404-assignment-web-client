CMPUT404-assignment-web-client
==============================

CMPUT404-assignment-web-client

See requirements.org (plain-text) for a description of the project.

Make a simple web-client like curl or wget

Contributors / Licensing
========================

httpclient.py contains advice/collaboration from:

- beomyoon: Help fix bug involving Get url withy Query but no Params (issue sending url instead of path)
- rmo1: Help me understand the basics of the assignment, the idea of urlencode and bug involving POST request 
  not being accepted (issue was sending POST without headers)
- landberg: Help me with issue with Get request (issues with headers), tips on how to handle params with POST
  requests, helped issue with hanging/freezing on one test function. Gave suggestions for the GET request (how
  to deal with empty path).
- archit2: Helped me understand the basics of the assignment, gave suggestions on how to split response and tips
  on dealing with queries
- hassnai1: Helped understand issues involving virtualhosting, extra imports and functions and helped understand
  that we need to add queries to GET request.

httpclient.py contains code from:

-https://stackoverflow.com/questions/20901768/how-to-encode-a-string-for-url-param-in-python (how to encode a querystring,
 taken from second and third answer)

Generally everything is LICENSE'D under the Apache 2 license by Abram Hindle, 
https://github.com/tywtyw2002, and https://github.com/treedust

But the server.py example is derived from the python documentation
examples thus some of the code is Copyright © 2001-2013 Python
Software Foundation; All Rights Reserved under the PSF license (GPL
compatible) http://docs.python.org/2/library/socketserver.html

