---
name: planner-delivery
description: Put a finished video into Jack's system. Adds one row per version to the Ready to Post column of his Notion Social content database, then opens each synced item in the Nova content planner and points its folder link at that version's assets. Use after delivering any video, or when Jack asks to add a video to Notion or the content planner, add its assets, or fix a folder link. Never posts or schedules.
---

# Planner delivery

Notion's Social content database syncs with the Nova content planner. A video goes in Notion, the sync creates its planner item, and that item's folder link (`finderPath`, the Open in Finder button on its Assets tab) points at the files. Do this when a video is delivered, and again only if a version is added.

**Never** post, schedule, change dates, write captions or touch variants. Never set `Nova sync ID` or any formula, rollup or button in Notion.

## 1. Check the folders

Each version has its own folder, and only that version's files go in it:
```
Exports/V1/Day 15 - V1.mp4
Exports/V1/Day 15 - V1 (music).mp4
Exports/V2/Day 15 - V2.mp4
```
`tools/render-trials.sh` writes there. Thumbnails, `NOTES.md` and `Drafts/` stay in `Exports/`.

## 2. Add one Notion row per version

Parent: data source `dc63cfac-ccf6-4cdc-aa30-35f4ee4775e4`. One row for each of V1, V2, V3. **A music copy never gets its own row**; it's in its version's folder.

Search the database for the video first. If a row already exists for this exact video, use it for V1 instead of adding a duplicate, and set its stage to Ready to Post. An idea row with a different topic isn't a match, even with the same day number; leave it and tell Jack.

| Property | Value |
| --- | --- |
| Name | `<Video folder name> · V1`, e.g. `Day 15 - Turn a Listing Into a Website · V1` |
| Production stage | `Ready to Post` |
| Greenlight | `__YES__` |
| Type / Format | `Short` / `Video` |
| Content tags | `["Short form","Video"]` |
| Platforms | `["TikTok","YouTube","Instagram"]` unless Jack says otherwise |
| Project | `https://app.notion.com/p/3fe4e142aa7d8196aad2f7ff6ba7b852` |
| Notes | One line: length and what's different about this version |
| Planned Schedule | `date:Planned Schedule:start` = the date Jack gave, else the day it's delivered, with `date:Planned Schedule:is_datetime` 0. **The sync only picks up rows with a date.** It's a calendar date he can move, not a post time |

Keep the page ID each row returns. Leave the page body blank.

## 3. Find each synced item in the planner

Page through `list_content` with `limit: 100`, following `nextCursor` to the end. There's no search and the order isn't by date, so scan everything. The results are too big for the chat and get saved to files; filter those with Python. The item for a page has either:
- `automationKey` ending in the page ID (`notion:<data source>:<page id>`), or
- that ID in `notionSyncBindings[].pageId`.

A dated row usually arrives within about 5 minutes (Day 14's took under 15). If an item isn't there yet, check again later rather than creating it yourself. If it still hasn't appeared after a few checks, tell Jack which rows are waiting.

## 4. Add the assets

For each item, call `update_content` with only:
```json
{"finderPath": "/Volumes/Extreme Pro/Jack - Organized/04 Media/Video Editing/Claude Edits/projects/<place>/Exports/V1"}
```
Use `assets-<page id>` as the `automationKey`. Link the version's folder, not a single file, so Jack gets the plain and music copies together. The Notion sync doesn't overwrite this field.

Check the path exists before writing, and that the result shows the new `finderPath`.

## 5. Report

List each version with its Notion link and whether its folder link is set. Name anything still waiting on the sync.

## If a folder moves

Links are absolute paths. After moving or renaming a video folder, scan for `finderPath` values under the old path and repoint them.
