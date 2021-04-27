#!/usr/bin/env python3
"""service and task objects"""
import logging
import yaml
from .base import BaseFileData
from .tasks import TaskManager


LOG = logging.getLogger(__name__)


class Service(BaseFileData):
    """service representation"""

    def __init__(self, definition):
        self._data = None
        self._tasks = None
        self._hosts = []
        self._task_mgr = TaskManager.instance()
        super().__init__(definition)

    @property
    def hosts(self) -> list:
        return self._hosts

    def add_host(self, host) -> list:
        self._hosts.append(host)
        return self.hosts

    def remove_host(self, host) -> list:
        self._hosts.remove(host)
        return self.hosts

    @property
    def type(self) -> str:
        return self._data.get("type", "service")

    @property
    def version(self) -> str:
        return self._data.get("version")

    @property
    def provides(self):
        return self.name

    @property
    def requires(self) -> list:
        return self._data.get("requires", [])

    @property
    def tasks(self) -> list:
        return self._data.get("tasks", [])

    def build_tasks(self, task_type_override=None):
        tasks = []
        for _task in self.tasks:
            if task_type_override:
                task_type = task_type_override
            else:
                task_type = self._task_mgr.get_driver(_task.get("driver", "service"))
            tasks.append(task_type(self.name, _task, self.hosts))
        return tasks

    def save(self, location) -> None:
        with open(location, "w") as fout:
            yaml.dump(self.data, fout)