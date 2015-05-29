"""
Pure Python bindings to the online Docverter Pandoc document format conversion API.
Karim Bahgat, 2015
"""
import os
import httplib
import mimetypes

#######################
# multipart form post method from: https://gist.github.com/wcaleb/b6a8c97ccb0f11bd16ab
# see docverter example using this method: http://omz-forums.appspot.com/editorial/post/4955159939514368
#######################

def _post_multipart(host, selector, fields, files):
    """
    Post fields and files to an http host as multipart/form-data.
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return the server's response page.
    """
    content_type, body = _encode_multipart_formdata(fields, files)
    h = httplib.HTTPConnection(host)
    h.putrequest('POST', selector)
    h.putheader('content-type', content_type)
    h.putheader('content-length', str(len(body)))
    h.endheaders()
    h.send(body)
    response = h.getresponse()
    output = response.read()
    return output
    # return h.file.read()
 
def _encode_multipart_formdata(fields, files):
    """
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return (content_type, body) ready for httplib.HTTP instance
    """
    BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
    CRLF = '\r\n'
    L = []
    for (key, value) in fields:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"' % key)
        L.append('')
        L.append(value)
    for (key, filename, value) in files:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
        L.append('Content-Type: %s' % _get_content_type(filename))
        L.append('')
        L.append(value)
    L.append('--' + BOUNDARY + '--')
    L.append('')
    body = CRLF.join(L)
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
    return content_type, body
 
def _get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

#########################
# end of borrowed multipart code
#########################

def convert(text, fromformat, toformat, **options):
    """
    - text: The text to be converted to another language format. If converting file use open(filepath).read(). Text should be encoded as raw byte string (e.g. "yourtext".encode(...)". 
    - fromformat: From language format. FORMAT can be markdown (markdown), textile (Textile), rst (reStructuredText), html (HTML), docbook (DocBook XML), or latex (LaTeX).
    - toformat: To language format. FORMAT can be markdown (markdown), rst (reStructuredText), html (XHTML 1), latex (LaTeX), context (ConTeXt), mediawiki (MediaWiki markup), textile (Textile), org (Emacs Org-Mode), texinfo (GNU Texinfo), docbook (DocBook XML), docx (Word docx), epub (EPUB book), mobi (Kindle book), asciidoc (AsciiDoc), or rtf (rich text format).
    - **options: Supply any additional Pandoc options for the conversion process. Note: Options that are only meant to be set on or off should be specified as strings "true" or "false". See docverter api website for more details on options: http://www.docverter.com/api
    """
    # setup
    host = "c.docverter.com"
    selector = "/convert"

    # set parameters
    files = [( "input_files[]", "puretext.txt", text )]
    fields = [("from", fromformat),
              ("to", toformat)]

    # add optional paramters
    for key,value in options.items():
        fields.append((key,value))

    # request
    results = _post_multipart(host=host,
                             selector=selector,
                             fields=fields,
                             files=files)
    return results
