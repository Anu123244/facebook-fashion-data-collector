import re


NOT_PUBLIC = "Not Publicly Listed"


# ============================================================
# FASHION KEYWORDS
# ============================================================

FASHION_KEYWORDS = [
    "fashion",
    "clothing",
    "clothes",
    "apparel",
    "boutique",
    "garments",
    "dress",
    "shirt",
    "t-shirt",
    "tshirt",
    "jeans",
    "saree",
    "sari",
    "sharee",
    "salwar",
    "kameez",
    "three piece",
    "three-piece",
    "panjabi",
    "kurti",
    "abaya",
    "hijab",
    "shawl",
    "lehenga",
    "blouse",
    "skirt",
    "jacket",
    "hoodie",
    "sweater",
    "kids clothing",
    "baby clothing",
    "women's clothing",
    "womens clothing",
    "men's clothing",
    "mens clothing",
    "fashion designer",
    "textile",
    "streetwear",
    "sportswear",
    "footwear",
    "shoes",
    "sneakers",
    "bags",
    "handmade clothing",
    "online clothing",
    "clothing store",
    "fashion store",
    "fashion house",
    "fashion brand",
]


# ============================================================
# CLEAN TEXT
# ============================================================

def clean_text(text):

    if not text:
        return ""

    text = str(text)

    # Replace multiple spaces/newlines.
    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()


# ============================================================
# FIND EMAIL
# ============================================================

