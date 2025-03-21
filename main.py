import requests
import time
import random
import sys

from concurrent.futures import ThreadPoolExecutor, as_completed

from colorama import init

from stem import Signal
from stem.control import Controller


from rich.console import Console
from rich.panel import Panel

init()

DELAY_BETWEEN_REQUESTS = 0.0001
OUTPUT_FILE = "ownerless_groups.txt"
TOR_SOCKS_PORT = 9050
TOR_CONTROL_PORT = 9051
TOR_PASSWORD = 'password here'

console = Console()

def renew_tor_identity():
    try:
        with Controller.from_port(port=TOR_CONTROL_PORT) as controller:
            controller.authenticate(password=TOR_PASSWORD)
            controller.signal(Signal.NEWNYM)
            return True
    except Exception as e:
        console.print(f"[bold red]Failed to change Tor identity: {e}[/bold red]")
        return False


def get_tor_session():
    session = requests.Session()
    session.proxies = {
        'http': f'socks5://127.0.0.1:{TOR_SOCKS_PORT}',
        'https': f'socks5://127.0.0.1:{TOR_SOCKS_PORT}'
    }
    return session


def get_group_info(session, group_id):
    url = f"https://groups.roblox.com/v1/groups/{group_id}"
    try:
        response = session.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.RequestException as e:
        console.print(f"[bold red]Request failed for group {group_id}: {e}[/bold red]")
        return None


def is_group_ownerless(group_info):
    return group_info.get("owner") is None


def is_group_joinable(group_info):
    return group_info.get("publicEntryAllowed", False)


def get_group_url(group_id):
    return f"https://www.roblox.com/groups/{group_id}"


def save_group_to_file(group_url):
    with open(OUTPUT_FILE, "a") as file:
        file.write(f"Group: {group_url}\n")


def process_group(session, group_id, thread_id):
    group_info = get_group_info(session, group_id)

    if group_info:
        if is_group_ownerless(group_info):
            if is_group_joinable(group_info):
                group_url = get_group_url(group_id)
                console.print(f"[bold green]Thread {thread_id} - Group {group_id} is ownerless and open to join![/bold green] [Link: {group_url}]")
                save_group_to_file(group_url)
            else:
                console.print(f"[bold yellow]Thread {thread_id} - Group {group_id} is ownerless but closed to joining.[/bold yellow]")
        else:
            console.print(f"[bold red]Thread {thread_id} - Group {group_id} has an owner.[/bold red]")
    else:
        console.print(f"[bold red]Thread {thread_id} - Group {group_id} does not exist or an error occurred.[/bold red]")


def find_ownerless_groups():
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = []
        for thread_id in range(100):  # How many threads you want checking
            session = get_tor_session()
            futures.append(executor.submit(run_group_checking, session, thread_id))

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                console.print(f"[bold red]Error in thread: {e}[/bold red]")
                executor.shutdown(wait=False)
                sys.exit("Tor service has stopped. Exiting threads.")


def run_group_checking(session, thread_id):
    request_count = 0
    while True:
        if not renew_tor_identity():
            console.print(f"[bold red]Thread {thread_id} - Tor service stopped or unavailable. Exiting thread.[/bold red]")
            break

        session = get_tor_session()

        group_id = random.randint(1, 9999999)
        process_group(session, group_id, thread_id)

        request_count += 1
        if request_count >= 5:
            console.print(f"[bold blue]Thread {thread_id} - Changing Tor IP...[/bold blue]")
            session = get_tor_session()
            request_count = 0

        time.sleep(DELAY_BETWEEN_REQUESTS)


if __name__ == "__main__":
    console.print(Panel("[bold cyan]Starting the Group Checker with Tor...[/bold cyan]", title="INFO"))
    find_ownerless_groups()
