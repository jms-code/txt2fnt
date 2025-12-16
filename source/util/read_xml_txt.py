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
import re
import xml.etree.ElementTree as ET
from source.util.safe_print import safe_print


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

    This function is tolerant: on parse errors it will sanitize control characters
    and fall back to a regex-based extraction of text between tags.
    """
    try:
        root = ET.fromstring(xml_string)
        out: List[str] = []
        _collect_texts(root, out)
        return out
    except ET.ParseError as e:
        # Best-effort fallback for malformed XML strings
        # Remove problematic control characters
        sanitized = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F]", "", xml_string)
        try:
            root = ET.fromstring(sanitized)
            out: List[str] = []
            _collect_texts(root, out)
            return out
        except ET.ParseError:
            # Final fallback: extract text between tags
            texts = re.findall(r">([^<>]+)<", sanitized)
            texts = [t.strip() for t in texts if t.strip()]
            return texts


def read_xml_texts(file_path: str) -> List[str]:
    """Read the XML file at `file_path` and return all node text values.

    Example:
        <a>hello<b>world</b> tail</a>
    returns ['hello', 'world', 'tail']

    This function will attempt to parse the XML normally, but if the input
    is not well-formed (common in user-supplied XML), it falls back to a
    tolerant extraction that (1) sanitizes control characters, (2) attempts
    `ET.fromstring` on the sanitized text, and finally (3) extracts text via
    a simple regex when parsing still fails.
    """
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        out: List[str] = []
        _collect_texts(root, out)
        return out
    except ET.ParseError as e:
        # Best-effort fallback for malformed XML: read as text and sanitize
        safe_print(f"⚠️  XML parse error for {file_path}: {e}. Falling back to tolerant text extraction.")
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()

        # Remove disallowed control characters that break XML parsing
        content = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F]", "", content)

        # Try parsing sanitized content
        try:
            root = ET.fromstring(content)
            out: List[str] = []
            _collect_texts(root, out)
            return out
        except ET.ParseError:
            # Final fallback: extract text between tags using a regex and strip
            texts = re.findall(r">([^<>]+)<", content)
            texts = [t.strip() for t in texts if t.strip()]
            return texts


__all__ = ["read_xml_texts", "read_xml_texts_from_string"]
