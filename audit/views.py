from urllib.parse import urlparse
import time
import requests
from bs4 import BeautifulSoup

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import WebsiteAnalysis


def home(request):
    return render(request, "index.html")


def is_valid_url(url):
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)
    return bool(parsed.scheme and parsed.netloc)


@api_view(["POST"])
def analyze_url(request):

    url = request.data.get("url")

    if not url:
        return Response(
            {"error": "Please enter a website URL."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    url = url.strip()

    if not is_valid_url(url):
        return Response(
            {
                "error": "Please enter a valid website URL (e.g., google.com or https://google.com)."
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:

        start = time.time()

        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        response_time = round(time.time() - start, 2)

        content_type = response.headers.get("Content-Type", "")

        if "text/html" not in content_type:
            return Response(
                {"error": "URL does not contain HTML content."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        soup = BeautifulSoup(response.text, "lxml")

        # ---------- Title ----------

        title = (
            soup.title.string.strip()
            if soup.title and soup.title.string
            else "No Title"
        )

        # ---------- Meta Description ----------

        meta = soup.find("meta", attrs={"name": "description"})

        meta_description = (
            meta.get("content").strip()
            if meta and meta.get("content")
            else "No Meta Description"
        )

        # ---------- H1 ----------

        h1_count = len(soup.find_all("h1"))

        # ---------- Images ----------

        images = soup.find_all("img")

        missing_alt = sum(
            1 for img in images if not img.get("alt")
        )

        # ---------- Word Count ----------

        words = soup.get_text(
            separator=" ",
            strip=True
        ).split()

        # ---------- Links ----------

        links = soup.find_all("a")

        # ---------- SEO SCORE ----------

        seo_score = 0

        if title != "No Title":
            seo_score += 20

        if 10 <= len(title) <= 60:
            seo_score += 10

        if meta_description != "No Meta Description":
            seo_score += 20

        if 50 <= len(meta_description) <= 160:
            seo_score += 10

        if h1_count >= 1:
            seo_score += 15

        if len(images) > 0:

            alt_percentage = (
                (len(images) - missing_alt)
                / len(images)
            ) * 100

            if alt_percentage >= 90:
                seo_score += 15
            elif alt_percentage >= 70:
                seo_score += 10
            elif alt_percentage >= 50:
                seo_score += 5

        else:
            seo_score += 15

        if url.startswith("https://"):
            seo_score += 10

        # ---------- PERFORMANCE GRADE ----------

        if seo_score >= 90:
            grade = "A"
        elif seo_score >= 80:
            grade = "B"
        elif seo_score >= 70:
            grade = "C"
        elif seo_score >= 60:
            grade = "D"
        else:
            grade = "F"

        # ---------- Favicon ----------

        domain = urlparse(url).netloc

        favicon = (
            f"https://www.google.com/s2/favicons?domain={domain}&sz=64"
        )

        # ---------- Save to Database ----------

        WebsiteAnalysis.objects.create(
            url=url,
            title=title,
            seo_score=seo_score,
            status_code=response.status_code,
            response_time=f"{response_time} sec",
            word_count=len(words),
            total_links=len(links),
            total_images=len(images),
        )

        return Response(
            {
                "status": response.status_code,
                "response_time": f"{response_time} sec",
                "title": title,
                "meta_description": meta_description,
                "h1_count": h1_count,
                "images_missing_alt": missing_alt,
                "word_count": len(words),
                "total_images": len(images),
                "total_links": len(links),
                "seo_score": seo_score,
                "grade": grade,
                "favicon": favicon,
            }
        )

    except requests.exceptions.Timeout:
        return Response(
            {"error": "Request timed out."},
            status=status.HTTP_408_REQUEST_TIMEOUT,
        )

    except requests.exceptions.ConnectionError:
        return Response(
            {"error": "Unable to connect to the website."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )