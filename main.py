from github_connector.client import GitHubClient
from configs.logging import setup_logging

setup_logging()

def main():
    
    get_repo = GitHubClient().get_repo("Kenn-stack", "PlayBoy")
    
    # get_repo = GitHubClient().get_repo("Kenn-stack", "PlayPort")

    # get_latest = GitHubClient().get_latest_release("Kenn-stack", "PlayPort")
    
    return {"Repo": get_repo}
    
    
    
if __name__ == "__main__":
    print(main())
    