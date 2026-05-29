import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).parent


def gitignore_has_env(gitignore_path: Path) -> bool:
    """.gitignore에 .env 항목이 있는지 확인합니다."""
    if not gitignore_path.exists():
        return False
    lines = [line.strip() for line in gitignore_path.read_text(encoding="utf-8").splitlines()]
    return ".env" in lines


def env_in_staged() -> bool:
    """git diff --cached --name-only 결과에 .env가 포함되어 있는지 확인합니다."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        capture_output=True,
        text=True,
        cwd=BASE_DIR,
    )
    staged = [line.strip() for line in result.stdout.splitlines()]
    return any(name == ".env" or name.endswith("/.env") for name in staged)


def main() -> None:
    ignored = gitignore_has_env(BASE_DIR / ".gitignore")
    staged = env_in_staged()

    print(f"[검사] .gitignore에 .env 포함: {'예' if ignored else '아니오'}")
    print(f"[검사] staged 목록에 .env 포함: {'예' if staged else '아니오'}")

    if ignored and not staged:
        print("push 가능")
    else:
        print("push 중단")


if __name__ == "__main__":
    main()
