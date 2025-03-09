from sql_lineage import walk_for_columns


def test_walk_for_columns():
    test_sql = """
    WITH abc AS (
        SELECT 
            DATE_DIFF(users_big.created_at, order_items_big.created_at, DAY) AS "ordered_since_signup",
            DATE_DIFF(users_big.created_at2, order_items_big.created_at2, DAY) AS "ordered_since_signup2"
        FROM "order_items_big"
        LEFT JOIN "users_big" as users_big ON "order_items_big.user_id" = "users_big.id"
    )
    SELECT 
        ordered_since_signup - def.ten_days_ago - abc.ordered_since_signup2 as "days_since" FROM abc, def
    """

    expected_columns = {
        "users_big.created_at",
        "order_items_big.created_at",
        "def.ten_days_ago",
        "order_items_big.created_at2",
        "users_big.created_at2",
    }

    result = walk_for_columns(test_sql, "days_since")
    result_columns = {str(col) for col in result}

    assert result_columns == expected_columns, (
        f"Expected {expected_columns}, but got {result_columns}"
    )
