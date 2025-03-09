from typing import List, Sequence

import looker_sdk
import structlog
from looker_sdk.sdk.api40.models import (
    LookmlModelExplore,
    LookmlModelExploreField,
    WriteQuery,
)

from sql_lineage import walk_for_columns

log = structlog.get_logger()

sdk = looker_sdk.init40()


class LookerFQCN:
    def __init__(
        self,
        *,
        table: str,
        column: str,
        field: LookmlModelExploreField,
        explore: LookmlModelExplore,
    ):
        self.table = table
        self.column = column
        self.field = field
        self.explore = explore

    def __str__(self):
        return " ".join(
            [
                "Explore:",
                self.explore.id,
                "-- Field:",
                self.field.name,
                "-- Column:",
                self.column,
            ]
        )


def main():
    # get models
    models = sdk.all_lookml_models(fields="id,name,explores")

    ends: List[LookerFQCN] = []
    # get explore fields
    for model in models:
        log.info("model", name=model.name)
        for model_explore in model.explores:
            log.info("explore", name=model_explore.name)
            # get explore fields
            explore = sdk.lookml_model_explore(model.name, model_explore.name)
            for field_type in explore.fields:
                if field_type not in ["dimensions", "measures"]:
                    continue
                log.info("field_type", name=field_type)
                fields: Sequence[LookmlModelExploreField] = getattr(
                    explore.fields, field_type, []
                )
                for field in fields:
                    log.info("field", name=field.name)

                    # generate sql for each field
                    try:
                        sql = sdk.run_inline_query(
                            result_format="sql",
                            body=WriteQuery(
                                model=model.name,
                                view=model_explore.name,
                                fields=[field.name],
                                limit=1,
                            ),
                            generate_drill_links=True,
                            rebuild_pdts=False,
                        )
                        walked = walk_for_columns(sql, field.name)
                        ends.extend(
                            [
                                LookerFQCN(
                                    table=x.table,
                                    column=x.column,
                                    field=field,
                                    explore=explore,
                                )
                                for x in walked
                            ]
                        )
                    except Exception as e:
                        log.error(
                            "error",
                            error=str(e),
                            sql=sql,
                            field=field.name,
                            explore=explore.name,
                        )

    with open("ends.txt", "w") as f:
        for end in ends:
            f.write(f"{end}\n")


if __name__ == "__main__":
    main()