def extract_email(text):

    pattern = (
        r"[A-Za-z0-9._%+-]+"
        r"@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    )

    matches = re.findall(
        pattern,
        text,
        flags=re.IGNORECASE,
    )

    if matches:
        return matches[0]

    return NOT_PUBLIC


# ============================================================
# FIND PHONE
# ============================================================

def extract_phone(text):

    # Bangladesh phone formats such as:
    # 01712345678
    # +8801712345678
    # +880 1712 345678
    # 01712-345678

    patterns = [

        r"\+880[\s-]?1[3-9][\s-]?\d{4}[\s-]?\d{4}",

        r"01[3-9][\s-]?\d{4}[\s-]?\d{4}",

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
        )

        if match:

            return re.sub(
                r"[\s-]+",
                "",
                match.group(0),
            )

    return NOT_PUBLIC


# ============================================================
# FIND WEBSITE
# ============================================================

def extract_website(text):

    patterns = [
        r"https?://[^\s]+",
        r"www\.[^\s]+",
    ]

    for pattern in patterns:

        matches = re.findall(
            pattern,
            text,
            flags=re.IGNORECASE,
        )

        for url in matches:

            url = url.rstrip(
                ".,;:)]}"
            )

            # Don't treat Facebook itself as the business website.
            if "facebook.com" in url.lower():
                continue

            if "instagram.com" in url.lower():
                continue

            return url

    return NOT_PUBLIC


# ============================================================
# FOLLOWERS
# ============================================================

def extract_followers(text):

    patterns = [

        r"([\d,.]+[KkMm]?)\s+followers",

        r"([\d,.]+[KkMm]?)\s+people follow this",

        r"([\d,.]+[KkMm]?)\s+follower",

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        )

        if match:
            return match.group(1)

    return NOT_PUBLIC


# ============================================================
# FOLLOWING
# ============================================================

def extract_following(text):

    patterns = [

        r"([\d,.]+[KkMm]?)\s+following",

        r"following\s+([\d,.]+[KkMm]?)",

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        )

        if match:
            return match.group(1)

    return NOT_PUBLIC


# ============================================================
# GROUP MEMBERS
# ============================================================

def extract_members(text):

    patterns = [

        r"([\d,.]+[KkMm]?)\s+members",

        r"([\d,.]+[KkMm]?)\s+member",

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        )

        if match:
            return match.group(1)

    return NOT_PUBLIC


# ============================================================
# LOCATION
# ============================================================

def extract_location(text):

    patterns = [

        r"located in\s+([^\n]+)",

        r"based in\s+([^\n]+)",

        r"location\s*[:\-]\s*([^\n]+)",

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        )

        if match:

            value = clean_text(
                match.group(1)
            )

            if value:
                return value

    # Common Bangladesh cities.
    cities = [
        "Dhaka",
        "Chattogram",
        "Chittagong",
        "Sylhet",
        "Rajshahi",
        "Khulna",
        "Barishal",
        "Rangpur",
        "Mymensingh",
        "Cumilla",
        "Comilla",
        "Gazipur",
        "Narayanganj",
    ]

    for city in cities:

        if re.search(
            rf"\b{re.escape(city)}\b",
            text,
            flags=re.IGNORECASE,
        ):

            return city

    return NOT_PUBLIC


# ============================================================
# ADDRESS
# ============================================================

def extract_address(text):

    patterns = [

        r"address\s*[:\-]\s*([^\n]+)",

        r"shop address\s*[:\-]\s*([^\n]+)",

        r"office address\s*[:\-]\s*([^\n]+)",

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        )

        if match:

            value = clean_text(
                match.group(1)
            )

            if value:
                return value

    return NOT_PUBLIC


# ============================================================
# BUSINESS HOURS
# ============================================================

def extract_business_hours(text):

    patterns = [

        r"hours\s*[:\-]\s*([^\n]+)",

        r"business hours\s*[:\-]\s*([^\n]+)",

        r"open\s*[:\-]\s*([^\n]+)",

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        )

        if match:

            value = clean_text(
                match.group(1)
            )

            if value:
                return value

    return NOT_PUBLIC


# ============================================================
# CATEGORY
# ============================================================

def extract_category(text):

    categories = [

        "Clothing Store",
        "Fashion Store",
        "Women's Clothing",
        "Men's Clothing",
        "Baby & Children's Clothing",
        "Boutique",
        "Fashion Designer",
        "Clothing Brand",
        "Garment Manufacturer",
        "Textile Company",
        "Shoe Store",
        "Accessories",
        "Shopping & Retail",
    ]

    lower_text = text.lower()

    for category in categories:

        if category.lower() in lower_text:

            return category

    return NOT_PUBLIC


# ============================================================
# DESCRIPTION
# ============================================================

def extract_description(text):

    # Try to find common About-section labels.

    patterns = [

        r"about\s*[:\-]\s*(.{20,500})",

        r"description\s*[:\-]\s*(.{20,500})",

        r"bio\s*[:\-]\s*(.{20,500})",

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        )

        if match:

            value = clean_text(
                match.group(1)
            )

            if value:
                return value[:1000]

    return NOT_PUBLIC


# ============================================================
# PAGE NAME
# ============================================================

def extract_page_name(
    text,
    page_title="",
):

    title = clean_text(
        page_title
    )

    if title:

        # Remove common Facebook suffixes.
        title = re.sub(
            r"\s*[-|]\s*Facebook.*$",
            "",
            title,
            flags=re.IGNORECASE,
        )

        title = title.strip()

        if title:
            return title

    # Try first meaningful line from body.
    lines = text.splitlines()

    ignored = {
        "facebook",
        "home",
        "about",
        "photos",
        "videos",
        "posts",
        "reels",
        "groups",
        "more",
    }

    for line in lines:

        line = clean_text(line)

        if not line:
            continue

        if line.lower() in ignored:
            continue

        if len(line) < 2:
            continue

        if len(line) > 150:
            continue

        return line

    return NOT_PUBLIC


# ============================================================
# FASHION KEYWORDS
# ============================================================

def extract_fashion_keywords(text):

    lower_text = text.lower()

    found = []

    for keyword in FASHION_KEYWORDS:

        if keyword.lower() in lower_text:

            found.append(keyword)

    # Remove duplicates.
    found = list(
        dict.fromkeys(found)
    )

    if found:
        return ", ".join(found)

    return NOT_PUBLIC


# ============================================================
# FASHION RELEVANCE
# ============================================================

def determine_fashion_relevance(
    text,
    fashion_keywords,
):

    if fashion_keywords == NOT_PUBLIC:
        return "NEEDS_REVIEW"

    keyword_count = len(
        fashion_keywords.split(",")
    )

    # A single generic keyword may not be enough.
    if keyword_count >= 2:
        return "RELEVANT"

    return "NEEDS_REVIEW"


# ============================================================
# MAIN EXTRACTION FUNCTION
# ============================================================

def extract_information(
    text,
    page_title="",
):

    text = clean_text(text)

    # --------------------------------------------
    # Individual fields
    # --------------------------------------------

    page_name = extract_page_name(
        text,
        page_title,
    )

    category = extract_category(
        text
    )

    description = extract_description(
        text
    )

    phone = extract_phone(
        text
    )

    email = extract_email(
        text
    )

    website = extract_website(
        text
    )

    followers = extract_followers(
        text
    )

    following = extract_following(
        text
    )

    members = extract_members(
        text
    )

    location = extract_location(
        text
    )

    address = extract_address(
        text
    )

    business_hours = extract_business_hours(
        text
    )

    fashion_keywords = extract_fashion_keywords(
        text
    )

    fashion_relevance = determine_fashion_relevance(
        text,
        fashion_keywords,
    )

    # --------------------------------------------
    # Final dictionary
    # --------------------------------------------

    result = {

        "page_name": page_name,

        "category": category,

        "description": description,

        "phone": phone,

        "email": email,

        "website": website,

        "followers": followers,

        "following": following,

        "members": members,

        "location": location,

        "address": address,

        "business_hours": business_hours,

        "fashion_keywords": fashion_keywords,

        "fashion_relevance": fashion_relevance,
    }

    # --------------------------------------------
    # Replace empty values
    # --------------------------------------------

    for key, value in result.items():

        if (
            value is None
            or str(value).strip() == ""
        ):

            result[key] = NOT_PUBLIC

    return result