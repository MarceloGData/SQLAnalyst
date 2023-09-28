#https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
import sys
sys.dont_write_bytecode = True

import os
os.system('color')

import warnings
warnings.filterwarnings("ignore")

from termcolor import colored, COLORS
from datetime import datetime
from anytree import Node, RenderTree
import pandas as pd

# <STACKS>
#https://www.geeksforgeeks.org/check-for-balanced-parentheses-in-python/
def validate_stacks(str, open_list, close_list):
    stack = []
    for i in str:
        if i in open_list:
            stack.append(i)
        elif i in close_list:
            pos = close_list.index(i)
            if ((len(stack) > 0) and
                (open_list[pos] == stack[len(stack)-1])):
                stack.pop()
            else:
                return False
    if len(stack) == 0:
        return True
    else:
        return False

def validate_stack(str, opening, closing):
    stack = []
    #implement change using indexes to do /* */ comments
    for i in str:
        if i == opening:
            stack.append(i)
        elif i == closing:
            if ((len(stack) > 0)):
                stack.pop()
            else:
                return False
    if len(stack) == 0:
        return True
    else:
        return False

def explode_contexts(str, opening, closing):
    if(not validate_stack(str, opening, closing)):
        raise Exception('Unbalanced stacks')
    
    str = opening + str + closing
    
    final_contexts = []

    stack_contexts = []

    stack_delimiters = []

    for i in str:
        if i == opening:
            stack_delimiters.append(i)
            stack_contexts.append('')

        for j in range(len(stack_contexts)):
            stack_contexts[j] += i

        if i == closing:
            if ((len(stack_delimiters) > 0)):
                stack_delimiters.pop()
                final_contexts.append(stack_contexts.pop())
            else:
                raise Exception('Unbalanced stacks')
            
    if len(stack_delimiters) == 0:
        return final_contexts
    else:
        raise Exception('Unbalanced stacks')


