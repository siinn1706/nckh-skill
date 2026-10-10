"""One offline engine for six public operations; Python 3.11+ only."""

import argparse
import json
import shutil
import sys
from pathlib import Path

if sys.version_info < (3, 11):
    raise SystemExit("Python 3.11+ required. Install it separately; this installer never downloads Python.")

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from core.build import load_json
from core.install import (SURFACE_HOST, commit_install, doctor, install_identity,
                          plan_install, read_index, inspect_target_paths, target_lock, uninstall)
from core.models import PROFILES
from core.paths import atomic_json, contained
from core.schema import ContractError
from core.hook_config import apply_install_hooks, preview_install_hooks


def choose(label, options):
    print(label + ": " + ", ".join(options), file=sys.stderr)
    result = input("> ").strip()
    if result not in options:
        raise ContractError("invalid choice: " + result)
    return result


def discovery():
    return {"claude-code": shutil.which("claude"), "codex-cli": shutil.which("codex"),
            "cursor-cli": shutil.which("agent"), "agy-cli": shutil.which("agy"),
            "other_surfaces": "select explicitly; a CLI binary does not verify an IDE/app",
            "model_availability": "unverified; no auth secret or trial API inspected"}


def default_package():
    candidates = [ROOT / "dist", ROOT.parent / "packages"]
    for path in candidates:
        if (path / "manifest.json").is_file() or any((path / host / "manifest.json").is_file()
                                                     for host in sorted(set(SURFACE_HOST.values()))):
            return path
    raise ContractError("no default package manifest; tried " + ", ".join(map(str, candidates))
                        + "; supply --package PATH")


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if not argv:
        print("Usage: install.ps1|install.sh OPERATION [OPTIONS]\n"
              "Examples:\n  install.ps1 --help\n  install.ps1 list-skills\n"
              "  install.ps1 install --runtime codex-cli --scope project --project PATH "
              "--kits core --mode copy --models balanced --dry-run")
        return 2
    parser = argparse.ArgumentParser(description="Offline NCKH installer: preview owned changes; never auto-trust hooks or call paid models.")
    parser.add_argument("operation", choices=["install", "update", "doctor", "config-models", "list-skills", "uninstall"])
    parser.add_argument("--package", type=Path)
    parser.add_argument("--runtime", nargs="+", choices=sorted(SURFACE_HOST))
    parser.add_argument("--scope", choices=["project", "global"])
    parser.add_argument("--project", type=Path, default=Path.cwd())
    parser.add_argument("--home", type=Path, default=Path.home(), help="Explicit home root; tests use isolated synthetic homes.")
    parser.add_argument("--kits", nargs="+", choices=["core", "engineer", "marketing"])
    parser.add_argument("--mode", choices=["copy", "symlink"])
    parser.add_argument("--models", choices=sorted(PROFILES))
    parser.add_argument("--capabilities", type=Path, help="Reviewed observed qualification record; never an authorization grant.")
    parser.add_argument("--candidate-evidence", type=Path, help="Update checks bound to candidate closure/source hashes; does not grant update authorization.")
    parser.add_argument("--state-dir", type=Path)
    parser.add_argument("--install-id")
    parser.add_argument("--replace-skill", action="append", default=[], help="Explicit reviewed replacement of only this edited skill; --yes alone never overwrites edits.")
    parser.add_argument("--keep-edited", action="store_true")
    parser.add_argument("--with-agents", action="store_true", default=None, help="Preview optional native agent files; model settings use only observed per-host mappings.")
    parser.add_argument("--hooks", choices=["advisory", "off"], default="advisory",
                        help="Project install/update enables non-blocking checks by default; off skips hook configuration.")
    parser.add_argument("--acknowledge-ancestor-visibility", action="store_true",
                        help="Accept same-name skills visible from ancestor roots, or home-level roots of a project "
                             "install, and record them in the transaction; update keeps only identical recorded "
                             "acknowledgements. Never accepts destination, nested or global-scope sibling duplicates.")
    parser.add_argument("--dry-run", action="store_true", help="Read-only JSON transaction preview.")
    parser.add_argument("--yes", action="store_true", help="Confirm a conflict-free preview; does not bypass rights, trust or user edits.")
    args = parser.parse_args(argv)
    try:
        if args.operation == "list-skills":
            print(json.dumps(load_json(ROOT / "core/registry/catalog/skills.json"), indent=2))
            return 0
        if args.operation in {"install", "update"} and sys.stdin.isatty() and not args.dry_run:
            print(json.dumps({"prerequisite": "Python 3.11+; instruction-only use does not need Python", "detected": discovery()}, indent=2), file=sys.stderr)
            args.runtime = args.runtime or [choose("1. Runtime/surface", sorted(SURFACE_HOST))]
            args.kits = args.kits or [choose("2. Kit (additional kits use --kits)", ["core", "engineer", "marketing"])]
            args.scope = args.scope or choose("3. Scope", ["project", "global"])
            args.mode = args.mode or choose("4. Mode (copy default; symlink needs qualification)", ["copy", "symlink"])
            args.models = args.models or choose("5. Model policy (native mapping remains unverified)", sorted(PROFILES))
        if not args.scope and not (args.state_dir and args.operation in {"doctor", "uninstall"}):
            raise ContractError("--scope required; no silent global target")
        if args.operation in {"install", "update"}:
            # Validate the hooks/scope contract before any filesystem scan; no targets means no reads.
            preview_install_hooks([], args.project, setting=args.hooks, scope=args.scope)
        base = args.project if args.scope == "project" else args.home
        state_dir = args.state_dir or base / ".nckh-state"
        if args.operation == "doctor":
            result = doctor(state_dir)
            result["discovery"] = discovery()
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return 0
        if args.operation == "uninstall":
            if not args.install_id:
                raise ContractError("--install-id required for owned uninstall")
            preview = uninstall(state_dir, args.install_id, dry_run=True)
            if not args.dry_run and not args.yes:
                raise ContractError("review uninstall preview with --dry-run, then confirm --yes")
            print(json.dumps(preview if args.dry_run else uninstall(state_dir, args.install_id, dry_run=False), indent=2))
            return 0
        if not args.runtime:
            raise ContractError("--runtime required")
        package = args.package if args.package is not None else default_package()
        targets = inspect_target_paths(package, args.runtime, scope=args.scope, project=args.project, home=args.home)
        if args.operation == "config-models":
            if not args.models:
                raise ContractError("--models required")
            install_id = install_identity(targets, args.scope)
            existing = read_index(state_dir)["installs"].get(install_id)
            if existing is None:
                raise ContractError("install target before configuring its owned native agents")
            args.kits, args.mode, args.with_agents = existing["kits"], existing["mode"], True
        elif args.operation == "update" and args.with_agents is None:
            existing = read_index(state_dir)["installs"].get(install_identity(targets, args.scope), {})
            args.with_agents = existing.get("with_agents", False)
        if not all([args.kits, args.mode, args.models]):
            raise ContractError("non-interactive requires --runtime --scope --kits --mode --models explicitly")
        capabilities = load_json(args.capabilities) if args.capabilities else {}
        plan = plan_install(targets, read_index(state_dir), kits=args.kits, mode=args.mode,
                            profile=args.models, scope=args.scope, replace_skills=args.replace_skill,
                            keep_edited=args.keep_edited, capabilities=capabilities, operation=args.operation,
                            candidate_evidence=load_json(args.candidate_evidence) if args.candidate_evidence else None,
                            with_agents=bool(args.with_agents),
                            acknowledge_ancestor_visibility=args.acknowledge_ancestor_visibility)
        if args.operation == "update" and plan["install_id"] not in read_index(state_dir)["installs"]:
            raise ContractError("update requires an existing owned install; use install for a new target")
        hook_previews = (preview_install_hooks(targets, args.project, setting=args.hooks, scope=args.scope)
                         if args.operation in {"install", "update"} and not plan["conflicts"] else [])
        hook_summary = [{"host": row["host"], "target": row["target"], "mode": row["mode"],
                         "events": [item["event"] for item in row["definitions"]],
                         "context_status": row["context_status"], "warnings": row["warnings"],
                         "native_qualification": "unverified"} for row in hook_previews]
        if args.dry_run:
            print(json.dumps({"status": "preview", "transaction": plan, "hooks": hook_summary}, ensure_ascii=False, indent=2))
            return 4 if plan["conflicts"] else 0
        if not args.yes:
            print(json.dumps({"transaction": plan, "hooks": hook_summary}, ensure_ascii=False, indent=2), file=sys.stderr)
            if not sys.stdin.isatty() or choose("6. Confirm this transaction", ["confirm", "cancel"]) != "confirm":
                raise ContractError("transaction not confirmed")
        result = commit_install(plan, state_dir)
        try:
            result["hooks"] = apply_install_hooks(hook_previews, grant_reference="confirmed-installer-transaction")
        except (ContractError, OSError, ValueError, KeyError) as error:
            result.update(status="skills-installed-hooks-incomplete", hooks_error=str(error))
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 4
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ContractError, OSError, ValueError, KeyError) as error:
        print(json.dumps({"status": "blocked", "error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 4


if __name__ == "__main__":
    sys.exit(main())
