"""lao command-line interface.

Commands:
  lao init             Bootstrap a working LAO runtime (dirs + config + sample event)
  lao trust-event      Interactive wizard to record a Trust Event
  lao verify           Recompute + display VerifyPing hashes for the ledger
  lao status           Show counts: trust events, verified, anchors
  lao demo             Run the 6-function capability demo
"""
from __future__ import annotations

import argparse
import os
import sys
from typing import Optional

from .schema import TrustEventLedger
from .init import init as _init


def _cmd_init(args) -> int:
    r = _init(workdir=args.dir, agent=args.agent, sample=not args.no_sample)
    print("✅ LAO initialized")
    print(f"   ledger : {r['ledger']}")
    print(f"   events : {r['events']}")
    if r.get("sample_event"):
        print(f"   sample : {r['sample_event']} (verified, hashed)")
    print("\nNext:  lao trust-event   # record a real event")
    return 0


def _cmd_trust_event(args) -> int:
    ledger = TrustEventLedger()
    try:
        import json as _json
        base = args.dir or os.getcwd()
        cfg_path = os.path.join(base, "lao.json")
        agent = args.agent
        if os.path.exists(cfg_path):
            import json
            agent = json.load(open(cfg_path)).get("agent", agent)
    except Exception:
        pass

    # Non-interactive mode (from script)
    if args.desc:
        from .schema import make_event
        ev = make_event(
            agent=agent, etype=args.type, description=args.desc,
            evidence=args.evidence, repair=args.repair,
            new_anchor=args.anchor, future_prevention=args.prevention,
            ledger=ledger,
        )
        print(f"✅ Trust Event recorded: {ev.event_id}")
        print(f"   type={ev.type} status={ev.status}")
        print(f"   hash={ev.hash[:16]}… (verified)")
        return 0

    # Interactive wizard
    print("LAO Trust Event Wizard")
    print("-" * 40)
    etype = input("Type [success/failure]: ").strip() or "success"
    desc = input("Description (what happened?): ").strip()
    if not desc:
        print("❌ description required")
        return 2
    evidence = input("Evidence (reproducible?): ").strip()
    repair = input("Repair (if failure): ").strip()
    from .schema import make_event
    ev = make_event(agent=agent, etype=etype, description=desc,
                    evidence=evidence, repair=repair, ledger=ledger)
    print(f"\n✅ Trust Event recorded: {ev.event_id}")
    print(f"   hash={ev.hash[:16]}… (verified)")
    return 0


def _cmd_verify(args) -> int:
    ledger = TrustEventLedger()
    events = ledger.load()
    if not events:
        print("No trust events yet. Run:  lao trust-event")
        return 0
    verified = sum(1 for e in events if e.verify())
    print(f"Trust Events: {len(events)} | Verified: {verified}")
    for e in events:
        ok = e.verify()
        print(f"  {'✅' if ok else '❌'} {e.event_id} [{e.type}] {e.hash[:12]}…")
    return 0 if verified == len(events) else 1


def _cmd_status(args) -> int:
    ledger = TrustEventLedger()
    events = ledger.load()
    verified = sum(1 for e in events if e.verify())
    print(f"LAO Status")
    print(f"  trust events : {len(events)}")
    print(f"  verified     : {verified}")
    from .schema import DEFAULT_LEDGER
    print(f"  ledger       : {os.environ.get('LAO_LEDGER', DEFAULT_LEDGER)}")
    anchors = os.path.join(args.dir or os.getcwd(), "live", "anchors")
    na = len([f for f in os.listdir(anchors) if os.path.isfile(os.path.join(anchors, f))]) if os.path.isdir(anchors) else 0
    print(f"  anchors      : {na}")
    return 0


def _cmd_demo(args) -> int:
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
        import subprocess
        demo = os.path.join(os.path.dirname(__file__), "..", "demo_record.py")
        if os.path.exists(demo):
            return subprocess.call([sys.executable, demo])
    except Exception:
        pass
    print("Demo script not found next to package.")
    return 1


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="lao", description="LAO reliability plugin")
    sub = p.add_subparsers(dest="command", required=True)

    si = sub.add_parser("init", help="Bootstrap a working LAO runtime")
    si.add_argument("--dir", default=None, help="target directory (default: cwd)")
    si.add_argument("--agent", default="demo", help="agent id (default: demo)")
    si.add_argument("--no-sample", action="store_true", help="skip sample event")
    si.set_defaults(func=_cmd_init)

    st = sub.add_parser("trust-event", help="Record a Trust Event")
    st.add_argument("--dir", default=None, help="target directory")
    st.add_argument("--agent", default=None, help="agent id")
    st.add_argument("--type", default="success", choices=["success", "failure"])
    st.add_argument("--desc", default=None, help="non-interactive description")
    st.add_argument("--evidence", default="")
    st.add_argument("--repair", default="")
    st.add_argument("--anchor", action="append", default=None)
    st.add_argument("--prevention", default="")
    st.set_defaults(func=_cmd_trust_event)

    sv = sub.add_parser("verify", help="Recompute VerifyPing hashes")
    sv.set_defaults(func=_cmd_verify)

    ss = sub.add_parser("status", help="Show trust event / anchor counts")
    ss.add_argument("--dir", default=None)
    ss.set_defaults(func=_cmd_status)

    sd = sub.add_parser("demo", help="Run the 6-function demo")
    sd.set_defaults(func=_cmd_demo)

    return p


def main(argv: Optional[list] = None) -> int:
    p = build_parser()
    args = p.parse_args(argv)
    try:
        return args.func(args)
    except KeyboardInterrupt:
        print("\naborted")
        return 130
    except Exception as e:  # noqa: BLE001
        print(f"❌ {type(e).__name__}: {e}")
        return 1


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
