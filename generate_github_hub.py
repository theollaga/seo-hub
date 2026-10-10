# -*- coding: utf-8 -*-
"""
========================================================================================
[GitHub DA 96점 백링크 허브 전자동 생성기 - 전체 포스트 전량 수집 버전]
- 블로그별 제한(limit) 없이 그동안 발행된 모든 글을 전량 추출하여 README.md 색인표 구성
- Blogger 플랫폼: max-results=500 파라미터를 통해 과거 전체 글 100% 수집
- 네이버 블로그: RSS 제공 최대 글(50편) 전량 수집
========================================================================================
"""

import os
import sys
import json
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "blogs_config.json")
OUTPUT_README = os.path.join(BASE_DIR, "README.md")
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def fetch_all_blog_posts(blog):
    """블로그에서 그동안 발행된 모든 포스트를 제한 없이 전량 추출합니다."""
    feed_url = blog.get("feed_url")
    if not feed_url:
        return []
    
    # Blogger 플랫폼인 경우 max-results=500을 붙여 과거 전체 글 수집
    if "blogger" in blog.get("platform", "") or "theollaga.com" in feed_url or "blogspot.com" in feed_url:
        if "?" in feed_url:
            feed_url += "&max-results=500"
        else:
            feed_url += "?alt=rss&max-results=500"

    posts = []
    for attempt in range(2):
        try:
            req = urllib.request.Request(feed_url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=35) as res:
                xml_data = res.read()
            root = ET.fromstring(xml_data)
            break
        except Exception as e:
            if attempt == 1:
                print(f"⚠️ {blog['name']} 글 수집 중 오류: {e}")
                root = None
            else:
                import time
                time.sleep(2)
    if root is None:
        return []
        
    try:
        # 1. RSS 2.0 파싱
        for item in root.findall('.//item'):
            t = item.find('title')
            l = item.find('link')
            pub_date = item.find('pubDate')
            date_str = pub_date.text.strip() if pub_date is not None and pub_date.text else ""
            if t is not None and l is not None and t.text and l.text:
                posts.append({
                    "title": t.text.strip(),
                    "url": l.text.strip(),
                    "date": date_str
                })
        
        # 2. Atom 파싱 (RSS 결과가 없을 때)
        if not posts:
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            for entry in root.findall('.//atom:entry', ns):
                t = entry.find('atom:title', ns)
                l = entry.find("atom:link[@rel='alternate']", ns) or entry.find("atom:link", ns)
                pub = entry.find('atom:published', ns) or entry.find('atom:updated', ns)
                date_str = pub.text.strip() if pub is not None and pub.text else ""
                if t is not None and l is not None and t.text and l.get('href'):
                    posts.append({
                        "title": t.text.strip(),
                        "url": l.get('href').strip(),
                        "date": date_str
                    })
    except Exception as e:
        print(f"⚠️ {blog['name']} 글 파싱 중 오류: {e}")
        
    # URL 기준 중복 제거
    seen = set()
    unique_posts = []
    for p in posts:
        if p["url"] not in seen:
            seen.add(p["url"])
            unique_posts.append(p)
            
    return unique_posts

def generate_hub():
    print("=== [GitHub DA 96점 백링크 허브] 전체 포스트 전량 수집 시작 ===")
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)
        
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    md_content = f"""# 🌐 Curated Web Knowledge Base & Comprehensive Article Directory
> **Verified High-Authority Knowledge Index & Backlink Registry**  
> *Last Updated: {now_str}*

Welcome to the central knowledge index repository. This open registry provides direct permanent links to comprehensive, fact-checked guides across government policy benefits, small space home organization, personal finance, tax optimization, and smart lifestyle systems.

---

## 📑 Directory Overview
"""

    blog_data = []
    total_articles = 0

    for b in config.get("blogs", []):
        if not b.get("enabled", True):
            continue
        print(f"-> 전체 글 수집 중: {b['name']} ({b['url']})...")
        posts = fetch_all_blog_posts(b)
        total_articles += len(posts)
        blog_data.append((b, posts))
        print(f"   ㄴ 완료: 총 {len(posts)}개 포스트 전량 확보!")

    # 목차 구성
    for b, posts in blog_data:
        anchor = b['name'].replace(" ", "-").replace("_", "-").lower()
        md_content += f"- [{b['name']}](#-{anchor}) ({len(posts)} articles)\n"
    md_content += f"\n**Total Tracked Articles: {total_articles} Verified Guides**\n\n---\n\n"

    # 블로그별 전체 글 섹션
    for b, posts in blog_data:
        md_content += f"## 📌 [{b['name']}]({b['url']})\n"
        md_content += f"- **Platform**: `{b.get('platform', 'Web')}` | **Home**: [{b['url']}]({b['url']}) | **Total Posts**: `{len(posts)}`\n\n"
        
        for idx, p in enumerate(posts, 1):
            md_content += f"{idx}. [{p['title']}]({p['url']})\n"
        md_content += "\n---\n\n"

    md_content += f"""## 🚀 Verification & Syndication Protocol
All links listed in this directory are permanently maintained with active external authority signals:
- **Seed Authority**: GitHub Open Source Ecosystem (Domain Authority: 96/100)
- **Permanent Archiving**: Synchronized with the Internet Archive (Wayback Machine)
- **Instant Search Syndication**: Automated indexing via WebSub, Superfeedr, IndexNow, and XML-RPC hubs
- **Total Published Backlinks**: {total_articles} links
"""

    with open(OUTPUT_README, "w", encoding="utf-8") as f:
        f.write(md_content)
        
    print(f"\n🎉 README.md 전량 갱신 완료! (총 {total_articles}개 고품질 백링크 연결)")
    print(f"저장 위치: {OUTPUT_README}")
    return total_articles

if __name__ == "__main__":
    generate_hub()
