"""
Original VB CODE

    SetText(lblStatus, folderName)

    If Form1.stopping = True Then Exit Sub

    'get base object name which is the folder name
    Dim baseName As String = Path.GetFileName(folderName)
    SetText(txtStatus, String.Format("Object ID: {0}", baseName))

    Dim m As Match = Regex.Match(baseName, ObjectIdRegex)
    If m.Success = False Then
      SetText(txtStatus, String.Format("   ERROR: Base folder name '{0}' does not match naming conventions for ObjectIDs ", baseName))
    Else
      SetText(txtStatus, String.Format("   OK: Base folder name '{0}' is a valid ObjectID ", baseName))
    End If


    SetText(txtStatus, New String("-", 20))
    SetText(txtStatus, "   Checking for expected root files and folders:")
    'check whether expected files exist
    CheckFileExists(folderName, "checksum.md5")
    CheckFileExists(folderName, "marc.xml")
    CheckFileExists(folderName, "meta.yml")

    'make sure folder does not contain any subfolders
    Dim subfolders() As String = Directory.GetDirectories(folderName)
    If subfolders.Count > 0 Then
      SetText(txtStatus, String.Format("      ERROR: The base folder '{0}' contains subfolders. ", baseName))
    Else
      SetText(txtStatus, String.Format("      OK: The base folder '{0}' has no subfolders", baseName))
    End If


    'validate that the checksums in the *.fil file match
    SetText(txtStatus, New String("-", 20))
    SetText(txtStatus, "   Validating Checksum File 'checksum.md5'")
    CheckChecksums(folderName)

    'validate that the MARC file is valid
    SetText(txtStatus, New String("-", 20))
    SetText(txtStatus, "   Validating MARC XML File 'marc.xml'")

    Dim xmlSet As New XmlReaderSettings()
    xmlSet.CheckCharacters = True
    xmlSet.ConformanceLevel = ConformanceLevel.Document
    xmlSet.Schemas.Add("http://www.loc.gov/MARC21/slim", "http://www.loc.gov/standards/marcxml/schema/MARC21slim.xsd")
    xmlSet.ValidationFlags = XmlSchemaValidationFlags.ProcessIdentityConstraints Or XmlSchemaValidationFlags.ProcessSchemaLocation Or XmlSchemaValidationFlags.ReportValidationWarnings

    xmlSet.ValidationType = ValidationType.Schema

    CheckXML(folderName, "marc.xml", xmlSet)

    'validate other xml files, currently ALTO
    SetText(txtStatus, New String("-", 20))
    SetText(txtStatus, String.Format("   Validating all other XML files"))

    xmlSet.Schemas.Add("http://www.loc.gov/standards/alto/ns-v2#", "http://www.loc.gov/standards/alto/alto.xsd")
    xmlSet.Schemas.Add("http://www.w3.org/1999/xlink", "http://www.loc.gov/standards/xlink/xlink.xsd")

    Dim allXML() As String = Directory.GetFiles(folderName, "*.xml")

    For Each xfile In allXML
      If Path.GetFileName(xfile).ToLower <> "marc.xml" Then
        SetText(txtStatus, String.Format("   Validating XML file '{0}'", Path.GetFileName(xfile)))
        CheckXML(xfile, xmlSet)
      End If
      Application.DoEvents()
    Next

    'Validate that the meta.yml file is valid; could also validate that the values are correct by comparing with the images
    SetText(txtStatus, New String("-", 20))
    SetText(txtStatus, "   Validating 'meta.yml' file")
    CheckYaml(folderName)

    Application.DoEvents()
"""
import os
import hashlib
import datetime
import logging
from lxml import etree
import yaml

import sys

DIRECTORY_REGEX = "^\d+(p\d+(_\d+)?)?(v\d+(_\d+)?)?(i\d+(_\d+)?)?(m\d+(_\d+)?)?$"

class ValidationError(Exception):
    pass

class InvalidChecksum(ValidationError):
    pass


#
# def load_validation(filename="hathi_validate/MARC21slim.xsd"):
#     def read_file():
#         with open(filename) as f:
#             for line in f:
#                 yield line.strip()
#
#     return "".join(read_file())

