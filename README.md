# Douyin API Python

Call Douyin (the Chinese TikTok) from Python: search videos by keyword with likes, comments, shares and saves, then pull the comments of a video with likes, reply counts and the commenter's region. You do not need a Douyin developer account or a mainland China network: each call is one POST request to the EveryInfra API.

Also covers: Douyin API alternative, Douyin scraper.

## Quick start

```bash
git clone https://github.com/everyinfra/douyin-api-python.git
cd douyin-api-python
pip install -r requirements.txt
export EVERYINFRA_API_KEY=your_key   # get one at everyinfra.com
python main.py search 咖啡 --out videos.csv
python main.py comments https://www.douyin.com/video/<id> --out comments.csv
```

Get an API key: [everyinfra.com/en/docs](https://everyinfra.com/en/docs?utm_source=github&utm_medium=example_repo&utm_campaign=douyin-api-python#quickstart). Without `--out`, the script prints the first three rows as JSON.

## Price

| Call | Price per 1,000 calls | Rows per call |
|---|---|---|
| [`douyin/search`](https://everyinfra.com/en/douyin-api/search?utm_source=github&utm_medium=example_repo&utm_campaign=douyin-api-python) | $8.33 | 10 in our test |
| [`douyin/comments`](https://everyinfra.com/en/douyin-api/comments?utm_source=github&utm_medium=example_repo&utm_campaign=douyin-api-python) | $0.56 | 20 in our test |

- You pay per call, not per month. Failed calls and empty results are not charged.
- New accounts can claim $1 of trial credit: create an account, star [everyinfra-agent-plugins](https://github.com/everyinfra/everyinfra-agent-plugins) and [seo-skills](https://github.com/everyinfra/seo-skills), then claim it in the console. It is valid for 24 hours and needs no card. See [pricing](https://everyinfra.com/en/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=douyin-api-python).

## What you get

### `search`

| Field | Meaning |
|---|---|
| `next_page_token` | Page token (search / user_posts / comments / comment_replies / billboard_video_hot / billboard_low_fan_explosion / billboard_high_completion / billboard_account_search / music_search): pass it back unchanged as page_token to fetch the next page, keeping the other parameters the same; valid for 24 hours. Every row of a page carries the same value, which also appears at the top level of the response. Absent on the last page. Comment pages walk all top-level comments page by page. |
| `id` | The record's unique ID on the platform. Unique only within one platform; IDs can repeat across platforms. |
| `url` | Link to the record on the platform. |
| `text` | Body text with HTML removed, returned in full and never cut short (on a few platforms the list results themselves carry only an excerpt; the platform's field notes say so). |
| `media_type` | Media type: video, or image for image posts. |
| `video_url` | Video playback URL (signed, expires; download promptly if you need to keep it). Null for image posts or when the source omits it. |
| `like_count` | Likes. null means the platform or this capability does not disclose it; it is not 0. |
| `comment_count` | Comments. null means not disclosed, not 0. |
| `share_count` | Shares. null means not disclosed, not 0. |
| `collect_count` | Saves or favorites. null means not disclosed, not 0. |
| `view_count` | Play count. Douyin does not publish play counts, so this field never carries real plays; judge reach by like_count, comment_count and share_count. |
| `author_name` | Author's display name. |
| `author_id` | Author's unique ID on the platform. |
| `author_douyin_id` | The author's Douyin ID. |
| `author_uid` | Numeric user ID of the author (on comments, of the commenter). author_id is the secUid; both identify the same person. |
| `author_bio` | The author's profile bio (search / user_posts / video rows). |
| `author_avatar_url` | Author avatar image URL: the creator on search, user_posts and video rows, the commenter on comments rows. |
| `author_follower_count` | Author's follower count. null means not disclosed. |
| `cover_image_url` | Video or image-post cover thumbnail URL (search / user_posts rows). |
| `video_width` | Video frame width in pixels. |
| `video_height` | Video frame height in pixels. |
| `duration_seconds` | Duration in seconds. null for content that is not video or audio. |
| `region` | Region. |
| `hashtags` | Hashtags in the text, in order of appearance; absent when there are none. |
| `posted_at` | Publish time in ISO 8601, UTC (for example 2026-08-07T12:34:56+00:00). Non-standard strings from the platform are passed through as is, so parse defensively. null means the platform does not disclose it. |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |
| `image_urls` | Array of image links in the platform's display order; absent when there are no images. |
| `duration_sec` | Video length in seconds. |
| `author_is_verified` | Whether the author is verified (search / user_posts / video rows). |
| `author_following_count` | How many accounts the author follows (search / user_posts / video rows). |
| `author_like_count` | Total likes the author's profile has received (search / user_posts / video / transcript). |
| `author_video_count` | Total number of posts on the author's profile (search / user_posts / video rows). |
| `author_ip_location` | The author's IP location, which Douyin displays on every profile. |
| `title` | Title. null when the platform has no titles (for example text-only posts). |
| `music` | Background track: id, title, author, is_original (original sound or not), duration_sec, cover_url and play_url (audio link, may expire). Absent when there is no music information. |
| `download_count` | How many times the post was downloaded. |
| `forward_count` | How many times the post was forwarded. |
| `is_pinned` | Whether the item is pinned (post rows: pinned on the author's profile; trending: pinned on the board). |
| `is_ad` | Whether the post is an ad. |
| `video_tags` | Content category tags Douyin assigned to the post (for example food or store visit). |
| `video_resolution` | Video quality tier as Douyin labels it (for example 720p). |
| `animated_cover_url` | Animated cover link. |
| `city` | City name in the platform's language, not normalized. |
| `location` | Location description passed through as is; the format varies by platform. |

Also returned, named as on the platform: `hashtag_ids`, `search_rank`, `city_code`, `text_language`, `video_bitrates`, `download_url`, `has_watermark`, `video_url_expires_at`, `permissions`, `author_gender`, `author_age`.

Full parameter list: [Douyin search API](https://everyinfra.com/en/douyin-api/search?utm_source=github&utm_medium=example_repo&utm_campaign=douyin-api-python).

### `comments`

| Field | Meaning |
|---|---|
| `next_page_token` | Page token (search / user_posts / comments / comment_replies / billboard_video_hot / billboard_low_fan_explosion / billboard_high_completion / billboard_account_search / music_search): pass it back unchanged as page_token to fetch the next page, keeping the other parameters the same; valid for 24 hours. Every row of a page carries the same value, which also appears at the top level of the response. Absent on the last page. Comment pages walk all top-level comments page by page. |
| `id` | The record's unique ID on the platform. Unique only within one platform; IDs can repeat across platforms. |
| `text` | Body text with HTML removed, returned in full and never cut short (on a few platforms the list results themselves carry only an excerpt; the platform's field notes say so). |
| `like_count` | Likes. null means the platform or this capability does not disclose it; it is not 0. |
| `reply_count` | Replies, usually replies to a comment. null means not disclosed. |
| `author_name` | Author's display name. |
| `author_id` | Author's unique ID on the platform. |
| `ip_location` | IP region Douyin displays (set by the platform, not entered by the user). |
| `is_hot` | Whether the comment carries Douyin's hot-comment badge (comments). |
| `is_reply` | Whether the row is a reply. |
| `reply_to_id` | ID of the top-level comment this reply sits under: on `comments` reply rows, the comment it hangs from; on every `comment_replies` row, the comment you asked about. |
| `posted_at` | Publish time in ISO 8601, UTC (for example 2026-08-07T12:34:56+00:00). Non-standard strings from the platform are passed through as is, so parse defensively. null means the platform does not disclose it. |
| `video_id` | ID of the video the comment belongs to (comments). |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |
| `liked_by_author` | Whether the video's author liked the comment; comments the author liked tend to carry more weight. |
| `author_avatar_url` | Author avatar image URL: the creator on search, user_posts and video rows, the commenter on comments rows. |
| `author_uid` | Numeric user ID of the author (on comments, of the commenter). author_id is the secUid; both identify the same person. |
| `images` | Array of image links in the platform's display order; absent when there are no images. |
| `mentioned_users` | People @-mentioned in the comment, each with user_id (secUid), uid (numeric ID) and nickname. Absent when nobody is mentioned. |

Full parameter list: [Douyin comments API](https://everyinfra.com/en/douyin-api/comments?utm_source=github&utm_medium=example_repo&utm_campaign=douyin-api-python).

## Tested

We ran both commands against the live API before publishing this repository (times in Singapore time, UTC+8).

| Command | Run at (SGT) | Rows | Charged |
|---|---|---|---|
| `search 咖啡` | 2026-11-08 03:37 | 10 | $0.008333 |
| `comments https://www.douyin.com/video/<id>` | 2026-11-08 03:37 | 20 | $0.000556 |

First row of the `search` result (long text cut, author fields left out of this sample):

```json
{
  "id": "7510430154377334075",
  "url": "https://www.douyin.com/video/7510430154377334075",
  "text": "咖啡不再傻傻分不清 #咖啡#中国成都国际非遗节 #百young非遗计划",
  "media_type": "video",
  "like_count": 2153372,
  "comment_count": 42444,
  "share_count": 961296,
  "collect_count": 448215,
  "region": "CN",
  "posted_at": "2025-05-31T02:24:50+00:00",
  "platform": "douyin",
  "title": "咖啡不再傻傻分不清",
  "is_pinned": false,
  "video_width": 1080,
  "video_height": 1920,
  "duration_sec": 37,
  "hashtags": [
    "咖啡",
    "中国成都国际非遗节",
    "百young非遗计划"
  ],
  "duration_seconds": 37
}
```

## How it works

Every call is one request. `everyinfra.py` wraps it in about 60 lines of `requests`:

```bash
curl -X POST https://api.everyinfra.com/api/v1/social \
  -H "Authorization: Bearer $EVERYINFRA_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"platform": "douyin", "action": "search", "params": {"keyword": "咖啡"}}'
```

- Slow actions (Instagram `user_posts`, for example) answer with a `job_id`. The script polls `GET /api/v1/jobs/{job_id}` every 5 seconds; polling is free.
- Errors come back as JSON with a code, a message and whether you were charged. A missing parameter returns 422 before any charge.
- The same key also works over MCP for Claude, Cursor and other AI agents: [docs](https://everyinfra.com/en/docs?utm_source=github&utm_medium=example_repo&utm_campaign=douyin-api-python).

## More

- [Douyin API on EveryInfra](https://everyinfra.com/en/douyin-api?utm_source=github&utm_medium=example_repo&utm_campaign=douyin-api-python): every Douyin action, with prices and live health
- Other examples: [google-maps-scraper](https://github.com/everyinfra/google-maps-scraper) · [instagram-scraper-python](https://github.com/everyinfra/instagram-scraper-python) · [tiktok-trends-api](https://github.com/everyinfra/tiktok-trends-api) · [tiktok-scraper-python](https://github.com/everyinfra/tiktok-scraper-python)

## License

MIT
