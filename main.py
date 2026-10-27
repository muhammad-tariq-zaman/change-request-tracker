"""Change request tracker: tiny CSV-backed tracker (add/list/status counts)."""
import argparse
import csv
import os
import sys

FIELDS = ["id", "title", "requester", "status"]
STATUSES = ("open", "in-progress", "done", "rejected")


def _read(path):
    if not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _write(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)


def add(path, title, requester):
    rows = _read(path)
    new_id = f"CR-{len(rows) + 1:03d}"
    rows.append({"id": new_id, "title": title, "requester": requester, "status": "open"})
    _write(path, rows)
    return new_id


def list_all(path):
    return _read(path)


def set_status(path, cr_id, status):
    if status not in STATUSES:
        raise ValueError(f"unknown status: {status} (use {', '.join(STATUSES)})")
    rows = _read(path)
    for row in rows:
        if row["id"] == cr_id:
            row["status"] = status
            _write(path, rows)
            return row
    raise KeyError(f"change request not found: {cr_id}")


def counts(path):
    result = {s: 0 for s in STATUSES}
    for row in _read(path):
        result[row["status"]] = result.get(row["status"], 0) + 1
    return result


def main(argv=None):
    p = argparse.ArgumentParser(description="CSV-backed change request tracker.")
    p.add_argument("--db", default="changes.csv")
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add")
    a.add_argument("--title", required=True)
    a.add_argument("--requester", required=True)
    sub.add_parser("list")
    sub.add_parser("count")
    u = sub.add_parser("set-status")
    u.add_argument("id")
    u.add_argument("status")
    args = p.parse_args(argv)
    if args.cmd == "add":
        print(add(args.db, args.title, args.requester))
    elif args.cmd == "list":
        for r in list_all(args.db):
            print(f"{r['id']}  [{r['status']}]  {r['title']} ({r['requester']})")
    elif args.cmd == "count":
        for s, n in counts(args.db).items():
            print(f"{s}: {n}")
    elif args.cmd == "set-status":
        r = set_status(args.db, args.id, args.status)
        print(f"{r['id']} -> {r['status']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
