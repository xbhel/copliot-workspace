#!/usr/bin/env bash
# Load variables from a .env file into the current shell session.
# Usage: source scripts/session_env.sh [path/to/.env]
# Default .env location: <script_dir>/../.env

__load_env() {
  local env_file="$1"

  if [[ ! -f "$env_file" ]]; then
    printf '%s\n' "env file not found: $env_file" >&2
    return 1
  fi

  local raw_line line name value
  while IFS= read -r raw_line; do
    line="$(printf '%s' "$raw_line" | sed -E 's/^[[:space:]]+|[[:space:]]+$//g')"

    if [[ -z "$line" || "$line" == \#* || "$line" != *=* ]]; then
      continue
    fi

    name="${line%%=*}"
    value="${line#*=}"

    name="$(printf '%s' "$name" | sed -E 's/^[[:space:]]+|[[:space:]]+$//g')"
    value="$(printf '%s' "$value" | sed -E 's/^[[:space:]]+|[[:space:]]+$//g')"

    if [[ ${#value} -ge 2 ]]; then
      if [[ "$value" == \"*\" && "$value" == *\" ]]; then
        value="${value:1:${#value}-2}"
      elif [[ "$value" == \'*\' && "$value" == *\' ]]; then
        value="${value:1:${#value}-2}"
      fi
    fi

    if [[ -n "$name" ]]; then
      export "$name=$value"
    fi
  done < "$env_file"
}

__env_script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
__load_env "${1:-${__env_script_dir}/../.env}"
__env_load_rc=$?
unset -f __load_env
unset __env_script_dir
return $__env_load_rc 2>/dev/null
# shellcheck disable=SC2317
exit "$__env_load_rc"