class WebsocketMessagePrefixesMixin:
    SERVER_MAX_LIMIT_OF_CONNECTIONS_PREFIX = "__server_exceeded_limit_of_connections"
    GAME_INIT_PREFIX = "__sapper_init_field_size"
    GAME_CELL_CLICK_PREFIX = "__sapper_cell_clicked"
    GAME_SERVER_RESPONSE_PREFIX = "__sapper_server_response_with_cell_info"
    GAME_DRAW_TABLE_PREFIX = "__sapper_draw_table_for_other_clients"
    GAME_TABLE_DELETE_PREFIX = "__sapper_game_table_delete"
    GAME_FINISH_PREFIX = "__sapper_game_finished"
    GAME_STARTED_PREFIX = "__sapper_game_started"

    @staticmethod
    def get_message_prefixes():
        prefixes = (value
                    for attribute, value in WebsocketMessagePrefixesMixin.__dict__.items()
                    if attribute.endswith("_PREFIX")
                    )
        return prefixes
