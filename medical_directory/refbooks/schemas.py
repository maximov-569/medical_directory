from drf_yasg import openapi

catalog_view_set_list = {
    "manual_parameters": [
        openapi.Parameter(
            "date",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description="Start date in the format YYYY-MM-DD. If specified, only reference books with versions that have a start date earlier or equal to the specified date will be returned.",
            example="2020-01-01",
        ),
    ],
    "responses": {
        200: openapi.Response(
            description="List of reference books",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "refbooks": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_STRING),
                                "code": openapi.Schema(type=openapi.TYPE_STRING),
                                "name": openapi.Schema(type=openapi.TYPE_STRING),
                            },
                        ),
                    )
                },
            ),
            examples={
                "application/json": {
                    "refbooks": [
                        {"id": "1", "code": "MS1", "name": "Example 1"},
                        {"id": "2", "code": "ICD-10", "name": "Example 2"},
                    ]
                }
            },
        )
    },
}

catalog_item_view_set_list = {
    "manual_parameters": [
        openapi.Parameter(
            "catalog_id",
            in_=openapi.IN_PATH,
            type=openapi.TYPE_STRING,
            description="Catalog ID",
            required=True,
        ),
        openapi.Parameter(
            "version",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description="Catalog version\n "
            "Reference book version. If not specified, the elements of the current version should be returned. The current version is the version whose start date is later than all other versions of the reference book, but not later than the current date.",
            example="1.0",
        ),
    ],
    "responses": {
        200: openapi.Response(
            description="List of elements",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "elements": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "code": openapi.Schema(type=openapi.TYPE_STRING),
                                "value": openapi.Schema(type=openapi.TYPE_STRING),
                            },
                        ),
                    )
                },
            ),
            examples={
                "application/json": {
                    "elements": [
                        {"code": "J00", "value": " ()"},
                        {"code": "J01", "value": " "},
                    ]
                }
            },
        )
    },
}

catalog_item_view_set_retrieve = {
    "manual_parameters": [
        openapi.Parameter(
            "catalog_id",
            in_=openapi.IN_PATH,
            type=openapi.TYPE_STRING,
            description="Catalog ID",
            required=True,
        ),
        openapi.Parameter(
            "version",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description="Catalog version\n "
            "Reference book version. If not specified, the elements of the current version should be returned. The current version is the version whose start date is later than all other versions of the reference book, but not later than the current date.",
            example="1.0",
        ),
        openapi.Parameter(
            "value",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description="Item value",
            example="()",
        ),
        openapi.Parameter(
            "code",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description="Item code",
            example="J00",
        ),
    ],
    "responses": {
        200: openapi.Response(
            description="Element",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "code": openapi.Schema(type=openapi.TYPE_STRING),
                    "value": openapi.Schema(type=openapi.TYPE_STRING),
                },
            ),
            examples={"application/json": {"code": "J00", "value": " ()"}},
        ),
        404: openapi.Response(
            description="Element not found",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={"status": openapi.Schema(type=openapi.TYPE_STRING)},
            ),
            examples={"application/json": {"status": "Element not found"}},
        ),
    },
}
