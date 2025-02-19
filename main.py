import asyncio
import os
from typing import List
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
import requests
from xml.etree import ElementTree

# Crowler borrowed from https://github.com/coleam00/Archon/blob/main/iterations/v1-single-agent/crawl_pydantic_ai_docs.py

documents_dir = "c:/Users/johnn/Downloads/examind-knowledge-base"


def get_sitemap_urls(sitemap_url: str) -> List[str]:
    try:
        response = requests.get(sitemap_url)
        response.raise_for_status()

        # Parse the XML
        root = ElementTree.fromstring(response.content)

        # Extract all URLs from the sitemap
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = [loc.text for loc in root.findall('.//ns:loc', namespace)]

        return urls
    except Exception as e:
        print(f"Error fetching sitemap: {e}")
        return []


async def save_document(url: str, markdown: str):
    os.makedirs(documents_dir, exist_ok=True)

    # Remove domain part and replace slashes with hyphens
    filename = url.split("//")[-1]  # Remove http(s)://
    filename = filename.split("/", 1)[-1]  # Remove domain
    filename = filename.replace("/", "-")
    if not filename:
        filename = "index"
    filename = f"{filename}.md"

    # Save with UTF-8 encoding to handle special characters
    with open(os.path.join(documents_dir, filename), "w", encoding='utf-8') as f:
        f.write(markdown)


async def crawl_parallel(urls: List[str], max_concurrent: int = 5):
    """Crawl multiple URLs in parallel with a concurrency limit."""
    browser_config = BrowserConfig(
        headless=True,
        verbose=False,
        extra_args=["--disable-gpu",
                    "--disable-dev-shm-usage", "--no-sandbox"],
    )
    crawl_config = CrawlerRunConfig(cache_mode=CacheMode.BYPASS)

    # Create the crawler instance
    crawler = AsyncWebCrawler(config=browser_config)

    try:
        await crawler.start()

        # Create a semaphore to limit concurrency
        semaphore = asyncio.Semaphore(max_concurrent)

        async def process_url(url: str):
            try:
                async with semaphore:
                    result = await crawler.arun(
                        url=url,
                        config=crawl_config,
                        session_id="session1"
                    )
                    if result.success:
                        print(f"Successfully crawled: {url}")
                        await save_document(url, result.markdown_v2.raw_markdown)
                    else:
                        print(
                            f"Failed to crawl: {url} - Error: {result.error_message}")
            except Exception as e:
                print(f"Error processing {url}: {str(e)}")

        # Process all URLs in parallel with limited concurrency
        await asyncio.gather(*[process_url(url) for url in urls], return_exceptions=True)
    except Exception as e:
        print(f"Error in crawler: {str(e)}")
    finally:
        try:
            await crawler.close()
        except Exception as e:
            print(f"Error closing crawler: {str(e)}")


async def main():
    sitemap_url = "https://examind.gitbook.io/v1/sitemap-pages.xml"

    urls = get_sitemap_urls(sitemap_url)

    if not urls:
        print("No URLs found in sitemap")
        return

    print(f"Found {len(urls)} URLs to crawl")
    await crawl_parallel(urls)

if __name__ == "__main__":
    asyncio.run(main())