# XSD = load_validation()
XSD = r"""<?xml version="1.0"?>
<xsd:schema targetNamespace="http://www.loc.gov/MARC21/slim" xmlns="http://www.loc.gov/MARC21/slim" xmlns:xsd="http://www.w3.org/2001/XMLSchema" elementFormDefault="qualified" attributeFormDefault="unqualified" version="1.1" xml:lang="en">
  <xsd:annotation>
    <xsd:documentation>
			MARCXML: The MARC 21 XML Schema
			Prepared by Corey Keith
			
				May 21, 2002 - Version 1.0  - Initial Release

**********************************************
Changes.

August 4, 2003 - Version 1.1 - 
Removed import of xml namespace and the use of xml:space="preserve" attributes on the leader and controlfields. 
                    Whitespace preservation in these subfields is accomplished by the use of xsd:whiteSpace value="preserve"

May 21, 2009  - Version 1.2 - 
in subfieldcodeDataType  the pattern 
                          "[\da-z!&quot;#$%&amp;'()*+,-./:;&lt;=&gt;?{}_^`~\[\]\\]{1}"
	changed to:	
                         "[\dA-Za-z!&quot;#$%&amp;'()*+,-./:;&lt;=&gt;?{}_^`~\[\]\\]{1}"
    i.e "A-Z" added after "[\d" before "a-z"  to allow upper case.  This change is for consistency with the documentation.
	
************************************************************
			This schema supports XML markup of MARC21 records as specified in the MARC documentation (see www.loc.gov).  It allows tags with
			alphabetics and subfield codes that are symbols, neither of which are as yet used in  the MARC 21 communications formats, but are 
			allowed by MARC 21 for local data.  The schema accommodates all types of MARC 21 records: bibliographic, holdings, bibliographic 
			with embedded holdings, authority, classification, and community information.
		</xsd:documentation>
  </xsd:annotation>
  <xsd:element name="record" type="recordType" nillable="true" id="record.e">
    <xsd:annotation>
      <xsd:documentation>record is a top level container element for all of the field elements which compose the record</xsd:documentation>
    </xsd:annotation>
  </xsd:element>
  <xsd:element name="collection" type="collectionType" nillable="true" id="collection.e">
    <xsd:annotation>
      <xsd:documentation>collection is a top level container element for 0 or many records</xsd:documentation>
    </xsd:annotation>
  </xsd:element>
  <xsd:complexType name="collectionType" id="collection.ct">
    <xsd:sequence minOccurs="0" maxOccurs="unbounded">
      <xsd:element ref="record"/>
    </xsd:sequence>
    <xsd:attribute name="id" type="idDataType" use="optional"/>
  </xsd:complexType>
  <xsd:complexType name="recordType" id="record.ct">
    <xsd:sequence minOccurs="0">
      <xsd:element name="leader" type="leaderFieldType"/>
      <xsd:element name="controlfield" type="controlFieldType" minOccurs="0" maxOccurs="unbounded"/>
      <xsd:element name="datafield" type="dataFieldType" minOccurs="0" maxOccurs="unbounded"/>
    </xsd:sequence>
    <xsd:attribute name="type" type="recordTypeType" use="optional"/>
    <xsd:attribute name="id" type="idDataType" use="optional"/>
  </xsd:complexType>
  <xsd:simpleType name="recordTypeType" id="type.st">
    <xsd:restriction base="xsd:NMTOKEN">
      <xsd:enumeration value="Bibliographic"/>
      <xsd:enumeration value="Authority"/>
      <xsd:enumeration value="Holdings"/>
      <xsd:enumeration value="Classification"/>
      <xsd:enumeration value="Community"/>
    </xsd:restriction>
  </xsd:simpleType>
  <xsd:complexType name="leaderFieldType" id="leader.ct">
    <xsd:annotation>
      <xsd:documentation>MARC21 Leader, 24 bytes</xsd:documentation>
    </xsd:annotation>
    <xsd:simpleContent>
      <xsd:extension base="leaderDataType">
        <xsd:attribute name="id" type="idDataType" use="optional"/>
      </xsd:extension>
    </xsd:simpleContent>
  </xsd:complexType>
  <xsd:simpleType name="leaderDataType" id="leader.st">
    <xsd:restriction base="xsd:string">
      <xsd:whiteSpace value="preserve"/>
      <xsd:pattern value="[\d ]{5}[\dA-Za-z ]{1}[\dA-Za-z]{1}[\dA-Za-z ]{3}(2| )(2| )[\d ]{5}[\dA-Za-z ]{3}(4500|    )"/>
    </xsd:restriction>
  </xsd:simpleType>
  <xsd:complexType name="controlFieldType" id="controlfield.ct">
    <xsd:annotation>
      <xsd:documentation>MARC21 Fields 001-009</xsd:documentation>
    </xsd:annotation>
    <xsd:simpleContent>
      <xsd:extension base="controlDataType">
        <xsd:attribute name="id" type="idDataType" use="optional"/>
        <xsd:attribute name="tag" type="controltagDataType" use="required"/>
      </xsd:extension>
    </xsd:simpleContent>
  </xsd:complexType>
  <xsd:simpleType name="controlDataType" id="controlfield.st">
    <xsd:restriction base="xsd:string">
      <xsd:whiteSpace value="preserve"/>
    </xsd:restriction>
  </xsd:simpleType>
  <xsd:simpleType name="controltagDataType" id="controltag.st">
    <xsd:restriction base="xsd:string">
      <xsd:whiteSpace value="preserve"/>
      <xsd:pattern value="00[1-9A-Za-z]{1}"/>
    </xsd:restriction>
  </xsd:simpleType>
  <xsd:complexType name="dataFieldType" id="datafield.ct">
    <xsd:annotation>
      <xsd:documentation>MARC21 Variable Data Fields 010-999</xsd:documentation>
    </xsd:annotation>
    <xsd:sequence maxOccurs="unbounded">
      <xsd:element name="subfield" type="subfieldatafieldType"/>
    </xsd:sequence>
    <xsd:attribute name="id" type="idDataType" use="optional"/>
    <xsd:attribute name="tag" type="tagDataType" use="required"/>
    <xsd:attribute name="ind1" type="indicatorDataType" use="required"/>
    <xsd:attribute name="ind2" type="indicatorDataType" use="required"/>
  </xsd:complexType>
  <xsd:simpleType name="tagDataType" id="tag.st">
    <xsd:restriction base="xsd:string">
      <xsd:whiteSpace value="preserve"/>
      <xsd:pattern value="(0([1-9A-Z][0-9A-Z])|0([1-9a-z][0-9a-z]))|(([1-9A-Z][0-9A-Z]{2})|([1-9a-z][0-9a-z]{2}))"/>
    </xsd:restriction>
  </xsd:simpleType>
  <xsd:simpleType name="indicatorDataType" id="ind.st">
    <xsd:restriction base="xsd:string">
      <xsd:whiteSpace value="preserve"/>
      <xsd:pattern value="[\da-z ]{1}"/>
    </xsd:restriction>
  </xsd:simpleType>
  <xsd:complexType name="subfieldatafieldType" id="subfield.ct">
    <xsd:simpleContent>
      <xsd:extension base="subfieldDataType">
        <xsd:attribute name="id" type="idDataType" use="optional"/>
        <xsd:attribute name="code" type="subfieldcodeDataType" use="required"/>
      </xsd:extension>
    </xsd:simpleContent>
  </xsd:complexType>
  <xsd:simpleType name="subfieldDataType" id="subfield.st">
    <xsd:restriction base="xsd:string">
      <xsd:whiteSpace value="preserve"/>
    </xsd:restriction>
  </xsd:simpleType>
  <xsd:simpleType name="subfieldcodeDataType" id="code.st">
    <xsd:restriction base="xsd:string">
      <xsd:whiteSpace value="preserve"/>
      <xsd:pattern value="[\dA-Za-z!&quot;#$%&amp;'()*+,-./:;&lt;=&gt;?{}_^`~\[\]\\]{1}"/>
      <!-- "A-Z" added after "\d" May 21, 2009 -->
    </xsd:restriction>
  </xsd:simpleType>
  <xsd:simpleType name="idDataType" id="id.st">
    <xsd:restriction base="xsd:ID"/>
  </xsd:simpleType>
</xsd:schema>"""


