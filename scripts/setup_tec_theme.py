from __future__ import annotations

import subprocess
import sys
from pathlib import Path


THEME_REPOSITORY = "https://github.com/EIEM-TEC/beamerTec.git"
SUBMODULE_PATH = "beamerTec"


def run_git(*args: str, cwd: Path) -> None:
    command = ["git", *args]
    print(f"> {' '.join(command)}")

    try:
        subprocess.run(
            command,
            cwd=cwd,
            check=True,
        )
    except FileNotFoundError:
        sys.exit("Error: Git no está instalado o no está disponible en PATH.")
    except subprocess.CalledProcessError as error:
        sys.exit(f"Error ejecutando Git. Código: {error.returncode}")


def is_registered_submodule(project: Path) -> bool:
    result = subprocess.run(
        [
            "git",
            "config",
            "--file",
            ".gitmodules",
            "--get-regexp",
            r"^submodule\..*\.path$",
        ],
        cwd=project,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        return False

    registered_paths = {
        line.split(maxsplit=1)[1].strip()
        for line in result.stdout.splitlines()
        if len(line.split(maxsplit=1)) == 2
    }

    return SUBMODULE_PATH in registered_paths


def main() -> None:
    script_path = Path(__file__).resolve()
    project = script_path.parent.parent
    submodule = project / SUBMODULE_PATH
    script_relative_path = script_path.relative_to(project)

    if not (project / ".git").exists():
        sys.exit(
            "Error: la carpeta padre de 'scripts' debe ser la raíz "
            "del repositorio Git."
        )

    if is_registered_submodule(project):
        print(f"El submódulo '{SUBMODULE_PATH}' ya está registrado.")
    elif submodule.exists():
        sys.exit(
            f"Error: la carpeta '{SUBMODULE_PATH}' ya existe, "
            "pero no está registrada como submódulo."
        )
    else:
        run_git(
            "submodule",
            "add",
            THEME_REPOSITORY,
            SUBMODULE_PATH,
            cwd=project,
        )

    run_git(
        "submodule",
        "update",
        "--init",
        "--recursive",
        cwd=project,
    )

    run_git(
        "add",
        ".gitmodules",
        SUBMODULE_PATH,
        script_relative_path.as_posix(),
        cwd=project,
    )

    print("\nBeamer TEC está listo y los cambios quedaron en staging.")


if __name__ == "__main__":
    main()