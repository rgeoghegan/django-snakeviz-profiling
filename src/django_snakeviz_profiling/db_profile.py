import contextlib
import logging
from collections import defaultdict

from django.db import connections

log = logging.getLogger("django_snakeviz_profiling")


class DbProfile:
    def __init__(self, connection_names):
        self.connection_names = connection_names

    def collate_queries(self):
        queries = []

        for conn in connections.all():
            if conn.alias not in self.connection_names:
                continue

            grouped_sql = defaultdict(list)
            for query in conn.queries:
                grouped_sql[query["sql"]].append(float(query["time"]))

            for query, times in grouped_sql.items():
                times.sort()
                total = sum(times)

                queries.append(
                    [
                        query,
                        conn.alias,
                        len(times),
                        total,
                        total / len(times),
                        times[len(times) // 2],
                    ]
                )

        return queries

    @classmethod
    @contextlib.contextmanager
    def start_logging_queries(cls, connection_names=None):
        """
        Mark connections as requiring logging, and unmark at the end of the
        request.
        """
        if connection_names is None:
            connection_names = ["default"]
        prev_marks = {}
        for conn in connections.all():
            if conn.alias in connection_names:
                # Should be false, but in case it is true for a connection
                prev_marks[conn.alias] = conn.force_debug_cursor
                conn.force_debug_cursor = True

        log.info("Now logging all queries for connections %r", list(prev_marks.keys()))
        yield DbProfile(list(prev_marks.keys()))

        # Re-wind all the force_debug_cursor setting
        for conn in connections.all():
            if conn.alias in connection_names:
                conn.force_debug_cursor = prev_marks[conn.alias]
        log.info("Have reset logging on connections %r", list(prev_marks.keys()))
