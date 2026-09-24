from pathlib import Path
import time

import pandas as pd

from scraper import FacebookScraper
from extractor import extract_information


# ============================================================
# FILE SETTINGS
# ============================================================

INPUT_FILE = "data/input_urls.csv"

PAGES_FILE = "data/pages.csv"
POSTS_FILE = "data/posts.csv"
COMMENTS_FILE = "data/comments.csv"

EXCEL_FILE = "data/output.xlsx"
COMBINED_CSV_FILE = "data/output.csv"

DELAY_BETWEEN_PAGES = 5

NOT_PUBLIC = "Not Publicly Listed"


# ============================================================
# CREATE DATA FOLDER
# ============================================================

Path("data").mkdir(parents=True, exist_ok=True)


# ============================================================
# LOAD EXISTING CSV
# ============================================================

def load_csv(filename):

    path = Path(filename)

    if not path.exists():
        return []

    try:

        df = pd.read_csv(
            filename,
            dtype=str,
            keep_default_na=False
        )

        df = df.fillna(NOT_PUBLIC)

        return df.to_dict("records")

    except Exception as e:

        print(f"Could not read {filename}: {e}")

        return []


# ============================================================
# SAVE PAGE / POST / COMMENT DATA
# ============================================================

def save_data(pages, posts, comments):

    # --------------------------------------------------------
    # PAGES
    # --------------------------------------------------------

    pages_df = pd.DataFrame(pages)

    if not pages_df.empty:

        if "url" in pages_df.columns:

            pages_df = pages_df.drop_duplicates(
                subset=["url"],
                keep="last"
            )

        pages_df = pages_df.fillna(NOT_PUBLIC)


    # --------------------------------------------------------
    # POSTS
    # --------------------------------------------------------

    posts_df = pd.DataFrame(posts)

    if not posts_df.empty:

        required_columns = [
            "page_url",
            "post_url",
            "post_text"
        ]

        existing_columns = [
            column
            for column in required_columns
            if column in posts_df.columns
        ]

        if existing_columns:

            posts_df = posts_df.drop_duplicates(
                subset=existing_columns,
                keep="last"
            )

        posts_df = posts_df.fillna(NOT_PUBLIC)


    # --------------------------------------------------------
    # COMMENTS
    # --------------------------------------------------------

    comments_df = pd.DataFrame(comments)

    if not comments_df.empty:

        required_columns = [
            "page_url",
            "comment_text"
        ]

        existing_columns = [
            column
            for column in required_columns
            if column in comments_df.columns
        ]

        if existing_columns:

            comments_df = comments_df.drop_duplicates(
                subset=existing_columns,
                keep="last"
            )

        comments_df = comments_df.fillna(NOT_PUBLIC)


    # --------------------------------------------------------
    # SAVE INDIVIDUAL CSV FILES
    # --------------------------------------------------------

    pages_df.to_csv(
        PAGES_FILE,
        index=False,
        encoding="utf-8-sig"
    )

    posts_df.to_csv(
        POSTS_FILE,
        index=False,
        encoding="utf-8-sig"
    )

    comments_df.to_csv(
        COMMENTS_FILE,
        index=False,
        encoding="utf-8-sig"
    )


    # --------------------------------------------------------
    # SAVE EXCEL
    # --------------------------------------------------------

    with pd.ExcelWriter(
        EXCEL_FILE,
        engine="openpyxl"
    ) as writer:

        pages_df.to_excel(
            writer,
            sheet_name="Pages",
            index=False
        )

        posts_df.to_excel(
            writer,
            sheet_name="Posts",
            index=False
        )

        comments_df.to_excel(
            writer,
            sheet_name="Comments",
            index=False
        )


# ============================================================
# CREATE COMBINED OUTPUT CSV
# ============================================================

