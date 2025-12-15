"""Utilities for reading XML and extracting plain text content.

Functions:
    read_xml_texts(file_path) -> List[str]
        Parse an XML file and return a list of all text nodes in document order,
        excluding tags and attributes. Text is stripped of surrounding whitespace
        and empty strings are omitted.
    read_xml_texts_from_string(xml_string) -> List[str]
        Same as above but accepts an XML string.
"""
from typing import List
import xml.etree.ElementTree as ET


def _collect_texts(elem: ET.Element, out: List[str]) -> None:
    """Recursively collect element.text and element.tail in document order.

    Both `text` and `tail` are stripped; empty strings are skipped.
    """
    if elem.text:
        text = elem.text.strip()
        if text:
            out.append(text)

    for child in elem:
        _collect_texts(child, out)

    if elem.tail:
        tail = elem.tail.strip()
        if tail:
            out.append(tail)


def read_xml_texts_from_string(xml_string: str) -> List[str]:
    """Parse an XML string and return all text nodes (no tags or attributes).

    Returns a list of text chunks in document order. CDATA is preserved as text.
    """
    root = ET.fromstring(xml_string)
    out: List[str] = []
    _collect_texts(root, out)
    return out


def read_xml_texts(file_path: str) -> List[str]:
    """Read the XML file at `file_path` and return all node text values.

    Example:
        <a>hello<b>world</b> tail</a>
    returns ['hello', 'world', 'tail']
    """
    tree = ET.parse(file_path)
    root = tree.getroot()
    out: List[str] = []
    _collect_texts(root, out)
    return out


__all__ = ["read_xml_texts", "read_xml_texts_from_string"]
