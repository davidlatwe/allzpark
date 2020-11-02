# API wrapper for Rez

from rez.resolved_context import ResolvedContext as env
from rez.packages_ import iter_packages as find
from rez.package_copy import copy_package
from rez.package_filter import Rule, PackageFilterList
from rez.package_repository import package_repository_manager
from rez.packages_ import Package
from rez.suite import Suite
from rez.utils.formatting import PackageRequest
from rez.config import config
from rez.util import which
from rez import __version__ as version
from rez.exceptions import (
    PackageFamilyNotFoundError,
    RexUndefinedVariableError,
    ResolvedContextError,
    RexError,
    PackageCommandError,
    PackageRequestError,
    PackageNotFoundError,
    RezError,
    SuiteError,
)
from rez.utils.graph_utils import save_graph


def clear_caches():
    for path in config.packages_path:
        repo = package_repository_manager.get_repository(path)
        repo.clear_caches()


def find_one(name, range_=None, paths=None):
    return next(find(name, range_, paths))


def find_latest(name, range_=None, paths=None):
    it = find(name, range_)
    it = sorted(it, key=lambda pkg: pkg.version)

    try:
        return list(it)[-1]
    except IndexError:
        raise PackageNotFoundError(
            "package family not found: %s" % name
        )


def is_from_suite(package):
    return package.context and package.context.suite_context_name


def uni_request_key(package, tool_entry=None):
    app_request = "%s==%s" % (package.name, package.version)
    if tool_entry:
        prefix = "%s::%s::" % (
            tool_entry["tool_alias"], tool_entry["context_name"])
        app_request = prefix + app_request

    return app_request


class RezApp(object):

    def __init__(self, package, app_request):
        in_suite = is_from_suite(package)
        if in_suite:
            tool_alias, _ = app_request.split("::", 1)
            tools = [tool_alias]
        else:
            tools = getattr(package, "tools", None) or [package.name]

        self._package = package
        self._tools = tools
        self._in_suite = in_suite
        self._uni_request_key = app_request

    def __repr__(self):
        return "RezApp(%s)" % self._uni_request_key

    def package(self):
        return self._package

    def tools(self):
        return self._tools

    def is_suite_tool(self):
        return self._in_suite

    def app_request(self):
        return self._uni_request_key


try:
    from rez import project
except ImportError:
    # nerdvegas/rez
    project = "rez"


__all__ = [
    "env",
    "find",
    "find_one",
    "find_latest",
    "uni_request_key",
    "config",
    "version",
    "project",
    "copy_package",
    "package_repository_manager",

    # Classes
    "Package",
    "PackageRequest",
    "Suite",
    "RezApp",

    # Exceptions
    "PackageFamilyNotFoundError",
    "ResolvedContextError",
    "RexUndefinedVariableError",
    "RexError",
    "PackageCommandError",
    "PackageNotFoundError",
    "PackageRequestError",
    "RezError",
    "SuiteError",

    # Filters
    "Rule",
    "PackageFilterList",

    # Extras
    "which",
    "save_graph",
    "clear_caches",
]
