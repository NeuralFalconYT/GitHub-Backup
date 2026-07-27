#!/usr/bin/env python3
"""
GitHub Repo Backup Tool — Premium Terminal UI
------------------------------------------------
Clones every repo (public + private) belonging to a GitHub account into
./{username}_backup/

Requires:
    pip install rich requests
"""

import os
import sys
import subprocess

import requests

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import (
    Progress,
    SpinnerColumn,
    BarColumn,
    TextColumn,
    TimeElapsedColumn,
)
from rich.prompt import Prompt
from rich import box

console = Console()

BANNER = r"""
[bold cyan] ██████╗ ██╗████████╗██╗  ██╗██╗   ██╗██████╗ [/bold cyan]
[bold cyan]██╔════╝ ██║╚══██╔══╝██║  ██║██║   ██║██╔══██╗[/bold cyan]
[bold cyan]██║  ███╗██║   ██║   ███████║██║   ██║██████╔╝[/bold cyan]
[bold cyan]██║   ██║██║   ██║   ██╔══██║██║   ██║██╔══██╗[/bold cyan]
[bold cyan]╚██████╔╝██║   ██║   ██║  ██║╚██████╔╝██████╔╝[/bold cyan]
[bold cyan] ╚═════╝ ╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ [/bold cyan]
      [white]B A C K U P   T O O L[/white]  [dim]v1.0[/dim]
"""


def get_credentials() -> tuple[str, str]:
    console.print(Panel.fit(BANNER, border_style="cyan", box=box.DOUBLE))
    console.print(
        Panel(
            "[white]Backup all your GitHub projects — public and private — "
            "into a local folder on your machine.[/white]\n\n"
            "[dim]Your token is only used locally to talk to the GitHub API "
            "and to authenticate git clones. It is never stored or sent "
            "anywhere else.[/dim]",
            title="[bold]About[/bold]",
            border_style="blue",
        )
    )
    console.print()

    username = Prompt.ask("[bold cyan]›[/bold cyan] GitHub username").strip()
    console.print(
        "[dim]  Tip: create a fine-grained Personal Access Token with "
        "'repo' read access at https://github.com/settings/tokens[/dim]"
    )
    token = Prompt.ask("[bold cyan]›[/bold cyan] GitHub access token").strip()

    if not username or not token:
        console.print("[bold red]✗ Username and token are both required.[/bold red]")
        sys.exit(1)

    return username, token


def fetch_all_repos(username: str, token: str) -> list[dict]:
    url = "https://api.github.com/user/repos"
    headers = {"Accept": "application/vnd.github+json"}
    auth = (username, token)

    repos = []
    page = 1

    with console.status("[bold cyan]Connecting to GitHub API...", spinner="dots"):
        resp = requests.get(f"{url}?per_page=1&page=1", auth=auth, headers=headers)

    if resp.status_code == 401:
        console.print(
            Panel(
                "[bold red]Authentication failed.[/bold red]\n"
                "Check that your username and token are correct, and that "
                "the token has 'repo' scope.",
                border_style="red",
            )
        )
        sys.exit(1)
    elif resp.status_code != 200:
        console.print(f"[bold red]✗ GitHub API error {resp.status_code}:[/bold red] {resp.text}")
        sys.exit(1)

    with Progress(
        SpinnerColumn(),
        TextColumn("[cyan]Fetching repository list...[/cyan] page {task.fields[page]}"),
        TimeElapsedColumn(),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task("fetch", page=1)
        page = 1
        while True:
            progress.update(task, page=page)
            r = requests.get(f"{url}?per_page=100&type=all&page={page}", auth=auth, headers=headers)
            if r.status_code != 200:
                console.print(f"[bold red]✗ Failed to fetch page {page}:[/bold red] {r.text}")
                break
            batch = r.json()
            if not batch:
                break
            repos.extend(batch)
            page += 1

    return repos


def clone_repos(username: str, token: str, repos: list[dict], backup_dir: str) -> dict:
    os.makedirs(backup_dir, exist_ok=True)

    results = {"cloned": [], "skipped": [], "failed": []}

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold white]{task.description}[/bold white]"),
        BarColumn(bar_width=40, complete_style="green", finished_style="green"),
        TextColumn("[cyan]{task.completed}/{task.total}[/cyan]"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Cloning repositories", total=len(repos))

        for repo in repos:
            name = repo["name"]
            visibility = "🔒 private" if repo.get("private") else "🌐 public"
            progress.update(task, description=f"Cloning [bold]{name}[/bold] ({visibility})")

            repo_path = os.path.join(backup_dir, name)
            if os.path.exists(repo_path):
                results["skipped"].append(name)
                progress.advance(task)
                continue

            clone_url = repo["clone_url"].replace(
                "https://", f"https://{username}:{token}@"
            )

            proc = subprocess.run(
                ["git", "clone", "--quiet", clone_url, repo_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            if proc.returncode == 0:
                results["cloned"].append(name)
            else:
                results["failed"].append(name)

            progress.advance(task)

    return results


def print_summary(results: dict, backup_dir: str):
    table = Table(title="Backup Summary", box=box.ROUNDED, border_style="cyan")
    table.add_column("Status", style="bold")
    table.add_column("Count", justify="right")
    table.add_column("Repositories")

    def fmt(names, limit=6):
        if not names:
            return "[dim]—[/dim]"
        shown = ", ".join(names[:limit])
        if len(names) > limit:
            shown += f", [dim]+{len(names) - limit} more[/dim]"
        return shown

    table.add_row("[green]✔ Cloned[/green]", str(len(results["cloned"])), fmt(results["cloned"]))
    table.add_row("[yellow]↷ Skipped (existing)[/yellow]", str(len(results["skipped"])), fmt(results["skipped"]))
    table.add_row("[red]✘ Failed[/red]", str(len(results["failed"])), fmt(results["failed"]))

    console.print()
    console.print(table)
    console.print()

    total_ok = len(results["cloned"]) + len(results["skipped"])
    total = total_ok + len(results["failed"])

    if results["failed"]:
        console.print(
            Panel(
                f"[bold]{total_ok}/{total}[/bold] repositories backed up successfully.\n"
                f"[red]{len(results['failed'])} failed — check network/token permissions.[/red]",
                title="[bold]Done[/bold]",
                border_style="yellow",
            )
        )
    else:
        console.print(
            Panel(
                f"[bold green]All {total} repositories backed up successfully![/bold green]\n"
                f"Saved to: [cyan]{os.path.abspath(backup_dir)}[/cyan]",
                title="[bold]🎉 Complete[/bold]",
                border_style="green",
            )
        )


def main():
    console.clear()
    username, token = get_credentials()

    backup_dir = f"./{username}_backup"

    console.print()
    repos = fetch_all_repos(username, token)

    if not repos:
        console.print("[yellow]No repositories found for this account.[/yellow]")
        sys.exit(0)

    console.print(
        Panel.fit(
            f"Found [bold cyan]{len(repos)}[/bold cyan] repositories.\n"
            f"Backup target: [cyan]{os.path.abspath(backup_dir)}[/cyan]",
            border_style="cyan",
        )
    )
    console.print()

    results = clone_repos(username, token, repos, backup_dir)
    print_summary(results, backup_dir)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red]Interrupted by user.[/bold red]")
        sys.exit(1)