def save_combined_csv(pages, posts, comments):

    print("\nCreating combined output.csv...")


    # --------------------------------------------------------
    # CREATE DATAFRAMES
    # --------------------------------------------------------

    pages_df = pd.DataFrame(pages)

    posts_df = pd.DataFrame(posts)

    comments_df = pd.DataFrame(comments)


    # --------------------------------------------------------
    # HANDLE EMPTY DATA
    # --------------------------------------------------------

    if pages_df.empty:

        print("No page data available.")

        return


    # --------------------------------------------------------
    # CLEAN PAGE DATA
    # --------------------------------------------------------

    pages_df = pages_df.fillna(NOT_PUBLIC)


    # --------------------------------------------------------
    # CLEAN POST DATA
    # --------------------------------------------------------

    if not posts_df.empty:

        posts_df = posts_df.fillna(NOT_PUBLIC)

    else:

        posts_df = pd.DataFrame(
            columns=[
                "page_url",
                "post_url",
                "post_text",
                "reactions",
                "comments",
                "shares"
            ]
        )


    # --------------------------------------------------------
    # CLEAN COMMENT DATA
    # --------------------------------------------------------

    if not comments_df.empty:

        comments_df = comments_df.fillna(NOT_PUBLIC)

    else:

        comments_df = pd.DataFrame(
            columns=[
                "page_url",
                "comment_text"
            ]
        )


    # ========================================================
    # PAGE + POST
    # ========================================================

    if not posts_df.empty:

        combined_df = posts_df.merge(
            pages_df,
            left_on="page_url",
            right_on="url",
            how="left",
            suffixes=("", "_page")
        )

    else:

        combined_df = pages_df.copy()


    # ========================================================
    # PAGE + POST + COMMENT
    # ========================================================

    if not comments_df.empty:

        combined_df = combined_df.merge(
            comments_df,
            on="page_url",
            how="left",
            suffixes=("", "_comment")
        )


    # ========================================================
    # REMOVE DUPLICATES
    # ========================================================

    combined_df = combined_df.drop_duplicates()


    # ========================================================
    # REPLACE EMPTY VALUES
    # ========================================================

    combined_df = combined_df.fillna(NOT_PUBLIC)


    # Replace actual empty strings as well

    combined_df = combined_df.replace(
        "",
        NOT_PUBLIC
    )


    # ========================================================
    # REORDER IMPORTANT COLUMNS
    # ========================================================

    preferred_columns = [

        # Page information
        "page_url",
        "url",
        "page_name",
        "page_type",
        "category",
        "description",
        "phone",
        "email",
        "website",
        "followers",
        "following",
        "members",
        "location",
        "address",
        "business_hours",
        "fashion_keywords",
        "fashion_relevance",
        "verification_status",
        "verification_evidence",
        "scrape_status",

        # Post information
        "post_url",
        "post_text",
        "reactions",
        "comments",
        "shares",

        # Comment information
        "comment_text"
    ]


    # Only use columns that actually exist

    existing_preferred_columns = [
        column
        for column in preferred_columns
        if column in combined_df.columns
    ]


    # Add any remaining columns

    remaining_columns = [
        column
        for column in combined_df.columns
        if column not in existing_preferred_columns
    ]


    final_columns = (
        existing_preferred_columns
        + remaining_columns
    )


    combined_df = combined_df[final_columns]


    # ========================================================
    # SAVE COMBINED CSV
    # ========================================================

    combined_df.to_csv(
        COMBINED_CSV_FILE,
        index=False,
        encoding="utf-8-sig"
    )


    # ========================================================
    # INFORMATION
    # ========================================================

    print("\n" + "=" * 70)

    print("COMBINED CSV CREATED")

    print("=" * 70)

    print(
        f"File: {COMBINED_CSV_FILE}"
    )

    print(
        f"Total rows: {len(combined_df)}"
    )

    print(
        f"Total columns: {len(combined_df.columns)}"
    )

    print(
        f"Pages: {len(pages_df)}"
    )

    print(
        f"Posts: {len(posts_df)}"
    )

    print(
        f"Comments: {len(comments_df)}"
    )

    print("=" * 70)


# ============================================================
# DETERMINE PAGE TYPE
# ============================================================

def get_page_type(url):

    if "/groups/" in url.lower():

        return "Group"

    return "Page"


# ============================================================
# VERIFICATION STATUS
# ============================================================

