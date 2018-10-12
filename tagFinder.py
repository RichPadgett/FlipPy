
# Demonstrating SAX-based parsing of XML

from xml.sax import parse, SAXParseException, ContentHandler

#Class to handle save data contains tag and data used in XML Write
class XMLSettings(object):
  def __init__(self, tag, data):
    self.tag = tag
    self.data = data

  def setTag(self, tag):
    self.tag = tag

  def setData(self, data):
    self.data = data



class TagInfoHandler( ContentHandler ):
  """Custom xml.sax.ContentHandler"""

  def __init__(self, tagName ):
    ContentHandler.__init__(self)
    self.tagName = tagName
    self.content = None
    self.get = False

  def startElement( self, name, attributes ):
    if name == self.tagName:
      self.get = True
    for attribute in attributes.getNames():
      pass
      #print attribute, attributes.getValue( attribute )
  
  def endElement( self, name ) :
    pass

  def characters( self, content ) :
    # strip only removes spaces!
    content = content.strip()
    if content: 
      if self.get:
        self.content = content
        self.get = False

  def getContent(self):
    return self.content

  #write uses this to write all of the tags
  def writeElement(self, FILE, tag, data ):
    FILE.write('   <'+tag+'>')
    FILE.write(data)
    FILE.write('</'+tag+'>\n')


  #call this with file location and settings class to write xml
  def writeXML(self, location, settings):
    FILE = open(location, 'w')
    FILE.write('<?xml version = "1.0"?>\n')
    FILE.write('<Settings>\n')
    for x in settings:
      self.writeElement(FILE, x.tag , x.data)
    FILE.write('</Settings>\n')
    FILE.close()


def main():
  print "Beginning XML processor..."
  file = raw_input( "Enter a file to parse: " )
  tagname = raw_input( "Enter a tag to search for: " )
  try:
    parse ( file, TagInfoHandler( tagname ) )
    
  except IOError, message:
    print "Error reading file: ", message
  except SAXParseException, message:
    print "Error parsing file: ", message

if __name__ == "__main__":
  main()
