from __future__ import annotations

import asyncio
import os
from typing import Any

from httpx import AsyncClient


class PlatformProvider:
    """Base class for platform providers that can create pull requests."""

    def __init__(self, context: dict[str, str], httpx_client: AsyncClient) -> None:
        self._context = context
        self._httpx_client = httpx_client

    async def is_supported(self) -> bool:
        """Determine if this provider can handle the given context."""
        raise NotImplementedError

    async def create_pull_request(self) -> dict[str, Any]:
        """Create a pull request using the context information."""
        raise NotImplementedError


async def run_cmd(args: list[str], cwd: str | None = None, input_bytes: bytes | None = None) -> str:
    """Run a command in a subprocess and return its output as a string.

    Raises RuntimeError if the command fails (non-zero exit code).
    """
    proc = await asyncio.create_subprocess_exec(
        *args,
        cwd=cwd,
        stdin=asyncio.subprocess.PIPE if input_bytes else None,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate(input=input_bytes)
    stdout_str = stdout.decode().strip()
    stderr_str = stderr.decode().strip()
    if proc.returncode != 0:
        raise RuntimeError(f"Command {' '.join(args)} failed with error: {stderr_str}")
    return stdout_str


async def get_credentials(remote_url: str, cwd: str | None = None) -> tuple[str, str]:
    """Get the username and token for the given remote URL using git credential helper.

    Raises RuntimeError if credentials cannot be found in either place.
    """
    user, password = os.getenv("GIT_USER"), os.getenv("GIT_TOKEN")
    if not user or not password:
        creds_input = f"url={remote_url}\n\n".encode()
        creds_output = await run_cmd(
            ["git", "credential", "fill"], cwd=cwd, input_bytes=creds_input
        )
        creds = dict(line.split("=", 1) for line in creds_output.splitlines() if "=" in line)
        user = creds.get("username", "")
        password = creds.get("password", "")
    if not user or not password:
        raise RuntimeError(
            "Git credentials not found in environment variables or git credential helper"
        )
    return user, password


async def build_git_context(cwd: str | None = None) -> dict[str, str]:
    """Build a context dictionary with git information for the current repository."""
    remote_url, branch = await asyncio.gather(
        *[
            run_cmd(["git", "rev-parse", "--abrev-ref", "HEAD"], cwd=cwd),
            run_cmd(["git", "remote", "get-url", "origin"], cwd=cwd),
        ]
    )
    user, token = await get_credentials(remote_url, cwd=cwd)
    return {"remote_url": remote_url, "branch": branch, "user": user, "token": token}


async def pull_request(llm_context: dict[str, str], cwd: str | None = None) -> dict[str, Any]:
    """Create a pull request using the given LLM context and git repository.
    Args:
        llm_context: A dictionary containing the following keys:
            - title: The title of the pull request.
            - description: The description of the pull request.
            - source_branch: The source branch for the pull request.
            - target_branch: The target branch for the pull request.
            - reviewers: A list of reviewers for the pull request (optional).
            - assignees: A list of assignees for the pull request (optional).
            - workitems: A list of work items to link to the pull request (optional).
            - is_draft: Whether the pull request should be created as a draft (optional).
            - is_auto_complete: Whether the pull request should be set to auto-complete (optional).
        cwd: The working directory of the git repository (optional).
    Returns:
        A dictionary containing information about the created pull request.
    Raises:
        RuntimeError: If no supported platform provider is found for the given repository.
    """
    git_context = await build_git_context(cwd=cwd)
    context = {**git_context, **llm_context}

    provider_classes: list[type[PlatformProvider]] = []

    async with AsyncClient() as httpx_client:
        for provider_class in provider_classes:
            provider = provider_class(context, httpx_client)

            if await provider.is_supported():
                return await provider.create_pull_request()

    raise RuntimeError(
        f"No supported platform provider found for the given repository: {context['remote_url']}"
    )
