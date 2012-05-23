SEARCH_SET = ( 
              ( '$gt', '>' ),
              ( '$lt', '<' ),
              ( '$gte', '>=' ),
              ( '$lte', '<=' ),
              ( '$exists', 'true' ),
              ( '$ne', '!=' ),
              ( '$in', 'in' ),
              ( '$nin', 'not in' ),
              ( '$all', 'all' ),
              ( '$nor', 'NOR' ),
              ( '$or', 'OR' ),
              ( '$and', 'AND' ),
              ( '$not', 'NOT' ),
              ( '$type', 'Type' ),
              ( '$size', 'Size' ),
              ( '', 'Equal' ),
              ( '$orderby', 'Order By' ),
              ( '$max', 'Max' ),
              ( '$min', 'Min' ),
              )

CURSOR_FUNC = ( 
               ( 'count', 'count' ),
               ( 'limit', 'limit' ),
               ( 'skip', 'skip' ),
               ( 'sort', 'sort' ),
               ( 'group', 'group' ),
               )
