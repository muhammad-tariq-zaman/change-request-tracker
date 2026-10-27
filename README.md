# change-request-tracker

A tiny CSV-backed change-request tracker: add, list, update status, and
count by status (`open`, `in-progress`, `done`, `rejected`).

## How to run

```bash
python3 main.py --db changes.csv add --title "Upgrade Wi-Fi" --requester ali
python3 main.py --db changes.csv list
python3 main.py --db changes.csv set-status CR-001 done
python3 main.py --db changes.csv count
```

## Example output (sample from test fixture data)

```text
CR-001
CR-001  [done]  Upgrade Wi-Fi (ali)
done: 1
open: 1
```

Standard library only. No network access.
