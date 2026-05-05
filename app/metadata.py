import re

from bs4 import BeautifulSoup

def clean_html(raw_html):
    """
    Convert HTML content into clean plain text.
    """
    if not raw_html:
        return ""
    
    # Remove HTML tags
    soup = BeautifulSoup(raw_html, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    
    # Replace multiple spaces with a single space
    return re.sub(r'\s+', ' ', text)

def limit_text(text, max_length=500):
    """
    Limit long summaries to keep the database and dashboard clean.
    """
    if not text:
        return ""
    
    if len(text) <= max_length:
        return text
    return text[:max_length].rstrip() + "..."

def extract_summary(entry):
    """
    Exctract and clean the article summary from an RSS entry.
    """
    summary = ""
    
    if entry.get("summary"):
        summary = entry.get("summary", "")
        
    elif entry.get("description"):
        summary = entry.get("description", "")
    
    elif entry.get("content"):
        content = entry.get("content", [])
        if isinstance(content, list) and content:
            summary = content[0].get("value", "")
            
    clean_summary = clean_html(summary)
    
    return limit_text(clean_summary)

def looks_like_image_url(url):
    """
    Check whether a URL appears to point to an image file.
    """
    if not url:
        return False
    image_extensions = [".jpg", ".jpeg", ".png", ".webp", ".gif"]
    return any(
        url.lower().split("?")[0].endswith(extension)
        for extension in image_extensions
    )

def extract_image_url(entry):
    """
    Try to extract an image URL from common RSS entry fields.
    """
    
    media_content = entry.get("media_content", [])
    
    for media in media_content:
        image_url = media.get("url")
        
        if image_url:
            return image_url
        
    media_thumbnail = entry.get("media_thumbnail", [])
    
    for media in media_thumbnail:
        image_url = media.get("url")
        
        if image_url:
            return image_url
    
    enclosures = entry.get("enclosures", [])
    
    for enclosure in enclosures:
        enclosure_type = enclosure.get("type", "")
        image_url = enclosure.get("href") or enclosure.get("url")
        
        if enclosure_type.startswith("image/") and image_url:
            return image_url
        
    links = entry.get("links", [])
    
    for link in links:
        link_type = link.get("type", "")
        image_url = link.get("href", "")
        
        if link_type.startswith("image/") and image_url:
            return image_url
        
        if looks_like_image_url(image_url):
            return image_url
        
    summary_html = entry.get("summary", "")
    
    if summary_html:
        soup = BeautifulSoup(summary_html, "html.parser")
        image = soup.find("img")
        
        if image and image.get("src"):
            return image.get("src")
        
    return ""