def find_missing_files(path: str) -> str:
    """
        check for expected files exist on the path
    Args:
        path:

    Yields: Any files missing

    """

    expected_files = [
        "checksum.md5",
        "marc.xml",
        "meta.yml",
    ]
    for file in expected_files:
        if not os.path.exists(os.path.join(path, file)):
            yield file


def find_extra_subdirectory(path):
    """
        Check path for any subdirectories
    Args:
        path:

    Yields: Any subdirectory

    """
    for item in os.scandir(path):
        if item.is_dir():
            yield item.path


def parse_checksum(line):
    md5_hash, raw_filename = line.strip().split(" ")
    if len(md5_hash) != 32:
        raise InvalidChecksum("Invalid Checksum")
    assert raw_filename[0] == "*"
    filename = raw_filename[1:]
    return md5_hash, filename


def calculate_md5(filename, chunk_size=8192):
    md5 = hashlib.md5()

    with open(filename, "rb") as f:
        while True:
            data = f.read(chunk_size)
            if not data:
                break
            md5.update(data)
        return md5.hexdigest()


def find_failing_checksums(path, report):
    """
        validate that the checksums in the *.fil file match

    Args:
        path:
        report:

    Returns:

    """

    logger = logging.getLogger(__name__)

    for report_md5_hash, filename in extracts_checksums(report):
        logger.info("Calculating the md5 checksum hash for {}".format(filename))
        file_path = os.path.join(path, filename)
        try:
            file_md5_hash = calculate_md5(filename=file_path)
        except FileNotFoundError as e:
            raise
        if file_md5_hash != report_md5_hash:
            yield file_path
        else:
            logger.info("{} successfully matches md5 hash in {}".format(filename, os.path.basename(report)))