def main():
    query = '''
    -- comment  
    with w_max_day_table1 as (
        select 
            id,
            max([day]) as max_day 
        from schema_a.table1 
        where field in (select field from table2 join table2 on 1=1)
        group by id
    ),
    w_cte2 as (
        select 
            a.* 
        from schema_a.table1 as a
        inner join w_max_day_table1 as b
        --on a.id1 = b.id1 --SECOND COMMENT
        --	and a.id2 = b.id2
        on a.id = b.id
            and a.[day] = b.max_day
    )
    select * from w_cte2
    '''
    
    query_list = query.split('\n')

    clean_query_list = []
    pretty_query_list = []

    #dealing with -- comments
    for line in query_list:
        # line = line.replace('\t',' ')
        comment_line_list = line.split('--')
        print(comment_line_list)

        clean_query_list.append(comment_line_list[0])

        # if(comment_line_list[0].strip() != ''):
        temp_line = comment_line_list[0]#.strip()
        
        if(len(comment_line_list) > 1):
            for i in range(1, len(comment_line_list)):
                temp_line += colored('--' + comment_line_list[i],'green')

        pretty_query_list.append(temp_line)      

    
    print(colored('\n\n\t\t<< PRETTY >>\n', 'cyan'))
    for line in pretty_query_list:
        print(line)

    
    print(colored('\n\n\t\t<< CLEAN >>\n', 'cyan'))
    for line in clean_query_list:
        print(line)

    inline_query = ''
    for line in clean_query_list:
        inline_query += ' ' + line

    inline_query = inline_query.replace('\t', ' ').replace('\n', ' ')

    while ('  ' in inline_query):
        inline_query = inline_query.replace('  ', ' ')

    
    print(colored('\n\n\t\t<< INLINE >>\n', 'cyan'))
    print(inline_query)

    
    print(colored('\n\n\t\t<< CONTEXTS >>\n', 'cyan'))
    
    print('validate_stacks with [\'(\'] and [\')\']', validate_stacks(inline_query, ['('], [')']))
    print('validate_stack with ( and )', validate_stack(inline_query, '(', ')'))
    
    query_to_explode = inline_query
    # query_to_explode = '\n'.join(clean_query_list)

    contexts = explode_contexts(query_to_explode, '(', ')')

    queries = []
    for c in contexts:
        print('\n\n' + c + '\n')

        if('select' in c):
            queries.append({
                'id':len(queries),
                'parent_id':-1,
                'node':None,
                'query':c
            })
    
    root = None
    for q in queries:
        #print('\n\n' + str(q) + '\n')
        if('('+query_to_explode+')' == q['query']):
            root = q
            break

    if(type(root) == type(None)):
        raise Exception('root is None')
    
    # print('root', root)

    for q in queries:
        if(q['parent_id'] == -1 and q != root):
            for q2 in queries:
                if(q['query'] in q2['query'] and q['query'] != q2['query']):
                    q['parent_id'] = q2['id']
                    break

        # print('\n\n',q,'\n')
    
    
    print(colored('\n\n\t\t<< QUERIES >>\n', 'cyan'))

    root_node = Node(root['id'])

    # print(root_node)
    nodes = [root_node]
    for q in queries:
        if(q['id'] == root['id']):
            node = root_node
        else:
            node = Node(q['id'])

        nodes.append(node)
        q['node'] = node
        
    # for q in queries:
    #     print(q)

    # print(nodes)

    for i in range(len(queries)):
        for q in queries:
            if(q['id'] == queries[i]['parent_id']):
                queries[i]['node'].parent = q['node']
                # print(queries[i]['id'],q['id'])
                # print('aqui')
                break
    
    for q in queries:
        print('\n\n',q,'\n')

    print(colored('\n\n\t\t<< QUERY TREE >>\n', 'cyan'))
    
    for pre, fill, node in RenderTree(root_node):
        print("%s%s" % (pre, node.name))

    #print(query)

    #print(COLORS)

    #var = colored('hello', 'red') + colored(' world', 'magenta') + ' bn'
    #print(var)

    print(colored('\n\n\t\t<< DATAFRAME >>\n', 'cyan'))
    for q in queries:
        q['path'] = str(q['node'])[6:-2]
        q['query'] = str(q['query'])[1:-1].strip()
    df = pd.DataFrame.from_records(queries)
    df = df.drop(columns=['node'])

    print(df)
    df['query_w_tokens'] = ''
    df['froms'] = ''
    df['from_joins'] = ''
    df['froms_distinct'] = ''

    print(colored('\n\n\t\t<< LAST >>\n', 'cyan'))
    for i in range(len(df)):
        query = df['query'][i]
        df_child_queries = df[df['parent_id'] == df['id'][i]].reset_index(drop=True)

        for j in range(len(df_child_queries)):
            if(df_child_queries['query'][j] in query):
                query = query.replace(df_child_queries['query'][j], '{' + str(df_child_queries['id'][j]) + '}')

        # print(query)
        # print(df_child_queries)

        df['query_w_tokens'][i] = query

        #doesnt support 'from a, b'
        froms = ''
        from_joins = ''
        query_array = query.lower().split('from')
        print(query_array)

        if(len(query_array) > 1):
            froms += query_array[1].strip().split(' ')[0]+','
            from_joins += query_array[1].strip().split(' ')[0]

        joins_list = [
            'inner join', 
            'left join',
            'left outer join', 
            'right join', 
            'right outer join',
            'full join', 
            'full outer join',
            'cross join',
            'join'
        ]
        froms_just_joins = ''
        for j in joins_list:
            query_array = query.lower().split(j)
            if(len(query_array) > 1):
                for q in query_array[1:]:
                    q0 = q.strip().split(' ')[0].replace(',','')
                    if(not q0 in froms_just_joins):
                        froms_just_joins +=  q0 + ','
                        from_joins += ' ' + j + ' ' + q0
        
        froms += froms_just_joins
        if(len(froms) > 0):
            froms = froms[:-1]

        df['froms'][i] = froms
        df['froms_distinct'][i] = ','.join(list(set(froms.split(','))))
        df['from_joins'][i] = from_joins

        #possible aliases

    print(df)

    print('\n\n')
    for a in df['froms_distinct']:
        print(a)

    print('\n\n')
    for a in df['froms']:
        print(a)

    print('\n\n')
    for a in df['from_joins']:
        print(a)

    # print('\n\n')
    # for a in df['query_w_tokens']:
    #     print(a)


if __name__ == "__main__":
    print(datetime.now())
    
    main()

    print(datetime.now())