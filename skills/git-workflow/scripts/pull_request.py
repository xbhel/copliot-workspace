from __future__ import annotations

import asyncio
import logging
import os
import re
from dataclasses import dataclass
from functools import cached_property
from typing import Any
from urllib.parse import quote_plus

import httpx

logger = logging.getLogger(__name__)
logger.setLevel(os.getenv("LOG_LEVEL", logging.DEBUG))


@dataclass
class PullRequestResult:
    id: str
    url: str
    repo: str
    repo_id: str
    owner: str
    title: str
    description: str
    source: str
    target: str
    is_draft: bool
    is_auto_complete: bool
    platform: str
    project: str | None = None


class PlatformProvider:
    """Base class for platform providers that can create pull requests."""

    def __init__(self, context: dict[str, Any], httpx_client: httpx.AsyncClient) -> None:
        self._context = context
        self._httpx_client = httpx_client

    @classmethod
    def ssh_to_https(cls, url: str) -> str | None:  # noqa: ARG003
        """Convert a provider-specific SSH URL to HTTPS for credential lookup.

        Returns the HTTPS URL if recognized, otherwise ``None``.
        """
        return None

    async def is_supported(self) -> bool:
        """Determine if this provider can handle the given context."""
        raise NotImplementedError

    async def create_pull_request(self) -> PullRequestResult:
        """Create a pull request using the context information."""
        raise NotImplementedError


