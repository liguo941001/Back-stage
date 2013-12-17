
# Function: Pagination
iterPages = (current, total) ->
    pagination = [1]
    
    if (current-1) > 2
        pagination.push.apply pagination, [null, current-1, current]
    else if current == 3
        pagination.push.apply pagination, [2, 3]
    else if current == 2
        pagination.push 2

    if (total-current) > 2
        pagination.push.apply pagination, [current+1, null]
    else if (total-current) == 2
        pagination.push(current+1)

    if total != current
        pagination.push total
        
    return pagination

        
# Test function
console.log iterPages 3, 14


# Function: Main
initApp = (appName, ctrlName, jsonUrl,
    templateBaseUrl, templateToolbarLeft) ->

    tableApp = angular.module appName, []    
    tableApp.controller ctrlName, ['$scope', '$http', ($scope, $http)->
        defaultParams = {}
        $scope.actionMeta = {
            edit: {label:'编辑', icon: 'fa-edit', btn: 'btn-primary'},
            del: {label:'删除', icon: 'fa-trash-o', btn: 'btn-danger'},
        }
        $scope.tempToolbarLeft = templateToolbarLeft
        $scope.tempBaseUrl = templateBaseUrl

        # Function.1: Load Page
        $scope.loadPage = (params) ->
            return 0 if params.page == null
            params.page = 1 if params.page < 1
            
            console.log "loadPage.BEGIN:", params, defaultParams
            $.extend defaultParams, params
            console.log "loadPage.END:", defaultParams

            ($http.get jsonUrl, {params:defaultParams}).success (data) ->
                console.log "data:", data
                $scope.title = data.title
                # Dicts
                $scope.keys = data.keys
                $scope.headDict = data.headDict
                $scope.sortableDict = data.sortableDict
                $scope.typeDict = data.typeDict
                $scope.actions = data.actions
                # Raw data 
                $scope.rows = data.rows
                $scope.oids = data.oids
                $scope.count = data.count
                $scope.page = data.page
                $scope.targetPage = data.page
                $scope.pages = data.pages
                # Other
                console.log 'data.actions', data.actions
                $scope.canEdit = if 'edit' of data.actions then true else false
                $scope.canDel = if 'del' of data.actions then true else false
                $scope.pagination = iterPages data.page, data.pages
                # Row Selecting
                $scope.allSelected = false
                $scope.selected = false
                $scope.selectedCnt = 0
                $scope.selectedRows = (false for _ in [1..data.rows.length])

                console.log $scope.pagination, $scope.selected, $scope.allSelected

        # Function.2: Order By
        $scope.orderBy = (order) ->
            if $scope.order?
                $scope.orderDirection = if $scope.orderDirection == 'desc' then 'asc' else 'desc'
            else
                $scope.orderDirection = 'asc'

            $scope.order = order
            $scope.loadPage {
                page: $scope.page,
                order: order,
                orderDirection: $scope.orderDirection
            }
    
        # Function.3: Filter
        $scope.filterBy = (keyword) ->
            console.log keyword
            $scope.keyword = keyword
            $scope.loadPage {
                page: $scope.page,
                keyword: keyword
            }

        # Function.4: Selected
        $scope.selectRow = (idx) ->
            # Select or Unselect ALL
            if idx is -1
                if $scope.selectedCnt == $scope.rows.length
                    $scope.selectedRows = (false for _ in [1..$scope.rows.length])
                    $scope.selectedCnt = 0
                else
                    $scope.selectedRows = (true for _ in [1..$scope.rows.length])
                    $scope.selectedCnt = $scope.rows.length
            # Select or Unselect one row                    
            else                
                $scope.selectedRows[idx] = not $scope.selectedRows[idx]
                if $scope.selectedRows[idx] then $scope.selectedCnt += 1 else $scope.selectedCnt -= 1
                
            $scope.selected = if $scope.selectedCnt > 0 then true else false
            $scope.allSelected = if $scope.selectedCnt == $scope.rows.length then true else false


        # Function.6: Delete records
        $scope.del = () ->
            selectedIdxs = []
            selectedOids = []
            for i in [0..($scope.selectedRows.length-1)]
                if $scope.selectedRows[i]
                    selectedIdxs.push i
                    selectedOids.push $scope.oids[i]

            console.log selectedIdxs, selectedOids
            console.log $scope.actions.del.link, {oids: selectedOids.join(',')}            
            $.post $scope.actions.del.link, {oids: selectedOids.join(',')}, () ->
                $scope.loadPage {page:$scope.page}


        # Function.7: Goto page
        $scope.gotoPage = (targetPage) ->
            return if not targetPage?
            $scope.loadPage({page:targetPage})


        #### Init
        $scope.targetPage = 1
        $scope.loadPage {page:1}
    ]
    

    
# Function: Helper
initCurrentApp = (jsonUrl, templateToolbarLeft) ->
    initApp "tableApp", 'Ctrl', jsonUrl, "/static/partials/table.html", templateToolbarLeft