def extracts_checksums(report):
    with open(report, "r") as f:
        for line in f:
            md5, filename = parse_checksum(line)
            yield md5, filename


def find_errors_marc(filename):
    """
    Validate the MARC file

    Args:
        filename:

    Returns:

    """
    xsd = etree.XML(XSD)
    scheme = etree.XMLSchema(xsd)
    with open(filename, "r") as f:
        raw_data = f.read()
    doc = etree.fromstring(raw_data)
    if not scheme.validate(doc):
        yield "Unable to validate {}".format(filename)


def parse_yaml(filename):
    with open(filename, "r") as f:
        data = yaml.load(f)
        return data


def find_errors_meta(filename, path):
    """
    Validate meta.yml file
    could also validate that the values are correct by comparing with the images

    Args:
        filename:

    Yields: Error messages

    """
    def find_pagedata_errors(metadata):
        pages = metadata["pagedata"]
        for image_name, attributes  in pages.items():
            if not os.path.exists(os.path.join(path, image_name)):
                yield "The pagedata {} contains an nonexistent file {}".format(filename, image_name)
            if attributes:
                pass

    def find_capture_date_errors(metadata):
        capture_date = metadata["capture_date"]
        if not isinstance(capture_date, datetime.datetime):
            yield "data in capture_date is not a date format"

    try:
        metadata = parse_yaml(filename=filename)

        try:
            for error in find_pagedata_errors(metadata):
                yield error
        except KeyError as e:
            yield "{} is missing key, {}".format(filename, e)

        try:
            for error in find_capture_date_errors(metadata):
                yield error
        except KeyError as e:
            yield "{} is missing key, {}".format(filename, e)
    except yaml.YAMLError as e:
        yield "Unable to read {}. Reason:{}".format(filename, e)



def process_directory(path: str):
    # TODO validate directory name
    logger = logging.getLogger(__name__)

    logger.info("Looking for missing files in {}".format(path))
    for missing_file in find_missing_files(path):
        print(missing_file)
    else:
        logger.info("Found no missing files in {}".format(path))

    logger.info("Looking for extra subdirectories in {}".format(path))
    for extra_subdirectory in find_extra_subdirectory(path=path):
        print(extra_subdirectory)
    else:
        logger.info("Found no extra subdirectories in {}".format(path))

    # TODO turn checksum check back on
    # checksum_report = os.path.join(path, "checksum.md5")
    # logger.info("Validating checksums in {}".format(checksum_report))
    # for failing_checksum in find_failing_checksums(path=path, report=checksum_report):
    #     print(failing_checksum)

    marc_file = os.path.join(path, "marc.xml")
    logger.info("Validating {}".format(marc_file))
    for error in find_errors_marc(filename=marc_file):
        print(error)
    else:
        logger.info("{} successfully validated".format(marc_file))

    # TODO: validate other xml files, currently ALTO
    yml_file = os.path.join(path, "meta.yml")
    logger.info("Validating {}".format(yml_file))
    for error in find_errors_meta(filename=yml_file, path=path):
        print(error)
    else:
        logger.info("{} successfully validated".format(yml_file))
    pass
