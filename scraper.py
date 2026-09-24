import re
import time

from playwright.sync_api import sync_playwright

PROFILE_DIR = "facebook_browser_profile"

MAX_POSTS = 30
MAX_COMMENTS = 200

NOT_PUBLIC = "Not Publicly Listed"


class FacebookScraper:

    def __init__(self):

        self.playwright = sync_playwright().start()

        self.context = self.playwright.chromium.launch_persistent_context(
            user_data_dir=PROFILE_DIR,
            headless=False,
            viewport={
                "width": 1400,
                "height": 900,
            },
        )

        if self.context.pages:
            self.page = self.context.pages[0]
        else:
            self.page = self.context.new_page()

    # ---------------------------------------------------------
    # LOGIN
    # ---------------------------------------------------------

    def login(self):

        print("\n" + "=" * 70)
        print("FACEBOOK LOGIN")
        print("=" * 70)

        try:
            self.page.goto(
                "https://www.facebook.com/",
                wait_until="domcontentloaded",
                timeout=60000,
            )

        except Exception as e:
            print("Could not open Facebook:", e)
            return

        time.sleep(6)

        print("\nFacebook browser opened.")
        print("Log in normally if Facebook asks.")
        print("Do NOT enter your password into Python.")

        input(
            "\nWhen Facebook is ready, press ENTER here..."
        )

    # ---------------------------------------------------------
    # SECURITY DETECTION
    # ---------------------------------------------------------

    def detect_restriction(self):

        try:
            body = self.page.locator(
                "body"
            ).inner_text(
                timeout=8000
            ).lower()

        except Exception:
            return False

        warning_words = [

            "unusual activity",
            "unusual login activity",

            "automated behavior",
            "automated activity",

            "we suspect automated",

            "confirm it's you",
            "confirm it’s you",

            "security check",

            "captcha",
            "recaptcha",

            "checkpoint",

            "temporarily blocked",
            "temporarily restricted",

            "suspicious activity",
        ]

        for word in warning_words:

            if word in body:
                return True

        return False

    # ---------------------------------------------------------
    # SAFE NAVIGATION
    # ---------------------------------------------------------

    def safe_goto(self, url):

        print("\nOpening:")
        print(url)

        try:

            self.page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=60000,
            )

            # Slow observation period.
            time.sleep(8)

        except Exception as e:

            print("Navigation error:", e)

            return False, "INACCESSIBLE"

        if self.detect_restriction():

            print("\n" + "!" * 70)
            print("FACEBOOK SECURITY WARNING DETECTED")
            print("Stopping this URL.")
            print("No CAPTCHA/security bypass will be attempted.")
            print("!" * 70)

            return False, "ACCESS_RESTRICTED"

        return True, "ACCESSIBLE"

    # ---------------------------------------------------------
    # BODY TEXT
    # ---------------------------------------------------------

    def get_body_text(self):

        try:

            return self.page.locator(
                "body"
            ).inner_text(
                timeout=15000
            )

        except Exception:

            return ""

    # ---------------------------------------------------------
    # STATUS
    # ---------------------------------------------------------

    def determine_status(self, body_text):

        if self.detect_restriction():
            return "ACCESS_RESTRICTED"

        text = body_text.lower()

        unavailable = [

            "this content isn't available",
            "this page isn't available",
            "content isn't available",
            "page isn't available",

            "something went wrong",

            "this group is no longer available",

            "this page is currently unavailable",
        ]

        for word in unavailable:

            if word in text:
                return "INACCESSIBLE"

        if len(body_text.strip()) < 100:

            return "INSUFFICIENT_DATA"

        return "ACCESSIBLE"

    # ---------------------------------------------------------
    # SLOW SCROLL
    # ---------------------------------------------------------

    def scroll_page(self, number_of_scrolls=4):

        for i in range(number_of_scrolls):

            if self.detect_restriction():

                print(
                    "Security warning detected during scrolling."
                )

                return False

            try:

                self.page.mouse.wheel(
                    0,
                    900
                )

                # Slow pause.
                time.sleep(4)

            except Exception:

                return False

        return True

    # ---------------------------------------------------------
    # ARTICLES
    # ---------------------------------------------------------

    def get_articles(self):

        try:

            return self.page.locator(
                '[role="article"]'
            )

        except Exception:

            return None

    # ---------------------------------------------------------
    # POST TEXT
    # ---------------------------------------------------------

    def extract_post_text(self, article):

        try:

            return article.inner_text(
                timeout=5000
            ).strip()

        except Exception:

            return ""

    # ---------------------------------------------------------
    # POST URL
    # ---------------------------------------------------------

    def extract_post_url(self, article):

        try:

            links = article.locator("a")

            count = min(
                links.count(),
                20
            )

            for i in range(count):

                try:

                    href = links.nth(i).get_attribute(
                        "href"
                    )

                    if not href:
                        continue

                    href_lower = href.lower()

                    if (
                        "/posts/" in href_lower
                        or "/photos/" in href_lower
                        or "/videos/" in href_lower
                        or "story_fbid=" in href_lower
                    ):

                        if href.startswith("/"):
                            href = (
                                "https://www.facebook.com"
                                + href
                            )

                        return href

                except Exception:
                    continue

        except Exception:
            pass

        return NOT_PUBLIC

    # ---------------------------------------------------------
    # METRICS
    # ---------------------------------------------------------

    def extract_metric(
        self,
        text,
        metric_names
    ):

        for metric in metric_names:

            pattern = (
                rf"([\d,.]+[KkMm]?)\s+"
                rf"{re.escape(metric)}"
            )

            match = re.search(
                pattern,
                text,
                flags=re.IGNORECASE
            )

            if match:

                return match.group(1)

        return NOT_PUBLIC

    def extract_post_metrics(self, text):

        reactions = self.extract_metric(
            text,
            [
                "reactions",
                "reaction",
                "likes",
                "like",
            ],
        )

        comments = self.extract_metric(
            text,
            [
                "comments",
                "comment",
            ],
        )

        shares = self.extract_metric(
            text,
            [
                "shares",
                "share",
            ],
        )

        return reactions, comments, shares

    # ---------------------------------------------------------
    # POSTS
    # ---------------------------------------------------------

    def collect_posts(self, page_url):

        records = []
        seen = set()

        if not self.scroll_page(4):
            return records

        articles = self.get_articles()

        if articles is None:
            return records

        try:

            count = articles.count()

        except Exception:

            return records

        for i in range(
            min(count, MAX_POSTS)
        ):

            try:

                article = articles.nth(i)

                text = self.extract_post_text(
                    article
                )

                if not text:
                    continue

                post_url = self.extract_post_url(
                    article
                )

                reactions, comments, shares = (
                    self.extract_post_metrics(text)
                )

                key = (
                    post_url,
                    text[:200]
                )

                if key in seen:
                    continue

                seen.add(key)

                records.append({

                    "page_url": page_url,

                    "post_url": post_url,

                    "post_text": text,

                    "reactions": reactions,

                    "comments": comments,

                    "shares": shares,

                })

            except Exception:

                continue

        return records

    # ---------------------------------------------------------
    # COMMENTS
    # ---------------------------------------------------------

    def collect_comments(self, page_url):

        records = []
        seen = set()

        try:

            elements = self.page.locator(
                '[role="article"] [dir="auto"]'
            )

            count = elements.count()

        except Exception:

            return records

        ignored_words = {

            "like",
            "reply",
            "share",
            "comment",
            "comments",

            "see more",

            "follow",
            "following",

            "send",
        }

        for i in range(
            min(count, MAX_COMMENTS)
        ):

            try:

                text = elements.nth(i).inner_text(
                    timeout=3000
                ).strip()

                if not text:
                    continue

                clean = text.lower().strip()

                if clean in ignored_words:
                    continue

                if len(clean) <= 3 and clean.isdigit():
                    continue

                if text in seen:
                    continue

                seen.add(text)

                records.append({

                    "page_url": page_url,

                    "comment_text": text,

                })

            except Exception:

                continue

        return records

    # ---------------------------------------------------------
    # SCRAPE PAGE
    # ---------------------------------------------------------

    def scrape_page(self, url):

        print("\n" + "=" * 70)
        print("SCRAPING")
        print(url)
        print("=" * 70)

        success, navigation_status = (
            self.safe_goto(url)
        )

        if not success:

            return {

                "url": url,

                "status": navigation_status,

                "title": "",

                "body_text": "",

                "posts": [],

                "comments": [],

            }

        body_text = self.get_body_text()

        status = self.determine_status(
            body_text
        )

        print("Status:", status)

        title = ""

        try:
            title = self.page.title()
        except Exception:
            pass

        if status != "ACCESSIBLE":

            return {

                "url": url,

                "status": status,

                "title": title,

                "body_text": body_text,

                "posts": [],

                "comments": [],

            }

        posts = self.collect_posts(url)

        print(
            f"Posts collected: {len(posts)}"
        )

        if self.detect_restriction():

            return {

                "url": url,

                "status": "ACCESS_RESTRICTED",

                "title": title,

                "body_text": body_text,

                "posts": [],

                "comments": [],

            }

        comments = self.collect_comments(url)

        print(
            f"Comments collected: {len(comments)}"
        )

        return {

            "url": url,

            "status": status,

            "title": title,

            "body_text": body_text,

            "posts": posts,

            "comments": comments,

        }

    # ---------------------------------------------------------
    # CLOSE
    # ---------------------------------------------------------

    def close(self):

        try:
            self.context.close()
        except Exception:
            pass

        try:
            self.playwright.stop()
        except Exception:
            pass