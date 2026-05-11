#!/usr/bin/env python3
"""
Demo script that exercises the main owgr_client routes and prints sample data.

Usage:
    PYTHONPATH=src python3 demo.py
"""
import json
import sys
import os

# Allow running from repo root without installing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from owgr_client import OwgrClient, OwgrTour
from owgr_client.models.owgr_player import OwgrPlayer


def section(title):
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}\n")


def main():
    client = OwgrClient()

    # ── 1. Get Tours ──────────────────────────────────────────
    section("1. GET TOURS")
    tours = client.get_tours()
    print(f"Total tours: {len(tours)}\n")
    print(f"{'ID':>4}  {'Code':<8}  {'Name'}")
    print(f"{'--':>4}  {'----':<8}  {'----'}")
    for t in tours[:15]:
        print(f"{t['tourId']:>4}  {t['code']:<8}  {t['name']}")
    if len(tours) > 15:
        print(f"  ... and {len(tours) - 15} more")

    # ── 2. Get Events (PGA Tour, current year) ────────────────
    section("2. GET EVENTS (PGA Tour, 2025)")
    events = client.get_events(tour=OwgrTour.PGATour, year=2025)
    event_list = events["eventsList"]
    print(f"Total events: {events['totalNumberOfEvents']}\n")
    print(
        f"{'ID':>6}  {'Wk':>3}  {'Event':<40}  "
        f"{'Winner':<25}  {'Pts':>8}"
    )
    print(
        f"{'--':>6}  {'--':>3}  {'-----':<40}  "
        f"{'------':<25}  {'---':>8}"
    )
    for ev in event_list[:10]:
        winner = ""
        pts = ""
        if ev.get("winners"):
            w = ev["winners"][0]
            winner = w["player"]["fullName"]
            pts = f"{w['pointsAwarded']:.2f}"
        print(
            f"{ev['id']:>6}  {ev['weekNumber']:>3}  "
            f"{ev['name']:<40}  {winner:<25}  {pts:>8}"
        )
    if len(event_list) > 10:
        print(f"  ... and {len(event_list) - 10} more events")

    # ── 3. Get Events with legacy string code ─────────────────
    section("3. GET EVENTS (legacy code 'Maj', 2025)")
    majors = client.get_events(tour="Maj", year=2025)
    for ev in majors["eventsList"]:
        winner = ""
        if ev.get("winners"):
            winner = ev["winners"][0]["player"]["fullName"]
        print(f"  {ev['name']:<40}  Winner: {winner}")

    # ── 4. Get Event Details + Results ────────────────────────
    section("4. GET EVENT DETAILS + RESULTS")
    major_id = majors["eventsList"][0]["id"]
    major_name = majors["eventsList"][0]["name"]
    print(f"Fetching details for: {major_name} (id={major_id})\n")
    event_detail = client.get_event_by_id(major_id)
    print(f"  Name:        {event_detail['name']}")
    print(f"  Field Size:  {event_detail['fieldSize']}")
    print(f"  Rounds:      {event_detail['scheduledRoundsCount']}")
    print(f"  Start:       {event_detail['startDate'][:10]}")
    print(f"  End:         {event_detail['endDate'][:10]}")
    tour_names = ", ".join(t["name"] for t in event_detail["tours"])
    print(f"  Tour(s):     {tour_names}")

    results = event_detail.get("results", [])
    print(f"\n  Results ({len(results)} players):\n")
    print(
        f"  {'Pos':>4}  {'Player':<30}  "
        f"{'Country':<15}  {'Points':>8}"
    )
    print(
        f"  {'---':>4}  {'------':<30}  "
        f"{'-------':<15}  {'------':>8}"
    )
    for r in results[:15]:
        name = r["player"]["fullName"]
        country = r["player"]["country"]["name"]
        pts = f"{r['pointsAwarded']:.4f}"
        pos = r["finishPosition"]
        print(
            f"  {pos:>4}  {name:<30}  "
            f"{country:<15}  {pts:>8}"
        )
    if len(results) > 15:
        print(f"  ... and {len(results) - 15} more")

    # ── 5. Get Player Profile ─────────────────────────────────
    section("5. GET PLAYER PROFILE (Scottie Scheffler)")
    player_data = client.get_player_by_id(18417)
    profile = player_data["profile"]
    player_info = profile["player"]
    print(f"  Name:       {player_info['fullName']}")
    print(f"  Country:    {player_info['country']['name']}")
    print(f"  OWGR Rank:  {profile['currentOWGRRank']}")
    print(f"  Best Rank:  {profile['bestOWGRRank']}")
    print(f"  Avg Points: {profile['pointsAverage']}")
    print(f"  Total Pts:  {profile['pointsTotal']:.2f}")

    events_table = player_data["events"]
    print(f"\n  Recent events ({len(events_table)} total):\n")
    print(
        f"  {'Year':>5}  {'Wk':>3}  {'Event':<35}  "
        f"{'Finish':>6}  {'Points':>10}"
    )
    print(
        f"  {'----':>5}  {'--':>3}  {'-----':<35}  "
        f"{'------':>6}  {'------':>10}"
    )
    for e in events_table[:10]:
        pts = f"{e['rankPoints']:.4f}"
        tour_codes = ", ".join(t["code"] for t in e["tours"])
        print(
            f"  {e['year']:>5}  {e['week']:>3}  "
            f"{e['event']:<35}  {e['finish']:>6}  {pts:>10}"
        )
    if len(events_table) > 10:
        print(f"  ... and {len(events_table) - 10} more events")

    print(f"\n  Active years: {player_data['years']}")

    # ── 6. OwgrPlayer model ───────────────────────────────────
    section("6. OWGR PLAYER MODEL")
    player = OwgrPlayer.from_api_data(player_data)
    print(f"  player.name    = {player.name}")
    print(f"  player.id      = {player.id}")
    print(f"  player.stats   = {json.dumps(player.stats, indent=15, default=str)}")
    print(f"  player.results = [{len(player.results)} events]")
    print(f"  player.years   = {player.years}")

    section("DONE")
    print("All routes exercised successfully!\n")


if __name__ == "__main__":
    main()
