import xml.etree.ElementTree as ET

xml = ET.fromstring("<r><f2>49.992</f2><n>C_242</n><z> 12.08.2024 18:05:20</z><p>276.4</p><d>007</d><dt>0</dt></r>")
print(xml.find("f2").text)