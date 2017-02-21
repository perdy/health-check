# -*- coding: utf-8 -*-
"""
Built-in check providers.
"""
import datetime

from git import Repo
from git.exc import InvalidGitRepositoryError

from status.settings import settings


def code(*args, **kwargs):
    """
    Code stats, such as current branch, debug mode, last commit, etc.

    :return: Source code stats.
    """
    stats = {'debug': settings.debug}
    try:
        scm_stats = {'scm': 'git'}
        repo = Repo(settings.base_dir)

        # Branch info
        branch = repo.active_branch
        scm_stats['branch'] = {
            'local': branch.name,
        }
        try:
            # Try to get remote branch name
            scm_stats['branch']['remote'] = branch.tracking_branch().name,
        except:
            scm_stats['branch']['remote'] = 'unknown'

        # Last commit info
        commit = repo.commit(branch)
        scm_stats['commit'] = {
            'id': commit.hexsha,
            'summary': commit.summary,
            'author': commit.author.name,
            'date': datetime.datetime.fromtimestamp(commit.authored_date)
        }

        # Get tag info
        tag = None
        tags = repo.tags
        tags.reverse()
        for t in (t for t in tags if tag is None):
            if t.commit == commit:
                tag = t
        if tag:
            scm_stats['tag'] = tag.name
    except InvalidGitRepositoryError:
        scm_stats = {}

    stats.update(scm_stats)

    return stats
