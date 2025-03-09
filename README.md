# Looker Column Lineage POC

Iterate through each field in each explore in each model. Generate a sql statement that will return just that field. Walk the lineage of that field to find the database columns that are used to generate it. This approach is for a proof of concept; see [Better approach](#better-approaches-for-tools-like-dataplex) for ideas for a better approachw.

## Usage

```
uv run --env-file .env src/main.py
```

The output currently is a txt list (see ends.example.txt) of fields explores and columns from table

## TODO

TODO - map sqlglot dialects to looker dialects?
TODO - how to handle filters and parameters
TODO - how to handle PDTS? Can looker generate sql without PDTS?
TODO - how to handle SELECT \*
TODO - ensure FQTN e.g. order_items in sql_table_name, but its FQTN IS `looker-private-demo.ecomm.order_items?
TODO - ensure FQCN e.g. order_items.sale_price, but its FQCN IS `looker-private-demo.ecomm.order_items.sale_price?
TODO - how are joins represented in the graph? And their join keys?
TODO - how are intermediate fields represented in the graph? For example, if I select one lookml field, but Looker selects two (this can happen with drill fields or links)
TODO - how would we parse custom fields to get their lineage?

## Better approaches for tools like dataplex

Dataplex <> Looker already has dashboard asset syncs; we could iterate through each tile (look or query) and get all the explore and field in it. Then get the sql for the tile as is on the dashboard, and walk the lineage of each field. We would create a set of all fields already parsed to not duplicate parsing.