def get_verification_status(
    extracted,
    scrape_status,
    posts,
    comments
):

    # --------------------------------------------------------
    # ACCESS RESTRICTED
    # --------------------------------------------------------

    if scrape_status == "ACCESS_RESTRICTED":

        return (
            "ACCESS_RESTRICTED",
            "Facebook security restriction detected."
        )


    # --------------------------------------------------------
    # INACCESSIBLE
    # --------------------------------------------------------

    if scrape_status == "INACCESSIBLE":

        return (
            "INACCESSIBLE",
            "Page could not be accessed normally."
        )


    # --------------------------------------------------------
    # INSUFFICIENT DATA
    # --------------------------------------------------------

    if scrape_status == "INSUFFICIENT_DATA":

        return (
            "NEEDS_REVIEW",
            "Insufficient publicly visible information."
        )


    # --------------------------------------------------------
    # COLLECT EVIDENCE
    # --------------------------------------------------------

    evidence = []


    if posts:

        evidence.append(
            f"{len(posts)} public post record(s) observed"
        )


    if comments:

        evidence.append(
            f"{len(comments)} public comment text record(s) observed"
        )


    # --------------------------------------------------------
    # FASHION RELEVANCE
    # --------------------------------------------------------

    fashion_relevance = extracted.get(
        "fashion_relevance",
        "NEEDS_REVIEW"
    )


    if fashion_relevance == "RELEVANT":

        return (
            "UNVERIFIED_RELEVANT",

            "; ".join(evidence)
            if evidence
            else
            "Fashion-related public information observed."
        )


    return (
        "NEEDS_REVIEW",

        "; ".join(evidence)
        if evidence
        else
        "No sufficient fashion-related evidence."
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print("\n" + "=" * 70)

    print(
        "FACEBOOK RESEARCH DATA COLLECTION"
    )

    print("=" * 70)


    # ========================================================
    # CHECK INPUT FILE
    # ========================================================

    input_path = Path(INPUT_FILE)


    if not input_path.exists():

        print(
            f"\nERROR: {INPUT_FILE} not found."
        )

        print(
            "\nPlease create input_urls.csv first."
        )

        return


    # ========================================================
    # READ INPUT URL FILE
    # ========================================================

    try:

        input_df = pd.read_csv(
            INPUT_FILE,
            dtype=str,
            keep_default_na=False
        )

    except Exception as e:

        print(
            f"\nCould not read input CSV: {e}"
        )

        return


    # ========================================================
    # NORMALIZE COLUMN NAMES
    # ========================================================

    input_df.columns = [
        str(column).strip().lower()
        for column in input_df.columns
    ]


    # ========================================================
    # CHECK URL COLUMN
    # ========================================================

    if "url" not in input_df.columns:

        print(
            "\nERROR: input_urls.csv must contain a 'url' column."
        )

        return


    # ========================================================
    # COLLECT UNIQUE FACEBOOK URLS
    # ========================================================

    urls = []


    for value in input_df["url"]:

        url = str(value).strip()


        if not url:
            continue


        if "facebook.com" not in url.lower():
            continue


        if url not in urls:

            urls.append(url)


    print(
        f"\nURLs available: {len(urls)}"
    )


    if not urls:

        print(
            "No Facebook URLs found."
        )

        return


    # ========================================================
    # LOAD PREVIOUS DATA
    # ========================================================

    pages = load_csv(PAGES_FILE)

    posts = load_csv(POSTS_FILE)

    comments = load_csv(COMMENTS_FILE)


    # ========================================================
    # FIND COMPLETED URLS
    # ========================================================

    completed_urls = {

        str(row.get("url", "")).strip()

        for row in pages

        if str(row.get("url", "")).strip()
    }


    print(
        f"Previously processed: {len(completed_urls)}"
    )


    # ========================================================
    # START FACEBOOK SCRAPER
    # ========================================================

    scraper = FacebookScraper()


    try:

        # ----------------------------------------------------
        # FACEBOOK LOGIN
        # ----------------------------------------------------

        scraper.login()


        # ----------------------------------------------------
        # PROCESS URLS
        # ----------------------------------------------------

        for index, url in enumerate(
            urls,
            start=1
        ):

            print(
                "\n" + "#" * 70
            )

            print(
                f"URL {index}/{len(urls)}"
            )

            print("#" * 70)


            # =================================================
            # SKIP ALREADY PROCESSED URLS
            # =================================================

            if url in completed_urls:

                print(
                    "Already processed. Skipping."
                )

                continue


            # =================================================
            # SCRAPE URL
            # =================================================

            try:

                result = scraper.scrape_page(
                    url
                )


                # ------------------------------------------------
                # GET SCRAPED DATA
                # ------------------------------------------------

                body_text = result.get(
                    "body_text",
                    ""
                )


                title = result.get(
                    "title",
                    ""
                )


                scrape_status = result.get(
                    "status",
                    "INSUFFICIENT_DATA"
                )


                page_posts = result.get(
                    "posts",
                    []
                )


                page_comments = result.get(
                    "comments",
                    []
                )


                # ------------------------------------------------
                # EXTRACT PAGE INFORMATION
                # ------------------------------------------------

                extracted = extract_information(
                    body_text,
                    page_title=title
                )


                # ------------------------------------------------
                # PAGE TYPE
                # ------------------------------------------------

                page_type = get_page_type(
                    url
                )


                # ------------------------------------------------
                # VERIFICATION
                # ------------------------------------------------

                (
                    verification_status,
                    evidence
                ) = get_verification_status(
                    extracted,
                    scrape_status,
                    page_posts,
                    page_comments
                )


                # =================================================
                # CREATE PAGE RECORD
                # =================================================

                page_record = {

                    "url": url,

                    "page_type": page_type,

                    "page_name":
                        extracted.get(
                            "page_name",
                            NOT_PUBLIC
                        ),

                    "category":
                        extracted.get(
                            "category",
                            NOT_PUBLIC
                        ),

                    "description":
                        extracted.get(
                            "description",
                            NOT_PUBLIC
                        ),

                    "phone":
                        extracted.get(
                            "phone",
                            NOT_PUBLIC
                        ),

                    "email":
                        extracted.get(
                            "email",
                            NOT_PUBLIC
                        ),

                    "website":
                        extracted.get(
                            "website",
                            NOT_PUBLIC
                        ),

                    "followers":
                        extracted.get(
                            "followers",
                            NOT_PUBLIC
                        ),

                    "following":
                        extracted.get(
                            "following",
                            NOT_PUBLIC
                        ),

                    "members":
                        extracted.get(
                            "members",
                            NOT_PUBLIC
                        ),

                    "location":
                        extracted.get(
                            "location",
                            NOT_PUBLIC
                        ),

                    "address":
                        extracted.get(
                            "address",
                            NOT_PUBLIC
                        ),

                    "business_hours":
                        extracted.get(
                            "business_hours",
                            NOT_PUBLIC
                        ),

                    "fashion_keywords":
                        extracted.get(
                            "fashion_keywords",
                            NOT_PUBLIC
                        ),

                    "fashion_relevance":
                        extracted.get(
                            "fashion_relevance",
                            "NEEDS_REVIEW"
                        ),

                    "verification_status":
                        verification_status,

                    "verification_evidence":
                        evidence,

                    "scrape_status":
                        scrape_status
                }


                # =================================================
                # ADD DATA
                # =================================================

                pages.append(
                    page_record
                )


                posts.extend(
                    page_posts
                )


                comments.extend(
                    page_comments
                )


                # =================================================
                # SAVE IMMEDIATELY
                # =================================================

                save_data(
                    pages,
                    posts,
                    comments
                )


                # =================================================
                # ADD URL TO COMPLETED
                # =================================================

                completed_urls.add(
                    url
                )


                # =================================================
                # CREATE COMBINED CSV
                # =================================================

                save_combined_csv(
                    pages,
                    posts,
                    comments
                )


                # =================================================
                # DISPLAY PROGRESS
                # =================================================

                print(
                    "\nDATA SAVED"
                )

                print(
                    f"Pages: {len(pages)}"
                )

                print(
                    f"Posts: {len(posts)}"
                )

                print(
                    f"Comments: {len(comments)}"
                )

                print(
                    f"Combined CSV: {COMBINED_CSV_FILE}"
                )


            # =================================================
            # ERROR HANDLING
            # =================================================

            except Exception as e:

                print(
                    "\nERROR PROCESSING URL:"
                )

                print(url)

                print(e)


            # =================================================
            # DELAY
            # =================================================

            if index < len(urls):

                print(
                    f"\nWaiting {DELAY_BETWEEN_PAGES} seconds..."
                )

                time.sleep(
                    DELAY_BETWEEN_PAGES
                )


    # ========================================================
    # USER STOPPED SCRIPT
    # ========================================================

    except KeyboardInterrupt:

        print(
            "\n\nStopped by user."
        )

        print(
            "Saving current progress..."
        )


    # ========================================================
    # ALWAYS SAVE
    # ========================================================

    finally:

        print(
            "\nSaving final data..."
        )


        # Save individual files

        save_data(
            pages,
            posts,
            comments
        )


        # Create combined CSV

        save_combined_csv(
            pages,
            posts,
            comments
        )


        # Close browser

        scraper.close()


    # ========================================================
    # FINAL SUMMARY
    # ========================================================

    print(
        "\n" + "=" * 70
    )

    print(
        "COLLECTION COMPLETE"
    )

    print(
        "=" * 70
    )

    print(
        f"Pages: {len(pages)}"
    )

    print(
        f"Posts: {len(posts)}"
    )

    print(
        f"Comments: {len(comments)}"
    )

    print(
        f"\nExcel file: {EXCEL_FILE}"
    )

    print(
        f"Combined CSV: {COMBINED_CSV_FILE}"
    )

    print(
        "=" * 70
    )


# ============================================================
# RUN PROGRAM
# ============================================================

if __name__ == "__main__":

    main()