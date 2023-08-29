import cProfile
import json
import logging
import tempfile
from pstats import Stats

from django.conf import settings
from django.shortcuts import render
from django.utils.safestring import SafeString
from snakeviz import stats

from django_snakeviz_profiling.db_profile import DbProfile

log = logging.getLogger("django_snakeviz_profiling")


PROFILING_PARAMETER = "SNAKEVIZ_PROFILING"
PROFILING_MAGIC_WORD = "PLEASE_PROFILE_REQUESTS"
HTTP_OK_STATUS_CODE = 200


def SnakevizProfilingMiddleware(get_response):  # noqa: N802
    # Immediately shortcut if we are not configured to process requests
    if getattr(settings, PROFILING_PARAMETER, "") != PROFILING_MAGIC_WORD:
        return get_response

    log.info("SnakevizProfilingMiddleware is activated")

    def snakeviz_profiling_middleware(request):
        # If we do not use the magic word, do nothing
        if request.GET.get(PROFILING_PARAMETER, "") != PROFILING_MAGIC_WORD:
            return get_response(request)

        log.info("Starting SnakevizProfilingMiddleware profiling (this will slow down requests!)")

        with DbProfile.start_logging_queries() as db_profile:
            with tempfile.NamedTemporaryFile() as prof_dump:
                profile = cProfile.Profile()
                profile.enable()
                try:
                    resp = get_response(request)
                finally:
                    profile.disable()

                profile.dump_stats(prof_dump.name)

                if resp.status_code == HTTP_OK_STATUS_CODE:
                    log.info(
                        "Got %d status code and %d byte response in profiled request",
                        resp.status_code,
                        len(resp.content),
                    )
                else:
                    log.warning(
                        "Got %d status code and %d byte response in profiled request",
                        resp.status_code,
                        len(resp.content),
                    )

                prof_data = Stats(prof_dump.name)
                table_rows = stats.table_rows(prof_data)
                callees = stats.json_stats(prof_data)

            db_queries = db_profile.collate_queries()

        context = {
            "profile_name": request.path,
            "table_rows": table_rows,
            "callees": SafeString(json.dumps(callees)),
            "db_queries": db_queries,
        }

        resp = render(
            request,
            "django_snakeviz_profiling/viz.html",
            context,
        )

        log.info("SnakevizProfilingMiddleware profiling done.")
        return resp

    return snakeviz_profiling_middleware
