---
name: jacks-notion-to-planner
description: "Jacks - Notion to Planner. When Jack says he's ready, take everything scheduled in his Notion Social content calendar and set it up in the Nova content planner: titles, captions, platforms and folder links. YouTube is scheduled through the API with the music version only when Jack says so for that run; otherwise everything is left for him to post by hand. Use when Jack says 'Notion to planner', 'set up what's scheduled', 'set up the planner', or asks to automate YouTube for scheduled videos."
---

# Jacks - Notion to Planner

Runs when Jack asks, never by itself. It sets up everything scheduled in Notion so it's ready in the planner.

**The YouTube rule:** only schedule YouTube if Jack says so in this request. If he says nothing about YouTube, he's posting by hand, so don't upload or schedule anything. He adds trending audio on the other platforms himself, so TikTok and Instagram are never scheduled here unless he asks.

Never publish now. Never change a Notion date or stage. Never use `permanent: true` on anything.

## 1. Find what's scheduled

Query data source `dc63cfac-ccf6-4cdc-aa30-35f4ee4775e4` for rows whose `Scheduled date` or `Planned Schedule` is today or later, and any other dates Jack names. Leave out rows at stage `Done`. `Carousel`, `Story`, `Text post`, `Long-form video` and `Short-form video` are templates, not videos, so skip them.

Show nothing back yet unless something is unclear: a row you can't match to a video gets reported in step 6 and left alone.

## 2. Open each planner item

Page through `list_content` (`limit: 100`, following `nextCursor`). Results are saved to files, so filter them with Python. An item matches a row when its `automationKey` ends in the page ID or `notionSyncBindings[].pageId` holds it. If a row hasn't synced, check again later and don't create the item yourself.

Skip any item with a published variant.

## 3. Connect the folder

Match the row name to its video: `Day 14 - Sell Websites to Local Businesses · V2` is `Claude Edits/projects/Series/30 Day AI Series/Day 14 - Sell Websites to Local Businesses/Exports/V2`. One-offs are under `projects/Other Videos/<Title>/Exports/V<n>`. Set `finderPath` with `update_content`, after checking the folder exists.

If a video has no `V<n>` folder, make one and move only that version and its music copy in. Fix the links of any other planner items that pointed at the moved files.

## 4. Set up the content

Only fill what's empty; never overwrite what Jack wrote.

- **Caption and CTA:** from the Notion page's Caption and CTA lines, else the video's `Exports/NOTES.md`. If neither has one, write a plain caption from what he says in the video, and flag it in the report. No invented results or numbers. A version with no day number gets a caption with no day number.
- **Format:** `Short-form video`.
- **Date and time:** leave `plannedDate` to the sync. Set `plannedTime` only if Jack gave one.
- **Platforms:** look up the `Personal` group with `list_groups` and add variants with `add_variants` for its TikTok, YouTube and Instagram accounts, only those in the row's `Platforms`. Use live account IDs. Accounts change, and archived ones are refused. If an existing variant is on an archived account, report it.
- **YouTube title:** `titleOverride` is the hook, under 100 characters.

## 5. Schedule YouTube (only if Jack said so)

Each version's file is `Exports/V<n>/<Label> - V<n> (music).mp4`.

1. **No music copy?** Stop for that video and tell Jack. Never post the plain version instead, and never make music without him asking.
2. **Upload to the YouTube variant only**, so the other platforms stay clean: `upload_media` with `contentId`, `variantId` and `filePath`. If the variant already has a video, check it's the music copy.
3. **Check, then schedule:** `schedule_variant` with `dryRun: true`, then for real, using:
   ```json
   {"provider": "youtube", "privacyStatus": "public", "madeForKids": false, "containsSyntheticMedia": false, "certifyCommunityGuidelines": true, "notifySubscribers": true}
   ```
4. **Time:** `scheduledLocal` from the Notion date and the time Jack gave, else the item's `plannedTime`, else `18:00` (Europe/London), which you must say in the report. Never schedule a time that's already passed; report it instead.
5. **AI footage:** if a video shows a realistic AI-generated person or scene, such as a Genjutsu hook, ask Jack before scheduling how `containsSyntheticMedia` should be set.
6. **Confirm** with `get_variant` that the variant is queued for the right time.

To cancel, use `unschedule_variant`.

## 6. Report

A short table: video and version, date, folder link set or not, caption source, YouTube scheduled at what time or "manual". Then list anything skipped and why, any caption you wrote yourself, and any default time you used.