class GithubProvider(PlatformProvider):
    """GitHub provider implementation."""

    _PATTERNS = [
        re.compile(r"^git@github\.com:(?P<owner>[^/]+)/(?P<repo>[^/.]+)(\.git)?$"),
        re.compile(r"^https://github\.com/(?P<owner>[^/]+)/(?P<repo>[^/.]+)(\.git)?$"),
    ]

    @classmethod
    def ssh_to_https(cls, url: str) -> str | None:
        info = regex_groupdict(cls._PATTERNS, url)
        if info and not url.startswith("https://"):
            return f"https://github.com/{info['owner']}/{info['repo']}"
        return None

    @cached_property
    def _repo_info(self) -> dict[str, str]:
        """Parse owner and repo from the remote URL. Cached after first call."""
        return regex_groupdict(self._PATTERNS, self._context["remote_url"])

    @property
    def _auth(self) -> httpx.BasicAuth:
        return httpx.BasicAuth("", self._context["access_token"])

    @property
    def _api_base(self) -> str:
        return f"https://api.github.com/repos/{self._repo_info['owner']}/{self._repo_info['repo']}"

    @property
    def _headers(self) -> dict[str, str]:
        return {"Content-Type": "application/json", "Accept": "application/vnd.github+json"}

    async def is_supported(self) -> bool:
        return bool(self._repo_info)

    def _build_create_payload(self) -> dict[str, Any]:
        """Build the GitHub PR creation payload from context."""
        description = self._context.get("description", "")
        workitems = self._context.get("workitems", [])
        if workitems:
            refs = "\n".join(f"Closes #{item}" for item in workitems)
            description = f"{description}\n\n{refs}"
        return {
            "title": self._context["title"],
            "body": description,
            "head": self._context["source"],
            "base": self._context["target"],
            "draft": self._context.get("is_draft", False),
        }

    def _parse_response(self, response_data: dict[str, Any]) -> PullRequestResult:
        """Parse the GitHub API JSON response into a PullRequestResult.

        Only extracts data from the API response — does not mix in context fields.
        """
        return PullRequestResult(
            id=str(response_data["number"]),
            url=response_data["html_url"],
            repo=response_data["base"]["repo"]["name"],
            repo_id=str(response_data["base"]["repo"]["id"]),
            owner=response_data["base"]["repo"]["owner"]["login"],
            title=response_data["title"],
            description=response_data.get("body", ""),
            source=response_data["head"]["ref"],
            target=response_data["base"]["ref"],
            is_draft=response_data.get("draft", False),
            is_auto_complete=False,
            platform="github",
        )

    def _build_update_requests(self, pr_number: str) -> list[dict[str, Any]]:
        """Build post-create requests for reviewers and assignees."""
        requests: list[dict[str, Any]] = []
        reviewers = self._context.get("reviewers", [])
        assignees = self._context.get("assignees", [])
        if reviewers:
            requests.append(
                {
                    "method": "POST",
                    "url": f"{self._api_base}/pulls/{pr_number}/requested_reviewers",
                    "headers": self._headers,
                    "json": {"reviewers": reviewers},
                    "auth": self._auth,
                }
            )
        if assignees:
            requests.append(
                {
                    "method": "POST",
                    "url": f"{self._api_base}/issues/{pr_number}/assignees",
                    "headers": self._headers,
                    "json": {"assignees": assignees},
                    "auth": self._auth,
                }
            )
        return requests

    async def create_pull_request(self) -> PullRequestResult:
        payload = self._build_create_payload()
        try:
            response = await self._httpx_client.post(
                f"{self._api_base}/pulls",
                headers=self._headers,
                auth=self._auth,
                json=payload,
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            logger.exception(
                "GitHub PR creation failed [%d] for %s/%s: %s",
                exc.response.status_code,
                self._repo_info.get("owner"),
                self._repo_info.get("repo"),
                exc.response.text,
            )
            raise
        result = self._parse_response(response.json())

        update_requests = self._build_update_requests(result.id)
        for coro in asyncio.as_completed(
            [self._httpx_client.request(**req) for req in update_requests]
        ):
            try:
                resp = await coro
                resp.raise_for_status()
            except httpx.HTTPStatusError as exc:
                logger.warning(
                    "GitHub post-create request failed [%d] %s: %s",
                    exc.response.status_code,
                    exc.request.url,
                    exc.response.text,
                )

        return result


class AzureDevOpsProvider(PlatformProvider):
    """Azure DevOps provider implementation."""

    _PATTERNS = [
        re.compile(
            r"^https://dev\.azure\.com/(?P<owner>[^/]+)/(?P<project>[^/]+)/_git/(?P<repo>[^/.]+)$"
        ),
        re.compile(
            r"^https://(?P<owner>[^.]+)\.visualstudio\.com/"
            r"DefaultCollection/(?P<project>[^/]+)/_git/(?P<repo>[^/.]+)$"
        ),
        re.compile(
            r"^git@ssh\.dev\.azure\.com:v3/(?P<owner>[^/]+)/(?P<project>[^/]+)/(?P<repo>[^/.]+)$"
        ),
        re.compile(
            r"^(?P<org>[^@]+)@vs-ssh\.visualstudio\.com:"
            r"v3/(?P<owner>[^/]+)/(?P<project>[^/]+)/(?P<repo>[^/.]+)$"
        ),
    ]

    @classmethod
    def ssh_to_https(cls, url: str) -> str | None:
        info = regex_groupdict(cls._PATTERNS, url)
        if info and not url.startswith("https://"):
            return f"https://dev.azure.com/{info['owner']}/{info['project']}/_git/{info['repo']}"
        return None

    @cached_property
    def _repo_info(self) -> dict[str, str]:
        return regex_groupdict(self._PATTERNS, self._context["remote_url"])

    @property
    def _auth(self) -> httpx.BasicAuth:
        return httpx.BasicAuth("", self._context["access_token"])

    @property
    def _api_base(self) -> str:
        info = self._repo_info
        return (
            f"https://dev.azure.com/{info['owner']}/{info['project']}"
            f"/_apis/git/repositories/{info['repo']}"
        )

    @property
    def _identity_api_base(self) -> str:
        return f"https://vssps.dev.azure.com/{self._repo_info['owner']}/_apis/identities"

    @property
    def _headers(self) -> dict[str, str]:
        return {"Content-Type": "application/json"}

    async def is_supported(self) -> bool:
        return bool(self._repo_info)

    async def _resolve_reviewer_ids(self, reviewers: list[str]) -> dict[str, str]:
        """Resolve Azure DevOps reviewers to identity GUIDs for PR APIs."""
        if not reviewers:
            return {}

        async def lookup(reviewer: str) -> tuple[str, httpx.Response]:
            response = await self._httpx_client.get(
                self._identity_api_base,
                headers=self._headers,
                # Use a PAT for the Identities API, as it may not accept Git API credentials.
                auth=httpx.BasicAuth("", self._context["access_token"]),
                params={
                    "searchFilter": "General",
                    "filterValue": reviewer,
                    "queryMembership": "None",
                    "api-version": "7.1",
                },
            )
            return reviewer, response

        reviewer_map: dict[str, str] = {}
        requests = [lookup(reviewer) for reviewer in reviewers]
        for request in asyncio.as_completed(requests):
            try:
                reviewer, response = await request
                response.raise_for_status()
                identities = response.json().get("value", [])
                if identities:
                    reviewer_map[reviewer] = identities[0]["id"]
                else:
                    logger.warning("Azure DevOps reviewer '%s' not found, skipping", reviewer)
            except httpx.HTTPStatusError as exc:
                logger.warning(
                    "Azure DevOps reviewer lookup failed [%d] for '%s': %s",
                    exc.response.status_code,
                    reviewer,
                    exc.response.text,
                )

        return reviewer_map

    def _build_create_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "sourceRefName": f"refs/heads/{self._context['source']}",
            "targetRefName": f"refs/heads/{self._context['target']}",
            "title": self._context["title"],
            "description": self._context.get("description", ""),
            "isDraft": self._context.get("is_draft", False),
        }
        workitems = self._context.get("workitems", [])
        if workitems:
            payload["workItemRefs"] = [{"id": item} for item in workitems]
        return payload

    def _parse_response(self, response_data: dict[str, Any]) -> PullRequestResult:
        info = self._repo_info
        repo_data = response_data.get("repository", {})
        pr_id = str(response_data["pullRequestId"])
        web_url = (
            f"https://dev.azure.com/{info['owner']}/{info['project']}"
            f"/_git/{info['repo']}/pullrequest/{pr_id}"
        )
        return PullRequestResult(
            id=pr_id,
            url=web_url,
            repo=repo_data.get("name", info.get("repo", "")),
            repo_id=str(repo_data["id"]) if repo_data.get("id") else "",
            owner=info["owner"],
            title=response_data["title"],
            description=response_data.get("description", ""),
            source=response_data["sourceRefName"].removeprefix("refs/heads/"),
            target=response_data["targetRefName"].removeprefix("refs/heads/"),
            is_draft=response_data.get("isDraft", False),
            is_auto_complete=bool(response_data.get("autoCompleteSetBy", {}).get("id")),
            platform="azure",
            project=info.get("project"),
        )

    def _build_auto_complete_request(self, pr_id: str, creator_id: str) -> dict[str, Any]:
        return {
            "method": "PATCH",
            "url": f"{self._api_base}/pullrequests/{pr_id}?api-version=7.1",
            "headers": self._headers,
            "json": {
                "autoCompleteSetBy": {"id": creator_id},
                "completionOptions": {"mergeStrategy": "squash"},
            },
            "auth": self._auth,
        }

    async def create_pull_request(self) -> PullRequestResult:
        payload = self._build_create_payload()
        reviewers = self._context.get("reviewers", [])
        if reviewers:
            reviewer_map = await self._resolve_reviewer_ids(reviewers)
            if reviewer_map:
                payload["reviewers"] = [{"id": rid} for rid in reviewer_map.values()]
            else:
                logger.warning("PR will be created without reviewers since none could be resolved.")

        try:
            response = await self._httpx_client.post(
                f"{self._api_base}/pullrequests?api-version=7.1",
                headers=self._headers,
                auth=self._auth,
                json=payload,
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            logger.exception(
                "Azure DevOps PR creation failed [%d] for %s/%s/%s: %s",
                exc.response.status_code,
                self._repo_info.get("owner"),
                self._repo_info.get("project"),
                self._repo_info.get("repo"),
                exc.response.text,
            )
            raise
        response_data = response.json()
        result = self._parse_response(response_data)

        if self._context.get("is_auto_complete"):
            creator_id = response_data.get("createdBy", {}).get("id", "")
            if creator_id:
                try:
                    req = self._build_auto_complete_request(result.id, creator_id)
                    resp = await self._httpx_client.request(**req)
                    resp.raise_for_status()
                    result.is_auto_complete = True
                except httpx.HTTPStatusError as exc:
                    logger.warning(
                        "Azure DevOps auto-complete failed [%d] for PR #%s: %s",
                        exc.response.status_code,
                        result.id,
                        exc.response.text,
                    )
            else:
                logger.warning(
                    "Cannot set auto-complete: createdBy.id missing from PR #%s response",
                    result.id,
                )

        return result


class GitLabProvider(PlatformProvider):
    """GitLab provider implementation."""

    _PATTERNS = [
        re.compile(r"^git@gitlab\.com:(?P<owner>[^/]+)/(?P<repo>[^/.]+)(\.git)?$"),
        re.compile(r"^https://gitlab\.com/(?P<owner>[^/]+)/(?P<repo>[^/.]+)(\.git)?$"),
    ]

    @classmethod
    def ssh_to_https(cls, url: str) -> str | None:
        info = regex_groupdict(cls._PATTERNS, url)
        if info and not url.startswith("https://"):
            return f"https://gitlab.com/{info['owner']}/{info['repo']}"
        return None

    @cached_property
    def _repo_info(self) -> dict[str, str]:
        return regex_groupdict(self._PATTERNS, self._context["remote_url"])

    @property
    def _headers(self) -> dict[str, str]:
        return {"Content-Type": "application/json", "PRIVATE-TOKEN": self._context["access_token"]}

    @property
    def _project_api(self) -> str:
        info = self._repo_info
        project_path = quote_plus(f"{info['owner']}/{info['repo']}")
        return f"https://gitlab.com/api/v4/projects/{project_path}"

    async def is_supported(self) -> bool:
        return bool(self._repo_info)

    async def _resolve_user_ids(self, usernames: list[str]) -> list[int]:
        """Resolve GitLab usernames to numeric user IDs via the Users API."""
        user_ids: list[int] = []
        for username in usernames:
            try:
                resp = await self._httpx_client.get(
                    f"https://gitlab.com/api/v4/users?username={username}",
                    headers=self._headers,
                )
                resp.raise_for_status()
                users = resp.json()
                if users:
                    user_ids.append(users[0]["id"])
                else:
                    logger.warning("GitLab user '%s' not found, skipping", username)
            except httpx.HTTPStatusError as exc:
                logger.warning(
                    "GitLab user lookup failed [%d] for '%s': %s",
                    exc.response.status_code,
                    exc.response.text,
                )
        return user_ids

    def _build_create_payload(self) -> dict[str, Any]:
        title = self._context["title"]
        if self._context.get("is_draft") and not title.startswith("Draft: "):
            title = f"Draft: {title}"
        description = self._context.get("description", "")
        workitems = self._context.get("workitems", [])
        if workitems:
            refs = "\n".join(f"Closes #{item}" for item in workitems)
            description = f"{description}\n\n{refs}"
        return {
            "source": self._context["source"],
            "target": self._context["target"],
            "title": title,
            "description": description,
        }

    def _parse_response(self, response_data: dict[str, Any]) -> PullRequestResult:
        info = self._repo_info
        title = response_data.get("title", "")
        is_draft = title.startswith("Draft: ")
        return PullRequestResult(
            id=str(response_data["iid"]),
            url=response_data["web_url"],
            repo=info.get("repo", ""),
            repo_id=str(response_data["project_id"]) if response_data.get("project_id") else "",
            owner=info["owner"],
            title=title,
            description=response_data.get("description", ""),
            source=response_data["source"],
            target=response_data["target"],
            is_draft=is_draft,
            is_auto_complete=False,
            platform="gitlab",
        )

    def _build_auto_merge_request(self, mr_iid: str) -> dict[str, Any]:
        return {
            "method": "PUT",
            "url": f"{self._project_api}/merge_requests/{mr_iid}/merge",
            "headers": self._headers,
            "json": {"merge_when_pipeline_succeeds": True},
        }

    async def create_pull_request(self) -> PullRequestResult:
        payload = self._build_create_payload()

        reviewers = self._context.get("reviewers", [])
        assignees = self._context.get("assignees", [])
        if reviewers or assignees:
            reviewer_ids, assignee_ids = await asyncio.gather(
                self._resolve_user_ids(reviewers) if reviewers else asyncio.sleep(0, []),
                self._resolve_user_ids(assignees) if assignees else asyncio.sleep(0, []),
            )
            if reviewer_ids:
                payload["reviewer_ids"] = reviewer_ids
            if assignee_ids:
                payload["assignee_ids"] = assignee_ids

        try:
            response = await self._httpx_client.post(
                f"{self._project_api}/merge_requests",
                headers=self._headers,
                json=payload,
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            logger.exception(
                "GitLab MR creation failed [%d] for %s/%s: %s",
                exc.response.status_code,
                self._repo_info.get("owner"),
                self._repo_info.get("repo"),
                exc.response.text,
            )
            raise
        result = self._parse_response(response.json())

        if self._context.get("is_auto_complete"):
            try:
                req = self._build_auto_merge_request(result.id)
                resp = await self._httpx_client.request(**req)
                resp.raise_for_status()
                result.is_auto_complete = True
            except httpx.HTTPStatusError as exc:
                logger.warning(
                    "GitLab auto-merge failed [%d] for MR !%s: %s",
                    exc.response.status_code,
                    result.id,
                    exc.response.text,
                )

        return result


def regex_groupdict(patterns: list[re.Pattern[str]], text: str) -> dict[str, str]:
    """Match the given text against a list of regex patterns
    and return the first match group dict."""
    for pattern in patterns:
        match = pattern.match(text)
        if match:
            return match.groupdict()
    return {}


_PROVIDER_CLASSES: list[type[PlatformProvider]] = [
    GithubProvider,
    AzureDevOpsProvider,
    GitLabProvider,
]


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
        logger.error(
            "Command '%s' exited with code %d: %s",
            " ".join(args),
            proc.returncode,
            stderr_str,
        )
        raise RuntimeError(f"Command {' '.join(args)} failed with error: {stderr_str}")
    return stdout_str


def _ssh_url_to_https(url: str) -> str:
    """Convert an SSH remote URL to HTTPS for ``git credential fill``."""
    for provider_cls in _PROVIDER_CLASSES:
        https_url = provider_cls.ssh_to_https(url)
        if https_url is not None:
            return https_url
    return url


async def get_credentials(remote_url: str, cwd: str | None = None) -> str:
    """Get the access token for the given remote URL using git credential helper.

    Raises RuntimeError if credentials cannot be found in either place.
    """
    access_token = os.getenv("GIT_PAT")
    if not access_token:
        cred_url = _ssh_url_to_https(remote_url)
        creds_input = f"url={cred_url}\n\n".encode()
        creds_output = await run_cmd(
            ["git", "credential", "fill"], cwd=cwd, input_bytes=creds_input
        )
        creds = dict(line.split("=", 1) for line in creds_output.splitlines() if "=" in line)
        access_token = creds.get("password")
    if not access_token:
        logger.error(
            "Git credentials not found for remote '%s'"
            " — set GIT_PAT or configure a credential helper",
            remote_url,
        )
        raise RuntimeError(
            "Git credentials not found in environment variables or git credential helper"
        )
    return access_token


async def build_git_context(cwd: str | None = None) -> dict[str, str]:
    """Build a context dictionary with git information for the current repository.
    Returns:
        A dictionary containing git information for the current repository. includes:
            - remote_url: The URL of the remote repository.
            - branch: The current branch name.
            - access_token: The access token for authentication.
    Raises:
        RuntimeError: If git commands fail or credentials cannot be found.
    """
    branch, remote_url = await asyncio.gather(
        *[
            run_cmd(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=cwd),
            run_cmd(["git", "remote", "get-url", "origin"], cwd=cwd),
        ]
    )
    access_token = await get_credentials(remote_url, cwd=cwd)
    return {"remote_url": remote_url, "branch": branch, "access_token": access_token}


async def pull_request(llm_context: dict[str, Any], cwd: str | None = None) -> PullRequestResult:
    """Create a pull request using the given LLM context and git repository.
    Args:
        llm_context: A dictionary containing the following keys:
            - title: The title of the pull request.
            - description: The description of the pull request.
            - source: The source branch for the pull request.
            - target: The target branch for the pull request.
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

    async with httpx.AsyncClient() as httpx_client:
        for provider_class in _PROVIDER_CLASSES:
            provider = provider_class(context, httpx_client)

            if await provider.is_supported():
                logger.info(
                    "Using %s provider for remote URL: %s",
                    provider_class.__name__,
                    context["remote_url"],
                )
                return await provider.create_pull_request()

    logger.error("No supported platform provider for remote URL: %s", context["remote_url"])
    raise RuntimeError(
        f"No supported platform provider found for the given repository: {context['remote_url']}"
    )


def main() -> None:
    """CLI entry point to create a pull request from the command line.

    Parses arguments, builds context, and delegates to :func:`pull_request`.
    Supports GitHub, Azure DevOps, and GitLab — the platform is auto-detected
    from the git remote URL.

    Example::

        python pull_request.py \\
            --title "Add new feature" \\
            --description "This PR adds a new feature." \\
            --source feat/278052-add-auth \\
            --target dev \\
            --reviewers tom allen \\
            --workitems 1234567 \\
            --is-draft \\
            --is-auto-complete
    """
    import argparse

    parser = argparse.ArgumentParser(description="Create a pull request from the command line.")
    parser.add_argument("--title", required=True, help="PR title")
    parser.add_argument("--description", default="", help="PR description/body")
    parser.add_argument("--source", required=True, help="Source branch")
    parser.add_argument("--target", required=True, help="Target branch")
    parser.add_argument("--reviewers", help="List of reviewers", nargs="*", default=[])
    parser.add_argument("--assignees", help="List of assignees", nargs="*", default=[])
    parser.add_argument("--workitems", help="List of work items (IDs)", nargs="*", default=[])
    parser.add_argument(
        "--cwd",
        default=None,
        help="Working directory of the git repository (optional, defaults to current directory).",
    )
    parser.add_argument(
        "--is-draft", action="store_true", help="Whether to create the pull request as a draft"
    )
    parser.add_argument(
        "--is-auto-complete",
        action="store_true",
        help=("Whether to set the pull request to auto-complete/auto-merge after creation"),
    )
    args = parser.parse_args()

    llm_context = vars(args)
    logger.info("llm_context: %s", llm_context)
    result = asyncio.run(pull_request(llm_context, cwd=args.cwd))
    logger.info("Pull request created successfully: %s", result.url)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    main()
