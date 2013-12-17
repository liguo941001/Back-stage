#coding: utf-8
# File: tango/jsontable.py

from flask import url_for
from datetime import datetime
from .gvars import db


def pre_process(meta_dict):
    for KEY, meta in meta_dict.iteritems():
        # print 'KEY:', KEY
        columns = meta['columns']
        actions = meta.get('actions', {})
    
        keys = []
        ## Lambda dict
        filterDict = {}
        accessorDict = {}
        linkDict = {}
        ## Static dict
        headDict = {}
        typeDict = {}
        sortableDict = {}
        
        DICTS = {
            'filter': filterDict,
            'accessor': accessorDict,
            'link': linkDict,
            'head': headDict,
            'type': typeDict,
            'sortable': sortableDict
        }
        # Build attribute dicts
        for column in columns:
            key = column['key']
            keys.append(key)
            
            fields = column.keys()
            for field, someDict in DICTS.iteritems():
                if field in fields:
                    someDict[key] = column[field]

        # Fill the sortable fields
        for _k in keys:
            if _k not in sortableDict:
                sortableDict[_k] = True
            if _k not in filterDict:
                filterDict[_k] = True

        meta['keys'] = keys
        meta['headDict'] = headDict
        meta['typeDict'] = typeDict
        meta['sortableDict'] = sortableDict
        meta['filterDict'] = filterDict
        meta['accessorDict'] = accessorDict
        meta['linkDict'] = linkDict
    


def resolve(accessor, record, k):
    if accessor is None:
        cell = getattr(record, k)
    elif callable(accessor):
        cell = accessor(record)
    else:
        cell = accessor # Static value
    return cell

    
def get_data(request, meta_dict, query=None):
    DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
    
    page = request.args.get('page', 1, type=int)
    perpage = request.args.get('perpage', 20)
    order = request.args.get('order', '')
    orderDirection = request.args.get('orderDirection', '')

    keys = meta_dict['keys']
    model = meta_dict['model']

    filterDict = meta_dict['filterDict']
    _accessorDict = meta_dict['accessorDict']
    _linkDict = meta_dict['linkDict']
    actions = meta_dict['actions']

    query = model.query if query is None else query
    # 1. Filter
    keyword = request.args.get('keyword', '').strip()
    if keyword:
        # 1. relationship字段无法进行ilike
        # 2. 此语句包含了检测一个字段是否为 relationship 字段的方法:
        #    isinstance(getattr(getattr(model, attr), 'property'), RelationshipProperty)
        filters  = []
        for attr in keys:
            ft = filterDict[attr]
            if callable(ft):
                # Custom filter
                filters.append(ft(keyword))
            elif ft is True:
                # Default filter
                filters.append(getattr(model, attr).ilike(u'%{0}%'.format(keyword)))
            elif ft is False:
                # Do not filter this field
                pass
            else:
                raise ValueError('Invalid filter: {0}'.format(ft))
        query = query.filter(db.or_(*filters))

        
    # 2. Order/Sort
    if order:
        criterion = getattr(model, order)
        if orderDirection == 'desc':
            criterion = criterion.desc()
        elif orderDirection == 'asc':
            criterion = criterion.asc()
        else:
            raise ValueError('Unexcepeted orderDirection: %s' % orderDirection)
            
        query = query.order_by(criterion)

    # 3. Calcute: count, page, pages, offset
    count = query.count()
    pages = (count+perpage-1) / perpage
    page = page if page < pages else pages # 当需要过滤时页码可能超范围
    # print 'count, page, pages:', count, page, pages
    offset = (page-1)*perpage if page >= 1 else 0
    records = query.limit(perpage).offset(offset).all()

    # 4. Get content from records
    oids = []
    rows = []
    for record in records:
        row = []
        for k in keys:
            cell = {}
            # Row.cell.v
            value = resolve(_accessorDict.get(k, None), record, k)
            if isinstance(value, datetime):
                value = value.strftime(DATETIME_FORMAT) if value is not None else ''
            cell['value'] = value
            # Row.cell.link
            func_l = _linkDict.get(k, None)
            if func_l is not None:
                cell['link'] = func_l(record)
            row.append(cell)

        # Record.ids
        oids.append(record.id)
        rows.append(row)

    # Generate link from endpoint for actions
    for action in actions.values():
        if 'endpoint' in action:
            action['link'] = url_for(action['endpoint'])
            action.pop('endpoint')
        
    # Static dict
    headDict = meta_dict['headDict']
    sortableDict = meta_dict['sortableDict']
    typeDict = meta_dict['typeDict']
    
    status =  'success'
    return {
        'status'       : status,
        'count'        : count,
        'page'         : page,
        'pages'        : pages,
        'keys'         : keys,
        'headDict'     : headDict,
        'sortableDict' : sortableDict,
        'typeDict'     : typeDict,
        'actions'      : actions,
        'oids'         : oids,
        'rows'         : rows,
    }
